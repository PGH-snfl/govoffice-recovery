from __future__ import annotations

import json
import re
import ast
import dis
import inspect
import marshal
import struct
import sys
import types
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent
SOURCE = WORKSPACE / "범피스1303_분석" / "decompiled" / "메인.py"
SOURCE_MARSHAL = WORKSPACE / "범피스1303_분석" / "extracted" / "code" / "메인.marshal"
CATALOG = PROJECT / "src" / "govoffice" / "runtime" / "recovered_hwp" / "catalog" / "verified_methods.json"
OUTPUT = PROJECT / "config" / "original_layout.json"
INSTITUTIONS = PROJECT / "src" / "govoffice" / "institutions" / "packages"
ICON_ROOT = PROJECT / "assets" / "icons"

TABS = ("표", "표세부", "블록", "이동", "편리", "글자", "문자", "중앙", "지자체", "사용", "교직", "공기업", "기본서식", "국방", "가이드")


def icon_dimensions(icon: str) -> tuple[int, int]:
    """원본 Tk 버튼처럼 PNG의 실제 픽셀 크기를 레이아웃 크기로 사용한다."""
    relative = icon.replace("\\", "/").removeprefix("아이콘/")
    path = ICON_ROOT.joinpath(*relative.split("/"))
    try:
        header = path.read_bytes()[:24]
    except OSError:
        return 50, 50
    if len(header) >= 24 and header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR":
        return struct.unpack(">II", header[16:24])
    return 50, 50


def source_text() -> str:
    # pycdc가 첫 헤더 한 줄만 CP949로 기록하고 본문은 UTF-8로 기록했다.
    return SOURCE.read_bytes().decode("utf-8", errors="replace")


