import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

from govoffice.adapters.json_style_presets import JSON서식프리셋저장소
from govoffice.domain.presets import 서식프리셋
from govoffice.services.hwpml_table_analysis import HWPMLTableFieldAnalyzer
from govoffice.services.style_presets import (
    HWPML등록필드분류기,
    HWPML서식치환기,
    서식프리셋서비스,
)


샘플_HWPML = """<?xml version="1.0" encoding="UTF-8"?>
<HWPML>
  <HEAD>
    <DOCSUMMARY><TITLE>민감한 내부 제목</TITLE><AUTHOR>김철수</AUTHOR></DOCSUMMARY>
    <MAPPINGTABLE>
      <FONTFACELIST><FONTFACE Lang="HANGUL"><FONT Id="0" Name="굴림" /></FONTFACE></FONTFACELIST>
      <CHARSHAPELIST>
        <CHARSHAPE Id="0" Height="1100" TextColor="0"><FONTID Hangul="0" /></CHARSHAPE>
        <CHARSHAPE Id="1" Height="900" TextColor="255"><FONTID Hangul="0" /><BOLD /></CHARSHAPE>
        <CHARSHAPE Id="2" Height="1600" TextColor="0"><FONTID Hangul="0" /><BOLD /></CHARSHAPE>
      </CHARSHAPELIST>
      <PARASHAPELIST>
        <PARASHAPE Id="0" Align="Center" />
        <PARASHAPE Id="1" Align="Left" />
      </PARASHAPELIST>
    </MAPPINGTABLE>
  </HEAD>
  <BODY>
    <SECTION>
      <SECDEF TextDirection="0"><PAGEDEF Landscape="1" PaperWidth="84188" PaperHeight="59528" LeftMargin="7777" RightMargin="4444" TopMargin="5555" BottomMargin="3333" HeaderLen="2222" FooterLen="1111" /></SECDEF>
      <P ParaShape="0"><TEXT CharShape="2"><CHAR>2025. 1. 2. 서울과학기술대학교 업무계획</CHAR></TEXT></P>
      <TABLE BorderFill="3"><ROW>
        <CELL Width="1000" ShadeColor="123"><P ParaShape="1"><TEXT CharShape="0"><CHAR>성명</CHAR></TEXT></P></CELL>
        <CELL Width="2000"><P ParaShape="1"><TEXT CharShape="1"><CHAR>김철수</CHAR></TEXT></P></CELL>
      </ROW><ROW>
        <CELL><P ParaShape="1"><TEXT CharShape="0"><CHAR>전화번호</CHAR></TEXT></P></CELL>
        <CELL><P ParaShape="1"><TEXT CharShape="1"><CHAR>010-9999-8888</CHAR></TEXT></P></CELL>
      </ROW><ROW>
        <CELL><P ParaShape="1"><TEXT CharShape="0"><CHAR>작성일</CHAR></TEXT></P></CELL>
        <CELL><P ParaShape="1"><TEXT CharShape="1"><CHAR>2024. 1. 2.</CHAR></TEXT></P></CELL>
      </ROW><ROW>
        <CELL><P ParaShape="1"><TEXT CharShape="0"><CHAR>안내</CHAR></TEXT></P></CELL>
        <CELL><P ParaShape="1"><TEXT CharShape="0"><CHAR>제출서류를 확인하세요.</CHAR></TEXT></P></CELL>
      </ROW><ROW>
        <CELL><P ParaShape="1"><TEXT CharShape="0"><CHAR></CHAR></TEXT></P></CELL>
        <CELL><P ParaShape="1"><TEXT CharShape="0"><CHAR>이메일: real.person@example.org</CHAR></TEXT></P></CELL>
      </ROW></TABLE>
    </SECTION>
  </BODY>
</HWPML>"""


def 본문텍스트(hwpml: str) -> str:
    루트 = ET.fromstring(hwpml.lstrip("\ufeff"))
    return "".join(루트.itertext())


class 가짜한글:
    def __init__(self, 내보낼내용: str = 샘플_HWPML) -> None:
        self.내보낼내용 = 내보낼내용
        self.삽입내용 = None
        self.선택새문서내용 = None

    def 선택영역서식내보내기(self) -> str:
        return self.내보낼내용

    def 서식조각삽입(self, hwpml: str):
        self.삽입내용 = hwpml
        return True

    def 선택영역새문서생성(self, hwpml: str):
        self.선택새문서내용 = hwpml
        return True


