from __future__ import annotations

import argparse
import ast
import dis
import importlib
import importlib.util
import inspect
import marshal
import sys
import types
from pathlib import Path


def find_class(code: types.CodeType, name: str) -> types.CodeType:
    for const in code.co_consts:
        if isinstance(const, types.CodeType) and const.co_name == name:
            return const
    raise ValueError(name)


def translate(code: types.CodeType) -> list[str] | None:
    instructions = list(dis.get_instructions(code, show_caches=False))
    stack: list[str | tuple[str, str]] = []
    statements: list[str] = []
    loop_depth = 0
    loop_headers: list[int] = []
    indent_depth = 0
    conditional_ends: dict[int, int] = {}
    open_condition_targets: list[int] = []
    temporary_counter = 0

    def emit(statement: str) -> None:
        statements.append(f"{'    ' * indent_depth}{statement}")

    for instruction_index, instruction in enumerate(instructions):
        ending = conditional_ends.pop(instruction.offset, 0)
        if ending:
            indent_depth -= ending
            for _ in range(ending):
                if instruction.offset in open_condition_targets:
                    reverse_index = len(open_condition_targets) - 1 - open_condition_targets[::-1].index(instruction.offset)
                    open_condition_targets.pop(reverse_index)
            if indent_depth < loop_depth:
                return None
        op = instruction.opname
        if op in {"RESUME", "NOP", "EXTENDED_ARG"}:
            continue
        if op == "PUSH_NULL":
            # Python 3.13 places the call sentinel after attribute-based
            # callables (for example ``datetime.today``).  It has no source
            # representation, so mark the expression already on our stack as
            # callable and continue.
            if not stack or not isinstance(stack[-1], str):
                return None
            stack[-1] = ("callable", stack[-1])
            continue
        if op == "LOAD_FAST":
            stack.append(str(instruction.argval))
            continue
        if op == "LOAD_FAST_LOAD_FAST":
            stack.extend(str(name) for name in instruction.argval)
            continue
        if op == "LOAD_CONST":
            stack.append(repr(instruction.argval))
            continue
        if op == "LOAD_GLOBAL":
            name = str(instruction.argval)
            if "NULL" in instruction.argrepr:
                stack.append(("callable", name))
            else:
                stack.append(name)
            continue
        if op == "LOAD_ATTR":
            if not stack:
                return None
            owner = stack.pop()
            if not isinstance(owner, str):
                return None
            expression = f"{owner}.{instruction.argval}"
            if "NULL|self" in instruction.argrepr:
                stack.append(("callable", expression))
            else:
                stack.append(expression)
            continue
        if op == "CALL":
            count = int(instruction.arg or 0)
            if len(stack) < count + 1:
                return None
            arguments = stack[-count:] if count else []
            if count:
                del stack[-count:]
            function = stack.pop()
            if not isinstance(function, tuple) or function[0] != "callable":
                return None
            if any(not isinstance(argument, str) for argument in arguments):
                return None
            stack.append(f"{function[1]}({', '.join(arguments)})")
            continue
        if op == "CALL_KW":
            count = int(instruction.arg or 0)
            if not stack or not isinstance(stack[-1], str):
                return None
            keyword_expression = stack.pop()
            try:
                keyword_names = eval(keyword_expression, {"__builtins__": {}})
            except Exception:
                return None
            if not isinstance(keyword_names, tuple) or len(stack) < count + 1:
                return None
            arguments = stack[-count:] if count else []
            if count:
                del stack[-count:]
            function = stack.pop()
            if not isinstance(function, tuple) or function[0] != "callable":
                return None
            positional_count = count - len(keyword_names)
            rendered = list(arguments[:positional_count])
            rendered.extend(
                f"{name}={value}"
                for name, value in zip(keyword_names, arguments[positional_count:])
            )
            stack.append(f"{function[1]}({', '.join(rendered)})")
            continue
        if op == "POP_TOP":
            if not stack:
                return None
            value = stack.pop()
            if isinstance(value, tuple) and value[0] == "iterator":
                continue
            if not isinstance(value, str):
                return None
            emit(value)
            continue
        if op == "STORE_FAST":
            if not stack:
                return None
            value = stack.pop()
            if isinstance(value, tuple) and value[0] == "loop_item":
                emit(f"for {instruction.argval} in {value[1]}:")
                loop_depth += 1
                indent_depth += 1
                continue
            if not isinstance(value, str):
                return None
            emit(f"{instruction.argval} = {value}")
            continue
        if op == "STORE_FAST_LOAD_FAST":
            if not stack:
                return None
            store_name, load_name = instruction.argval
            value = stack.pop()
            if isinstance(value, tuple) and value[0] == "loop_item":
                emit(f"for {store_name} in {value[1]}:")
                loop_depth += 1
                indent_depth += 1
                stack.append(str(load_name))
                continue
            if not isinstance(value, str):
                return None
            emit(f"{store_name} = {value}")
            stack.append(str(load_name))
            continue
        if op == "STORE_FAST_STORE_FAST":
            if len(stack) < 2:
                return None
            first_name, second_name = instruction.argval
            first_value = stack.pop()
            second_value = stack.pop()
            if not isinstance(first_value, str) or not isinstance(second_value, str):
                return None
            emit(f"{first_name} = {first_value}")
            emit(f"{second_name} = {second_value}")
            continue
        if op == "STORE_ATTR":
            if len(stack) < 2:
                return None
            owner = stack.pop()
            value = stack.pop()
            if not isinstance(owner, str) or not isinstance(value, str):
                return None
            emit(f"{owner}.{instruction.argval} = {value}")
            continue
        if op == "STORE_SUBSCR":
            if len(stack) < 3:
                return None
            index = stack.pop()
            owner = stack.pop()
            value = stack.pop()
            if not all(isinstance(item, str) for item in (owner, index, value)):
                return None
            emit(f"{owner}[{index}] = {value}")
            continue
        if op == "GET_ITER":
            if not stack or not isinstance(stack[-1], str):
                return None
            stack[-1] = ("iterator", stack[-1])
            continue
        if op == "FOR_ITER":
            if not stack or not isinstance(stack[-1], tuple) or stack[-1][0] != "iterator":
                return None
            stack.append(("loop_item", stack[-1][1]))
            loop_headers.append(instruction.offset)
            continue
        if op in {"JUMP_BACKWARD", "JUMP_BACKWARD_NO_INTERRUPT"}:
            if loop_depth < 1 or not loop_headers or int(instruction.argval) != loop_headers[-1]:
                return None
            if (
                instruction_index + 1 < len(instructions)
                and instructions[instruction_index + 1].offset in conditional_ends
            ):
                emit("continue")
            continue
        if op == "END_FOR":
            if loop_depth < 1 or not stack:
                return None
            iterator = stack[-1]
            if not isinstance(iterator, tuple) or iterator[0] != "iterator":
                return None
            loop_depth -= 1
            indent_depth -= 1
            loop_headers.pop()
            continue
        if op == "COMPARE_OP":
            if len(stack) < 2:
                return None
            right = stack.pop()
            left = stack.pop()
            if not isinstance(left, str) or not isinstance(right, str):
                return None
            stack.append(f"({left} {instruction.argval} {right})")
            continue
        if op == "CONTAINS_OP":
            if len(stack) < 2:
                return None
            container = stack.pop()
            item = stack.pop()
            if not isinstance(item, str) or not isinstance(container, str):
                return None
            operator = "not in" if instruction.arg else "in"
            stack.append(f"({item} {operator} {container})")
            continue
        if op == "TO_BOOL":
            if not stack or not isinstance(stack[-1], str):
                return None
            continue
        if op in {"POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE", "POP_JUMP_IF_NONE"}:
            if not stack or not isinstance(stack[-1], str):
                return None
            target = int(instruction.argval)
            if target <= instruction.offset:
                return None
            condition = stack.pop()
            if op == "POP_JUMP_IF_FALSE":
                rendered = condition
            elif op == "POP_JUMP_IF_TRUE":
                rendered = f"not ({condition})"
            else:
                rendered = f"{condition} is not None"
            emit(f"if {rendered}:")
            indent_depth += 1
            conditional_ends[target] = conditional_ends.get(target, 0) + 1
            open_condition_targets.append(target)
            continue
        if op == "JUMP_FORWARD":
            if instruction_index + 1 >= len(instructions):
                return None
            else_offset = instructions[instruction_index + 1].offset
            if not open_condition_targets or open_condition_targets[-1] != else_offset:
                return None
            conditional_ends[else_offset] -= 1
            if conditional_ends[else_offset] == 0:
                del conditional_ends[else_offset]
            open_condition_targets.pop()
            indent_depth -= 1
            if indent_depth < loop_depth:
                return None
            emit("else:")
            indent_depth += 1
            target = int(instruction.argval)
            conditional_ends[target] = conditional_ends.get(target, 0) + 1
            open_condition_targets.append(target)
            continue
        if op == "BINARY_OP":
            if len(stack) < 2:
                return None
            right = stack.pop()
            left = stack.pop()
            if not isinstance(left, str) or not isinstance(right, str):
                return None
            stack.append(f"({left} {instruction.argrepr} {right})")
            continue
        if op == "BINARY_SUBSCR":
            if len(stack) < 2:
                return None
            index = stack.pop()
            owner = stack.pop()
            if not isinstance(owner, str) or not isinstance(index, str):
                return None
            stack.append(f"{owner}[{index}]")
            continue
        if op in {"BUILD_TUPLE", "BUILD_LIST"}:
            count = int(instruction.arg or 0)
            if len(stack) < count:
                return None
            values = stack[-count:] if count else []
            if count:
                del stack[-count:]
            if any(not isinstance(value, str) for value in values):
                return None
            opening, closing = ("(", ")") if op == "BUILD_TUPLE" else ("[", "]")
            body = ", ".join(values)
            if op == "BUILD_TUPLE" and count == 1:
                body += ","
            stack.append(f"{opening}{body}{closing}")
            continue
        if op == "LIST_EXTEND":
            depth = int(instruction.arg or 0)
            if not stack or depth < 1 or len(stack) < depth + 1:
                return None
            iterable = stack.pop()
            target_index = -depth
            target = stack[target_index]
            if not isinstance(target, str) or not isinstance(iterable, str):
                return None
            try:
                target_value = ast.literal_eval(target)
                iterable_value = ast.literal_eval(iterable)
            except (SyntaxError, ValueError):
                stack[target_index] = f"[*{target}, *{iterable}]"
            else:
                if not isinstance(target_value, list):
                    return None
                try:
                    target_value.extend(iterable_value)
                except TypeError:
                    return None
                stack[target_index] = repr(target_value)
            continue
        if op == "BINARY_SLICE":
            if len(stack) < 3:
                return None
            stop = stack.pop()
            start = stack.pop()
            owner = stack.pop()
            if not all(isinstance(item, str) for item in (owner, start, stop)):
                return None
            start_text = "" if start == "None" else start
            stop_text = "" if stop == "None" else stop
            stack.append(f"{owner}[{start_text}:{stop_text}]")
            continue
        if op == "UNPACK_SEQUENCE":
            if not stack:
                return None
            count = int(instruction.arg or 0)
            value = stack.pop()
            temporary_counter += 1
            temporary = f"_복구_분해_{temporary_counter}"
            if isinstance(value, tuple) and value[0] == "loop_item":
                emit(f"for {temporary} in {value[1]}:")
                loop_depth += 1
                indent_depth += 1
            elif isinstance(value, str):
                emit(f"{temporary} = {value}")
            else:
                return None
            stack.extend(f"{temporary}[{index}]" for index in reversed(range(count)))
            continue
        if op == "BUILD_MAP":
            count = int(instruction.arg or 0)
            if len(stack) < count * 2:
                return None
            items = stack[-count * 2 :] if count else []
            if count:
                del stack[-count * 2 :]
            if any(not isinstance(item, str) for item in items):
                return None
            pairs = [f"{items[index]}: {items[index + 1]}" for index in range(0, len(items), 2)]
            stack.append("{" + ", ".join(pairs) + "}")
            continue
        if op == "BUILD_CONST_KEY_MAP":
            count = int(instruction.arg or 0)
            if len(stack) < count + 1:
                return None
            keys_expression = stack.pop()
            values = stack[-count:] if count else []
            if count:
                del stack[-count:]
            try:
                keys = ast.literal_eval(keys_expression) if isinstance(keys_expression, str) else None
            except (SyntaxError, ValueError):
                return None
            if not isinstance(keys, tuple) or len(keys) != count:
                return None
            if any(not isinstance(value, str) for value in values):
                return None
            stack.append("{" + ", ".join(f"{key!r}: {value}" for key, value in zip(keys, values)) + "}")
            continue
        if op == "DICT_UPDATE":
            depth = int(instruction.arg or 0)
            if not stack or depth < 1 or len(stack) < depth + 1:
                return None
            update = stack.pop()
            target_index = -depth
            target = stack[target_index]
            if not isinstance(target, str) or not isinstance(update, str):
                return None
            stack[target_index] = f"{{**{target}, **{update}}}"
            continue
        if op == "BUILD_SLICE":
            count = int(instruction.arg or 0)
            if count not in {2, 3} or len(stack) < count:
                return None
            values = stack[-count:]
            del stack[-count:]
            if any(not isinstance(value, str) for value in values):
                return None
            stack.append(f"slice({', '.join(values)})")
            continue
        if op == "UNARY_NEGATIVE":
            if not stack or not isinstance(stack[-1], str):
                return None
            stack.append(f"-({stack.pop()})")
            continue
        if op == "FORMAT_SIMPLE":
            if not stack or not isinstance(stack[-1], str):
                return None
            stack.append(f"str({stack.pop()})")
            continue
        if op == "BUILD_STRING":
            count = int(instruction.arg or 0)
            if len(stack) < count:
                return None
            values = stack[-count:] if count else []
            if count:
                del stack[-count:]
            if any(not isinstance(value, str) for value in values):
                return None
            stack.append(" + ".join(values) if values else "''")
            continue
        if op == "RETURN_CONST":
            if stack:
                return None
            if instruction.argval is not None:
                emit(f"return {instruction.argval!r}")
            continue
        if op == "RETURN_VALUE":
            if len(stack) != 1 or not isinstance(stack[0], str):
                return None
            emit(f"return {stack.pop()}")
            continue
        return None
    return statements if statements or len(code.co_code) <= 8 else None


