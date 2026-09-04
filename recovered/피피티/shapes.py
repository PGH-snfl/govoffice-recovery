"""PowerPoint 도형과 이미지 조작."""


class ShapeMixin:
    def _현재슬라이드(self):
        return self.피피티.ActiveWindow.View.Slide

    def 도형(self, 포인트, 색상, 라인, 굵기, 테두리색):
        현재슬라이드 = self._현재슬라이드()
        도형포인트 = 현재슬라이드.Shapes.BuildFreeform(
            EditingType=1,
            X1=포인트[0][0],
            Y1=포인트[0][1],
        )
        for x, y in 포인트[1:]:
            도형포인트.AddNodes(SegmentType=1, EditingType=1, X1=x, Y1=y)
        도형모양 = 도형포인트.ConvertToShape()
        도형모양.Fill.ForeColor.RGB = 색상
        도형모양.Line.Visible = 라인
        도형모양.Line.Weight = 굵기
        도형모양.Line.ForeColor.RGB = 테두리색
        return 도형모양

    def 사각형(self, 왼쪽, 위쪽, 너비, 높이, 색상):
        현재슬라이드 = self._현재슬라이드()
        도형 = 현재슬라이드.Shapes.AddShape(1, 왼쪽, 위쪽, 너비, 높이)
        도형.Line.Visible = 0
        도형.Fill.ForeColor.RGB = 색상

    def 사각형그라데이션(self, 왼쪽, 위쪽, 너비, 높이, 색상1, 색상2):
        현재슬라이드 = self._현재슬라이드()
        도형 = 현재슬라이드.Shapes.AddShape(1, 왼쪽, 위쪽, 너비, 높이)
        도형.Line.Visible = 0
        채우기 = 도형.Fill
        채우기.Visible = True
        채우기.TwoColorGradient(2, 1)
        채우기.ForeColor.RGB = 색상1
        채우기.BackColor.RGB = 색상2

    def 이미지(self, 이미지, 왼쪽, 위쪽, 너비, 높이):
        현재슬라이드 = self._현재슬라이드()
        현재슬라이드.Shapes.AddPicture(
            FileName=이미지,
            LinkToFile=False,
            SaveWithDocument=True,
            Left=왼쪽,
            Top=위쪽,
            Width=너비,
            Height=높이,
        )

    def 중심정렬(self):
        선택 = self.피피티.ActiveWindow.Selection
        선택.ShapeRange.Align(AlignCmd=1, RelativeTo=0)
        선택.ShapeRange.Align(AlignCmd=4, RelativeTo=0)

