"""Real paragraph breaks, inherited styles and review colour without control copies."""
from copy import deepcopy
import re
import xml.etree.ElementTree as ET

REVIEW=re.compile(r'(?:확인|검토)\s*필요|(?<![가-힣])(?:미확정|미제공|미정)(?![가-힣])')
BOUNDARY=re.compile(r'[.!?](?=\s|$)|[;；\n]')


def review_spans(value, notes=()):
    """Mark explicit review sentences/brackets, never an entire field by flag.

    Quoted excerpts in field-specific review notes can identify a smaller range.
    Generic review reports and ordinary words such as 가정용/예시 are not colours.
    Offsets refer to unchanged source text, including spaces and punctuation.
    """
    spans=[]
    brackets=list(re.finditer(r'\[[^\[\]]*\]|\([^()]*\)|【[^【】]*】',value))
    boundaries=list(BOUNDARY.finditer(value))
    for marker in REVIEW.finditer(value):
        if re.match(r'\s*(?:없|하지\s*않)',value[marker.end():]):continue
        enclosing=next((b for b in brackets if b.start()<=marker.start() and b.end()>=marker.end()),None)
        if enclosing:
            start,end=enclosing.span()
        else:
            start=max([b.end() for b in boundaries if b.end()<=marker.start()]+[0])
            end=min([b.end() for b in boundaries if b.start()>=marker.end()]+[len(value)])
        while start<end and value[start].isspace():start+=1
        while end>start and value[end-1].isspace():end-=1
        spans.append((start,end))
    if value.strip()=='?':spans.append((value.index('?'),value.index('?')+1))
    for note in notes:
        for quote in re.findall(r'["“‘「]([^"”’」]+)["”’」]',note):
            if len(quote.strip())<2:continue
            spans.extend(m.span() for m in re.finditer(re.escape(quote),value))
    merged=[]
    for start,end in sorted(spans):
        if merged and start<=merged[-1][1]:merged[-1]=(merged[-1][0],max(end,merged[-1][1]))
        else:merged.append((start,end))
    return merged


def review_paragraphs(parts, notes=()):
    """Place review annotations below their body paragraph, never in-line.

    Explicit review text is moved, not discarded. Quoted review notes do not
    remove the quoted body value. Field-wide notes follow the last paragraph.
    Each tuple contains the exact rendered text and whether it is a blue note.
    """
    output=[];pending=[]
    def clean(note):
        note=re.sub(r'\bP\d{4,}\b\s*[:：-]?\s*','',note).strip()
        if len(note)>1 and (note[0],note[-1]) in {('[',']'),('(',')'),('【','】')}:
            note=note[1:-1].strip()
        if note=='?':note='확인 필요: 일정 미확정'
        if not REVIEW.search(note):note='확인 필요: '+note
        return '('+note+')'
    def key(note):return re.sub(r'[\s\[\]()【】.:：。]','',note)
    for note in notes:
        if re.search(r'(?:확인|검토)\s*(?:완료|불필요)|확인\s*필요\s*없',note):continue
        quotes=re.findall(r'["“‘「]([^"”’」]+)["”’」]',note)
        target=next((i for i,part in enumerate(parts) if any(q in part for q in quotes)),len(parts)-1)
        pending.append((target,note))
    for i,part in enumerate(parts):
        spans=review_spans(part)
        # Do not cut a placeholder out of the middle of a grammatical sentence
        # (e.g. "예산은 [확인 필요: 금액]입니다"). Move that sentence intact.
        expanded=[];boundaries=list(BOUNDARY.finditer(part))
        for start,end in spans:
            if part[start:start+1] in {'[','(','【'}:
                left=max([b.end() for b in boundaries if b.end()<=start]+[0])
                right=min([b.end() for b in boundaries if b.start()>=end]+[len(part)])
                if part[left:start].strip() and part[end:right].strip(' .!?;；'):
                    start,end=left,right
                    while start<end and part[start].isspace():start+=1
            if expanded and start<=expanded[-1][1]:expanded[-1]=(expanded[-1][0],max(end,expanded[-1][1]))
            else:expanded.append((start,end))
        spans=expanded
        body=[];annotations=[];offset=0
        for start,end in spans:
            body.append(part[offset:start]);annotations.append(clean(part[start:end]));offset=end
        body.append(part[offset:])
        text=re.sub(r' {2,}',' ',''.join(body)).strip() if spans else part
        if text:output.append((text,False))
        for target,note in pending:
            if target==i:annotations.append(clean(note))
        seen=set()
        for annotation in annotations:
            if key(annotation) not in seen:
                output.append((annotation,True));seen.add(key(annotation))
    return output or [('',False)]


