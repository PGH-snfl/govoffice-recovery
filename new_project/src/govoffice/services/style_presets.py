from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from collections import defaultdict
from collections.abc import Sequence
from typing import Any, Callable, Mapping
from uuid import uuid4

from ..domain.presets import 서식필드, 서식프리셋
from ..ports.hwp import 한글문서포트
from ..ports.presets import 서식프리셋저장포트
from .profile_fill import HWPML개인정보채우기


_XML_DECLARATION = '<?xml version="1.0" encoding="UTF-16"?>'
_TOKEN_PATTERN = re.compile(r"\{\{GOVOFFICE_FIELD_[0-9]{4}\}\}")
_RUN_TOKEN_PATTERN = re.compile(r"\{\{GOVOFFICE_RUN_[0-9]{4}_[0-9]{4}_[0-9]{4}\}\}")
_PHONE_PATTERN = re.compile(r"(?<!\d)(?:01[016789]|0[2-6][0-5]?)[- .]?\d{3,4}[- .]?\d{4}(?!\d)")
_EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
_RESIDENT_PATTERN = re.compile(r"(?<!\d)\d{6}\s*[- ]\s*[1-8]\d{6}(?!\d)")
_DATE_KOREAN_PATTERN = re.compile(
    r"(?<!\d)(?P<year>(?:19|20)\d{2})\s*년\s*(?P<month>\d{1,2})\s*월\s*(?P<day>\d{1,2})\s*일"
)
_DATE_SEPARATOR_PATTERN = re.compile(
    r"(?<!\d)(?P<year>(?:19|20)\d{2})(?P<sep>[./-])(?P<space1>\s*)"
    r"(?P<month>\d{1,2})(?P=sep)(?P<space2>\s*)(?P<day>\d{1,2})(?P<trailing>\.)?(?!\d)"
)
_NAME_WITH_LABEL_PATTERN = re.compile(
    r"(?P<label>(?:성명|이름|담당자|작성자|신청인|대표자)\s*[:：]?\s*)"
    r"(?P<value>[가-힣]{2,4})(?![가-힣])"
)
_ADDRESS_WITH_LABEL_PATTERN = re.compile(
    r"(?P<label>(?:주소|거주지)\s*[:：]\s*)(?P<value>[^\r\n\t]+)"
)
_ACCOUNT_WITH_LABEL_PATTERN = re.compile(
    r"(?P<label>(?:계좌번호|계좌)\s*[:：]?\s*)(?P<value>\d[\d -]{7,}\d)"
)

_NAME_LABELS = {"성명", "이름", "담당자", "작성자", "신청인", "대표자"}
_ADDRESS_LABELS = {"주소", "거주지"}
_ACCOUNT_LABELS = {"계좌", "계좌번호"}
_TITLE_WORDS = ("제목", "계획", "보고", "회의", "결과", "현황", "공고", "안내", "신청서")
_PRIVACY_LABELS = _NAME_LABELS | _ADDRESS_LABELS | _ACCOUNT_LABELS | {
    "전화", "전화번호", "연락처", "휴대전화", "작성일", "날짜", "일자", "주민등록번호", "이메일"
}


def _태그이름(태그: str) -> str:
    return 태그.rsplit("}", 1)[-1].upper()


def _속성(요소: ET.Element | None, 이름: str) -> str | None:
    if 요소 is None:
        return None
    찾을이름 = 이름.casefold()
    for 키, 값 in 요소.attrib.items():
        if 키.rsplit("}", 1)[-1].casefold() == 찾을이름:
            return 값
    return None


def _직렬화(루트: ET.Element) -> str:
    본문 = ET.tostring(루트, encoding="unicode", short_empty_elements=False)
    return f"{_XML_DECLARATION}\n{본문}"


def _라벨정규화(텍스트: str) -> str:
    return re.sub(r"[\s:：()\[\]]+", "", 텍스트).strip()


@dataclass(frozen=True, slots=True)
class HWPML치환결과:
    hwpml: str
    필드목록: tuple[서식필드, ...]


