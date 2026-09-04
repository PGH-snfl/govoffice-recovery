"""기관별 '궁극의정리범위글머리' 계열의 공통 제어 흐름 복구본."""

import re


class HwpRangeCleanupBase:
    def _궁극의정리범위글머리공통(self, 특수문자, 정리, 정리인수=(), 네모초기화=False):
        if 네모초기화:
            self.네모숫자카운트 = 0

        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        if 시작지점.Item("Para") is None:
            return

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
        self.문장(특수문자 + " " + 텍스트[한글찾기.search(텍스트).start() : len(텍스트)])
        정리(*정리인수)

        while 시작지점.Item("Para") != 끝지점.Item("Para"):
            지금위치 = self.대상.GetPosBySet().Item("Para")
            if 지금위치 == 아까위치:
                return
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)
            텍스트 = self.블록스캔()[1]
            한글찾기 = re.compile(r"[(가-힣0-9a-zA-Z“]+")
            self.문장(특수문자 + " " + 텍스트[한글찾기.search(텍스트).start() : len(텍스트)])
            정리(*정리인수)
            if 지금위치 >= 마지막위치:
                return
            아까위치 = 지금위치


class Hwp1RangeCleanupMixin(HwpRangeCleanupBase):
    def 세종교궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.세종교궁극의정리, (이미지,), True)

    def 강원궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.강원궁극의정리, (이미지,))

    def 행안궁극의정리범위글머리(self, 특수문자, 이미지, 옵션):
        return self._궁극의정리범위글머리공통(특수문자, self.행안궁극의정리, (이미지, 옵션))

    def 철도궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.철도궁극의정리, (이미지,))

    def 경기신보궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.경기신보궁극의정리, (이미지,), True)

    def 경기궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.경기궁극의정리, (이미지,), True)

    def 우본궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.우본궁극의정리, (이미지,))

    def 충남궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.충남궁극의정리, (이미지,))

    def 부여궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.부여궁극의정리, (이미지,), True)

    def 홍성궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.홍성궁극의정리, (이미지,))

    def 경기문재일반궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.경기문재일반궁극의정리, (이미지,), True)


class Hwp2RangeCleanupMixin(HwpRangeCleanupBase):
    def 부교공궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.부교공궁극의정리, (이미지,))

    def 여광항궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.여광항궁극의정리, (이미지,))

    def 석유공궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.석유공궁극의정리, (이미지,))

    def 공항공궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.공항공궁극의정리, (이미지,))

    def 가스공궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.가스공궁극의정리, (이미지,))

    def 토주공궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.토주공궁극의정리, (이미지,))

    def 전남교궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.전남교궁극의정리, (이미지,), True)

    def 해경궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.해경궁극의정리, (이미지,))

    def 한수원궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.한수원궁극의정리, (이미지,))

    def 인진궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.인진궁극의정리, (이미지,))

    def 세종궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.세종궁극의정리, (이미지,))


class MainRangeCleanupMixin(HwpRangeCleanupBase):
    def 서교공궁극의정리범위글머리(self, 특수문자):
        return self._궁극의정리범위글머리공통(특수문자, self.서교공궁극의정리)

    def 기본서식궁극의정리범위글머리(self, 특수문자):
        return self._궁극의정리범위글머리공통(특수문자, self.기본서식궁극의정리)

    def 산인공궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.산인공궁극의정리, (이미지,), True)

    def 경남도궁극의정리범위글머리(self, 특수문자):
        return self._궁극의정리범위글머리공통(특수문자, self.경남도궁극의정리)

    def 울항궁극의정리범위글머리(self, 특수문자, 이미지):
        return self._궁극의정리범위글머리공통(특수문자, self.울항궁극의정리, (이미지,), True)


__all__ = ["Hwp1RangeCleanupMixin", "Hwp2RangeCleanupMixin", "MainRangeCleanupMixin"]

