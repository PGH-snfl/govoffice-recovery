"""원본 Python 3.13 클래스 코드 객체를 이용한 임시 호환 계층.

아직 사람이 읽을 수 있는 소스로 옮기지 않은 메서드의 동작과 공개 API를
보존한다. 소스 복구 메서드는 이 계층보다 항상 우선하며, 최종 목표는 이
모듈에 의존하는 메서드 수를 0으로 만드는 것이다.
"""

from __future__ import annotations

import json
import marshal
import math
import os
import re
import time
import types
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

try:
    import pythoncom
    from tkinter import filedialog
    from win32com.client.gencache import EnsureDispatch
except ImportError:
    pythoncom = None
    filedialog = None
    EnsureDispatch = None


_MODULE_FILES = {
    "한컴기본": "한컴라이브러리_기본.marshal",
    "한컴1": "한컴라이브러리_1.marshal",
    "한컴2": "한컴라이브러리_2.marshal",
    "기본한컴": "한컴라이브러리.marshal",
}


def _legacy_random_int(maximum: int) -> int:
    """원본 모듈의 클래스 바깥 랜덤정수 함수를 호환 계층에 복원한다."""
    return int.from_bytes(os.urandom(4), byteorder="big") % maximum


def _legacy_random_choice(items):
    """원본 모듈의 클래스 바깥 랜덤선택 함수를 호환 계층에 복원한다."""
    return items[_legacy_random_int(len(items))]


def _bytecode_root() -> Path:
    local_snapshot = Path(__file__).resolve().parents[2] / "bytecode" / "한컴오피스"
    if local_snapshot.is_dir():
        return local_snapshot
    return (
        Path(__file__).resolve().parents[3]
        / "범피스1303_분석"
        / "pyz_modules"
        / "한컴오피스"
    )


def _class_code(filename: str, class_name: str) -> types.CodeType:
    module = marshal.loads((_bytecode_root() / filename).read_bytes())
    for constant in module.co_consts:
        if isinstance(constant, types.CodeType) and constant.co_name == class_name:
            return constant
    raise RuntimeError(f"원본 클래스 코드 객체를 찾지 못했습니다: {class_name}")


def _globals() -> dict:
    return {
        "__name__": "한컴오피스.compat.legacy_runtime",
        "pythoncom": pythoncom,
        "EnsureDispatch": EnsureDispatch,
        "filedialog": filedialog,
        "datetime": datetime,
        "timedelta": timedelta,
        "Decimal": Decimal,
        "re": re,
        "os": os,
        "json": json,
        "math": math,
        "time": time,
        # 원본 marshal 모듈은 클래스 정의 전에 이 두 함수를 전역으로
        # 만들고, 서식자기개발·보도자료 랜덤 기능이 이를 참조한다.
        # 클래스 코드만 exec하던 기존 호환 계층에는 누락되어 NameError가
        # 발생했으므로 원본 전역 이름을 그대로 제공한다.
        "랜덤정수": _legacy_random_int,
        "랜덤선택": _legacy_random_choice,
    }


def _build_class(class_name: str, bases: tuple[type, ...], globals_dict: dict) -> type:
    namespace: dict = {}
    exec(_class_code(_MODULE_FILES[class_name], class_name), globals_dict, namespace)
    namespace.pop("__firstlineno__", None)
    namespace["__module__"] = __name__
    return type(f"Legacy{class_name}", bases, namespace)


_legacy_globals = _globals()
Legacy한컴기본 = _build_class("한컴기본", (object,), _legacy_globals)
_legacy_globals["한컴기본"] = Legacy한컴기본
Legacy한컴1 = _build_class("한컴1", (Legacy한컴기본,), _legacy_globals)
Legacy한컴2 = _build_class("한컴2", (Legacy한컴기본,), _legacy_globals)
_legacy_globals.update({"한컴1": Legacy한컴1, "한컴2": Legacy한컴2})
Legacy기본한컴 = _build_class("기본한컴", (Legacy한컴1, Legacy한컴2), _legacy_globals)


def attach_missing_methods(
    target: type,
    legacy: type,
    *,
    preserve_inherited: bool = False,
    preserve_names: set[str] | None = None,
) -> list[str]:
    """`target`에 직접 구현되지 않은 원본 메서드만 복사한다."""
    attached = []
    preserve_names = preserve_names or set()
    for name, value in legacy.__dict__.items():
        if name.startswith("__") or not callable(value):
            continue
        if (
            name in preserve_names
            or name in target.__dict__
            or (preserve_inherited and hasattr(target, name))
        ):
            continue
        setattr(target, name, value)
        attached.append(name)
    return attached
