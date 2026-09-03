from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Mapping


_라벨필드 = {
    "성명": "이름",
    "이름": "이름",
    "신청인": "이름",
    "작성자": "이름",
    "담당자": "이름",
    "전화": "전화번호",
    "전화번호": "전화번호",
    "연락처": "전화번호",
    "휴대전화": "전화번호",
    "휴대폰": "전화번호",
    "이메일": "이메일",
    "전자우편": "이메일",
    "소속": "소속",
    "기관명": "소속",
    "부서": "부서",
    "부서명": "부서",
    "직위": "직위",
    "직급": "직위",
}
_라벨대안 = "|".join(re.escape(라벨) for 라벨 in sorted(_라벨필드, key=len, reverse=True))
_인라인패턴 = re.compile(
    rf"(?P<label>{_라벨대안})(?P<separator>\s*[:：]\s*|\s+)(?P<value>[^\r\n\t]+)"
)


def _태그이름(태그: str) -> str:
    return 태그.rsplit("}", 1)[-1].upper()


def _라벨정규화(텍스트: str) -> str:
    return re.sub(r"[\s:：()\[\]]+", "", 텍스트).strip()


class HWPML개인정보채우기:
    """저장 원본은 건드리지 않고 출력 HWPML의 라벨 옆 텍스트만 채운다."""

    def 채우기(self, hwpml: str, 개인정보: Mapping[str, str]) -> str:
        값 = {키: str(내용) for 키, 내용 in 개인정보.items() if str(내용)}
        if not 값:
            return hwpml
        try:
            루트 = ET.fromstring(hwpml.lstrip("\ufeff"))
        except ET.ParseError as 오류:
            raise ValueError(f"저장된 프리셋 HWPML이 손상되었습니다: {오류}") from 오류

        대기필드: str | None = None
        치환수 = 0
        for 문자요소 in (요소 for 요소 in 루트.iter() if _태그이름(요소.tag) == "CHAR"):
            위치목록 = [(문자요소, "text"), *((하위, "tail") for 하위 in 문자요소)]
            원문 = (문자요소.text or "") + "".join(하위.tail or "" for 하위 in 문자요소)
            정규라벨 = _라벨정규화(원문)
            현재필드 = _라벨필드.get(정규라벨)
            if 현재필드:
                대기필드 = 현재필드 if 값.get(현재필드) else None
                continue

            인라인치환됨 = False
            for 소유자, 속성이름 in 위치목록:
                조각 = getattr(소유자, 속성이름)
                if not 조각:
                    continue

                def 바꾸기(매치: re.Match[str]) -> str:
                    nonlocal 치환수, 인라인치환됨
                    필드 = _라벨필드[매치.group("label")]
                    대체값 = 값.get(필드)
                    if not 대체값:
                        return 매치.group(0)
                    치환수 += 1
                    인라인치환됨 = True
                    return 매치.group("label") + 매치.group("separator") + 대체값

                setattr(소유자, 속성이름, _인라인패턴.sub(바꾸기, 조각))
            if 인라인치환됨:
                대기필드 = None
                continue

            if 대기필드 and 값.get(대기필드):
                대체값 = 값[대기필드]
                비어있지않은위치 = next(
                    ((소유자, 속성이름, 문자열) for 소유자, 속성이름 in 위치목록 if (문자열 := getattr(소유자, 속성이름)) and 문자열.strip()),
                    None,
                )
                if 비어있지않은위치:
                    소유자, 속성이름, 문자열 = 비어있지않은위치
                    앞공백 = 문자열[: len(문자열) - len(문자열.lstrip())]
                    뒤공백 = 문자열[len(문자열.rstrip()) :]
                    setattr(소유자, 속성이름, 앞공백 + 대체값 + 뒤공백)
                    for 다른소유자, 다른속성 in 위치목록:
                        if (다른소유자, 다른속성) != (소유자, 속성이름):
                            다른문자열 = getattr(다른소유자, 다른속성)
                            if 다른문자열 and 다른문자열.strip():
                                setattr(다른소유자, 다른속성, "")
                else:
                    문자요소.text = 대체값
                치환수 += 1
                대기필드 = None

        if 치환수 == 0:
            return hwpml
        본문 = ET.tostring(루트, encoding="unicode", short_empty_elements=False)
        return '<?xml version="1.0" encoding="UTF-16"?>\n' + 본문
