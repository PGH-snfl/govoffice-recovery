from __future__ import annotations

import json
from pathlib import Path

from ..domain.functions import 기능, 기능출처, 기관


class 기관카탈로그오류(ValueError):
    pass


def 기본패키지경로() -> Path:
    return Path(__file__).resolve().parent / "packages"


class 기관카탈로그:
    필수항목 = ("id", "name", "type", "version", "api_version", "functions")

    def __init__(self, 패키지경로: str | Path | None = None):
        self.패키지경로 = Path(패키지경로) if 패키지경로 else 기본패키지경로()

    def _manifest읽기(self, 경로: Path) -> 기관:
        try:
            데이터 = json.loads(경로.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise 기관카탈로그오류(f"기관 manifest를 읽을 수 없습니다: {경로}") from e
        누락 = [이름 for 이름 in self.필수항목 if 이름 not in 데이터]
        if 누락:
            raise 기관카탈로그오류(f"기관 manifest 필수 항목 누락: {', '.join(누락)}")

        기능목록 = []
        for 항목 in 데이터["functions"]:
            기능목록.append(
                기능(
                    id=항목["id"],
                    이름=항목["name"],
                    출처=기능출처.기관,
                    실행메서드=항목["method"],
                    기관id=데이터["id"],
                    매개변수=tuple(항목.get("parameters", ())),
                    화면실행가능=항목.get("ui_ready", True),
                    복구상태=항목.get("recovery_status", "source"),
                )
            )
        return 기관(id=데이터["id"], 이름=데이터["name"], 기능목록=tuple(기능목록))

    def 전체(self) -> tuple[기관, ...]:
        결과 = []
        ids = set()
        if not self.패키지경로.exists():
            return ()
        for 경로 in sorted(self.패키지경로.glob("*/manifest.json")):
            기관정보 = self._manifest읽기(경로)
            if 기관정보.id in ids:
                raise 기관카탈로그오류(f"중복 기관 ID: {기관정보.id}")
            ids.add(기관정보.id)
            결과.append(기관정보)
        return tuple(결과)

    def 찾기(self, 기관id: str) -> 기관:
        try:
            return next(기관정보 for 기관정보 in self.전체() if 기관정보.id == 기관id)
        except StopIteration as e:
            raise 기관카탈로그오류(f"등록되지 않은 기관: {기관id}") from e

