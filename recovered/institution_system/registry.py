"""내부용 기관 라이브러리 등록부."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


class 기관등록오류(ValueError):
    pass


@dataclass(frozen=True)
class 기관정보:
    id: str
    name: str
    type: str
    version: str
    api_version: str
    package_path: Path
    functions: tuple[dict, ...]


class 기관등록부:
    """`institutions/*/manifest.json`을 읽어 기관 목록을 구성한다."""

    필수항목 = ("id", "name", "type", "version", "api_version", "functions")

    def __init__(self, 기관폴더: str | Path):
        self.기관폴더 = Path(기관폴더)

    def _읽기(self, manifest경로: Path) -> 기관정보:
        try:
            데이터 = json.loads(manifest경로.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise 기관등록오류(f"기관 설정을 읽을 수 없습니다: {manifest경로}") from e

        누락 = [항목 for 항목 in self.필수항목 if 항목 not in 데이터]
        if 누락:
            raise 기관등록오류(f"기관 설정 필수 항목 누락: {', '.join(누락)}")
        if not isinstance(데이터["functions"], list):
            raise 기관등록오류("functions는 목록이어야 합니다.")

        return 기관정보(
            id=데이터["id"],
            name=데이터["name"],
            type=데이터["type"],
            version=데이터["version"],
            api_version=데이터["api_version"],
            package_path=manifest경로.parent,
            functions=tuple(데이터["functions"]),
        )

    def 전체기관(self) -> dict[str, 기관정보]:
        결과 = {}
        if not self.기관폴더.exists():
            return 결과
        for manifest경로 in sorted(self.기관폴더.glob("*/manifest.json")):
            기관 = self._읽기(manifest경로)
            if 기관.id in 결과:
                raise 기관등록오류(f"중복 기관 ID: {기관.id}")
            결과[기관.id] = 기관
        return 결과

    def 기관찾기(self, 기관id: str) -> 기관정보:
        try:
            return self.전체기관()[기관id]
        except KeyError as e:
            raise 기관등록오류(f"등록되지 않은 기관: {기관id}") from e

