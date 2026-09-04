"""문서 전체 필드 입력 및 스타일 정리 기능."""

import re


class MainDocumentCleanupMixin:
    def 역학글머리(self, 글머리, 여백, 내어쓰기, 진하게=0, 자간=0):
        시작지점 = self.블록첫위치()
        한글찾기 = re.compile(r"[(가-힣0-9a-zA-Z]+")
        결과텍스트 = ""
        체크 = 0
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            while 블록스캔값 in (2, 3):
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():]
                결과텍스트 += 글머리 + 글꼬리
                블록스캔값, 텍스트 = self.대상.GetText()
                체크 = 1
            self.대상.ReleaseScan()
            self.문장(결과텍스트)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
            체크 = 0
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()
            체크 = 0
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")
        if 체크 == 1:
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
            self.문단위(0)
            self.대상.HAction.Run("CharShapeNormal")
            if 진하게 == 1:
                self.대상.HAction.Run("CharShapeBold")
            self.폰트("맑은 고딕")
            self.글자크기(12.5)
            self.줄간격(160)
            self.글자간격(자간)
            self.문단여백(여백, 0)
            self.내어쓰기(내어쓰기)
            self.자간헌터(0)

    def 역학조사본문(self):
        # 빈 문서/빈 선택에서 블록 위치 탐색과 COM 스캔이 응답하지 않는 것을 방지한다.
        if not str(self.대상.GetTextFile("TEXT", "") or "").strip():
            return None
        시작지점 = self.블록첫위치()
        결과텍스트 = ""
        체크 = 0
        try:
            self.대상.InitScan(0, 255)
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                if 블록스캔값 not in (2, 3):
                    break
                결과텍스트 += 텍스트.strip() + "\r\n"
                if 체크 == 0:
                    체크 = 1
            self.대상.ReleaseScan()
            결과텍스트 = re.sub(r" +", " ", 결과텍스트)
            결과텍스트 = re.sub(r"(\r\n)+", "\r\n", 결과텍스트)
            self.문장(결과텍스트.strip())
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            체크 = 0
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            체크 = 0
            self.대상.ReleaseScan()
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")
        if 체크 == 1:
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
            self.기본정렬()
            self.문단위(6)
            self.기본글자()
            self.폰트("휴먼명조")
            self.글자크기(13)
            self.줄간격(180)
            self.자간헌터(0)
            self.내어쓰기(10)
            self.글자간격(-10)

    def _기본서식한페이지압축(self, 반복한도):
        카운트 = 0
        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        self.캔슬()
        self.대상.SetPosBySet(시작지점)
        시작위치 = int(self.대상.KeyIndicator()[3])
        self.대상.SetPosBySet(끝지점)
        끝위치 = int(self.대상.KeyIndicator()[3])
        while 끝위치 - 시작위치 == 1 and 카운트 < 반복한도:
            카운트 += 1
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(끝지점)
            self.대상.HAction.Run("ParagraphShapeDecreaseLineSpacing")
            끝지점 = self.블록끝위치()
            끝위치 = int(self.대상.KeyIndicator()[3])
            self.캔슬()
        self.대상.SetPosBySet(시작지점)
        self.대상.HAction.Run("Select")
        self.대상.SetPosBySet(끝지점)
        끝지점 = self.블록끝위치()
        끝위치 = int(self.대상.KeyIndicator()[3])
        for _ in range(3):
            if 끝위치 == 시작위치:
                self.대상.HAction.Run("ParagraphShapeIncreaseLineSpacing")
            끝지점 = self.블록끝위치()
            끝위치 = int(self.대상.KeyIndicator()[3])
        self.대상.HAction.Run("ParagraphShapeDecreaseLineSpacing")

    def 기본서식한페이지압축하기(self):
        self._기본서식한페이지압축(14)

    def 기본서식한페이지압축하기2(self):
        self.줄간격(180)
        self._기본서식한페이지압축(15)

    def 기본서식한줄압축하기(self):
        카운트 = 0
        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        self.캔슬()
        self.대상.SetPosBySet(시작지점)
        시작위치 = int(self.대상.KeyIndicator()[5])
        self.대상.SetPosBySet(끝지점)
        끝위치 = int(self.대상.KeyIndicator()[5])
        self.대상.SetPosBySet(시작지점)
        self.대상.HAction.Run("Select")
        self.대상.SetPosBySet(끝지점)
        끝지점 = self.블록끝위치()
        끝위치 = int(self.대상.KeyIndicator()[5])
        if 끝위치 - 시작위치 < 3:
            self.글자간격(0)
            self.글자장평(100)
        끝지점 = self.블록끝위치()
        끝위치 = int(self.대상.KeyIndicator()[5])
        while 끝위치 - 시작위치 == 1 and 카운트 < 30:
            카운트 += 1
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(끝지점)
            self.대상.HAction.Run("CharShapeSpacingDecrease")
            if 카운트 > 15:
                self.대상.HAction.Run("CharShapeWidthDecrease")
            끝지점 = self.블록끝위치()
            끝위치 = int(self.대상.KeyIndicator()[5])
            self.캔슬()

    def 메머체워넣기(self, 내용):
        간이배열 = 내용.split("\n")
        간이필드 = [f"필드{i}" for i in range(1, 21)]
        for i in range(0, len(간이배열)):
            self.대상.PutFieldText(간이필드[i], 간이배열[i])

    def 전체문단스타일제거(self):
        def 모양복사():
            설정 = self.대상.HParameterSet.HShapeCopyPaste
            self.대상.HAction.GetDefault("ShapeCopyPaste", 설정.HSet)
            설정.type = 2
            self.대상.HAction.Execute("ShapeCopyPaste", 설정.HSet)

        self.대상.MovePos(3)
        마지막위치 = self.대상.GetPos()
        self.대상.MovePos(2)
        while self.대상.GetPos() != 마지막위치:
            스타일 = self.글자스타일조회()
            if 스타일 != 0:
                모양복사()
                self.글자스타일(0)
                self.대상.HAction.Run("MoveSelLineEnd")
                self.대상.Run("ShapeCopyPaste")
            self.대상.HAction.Run("Cancel")
            self.대상.HAction.Run("MoveNextParaBegin")

    def 전체표스타일제거(self):
        def 글자취급():
            액션 = self.대상.CreateAction("ShapeObjDialog")
            설정 = 액션.CreateSet()
            액션.GetDefault(설정)
            설정.SetItem("TreatAsChar", 1)
            액션.Execute(설정)

        def 모양복사():
            설정 = self.대상.HParameterSet.HShapeCopyPaste
            self.대상.HAction.GetDefault("ShapeCopyPaste", 설정.HSet)
            설정.type = 2
            self.대상.HAction.Execute("ShapeCopyPaste", 설정.HSet)

        self.대상.MovePos(3)
        self.표만들기([1], [1])
        글자취급()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.SetMessageBoxMode(16)
        self.대상.HAction.Run("MoveRight")
        self.대상.HAction.Run("DeleteBack")
        self.대상.SetMessageBoxMode(240)
        for i in range(2, 마지막위치.Item("List")):
            self.대상.SetPosBySet(self.셀위치(i))
            모양복사()
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("Select")
            self.글자스타일(0)
            self.대상.Run("ShapeCopyPaste")
            self.대상.HAction.Run("Cancel")


__all__ = ["MainDocumentCleanupMixin"]
