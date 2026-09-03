from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import uuid4

from ..domain.user_profile import 사용자프로필


class JSON사용자프로필저장소:
    """내부용 사용자 프로필을 사람이 확인 가능한 JSON으로 보관한다."""

    def __init__(self, 경로: str | Path) -> None:
        self._경로 = Path(경로)

    def 불러오기(self) -> 사용자프로필:
        if not self._경로.is_file():
            return 사용자프로필()
        try:
            데이터 = json.loads(self._경로.read_text(encoding="utf-8"))
            if 데이터.get("schema_version") not in {2, 3, 4}:
                raise ValueError("지원하지 않는 사용자 프로필 형식입니다.")
            return 사용자프로필.생성(데이터.get("values", {}))
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as 오류:
            raise ValueError("저장된 사용자 프로필 JSON을 읽을 수 없습니다.") from 오류

    def 저장(self, 프로필: 사용자프로필) -> None:
        # v2의 평면 필드는 사용자프로필.생성에서 대표필드로 이전하고,
        # 첫 저장부터 안정 ID·별칭·값 목록·기본값·부모 ID를 가진 v4로 고정한다.
        데이터 = {"schema_version": 4, "values": 프로필.사전()}
        self._경로.parent.mkdir(parents=True, exist_ok=True)
        임시경로 = self._경로.with_name(f".{self._경로.name}.{uuid4().hex}.tmp")
        try:
            with 임시경로.open("w", encoding="utf-8", newline="\n") as 파일:
                json.dump(데이터, 파일, ensure_ascii=False, indent=2)
                파일.write("\n")
                파일.flush()
                os.fsync(파일.fileno())
            임시경로.replace(self._경로)
        except (OSError, UnicodeError) as 오류:
            raise ValueError("사용자 프로필 파일을 저장할 수 없습니다.") from 오류
        finally:
            try:
                임시경로.unlink(missing_ok=True)
            except OSError:
                pass
