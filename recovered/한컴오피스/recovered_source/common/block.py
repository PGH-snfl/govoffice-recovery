"""블록 선택, 스캔 및 변환 기능."""

import re
from datetime import datetime
from decimal import Decimal


class _BlockScanBase:
    def _블록조각(self):
        self.대상.InitScan(1, 255)
        try:
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                if 블록스캔값 not in (2, 3):
                    break
                yield 텍스트
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
        finally:
            self.대상.ReleaseScan()


class HwpBlockFeatureMixin(_BlockScanBase):
    def 글머리기본(self, 글머리):
        한글찾기 = re.compile(r"[가-힣0-9a-zA-Z]+")
        결과텍스트 = ""
        카운트 = 0
        지울배열 = [
            "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.",
            "10", "11", "12", "13", "14", "가.", "나.", "다.", "라.",
            "마.", "바.", "사.", "아.", "자.", "차.", "카.", "타.", "파.",
            "하.", "1)", "2)", "3)", "4)", "5)", "6)", "7)", "8)", "9)",
            "10", "11", "12", "13", "14", "가)", "나)", "다)", "라)",
            "마)", "바)", "사)", "아)", "자)", "차)", "카)", "타)", "파)", "하)",
        ]
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            while 블록스캔값 in (2, 3):
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():]
                if 글꼬리[:2] in 지울배열:
                    글꼬리 = 글꼬리[3:]
                    글꼬리 = 글꼬리[한글찾기.search(글꼬리).start():]
                결과텍스트 += 글머리[0] + 글머리[카운트 + 1] + " " + 글꼬리
                블록스캔값, 텍스트 = self.대상.GetText()
                카운트 += 1
                if 카운트 > 13:
                    카운트 = 0
            self.대상.ReleaseScan()
            self.문장(결과텍스트)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()
            self.대상.ReleaseScan()
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")

    def 답번호기본(self):
        한글찾기 = re.compile(r"[(ㄱ-ㅎ가-힣0-9a-zA-Z]+")
        답배열 = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮"]
        답카운트 = 0
        결과텍스트 = ""
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            while 블록스캔값 in (2, 3):
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():]
                if 답카운트 < 15:
                    결과텍스트 += " " + 답배열[답카운트] + " " + 글꼬리
                    답카운트 += 1
                else:
                    결과텍스트 += 글꼬리
                블록스캔값, 텍스트 = self.대상.GetText()
            self.대상.ReleaseScan()
            self.문장(결과텍스트)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")

    def 블록계산(self):
        패턴 = re.compile(r"(?:(?<=[^\d\.])(?=\d)|(?=[^\d\.]))")
        연산자 = ("*", "/", "+", "-", "(", ")")
        연산순위 = {"*": 2, "/": 2, "+": 1, "-": 1, "(": 0}
        후위식, 스택 = [], []
        계산자 = ("*", "/", "+", "-")
        계산식 = {
            "*": lambda x, y: y * x,
            "/": lambda x, y: y / x,
            "+": lambda x, y: y + x,
            "-": lambda x, y: y - x,
        }
        계산스택 = []
        블록스캔값, 텍스트 = self.블록스캔()
        if "\r" in 텍스트:
            return None
        try:
            텍스트 = (텍스트.replace("더하기", "+").replace("곱하기", "*")
                      .replace("나누기", "/").replace("빼기", "-").replace("더하기", "+"))
            산식 = re.sub(r"[^\d\(\)\-\*\/\+.]", "", 텍스트)
            토큰덩어리 = re.sub(패턴, " ", 산식).split(" ")
            for 토큰 in 토큰덩어리:
                if 토큰 not in 연산자:
                    후위식.append(토큰)
                elif 토큰 == "(":
                    스택.append(토큰)
                elif 토큰 == ")":
                    while 스택 != [] and 스택[-1] != "(":
                        후위식.append(스택.pop())
                    스택.pop()
                else:
                    while 스택 != [] and 연산순위[스택[-1]] >= 연산순위[토큰]:
                        후위식.append(스택.pop())
                    스택.append(토큰)
            while 스택:
                후위식.append(스택.pop())
            for 토큰 in 후위식:
                if 토큰 not in 계산자:
                    계산스택.append(float(토큰) if "." in 토큰 else int(토큰))
                else:
                    x = 계산스택.pop()
                    y = 계산스택.pop()
                    계산스택.append(계산식[토큰](x, y))
            self.문장(str(계산스택[-1]))
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 블록글머리(self, 종류):
        한글찾기 = re.compile(r"[(가-힣0-9a-zA-Z]+")
        try:
            조각 = list(self._블록조각())
            결과 = []
            if 종류 == "복사" and 조각:
                매치 = 한글찾기.search(조각[0])
                self.글머리 = 조각[0][:매치.start()]
                결과.append(조각.pop(0))
            for 텍스트 in 조각:
                매치 = 한글찾기.search(텍스트)
                글꼬리 = 텍스트[매치.start():]
                결과.append(글꼬리 if 종류 == "삭제" else self.글머리 + 글꼬리)
            self.문장("".join(결과))
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")

    def 블록금액비율(self, 일번이름, 이번이름, 삼번이름, 사번이름, 일번값, 이번값, 삼번값, 사번값):
        텍스트 = self.블록스캔()[1]
        if "\r" in 텍스트:
            return None
        텍스트 = re.sub(r"\([^)]*\)", "", 텍스트)
        try:
            숫자만 = re.sub(r"[^0-9]", "", 텍스트)
            전체값 = 일번값 + 이번값 + 삼번값 + 사번값
            출력배열 = []
            for 이름, 값 in ((일번이름, 일번값), (이번이름, 이번값), (삼번이름, 삼번값), (사번이름, 사번값)):
                if 값 != 0:
                    출력배열.append(이름 + " " + format(round(float(숫자만) * 값 / 전체값), ","))
            if 출력배열:
                self.문장(텍스트 + "(" + ", ".join(출력배열) + ")")
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 블록순환(self, 종류):
        시작지점 = self.블록첫위치()
        결과텍스트 = [텍스트.replace("\r\n", "") for 텍스트 in self._블록조각()]
        if 종류 == "짧은차순":
            결과텍스트.sort(key=len)
        elif 종류 == "오름차순":
            결과텍스트.sort()
        elif 종류 == "내림차순":
            결과텍스트.sort(reverse=True)
        self.문장("\r\n".join(결과텍스트))
        if 결과텍스트:
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)

    def 블록여러줄(self, 종류, 내용1, 내용2, 내용3, 내용4, 내용5, 내용6):
        시작지점 = self.블록첫위치()
        결과 = []
        for 텍스트 in self._블록조각():
            엔터 = "\r\n" in 텍스트
            if 종류 == "앞": 텍스트 = str(내용1) + 텍스트
            elif 종류 == "뒤":
                위치 = 텍스트.find("\r") if 엔터 else len(텍스트)
                텍스트 = 텍스트[:위치] + str(내용1) + 텍스트[위치:]
            elif 종류 == "삭제": 텍스트 = 텍스트.replace(내용1, "")
            elif 종류 == "바꾸기":
                텍스트 = 텍스트.replace(내용1, 내용2).replace(내용3, 내용4).replace(내용5, 내용6)
            elif 종류 == "맨앞제거": 텍스트 = 텍스트[1:]
            elif 종류 == "맨앞표": 텍스트 = "표:" + 텍스트
            elif 종류 in ("탭띄숫자", "탭띄숫자1"):
                텍스트 = 텍스트.replace("\r", "").replace("\n", "") + "\t" + (" 00" if 종류 == "탭띄숫자" else " 0")
                if 엔터: 텍스트 += "\r"
            elif 종류 == "맨앞어절제거":
                텍스트 = " ".join(텍스트.strip().split()[1:]) + ("\r" if 엔터 else "")
            elif 종류 == "맨뒤제거":
                텍스트 = 텍스트.replace("\r", "").replace("\n", "")[:-1] + ("\r" if 엔터 else "")
            elif 종류 == "맨뒤어절제거":
                텍스트 = " ".join(텍스트.strip().split()[:-1]) + ("\r" if 엔터 else "")
            결과.append(텍스트)
        self.문장("".join(결과))
        if 결과:
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)

    def 짧순정답(self):
        시작지점 = self.블록첫위치()
        체크 = 0
        결과텍스트 = []
        한글찾기 = re.compile(r"[(ㄱ-ㅎ가-힣0-9a-zA-Z]+")
        self.대상.InitScan(1, 255)
        try:
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                if 블록스캔값 not in (2, 3):
                    break
                체크 = 1
                텍스트 = 텍스트.replace("\r\n", "")
                매치 = 한글찾기.search(텍스트)
                텍스트 = 텍스트[매치.start():]
                결과텍스트.append(텍스트)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            return None
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            return None
        finally:
            self.대상.ReleaseScan()
        결과텍스트.sort(key=len)
        답배열 = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮"]
        줄 = []
        for i, 텍스트 in enumerate(결과텍스트):
            줄.append((" " + 답배열[i] + " " if i < 15 else "") + 텍스트)
        self.문장("\r\n".join(줄))
        if 체크 == 1:
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)

    def 블록한줄(self, 종류):
        텍스트 = self.블록스캔()[1]
        if "\r" in 텍스트:
            return None
        try:
            if 종류 == "금액한글화":
                숫자 = int(re.sub(r"[^0-9]", "", 텍스트))
                self.문장("금" + format(숫자, ",") + "원(금" + self.한글화(숫자) + "원)")
            elif 종류 == "인국공금액한글화":
                숫자 = int(re.sub(r"[^0-9]", "", 텍스트))
                self.문장("일금 " + self.한글화(숫자) + " 원정(₩" + format(숫자, ",") + ")")
            elif 종류 in ("천원", "백만원"):
                곱하기 = 1000 if "천원" in 텍스트 else 1000000 if "백만원" in 텍스트 else 100000000 if "억" in 텍스트 else 1
                숫자 = Decimal(re.sub(r"[^0-9.]", "", 텍스트)) * 곱하기
                나누기 = 1000 if 종류 == "천원" else 1000000
                self.문장(format(round(숫자 / 나누기), ",") + 종류)
            elif 종류 == "블록콤마넣기":
                self.문장(format(int(텍스트), ","))
            elif 종류 == "블록콤마빼기":
                self.문장(텍스트.replace(",", ""))
            elif 종류 == "블록주민변환":
                년도 = re.sub(r"[^0-9]", "", 텍스트)
                if len(년도) == 6:
                    년 = int(년도[:2])
                    년도 = ("19" if 년 > datetime.today().year % 100 else "20") + 년도
                    self.문장(년도)
            elif 종류 in ("블록나이", "블록개월"):
                텍스트 = re.sub(r"\([^)]*\)", "", 텍스트)
                년도 = re.sub(r"[^0-9]", "", 텍스트)
                if len(년도) not in (6, 8):
                    return None
                if len(년도) == 6:
                    년, 월, 일 = int(년도[:2]), int(년도[2:4]), int(년도[4:])
                    년 += 1900 if 년 > datetime.today().year % 100 else 2000
                else:
                    년, 월, 일 = int(년도[:4]), int(년도[4:6]), int(년도[6:])
                오늘 = datetime.today()
                if 종류 == "블록나이":
                    나이 = 오늘.year - 년
                    if 월 > 오늘.month or (월 == 오늘.month and 일 > 오늘.day):
                        나이 -= 1
                    self.문장(텍스트 + "(" + str(나이) + ")")
                else:
                    개월 = (오늘.year - 년) * 12 + 오늘.month - 월
                    if 일 > 오늘.day:
                        개월 -= 1
                    self.문장(텍스트 + "(" + str(개월) + ")")
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 블록전체스캔(self):
        return [텍스트.replace("\r", "").replace("\n", "") for 텍스트 in self._블록조각()]

    def 블록문장스캔(self):
        return "".join(self._블록조각())

    def 블록텍스트(self):
        return "".join(self._블록조각())

    def 블록여백정리(self):
        결과텍스트 = re.sub(r" +", " ", "".join(self._블록조각()))
        self.문장(결과텍스트)

    def 블록엔터코드(self):
        결과텍스트 = repr("".join(self._블록조각()))
        print(결과텍스트)
        self.문장(결과텍스트)

    def 블록엔터정리(self):
        결과텍스트 = re.sub(r"(\r\n)+", "\r\n", "".join(self._블록조각()))
        self.문장(결과텍스트)

    def 블록엔터정리공백정리(self):
        결과텍스트 = re.sub(r"(\r\n)+", "\r\n", "".join(self._블록조각()))
        결과텍스트 = re.sub(r" +", " ", 결과텍스트)
        self.문장(결과텍스트)

    def 블록엔터제거공백정리(self):
        결과텍스트 = re.sub(r"(\r\n)+", " ", "".join(self._블록조각()))
        결과텍스트 = re.sub(r" +", " ", 결과텍스트)
        결과텍스트 = re.sub(r"(?<=[가-힣])ㆍ\s+", "ㆍ", 결과텍스트)
        self.문장(결과텍스트)


class MainBlockFeatureMixin(_BlockScanBase):
    def 메모블록메모(self):
        결과텍스트 = "".join(self._블록조각())
        self.대상.HAction.Run("Delete")
        self.대상.HAction.Run("InsertFieldMemo")
        self.문장(결과텍스트)


__all__ = ["HwpBlockFeatureMixin", "MainBlockFeatureMixin"]
