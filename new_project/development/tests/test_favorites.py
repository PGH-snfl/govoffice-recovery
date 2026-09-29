import tempfile
import unittest
from pathlib import Path

from govoffice.adapters.json_favorites import JSON즐겨찾기저장소
from govoffice.domain.functions import 기능, 기능출처, 기관
from govoffice.presentation.institution_tab import 기관탭모델
from govoffice.services.favorites import 즐겨찾기서비스


class 가짜한글:
    def __init__(self):
        self.호출 = []

    def 기능실행(self, 메서드, *args, **kwargs):
        self.호출.append((메서드, args, kwargs))
        return "완료"


class 즐겨찾기시험(unittest.TestCase):
    def setUp(self):
        self.임시폴더 = tempfile.TemporaryDirectory()
        저장소 = JSON즐겨찾기저장소(Path(self.임시폴더.name) / "favorites.json")
        self.한글 = 가짜한글()
        self.서비스 = 즐겨찾기서비스(저장소, self.한글)
        self.기본기능 = 기능(
            id="hwp:엔터3회",
            이름="엔터 3회",
            출처=기능출처.한글기본,
            실행메서드="엔터",
            인자=(3,),
        )
        self.기관기능 = 기능(
            id="seoultech:보고서제목",
            이름="보고서 제목",
            출처=기능출처.기관,
            실행메서드="서울과기대보고서제목",
            기관id="seoultech",
        )

    def tearDown(self):
        self.임시폴더.cleanup()

    def test_기본기능과_기관기능을_같은_즐겨찾기에_저장한다(self):
        self.assertTrue(self.서비스.추가(self.기본기능))
        self.assertTrue(self.서비스.추가(self.기관기능))
        self.assertEqual([기능.이름 for 기능 in self.서비스.목록()], ["엔터 3회", "보고서 제목"])

    def test_기관탭은_상단과_하단을_구분한다(self):
        self.서비스.추가(self.기본기능)
        모델 = 기관탭모델(기관("seoultech", "서울과학기술대학교", (self.기관기능,)), self.서비스)
        self.assertEqual(모델.상단기능, (self.기본기능,))
        self.assertEqual(모델.하단기능, (self.기관기능,))
        self.assertTrue(모델.상단으로끌어놓기(self.기관기능))

    def test_즐겨찾기_순서를_드래그_결과대로_바꾼다(self):
        self.서비스.추가(self.기본기능)
        self.서비스.추가(self.기관기능)
        self.assertTrue(self.서비스.이동(self.기관기능.id, 0))
        self.assertEqual(self.서비스.목록()[0], self.기관기능)

    def test_저장된_인자로_한글_기능을_실행한다(self):
        self.서비스.추가(self.기본기능)
        self.assertEqual(self.서비스.실행(self.기본기능.id), "완료")
        self.assertEqual(self.한글.호출, [("엔터", (3,), {})])


if __name__ == "__main__":
    unittest.main()

