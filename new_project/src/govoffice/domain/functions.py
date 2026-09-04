from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class 기능출처(StrEnum):
    한글기본 = "hwp"
    기관 = "institution"


@dataclass(frozen=True, slots=True)
class 기능:
    id: str
    이름: str
    출처: 기능출처
    실행메서드: str
    기관id: str | None = None
    인자: tuple = field(default_factory=tuple)
    키워드인자: dict = field(default_factory=dict)
    매개변수: tuple[str, ...] = field(default_factory=tuple)
    화면실행가능: bool = True
    복구상태: str = "source"


@dataclass(frozen=True, slots=True)
class 기관:
    id: str
    이름: str
    기능목록: tuple[기능, ...] = field(default_factory=tuple)
