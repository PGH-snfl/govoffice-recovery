"""Typeset conservative scientific tokens with the source font's script styles.

The character shape is cloned rather than substituting Unicode subscript glyphs,
which could silently switch fonts in an otherwise uniform paragraph or cell.
"""
from copy import deepcopy
import re
import xml.etree.ElementTree as ET

from .authoring_equations import FORMULA


SPECIAL = re.compile(
    r'(?<![A-Za-z0-9_])(?P<power>(?:[kMGT]?W)_?(?:th|e))(?![A-Za-z0-9_])'
    r'|(?<![A-Za-z0-9_])(?P<chemical>H_?2O|H_?2SO_?4|CO_?2(?:eq|e)?|CH_?4|NH_?3|H_?2|O_?2|N_?2|D_?2|T_?2)(?![A-Za-z0-9_])'
    r'|(?<![A-Za-z0-9_])(?P<area>(?:mm|cm|km|m)\^[23])(?![A-Za-z0-9_])'
    r'|(?<=/)(?P<slash_area>m[23])(?![A-Za-z0-9_])'
)


def _token_parts(match):
    if match.lastgroup == 'power':
        token = match.group()
        suffix = 'th' if token.endswith('th') else 'e'
        return [('base', token[:-len(suffix)].rstrip('_')), ('sub', suffix)]
    if match.lastgroup in {'area', 'slash_area'}:
        token = match.group()
        return [('base', token[:-2] if '^' in token else token[:-1]),
                ('super', token[-1])]
    token = match.group()
    parts = []
    for char in token:
        if char == '_':
            continue
        kind = 'sub' if char.isdigit() else 'base'
        if parts and parts[-1][0] == kind:
            parts[-1] = (kind, parts[-1][1] + char)
        else:
            parts.append((kind, char))
    return parts


def scientific_parts(value):
    """Return visual text runs, never reinterpret an algebraic equation span."""
    parts = []
    offset = 0
    for formula in FORMULA.finditer(value):
        parts.extend(_plain_parts(value[offset:formula.start()]))
        parts.append(('base', formula.group()))
        offset = formula.end()
    parts.extend(_plain_parts(value[offset:]))
    merged = []
    for kind, text in parts:
        if not text:
            continue
        if merged and merged[-1][0] == kind:
            merged[-1] = (kind, merged[-1][1] + text)
        else:
            merged.append((kind, text))
    return merged


def _plain_parts(value):
    parts = []
    offset = 0
    for match in SPECIAL.finditer(value):
        if match.start() > offset:
            parts.append(('base', value[offset:match.start()]))
        parts.extend(_token_parts(match))
        offset = match.end()
    if offset < len(value):
        parts.append(('base', value[offset:]))
    return parts


def display_value(value):
    return ''.join(text for _, text in scientific_parts(value))


def format_scientific_notation(root, refs):
    shape_list = root.find('.//CHARSHAPELIST')
    if shape_list is None:
        return 0
    shapes = {shape.get('Id'): shape for shape in shape_list}
    next_id = max((int(key) for key in shapes), default=-1) + 1
    cache = {}
    converted = 0

    def style(old, kind):
        nonlocal next_id
        if kind == 'base' or old not in shapes:
            return old
        key = old, kind
        if key not in cache:
            shape = deepcopy(shapes[old])
            shape.set('Id', str(next_id))
            for tag in ('SUBSCRIPT', 'SUPERSCRIPT'):
                for child in list(shape.findall(tag)):
                    shape.remove(child)
            ET.SubElement(shape, 'SUBSCRIPT' if kind == 'sub' else 'SUPERSCRIPT')
            shape_list.append(shape)
            shapes[str(next_id)] = shape
            cache[key] = str(next_id)
            next_id += 1
        return cache[key]

    for entry, paragraphs, _ in refs:
        if entry.get('source') != 'agent':
            continue
        for paragraph in paragraphs:
            for run in list(paragraph.findall('TEXT')):
                old = run.get('CharShape')
                if old not in shapes or not any(child.tag == 'CHAR' and
                                                any(kind != 'base' for kind, _ in scientific_parts(child.text or ''))
                                                for child in run):
                    continue
                replacement = []
                for child in list(run):
                    if child.tag != 'CHAR':
                        new_run = ET.Element('TEXT', dict(run.attrib))
                        new_run.append(child)
                        replacement.append(new_run)
                        continue
                    for kind, text in scientific_parts(child.text or ''):
                        new_run = ET.Element('TEXT', {**run.attrib, 'CharShape': style(old, kind)})
                        ET.SubElement(new_run, 'CHAR').text = text
                        replacement.append(new_run)
                        if kind != 'base':
                            converted += 1
                position = list(paragraph).index(run)
                paragraph.remove(run)
                for index, new_run in enumerate(replacement):
                    paragraph.insert(position + index, new_run)
    shape_list.set('Count', str(len(shape_list)))
    return converted