class HWPML서식치환기시험(unittest.TestCase):
    def setUp(self) -> None:
        self.치환기 = HWPML서식치환기(오늘제공=lambda: date(2026, 8, 31))
        self.결과 = self.치환기.치환(샘플_HWPML)

    def test_제목과_일반문구는_유지하고_민감정보만_토큰화한다(self):
        저장본문 = 본문텍스트(self.결과.hwpml)
        self.assertIn("2025. 1. 2. 서울과학기술대학교 업무계획", 저장본문)
        self.assertIn("제출서류를 확인하세요.", 저장본문)
        self.assertNotIn("김철수", 저장본문)
        self.assertNotIn("010-9999-8888", 저장본문)
        self.assertNotIn("2024. 1. 2.", 저장본문)
        self.assertNotIn("real.person@example.org", 저장본문)
        self.assertEqual(["name", "phone", "date", "email"], [필드.값유형 for 필드 in self.결과.필드목록])

    def test_출력할_때_예시값과_당일날짜를_넣는다(self):
        프리셋 = 서식프리셋("style_test", "시험", self.결과.hwpml, self.결과.필드목록)
        출력본문 = 본문텍스트(self.치환기.출력용생성(프리셋))
        self.assertIn("홍길동", 출력본문)
        self.assertIn("010-1234-1234", 출력본문)
        self.assertIn("2026. 8. 31.", 출력본문)
        self.assertIn("example@example.com", 출력본문)
        self.assertNotIn("GOVOFFICE_FIELD", 출력본문)

    def test_원래_빈칸은_빈칸으로_두고_필드를_만들지_않는다(self):
        루트 = ET.fromstring(self.결과.hwpml.lstrip("\ufeff"))
        빈문자 = [요소 for 요소 in 루트.iter() if 요소.tag.rsplit("}", 1)[-1].upper() == "CHAR" and not "".join(요소.itertext())]
        self.assertEqual(1, len(빈문자))
        self.assertEqual(4, len(self.결과.필드목록))

    def test_표와_셀과_민감값_위치의_글자서식을_보존한다(self):
        self.assertIn('BorderFill="3"', self.결과.hwpml)
        self.assertIn('ShadeColor="123"', self.결과.hwpml)
        self.assertEqual("1", self.결과.필드목록[0].글자모양id)
        self.assertEqual(9.0, self.결과.필드목록[0].스타일["font_size_pt"])
        self.assertTrue(self.결과.필드목록[0].스타일["bold"])

    def test_사용자가_지정한_값은_예시값보다_우선한다(self):
        프리셋 = 서식프리셋("style_test", "시험", self.결과.hwpml, self.결과.필드목록)
        입력값 = {필드.id: f"사용자값-{순번}" for 순번, 필드 in enumerate(프리셋.필드목록, 1)}
        출력본문 = 본문텍스트(self.치환기.출력용생성(프리셋, 입력값))
        for 값 in 입력값.values():
            self.assertIn(값, 출력본문)
        self.assertNotIn("홍길동", 출력본문)

    def test_민감정보가_없는_서식도_그대로_저장한다(self):
        단순 = "<HWPML><BODY><P><TEXT><CHAR>일반 안내문</CHAR><CHAR></CHAR></TEXT></P></BODY></HWPML>"
        결과 = self.치환기.치환(단순)
        self.assertEqual((), 결과.필드목록)
        self.assertIn("일반 안내문", 결과.hwpml)


