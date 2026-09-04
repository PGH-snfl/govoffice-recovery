from __future__ import annotations

import argparse
import importlib
import inspect
import json
import sys
from pathlib import Path


RECOVERED_MODULES = {
    "한컴라이브러리_기본": ("한컴오피스.한컴라이브러리_기본", "한컴기본"),
    "한컴라이브러리_1": ("한컴오피스.한컴라이브러리_1", "한컴1"),
    "한컴라이브러리_2": ("한컴오피스.한컴라이브러리_2", "한컴2"),
    "한컴라이브러리": ("한컴오피스.한컴라이브러리", "기본한컴"),
}


def signature_shape(callable_object) -> list[str]:
    return [parameter.name for parameter in inspect.signature(callable_object).parameters.values()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("recovered_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    sys.path.insert(0, str(args.recovered_root.resolve()))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    report = {
        "modules": {},
        "totals": {
            "expected": 0,
            "recovered": 0,
            "source_recovered": 0,
            "bytecode_backed": 0,
            "missing": 0,
            "signature_mismatch": 0,
        },
    }

    for module_name, module_data in manifest["modules"].items():
        import_name, class_name = RECOVERED_MODULES[module_name]
        try:
            recovered_module = importlib.import_module(import_name)
            recovered_class = getattr(recovered_module, class_name)
            bytecode_backed_names = set(
                getattr(recovered_module, "BYTECODE_BACKED_METHODS", ())
            )
        except (ImportError, AttributeError):
            recovered_class = None
            bytecode_backed_names = set()

        recovered = []
        missing = []
        signature_mismatch = []
        source_recovered = []
        bytecode_backed = []
        for method in module_data["methods"]:
            expected_args = method["args"]
            actual = getattr(recovered_class, method["name"], None) if recovered_class else None
            if not callable(actual):
                missing.append(method["name"])
                continue
            actual_args = signature_shape(actual)
            if actual_args != expected_args:
                signature_mismatch.append(
                    {"name": method["name"], "expected": expected_args, "actual": actual_args}
                )
                continue
            recovered.append(method["name"])
            if method["name"] in bytecode_backed_names:
                bytecode_backed.append(method["name"])
            else:
                source_recovered.append(method["name"])

        module_report = {
            "class": class_name,
            "expected": len(module_data["methods"]),
            "recovered": recovered,
            "source_recovered": source_recovered,
            "bytecode_backed": bytecode_backed,
            "missing": missing,
            "signature_mismatch": signature_mismatch,
        }
        report["modules"][module_name] = module_report
        report["totals"]["expected"] += module_report["expected"]
        report["totals"]["recovered"] += len(recovered)
        report["totals"]["source_recovered"] += len(source_recovered)
        report["totals"]["bytecode_backed"] += len(bytecode_backed)
        report["totals"]["missing"] += len(missing)
        report["totals"]["signature_mismatch"] += len(signature_mismatch)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["totals"], ensure_ascii=False))


if __name__ == "__main__":
    main()
