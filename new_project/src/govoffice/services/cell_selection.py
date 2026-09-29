"""Project a native selection scan onto original cells without expanding it.

HWP 2018 exports the enclosing table for cell-block saveblock. The bounded
InitScan result is the content authority; XML is used only for cell structure.
Ambiguous rectangles and ranges cutting merged cells are rejected, not guessed.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import re
import xml.etree.ElementTree as ET


def compact(text: str) -> str:
    return ''.join(text.split())


def cell_cursor(indicator: str) -> tuple[int, int] | None:
    match = re.search(r'\(([A-Z]+)([1-9][0-9]*)\)', indicator)
    if not match:
        return None
    col = 0
    for char in match[1]:
        col = col * 26 + ord(char) - ord('A') + 1
    return int(match[2]) - 1, col - 1


@dataclass
class Cell:
    node: ET.Element
    row: int
    col: int
    bottom: int
    right: int
    text: str


def crop_scanned_cells(hwpml: str, scanned_text: str, cursor: tuple[int, int] | None):
    target = compact(scanned_text)
    if not target:
        raise ValueError('선택한 셀에 분석할 텍스트가 없습니다.')
    root = ET.fromstring(hwpml)
    tables = list(root.iter('TABLE'))
    if len(tables) != 1:
        raise ValueError('선택 셀의 표를 하나로 식별하지 못했습니다. 중첩 표는 별도로 선택하세요.')
    table = tables[0]
    cells = []
    for row in table.findall('ROW'):
        for node in row.findall('CELL'):
            try:
                r, c = int(node.attrib['RowAddr']), int(node.attrib['ColAddr'])
                rs, cs = int(node.get('RowSpan', '1')), int(node.get('ColSpan', '1'))
            except (KeyError, ValueError) as exc:
                raise ValueError('셀 주소를 확인하지 못해 선택 범위를 추측하지 않았습니다.') from exc
            if min(r, c) < 0 or min(rs, cs) < 1:
                raise ValueError('셀 주소 또는 병합 크기가 올바르지 않습니다.')
            text = ''.join(''.join(char.itertext()) for char in node.iter('CHAR'))
            cells.append(Cell(node, r, c, r + rs, c + cs, compact(text)))
    cells.sort(key=lambda cell: (cell.row, cell.col))
    if not cells or len(cells) > 5000:
        raise ValueError('선택 범위의 셀 구조를 안전하게 확인할 수 없습니다.')
    firsts = [cell for cell in cells if target.startswith(cell.text)]
    lasts = [cell for cell in cells if target.endswith(cell.text)]
    if len(firsts) * len(lasts) > 10000:
        raise ValueError('같은 내용 또는 빈 셀이 너무 많아 선택 범위를 확정하지 못했습니다.')
    matches = {}
    for first in firsts:
        for last in lasts:
            top, left, bottom, right = first.row, first.col, last.bottom, last.right
            if top >= bottom or left >= right:
                continue
            if cursor is not None and not (top <= cursor[0] < bottom and left <= cursor[1] < right):
                continue
            picked = [cell for cell in cells
                      if cell.row < bottom and cell.bottom > top and cell.col < right and cell.right > left]
            if not picked or any(cell.row < top or cell.col < left or cell.bottom > bottom or cell.right > right for cell in picked):
                continue  # Never enlarge a range to include a cut merged cell.
            if ''.join(cell.text for cell in picked) != target:
                continue
            # Reject holes/overlaps. This also avoids mistaking a nested or broken
            # table serialization for an actual rectangular selection.
            area = sum((cell.bottom-cell.row)*(cell.right-cell.col) for cell in picked)
            if area != (bottom-top)*(right-left):
                continue
            if any(a.row < b.bottom and a.bottom > b.row and a.col < b.right and a.right > b.col
                   for i, a in enumerate(picked) for b in picked[i+1:]):
                continue
            matches[(top,left,bottom,right)] = picked
    if len(matches) != 1:
        raise ValueError('선택한 내용에 대응하는 셀 범위를 하나로 확정하지 못했습니다. 표 전체로 대체하지 않았습니다.')
    (top,left,bottom,right), picked = next(iter(matches.items()))
    # Copy the original CELL nodes, including paragraphs, spans and run data.
    # Do not synthesize labels from lines or send enclosing-table text to analysis.
    result = ET.Element('HWPML')
    section = ET.SubElement(ET.SubElement(result, 'BODY'), 'SECTION')
    output_table = ET.SubElement(section, 'TABLE', dict(table.attrib))
    output_table.set('RowCount', str(bottom-top))
    output_table.set('ColCount', str(right-left))
    rows = {r: ET.SubElement(output_table, 'ROW') for r in range(top,bottom)}
    for cell in picked:
        node = deepcopy(cell.node)
        node.set('RowAddr', str(cell.row-top))
        node.set('ColAddr', str(cell.col-left))
        rows[cell.row].append(node)
    return ET.tostring(result, encoding='unicode'), {
        'source_cell_count': len(cells), 'selected_cell_count': len(picked),
        'selected_bounds': [top,left,bottom,right], 'selection_match_count': 1,
    }