class HWPML선택후보분류시험(unittest.TestCase):
    HWPML = (
        "<HWPML><BODY><TABLE>"
        "<ROW><CELL><CHAR>책임자</CHAR></CELL><CELL><CHAR>홍길동</CHAR></CELL></ROW>"
        "<ROW><CELL><CHAR>연구자</CHAR></CELL><CELL><CHAR>홍길동</CHAR></CELL></ROW>"
        "<ROW><CELL><CHAR>성함</CHAR></CELL><CELL><CHAR>홍길동</CHAR></CELL></ROW>"
        "</TABLE></BODY></HWPML>"
    )

    @staticmethod
    def 후보(candidate_id: str, 필드: str, 행: int, 프로필id: str | None):
        return {
            "candidate_id": candidate_id,
            "field": 필드,
            "canonical_field": 필드,
            "profile_field_id": 프로필id,
            "value": "홍길동",
            "locator": {
                "segments": [
                    {
                        "element_path": [0, 0, 행, 1, 0],
                        "text_slot": "text",
                        "start": 0,
                        "end": 3,
                        "text": "홍길동",
                    }
                ]
            },
        }

    def test_같은값이어도_선택위치에_따라_서로_다른_대표필드로_분류한다(self):
        결과 = HWPML등록필드분류기().선택후보분류(
            self.HWPML,
            [
                self.후보("c1", "책임자", 0, "profile_field_owner"),
                self.후보("c2", "연구자", 1, "profile_field_researcher"),
            ],
        )
        본문 = 본문텍스트(결과.hwpml)
        self.assertEqual(2, len(결과.필드목록))
        self.assertEqual(["책임자", "연구자"], [필드.값유형 for 필드 in 결과.필드목록])
        self.assertEqual(2, 본문.count("GOVOFFICE_FIELD"))
        self.assertEqual(1, 본문.count("홍길동"))
        self.assertEqual(
            ["profile_field_owner", "profile_field_researcher"],
            [필드.프로필필드id for 필드 in 결과.필드목록],
        )

    def test_같은_대표필드의_별칭위치는_하나의_출력선택을_공유한다(self):
        결과 = HWPML등록필드분류기().선택후보분류(
            self.HWPML,
            [
                self.후보("c1", "이름", 0, "profile_field_name"),
                self.후보("c3", "이름", 2, "profile_field_name"),
            ],
        )
        self.assertEqual(1, len(결과.필드목록))
        self.assertEqual(2, 결과.hwpml.count(결과.필드목록[0].토큰))
        프리셋 = 서식프리셋("style_alias", "별칭", 결과.hwpml, 결과.필드목록)
        출력 = HWPML서식치환기().출력용생성(
            프리셋, {결과.필드목록[0].id: "김새봄"}
        )
        self.assertEqual(2, 본문텍스트(출력).count("김새봄"))
        self.assertEqual(1, 본문텍스트(출력).count("홍길동"))

    def test_뒤_후보의_안정ID도_같은_대표필드에_보강한다(self):
        첫후보 = self.후보("c1", "이름", 0, None)
        저장값후보 = self.후보("c3", "이름", 2, "profile_field_name")

        결과 = HWPML등록필드분류기().선택후보분류(
            self.HWPML,
            [첫후보, 저장값후보],
        )

        self.assertEqual("profile_field_name", 결과.필드목록[0].프로필필드id)

    def test_체크하지_않은_후보위치는_원문으로_남긴다(self):
        결과 = HWPML등록필드분류기().선택후보분류(
            self.HWPML,
            [self.후보("c2", "연구자", 1, "profile_field_researcher")],
        )
        self.assertEqual(2, 본문텍스트(결과.hwpml).count("홍길동"))
        self.assertEqual(1, 결과.hwpml.count("GOVOFFICE_FIELD"))

    def test_분석기와_같은_locator를_써서_여러_XML조각의_값도_정확히_치환한다(self):
        원본 = (
            "<HWPML><BODY><SECTION><P><TEXT><CHAR>기본 사용자 정보</CHAR></TEXT></P>"
            "<TABLE><ROW><CELL><P><TEXT CharShape='1'><CHAR>성명: 홍<MARK/>길</CHAR></TEXT>"
            "<TEXT CharShape='2'><CHAR>동</CHAR></TEXT></P></CELL></ROW></TABLE>"
            "</SECTION></BODY></HWPML>"
        )
        후보 = HWPMLTableFieldAnalyzer().analyze(
            원본,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        ).registered_candidates[0]
        결과 = HWPML등록필드분류기().선택후보분류(원본, [후보])

        self.assertEqual("이름", 결과.필드목록[0].값유형)
        self.assertIn("성명: ", 본문텍스트(결과.hwpml))
        self.assertNotIn("홍길동", 본문텍스트(결과.hwpml))
        self.assertEqual(1, 결과.hwpml.count(결과.필드목록[0].토큰))

        프리셋 = 서식프리셋("style_runs", "글자 런", 결과.hwpml, 결과.필드목록)
        출력 = HWPML서식치환기().출력용생성(
            프리셋, {결과.필드목록[0].id: "김철수"}
        )
        루트 = ET.fromstring(출력.lstrip("\ufeff"))
        실제런 = [
            (TEXT.attrib.get("CharShape"), "".join(TEXT.itertext()))
            for TEXT in 루트.iter()
            if TEXT.tag.rsplit("}", 1)[-1].upper() == "TEXT"
            and TEXT.attrib.get("CharShape") in {"1", "2"}
        ]
        self.assertEqual([("1", "성명: 김철"), ("2", "수")], 실제런)
        self.assertNotIn("GOVOFFICE_RUN", 출력)

    def test_한_XML문자열의_두_후보도_offset을_보존해_각_대표필드로_치환한다(self):
        원본 = (
            "<HWPML><BODY><SECTION><TABLE><ROW><CELL><P><TEXT>"
            "<CHAR>책임자: 홍길동\n연구자: 홍길동</CHAR>"
            "</TEXT></P></CELL></ROW></TABLE></SECTION></BODY></HWPML>"
        )
        후보 = HWPMLTableFieldAnalyzer().analyze(
            원본,
            registered_fields=("책임자", "연구자"),
        ).registered_candidates
        결과 = HWPML등록필드분류기().선택후보분류(원본, 후보)

        self.assertEqual(["책임자", "연구자"], [필드.값유형 for 필드 in 결과.필드목록])
        self.assertEqual(2, 결과.hwpml.count("GOVOFFICE_FIELD"))
        self.assertNotIn("홍길동", 본문텍스트(결과.hwpml))


