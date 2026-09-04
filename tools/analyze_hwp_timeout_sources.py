"""동적 검증 타임아웃 함수의 소스상 정체 위험 지점을 찾는다."""

from __future__ import annotations

import ast
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "recovered"
META = RECOVERED / "metadata"
SOURCE = RECOVERED / "한컴오피스" / "recovered_source"

CALL_RISKS = {
    "dialog": {"askopenfilename", "askopenfilenames", "asksaveasfilename", "불러오기"},
    "external_com": {"EnsureDispatch", "Dispatch", "DispatchEx"},
    "file_io": {"Open", "SaveAs", "FileOpen", "FileSaveAs", "InsertFile"},
    "document_clone": {"Copy", "Paste", "SelectAll", "새창"},
    "scan": {"InitScan", "GetText", "ReleaseScan", "블록스캔"},
}


def call_name(node: ast.Call) -> str:
    fn = node.func
    if isinstance(fn, ast.Name):
        return fn.id
    if isinstance(fn, ast.Attribute):
        return fn.attr
    return ""


def index_functions():
    found = {}
    for path in SOURCE.rglob("*.py"):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.setdefault(node.name, []).append((path, node))
    return found


def analyze(node: ast.FunctionDef):
    calls = [call_name(item) for item in ast.walk(node) if isinstance(item, ast.Call)]
    risks = []
    loops = [item for item in ast.walk(node) if isinstance(item, (ast.For, ast.While))]
    unbounded = [item for item in loops if isinstance(item, ast.While) and isinstance(item.test, ast.Constant) and item.test.value is True]
    if unbounded:
        risks.append("unbounded_while")
    elif loops:
        risks.append("loop")
    for label, names in CALL_RISKS.items():
        if names.intersection(calls):
            risks.append(label)
    if node.name in calls:
        risks.append("direct_recursion")
    if len(list(ast.walk(node))) > 400:
        risks.append("large_function")
    return sorted(set(risks)), Counter(calls).most_common(12)


def main():
    latest = json.loads((META / "hwp_equivalence_latest.json").read_text(encoding="utf-8"))
    targets = [row for row in latest["methods"] if row["status"] == "timeout"]
    functions = index_functions()
    rows = []
    for row in targets:
        candidates = functions.get(row["method"], [])
        if not candidates:
            rows.append({**row, "source": None, "line": None, "risks": ["source_not_found"]})
            continue
        path, node = candidates[0]
        risks, calls = analyze(node)
        rows.append({
            **row,
            "source": str(path.relative_to(ROOT)),
            "line": node.lineno,
            "risks": risks or ["hwp_com_or_fixture_wait"],
            "top_calls": calls,
        })
    counts = Counter(risk for row in rows for risk in row["risks"])
    report = {"total": len(rows), "risk_counts": dict(counts.most_common()), "methods": rows}
    (META / "hwp_timeout_source_analysis.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"total": len(rows), "risk_counts": report["risk_counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
