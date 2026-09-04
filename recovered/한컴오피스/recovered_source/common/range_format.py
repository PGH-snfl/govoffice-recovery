"""기관별 '궁극의정리범위' 반복 제어 흐름의 소스 복구본."""

import re


class HwpRangeFormatBase:
    def _궁극의정리범위공통(
        self,
        정리,
        정리인수=(),
        초기화필드=(),
        보정대상=(),
        위치보정=True,
        종료시방금처리초기화=True,
    ):
        for 필드 in 초기화필드:
            setattr(self, 필드, 0)

        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        if 시작지점.Item("Para") is None:
            return

        self.캔슬()
        self.대상.SetPosBySet(끝지점)
        마지막위치 = self.대상.GetPosBySet().Item("Para")
        self.대상.SetPosBySet(시작지점)
        아까위치 = self.대상.GetPosBySet().Item("Para")

        정리(*정리인수)
        if 위치보정:
            마지막위치 += self.궁극의정리위치보정
            self.궁극의정리위치보정 = 0

        임시보정값 = 0
        while 시작지점.Item("Para") != 끝지점.Item("Para"):
            지금위치 = self.대상.GetPosBySet().Item("Para")
            if 지금위치 == 아까위치 and 임시보정값 == 0:
                return

            정리(*정리인수)
            if 위치보정:
                마지막위치 += self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0

            임시보정값 = 1 if 보정대상 and self.방금처리 in 보정대상 else 0
            if 지금위치 >= 마지막위치 + 임시보정값:
                if 종료시방금처리초기화:
                    self.방금처리 = 0
                return
            아까위치 = 지금위치


일반초기화 = ("소제목카운트", "중제목카운트", "위치저장", "방금처리", "궁극의정리위치보정")
네모초기화 = ("소제목카운트", "네모숫자카운트", "위치저장", "방금처리", "궁극의정리위치보정")


class Hwp1RangeFormatMixin(HwpRangeFormatBase):
    def 세종교궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.세종교궁극의정리, (이미지,), 일반초기화, ("우본표", "컨트롤엔터"))

    def 강원궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.강원궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 행안궁극의정리범위(self, 이미지, 옵션):
        초기화 = ("소제목카운트", "네모숫자카운트", "위치저장", "방금처리", "궁극의정리위치보정")
        return self._궁극의정리범위공통(self.행안궁극의정리, (이미지, 옵션), 초기화, ("행안표", "행안연간일정", "행안단계"))

    def 철도궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.철도궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 경기신보궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.경기신보궁극의정리, (이미지,), 네모초기화, ("경기표", "부여추진일정"))

    def 경기궁극의정리범위(self, 이미지, 옵션):
        초기화 = ("소제목카운트", "네모숫자카운트", "참고카운트", "붙임카운트", "위치저장", "방금처리", "궁극의정리위치보정")
        return self._궁극의정리범위공통(self.경기궁극의정리, (이미지, 옵션), 초기화, ("경기표", "부여추진일정"))

    def 우본궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.우본궁극의정리, (이미지,), 일반초기화, ("우본표", "컨트롤엔터"))

    def 충남궁극의정리범위(self, 이미지, 모드):
        return self._궁극의정리범위공통(self.충남궁극의정리, (이미지, 모드), 일반초기화, ("충남시간계획표",))

    def 부여궁극의정리범위(self, 이미지, 모드):
        return self._궁극의정리범위공통(self.부여궁극의정리, (이미지, 모드), 네모초기화, ("부여시간계획", "부여추진일정"))

    def 홍성궁극의정리범위(self, 이미지):
        초기화 = ("소제목카운트", "중제목카운트", "궁극의정리위치보정")
        return self._궁극의정리범위공통(self.홍성궁극의정리, (이미지,), 초기화, (), True, False)

    def 경기문재일반궁극의정리범위(self, 이미지, 옵션):
        초기화 = ("소제목카운트", "네모숫자카운트", "참고카운트", "붙임카운트", "위치저장", "방금처리", "궁극의정리위치보정")
        return self._궁극의정리범위공통(self.경기문재일반궁극의정리, (이미지, 옵션), 초기화, ("경기표", "부여추진일정"))


