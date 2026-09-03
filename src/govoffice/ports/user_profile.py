from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..domain.user_profile import 사용자프로필


@runtime_checkable
class 사용자프로필저장포트(Protocol):
    def 불러오기(self) -> 사용자프로필: ...

    def 저장(self, 프로필: 사용자프로필) -> None: ...
