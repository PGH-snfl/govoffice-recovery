"""Source guide tables plus blue annotations; never copy surrounding body text."""
import json
import re


def blue_annotations(root, ps, table_ids, *, excluded=None):
    """Read direct CHAR runs only, so black text and nested tables cannot leak."""
    shapes = set()
    for shape in root.iter('CHARSHAPE'):
        color = int(shape.get('TextColor', '0'))
        # HWPML stores COLORREF as BGR, not RGB.
        red, green, blue = color & 255, (color >> 8) & 255, (color >> 16) & 255
        if blue > 120 and red < 100 and blue > green:
            shapes.add(shape.get('Id'))
    candidates, notes, omitted = {}, {}, {}
    for i, p in enumerate(ps):
        if i in table_ids:
            continue
        value = ''.join(''.join(c.itertext()) for t in p.findall('TEXT')
                        if t.get('CharShape') in shapes for c in t if c.tag == 'CHAR').strip()
        if not value:
            continue
        candidates[i] = value
        reason = (excluded or {}).get(i)
        if not reason and (not re.search(r'[가-힣A-Za-z0-9]', value) or value in {'o', 'ㅇ'}):
            reason = '빈 입력 표시·글머리표·기호'
        if reason:
            omitted[i] = {'text': value, 'reason': reason}
        else:
            notes[i] = value
    unknown = set(excluded or {}) - set(candidates)
    if unknown:
        raise ValueError(f'파란 주석 제외 위치가 원문과 일치하지 않습니다: {sorted(unknown)}')
    return notes, candidates, omitted


