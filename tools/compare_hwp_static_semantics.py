"""Compare original and recovered Python 3.13 instruction streams for all HWP APIs."""

from __future__ import annotations

import dis
import json
import sys
import types
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "recovered"
sys.path.insert(0, str(RECOVERED))

from 한컴오피스.compat.legacy_runtime import (  # noqa: E402
    Legacy기본한컴, Legacy한컴1, Legacy한컴2, Legacy한컴기본,
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
IGNORED = {"RESUME", "NOP", "CACHE", "EXTENDED_ARG", "COPY_FREE_VARS"}


def normalize_value(value):
    if isinstance(value, types.CodeType):
        return ("code", value.co_name, fingerprint(value))
    if isinstance(value, (str, int, float, complex, bytes, bool, type(None))):
        return value
    if isinstance(value, tuple):
        return tuple(normalize_value(item) for item in value)
    return repr(value)


def fingerprint(code):
    result = []
    for instruction in dis.get_instructions(code, show_caches=False):
        if instruction.opname in IGNORED:
            continue
        if instruction.opname in {"LOAD_CONST", "RETURN_CONST"}:
            arg = normalize_value(instruction.argval)
        elif instruction.opname == "BINARY_OP":
            arg = instruction.argrepr
        elif instruction.opname.startswith(("JUMP", "POP_JUMP", "FOR_ITER")):
            arg = "<TARGET>"
        else:
            arg = instruction.argval if instruction.argval is not None else instruction.argrepr
        result.append((instruction.opname, arg))
    return tuple(result)


def main():
    inventory_path = RECOVERED / "metadata" / "hwp_equivalence_inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    counts = Counter()
    for row in inventory["methods"]:
        legacy_class, recovered_class = CLASS_MAP[row["module"]]
        legacy = legacy_class.__dict__.get(row["method"])
        recovered = getattr(recovered_class, row["method"], None)
        exact = bool(
            callable(legacy)
            and callable(recovered)
            and hasattr(legacy, "__code__")
            and hasattr(recovered, "__code__")
            and fingerprint(legacy.__code__) == fingerprint(recovered.__code__)
        )
        row["static_instruction_exact"] = exact
        row["status"] = "static_exact" if exact else "pending_dynamic"
        counts[row["status"]] += 1
    inventory["static_counts"] = dict(sorted(counts.items()))
    inventory_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(inventory["static_counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
