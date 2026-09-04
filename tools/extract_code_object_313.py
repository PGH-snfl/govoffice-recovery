from __future__ import annotations

import marshal
import sys
import types
from pathlib import Path


def walk(code: types.CodeType):
    yield code
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            yield from walk(value)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: extract_code_object_313.py INPUT.marshal QUALNAME OUTPUT.marshal")
    source, wanted, output = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    root = marshal.loads(source.read_bytes())
    matches = [code for code in walk(root) if code.co_qualname == wanted]
    if len(matches) != 1:
        names = [code.co_qualname for code in walk(root) if wanted in code.co_qualname]
        raise SystemExit(f"expected one exact match, got {len(matches)}; related={names}")
    output.write_bytes(marshal.dumps(matches[0]))
    print(f"extracted {matches[0].co_qualname}: {len(matches[0].co_code)} bytecode bytes")


if __name__ == "__main__":
    main()
