from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping, Sequence
from uuid import uuid4


기본사용자정보필드 = ("이름", "전화번호", "이메일")
# 이전 호출 코드가 가져가는 이름은 유지하되 고정 필드는 세 개로 제한한다.
사용자정보필드 = 기본사용자정보필드
기본대표필드별칭: dict[str, tuple[str, ...]] = {
    "이름": ("성명", "성함"),
    "전화번호": ("전화", "연락처", "휴대전화"),
    "이메일": ("전자우편", "E-mail"),
}
_레거시기타필드 = ("소속", "부서", "직위")


def _문자열(값: object, 이름: str, 최대길이: int = 1000) -> str:
    결과 = str(값 or "").strip()
    if len(결과) > 최대길이:
        raise ValueError(f"{이름} 값이 너무 깁니다.")
    return 결과


def _원시목록(값: object, 이름: str) -> tuple[object, ...]:
    if 값 is None:
        return ()
    if isinstance(값, (str, bytes)):
        return (값,)
    if not isinstance(값, Sequence):
        raise ValueError(f"{이름}은(는) 목록이어야 합니다.")
    return tuple(값)


def _새필드ID() -> str:
    return f"profile_field_{uuid4().hex}"


@dataclass(frozen=True, slots=True)
class 사용자문서항목:
    """이전 UI가 사용하는 필드 이름과 실제 입력값 한 쌍."""

    필드명: str
    입력값: str

    @classmethod
    def 생성(cls, 필드명: object, 입력값: object) -> "사용자문서항목":
        이름 = _문자열(필드명, "필드 이름", 100)
        값 = _문자열(입력값, "입력값")
        if not 이름:
            raise ValueError("필드 이름을 입력하세요.")
        if not 값:
            raise ValueError("필드 입력값을 입력하세요.")
        return cls(이름, 값)

    def 사전(self) -> dict[str, str]:
        return {"필드명": self.필드명, "입력값": self.입력값}


@dataclass(frozen=True, slots=True)
class 사용자대표필드:
    """문서의 여러 별칭과 여러 값을 한 의미 단위로 묶는 대표 필드."""

    대표필드명: str
    별칭: tuple[str, ...] = ()
    값목록: tuple[str, ...] = ()
    기본값: str = ""
    id: str = ""
    # 빈 문자열이면 최상위 대표필드, 값이 있으면 해당 안정 ID 아래의
    # 하위 필드다. 이름 대신 ID를 저장해 부모 이름 변경에도 관계가 유지된다.
    상위필드id: str = ""

    @classmethod
    def 생성(cls, 원시값: Mapping[str, object]) -> "사용자대표필드":
        필드명 = _문자열(
            원시값.get(
                "대표필드명",
                원시값.get(
                    "대표필드",
                    원시값.get("필드명", 원시값.get("canonical_name", 원시값.get("name", ""))),
                ),
            ),
            "대표 필드 이름",
            100,
        )
        if not 필드명:
            raise ValueError("대표 필드 이름을 입력하세요.")

        원시별칭 = 원시값.get("별칭", 원시값.get("aliases", ()))
        별칭목록: list[str] = []
        본별칭: set[str] = {필드명.casefold()}
        for 원시별칭값 in _원시목록(원시별칭, "별칭"):
            별칭 = _문자열(원시별칭값, "별칭", 100)
            if not 별칭:
                continue
            키 = 별칭.casefold()
            if 키 in 본별칭:
                continue
            본별칭.add(키)
            별칭목록.append(별칭)

        원시입력값 = 원시값.get(
            "값목록",
            원시값.get("values", 원시값.get("입력값", 원시값.get("value", ()))),
        )
        값목록: list[str] = []
        본값: set[str] = set()
        for 원시입력값항목 in _원시목록(원시입력값, "대표 필드 값"):
            입력값 = _문자열(원시입력값항목, "입력값")
            if not 입력값 or 입력값 in 본값:
                continue
            본값.add(입력값)
            값목록.append(입력값)

        기본값키 = next(
            (키 for 키 in ("기본값", "default", "default_value") if 키 in 원시값),
            None,
        )
        if 기본값키 is None:
            기본값 = 값목록[0] if 값목록 else ""
        else:
            기본값 = _문자열(원시값.get(기본값키, ""), "기본값")
            if 기본값 and 기본값 not in 본값:
                값목록.insert(0, 기본값)

        필드ID = _문자열(
            원시값.get("id", 원시값.get("profile_field_id", "")),
            "대표 필드 ID",
            200,
        ) or _새필드ID()
        상위필드ID = _문자열(
            원시값.get(
                "상위필드id",
                원시값.get("parent_field_id", 원시값.get("parent_id", "")),
            ),
            "상위 대표 필드 ID",
            200,
        )
        if len(값목록) > 1000:
            raise ValueError("한 대표 필드에는 값을 최대 1000개까지 저장할 수 있습니다.")
        if len(별칭목록) > 1000:
            raise ValueError("한 대표 필드에는 별칭을 최대 1000개까지 저장할 수 있습니다.")
        if 상위필드ID == 필드ID:
            raise ValueError("대표 필드는 자기 자신을 상위 필드로 지정할 수 없습니다.")
        return cls(
            필드명,
            tuple(별칭목록),
            tuple(값목록),
            기본값,
            필드ID,
            상위필드ID,
        )

    @property
    def 대표필드(self) -> str:
        return self.대표필드명

    def 사전(self) -> dict[str, object]:
        return {
            "id": self.id,
            "대표필드명": self.대표필드명,
            "별칭": list(self.별칭),
            "값목록": list(self.값목록),
            "기본값": self.기본값,
            "상위필드id": self.상위필드id,
        }

    def 일치(self, 필드명: object) -> bool:
        이름 = _문자열(필드명, "필드 이름", 100)
        if not 이름:
            return False
        키 = 이름.casefold()
        return 키 == self.대표필드명.casefold() or any(
            키 == 별칭.casefold() for 별칭 in self.별칭
        )


