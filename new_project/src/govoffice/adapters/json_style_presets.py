from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from ..domain.presets import 서식필드, 서식프리셋


class JSON서식프리셋저장소:
    """메타데이터 JSON과 선택 영역 HWPML을 한 쌍으로 보관한다."""

    def __init__(self, 디렉터리: str | Path) -> None:
        self._디렉터리 = Path(디렉터리)

    def 저장(self, 프리셋: 서식프리셋) -> None:
        self._디렉터리.mkdir(parents=True, exist_ok=True)
        메타데이터 = {
            "schema_version": 4,
            "id": 프리셋.id,
            "name": 프리셋.이름,
            "created_at": 프리셋.생성시각,
            "scope": 프리셋.범위,
            "content_policy": 프리셋.내용정책,
            "template": f"{프리셋.id}.hml",
            "fields": [asdict(필드) for 필드 in 프리셋.필드목록],
            "cell_style_rules": {
                str(역할): list(서명목록)
                for 역할, 서명목록 in 프리셋.셀서식규칙.items()
            },
        }
        self._쌍저장(
            프리셋.id,
            프리셋.hwpml,
            json.dumps(메타데이터, ensure_ascii=False, indent=2),
        )

    def 목록(self) -> tuple[서식프리셋, ...]:
        결과 = []
        if not self._디렉터리.exists():
            return ()
        for 경로 in self._디렉터리.glob("style_*.json"):
            try:
                결과.append(self._메타데이터읽기(경로))
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                continue
        return tuple(sorted(결과, key=lambda 항목: 항목.생성시각, reverse=True))

    def 불러오기(self, 프리셋id: str) -> 서식프리셋:
        안전한id = self._id검증(프리셋id)
        경로 = self._디렉터리 / f"{안전한id}.json"
        if not 경로.is_file():
            raise KeyError(f"서식 프리셋을 찾을 수 없습니다: {안전한id}")
        return self._메타데이터읽기(경로)

    def 삭제(self, 프리셋id: str) -> bool:
        안전한id = self._id검증(프리셋id)
        삭제됨 = False
        for 확장자 in (".json", ".hml"):
            경로 = self._디렉터리 / f"{안전한id}{확장자}"
            if 경로.is_file():
                경로.unlink()
                삭제됨 = True
        return 삭제됨

    def _메타데이터읽기(self, 경로: Path) -> 서식프리셋:
        데이터 = json.loads(경로.read_text(encoding="utf-8"))
        프리셋id = self._id검증(str(데이터["id"]))
        범위 = str(데이터.get("scope", "selection"))
        if 범위 not in {"selection", "selection_page", "document"}:
            raise ValueError(f"허용되지 않은 프리셋 범위입니다: {범위}")
        내용정책 = str(데이터.get("content_policy", "sanitize"))
        if 내용정책 not in {"sanitize", "original", "registered_fields"}:
            raise ValueError(f"허용되지 않은 내용 보존 정책입니다: {내용정책}")
        템플릿이름 = str(데이터.get("template", f"{프리셋id}.hml"))
        if Path(템플릿이름).name != 템플릿이름 or 템플릿이름 != f"{프리셋id}.hml":
            raise ValueError("허용되지 않은 프리셋 템플릿 경로입니다.")
        hwpml = (self._디렉터리 / 템플릿이름).read_text(encoding="utf-8")
        def 조각그룹읽기(원본: object) -> tuple[tuple[tuple[str, int], ...], ...]:
            if 원본 in (None, []):
                return ()
            if not isinstance(원본, list):
                raise ValueError("서식 필드의 조각 서식 정보가 올바르지 않습니다.")
            그룹목록: list[tuple[tuple[str, int], ...]] = []
            for 그룹 in 원본:
                if not isinstance(그룹, list) or not 그룹:
                    raise ValueError("서식 필드의 조각 그룹이 올바르지 않습니다.")
                조각목록: list[tuple[str, int]] = []
                for 조각 in 그룹:
                    if not isinstance(조각, list) or len(조각) != 2:
                        raise ValueError("서식 필드의 조각 위치가 올바르지 않습니다.")
                    표식 = str(조각[0])
                    try:
                        길이 = int(조각[1])
                    except (TypeError, ValueError) as 오류:
                        raise ValueError("서식 필드의 조각 길이가 올바르지 않습니다.") from 오류
                    if not 표식 or 길이 < 0:
                        raise ValueError("서식 필드의 조각 정보가 올바르지 않습니다.")
                    조각목록.append((표식, 길이))
                그룹목록.append(tuple(조각목록))
            return tuple(그룹목록)

        필드목록 = tuple(
            서식필드(
                id=str(항목["id"]),
                토큰=str(항목["토큰"]),
                안내문구=str(항목["안내문구"]),
                글자모양id=항목.get("글자모양id"),
                문단모양id=항목.get("문단모양id"),
                스타일=dict(항목.get("스타일", {})),
                값유형=str(항목.get("값유형", "example")),
                출력형식=항목.get("출력형식"),
                프로필필드id=(
                    str(항목["프로필필드id"])
                    if 항목.get("프로필필드id")
                    else None
                ),
                조각그룹=조각그룹읽기(항목.get("조각그룹")),
            )
            for 항목 in 데이터.get("fields", [])
        )
        원시서식규칙 = 데이터.get("cell_style_rules", {})
        if not isinstance(원시서식규칙, dict):
            raise ValueError("셀 서식 판별 규칙이 올바르지 않습니다.")
        셀서식규칙: dict[str, tuple[str, ...]] = {}
        for 역할 in ("field", "value"):
            원시목록 = 원시서식규칙.get(역할, [])
            if not isinstance(원시목록, list):
                raise ValueError("셀 서식 서명 목록이 올바르지 않습니다.")
            서명목록 = tuple(dict.fromkeys(str(서명) for 서명 in 원시목록 if str(서명)))
            셀서식규칙[역할] = 서명목록
        return 서식프리셋(
            id=프리셋id,
            이름=str(데이터["name"]),
            hwpml=hwpml,
            필드목록=필드목록,
            생성시각=str(데이터["created_at"]),
            범위=범위,
            내용정책=내용정책,
            셀서식규칙=셀서식규칙,
        )

    @staticmethod
    def _id검증(프리셋id: str) -> str:
        if not 프리셋id.startswith("style_") or not 프리셋id[6:].isalnum():
            raise ValueError("허용되지 않은 서식 프리셋 ID입니다.")
        return 프리셋id

    def _쌍저장(self, 프리셋id: str, hwpml: str, 메타데이터: str) -> None:
        """HWPML과 JSON을 하나의 논리적 트랜잭션으로 교체한다.

        ``.json``은 목록/불러오기가 프리셋을 발견하는 커밋 표식이다.
        따라서 두 임시 파일을 모두 디스크에 동기화한 뒤 HWPML을 먼저,
        JSON을 마지막에 교체한다. 기존 프리셋은 커밋 전에 숨은
        백업으로 이동하고, 중간 오류가 나면 HWPML을 먼저 복구한 후
        JSON을 마지막에 복구한다.
        """

        안전한id = self._id검증(프리셋id)
        hml경로 = self._디렉터리 / f"{안전한id}.hml"
        json경로 = self._디렉터리 / f"{안전한id}.json"
        트랜잭션id = uuid4().hex
        임시hml = self._디렉터리 / f".{안전한id}.{트랜잭션id}.new.hml"
        임시json = self._디렉터리 / f".{안전한id}.{트랜잭션id}.new.json"
        백업hml = self._디렉터리 / f".{안전한id}.{트랜잭션id}.backup.hml"
        백업json = self._디렉터리 / f".{안전한id}.{트랜잭션id}.backup.json"

        기존hml = hml경로.is_file()
        기존json = json경로.is_file()
        hml백업됨 = False
        json백업됨 = False
        hml승격됨 = False
        json승격됨 = False
        보존할백업: set[Path] = set()

        try:
            # 커밋을 시작하기 전에 두 파일 모두의 쓰기와 fsync가
            # 성공해야 한다. 하나라도 실패하면 기존 파일은 건드리지 않는다.
            self._동기화쓰기(임시hml, hwpml)
            self._동기화쓰기(임시json, 메타데이터)

            # JSON이 보이는 동안은 저장소가 프리셋을 커밋된 것으로
            # 판단하므로 먼저 숨긴다.
            if 기존json:
                os.replace(json경로, 백업json)
                json백업됨 = True
            if 기존hml:
                os.replace(hml경로, 백업hml)
                hml백업됨 = True

            os.replace(임시hml, hml경로)
            hml승격됨 = True
            os.replace(임시json, json경로)
            json승격됨 = True
        except BaseException as 오류:
            보존할백업.update(
                self._쌍저장롤백(
                    hml경로=hml경로,
                    json경로=json경로,
                    백업hml=백업hml,
                    백업json=백업json,
                    기존hml=기존hml,
                    기존json=기존json,
                    hml백업됨=hml백업됨,
                    json백업됨=json백업됨,
                    hml승격됨=hml승격됨,
                    json승격됨=json승격됨,
                )
            )
            if isinstance(오류, (OSError, UnicodeError)):
                raise ValueError(
                    f"서식 프리셋 파일을 저장할 수 없습니다: {안전한id}"
                ) from 오류
            raise
        finally:
            for 경로 in (임시hml, 임시json, 백업hml, 백업json):
                if 경로 not in 보존할백업:
                    self._안전삭제(경로)

    @staticmethod
    def _동기화쓰기(경로: Path, 내용: str) -> None:
        with 경로.open("w", encoding="utf-8", newline="\n") as 파일:
            파일.write(내용)
            파일.flush()
            os.fsync(파일.fileno())

    @classmethod
    def _쌍저장롤백(
        cls,
        *,
        hml경로: Path,
        json경로: Path,
        백업hml: Path,
        백업json: Path,
        기존hml: bool,
        기존json: bool,
        hml백업됨: bool,
        json백업됨: bool,
        hml승격됨: bool,
        json승격됨: bool,
    ) -> tuple[Path, ...]:
        보존할백업: set[Path] = set()
        # 신규 JSON을 먼저 숨겨 롤백 중 목록에 반쪽짜리 프리셋이
        # 노출되지 않게 한다.
        if json승격됨 or json백업됨:
            cls._안전삭제(json경로)
        if hml승격됨:
            cls._안전삭제(hml경로)

        hml복구됨 = 기존hml and not hml백업됨 and hml경로.is_file()
        if 기존hml and hml백업됨 and 백업hml.is_file():
            try:
                os.replace(백업hml, hml경로)
                hml복구됨 = True
            except OSError:
                hml복구됨 = False
                보존할백업.add(백업hml)
                if 백업json.is_file():
                    보존할백업.add(백업json)

        # 기존에 완전한 쌍이 있었고 HWPML 복구까지 성공한
        # 경우에만 JSON 커밋 표식을 복구한다. JSON만 있던 기존
        # 고아 파일은 다시 노출하지 않는다.
        if (
            기존json
            and 기존hml
            and json백업됨
            and hml복구됨
            and 백업json.is_file()
        ):
            try:
                os.replace(백업json, json경로)
            except OSError:
                cls._안전삭제(json경로)
                보존할백업.add(백업json)
        elif 기존json and not json백업됨:
            # JSON 백업 이전에 실패했다면 원본은 그대로이다.
            pass
        else:
            cls._안전삭제(json경로)
            if 기존json and json백업됨 and 백업json.is_file():
                # JSON만 있던 고아 파일도 데이터 유실 대신 숨은
                # 복구용 백업으로 남긴다. 목록에는 노출되지 않는다.
                보존할백업.add(백업json)

        return tuple(보존할백업)

    @staticmethod
    def _안전삭제(경로: Path) -> None:
        try:
            경로.unlink(missing_ok=True)
        except OSError:
            pass
