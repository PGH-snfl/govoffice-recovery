from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..domain.presets import 서식프리셋


@runtime_checkable
class 서식프리셋저장포트(Protocol):
    def 저장(self, 프리셋: 서식프리셋) -> None: ...

    def 목록(self) -> tuple[서식프리셋, ...]: ...

    def 불러오기(self, 프리셋id: str) -> 서식프리셋: ...

    def 삭제(self, 프리셋id: str) -> bool: ...
