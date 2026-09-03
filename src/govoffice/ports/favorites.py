from __future__ import annotations

from typing import Protocol

from ..domain.functions import 기능


class 즐겨찾기포트(Protocol):
    def 전체(self) -> tuple[기능, ...]: ...

    def 저장(self, 기능목록: tuple[기능, ...]) -> None: ...

