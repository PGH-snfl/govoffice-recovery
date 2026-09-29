"""Two deterministic document-wide font profiles for written content.

Select from source input slots, never from generated response text. Each slot
gets one vote, so a long response or a later partial render cannot change the
choice. Fixed labels, title strips and original source styles are untouched.
"""
from collections import Counter, defaultdict
from copy import deepcopy
import xml.etree.ElementTree as ET
import re


def font_group(paragraph, parents):
    node = parents.get(id(paragraph))
    while node is not None:
        if node.tag == 'CELL':
            return 'table'
        node = parents.get(id(node))
    return 'body'


def document_font_profiles(root, manifest):
    parents = {id(c): p for p in root.iter() for c in p}
    ps = list(root.iter('P'))
    shapes = {s.get('Id'): s for s in root.iter('CHARSHAPE')}
    faces = {f.get('Lang'): {x.get('Id'): x.get('Name') for x in f.findall('FONT')}
             for f in root.iter('FONTFACE')}
    slots = {'table': [], 'body': []}
    for topic in manifest['topics']:
        for field in topic['fields']:
            if field.get('write_blocked'):
                continue
            paragraph = ps[field['index']]
            run = paragraph.find('TEXT')
            shape = shapes.get(run.get('CharShape')) if run is not None else None
            if shape is not None and shape.find('FONTID') is not None:
                slots[font_group(paragraph, parents)].append(shape)
    profiles = {}
    for group, candidates in slots.items():
        if not candidates:
            continue
        family = Counter(s.find('FONTID').get('Hangul', '0') for s in candidates).most_common(1)[0][0]
        same_family = [s for s in candidates if s.find('FONTID').get('Hangul', '0') == family]
        regular = [s for s in same_family if 1000 <= int(s.get('Height', '0')) <= 1200
                   and s.find('BOLD') is None and s.find('ITALIC') is None]
        usable = regular or [s for s in same_family if 1000 <= int(s.get('Height', '0')) <= 1200] or same_family
        counts = Counter(s.get('Id') for s in usable)
        base = shapes[counts.most_common(1)[0][0]]
        profile = deepcopy(base)
        height = int(profile.get('Height', '1100'))
        profile.set('Height', str(height if 1000 <= height <= 1200 else (1000 if group == 'table' else 1100)))
        profile.set('TextColor', '0')
        for tag in ('BOLD', 'ITALIC', 'UNDERLINE', 'STRIKEOUT', 'OUTLINE', 'SHADOW', 'SUPERSCRIPT', 'SUBSCRIPT'):
            for item in list(profile.findall(tag)):
                profile.remove(item)
        # Language-specific font IDs differ, even for the same typeface.
        # Resolve each by family name rather than copying the Hangul ID.
        family_name = faces.get('Hangul', {}).get(family)
        font_ids = profile.find('FONTID')
        if family_name:
            for language, mapping in faces.items():
                matching = next((key for key, name in mapping.items() if name == family_name), None)
                if matching is not None:
                    font_ids.set(language, matching)
        profiles[group] = profile
    return profiles


def resolve_font_profile(profiles, *, field_id=None, index=None, group='body'):
    """Resolve by actual source position before falling back to legacy groups."""
    if not profiles:
        return None
    if field_id in profiles.get('by_field', {}):
        return profiles['by_field'][field_id]
    if index in profiles.get('by_index', {}):
        return profiles['by_index'][index]
    return profiles.get(group)


