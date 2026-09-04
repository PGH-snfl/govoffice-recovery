import unittest
from types import SimpleNamespace

from 피피티.피피티라이브러리 import 피피티


class 호출기록:
    def __init__(self, 반환값=None):
        self.호출 = []
        self.반환값 = 반환값

    def __call__(self, *args, **kwargs):
        self.호출.append((args, kwargs))
        return self.반환값


class 슬라이드목록:
    def __init__(self):
        self.Count = 2
        self.호출 = []

    def Add(self, 위치, 레이아웃):
        self.호출.append(((위치, 레이아웃), {}))
        self.Count += 1


def 색상객체():
    return SimpleNamespace(RGB=None)


class PowerPoint기본기능시험(unittest.TestCase):
    def setUp(self):
        self.텍스트범위 = SimpleNamespace(
            Text=None,
            Font=SimpleNamespace(
                NameFarEast=None,
                Name=None,
                Size=None,
                Bold=None,
                Color=색상객체(),
            ),
            ParagraphFormat=SimpleNamespace(Alignment=None),
        )
        self.글상자 = SimpleNamespace(
            TextFrame=SimpleNamespace(TextRange=self.텍스트범위),
            Fill=SimpleNamespace(ForeColor=색상객체()),
        )
        self.AddTextbox = 호출기록(self.글상자)
        self.AddPicture = 호출기록()
        self.AddShape = 호출기록(
            SimpleNamespace(Line=SimpleNamespace(Visible=None), Fill=SimpleNamespace(ForeColor=색상객체()))
        )
        self.슬라이드 = SimpleNamespace(
            Shapes=SimpleNamespace(
                AddTextbox=self.AddTextbox,
                AddPicture=self.AddPicture,
                AddShape=self.AddShape,
            )
        )
        self.슬라이드목록 = 슬라이드목록()
        self.페이지이동 = 호출기록()
        self.프레젠테이션 = SimpleNamespace(
            PageSetup=SimpleNamespace(SlideWidth=None, SlideHeight=None),
            Slides=self.슬라이드목록,
        )
        self.대상 = 피피티()
        self.대상.피피티 = SimpleNamespace(
            ActivePresentation=self.프레젠테이션,
            ActiveWindow=SimpleNamespace(
                View=SimpleNamespace(Slide=self.슬라이드, GotoSlide=self.페이지이동)
            ),
        )

    def test_문장은_원본_키워드로_텍스트상자를_만든다(self):
        self.대상.문장(10, 20, 300, 40, "제목", "맑은 고딕", 18, True, 123, 2)

        self.assertEqual(
            self.AddTextbox.호출,
            [((), {"Orientation": 1, "Left": 10, "Top": 20, "Width": 300, "Height": 40})],
        )
        self.assertEqual(self.텍스트범위.Text, "제목")
        self.assertEqual(self.텍스트범위.Font.NameFarEast, "맑은 고딕")
        self.assertEqual(self.텍스트범위.Font.Color.RGB, 123)
        self.assertEqual(self.텍스트범위.ParagraphFormat.Alignment, 2)

    def test_이미지는_문서에_포함되도록_추가한다(self):
        self.대상.이미지("그림.png", 1, 2, 3, 4)
        self.assertEqual(
            self.AddPicture.호출,
            [(
                (),
                {
                    "FileName": "그림.png",
                    "LinkToFile": False,
                    "SaveWithDocument": True,
                    "Left": 1,
                    "Top": 2,
                    "Width": 3,
                    "Height": 4,
                },
            )],
        )

    def test_화면은_960_대_540으로_설정한다(self):
        self.대상.화면("사용되지 않는 원본 인자")
        self.assertEqual(self.프레젠테이션.PageSetup.SlideWidth, 960)
        self.assertEqual(self.프레젠테이션.PageSetup.SlideHeight, 540)

    def test_다음페이지는_끝에_빈_슬라이드를_추가하고_이동한다(self):
        self.대상.다음페이지()
        self.assertEqual(self.슬라이드목록.호출, [((3, 12), {})])
        self.assertEqual(self.페이지이동.호출, [((3,), {})])


if __name__ == "__main__":
    unittest.main()
