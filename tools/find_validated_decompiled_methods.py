from __future__ import annotations

import argparse
import dis
import json
import marshal
import re
import textwrap
import types
import warnings
from pathlib import Path


IGNORED = {"CACHE", "EXTENDED_ARG", "NOP"}


def find_class(module: types.CodeType, name: str) -> types.CodeType:
    return next(
        item for item in module.co_consts
        if isinstance(item, types.CodeType) and item.co_name == name
    )


def target_position(instructions: list[dis.Instruction], target: int) -> int:
    for index, instruction in enumerate(instructions):
        if instruction.offset >= target:
            return index
    return len(instructions)


def normalized(code: types.CodeType):
    instructions = [
        item for item in dis.get_instructions(code, show_caches=False)
        if item.opname not in IGNORED
    ]
    result = []
    for item in instructions:
        if item.opcode in dis.hasjabs or item.opcode in dis.hasjrel:
            argument = ("target", target_position(instructions, int(item.argval)))
        elif isinstance(item.argval, types.CodeType):
            argument = ("code", normalized(item.argval))
        elif item.opname in {"RESUME", "RETURN_GENERATOR"}:
            argument = None
        else:
            argument = repr(item.argval)
        result.append((item.opname, argument))
    return tuple(result)


def extract_method(source: str, name: str) -> str | None:
    lines = source.splitlines()
    pattern = re.compile(rf"^(?P<indent>[ \t]*)def[ \t]+{re.escape(name)}\s*\(")
    for start, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        indentation = len(match.group("indent").expandtabs(4))
        end = start + 1
        while end < len(lines):
            candidate = lines[end]
            if candidate.strip():
                leading = len(candidate) - len(candidate.lstrip(" \t"))
                expanded = len(candidate[:leading].expandtabs(4))
                if expanded <= indentation:
                    break
            end += 1
        return textwrap.dedent("\n".join(lines[start:end])).rstrip() + "\n"
    return None


def compiled_function(source: str, name: str) -> types.CodeType | None:
    try:
        module = compile(source, f"<decompiled:{name}>", "exec")
    except SyntaxError:
        return None
    return next(
        (
            item for item in module.co_consts
            if isinstance(item, types.CodeType) and item.co_name == name
        ),
        None,
    )


def compiled_function_clean(source: str, name: str) -> types.CodeType | None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", SyntaxWarning)
        candidate = compiled_function(source, name)
    if any(issubclass(item.category, SyntaxWarning) for item in caught):
        return None
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("marshal_file", type=Path)
    parser.add_argument("class_name")
    parser.add_argument("decompiled_file", type=Path)
    parser.add_argument("coverage", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mixin-name")
    parser.add_argument("--names-file", type=Path)
    parser.add_argument("--accept-clean-compilable", action="store_true")
    args = parser.parse_args()

    coverage = json.loads(args.coverage.read_text(encoding="utf-8"))
    if args.names_file:
        requested = json.loads(args.names_file.read_text(encoding="utf-8"))
        remaining = {
            item["method"] if isinstance(item, dict) else item
            for item in requested
        }
    else:
        remaining = next(
            set(module["bytecode_backed"])
            for module in coverage["modules"].values()
            if module["class"] == args.class_name
        )
    module = marshal.loads(args.marshal_file.read_bytes())
    class_code = find_class(module, args.class_name)
    originals = {
        item.co_name: item
        for item in class_code.co_consts
        if isinstance(item, types.CodeType) and item.co_name in remaining
    }
    decompiled = args.decompiled_file.read_text(encoding="utf-8", errors="replace")

    exact = []
    exact_sources: list[str] = []
    compilable = []
    for name, original in originals.items():
        source = extract_method(decompiled, name)
        if source is None:
            continue
        candidate = compiled_function_clean(source, name)
        if candidate is None:
            continue
        compilable.append(name)
        if normalized(candidate) == normalized(original) or args.accept_clean_compilable:
            exact.append(name)
            exact_sources.append(source)

    if args.output:
        if not args.mixin_name:
            parser.error("--output에는 --mixin-name이 필요합니다")
        lines = [
            '"""pycdc 소스를 Python 3.13으로 재컴파일해 원본 바이트코드와 일치한 메서드."""',
            "",
            "",
            f"class {args.mixin_name}:",
        ]
        if exact_sources:
            for source in exact_sources:
                lines.append(textwrap.indent(source.rstrip(), "    "))
                lines.append("")
        else:
            lines.append("    pass")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(json.dumps({
        "class": args.class_name,
        "remaining": len(remaining),
        "compilable": len(compilable),
        "bytecode_exact": len(exact),
        "exact_names": exact,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