class 서식프리셋저장과서비스시험(unittest.TestCase):
    def test_셀서식_역할규칙을_프리셋_메타데이터로_왕복한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            저장소 = JSON서식프리셋저장소(Path(임시))
            원본 = 서식프리셋(
                id="style_cellstylerules",
                이름="셀 서식",
                hwpml="<HWPML/>",
                셀서식규칙={"field": ("field-signature",), "value": ("value-signature",)},
            )
            저장소.저장(원본)

            결과 = 저장소.불러오기(원본.id)
            self.assertEqual(("field-signature",), 결과.셀서식규칙["field"])
            self.assertEqual(("value-signature",), 결과.셀서식규칙["value"])

    def test_선택영역의_원본내용과_쪽서식을_그대로_저장하고_출력한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            한글 = 가짜한글()
            저장소 = JSON서식프리셋저장소(Path(임시))
            치환기 = HWPML서식치환기(오늘제공=lambda: date(2026, 8, 31))
            서비스 = 서식프리셋서비스(한글, 저장소, 치환기)

            저장됨 = 서비스.선택영역저장("개인정보 안전 서식")
            불러옴 = 저장소.불러오기(저장됨.id)
            self.assertEqual("selection_page", 불러옴.범위)
            self.assertEqual("original", 불러옴.내용정책)
            self.assertEqual((), 불러옴.필드목록)
            메타 = json.loads((Path(임시) / f"{저장됨.id}.json").read_text(encoding="utf-8"))
            self.assertEqual(4, 메타["schema_version"])
            self.assertEqual("selection_page", 메타["scope"])
            self.assertEqual("original", 메타["content_policy"])
            self.assertEqual([], 메타["fields"])
            저장hwpml = (Path(임시) / f"{저장됨.id}.hml").read_text(encoding="utf-8")
            self.assertEqual(샘플_HWPML, 저장hwpml)
            self.assertIn("김철수", 저장hwpml)
            self.assertIn("010-9999-8888", 저장hwpml)
            self.assertIn("2024. 1. 2.", 저장hwpml)
            self.assertIn('Landscape="1"', 저장hwpml)
            self.assertIn('PaperWidth="84188"', 저장hwpml)
            self.assertIn('LeftMargin="7777"', 저장hwpml)

            self.assertTrue(서비스.출력(저장됨.id))
            self.assertIsNone(한글.삽입내용)
            self.assertEqual(샘플_HWPML, 한글.선택새문서내용)
            출력본문 = 본문텍스트(한글.선택새문서내용)
            self.assertIn("김철수", 출력본문)
            self.assertIn("010-9999-8888", 출력본문)
            self.assertIn("2024. 1. 2.", 출력본문)
            self.assertNotIn("홍길동", 출력본문)
            self.assertIn('HeaderLen="2222"', 한글.선택새문서내용)

    def test_기존_선택영역_프리셋은_커서에_삽입한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            한글 = 가짜한글()
            저장소 = JSON서식프리셋저장소(Path(임시))
            치환기 = HWPML서식치환기()
            서비스 = 서식프리셋서비스(한글, 저장소, 치환기)
            치환결과 = 치환기.치환(샘플_HWPML)
            프리셋 = 서식프리셋(
                "style_legacy",
                "기존 방식",
                치환결과.hwpml,
                치환결과.필드목록,
                범위="selection",
            )
            저장소.저장(프리셋)
            self.assertTrue(서비스.출력("style_legacy"))
            self.assertIsNotNone(한글.삽입내용)
            self.assertIsNone(한글.선택새문서내용)


if __name__ == "__main__":
    unittest.main()
