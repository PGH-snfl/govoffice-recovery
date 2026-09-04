"""기관탭 상단에 표시할 한글 기능 즐겨찾기 저장소."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path


@dataclass(frozen=True)
class 즐겨찾기항목:
    id: str
    name: str
    source: str
    institution_id: str | None = None
    function_id: str | None = None
    hwp_method: str | None = None
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)

    @classmethod
    def 읽기(cls, 데이터: dict):
        데이터 = dict(데이터)
        데이터["args"] = tuple(데이터.get("args", ()))
        데이터["kwargs"] = dict(데이터.get("kwargs", {}))
        return cls(**데이터)


class 즐겨찾기저장소:
    def __init__(self, 경로: str | Path):
        self.경로 = Path(경로)

    def 전체(self) -> tuple[즐겨찾기항목, ...]:
        if not self.경로.exists():
            return ()
        데이터 = json.loads(self.경로.read_text(encoding="utf-8"))
        return tuple(즐겨찾기항목.읽기(항목) for 항목 in 데이터.get("favorites", []))

    def _저장(self, 항목들):
        self.경로.parent.mkdir(parents=True, exist_ok=True)
        데이터 = {"favorites": [asdict(항목) for 항목 in 항목들]}
        임시경로 = self.경로.with_suffix(self.경로.suffix + ".tmp")
        임시경로.write_text(
            json.dumps(데이터, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        임시경로.replace(self.경로)

    def 추가(self, 항목: 즐겨찾기항목):
        현재 = list(self.전체())
        if any(기존.id == 항목.id for 기존 in 현재):
            return False
        현재.append(항목)
        self._저장(현재)
        return True

    def 삭제(self, 항목id: str):
        현재 = list(self.전체())
        변경 = [항목 for 항목 in 현재 if 항목.id != 항목id]
        if len(현재) == len(변경):
            return False
        self._저장(변경)
        return True

    def 이동(self, 항목id: str, 새위치: int):
        현재 = list(self.전체())
        기존위치 = next((i for i, 항목 in enumerate(현재) if 항목.id == 항목id), None)
        if 기존위치 is None:
            return False
        항목 = 현재.pop(기존위치)
        새위치 = max(0, min(새위치, len(현재)))
        현재.insert(새위치, 항목)
        self._저장(현재)
        return True

    def 기관기능추가(self, 기관id: str, 기능):
        return self.추가(
            즐겨찾기항목(
                id=f"institution:{기관id}:{기능.id}",
                name=기능.name,
                source="institution",
                institution_id=기관id,
                function_id=기능.id,
                hwp_method=기능.legacy_method,
            )
        )

    def 한글기본기능추가(self, 메서드: str, 이름: str | None = None, args=(), kwargs=None):
        return self.추가(
            즐겨찾기항목(
                id=f"hwp:{메서드}",
                name=이름 or 메서드,
                source="hwp",
                hwp_method=메서드,
                args=tuple(args),
                kwargs=dict(kwargs or {}),
            )
        )


def 즐겨찾기실행(항목: 즐겨찾기항목, 한컴):
    if not 항목.hwp_method:
        raise ValueError(f"실행 메서드가 없는 즐겨찾기: {항목.id}")
    return getattr(한컴, 항목.hwp_method)(*항목.args, **항목.kwargs)

