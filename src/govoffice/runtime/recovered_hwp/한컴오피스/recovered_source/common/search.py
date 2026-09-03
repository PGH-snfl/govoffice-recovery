"""찾기·바꾸기 및 검색 결과 좌표 처리 기능."""


class HwpSearchFeatureMixin:
    """한글의 반복 찾기 결과를 파이썬 목록으로 변환한다."""

    def 글자좌표리스트(self, 내용):
        self.대상.MovePos(2)
        결과리스트 = []

        while True:
            self.정규표현식(내용)
            시작지점 = self.대상.CreateSet("ListParaPos")
            끝지점 = self.대상.CreateSet("ListParaPos")
            self.대상.GetSelectedPosBySet(시작지점, 끝지점)
            if 시작지점.Item("Pos") is None:
                break

            self.대상.HAction.Run("Cancel")
            self.대상.SetPosBySet(
                self.좌표(
                    시작지점.Item("List"),
                    시작지점.Item("Para"),
                    시작지점.Item("Pos") + 1,
                )
            )
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(
                self.좌표(
                    끝지점.Item("List"),
                    끝지점.Item("Para"),
                    끝지점.Item("Pos") - 2,
                )
            )
            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            텍스트 = 블록스캔[1]
            self.대상.ReleaseScan()
            결과리스트.append([시작지점, 끝지점, 텍스트])
            self.대상.HAction.Run("Cancel")

        return 결과리스트

    def 글자크기좌표리스트(self, 크기):
        self.대상.MovePos(2)
        결과리스트 = []

        while True:
            self.글자크기찾기(크기)
            시작지점 = self.대상.CreateSet("ListParaPos")
            끝지점 = self.대상.CreateSet("ListParaPos")
            self.대상.GetSelectedPosBySet(시작지점, 끝지점)
            if 시작지점.Item("Pos") is None:
                break

            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            텍스트 = 블록스캔[1]
            self.대상.ReleaseScan()
            페이지위치 = self.대상.KeyIndicator()[3]
            결과리스트.append([페이지위치, 텍스트])
            self.대상.HAction.Run("Cancel")

        return 결과리스트


class MainSearchFeatureMixin(HwpSearchFeatureMixin):
    def 날짜검색(self, 값):
        self.대상.MovePos(2)
        표현식 = r"([0-9]+\.\b[0-9]+\.\b[0-9]+\.)|([0-9]+\.\b[0-9]+\.)|([0-9]+년)|([0-9]+월)|([0-9]+일)"
        while True:
            self.정규표현식(표현식)
            시작지점 = self.대상.CreateSet("ListParaPos")
            끝지점 = self.대상.CreateSet("ListParaPos")
            self.대상.GetSelectedPosBySet(시작지점, 끝지점)
            if 시작지점.Item("Pos") is None:
                return None
            if 값 == 2:
                self.글자색(0, 0, 0)
            else:
                self.글자색(255, 0, 0)
            self.대상.HAction.Run("Cancel")
