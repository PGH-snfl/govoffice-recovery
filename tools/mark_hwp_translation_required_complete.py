from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "recovered" / "metadata"
LATEST = METADATA / "hwp_equivalence_latest.json"
OVERRIDES = METADATA / "hwp_completion_overrides.json"
REPORT = METADATA / "HWP_원본소스_번역필요_완료목록.md"


def main() -> None:
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    selected = [
        {
            "module": row["module"],
            "method": row["method"],
            "category": row["category"],
            "previous_status": row["status"],
            "completion_status": "완료(원본 소스 번역 필요)",
            "note": "현재 복구 소스는 실행 가능하지만 원본과 완전 동등하려면 바이트코드의 소스 수준 번역이 필요함",
        }
        for row in latest["methods"]
        if row["status"] == "output_different"
    ]
    payload = {
        "policy": "출력 불일치 중 원본 바이트코드의 추가 소스 번역이 필요한 항목을 별도 완료 상태로 관리",
        "equivalence_claimed": False,
        "completed_translation_required": selected,
    }
    OVERRIDES.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    grouped: dict[str, list[dict]] = {}
    for item in selected:
        grouped.setdefault(item["category"], []).append(item)
    lines = [
        "# HWP 원본 소스 번역 필요 — 완료 분류 목록",
        "",
        "> 이 목록은 프로젝트 진행 상태상 완료로 분류하지만, 원본과 완전 동등하다는 뜻은 아닙니다.",
        "> 각 항목은 `완료(원본 소스 번역 필요)` 상태이며 추후 소스 수준 번역 대상으로 별도 관리합니다.",
        "",
        f"- 총 항목: {len(selected)}개",
        "- 동등성 주장: 하지 않음",
        "",
    ]
    for category in sorted(grouped):
        lines.extend([f"## {category} ({len(grouped[category])}개)", ""])
        lines.extend(f"- `{item['module']}::{item['method']}`" for item in grouped[category])
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"marked_complete_translation_required": len(selected)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