class HWPML등록필드분류기:
    """사용자 탭에 실제로 저장된 값만 선택 영역에서 입력 필드로 바꾼다."""

    def 분류(self, hwpml: str, 등록값: Mapping[str, object]) -> HWPML치환결과:
        값목록: list[tuple[str, str]] = []
        for 필드원본, 값원본 in 등록값.items():
            필드 = str(필드원본).strip()
            if not 필드:
                continue
            원시값목록 = 값원본 if isinstance(값원본, Sequence) and not isinstance(값원본, (str, bytes)) else (값원본,)
            for 원시값 in 원시값목록:
                값 = str(원시값).strip()
                if 값:
                    값목록.append((필드, 값))
        if not 값목록:
            return HWPML치환결과(hwpml, ())
        try:
            루트 = ET.fromstring(hwpml.lstrip("\ufeff"))
        except ET.ParseError as 오류:
            raise ValueError(f"선택 영역 HWPML을 해석할 수 없습니다: {오류}") from 오류

        # 긴 값을 먼저 찾아 짧은 값이 긴 값의 일부를 선점하지 않게 한다.
        값목록.sort(key=lambda 항목: len(항목[1]), reverse=True)
        토큰표: dict[str, str] = {}
        발견필드: list[str] = []

        def 문자열분류(문자열: str | None) -> str | None:
            if not 문자열:
                return 문자열
            결과 = 문자열
            for 필드, 값 in 값목록:
                if 값 not in 결과:
                    continue
                if 필드 not in 토큰표:
                    토큰표[필드] = f"{{{{GOVOFFICE_FIELD_{len(토큰표) + 1:04d}}}}}"
                    발견필드.append(필드)
                결과 = 결과.replace(값, 토큰표[필드])
            return 결과

        for 요소 in 루트.iter():
            요소.text = 문자열분류(요소.text)
            요소.tail = 문자열분류(요소.tail)

        if not 발견필드:
            # 일치하는 등록값이 없으면 바이트 수준에 가까운 원본 보존을 위해 재직렬화하지 않는다.
            return HWPML치환결과(hwpml, ())
        필드목록 = tuple(
            서식필드(
                id=f"profile_{순번:04d}",
                토큰=토큰표[필드],
                안내문구=필드,
                값유형=필드,
            )
            for 순번, 필드 in enumerate(발견필드, 1)
        )
        return HWPML치환결과(_직렬화(루트), 필드목록)

    def 선택후보분류(
        self,
        hwpml: str,
        후보목록: Sequence[object],
    ) -> HWPML치환결과:
        """분석기가 지정한 XML 위치만 대표필드 토큰으로 바꾼다.

        같은 글자값이 책임자와 연구자처럼 서로 다른 대표필드에 쓰이더라도
        전역 문자열 치환을 하지 않으므로 사용자가 체크한 표 셀만 정확히
        분리된다. 한 대표필드의 별칭/여러 위치는 같은 토큰을 공유한다.
        """

        if not 후보목록:
            return HWPML치환결과(hwpml, ())
        try:
            루트 = ET.fromstring(hwpml.lstrip("\ufeff"))
        except ET.ParseError as 오류:
            raise ValueError(f"선택 영역 HWPML을 해석할 수 없습니다: {오류}") from 오류

        def 값읽기(대상: object, 이름: str, 기본값: Any = None) -> Any:
            if isinstance(대상, Mapping):
                return 대상.get(이름, 기본값)
            return getattr(대상, 이름, 기본값)

        def 경로요소(경로: tuple[int, ...]) -> ET.Element:
            요소 = 루트
            try:
                for 자식순번 in 경로:
                    요소 = list(요소)[자식순번]
            except (IndexError, TypeError) as 오류:
                raise ValueError("선택 후보의 HWPML 위치가 원본과 일치하지 않습니다.") from 오류
            return 요소

        토큰표: dict[str, str] = {}
        필드정보: dict[str, tuple[str, str | None]] = {}
        조각그룹표: dict[str, list[tuple[tuple[str, int], ...]]] = defaultdict(list)
        사용중조각표식: set[str] = set()
        본후보위치: set[tuple[str, tuple[tuple[tuple[int, ...], str, int, int], ...]]] = set()
        # (요소 경로, text/tail)별로 원본 offset 기반 편집을 모은다.
        편집표: dict[tuple[tuple[int, ...], str], list[tuple[int, int, str, str]]] = defaultdict(list)

        for 후보 in 후보목록:
            대표필드 = str(
                값읽기(후보, "canonical_field", 값읽기(후보, "field", ""))
            ).strip()
            값 = str(값읽기(후보, "value", "")).strip()
            if not 대표필드 or not 값:
                raise ValueError("선택한 필드 후보의 대표필드명 또는 값이 비어 있습니다.")
            프로필필드id원본 = 값읽기(후보, "profile_field_id")
            프로필필드id = str(프로필필드id원본).strip() if 프로필필드id원본 else None
            if 대표필드 not in 토큰표:
                토큰순번 = len(토큰표) + 1
                토큰 = f"{{{{GOVOFFICE_FIELD_{토큰순번:04d}}}}}"
                while 토큰 in hwpml or 토큰 in 토큰표.values():
                    토큰순번 += 1
                    토큰 = f"{{{{GOVOFFICE_FIELD_{토큰순번:04d}}}}}"
                토큰표[대표필드] = 토큰
                필드정보[대표필드] = (값, 프로필필드id)
            elif 프로필필드id:
                기존값, 기존프로필필드id = 필드정보[대표필드]
                if 기존프로필필드id is None:
                    # 같은 대표필드의 첫 후보가 일반 라벨 분석에서 왔더라도
                    # 뒤의 저장값 후보가 가진 안정 ID를 잃지 않는다.
                    필드정보[대표필드] = (기존값, 프로필필드id)
                elif 기존프로필필드id != 프로필필드id:
                    raise ValueError(f"대표필드 '{대표필드}'의 식별자가 서로 다릅니다.")

            위치 = 값읽기(후보, "locator")
            조각목록 = tuple(값읽기(위치, "segments", ()) or ())
            if not 조각목록:
                raise ValueError(f"'{대표필드}' 후보의 문서 위치 정보가 없습니다.")
            조각텍스트 = "".join(str(값읽기(조각, "text", "")) for 조각 in 조각목록)
            if 조각텍스트 != 값:
                raise ValueError(
                    f"'{대표필드}' 후보의 값과 선택 문서 위치가 일치하지 않습니다. 다시 분석하세요."
                )

            위치키 = tuple(
                (
                    tuple(int(순번) for 순번 in (값읽기(조각, "element_path", ()) or ())),
                    str(값읽기(조각, "text_slot", "")),
                    int(값읽기(조각, "start", -1)),
                    int(값읽기(조각, "end", -1)),
                )
                for 조각 in 조각목록
            )
            후보위치키 = (대표필드.casefold(), 위치키)
            if 후보위치키 in 본후보위치:
                continue
            본후보위치.add(후보위치키)

            위치순번 = len(조각그룹표[대표필드]) + 1
            위치조각: list[tuple[str, int]] = []
            for 조각순번, 조각 in enumerate(조각목록, 1):
                경로 = tuple(int(순번) for 순번 in (값읽기(조각, "element_path", ()) or ()))
                슬롯 = str(값읽기(조각, "text_slot", ""))
                if 슬롯 not in {"text", "tail"}:
                    raise ValueError("선택 후보의 문자열 위치 형식이 올바르지 않습니다.")
                시작 = int(값읽기(조각, "start", -1))
                끝 = int(값읽기(조각, "end", -1))
                예상 = str(값읽기(조각, "text", ""))
                요소 = 경로요소(경로)
                원문 = getattr(요소, 슬롯) or ""
                if 시작 < 0 or 끝 < 시작 or 원문[시작:끝] != 예상:
                    raise ValueError(
                        f"'{대표필드}' 후보 위치의 내용이 바뀌었습니다. 선택 영역을 다시 분석하세요."
                    )
                표식순번 = 위치순번
                조각표식 = (
                    f"{{{{GOVOFFICE_RUN_{list(토큰표).index(대표필드) + 1:04d}_"
                    f"{표식순번:04d}_{조각순번:04d}}}}}"
                )
                while 조각표식 in hwpml or 조각표식 in 사용중조각표식:
                    표식순번 += 1
                    조각표식 = (
                        f"{{{{GOVOFFICE_RUN_{list(토큰표).index(대표필드) + 1:04d}_"
                        f"{표식순번:04d}_{조각순번:04d}}}}}"
                    )
                사용중조각표식.add(조각표식)
                대체 = (토큰표[대표필드] if 조각순번 == 1 else "") + 조각표식
                위치조각.append((대체, len(예상)))
                편집표[(경로, 슬롯)].append((시작, 끝, 대체, 대표필드))
            조각그룹표[대표필드].append(tuple(위치조각))

        for (경로, 슬롯), 편집목록 in 편집표.items():
            # 중복된 동일 편집은 한 번만 적용하되, 겹치는 다른 필드 선택은
            # 잘못된 토큰 소유권을 만들 수 있으므로 조용히 추측하지 않는다.
            고유편집: list[tuple[int, int, str, str]] = []
            for 편집 in sorted(set(편집목록), key=lambda 항목: (항목[0], 항목[1], 항목[3])):
                if 고유편집 and 편집[0] < 고유편집[-1][1]:
                    raise ValueError(
                        "같은 문서 위치가 둘 이상의 필드 후보로 선택되었습니다. 하나만 선택하세요."
                    )
                고유편집.append(편집)
            요소 = 경로요소(경로)
            결과문자열 = getattr(요소, 슬롯) or ""
            for 시작, 끝, 대체, _ in reversed(고유편집):
                결과문자열 = 결과문자열[:시작] + 대체 + 결과문자열[끝:]
            setattr(요소, 슬롯, 결과문자열)

        필드목록 = tuple(
            서식필드(
                id=f"profile_{순번:04d}",
                토큰=토큰표[대표필드],
                안내문구=필드정보[대표필드][0],
                값유형=대표필드,
                프로필필드id=필드정보[대표필드][1],
                조각그룹=tuple(조각그룹표[대표필드]),
            )
            for 순번, 대표필드 in enumerate(토큰표, 1)
        )
        결과 = _직렬화(루트)
        if not all(필드.토큰 in 결과 for 필드 in 필드목록):
            raise RuntimeError("선택한 필드의 대체 토큰 생성에 실패했습니다.")
        return HWPML치환결과(결과, 필드목록)


