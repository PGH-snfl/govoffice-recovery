"""Local form inputs are separate from AI prose and never inferred as facts."""
import re


def own(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')


def blank_candidates(root, ps, excluded):
    parents = {id(c): p for p in root.iter() for c in p}
    result = set()
    for i,p in enumerate(ps):
        if i in excluded or any(c.tag != 'CHAR' for t in p.findall('TEXT') for c in t):
            continue
        value = own(p).strip()
        parent = parents.get(id(p))
        in_cell = parent is not None and parent.tag == 'PARALIST' and parents.get(id(parent)) is not None and parents[id(parent)].tag == 'CELL'
        # Only the first empty paragraph of a cell, not every spacer paragraph.
        if (not value and in_cell and parent.find('P') is p) or re.fullmatch(r'[_＿]{2,}|\[\s*\]|\(\s*\)',value):
            result.add(i)
    return result


def field_labels(root, ps):
    indices = {id(p):i for i,p in enumerate(ps)}
    labels = {}
    for table in root.iter('TABLE'):
        cells = [c for row in table.findall('ROW') for c in row.findall('CELL')]
        for cell in cells:
            row,col = int(cell.get('RowAddr',0)),int(cell.get('ColAddr',0))
            candidates = [c for c in cells if int(c.get('RowAddr',0)) == row and int(c.get('ColAddr',0)) < col]
            candidates.sort(key=lambda c:int(c.get('ColAddr',0)),reverse=True)
            candidates += sorted([c for c in cells if int(c.get('RowAddr',0)) < row and
                                  int(c.get('ColAddr',0)) <= col < int(c.get('ColAddr',0))+int(c.get('ColSpan',1))],
                                 key=lambda c:int(c.get('RowAddr',0)),reverse=True)
            label = next((' / '.join(own(p).strip() for p in c.iter('P') if own(p).strip())
                          for c in candidates if any(own(p).strip() for p in c.iter('P'))),'')
            for p in cell.findall('PARALIST/P'):
                labels[indices[id(p)]] = label[:240]
    return labels


def input_rows(manifest, profile):
    rows = []
    for topic in manifest['topics']:
        front = topic['title'] in {'표지·과제 기본정보','본문 과제정보','기본정보'}
        for field in topic['fields']:
            label = field.get('label') or field.get('context') or field['id']
            # Exact label/alias matches only. Never select a person from nearby
            # narrative, or fill all telephone columns with an arbitrary value.
            key = next((k for k in profile if k.casefold() == label.strip().casefold()),None)
            personal = label.strip() in {'이름','성명','전화번호','연락처','휴대전화','이메일','전자우편','E-mail'}
            rows.append({'id':field['id'],'topic':topic['title'].split('※',1)[0].strip(),
                         'label':label,'context':field.get('context',''),
                         'ai':not(front or personal or key is not None),
                         'value':profile.get(key,'') if key else '',
                         'max_chars':field['max_chars']})
    return rows


def validate_local_values(manifest, values):
    if values is None:
        return {}
    if not isinstance(values,dict):
        raise ValueError('직접 입력값 형식이 올바르지 않습니다.')
    fields = {f['id']:f for t in manifest['topics'] for f in t['fields']}
    clean = {}
    for key,value in values.items():
        if key not in fields or not isinstance(value,str):
            raise ValueError('등록되지 않은 입력 위치 또는 잘못된 입력값입니다.')
        field = fields[key]
        if len(value) > field['max_chars'] or any(ord(c)<32 and c not in '\r\n\t' for c in value):
            raise ValueError(key+': 입력 길이 또는 제어 문자를 확인하세요.')
        value = re.sub(r'[\r\n\t]+',' ',value).strip()
        if field.get('kind') == 'schedule_marker' and value not in {'','■','?'}:
            raise ValueError(key+': 일정 칸은 ■, ? 또는 빈칸만 입력할 수 있습니다.')
        clean[key] = value
    return clean


def saved_input_snapshot(manifest, values, rows=None):
    """Persist display-only grouping; values always come from validated job inputs."""
    fields={f['id']:(t,f) for t in manifest['topics'] for f in t['fields']}
    result=[];seen=set()
    if rows is not None and (not isinstance(rows,list) or len(rows)>len(values)):
        raise ValueError('입력 확인 목록의 형식이 올바르지 않습니다.')
    for row in rows or []:
        if not isinstance(row,dict): raise ValueError('입력 확인 항목 형식이 올바르지 않습니다.')
        ids=row.get('field_ids')
        if not isinstance(ids,list) or not ids or any(not isinstance(i,str) or i not in values or i in seen for i in ids):
            raise ValueError('입력 확인 목록에 잘못되거나 중복된 문서 위치가 있습니다.')
        if len(set(ids))!=len(ids) or len({values[i] for i in ids})!=1:
            raise ValueError('서로 다른 입력값은 하나의 확인 항목으로 합칠 수 없습니다.')
        label=row.get('label');path=row.get('path')
        if not isinstance(label,str) or not label or len(label)>1000 or not isinstance(path,list) or not 1<=len(path)<=30 or any(not isinstance(p,str) or not p or len(p)>1000 for p in path):
            raise ValueError('입력 확인 항목의 이름 또는 경로가 올바르지 않습니다.')
        result.append(dict(id=ids[0],field_ids=list(ids),label=label,path=list(path),
                           topic='작업 입력 정보',context=' > '.join(path),value=values[ids[0]],ai=False))
        seen.update(ids)
    # Old jobs have no saved UI hierarchy: show only their actual stored inputs.
    for fid,value in values.items():
        if fid in seen:continue
        topic,field=fields[fid];label=field.get('label') or field.get('context') or fid
        result.append(dict(id=fid,field_ids=[fid],label=label,path=[topic['title'],label],
                           topic=topic['title'],context=label,value=value,ai=False))
    return result


def saved_profile_rows(manifest, profile):
    """One visible row per saved personal field, retaining every document target.

    Exact unambiguous labels/aliases only. Never merge unrelated fields merely
    because they share a name or value, and never expose empty/template values.
    """
    labels = {}
    for field in profile.대표필드목록:
        for label in (field.id, field.대표필드명, profile.필드경로(field), *field.별칭):
            labels.setdefault(label.strip().casefold(), {})[field.id] = field
    groups = {}
    for topic in manifest['topics']:
        for target in topic['fields']:
            if manifest.get('guide_mode')=='ai_analysis' and target.get('role')!='personal':
                continue
            label = target.get('label') or target.get('context') or target['id']
            candidates = labels.get(label.strip().casefold(), {})
            if len(candidates) != 1:
                continue
            field = next(iter(candidates.values()))
            value = field.기본값
            if not value or not value.strip():
                continue
            if field.id not in groups:
                path = profile.필드경로(field)
                groups[field.id] = dict(id=target['id'], profile_field_id=field.id,
                    field_ids=[], label=field.대표필드명, path=path.split(' > '),
                    topic='저장된 개인정보', context=path, value=value, ai=False,
                    max_chars=target['max_chars'])
            row = groups[field.id]
            if target['id'] not in row['field_ids']:
                row['field_ids'].append(target['id'])
            row['max_chars'] = min(row['max_chars'], target['max_chars'])
    return list(groups.values())


def attach_input_paths(rows, profile):
    """Display-only hierarchy; never merge document IDs or change input values.

    Reuse a personal field path only for an unambiguous exact name/path/alias.
    Otherwise retain the document label under its topic, without guessing a parent.
    """
    candidates = {}
    for field in profile.대표필드목록:
        path = tuple(p.strip() for p in profile.필드경로(field).split('>') if p.strip())
        for label in (field.대표필드명, *field.별칭, profile.필드경로(field)):
            candidates.setdefault(label.strip().casefold(), set()).add(path)
    for row in rows:
        label = row['label'].strip()
        matches = candidates.get(label.casefold(), set())
        parts = list(next(iter(matches))) if len(matches) == 1 else [p.strip() for p in label.split('>') if p.strip()]
        row['path'] = [row['topic'] or '문서 입력정보', *(parts or [row['id']])]
    return rows