def _대표필드병합(필드목록: Sequence[사용자대표필드]) -> tuple[사용자대표필드, ...]:
    """같은 부모 아래의 같은 필드는 합치고, 형제 사이 이름 충돌은 거부한다."""

    결과: list[사용자대표필드] = []
    필드위치: dict[str, int] = {}
    for 필드 in 필드목록:
        키 = f"{필드.상위필드id.casefold()}\0{필드.대표필드명.casefold()}"
        if 키 not in 필드위치:
            필드위치[키] = len(결과)
            결과.append(필드)
            continue
        위치 = 필드위치[키]
        기존 = 결과[위치]
        별칭 = list(기존.별칭)
        본별칭 = {항목.casefold() for 항목 in (기존.대표필드명, *별칭)}
        for 항목 in 필드.별칭:
            if 항목.casefold() not in 본별칭:
                본별칭.add(항목.casefold())
                별칭.append(항목)
        값목록 = list(기존.값목록)
        for 입력값 in 필드.값목록:
            if 입력값 not in 값목록:
                값목록.append(입력값)
        결과[위치] = 사용자대표필드.생성(
            {
                "id": 기존.id,
                "대표필드명": 기존.대표필드명,
                "별칭": 별칭,
                "값목록": 값목록,
                "기본값": 기존.기본값,
                "상위필드id": 기존.상위필드id,
            }
        )

    ID목록: set[str] = set()
    이름소유자: dict[tuple[str, str], 사용자대표필드] = {}
    for 필드 in 결과:
        if 필드.id in ID목록:
            raise ValueError(f"대표 필드 ID '{필드.id}'가 중복되었습니다.")
        ID목록.add(필드.id)
        for 이름 in (필드.대표필드명, *필드.별칭):
            키 = (필드.상위필드id.casefold(), 이름.casefold())
            이전 = 이름소유자.get(키)
            if 이전 is not None and 이전.id != 필드.id:
                raise ValueError(
                    f"필드 이름 또는 별칭 '{이름}'이 대표 필드 "
                    f"'{이전.대표필드명}'과(와) 겹칩니다."
                )
            이름소유자[키] = 필드
    ID필드 = {필드.id: 필드 for 필드 in 결과}
    for 필드 in 결과:
        if not 필드.상위필드id:
            continue
        상위 = ID필드.get(필드.상위필드id)
        if 상위 is None:
            raise ValueError(
                f"하위 필드 '{필드.대표필드명}'의 상위 대표 필드를 찾을 수 없습니다."
            )
        # 대표필드 아래에 다른 대표필드를 옮겨 사용자가 직접 계층을
        # 구성할 수 있다. 대신 순환 참조만은 저장 단계에서 차단한다.
        본ID = {필드.id}
        현재 = 상위
        while 현재 is not None:
            if 현재.id in 본ID:
                raise ValueError("대표필드 계층을 순환 구조로 만들 수 없습니다.")
            본ID.add(현재.id)
            현재 = ID필드.get(현재.상위필드id) if 현재.상위필드id else None
    if len(결과) > 1003:
        raise ValueError("대표 필드는 최대 1003개까지 저장할 수 있습니다.")
    return tuple(결과)


def _대표필드에값추가(
    필드: 사용자대표필드,
    입력값: str,
    *,
    비어있으면기본값: bool = True,
) -> 사용자대표필드:
    if 입력값 in 필드.값목록:
        return 필드
    값목록 = (*필드.값목록, 입력값)
    기본값 = 필드.기본값
    if 비어있으면기본값 and not 기본값 and len(값목록) == 1:
        기본값 = 입력값
    return 사용자대표필드.생성(
        {
            "id": 필드.id,
            "대표필드명": 필드.대표필드명,
            "별칭": 필드.별칭,
            "값목록": 값목록,
            "기본값": 기본값,
            "상위필드id": 필드.상위필드id,
        }
    )