@dataclass(slots=True)
class _문자런:
    문자요소: ET.Element
    글자모양id: str | None
    문단모양id: str | None
    스타일: dict[str, str | int | float | bool | None]
    원문: str


class HWPML서식치환기:
    """전체 디자인과 일반 문구는 유지하고 민감정보만 안전한 예시로 바꾼다."""

    def __init__(self, 오늘제공: Callable[[], date] | None = None) -> None:
        self._오늘제공 = 오늘제공 or date.today

    def 치환(self, hwpml: str) -> HWPML치환결과:
        if not isinstance(hwpml, str) or not hwpml.strip():
            raise ValueError("선택 영역에서 가져온 HWPML이 비어 있습니다.")
        try:
            루트 = ET.fromstring(hwpml.lstrip("\ufeff"))
        except ET.ParseError as 오류:
            raise ValueError(f"선택 영역 HWPML을 해석할 수 없습니다: {오류}") from 오류

        부모 = {자식: 상위 for 상위 in 루트.iter() for 자식 in 상위}
        글꼴 = self._글꼴목록(루트)
        글자모양 = self._글자모양목록(루트, 글꼴)
        문단모양 = self._문단모양목록(루트)
        self._문서메타데이터제거(루트)

        문자런목록: list[_문자런] = []
        for 문자요소 in (요소 for 요소 in 루트.iter() if _태그이름(요소.tag) == "CHAR"):
            텍스트요소 = self._상위찾기(문자요소, 부모, "TEXT")
            if 텍스트요소 is None:
                continue
            문단요소 = self._상위찾기(텍스트요소, 부모, "P")
            글자모양id = _속성(텍스트요소, "CharShape")
            문단모양id = _속성(문단요소, "ParaShape")
            스타일 = dict(글자모양.get(글자모양id, {}))
            if 문단모양id in 문단모양:
                스타일.update(문단모양[문단모양id])
            문자런목록.append(
                _문자런(
                    문자요소=문자요소,
                    글자모양id=글자모양id,
                    문단모양id=문단모양id,
                    스타일=스타일,
                    원문=self._문자열읽기(문자요소),
                )
            )

        필드목록: list[서식필드] = []
        이전본문 = ""
        비어있지않은순번 = 0
        for 문자런 in 문자런목록:
            제목영역 = self._제목영역인가(문자런.원문, 문자런.스타일, 비어있지않은순번)
            조각이전본문 = 이전본문
            for 소유자, 속성이름 in self._문자열위치목록(문자런.문자요소):
                조각 = getattr(소유자, 속성이름)
                if 조각 is None or not 조각.strip():
                    # 원래 빈칸과 공백은 그대로 둔다.
                    continue
                변환문자열 = 조각 if 제목영역 else self._민감정보치환(
                    조각,
                    조각이전본문,
                    문자런,
                    필드목록,
                )
                setattr(소유자, 속성이름, 변환문자열)
                조각이전본문 = 조각.strip()
            if 문자런.원문.strip():
                이전본문 = 조각이전본문 or 문자런.원문.strip()
                비어있지않은순번 += 1

        결과 = _직렬화(루트)
        if not all(필드.토큰 in 결과 for 필드 in 필드목록):
            raise RuntimeError("민감정보 대체 토큰 생성에 실패했습니다.")
        return HWPML치환결과(결과, tuple(필드목록))

    def 출력용생성(
        self,
        프리셋: 서식프리셋,
        입력값: Mapping[str, str] | None = None,
    ) -> str:
        값 = dict(입력값 or {})
        try:
            루트 = ET.fromstring(프리셋.hwpml.lstrip("\ufeff"))
        except ET.ParseError as 오류:
            raise ValueError(f"저장된 프리셋 HWPML이 손상되었습니다: {오류}") from 오류

        치환표 = {
            필드.토큰: str(값[필드.id]) if 필드.id in 값 else self._기본출력값(필드)
            for 필드 in 프리셋.필드목록
        }
        발견: set[str] = set()

        def 조각표식치환(표식: str, 대체값: str) -> None:
            발견수 = 0
            for 요소 in 루트.iter():
                for 속성이름 in ("text", "tail"):
                    문자열 = getattr(요소, 속성이름)
                    if 문자열 is None or 표식 not in 문자열:
                        continue
                    발견수 += 문자열.count(표식)
                    setattr(요소, 속성이름, 문자열.replace(표식, 대체값))
            if 발견수 != 1:
                raise ValueError("프리셋의 글자 서식 조각 위치가 손상되었습니다.")

        for 필드 in 프리셋.필드목록:
            if not 필드.조각그룹:
                continue
            출력값 = 치환표[필드.토큰]
            for 조각그룹 in 필드.조각그룹:
                남은값 = 출력값
                for 조각순번, (조각표식, 원문길이) in enumerate(조각그룹):
                    if 조각순번 == len(조각그룹) - 1:
                        조각값 = 남은값
                        남은값 = ""
                    else:
                        조각값 = 남은값[:원문길이]
                        남은값 = 남은값[원문길이:]
                    조각표식치환(조각표식, 조각값)
            발견.add(필드.토큰)

        def 문자열치환(문자열: str | None) -> str | None:
            if 문자열 is None:
                return None
            결과문자열 = 문자열
            for 토큰, 대체값 in 치환표.items():
                if any(필드.토큰 == 토큰 and 필드.조각그룹 for 필드 in 프리셋.필드목록):
                    continue
                if 토큰 in 결과문자열:
                    발견.add(토큰)
                    결과문자열 = 결과문자열.replace(토큰, 대체값)
            return 결과문자열

        for 요소 in 루트.iter():
            요소.text = 문자열치환(요소.text)
            요소.tail = 문자열치환(요소.tail)
        누락 = set(치환표) - 발견
        if 누락:
            raise ValueError(f"프리셋 입력 자리 {len(누락)}개를 찾지 못했습니다.")
        결과 = _직렬화(루트)
        if _TOKEN_PATTERN.search(결과) or _RUN_TOKEN_PATTERN.search(결과):
            raise ValueError("출력 문서에 변환되지 않은 입력 자리가 남았습니다.")
        return 결과

    def _민감정보치환(
        self,
        원문: str,
        이전본문: str,
        문자런: _문자런,
        필드목록: list[서식필드],
    ) -> str:
        def 필드생성(값유형: str, 안내문구: str, 출력형식: str | None = None) -> str:
            순번 = len(필드목록) + 1
            필드 = 서식필드(
                id=f"field_{순번:04d}",
                토큰=f"{{{{GOVOFFICE_FIELD_{순번:04d}}}}}",
                안내문구=안내문구,
                글자모양id=문자런.글자모양id,
                문단모양id=문자런.문단모양id,
                스타일=dict(문자런.스타일),
                값유형=값유형,
                출력형식=출력형식,
            )
            필드목록.append(필드)
            return 필드.토큰

        결과 = _NAME_WITH_LABEL_PATTERN.sub(
            lambda 매치: 매치.group("label") + 필드생성("name", "홍길동"), 원문
        )
        결과 = _ADDRESS_WITH_LABEL_PATTERN.sub(
            lambda 매치: 매치.group("label") + 필드생성("address", "서울특별시 중구 세종대로 110"), 결과
        )
        결과 = _ACCOUNT_WITH_LABEL_PATTERN.sub(
            lambda 매치: 매치.group("label") + 필드생성("account", "000-0000-0000-00"), 결과
        )
        결과 = _RESIDENT_PATTERN.sub(lambda _: 필드생성("resident_id", "900101-1234567"), 결과)
        결과 = _EMAIL_PATTERN.sub(lambda _: 필드생성("email", "example@example.com"), 결과)
        결과 = _PHONE_PATTERN.sub(lambda _: 필드생성("phone", "010-1234-1234"), 결과)
        결과 = _DATE_KOREAN_PATTERN.sub(
            lambda _: 필드생성("date", "", "{year:04d}년 {month:d}월 {day:d}일"), 결과
        )

        def 구분날짜치환(매치: re.Match[str]) -> str:
            월형식 = "02d" if len(매치.group("month")) == 2 else "d"
            일형식 = "02d" if len(매치.group("day")) == 2 else "d"
            형식 = (
                "{year:04d}" + 매치.group("sep") + 매치.group("space1")
                + "{month:" + 월형식 + "}" + 매치.group("sep") + 매치.group("space2")
                + "{day:" + 일형식 + "}" + (매치.group("trailing") or "")
            )
            return 필드생성("date", "", 형식)

        결과 = _DATE_SEPARATOR_PATTERN.sub(구분날짜치환, 결과)

        이전라벨 = _라벨정규화(이전본문)
        현재값 = 결과.strip()
        if 이전라벨 in _NAME_LABELS and re.fullmatch(r"[가-힣]{2,4}", 현재값):
            결과 = 결과.replace(현재값, 필드생성("name", "홍길동"), 1)
        elif 이전라벨 in _ADDRESS_LABELS and 현재값 and not _TOKEN_PATTERN.search(현재값):
            결과 = 결과.replace(현재값, 필드생성("address", "서울특별시 중구 세종대로 110"), 1)
        elif 이전라벨 in _ACCOUNT_LABELS and 현재값 and not _TOKEN_PATTERN.search(현재값):
            결과 = 결과.replace(현재값, 필드생성("account", "000-0000-0000-00"), 1)
        return 결과

    def _기본출력값(self, 필드: 서식필드) -> str:
        if 필드.값유형 == "date":
            오늘 = self._오늘제공()
            형식 = 필드.출력형식 or "{year:04d}. {month:d}. {day:d}."
            return 형식.format(year=오늘.year, month=오늘.month, day=오늘.day)
        return 필드.안내문구

    @staticmethod
    def _제목영역인가(원문: str, 스타일: Mapping[str, object], 순번: int) -> bool:
        정리 = 원문.strip()
        if not 정리:
            return False
        라벨정리 = _라벨정규화(정리)
        if any(라벨정리.startswith(라벨) for 라벨 in _PRIVACY_LABELS):
            return False
        크기값 = 스타일.get("font_size_pt")
        크기 = float(크기값) if isinstance(크기값, (int, float)) else 0.0
        정렬 = str(스타일.get("paragraph_align") or "").casefold()
        큰가운데제목 = 크기 >= 14 and ("center" in 정렬 or "가운데" in 정렬 or 순번 < 2)
        제목문구 = 순번 < 4 and 크기 >= 11 and any(단어 in 정리 for 단어 in _TITLE_WORDS)
        return 큰가운데제목 or 제목문구

    @staticmethod
    def _문자열읽기(문자요소: ET.Element) -> str:
        return (문자요소.text or "") + "".join(하위.tail or "" for 하위 in 문자요소)

    @staticmethod
    def _문자열위치목록(문자요소: ET.Element) -> list[tuple[ET.Element, str]]:
        return [(문자요소, "text"), *((하위, "tail") for 하위 in 문자요소)]

    @staticmethod
    def _상위찾기(
        요소: ET.Element,
        부모: dict[ET.Element, ET.Element],
        태그: str,
    ) -> ET.Element | None:
        현재 = 부모.get(요소)
        while 현재 is not None:
            if _태그이름(현재.tag) == 태그:
                return 현재
            현재 = 부모.get(현재)
        return None

    @staticmethod
    def _문서메타데이터제거(루트: ET.Element) -> None:
        for 요소 in 루트.iter():
            if _태그이름(요소.tag) != "DOCSUMMARY":
                continue
            for 하위 in 요소.iter():
                하위.text = None
                하위.tail = None

    @staticmethod
    def _글꼴목록(루트: ET.Element) -> dict[str, str]:
        결과: dict[str, str] = {}
        for 묶음 in (요소 for 요소 in 루트.iter() if _태그이름(요소.tag) == "FONTFACE"):
            언어 = (_속성(묶음, "Lang") or "").upper()
            if 언어 not in {"HANGUL", "KOREAN", ""}:
                continue
            for 요소 in 묶음:
                if _태그이름(요소.tag) != "FONT":
                    continue
                id값 = _속성(요소, "Id")
                이름 = _속성(요소, "Name")
                if id값 is not None and 이름:
                    결과[id값] = 이름
        return 결과

    @staticmethod
    def _글자모양목록(
        루트: ET.Element, 글꼴: Mapping[str, str]
    ) -> dict[str | None, dict[str, str | int | float | bool | None]]:
        결과: dict[str | None, dict[str, str | int | float | bool | None]] = {}
        for 요소 in (항목 for 항목 in 루트.iter() if _태그이름(항목.tag) == "CHARSHAPE"):
            id값 = _속성(요소, "Id")
            높이원본 = _속성(요소, "Height")
            폰트id = None
            for 하위 in 요소:
                if _태그이름(하위.tag) == "FONTID":
                    폰트id = _속성(하위, "Hangul") or _속성(하위, "Korean")
                    break
            높이 = None
            if 높이원본 is not None:
                try:
                    높이 = float(높이원본) / 100.0
                except ValueError:
                    높이 = None
            결과[id값] = {
                "font_family": 글꼴.get(폰트id or ""),
                "font_size_pt": 높이,
                "bold": any(_태그이름(하위.tag) == "BOLD" for 하위 in 요소),
                "italic": any(_태그이름(하위.tag) == "ITALIC" for 하위 in 요소),
                "text_color": _속성(요소, "TextColor"),
                "shade_color": _속성(요소, "ShadeColor"),
            }
        return 결과

    @staticmethod
    def _문단모양목록(루트: ET.Element) -> dict[str | None, dict[str, str | int | float | bool | None]]:
        결과: dict[str | None, dict[str, str | int | float | bool | None]] = {}
        for 요소 in (항목 for 항목 in 루트.iter() if _태그이름(항목.tag) == "PARASHAPE"):
            id값 = _속성(요소, "Id")
            정렬 = _속성(요소, "Align") or _속성(요소, "AlignType")
            결과[id값] = {"paragraph_align": 정렬}
        return 결과


