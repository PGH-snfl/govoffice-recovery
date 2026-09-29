"""Remove registered authoring aids, preserving document controls and bound text."""
from copy import deepcopy
import xml.etree.ElementTree as ET


def text(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')


def clean_rendered_form(root, ps, manifest, field_log):
    policy = manifest['render_policy']
    parents = {id(c): p for p in root.iter() for c in p}
    indices = {id(p): i for i, p in enumerate(ps)}
    bound = {f.get('input_index',int(f['field_id'][1:])) for f in field_log}
    protected = set(manifest.get('protected_design_indices', []))
    cleared = set()
    for topic in manifest['topics']:
        for field in topic['fields']:
            if field['index'] in bound:
                cleared.update(i for i in field.get('clear_indices', []) if i not in bound)
    for i in cleared - protected:
        for t in ps[i].findall('TEXT'):
            for c in list(t.findall('CHAR')):
                t.remove(c)
    headings = {t['start'] for t in manifest['topics']}
    headings.update(s['start'] for t in manifest['topics'] for s in t.get('subsections', []))
    guide_ids = {i for g in manifest['guide_groups'] for i in g}
    shapes = {s.get('Id'): s for s in root.iter('CHARSHAPE')}
    for table in list(root.iter('TABLE')):
        cells = list(table.iter('P'))
        if cells and indices[id(cells[0])] in guide_ids:
            parents[id(table)].remove(table)
    # Remove blue instructional runs, not newly inserted field values/headings.
    for p in root.iter('P'):
        index = indices[id(p)]
        if index in bound | protected:
            continue
        for t in p.findall('TEXT'):
            color = int(shapes.get(t.get('CharShape'), {}).get('TextColor', '0'))
            if (color >> 16 & 255) > 120 and (color & 255) < 100 and index not in headings:
                for c in list(t):
                    if c.tag == 'CHAR':
                        t.remove(c)
        # Inline remarks in mixed-colour headings are preserved in guide MD,
        # but not shown as instructions in the generated form.
        if index in headings:
            for t in p.findall('TEXT'):
                for c in t.findall('CHAR'):
                    if c.text and '※' in c.text:
                        c.text = c.text.split('※', 1)[0].rstrip()
    section = root.find('BODY/SECTION')
    cutoff = policy.get('remove_before', 0)
    if section is not None and cutoff:
        removed = [p for p in list(section) if p.tag == 'P' and indices[id(p)] < cutoff]
        # Hancom only applies the section definition in its leading paragraph.
        # A blank page-hiding/control paragraph still precedes visible headings.
        keep = [p for p in list(section) if p.tag == 'P' and p not in removed]
        if keep:
            target = keep[0].find('TEXT')
            if target is None:
                target = ET.SubElement(keep[0], 'TEXT', {'CharShape':'0'})
            if target is not None:
                controls = [deepcopy(c) for p in removed for t in p.findall('TEXT') for c in t
                            if c.tag in {'SECDEF', 'COLDEF', 'HEADER', 'FOOTER', 'PAGENUM', 'PAGEHIDING'}]
                for n, c in enumerate(controls):
                    target.insert(n, c)
            for p in removed:
                section.remove(p)
            # The cover's old hard page break followed the deleted instruction
            # pages. Leaving it here creates a completely blank first page.
            for p in keep:
                p.attrib.pop('PageBreak', None)
                if text(p).strip() or list(p.iter('TABLE')):
                    break
    # Clear an outdated static TOC; never fabricate page numbers.
    for a, b in policy.get('remove_ranges', []):
        if section is not None:
            for p in list(section):
                if p.tag == 'P' and a <= indices[id(p)] <= b:
                    if any(indices[id(q)] in bound for q in p.iter('P')):
                        raise ValueError('입력 문단이 포함된 범위는 삭제할 수 없습니다.')
                    section.remove(p)
    if section is not None and not policy.get('preserve_layout'):
        # Collapse the leading control-only paragraph into the cover anchor.
        # Otherwise its empty line can push a nearly page-high cover off page 1.
        while len(section) > 1:
            first, second = section[0], section[1]
            if first.tag != 'P' or second.tag != 'P' or text(first).strip() or list(first.iter('TABLE')):
                break
            if indices.get(id(first)) in bound:
                break
            target = second.find('TEXT')
            if target is None:
                target = ET.SubElement(second, 'TEXT', {'CharShape':'0'})
            controls = [c for t in first.findall('TEXT') for c in t if c.tag != 'CHAR']
            for n,c in enumerate(controls):
                target.insert(n,c)
            section.remove(first)
        for p in list(section):
            if p.tag == 'P' and not text(p).strip() and all(c.tag == 'CHAR' for t in p for c in t):
                section.remove(p)
    # Permit tall tables to continue on subsequent pages. Keep borders, widths,
    # margins, numbering and original cell structure.
    cover_table = next(root.iter('TABLE'), None)
    for table in root.iter('TABLE'):
        if policy.get('preserve_layout'):
            continue
        table.set('PageBreak', 'Cell')
        pos = table.find('SHAPEOBJECT/POSITION')
        if pos is not None:
            # The nearly page-high cover needs flowing placement. Other tables
            # follow their text anchors to avoid colliding with nearby headings.
            pos.set('TreatAsChar', 'false' if table is cover_table else 'true')
            pos.set('FlowWithText', 'true')
            pos.set('AllowOverlap', 'false')
    # Original timeline bars are formatting examples, not actual task progress.
    # Clear those graphic cell borders and let validated marker fields draw the plan.
    scheduled = set(policy.get('schedule_cells', []))
    for cell in root.iter('CELL'):
        cp = list(cell.iter('P'))
        if cp and indices.get(id(cp[0])) in scheduled:
            cell.set('BorderFill', '1')
    # Source field styles can be blue/example-only. New text uses black and the
    # original form's required 12pt body / 8pt table typography.
    shape_list = root.find('.//CHARSHAPELIST')
    table_ids = {id(p) for t in root.iter('TABLE') for p in t.iter('P')}
    cache = {}
    if shape_list is not None and shapes:
        next_id = max(map(int, shapes)) + 1
        for p in root.iter('P'):
            if indices.get(id(p)) not in bound:
                continue
            for t in p.findall('TEXT'):
                old = t.get('CharShape')
                height = (int(shapes.get(old,{}).get('Height',1200)) if policy.get('preserve_layout')
                          else 800 if id(p) in table_ids else 1200)
                key = (old, height)
                if old not in shapes:
                    continue
                if key not in cache:
                    new = deepcopy(shapes[old])
                    new.set('Id', str(next_id)); new.set('TextColor', '0'); new.set('Height', str(height))
                    shape_list.append(new); cache[key] = str(next_id); next_id += 1
                t.set('CharShape', cache[key])
        shape_list.set('Count', str(len(shape_list)))
    output_ps = list(root.iter('P'))
    output_indices = {id(p): i for i, p in enumerate(output_ps)}
    log = []
    for entry in field_log:
        original = int(entry['field_id'][1:])
        if id(ps[original]) not in output_indices:
            raise ValueError('안내 정리 중 입력 문단이 삭제되었습니다: ' + entry['field_id'])
        log.append({**entry, 'output_index': output_indices[id(ps[original])]})
    return log