def render(class_name: str, legacy_class: type, methods: list[tuple[str, list[str]]]) -> str:
    generated_name = f"Generated{class_name}CompositionMixin"
    lines = [
        '"""원본 바이트코드에서 복구한 직선형 메서드 조합."""',
        "",
        "",
        f"class {generated_name}:",
    ]
    for name, statements in methods:
        signature = inspect.signature(legacy_class.__dict__[name])
        lines.append(f"    def {name}{signature}:")
        if statements:
            lines.extend(f"        {statement}" for statement in statements)
        else:
            lines.append("        pass")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("marshal_file", type=Path)
    parser.add_argument("class_name")
    parser.add_argument("legacy_class_name")
    parser.add_argument("recovered_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    runtime_path = (
        args.recovered_root.resolve()
        / "한컴오피스"
        / "compat"
        / "legacy_runtime.py"
    )
    runtime_spec = importlib.util.spec_from_file_location(
        "hwp_legacy_runtime_for_generation", runtime_path
    )
    if runtime_spec is None or runtime_spec.loader is None:
        raise RuntimeError(f"legacy runtime을 불러올 수 없습니다: {runtime_path}")
    runtime = importlib.util.module_from_spec(runtime_spec)
    runtime_spec.loader.exec_module(runtime)
    legacy_class = getattr(runtime, args.legacy_class_name)
    module = marshal.loads(args.marshal_file.read_bytes())
    class_code = find_class(module, args.class_name)
    methods = []
    for const in class_code.co_consts:
        if not isinstance(const, types.CodeType) or const.co_name.startswith("<"):
            continue
        statements = translate(const)
        if statements is not None and const.co_name in legacy_class.__dict__:
            candidate = render(args.class_name, legacy_class, [(const.co_name, statements)])
            try:
                compile(candidate, f"<{const.co_name}>", "exec")
            except (SyntaxError, ValueError):
                continue
            methods.append((const.co_name, statements))
    args.output.write_text(render(args.class_name, legacy_class, methods), encoding="utf-8")
    print(f"generated {len(methods)} methods")


if __name__ == "__main__":
    main()
