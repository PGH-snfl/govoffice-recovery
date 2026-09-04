"""정적 비교와 분산된 동적 검증 결과를 메서드별 최신 상태로 집계한다."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "recovered" / "metadata"
COMPLETION_OVERRIDES = METADATA / "hwp_completion_overrides.json"


def classification(result: dict) -> str:
    if result.get("timed_out") or result.get("timeout"):
        return "timeout"
    comparison = result.get("comparison", {})
    legacy = result.get("legacy", {})
    recovered = result.get("recovered", {})
    if comparison.get("both_ok"):
        if (
            comparison.get("text_equal")
            and comparison.get("hwpml_equal")
            and comparison.get("return_equal")
        ):
            return "dynamic_exact"
        return "output_different"
    if comparison.get("outcome_equal") and comparison.get("error_type_equal"):
        return "same_error"
    if not recovered.get("ok", False):
        return "recovered_error"
    if not legacy.get("ok", False):
        return "legacy_error"
    return "different"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=METADATA / "hwp_equivalence_latest.json")
    parser.add_argument("--export-status")
    args = parser.parse_args()

    inventory = json.loads((METADATA / "hwp_equivalence_inventory.json").read_text(encoding="utf-8"))
    inventory_rows = inventory["methods"]
    completion_overrides = set()
    validation_blocked_overrides = set()
    if COMPLETION_OVERRIDES.exists():
        payload = json.loads(COMPLETION_OVERRIDES.read_text(encoding="utf-8"))
        completion_overrides = {
            (item["module"], item["method"])
            for item in payload.get("completed_translation_required", [])
        }
        validation_blocked_overrides = {
            (item["module"], item["method"])
            for item in payload.get("completed_validation_blocked", [])
        }
    method_keys = {(row["module"], row["method"]) for row in inventory_rows}
    latest: dict[tuple[str, str], dict] = {}

    excluded = {"hwp_equivalence_inventory.json", args.output.name}
    candidates = sorted(
        (path for path in METADATA.glob("*.json") if path.name not in excluded),
        key=lambda path: (path.stat().st_mtime_ns, path.name),
    )
    for path in candidates:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        results = payload.get("results") if isinstance(payload, dict) else None
        if not isinstance(results, list):
            continue
        for result in results:
            if not isinstance(result, dict) or "method" not in result:
                continue
            module = result.get("module")
            if module is None:
                matches = [key for key in method_keys if key[1] == result["method"]]
                if len(matches) != 1:
                    continue
                module = matches[0][0]
            key = (module, result["method"])
            if key not in method_keys:
                continue
            latest[key] = {
                "source": path.name,
                "classification": classification(result),
                "comparison": result.get("comparison", {}),
                "legacy": {k: v for k, v in result.get("legacy", {}).items() if k != "hwpml" and k != "text"},
                "recovered": {k: v for k, v in result.get("recovered", {}).items() if k != "hwpml" and k != "text"},
            }

    rows = []
    for row in inventory_rows:
        key = (row["module"], row["method"])
        if key in validation_blocked_overrides:
            status, source = "completed_validation_blocked", COMPLETION_OVERRIDES.name
        elif key in completion_overrides:
            status, source = "completed_translation_required", COMPLETION_OVERRIDES.name
        elif row.get("static_instruction_exact"):
            status, source = "static_exact", "hwp_equivalence_inventory.json"
        elif key in latest:
            status, source = latest[key]["classification"], latest[key]["source"]
        else:
            status, source = "not_tested", None
        rows.append({
            "module": key[0], "class": row["class"], "method": key[1],
            "category": row["category"], "status": status, "source": source,
        })

    counts = Counter(row["status"] for row in rows)
    exact = counts["static_exact"] + counts["dynamic_exact"] + counts["same_error"]
    translation_required = counts["completed_translation_required"]
    validation_blocked = counts["completed_validation_blocked"]
    completed = exact + translation_required + validation_blocked
    report = {
        "total": len(rows),
        "fully_equivalent": exact,
        "completed": completed,
        "completed_translation_required": translation_required,
        "completed_validation_blocked": validation_blocked,
        "remaining": len(rows) - completed,
        "equivalence_remaining": len(rows) - exact,
        "counts": dict(sorted(counts.items())),
        "methods": rows,
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.export_status:
        categories = sorted({row["category"] for row in rows if row["status"] == args.export_status})
        for category in categories:
            selected = [
                {"module": row["module"], "method": row["method"]}
                for row in rows
                if row["status"] == args.export_status and row["category"] == category
            ]
            target = METADATA / f"retry_latest_{args.export_status}_{category}.json"
            target.write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"exported {len(selected)}: {target.name}")
    print(json.dumps({k: report[k] for k in ("total", "fully_equivalent", "completed", "completed_translation_required", "completed_validation_blocked", "remaining", "equivalence_remaining", "counts")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
