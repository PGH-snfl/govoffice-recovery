"""Build a complete verification inventory for every original HWP API."""

from __future__ import annotations

import inspect
import json
import sys
import types
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "recovered"
sys.path.insert(0, str(RECOVERED))

from 한컴오피스.compat.legacy_runtime import (  # noqa: E402
    Legacy기본한컴,
    Legacy한컴1,
    Legacy한컴2,
    Legacy한컴기본,
)
from 한컴오피스.한컴라이브러리 import 기본한컴  # noqa: E402
from 한컴오피스.한컴라이브러리_1 import 한컴1  # noqa: E402
from 한컴오피스.한컴라이브러리_2 import 한컴2  # noqa: E402
from 한컴오피스.한컴라이브러리_기본 import 한컴기본  # noqa: E402


CLASS_MAP = {
    "한컴라이브러리_기본": (Legacy한컴기본, 한컴기본),
    "한컴라이브러리_1": (Legacy한컴1, 한컴1),
    "한컴라이브러리_2": (Legacy한컴2, 한컴2),
    "한컴라이브러리": (Legacy기본한컴, 기본한컴),
}

INTERACTIVE = {
    "filedialog", "askopenfilename", "asksaveasfilename", "ShowDialog",
    "Print", "PrintToPDF", "Save", "SaveAs", "FileOpen", "FileSaveAs",
}
FILE_TOKENS = {
    "Open", "InsertPicture", "Picture", "CreateItemFromFile", "FilePath",
}
TABLE_TOKENS = {"Table", "Cell", "FindCtrl", "ShapeObjTable"}
IMAGE_ARG_TOKENS = ("이미지", "그림", "로고", "사진", "파일", "경로")


def string_constants(value) -> list[str]:
    code = getattr(value, "__code__", None)
    if code is None:
        return []
    result = []
    for item in code.co_consts:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, types.CodeType):
            result.extend(
                nested for nested in item.co_consts if isinstance(nested, str)
            )
    return result


def classify(method: dict, constants: list[str]) -> tuple[str, str]:
    calls = set(method.get("calls", []))
    args = method.get("args", [])[1:]
    joined_calls = " ".join([*map(str, calls), *constants])
    if calls & INTERACTIVE or any(token in joined_calls for token in INTERACTIVE):
        return "isolated_interactive", "파일·저장·인쇄 또는 대화상자 호출"
    if any(token in joined_calls for token in FILE_TOKENS) or any(
        token in str(arg) for arg in args for token in IMAGE_ARG_TOKENS
    ):
        return "file_fixture", "파일 또는 이미지 fixture 필요"
    if any(token in joined_calls for token in TABLE_TOKENS):
        return "table_fixture", "표/개체가 포함된 문서 fixture 필요"
    if not args:
        return "blank_document", "빈 문서 격리 실행 가능 후보"
    return "argument_fixture", "인수 fixture 필요"


def main() -> None:
    manifest_path = RECOVERED / "metadata" / "hwp_api_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = []
    for module_name, module in manifest["modules"].items():
        legacy_class, recovered_class = CLASS_MAP[module_name]
        for method in module["methods"]:
            name = method["name"]
            legacy_value = getattr(legacy_class, name, None)
            recovered_value = getattr(recovered_class, name, None)
            constants = string_constants(legacy_value)
            category, reason = classify(method, constants)
            source_file = None
            if recovered_value is not None:
                try:
                    source_file = str(Path(inspect.getsourcefile(recovered_value)).relative_to(ROOT))
                except (TypeError, ValueError):
                    source_file = inspect.getsourcefile(recovered_value)
            rows.append(
                {
                    "module": module_name,
                    "class": module["class"],
                    "method": name,
                    "args": method.get("args", []),
                    "calls": method.get("calls", []),
                    "string_constants": constants,
                    "bytecode_size": method.get("bytecode_size"),
                    "instruction_count": method.get("instruction_count"),
                    "legacy_present": callable(legacy_value),
                    "recovered_present": callable(recovered_value),
                    "recovered_source": source_file,
                    "category": category,
                    "reason": reason,
                    "status": "pending",
                }
            )
    counts = Counter(row["category"] for row in rows)
    result = {
        "total": len(rows),
        "category_counts": dict(sorted(counts.items())),
        "missing_legacy": sum(not row["legacy_present"] for row in rows),
        "missing_recovered": sum(not row["recovered_present"] for row in rows),
        "methods": rows,
    }
    output = RECOVERED / "metadata" / "hwp_equivalence_inventory.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "methods"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
