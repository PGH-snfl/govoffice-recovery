from __future__ import annotations

import inspect
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class 실행기능:
    모듈: str
    클래스: str
    이름: str
    분류: str
    검증상태: str


def _카탈로그경로() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "runtime"
        / "recovered_hwp"
        / "catalog"
        / "verified_methods.json"
    )


def 검증완료기능목록() -> tuple[실행기능, ...]:
    data = json.loads(_카탈로그경로().read_text(encoding="utf-8"))
    return tuple(
        실행기능(
            모듈=item["module"],
            클래스=item["class"],
            이름=item["method"],
            분류=item.get("category", "unknown"),
            검증상태=item["status"],
        )
        for item in data["methods"]
    )


def 필수인자목록(대상: Any, 메서드명: str) -> tuple[str, ...]:
    signature = inspect.signature(getattr(대상, 메서드명))
    return tuple(
        parameter.name
        for parameter in signature.parameters.values()
        if parameter.default is inspect.Parameter.empty
        and parameter.kind
        not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    )
