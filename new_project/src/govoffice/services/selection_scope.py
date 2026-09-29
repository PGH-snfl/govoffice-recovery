"""Conservative cross-check of native selection exports; never guesses a range."""
from __future__ import annotations

import xml.etree.ElementTree as ET


def assert_same_selection_text(hwpml: str, selected_text: str) -> None:
    """Reject a wider structured block instead of searching by matching values.

    Preserve sequence and repeated values. Ignore only whitespace differences
    between the two serialization formats. This is a safety check, not a cell
    coordinate API: it cannot prove native TEXT/saveblock itself is correct.
    """
    if not isinstance(selected_text, str) or not selected_text.strip():
        raise ValueError("현재 선택 영역의 텍스트를 확인하지 못해 가져오기를 중단했습니다.")
    try:
        root = ET.fromstring(hwpml)
    except ET.ParseError as exc:
        raise ValueError("선택 영역의 서식 데이터를 해석하지 못했습니다.") from exc
    tag = lambda node: node.tag.rsplit('}', 1)[-1].upper()
    bodies = [node for node in root.iter() if tag(node) == 'BODY']
    if len(bodies) != 1:
        raise ValueError("선택 영역의 본문 범위를 확인하지 못했습니다.")
    structured_text = ''.join(
        ''.join(node.itertext()) for node in bodies[0].iter() if tag(node) == 'CHAR'
    )
    canonical = lambda value: ''.join(value.split())
    if canonical(structured_text) != canonical(selected_text):
        raise ValueError(
            "선택한 텍스트와 읽어 온 셀 내용의 범위가 달라 가져오기를 중단했습니다. "
            "표 전체나 이전 선택으로 대체하지 않았습니다."
        )
