"""한글 CreateAction 및 HParameterSet 기반 서식 명령."""


class HwpFormattingMixin:
    def _액션셋(self, 이름):
        액션 = self.대상.CreateAction(이름)
        파라미터 = 액션.CreateSet()
        액션.GetDefault(파라미터)
        return 액션, 파라미터

    def 글자간격(self, 간격):
        액션, 파라미터 = self._액션셋("CharShape")
        for 항목 in (
            "SpacingJapanese",
            "SpacingHanja",
            "SpacingLatin",
            "SpacingHangul",
            "SpacingUser",
            "SpacingSymbol",
            "SpacingOther",
        ):
            파라미터.SetItem(항목, 간격)
        액션.Execute(파라미터)

    def 글자색(self, 빨강, 초록, 파랑):
        액션, 파라미터 = self._액션셋("CharShape")
        파라미터.SetItem("TextColor", self.대상.RGBColor(빨강, 초록, 파랑))
        액션.Execute(파라미터)

    def 글자음영(self, 색상):
        액션, 파라미터 = self._액션셋("CharShape")
        파라미터.SetItem("ShadeColor", 색상)
        액션.Execute(파라미터)

    def 글자장평(self, 장평):
        액션, 파라미터 = self._액션셋("CharShape")
        for 항목 in (
            "RatioHangul",
            "RatioLatin",
            "RatioHanja",
            "RatioJapanese",
            "RatioOther",
            "RatioSymbol",
            "RatioUser",
        ):
            파라미터.SetItem(항목, 장평)
        액션.Execute(파라미터)

    def 글자크기(self, 크기):
        액션, 파라미터 = self._액션셋("CharShape")
        파라미터.SetItem("Height", 크기 * 100)
        액션.Execute(파라미터)

    def 문단여백(self, 좌측, 우측):
        액션, 파라미터 = self._액션셋("ParagraphShape")
        파라미터.SetItem("LeftMargin", self.대상.PointToHwpUnit(좌측 * 2))
        파라미터.SetItem("RightMargin", self.대상.PointToHwpUnit(우측 * 2))
        액션.Execute(파라미터)

    def 문단위(self, 간격):
        액션, 파라미터 = self._액션셋("ParagraphShape")
        파라미터.SetItem("PrevSpacing", 간격 * 200)
        액션.Execute(파라미터)

    def 문단아래(self, 간격):
        액션, 파라미터 = self._액션셋("ParagraphShape")
        파라미터.SetItem("NextSpacing", 간격 * 200)
        액션.Execute(파라미터)

    def 문단음영(self, 색상):
        문단모양 = self.대상.HParameterSet.HParaShape
        self.대상.HAction.GetDefault("ParagraphShape", 문단모양.HSet)
        문단모양.BorderFill.FillAttr.WinBrushFaceColor = 색상
        self.대상.HAction.Execute("ParagraphShape", 문단모양.HSet)

    def 문서여백(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리):
        구역설정 = self.대상.HParameterSet.HSecDef
        self.대상.HAction.GetDefault("PageSetup", 구역설정.HSet)
        쪽 = 구역설정.PageDef
        쪽.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        쪽.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        쪽.TopMargin = self.대상.MiliToHwpUnit(위)
        쪽.BottomMargin = self.대상.MiliToHwpUnit(아래)
        쪽.HeaderLen = self.대상.MiliToHwpUnit(머리)
        쪽.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        쪽.Landscape = 0
        구역설정.HSet.SetItem("ApplyTo", 3)
        self.대상.HAction.Execute("PageSetup", 구역설정.HSet)

    def 문장(self, 내용):
        액션, 파라미터 = self._액션셋("InsertText")
        파라미터.SetItem("Text", 내용)
        액션.Execute(파라미터)

    def 문장오른쪽(self, 내용):
        self.표오른쪽(1)
        self.문장(내용)

    def 문장아래쪽(self, 내용):
        self.표아래쪽(1)
        self.문장(내용)

