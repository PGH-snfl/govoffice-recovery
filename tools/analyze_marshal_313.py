from __future__ import annotations

import dis
import io
import json
import marshal
import sys
import types
from pathlib import Path


def walk(code: types.CodeType, qualified: str = "<module>"):
    yield qualified, code
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            child = f"{qualified}.{const.co_qualname}"
            yield from walk(const, child)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: analyze_marshal_313.py INPUT.marshal OUTPUT_DIR")
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    output.mkdir(parents=True, exist_ok=True)

    code = marshal.loads(source.read_bytes())
    if not isinstance(code, types.CodeType):
        raise SystemExit(f"top-level object is {type(code)!r}, not a code object")

    inventory = []
    imports: set[str] = set()
    strings: set[str] = set()
    listing = io.StringIO()

    for qualified, item in walk(code):
        instructions = list(dis.get_instructions(item, show_caches=False))
        inventory.append(
            {
                "qualified_name": qualified,
                "name": item.co_name,
                "qualname": item.co_qualname,
                "filename": item.co_filename,
                "first_line": item.co_firstlineno,
                "arg_count": item.co_argcount,
                "positional_only": item.co_posonlyargcount,
                "keyword_only": item.co_kwonlyargcount,
                "locals": item.co_nlocals,
                "flags": item.co_flags,
                "bytecode_size": len(item.co_code),
                "instruction_count": len(instructions),
                "names": list(item.co_names),
                "variables": list(item.co_varnames),
                "freevars": list(item.co_freevars),
                "cellvars": list(item.co_cellvars),
            }
        )
        for const in item.co_consts:
            if isinstance(const, str):
                strings.add(const)
        for instruction in instructions:
            if instruction.opname == "IMPORT_NAME" and isinstance(instruction.argval, str):
                imports.add(instruction.argval)

        listing.write(f"\n{'=' * 100}\n{qualified}\n")
        listing.write(
            f"file={item.co_filename!r} line={item.co_firstlineno} "
            f"args={item.co_argcount} locals={item.co_nlocals}\n"
        )
        dis.dis(item, file=listing, depth=0, show_caches=False)

    (output / "code_inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "imports.txt").write_text("\n".join(sorted(imports)), encoding="utf-8")
    (output / "string_constants.txt").write_text("\n".join(sorted(strings)), encoding="utf-8")
    (output / "disassembly.txt").write_text(listing.getvalue(), encoding="utf-8")
    print(
        json.dumps(
            {
                "code_objects": len(inventory),
                "imports": len(imports),
                "string_constants": len(strings),
                "disassembly_chars": listing.tell(),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
