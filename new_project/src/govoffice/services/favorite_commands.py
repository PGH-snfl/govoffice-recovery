"""Favorites for verified GUI buttons, sharing the existing favorites file."""
from copy import deepcopy
import hashlib
import json
import re
from uuid import uuid4

from ..domain.functions import 기능, 기능출처


class FavoriteCommands:
    def __init__(self, store, layout, allowed_methods):
        self.store = store
        self.allowed = set(allowed_methods)
        self.catalog = {}

        def add(button, category, institution=None):
            operations = button.get("operations", [])
            if button.get("enabled") is False or not operations:
                return
            try:
                self.validate(operations)
            except ValueError:
                return
            identity = json.dumps([category, button.get("name"), operations], sort_keys=True, ensure_ascii=False)
            key = hashlib.sha256(identity.encode()).hexdigest()[:24]
            self.catalog[key] = dict(id=key, name=button.get("name", "기능"), category=category,
                                     institution_id=institution, operations=deepcopy(operations))
        for tab in layout.get("tabs", []):
            for button in tab.get("buttons", []):
                add(button, tab["id"])
        for key, institution in layout.get("institutions", {}).items():
            category = institution.get("name", key)
            spec = institution.get("layout") or {}
            for button in [*institution.get("layout_buttons", []), *spec.get("base_buttons", [])]:
                add(button, category, key)
            for page in spec.get("pages", []):
                for button in page.get("buttons", []):
                    add(button, category, key)
            for fn in institution.get("functions", []):
                if fn.get("ui_ready") and not fn.get("parameters"):
                    add(dict(name=fn["name"], operations=[dict(type="method", method=fn["method"], args=[])]), category, key)

    def validate(self, operations):
        if not isinstance(operations, (list, tuple)) or not operations or len(operations) > 100:
            raise ValueError("저장할 기능 동작이 올바르지 않습니다.")
        for op in operations:
            if not isinstance(op, dict) or op.get("allowed") is False:
                raise ValueError("실행 제외 기능은 즐겨찾기에 저장할 수 없습니다.")
            if op.get("type") == "method":
                if op.get("method") not in self.allowed or not isinstance(op.get("args", []), list):
                    raise ValueError("지원하지 않는 기능 또는 입력값입니다.")
            elif op.get("type") == "h_action":
                if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", str(op.get("command", ""))):
                    raise ValueError("지원하지 않는 한글 명령입니다.")
            else:
                raise ValueError("즐겨찾기는 실행 가능한 기능만 지원합니다.")
        json.dumps(operations, allow_nan=False)

    def find(self, id):
        for item in self.store.전체():
            if item.id == id:
                return item
        raise ValueError("즐겨찾기가 없거나 다른 화면에서 삭제됐습니다.")

    def operations(self, item):
        if item.동작:
            result = deepcopy(list(item.동작))
        else:
            if item.키워드인자:
                raise ValueError("이전 즐겨찾기의 이름 있는 입력값은 다시 등록해 주세요.")
            result = [dict(type="method", method=item.실행메서드, args=list(item.인자))]
        self.validate(result)
        return result

    def view(self, item):
        result = dict(id=item.id, name=item.이름, institution_id=item.기관id, catalog_id=item.카탈로그id)
        try:
            result.update(operations=self.operations(item), available=True)
        except ValueError as error:
            result.update(operations=[], available=False, reason=str(error))
        return result

    def listing(self, institution=None):
        return [self.view(item) for item in self.store.전체()
                if not institution or item.기관id in (None, institution)]

    def save(self, catalog_id, name, operations, id=None):
        name = str(name or "").strip()
        if not name or len(name) > 100:
            raise ValueError("즐겨찾기 이름은 1~100자로 입력하세요.")
        entry = self.catalog.get(catalog_id)
        if entry is None:
            raise ValueError("기능 목록이 변경되었습니다. 기능을 다시 선택하세요.")
        self.validate(operations)
        operations = deepcopy(list(operations))
        original = entry["operations"]
        if len(original) != len(operations):
            raise ValueError("즐겨찾기의 기능 구성을 변경할 수 없습니다.")
        for before, after in zip(original, operations):
            if any(before.get(k) != after.get(k) for k in ("type", "method", "command")) or len(before.get("args", [])) != len(after.get("args", [])):
                raise ValueError("기능은 유지하고 입력값만 수정할 수 있습니다.")
            for index, (a, b) in enumerate(zip(before.get("args", []), after.get("args", []))):
                # PowerShell JSON can serialize 1.0 as 1; preserve the declared numeric type.
                if type(a) is float and type(b) in (int, float):
                    after["args"][index] = b = float(b)
                if type(a) is not type(b) or isinstance(a, (dict, list)) and a != b:
                    raise ValueError("입력값 형식이 원래 기능과 다릅니다.")
        current = list(self.store.전체())
        if id:
            self.find(id)
        else:
            for item in current:
                if item.카탈로그id == catalog_id and item.동작 == tuple(operations) and item.이름 == name:
                    return self.view(item)
        item = 기능(id=id or f"favorite:{uuid4().hex}", 이름=name,
                    출처=기능출처.기관 if entry["institution_id"] else 기능출처.한글기본,
                    실행메서드="", 기관id=entry["institution_id"], 동작=tuple(deepcopy(operations)), 카탈로그id=catalog_id)
        if id:
            current = [item if existing.id == id else existing for existing in current]
        else:
            current.append(item)
        self.store.저장(tuple(current))
        return self.view(item)
