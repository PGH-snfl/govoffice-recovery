"""표 컨트롤 탐색과 표 전체 작업의 소스 복구본."""

import re
import random
from datetime import datetime
from decimal import Decimal


class HwpTableFeatureMixin:
    def 셀순환(self, 종류, 종류2=""):
        try:
            정보 = self.셀정보()
            if not 정보 or 정보[0] != 1:
                return None
            정상, 처음위치, 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열 = 정보
            블록리스트 = self.블록리스트생성(행, 열, 한줄, 처음위치)
            처음숫자 = 0
            for i, 셀번호 in enumerate(블록리스트):
                try:
                    if 종류 == "셀번호매기기":
                        if i == 0:
                            처음숫자 = int(self._블록셀텍스트(셀번호))
                        self.문장(str(처음숫자 + i))
                        continue

                    결과텍스트 = self._블록셀텍스트(셀번호)
                    if 종류 == "나누기천":
                        숫자 = re.sub(r"[^0-9]", "", 결과텍스트)
                        self.문장(str(round(int(숫자) / 1000)))
                    elif 종류 == "표대반올림":
                        숫자 = re.sub(r"[^0-9.]", "", 결과텍스트)
                        self.문장(str(int(round(float(숫자)))))
                    elif 종류 in ("원", "천원", "백만원", "억원"):
                        곱하기 = 1
                        if "천원" in 결과텍스트:
                            곱하기 = 1000
                        elif "백만원" in 결과텍스트:
                            곱하기 = 1000000
                        elif "억" in 결과텍스트:
                            곱하기 = 100000000
                        숫자 = Decimal(re.sub(r"[^0-9.]", "", 결과텍스트)) * 곱하기
                        나누기, 접미사 = {
                            "원": (1, "원"),
                            "천원": (1000, "천원"),
                            "백만원": (1000000, "백만원"),
                            "억원": (100000000, "억원"),
                        }[종류]
                        self.문장(f"{round(숫자 / 나누기):,}" + 접미사)
                    elif 종류 == "곱하기천":
                        숫자 = re.sub(r"[^0-9.]", "", 결과텍스트)
                        self.문장(str(round(int(숫자) * 1000)))
                    elif 종류 == "가지치기":
                        정리 = " ".join(결과텍스트.replace("\r", "").replace("\n", "").strip().split())
                        self.문장(정리)
                    elif 종류 == "괄호제거":
                        정리 = re.sub(r"\([^)]*\)", "", 결과텍스트)
                        self.문장(정리.replace("\r", "").replace("\n", "").strip())
                    elif 종류 == "괄호안에만":
                        self.문장(re.compile(r"\(([^)]+)").findall(결과텍스트)[0])
                    elif 종류 == "숫자만":
                        self.문장(re.sub(r"[^0-9.]", "", 결과텍스트))
                    elif 종류 == "주민암호화":
                        숫자만 = re.sub(r"[^0-9,]", "", 결과텍스트)
                        if len(숫자만) == 13:
                            숫자만 = 숫자만[:6] + "-" + 숫자만[6:7] + "******"
                        else:
                            숫자만 += "오류"
                        self.문장(숫자만)
                    elif 종류 in ("표대더하기", "표대빼기", "표대곱하기", "표대나누기"):
                        숫자 = Decimal(re.sub(r"[^0-9.]", "", 결과텍스트))
                        피연산자 = Decimal(종류2)
                        if 종류 == "표대더하기":
                            결과값 = 숫자 + 피연산자
                        elif 종류 == "표대빼기":
                            결과값 = 숫자 - 피연산자
                        elif 종류 == "표대곱하기":
                            결과값 = 숫자 * 피연산자
                        else:
                            결과값 = 숫자 / 피연산자
                        self.문장(str(결과값))
                    elif 종류 == "주민변환":
                        년도 = re.sub(r"[^0-9]", "", 결과텍스트)
                        if len(년도) == 6:
                            년 = int(년도[:2])
                            년도 = ("19" if 년 > datetime.today().year % 100 else "20") + 년도
                        self.문장(년도)
                    elif 종류 == "날짜변환":
                        self.문장(self.날짜변환(결과텍스트, 종류2))
                    elif 종류 in ("나이", "개월"):
                        원문 = re.sub(r"\([^)]*\)", "", 결과텍스트)
                        년도 = re.sub(r"[^0-9]", "", 원문)
                        if len(년도) == 6:
                            년, 월, 일 = int(년도[:2]), int(년도[2:4]), int(년도[4:])
                            년 += 1900 if 년 > datetime.today().year % 100 else 2000
                        elif len(년도) == 8:
                            년, 월, 일 = int(년도[:4]), int(년도[4:6]), int(년도[6:])
                        else:
                            continue
                        오늘 = datetime.today()
                        나이 = 오늘.year - 년
                        if 종류 == "나이":
                            if 월 > 오늘.month or (월 == 오늘.month and 일 > 오늘.day):
                                나이 -= 1
                            self.문장(원문 + "(" + str(나이) + ")")
                        else:
                            개월 = 오늘.month - 월
                            if 일 > 오늘.day:
                                개월 -= 1
                            self.문장(원문 + "(" + str(나이 * 12 + 개월) + ")")
                except ValueError as e:
                    print(f"값 오류 : {e}")
                    self.대상.ReleaseScan()
                    처음숫자 = 1
                except Exception as e:
                    print(f"오류 발생 : {e}")
                    self.대상.ReleaseScan()
                    처음숫자 = 1
        except ValueError as e:
            print(f"값 오류 : {e}")
        except Exception as e:
            print(f"오류 발생 : {e}")

    def 셀이중순환(self, 종류):
        try:
            정보 = self.셀정보()
            if not 정보 or 정보[0] != 1:
                return None
            정상, 처음위치, 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열 = 정보
            블록리스트 = self.블록리스트생성(행, 열, 한줄, 처음위치)
            데이터리스트 = []
            for 셀번호 in 블록리스트:
                try:
                    결과텍스트 = self._블록셀텍스트(셀번호)
                    결과텍스트 = " ".join(결과텍스트.replace("\r", "").replace("\n", "").strip().split())
                    if 종류 in ("셀퍼센트", "셀다중퍼센트"):
                        결과텍스트 = re.sub(r"\([^)]*\)", "", 결과텍스트)
                        결과텍스트 = re.sub(r"[^0-9.]", "", 결과텍스트)
                    데이터리스트.append(결과텍스트)
                    self.문장(결과텍스트)
                except ValueError as e:
                    print(f"값 오류 : {e}")
                    self.대상.ReleaseScan()
                except Exception as e:
                    print(f"오류 발생 : {e}")
                    self.대상.ReleaseScan()

            def 셀에쓰기(순번, 값):
                self.대상.SetPosBySet(self.셀위치(블록리스트[순번]))
                for _ in range(3):
                    self.대상.HAction.Run("Select")
                self.문장(값)

            if 종류 == "셀퍼센트":
                데이터리스트 = list(map(float, 데이터리스트))
                총합 = sum(데이터리스트)
                for i in range(len(블록리스트)):
                    임시입력값 = round(데이터리스트[i] / 총합 * 100, 1)
                    if 데이터리스트[i] - int(데이터리스트[i]) == 0:
                        데이터리스트[i] = int(데이터리스트[i])
                    셀에쓰기(i, str(데이터리스트[i]) + "\r(" + str(임시입력값) + "%)")
                return None

            if 종류 == "셀다중퍼센트":
                데이터리스트 = list(map(float, 데이터리스트))
                합계리스트 = [sum(데이터리스트[i:i + int(열)]) for i in range(0, len(데이터리스트), int(열))]
                for i in range(len(블록리스트)):
                    임시입력값 = round(데이터리스트[i] / 합계리스트[int(i / int(열))] * 100, 1)
                    if 데이터리스트[i] - int(데이터리스트[i]) == 0:
                        데이터리스트[i] = int(데이터리스트[i])
                    셀에쓰기(i, str(데이터리스트[i]) + "\r(" + str(임시입력값) + "%)")
                return None

            if 종류 == "셀다중퍼센트세로":
                데이터리스트 = list(map(float, 데이터리스트))
                합계리스트 = [0] * 열
                for i in range(len(데이터리스트)):
                    합계리스트[i % 열] += 데이터리스트[i]
                for i in range(len(블록리스트)):
                    임시입력값 = round(데이터리스트[i] / 합계리스트[i % 열] * 100, 1)
                    if 데이터리스트[i] - int(데이터리스트[i]) == 0:
                        데이터리스트[i] = int(데이터리스트[i])
                    셀에쓰기(i, str(데이터리스트[i]) + "\r(" + str(임시입력값) + "%)")
                return None

            if 종류 == "셔플":
                for i in range(len(데이터리스트) - 1, 0, -1):
                    j = random.randint(0, i)
                    데이터리스트[i], 데이터리스트[j] = 데이터리스트[j], 데이터리스트[i]
                for i in range(len(블록리스트)):
                    셀에쓰기(i, str(데이터리스트[i]))
                return None

            if 종류 in ("문자오름차순", "문자내림차순", "숫자오름차순", "숫자내림차순", "짧은차순"):
                필터리스트 = []
                for j in range(행):
                    숫자 = int(열 * j)
                    필터리스트.append([데이터리스트[숫자], 숫자])
                if 종류 == "문자오름차순":
                    필터리스트.sort(key=lambda x: x[0])
                elif 종류 == "문자내림차순":
                    필터리스트.sort(key=lambda x: x[0], reverse=True)
                elif 종류 == "숫자오름차순":
                    필터리스트.sort(key=lambda x: int(x[0]))
                elif 종류 == "숫자내림차순":
                    필터리스트.sort(key=lambda x: -int(x[0]))
                elif 종류 == "짧은차순":
                    필터리스트.sort(key=lambda x: len(x[0]))
                데이터배열 = []
                for 기준 in 필터리스트:
                    for i in range(열):
                        데이터배열.append(int(기준[1] + i))
                for i in range(len(블록리스트)):
                    셀에쓰기(i, 데이터리스트[데이터배열[i]])
                return None
        except ValueError as e:
            print(f"값 오류 : {e}")
        except Exception as e:
            print(f"오류 발생 : {e}")

    def _선택블록셀목록(self):
        정보 = self.셀정보()
        if not 정보 or 정보[0] != 1:
            return []
        _, 처음위치, 행, 열, 한줄, *_ = 정보
        return self.블록리스트생성(행, 열, 한줄, 처음위치)

    def _블록셀텍스트(self, 셀번호):
        self.대상.SetPosBySet(self.셀위치(셀번호))
        for _ in range(3):
            self.대상.HAction.Run("Select")
        return "".join(self._블록조각())

    def 셀앞뒤붙임(self, 앞내용, 뒷내용, 삭제):
        try:
            for 셀번호 in self._선택블록셀목록():
                결과텍스트 = str(앞내용) + self._블록셀텍스트(셀번호) + str(뒷내용)
                self.문장(결과텍스트.replace(삭제, ""))
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 셀찾아서바꾸기(self, 찾기1, 바꾸기1, 찾기2, 바꾸기2, 찾기3, 바꾸기3):
        try:
            for 셀번호 in self._선택블록셀목록():
                결과텍스트 = self._블록셀텍스트(셀번호)
                결과텍스트 = 결과텍스트.replace(찾기1, 바꾸기1)
                결과텍스트 = 결과텍스트.replace(찾기2, 바꾸기2)
                결과텍스트 = 결과텍스트.replace(찾기3, 바꾸기3)
                self.문장(결과텍스트)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 역가로합(self):
        try:
            정상, 처음위치, 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열 = self.셀정보()
            if 정상 != 1 or 열 < 2 or 블록처음열 == "A":
                return None
            for i in range(행):
                포인트행 = str(int(블록처음행) + i)
                self.대상.SetPosBySet(self.셀위치(처음위치 - 1 + i * 한줄))
                self.합계수식(블록처음열 + 포인트행, 블록마지막열 + 포인트행)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 역세로합(self):
        try:
            정상, 처음위치, 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열 = self.셀정보()
            if 정상 != 1 or 행 < 2 or int(블록처음행) < 2:
                return None
            포인트 = ord(블록처음열)
            for i in range(열):
                포인트수정열 = chr(포인트 + i)
                self.대상.SetPosBySet(self.셀위치(처음위치 - 한줄 + i))
                self.합계수식(포인트수정열 + 블록처음행, 포인트수정열 + 블록마지막행)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 셀너비자동조절(self):
        def 셀너비붙여넣기(셀너비):
            설정 = self.대상.HParameterSet.HShapeObject
            self.대상.HAction.GetDefault("TablePropertyDialog", 설정.HSet)
            설정.HSet.SetItem("ShapeType", 3)
            설정.HSet.SetItem("ShapeCellSize", 1)
            설정.ShapeTableCell.Width = 셀너비
            self.대상.HAction.Execute("TablePropertyDialog", 설정.HSet)

        def 행너비측정():
            액션 = self.대상.CreateAction("TablePropertyDialog")
            설정 = 액션.CreateSet()
            셀설정 = 설정.CreateItemSet("ShapeTableCell", "Cell")
            액션.GetDefault(설정)
            return 셀설정.Item("Width")

        if not self.대상.CellShape:
            return None
        self.대상.HAction.Run("Cancel")
        self.대상.MovePos(106)
        self.대상.MovePos(105)
        끝셀 = self.대상.KeyIndicator()[-1][1:].split(")")[0][0]
        행개수 = ord(끝셀) - ord("A") + 1
        self.대상.MovePos(104)
        행너비목록 = []
        for i in range(행개수):
            행너비목록.append(행너비측정())
            if i < 행개수 - 1:
                self.표오른쪽(1)
        self.대상.MovePos(104)
        전체너비합 = sum(행너비목록)
        문서너비 = self.대상.MiliToHwpUnit(208 - 0.7 * 행개수 - self.문단여백측정())
        for i in range(행개수):
            self.대상.HAction.Run("TableCellBlock")
            self.대상.HAction.Run("TableCellBlockExtend")
            self.대상.MovePos(107)
            셀너비붙여넣기(int(문서너비 * (행너비목록[i] / 전체너비합)))
            self.대상.MovePos(106)
            self.대상.HAction.Run("Cancel")
            if i < 행개수 - 1:
                self.표오른쪽(1)

    def 셀정보(self):
        if not self.대상.CellShape:
            return None

        def 선택경고():
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("드래그할때 오른쪽아래(↘) 방향으로 해야 정상작동해요!, 만약 셀1개면 다른탭을 이용하세요!")

        정상 = 1
        블록마지막 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.SetPosBySet(처음위치)
        self.대상.ReleaseScan()
        블록처음 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
        블록처음열 = re.sub(r"[^A-z]", "", 블록처음)
        블록처음행 = re.sub(r"[^0-9]", "", 블록처음)
        블록마지막열 = re.sub(r"[^A-z]", "", 블록마지막)
        블록마지막행 = re.sub(r"[^0-9]", "", 블록마지막)
        열 = ord(블록마지막열) - ord(블록처음열) + 1
        행 = int(블록마지막행) - int(블록처음행) + 1
        # 원본 바이트코드: (마지막-처음) - (열-1)
        한줄 = 마지막위치.Item("List") - 처음위치.Item("List") - (열 - 1)
        소수체크 = 0
        if 행 != 1:
            한줄 = 한줄 / (행 - 1)
            소수체크 = 한줄 - int(한줄)
        if 열 == 1 and 행 == 1:
            정상 = 0
            선택경고()
        elif 소수체크 > 0:
            선택경고()
            정상 = 0
        elif 행 >= 2:
            self.대상.SetPosBySet(self.셀위치(처음위치.Item("List") + 한줄))
            확인열 = re.sub(r"[^A-z]", "", self.대상.KeyIndicator()[-1][1:].split(")")[0])
            if 블록처음열 != 확인열:
                선택경고()
                정상 = 0
            if int(블록처음행) >= 2:
                self.대상.SetPosBySet(self.셀위치(처음위치.Item("List") - 한줄))
                확인열 = re.sub(r"[^A-z]", "", self.대상.KeyIndicator()[-1][1:].split(")")[0])
                if 블록처음열 != 확인열:
                    선택경고()
                    정상 = 0
        return (정상, 처음위치.Item("List"), 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열)

    def _선택셀번호범위(self):
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        return range(처음위치.Item("List"), 마지막위치.Item("List") + 1)

    def _셀텍스트선택(self, 셀번호, 선택횟수=3):
        self.대상.SetPosBySet(self.셀위치(셀번호))
        for _ in range(선택횟수):
            self.대상.HAction.Run("Select")
        return "".join(self._블록조각())

    def 셀공백제거(self):
        if not self.대상.CellShape:
            return None
        for 셀번호 in self._선택셀번호범위():
            결과텍스트 = self._셀텍스트선택(셀번호)
            결과텍스트 = 결과텍스트.replace("\r", "").replace("\n", "").strip()
            self.문장(" ".join(결과텍스트.split()))

    def 셀숫자오른쪽정렬(self):
        if not self.대상.CellShape:
            return None
        for 셀번호 in self._선택셀번호범위():
            결과텍스트 = self._셀텍스트선택(셀번호)
            if re.search(r"[0-9,]+", 결과텍스트.strip()):
                self.오른쪽정렬()
            self.문단여백(0, 10)
            self.문장(결과텍스트)

    def 셀엔터변환(self):
        if not self.대상.CellShape:
            return None
        for 셀번호 in self._선택셀번호범위():
            결과텍스트 = self._셀텍스트선택(셀번호, 4)
            if 결과텍스트 == "":
                self.캔슬()
                self.문장("-")
                continue
            결과텍스트 = 결과텍스트.replace("\r\n", " 엔터 ").replace("\n", " 엔터 ")
            self.문장(결과텍스트)

    def 셀전체크기(self):
        def 페이지넓이():
            액션 = self.대상.CreateAction("PageSetup")
            설정 = 액션.CreateSet()
            액션.GetDefault(설정)
            페이지 = 설정.Item("PageDef")
            return 페이지.Item("LeftMargin") + 페이지.Item("RightMargin")

        def 페이지높이():
            액션 = self.대상.CreateAction("PageSetup")
            설정 = 액션.CreateSet()
            액션.GetDefault(설정)
            페이지 = 설정.Item("PageDef")
            return (
                페이지.Item("TopMargin")
                + 페이지.Item("BottomMargin")
                + 페이지.Item("HeaderLen")
                + 페이지.Item("FooterLen")
            )

        넓이 = 페이지넓이()
        높이 = 페이지높이()
        if self.대상.CellShape:
            설정 = self.대상.HParameterSet.HShapeObject
            self.대상.HAction.GetDefault("TablePropertyDialog", 설정.HSet)
            설정.HSet.SetItem("ShapeType", 3)
            설정.HSet.SetItem("ShapeCellSize", 1)
            설정.ShapeTableCell.Width = 58962 - 넓이
            설정.ShapeTableCell.Height = 83520 - 높이
            self.대상.HAction.Execute("TablePropertyDialog", 설정.HSet)

    def 사진표만들기(self):
        from tkinter import filedialog

        이름 = filedialog.askopenfilenames(
            title="Open File",
            filetypes=[("image files", (".png", ".jpg"))],
        )
        표너비값 = (203 - self.문단여백측정()) / 2
        self.표만들기([표너비값, 표너비값], [30, 4])
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.글자크기(12)
        self.가운데정렬()
        self.진하게()
        self.폰트("맑은 고딕")
        self.대상.HAction.Run("Copy")
        self.캔슬()
        self.표처음()

        for i in range(len(이름)):
            if i != 0:
                self.표오른쪽(1)
            self.대상.InsertBackgroundPicture(
                "SelectedCell", 이름[i], 1, 5, 0, 0, 0, 0
            )
            if i % 2 != 1:
                continue

            그림제목 = re.search(r"\(([^()]+)\)(?!.*\()", 이름[i - 1])
            self.표오른쪽(1)
            self.문장(그림제목.group(1))
            그림제목 = re.search(r"\(([^()]+)\)(?!.*\()", 이름[i])
            self.표오른쪽(1)
            self.문장(그림제목.group(1))
            if i != len(이름) - 1:
                self.아래로붙이기()

    def 컨트롤표목록(self):
        표목록 = []
        컨트롤 = self.대상.HeadCtrl.Next.Next
        while 컨트롤:
            if 컨트롤.CtrlID == "tbl":
                표목록.append(컨트롤)
            컨트롤 = 컨트롤.Next
        return 표목록

    def 전체셀보호해제(self):
        if self.대상.CellShape:
            self.셀보호해제()
            return

        컨트롤 = self.대상.HeadCtrl
        while 컨트롤:
            if 컨트롤.CtrlID == "tbl":
                위치 = 컨트롤.GetAnchorPos(0)
                self.대상.SetPosBySet(위치)
                self.대상.FindCtrl()
                self.대상.HAction.Run("ShapeObjTableSelCell")
                self.대상.HAction.Run("TableCellBlockExtend")
                self.대상.HAction.Run("TableCellBlockExtend")
                self.셀보호해제()
            컨트롤 = 컨트롤.Next


__all__ = ["HwpTableFeatureMixin"]
