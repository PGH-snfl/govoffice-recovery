from __future__ import annotations

import argparse
import collections
import dis
import importlib.util
import marshal
import types
from pathlib import Path

_GENERATOR_PATH = Path(__file__).with_name("generate_hwp_simple_compositions.py")
_SPEC = importlib.util.spec_from_file_location("hwp_composition_generator", _GENERATOR_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_GENERATOR = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_GENERATOR)
find_class = _GENERATOR.find_class
translate = _GENERATOR.translate


SUPPORTED = {
    "RESUME", "PUSH_NULL", "LOAD_FAST", "LOAD_FAST_LOAD_FAST", "LOAD_CONST",
    "LOAD_GLOBAL", "LOAD_ATTR", "CALL", "CALL_KW", "POP_TOP", "STORE_FAST",
    "STORE_FAST_LOAD_FAST", "STORE_ATTR", "STORE_SUBSCR", "BINARY_OP",
    "BINARY_SUBSCR", "BUILD_TUPLE", "BUILD_LIST", "UNARY_NEGATIVE",
    "FORMAT_SIMPLE", "BUILD_STRING", "RETURN_CONST", "RETURN_VALUE", "NOP",
    "EXTENDED_ARG", "LIST_EXTEND", "BINARY_SLICE",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("marshal_file", type=Path)
    parser.add_argument("class_name")
    args = parser.parse_args()

    module = marshal.loads(args.marshal_file.read_bytes())
    class_code = find_class(module, args.class_name)
    failures: list[types.CodeType] = []
    for constant in class_code.co_consts:
        if isinstance(constant, types.CodeType) and not constant.co_name.startswith("<"):
            if translate(constant) is None:
                failures.append(constant)

    unsupported = collections.Counter()
    shapes = collections.Counter()
    examples: dict[tuple[str, ...], list[str]] = collections.defaultdict(list)
    for code in failures:
        operations = [item.opname for item in dis.get_instructions(code, show_caches=False)]
        unsupported.update(set(operations) - SUPPORTED)
        shape = tuple(op for op in operations if op not in SUPPORTED)
        shapes.update([shape])
        examples[shape].append(code.co_name)

    print(f"{args.class_name}: {len(failures)} translation gaps")
    print("unsupported opcodes (method count):")
    for name, count in unsupported.most_common():
        print(f"  {name}: {count}")
    print("common unsupported shapes:")
    for shape, count in shapes.most_common(20):
        sample = ", ".join(examples[shape][:5])
        print(f"  {count:4}  {' '.join(shape) or '<stack semantics>'}  [{sample}]")


if __name__ == "__main__":
    main()
