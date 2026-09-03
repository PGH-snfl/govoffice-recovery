from __future__ import annotations

from ..domain.functions import 기능
from ..ports.favorites import 즐겨찾기포트
from ..ports.hwp import 한글문서포트


class 즐겨찾기서비스:
    def __init__(self, 저장소: 즐겨찾기포트, 한글: 한글문서포트):
        self.저장소 = 저장소
        self.한글 = 한글

    def 목록(self) -> tuple[기능, ...]:
        return self.저장소.전체()

    def 추가(self, 대상: 기능) -> bool:
        현재 = list(self.저장소.전체())
        if any(기능.id == 대상.id for 기능 in 현재):
            return False
        현재.append(대상)
        self.저장소.저장(tuple(현재))
        return True

    def 삭제(self, 기능id: str) -> bool:
        현재 = self.저장소.전체()
        변경 = tuple(기능 for 기능 in 현재 if 기능.id != 기능id)
        if len(현재) == len(변경):
            return False
        self.저장소.저장(변경)
        return True

    def 이동(self, 기능id: str, 새위치: int) -> bool:
        현재 = list(self.저장소.전체())
        기존위치 = next((i for i, 기능 in enumerate(현재) if 기능.id == 기능id), None)
        if 기존위치 is None:
            return False
        대상 = 현재.pop(기존위치)
        새위치 = max(0, min(새위치, len(현재)))
        현재.insert(새위치, 대상)
        self.저장소.저장(tuple(현재))
        return True

    def 실행(self, 기능id: str):
        대상 = next(기능 for 기능 in self.저장소.전체() if 기능.id == 기능id)
        return self.한글.기능실행(대상.실행메서드, *대상.인자, **대상.키워드인자)

