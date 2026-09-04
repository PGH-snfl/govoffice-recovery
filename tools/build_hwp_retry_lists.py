"""Build retry lists from a previous differential failure reason."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = (
    "hwp_equivalence_blank_all.json",
    "hwp_equivalence_blank_isolated.json",
    "hwp_equivalence_arguments_all.json",
    "hwp_equivalence_tables_all.json",
    "hwp_equivalence_tables_remaining.json",
    "hwp_equivalence_files_all.json",
    "hwp_equivalence_interactive_all.json",
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--error", required=True)
    parser.add_argument("--prefix", required=True)
    args = parser.parse_args()
    metadata = ROOT / "recovered" / "metadata"
    inventory = json.loads((metadata / "hwp_equivalence_inventory.json").read_text(encoding="utf-8"))
    categories = {(row["module"], row["method"]): row["category"] for row in inventory["methods"]}
    found = defaultdict(dict)
    for filename in REPORTS:
        path = metadata / filename
        if not path.exists():
            continue
        for row in json.loads(path.read_text(encoding="utf-8")).get("results", []):
            if (row.get("recovered") or {}).get("error") == args.error:
                key = (row["module"], row["method"])
                found[categories[key]][key] = {"module": key[0], "method": key[1]}
    for category, rows in found.items():
        output = metadata / f"{args.prefix}_{category}.json"
        output.write_text(json.dumps(list(rows.values()), ensure_ascii=False, indent=2), encoding="utf-8")
        print(category, len(rows), output)


if __name__ == "__main__":
    main()
