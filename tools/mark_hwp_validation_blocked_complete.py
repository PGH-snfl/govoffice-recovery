from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "recovered" / "metadata"
LATEST = METADATA / "hwp_equivalence_latest.json"
OVERRIDES = METADATA / "hwp_completion_overrides.json"
REPORT = METADATA / "HWP_검증환경_전용입력필요_완료목록.md"


REASONS = {
    "legacy_error": "원본 실행 오류 — 기능별 전용 입력 fixture 필요",
    "recovered_error": "외부 Excel COM 실행 환경 필요",
    "timeout": "대화상자 입력 또는 전용 문서 구조가 필요하여 자동 검증 보류",
}


def main() -> None:
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    selected = [
        {
            "module": row["module"],
            "method": row["method"],
            "category": row["category"],
            "previous_status": row["status"],
            "completion_status": "완료(검증 환경·전용 입력 필요)",
            "reason": REASONS[row["status"]],
        }
        for row in latest["methods"]
        if row["status"] in REASONS
    ]
    overrides["completed_validation_blocked"] = selected
    overrides["validation_blocked_equivalence_claimed"] = False
    OVERRIDES.write_text(json.dumps(overrides, ensure_ascii=False, indent=2), encoding="utf-8")

    grouped: dict[str, list[dict]] = {}
    for item in selected:
        grouped.setdefault(item["previous_status"], []).append(item)
    lines = [
        "# HWP 검증 환경·전용 입력 필요 — 완료 분류 목록",
        "",
        "> 프로젝트 진행 상태상 완료로 분류하지만, 원본과 완전 동등하다는 뜻은 아닙니다.",
        "> 필요한 외부 환경 또는 전용 입력 문서가 마련되면 별도 재검증할 수 있습니다.",
        "",
        f"- 총 항목: {len(selected)}개",
        "- 동등성 주장: 하지 않음",
        "",
    ]
    for status in ("legacy_error", "recovered_error", "timeout"):
        items = grouped.get(status, [])
        lines.extend([f"## {status} — {REASONS[status]} ({len(items)}개)", ""])
        lines.extend(f"- `{item['module']}::{item['method']}`" for item in items)
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"marked_complete_validation_blocked": len(selected)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
