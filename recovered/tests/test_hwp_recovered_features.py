import unittest
from types import SimpleNamespace

from 한컴오피스.한컴라이브러리_기본 import 한컴기본


class 복구기능시험(unittest.TestCase):
    def test_날짜변환은_원본_출력형식을_유지한다(self):
        한글 = 한컴기본()
        self.assertEqual("2026.08.25.", 한글.날짜변환("20260825", "점"))
        self.assertEqual("2026년 8월 25일 화요일", 한글.날짜변환("2026-8-25", "한글"))
        self.assertEqual("잘못된날짜", 한글.날짜변환("잘못된날짜", "점"))

    def test_증감계산은_퍼센트와_단위를_구분한다(self):
        한글 = 한컴기본()
        self.assertEqual("10%→15%로 50% 증가(5%p↑)", 한글.증감계산("10→15", "퍼센트정수"))
        self.assertEqual("10명→8명으로 20% 감소(2명↓)", 한글.증감계산("10명→8명", "단위정수"))

    def test_JSON에서변환은_중첩구조를_원본접두사로_펼친다(self):
        한글 = 한컴기본()
        한글.블록텍스트 = lambda: '{"제목": {"항목": 1}, "목록": ["값"]}'
        결과 = []
        한글.문장 = 결과.append

        한글.JSON에서변환()

        self.assertEqual("제목\r\n원:항목:1\r\n네모:목록\r\n원:값", 결과[0])

    def test_컨트롤표목록은_tbl_컨트롤만_순서대로_반환한다(self):
        끝 = SimpleNamespace(CtrlID="tbl", Next=None)
        중간 = SimpleNamespace(CtrlID="gso", Next=끝)
        시작 = SimpleNamespace(CtrlID="tbl", Next=중간)
        머리다음 = SimpleNamespace(Next=시작)
        한글 = 한컴기본()
        한글.대상 = SimpleNamespace(HeadCtrl=SimpleNamespace(Next=머리다음))

        self.assertEqual([시작, 끝], 한글.컨트롤표목록())

    def test_증감계산은_구분자없는_입력에서_오류대신_원문을_반환한다(self):
        한글 = 한컴기본()
        self.assertEqual("테스트", 한글.증감계산("테스트", "퍼센트정수"))
        self.assertEqual("0→5", 한글.증감계산("0→5", "단위정수"))

    def test_JSON변환은_빈_문서에서_조용히_종료한다(self):
        한글 = 한컴기본()
        한글.블록텍스트 = lambda: ""
        한글.문장 = lambda *_: self.fail("빈 JSON은 문장을 삽입하지 않아야 합니다")
        self.assertFalse(한글.JSON에서변환())


if __name__ == "__main__":
    unittest.main()
