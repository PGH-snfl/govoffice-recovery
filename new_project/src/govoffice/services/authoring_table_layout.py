"""Readable bound cells; safely rebalance plain tables without changing total width.

HWPML: LineWrap=Break wraps without squeezing glyphs. Floating tables with
PageBreak=Cell can continue cell text across pages; inline tables cannot.
Hancom's layout engine expands row heights after SetTextFile/SaveAs, so do not
guess heights or shrink fonts based on a character-count approximation.
"""
from copy import deepcopy
import re
import unicodedata
import xml.etree.ElementTree as ET
from .authoring_paragraph_style import paragraph_gap,list_indent


def format_written_cells(root, refs, fields):
    from .authoring_table_width import rebalance_written_tables
    rebalance_written_tables(root,refs,fields)
    parents={id(c):p for p in root.iter() for c in p}
    shape_list=root.find('.//PARASHAPELIST')
    shapes={s.get('Id'):s for s in root.iter('PARASHAPE')}
    chars={s.get('Id'):s for s in root.iter('CHARSHAPE')}
    cache={};next_id=max([int(k) for k in shapes]+[-1])+1
    cells={}
    def ancestor(node,tag):
        while node is not None:
            if node.tag==tag:return node
            node=parents.get(id(node))
    for entry,paragraphs,parts in refs:
        for p,value in zip(paragraphs,parts):
            cell=ancestor(p,'CELL')
            if cell is not None:cells.setdefault(cell,[]).append((p,value,fields[entry['field_id']]))
    for cell,written in cells.items():
        table=ancestor(parents.get(id(cell)),'TABLE')
        paralist=cell.find('PARALIST')
        if table is None or paralist is None:continue
        margin=cell.find('CELLMARGIN') if cell.get('HasMargin')=='true' else table.find('INSIDEMARGIN')
        full_width=max(1,int(cell.get('Width','10000')))
        padding={k:int(margin.get(k,'0')) if margin is not None else 0 for k in ('Left','Right','Top','Bottom')}
        for side in ('Left','Right'):
            padding[side]=min(max(padding[side],min(283,full_width//14)),full_width//5)
        for side in ('Top','Bottom'):padding[side]=max(141,padding[side])
        own_margin=cell.find('CELLMARGIN')
        if own_margin is None:
            own_margin=ET.Element('CELLMARGIN');cell.insert(list(cell).index(paralist),own_margin)
        own_margin.attrib.update({k:str(v) for k,v in padding.items()})
        cell.set('HasMargin','true')
        width=max(1,full_width-padding['Left']-padding['Right'])
        def long_line(p,value):
            run=p.find('TEXT');shape=chars.get(run.get('CharShape') if run is not None else None,{})
            height=int(shape.get('Height','1000'))
            return sum(1 if unicodedata.east_asian_width(c) in 'WF' else .6 for c in value)*height>width
        long=len(paralist.findall('P'))>1 or any(long_line(p,v) for p,v,_ in written)
        paralist.set('LineWrap','Break')
        paralist.set('VertAlign','Top' if long else 'Center')
        for written_index,(p,value,field) in enumerate(written):
            old=p.get('ParaShape')
            if old not in shapes or shape_list is None:continue
            numeric=bool(re.search(r'금액|예산|비용|수량|인원|비율|백분율|합계|단가',field.get('label',''))
                         and re.fullmatch(r'\s*[-+]?\d[\d,.]*(?:\s*(?:원|천원|백만원|억원|명|개|건|%))?\s*',value))
            prose=field.get('role')=='body' and field.get('kind') not in {'factual_cell','schedule_marker'}
            run=p.find('TEXT');char=chars.get(run.get('CharShape') if run is not None else None,{})
            font=int(char.get('Height','1000'));review=char.get('TextColor')==str(0xFF0000)
            align='Right' if numeric else 'Left' if long or prose or review else shapes[old].get('Align','Left')
            if align not in {'Left','Center','Right'}:align='Left'
            before=paragraph_gap(font,review) if list(paralist).index(p)>0 else 0
            indent=min(list_indent(value,font),width//3) if prose and not review else 0
            subheading=(written_index+1<len(written) and written[written_index+1][2]['id']==field['id']
                        and len(value.strip())<=60 and bool(re.match(r'^\d{1,2}[.)]\s+\S',value.strip()))
                        and not value.rstrip().endswith(('.', '!', '?', '다', '함')))
            key=(old,align,before,indent,subheading)
            if key not in cache:
                shape=deepcopy(shapes[old]);shape.set('Id',str(next_id))
                shape.attrib.update(Align=align,LineWrap='Break',
                                    KeepLines='false',KeepWithNext='true' if subheading else 'false',
                                    PageBreakBefore='false',SnapToGrid='false')
                pm=shape.find('PARAMARGIN')
                if pm is None:pm=ET.SubElement(shape,'PARAMARGIN')
                spacing=int(pm.get('LineSpacing','130')) if pm.get('LineSpacingType')=='Percent' else 130
                # HWP paragraph margins use 2x HWP units (URC). Negative indent
                # offsets continuation lines, not the first line as CSS does.
                pm.attrib.update(Left='0',Right='0',Indent=str(-2*indent),Prev=str(2*before),Next='0',
                                 LineSpacingType='Percent',LineSpacing=str(max(130,min(160,spacing))))
                shape_list.append(shape);cache[key]=str(next_id);next_id+=1
            p.set('ParaShape',cache[key])
        # Reflow can strand a fixed, short table subheading at a page bottom.
        # Keep it (and blank spacers) with its generated content, without
        # touching the original heading's font or alignment.
        written_ids={id(p) for p,_,_ in written}
        siblings=paralist.findall('P')
        for p,_,_ in written:
            preceding=[]
            for previous in reversed(siblings[:siblings.index(p)]):
                if id(previous) in written_ids:break
                text=''.join(c.text or '' for t in previous.findall('TEXT') for c in t.findall('CHAR')).strip()
                if any(c.tag!='CHAR' for t in previous.findall('TEXT') for c in t):break
                if not text:
                    preceding.append(previous);continue
                if len(text)<=60 and re.match(r'^[o○•]\s+\S',text):
                    preceding.append(previous)
                    for heading in preceding:
                        old=heading.get('ParaShape');key=('fixed-heading',old)
                        if old not in shapes or shape_list is None:continue
                        if key not in cache:
                            shape=deepcopy(shapes[old]);shape.set('Id',str(next_id));shape.set('KeepWithNext','true')
                            shape_list.append(shape);cache[key]=str(next_id);next_id+=1
                        heading.set('ParaShape',cache[key])
                break
        # Do not move an embedded/nested table outside its containing cell.
        # Only long generated text requires changing an inline table to flowing.
        # A size-budgeted cell that fits must not change the table's anchoring.
        # Protected values/blue notes may still require the safe overflow path.
        from .authoring_cell_budget import line_count
        grouped={}
        for _,value,field in written:grouped.setdefault(field['id'],(field,[]))[1].append(value)
        fits_budget=all(f.get('table_fit') and
                        sum(line_count(v,f['table_fit']['chars_per_line']) for v in values)<=
                        f['table_fit']['max_body_lines']+f['table_fit']['reserved_review_lines']
                        for f,values in grouped.values())
        if long and not fits_budget and ancestor(parents.get(id(table)),'CELL') is None:
            table.set('PageBreak','Cell')
            obj=table.find('SHAPEOBJECT')
            if obj is not None:
                obj.set('TextWrap','TopAndBottom')
                pos=obj.find('POSITION')
                if pos is not None:
                    pos.attrib.update(TreatAsChar='false',FlowWithText='true',AllowOverlap='false',
                                      VertRelTo='Para',VertAlign='Top',VertOffset='0')
                size=obj.find('SIZE')
                if size is not None:size.set('Protect','false')
    if shape_list is not None:shape_list.set('Count',str(len(shape_list)))