class Hwp2RangeFormatMixin(HwpRangeFormatBase):
    def 부교공궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.부교공궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 여광항궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.여광항궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 석유공궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.석유공궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 공항공궁극의정리범위(self, 이미지):
        초기화 = ("소제목카운트", "중제목카운트", "참고카운트", "카운트카운트", "위치저장", "방금처리", "궁극의정리위치보정")
        return self._궁극의정리범위공통(self.공항공궁극의정리, (이미지,), 초기화, ("부여시간계획", "부여추진일정"))

    def 가스공궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.가스공궁극의정리, (이미지,), 일반초기화, ("가스공표",))

    def 토주공궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.토주공궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 전남교궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.전남교궁극의정리, (이미지,), 일반초기화, ("우본표", "컨트롤엔터"))

    def 해경궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.해경궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))

    def 한수원궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.한수원궁극의정리, (이미지,), 일반초기화, ("한수원표", "부여추진일정"))

    def 인진궁극의정리범위(self, 이미지):
        초기화 = ("소제목카운트", "참고카운트", "붙임카운트", "중제목카운트", "위치저장", "방금처리", "궁극의정리위치보정")
        return self._궁극의정리범위공통(self.인진궁극의정리, (이미지,), 초기화, ("인진표", "부여추진일정"))

    def 세종궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.세종궁극의정리, (이미지,), 일반초기화, ("부여시간계획", "부여추진일정"))


class MainRangeFormatMixin(HwpRangeFormatBase):
    def 서교공궁극의정리범위(self):
        self.문서여백(18, 18, 12.7, 12.7, 12.7, 12.7)
        self.임시카운트 = 0
        self.원숫자카운트 = 0
        return self._궁극의정리범위공통(
            self.서교공궁극의정리,
            초기화필드=(),
            보정대상=("컨트롤엔터",),
        )

    def 인국공궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(
            self.인국공궁극의정리,
            (이미지,),
            ("소제목카운트", "중제목카운트", "궁극의정리위치보정"),
            위치보정=False,
            종료시방금처리초기화=False,
        )

    def 인국공궁극의정리범위글머리(self, 이미지, 특수문자):
        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        if 시작지점.Item("Para") is None:
            return None
        self.캔슬()
        self.대상.SetPosBySet(끝지점)
        마지막위치 = self.대상.GetPosBySet().Item("Para")
        self.대상.SetPosBySet(시작지점)
        아까위치 = self.대상.GetPosBySet().Item("Para")

        self.대상.MovePos(6)
        self.대상.HAction.Run("Select")
        self.대상.MovePos(7)
        텍스트 = self.블록스캔()[1]
        한글찾기 = re.compile(r"[(가-힣0-9a-zA-Z“(]+")
        self.문장(특수문자 + " " + 텍스트[한글찾기.search(텍스트).start():])
        self.인국공궁극의정리(이미지)

        while 시작지점.Item("Para") != 끝지점.Item("Para"):
            지금위치 = self.대상.GetPosBySet().Item("Para")
            if 지금위치 == 아까위치:
                return None
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)
            텍스트 = self.블록스캔()[1]
            한글찾기 = re.compile(r"[(가-힣0-9a-zA-Z“]+")
            self.문장(특수문자 + " " + 텍스트[한글찾기.search(텍스트).start():])
            self.인국공궁극의정리(이미지)
            마지막위치 += self.궁극의정리위치보정
            self.궁극의정리위치보정 = 0
            if 지금위치 >= 마지막위치:
                return None
            아까위치 = 지금위치

    def 서교공궁극의정리전체(self):
        self.문서여백(18, 18, 12.7, 12.7, 12.7, 12.7)
        self.임시카운트 = 0
        self.원숫자카운트 = 0
        self.대상.MovePos(2)
        아까위치 = self.대상.GetPosBySet().Item("Para")
        while True:
            self.서교공궁극의정리("다음")
            지금위치 = self.대상.GetPosBySet().Item("Para")
            if 지금위치 == 아까위치:
                return None
            아까위치 = 지금위치

    def 기본서식궁극의정리범위(self):
        return self._궁극의정리범위공통(self.기본서식궁극의정리, 위치보정=False, 종료시방금처리초기화=False)

    def 경남도궁극의정리범위(self):
        return self._궁극의정리범위공통(self.경남도궁극의정리, 초기화필드=("임시카운트",), 위치보정=False, 종료시방금처리초기화=False)

    def 산인공궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.산인공궁극의정리, (이미지,), 네모초기화, ("산인공시간계획표", "부여추진일정"))

    def 산인공궁극의정리범위2(self):
        try:
            self.대상.InitScan(1, 255)
            블록스캔값, 텍스트 = self.대상.GetText()
            결과텍스트 = ""
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔값, 텍스트 = self.대상.GetText()
            self.대상.ReleaseScan()
            결과텍스트 = re.sub(r"\r\n {4,}", " ", 결과텍스트)
            self.백스페이스()
            시작지점 = self.현재위치()
            self.문장(결과텍스트)
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
            self.임시카운트 = 0
            return self._궁극의정리범위공통(
                self.산인공궁극의정리2,
                위치보정=False,
                종료시방금처리초기화=False,
            )
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()

    def 울항궁극의정리범위(self, 이미지):
        return self._궁극의정리범위공통(self.울항궁극의정리, (이미지,), 네모초기화, ("산인공시간계획표", "부여추진일정"))


__all__ = ["Hwp1RangeFormatMixin", "Hwp2RangeFormatMixin", "MainRangeFormatMixin"]
