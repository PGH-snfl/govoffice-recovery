"""바이트코드에서 기계적으로 복구한 단순 HAction.Run 명령."""


class GeneratedSimpleCommandMixin:
    def 가운데정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignCenter')

    def 기본정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    def 기본글자(self):
        self.대상.HAction.Run('CharShapeNormal')

    def 다음페이지(self):
        self.대상.HAction.Run('BreakPage')

    def 도형나가기(self):
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')
        self.대상.HAction.Run('BreakPara')

    def 도형나가기2(self):
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')

    def 도형텍스트입력(self):
        self.대상.HAction.Run('ShapeObjAttachTextBox')

    def 딜리트(self):
        self.대상.HAction.Run('Delete')

    def 문장내어쓰기(self):
        self.대상.HAction.Run('ParagraphShapeIndentAtCaret')

    def 밑줄(self):
        self.대상.HAction.Run('CharShapeUnderline')

    def 배분정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignDistribute')

    def 백스페이스(self):
        self.대상.HAction.Run('DeleteBack')

    def 복사(self):
        self.대상.HAction.Run('Copy')

    def 셀병합(self):
        self.대상.HAction.Run('TableMergeCell')

    def 셀선택(self):
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')

    def 셀전체(self):
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableCellBlockExtend')

    def 엔드(self):
        self.대상.HAction.Run('MoveLineEnd')

    def 오른쪽정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignRight')

    def 왼쪽정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignLeft')

    def 윗첨자(self):
        self.대상.HAction.Run('CharShapeSuperscript')

    def 이탤릭(self):
        self.대상.HAction.Run('CharShapeItalic')

    def 진하게(self):
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')

    def 진하게단일(self):
        self.대상.HAction.Run('CharShapeBold')

    def 표나가기(self):
        self.대상.HAction.Run('MoveRight')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    def 표나가기0(self):
        self.대상.HAction.Run('CloseEx')

    def 표전체(self):
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableCellBlockExtend')

    def 페이지엔터(self):
        self.대상.HAction.Run('BreakPage')

    def 캔슬(self):
        self.대상.HAction.Run('Cancel')

    def 탭(self):
        self.대상.HAction.Run('InsertTab')

    def 고급붙임(self):
        self.대상.HAction.Run('PasteSpecial')

    def 글자마이(self):
        self.대상.HAction.Run('CharShapeHeightDecrease')
        self.대상.HAction.Run('CharShapeHeightDecrease')

    def 글자플이(self):
        self.대상.HAction.Run('CharShapeHeightIncrease')
        self.대상.HAction.Run('CharShapeHeightIncrease')

    def 표탈출(self):
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveDown')
        self.대상.HAction.Run('CloseEx')