def frame_body(text: str, tab: str) -> str:
    match = re.search(rf"^def {re.escape(tab)}프레임\([^\n]*\):\r?\n(.*?)(?=^def |^if __name__)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def function_body(text: str, function_name: str) -> str:
    """Return one top-level function body from the pycdc text."""
    match = re.search(
        rf"^def {re.escape(function_name)}\([^\n]*\):\r?\n(.*?)(?=^def |^if __name__)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def _literal_args(callback: str, match: re.Match) -> list | None:
    start = match.end()
    depth = 1
    quote = None
    escaped = False
    end = start
    for end in range(start, len(callback)):
        char = callback[end]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                break
    try:
        parsed = ast.parse(f"f({callback[start:end]})", mode="eval").body
        def value(node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "이미지" and len(node.args) == 1:
                return {"asset": ast.literal_eval(node.args[0]).replace("\\", "/")}
            return ast.literal_eval(node)
        return [value(node) for node in parsed.args]
    except (SyntaxError, ValueError, TypeError):
        return None


def _operations(callback: str, allowed: set[str], required_counts: dict[str, int]) -> list[dict]:
    found = []
    for match in re.finditer(r"기본\.([가-힣A-Za-z_][가-힣A-Za-z_0-9]*)\s*\(", callback):
        method = match.group(1)
        args = _literal_args(callback, match)
        found.append((match.start(), {"type": "method", "method": method, "args": args, "allowed": method in allowed and args is not None and len(args) >= required_counts.get(method, 10**6)}))
    for match in re.finditer(r"기본\.대상\.HAction\.Run\('([^']+)'\)", callback):
        found.append((match.start(), {"type": "h_action", "command": match.group(1), "allowed": True}))
    return [operation for _, operation in sorted(found, key=lambda item: item[0])]


def _balanced_call(text: str, opening: int) -> str | None:
    depth = 0
    quote = None
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[opening : index + 1]
    return None


def _deduplicate_buttons(buttons: list[dict]) -> list[dict]:
    result = []
    seen = set()
    for button in buttons:
        key = (
            button["name"],
            button["x"],
            button["y"],
            button["width"],
            button["height"],
            button["icon"],
            json.dumps(button["operations"], ensure_ascii=False, sort_keys=True),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(button)
    return result


def extract_buttons(
    body: str,
    allowed: set[str],
    required_counts: dict[str, int],
    *,
    parent: str | None = None,
) -> list[dict]:
    result = []
    assignment = re.compile(r"^\s*([^\s=]+)\s*=\s*(버튼|설명버튼)\(", re.MULTILINE)
    for match in assignment.finditer(body):
        call = _balanced_call(body, match.end() - 1)
        if not call:
            continue
        header = re.match(r"\(\s*([^,]+),\s*(\d+),\s*(\d+),\s*'([^']+)'\s*,(.*)\)$", call, re.DOTALL)
        if not header:
            continue
        master, x, y, icon, callback = header.groups()
        if parent is not None and master.strip() != parent:
            continue
        icon = icon.replace("\\", "/")
        width, height = icon_dimensions(icon)
        operations = _operations(callback, allowed, required_counts)
        executable = bool(operations) and all(
            operation["allowed"] and (operation["type"] != "method" or operation["args"] is not None)
            for operation in operations
        )
        result.append(
            {
                "name": match.group(1).strip().removesuffix("버튼"),
                "x": int(x),
                "y": int(y),
                "width": width,
                "height": height,
                "icon": icon,
                "operations": operations,
                "enabled": executable,
            }
        )
    return _deduplicate_buttons(result)


def _walk_code(code: types.CodeType):
    yield code
    for constant in code.co_consts:
        if isinstance(constant, types.CodeType):
            yield from _walk_code(constant)


def load_code_index() -> dict[str, list[types.CodeType]]:
    """Load the original Python 3.13 code objects used for damaged pycdc calls."""
    try:
        root = marshal.loads(SOURCE_MARSHAL.read_bytes())
    except (OSError, EOFError, ValueError, TypeError):
        return {}
    result: dict[str, list[types.CodeType]] = {}
    for code in _walk_code(root):
        result.setdefault(code.co_name, []).append(code)
    return result


def _lambda_geometry(code: types.CodeType) -> dict[str, int] | None:
    if "geometry" not in code.co_names:
        return None
    numbers = [value for value in code.co_consts if type(value) is int]
    if len(numbers) < 2:
        return None
    return {"width": numbers[0], "height": numbers[1]}


def extract_page_controls(code_index: dict[str, list[types.CodeType]], window_function: str) -> list[dict]:
    """Recover ButtonDoubleClick navigation calls directly from original bytecode."""
    candidates = code_index.get(window_function, [])
    if not candidates:
        return []
    instructions = list(dis.get_instructions(candidates[0], show_caches=False))
    controls = []
    for position, instruction in enumerate(instructions):
        if instruction.opname != "STORE_FAST" or not str(instruction.argval).endswith("버튼"):
            continue
        starts = [
            index
            for index in range(max(0, position - 64), position)
            if instructions[index].opname == "LOAD_GLOBAL" and instructions[index].argval == "버튼더블클릭"
        ]
        if not starts:
            continue
        start = starts[-1]
        segment = instructions[start:position]
        if any(item.opname == "STORE_FAST" for item in segment[1:]):
            continue
        numbers = [item.argval for item in segment if item.opname == "LOAD_CONST" and type(item.argval) is int]
        strings = [item.argval for item in segment if item.opname == "LOAD_CONST" and isinstance(item.argval, str)]
        lambdas = [
            item.argval
            for item in segment
            if item.opname == "LOAD_CONST" and isinstance(item.argval, types.CodeType)
        ]
        if len(numbers) < 2 or not strings or len(lambdas) < 3:
            continue
        open_lambda, close_lambda, state_lambda = lambdas[-3:]
        page_functions = [
            name
            for name in open_lambda.co_freevars
            if name.endswith("프레임") and name != "지역프레임"
        ]
        if not page_functions:
            continue
        control_name = str(instruction.argval).removesuffix("버튼")
        state_strings = [value for value in state_lambda.co_consts if isinstance(value, str)]
        page_id = state_strings[-1] if state_strings else control_name
        icon = strings[0].replace("\\", "/")
        width, height = icon_dimensions(icon)
        expanded_window = _lambda_geometry(open_lambda)
        collapsed_window = _lambda_geometry(close_lambda)
        controls.append(
            {
                "name": control_name,
                "x": numbers[0],
                "y": numbers[1],
                "width": width,
                "height": height,
                "icon": icon,
                "page_id": page_id,
                "page_function": page_functions[0],
                "geometry": expanded_window,
                "expanded_window": expanded_window,
                "collapsed_window": collapsed_window,
                "toggle": True,
                "enabled": False,
            }
        )
    return controls


def page_function_body(institution_body: str, function_name: str) -> str:
    """Select the named page function, excluding pycdc's preceding inline copy."""
    match = re.search(rf"^\s+def\s+{re.escape(function_name)}\([^\n]*\):", institution_body, re.MULTILINE)
    if not match:
        return ""
    tail = institution_body[match.start() :]
    boundaries = []
    for pattern in (
        r"\r?\n\s*if \(lambda : 서브프레임\.place_forget\(\)",
        r"\r?\n\s*if \(lambda 버튼명",
        r"\r?\n\s*def 버튼확인\(",
    ):
        boundary = re.search(pattern, tail[match.end() - match.start() :])
        if boundary:
            boundaries.append(match.end() - match.start() + boundary.start())
    return tail[: min(boundaries)] if boundaries else tail


def _mask_widget_callbacks(body: str) -> str:
    """Blank widget constructor calls so callback methods are not treated as page-open actions."""
    masked = list(body)
    # pycdc emits guarded widget construction as ``if (lambda: callback()):``.
    # The lambda body is metadata for a button, not an action run while opening
    # the page, so mask the complete condition before looking for direct calls.
    for match in re.finditer(r"\bif\s*\(lambda\b", body):
        opening = body.find("(", match.start(), match.end())
        stack = []
        quote = None
        escaped = False
        end = None
        for index in range(opening, len(body)):
            char = body[index]
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue
            if char in "'\"":
                quote = char
            elif char in "([{":
                stack.append(char)
            elif char in ")]}":
                if stack:
                    stack.pop()
                if not stack:
                    end = index + 1
                    break
        if end is not None:
            for index in range(match.start(), end):
                if masked[index] not in "\r\n":
                    masked[index] = " "
    assignment = re.compile(r"=\s*(?:버튼|설명버튼|서브프레임|지역프레임)\(")
    for match in assignment.finditer(body):
        opening = match.end() - 1
        call = _balanced_call(body, opening)
        if not call:
            continue
        for index in range(opening, opening + len(call)):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def direct_page_operations(body: str, allowed: set[str], required_counts: dict[str, int]) -> list[dict]:
    """Extract operations executed while opening a page, outside button callbacks."""
    body = _mask_widget_callbacks(body)
    found = []
    for match in re.finditer(r"기본\.([가-힣A-Za-z_][가-힣A-Za-z_0-9]*)\s*\(", body):
        if body[body.rfind("\n", 0, match.start()) + 1 : match.start()].strip():
            continue
        method = match.group(1)
        args = _literal_args(body, match)
        found.append(
            (
                match.start(),
                {
                    "type": "method",
                    "method": method,
                    "args": args,
                    "allowed": method in allowed
                    and args is not None
                    and len(args) >= required_counts.get(method, 10**6),
                },
            )
        )
    for match in re.finditer(r"기본\.대상\.HAction\.Run\('([^']+)'\)", body):
        if body[body.rfind("\n", 0, match.start()) + 1 : match.start()].strip():
            continue
        found.append((match.start(), {"type": "h_action", "command": match.group(1), "allowed": True}))
    return [operation for _, operation in sorted(found, key=lambda item: item[0])]


def _shift_buttons(buttons: list[dict], x: int, y: int) -> list[dict]:
    shifted = []
    for button in buttons:
        item = dict(button)
        item["x"] += x
        item["y"] += y
        shifted.append(item)
    return shifted


def extract_page(
    text: str,
    institution_body: str,
    control: dict,
    allowed: set[str],
    required_counts: dict[str, int],
) -> dict | None:
    body = page_function_body(institution_body, control["page_function"])
    if not body:
        return None
    frame_match = re.search(
        r"서브프레임\s*=\s*프레임\(지역프레임,\s*(-?\d+),\s*(-?\d+),\s*(\d+),\s*(\d+)\)",
        body,
    )
    if frame_match:
        frame_x, frame_y, frame_width, frame_height = map(int, frame_match.groups())
    else:
        collapsed = control.get("collapsed_window") or {"width": 320, "height": 0}
        expanded = control.get("expanded_window") or collapsed
        frame_x, frame_y = 0, collapsed["height"]
        frame_width = collapsed["width"]
        frame_height = max(0, expanded["height"] - collapsed["height"])
    buttons = extract_buttons(body, allowed, required_counts, parent="서브프레임")
    shared_match = re.search(
        r"(?<!def )\b(공용분석계산프레임|공용표편집프레임|문자프레임)"
        r"\(서브프레임,\s*(-?\d+),\s*(-?\d+),\s*(\d+),\s*(\d+)\)",
        body,
    )
    shared_builder = None
    if shared_match:
        builder_name, x, y, width, height = shared_match.groups()
        builder_x, builder_y, builder_width, builder_height = map(int, (x, y, width, height))
        builder_buttons = extract_buttons(
            function_body(text, builder_name),
            allowed,
            required_counts,
            parent="지역프레임",
        )
        buttons.extend(_shift_buttons(builder_buttons, builder_x, builder_y))
        shared_builder = {
            "name": builder_name,
            "x": builder_x,
            "y": builder_y,
            "width": builder_width,
            "height": builder_height,
        }
    buttons = _deduplicate_buttons(buttons)
    on_open_operations = direct_page_operations(body, allowed, required_counts)
    on_open_allowed = all(operation["allowed"] for operation in on_open_operations)
    enabled = on_open_allowed and (
        any(button["enabled"] for button in buttons) or bool(on_open_operations)
    )
    return {
        "id": control["page_id"],
        "name": control["name"],
        "function": control["page_function"],
        "frame": {
            "x": frame_x,
            "y": frame_y,
            "width": frame_width,
            "height": frame_height,
        },
        "geometry": control.get("expanded_window"),
        "expanded_window": control.get("expanded_window"),
        "buttons": buttons,
        "shared_builder": shared_builder,
        "on_open_operations": on_open_operations,
        "enabled": enabled,
    }


def apply_layout_corrections(
    institution_id: str,
    base_buttons: list[dict],
    page_controls: list[dict],
) -> list[dict]:
    """Apply audited visual corrections while retaining original coordinates."""
    corrections = {
        ("gyeonggi", "base_button", "경기붙임"): ("x", 110, "25px icons touched with a 5px overlap"),
        ("sejong", "page_control", "세종프롬프트"): ("y", 40, "align the two page controls without overlap"),
        ("sejong", "page_control", "세종문서편집"): ("y", 120, "end at the y=200 base-button row"),
    }
    result = []
    for scope_name, items in (("base_button", base_buttons), ("page_control", page_controls)):
        for item in items:
            correction = corrections.get((institution_id, scope_name, item["name"]))
            if correction is None:
                continue
            field, value, reason = correction
            source_value = item[field]
            item[f"source_{field}"] = source_value
            item[field] = value
            result.append(
                {
                    "scope": scope_name,
                    "name": item["name"],
                    "field": field,
                    "source": source_value,
                    "value": value,
                    "reason": reason,
                }
            )
    return result


def main() -> None:
    text = source_text()
    code_index = load_code_index()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    allowed = {item["method"] for item in catalog["methods"] if item["status"] in {"static_exact", "dynamic_exact"}}
    sys.path.insert(0, str(PROJECT / "src"))
    from govoffice.adapters.recovered_hwp import _복구클래스
    recovered_class = _복구클래스()
    required_counts = {}
    for method in allowed:
        try:
            required_counts[method] = sum(
                parameter.name != "self"
                and parameter.default is inspect.Parameter.empty
                and parameter.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                for parameter in inspect.signature(getattr(recovered_class, method)).parameters.values()
            )
        except (AttributeError, TypeError, ValueError):
            required_counts[method] = 10**6
    institutions = {}
    institution_by_name = {}
    for manifest_path in sorted(INSTITUTIONS.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        functions = []
        for item in manifest.get("functions", []):
            method = item["method"]
            parameters = list(item.get("parameters", []))
            if method not in allowed or len(parameters) < required_counts.get(method, 10**6):
                continue
            functions.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "method": method,
                    "parameters": parameters,
                    "ui_ready": item.get("ui_ready", True),
                }
            )
        institution_body = frame_body(text, f"{manifest['name']}창".removesuffix("프레임"))
        if not institution_body:
            window_match = re.search(rf"^def {re.escape(manifest['name'])}창\(\):\r?\n(.*?)(?=^def |^if __name__)", text, re.MULTILINE | re.DOTALL)
            institution_body = window_match.group(1) if window_match else ""
        geometry = re.search(r"우측새탭\(창,\s*\d+,\s*\d+,\s*(\d+),\s*(\d+)\)", institution_body)
        window_geometry = (
            {"width": int(geometry.group(1)), "height": int(geometry.group(2))}
            if geometry
            else None
        )
        base_buttons = (
            extract_buttons(institution_body, allowed, required_counts, parent="지역프레임")
            if institution_body
            else []
        )
        page_controls = extract_page_controls(code_index, f"{manifest['name']}창") if institution_body else []
        layout_corrections = apply_layout_corrections(manifest["id"], base_buttons, page_controls)
        pages = []
        for control in page_controls:
            page = extract_page(text, institution_body, control, allowed, required_counts)
            if page is not None:
                pages.append(page)
        page_by_id = {page["id"]: page for page in pages}
        for control in page_controls:
            control["enabled"] = bool(page_by_id.get(control["page_id"], {}).get("enabled"))
        layout = {
            "geometry": window_geometry,
            "base_buttons": base_buttons,
            "page_controls": page_controls,
            "pages": pages,
            "default_page": None,
            "layout_corrections": layout_corrections,
        }
        info = {
            "id": manifest["id"],
            "name": manifest["name"],
            "functions": functions,
            "window": window_geometry,
            "layout": layout,
            # Compatibility for older launchers. Unlike the previous flattened
            # value, this contains only the always-visible base frame.
            "layout_buttons": list(base_buttons),
        }
        institutions[manifest["id"]] = info
        institution_by_name[manifest["name"]] = manifest["id"]
    tabs = []
    for tab in TABS:
        buttons = extract_buttons(frame_body(text, tab), allowed, required_counts)
        if tab == "지자체":
            for button in buttons:
                institution_id = institution_by_name.get(button["name"])
                button["institution_id"] = institution_id
                button["enabled"] = bool(
                    institution_id
                    and (
                        institutions[institution_id]["functions"]
                        or any(item["enabled"] for item in institutions[institution_id]["layout"]["base_buttons"])
                        or any(item["enabled"] for item in institutions[institution_id]["layout"]["page_controls"])
                    )
                )
        tabs.append({"id": tab, "buttons": buttons})
        print(f"{tab}: {len(buttons)}개 (실행 연결 {sum(item['enabled'] for item in buttons)}개)")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(
            {
                "source": str(SOURCE.relative_to(WORKSPACE)),
                "window": {"width": 300, "height": 680, "top": 50, "content_top": 100, "content_height": 400, "navigation_top": 500},
                "tabs": tabs,
                "institutions": institutions,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
