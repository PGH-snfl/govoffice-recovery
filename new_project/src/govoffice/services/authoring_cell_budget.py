"""Conservative cell writing budgets, not font shrinking or text truncation.

Dimensions provide estimates, not a substitute for Hancom's layout engine.
Personal/factual values and review annotations are never shortened here.
"""
import math
import re
import unicodedata
from .authoring_typography import review_paragraphs
from .authoring_paragraph_style import paragraph_gap,list_indent
from .authoring_word_wrap import middle_dot_breaks,SOFT_BREAK


class CellContentTooLong(ValueError):
    pass


def text_units(value):
    return sum(1 if unicodedata.east_asian_width(c) in 'WF' else .6 for c in value)


def line_count(value, columns):
    # Continuation lines in a list align with the item text, after its marker.
    indent=min(list_indent(value,1000)/1000,columns/3)
    width=max(1,columns-indent)
    count=0
    # Pack whole whitespace-delimited words, rather than assuming all unused
    # space at line ends can hold fragments. Don't credit tracking compression:
    # this remains a conservative estimate, not font-metric measurement.
    for line in value.split('\n'):
        lines=1;used=0.;pending=0.
        for token in re.findall(r'\u200b|\s+|[^\s\u200b]+',middle_dot_breaks(line)):
            if token==SOFT_BREAK:continue
            units=text_units(token)
            if token.isspace():
                pending+=units
                continue
            gap=pending if used else 0.
            if used and used+gap+units>width:
                lines+=1;used=0.;gap=0.
            used+=gap+units;pending=0.
            if used>width:
                # A token wider than the entire cell cannot be kept on one
                # line at the inherited font size. Estimate emergency wrapping.
                extra=max(0,math.ceil(used/width)-1)
                lines+=extra;used-=extra*width
        count+=lines
    return count


def attach_cell_budgets(root, manifest, local_values=None):
    from .authoring_design_fields import safe_writing_manifest, writing_routes, classify_tables
    fields=[f for t in manifest['topics'] for f in t['fields']]
    protected,routes=writing_routes(root,fields)
    classify_tables(root,manifest,protected)
    effective=safe_writing_manifest(root,manifest)
    _attach_cell_budgets(root,effective,local_values)
    mapped={f['id']:f for t in effective['topics'] for f in t['fields']}
    for f in fields:
        f.pop('table_fit',None)
        f.pop('write_target',None)
        if 'table_fit' in mapped[f['id']]:f['table_fit']=mapped[f['id']]['table_fit']
        if f['id'] in routes:f['write_target']=routes[f['id']]
    return manifest


