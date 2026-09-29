from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_original_layout import PROJECT, SOURCE, _literal_args


LAYOUT = PROJECT / "config" / "original_layout.json"
REPORT_JSON = PROJECT / "development" / "reports" / "button_binding_verification.json"
REPORT_MD = PROJECT / "development" / "reports" / "button_binding_verification.md"


def block(text: str, function_name: str) -> str:
    match = re.search(
        rf"^def {re.escape(function_name)}\([^\n]*\):\r?\n(.*?)(?=^def |^if __name__)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def balanced_call(text: str, opening: int) -> str | None:
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


def exact_buttons(body: str) -> list[dict]:
    result = []
    # 공용 프레임과 일부 기관은 동일한 버튼 생성기에 툴팁만 더한
    # `설명버튼`을 사용한다. 기능 콜백의 형식은 일반 `버튼`과 같다.
    assignment = re.compile(r"^\s*([^\s=]+)\s*=\s*(?:설명)?버튼\(", re.MULTILINE)
    for match in assignment.finditer(body):
        call = balanced_call(body, match.end() - 1)
        if not call:
            continue
        header = re.match(r"\([^,]+,\s*(\d+),\s*(\d+),\s*'([^']+)'\s*,(.*)\)$", call, re.DOTALL)
        if not header:
            continue
        x, y, icon, callback = header.groups()
        operations = []
        found = []
        for method in re.finditer(r"기본\.([가-힣A-Za-z_][가-힣A-Za-z_0-9]*)\s*\(", callback):
            found.append((method.start(), {"type": "method", "method": method.group(1), "args": _literal_args(callback, method)}))
        for action in re.finditer(r"기본\.대상\.HAction\.Run\('([^']+)'\)", callback):
            found.append((action.start(), {"type": "h_action", "command": action.group(1)}))
        operations.extend(item for _, item in sorted(found, key=lambda pair: pair[0]))
        result.append(
            {
                "name": match.group(1).removesuffix("버튼"),
                "x": int(x),
                "y": int(y),
                "icon": icon.replace("\\", "/").replace("//", "/"),
                "operations": operations,
            }
        )
    return result


def signature(operations: list[dict]) -> list[dict]:
    return [
        {key: value for key, value in operation.items() if key in {"type", "method", "command", "args"}}
        for operation in operations
    ]


def binding_key(button: dict) -> tuple[str, str, str]:
    """좌표와 무관한 버튼 기능 식별자.

    기관 서브페이지는 원본 프레임의 로컬 좌표를 유지하고, 원본 자체의
    겹침 좌표 몇 곳은 렌더 좌표만 최소 보정한다. 따라서 콜백 동등성은
    이름·아이콘·동작으로 검증하고 좌표는 레이아웃 회귀시험에서 맡는다.
    """
    return (
        button["name"],
        str(button.get("icon") or "").replace("//", "/"),
        json.dumps(signature(button.get("operations", [])), ensure_ascii=False, sort_keys=True),
    )


def unique_bindings(buttons: list[dict]) -> dict[tuple[str, str, str], dict]:
    return {binding_key(button): button for button in buttons}


def institution_buttons(institution: dict) -> list[dict]:
    layout = institution.get("layout")
    if not layout:
        return list(institution["layout_buttons"])
    buttons = list(layout.get("base_buttons", []))
    for page in layout.get("pages", []):
        buttons.extend(page.get("buttons", []))
    return list(unique_bindings(buttons).values())


def compare_institution_scope(
    scope: str,
    current: list[dict],
    exact_scope: list[dict],
    exact_global: list[dict],
) -> list[dict]:
    """페이지형 기관 버튼을 원본 콜백과 비교한다.

    공용 분석/표 편집/문자 빌더는 기관 함수 밖에 정의되므로 현재 버튼은
    전체 원본에서도 찾는다. 반대로 기관 함수 안의 실제 버튼은 페이지로
    모두 옮겨졌는지 별도로 확인한다. pycdc의 inline/def 이중 출력은
    binding_key로 한 번만 계산한다.
    """
    current_by_binding = unique_bindings(current)
    global_by_name_icon: dict[tuple[str, str], list[dict]] = {}
    for source in exact_global:
        key = (source["name"], source["icon"].replace("//", "/"))
        global_by_name_icon.setdefault(key, []).append(source)

    differences = []
    for item in current_by_binding.values():
        name_icon = (item["name"], item["icon"].replace("//", "/"))
        candidates = global_by_name_icon.get(name_icon, [])
        if not candidates:
            differences.append({"scope": scope, "button": item["name"], "kind": "source_button_not_found"})
            continue
        current_signature = signature(item.get("operations", []))
        if not any(current_signature == signature(source["operations"]) for source in candidates):
            differences.append(
                {
                    "scope": scope,
                    "button": item["name"],
                    "kind": "operation_mismatch",
                    "current": current_signature,
                    "exact_candidates": [signature(source["operations"]) for source in candidates],
                }
            )

    for key, source in unique_bindings(exact_scope).items():
        if key not in current_by_binding:
            differences.append({"scope": scope, "button": source["name"], "kind": "layout_button_missing"})
    return differences


def compare_scope(scope: str, current: list[dict], exact: list[dict]) -> list[dict]:
    # 원본에 없지만 새 프로젝트에서 명시적으로 추가한 기관 진입점은
    # 원본 버튼 동등성 비교 대상이 아니다. source_extension 표식으로
    # 복구 버튼과 제품 확장 버튼을 계속 분리한다.
    current = [item for item in current if not item.get("source_extension")]
    exact_by_key = {(item["x"], item["y"], item["icon"]): item for item in exact}
    current_by_key = {(item["x"], item["y"], item["icon"].replace("//", "/")): item for item in current}
    differences = []
    for item in current:
        key = (item["x"], item["y"], item["icon"].replace("//", "/"))
        source = exact_by_key.get(key)
        if source is None:
            differences.append({"scope": scope, "button": item["name"], "kind": "source_button_not_found"})
            continue
        current_signature = signature(item.get("operations", []))
        exact_signature = signature(source["operations"])
        if current_signature != exact_signature:
            differences.append(
                {
                    "scope": scope,
                    "button": item["name"],
                    "kind": "operation_mismatch",
                    "current": current_signature,
                    "exact": exact_signature,
                }
            )
    for key, source in exact_by_key.items():
        if key not in current_by_key:
            differences.append({"scope": scope, "button": source["name"], "kind": "layout_button_missing"})
    return differences


def main() -> None:
    text = SOURCE.read_bytes().decode("utf-8", errors="replace")
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    exact_global = exact_buttons(text)
    differences = []
    checked = 0
    source_extensions = 0
    for tab in layout["tabs"]:
        exact = exact_buttons(block(text, f"{tab['id']}프레임"))
        checked += len(tab["buttons"])
        source_extensions += sum(bool(item.get("source_extension")) for item in tab["buttons"])
        differences.extend(compare_scope(f"main/{tab['id']}", tab["buttons"], exact))
    for institution in layout["institutions"].values():
        exact = exact_buttons(block(text, f"{institution['name']}창"))
        current = institution_buttons(institution)
        checked += len(current)
        differences.extend(
            compare_institution_scope(
                f"institution/{institution['id']}",
                current,
                exact,
                exact_global,
            )
        )

    mismatches = [item for item in differences if item["kind"] == "operation_mismatch"]
    missing = [item for item in differences if item["kind"] == "source_button_not_found"]
    layout_missing = [item for item in differences if item["kind"] == "layout_button_missing"]
    report = {"checked": checked, "source_extensions": source_extensions, "differences": len(differences), "operation_mismatches": len(mismatches), "source_not_found": len(missing), "layout_button_missing": len(layout_missing), "items": differences}
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(
        "# 버튼 연결 전수 검증\n\n"
        f"- 검사 버튼: {checked}개\n"
        f"- 새 프로젝트 전용 진입점: {source_extensions}개\n"
        f"- 동작 불일치: {len(mismatches)}개\n"
        f"- 원본 버튼 경계 확인 실패: {len(missing)}개\n"
        f"- 연결표에서 누락된 원본 버튼: {len(layout_missing)}개\n"
        f"- 전체 차이: {len(differences)}개\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in report.items() if key != "items"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