def write_table_guides(folder, ps, guide_groups, topics, *, overrides=None,
                       common_ranges=(), shared=None, excluded=None, root=None,
                       common_blue=(), excluded_blue=None, group_starts=None):
    def text(p):
        return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')

    allowed = {i for g in guide_groups for i in g}
    nonempty = {i for i in allowed if text(ps[i]).strip()}
    blue, blue_candidates, blue_omitted = blue_annotations(
        root, ps, allowed, excluded=excluded_blue) if root is not None else ({}, {}, {})
    if not set(common_blue) <= blue.keys():
        raise ValueError('공통 파란 주석 위치가 원문과 일치하지 않습니다.')
    blue_common = {i for i in blue if i < topics[0]['start']} | set(common_blue)
    blue_assignments = {t['id']: {i for i in blue if t['start'] <= i < t['end']} - blue_common
                        for t in topics}
    def expand(ranges):
        ids = {i for a,b in ranges for i in range(a,b+1)}
        if not ids <= allowed:
            raise ValueError('작성요령 표 밖의 문단은 작성요령에 포함할 수 없습니다.')
        return ids

    common = {i for i in allowed if i < topics[0]['start']} | expand(common_ranges)
    assignments = {}
    for topic in topics:
        start = topic['start']
        if overrides is not None and start in overrides:
            ids = expand(overrides[start])
        else:
            ids = {i for i in allowed if start <= i < topic['end']}
            ids |= expand((shared or {}).get(start, []))
            for a,b in (excluded or {}).get(start, []):
                ids.difference_update(range(a,b+1))
        assignments[topic['id']] = (ids-common) & nonempty

    def content(ids, note_ids=(), level='##'):
        lines = [level+' 작성요령 표', '']
        for i in sorted(ids & nonempty):
            lines.extend([f'<!-- P{i:04d} -->', text(ps[i]), ''])
        if not ids & nonempty:
            lines.extend(['연결된 작성요령 표 내용이 없습니다.', ''])
        lines.extend([level+' 파란 주석·조건', ''])
        for i in sorted(note_ids):
            lines.extend([f'<!-- P{i:04d} -->', blue[i], ''])
        if not note_ids:
            lines.extend(['연결된 파란 주석이 없습니다.', ''])
        return lines

    def save(filename, title, ids, note_ids=(), sections=()):
        lines = ['# '+title, '']
        if sections:
            for section in sections:
                lines.extend([f"<!-- topic:{section['id']}:start -->", ''])
                lines.extend(['## '+section['title'].split('※',1)[0].strip(), ''])
                lines.extend(content(set(section['table_guide_paragraphs']),
                                     section['blue_note_paragraphs'], '###'))
                lines.extend([f"<!-- topic:{section['id']}:end -->", ''])
        else:
            lines.extend(content(ids,note_ids))
        (folder/filename).write_text('\n'.join(lines),encoding='utf-8')

    save('guides/common.md','공통 작성요령',common,blue_common)
    for topic in topics:
        ids = assignments[topic['id']]
        note_ids = blue_assignments[topic['id']]
        topic['table_guide_paragraphs'] = sorted(ids)
        topic['blue_note_paragraphs'] = sorted(note_ids)
        topic['guide_paragraphs'] = sorted(ids | note_ids)
        topic['guide_status'] = ('table_and_blue' if ids and note_ids else 'table_content'
                                 if ids else 'blue_notes_only' if note_ids else 'no_guidance')
    # File grouping must not change the writing/request units. Every original
    # topic keeps its own fields and an explicit section inside the shared MD.
    subsection_audit = {t['id']: t['guide_paragraphs'] for t in topics}
    output_topics = topics
    if group_starts:
        grouped = []
        starts = sorted(group_starts)
        if len({i for i,_ in starts}) != len(starts) or starts[0][0] > topics[0]['start']:
            raise ValueError('대주제 시작 위치가 중복되거나 앞부분을 누락합니다.')
        for n, (start,title) in enumerate(starts):
            end = starts[n+1][0] if n+1 < len(starts) else len(ps)
            if not 0 <= start < end <= len(ps):
                raise ValueError('대주제 범위가 원문을 벗어났습니다.')
            children = [t for t in topics if start <= t['start'] < end]
            if not children:
                raise ValueError(f'대주제에 연결할 하위 항목이 없습니다: {title}')
            gid = f'g{n+1:03d}_p{start:04d}'
            filename = re.sub(r'[<>:"/\\|?*]', '_', title).strip().rstrip('.')
            fields = [f for t in children for f in t['fields']]
            group = {'id':gid,'title':title,'start':start,'end':end,
                     'guide':f'guides/{gid}_{filename}.md','fields':fields,
                     'subsections':[{k:v for k,v in t.items() if k not in {'fields','guide'}}
                                    for t in children]}
            for key in ('table_guide_paragraphs','blue_note_paragraphs','guide_paragraphs'):
                group[key] = sorted({i for t in children for i in t[key]})
            group['guide_status'] = ('table_and_blue' if group['table_guide_paragraphs'] and group['blue_note_paragraphs']
                                     else 'table_content' if group['table_guide_paragraphs']
                                     else 'blue_notes_only' if group['blue_note_paragraphs'] else 'no_guidance')
            grouped.append(group)
            for child in children:
                child['guide'] = group['guide']
                child['guide_section'] = child['id']
                child['guide_document_id'] = gid
        if [f['id'] for t in grouped for f in t['fields']] != [f['id'] for t in topics for f in t['fields']]:
            raise ValueError('대주제 통합 중 입력 위치 순서가 변경되었습니다.')
        output_topics = grouped
    for topic in output_topics:
        save(topic['guide'],topic['title'].split('※',1)[0].strip(),
             set(topic['table_guide_paragraphs']),topic['blue_note_paragraphs'],topic.get('subsections',()))
    assigned = common | set().union(*assignments.values())
    unassigned = nonempty-assigned
    if unassigned:
        save('guides/unassigned.md','소주제 연결 확인 필요 — 작성요령 표 원문',unassigned)
    unassigned_blue = set(blue) - blue_common - set().union(*blue_assignments.values())
    if unassigned_blue:
        save('guides/unassigned.md','소주제 연결 확인 필요',unassigned,unassigned_blue)
    audit = {'mode':'tables_and_blue_notes','table_count':len(guide_groups),
             'source_paragraphs':sorted(nonempty | set(blue)),
             'table_source_paragraphs':sorted(nonempty),'blue_source_paragraphs':sorted(blue),
             'common_paragraphs':sorted((common & nonempty) | blue_common),
             'common_blue_paragraphs':sorted(blue_common),
             'topics':{k:sorted(v | blue_assignments[k]) for k,v in assignments.items()},
             'subsections':subsection_audit,
             'granularity':'subtopic',
             'file_granularity':'chapter' if group_starts else 'subtopic',
             'guide_documents':[{k:t[k] for k in ('id','title','guide','guide_paragraphs')}
                                | {'topic_ids':[s['id'] for s in t.get('subsections',[t])]}
                                for t in output_topics],
             'blue_candidates':{str(k):v for k,v in blue_candidates.items()},
             'excluded_blue_paragraphs':{str(k):v for k,v in blue_omitted.items()},
             'unassigned_paragraphs':sorted(unassigned | unassigned_blue),
             'outside_table_paragraphs':sorted(blue)}
    (folder/'작성요령_분류.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    return audit
