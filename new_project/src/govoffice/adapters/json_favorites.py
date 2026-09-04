from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from ..domain.functions import 기능, 기능출처


class JSON즐겨찾기저장소:
    def __init__(self, 경로: str | Path):
        self.경로 = Path(경로)

    def 전체(self) -> tuple[기능, ...]:
        if not self.경로.exists():
            return ()
        데이터 = json.loads(self.경로.read_text(encoding="utf-8"))
        결과 = []
        for 항목 in 데이터.get("favorites", []):
            항목["출처"] = 기능출처(항목["출처"])
            항목["인자"] = tuple(항목.get("인자", ()))
            항목["키워드인자"] = dict(항목.get("키워드인자", {}))
            항목["매개변수"] = tuple(항목.get("매개변수", ()))
            결과.append(기능(**항목))
        return tuple(결과)

    def 저장(self, 기능목록: tuple[기능, ...]) -> None:
        self.경로.parent.mkdir(parents=True, exist_ok=True)
        데이터 = {"favorites": [asdict(기능) for 기능 in 기능목록]}
        임시경로 = self.경로.with_suffix(self.경로.suffix + ".tmp")
        임시경로.write_text(
            json.dumps(데이터, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        임시경로.replace(self.경로)
