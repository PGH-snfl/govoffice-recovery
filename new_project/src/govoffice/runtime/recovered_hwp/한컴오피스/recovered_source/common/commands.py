"""한글의 단순 HAction 및 커서 이동 명령."""


class HwpCommandMixin:
    def _실행(self, 명령):
        return self.대상.HAction.Run(명령)

    def _반복실행(self, 명령, 횟수=1):
        for _ in range(0, 횟수):
            self._실행(명령)

    def _이동(self, 위치):
        return self.대상.MovePos(위치)

    def 가운데정렬(self): self._실행("ParagraphShapeAlignCenter")
    def 고정여백(self, 횟수=1): self._반복실행("InsertFixedWidthSpace", 횟수)
    def 객체찾기(self): self.대상.FindCtrl()
    def 기본정렬(self): self._실행("ParagraphShapeAlignJustify")
    def 기본글자(self): self._실행("CharShapeNormal")
    def 글자작게(self, 횟수=1): self._반복실행("CharShapeHeightDecrease", 횟수)
    def 글자크게(self, 횟수=1): self._반복실행("CharShapeHeightIncrease", 횟수)
    def 다음페이지(self): self._실행("BreakPage")

    def 도형나가기(self):
        self._실행("CloseEx")
        self._실행("MoveLineEnd")
        self._실행("BreakPara")

    def 도형나가기2(self):
        self._실행("CloseEx")
        self._실행("MoveLineEnd")

    def 도형텍스트입력(self): self._실행("ShapeObjAttachTextBox")
    def 딜리트(self): self._실행("Delete")
    def 리스트시작(self): self._이동(4)
    def 리스트끝(self): self._이동(5)
    def 문서처음(self): self._이동(2)
    def 문장내어쓰기(self): self._실행("ParagraphShapeIndentAtCaret")
    def 밑줄(self): self._실행("CharShapeUnderline")
    def 배분정렬(self): self._실행("ParagraphShapeAlignDistribute")
    def 백스페이스(self): self._실행("DeleteBack")
    def 복사(self): self._실행("Copy")
    def 셀병합(self): self._실행("TableMergeCell")

    def 셀선택(self):
        self._실행("TableCellBlock")
        self._실행("TableCellBlockExtend")

    def 셀전체(self):
        self._실행("TableCellBlock")
        self._실행("TableCellBlockExtend")
        self._실행("TableCellBlockExtend")

    def 엔드(self): self._실행("MoveLineEnd")
    def 엔터(self, 횟수=1): self._반복실행("BreakPara", 횟수)
    def 오른쪽정렬(self): self._실행("ParagraphShapeAlignRight")
    def 왼쪽정렬(self): self._실행("ParagraphShapeAlignLeft")
    def 윗첨자(self): self._실행("CharShapeSuperscript")
    def 이탤릭(self): self._실행("CharShapeItalic")

    def 진하게(self):
        self._실행("CharShapeNormal")
        self._실행("CharShapeBold")

    def 진하게단일(self): self._실행("CharShapeBold")

    def 표나가기(self):
        self._실행("MoveRight")
        self._실행("BreakPara")
        self._실행("ParagraphShapeAlignJustify")

    def 표나가기0(self): self._실행("CloseEx")
    def 표너비줄이기(self, 횟수=1): self._반복실행("TableResizeExLeft", 횟수)
    def 표높이줄이기(self, 횟수=1): self._반복실행("TableResizeExUp", 횟수)
    def 표오른쪽(self, 횟수=1): self._반복실행("TableRightCellAppend", 횟수)
    def 표오른쪽끝(self): self._이동(105)
    def 표왼쪽끝(self): self._이동(104)
    def 표왼쪽(self, 횟수=1):
        for _ in range(0, 횟수): self._이동(104)
    def 표아래쪽(self, 횟수=1):
        for _ in range(0, 횟수): self._이동(103)
    def 표위쪽(self, 횟수=1):
        for _ in range(0, 횟수): self._이동(102)
    def 표위쪽끝(self): self._이동(106)
    def 표아래쪽끝(self): self._이동(107)

    def 표전체(self):
        self._실행("TableCellBlock")
        self._실행("TableCellBlockExtend")
        self._실행("TableCellBlockExtend")

    def 표처음(self):
        self._이동(106)
        self._이동(104)

    def 표끝(self):
        self._이동(105)
        self._이동(107)

    def 페이지엔터(self): self._실행("BreakPage")
    def 캔슬(self): self._실행("Cancel")
    def 탭(self): self._실행("InsertTab")

