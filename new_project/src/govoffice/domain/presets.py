from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class 서식필드:
    """민감한 원문 대신 서식 프리셋 안에 들어가는 안전한 입력 자리."""

    id: str
    토큰: str
    안내문구: str
    글자모양id: str | None = None
    문단모양id: str | None = None
    스타일: dict[str, str | int | float | bool | None] = field(default_factory=dict)
    값유형: str = "example"
    출력형식: str | None = None
    # 대표필드 이름이 바뀌어도 이미 저장된 프리셋이 같은 사용자 필드를
    # 가리킬 수 있도록 보존하는 안정 식별자다. 이전 프리셋은 None이다.
    프로필필드id: str | None = None
    # 하나의 값이 여러 CHAR/TEXT 런에 걸쳐 있으면 각 런의 글자
    # 서식을 보존해야 한다. 각 위치는 ``(조각 표식, 원문 길이)``의
    # 묶음이며, 이전 프리셋은 빈 튜플을 사용한다.
    조각그룹: tuple[tuple[tuple[str, int], ...], ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class 서식프리셋:
    """선택 영역의 내용과 전체 디자인을 저장한 HWPML 서식 조각."""

    id: str
    이름: str
    hwpml: str
    필드목록: tuple[서식필드, ...] = field(default_factory=tuple)
    생성시각: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )
    범위: str = "selection"
    내용정책: str = "sanitize"
    # 프리셋이 추출된 문서에서 확인한 라벨/값 셀의 정규화 서명이다.
    # HWPML 원본도 서식을 보존하지만, 이 규칙은 다음 분석 때 역할을
    # 설명하고 재사용할 수 있도록 메타데이터로 별도 저장한다.
    셀서식규칙: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def 필드수(self) -> int:
        return len(self.필드목록)