@dataclass(frozen=True, slots=True)
class 사용자프로필:
    이름: str = ""
    전화번호: str = ""
    이메일: str = ""
    문서항목: tuple[사용자문서항목, ...] = ()
    대표필드목록: tuple[사용자대표필드, ...] = ()

    @classmethod
    def 생성(cls, 값: Mapping[str, object]) -> "사용자프로필":
        if not isinstance(값, Mapping):
            raise ValueError("사용자 프로필 값은 객체여야 합니다.")

        원시대표필드 = 값.get(
            "대표필드목록",
            값.get("대표필드", 값.get("canonical_fields", 값.get("fields"))),
        )
        대표필드입력있음 = 원시대표필드 is not None
        대표필드목록: list[사용자대표필드] = []
        if isinstance(원시대표필드, Mapping):
            for 필드명, 필드값 in 원시대표필드.items():
                if isinstance(필드값, Mapping):
                    정의 = dict(필드값)
                    정의.setdefault("대표필드명", 필드명)
                else:
                    정의 = {"대표필드명": 필드명, "값목록": 필드값}
                대표필드목록.append(사용자대표필드.생성(정의))
        elif 원시대표필드 is not None:
            if not isinstance(원시대표필드, Sequence) or isinstance(
                원시대표필드, (str, bytes)
            ):
                raise ValueError("대표 필드 목록은 객체 목록이어야 합니다.")
            for 원시필드 in 원시대표필드:
                if not isinstance(원시필드, Mapping):
                    raise ValueError("대표 필드는 이름·별칭·값을 가진 객체여야 합니다.")
                대표필드목록.append(사용자대표필드.생성(원시필드))

        # schema v2와 기존 API의 평면 기본값은 각 이름의 대표 필드로 이전한다.
        if not 대표필드입력있음:
            for 필드명 in 기본사용자정보필드:
                입력값 = _문자열(값.get(필드명, ""), 필드명, 500)
                대표필드목록.append(
                    사용자대표필드.생성(
                        {
                            "대표필드명": 필드명,
                            "별칭": 기본대표필드별칭[필드명],
                            "값목록": (입력값,) if 입력값 else (),
                            "기본값": 입력값,
                        }
                    )
                )

        대표필드목록 = list(_대표필드병합(대표필드목록))

        # 기존 v3에 별칭이 없더라도 기본 세 필드는 대표필드로 보장하고,
        # 다른 대표필드가 이미 소유하지 않은 표준 별칭만 안전하게 보강한다.
        for 기본순번, 필드명 in enumerate(기본사용자정보필드):
            기본필드 = next(
                (
                    대표필드
                    for 대표필드 in 대표필드목록
                    if not 대표필드.상위필드id
                    and 대표필드.대표필드명.casefold() == 필드명.casefold()
                ),
                None,
            )
            if 기본필드 is None:
                기본이름소유자 = next(
                    (
                        대표필드
                        for 대표필드 in 대표필드목록
                        if not 대표필드.상위필드id
                        if any(별칭.casefold() == 필드명.casefold() for 별칭 in 대표필드.별칭)
                    ),
                    None,
                )
                if 기본이름소유자 is not None:
                    raise ValueError(f"{필드명}은(는) 기본 대표 필드 이름으로 사용해야 합니다.")
                기본필드 = 사용자대표필드.생성({"대표필드명": 필드명})
                대표필드목록.insert(min(기본순번, len(대표필드목록)), 기본필드)

            위치 = next(
                위치
                for 위치, 대표필드 in enumerate(대표필드목록)
                if 대표필드.id == 기본필드.id
            )
            별칭목록 = list(기본필드.별칭)
            for 기본별칭 in 기본대표필드별칭[필드명]:
                소유자 = next(
                    (
                        대표필드
                        for 대표필드 in 대표필드목록
                        if 대표필드.상위필드id == 기본필드.상위필드id
                        if 대표필드.일치(기본별칭)
                    ),
                    None,
                )
                if 소유자 is None:
                    별칭목록.append(기본별칭)
            if tuple(별칭목록) != 기본필드.별칭:
                대표필드목록[위치] = replace(기본필드, 별칭=tuple(별칭목록))

        대표필드목록 = list(_대표필드병합(대표필드목록))

        def 필드찾기(필드명: str) -> tuple[int, 사용자대표필드] | None:
            키 = 필드명.casefold()
            # 레거시 평면 입력은 최상위 필드만 대상으로 한다. 하위 필드는
            # 안정 ID 또는 ``상위 > 하위`` 경로로 명시해야 한다.
            for 위치, 대표필드 in enumerate(대표필드목록):
                if 대표필드.상위필드id:
                    continue
                if 키 == 대표필드.대표필드명.casefold() or any(
                    키 == 별칭.casefold() for 별칭 in 대표필드.별칭
                ):
                    return 위치, 대표필드
            return None

        # v3/v4의 문서항목은 UI 호환용 평면 투영이다. 대표필드목록이
        # 있으면 안정 ID 기반 트리를 유일한 원본으로 사용해 하위 필드를
        # ``상위 > 하위``라는 별도 루트 필드로 중복 생성하지 않는다.
        원시항목 = () if 대표필드입력있음 else 값.get("문서항목", 값.get("기타필드", ()))
        항목목록: list[사용자문서항목] = []
        if isinstance(원시항목, Sequence) and not isinstance(원시항목, (str, bytes)):
            for 원시값 in 원시항목:
                if not isinstance(원시값, Mapping):
                    raise ValueError("기타 문서 항목은 필드명과 입력값을 가진 객체여야 합니다.")
                필드명 = 원시값.get(
                    "필드명",
                    원시값.get("name", 원시값.get("canonical_field", "")),
                )
                입력값목록 = 원시값.get(
                    "입력값",
                    원시값.get("value", 원시값.get("values", "")),
                )
                for 입력값 in _원시목록(입력값목록, "입력값"):
                    항목목록.append(사용자문서항목.생성(필드명, 입력값))
        elif 원시항목 is not None:
            raise ValueError("기타 문서 항목은 객체 목록이어야 합니다.")

        # schema v1의 소속·부서·직위도 각각 독립된 대표 필드로 이전한다.
        for 필드명 in _레거시기타필드:
            이전값 = _문자열(값.get(필드명, ""), 필드명, 500)
            if 이전값:
                항목목록.append(사용자문서항목(필드명, 이전값))

        본쌍: set[tuple[str, str]] = set()
        for 항목 in 항목목록:
            키 = (항목.필드명.casefold(), 항목.입력값)
            if 키 in 본쌍:
                continue
            본쌍.add(키)
            찾은필드 = 필드찾기(항목.필드명)
            if 찾은필드 is None:
                대표필드목록.append(
                    사용자대표필드.생성(
                        {"대표필드명": 항목.필드명, "값목록": (항목.입력값,)}
                    )
                )
                continue
            위치, 대표필드 = 찾은필드
            대표필드목록[위치] = _대표필드에값추가(대표필드, 항목.입력값)

        # 기본정보 저장 API가 대표필드 목록을 함께 왕복하더라도 상단 편집값을 반영한다.
        for 기본순번, 필드명 in enumerate(기본사용자정보필드):
            찾은필드 = next(
                (
                    (위치, 대표필드)
                    for 위치, 대표필드 in enumerate(대표필드목록)
                    if not 대표필드.상위필드id
                    and 대표필드.대표필드명.casefold() == 필드명.casefold()
                ),
                None,
            )
            if 찾은필드 is None:
                # 기본 필드 이름이 다른 필드의 별칭이면 해석이 모호해지므로 추측하지 않는다.
                별칭소유자 = 필드찾기(필드명)
                if 별칭소유자 is not None:
                    raise ValueError(f"{필드명}은(는) 기본 대표 필드 이름으로 사용해야 합니다.")
                새필드 = 사용자대표필드.생성({"대표필드명": 필드명})
                대표필드목록.insert(min(기본순번, len(대표필드목록)), 새필드)
                찾은필드 = (대표필드목록.index(새필드), 새필드)
            if 필드명 not in 값:
                continue
            위치, 대표필드 = 찾은필드
            입력값 = _문자열(값.get(필드명, ""), 필드명, 500)
            if 입력값 == 대표필드.기본값:
                continue
            값목록 = [항목 for 항목 in 대표필드.값목록 if 항목 != 대표필드.기본값]
            if 입력값:
                값목록 = [입력값, *[항목 for 항목 in 값목록 if 항목 != 입력값]]
            대표필드목록[위치] = 사용자대표필드.생성(
                {
                    "id": 대표필드.id,
                    "대표필드명": 대표필드.대표필드명,
                    "별칭": 대표필드.별칭,
                    "값목록": 값목록,
                    "기본값": 입력값,
                }
            )

        대표필드목록 = list(_대표필드병합(대표필드목록))
        # UI와 역색인의 순서는 이름·전화번호·이메일 뒤에 사용자 필드가 오도록 고정한다.
        기본대표필드: list[사용자대표필드] = []
        기타대표필드: list[사용자대표필드] = []
        기본키 = {필드.casefold() for 필드 in 기본사용자정보필드}
        for 대표필드 in 대표필드목록:
            if not 대표필드.상위필드id and 대표필드.대표필드명.casefold() in 기본키:
                기본대표필드.append(대표필드)
            else:
                기타대표필드.append(대표필드)
        기본대표필드.sort(
            key=lambda 대표필드: tuple(x.casefold() for x in 기본사용자정보필드).index(
                대표필드.대표필드명.casefold()
            )
        )
        # 부모가 항상 모든 후손보다 먼저 오도록 해 UI와 직렬화 순서를
        # 안정시킨다. 같은 깊이의 입력 순서는 stable sort로 유지한다.
        필드표 = {필드.id: 필드 for 필드 in 대표필드목록}

        def 계층깊이(필드: 사용자대표필드) -> int:
            깊이 = 0
            현재 = 필드
            본ID: set[str] = set()
            while 현재.상위필드id:
                if 현재.id in 본ID:
                    break
                본ID.add(현재.id)
                상위 = 필드표.get(현재.상위필드id)
                if 상위 is None:
                    break
                깊이 += 1
                현재 = 상위
            return 깊이

        기타대표필드.sort(key=계층깊이)
        대표필드목록 = [*기본대표필드, *기타대표필드]

        기본값 = {
            대표필드.대표필드명: 대표필드.기본값
            for 대표필드 in 대표필드목록
            if not 대표필드.상위필드id
            and 대표필드.대표필드명.casefold() in 기본키
        }
        투영항목 = tuple(
            사용자문서항목(
                cls._필드경로_from_list(대표필드, 대표필드목록), 입력값
            )
            for 대표필드 in 기타대표필드
            for 입력값 in 대표필드.값목록
        )
        if len(투영항목) > 1000:
            raise ValueError("기타 문서 항목은 최대 1000개까지 저장할 수 있습니다.")
        return cls(
            **{필드: 기본값.get(필드, "") for 필드 in 기본사용자정보필드},
            문서항목=투영항목,
            대표필드목록=tuple(대표필드목록),
        )

    def _유효대표필드목록(self) -> tuple[사용자대표필드, ...]:
        if self.대표필드목록:
            return self.대표필드목록
        # 직접 생성한 기존 사용자프로필 객체도 새 조회 API에서 동일하게 보이게 한다.
        return type(self).생성(
            {
                **{필드: getattr(self, 필드) for 필드 in 기본사용자정보필드},
                "문서항목": [항목.사전() for 항목 in self.문서항목],
            }
        ).대표필드목록

    @property
    def 대표필드(self) -> tuple[사용자대표필드, ...]:
        return self._유효대표필드목록()

    def 사전(self) -> dict[str, object]:
        대표필드목록 = self._유효대표필드목록()
        기본정보 = self.기본정보사전()
        기본키 = {필드.casefold() for 필드 in 기본사용자정보필드}
        문서항목 = [
            사용자문서항목(self.필드경로(대표필드), 입력값).사전()
            for 대표필드 in 대표필드목록
            if 대표필드.대표필드명.casefold() not in 기본키
            for 입력값 in 대표필드.값목록
        ]
        return {
            **기본정보,
            "문서항목": 문서항목,
            "대표필드목록": [대표필드.사전() for 대표필드 in 대표필드목록],
        }

    def 기본정보사전(self) -> dict[str, str]:
        결과 = {필드: "" for 필드 in 기본사용자정보필드}
        기본키 = {필드.casefold(): 필드 for 필드 in 기본사용자정보필드}
        for 대표필드 in self._유효대표필드목록():
            if 대표필드.상위필드id:
                continue
            출력키 = 기본키.get(대표필드.대표필드명.casefold())
            if 출력키 is not None:
                결과[출력키] = 대표필드.기본값
        return 결과

    def 대표필드찾기(self, 필드명: object) -> 사용자대표필드 | None:
        이름 = _문자열(필드명, "필드 이름", 1000)
        if not 이름:
            return None
        필드목록 = self._유효대표필드목록()
        # 명시 경로는 임의 깊이의 계층을 부모부터 차례로 찾아간다.
        if ">" in 이름:
            경로 = [부분.strip() for 부분 in 이름.split(">") if 부분.strip()]
            if len(경로) < 2:
                return None
            후보 = [
                필드 for 필드 in 필드목록
                if not 필드.상위필드id and 필드.일치(경로[0])
            ]
            for 경로항목 in 경로[1:]:
                부모ID = {필드.id for 필드 in 후보}
                후보 = [
                    필드 for 필드 in 필드목록
                    if 필드.상위필드id in 부모ID and 필드.일치(경로항목)
                ]
                if not 후보:
                    return None
            return 후보[0] if len(후보) == 1 else None
        일치목록 = [필드 for 필드 in 필드목록 if 필드.일치(이름)]
        # 같은 하위 별칭이 여러 그룹에 있으면 추측하지 않는다. 반면
        # 최상위 이름은 이전 버전과 동일하게 우선한다.
        최상위 = [필드 for 필드 in 일치목록 if not 필드.상위필드id]
        if len(최상위) == 1:
            return 최상위[0]
        return 일치목록[0] if len(일치목록) == 1 else None

    @staticmethod
    def _필드경로_from_list(
        필드: 사용자대표필드,
        필드목록: Sequence[사용자대표필드],
    ) -> str:
        필드표 = {항목.id: 항목 for 항목 in 필드목록}
        경로 = [필드.대표필드명]
        현재 = 필드
        본ID = {필드.id}
        while 현재.상위필드id:
            상위 = 필드표.get(현재.상위필드id)
            if 상위 is None or 상위.id in 본ID:
                break
            본ID.add(상위.id)
            경로.append(상위.대표필드명)
            현재 = 상위
        return " > ".join(reversed(경로))

    def 필드경로(self, 필드: 사용자대표필드 | object) -> str:
        대상 = 필드 if isinstance(필드, 사용자대표필드) else self._변경대상찾기(필드)
        if 대상 is None:
            return ""
        return self._필드경로_from_list(대상, self._유효대표필드목록())

    def 하위필드목록(self, 상위필드: object) -> tuple[사용자대표필드, ...]:
        상위 = self.대표필드ID찾기(상위필드) or self.대표필드찾기(상위필드)
        if 상위 is None:
            return ()
        return tuple(
            필드 for 필드 in self._유효대표필드목록()
            if 필드.상위필드id == 상위.id
        )

    def 대표필드ID찾기(self, 필드ID: object) -> 사용자대표필드 | None:
        ID = _문자열(필드ID, "대표 필드 ID", 200)
        if not ID:
            return None
        return next(
            (대표필드 for 대표필드 in self._유효대표필드목록() if 대표필드.id == ID),
            None,
        )

    def 대표필드명찾기(self, 필드명: object) -> str | None:
        대표필드 = self.대표필드찾기(필드명)
        return 대표필드.대표필드명 if 대표필드 is not None else None

    def 필드ID찾기(self, 필드명: object) -> str | None:
        대표필드 = self.대표필드찾기(필드명)
        return 대표필드.id if 대표필드 is not None else None

    def 대표필드ID매핑(self) -> dict[str, str]:
        return {
            self.필드경로(대표필드): 대표필드.id
            for 대표필드 in self._유효대표필드목록()
        }

    def 필드값찾기(self, 필드명: object) -> tuple[str, ...]:
        대표필드 = self.대표필드찾기(필드명)
        return 대표필드.값목록 if 대표필드 is not None else ()

    def 필드기본값찾기(self, 필드명: object) -> str:
        대표필드 = self.대표필드찾기(필드명)
        return 대표필드.기본값 if 대표필드 is not None else ""

    def 별칭매핑(self) -> dict[str, tuple[str, ...]]:
        """표 분석기에 바로 전달할 대표필드명→별칭 목록을 반환한다."""

        return {
            self.필드경로(대표필드): tuple(
                f"{self.필드경로(self.대표필드ID찾기(대표필드.상위필드id))} > {별칭}"
                if 대표필드.상위필드id else 별칭
                for 별칭 in 대표필드.별칭
            )
            for 대표필드 in self._유효대표필드목록()
            if 대표필드.별칭
        }

    def 별칭대표필드매핑(self) -> dict[str, str]:
        결과: dict[str, str] = {}
        for 대표필드 in self._유효대표필드목록():
            경로 = self.필드경로(대표필드)
            상위 = self.대표필드ID찾기(대표필드.상위필드id)
            for 별칭 in 대표필드.별칭:
                키 = f"{self.필드경로(상위)} > {별칭}" if 상위 else 별칭
                결과[키] = 경로
        return 결과

    def 필드값목록(self) -> dict[str, tuple[str, ...]]:
        """대표 필드별 입력값을 입력 순서대로 반환한다."""

        return {
            self.필드경로(대표필드): 대표필드.값목록
            for 대표필드 in self._유효대표필드목록()
            if 대표필드.값목록
        }

    def 별칭포함필드값목록(self) -> dict[str, tuple[str, ...]]:
        """문서 라벨을 바로 조회할 수 있도록 대표명과 모든 별칭을 펼친다."""

        결과: dict[str, tuple[str, ...]] = {}
        for 대표필드 in self._유효대표필드목록():
            if not 대표필드.값목록:
                continue
            경로 = self.필드경로(대표필드)
            결과[경로] = 대표필드.값목록
            상위 = self.대표필드ID찾기(대표필드.상위필드id)
            for 별칭 in 대표필드.별칭:
                별칭경로 = f"{self.필드경로(상위)} > {별칭}" if 상위 else 별칭
                결과[별칭경로] = 대표필드.값목록
        return 결과

    def 값별필드목록(self) -> dict[str, tuple[str, ...]]:
        """같은 실제 값에 연결된 서로 다른 대표 필드명을 역색인한다."""

        결과: dict[str, list[str]] = {}
        for 필드, 값목록 in self.필드값목록().items():
            for 값 in 값목록:
                필드목록 = 결과.setdefault(값, [])
                if 필드 not in 필드목록:
                    필드목록.append(필드)
        return {값: tuple(필드목록) for 값, 필드목록 in 결과.items()}

    def 기본선택값(self) -> dict[str, str]:
        return {
            self.필드경로(대표필드): 대표필드.기본값
            for 대표필드 in self._유효대표필드목록()
            if 대표필드.기본값
        }

    def 별칭포함기본선택값(self) -> dict[str, str]:
        결과: dict[str, str] = {}
        for 대표필드 in self._유효대표필드목록():
            if not 대표필드.기본값:
                continue
            경로 = self.필드경로(대표필드)
            결과[경로] = 대표필드.기본값
            상위 = self.대표필드ID찾기(대표필드.상위필드id)
            for 별칭 in 대표필드.별칭:
                별칭경로 = f"{self.필드경로(상위)} > {별칭}" if 상위 else 별칭
                결과[별칭경로] = 대표필드.기본값
        return 결과

    def _대표필드로갱신(
        self, 대표필드목록: Sequence[사용자대표필드]
    ) -> "사용자프로필":
        return type(self).생성(
            {"대표필드목록": [대표필드.사전() for 대표필드 in 대표필드목록]}
        )

    def _변경대상찾기(self, 식별자: object) -> 사용자대표필드 | None:
        return self.대표필드찾기(식별자) or self.대표필드ID찾기(식별자)

    def 대표필드추가(
        self,
        대표필드명: object,
        값목록: object = (),
        별칭: object = (),
        기본값: object | None = None,
        필드ID: object | None = None,
        상위필드: object | None = None,
    ) -> "사용자프로필":
        정의: dict[str, object] = {
            "대표필드명": 대표필드명,
            "값목록": 값목록,
            "별칭": 별칭,
        }
        if 기본값 is not None:
            정의["기본값"] = 기본값
        if 필드ID is not None:
            정의["id"] = 필드ID
        if 상위필드 is not None:
            상위 = self.대표필드ID찾기(상위필드) or self.대표필드찾기(상위필드)
            if 상위 is None:
                raise ValueError("하위 필드의 상위 대표필드를 찾을 수 없습니다.")
            정의["상위필드id"] = 상위.id
        새필드 = 사용자대표필드.생성(정의)
        같은범위 = next(
            (
                필드 for 필드 in self._유효대표필드목록()
                if 필드.상위필드id == 새필드.상위필드id
                and 필드.일치(새필드.대표필드명)
            ),
            None,
        )
        if 같은범위 is not None:
            raise ValueError(f"'{새필드.대표필드명}' 이름 또는 별칭은 이미 등록되어 있습니다.")
        if self.대표필드ID찾기(새필드.id) is not None:
            raise ValueError(f"대표 필드 ID '{새필드.id}'가 이미 등록되어 있습니다.")
        return self._대표필드로갱신((*self._유효대표필드목록(), 새필드))

    def 하위필드추가(
        self,
        상위필드: object,
        하위필드명: object,
        값목록: object = (),
        별칭: object = (),
        기본값: object | None = None,
        필드ID: object | None = None,
    ) -> "사용자프로필":
        return self.대표필드추가(
            하위필드명,
            값목록,
            별칭,
            기본값,
            필드ID,
            상위필드,
        )

    def 대표필드상위변경(
        self,
        대표필드: object,
        새상위필드: object | None = None,
    ) -> "사용자프로필":
        """값과 안정 ID를 유지한 채 필드를 대표/하위 계층 사이에서 옮긴다."""

        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            raise ValueError("상위를 변경할 필드를 찾을 수 없습니다.")
        새상위 = None
        if 새상위필드 not in (None, ""):
            새상위 = (
                self.대표필드ID찾기(새상위필드)
                or self.대표필드찾기(새상위필드)
            )
            if 새상위 is None:
                raise ValueError("새 상위 대표필드를 찾을 수 없습니다.")
            if 새상위.id == 대상.id:
                raise ValueError("필드를 자기 자신의 하위필드로 지정할 수 없습니다.")
            현재 = 새상위
            while 현재 is not None:
                if 현재.id == 대상.id:
                    raise ValueError("대표필드를 자기 후손 아래로 옮길 수 없습니다.")
                현재 = (
                    self.대표필드ID찾기(현재.상위필드id)
                    if 현재.상위필드id
                    else None
                )
        새상위ID = 새상위.id if 새상위 is not None else ""
        if 대상.상위필드id == 새상위ID:
            return self
        if (
            not 대상.상위필드id
            and 대상.대표필드명.casefold()
            in {필드.casefold() for 필드 in 기본사용자정보필드}
        ):
            raise ValueError(f"{대상.대표필드명} 기본 대표 필드의 상위는 변경할 수 없습니다.")
        대상이름 = {이름.casefold() for 이름 in (대상.대표필드명, *대상.별칭)}
        충돌필드 = next(
            (
                필드
                for 필드 in self._유효대표필드목록()
                if 필드.id != 대상.id and 필드.상위필드id == 새상위ID
                if 대상이름
                & {이름.casefold() for 이름 in (필드.대표필드명, *필드.별칭)}
            ),
            None,
        )
        if 충돌필드 is not None:
            raise ValueError(
                f"이동 대상 아래에 같은 이름 또는 별칭의 필드 "
                f"'{충돌필드.대표필드명}'이 이미 있습니다. 자동 병합하지 않습니다."
            )
        이동필드 = replace(대상, 상위필드id=새상위ID)
        # _대표필드로갱신이 새 범위의 이름·별칭 충돌과 순환 계층을 함께
        # 검증한다. 값목록·기본값·별칭·ID와 모든 후손은 그대로 유지된다.
        return self._대표필드로갱신(
            tuple(
                이동필드 if 필드.id == 대상.id else 필드
                for 필드 in self._유효대표필드목록()
            )
        )

    def 대표필드삭제(self, 대표필드: object) -> "사용자프로필":
        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            return self
        if not 대상.상위필드id and 대상.대표필드명.casefold() in {
            필드.casefold() for 필드 in 기본사용자정보필드
        }:
            raise ValueError(f"{대상.대표필드명} 기본 대표 필드는 삭제할 수 없습니다.")
        삭제ID = {대상.id}
        while True:
            후손 = {
                필드.id for 필드 in self._유효대표필드목록()
                if 필드.상위필드id in 삭제ID and 필드.id not in 삭제ID
            }
            if not 후손:
                break
            삭제ID.update(후손)
        return self._대표필드로갱신(
            tuple(필드 for 필드 in self._유효대표필드목록() if 필드.id not in 삭제ID)
        )

    def 대표필드병합(
        self, 원본대표필드: object, 대상대표필드: object
    ) -> "사용자프로필":
        """원본의 값·별칭·대표명을 대상에 합치고 대상의 안정 ID를 유지한다."""

        원본 = self._변경대상찾기(원본대표필드)
        대상 = self._변경대상찾기(대상대표필드)
        if 원본 is None:
            raise ValueError("병합할 원본 대표 필드를 찾을 수 없습니다.")
        if 대상 is None:
            raise ValueError("병합 대상 대표 필드를 찾을 수 없습니다.")
        if 원본.id == 대상.id:
            return self
        if 원본.상위필드id != 대상.상위필드id:
            raise ValueError("서로 다른 상위 필드에 속한 하위 필드는 병합할 수 없습니다.")
        if not 원본.상위필드id and 원본.대표필드명.casefold() in {
            필드.casefold() for 필드 in 기본사용자정보필드
        }:
            raise ValueError(f"{원본.대표필드명} 기본 대표 필드는 다른 필드로 병합할 수 없습니다.")

        합친값 = list(대상.값목록)
        for 입력값 in 원본.값목록:
            if 입력값 not in 합친값:
                합친값.append(입력값)
        합친별칭 = list(대상.별칭)
        본별칭 = {항목.casefold() for 항목 in (대상.대표필드명, *합친별칭)}
        for 별칭 in (원본.대표필드명, *원본.별칭):
            if 별칭.casefold() not in 본별칭:
                본별칭.add(별칭.casefold())
                합친별칭.append(별칭)
        새대상 = replace(
            대상,
            값목록=tuple(합친값),
            별칭=tuple(합친별칭),
            기본값=대상.기본값 or 원본.기본값,
        )
        return self._대표필드로갱신(
            tuple(
                새대상 if 필드.id == 대상.id else 필드
                for 필드 in self._유효대표필드목록()
                if 필드.id != 원본.id
            )
        )

    def 별칭추가(self, 대표필드: object, 별칭: object) -> "사용자프로필":
        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            raise ValueError(f"대표 필드 '{_문자열(대표필드, '대표 필드', 200)}'을(를) 찾을 수 없습니다.")
        새별칭 = _문자열(별칭, "별칭", 100)
        if not 새별칭:
            raise ValueError("별칭을 입력하세요.")
        기존소유자 = next(
            (
                필드 for 필드 in self._유효대표필드목록()
                if 필드.상위필드id == 대상.상위필드id and 필드.일치(새별칭)
            ),
            None,
        )
        if 기존소유자 is not None:
            if 기존소유자.id == 대상.id:
                return self
            raise ValueError(
                f"별칭 '{새별칭}'은(는) 대표 필드 '{기존소유자.대표필드명}'에서 사용 중입니다."
            )
        새대상 = replace(대상, 별칭=(*대상.별칭, 새별칭))
        return self._대표필드로갱신(
            tuple(새대상 if 필드.id == 대상.id else 필드 for 필드 in self._유효대표필드목록())
        )

    def 별칭삭제(self, 대표필드: object, 별칭: object) -> "사용자프로필":
        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            return self
        별칭키 = _문자열(별칭, "별칭", 100).casefold()
        새별칭 = tuple(항목 for 항목 in 대상.별칭 if 항목.casefold() != 별칭키)
        if 새별칭 == 대상.별칭:
            return self
        새대상 = replace(대상, 별칭=새별칭)
        return self._대표필드로갱신(
            tuple(새대상 if 필드.id == 대상.id else 필드 for 필드 in self._유효대표필드목록())
        )

    def 대표필드값추가(
        self,
        대표필드: object,
        입력값: object,
        *,
        기본값으로설정: bool = False,
    ) -> "사용자프로필":
        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            raise ValueError(f"대표 필드 '{_문자열(대표필드, '대표 필드', 200)}'을(를) 찾을 수 없습니다.")
        값 = _문자열(입력값, "입력값")
        if not 값:
            raise ValueError("필드 입력값을 입력하세요.")
        새대상 = _대표필드에값추가(대상, 값)
        if 기본값으로설정 and 새대상.기본값 != 값:
            새대상 = replace(새대상, 기본값=값)
        if 새대상 == 대상:
            return self
        return self._대표필드로갱신(
            tuple(새대상 if 필드.id == 대상.id else 필드 for 필드 in self._유효대표필드목록())
        )

    def 대표필드값삭제(self, 대표필드: object, 입력값: object) -> "사용자프로필":
        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            return self
        값 = _문자열(입력값, "입력값")
        값목록 = tuple(항목 for 항목 in 대상.값목록 if 항목 != 값)
        if 값목록 == 대상.값목록:
            return self
        기본값 = 대상.기본값
        if 기본값 == 값:
            기본값 = 값목록[0] if 값목록 else ""
        새대상 = replace(대상, 값목록=값목록, 기본값=기본값)
        return self._대표필드로갱신(
            tuple(새대상 if 필드.id == 대상.id else 필드 for 필드 in self._유효대표필드목록())
        )

    def 기본값지정(self, 대표필드: object, 입력값: object) -> "사용자프로필":
        대상 = self._변경대상찾기(대표필드)
        if 대상 is None:
            raise ValueError(f"대표 필드 '{_문자열(대표필드, '대표 필드', 200)}'을(를) 찾을 수 없습니다.")
        값 = _문자열(입력값, "기본값")
        if 값 and 값 not in 대상.값목록:
            raise ValueError(f"'{값}'은(는) {대상.대표필드명}에 저장된 값이 아닙니다.")
        if 값 == 대상.기본값:
            return self
        새대상 = replace(대상, 기본값=값)
        return self._대표필드로갱신(
            tuple(새대상 if 필드.id == 대상.id else 필드 for 필드 in self._유효대표필드목록())
        )

    def 문서항목추가(self, 필드명: object, 입력값: object) -> "사용자프로필":
        새항목 = 사용자문서항목.생성(필드명, 입력값)
        대표필드 = self.대표필드찾기(새항목.필드명)
        if 대표필드 is not None and not 대표필드.상위필드id and 대표필드.대표필드명.casefold() in {
            필드.casefold() for 필드 in 기본사용자정보필드
        }:
            raise ValueError(f"{새항목.필드명}은(는) 사용자 탭 상단의 기본 정보에서 수정하세요.")
        if 대표필드 is None:
            return self.대표필드추가(새항목.필드명, (새항목.입력값,))
        return self.대표필드값추가(대표필드.id, 새항목.입력값)

    def 문서항목삭제(self, 필드명: object, 입력값: object) -> "사용자프로필":
        대표필드 = self.대표필드찾기(필드명)
        if 대표필드 is None or (not 대표필드.상위필드id and 대표필드.대표필드명.casefold() in {
            필드.casefold() for 필드 in 기본사용자정보필드
        }):
            return self
        return self.대표필드값삭제(대표필드.id, 입력값)
