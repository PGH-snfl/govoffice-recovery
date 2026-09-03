import unittest

from govoffice.institutions import 기관카탈로그


class 기관카탈로그시험(unittest.TestCase):
    def setUp(self):
        self.카탈로그 = 기관카탈로그()

    def test_정리된_기관_24개를_읽는다(self):
        기관들 = self.카탈로그.전체()
        self.assertEqual(len(기관들), 24)
        self.assertEqual(len({기관.id for 기관 in 기관들}), 24)

    def test_기관별_기능_503개를_읽는다(self):
        기능수 = sum(len(기관.기능목록) for 기관 in self.카탈로그.전체())
        self.assertEqual(기능수, 503)

    def test_서울_기능은_새_도메인_모델로_변환된다(self):
        서울 = self.카탈로그.찾기("seoul")
        보고서 = next(기능 for 기능 in 서울.기능목록 if 기능.실행메서드 == "서울보고서")
        self.assertEqual(보고서.기관id, "seoul")
        self.assertTrue(보고서.화면실행가능)
        self.assertEqual(보고서.복구상태, "legacy-compatible")

    def test_인자가_필요한_기능은_화면실행을_보류한다(self):
        서울 = self.카탈로그.찾기("seoul")
        대제목 = next(기능 for 기능 in 서울.기능목록 if 기능.실행메서드 == "서울대제목")
        self.assertFalse(대제목.화면실행가능)
        self.assertEqual(대제목.매개변수, ("제목상단", "제목하단"))

    def test_서울과학기술대학교도_신규_기관으로_유지한다(self):
        서울과기대 = self.카탈로그.찾기("seoultech")
        self.assertEqual(서울과기대.이름, "서울과학기술대학교")
        self.assertEqual(서울과기대.기능목록, ())


if __name__ == "__main__":
    unittest.main()

