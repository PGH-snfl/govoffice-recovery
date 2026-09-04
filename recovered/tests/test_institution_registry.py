import unittest
from pathlib import Path

from institution_system import 기관기능실행, 기관등록부, 기관탭목록


class 기관등록부시험(unittest.TestCase):
    def setUp(self):
        복구루트 = Path(__file__).resolve().parents[1]
        self.등록부 = 기관등록부(복구루트 / "institutions")

    def test_서울과학기술대학교가_등록되어_있다(self):
        기관 = self.등록부.기관찾기("seoultech")
        self.assertEqual(기관.name, "서울과학기술대학교")
        self.assertEqual(기관.type, "university")
        self.assertEqual(기관.version, "0.1.0")

    def test_전용기능은_아직_등록되지_않았다(self):
        기관 = self.등록부.기관찾기("seoultech")
        self.assertEqual(기관.functions, ())

    def test_원본_지자체와_추가기관이_탭_모델로_변환된다(self):
        탭 = 기관탭목록(self.등록부)
        self.assertEqual(len(탭), 24)
        서울 = next(항목 for 항목 in 탭 if 항목.id == "seoul")
        self.assertEqual(서울.name, "서울")
        self.assertTrue(any(기능.legacy_method == "서울보고서" for 기능 in 서울.functions))

    def test_기관_호환_실행기는_한컴_facade를_호출한다(self):
        from institutions.seoul.functions.legacy import 실행

        class 가짜한컴:
            def 서울보고서(self, 값):
                return f"실행:{값}"

        self.assertEqual(실행(가짜한컴(), "서울보고서", "시험"), "실행:시험")

    def test_manifest_기능을_로더로_실행한다(self):
        서울 = next(항목 for 항목 in 기관탭목록(self.등록부) if 항목.id == "seoul")
        기능 = next(항목 for 항목 in 서울.functions if 항목.legacy_method == "서울작성자")

        class 가짜한컴:
            def 서울작성자(self):
                return "작성자 서식 적용"

        self.assertTrue(기능.ui_ready)
        self.assertEqual(기관기능실행("seoul", 기능, 가짜한컴()), "작성자 서식 적용")

    def test_입력이_필요한_기능은_자동버튼_실행을_보류한다(self):
        서울 = next(항목 for 항목 in 기관탭목록(self.등록부) if 항목.id == "seoul")
        기능 = next(항목 for 항목 in 서울.functions if 항목.legacy_method == "서울대제목")
        self.assertFalse(기능.ui_ready)
        self.assertEqual(기능.parameters, ("제목상단", "제목하단"))


if __name__ == "__main__":
    unittest.main()