def flowing_font_profiles(root, manifest):
    """Follow real body formatting changes; unspecified tables inherit body.

    Empty slot formatting, headings and guidance typography are not changes to
    the body. Actual prose or a literal font instruction can establish a change.
    Table-specific instructions/samples stay local and cannot change later body.
    The entire plan is made from the source before any response is written.
    """
    parents = {id(c): p for p in root.iter() for c in p}
    ps = list(root.iter('P'))
    indices = {id(p): i for i, p in enumerate(ps)}
    shapes = {s.get('Id'): s for s in root.iter('CHARSHAPE')}
    faces = {f.get('Lang'): {x.get('Id'): x.get('Name') for x in f.findall('FONT')}
             for f in root.iter('FONTFACE')}
    fields = [f for t in manifest['topics'] for f in t['fields'] if not f.get('write_blocked')]
    by_index = {f['index']: f for f in fields}
    protected = set(manifest.get('protected_design_indices', []))
    guides = set(manifest.get('clear_guide_indices', []))
    headings = {t['start'] for t in manifest['topics']}
    def ancestor(node, tag):
        while node is not None:
            if node.tag == tag:return node
            node = parents.get(id(node))
    def own(p):
        return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')
    def regular(shape, family_name=None):
        result = deepcopy(shape)
        result.set('TextColor', '0')
        for tag in ('BOLD','ITALIC','UNDERLINE','STRIKEOUT','OUTLINE','SHADOW','SUPERSCRIPT','SUBSCRIPT'):
            for child in list(result.findall(tag)):result.remove(child)
        font = result.find('FONTID')
        if font is not None:
            name = family_name or faces.get('Hangul', {}).get(font.get('Hangul'))
            if name:
                for language, mapping in faces.items():
                    match = next((key for key, value in mapping.items() if value == name), None)
                    if match is not None:font.set(language, match)
        return result
    def sample(i, p):
        text = own(p).strip()
        if i in guides | protected | headings or not text or len(text) < 8:return None
        if re.match(r'^(?:\d+(?:[-.]\d+)*[.)]|\([0-9]+\)|[가-하][.)]|[o○◦※*]|[-•])\s*', text):return None
        if text.endswith((':','：')) or re.search(r'작성\s*요령|작성\s*방법|\(예\)|예시|글꼴|서체|폰트', text):return None
        field = by_index.get(i)
        if field and (field.get('insert_after') or field.get('role') == 'personal' or field.get('kind') in {'factual_cell','schedule_marker'}):return None
        # A table's labels are not typography instructions. Only a genuine
        # bound prose paragraph can establish its own table font implicitly.
        if ancestor(p,'CELL') is not None and not field:return None
        candidates=[]
        for run in p.findall('TEXT'):
            value=''.join(c.text or '' for c in run.findall('CHAR')).strip()
            shape=shapes.get(run.get('CharShape'))
            if shape is not None and shape.find('FONTID') is not None and value:
                if 800 <= int(shape.get('Height','0')) <= 1600 and shape.get('TextColor','0') == '0':
                    candidates.append((len(value),shape))
        return regular(max(candidates,key=lambda item:item[0])[1]) if candidates else None
    names = sorted(set(faces.get('Hangul', {}).values()), key=len, reverse=True)
    def directives(text):
        # Read literal formatting data, never execute instructions in a form.
        result=[]
        for clause in re.split(r'[;\n]|(?=본문(?:\s|은|의|:))|(?=표\s*(?:안|내|내용))',text):
            if not re.search(r'본문|표\s*(?:안|내|내용)|글꼴|글씨체|서체|폰트',clause):continue
            if re.search(r'아닌|아니라|사용하지|금지',clause):continue
            matches=[]
            for name in names:
                if name in clause and not any(name in longer for longer in matches):matches.append(name)
            # Do not guess between two alternative fonts in one instruction.
            if len(matches)>1:continue
            name=matches[0] if matches else None
            size=re.search(r'(\d{1,2}(?:\.\d+)?)\s*(?:pt|포인트)',clause,re.I)
            if name is None and size is None:continue
            target='table' if re.search(r'표\s*(?:안|내|내용)',clause) else 'body'
            result.append((target,name,float(size.group(1)) if size else None))
        return result
    def override(base, rule):
        _, name, size = rule
        result = regular(base, name)
        if size is not None and 8 <= size <= 24:result.set('Height', str(round(size*100)))
        return result
    legacy = document_font_profiles(root, manifest)
    default = legacy.get('body')
    if default is None:default = legacy.get('table')
    if default is None:return {}
    samples={i:s for i,p in enumerate(ps) if (s:=sample(i,p)) is not None}
    first_body=next((s for i,s in samples.items() if font_group(ps[i],parents)=='body'),None)
    if first_body is not None:default=first_body
    # Explicit table formatting is local to the actual table, including nested
    # tables. A directive outside a table applies to the next writable table.
    writable_tables={ancestor(ps[f['index']],'TABLE') for f in fields}
    writable_tables.discard(None)
    table_rules={};table_samples={};body_rules={}
    # An existing value in a writable cell is strongest evidence of the table's
    # content font. When it has only input markers, their original style still
    # beats the surrounding body font. Use one source style per table.
    table_inputs=defaultdict(list)
    table_slots=defaultdict(list)
    for field in fields:
        if field.get('insert_after'):continue  # An anchor heading is not an input cell.
        i=field['index'];p=ps[i];table=ancestor(p,'TABLE')
        if table is None or i in guides | protected:continue
        value=own(p).strip()
        substantive=(len(value)>=2 and value!=field.get('slot_marker') and
                     bool(re.search(r'[가-힣A-Za-z0-9]',value)) and
                     not re.search(r'확인\s*필요|작성\s*요령|작성\s*방법',value))
        candidates=[]
        for run in p.findall('TEXT'):
            run_text=''.join(c.text or '' for c in run.findall('CHAR')).strip()
            shape=shapes.get(run.get('CharShape'))
            if (shape is not None and shape.find('FONTID') is not None
                    and 800<=int(shape.get('Height','0'))<=1600
                    and shape.get('TextColor','0')=='0'):
                candidates.append((len(run_text) if substantive else 0,shape))
        if candidates:
            _,shape=max(candidates,key=lambda item:item[0])
            target=table_inputs if substantive else table_slots
            target[table].append((shape.get('Id'),len(value),shape))
    for table,choices in {**table_slots,**table_inputs}.items():
        counts=Counter(shape_id for shape_id,_,_ in choices)
        winner=max(choices,key=lambda item:(counts[item[0]],item[1]))[2]
        table_samples[table]=regular(winner)
    for i,p in enumerate(ps):
        table=ancestor(p,'TABLE')
        for rule in directives(own(p)):
            if rule[0]=='body':body_rules[i]=rule
            else:
                target=table if table in writable_tables else next((t for t in root.iter('TABLE')
                    if t in writable_tables and min((indices[id(q)] for q in t.iter('P')),default=-1)>i),None)
                if target is not None:table_rules[target]=rule
        if table is not None and i in samples:table_samples.setdefault(table,samples[i])
    active=regular(default);positions={}
    for i,p in enumerate(ps):
        if i in body_rules:active=override(active,body_rules[i])
        if font_group(p,parents)=='body' and i in samples:active=samples[i]
        chosen=active
        table=ancestor(p,'TABLE')
        while table is not None:
            if table in table_rules:
                chosen=override(active,table_rules[table]);break
            if table in table_samples:
                chosen=table_samples[table];break
            table=ancestor(parents.get(id(table)),'TABLE')
        positions[i]=deepcopy(chosen)
    return {'body':regular(default), 'by_index':positions,
            'by_field':{f['id']:positions[f['index']] for f in fields}}
