"""Balanced tracking and word wrapping for generated text only.

Leave visible text, font family/height, paragraph alignment and fixed template
labels alone. HWP performs the actual line layout; never insert hard breaks.
"""
from copy import deepcopy
import re
import unicodedata
import xml.etree.ElementTree as ET


WORD_WRAP = {'BreakLatinWord': 'KeepWord', 'BreakNonLatinWord': 'false',
             'LineWrap': 'Break', 'Condense': '5'}
CHARACTER_WRAP = {'BreakLatinWord': 'BreakWord', 'BreakNonLatinWord': 'true'}
LANGUAGES = ('Hangul', 'Latin', 'Hanja', 'Japanese', 'Other', 'Symbol', 'User')
SOFT_BREAK='\u200b'
MIDDLE_DOT_GROUP=re.compile(r'(?<=\w)·(?=\w)')


def middle_dot_breaks(value):
    """Allow a line break after separators in grouped words, without a gap."""
    return MIDDLE_DOT_GROUP.sub('·'+SOFT_BREAK,value)


def visible_text(value):
    return value.replace(SOFT_BREAK,'')


def _text_units(value):
    return sum(0 if c==SOFT_BREAK else 1 if unicodedata.east_asian_width(c) in 'WF' else .6 for c in value)


def _line_widths(value, columns, spacing):
    """Estimate word-aware line fill; the final layout remains Hancom's job."""
    factor=1+spacing/100
    widths=[];used=0.;gap=0.
    for token in re.findall(r'\u200b|\s+|[^\s\u200b]+',value):
        if token==SOFT_BREAK:continue
        size=_text_units(token)*factor
        if token.isspace():gap+=size;continue
        if used and used+gap+size>columns:
            widths.append(used);used=0.;gap=0.
        used+=gap+size;gap=0.
        while used>columns and size>columns:
            widths.append(columns);used-=columns
    widths.append(used)
    return widths


def balanced_tracking(value, columns, original):
    """Try compression first; expand only to fix conspicuously ragged lines.

    Never widen a short isolated line, add a line to fill whitespace, or
    override an intentionally tight source style (below -5%).
    """
    original=int(original)
    if not value.strip() or columns is None or columns<4 or not -5<=original<=5:
        return original
    baseline=_line_widths(value,columns,original)
    def layout(spacing):
        widths=_line_widths(value,columns,spacing)
        ragged=sum((max(0,columns-width)/columns)**2 for width in widths)/len(widths)
        return len(widths),ragged
    choices=range(max(-5,original-5),min(5,original)+1)
    contraction=[spacing for spacing in choices if spacing<=original]
    def score(spacing):
        lines,ragged=layout(spacing)
        return lines*10+ragged+.002*abs(spacing-original)
    best=min(contraction,key=lambda spacing:(score(spacing),abs(spacing-original)))
    best_lines,best_ragged=layout(best)
    if best_lines<len(baseline) or best_ragged<.12:
        return best
    expansion=[spacing for spacing in range(original+1,min(5,original+3)+1)
               if layout(spacing)[0]<=best_lines]
    if not expansion:return best
    wider=min(expansion,key=lambda spacing:(score(spacing),spacing))
    # A little extra width is justified only by a visible improvement in line
    # balance, never merely to stretch ordinary short text.
    return wider if best_ragged-layout(wider)[1]>=.025 else best


def _available_columns(root, paragraph, parents, font_height):
    node=paragraph;cell=None
    while id(node) in parents:
        node=parents[id(node)]
        if node.tag=='CELL':cell=node;break
    if cell is not None:
        margin=cell.find('CELLMARGIN')
        width=int(cell.get('Width','0') or 0)
        if margin is not None:
            width-=int(margin.get('Left','0'))+int(margin.get('Right','0'))
    else:
        page=root.find('.//PAGEDEF');margin=root.find('.//PAGEMARGIN')
        if page is None:return None
        width=int(page.get('Width','0') or 0)
        if margin is not None:
            width-=sum(int(margin.get(side,'0')) for side in ('Left','Right','Gutter'))
    return width/font_height if width>0 and font_height>0 else None


def needs_character_wrap(value, columns):
    """Only relax word protection for an overlong symbol-bearing token."""
    if columns is None or columns<1:return False
    return any(_text_units(token)>columns*.95 and
               any(unicodedata.category(c)[0] in {'P','S'} for c in token)
               for token in re.findall(r'[^\s\u200b]+',value))


def format_word_wrapping(root, refs):
    paragraphs = {id(p): p for _, ps, _ in refs for p in ps}
    for paragraph in paragraphs.values():
        for run in paragraph.findall('TEXT'):
            for char in run.findall('CHAR'):
                if char.text:char.text=middle_dot_breaks(char.text)
    parents={id(c):p for p in root.iter() for c in p}
    char_shapes={s.get('Id'):s for s in root.iter('CHARSHAPE')}
    for kind, attr in (('PARA', 'ParaShape'), ('CHAR', 'CharShape')):
        shape_list = root.find('.//' + kind + 'SHAPELIST')
        if shape_list is None:
            continue
        shapes = {s.get('Id'): s for s in shape_list}
        next_id = max([int(k) for k in shapes] + [-1]) + 1
        cache = {}
        nodes = ([(p,p) for p in paragraphs.values()] if kind == 'PARA' else
                 [(p,t) for p in paragraphs.values() for t in p.findall('TEXT')
                  if any(c.text for c in t.findall('CHAR'))])
        for paragraph,node in nodes:
            old = node.get(attr)
            if old not in shapes:
                continue
            adjustment=0
            character_wrap=False
            if kind == 'PARA':
                run=paragraph.find('TEXT')
                char=char_shapes.get(run.get('CharShape')) if run is not None else None
                if char is not None:
                    value=''.join(c.text or '' for t in paragraph.findall('TEXT') for c in t.findall('CHAR'))
                    columns=_available_columns(root,paragraph,parents,int(char.get('Height','1000')))
                    character_wrap=needs_character_wrap(value,columns)
            if kind == 'CHAR':
                shape=shapes[old]
                source=shape.find('CHARSPACING')
                original=int(source.get('Hangul','0')) if source is not None else 0
                value=''.join(c.text or '' for c in node.findall('CHAR'))
                columns=_available_columns(root,paragraph,parents,int(shape.get('Height','1000')))
                adjustment=balanced_tracking(value,columns,original)-original
            key=(old,adjustment,character_wrap)
            if key not in cache:
                shape = deepcopy(shapes[old])
                shape.set('Id', str(next_id))
                if kind == 'PARA':
                    shape.attrib.update(WORD_WRAP)
                    if character_wrap:shape.attrib.update(CHARACTER_WRAP)
                else:
                    spacing = shape.find('CHARSPACING')
                    if spacing is None:
                        spacing = ET.Element('CHARSPACING')
                        # HWPML character child order: FONTID, RATIO, CHARSPACING,
                        # RELSIZE, CHAROFFSET, decoration elements.
                        before = next((i for i, c in enumerate(shape)
                                       if c.tag not in {'FONTID', 'RATIO'}), len(shape))
                        shape.insert(before, spacing)
                    for language in LANGUAGES:
                        current=int(spacing.get(language,'0'))
                        spacing.set(language,str(max(-5,min(5,current+adjustment))
                                                 if -5<=current<=5 else current))
                shape_list.append(shape)
                cache[key] = str(next_id)
                next_id += 1
            node.set(attr, cache[key])
        shape_list.set('Count', str(len(shape_list)))
