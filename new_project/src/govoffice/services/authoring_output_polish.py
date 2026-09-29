"""Source-aware finishing of generated drafts, without changing the source form.

Only explicit instruction/example zones are removed. Bound values and design
title strips are never candidates for deletion. All decisions use the source,
before instruction text is blanked, and logs are indexed after finishing.
"""
from copy import deepcopy
import re
import xml.etree.ElementTree as ET


def own(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')


def normalized_body_height(height):
    height = int(height)
    return height if 1000 <= height <= 1200 else 1100


class OutputPolisher:
    def __init__(self, root, ps, manifest):
        self.root, self.ps, self.manifest = root, ps, manifest
        self.parents = {id(c): p for p in root.iter() for c in p}
        self.indices = {id(p): i for i, p in enumerate(ps)}
        self.texts = [own(p) for p in ps]
        self.bound = {f['index'] for t in manifest['topics'] for f in t['fields']}
        self.protected = set(manifest.get('protected_design_indices', []))
        self.guides = set(manifest.get('clear_guide_indices', []))
        self.remove = []
        self.unwrap = []
        self.mirrors = []
        self.headings = []
        self.compact_rows = []
        self.cover_paragraphs = []
        for i, p in enumerate(ps):
            if i not in self.protected and re.match(r'^\s*(?:\d+(?:[-.]\d+)*\.|\([0-9]+\)|[가-하]\.)\s*\S', self.texts[i]):
                self.headings.append(p)
        tables = list(root.iter('TABLE'))
        for table in tables:
            inside = {self.indices[id(p)] for p in table.iter('P')}
            first = min(inside, default=0)
            # Explicitly labelled instruction tables, including nested examples.
            if not inside & (self.bound | self.protected):
                # Guide labels may follow table headers or explanatory text.
                # Inspect the complete table so its shell is removed too.
                table_text = ''.join(self.texts[i] for i in sorted(inside))
                if '작성요령' in re.sub(r'\s+', '', table_text):
                    self.remove.append(table)
                    continue
                # An unbound nested example table immediately following a
                # confirmed '(예)' instruction belongs to that example block.
                before = [i for i in range(max(0, first-4), first) if self.texts[i].strip()]
                if (self.ancestor(self.parents.get(id(table)), 'CELL') is not None and before
                        and before[-1] in self.guides and '(예)' in self.texts[before[-1]]):
                    self.remove.append(table)
            # Oversized one-cell wrappers prevent their inner table from paging.
            cells = table.findall('ROW/CELL')
            if len(cells) == 1 and cells[0].find('.//TABLE') is not None:
                direct = cells[0].findall('PARALIST/P')
                size = table.find('SHAPEOBJECT/SIZE')
                if size is not None and int(size.get('Height', '0')) > 65000 and not any(own(p).strip() for p in direct):
                    self.unwrap.append((table, direct))
                    self.cover_paragraphs.extend(p for p in table.iter('P') if len(own(p)) > 90)
            # Only drawings explicitly introduced as an example are cleared.
            if first >= 2 and any(i in self.guides and re.search(r'예\s*[:：]', self.texts[i])
                                  for i in range(max(0, first-3), first)):
                for drawing in table.iter('CONTAINER'):
                    if not any(self.indices.get(id(p)) in self.bound for p in drawing.iter('P')):
                        self.remove.append(drawing)
                        row = self.ancestor(drawing, 'ROW')
                        if row is not None and row not in self.compact_rows:
                            self.compact_rows.append(row)
        self._find_mirrors(tables)

    def ancestor(self, node, tag):
        while node is not None:
            if node.tag == tag:
                return node
            node = self.parents.get(id(node))

    def _find_mirrors(self, tables):
        """Mirror named summary fields into their unbound cover counterparts.

        Do not guess a project name, business identifier, budget, or translation.
        Korean title rows have a distinct '국문' cell; English stays untouched.
        """
        fields = [f for t in self.manifest['topics'] for f in t['fields']]
        def in_summary(field):
            table = self.ancestor(self.ps[field['index']], 'TABLE')
            title = ''.join(own(p) for p in list(table.iter('P'))[:2]) if table is not None else ''
            return '요약문' in re.sub(r'\s+', '', title)
        for label in ('연구개발과제명', '사업명', '내역사업명'):
            sources = [f for f in fields if re.sub(r'\s+', '', f.get('label', '').split('/')[0]) == label]
            if len(sources) > 1:
                sources = [f for f in sources if in_summary(f)]
            if len(sources) != 1:
                continue
            source = sources[0]
            source_table = self.ancestor(self.ps[source['index']], 'TABLE')
            for table in tables:
                if table is source_table or source_table in list(table.iter('TABLE')):
                    continue
                for row in table.findall('ROW'):
                    cells = row.findall('CELL')
                    for n, cell in enumerate(cells[:-1]):
                        value = re.sub(r'\s+', '', ''.join(own(p) for p in cell.findall('PARALIST/P')))
                        if value != label and not (label == '내역사업명' and value == '내역사업명(해당시작성)'):
                            continue
                        target = cells[n+1]
                        if label == '연구개발과제명':
                            if ''.join(own(p) for p in target.iter('P')).strip() != '국문' or n+2 >= len(cells):
                                continue
                            target = cells[n+2]
                        candidates = target.findall('PARALIST/P')
                        if len(candidates) != 1:
                            continue
                        if re.sub(r'\s+', '', own(candidates[0])) == label:
                            continue  # repeated/merged label, not a value cell
                        index = self.indices[id(candidates[0])]
                        if index < source['index'] and index not in self.bound | self.protected:
                            self.mirrors.append((source['id'], index))

    def finish(self, refs, fields):
        # Copy only rendered values; '확인 필요' factual slots stay empty, just
        # like the corresponding summary. Never copy an unrendered AI proposal.
        by_id = {entry['field_id']: (paragraphs, parts) for entry, paragraphs, parts in refs}
        for source, index in self.mirrors:
            if source not in by_id:
                continue
            paragraphs, parts = by_id[source]
            p = self.ps[index]
            for run in p.findall('TEXT'):
                for c in list(run.findall('CHAR')):
                    run.remove(c)
            run = p.find('TEXT')
            if run is None:
                run = ET.SubElement(p, 'TEXT', {'CharShape': '0'})
            text = ' '.join(v for v in parts if v.strip())
            ET.SubElement(run, 'CHAR').text = text
            field_id = f'P{index:04d}'
            fields[field_id] = {'id': field_id, 'role': 'personal', 'label': '표지·요약 일치'}
            refs.append(({'field_id': field_id, 'value': text, 'source': 'program', 'input_index': index,
                          'mirrored_from': source}, [p], [text]))
        for node in self.remove:
            parent = self.parents.get(id(node))
            if parent is not None and node in list(parent):
                parent.remove(node)
        # Removing an example flowchart must also release its 30 cm row height.
        # Keep the real year labels and blank input cell; do not fabricate a plan.
        for row in self.compact_rows:
            cells = row.findall('CELL')
            if any(c.get('RowSpan', '1') != '1' for c in cells):
                continue
            if any(self.indices.get(id(p)) in self.bound for c in cells for p in c.iter('P')):
                continue
            for cell in cells:
                cell.set('Height', str(min(4000, int(cell.get('Height', '4000')))))
            table = self.ancestor(row, 'TABLE')
            size = table.find('SHAPEOBJECT/SIZE') if table is not None else None
            if size is not None:
                size.set('Height', str(sum(max([int(c.get('Height', '0')) for c in r.findall('CELL')] + [0])
                                          for r in table.findall('ROW'))))
        for table, children in self.unwrap:
            host = self.ancestor(table, 'P')
            parent = self.parents.get(id(host))
            run = self.parents.get(id(table))
            if parent is None or run is None:
                continue
            position = list(parent).index(host)
            run.remove(table)
            for offset, child in enumerate(children, 1):
                parent.insert(position + offset, child)
        # Remove empty remnants of cleared guides, but retain bound anchors,
        # section controls and at least one paragraph in every cell.
        parents = {id(c): p for p in self.root.iter() for c in p}
        for i in self.guides - self.bound - self.protected:
            p = self.ps[i]
            parent = parents.get(id(p))
            if parent is not None and not own(p).strip() and not any(c.tag != 'CHAR' for t in p.findall('TEXT') for c in t):
                if len(parent.findall('P')) > 1:
                    parent.remove(p)
        self._paragraphs(refs, parents)
        self._flow_tables()

    def _paragraphs(self, refs, parents):
        shape_list = self.root.find('.//PARASHAPELIST')
        if shape_list is None:
            return
        shapes = {s.get('Id'): s for s in shape_list}
        next_id = max([int(k) for k in shapes] + [-1]) + 1
        cache = {}
        written = {id(p) for _, paragraphs, _ in refs for p in paragraphs}
        def apply(p, heading=False, keep_next=False):
            nonlocal next_id
            old = p.get('ParaShape')
            if old not in shapes:
                return
            key = (old, heading, keep_next)
            if key not in cache:
                shape = deepcopy(shapes[old]); shape.set('Id', str(next_id))
                shape.attrib.update(KeepWithNext='true' if heading or keep_next else 'false', KeepLines='false', SnapToGrid='false')
                if not heading:
                    shape.attrib.update(Align='Justify', PageBreakBefore='false')
                    margin = shape.find('PARAMARGIN')
                    if margin is None:
                        margin = ET.SubElement(shape, 'PARAMARGIN')
                    margin.attrib.update(Left='0', Right='0', Indent='0', Prev='0', Next='350', LineSpacingType='Percent', LineSpacing='150')
                shape_list.append(shape); cache[key] = str(next_id); next_id += 1
            p.set('ParaShape', cache[key])
        for p in self.headings:
            if id(p) in parents and id(p) not in written:
                apply(p, True)
                # Empty spacer paragraphs between heading and body must also
                # stay with the following text, not defeat keep-with-next.
                parent = parents[id(p)]
                for nxt in list(parent)[list(parent).index(p)+1:]:
                    if nxt.tag != 'P' or own(nxt).strip() or any(c.tag != 'CHAR' for t in nxt.findall('TEXT') for c in t):
                        break
                    apply(nxt, True)
        # Legal declarations must not leave their first line on the prior page.
        for p in self.cover_paragraphs:
            old = p.get('ParaShape')
            if id(p) not in parents or old not in shapes:
                continue
            shape = deepcopy(shapes[old]); shape.set('Id', str(next_id)); next_id += 1
            shape.set('KeepLines', 'true')
            shape_list.append(shape); p.set('ParaShape', shape.get('Id'))
        for _, paragraphs, parts in refs:
            for number, p in enumerate(paragraphs):
                node = parents.get(id(p)); in_cell = False
                while node is not None:
                    if node.tag == 'CELL': in_cell = True; break
                    node = parents.get(id(node))
                if not in_cell:
                    value = parts[number].strip()
                    # A font change can push an authored numbered subheading
                    # onto the last line of a page. Keep its following prose.
                    subheading = (number + 1 < len(paragraphs) and len(value) <= 60
                                  and bool(re.match(r'^\d{1,2}[.)]\s+\S', value))
                                  and not value.endswith(('.', '!', '?', '다', '함')))
                    apply(p, keep_next=subheading)
        shape_list.set('Count', str(len(shape_list)))

    def _flow_tables(self):
        parents = {id(c): p for p in self.root.iter() for c in p}
        for table in self.root.iter('TABLE'):
            node = parents.get(id(table)); nested = False
            while node is not None:
                if node.tag == 'CELL': nested = True; break
                node = parents.get(id(node))
            size = table.find('SHAPEOBJECT/SIZE')
            if nested or size is None or int(size.get('Height', '0')) < 25000:
                continue
            table.set('PageBreak', 'Cell')
            obj = table.find('SHAPEOBJECT'); obj.set('TextWrap', 'TopAndBottom')
            pos = obj.find('POSITION')
            if pos is not None:
                pos.attrib.update(TreatAsChar='false', FlowWithText='true', AllowOverlap='false', VertRelTo='Para', VertAlign='Top', VertOffset='0')
            size.set('Protect', 'false')
