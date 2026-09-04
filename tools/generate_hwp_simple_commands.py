from __future__ import annotations

import argparse
import dis
import marshal
import types
from pathlib import Path


BRANCH_PREFIXES = ("JUMP", "POP_JUMP", "FOR_ITER", "RERAISE")
ALLOWED_NAMES = {"대상", "HAction", "Run"}


def find_class(code: types.CodeType, name: str) -> types.CodeType:
    for const in code.co_consts:
        if isinstance(const, types.CodeType) and const.co_name == name:
            return const
    raise ValueError(f"class code object not found: {name}")


def simple_run_commands(code: types.CodeType) -> list[str] | None:
    if code.co_argcount != 1 or set(code.co_names) - ALLOWED_NAMES:
        return None
    instructions = list(dis.get_instructions(code, show_caches=False))
    if any(
        instruction.opname.startswith(BRANCH_PREFIXES)
        or instruction.opname in {"PUSH_EXC_INFO", "CHECK_EXC_MATCH"}
        for instruction in instructions
    ):
        return None
    commands = [
        instruction.argval
        for instruction in instructions
        if instruction.opname == "LOAD_CONST" and isinstance(instruction.argval, str)
    ]
    run_calls = sum(
        instruction.opname == "LOAD_ATTR" and instruction.argval == "Run"
        for instruction in instructions
    )
    return commands if commands and len(commands) == run_calls else None


def render(methods: list[tuple[str, list[str]]]) -> str:
    lines = [
        '"""바이트코드에서 기계적으로 복구한 단순 HAction.Run 명령."""',
        "",
        "",
        "class GeneratedSimpleCommandMixin:",
    ]
    for name, commands in methods:
        lines.append(f"    def {name}(self):")
        for command in commands:
            lines.append(f"        self.대상.HAction.Run({command!r})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("marshal_file", type=Path)
    parser.add_argument("class_name")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    module = marshal.loads(args.marshal_file.read_bytes())
    class_code = find_class(module, args.class_name)
    methods = []
    for const in class_code.co_consts:
        if not isinstance(const, types.CodeType) or const.co_name.startswith("<"):
            continue
        commands = simple_run_commands(const)
        if commands is not None:
            methods.append((const.co_name, commands))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(methods), encoding="utf-8")
    print(f"generated {len(methods)} methods")


if __name__ == "__main__":
    main()

