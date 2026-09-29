"""Native Hancom Memo fields, with body-preserving read-back verification."""
from copy import deepcopy
import xml.etree.ElementTree as ET


def body_paragraphs(root):
    def visit(node):
        if node.tag == 'FIELDBEGIN' and node.get('Type') == 'Memo':
            return
        if node.tag == 'P':
            yield node
        for child in node:
            yield from visit(child)
    return list(visit(root))


def paragraph_text(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')


def memo_fields(root):
    return [n for n in root.iter('FIELDBEGIN') if n.get('Type') == 'Memo']


def body_signature(root):
    # Memo controls must not alter prose, paragraph layout, or character styles.
    shapes = {tag: {n.get('Id'): n for n in root.iter(tag)} for tag in ('PARASHAPE','CHARSHAPE')}
    def shape(tag, key):
        node = shapes[tag].get(key)
        if node is None:return key
        node = deepcopy(node);node.attrib.pop('Id',None)
        return ET.tostring(node,encoding='unicode')
    result = []
    for p in body_paragraphs(root):
        attrs = {k:v for k,v in p.attrib.items() if k != 'InstId'}
        attrs['ParaShape'] = shape('PARASHAPE',p.get('ParaShape'))
        runs = []
        for t in p.findall('TEXT'):
            text = ''.join(''.join(c.itertext()) for c in t if c.tag == 'CHAR')
            style = shape('CHARSHAPE',t.get('CharShape'))
            if text:
                if runs and runs[-1][0] == style:runs[-1] = (style,runs[-1][1]+text)
                else:runs.append((style,text))
        if not runs and p.find('TEXT') is not None:
            runs = [(shape('CHARSHAPE',p.find('TEXT').get('CharShape')),'')]
        result.append((attrs,runs))
    return result


def compose_memos(base, prototype_root, entries):
    """Use a native memo control prototype and the base document's styles."""
    root = deepcopy(base)
    # Native serialization can renumber shapes. Keep the base mappings and use
    # its own Memo style, never copy a prototype HEAD over unrelated body IDs.
    style = next((s for s in base.iter('STYLE') if s.get('EngName') == 'Memo'), None)
    if style is None:style = next(iter(base.iter('STYLE')), None)
    memo_para = {'ParaShape':style.get('ParaShape','0'),'Style':style.get('Id','0')} if style is not None else {'ParaShape':'0','Style':'0'}
    memo_run = {'CharShape':style.get('CharShape','0')} if style is not None else {'CharShape':'0'}
    prototypes = memo_fields(prototype_root)
    if not prototypes:
        raise RuntimeError('한글 메모 원형을 만들지 못했습니다.')
    prototype = prototypes[-1]
    ps = body_paragraphs(root)
    all_ps = list(root.iter('P'))
    body_indices = {id(p): i for i,p in enumerate(ps)}
    used = {int(value) for n in prototype_root.iter() for key, value in n.attrib.items()
            if key in {'FieldId', 'InstId'} and value.isdigit()}
    next_id = 1000000
    zorder = max([int(n.get('Zorder', '0')) for n in memo_fields(base)] + [0])
    record = []
    for entry in entries:
        memo = entry.get('review_memo')
        if not memo:
            continue
        original_index = entry['output_indices'][0]
        index = body_indices.get(id(all_ps[original_index]))
        if index is None:
            raise RuntimeError('기존 메모 안에는 새 확인 메모를 중첩하지 않습니다.')
        p = ps[index]
        run = next((t for t in p.findall('TEXT') if t.find('CHAR') is not None), None)
        if run is None:
            run = p.find('TEXT')
            if run is None:
                run = ET.SubElement(p, 'TEXT', {'CharShape': '0'})
            ET.SubElement(run, 'CHAR')
        chars = [c for c in run if c.tag == 'CHAR']
        begin = deepcopy(prototype)
        zorder += 1
        while next_id in used or next_id + 1 in used:next_id += 2
        # FieldId is Hancom's shared %%me type marker, not a unique memo ID.
        # InstId identifies each control; MEMO's third command item is Zorder.
        begin.set('InstId', str(next_id + 1))
        command = begin.get('Command','').split('/')
        if len(command) < 4 or command[0] != 'MEMO':
            raise RuntimeError('한글 메모 명령 형식을 확인하지 못했습니다.')
        command[2] = str(zorder); begin.set('Command','/'.join(command))
        begin.set('Zorder', str(zorder)); next_id += 2
        para_list = begin.find('PARALIST')
        if para_list is None or para_list.find('P') is None:
            raise RuntimeError('한글 메모 문단 구조를 확인하지 못했습니다.')
        for child in list(para_list):
            para_list.remove(child)
        for line in memo['text'].split('\n'):
            mp = ET.SubElement(para_list, 'P', memo_para)
            mt = ET.SubElement(mp, 'TEXT', memo_run)
            ET.SubElement(mt, 'CHAR').text = line
        end = ET.Element('FIELDEND', {key: begin.get(key) for key in
                         ('Editable', 'FieldId', 'Property', 'Type', 'Zorder')})
        # Only enclose text, never table/design controls in the same run.
        run.insert(list(run).index(chars[0]), begin)
        run.insert(list(run).index(chars[-1]) + 1, end)
        record.append({**memo, 'anchor_index': index, 'native_inst_id': begin.get('InstId')})
    if body_signature(root) != body_signature(base):
        raise RuntimeError('메모 연결 중 본문·글자 서식이 변경되었습니다.')
    return root, record


def verify_memos(root, records, baseline, *, bind_native_ids=False):
    actual_signature, expected_signature = body_signature(root), body_signature(baseline)
    if actual_signature != expected_signature:
        difference = next((i for i, (a,b) in enumerate(zip(actual_signature, expected_signature)) if a != b), -1)
        raise RuntimeError('한글 메모 저장 후 본문·글자 서식이 달라졌습니다. 문단 '+str(difference))
    ps = body_paragraphs(root)
    for record in records:
        matches = [n for n in ps[record['anchor_index']].iter('FIELDBEGIN')
                   if n.get('Type') == 'Memo' and
                   (bind_native_ids or n.get('InstId') == record['native_inst_id']) and
                   '\n'.join(paragraph_text(p) for p in n.iter('P')) == record['text']]
        if len(matches) != 1:
            raise RuntimeError('확인 메모 입력 위치·내용 검증 실패: ' + record['field_id'])
        if bind_native_ids:record['native_inst_id'] = matches[0].get('InstId')
        text = '\n'.join(paragraph_text(p) for p in matches[0].iter('P'))
        if text != record['text']:
            raise RuntimeError('확인 메모 내용 검증 실패: ' + record['field_id'])
    if len({n.get('InstId') for n in memo_fields(root)}) != len(memo_fields(root)):
        raise RuntimeError('한글 메모 식별번호가 중복되었습니다.')
    memo_content = lambda n: (n.get('Command'), '\n'.join(paragraph_text(p) for p in n.iter('P')))
    expected_old = {n.get('InstId'): memo_content(n) for n in memo_fields(baseline)}
    actual = {n.get('InstId'): memo_content(n) for n in memo_fields(root)}
    if any(actual.get(k) != v for k, v in expected_old.items()):
        raise RuntimeError('양식에 있던 기존 메모가 변경되었습니다.')


def attach_native_memos(app, base, entries):
    if not any(e.get('review_memo') for e in entries):
        return base, []
    def insert(text):
        app.HAction.GetDefault('InsertText', app.HParameterSet.HInsertText.HSet)
        app.HParameterSet.HInsertText.Text = text
        if app.HAction.Execute('InsertText', app.HParameterSet.HInsertText.HSet) is False:
            raise RuntimeError('한글 메모 원형 입력 실패')
    app.HAction.Run('MoveDocEnd'); app.HAction.Run('BreakPara')
    insert('GOVOFFICE_TEMP_MEMO_ANCHOR')
    app.HAction.Run('MoveLineBegin'); app.HAction.Run('MoveSelLineEnd')
    if not app.HAction.Run('InsertFieldMemo'):
        raise RuntimeError('한글에서 메모 추가를 실행하지 못했습니다.')
    insert('검토 메모')
    app.HAction.Run('CloseEx')
    prototype_root = ET.fromstring(app.GetTextFile('HWPML2X', ''))
    annotated, records = compose_memos(base, prototype_root, entries)
    xml = '<?xml version="1.0" encoding="UTF-16"?>\n' + ET.tostring(annotated, encoding='unicode')
    if not app.SetTextFile(xml, 'HWPML2X', ''):
        raise RuntimeError('한글이 확인 메모를 읽지 못했습니다.')
    actual = ET.fromstring(app.GetTextFile('HWPML2X', ''))
    verify_memos(actual, records, base, bind_native_ids=True)
    return actual, records