class 서식프리셋서비스:
    def __init__(
        self,
        한글: 한글문서포트,
        저장소: 서식프리셋저장포트,
        치환기: HWPML서식치환기 | None = None,
        개인정보제공: Callable[[], Mapping[str, str]] | None = None,
        개인정보채우기: HWPML개인정보채우기 | None = None,
        등록필드분류기: HWPML등록필드분류기 | None = None,
        등록필드제공: Callable[[], Mapping[str, object]] | None = None,
    ) -> None:
        self._한글 = 한글
        self._저장소 = 저장소
        self._치환기 = 치환기 or HWPML서식치환기()
        self._개인정보제공 = 개인정보제공 or (lambda: {})
        self._개인정보채우기 = 개인정보채우기 or HWPML개인정보채우기()
        self._등록필드분류기 = 등록필드분류기 or HWPML등록필드분류기()
        self._등록필드제공 = 등록필드제공 or self._개인정보제공

    def 선택영역저장(
        self,
        이름: str,
        원본hwpml: str | None = None,
        등록값: Mapping[str, object] | None = None,
    ) -> 서식프리셋:
        정리된이름 = str(이름).strip()
        if not 정리된이름:
            raise ValueError("프리셋 이름을 입력하세요.")
        원본hwpml = 원본hwpml if 원본hwpml is not None else self._한글.선택영역서식내보내기()
        분류결과 = self._등록필드분류기.분류(
            원본hwpml,
            등록값 if 등록값 is not None else self._등록필드제공(),
        )
        필드있음 = bool(분류결과.필드목록)
        프리셋 = 서식프리셋(
            id=f"style_{uuid4().hex}",
            이름=정리된이름,
            hwpml=분류결과.hwpml,
            필드목록=분류결과.필드목록,
            범위="selection_page",
            내용정책="registered_fields" if 필드있음 else "original",
        )
        self._저장소.저장(프리셋)
        return 프리셋

    def 선택후보저장(
        self,
        이름: str,
        원본hwpml: str,
        후보목록: Sequence[object],
        셀서식규칙: Mapping[str, object] | None = None,
    ) -> 서식프리셋:
        """검토 화면에서 체크한 후보 위치만 입력 필드로 저장한다."""

        정리된이름 = str(이름).strip()
        if not 정리된이름:
            raise ValueError("프리셋 이름을 입력하세요.")
        분류결과 = self._등록필드분류기.선택후보분류(원본hwpml, 후보목록)
        필드있음 = bool(분류결과.필드목록)
        프리셋 = 서식프리셋(
            id=f"style_{uuid4().hex}",
            이름=정리된이름,
            hwpml=분류결과.hwpml,
            필드목록=분류결과.필드목록,
            범위="selection_page",
            내용정책="registered_fields" if 필드있음 else "original",
            셀서식규칙={
                역할: tuple(dict.fromkeys(str(서명) for 서명 in 원시목록))
                for 역할, 원시목록 in (셀서식규칙 or {}).items()
                if 역할 in {"field", "value"}
                and isinstance(원시목록, Sequence)
                and not isinstance(원시목록, (str, bytes))
            },
        )
        self._저장소.저장(프리셋)
        return 프리셋

    def 출력(self, 프리셋id: str, 입력값: Mapping[str, str] | None = None):
        프리셋 = self._저장소.불러오기(프리셋id)
        if 프리셋.내용정책 == "original":
            출력hwpml = 프리셋.hwpml
        elif 프리셋.내용정책 == "registered_fields":
            프로필값 = {str(키): str(값) for 키, 값 in self._개인정보제공().items() if str(값)}
            출력값: dict[str, str] = {}
            for 필드 in 프리셋.필드목록:
                # 새 프리셋은 안정 ID를 우선하고, 구형 프리셋은 대표명/별칭
                # 조회를 그대로 지원한다.
                조회키 = next(
                    (
                        키
                        for 키 in (필드.프로필필드id, 필드.값유형)
                        if 키 and 키 in 프로필값
                    ),
                    None,
                )
                if 조회키 is not None:
                    출력값[필드.id] = 프로필값[조회키]
            출력값.update({str(키): str(값) for 키, 값 in (입력값 or {}).items()})
            누락 = [필드.값유형 for 필드 in 프리셋.필드목록 if 필드.id not in 출력값]
            if 누락:
                raise ValueError("현재 사용자 탭에 필요한 필드 값이 없습니다: " + ", ".join(누락))
            출력hwpml = self._치환기.출력용생성(프리셋, 출력값)
        else:
            출력hwpml = self._치환기.출력용생성(프리셋, 입력값)
        if 프리셋.범위 in {"selection_page", "document"}:
            return self._한글.선택영역새문서생성(출력hwpml)
        return self._한글.서식조각삽입(출력hwpml)

    def 목록(self) -> tuple[서식프리셋, ...]:
        return self._저장소.목록()

    def 삭제(self, 프리셋id: str) -> bool:
        return self._저장소.삭제(프리셋id)
