"""Keep labels, badges and other decorative table cells out of writing slots."""
import re
from copy import deepcopy


def _text(node):
    return ''.join(c.text or '' for c in node.iter('CHAR')).strip()


def title_strip_tables(root):
    """Require a number badge AND a short wide title, not merely colour/width."""
    result=[]
    for table in root.iter('TABLE'):
        rows=table.findall('ROW')
        if len(rows)!=1:continue
        cells=rows[0].findall('CELL')
        if not 2<=len(cells)<=4:continue
        widths=[int(c.get('Width','0') or 0) for c in cells]
        texts=[_text(c) for c in cells]
        if (sum(widths)>0 and re.fullmatch(r'(?:\d{1,2}|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)[.)]?',texts[0])
                and widths[0]<sum(widths)*.25 and widths[-1]>sum(widths)*.5
                and 1<len(texts[-1])<180 and not any(texts[1:-1])
                and len([p for p in cells[-1].iter('P') if _text(p)])==1
                and not any(c.find('.//TABLE') is not None for c in cells)):
            result.append(table)
    return result


def _structure(root):
    ps=list(root.iter('P'));parents={id(c):p for p in root.iter() for c in p};indices={id(p):i for i,p in enumerate(ps)}
    def ancestor(node,tag):
        while id(node) in parents:
            node=parents[id(node)]
            if node.tag==tag:return node
    return ps,parents,indices,ancestor


def structural_design_indices(root):
    """Find blank separator cells in numbered section-title design strips."""
    _,_,indices,_=_structure(root);protected=set()
    for table in title_strip_tables(root):
        protected.update(indices[id(p)] for p in table.iter('P'))
    for row in root.iter('ROW'):
        cells=row.findall('CELL')
        for position,cell in enumerate(cells):
            width=int(cell.get('Width','0') or 0)
            value=''.join(''.join(p.itertext()) for p in cell.iter('P')).strip()
            before=(''.join(cells[position-1].itertext()).strip() if position else '')
            after=(''.join(cells[position+1].itertext()).strip() if position+1<len(cells) else '')
            if width<=1000 and not value and re.fullmatch(r'\d{1,2}',before) and after:
                protected.update(indices[id(p)] for p in cell.iter('P'))
    return protected


def writing_routes(root, fields):
    """Route body text out of title strips and fixed label cells.

    Original IDs/indices remain the saved-response identity. Destinations are
    recomputed from the immutable source, never trusted from imported metadata.
    """
    ps,parents,indices,ancestor=_structure(root)
    protected=decorative_field_indices(root,fields);routes={}
    strips={id(t) for t in title_strip_tables(root)}
    for field in fields:
        index=field['index'];p=ps[index];table=ancestor(p,'TABLE');cell=ancestor(p,'CELL')
        target=None;reason=None
        if table is not None and id(table) in strips:
            if _text(p) and not re.fullmatch(r'\d{1,2}',_text(p)):
                target=ancestor(table,'P');reason='제목 막대 아래 본문'
        elif cell is not None and _text(p) and field.get('role')!='personal':
            row=parents[id(cell)];cells=row.findall('CELL')
            if len(cells)>=2 and cell is cells[0]:
                right=cells[1];left_width=int(cell.get('Width','0') or 0)
                right_width=int(right.get('Width','0') or 0)
                label=_text(cell)
                if (0<left_width<right_width*.5 and 0<len(label)<80
                        and len([q for q in cell.iter('P') if _text(q)])==1
                        and _text(right) not in {'내용','작성내용','작성 내용'}):
                    candidates=[q for q in right.findall('PARALIST/P')
                                if not any(c.tag!='CHAR' for t in q.findall('TEXT') for c in t)]
                    if candidates:
                        target=candidates[0];reason='항목명 오른쪽 내용 칸'
                        protected.update(indices[id(q)] for q in cell.iter('P'))
        if target is not None:
            routes[field['id']]={'index':indices[id(target)],'original':_own_text(target),
                'insert_after':True,'in_table':ancestor(target,'CELL') is not None,'reason':reason}
    return protected,routes


def _own_text(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag=='CHAR')


def safe_writing_manifest(root, manifest):
    effective=deepcopy(manifest)
    fields=[f for t in effective.get('topics',[]) for f in t.get('fields',[])]
    protected,routes=writing_routes(root,fields)
    for field in fields:
        field.pop('write_target',None)
        field.pop('write_blocked',None)
        if field['id'] in routes:
            field.update(routes[field['id']])
            field.pop('style_from_index',None)
        elif field['index'] in protected:
            field['write_blocked']=True
    effective['protected_design_indices']=sorted(protected)
    return effective


def decorative_field_indices(root, fields):
    """Return blank fields whose label comes from a narrow numeric badge cell."""
    ps,_,_,ancestor=_structure(root);protected=structural_design_indices(root)
    for field in fields:
        index=field.get('index');label=str(field.get('label') or field.get('context') or '').strip()
        if not isinstance(index,int) or not 0<=index<len(ps) or not re.fullmatch(r'\d{1,2}',label):continue
        cell=ancestor(ps[index],'CELL')
        if cell is not None and int(cell.get('Width','0') or 0)<=1000:
            protected.add(index)
    return protected


def classify_tables(root, manifest, protected_indices=None):
    """Record whether each table is design-only, input, or mixed."""
    ps,_,_,ancestor=_structure(root);tables=list(root.iter('TABLE'))
    protected=set(protected_indices or ())|structural_design_indices(root)
    fields=[f for topic in manifest.get('topics',[]) for f in topic.get('fields',[])]
    rows=[]
    for number,table in enumerate(tables):
        present=[f for f in fields if ancestor(ps[f['index']],'TABLE') is table]
        locked=[f for f in present if f['index'] in protected]
        inputs=[f for f in present if f['index'] not in protected]
        protected_here=any(i in protected for i,p in enumerate(ps) if ancestor(p,'TABLE') is table)
        role='mixed' if protected_here and inputs else ('input' if inputs else 'design' if protected_here else 'static')
        rows.append({'table_index':number,'role':role,'input_field_ids':[f['id'] for f in inputs],
                     'protected_field_ids':[f['id'] for f in locked]})
    manifest['table_roles']=rows
    return rows


def remove_decorative_fields(root, manifest):
    fields=[f for topic in manifest.get('topics',[]) for f in topic.get('fields',[])]
    protected,routes=writing_routes(root,fields)
    classify_tables(root,manifest,protected)
    if not protected:return []
    removed=[]
    for topic in manifest['topics']:
        keep=[]
        for field in topic.get('fields',[]):
            if field['id'] in routes:
                field['write_target']=routes[field['id']];keep.append(field)
            elif field['index'] in protected:removed.append(field)
            else:keep.append(field)
        topic['fields']=keep
    manifest['manual_topics']=[t['title'] for t in manifest['topics'] if not t.get('fields')]
    if removed:
        manifest.setdefault('notes',[]).append(
            '좁은 숫자 표시칸은 디자인 영역으로 보호하여 글자를 입력하지 않습니다: '+', '.join(f['id'] for f in removed))
    return removed
