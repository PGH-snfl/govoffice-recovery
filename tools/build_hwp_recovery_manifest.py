from __future__ import annotations

import argparse
import json
from pathlib import Path


MODULES = {
    "한컴라이브러리_기본": "한컴기본",
    "한컴라이브러리_1": "한컴1",
    "한컴라이브러리_2": "한컴2",
    "한컴라이브러리": "기본한컴",
}


def direct_methods(inventory: list[dict], class_name: str) -> list[dict]:
    prefix = f"<module>.{class_name}.{class_name}."
    methods = []
    for item in inventory:
        qualified = item["qualified_name"]
        if not qualified.startswith(prefix):
            continue
        remainder = qualified[len(prefix) :]
        if "." in remainder or item["name"].startswith("<"):
            continue
        methods.append(
            {
                "name": item["name"],
                "line": item["first_line"],
                "arg_count": item["arg_count"],
                "args": item["variables"][: item["arg_count"]],
                "bytecode_size": item["bytecode_size"],
                "instruction_count": item["instruction_count"],
                "calls": item["names"],
            }
        )
    return sorted(methods, key=lambda method: method["line"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    manifest = {"modules": {}, "totals": {"methods": 0, "code_objects": 0}}
    for module, class_name in MODULES.items():
        inventory_path = args.analysis_root / module / "code_inventory.json"
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        methods = direct_methods(inventory, class_name)
        manifest["modules"][module] = {
            "class": class_name,
            "code_objects": len(inventory),
            "methods": methods,
        }
        manifest["totals"]["methods"] += len(methods)
        manifest["totals"]["code_objects"] += len(inventory)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest["totals"], ensure_ascii=False))


if __name__ == "__main__":
    main()

