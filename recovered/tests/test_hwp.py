import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from 한컴오피스.한컴라이브러리_기본 import 한컴기본


class 기록함수:
    def __init__(self, 반환값=None):
        self.호출 = []
        self.반환값 = 반환값

    def __call__(self, *args, **kwargs):
        self.호출.append((args, kwargs))
        return self.반환값


class 파라미터기록:
    def __init__(self):
        self.항목 = []

    def SetItem(self, 이름, 값):
        self.항목.append((이름, 값))


class 액션기록:
    def __init__(self):
        self.파라미터 = 파라미터기록()
        self.기본값 = []
        self.실행 = []

    def CreateSet(self):
        return self.파라미터

    def GetDefault(self, 파라미터):
        self.기본값.append(파라미터)

    def Execute(self, 파라미터):
        self.실행.append(파라미터)


class 한글명령시험(unittest.TestCase):
    def setUp(self):
        self.Run = 기록함수()
        self.MovePos = 기록함수()
        self.FindCtrl = 기록함수()
        self.한글 = 한컴기본()
        self.한글.대상 = SimpleNamespace(
            HAction=SimpleNamespace(Run=self.Run),
            MovePos=self.MovePos,
            FindCtrl=self.FindCtrl,
        )

    def test_반복명령은_요청한_횟수만큼_실행한다(self):
        self.한글.엔터(3)
        self.assertEqual(self.Run.호출, [(("BreakPara",), {})] * 3)

    def test_셀전체는_선택을_두번_확장한다(self):
        self.한글.셀전체()
        self.assertEqual(
            self.Run.호출,
            [
                (("TableCellBlock",), {}),
                (("TableCellBlockExtend",), {}),
                (("TableCellBlockExtend",), {}),
            ],
        )

    def test_표처음과_표끝의_이동코드를_보존한다(self):
        self.한글.표처음()
        self.한글.표끝()
        self.assertEqual(
            self.MovePos.호출,
            [((106,), {}), ((104,), {}), ((105,), {}), ((107,), {})],
        )

    def test_도형나가기의_명령순서를_보존한다(self):
        self.한글.도형나가기()
        self.assertEqual(
            self.Run.호출,
            [(("CloseEx",), {}), (("MoveLineEnd",), {}), (("BreakPara",), {})],
        )

    def test_자동복구된_표탈출_명령순서를_보존한다(self):
        self.한글.표탈출()
        self.assertEqual(
            self.Run.호출,
            [(("CloseEx",), {}), (("MoveDown",), {}), (("CloseEx",), {})],
        )


class 한글연결시험(unittest.TestCase):
    def test_실행중인_한글이_있으면_새객체를_만들지_않는다(self):
        한글 = 한컴기본()
        실행객체 = object()
        with patch.object(한글, "_com확인"), patch.object(
            한글, "_실행중인_한글찾기", return_value=실행객체
        ), patch.object(한글, "_보안모듈등록") as 보안모듈등록, patch.object(
            한글, "_새한글"
        ) as 새한글:
            한글.한컴열기()
        self.assertIs(한글.대상, 실행객체)
        보안모듈등록.assert_called_once_with()
        새한글.assert_not_called()

    def test_새한글은_창을_표시하기_전에_보안모듈을_등록한다(self):
        한글 = 한컴기본()
        호출 = []
        창 = SimpleNamespace(Visible=False)
        대상 = SimpleNamespace(XHwpWindows=SimpleNamespace(Item=lambda _: 창))
        with patch("한컴오피스.recovered_source.common.connection.EnsureDispatch", return_value=대상), patch.object(
            한글, "_보안모듈등록", side_effect=lambda: 호출.append("보안모듈")
        ):
            한글._새한글()
        self.assertEqual(호출, ["보안모듈"])
        self.assertTrue(창.Visible)

    def test_보안모듈등록은_공식_모듈이름을_사용한다(self):
        한글 = 한컴기본()
        등록 = Mock(return_value=True)
        한글.대상 = SimpleNamespace(RegisterModule=등록)
        self.assertTrue(한글._보안모듈등록())
        등록.assert_called_once_with("FilePathCheckDLL", "FilePathCheckerModuleExample")


class 한글서식시험(unittest.TestCase):
    def setUp(self):
        self.액션들 = []

        def 액션생성(이름):
            액션 = 액션기록()
            self.액션들.append((이름, 액션))
            return 액션

        self.한글 = 한컴기본()
        self.한글.대상 = SimpleNamespace(
            CreateAction=액션생성,
            RGBColor=lambda r, g, b: (r, g, b),
            PointToHwpUnit=lambda 값: 값 * 10,
        )

    def test_글자크기는_포인트를_백분율_단위로_바꾼다(self):
        self.한글.글자크기(13)
        이름, 액션 = self.액션들[0]
        self.assertEqual(이름, "CharShape")
        self.assertEqual(액션.파라미터.항목, [("Height", 1300)])
        self.assertEqual(액션.실행, [액션.파라미터])

    def test_글자간격은_일곱_문자종류에_같이_적용한다(self):
        self.한글.글자간격(-5)
        _, 액션 = self.액션들[0]
        self.assertEqual(len(액션.파라미터.항목), 7)
        self.assertTrue(all(값 == -5 for _, 값 in 액션.파라미터.항목))

    def test_글자색은_RGBColor_결과를_사용한다(self):
        self.한글.글자색(1, 2, 3)
        _, 액션 = self.액션들[0]
        self.assertEqual(액션.파라미터.항목, [("TextColor", (1, 2, 3))])

    def test_문단여백은_원본처럼_두배_후_단위를_변환한다(self):
        self.한글.문단여백(5, 7)
        _, 액션 = self.액션들[0]
        self.assertEqual(
            액션.파라미터.항목,
            [("LeftMargin", 100), ("RightMargin", 140)],
        )

    def test_문장은_InsertText_액션으로_입력한다(self):
        self.한글.문장("복구 시험")
        이름, 액션 = self.액션들[0]
        self.assertEqual(이름, "InsertText")
        self.assertEqual(액션.파라미터.항목, [("Text", "복구 시험")])

    def test_문서여백은_여섯_값과_적용범위를_설정한다(self):
        구역셋 = 파라미터기록()
        페이지 = SimpleNamespace()
        구역 = SimpleNamespace(HSet=구역셋, PageDef=페이지)
        기본값 = 기록함수()
        실행 = 기록함수()
        self.한글.대상.HParameterSet = SimpleNamespace(HSecDef=구역)
        self.한글.대상.HAction = SimpleNamespace(GetDefault=기본값, Execute=실행)
        self.한글.대상.MiliToHwpUnit = lambda 값: 값 * 100

        self.한글.문서여백(20, 21, 15, 16, 10, 11)

        self.assertEqual(page_values := (
            페이지.LeftMargin,
            페이지.RightMargin,
            페이지.TopMargin,
            페이지.BottomMargin,
            페이지.HeaderLen,
            페이지.FooterLen,
            페이지.Landscape,
        ), (2000, 2100, 1500, 1600, 1000, 1100, 0))
        self.assertEqual(구역셋.항목, [("ApplyTo", 3)])
        self.assertEqual(기본값.호출, [(("PageSetup", 구역셋), {})])
        self.assertEqual(실행.호출, [(("PageSetup", 구역셋), {})])


if __name__ == "__main__":
    unittest.main()