def _attach_cell_budgets(root, manifest, local_values=None):
    """Only mutate a new job's snapshot; share space across bound fields."""
    local_values=local_values or {}
    parents={id(c):p for p in root.iter() for c in p}
    ps=list(root.iter('P'));indices={id(p):i for i,p in enumerate(ps)}
    chars={s.get('Id'):s for s in root.iter('CHARSHAPE')}
    profiles={}
    if manifest.get('render_policy',{}).get('flowing_content_fonts'):
        from .authoring_font_profiles import flowing_font_profiles
        profiles=flowing_font_profiles(root,manifest)
    elif manifest.get('render_policy',{}).get('uniform_content_fonts'):
        from .authoring_font_profiles import document_font_profiles
        profiles=document_font_profiles(root,manifest)
    paras={s.get('Id'):s for s in root.iter('PARASHAPE')}
    cells={}
    bound_indices={f['index'] for t in manifest['topics'] for f in t['fields']}
    def ancestor(node,tag):
        while node is not None:
            if node.tag==tag:return node
            node=parents.get(id(node))
    def font_height(p):
        if 'by_index' in profiles and indices.get(id(p)) in bound_indices:
            return int(profiles['by_index'][indices[id(p)]].get('Height','1100'))
        if 'table' in profiles and ancestor(p,'CELL') is not None:
            return int(profiles['table'].get('Height','1000'))
        height=max([int(chars.get(t.get('CharShape'),{}).get('Height','1000')) for t in p.findall('TEXT')]+[1])
        if manifest.get('render_policy',{}).get('polished_output'):
            from .authoring_output_polish import normalized_body_height
            return normalized_body_height(height)
        return height
    for topic in manifest['topics']:
        for field in topic['fields']:
            field.pop('table_fit',None)
            if field.get('write_blocked'):continue
            p=ps[field['index']];cell=ancestor(p,'CELL')
            if cell is not None:cells.setdefault(cell,[]).append((field,p))
    for cell,items in cells.items():
        width=int(cell.get('Width','0'));height=int(cell.get('Height','0'))
        if width<=0 or height<=0:continue
        row=parents.get(id(cell));table=ancestor(row,'TABLE')
        if cell.get('RowSpan','1')=='1' and row is not None:
            height=max([height]+[int(c.get('Height','0')) for c in row.findall('CELL') if c.get('RowSpan','1')=='1'])
        margin=cell.find('CELLMARGIN') if cell.get('HasMargin')=='true' else table.find('INSIDEMARGIN') if table is not None else None
        padding={k:int(margin.get(k,'0')) if margin is not None else 0 for k in ('Left','Right','Top','Bottom')}
        for side in ('Left','Right'):padding[side]=min(max(padding[side],min(283,width//14)),width//5)
        for side in ('Top','Bottom'):padding[side]=max(141,padding[side])
        usable_width=max(1,width-padding['Left']-padding['Right'])
        writable={f['index'] for f,_ in items if not f.get('insert_after')}
        cleared=set(manifest.get('clear_guide_indices',[]))|set(manifest.get('blank_indices',[]))
        fixed_height=0
        for p in cell.findall('PARALIST/P'):
            if indices[id(p)] in writable|cleared:continue
            text=''.join(c.text or '' for t in p.findall('TEXT') for c in t.findall('CHAR'))
            fixed_height+=line_count(text,usable_width/font_height(p))*font_height(p)*1.6
        prose=[(f,p) for f,p in items if f.get('role')!='personal'
               and f.get('kind') not in {'factual_cell','schedule_marker'} and f['id'] not in local_values]
        if not prose:continue
        protected_height=0
        for f,p in items:
            if any(f is pf for pf,_ in prose):continue
            value=local_values.get(f['id'],f.get('original',''))
            protected_height+=line_count(value,usable_width/font_height(p))*font_height(p)*1.6
        available=max(0,height-padding['Top']-padding['Bottom']-fixed_height-protected_height)
        for field,p in prose:
            font=font_height(p)
            pm=paras.get(p.get('ParaShape'))
            pm=pm.find('PARAMARGIN') if pm is not None else None
            spacing=int(pm.get('LineSpacing','130')) if pm is not None and pm.get('LineSpacingType')=='Percent' else 130
            spacing=max(130,min(160,spacing))
            columns=max(1,int(usable_width/font*.90))
            lines=max(1,int(available/len(prose)/(font*spacing/100+paragraph_gap(font))))
            reserve=1 if lines>=2 else 0
            body_lines=max(1,lines-reserve)
            field['table_fit']={'cell_width':width,'cell_height':height,'font_height':font,
                                'chars_per_line':columns,'max_body_lines':body_lines,
                                'max_body_chars':min(field['max_chars'],columns*body_lines),
                                'reserved_review_lines':reserve,'paragraph_gap':paragraph_gap(font),'estimated':True}
    return manifest


def validate_cell_content(topic,result):
    for field in topic['fields']:
        budget=field.get('table_fit')
        if not budget or budget.get('offline_replay'):continue
        parts=[p.strip() for p in result['values'][field['id']].split('\n') if p.strip()]
        body=[value for value,review in review_paragraphs(parts) if not review]
        lines=sum(line_count(value,budget['chars_per_line']) for value in body)
        count=sum(len(value) for value in body)
        if lines>budget['max_body_lines'] or count>budget['max_body_chars']:
            raise CellContentTooLong(
                f"{field['id']}: 표 셀 분량 초과(현재 본문 {count}자/{lines}줄). "
                f"본문을 {budget['max_body_chars']}자, {budget['max_body_lines']}줄 이내로 요약하세요. "
                '숫자·이름·날짜·조건·부정 표현은 바꾸지 말고 반복 설명만 줄이세요. 확인 안내는 보존하세요.')


def validate_fit_revision(topic,previous,current):
    """Do not accept a size repair that silently edits protected field values."""
    for field in topic['fields']:
        old=previous['values'][field['id']];new=current['values'][field['id']]
        if not field.get('table_fit'):
            if old!=new:raise ValueError(field['id']+': 표 요약 중 다른 필드 값이 바뀌었습니다.')
            continue
        numbers=lambda value:set(re.findall(r'\d+(?:\.\d+)?',value.replace(',','')))
        if not numbers(old)<=numbers(new):
            raise ValueError(field['id']+': 표 요약 중 수치 또는 날짜가 누락·변경되었습니다.')
        old_notes={v for v,blue in review_paragraphs(old.split('\n')) if blue}
        new_notes={v for v,blue in review_paragraphs(new.split('\n')) if blue}
        if not old_notes<=new_notes:raise ValueError(field['id']+': 표 요약 중 확인 안내가 누락·변경되었습니다.')
    if not set(previous['needs_review'])<=set(current['needs_review']):
        raise ValueError('표 요약 중 검토 사유가 누락·변경되었습니다.')
