"""PowerPoint 텍스트 상자 조작."""


class TextMixin:
    def 문장(self, 왼쪽, 위쪽, 너비, 높이, 글자, 폰트, 크기, 볼드, 색상, 정렬):
        현재슬라이드 = self._현재슬라이드()
        글상자 = 현재슬라이드.Shapes.AddTextbox(
            Orientation=1,
            Left=왼쪽,
            Top=위쪽,
            Width=너비,
            Height=높이,
        )
        텍스트 = 글상자.TextFrame.TextRange
        텍스트.Text = 글자
        텍스트.Font.NameFarEast = 폰트
        텍스트.Font.Name = 폰트
        텍스트.Font.Size = 크기
        텍스트.Font.Bold = 볼드
        텍스트.Font.Color.RGB = 색상
        텍스트.ParagraphFormat.Alignment = 정렬

    def 문장음영(self, 왼쪽, 위쪽, 너비, 높이, 글자, 폰트, 크기, 볼드, 색상, 배경색):
        현재슬라이드 = self._현재슬라이드()
        글상자 = 현재슬라이드.Shapes.AddTextbox(
            Orientation=1,
            Left=왼쪽,
            Top=위쪽,
            Width=너비,
            Height=높이,
        )
        텍스트 = 글상자.TextFrame.TextRange
        텍스트.Text = 글자
        텍스트.Font.Name = 폰트
        텍스트.Font.Size = 크기
        텍스트.Font.Bold = 볼드
        글상자.Fill.ForeColor.RGB = 배경색
        텍스트.Font.Color.RGB = 색상
        텍스트.ParagraphFormat.Alignment = 1

