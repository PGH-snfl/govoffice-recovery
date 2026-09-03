from __future__ import annotations

from dataclasses import dataclass

from ..domain.functions import 기능, 기관
from ..services.favorites import 즐겨찾기서비스


@dataclass(slots=True)
class 기관탭모델:
    """GUI가 상단 즐겨찾기와 하단 기관 기능을 분리해 그릴 수 있는 모델."""

    기관: 기관
    즐겨찾기: 즐겨찾기서비스

    @property
    def 상단기능(self) -> tuple[기능, ...]:
        return self.즐겨찾기.목록()

    @property
    def 하단기능(self) -> tuple[기능, ...]:
        return self.기관.기능목록

    def 상단으로끌어놓기(self, 기능: 기능) -> bool:
        return self.즐겨찾기.추가(기능)

    def 상단에서순서변경(self, 기능id: str, 새위치: int) -> bool:
        return self.즐겨찾기.이동(기능id, 새위치)

