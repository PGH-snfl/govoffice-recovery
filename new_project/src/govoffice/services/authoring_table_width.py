"""Conservatively share width between plain table columns after writing text.

The table's total width, row/column count, borders and cell merges are never
changed. Complex or nested tables retain their source geometry.
"""
from .authoring_cell_budget import line_count


def rebalance_written_tables(root, refs, fields):
    parents={id(c):p for p in root.iter() for c in p}
    chars={s.get('Id'):s for s in root.iter('CHARSHAPE')}
    written={id(p) for _,paragraphs,_ in refs for p in paragraphs}

    def ancestor(node,tag):
        while node is not None:
            if node.tag==tag:return node
            node=parents.get(id(node))

    touched=set()
    for _,paragraphs,_ in refs:
        for p in paragraphs:
            table=ancestor(parents.get(id(p)),'TABLE')
            if table is not None:touched.add(table)

    changes=[]
    for table in touched:
        rows=[row.findall('CELL') for row in table.findall('ROW')]
        if not rows or not 2<=len(rows[0])<=6 or any(len(row)!=len(rows[0]) for row in rows):continue
        if table.find('CELLZONELIST') is not None or ancestor(parents.get(id(table)),'CELL') is not None:continue
        if any(cell.get('ColSpan','1')!='1' or cell.get('RowSpan','1')!='1' or
               cell.find('.//TABLE') is not None for row in rows for cell in row):continue
        if any(any(child.tag!='CHAR' for text in cell.iter('TEXT') for child in text)
               for row in rows for cell in row):continue
        if any(any(cell.get('ColAddr',str(col))!=rows[0][col].get('ColAddr',str(col))
                   for col,cell in enumerate(row)) for row in rows):continue
        widths=[int(cell.get('Width','0') or 0) for cell in rows[0]]
        if min(widths)<=0 or any([int(cell.get('Width','0') or 0) for cell in row]!=widths for row in rows):continue
        if table.get('ColCount') and int(table.get('ColCount'))!=len(widths):continue

        def metric(cell,width,generated_only=False):
            row=parents.get(id(cell))
            row_height=max(int(other.get('Height','0') or 0) for other in row.findall('CELL'))
            margin=cell.find('CELLMARGIN') if cell.get('HasMargin')=='true' else table.find('INSIDEMARGIN')
            padding={side:int(margin.get(side,'0')) if margin is not None else 0
                     for side in ('Left','Right','Top','Bottom')}
            for side in ('Left','Right'):
                padding[side]=min(max(padding[side],min(283,width//14)),width//5)
            for side in ('Top','Bottom'):padding[side]=max(141,padding[side])
            usable=max(1,width-padding['Left']-padding['Right'])
            lines=0;maximum_font=1000;has_written=False
            for p in cell.findall('PARALIST/P'):
                value=''.join(c.text or '' for t in p.findall('TEXT') for c in t.findall('CHAR')).strip()
                if not value:continue
                run=p.find('TEXT');shape=chars.get(run.get('CharShape')) if run is not None else None
                font=int(shape.get('Height','1000')) if shape is not None else 1000
                maximum_font=max(maximum_font,font)
                lines+=line_count(value,max(1,usable/font))
                has_written|=id(p) in written
            if generated_only and not has_written:return 0,maximum_font,False,lines
            capacity=max(1,int(max(0,row_height-padding['Top']-padding['Bottom'])/(maximum_font*1.45)))
            return max(0,lines-capacity),maximum_font,has_written,lines

        before=[sum(metric(row[col],widths[col],True)[0] for row in rows)
                for col in range(len(widths))]
        candidates=[col for col,overflow in enumerate(before) if overflow>0 and
                    any(any(id(p) in written for p in row[col].findall('PARALIST/P')) for row in rows)]
        best=None
        for target in candidates:
            for donor in range(len(widths)):
                if donor==target or before[donor]:continue
                donor_font=max(metric(row[donor],widths[donor])[1] for row in rows)
                donor_floor=max(int(widths[donor]*.65),donor_font*4)
                limit=min(int(widths[target]*.30),int(widths[donor]*.20),widths[donor]-donor_floor)
                for step in range(1,7):
                    delta=int(widths[target]*.05*step)
                    if delta<=0 or delta>limit:continue
                    # A donor's fixed labels and written values must not gain
                    # another line merely to make room elsewhere.
                    if any(metric(row[donor],widths[donor]-delta)[3]>
                           metric(row[donor],widths[donor])[3] for row in rows):continue
                    after=sum(metric(row[target],widths[target]+delta,True)[0] for row in rows)
                    gain=before[target]-after
                    if gain<=0:continue
                    choice=(gain,-delta,target,donor,delta)
                    if best is None or choice>best:best=choice
        if best is None:continue
        _,_,target,donor,delta=best
        for row in rows:
            row[target].set('Width',str(widths[target]+delta))
            row[donor].set('Width',str(widths[donor]-delta))
        changes.append({'target':target,'donor':donor,'width_added':delta})
    return changes
