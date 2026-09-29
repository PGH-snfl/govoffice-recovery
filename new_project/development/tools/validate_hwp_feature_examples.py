from __future__ import annotations

import argparse
import json
from pathlib import Path

from win32com.client import DispatchEx


SECTION_MARKERS = [
    "1. 문서 기본정보 및 개인정보 치환",
    "2. 글자·문단 기본 기능",
    "3. 제목·목차·보기변환 확인",
    "4. 표 서식·정렬·스타일 제거 확인",
    "5. 시간계획·일정표 확인",
    "6. 점수분배 시험",
    "7. 서식 복사·프리셋 저장 선택영역",
    "8. 빈칸 유지 및 내용만 교체",
]


def read_document(path: Path, expected: list[str]) -> dict[str, object]:
    hwp = DispatchEx("HWPFrame.HwpObject")
    try:
        registered = bool(
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")
        )
        hwp.XHwpWindows.Item(0).Visible = False
        opened = hwp.Open(str(path), "HWP", "forceopen:true")
        text = hwp.GetTextFile("TEXT", "")
        section_checks = {marker: marker in text for marker in SECTION_MARKERS}
        expected_checks = {value: value in text for value in expected}
        return {
            "path": str(path),
            "size": path.stat().st_size,
            "ole_header": path.read_bytes()[:8].hex() == "d0cf11e0a1b11ae1",
            "security_registered": registered,
            "opened": bool(opened),
            "text_length": len(text),
            "pages": int(hwp.PageCount),
            "section_count": sum(section_checks.values()),
            "all_sections": all(section_checks.values()),
            "expected_content": expected_checks,
            "valid": (
                bool(opened)
                and len(text) > 500
                and all(section_checks.values())
                and all(expected_checks.values())
            ),
        }
    finally:
        try:
            hwp.HAction.Run("FileClose")
        finally:
            hwp.Quit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    args = parser.parse_args()
    results = [
        read_document(args.first.resolve(), ["서울과학기술대학교", "홍길동"]),
        read_document(args.second.resolve(), ["한빛연구원", "김하늘"]),
    ]
    print(json.dumps(results, ensure_ascii=True, indent=2))
    if not all(item["valid"] for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