def format_written_fields(root, ps, manifest, entries, polisher=None, font_profiles=None):
    from .authoring_font_profiles import font_group, resolve_font_profile
    parents={id(c):p for p in root.iter() for c in p}
    fields={f['id']:f for t in manifest['topics'] for f in t['fields']}
    headings={t['start'] for t in manifest['topics']}
    guides=set(manifest.get('clear_guide_indices',[]))
    shape_list=root.find('.//CHARSHAPELIST')
    shapes={s.get('Id'):s for s in root.iter('CHARSHAPE')}
    colors={};next_id=max([int(k) for k in shapes]+[-1])+1
    refs=[]
    def color(old,blue,body=False,group=None,field_id=None,index=None):
        nonlocal next_id
        if shape_list is None or old not in shapes:return old
        profile=resolve_font_profile(font_profiles,field_id=field_id,index=index,group=group)
        key=(ET.tostring(profile) if profile is not None else old,bool(blue),body)
        if key not in colors:
            shape=deepcopy(profile if profile is not None else shapes[old]);shape.set('Id',str(next_id))
            shape.set('TextColor',str(0xFF0000 if blue else 0))
            if body and profile is None:
                from .authoring_output_polish import normalized_body_height
                shape.set('Height',str(normalized_body_height(shape.get('Height','1100'))))
                for tag in ('BOLD','ITALIC'):
                    for item in list(shape.findall(tag)):shape.remove(item)
            shape_list.append(shape);colors[key]=str(next_id);shapes[str(next_id)]=shape;next_id+=1
        return colors[key]
    def colour_paragraph(p,blue,body=False,group=None,field_id=None,index=None):
        for run in p.findall('TEXT'):
            run.set('CharShape',color(run.get('CharShape'),blue,body,group,field_id,index) or '0')
    def plain(p):return not any(c.tag!='CHAR' for t in p.findall('TEXT') for c in t)
    def new_paragraph(model,value):
        p=ET.Element('P',{k:v for k,v in model.attrib.items() if k not in {'PageBreak','ColumnBreak','InstId'}})
        run=model.find('TEXT')
        t=ET.SubElement(p,'TEXT',dict(run.attrib) if run is not None else {'CharShape':'0'})
        ET.SubElement(t,'CHAR').text=value
        return p
    for entry in entries:
        field=fields[entry['field_id']];original=ps[field['index']]
        parent=parents[id(original)]
        model=original
        style_index=field.get('style_from_index')
        if style_index is not None:
            if not isinstance(style_index,int) or style_index<0 or style_index>=len(ps) or parents.get(id(ps[style_index])) is not parent:
                raise ValueError(entry['field_id']+': 글자 모양 참조 문단이 같은 입력 영역에 있지 않습니다.')
            model=ps[style_index]
        if field.get('insert_after'):
            candidates=[(abs(i-field['index']),p) for i,p in enumerate(ps)
                        if i not in headings|guides and parents.get(id(p)) is parent and plain(p)
                        and p.find('TEXT') is not None]
            if candidates:model=min(candidates,key=lambda x:x[0])[1]
        parts=entry['value'].split('\n') if field.get('multiline') else [entry['value']]
        parts=[p.strip() for p in parts if p.strip()] or ['']
        if manifest.get('render_policy',{}).get('review_memos') and entry.get('source') != 'user':
            from .authoring_review_memos import memo_body
            parts = [memo_body(p) for p in parts]
            rendered = [(p,False) for p in parts if p] or [('',False)]
        else:
            rendered=(review_paragraphs(parts,entry.get('review_notes',()))
                  if manifest.get('render_policy',{}).get('blue_review') else [(p,False) for p in parts])
        parts=[value for value,_ in rendered]
        paragraphs=[];position=list(parent).index(original)
        for n,value in enumerate(parts):
            if n==0 and not field.get('insert_after'):
                p=original
                if style_index is not None:
                    for key in ('ParaShape','Style'):
                        if key in model.attrib:p.set(key,model.get(key))
                for t in p.findall('TEXT'):
                    for c in list(t.findall('CHAR')):t.remove(c)
                first=p.find('TEXT')
                if first is None:first=ET.SubElement(p,'TEXT',{'CharShape':'0'})
                if style_index is not None and model.find('TEXT') is not None:
                    first.set('CharShape',model.find('TEXT').get('CharShape','0'))
                ET.SubElement(first,'CHAR').text=value
            else:
                p=new_paragraph(model,value)
                parent.insert(position+n+(1 if field.get('insert_after') else 0),p)
            paragraphs.append(p)
        for p,(_,blue) in zip(paragraphs,rendered):
            body=bool(polisher and field.get('role')=='body' and field.get('kind') not in {'factual_cell','schedule_marker'})
            colour_paragraph(p,blue,body,font_group(original,parents),field['id'],field['index'])
        refs.append((entry,paragraphs,parts))
    existing_refs=len(refs)
    if polisher is not None:polisher.finish(refs,fields)
    # The finisher may mirror a summary value into an unbound cover input cell.
    # Such program-written values use the same table profile as all other input.
    final_parents={id(c):p for p in root.iter() for c in p}
    if font_profiles:
        for entry,paragraphs,_ in refs[existing_refs:]:
            for p in paragraphs:colour_paragraph(p,False,False,font_group(p,final_parents),entry['field_id'],entry.get('input_index'))
    if shape_list is not None:shape_list.set('Count',str(len(shape_list)))
    from .authoring_table_layout import format_written_cells
    format_written_cells(root,refs,fields)
    from .authoring_word_wrap import format_word_wrapping
    format_word_wrapping(root,refs)
    from .authoring_equations import format_equations
    equation_counts=format_equations(root,refs)
    from .authoring_scientific_notation import format_scientific_notation
    format_scientific_notation(root,refs)
    indices={id(p):i for i,p in enumerate(root.iter('P'))}
    logs=[{**e,'output_index':indices[id(paragraphs[0])],
             'output_indices':[indices[id(p)] for p in paragraphs],
             'paragraph_values':parts,
             'equation_count':sum(equation_counts.get(id(p),0) for p in paragraphs)}
            for e,paragraphs,parts in refs]
    from .authoring_cell_budget import line_count
    for entry in logs:
        budget=fields[entry['field_id']].get('table_fit')
        if budget and sum(line_count(v,budget['chars_per_line']) for v in entry['paragraph_values'])>budget['max_body_lines']+budget['reserved_review_lines']:
            entry['table_fit_warning']='저장 내용·확인 안내를 보존하여 원본 셀의 예상 분량을 초과했습니다. 최종 표 높이를 확인하세요.'
    return logs
