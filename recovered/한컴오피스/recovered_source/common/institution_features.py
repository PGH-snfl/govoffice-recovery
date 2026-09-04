"""기관별 메서드 중 독립적으로 확인된 소형 조합 기능."""

import re
import os
from datetime import datetime, timedelta
from decimal import Decimal
from importlib import import_module

try:
    from tkinter import filedialog
except ImportError:
    filedialog = None


class Hwp1InstitutionFeatureMixin:
    def _선택표행추출(self, 열수):
        if not self.대상.CellShape:
            return []
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        셀값 = []
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            셀값.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        return [셀값[i:i + 열수] for i in range(0, len(셀값), 열수)]

    @staticmethod
    def _행안부정리데이터(세부사업명, 분할리스트):
        정리데이터 = []
        내역사업명 = ""
        for 줄 in 분할리스트[1:]:
            if 줄[0] == "계":
                정리데이터.append([세부사업명, "합계", "합계", *줄[1:9]])
            elif "-" not in 줄[0] and 줄[0] != "":
                내역사업명 = 줄[0]
                정리데이터.append([세부사업명, 줄[0], "소계", *줄[1:9]])
            elif "-" in 줄[0]:
                정리데이터.append([세부사업명, 내역사업명, 줄[0], *줄[1:9]])
        return 정리데이터

    @staticmethod
    def _행안부엑셀시작():
        from 엑셀.엑셀라이브러리 import 엑셀

        임시엑셀 = 엑셀()
        임시엑셀.시작()
        return 임시엑셀

    def _기본기관표(self, 이름, 내용, 행높이, 글자크기, 배경색):
        if self.방금처리 == 이름:
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A1":
                self.표아래쪽(1)
            else:
                self.표오른쪽(1)
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
                if "○" in 입력내용:
                    입력내용 = 입력내용.replace("○", " ○")
                    self.왼쪽정렬()
                elif "□" in 입력내용:
                    입력내용 = 입력내용.replace("□", " □")
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif "▪" in 입력내용:
                    입력내용 = 입력내용.replace("▪", " ▪")
                    self.왼쪽정렬()
                    self.내어쓰기(-15.9)
                    self.진하게()
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = 이름
            self.표나가기2()
            return None

        표개수 = len(내용)
        전체길이 = 207 - 표개수 * 3.5 - self.문단여백측정()
        표넓이 = [2] * 표개수
        for i in range(표개수):
            검사내용 = 내용[i].replace("엔터 ", "").replace(" ", "")
            if any(키워드 in 검사내용 for 키워드 in ("소요시간",)):
                표넓이[i] = 0.5
            elif any(키워드 in 검사내용 for 키워드 in ("연번", "순번", "번호", "구분")):
                표넓이[i] = 1
            elif any(키워드 in 검사내용 for 키워드 in ("시간계획",)):
                표넓이[i] = 1.5
            elif any(키워드 in 검사내용 for 키워드 in ("주민번호", "비고")):
                표넓이[i] = 2
            elif any(키워드 in 검사내용 for 키워드 in ("주소", "내용", "사항", "세부", "수집항목")):
                표넓이[i] = 4
        표넓이합 = sum(표넓이)
        for i in range(표개수):
            표넓이[i] = 표넓이[i] / 표넓이합 * 전체길이
        self.표만들기(표넓이, 행높이)
        self.표전체()
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(글자크기)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.글자크기(글자크기)
        self.표배경색(*배경색)
        self.캔슬()
        self.표처음()
        for i in range(표개수):
            if i != 0:
                self.표오른쪽(1)
            입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = 이름
        self.표나가기2()

    def 우본표(self, 내용=[]):
        return self._기본기관표("우본표", 내용, [6.5] * 2, 12, (210, 235, 238))

    def 행안표(self, 내용=[]):
        return self._기본기관표("행안표", 내용, [10, 7], 11, (223, 230, 247))

    def 경기표(self, 내용=[]):
        if self.방금처리 == "경기표":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A1":
                self.표아래쪽(1)
            else:
                self.표오른쪽(1)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A3":
                self.셀선택()
                self.표오른쪽끝()
                self.표단일선("상", 1, 1)
                self.캔슬()
                self.표왼쪽끝()
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
                if "○" in 입력내용:
                    입력내용 = 입력내용.replace("○", " ○")
                    self.왼쪽정렬()
                elif "□" in 입력내용:
                    입력내용 = 입력내용.replace("□", " □")
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif "▪" in 입력내용:
                    입력내용 = 입력내용.replace("▪", " ▪")
                    self.왼쪽정렬()
                    self.내어쓰기(-15.9)
                    self.진하게()
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = "경기표"
            self.표나가기2()
            return None

        표개수 = len(내용)
        전체길이 = 207 - 표개수 * 3.5 - self.문단여백측정()
        표넓이 = [2] * 표개수
        for i in range(표개수):
            검사내용 = 내용[i].replace("엔터 ", "").replace(" ", "")
            if any(키워드 in 검사내용 for 키워드 in ("소요시간",)):
                표넓이[i] = 0.7
            elif any(키워드 in 검사내용 for 키워드 in ("주민번호",)):
                표넓이[i] = 2
            elif any(키워드 in 검사내용 for 키워드 in ("연번", "순번", "번호", "구분", "이름")):
                표넓이[i] = 1
            elif any(키워드 in 검사내용 for 키워드 in ("시간계획", "비고", "시간")):
                표넓이[i] = 1.5
            elif any(키워드 in 검사내용 for 키워드 in ("주소", "내용", "사항", "세부", "수집항목")):
                표넓이[i] = 4
        표넓이합 = sum(표넓이)
        for i in range(표개수):
            표넓이[i] = 표넓이[i] / 표넓이합 * 전체길이
        self.표만들기(표넓이, [6.5] * 2)
        self.표전체()
        self.셀한줄(1)
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(12)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트("경기천년바탕 Regular")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.표배경색(230, 238, 247)
        self.폰트("경기천년제목 Light")
        self.진하게()
        self.표단일선("하", 6, 8)
        self.캔슬()
        self.표처음()
        for i in range(표개수):
            if i != 0:
                self.표오른쪽(1)
            입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "경기표"
        self.표나가기2()

    def 행안되돌리기(self):
        self.문서처음()
        self.대상.HAction.Run("SelectAll")
        self.대상.HAction.Run("Copy")
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.대상.HAction.Run("Paste")
        for 컨트롤표 in self.컨트롤표목록():
            self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
            self.문장("표:")
            self.대상.HAction.Run("MoveRight")
            self.표전체()
            self.셀엔터변환()
            self.표문장변환()
        self.대상.HAction.Run("SelectAll")
        self.대상.InitScan(1, 255)
        try:
            결과텍스트 = ""
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                if 블록스캔값 not in (2, 3):
                    break
                결과텍스트 += 텍스트
            self.대상.ReleaseScan()
            분할데이터 = 결과텍스트.splitlines() + [""]
            정리데이터 = []
            for 순번, 줄 in enumerate(분할데이터):
                if 줄.startswith("표:◆ ") or 줄.startswith("표: ◆ "):
                    정리데이터.append(줄.replace("표:◆ ", "요약 : ", 1).replace("표: ◆ ", "요약 : ", 1))
                elif 줄.startswith("표:") and re.match(r"표:\d+\s+", 줄):
                    정리데이터.append(re.sub(r"^표:\d+", "소제목:", 줄))
                elif 줄.startswith("표:"):
                    정리데이터.append(줄.replace("표:연간일정:1월:2월:3월:4월:5월:6월:7월:8월:9월:10월:11월:12월", "표:연간일정", 1))
                elif 줄.startswith(("□", "ㅁ")):
                    정리데이터.append(줄.replace("□", "네모: ", 1).replace("ㅁ", "네모: ", 1))
                elif 줄.startswith(("○", "◯")):
                    정리데이터.append(줄.replace("○", "원: ", 1).replace("◯", "원: ", 1))
                elif 줄.startswith("-"):
                    정리데이터.append(줄.replace("-", "바: ", 1))
                elif 줄.startswith("※"):
                    정리데이터.append(줄.replace("※", "당구: ", 1))
                elif 줄.startswith("*"):
                    정리데이터.append(줄.replace("*", "별: ", 1))
                elif 줄.startswith("<") and 줄.endswith(">"):
                    정리데이터.append("설명: " + 줄.replace("<", "").replace(">", ""))
                elif re.match(r"^대면보고\s*/\s*", 줄):
                    정리데이터.append(re.sub(r"\s*/.*?/\s*", "", 줄).strip().replace("대면보고", "대면보고 : ", 1))
                elif re.match(r"^서면보고\s*/\s*", 줄):
                    정리데이터.append(re.sub(r"\s*/.*?/\s*", "", 줄).strip().replace("서면보고", "서면보고 : ", 1))
                elif re.match(r"^\d+\.\s+(.+)", 줄):
                    정리데이터.append(re.sub(r"^\d+\.\s+(.+)", r"소제목 : \1", 줄))
                elif re.match(r"^[가-하]\.", 줄):
                    정리데이터.append(re.sub(r"^[가-하]\.", "가제목:", 줄))
                elif 줄 != "":
                    정리데이터.append("제목 : " + 줄)
                else:
                    정리데이터.append(줄)
            재정리데이터 = []
            for 순번, 줄 in enumerate(정리데이터):
                if 줄.startswith("표:") and 0 < 순번 < len(정리데이터) - 1:
                    if not 정리데이터[순번 - 1].startswith("표:") and not 정리데이터[순번 + 1].startswith("표:"):
                        줄 = 줄.replace("표:", "글상자: ", 1)
                재정리데이터.append(줄)
            결과텍스트 = "\r\n".join(재정리데이터).replace("요약\r\n", "요약 : ")
            self.백스페이스()
            시작지점 = self.현재위치()
            self.기본정렬()
            self.기본글자()
            self.글자크기(10)
            self.폰트("맑은 고딕")
            self.줄간격(150)
            self.문단위(0)
            self.내어쓰기(0)
            self.문장(결과텍스트)
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
            return None
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
            return None
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()
            return None

    def _행안단계배경(self, 내용, 이미지):
        셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
        if 셀위치 in ("A1", "A2"):
            self.사진넣기배경(이미지[5])
        elif 셀위치 in ("B1", "C1", "D1") and len(내용) == 4:
            self.사진넣기배경(이미지[6])
        elif 셀위치 in ("B1", "C1", "D1", "E1") and len(내용) == 5:
            self.사진넣기배경(이미지[12])
        elif 셀위치 == "B2" and len(내용) == 4:
            self.사진넣기배경(이미지[7])
        elif 셀위치 == "B2" and len(내용) == 5:
            self.사진넣기배경(이미지[13])
        elif 셀위치 == "C2" and len(내용) == 4:
            self.사진넣기배경(이미지[8])
        elif 셀위치 in ("C2", "D2") and len(내용) == 5:
            self.사진넣기배경(이미지[14])
        elif 셀위치 == "D2" and len(내용) == 4:
            self.사진넣기배경(이미지[9])
        elif 셀위치 == "E2" and len(내용) == 5:
            self.사진넣기배경(이미지[15])
        elif 셀위치 == "A3":
            self.사진넣기배경(이미지[10])
        elif 셀위치 in ("B3", "C3", "D3") and len(내용) == 4:
            self.사진넣기배경(이미지[11])
        elif 셀위치 in ("B3", "C3", "D3", "E3") and len(내용) == 5:
            self.사진넣기배경(이미지[16])

    def 행안단계(self, 내용, 옵션값, 이미지):
        if self.방금처리 == "행안단계":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            self.표오른쪽(1)
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                if 내용[i] == "-":
                    내용[i] = ""
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 "))
                self.문장(입력내용.replace(";", ":"))
                if 옵션값 != 0:
                    self._행안단계배경(내용, 이미지)
            self.표오른쪽끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = "행안단계"
            self.표나가기2()
            return None

        표개수 = len(내용)
        if 표개수 == 4:
            self.표만들기([16] + [46] * 3, [12, 12, 20])
        elif 표개수 == 5:
            self.표만들기([16] + [33.7] * 4, [12, 12, 20])
        self.표전체()
        if 옵션값 == 1:
            self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.셀여백제로()
        self.글자크기(12)
        self.글자간격(-5)
        self.진하게()
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        if 옵션값 == 0:
            self.표배경색(223, 230, 247)
        self.캔슬()
        self.표처음()
        for i in range(표개수):
            if i != 0:
                self.표오른쪽(1)
            self.문장("\r\n".join(part.strip() for part in 내용[i].split("엔터 ")))
            if 옵션값 != 0:
                self._행안단계배경(내용, 이미지)
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "행안단계"
        self.표나가기2()
        return None

    def 산인공대제목(self, 종류, 상단=0, 하단=0):
        if 종류 == 2:
            self.표만들기([16, 27, 34, 77.5], [0.5, 10, 0.5, 6])
        elif 종류 == 3:
            self.표만들기([38, 77, 1, 38.5], [0.5, 10, 0.5, 6])
        else:
            self.표만들기([205.5 - self.문단여백측정()], [0.5, 10, 0.5, 6])
        self.셀여백제로()
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.글자크기(1)
        self.캔슬()
        self.표처음()

        빈색 = [0, 0, 0, 0]
        def 그라데이션(시작, 끝):
            self.표배경그라데이션("Linear", 90, [시작, 끝] + [빈색] * 8)

        if 종류 == 1:
            self.표배경색(0, 128, 192)
        elif 종류 == 2:
            for 색 in ((231, 238, 242), (194, 217, 228), (115, 187, 222), (0, 128, 192)):
                self.표배경색(*색)
                if 색 != (0, 128, 192):
                    self.표오른쪽(1)
        elif 종류 == 3:
            조합 = (
                ([0, 255, 255, 255], [255, 2, 173, 255]),
                ([0, 2, 173, 255], [255, 45, 98, 156]),
                ([0, 45, 98, 156], [255, 2, 173, 255]),
                ([0, 2, 173, 255], [255, 255, 255, 255]),
            )
            for 순번, (시작, 끝) in enumerate(조합):
                그라데이션(시작, 끝)
                if 순번 < 3:
                    self.표오른쪽(1)
        elif 종류 == 4:
            self.사진넣기배경(상단)
        elif 종류 == 5:
            그라데이션([0, 97, 184, 10], [255, 14, 67, 46])
        elif 종류 == 6:
            self.표배경색(120, 62, 148)

        self.표오른쪽(1)
        if 종류 in (2, 3):
            self.셀선택()
            self.표오른쪽(3)
            self.셀병합()
        self.폰트("HY헤드라인M")
        self.글자크기(20)
        self.가운데정렬()
        self.문장("대제목")
        self.표오른쪽(1)

        if 종류 == 1:
            그라데이션([0, 0, 128, 192], [255, 56, 187, 251])
        elif 종류 == 2:
            self.셀선택()
            self.표오른쪽(3)
            self.셀병합()
            self.표배경색(0, 128, 192)
        elif 종류 == 3:
            조합 = (
                ([0, 255, 255, 255], [255, 2, 173, 255]),
                ([0, 2, 173, 255], [255, 45, 98, 156]),
                ([0, 45, 98, 156], [255, 2, 173, 255]),
                ([0, 2, 173, 255], [255, 255, 255, 255]),
            )
            for 순번, (시작, 끝) in enumerate(조합):
                그라데이션(시작, 끝)
                if 순번 < 3:
                    self.표오른쪽(1)
        elif 종류 == 4:
            self.사진넣기배경(하단)
        elif 종류 == 5:
            그라데이션([255, 14, 67, 46], [0, 97, 184, 10])
        elif 종류 == 6:
            self.표배경색(120, 62, 148)

        self.표오른쪽(1)
        if 종류 in (2, 3):
            self.셀선택()
            self.표오른쪽(3)
            self.셀병합()
        self.폰트("맑은 고딕")
        self.글자크기(12)
        self.오른쪽정렬()
        self.문장("< ")
        self.오늘날짜축약()
        self.문장(", 조직문화TF >")
        self.표나가기2()

    def 경기신보제목2(self, 제목=[], 이미지=""):
        self.표만들기([34, 73, 8, 11, 25], [4, 4.5, 4.5, 4.5, 0.5, 1, 12, 17])
        self.셀여백제로()
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.가운데정렬()
        self.폰트("경기천년제목 Light")
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표아래쪽(3)
        self.셀병합()
        self.사진넣기절대값(이미지[1], 27, 22)
        self.표오른쪽(1)
        self.셀선택()
        self.표아래쪽(3)
        self.셀병합()
        self.글자크기(32)
        self.폰트("경기천년제목 Bold")
        self.문장("업 무 보 고")
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.오늘날짜()
        self.표테두리타입(1, 1, 1, 1)
        self.표오른쪽(3)
        self.셀선택()
        self.표오른쪽(2)
        self.표아래쪽(2)
        self.표테두리타입(1, 1, 1, 1)
        self.표내부선타입(3, 3)
        self.캔슬()
        self.표왼쪽(2)
        self.표위쪽(2)
        for 직급 in ("부 장", "차 장", "대 리"):
            self.문장(직급)
            self.문장오른쪽("ㅇㅇㅇ")
            self.문장오른쪽("000-0000-0000")
            if 직급 != "대 리":
                self.표오른쪽(3)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(4)
        self.셀병합()
        self.글자크기(1)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(4)
        self.셀병합()
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(10, 1, 0, 0)
        self.표테두리단일선색("상", 9, 46, 153)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(4)
        self.셀병합()
        self.표테두리타입(1, 0, 1, 1)
        self.표배경색(255, 255, 229)
        self.가운데정렬()
        self.폰트("경기천년제목 Bold")
        self.진하게()
        self.글자크기(18)
        self.셀여백지정(1, 1, 0, 0)
        self.문장(제목[0] if len(제목) >= 1 else "사업 계획(안)")
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(4)
        self.셀병합()
        self.표테두리타입(0, 1, 1, 1)
        self.표배경색(255, 255, 229)
        self.기본정렬()
        self.폰트("경기천년제목 Medium")
        self.글자크기(14)
        self.내어쓰기(-27.3)
        self.셀여백지정(1, 1, 0, 0)
        if len(제목) >= 2:
            입력내용 = "\r\n".join(" ◈ " + part.strip() for part in 제목[1].split("엔터 "))
            self.문장(입력내용)
        else:
            self.문장("◈ 경기천년제목 Medium 14\r\n◈ 경기천년제목 Medium 14")
        self.표나가기2()

    def 공항서명패생성(self, 이미지=[]):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트]
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        for 순번 in range(1, len(분할리스트)):
            줄 = 분할리스트[순번]
            self.표만들기([70, 70], [21, 49])
            self.표전체()
            self.표테두리색(166, 166, 166)
            self.표내부선색(166, 166, 166)
            self.가운데정렬()
            self.폰트("HY헤드라인M")
            self.표내부선타입(1, 0)
            self.캔슬()
            self.표처음()
            if "공항서비스" in 줄[0]:
                self.사진넣기절대값(이미지[0], 52, 8)
                색 = (244, 229, 178)
                self.표배경색(*색)
                self.표오른쪽()
                self.표배경색(*색)
            else:
                if "전국공항노동조합" in 줄[0]:
                    self.사진넣기절대값(이미지[1], 56, 13)
                elif "공공연대노동조합" in 줄[0]:
                    self.사진넣기절대값(이미지[2], 51, 15)
                else:
                    self.글자크기(25)
                    self.문장(줄[0])
                self.표배경색(217, 217, 217)
                self.표오른쪽()
                self.표배경색(217, 217, 217)
            self.글자크기(25)
            self.문장(줄[1])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.글자크기(100)
            self.문장(줄[2])
            self.표나가기2()

    def 부여명패생성(self, 사진=[], 옵션=0):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트][1:]
        분할리스트 = [데이터 for 데이터 in 분할리스트 for _ in range(2)]
        self.새창()
        self.문서여백(5, 5, 5, 5, 5, 5)
        self.줄간격(140 if 옵션 == 1 else 80)
        for 줄 in 분할리스트:
            self.표만들기([41, 104.5, 41], [28, 41, 1] if 옵션 == 1 else [28, 40, 3])
            self.표전체()
            self.표내부선타입(0, 0)
            if 옵션 == 1:
                self.표테두리타입(11, 11, 11, 11)
                self.표테두리굵기(12, 12, 12, 12)
            self.캔슬()
            self.표처음()
            self.사진넣기절대값(사진[0], 39, 16)
            self.표오른쪽(1)
            self.폰트("HY헤드라인M")
            self.진하게()
            self.배분정렬()
            self.셀한줄(1)
            self.글자크기(35)
            if len(줄[0]) <= 4:
                self.문단여백(50, 50)
            self.문장(줄[0])
            self.표오른쪽(1)
            self.사진넣기절대값(사진[1], 22, 15.5)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.진하게()
            self.글자크기(80)
            self.폰트("HY헤드라인M")
            self.가운데정렬()
            if len(줄[1]) == 3:
                self.문장(줄[1][0] + "  " + 줄[1][1] + "  " + 줄[1][2])
            elif len(줄[2]) == 2:
                self.문장(줄[1][0] + "      " + 줄[1][1])
            else:
                self.문장(줄[1])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            if 옵션 == 0:
                self.표배경색(31, 78, 120)
            self.표나가기2()

    def 홍성명패생성(self, 사진=[]):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트][1:]
        분할리스트 = [데이터 for 데이터 in 분할리스트 for _ in range(2)]
        self.새창()
        self.문서여백(5.1, 5.1, 5, 5, 2, 5)
        self.줄간격(110)
        for 줄 in 분할리스트:
            self.표만들기([31, 126, 31], [26, 52])
            self.표전체()
            self.표테두리굵기(6, 6, 6, 6)
            self.캔슬()
            self.표처음()
            self.사진넣기절대값(사진[2], 32, 21)
            self.표오른쪽(1)
            self.폰트("HY헤드라인M")
            self.표배경색(223, 230, 247)
            self.배분정렬()
            self.셀한줄(1)
            self.글자크기(46)
            self.문단여백(5, 5)
            if len(줄[0]) <= 4:
                self.문단여백(50, 50)
            self.문장(줄[0])
            self.표오른쪽(1)
            self.사진넣기절대값(사진[0], 31, 17)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.폰트("HY헤드라인M")
            self.글자크기(41)
            self.진하게()
            self.문장(줄[1][0] + " " + 줄[1][1] if len(줄[1]) == 2 else 줄[1])
            self.문장(" ")
            self.글자크기(80)
            self.가운데정렬()
            if len(줄[2]) == 3:
                self.문장(줄[2][0] + " " + 줄[2][1] + " " + 줄[2][2])
            elif len(줄[2]) == 2:
                self.문장(줄[2][0] + "    " + 줄[2][1])
            elif len(줄[2]) == 4 and 줄[1] == "":
                self.문장(" ".join(줄[2]))
            else:
                self.문장(줄[2])
            self.표나가기2()

    def 충남시간계획표(self, 내용=["13", "00", "13", "50", "50", "개회", "기획팀장"]):
        내용 = [x.zfill(2) if x.isdigit() else x for x in 내용]
        내용비고 = []
        for 원소 in 내용:
            if 원소 != "" and not re.fullmatch(r"\d{2}", 원소):
                내용비고.append(원소)
            if len(내용비고) == 2:
                break
        시간목록 = []
        for 원소 in 내용:
            if re.fullmatch(r"\d{2}", 원소):
                시간목록.append(원소)
            if len(시간목록) == 4:
                시작 = int(시간목록[0]) * 60 + int(시간목록[1])
                끝 = int(시간목록[2]) * 60 + int(시간목록[3])
                시간목록.append(str(끝 - 시작))
                if int(시간목록[4]) < 0:
                    시간목록[4] = str(끝 - 시작 + 1440)
                break
        시간목록 += [""] * (5 - len(시간목록))
        내용비고 += [""] * (2 - len(내용비고))
        내용 = 시간목록 + 내용비고

        def 시간입력():
            if 내용[0] != "":
                self.문장(내용[0] + ":" + 내용[1])
            if 내용[2] != "":
                self.문장("~")
                self.문장(내용[2] + ":" + 내용[3])

        if self.방금처리 == "충남시간계획표":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            self.표오른쪽(1)
            시간입력()
            self.표테두리단일선("상", 1, 1)
            self.표오른쪽(1)
            self.표테두리단일선("좌", 1, 3)
            self.표테두리단일선("상", 1, 1)
            if 내용[4] != "":
                self.문장(내용[4] + "‘")
            self.셀한줄(1)
            self.표오른쪽(1)
            self.기본정렬()
            self.문장("\r\n".join("▸ " + part.strip() for part in 내용[5].split("엔터 ")))
            self.표테두리단일선("상", 1, 1)
            self.표오른쪽(1)
            self.문장("\r\n".join(part.strip() for part in 내용[6].split("엔터 ")))
            self.표테두리단일선("상", 1, 1)
            self.위치저장 = self.대상.GetPosBySet()
            self.표나가기2()
            return None

        self.표만들기([26, 7, 95, 26], [9.5, 9])
        self.셀여백제로()
        self.표전체()
        self.글자크기(13)
        self.폰트("맑은 고딕")
        self.가운데정렬()
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(6, 6, 1, 1)
        self.표내부선타입(3, 1)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.진하게()
        self.문장("시간계획")
        self.표배경색(249, 237, 237)
        self.표테두리단일선("하", 7, 8)
        self.표오른쪽(1)
        self.진하게()
        self.문장("내 용")
        self.표배경색(249, 237, 237)
        self.표테두리단일선("하", 7, 8)
        self.표오른쪽(1)
        self.진하게()
        self.문장("비 고")
        self.표배경색(249, 237, 237)
        self.표테두리단일선("하", 7, 8)
        self.표오른쪽(1)
        시간입력()
        self.표오른쪽(1)
        self.표테두리단일선("좌", 1, 3)
        self.셀한줄(1)
        if 내용[4] != "":
            self.문장(내용[4] + "‘")
        self.표오른쪽(1)
        self.기본정렬()
        self.문장("\r\n".join("▸ " + part.strip() for part in 내용[5].split("엔터 ")))
        self.표오른쪽(1)
        self.문장("\r\n".join(part.strip() for part in 내용[6].split("엔터 ")))
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "충남시간계획표"
        self.표나가기2()

    def 부여추진일정(self, 내용=["계획수립 엔터 및 통지", "2026년 시책구상 추진계획 수립 및 통보 엔터 중점방향, 세부계획 등 수립 및 전 부서 알림", "~ 7. 25.(금)"]):
        if isinstance(내용, str):
            내용 = re.split(r"\r?\n", 내용)
        elif 내용 is None:
            내용 = []
        else:
            try:
                내용 = list(내용)
            except TypeError:
                내용 = [str(내용)]
        내용 = [str(값) for 값 in 내용[:3]]
        내용 += [""] * (3 - len(내용))

        def 구분텍스트():
            return "\r\n".join(part.strip() for part in 내용[0].split("엔터 "))

        def 내용텍스트():
            부분들 = [부분.strip() for 부분 in 내용[1].split("엔터 ")]
            입력내용 = "▸" + 부분들[0]
            if len(부분들) >= 2:
                입력내용 += "\r\n" + "\r\n".join("  - " + part for part in 부분들[1:])
            return 입력내용

        def 일정텍스트():
            return "\r\n".join(part.strip() for part in 내용[2].split("엔터 "))

        if self.방금처리 == "부여추진일정":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            self.표오른쪽(1)
            self.표오른쪽끝()
            self.표오른쪽(1)
            self.문장(구분텍스트())
            self.표오른쪽(2)
            self.기본정렬()
            self.문장(내용텍스트())
            self.표오른쪽(2)
            self.문장(일정텍스트())
            self.위치저장 = self.대상.GetPosBySet()
            self.표위쪽(1)
            self.셀선택()
            self.표왼쪽끝()
            self.표배경색(255, 255, 255)
            self.표테두리단일선("좌", 1, 0)
            self.표테두리단일선("우", 1, 0)
            self.표내부선타입(0, 0)
            self.캔슬()
            self.글자색(0, 0, 0)
            self.문장("⇓")
            self.표나가기2()
            return None

        self.오른쪽정렬()
        self.표만들기([20, 1, 110, 1, 22], [5, 1, 5])
        self.셀여백제로()
        self.표전체()
        self.글자크기(12)
        self.가운데정렬()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.표테두리굵기(5, 5, 5, 5)
        self.표내부선굵기(5, 5)
        self.진하게()
        self.폰트("맑은 고딕")
        self.줄간격(140)
        self.캔슬()
        self.표처음()
        for 제목, 이동 in (("구  분", 2), ("내   용", 1), ("일 정", 1)):
            self.표테두리색(0, 102, 255)
            self.표테두리타입(1, 1, 1, 1)
            self.표배경색(223, 230, 247)
            self.문장(제목)
            self.표오른쪽(이동)
            if 제목 == "내   용":
                self.표너비줄이기(3)
                self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽끝()
        self.글자크기(8)
        self.캔슬()
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽끝()
        self.셀여백지정(1, 1, 0, 0)
        self.캔슬()
        self.표왼쪽끝()
        self.표테두리색(0, 102, 255)
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(32, 58, 123)
        self.글자색(255, 255, 255)
        self.문장(구분텍스트())
        self.표오른쪽(2)
        self.표테두리색(0, 102, 255)
        self.표테두리타입(1, 1, 1, 1)
        self.기본정렬()
        self.문장(내용텍스트())
        self.표오른쪽(2)
        self.표테두리색(0, 102, 255)
        self.표테두리타입(1, 1, 1, 1)
        self.문장(일정텍스트())
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "부여추진일정"
        self.표나가기2()

    def 충남명패생성(self, 사진=[], 사이즈="0"):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트][1:]
        분할리스트 = [데이터 for 데이터 in 분할리스트 for _ in range(2)]
        self.새창()
        self.문서여백(7.1, 7.1, 5, 5, 2, 5)
        self.줄간격(110)
        for 줄 in 분할리스트:
            if 사이즈 == "0":
                self.표만들기([30, 124, 30], [23, 37, 2])
            elif 사이즈 == "80":
                self.표만들기([30, 124, 30], [28, 45.5, 3])
            self.표전체()
            self.표내부선타입(0, 0)
            self.표테두리타입(8, 8, 8, 8)
            self.표테두리굵기(6, 6, 6, 6)
            self.캔슬()
            self.표처음()
            self.사진넣기절대값(사진[0], 30, 16)
            self.표오른쪽(1)
            self.폰트("HY헤드라인M")
            self.진하게()
            self.배분정렬()
            self.셀한줄(1)
            self.글자크기(46)
            if len(줄[0]) <= 4:
                self.문단여백(50, 50)
            self.문장(줄[0])
            self.표오른쪽(1)
            self.사진넣기절대값(사진[1], 22, 15.5)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.진하게()
            self.글자크기(80)
            self.폰트("HY헤드라인M")
            self.가운데정렬()
            if len(줄[2]) == 3:
                self.문장(" ".join(줄[2]))
            elif len(줄[2]) == 2:
                self.문장(줄[2][0] + "    " + 줄[2][1])
            else:
                self.문장(줄[2])
            self.글자크기(41)
            self.글자장평(80)
            self.문장(" ")
            self.문장(줄[1][0] + " " + 줄[1][1] if len(줄[1]) == 2 else 줄[1])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.표배경그라데이션2("Linear", 90, [[255, 255, 102, 0], [0, 255, 0, 0]])
            self.표나가기2()

    def 충남미니명패생성(self, 사진=[]):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트][1:]
        분할리스트 = [데이터 for 데이터 in 분할리스트 for _ in range(2)]
        self.새창()
        self.문서여백(15, 15, 10, 10, 5, 5)
        self.줄간격(100)
        for 줄 in 분할리스트:
            self.표만들기([17, 46, 15], [13, 31, 1])
            self.표전체()
            self.글자크기(9)
            self.표내부선타입(0, 0)
            self.표테두리타입(8, 8, 8, 8)
            self.표테두리굵기(6, 6, 6, 6)
            self.캔슬()
            self.표처음()
            self.사진넣기절대값(사진[0], 17, 9)
            self.표오른쪽(1)
            self.폰트("HY헤드라인M")
            self.진하게()
            self.배분정렬()
            self.셀한줄(1)
            self.글자크기(15)
            if len(줄[0]) <= 4:
                self.문단여백(10, 10)
            self.문장(줄[0])
            self.표오른쪽(1)
            self.사진넣기절대값(사진[1], 13, 8)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.진하게()
            self.글자크기(40)
            self.폰트("HY헤드라인M")
            self.가운데정렬()
            if len(줄[2]) == 3:
                self.문장(" ".join(줄[2]))
            elif len(줄[2]) == 2:
                self.문장(줄[2][0] + "    " + 줄[2][1])
            else:
                self.문장(줄[2])
            self.글자크기(15)
            self.글자장평(80)
            self.문장(" ")
            self.문장(줄[1][0] + " " + 줄[1][1] if len(줄[1]) == 2 else 줄[1])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.표배경그라데이션2("Linear", 90, [[255, 255, 102, 0], [0, 255, 0, 0]])
            self.표나가기0()
            self.백스페이스()
            self.대상.HAction.Run("MoveLineEnd")

    def 충남의회미니명패(self, 사진=[]):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트][1:]
        self.새창()
        self.문서여백(10, 10, 4, 4, 4, 4)
        self.줄간격(100)
        self.가운데정렬()
        for 줄 in 분할리스트:
            self.표만들기([12, 69], [2.4, 14, 27, 3.5])
            self.표전체()
            self.글자크기(1)
            self.표내부선타입(0, 0)
            self.표테두리굵기(6, 6, 6, 6)
            self.캔슬()
            self.표처음()
            self.표오른쪽(2)
            self.사진넣기절대값(사진[0], 12, 12)
            self.오른쪽정렬()
            self.표오른쪽(1)
            self.폰트("HY헤드라인M")
            self.글자간격(-16)
            self.글자장평(77)
            self.배분정렬()
            self.셀한줄(1)
            self.글자크기(28)
            self.문단여백(5, 10)
            self.문장(줄[0])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.글자크기(43)
            self.문단여백(2, 2)
            self.배분정렬()
            self.폰트("HY헤드라인M")
            if len(줄[2]) == 3:
                self.문장(" ".join(줄[2]))
            elif len(줄[2]) == 2:
                self.문장(줄[2][0] + "    " + 줄[2][1])
            else:
                self.문장(줄[2])
            self.글자크기(15)
            self.진하게()
            self.문장(" " + 줄[1])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.사진넣기배경(사진[1])
            self.표나가기0()
            self.백스페이스()
            self.대상.HAction.Run("MoveLineEnd")

    def _충남의회대형명패(self, 사진, 너비, 이름크기, 여백):
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        데이터리스트 = []
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄[1:4] for 줄 in 분할리스트 if 줄[1].strip() != ""][1:]
        self.새창()
        self.문서여백(3.5, 3.6, 4, 4, 4, 4)
        self.줄간격(85)
        self.가운데정렬()
        for 순번, 줄 in enumerate(분할리스트):
            첫쪽 = 순번 == 0
            self.표만들기([24 if 첫쪽 else 20, 너비[0] if 첫쪽 else 너비[1]], [19, 42, 5])
            self.표전체()
            if 첫쪽:
                self.표내부선타입(0, 0)
            self.표테두리굵기(7, 7, 7, 7)
            self.캔슬()
            self.표처음()
            self.사진넣기절대값(사진[0], 20 if 첫쪽 else 17, 20 if 첫쪽 else 17)
            self.오른쪽정렬()
            self.표오른쪽(1)
            self.폰트("HY헤드라인M")
            self.글자간격(-20)
            self.글자장평(90)
            self.진하게()
            self.글자색(28, 61, 98)
            self.배분정렬()
            self.셀한줄(1)
            self.글자크기(44)
            self.문단여백(여백, 여백)
            if "위원회" in 줄[0] and "위원장" in 줄[1]:
                self.문장(줄[0].replace("위원회", "위원장"))
            else:
                self.문장(줄[0] + " " + 줄[1])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.진하게()
            self.글자크기(이름크기)
            self.문단여백(20, 20)
            self.배분정렬()
            self.폰트("HY헤드라인M")
            if len(줄[2]) == 3:
                self.문장(" ".join(줄[2]))
            elif len(줄[2]) == 2:
                self.문장(줄[2][0] + "    " + 줄[2][1])
            else:
                self.문장(줄[2])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.사진넣기배경(사진[1])
            self.표나가기2()
            if 첫쪽:
                self.페이지엔터()
        return None

    def 충남의회명패200(self, 사진):
        return self._충남의회대형명패(사진, (164, 168), 104, 30)

    def 충남의회명패170(self, 사진):
        return self._충남의회대형명패(사진, (136, 137), 100, 20)

    def 충남제목2개큰명찰(self, 사진=[]):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:3] for 줄 in 분할리스트][1:]
        self.문서처음()
        self.대상.MovePos(6)
        self.대상.HAction.Run("Select")
        self.대상.MovePos(7)
        임시텍스트 = self.블록스캔()[1]
        self.캔슬()
        임시첫번째 = 임시텍스트.strip().split()[0]
        임시두번째 = 임시텍스트.strip().split()[1]
        self.새창()
        self.문서여백(8, 8, 10, 10, 10, 10)
        self.줄간격(160)
        for 줄 in 분할리스트:
            self.표만들기([22.5, 65.5], [31, 19, 6, 20, 29, 7])
            self.셀여백제로()
            self.표전체()
            self.표내부선타입(0, 0)
            self.표테두리굵기(8, 8, 8, 8)
            self.가운데정렬()
            self.폰트("HY헤드라인M")
            self.셀한줄()
            self.캔슬()
            self.표처음()
            self.사진넣기절대값(사진[12], 26, 27)
            self.표오른쪽(1)
            self.글자장평(80)
            self.글자크기(40)
            if len(임시첫번째) > 6:
                self.글자크기(35)
            if len(임시첫번째) > 7:
                self.글자크기(32)
            self.문장(임시첫번째)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.글자크기(32)
            self.진하게()
            self.글자색(0, 0, 255)
            self.문장(임시두번째)
            self.표오른쪽(3)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.글자크기(48)
            self.진하게()
            self.문장(줄[0])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.글자크기(68)
            self.진하게()
            self.배분정렬()
            self.문단여백(5, 5)
            self.문장(줄[1])
            self.표나가기0()
            self.백스페이스()
            self.대상.HAction.Run("MoveLineEnd")

    def 충남제목2개작은명찰(self, 사진=[]):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.캔슬()
        self.표전체()
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i))
            결과텍스트 = ""
            self.대상.InitScan(0, 85)
            while True:
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                결과텍스트 += 텍스트
                if 블록스캔값 in (0, 1):
                    break
            데이터리스트.append(결과텍스트.strip())
            self.대상.ReleaseScan()
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if 줄[1].strip() != ""]
        분할리스트 = [줄[1:3] for 줄 in 분할리스트][1:]
        self.문서처음()
        self.대상.MovePos(6)
        self.대상.HAction.Run("Select")
        self.대상.MovePos(7)
        임시텍스트 = self.블록스캔()[1]
        self.캔슬()
        임시첫번째, 임시두번째 = 임시텍스트.strip().split()[:2]
        self.새창()
        self.문서여백(6, 6, 10, 10, 0, 0)
        self.줄간격(100)
        for 줄 in 분할리스트:
            self.표만들기([22, 20, 45], [15.5, 10, 19.5, 14])
            self.셀여백제로()
            self.표전체()
            self.표내부선타입(0, 0)
            self.표테두리굵기(8, 8, 8, 8)
            self.가운데정렬()
            self.폰트("HY울릉도M")
            self.셀한줄()
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.표배경색(242, 229, 255)
            self.글자크기(20)
            self.셀여백지정(1, 1, 3, 1)
            self.진하게()
            self.문장(임시첫번째)
            self.표오른쪽(1)
            self.표배경색(242, 229, 255)
            self.글자크기(20)
            self.진하게()
            self.문장(임시두번째)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.글자크기(22)
            self.글자색(0, 0, 255)
            self.폰트("배달의민족 도현")
            self.배분정렬()
            직함길이 = len(줄[0])
            if 직함길이 == 1:
                self.가운데정렬()
            elif 직함길이 == 2:
                self.문단여백(110, 110)
            elif 직함길이 == 3:
                self.문단여백(90, 90)
            elif 직함길이 == 4:
                self.문단여백(70, 70)
            elif 직함길이 == 5:
                self.문단여백(60, 60)
            elif 직함길이 >= 7:
                self.문단여백(20, 20)
            self.문장(줄[0])
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(2)
            self.셀병합()
            self.진하게()
            self.글자크기(50)
            self.배분정렬()
            self.폰트("배달의민족 주아")
            self.배분정렬()
            이름길이 = len(줄[1])
            if 이름길이 == 1:
                self.가운데정렬()
            elif 이름길이 == 2:
                self.문단여백(60, 60)
            elif 이름길이 == 3:
                self.문단여백(50, 50)
            elif 이름길이 == 4:
                self.문단여백(30, 30)
            elif 이름길이 >= 5:
                self.문단여백(10, 10)
            self.문장(줄[1])
            self.표오른쪽(1)
            self.사진넣기절대값(사진[1], 15, 10)
            self.오른쪽정렬()
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.기본정렬()
            self.글자크기(18)
            self.진하게()
            self.문장(" 충청남도농업기술원")
            self.표나가기0()
            self.백스페이스()
            self.대상.HAction.Run("MoveLineEnd")

    def 충남단축키(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.충남중제목("단축키 모음")
        self.표만들기([125, 35], [220])
        self.표테두리타입(0, 0, 0, 0)
        self.셀여백제로()
        self.표만들기([60, 60], [5, 95, 5, 27, 5, 23, 5, 23])
        self.표전체()
        self.폰트("맑은 고딕")
        self.글자크기(10)
        self.줄간격(140)
        self.진하게()
        self.캔슬()
        self.표처음()
        self.글자크기(12)
        self.문장("<한글 단축키>")
        self.표테두리타입(0, 1, 0, 0)
        self.표오른쪽(1)
        self.표테두리타입(0, 1, 0, 0)
        self.표오른쪽(1)
        self.문장("Alt+C : 모양복사\r\nCtrl+O : 끼워 넣기\r\nCtrl+Shift+L/C/R : 정렬\r\nAlt+G : 페이지 찾아가기\r\nShift+Tab : 줄맞추기\r\nCtrl+Shift+Tab : 표안에서 줄맞추기\r\nAlt+L / Alt+T : 글자모양, 문단모양\r\nShift+Alt+N/W : 자간 좁게/넓게\r\nShift+Alt+A/Z : 줄간격 좁게/넓게\r\nCtrl+Enter : 강제 쪽나누기\r\n표안에서 Ctrl+Enter : 한줄 추가\r\nCtrl+C : 복사\r\nCtrl+V : 붙여넣기\r\nCtrl+X : 잘라내기\r\n표안에서 : M(합치기), S(나누기)\r\n           L(선모양), C(셀모양)\r\nCtrl+N, K : 개체속성\r\nCtrl+F7 : 왼쪽, 오른쪽 여백 증가\r\nCtrl+F8 : 왼쪽, 오른쪽 여백 감소")
        self.표오른쪽(1)
        self.문장("Alt+N : 새창\r\nF9 : 한자\r\nCtrl+F : 찾기\r\nCtrf+F2 : 찾아 바꾸기\r\nF7 : 여백보기\r\nF8 : 맞춤법\r\nCtrl+G+C : 조판부호\r\nShift+Alt+J : 장평 좁게\r\nShift+Alt+K : 장평 넓게\r\nShift+Alt+B 또는 Ctrl+B : 진하게\r\nShift+Alt+I 또는 Ctrl+I : 이탤릭\r\nShift+Alt+U 또는 Ctrl+U : 밑줄\r\nCtrl+N, T : 표 만들기\r\nCtrl+N, I : 그림 넣기\r\nShift+F10 : 메뉴(마우스 오른쪽)")
        self.표오른쪽(1)
        self.글자크기(12)
        self.문장("\r\n<엑셀 단축키>")
        self.표테두리타입(1, 1, 0, 0)
        self.표오른쪽(1)
        self.표테두리타입(1, 1, 0, 0)
        self.표오른쪽(1)
        self.문장("Ctrl+1 : 셀 서식\r\nF4 : 반복작업\r\n엔터효과 함수 : Char(10)\r\nCtrl+~ : 수식확인\r\nAlt+Enter : 셀안에서 엔터")
        self.표오른쪽(1)
        self.문장("Ctrl+PageUP : 앞 시트 이동\r\nCtrl+PageDown : 뒤 시트 이동\r\nF12 : 다른 이름으로 저장\r\nCtrl+마우스 휠 : 화면크기 조정\r\nCtrl+(Shift)+방향키 : 이동(범위지정)")
        self.표오른쪽(1)
        self.글자크기(12)
        self.문장("\r\n<윈도우 단축키>")
        self.표테두리타입(1, 1, 0, 0)
        self.표오른쪽(1)
        self.표테두리타입(1, 1, 0, 0)
        self.표오른쪽(1)
        self.문장("윈도우키+E : 탐색기\r\n윈도우키+F : 찾기\r\n윈도우키+D : 바탕화면\r\n윈도우키+Shift+S : 화면캡쳐")
        self.표오른쪽(1)
        self.문장("윈도우키+M : 화면내리기\r\n윈도우키+↑ : 창 최대화\r\n윈도우키+↓ : 창 최소화\r\n윈도우키+←→ : 창 좌우 배치")
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.글자크기(12)
        self.문장("\r\n<파일첨부 쉽게하기>")
        self.표테두리타입(1, 1, 0, 0)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장("한글 : 한글파일 상단에서 오른쪽 클릭 후 ‘파일 경로 및 이름 복사’\r\n엑셀 : 엑셀 - 파일 - 정보 - 파일경로 복사\r\n윈도우 : 파일 선택 후 Shift 누른채로 마우스 오른쪽 클릭 후\r\n        ‘경로로 복사 선택’")
        self.표나가기2()

    def 지문(self, 종류):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
        결과텍스트 = ""
        체크 = 0
        try:
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                체크 = 1
            self.대상.ReleaseScan()
            self.대상.HAction.Run("Delete")
            결과텍스트 = 결과텍스트.strip()
            self.블록첫위치()
            if 체크 == 1:
                if 종류 in ("영어지문", "국어지문"):
                    self.표만들기([102], [5])
                    if 종류 == "영어지문":
                        self.표테두리타입(0, 0, 0, 0)
                        self.표내부선타입(0, 0)
                    self.셀여백지정(2.5, 3.5, 2.5, 2.5)
                self.문장("  " + 결과텍스트)
        except ValueError as e:
            print(f"값 오류 : {e}")
            self.대상.ReleaseScan()
            체크 = 0
        except Exception as e:
            print(f"오류 발생 : {e}")
            self.대상.ReleaseScan()
            체크 = 0
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")
        if 체크 != 1:
            return None
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        if 종류 == "영어지문":
            self.자간헌터(0)
            self.글자간격(-5)
            self.줄간격(140)
            self.글자장평(100)
            self.글자음영(0xFFFFFFFF)
            self.문단여백(0, 0)
            self.타임즈뉴로만()
            self.글자크기(11)
            self.글자위치(-10)
            self.대상.HAction.Run("CharShapeNormal")
        elif 종류 == "국어지문":
            self.자간헌터(0)
            self.글자간격(-5)
            self.줄간격(150)
            self.글자장평(92)
            self.글자음영(0xFFFFFFFF)
            self.문단여백(0, 0)
            self.신명중명조()
            self.글자크기(11)
            self.글자위치(-10)
            self.대상.HAction.Run("CharShapeNormal")
        self.대상.HAction.Run("Cancel")
        self.대상.HAction.Run("MoveListEnd")
        self.대상.HAction.Run("MoveRight")
        self.대상.HAction.Run("BreakPara")

    def 행안JSON변환(self):
        self.문서처음()
        self.대상.HAction.Run("SelectAll")
        self.대상.HAction.Run("Copy")
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.대상.HAction.Run("Paste")
        self.대상.HAction.Run("SelectAll")
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            결과텍스트 = ""
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔값, 텍스트 = self.대상.GetText()
            self.대상.ReleaseScan()
            결과텍스트 = 결과텍스트.strip().lstrip("{").rstrip("}")
            임시패턴 = r',(?=(?:[^"]*"[^"]*")*[^"]*$)'
            분할데이터 = [줄.strip() for 줄 in re.split(임시패턴, 결과텍스트)]
            print(분할데이터)
            정리데이터 = []
            for 순번, 줄 in enumerate(분할데이터):
                if ":" not in 줄:
                    continue
                왼쪽, 오른쪽 = 줄.split(":", 1)
                왼쪽 = 왼쪽.strip().strip('"')
                오른쪽 = 오른쪽.strip().strip('"')
                정리데이터.append(왼쪽 + ":" + 오른쪽)
            결과텍스트 = "\r\n".join(정리데이터)
            self.백스페이스()
            시작지점 = self.현재위치()
            self.기본정렬()
            self.기본글자()
            self.글자크기(10)
            self.폰트("맑은 고딕")
            self.줄간격(150)
            self.문단위(0)
            self.내어쓰기(0)
            self.문장(결과텍스트)
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()

    def 행안연간일정(self, 내용=[], 옵션값=0):
        if isinstance(내용, str):
            내용 = re.split(r"\r?\n", 내용)
        elif 내용 is None:
            내용 = []
        else:
            try:
                내용 = list(내용)
            except TypeError:
                내용 = [str(내용)]
        # 원본 표는 13개 열을 전제로 하므로 부족한 선택값은 빈 셀로 채운다.
        내용 = [str(값) for 값 in 내용[:13]]
        내용.extend([""] * (13 - len(내용)))
        if self.방금처리 == "행안연간일정":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A1":
                self.표아래쪽(1)
            else:
                self.표오른쪽(1)
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                if 내용[i] == "-":
                    내용[i] = ""
                if 옵션값 != 0 and i != 0:
                    if 내용[i] != "":
                        self.글자색(128, 128, 128)
                        self.표배경색(166, 166, 166)
                    else:
                        self.글자색(0, 0, 0)
                        self.표배경색(255, 255, 255)
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 "))
                self.문장(입력내용.replace(";", ":"))
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = "행안연간일정"
            self.표나가기2()
            return None

        표개수 = len(내용)
        self.표만들기([38] + [7] * 12, [7, 8])
        self.표전체()
        self.셀여백제로()
        self.글자크기(12)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.표배경색(223, 230, 247)
        self.캔슬()
        self.표처음()
        for i in range(13):
            if i != 0:
                self.표오른쪽(1)
            입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 "))
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "행안연간일정"
        self.표나가기2()

    def 충남블록변환범위(self, 내용=[], 종류="바꾸기"):
        def 비교(a, b):
            return a > b

        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        문장내용 = self.블록문장스캔()
        if 시작지점.Item("Para") is None:
            return None
        self.캔슬()
        self.대상.SetPosBySet(끝지점)
        위치 = self.대상.GetPosBySet()
        마지막 = (위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos"))

        if 종류 == "바꾸기":
            for i in range(3):
                보정값 = 0
                while True:
                    self.대상.SetPosBySet(시작지점)
                    위치 = self.대상.GetPosBySet()
                    지금 = (위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos"))
                    if not 비교(마지막, 지금):
                        break
                    방금 = 지금
                    self.정규표현식(내용[2 * i])
                    if 지금[1] == 마지막[1] and 지금[0] == 마지막[0]:
                        보정값 = len(내용[2 * i]) - len(내용[2 * i + 1])
                    위치 = self.대상.GetPosBySet()
                    지금 = (위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos"))
                    if 비교(지금, 마지막) or 지금 == 방금:
                        break
                    self.문장(내용[2 * i + 1])
                    if 지금[1] == 마지막[1] and 지금[0] == 마지막[0]:
                        마지막 = (마지막[0], 마지막[1], 마지막[2] - 보정값)
                    if not 비교(마지막, 지금):
                        break
        elif 종류 == "공백정리":
            매치 = re.findall(r" {2,}", 문장내용)
            self.대상.SetPosBySet(시작지점)
            for i in range(len(매치) + 1):
                self.정규표현식바꾸기(r"\b+\b+", " ")
            self.캔슬()
            self.대상.SetPosBySet(시작지점)

    def 점수분배(self):
        점수리스트 = []
        try:
            정상, 처음위치, 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열 = self.셀정보()
            if 정상 == 1:
                블록리스트 = self.블록리스트생성(행, 열, 한줄, 처음위치)
                for i in range(len(블록리스트)):
                    self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                    self.대상.HAction.Run("Select")
                    self.대상.HAction.Run("Select")
                    self.대상.HAction.Run("Select")
                    try:
                        self.대상.InitScan(1, 255)
                        텍스트 = self.대상.GetText()[1]
                        숫자만 = re.sub(r"[^0-9.]", "", 텍스트)
                        if 숫자만 != "":
                            점수리스트.append(숫자만)
                        self.대상.ReleaseScan()
                    except ValueError as 오류:
                        print(f"값 오류 : {오류}")
                        self.대상.ReleaseScan()
                    except Exception as 오류:
                        print(f"오류 발생 : {오류}")
                        self.대상.ReleaseScan()
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

        self.표탈출()
        좌표리스트 = self.글자좌표리스트(r"\[[^\[^점\]]*점\]")
        if len(좌표리스트) == len(점수리스트):
            for i in range(len(좌표리스트) - 1, -1, -1):
                시작, 종료, _ = 좌표리스트[i]
                self.대상.SetPosBySet(self.좌표(시작.Item("List"), 시작.Item("Para"), 시작.Item("Pos") + 1))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(종료.Item("List"), 종료.Item("Para"), 종료.Item("Pos") - 2))
                self.문장(점수리스트[i])
                self.대상.HAction.Run("Cancel")

    def 부여시간계획(self, 내용):
        내용 = [값.zfill(2) if 값.isdigit() else 값 for 값 in 내용]
        내용비고 = []
        for 원소 in 내용:
            if 원소 != "" and not re.fullmatch(r"\d{2}", 원소):
                내용비고.append(원소)
            if len(내용비고) == 2:
                break

        시간목록 = []
        for 원소 in 내용:
            if re.fullmatch(r"\d{2}", 원소):
                시간목록.append(원소)
            if len(시간목록) == 4:
                시작 = int(시간목록[0]) * 60 + int(시간목록[1])
                끝 = int(시간목록[2]) * 60 + int(시간목록[3])
                시간목록.append(str(끝 - 시작))
                if int(시간목록[4]) < 0:
                    시간목록[4] = str(끝 - 시작 + 1440)
                break
        시간목록 += [""] * (5 - len(시간목록))
        내용비고 += [""] * (2 - len(내용비고))
        내용 = 시간목록 + 내용비고

        if self.방금처리 == "부여시간계획":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            self.표오른쪽(1)
            if 내용[0] != "":
                self.문장(내용[0] + ":" + 내용[1])
            self.표오른쪽(1)
            if 내용[2] != "":
                self.문장(내용[2] + ":" + 내용[3])
            self.표오른쪽(1)
            self.문장(내용[4])
            self.표오른쪽(1)
            self.기본정렬()
            self.문장("\r\n".join(" ◦ " + part.strip() for part in 내용[5].split("엔터 ")))
            self.표오른쪽(1)
            self.문장("\r\n".join(part.strip() for part in 내용[6].split("엔터 ")))
            self.위치저장 = self.대상.GetPosBySet()
            self.표나가기2()
            return None

        self.오른쪽정렬()
        self.표만들기([17, 17, 17, 64, 35], [4.5, 5, 1, 6])
        self.셀여백제로()
        self.표전체()
        self.글자크기(12)
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.문장("시간")
        self.표오른쪽(1)
        self.셀선택()
        self.표아래쪽(1)
        self.셀병합()
        self.문장("내용")
        self.표오른쪽(1)
        self.셀선택()
        self.표아래쪽(1)
        self.셀병합()
        self.문장("비고")
        self.표오른쪽(1)
        self.문장("부터")
        self.표오른쪽(1)
        self.문장("까지")
        self.표오른쪽(1)
        self.문장("소요(분)")
        self.표처음()
        self.셀선택()
        self.표아래쪽(1)
        self.표오른쪽(2)
        self.표테두리색(0, 0, 255)
        self.표내부선색(0, 0, 255)
        self.표배경색(223, 230, 247)
        self.진하게()
        self.캔슬()
        self.표처음()
        self.표아래쪽(2)
        self.셀선택()
        self.표오른쪽끝()
        self.표테두리타입(1, 1, 0, 0)
        self.표내부선타입(1, 0)
        self.글자크기(1)
        self.캔슬()
        self.표왼쪽끝()
        self.표아래쪽(1)
        self.셀선택()
        self.표오른쪽끝()
        self.표테두리색(48, 87, 185)
        self.표내부선색(48, 87, 185)
        self.글자크기(13)
        self.줄간격(110)
        self.셀여백지정(1, 1, 0, 0)
        self.캔슬()
        self.표왼쪽끝()
        if 내용[0] != "":
            self.문장(내용[0] + ":" + 내용[1])
        self.표오른쪽(1)
        if 내용[2] != "":
            self.문장(내용[2] + ":" + 내용[3])
        self.표오른쪽(1)
        self.문장(내용[4])
        self.표오른쪽(1)
        self.기본정렬()
        self.문장("\r\n".join(" ◦ " + part.strip() for part in 내용[5].split("엔터 ")))
        self.표오른쪽(1)
        self.문장("\r\n".join(part.strip() for part in 내용[6].split("엔터 ")))
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "부여시간계획"
        self.표나가기2()
        return None

    def 부여한줄일정(self, 내용=["계획수립‧통지", "‘26. 7. 25.限", "시책발굴", "‘26. 8. 26.限", "정책자문", "‘26. 9. 5.限", "토론회 개최", "‘26. 9. 15.限", "군정반영", "‘26. 9.~12.限"]):
        def 리스트정규화(리스트):
            if len(리스트) > 10:
                return 리스트[:10]
            for 타겟 in [4, 6, 8, 10]:
                if len(리스트) <= 타겟:
                    return 리스트 + ["입력"] * (타겟 - len(리스트))
            return 리스트

        내용 = [원소.strip() for 원소 in 리스트정규화(내용)]
        개수 = int(len(내용) / 2)
        if 개수 == 5:
            폭 = 25
        elif 개수 == 4:
            폭 = 35
        elif 개수 == 3:
            폭 = 50
        elif 개수 == 2:
            폭 = 70
        self.가운데정렬()
        self.표만들기([폭, 3] * (개수 - 1) + [폭], [8, 0.4, 9])
        self.셀여백제로()
        self.표전체()
        self.글자크기(12)
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.캔슬()
        self.표처음()
        for i in range(개수 - 1):
            self.표오른쪽(1)
            self.셀선택()
            self.표아래쪽(2)
            self.셀병합()
            self.표테두리타입(0, 0, 0, 0)
            self.글자색(51, 51, 153)
            self.문장("➡")
            self.표오른쪽(1)
        for i in range(개수):
            self.표처음()
            self.표오른쪽(i * 2)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리색(0, 0, 255)
            self.표배경색(223, 230, 247)
            self.진하게()
            self.문장(내용[i * 2])
            self.표아래쪽(1)
            self.글자크기(1)
            self.표테두리타입(1, 1, 0, 0)
            self.표아래쪽(1)
            self.표테두리색(48, 87, 185)
            self.표테두리타입(1, 1, 1, 1)
            if i == 개수 - 1:
                self.문장(내용[i * 2 + 1] + "\u200b")
            else:
                self.문장(내용[i * 2 + 1])
        self.표나가기2()

    def 행안JSON질문(self):
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            결과텍스트 = ""
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔값, 텍스트 = self.대상.GetText()
            self.대상.ReleaseScan()
            분할데이터 = [줄.strip() for 줄 in 결과텍스트.splitlines()]
            정리데이터 = []
            for 순번, 줄 in enumerate(분할데이터):
                if ":" in 줄:
                    왼쪽, 오른쪽 = 줄.split(":", 1)
                    정리데이터.append('"' + 왼쪽.strip() + '" : "' + 오른쪽.strip() + '"')
                else:
                    정리데이터.append('"엔터" : "엔터"')
            결과텍스트 = ",\r\n".join(정리데이터)
            self.문장("{" + 결과텍스트 + '} key값이 "표"면 "value"값을 그대로 두세요. JSON 구조는 유지하며, 내용만 간략하게 2줄 이내 개조식으로 바꿔주세요, 리스트로 합치지 마세요. JSON구조는 꼭 유지하고, value만 간략하게 2줄이내 개조식으로, key 버리지마세요')
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()

    def 행안부단일추출(self):
        self.상단캡션()
        self.리스트시작()
        self.대상.MovePos(6)
        self.대상.HAction.Run("Select")
        self.대상.MovePos(7)
        텍스트 = self.블록스캔()[1]
        self.캔슬()
        self.리스트끝()
        self.대상.HAction.Run("MoveDown")
        세부사업명 = 텍스트.replace("□ 비목별 검토내역", "").replace(":", "").strip()
        분할리스트 = self._선택표행추출(9)
        if not 분할리스트:
            return None
        정리데이터 = self._행안부정리데이터(세부사업명, 분할리스트)
        임시엑셀 = self._행안부엑셀시작()
        새워크북 = 임시엑셀.엑셀.Workbooks.Add()
        for _ in range(1):
            새워크북.Sheets.Add()
        새워크북.Sheets(1).Name = "정리"
        정리 = 새워크북.Sheets("정리")
        정리.Cells(임시엑셀.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        for 열, 값 in enumerate(["세부사업명", "내역사업명", "비목", "25년 집행액", "26년 예산", "27년 요구값"], start=1):
            정리.Cells(1, 열).Value = 값
        for 행, 줄 in enumerate(정리데이터, start=2):
            for 열, 값 in enumerate(줄, start=1):
                정리.Cells(행, 열).Value = 값
        return None

    def 행안부전체추출(self):
        임시엑셀 = self._행안부엑셀시작()
        새워크북 = 임시엑셀.엑셀.Workbooks.Add()
        새워크북.Sheets(1).Name = "정리"
        정리 = 새워크북.Sheets("정리")
        제목 = ["세부사업명", "내역사업명", "비목", "25년 집행액", "26년 예산", "27년 요구값", "27년 검토", "추가요구", "검토 한도내", "검토 한도외", "최종 한도내"]
        for 열, 값 in enumerate(제목, start=1):
            정리.Cells(1, 열).Value = 값
        시작행 = 2
        for 시작좌표, _ in self.글자좌표리스트("□ 비목별 검토내역"):
            self.대상.SetPosBySet(self.좌표(시작좌표.Item("List"), 시작좌표.Item("Para"), 시작좌표.Item("Pos") + 1))
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)
            텍스트 = self.블록스캔()[1]
            self.캔슬()
            self.리스트끝()
            self.대상.HAction.Run("MoveDown")
            세부사업명 = 텍스트.replace("□ 비목별 검토내역", "").replace(":", "").strip()
            분할리스트 = self._선택표행추출(9)
            if not 분할리스트:
                continue
            정리데이터 = self._행안부정리데이터(세부사업명, 분할리스트)
            for 행, 줄 in enumerate(정리데이터, start=시작행):
                for 열, 값 in enumerate(줄, start=1):
                    정리.Cells(행, 열).Value = 값
            시작행 += len(정리데이터)
        return None

    def 경기문재일반궁극의정리(self, 이미지, 옵션):
        def 줄선택():
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)

        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6)
            시작줄 = int(self.대상.KeyIndicator()[5])
            self.대상.MovePos(7)
            끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("MoveLineBegin")
            끝줄개수 = len(self.블록스캔()[1])
            self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                self.대상.HAction.Run("Select")
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                self.캔슬()
                표식들 = [
                    (r"󰏚 ", r"󰏚 [가-힣\s]+:"),
                    (r" ○ ", r" ○ [가-힣\s]+:"),
                    (r"   - ", r"-[가-힣\s]+:"),
                    (r"     \* ", r"\*[가-힣\s]+:"),
                    (r"     ※ ", None),
                ]
                for 표식, 제목표식 in 표식들:
                    매치 = re.search(표식, 텍스트)
                    if 매치:
                        끝위치 = 매치.end()
                        if 제목표식:
                            제목매치 = re.search(제목표식, 텍스트)
                            if 제목매치:
                                끝위치 = 제목매치.end() + 1
                        self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치))
                        self.대상.HAction.Run("Select")
                        self.대상.MovePos(7)
                        break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1
                        self.대상.HAction.Run("CharShapeSpacingDecrease")
                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8:
                            self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()

        def 다음문단():
            self.캔슬()
            self.대상.MovePos(10)

        줄선택()
        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트)
        텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트)
        텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "경기표" and not re.match(r"^표", 텍스트):
            self.방금처리 = 0
        if self.방금처리 == "부여추진일정" and not re.match(r"^추진일정", 텍스트):
            self.방금처리 = 0
        if re.match(r"^표\s*:\s*", 텍스트) or re.match(r"^표\s+", 텍스트):
            텍스트 = re.sub(r"^(표\s*:|표)\s*", "시간계획:", 텍스트, count=1)
            self.백스페이스()
            텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트)
            self.경기표([x.strip() for x in 텍스트.split(":")[1:]])
            self.백스페이스()
        elif re.match(r"^\d+\.\s*", 텍스트):
            텍스트 = re.sub(r"^(\d+\.)\s*", r"\1 ", 텍스트)
            self.문장(텍스트)
            줄선택()
            self.폰트("굴림체")
            self.글자크기(12)
            self.내어쓰기(-18)
            self.문단여백(0, 0)
            self.캔슬()
            self.대상.MovePos(6)
            self.대상.GetPosBySet()
            궁극자간(9)
        elif re.match(r"^[가나다라마바사아자차카타파하]\)\s*", 텍스트):
            텍스트 = re.sub(r"^([가나다라마바사아자차카타파하]\))\s*", r"\1 ", 텍스트)
            self.문장(텍스트)
            줄선택()
            self.폰트("굴림체")
            self.글자크기(12)
            self.내어쓰기(-24)
            self.문단여백(18, 0)
            self.캔슬()
            self.대상.MovePos(6)
            self.대상.GetPosBySet()
            궁극자간(9)
        다음문단()
        return None

    def 세종교궁극의정리(self, 이미지):
        def 줄선택():
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)

        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6)
            시작줄 = int(self.대상.KeyIndicator()[5])
            self.대상.MovePos(7)
            끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("MoveLineBegin")
            끝줄개수 = len(self.블록스캔()[1])
            self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                self.대상.HAction.Run("Select")
                self.대상.MovePos(7)
                전체텍스트 = self.블록스캔()[1]
                self.캔슬()
                for 표식, 제목표식 in [
                    (r"□ ", r"□ [가-힣\s]+:"),
                    (r" ◦ ", r" ◦ [가-힣\s]+:"),
                    (r"   - ", r"   - [가-힣\s]+:"),
                    (r"      \* ", r"\*[가-힣\s]+:"),
                    (r"      ※ ", None),
                ]:
                    매치 = re.search(표식, 전체텍스트)
                    if 매치:
                        끝위치 = 매치.end()
                        제목매치 = re.search(제목표식, 전체텍스트) if 제목표식 else None
                        if 제목매치:
                            끝위치 = 제목매치.end() + 1
                        self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치))
                        self.대상.HAction.Run("Select")
                        self.대상.MovePos(7)
                        break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1
                        self.대상.HAction.Run("CharShapeSpacingDecrease")
                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8:
                            self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()

        def 콜론내어쓰기(전체텍스트, 위치, 종류):
            매치 = re.search(rf"{re.escape(종류)}[가-힣\(\)0-9\s]+: ", 전체텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                self.문장내어쓰기()

        def 별찾아바꾸기(전체텍스트, 위치):
            for i, 문자 in enumerate(전체텍스트):
                if 문자 != "*":
                    continue
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + i))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + i + 1))
                self.윗첨자()
                self.캔슬()

        def 다음문단():
            self.캔슬()
            self.대상.MovePos(10)

        def 명령(이름):
            return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s+", 텍스트)

        줄선택()
        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(150)
        self.기본정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트)
        텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트)
        텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "우본표" and not re.match(r"^(표\s*:|표)\s+", 텍스트):
            self.방금처리 = 0
        if self.방금처리 == "컨트롤엔터" and not re.match(r"^(컨트롤엔터\s*:|컨트롤엔터)\s+", 텍스트):
            self.방금처리 = 0

        if 명령("제목"):
            텍스트 = re.sub(r"^(제목\s*:|제목)\s*", "제목:", 텍스트, count=1)
            self.백스페이스()
            self.세종교제목([x.strip() for x in 텍스트.split(":")[1:]])
            self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1)
            self.백스페이스()
            self.소제목카운트 += 1
            self.우본소제목(self.소제목카운트, 텍스트.split(":", 1)[1].strip())
            self.백스페이스()
        elif 명령("중제목"):
            텍스트 = re.sub(r"^(중제목\s*:|중제목)\s*", "중제목:", 텍스트, count=1)
            self.백스페이스()
            self.소제목카운트 = 0
            self.중제목카운트 += 1
            if self.중제목카운트 == 13:
                self.중제목카운트 = 1
            self.우본중제목(self.로마숫자[self.중제목카운트], 텍스트.split(":", 1)[1].strip())
            self.백스페이스()
        elif 명령("개요"):
            텍스트 = re.sub(r"^(개요\s*:|개요)\s*", "개요:", 텍스트, count=1)
            self.백스페이스()
            self.우본개요1([x.strip() for x in 텍스트.split(":")[1:]])
            self.백스페이스()
        elif 명령("표"):
            텍스트 = re.sub(r"^(표\s*:|표)\s*", "표:", 텍스트, count=1)
            self.백스페이스()
            텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트)
            self.우본표([x.strip() for x in 텍스트.split(":")[1:]])
            self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1)
            self.백스페이스()
            self.세종교표지([x.strip() for x in 텍스트.split(":")[1:]], 이미지)
            self.백스페이스()
        elif 명령("목차"):
            self.백스페이스()
            self.우본목차2(이미지)
            self.백스페이스()
        elif 명령("참고"):
            텍스트 = re.sub(r"^(참고\s*:|참고)\s*", "참고:", 텍스트, count=1)
            self.백스페이스()
            self.우본참고(텍스트.split(":", 1)[1].strip())
            self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1)
            self.백스페이스()
            self.우본붙임(텍스트.split(":", 1)[1].strip())
            self.백스페이스()
        elif re.match(r"^컨트롤엔터\s*", 텍스트):
            self.백스페이스()
            self.페이지엔터()
            self.방금처리 = "컨트롤엔터"
            self.딜리트()
            self.궁극의정리위치보정 -= 1
            self.캔슬()
            self.대상.MovePos(11)
        elif 명령("설명"):
            텍스트 = re.sub(r"^(설명\s*:|설명|)\s*", "", 텍스트, count=1)
            self.문장("< " + 텍스트.strip() + " >")
            줄선택()
            self.중고딕()
            self.글자크기(13)
            self.기본글자()
            self.문단위(10)
            self.가운데정렬()
            self.진하게()
            self.캔슬()
            self.대상.MovePos(6)
        elif 텍스트.startswith(("ㅁ", "□", "네모 ", "", "네모:")):
            텍스트 = re.sub(r"^(ㅁ|□||네모\s*:|네모|)\s*", "□ ", 텍스트, count=1)
            self.문장(텍스트)
            줄선택()
            self.폰트("HY헤드라인M")
            self.글자크기(16)
            self.문단위(15)
            self.내어쓰기(-24)
            self.캔슬()
            self.대상.MovePos(6)
            self.대상.GetPosBySet()
            궁극자간(5)
        elif 텍스트.startswith(("ㅇ", "○", "◦", "❍", "", "원 ", "원:")):
            텍스트 = re.sub(r"^(ㅇ|○|❍||◦|원\s*:|원)\s*", " ◦ ", 텍스트, count=1)
            self.문장(텍스트)
            줄선택()
            self.폰트("휴먼명조")
            self.글자크기(15)
            self.내어쓰기(-30)
            self.문단위(12)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            별찾아바꾸기(텍스트, 위치)
            매치 = re.search(r" ◦ ", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            self.문장내어쓰기()
            콜론내어쓰기(텍스트, 위치, "◦")
            궁극자간(9)
        elif 텍스트.startswith(("-", "바 ", "바:")):
            텍스트 = re.sub(r"^(-|바\s*:|바)\s*", "   - ", 텍스트, count=1)
            self.문장(텍스트)
            줄선택()
            self.폰트("휴먼명조")
            self.글자크기(15)
            self.내어쓰기(-39.6)
            self.문단위(10)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            별찾아바꾸기(텍스트, 위치)
            콜론내어쓰기(텍스트, 위치, "-")
            궁극자간(9)
        elif 텍스트.startswith(("*", "별 ", "별:")):
            텍스트 = re.sub(r"^(\*|별\s*:|별)\s*", "      * ", 텍스트, count=1)
            self.문장(텍스트)
            줄선택()
            self.중고딕()
            self.글자크기(13)
            self.문단위(5)
            self.내어쓰기(-50.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            콜론내어쓰기(텍스트, 위치, "*")
            궁극자간(10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ", "당구:", "당구장:")):
            텍스트 = re.sub(r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "      ※ ", 텍스트, count=1)
            self.문장(텍스트)
            줄선택()
            self.중고딕()
            self.글자크기(13)
            self.문단위(5)
            self.내어쓰기(-58.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            콜론내어쓰기(텍스트, 위치, "※")
            궁극자간(10)
        다음문단()
        return None

    def 강원궁극의정리(self, 이미지):
        def 줄선택():
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)

        def 범위글자크기(전체텍스트, 위치, 범위들, 크기):
            for 시작, 끝 in 범위들:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 시작))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝))
                self.글자크기(크기)
                self.캔슬()

        def 괄호찾아바꾸기(전체텍스트, 위치, 크기):
            스택, 범위들 = [], []
            for i, 문자 in enumerate(전체텍스트):
                if 문자 == "(":
                    스택.append(i)
                elif 문자 == ")" and 스택:
                    범위들.append((스택.pop(), i + 1))
            범위글자크기(전체텍스트, 위치, 범위들, 크기)

        def 요일찾아바꾸기(전체텍스트, 위치, 크기):
            범위글자크기(전체텍스트, 위치, [(m.start(), m.end()) for m in re.finditer(r"\((월|화|수|목|금|토|일)\)", 전체텍스트)], 크기)

        def 별찾아바꾸기(전체텍스트, 위치):
            for i, 문자 in enumerate(전체텍스트):
                if 문자 == "*":
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + i))
                    self.대상.HAction.Run("Select")
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + i + 1))
                    self.윗첨자()
                    self.캔슬()

        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6)
            시작줄 = int(self.대상.KeyIndicator()[5])
            self.대상.MovePos(7)
            끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("MoveLineBegin")
            끝줄개수 = len(self.블록스캔()[1])
            self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                self.대상.HAction.Run("Select")
                self.대상.MovePos(7)
                전체텍스트 = self.블록스캔()[1]
                self.캔슬()
                for 표식, 제목표식 in [
                    (r" □ ", None), (r"   ", r"   \((.*?)\) "),
                    (r"    - ", r"    - [가-힣\s]+:"), (r"   \* ", None),
                ]:
                    매치 = re.search(표식, 전체텍스트)
                    if 매치:
                        끝위치 = 매치.end()
                        제목매치 = re.search(제목표식, 전체텍스트) if 제목표식 else None
                        if 제목매치:
                            끝위치 = 제목매치.end() + (1 if "[가-힣" in 제목표식 else 0)
                        self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치))
                        self.대상.HAction.Run("Select")
                        self.대상.MovePos(7)
                        break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1
                        self.대상.HAction.Run("CharShapeSpacingDecrease")
                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8:
                            self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()

        def 다음문단():
            self.캔슬()
            self.대상.MovePos(10)

        def 명령(이름):
            return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)

        줄선택()
        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트)
        텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트)
        텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "부여시간계획" and not re.match(r"^시간계획", 텍스트):
            self.방금처리 = 0
        if self.방금처리 == "부여추진일정" and not re.match(r"^추진일정", 텍스트):
            self.방금처리 = 0
        if 명령("제목"):
            텍스트 = re.sub(r"^(제목\s*:|제목)\s*", "제목:", 텍스트, count=1)
            self.백스페이스(); self.강원제목(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("중제목"):
            텍스트 = re.sub(r"^(중제목\s*:|중제목)\s*", "중제목:", 텍스트, count=1)
            self.백스페이스(); self.강원중제목(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("보고자"):
            텍스트 = re.sub(r"^(보고자\s*:|보고자)\s*", "보고자:", 텍스트, count=1)
            self.백스페이스(); self.강원보고자(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1)
            self.백스페이스(); self.강원표지([x.strip() for x in 텍스트.split(":")[1:]], 이미지); self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1)
            self.백스페이스()
            self.소제목카운트 += 1
            if self.소제목카운트 > 12:
                self.소제목카운트 = 1
            self.강원소제목(self.로마숫자[self.소제목카운트], 텍스트.split(":", 1)[1].strip())
            self.백스페이스()
        elif 명령("요약"):
            텍스트 = re.sub(r"^(요약\s*:|요약)\s*", "요약:", 텍스트, count=1)
            self.백스페이스(); self.강원요약(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("참고"):
            텍스트 = re.sub(r"^(참고\s*:|참고)\s*", "참고:", 텍스트, count=1)
            self.백스페이스(); self.강원참고(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1)
            self.백스페이스(); self.강원붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 텍스트.startswith(("ㅁ", "□", "네모 ", "", "네모:")):
            텍스트 = re.sub(r"^(ㅁ|□||네모\s*:|네모|)\s*", " □ ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("HY헤드라인M"); self.글자크기(17)
            self.문단위(10); self.내어쓰기(-34); self.캔슬(); self.대상.MovePos(6)
            self.대상.GetPosBySet(); 궁극자간(5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "◦", "원 ", "원:")):
            텍스트 = re.sub(r"^(ㅇ|○|❍||◦|원\s*:|원)\s*", "   ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-40.8); self.문단위(7); self.캔슬(); self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            괄호찾아바꾸기(텍스트, 위치, 14); 별찾아바꾸기(텍스트, 위치); 요일찾아바꾸기(텍스트, 위치, 15)
            매치 = re.search(r"   \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                self.진하게(); self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            궁극자간(9)
        elif 텍스트.startswith(("-", "바 ", "바:")):
            텍스트 = re.sub(r"^(-|바\s*:|바)\s*", "    - ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(14)
            self.내어쓰기(-46.7); self.문단위(5); self.캔슬(); self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            괄호찾아바꾸기(텍스트, 위치, 13); 별찾아바꾸기(텍스트, 위치); 요일찾아바꾸기(텍스트, 위치, 14)
            매치 = re.search(r"    - \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            궁극자간(9)
        elif 텍스트.startswith(("*", "별 ", "별:")):
            텍스트 = re.sub(r"^(\*|별\s*:|별)\s*", "      * ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("맑은 고딕"); self.글자크기(12)
            self.내어쓰기(-47.6); self.문단위(0); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(10)
        elif 텍스트.startswith(("※", "당구장 ", "당구 ", "당구장:", "당구:")):
            텍스트 = re.sub(r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "      ※ ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("맑은 고딕"); self.글자크기(12)
            self.내어쓰기(-51.6); self.문단위(0); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(10)
        다음문단()
        return None

    def 철도궁극의정리(self, 이미지):
        def 줄선택():
            self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)

        def 범위크기(전체텍스트, 위치, 범위들, 크기):
            for 시작, 끝 in 범위들:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 시작))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝))
                self.글자크기(크기); self.캔슬()

        def 괄호찾아바꾸기(전체텍스트, 위치):
            스택, 범위들 = [], []
            for i, 문자 in enumerate(전체텍스트):
                if 문자 == "(": 스택.append(i)
                elif 문자 == ")" and 스택: 범위들.append((스택.pop(), i + 1))
            범위크기(전체텍스트, 위치, 범위들, 13)

        def 요일찾아바꾸기(전체텍스트, 위치, 크기):
            범위크기(전체텍스트, 위치, [(m.start(), m.end()) for m in re.finditer(r"\((월|화|수|목|금|토|일)\)", 전체텍스트)], 크기)

        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6); 시작줄 = int(self.대상.KeyIndicator()[5])
            self.대상.MovePos(7); 끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin")
            끝줄개수 = len(self.블록스캔()[1]); self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0
                self.대상.MovePos(6); 위치 = self.대상.GetPosBySet()
                self.대상.HAction.Run("Select"); self.대상.MovePos(7)
                전체텍스트 = self.블록스캔()[1]; self.캔슬()
                for 표식, 제목표식 in [(r"□ ", None), (r" ◦ ", r" ◦ \((.*?)\) "), (r"    - ", r"    - [가-힣\s]+:"), (r"   \* ", None)]:
                    매치 = re.search(표식, 전체텍스트)
                    if not 매치: continue
                    끝위치 = 매치.end()
                    제목매치 = re.search(제목표식, 전체텍스트) if 제목표식 else None
                    if 제목매치: 끝위치 = 제목매치.end() + (1 if "[가-힣" in 제목표식 else 0)
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치))
                    self.대상.HAction.Run("Select"); self.대상.MovePos(7); break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease")
                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()

        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)

        줄선택(); self.기본글자(); self.글자간격(0); self.글자장평(100)
        self.문단여백(0, 0); self.문단위(0); self.문단아래(0); self.줄간격(160)
        self.왼쪽정렬(); self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트)
        텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "부여시간계획" and not re.match(r"^시간계획", 텍스트): self.방금처리 = 0
        if self.방금처리 == "부여추진일정" and not re.match(r"^추진일정", 텍스트): self.방금처리 = 0

        if 명령("제목"):
            텍스트 = re.sub(r"^(제목\s*:|제목)\s*", "제목:", 텍스트, count=1)
            self.백스페이스(); self.철도제목(이미지, 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1)
            self.백스페이스(); self.소제목카운트 += 1
            self.철도소제목(self.로마숫자[self.소제목카운트], 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("전략"):
            텍스트 = re.sub(r"^(전략\s*:|전략)\s*", "전략:", 텍스트, count=1)
            self.백스페이스(); self.철도전략(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("개요"):
            텍스트 = re.sub(r"^(개요\s*:|개요)\s*", "개요:", 텍스트, count=1)
            self.백스페이스(); self.우본개요1([x.strip() for x in 텍스트.split(":")[1:]]); self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1)
            self.백스페이스(); self.철도표지(텍스트.split(":", 1)[1].strip(), 이미지); self.백스페이스()
        elif 명령("목차"):
            self.백스페이스(); self.철도목차(); self.백스페이스()
        elif 명령("참고"):
            텍스트 = re.sub(r"^(참고\s*:|참고)\s*", "참고:", 텍스트, count=1)
            self.백스페이스(); self.철도참고(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1)
            self.백스페이스(); self.철도붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 텍스트.startswith(("ㅁ", "□", "네모 ", "", "네모:")):
            텍스트 = re.sub(r"^(ㅁ|□||네모\s*:|네모|)\s*", "□ ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("HY헤드라인M"); self.글자크기(16)
            self.문단위(15); self.내어쓰기(-24); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "◦", "원 ", "원:")):
            텍스트 = re.sub(r"^(ㅇ|○|❍||◦|원\s*:|원)\s*", " ◦ ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.휴먼명조(); self.글자크기(15)
            self.내어쓰기(-30); self.문단위(8); self.캔슬(); self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet(); 괄호찾아바꾸기(텍스트, 위치); 요일찾아바꾸기(텍스트, 위치, 15)
            매치 = re.search(r" ◦ \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                self.진하게(); self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            궁극자간(9)
        elif 텍스트.startswith(("-", "바 ", "바:")):
            텍스트 = re.sub(r"^(-|바\s*:|바)\s*", "    - ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-42.4); self.문단위(5); self.캔슬(); self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet(); 괄호찾아바꾸기(텍스트, 위치); 요일찾아바꾸기(텍스트, 위치, 15)
            if re.search(r"    - \((.*?)\)", 텍스트):
                매치 = re.search(r"   - \((.*?)\)", 텍스트)
                if 매치:
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3))
                    self.대상.HAction.Run("Select")
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                    self.글자크기(15); self.캔슬()
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            궁극자간(9)
        elif 텍스트.startswith(("*", "별 ", "별:")):
            텍스트 = re.sub(r"^(\*|별\s*:|별)\s*", "   * ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.중고딕(); self.글자크기(13)
            self.내어쓰기(-31.4); self.문단위(10); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(10)
        다음문단(); return None

    def 홍성궁극의정리(self, 이미지):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 범위크기(위치, 범위들, 크기):
            for 시작, 끝 in 범위들:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 시작))
                self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝))
                self.글자크기(크기); self.캔슬()
        def 괄호찾아바꾸기(전체텍스트, 위치):
            스택, 범위들 = [], []
            for i, 문자 in enumerate(전체텍스트):
                if 문자 == "(": 스택.append(i)
                elif 문자 == ")" and 스택: 범위들.append((스택.pop(), i + 1))
            범위크기(위치, 범위들, 13)
        def 요일찾아바꾸기(전체텍스트, 위치, 크기):
            범위크기(위치, [(m.start(), m.end()) for m in re.finditer(r"\((월|화|수|목|금|토|일)\)", 전체텍스트)], 크기)
        def 콜론내어쓰기(전체텍스트, 위치, 종류):
            매치 = re.search(rf"{re.escape(종류)}[가-힣\(\)0-9\s]+: ", 전체텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.문장내어쓰기()
        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6); 시작줄 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 끝줄개수 = len(self.블록스캔()[1]); self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0; self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
                전체텍스트 = self.블록스캔()[1]; self.캔슬()
                표식들 = [(r"󰏚 ", r"󰏚 [가-힣\s]+:"), (r"  ", r" [가-힣\s]+:|  \((.*?)\) "), (r"  - ", r"-[가-힣\s]+:"), (r"   · ", r"·[가-힣\s]+:"), (r"      \* ", r"\*[가-힣\s]+:"), (r"      ※ ", None)]
                for 표식, 제목표식 in 표식들:
                    매치 = re.search(표식, 전체텍스트)
                    if not 매치: continue
                    끝위치 = 매치.end(); 제목매치 = re.search(제목표식, 전체텍스트) if 제목표식 else None
                    if 제목매치: 끝위치 = 제목매치.end() + (1 if "[가-힣" in 제목표식 else 0)
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치)); self.대상.HAction.Run("Select"); self.대상.MovePos(7); break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)

        줄선택(); self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0)
        self.줄간격(160); self.왼쪽정렬(); self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip(); 텍스트 = re.sub(r"\s*:\s*", " : ", 텍스트)
        텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트); 텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if 명령("중제목"):
            텍스트 = re.sub(r"^(중제목\s*:|중제목)\s*", "중제목:", 텍스트, count=1); self.백스페이스(); self.충남중제목(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("요약"):
            텍스트 = re.sub(r"^(요약\s*:|요약)\s*", "요약:", 텍스트, count=1); self.백스페이스(); self.홍성요약([x.strip() for x in 텍스트.split(":")[1:]]); self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1); self.백스페이스(); self.소제목카운트 += 1
            self.충남소제목(str(self.소제목카운트), 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1); self.백스페이스(); self.충남붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("끝장"):
            self.백스페이스(); self.홍성끝장(이미지); self.백스페이스()
        elif 명령("참고"):
            텍스트 = re.sub(r"^(참고\s*:|참고)\s*", "참고:", 텍스트, count=1); self.백스페이스(); self.충남참고(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1); self.백스페이스(); self.홍성표지([x.strip() for x in 텍스트.split(":")[1:]], 이미지); self.백스페이스()
        elif 명령("동향제목"):
            텍스트 = re.sub(r"^(동향제목\s*:|동향제목)\s*", "동향제목:", 텍스트, count=1); self.백스페이스()
            self.홍성동향제목([x.strip() for x in 텍스트.split(":")[1:]][:10]); self.백스페이스()
        elif 텍스트.startswith(("ㅁ", "□", "네모 ", "", "󰏚")):
            텍스트 = re.sub(r"^(ㅁ|□||󰏚|네모\s*:|네모|)\s*", "󰏚 ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("HY헤드라인M"); self.글자크기(16)
            self.내어쓰기(-24); self.문단위(10); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ")):
            텍스트 = re.sub(r"^(ㅇ|○|❍||원\s*:|원)\s*", "  ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-29.2); self.문단위(5); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 괄호찾아바꾸기(텍스트, 위치); 요일찾아바꾸기(텍스트, 위치, 15)
            매치 = re.search(r"  \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3)); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.진하게(); self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            콜론내어쓰기(텍스트, 위치, ""); 궁극자간(9)
        elif 텍스트.startswith(("-", "바 ")):
            텍스트 = re.sub(r"^(-|바\s*:|바)\s*", "  - ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-30); self.문단위(5); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 괄호찾아바꾸기(텍스트, 위치); 요일찾아바꾸기(텍스트, 위치, 15)
            매치 = re.search(r"  - \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3)); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.진하게(); self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            콜론내어쓰기(텍스트, 위치, "-"); 궁극자간(9)
        elif 텍스트.startswith(("·", "점 ")):
            텍스트 = re.sub(r"^(·|점\s*:|점)\s*", "   · ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-34.9); self.문단위(5); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "·"); 궁극자간(10)
        elif 텍스트.startswith(("*", "별 ")):
            텍스트 = re.sub(r"^(\*|별\s*:|별)\s*", "      * ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("맑은 고딕"); self.글자크기(12)
            self.내어쓰기(-47.1); self.문단위(2); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "*"); 궁극자간(10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ")):
            텍스트 = re.sub(r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "      ※ ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("맑은 고딕"); self.글자크기(12)
            self.내어쓰기(-47.1); self.문단위(2); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "※"); 궁극자간(10)
        다음문단(); return None

    def 경기궁극의정리(self, 이미지, 옵션):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 부분크기(위치, 범위들, 크기):
            for 시작, 끝 in 범위들:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 시작)); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝)); self.글자크기(크기); self.캔슬()
        def 괄호찾아바꾸기(전체텍스트, 위치, 크기):
            스택, 범위들 = [], []
            for i, 문자 in enumerate(전체텍스트):
                if 문자 == "(": 스택.append(i)
                elif 문자 == ")" and 스택: 범위들.append((스택.pop(), i + 1))
            부분크기(위치, 범위들, 크기)
        def 요일찾아바꾸기(전체텍스트, 위치, 크기): 부분크기(위치, [(m.start(), m.end()) for m in re.finditer(r"\((월|화|수|목|금|토|일)\)", 전체텍스트)], 크기)
        def 콜론내어쓰기(전체텍스트, 위치, 종류):
            매치 = re.search(rf"{re.escape(종류)}[가-힣\(\)0-9\s]+: ", 전체텍스트)
            if 매치: self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.문장내어쓰기()
        def 별찾아바꾸기(전체텍스트, 위치):
            for i, 문자 in enumerate(전체텍스트):
                if 문자 == "*":
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + i)); self.대상.HAction.Run("Select")
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + i + 1)); self.윗첨자(); self.캔슬()
        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6); 시작줄 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 끝줄개수 = len(self.블록스캔()[1]); self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0; self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
                전체텍스트 = self.블록스캔()[1]; self.캔슬()
                for 표식, 제목표식 in [(r"□ ", r"□ [가-힣\s]+:"), (r" ○ ", r" ○ \((.*?)\) | ○ [가-힣\s]+:"), (r"   - ", r"-[가-힣\s]+:"), (r"     \* ", r"\*[가-힣\s]+:"), (r"     ※ ", None)]:
                    매치 = re.search(표식, 전체텍스트)
                    if not 매치: continue
                    끝위치 = 매치.end(); 제목매치 = re.search(제목표식, 전체텍스트) if 제목표식 else None
                    if 제목매치: 끝위치 = 제목매치.end() + (1 if "[가-힣" in 제목표식 else 0)
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치)); self.대상.HAction.Run("Select"); self.대상.MovePos(7); break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름, 공백형=True): return re.match(rf"^{이름}\s*:\s*", 텍스트) or (공백형 and re.match(rf"^{이름}\s*", 텍스트))
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]

        줄선택(); self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0)
        self.줄간격(150); self.왼쪽정렬(); self.자간헌터(0); 텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "경기표" and not re.match(r"^표", 텍스트): self.방금처리 = 0
        if self.방금처리 == "부여추진일정" and not re.match(r"^추진일정", 텍스트): self.방금처리 = 0
        if 명령("제목"):
            텍스트 = re.sub(r"^(제목\s*:|제목)\s*", "제목:", 텍스트, count=1); self.백스페이스(); self.경기제목(인자목록(텍스트), 이미지, 옵션); self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1); self.백스페이스(); self.소제목카운트 += 1
            self.경기소제목(str(self.소제목카운트), 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1); self.백스페이스(); self.경기표지(텍스트.split(":", 1)[1].strip(), 이미지); self.백스페이스()
        elif re.match(r"^표\s*:\s*", 텍스트) or re.match(r"^표\s+", 텍스트):
            텍스트 = re.sub(r"^(표\s*:|표)\s*", "시간계획:", 텍스트, count=1); self.백스페이스()
            텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트); self.경기표(인자목록(텍스트)); self.백스페이스()
        elif 명령("요약"):
            텍스트 = re.sub(r"^(요약\s*:|요약)\s*", "요약:", 텍스트, count=1); self.백스페이스(); self.경기요약(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("목차"):
            self.백스페이스(); self.경기목차(); self.백스페이스()
        elif 명령("서론"):
            텍스트 = re.sub(r"^(서론\s*:|서론)\s*", "서론:", 텍스트, count=1); self.백스페이스(); self.부여서론(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1); self.백스페이스(); self.붙임카운트 += 1
            self.경기붙임(str(self.붙임카운트), 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("참고"):
            텍스트 = re.sub(r"^(참고\s*:|참고)\s*", "참고:", 텍스트, count=1); self.백스페이스(); self.참고카운트 += 1
            self.경기참고(str(self.참고카운트), 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("인사말씀"):
            self.백스페이스(); self.경기인사말씀(이미지); self.백스페이스()
        elif 명령("시간계획"):
            텍스트 = re.sub(r"^(시간계획\s*:|시간계획)\s*", "시간계획:", 텍스트, count=1); self.백스페이스(); self.부여시간계획(인자목록(텍스트)); self.백스페이스()
        elif 명령("추진일정"):
            텍스트 = re.sub(r"^(추진일정\s*:|추진일정)\s*", "추진일정:", 텍스트, count=1); self.백스페이스(); self.부여추진일정(인자목록(텍스트)); self.백스페이스()
        elif 명령("동향제목"):
            텍스트 = re.sub(r"^(동향제목\s*:|동향제목)\s*", "동향제목:", 텍스트, count=1); self.백스페이스(); self.부여동향제목(이미지[3], 인자목록(텍스트)); self.백스페이스()
        elif 텍스트.startswith(("ㅁ", "□", "네모 ", "네모:", "", "󰏚")):
            텍스트 = re.sub(r"^(ㅁ|□||󰏚|네모\s*:|네모|)\s*", "□ ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.문단위(10)
            self.폰트("경기천년제목 Medium"); self.글자크기(17); self.내어쓰기(-23.6); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ", "원:")):
            텍스트 = re.sub(r"^(ㅇ|○|❍||원\s*:|원)\s*", " ○ ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("경기천년바탕 Regular")
            self.글자크기(15); self.내어쓰기(-29.4); self.문단위(7); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet()
            별찾아바꾸기(텍스트, 위치); 궁극자간(9); 괄호찾아바꾸기(텍스트, 위치, 13); 요일찾아바꾸기(텍스트, 위치, 15)
            매치 = re.search(r" ○ \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3)); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.진하게(); self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
        elif 텍스트.startswith(("-", "바 ", "바:")):
            텍스트 = re.sub(r"^(-|바\s*:|바)\s*", "   - ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("경기천년바탕 Regular")
            self.글자크기(15); self.내어쓰기(-37.7); self.문단위(5); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 별찾아바꾸기(텍스트, 위치); 궁극자간(9)
        elif 텍스트.startswith(("*", "별 ", "별:")):
            텍스트 = re.sub(r"^(\*|별\s*:|별)\s*", "     * ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("경기천년제목 Light")
            self.글자크기(13); self.내어쓰기(-46.4); self.문단위(2); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ", "당구:", "당구장:")):
            텍스트 = re.sub(r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "     ※ ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("경기천년제목 Light")
            self.글자크기(13); self.내어쓰기(-50.4); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(10)
        다음문단(); return None

    def 경기신보궁극의정리(self, 이미지):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]
        줄선택(); self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0)
        self.줄간격(150); self.왼쪽정렬(); self.자간헌터(0); 텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "경기표" and not re.match(r"^표", 텍스트): self.방금처리 = 0
        if self.방금처리 == "부여추진일정" and not re.match(r"^추진일정", 텍스트): self.방금처리 = 0
        처리함 = True
        if 명령("제목2"):
            텍스트 = re.sub(r"^(제목2\s*:|제목2)\s*", "제목2:", 텍스트, count=1); self.백스페이스(); self.경기신보제목2(인자목록(텍스트), 이미지); self.백스페이스()
        elif 명령("회색박스"):
            텍스트 = re.sub(r"^(회색박스\s*:|회색박스)\s*", "회색박스:", 텍스트, count=1); self.백스페이스(); self.경기신보회색박스(인자목록(텍스트)); self.백스페이스()
        elif 명령("제목"):
            텍스트 = re.sub(r"^(제목\s*:|제목)\s*", "제목:", 텍스트, count=1); self.백스페이스(); self.경기신보제목(인자목록(텍스트), 이미지); self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1); self.백스페이스(); self.소제목카운트 += 1
            self.경기소제목(str(self.소제목카운트), 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1); self.백스페이스()
            텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트)
            self.경기표지(텍스트.split(":", 1)[1].strip(), 이미지); self.백스페이스()
        elif 명령("요약"):
            텍스트 = re.sub(r"^(요약\s*:|요약)\s*", "요약:", 텍스트, count=1); self.백스페이스(); self.경기요약(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("참고박스"):
            텍스트 = re.sub(r"^(참고박스\s*:|참고박스)\s*", "참고박스:", 텍스트, count=1); self.백스페이스(); self.부여참고박스(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("서론"):
            텍스트 = re.sub(r"^(서론\s*:|서론)\s*", "서론:", 텍스트, count=1); self.백스페이스(); self.부여서론(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1); self.백스페이스(); self.부여붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("한줄일정"):
            텍스트 = re.sub(r"^(한줄일정\s*:|한줄일정)\s*", "한줄일정:", 텍스트, count=1); self.백스페이스(); self.부여한줄일정(인자목록(텍스트)); self.백스페이스()
        elif re.match(r"^표\s*:\s*", 텍스트) or re.match(r"^표\s+", 텍스트):
            텍스트 = re.sub(r"^(표\s*:|표)\s*", "표:", 텍스트, count=1); self.백스페이스()
            텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트); self.경기표(인자목록(텍스트)); self.백스페이스()
        elif 명령("추진일정"):
            텍스트 = re.sub(r"^(추진일정\s*:|추진일정)\s*", "추진일정:", 텍스트, count=1); self.백스페이스(); self.부여추진일정(인자목록(텍스트)); self.백스페이스()
        elif 명령("동향제목"):
            텍스트 = re.sub(r"^(동향제목\s*:|동향제목)\s*", "동향제목:", 텍스트, count=1); self.백스페이스(); self.부여동향제목(이미지[3], 인자목록(텍스트)); self.백스페이스()
        else:
            처리함 = False
        if 처리함:
            self.캔슬(); self.대상.MovePos(10); return None
        return self.경기궁극의정리(이미지, 0)

    def 부여궁극의정리(self, 이미지, 모드):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 콜론내어쓰기(전체텍스트, 위치, 종류):
            매치 = re.search(rf"{re.escape(종류)}[가-힣\(\)0-9\s]+: ", 전체텍스트)
            if 매치: self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.문장내어쓰기()
        def 궁극자간(끝줄개수설정=9):
            self.대상.MovePos(6); 시작줄 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 끝줄개수 = len(self.블록스캔()[1]); self.캔슬()
            if 끝줄개수 < 끝줄개수설정:
                카운트 = 0; self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
                전체텍스트 = self.블록스캔()[1]; self.캔슬()
                표식들 = [(r"[□󰏚󰊱-󰊹] ", r"[□󰏚󰊱-󰊹] [가-힣\s]+:"), (r"  ❍ ", r"  ❍ \((.*?)\) |❍[가-힣\s]+:"), (r"    - ", r"-[가-힣\s]+:"), (r"      • ", r"•[가-힣\s]+:"), (r"     \* ", r"\*[가-힣\s]+:"), (r"    ※ ", None)]
                for 표식, 제목표식 in 표식들:
                    매치 = re.search(표식, 전체텍스트)
                    if not 매치: continue
                    끝위치 = 매치.end(); 제목매치 = re.search(제목표식, 전체텍스트) if 제목표식 else None
                    if 제목매치: 끝위치 = 제목매치.end() + (1 if "[가-힣" in 제목표식 else 0)
                    self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 끝위치)); self.대상.HAction.Run("Select"); self.대상.MovePos(7); break
                if 끝줄 - 시작줄 >= 1:
                    임시끝줄 = 끝줄
                    while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                        카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 임시끝줄 = int(self.대상.KeyIndicator()[5])
                        if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]

        줄선택(); self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0)
        self.줄간격(170); self.왼쪽정렬(); self.자간헌터(0); 텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if 모드 == 1: 텍스트 = re.sub(r"\s+", " ", 텍스트)
        if self.방금처리 == "부여시간계획" and not re.match(r"^시간계획", 텍스트): self.방금처리 = 0
        if self.방금처리 == "부여추진일정" and not re.match(r"^추진일정", 텍스트): self.방금처리 = 0
        if 명령("표지제목"):
            텍스트 = re.sub(r"^(표지제목\s*:|표지제목)\s*", "표지제목:", 텍스트, count=1); self.백스페이스(); self.부여표지제목(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("제목"):
            텍스트 = re.sub(r"^(제목\s*:|제목)\s*", "제목:", 텍스트, count=1); self.백스페이스(); self.부여제목(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("소제목"):
            텍스트 = re.sub(r"^(소제목\s*:|소제목)\s*", "소제목:", 텍스트, count=1); self.백스페이스(); self.소제목카운트 += 1
            if self.소제목카운트 == 13: self.소제목카운트 = 1
            self.부여소제목(self.로마숫자[self.소제목카운트], 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("점선박스"):
            텍스트 = re.sub(r"^(점선박스\s*:|점선박스)\s*", "점선박스:", 텍스트, count=1); self.백스페이스(); self.부여점선박스(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("참고박스"):
            텍스트 = re.sub(r"^(참고박스\s*:|참고박스)\s*", "참고박스:", 텍스트, count=1); self.백스페이스(); self.부여참고박스(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"):
            텍스트 = re.sub(r"^(표지\s*:|표지)\s*", "표지:", 텍스트, count=1); self.백스페이스(); self.부여표지(텍스트.split(":", 1)[1].strip(), 이미지[0:3]); self.백스페이스()
        elif 명령("서론"):
            텍스트 = re.sub(r"^(서론\s*:|서론)\s*", "서론:", 텍스트, count=1); self.백스페이스(); self.부여서론(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"):
            텍스트 = re.sub(r"^(붙임\s*:|붙임)\s*", "붙임:", 텍스트, count=1); self.백스페이스(); self.부여붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("한줄일정"):
            텍스트 = re.sub(r"^(한줄일정\s*:|한줄일정)\s*", "한줄일정:", 텍스트, count=1); self.백스페이스(); self.부여한줄일정(인자목록(텍스트)); self.백스페이스()
        elif 명령("시간계획"):
            텍스트 = re.sub(r"^(시간계획\s*:|시간계획)\s*", "시간계획:", 텍스트, count=1); self.백스페이스(); self.부여시간계획(인자목록(텍스트)); self.백스페이스()
        elif 명령("추진일정"):
            텍스트 = re.sub(r"^(추진일정\s*:|추진일정)\s*", "추진일정:", 텍스트, count=1); self.백스페이스(); self.부여추진일정(인자목록(텍스트)); self.백스페이스()
        elif 명령("동향제목"):
            텍스트 = re.sub(r"^(동향제목\s*:|동향제목)\s*", "동향제목:", 텍스트, count=1); self.백스페이스(); self.부여동향제목(이미지[3], 인자목록(텍스트)); self.백스페이스()
        elif 텍스트.startswith(("ㅁ", "□", "네모 ", "", "󰏚", "󰊱", "󰊲", "󰊳", "󰊴", "󰊵", "󰊶", "󰊷", "󰊸", "󰊹")):
            self.네모숫자카운트 += 1
            if self.네모숫자카운트 == 10: self.네모숫자카운트 = 1
            텍스트 = re.sub(r"^(ㅁ|□||󰏚|󰊱|󰊲|󰊳|󰊴|󰊵|󰊶|󰊷|󰊸|󰊹|네모\s*:|네모|)\s*", f"{self.네모숫자[self.네모숫자카운트]} ", 텍스트, count=1)
            self.문장(텍스트); 줄선택(); self.폰트("HY헤드라인M"); self.글자크기(16); self.내어쓰기(-24); self.캔슬(); self.대상.MovePos(6); self.대상.GetPosBySet(); 궁극자간(5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ")):
            텍스트 = re.sub(r"^(ㅇ|○|❍||원\s*:|원)\s*", "  ❍ ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-32.5); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 매치 = re.search(r"  ❍ \((.*?)\)", 텍스트)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start() + 3)); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.진하게(); self.글자크기(15); self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
            콜론내어쓰기(텍스트, 위치, "❍"); 궁극자간(9)
        elif 텍스트.startswith(("-", "바 ")):
            텍스트 = re.sub(r"^(-|바\s*:|바)\s*", "    - ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(15)
            self.내어쓰기(-31.7); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "-"); 궁극자간(9)
        elif 텍스트.startswith(("·", "•", "점 ")):
            텍스트 = re.sub(r"^(·|•|점\s*:|점)\s*", "      • ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조"); self.글자크기(14)
            self.내어쓰기(-31.7); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "•"); 궁극자간(10)
        elif 텍스트.startswith(("*", "별 ")):
            텍스트 = re.sub(r"^(\*|별\s*:|별)\s*", "     * ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.중고딕(); self.글자크기(13)
            self.내어쓰기(-32.2); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "*"); 궁극자간(10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ")):
            텍스트 = re.sub(r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "    ※ ", 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트("휴먼명조")
            self.글자색(0, 0, 255); self.글자크기(13); self.내어쓰기(-31.7); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet(); 콜론내어쓰기(텍스트, 위치, "※"); 궁극자간(10)
        다음문단(); return None

    def 충남궁극의정리(self, 이미지, 모드):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]
        def 콜론내어쓰기(전체, 위치, 종류):
            매치 = re.search(rf"{re.escape(종류)}[가-힣\(\)0-9\s]+: ", 전체)
            if 매치:
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.문장내어쓰기()
        def 궁극자간(끝줄개수설정):
            self.대상.MovePos(6); 시작줄 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 끝줄개수 = len(self.블록스캔()[1]); self.캔슬()
            if 끝줄개수 < 끝줄개수설정 and 끝줄 - 시작줄 >= 1:
                카운트 = 0; 임시끝줄 = 끝줄
                while 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                    카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 임시끝줄 = int(self.대상.KeyIndicator()[5])
                    if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()
        def 괄호강조(전체, 위치, 크기):
            for 매치 in re.finditer(r"\([^()]*\)", 전체):
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start())); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.글자크기(크기); self.캔슬()

        줄선택(); self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0)
        self.줄간격(160); self.왼쪽정렬(); self.자간헌터(0); 텍스트 = self.블록스캔()[1].strip()
        텍스트 = re.sub(r"\s*:\s*", " : ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트)
        텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if 모드 == 1: 텍스트 = re.sub(r"\s+", " ", 텍스트)
        if self.방금처리 == "충남시간계획표" and not re.match(r"^시간계획", 텍스트): self.방금처리 = 0
        처리함 = True
        if 명령("제목"): self.백스페이스(); self.충남중제목(re.sub(r"^(제목\s*:|제목)\s*", "", 텍스트, count=1)); self.백스페이스()
        elif 명령("시간계획표"): self.백스페이스(); self.충남시간계획표([x.strip() for x in re.split(r"[:~]", 텍스트)[1:]]); self.백스페이스()
        elif 명령("관련부처"): self.백스페이스(); self.충남관련부처(인자목록(텍스트)); self.백스페이스()
        elif 명령("청한장제목"): self.백스페이스(); self.충남청한장제목(이미지[4], 인자목록(텍스트)); self.백스페이스()
        elif 명령("청서론"): self.백스페이스(); self.충남청서론(인자목록(텍스트)); self.백스페이스()
        elif 명령("청소제목"):
            self.백스페이스(); self.소제목카운트 += 1
            if self.소제목카운트 == 10: self.소제목카운트 = 1
            self.충남청소제목(self.로마숫자[self.소제목카운트], 텍스트.split(":", 1)[1].strip(), 이미지[8]); self.백스페이스()
        elif 명령("한장제목"): self.백스페이스(); self.충남한장제목("·".join(인자목록(텍스트))[:11]); self.백스페이스()
        elif 명령("지사님하실일"): self.백스페이스(); self.충남지사님하실일(인자목록(텍스트)); self.백스페이스()
        elif 명령("소제목"): self.백스페이스(); self.소제목카운트 += 1; self.충남소제목(str(self.소제목카운트), 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("서론"): self.백스페이스(); self.충남서론(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"): self.백스페이스(); self.충남붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"): self.백스페이스(); self.충남표지(인자목록(텍스트), 이미지); self.백스페이스()
        elif 명령("청표지"): self.백스페이스(); self.충남청표지(이미지[5:8], 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("청제목"): self.백스페이스(); self.충남청중제목(이미지[7], 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("끝장원1"): self.백스페이스(); self.충남끝장원(이미지[9]); self.백스페이스()
        elif 명령("끝장원2"): self.백스페이스(); self.충남끝장원(이미지[10]); self.백스페이스()
        elif 명령("끝장"): self.백스페이스(); self.충남CI(이미지[3]); self.백스페이스()
        else: 처리함 = False
        if 처리함: 다음문단(); return None

        사양 = None
        if 텍스트.startswith(("ㅁ", "□", "네모 ", "", "퀀0")): 사양 = (r"^(ㅁ|□||퀀0|네모\s*:|네모|)\s*", "퀀0 ", "HY헤드라인M", 16, -24, 10, 5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ")): 사양 = (r"^(ㅇ|○|❍||원\s*:|원)\s*", "  ", "휴먼명조", 15, -29.2, 5, 9)
        elif 텍스트.startswith(("-", "바 ")): 사양 = (r"^(-|바\s*:|바)\s*", "  - ", "휴먼명조", 15, -30, 5, 9)
        elif 텍스트.startswith(("·", "점 ")): 사양 = (r"^(·|점\s*:|점)\s*", "   · ", "휴먼명조", 15, -34.9, 5, 10)
        elif 텍스트.startswith(("*", "별 ")): 사양 = (r"^(\*|별\s*:|별)\s*", "      * ", "맑은 고딕", 12, -47.1, 2, 10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ")): 사양 = (r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "      ※ ", "맑은 고딕", 12, -47.1, 2, 10)
        if 사양:
            패턴, 머리, 폰트, 크기, 내어, 위, 자간 = 사양; 텍스트 = re.sub(패턴, 머리, 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트(폰트); self.글자크기(크기); self.내어쓰기(내어); self.문단위(위); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet()
            if 머리 in ("  ", "  - "): 괄호강조(텍스트, 위치, 15)
            콜론내어쓰기(텍스트, 위치, 머리.strip()); 궁극자간(자간)
        다음문단(); return None


    def _지도통계생성(self, 색단계, 지역좌표):
        """선택 표의 수치를 7단계 색상으로 분류하여 지역별 PPT 지도를 만든다."""
        if not self.대상.CellShape:
            return None
        열표시 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
        열문자 = re.sub(r"[^A-z]", "", 열표시)
        열개수 = ord(열문자) - 64
        셀값 = self._선택표행추출(열개수)
        행 = [셀값[i:i + 열개수] for i in range(0, len(셀값), 열개수)]
        if len(행) < 2 or 열개수 < 2:
            return None

        def 자리처리(숫자):
            if 숫자 >= 100:
                자리수 = len(str(숫자).split(".")[0]) - 2
                return round(숫자, -자리수)
            if 숫자 >= 10:
                return round(숫자, -1)
            if 숫자 >= 1:
                return round(숫자, 1)
            return round(숫자, 2)

        from win32com.client.gencache import EnsureDispatch
        피피티 = EnsureDispatch("PowerPoint.Application")
        피피티.Visible = True
        프레젠테이션 = 피피티.Presentations.Add()

        for 순번 in range(1, 열개수):
            값목록 = [float(r[순번]) for r in 행[1:] if len(r) > 순번 and r[0] in 지역좌표 and r[순번] != ""]
            if not 값목록:
                continue
            최대값, 최소값 = max(값목록), min(값목록)
            마진값 = round((최대값 - 최소값) / 14)
            차이 = round((마진값 * 2 + 최대값 - 최소값) / 7)
            원단계 = [최대값 - 마진값 - 차이 * i for i in range(7)]
            단계 = [int(v) if 차이 >= 10 else 자리처리(v) for v in 원단계]
            슬라이드 = 프레젠테이션.Slides.Add(순번, 1)
            for 객체 in list(슬라이드.Shapes):
                객체.Delete()

            for 지역, 좌표문자열 in 지역좌표.items():
                점 = [tuple(map(float, p.split(","))) for p in 좌표문자열.split()]
                값 = next((float(r[순번]) for r in 행[1:] if len(r) > 순번 and r[0] == 지역 and r[순번] != ""), 최소값)
                색상 = 색단계[6]
                for 단계번호 in range(1, 7):
                    if 값 > 단계[단계번호]:
                        색상 = 색단계[단계번호 - 1]
                        break
                작성기 = 슬라이드.Shapes.BuildFreeform(EditingType=1, X1=점[0][0], Y1=점[0][1])
                for x, y in 점[1:]:
                    작성기.AddNodes(SegmentType=0, EditingType=0, X1=x, Y1=y)
                모양 = 작성기.ConvertToShape()
                모양.Fill.ForeColor.RGB = 색상
                모양.Line.Weight = 1
                모양.Line.ForeColor.RGB = 0
                중심X = sum(x for x, _ in 점) / len(점)
                중심Y = sum(y for _, y in 점) / len(점)
                글자 = 슬라이드.Shapes.AddTextbox(Orientation=1, Left=중심X - 28, Top=중심Y - 11, Width=56, Height=22)
                글자.TextFrame.TextRange.Text = 지역 + "\r" + format(값, ",")
                글자.TextFrame.TextRange.Font.Name = "맑은 고딕"
                글자.TextFrame.TextRange.Font.Size = 10
                글자.TextFrame.TextRange.Font.Bold = True
                글자.TextFrame.TextRange.ParagraphFormat.Alignment = 2

            제목 = 슬라이드.Shapes.AddTextbox(Orientation=1, Left=0, Top=0, Width=100, Height=22)
            제목.TextFrame.TextRange.Text = 행[0][순번] if len(행[0]) > 순번 else "기본"
            제목.TextFrame.TextRange.Font.Name = "맑은 고딕"
            제목.TextFrame.TextRange.Font.Size = 12
            제목.TextFrame.TextRange.Font.Bold = True
        return None

    def 충남지도통계(self, 색단계):
        지역좌표 = {"천안시":"514,138 523,127 550,136 551,143 561,149 566,147 589,171 589,174 589,177 589,180 608,191 605,198 614,207 608,214 599,205 587,208 591,217 572,233 538,214 528,224 537,231 542,255 537,256 530,241 518,239 514,246 499,242 508,228 517,227 520,210 528,206 522,188 524,167 519,163 520,150 514,138","공주시":"481,245 488,248 496,244 516,250 520,244 528,245 535,258 551,272 541,296 547,316 564,334 574,331 574,353 570,358 563,346 545,352 545,355 545,358 545,361 533,368 522,355 511,370 508,382 490,373 489,354 500,335 484,311 467,319 456,297 462,280 477,249 481,245","보령시":"346,295 357,303 364,304 370,302 373,312 380,312 397,322 398,336 405,346 399,353 395,366 398,388 409,396 399,413 380,421 354,413 352,397 357,384 354,374 349,374 345,364 361,358 361,355 344,343 338,345 342,329 340,315 339,299 346,295","아산시":"511,140 517,151 515,165 522,170 518,190 524,204 517,207 514,224 506,225 495,241 487,246 481,240 484,230 477,223 466,225 463,214 445,206 446,196 451,193 444,178 450,162 467,157 482,147 487,141 500,143 511,140","서산시":"296,118 313,113 330,115 340,139 335,162 345,167 352,184 371,182 382,188 390,200 387,210 375,219 370,240 358,249 336,249 331,227 327,251 322,262 307,255 305,240 301,220 304,196 297,184 293,172 312,160 320,148 316,140 300,138 297,129 296,118","논산시":"522,360 533,373 545,365 545,374 544,396 567,408 575,399 587,416 584,439 563,445 566,456 562,456 551,449 547,455 532,453 529,463 510,456 509,441 505,432 495,435 490,428 492,426 486,413 490,406 495,408 499,402 506,393 511,390 510,384 514,372 522,360","계룡시":"547,356 562,350 570,366 569,380 581,390 566,404 547,394 548,374 547,356","당진시":"334,109 344,97 354,99 353,103 379,114 378,118 386,125 390,128 394,121 401,118 428,128 433,146 441,161 438,177 447,191 444,193 436,201 431,198 424,207 411,192 402,191 392,200 383,186 372,178 354,181 348,165 338,161 343,140 340,128 334,109","금산군":"590,415 597,404 595,385 605,384 610,406 621,413 637,397 663,400 667,410 666,427 663,434 668,443 673,444 678,461 678,473 672,485 659,477 648,471 647,488 636,491 623,490 617,474 607,483 601,477 593,446 587,440 590,415","부여군":"506,384 507,390 504,391 494,404 489,402 482,413 487,424 486,428 485,432 478,429 466,435 457,436 453,446 454,461 443,456 445,442 430,435 431,420 414,418 408,421 400,416 413,395 401,385 398,367 403,353 412,347 420,356 432,356 438,344 448,346 449,365 462,365 471,370 480,363 486,362 486,366 486,371 487,375 506,384","서천군":"353,415 381,423 399,417 410,425 416,421 428,422 427,437 443,443 440,458 450,463 431,473 421,472 410,487 389,484 381,461 383,453 362,435 347,430 343,439 339,426 349,424 353,415","청양군":"394,315 400,321 401,334 408,346 413,343 421,354 430,354 437,341 450,344 451,362 463,362 472,367 480,360 486,359 486,353 498,336 483,314 466,322 453,298 459,280 446,276 440,292 424,290 423,295 414,312 405,308 394,315","홍성군":"335,252 359,251 371,241 373,247 370,259 382,258 382,247 406,239 416,239 414,247 418,249 421,259 424,259 424,267 416,274 417,281 413,283 421,289 421,295 413,309 405,306 391,314 381,309 375,310 371,297 363,302 358,300 345,292 341,294 333,285 336,280 332,267 339,262 335,252","예산군":"403,193 410,194 424,211 431,202 437,204 443,197 441,207 460,217 464,228 476,225 481,232 478,242 461,278 445,273 439,290 424,288 418,284 421,282 419,276 427,269 427,257 423,256 421,245 417,245 419,237 406,236 380,244 380,256 374,256 376,246 373,239 376,221 389,212 391,204 394,204 403,193","태안군":"287,127 294,160 286,172 300,199 297,223 302,258 327,334 320,341 294,325 287,273 280,271 285,243 273,237 272,223 257,240 240,239 241,226 261,225 259,214 246,208 234,226 232,221 233,201 244,171 252,176 255,173 250,159 272,148 282,153 282,145 282,137 282,129 287,127"}
        return self._지도통계생성(색단계, 지역좌표)

    def 강원지도통계(self, 색단계):
        지역좌표 = {"춘천시":"389,241 389,249 401,255 403,247 408,248 411,252 405,262 408,271 399,294 391,285 386,294 372,294 380,314 378,319 350,323 347,332 336,335 328,325 314,323 320,315 318,297 328,288 335,287 336,275 332,264 318,263 318,252 326,247 323,234 327,233 338,240 343,240 345,246 355,244 359,248 363,246 373,255 382,247 382,241 389,241","원주시":"373,401 380,403 381,413 388,411 387,396 394,392 398,383 404,396 408,393 425,397 432,404 429,408 430,415 423,418 423,429 433,436 438,443 447,443 454,437 456,440 454,446 447,453 438,449 433,458 422,459 419,450 408,446 396,452 398,468 395,470 382,469 373,473 362,461 365,436 365,417 370,409 373,401","강릉시":"582,376 589,354 598,354 602,367 605,365 609,365 611,366 623,363 624,348 622,346 623,334 607,317 601,315 601,309 578,284 576,276 564,277 546,282 541,279 530,289 530,292 530,295 531,298 534,301 534,310 539,308 552,309 562,318 568,336 561,341 562,354 558,357 554,358 550,365 555,370 560,367 571,367 574,369 576,375 578,377 582,376","동해시":"607,393 616,399 624,394 636,391 648,388 637,373 637,367 640,361 627,350 625,364 609,369 606,375 613,382 607,393","태백시":"600,454 603,435 609,423 617,421 620,438 617,444 619,465 633,467 633,484 630,488 622,486 610,485 609,486 606,482 604,483 600,493 591,491 593,484 590,478 594,476 595,469 601,469 600,454","속초시":"528,192 531,201 534,211 524,214 504,219 494,203 498,201 508,203 528,192","삼척시":"605,394 615,402 624,396 651,390 654,391 655,402 666,408 668,422 677,430 688,444 684,447 689,468 687,468 680,475 674,474 663,485 664,494 660,495 642,481 636,481 636,476 636,471 636,465 621,462 619,444 623,438 618,418 607,421 602,434 599,446 598,448 590,429 591,423 588,419 587,410 597,403 597,397 605,394","홍천군":"323,328 323,333 323,337 323,341 320,346 323,349 333,345 352,358 372,359 381,369 386,368 390,357 402,353 407,345 418,350 428,341 433,341 437,335 458,344 459,349 463,350 464,340 478,327 499,329 504,320 517,319 517,314 522,301 529,300 526,291 519,284 509,284 503,288 494,285 484,299 475,296 472,288 466,289 454,302 443,289 443,283 429,282 418,272 411,272 399,299 392,290 388,296 376,297 384,314 381,322 353,326 350,334 334,337 328,330 323,328","횡성군":"372,399 381,401 383,410 386,408 384,393 392,388 398,379 405,392 409,389 428,395 436,405 432,409 433,417 425,420 426,428 435,432 435,426 447,424 449,422 447,416 448,410 461,408 463,403 459,390 471,379 466,356 464,352 458,353 455,347 438,338 435,344 429,344 419,354 408,349 404,356 393,359 389,369 377,374 365,383 373,390 372,399","영월군":"588,492 591,484 588,477 593,475 593,469 585,467 568,457 557,465 545,463 538,454 533,455 530,446 532,440 523,436 519,437 515,432 508,432 502,422 496,424 495,435 492,437 486,430 480,432 479,424 473,410 467,405 463,411 453,411 450,414 452,422 448,427 437,428 436,434 441,441 447,440 454,434 458,438 457,446 469,454 473,452 481,451 484,457 472,469 475,473 481,470 493,470 501,480 518,478 527,485 541,484 566,500 565,494 573,485 588,492","평창군":"531,302 532,313 539,310 552,312 560,320 564,334 559,339 558,351 557,354 553,356 548,363 544,367 536,360 532,366 529,377 529,381 526,381 524,390 518,391 515,395 515,407 520,410 532,436 530,437 523,433 520,434 515,428 509,429 501,419 492,422 493,433 492,433 486,426 482,430 481,421 475,408 466,402 463,392 474,380 469,354 465,349 468,341 478,330 500,332 502,331 507,322 519,322 520,311 524,304 531,302","정선군":"594,467 599,466 598,454 586,430 587,424 585,420 584,409 594,401 595,395 605,391 609,383 604,376 606,369 605,367 601,371 596,361 595,357 590,357 585,379 577,379 571,370 559,371 555,373 548,368 543,370 537,364 533,371 531,378 532,383 529,383 527,393 521,392 519,394 518,404 521,406 535,440 532,445 534,452 539,451 546,461 557,462 568,455 581,462 594,467","철원군":"329,169 324,176 328,185 325,190 317,192 317,194 317,196 317,198 310,198 304,212 310,216 307,221 299,221 297,225 282,223 280,227 276,227 276,224 268,223 270,210 265,207 254,215 246,209 248,206 240,190 234,193 233,183 238,176 240,169 250,174 258,169 267,171 272,175 276,171 283,170 286,168 306,175 312,178 324,168 329,169","화천군":"332,169 350,170 353,165 358,167 365,164 373,170 380,191 378,202 386,206 385,226 391,233 390,238 380,238 380,241 380,244 380,247 373,252 363,241 360,243 354,241 348,243 344,238 338,237 327,228 319,232 322,246 314,250 305,251 301,224 308,223 313,215 307,211 312,200 319,200 319,194 326,192 330,184 327,177 332,169","양구군":"376,171 388,166 423,174 436,167 440,172 438,184 433,187 433,198 424,212 428,222 425,227 432,236 431,243 423,238 421,247 411,249 409,245 402,244 400,251 391,246 393,231 388,225 388,204 381,200 383,190 376,171","인제군":"437,165 453,157 460,161 460,173 470,171 473,186 479,186 478,191 489,195 495,190 497,192 497,194 497,196 497,198 491,201 500,218 492,223 493,242 507,243 510,255 504,262 506,281 501,285 494,279 483,296 477,294 473,285 463,286 454,299 447,289 446,279 431,279 420,269 411,269 408,261 410,257 416,250 424,249 425,242 433,246 434,234 427,227 431,223 427,214 435,198 436,189 441,186 442,170 437,165","고성군":"474,101 481,98 490,108 488,113 502,134 500,139 515,163 527,190 508,201 501,199 499,198 499,190 495,188 487,191 480,188 480,183 475,183 471,168 462,171 462,159 453,154 471,133 474,101","양양군":"496,225 504,222 533,214 545,230 552,242 557,245 560,253 574,273 566,274 548,279 540,276 528,288 521,281 508,281 507,263 514,256 509,240 496,238 496,225"}
        return self._지도통계생성(색단계, 지역좌표)


    def 행안궁극의정리(self, 이미지, 옵션):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s*", 텍스트)
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]
        def 궁극자간(기준):
            self.대상.MovePos(6); 시작 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝 = int(self.대상.KeyIndicator()[5]); self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 길이 = len(self.블록스캔()[1]); self.캔슬()
            if 길이 < 기준 and 끝 > 시작:
                현재 = 끝; 카운트 = 0
                while 현재 == 끝 and 카운트 < 15:
                    카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 현재 = int(self.대상.KeyIndicator()[5])
                    if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()
        def 괄호서식(전체, 위치, 진하게=False):
            for 매치 in re.finditer(r"\([^()]*\)", 전체):
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start())); self.대상.HAction.Run("Select"); self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                if 진하게: self.진하게()
                self.글자크기(15); self.캔슬()

        self.기본글자(); self.글자색(0, 0, 0); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0); self.줄간격(150); self.왼쪽정렬(); self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip(); 텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트); 텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 in ("행안표", "행안연간일정", "행안단계") and not re.match(r"^표", 텍스트): self.방금처리 = 0
        처리함 = True
        if 명령("소제목"):
            self.소제목카운트 += 1; 내용 = re.sub(r"^(소제목\s*:|소제목)\s*", "", 텍스트, count=1); self.문장(f"{self.소제목카운트}. {self.행안옛날소제목(내용) if False else 내용}"); 줄선택(); self.폰트("함초롬바탕"); self.글자크기(15); self.진하게(); self.캔슬(); self.대상.MovePos(6)
        elif 명령("가제목"):
            self.가제목카운트 += 1; 내용 = re.sub(r"^(가제목\s*:|가제목)\s*", "", 텍스트, count=1); self.문장(f"{self.가숫자[self.가제목카운트]} { 내용}"); 줄선택(); self.폰트("함초롬바탕"); self.글자크기(14); self.진하게(); self.캔슬(); self.대상.MovePos(6)
        elif 명령("엔터"): self.백스페이스(); self.엔터(1); self.백스페이스()
        elif 명령("글상자"): self.백스페이스(); self.행안글상자(인자목록(텍스트)); self.백스페이스()
        elif 명령("참고박스"): self.백스페이스(); self.부여참고박스(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표지"): self.백스페이스(); self.부여표지(텍스트.split(":", 1)[1].strip(), 이미지[0:3]); self.백스페이스()
        elif 명령("서론"): self.백스페이스(); self.부여서론(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"): self.백스페이스(); self.부여붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("한줄일정"): self.백스페이스(); self.부여한줄일정(인자목록(텍스트)); self.백스페이스()
        elif re.match(r"^표\s*:?\s*연간일정", 텍스트) or (self.방금처리 == "행안연간일정" and re.match(r"^표", 텍스트)):
            텍스트 = re.sub(r"^표\s*:?\s*연간일정", "표:연간일정", 텍스트, count=1); self.백스페이스(); self.행안연간일정(인자목록(텍스트), 옵션); self.백스페이스()
        elif re.match(r"^표\s*:?\s*단계", 텍스트) or (self.방금처리 == "행안단계" and re.match(r"^표", 텍스트)):
            텍스트 = re.sub(r"^표\s*:?\s*단계", "표:단계", 텍스트, count=1); self.백스페이스(); self.행안단계(인자목록(텍스트), 옵션, 이미지); self.백스페이스()
        elif re.match(r"^표\s+", 텍스트):
            텍스트 = re.sub(r"^(표\s*:|표)\s*", "표:", 텍스트, count=1); 텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트); self.백스페이스(); self.행안표(인자목록(텍스트)); self.백스페이스()
        elif 명령("요약"):
            내용 = re.sub(r"^(요약\s*:|요약)\s*", "", 텍스트, count=1)
            if 옵션 == 1: self.백스페이스(); self.행안옛날요약(내용); self.백스페이스()
            else: self.문장("요약"); self.엔터(1); self.문장(" " + 내용); 줄선택(); self.폰트("함초롬바탕"); self.글자크기(12); self.진하게(); self.캔슬()
        elif 명령("제목"):
            내용 = re.sub(r"^(제목\s*:|제목)\s*", "", 텍스트, count=1)
            if 옵션 == 1: self.백스페이스(); self.행안옛날제목(내용); self.백스페이스()
            else: self.문장(내용); 줄선택(); self.폰트("HY헤드라인M"); self.글자크기(20); self.글자간격(-8); self.진하게(); self.캔슬()
        elif 명령("대면보고") or 명령("서면보고"):
            종류 = "대면보고" if 텍스트.startswith("대면보고") else "서면보고"; 내용 = re.sub(rf"^({종류}\s*:|{종류}|)\s*", "", 텍스트, count=1)
            self.문장(종류 + " / "); self.오늘날짜무공백(); self.문장(" / " + 내용.strip()); 줄선택(); self.폰트("맑은 고딕"); self.글자크기(12 if len(내용.strip()) > 25 else 13); self.오른쪽정렬(); self.캔슬()
        elif 명령("설명"):
            내용 = re.sub(r"^(설명\s*:|설명|)\s*", "", 텍스트, count=1); self.문장("< " + 내용.strip() + " >"); 줄선택(); self.폰트("맑은 고딕"); self.글자크기(13); self.가운데정렬(); self.진하게(); self.캔슬()
        else: 처리함 = False
        if 처리함: 다음문단(); return None

        사양 = None
        if 텍스트.startswith(("ㅁ", "□", "네모 ", "네모:")): 사양 = (r"^(ㅁ|□||퀀0|네모\s*:|네모|)\s*", " □ ", "HY헤드라인M" if 옵션 else "함초롬바탕", 16 if 옵션 else 15, -24 if 옵션 else -30, 10 if 옵션 else 0, 5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ", "원:")): 사양 = (r"^(ㅇ|○|❍||원\s*:|원)\s*", "  ○ ", "바탕체" if 옵션 else "함초롬바탕", 15, -37.4, 7 if 옵션 else 0, 9)
        elif 텍스트.startswith(("-", "바 ", "바:")): 사양 = (r"^(-|바\s*:|바)\s*", "   - ", "함초롬바탕", 15, -38.2 if 옵션 else -35, 0, 9)
        elif 텍스트.startswith(("*", "별 ", "별:")): 사양 = (r"^(\*|별\s*:|별)\s*", "    * ", "맑은 고딕", 13, -35.1, 0, 10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ", "당구:", "당구장:")): 사양 = (r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "    ※ ", "맑은 고딕", 13, -46.8, 0, 10)
        if 사양:
            패턴, 머리, 폰트, 크기, 내어, 위, 자간 = 사양; 텍스트 = re.sub(패턴, 머리, 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트(폰트); self.글자크기(크기); self.내어쓰기(내어)
            if 위: self.문단위(위)
            self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet()
            if 머리 in ("  ○ ", "   - "): 괄호서식(텍스트, 위치, 머리 == "  ○ ")
            궁극자간(자간)
        다음문단(); return None

    def 우본궁극의정리(self, 이미지):
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 명령(이름): return re.match(rf"^{이름}\s*:\s*", 텍스트) or re.match(rf"^{이름}\s+", 텍스트)
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]
        def 궁극자간(기준):
            self.대상.MovePos(6); 시작줄 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝줄 = int(self.대상.KeyIndicator()[5])
            self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 길이 = len(self.블록스캔()[1]); self.캔슬()
            if 길이 < 기준 and 끝줄 > 시작줄:
                카운트 = 0; 현재 = 끝줄
                while 현재 == 끝줄 and 카운트 < 15:
                    카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 현재 = int(self.대상.KeyIndicator()[5])
                    if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()
        def 부분서식(전체, 위치, 패턴, 크기=13, 진하게=False):
            for 매치 in re.finditer(패턴, 전체):
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start())); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end()))
                self.글자크기(크기)
                if 진하게: self.진하게()
                self.캔슬()

        self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0); self.줄간격(170); self.기본정렬(); self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip(); 텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트); 텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if self.방금처리 == "우본표" and not re.match(r"^(표\s*:|표)\s+", 텍스트): self.방금처리 = 0
        if self.방금처리 == "컨트롤엔터" and not re.match(r"^(컨트롤엔터\s*:|컨트롤엔터)\s+", 텍스트): self.방금처리 = 0
        처리함 = True
        if 명령("제목"): self.백스페이스(); self.우본제목(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("소제목"): self.백스페이스(); self.소제목카운트 += 1; self.우본소제목(self.소제목카운트, 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("중제목"):
            self.백스페이스(); self.소제목카운트 = 0; self.중제목카운트 += 1
            if self.중제목카운트 == 13: self.중제목카운트 = 1
            self.우본중제목(self.로마숫자[self.중제목카운트], 텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("개요"): self.백스페이스(); self.우본개요1(인자목록(텍스트)); self.백스페이스()
        elif 명령("요약"): self.백스페이스(); self.우본요약(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("표"):
            self.백스페이스(); 텍스트 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 텍스트); self.우본표(인자목록(텍스트)); self.백스페이스()
        elif 명령("대상표"): self.백스페이스(); self.우본대상표(); self.백스페이스()
        elif 명령("일정표"): self.백스페이스(); self.우본일정표(); self.백스페이스()
        elif 명령("예산표"): self.백스페이스(); self.우본예산표(); self.백스페이스()
        elif 명령("안전관리자"): self.백스페이스(); self.우본안전관리자(); self.백스페이스()
        elif 명령("예방담당관"): self.백스페이스(); self.우본예방담당관(); self.백스페이스()
        elif 명령("표지"): self.백스페이스(); self.우본표지(텍스트.split(":", 1)[1].strip(), 이미지); self.백스페이스()
        elif 명령("목차"): self.백스페이스(); self.우본목차2(이미지); self.백스페이스()
        elif 명령("글상자"): self.백스페이스(); self.우본글상자2(); self.백스페이스()
        elif 명령("순서도"): self.백스페이스(); self.우본3단순서도(); self.백스페이스()
        elif 명령("참고"): self.백스페이스(); self.우본참고(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif 명령("붙임"): self.백스페이스(); self.우본붙임(텍스트.split(":", 1)[1].strip()); self.백스페이스()
        elif re.match(r"^컨트롤엔터\s*", 텍스트):
            self.백스페이스(); self.페이지엔터(); self.방금처리 = "컨트롤엔터"; self.딜리트(); self.궁극의정리위치보정 -= 1; self.캔슬(); self.대상.MovePos(11); return None
        elif 명령("설명"):
            내용 = re.sub(r"^(설명\s*:|설명|)\s*", "", 텍스트, count=1); self.문장("< " + 내용.strip() + " >"); 줄선택(); self.중고딕(); self.글자크기(13); self.기본글자(); self.문단위(10); self.가운데정렬(); self.진하게(); self.캔슬(); self.대상.MovePos(6)
        else: 처리함 = False
        if 처리함: 다음문단(); return None

        사양 = None
        if 텍스트.startswith(("ㅁ", "□", "네모 ", "", "네모:")): 사양 = (r"^(ㅁ|□||네모\s*:|네모|)\s*", "□ ", "HY헤드라인M", 15, -22.5, 9, 5)
        elif 텍스트.startswith(("진한원 ", "진한원:")): 사양 = (r"^(진한원\s*:|진한원)\s*", " ㅇ ", "휴먼명조", 15, -30, 3, None)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ", "원:")): 사양 = (r"^(ㅇ|○|❍||원\s*:|원)\s*", " ㅇ ", "휴먼명조", 15, -30, 3, 9)
        elif 텍스트.startswith(("-", "바 ", "바:")): 사양 = (r"^(-|바\s*:|바)\s*", "   - ", "휴먼명조", 15, -37.4, 0, 9)
        elif 텍스트.startswith(("*", "별 ", "별:")): 사양 = (r"^(\*|별\s*:|별)\s*", "     * ", "맑은 고딕", 13, -44.4, 0, 10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ", "당구:", "당구장:")): 사양 = (r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "     ※ ", "맑은 고딕", 13, -49.3, 0, 10)
        if 사양:
            패턴, 머리, 폰트, 크기, 내어, 위, 자간 = 사양; 텍스트 = re.sub(패턴, 머리, 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트(폰트); self.글자크기(크기); self.내어쓰기(내어)
            if 위: self.문단위(위)
            self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet()
            if 머리 == " ㅇ " and 텍스트.startswith("진한원"): 부분서식(텍스트, 위치, r"ㅇ.*", 15, True)
            elif 머리 in (" ㅇ ", "   - "): 부분서식(텍스트, 위치, r"\([^()]*\)", 15, 머리 == " ㅇ ")
            if 머리 == " ㅇ ": self.문장내어쓰기()
            if 자간: 궁극자간(자간)
        다음문단(); return None

    def 보기변환(self, 종류):
        """선택한 다섯 개 보기 문단을 시험지용 보기 표로 변환한다.

        원본의 1·2·3단/국어·영어 분기는 표 크기와 항목 기호만 다르고
        셀 구성 순서는 같으므로 한 번의 소스 구현으로 공유한다.
        """
        결과텍스트 = []
        self.대상.InitScan(1, 255)
        try:
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                if 블록스캔값 not in (2, 3):
                    break
                결과텍스트.append(텍스트.replace("\r", "").replace("\n", ""))
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
        finally:
            self.대상.ReleaseScan()
        if not 결과텍스트:
            return None

        self.대상.HAction.Run("Delete")
        설정 = {
            "3단국어": ([6, 22, 6, 22, 6, 22], [2, 2, 5, 8], ["ㄱ.", "ㄴ.", "ㄷ.", "ㄹ.", "ㅁ."], False),
            "3단영어": ([6, 22, 6, 22, 6, 22], [2, 2, 5, 8], ["(A)", "(B)", "(C)", "(D)", "(E)"], False),
            "2단국어": ([6, 39.5, 6, 39.5], [2, 2, 5, 5, 5], ["ㄱ.", "ㄴ.", "ㄷ.", "ㄹ.", "ㅁ."], True),
            "2단영어": ([6, 39.5, 6, 39.5], [2, 2, 5, 5, 5], ["(A)", "(B)", "(C)", "(D)", "(E)"], True),
            "1단국어": ([6, 92], [2, 2, 5, 5, 5, 5, 5], ["ㄱ.", "ㄴ.", "ㄷ.", "ㄹ.", "ㅁ."], True),
            "1단영어": ([6, 92], [2, 2, 5, 5, 5, 5, 5], ["(A)", "(B)", "(C)", "(D)", "(E)"], True),
        }
        if 종류 not in 설정:
            return None
        열너비, 행높이, 기호, 높이보정 = 설정[종류]
        self.표만들기(열너비, 행높이)
        self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableCellBlockExtend")
        self.셀여백제로(); self.표테두리타입(0, 0, 0, 0); self.표내부선타입(0, 0); self.신명중명조(); self.글자크기(11); self.대상.HAction.Run("Cancel")
        # 원본 레이아웃: 상단 외곽, 중앙 <보 기>, 7x2 항목 영역.
        self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableUpperCell"); self.대상.HAction.Run("TableUpperCell"); self.대상.HAction.Run("TableColBegin")
        self.표테두리타입(1, 1, 1, 1); self.대상.HAction.Run("Cancel")
        self.대상.HAction.Run("TableRightCellAppend"); self.대상.HAction.Run("TableRightCellAppend"); self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableRightCellAppend"); self.대상.HAction.Run("TableUpperCell"); self.대상.HAction.Run("TableMergeCell")
        self.셀나누기(7, 2); self.표테두리단일선("하", 1, 1); self.대상.HAction.Run("TableLeftCell"); self.표테두리단일선("하", 1, 1)
        self.대상.HAction.Run("TableLeftCell"); self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableLeftCell"); self.대상.HAction.Run("TableLeftCell"); self.대상.HAction.Run("TableLowerCell"); self.대상.HAction.Run("TableMergeCell")
        self.대상.HAction.Run("ParagraphShapeAlignCenter"); self.문장("<보 기>")
        for 순번, 항목기호 in enumerate(기호):
            self.대상.HAction.Run("TableRightCellAppend"); self.대상.HAction.Run("ParagraphShapeAlignRight"); self.문장(항목기호)
            self.대상.HAction.Run("TableRightCellAppend")
            if 순번 < len(결과텍스트): self.문장(" " + 결과텍스트[순번])
            if 높이보정: self.셀높이지정(1)
        self.대상.HAction.Run("MoveRight"); self.대상.HAction.Run("BreakPara")
        return None

    def 충남맨앞제거(self, 개수):
        def 맨앞제거():
            self.대상.MovePos(6)
            self.대상.HAction.Run("Select")
            self.대상.MovePos(7)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos")))
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 개수))
            self.딜리트()
            self.대상.MovePos(10)

        시작지점 = self.블록첫위치()
        끝지점 = self.블록끝위치()
        if 시작지점.Item("Para") is None:
            return None
        self.캔슬()
        self.대상.SetPosBySet(끝지점)
        마지막위치 = self.대상.GetPosBySet().Item("Para")
        self.대상.SetPosBySet(시작지점)
        지금위치 = 아까위치 = self.대상.GetPosBySet().Item("Para")
        맨앞제거()
        if 시작지점.Item("Para") != 끝지점.Item("Para"):
            while True:
                지금위치 = self.대상.GetPosBySet().Item("Para")
                if 지금위치 == 아까위치:
                    break
                맨앞제거()
                if 지금위치 >= 마지막위치:
                    break
                아까위치 = 지금위치
        self.대상.SetPosBySet(self.좌표(끝지점.Item("List"), 끝지점.Item("Para"), 0))
        self.대상.MovePos(7)
        self.대상.HAction.Run("Select")
        self.대상.SetPosBySet(시작지점)

    def _기관사진표(self, 단수, 열너비, 사진너비, 사진높이, 제목높이, 폰트, 테두리, 괄호):
        from tkinter import filedialog

        이름 = filedialog.askopenfilenames(title="Open File", filetypes=[("image files", (".png", ".jpg"))])
        self.가운데정렬()
        self.표만들기([열너비] * 단수, [사진높이, 제목높이])
        self.표전체()
        self.표테두리타입(테두리, 0, 0, 0)
        self.표내부선타입(테두리, 0)
        if 테두리:
            self.표테두리굵기(6, 6, 0, 0)
            self.표내부선굵기(6, 0)
        self.글자크기(12)
        self.가운데정렬()
        self.진하게()
        self.폰트(폰트)
        self.대상.HAction.Run("Copy")
        self.캔슬()
        self.표처음()
        for i, 경로 in enumerate(이름):
            if i != 0:
                self.표오른쪽(1)
            self.사진넣기절대값(경로, 사진너비, 사진높이)
            if i % 단수 != 단수 - 1:
                continue
            for 제목경로 in 이름[i - 단수 + 1:i + 1]:
                self.표오른쪽(1)
                매치 = re.search(r"\(([^()]+)\)(?!.*\()", 제목경로)
                self.문장(괄호[0] + (매치.group(1) if 매치 else "") + 괄호[1])
            if i != len(이름) - 1:
                self.아래로붙이기()
        self.표나가기2()

    def 경기신보사진3단(self):
        self._기관사진표(3, 51, 51, 33, 7, "경기천년제목 Light", 0, "()")

    def 경기신보사진2단(self):
        self._기관사진표(2, 79, 75, 45, 7, "경기천년제목 Light", 0, "()")

    def 충남사진3단(self):
        self._기관사진표(3, 50, 50, 30, 5, "맑은 고딕", 1, "<>")

    def 충남사진2단(self):
        self._기관사진표(2, 75, 75, 50, 5, "맑은 고딕", 1, "<>")

    def _보도자료본문서식(self, 글자크기, 줄간격=160):
        텍스트 = "\r\n\r\n".join(re.split(r"(?:\r\n)+", self.블록텍스트()))
        self.문단위(0)
        self.문단아래(0)
        self.내어쓰기(0)
        self.문단여백(0, 0)
        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.줄간격(줄간격)
        self.기본정렬()
        self.폰트("휴먼명조")
        self.글자크기(글자크기)
        self.문장(텍스트)

    def 충남청보도자료본문서식(self):
        self._보도자료본문서식(15)

    def 충남보도자료본문(self):
        self._보도자료본문서식(15)

    def 홍성보도자료본문서식(self):
        self._보도자료본문서식(14)

    def 블록엔터정리블록(self):
        결과텍스트 = re.sub(r"(\r\n)+", "\r\n", "".join(self._블록조각()))
        self.백스페이스()
        시작지점 = self.현재위치()
        self.문장(결과텍스트)
        종료지점 = self.현재위치()
        self.대상.SetPosBySet(시작지점)
        self.대상.HAction.Run("Select")
        self.대상.SetPosBySet(종료지점)

    def 점수합산(self):
        결과리스트 = self.글자좌표리스트(r"\[[^\[^점\]]*점\]")
        self.대상.MovePos(3)
        self.대상.HAction.Run("BreakPara")
        합계점수 = 0
        self.표만들기([10, 10, 10, 10, 10], [10])
        for i in range(len(결과리스트)):
            숫자만 = re.sub(r"[^0-9.]", "", 결과리스트[i][2])
            if 숫자만 in ("", ".", ".."):
                self.문장("오류")
            else:
                self.문장(str(숫자만))
                합계점수 = Decimal(str(합계점수)) + Decimal(str(숫자만))
            self.대상.HAction.Run("TableRightCellAppend")
        self.표탈출()
        self.문장("합계점수는 " + str(합계점수) + " 입니다!")

    def 경기신보회색박스(self, 내용):
        self.가운데정렬()
        self.표만들기([150], [7, 10])
        self.표배경색(229, 229, 229)
        self.폰트("경기천년제목 Medium")
        self.글자크기(12)
        self.가운데정렬()
        self.문장(내용[0] if len(내용) >= 1 else "회색박스")
        self.표오른쪽(1)
        self.폰트("경기천년제목 Light")
        self.글자크기(12)
        self.줄간격(130)
        self.셀여백지정(2, 2, 2, 2)
        self.표나가기2()

    def 부여참고박스(self, 내용):
        self.표만들기([205.5 - self.문단여백측정()], [10])
        self.자간헌터(0)
        self.글자간격(-10)
        self.글자크기(15)
        self.폰트("바탕")
        self.진하게()
        self.문장("[참고]\r\n")
        self.기본글자()
        self.글자크기(14)
        입력내용 = "\r\n".join(part.strip() for part in 내용.split("엔터 "))
        self.문장(입력내용)
        self.표나가기2()

    def 경기요약(self, 내용):
        self.표만들기([205.5 - self.문단여백측정()], [8])
        self.내어쓰기(-28.3)
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(6, 6, 0, 0)
        self.자간헌터(0)
        self.셀여백지정(2, 2, 2, 2)
        self.폰트("경기천년바탕 Regular")
        self.글자크기(14)
        self.줄간격(150)
        입력내용 = "\r\n".join("  " + part.strip() for part in 내용.split("엔터 "))
        self.문장(입력내용)
        self.표나가기2()

    def 공항서단표(self, 단):
        self.표만들기([(180 - self.문단여백측정()) / 단] * 단, [6] * (4 if 단 == 3 else 2))
        self.공항서표서식(2 if 단 == 3 else 1)
        self.표처음()
        self.문장("구분")
        for i in range(1, 단):
            self.표오른쪽(1)
            self.문장("내용")
        self.표나가기2()


class Hwp2InstitutionFeatureMixin:
    def _기관궁극정리(self, 이미지, 설정):
        """2번 라이브러리의 공통 명령 문단과 글머리 서식을 처리한다."""
        def 줄선택(): self.대상.MovePos(6); self.대상.HAction.Run("Select"); self.대상.MovePos(7)
        def 다음문단(): self.캔슬(); self.대상.MovePos(10)
        def 인자목록(값): return [x.strip() for x in 값.split(":")[1:]]
        def 부분서식(전체, 위치, 패턴, 크기, 진하게=False):
            for 매치 in re.finditer(패턴, 전체):
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.start())); self.대상.HAction.Run("Select")
                self.대상.SetPosBySet(self.좌표(위치.Item("List"), 위치.Item("Para"), 위치.Item("Pos") + 매치.end())); self.글자크기(크기)
                if 진하게: self.진하게()
                self.캔슬()
        def 궁극자간(기준):
            self.대상.MovePos(6); 시작 = int(self.대상.KeyIndicator()[5]); self.대상.MovePos(7); 끝 = int(self.대상.KeyIndicator()[5]); self.대상.HAction.Run("Select"); self.대상.HAction.Run("MoveLineBegin"); 길이 = len(self.블록스캔()[1]); self.캔슬()
            if 길이 < 기준 and 끝 > 시작:
                현재 = 끝; 카운트 = 0
                while 현재 == 끝 and 카운트 < 15:
                    카운트 += 1; self.대상.HAction.Run("CharShapeSpacingDecrease"); 현재 = int(self.대상.KeyIndicator()[5])
                    if 카운트 > 8: self.대상.HAction.Run("CharShapeWidthDecrease")
            self.캔슬()

        self.기본글자(); self.글자간격(0); self.글자장평(100); self.문단여백(0, 0); self.문단위(0); self.문단아래(0); self.줄간격(설정.get("줄간격", 160))
        if 설정.get("정렬") == "기본": self.기본정렬()
        else: self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1].strip(); 텍스트 = re.sub(r"\s*:\s*", ": ", 텍스트); 텍스트 = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", 텍스트); 텍스트 = re.sub(r"\s*·\s*", "·", 텍스트); 텍스트 = re.sub(r"\(\s*", "(", 텍스트)
        if not 텍스트:
            self.캔슬()
            return None
        for 명령, 호출정보 in 설정.get("명령", {}).items():
            if not (re.match(rf"^{명령}\s*:\s*", 텍스트) or re.match(rf"^{명령}\s+", 텍스트)):
                continue
            메서드명, 인자형 = 호출정보; 내용 = re.sub(rf"^({명령}\s*:|{명령})\s*", "", 텍스트, count=1); self.백스페이스(); 메서드 = getattr(self, 메서드명)
            if 인자형 == "문자열": 메서드(내용)
            elif 인자형 == "목록": 메서드(인자목록("임시:" + 내용))
            elif 인자형 == "목록이미지": 메서드(인자목록("임시:" + 내용), 이미지)
            elif 인자형 == "이미지": 메서드(이미지)
            elif 인자형 == "문자열이미지": 메서드(내용, 이미지)
            elif 인자형 == "이미지문자열": 메서드(이미지, 내용)
            elif 인자형 == "카운트문자열":
                self.소제목카운트 += 1; 메서드(str(self.소제목카운트), 내용)
            elif 인자형 == "로마문자열":
                self.소제목카운트 += 1; 메서드(self.로마숫자[self.소제목카운트], 내용)
            elif 인자형 == "무인자": 메서드()
            self.백스페이스(); 다음문단(); return None
        if re.match(r"^설명\s*", 텍스트):
            내용 = re.sub(r"^(설명\s*:|설명)\s*", "", 텍스트, count=1); self.문장("< " + 내용 + " >"); 줄선택(); self.중고딕(); self.글자크기(13); self.가운데정렬(); self.진하게(); self.캔슬(); 다음문단(); return None

        글머리 = None
        if 텍스트.startswith(("ㅁ", "□", "네모 ", "네모:")): 글머리 = (r"^(ㅁ|□||퀀0|네모\s*:|네모|)\s*", " □ ", "HY헤드라인M", 16, -24, 10, 5)
        elif 텍스트.startswith(("ㅇ", "○", "❍", "", "원 ", "원:")): 글머리 = (r"^(ㅇ|○|❍||원\s*:|원)\s*", "  ○ ", "휴먼명조", 15, -32, 5, 9)
        elif 텍스트.startswith(("-", "바 ", "바:")): 글머리 = (r"^(-|바\s*:|바)\s*", "    - ", "휴먼명조", 15, -35, 3, 9)
        elif 텍스트.startswith(("*", "별 ", "별:")): 글머리 = (r"^(\*|별\s*:|별)\s*", "     * ", "맑은 고딕", 13, -40, 2, 10)
        elif 텍스트.startswith(("※", "당구 ", "당구장 ", "당구:", "당구장:")): 글머리 = (r"^(※|당구장\s*:|당구\s*:|당구장|당구)\s*", "    ※ ", "맑은 고딕", 13, -42, 2, 10)
        if 글머리:
            패턴, 머리, 폰트, 크기, 내어, 위, 자간 = 글머리; 텍스트 = re.sub(패턴, 머리, 텍스트, count=1); self.문장(텍스트); 줄선택(); self.폰트(폰트); self.글자크기(크기); self.내어쓰기(내어); self.문단위(위); self.캔슬(); self.대상.MovePos(6); 위치 = self.대상.GetPosBySet()
            if 머리 in ("  ○ ", "    - "): 부분서식(텍스트, 위치, r"\([^()]*\)", 크기, 머리 == "  ○ ")
            궁극자간(자간)
        다음문단(); return None

    def _공기업정리설정(self, 제목, 소제목, 요약="토주공요약", 표=None, 표지="강원표지", 참고="강원참고", 붙임="강원붙임"):
        명령 = {"제목": (제목, "문자열"), "중제목": ("강원중제목", "문자열"), "보고자": ("강원보고자", "문자열"), "표지": (표지, "문자열이미지"), "소제목": (소제목, "카운트문자열"), "요약": (요약, "문자열"), "참고": (참고, "문자열"), "붙임": (붙임, "문자열")}
        if 표: 명령["표"] = (표, "목록")
        return {"명령": 명령, "줄간격": 160}

    def 부교공궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("부교공제목", "여광항소제목"))
    def 여광항궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("여광항제목", "여광항소제목"))
    def 석유공궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("석유공제목", "석유공소제목", "석유공요약"))
    def 공항공궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("공항공제목", "공항공소제목", 참고="공항공참고", 붙임="공항공붙임"))
    def 가스공궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("가스공제목", "가스공소제목", 표="가스공표", 표지="가스공표지"))
    def 토주공궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("토주공제목", "토주공소제목"))
    def 해경궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("토주공제목", "토주공소제목"))
    def 한수원궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("한수원제목", "한수원소제목", "강원요약", 표="한수원표"))
    def 세종궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("세종제목", "세종소제목", "세종요약", 표지="강원표지", 참고="세종참고", 붙임="세종붙임"))
    def 전남교궁극의정리(self, 이미지): return self._기관궁극정리(이미지, self._공기업정리설정("전남교제목", "전남교소제목", 표="우본표", 표지="세종교표지", 참고="우본참고", 붙임="우본붙임"))

    def 인진궁극의정리(self, 이미지):
        설정 = self._공기업정리설정("인진제목", "강원소제목", 표="인진표", 표지="인진표지", 참고="인진참고", 붙임="인진붙임")
        설정["명령"]["보도자료"] = ("인진보도자료", "문자열")
        return self._기관궁극정리(이미지, 설정)

    def 충남주자사업계획서(self):
        self.새창(); self.문서여백(20, 20, 10, 10, 10, 10); self.충남주자서식("2", "사업계획서"); self.가운데정렬(); self.폰트("휴먼명조"); self.글자크기(16); self.진하게(); self.문장("충청남도 주민자치회 제안사업 사업계획서\r\n\r\n")
        self.기본정렬()
        for 내용 in ("Ⅰ. 일반 현황", "  1. 읍·면·동 현황", "   ◦ 인구/세대/면적, 지역여건·특성 등", "  2. 주민자치회 기본 현황", "   ◦ 결성일자, 위원수(연령별 구성), 회의 개최 등\r\n   ◦ 예산 현황(시군비, 자체예산 등), 간사 현황, 전용공간 현황 등\r\n   ◦ 주요 활동 내역"):
            self.문장(내용 + "\r\n")
        self.표만들기([8, 28, 19, 17, 40, 10], [6] * 4); self.표전체(); self.캔슬(); self.표처음()
        for 값 in ("연번", "사업명", "기간", "대상인원", "사업내용", "비고", "1"):
            self.문장(값); self.표오른쪽(1)
        self.표나가기2(); self.문장("\r\nⅡ. 사업 계획서\r\n"); self.줄간격(140); self.문장("[작성요령]\r\n 1. 사업성격 및 평가기준이 잘 드러나도록 자유롭게 작성(양식 편집 가능)\r\n 2. 사업선정 경위, 지속가능성 여부에 대한 자체 판단 등 포함 작성\r\n 3. 심사항목을 참고하여 사례의 추진배경 및 과정, 주요내용, 성과 등 기재\r\n 4. 작성 서류는 공모신청서를 포함하여 10쪽을 넘지 않도록 작성\r\n")
        for 내용 in ("  1. 사업명 : ", "  2. 사업개요", "   ◦ 사업기간 : \r\n   ◦ 장    소 : \r\n   ◦ 추진주체 : \r\n   ◦ 사 업 량 : ", "  3. 추진배경 및 필요성", "    - 지역특성 반영, 주민총회 개최 여부, 의견수렴 과정 등\r\n\r\n", "  4. 추진과정 및 내용", "    - 기획에서부터 실행, 의견 수렴, 평가에 대해 구체적 서술\r\n\r\n", "  5. 세부추진계획"):
            self.문장(내용 + "\r\n")
        self.표만들기([25, 43, 60], [6] * 4); self.표처음()
        for 값 in ("일정", "추진단위", "세부추진내용"):
            self.문장(값); self.표오른쪽(1)
        self.표나가기2(); self.문장("  6. 추진배경 및 필요성\r\n   ◦ 사회적 기여도\r\n       * 해당 사례의 파급 효과, 확산 가능성, 사회문제 해결 등 기술\r\n\r\n\r\n   ◦ 사업수행 단체에 대한 기여도\r\n       * 본 사업 지원의 기대효과 기술\r\n\r\n\r\n  7. 기타\r\n   - 사업 추진시 예상되는 장애요인 및 해결방안 등\r\n")
        self.페이지엔터(); self.문장("Ⅲ. 지방보조사업 재정운영 계획서\r\n[작성요령]\r\n 1. 사업예산과 경상예산 구분, 지방보조금과 자부담 구분\r\n 2. 세입예산과 세출예산 합계 일치\r\n 3. 자부담이 있는 경우 예산확보 방안 및 증빙서 첨부\r\n\r\n  1. 세입예산\r\n")
        self.표만들기([13, 40, 97], [7] * 9); self.표처음()
        for 값 in ("비 목", "세입예산", "합 계", "자체\r\n수입", "소 계", "ㅇ 산출기초", "보조금\r\n수입"):
            self.문장(값); self.표오른쪽(1)
        self.표나가기2(); self.오른쪽정렬(); self.문장("(단위 : 천원)\r\n  2. 세출예산\r\n"); self.표만들기([21, 21, 21, 21, 60], [8] * 7); self.표처음()
        for 값 in ("구 분", "단위사업", "지출항목", "금액", "산출내역", "합계", "보조금", "기타"):
            self.문장(값); self.표오른쪽(1)
        self.표나가기2(); return None

    def 인진되돌리기(self):
        """서식화된 인진 문서를 다시 편집용 명령 텍스트로 변환한다."""
        if not str(self.대상.GetTextFile("TEXT", "") or "").strip():
            return None
        self.문서처음(); self.대상.HAction.Run("SelectAll"); self.대상.HAction.Run("Copy"); self.새창(); self.문서여백(20, 20, 10, 10, 10, 10); self.대상.HAction.Run("Paste"); self.대상.HAction.Run("MoveRight")
        # 누름틀/제어 표에 보관된 표지·제목·보도자료 내용을 먼저 명령문으로 복원한다.
        for 컨트롤표 in list(self.컨트롤표목록()):
            try:
                self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0)); 표식별 = self.블록스캔()[1].strip()
                if "[표지]" in 표식별: 접두어 = "표지:"
                elif "[제목]" in 표식별: 접두어 = "제목:"
                elif "[보도자료]" in 표식별: 접두어 = "보도자료:"
                else: continue
                self.표전체(); 내용 = self.블록스캔()[1].replace("\r", " ").strip(); self.딜리트(); self.문장(접두어 + 내용)
            except Exception:
                self.캔슬()

        self.대상.HAction.Run("SelectAll"); self.대상.InitScan(1, 255); 결과텍스트 = ""
        try:
            while True:
                상태, 텍스트 = self.대상.GetText()
                if 상태 not in (2, 3): break
                결과텍스트 += 텍스트
        finally:
            self.대상.ReleaseScan()
        변환행 = []
        for 줄 in 결과텍스트.splitlines():
            줄 = 줄.strip()
            if not 줄: continue
            if 줄.startswith(("□", "ㅁ")): 줄 = re.sub(r"^(□|ㅁ)\s*", "네모: ", 줄)
            elif 줄.startswith(("○", "◯")): 줄 = re.sub(r"^(○|◯)\s*", "원: ", 줄)
            elif 줄.startswith("-"): 줄 = re.sub(r"^-\s*", "바: ", 줄)
            elif 줄.startswith("※"): 줄 = re.sub(r"^※\s*", "당구: ", 줄)
            elif 줄.startswith("*"): 줄 = re.sub(r"^\*\s*", "별: ", 줄)
            elif 줄.startswith("◆"): 줄 = "표:◆ " + 줄[1:].strip()
            elif 줄.startswith("<") and 줄.endswith(">>"): 줄 = "설명: " + 줄.strip("<> ")
            elif re.match(r"^대면보고\s*/", 줄): 줄 = "대면보고 : " + re.sub(r"^대면보고\s*/\s*|\s*/.*?/\s*", "", 줄)
            elif re.match(r"^서면보고\s*/", 줄): 줄 = "서면보고 : " + re.sub(r"^서면보고\s*/\s*|\s*/.*?/\s*", "", 줄)
            elif re.match(r"^\d+\.\s+", 줄): 줄 = re.sub(r"^\d+\.\s+(.+)", r"소제목: \1", 줄)
            elif re.match(r"^[가-하]\.", 줄): 줄 = "가제목:" + 줄
            변환행.append(줄)
        결과 = "\r\n".join(변환행).replace("요약\r\n", "요약 : ")
        self.대상.HAction.Run("SelectAll"); self.딜리트(); 시작지점 = self.현재위치(); self.기본정렬(); self.기본글자(); self.글자크기(10); self.폰트("맑은 고딕"); self.줄간격(150); self.문단위(0); self.내어쓰기(0); self.문장(결과); 종료지점 = self.현재위치(); self.대상.SetPosBySet(시작지점); self.대상.HAction.Run("Select"); self.대상.SetPosBySet(종료지점); return None

    def 인국공명찰(self, 이미지):
        if not self.대상.CellShape: return None
        self.캔슬(); self.표전체(); 마지막위치 = self.대상.GetPosBySet(); self.대상.InitScan(1, 255); self.대상.GetText(); self.대상.MovePos(201); 처음위치 = self.대상.GetPosBySet(); self.대상.ReleaseScan(); 데이터리스트 = []
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i)); self.대상.InitScan(0, 85); 내용 = ""
            while True:
                상태, 텍스트 = self.대상.GetText(); 내용 += 텍스트
                if 상태 in (0, 1): break
            self.대상.ReleaseScan(); 데이터리스트.append(내용.strip())
        행 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5) if len(데이터리스트[i:i + 5]) == 5]
        from win32com.client.gencache import EnsureDispatch
        피피티 = EnsureDispatch("PowerPoint.Application"); 피피티.Visible = True; 프레젠테이션 = 피피티.Presentations.Add(); 프레젠테이션.PageSetup.SlideWidth = 720; 프레젠테이션.PageSetup.SlideHeight = 540
        def 글자(슬라이드, x, y, w, h, 내용, 크기, 폰트="HY견고딕", 정렬=2, 색=0):
            박스 = 슬라이드.Shapes.AddTextbox(Orientation=1, Left=x, Top=y, Width=w, Height=h); 범위 = 박스.TextFrame.TextRange; 범위.Text = 내용; 범위.Font.Name = 폰트; 범위.Font.Size = 크기; 범위.Font.Bold = True; 범위.Font.Color.RGB = 색; 범위.ParagraphFormat.Alignment = 정렬; return 박스
        def 배경(슬라이드, 점, 색):
            작성기 = 슬라이드.Shapes.BuildFreeform(EditingType=1, X1=점[0][0], Y1=점[0][1])
            for x, y in 점[1:]: 작성기.AddNodes(SegmentType=0, EditingType=0, X1=x, Y1=y)
            도형 = 작성기.ConvertToShape(); 도형.Fill.ForeColor.RGB = 색; 도형.Line.Visible = False; return 도형
        for 순번, 줄 in enumerate(행):
            슬라이드 = 프레젠테이션.Slides.Add(순번 + 1, 1)
            for 객체 in list(슬라이드.Shapes): 객체.Delete()
            소속, 직위, 이름, 영문이름, 비고 = 줄
            배경(슬라이드, ((338, 92), (593, 92), (593, 259), (338, 259), (338, 92)), 11693695); 배경(슬라이드, ((338, 320), (655, 320), (655, 524), (338, 524), (338, 320)), 11234471); 배경(슬라이드, ((31, 194), (278, 194), (278, 524), (31, 524), (31, 194)), 13998939)
            이름크기 = 72 if len(이름) <= 3 else 60 if len(이름) == 4 else 50 if len(이름) == 5 else 40
            글자(슬라이드, 340, 178, 250, 90, 이름, 이름크기); 글자(슬라이드, 339, 320, 317, 60, 소속, 36, "나눔고딕 ExtraBold"); 글자(슬라이드, 335, 442, 200, 48, 직위, 32); 글자(슬라이드, 31, 194, 247, 90, 영문이름 or 이름, 31, "넥슨Lv2고딕 Bold", 2, 16777215); 글자(슬라이드, 31, 423, 247, 60, 비고, 14, "넥슨Lv2고딕 Bold", 2, 16279883)
            for 이미지경로, x, y, w, h in ((이미지[0] if len(이미지) > 0 else "", 433, 491, 127, 17.5), (이미지[1] if len(이미지) > 1 else "", 535, 414, 110, 31)):
                if 이미지경로: 슬라이드.Shapes.AddPicture(FileName=이미지경로, LinkToFile=False, SaveWithDocument=True, Left=x, Top=y, Width=w, Height=h)
        return None

    def 인진MD변환(self):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
        결과텍스트 = ""
        try:
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
            self.대상.ReleaseScan()
            분할데이터 = [줄.strip() for 줄 in 결과텍스트.splitlines()]
            정리데이터 = []
            단순변환 = (
                ("네모:", "[□]"),
                ("원:", "  [○]"),
                ("바:", "    [-]"),
                ("별:", "    [*]"),
                ("당구:", "    [※]"),
                ("설명:", "[설명]"),
                ("참고:", "[참고]"),
                ("붙임:", "[붙임]"),
                ("보도자료:", "[보도자료]"),
                ("제목:", "# "),
            )
            for 순번, 줄 in enumerate(분할데이터):
                변환됨 = False
                for 접두어, 대체어 in 단순변환:
                    if 줄.startswith(접두어):
                        정리데이터.append(줄.replace(접두어, 대체어, 1))
                        변환됨 = True
                        break
                if 변환됨:
                    continue
                if 줄.startswith("표지:"):
                    정리데이터.extend(("---", 줄, "---"))
                    continue
                이전도표 = 순번 > 0 and 분할데이터[순번 - 1].startswith("표:")
                if 이전도표 and 줄.startswith("표:"):
                    줄 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 줄)
                    정리데이터.append(줄.replace("표:", "|", 1).replace(":", "|").replace(";", ":") + "|")
                    continue
                if (순번 == 0 and 줄.startswith("표:")) or (줄.startswith("표:") and not 이전도표):
                    줄 = re.sub(r"\b(\d{1,2}):(\d{2})\s*~\s*(\d{1,2}):(\d{2})\b", r"\1;\2~\3;\4", 줄)
                    개수 = 줄.count(":")
                    정리데이터.append(줄.replace("표:", "|", 1).replace(":", "|").replace(";", ":") + "|")
                    정리데이터.append("|---" * 개수 + "|")
                    continue
                정리데이터.append(줄)
            print(정리데이터)
            self.문장("\r\n".join(정리데이터))
        except ValueError as e:
            print(f"값 오류 : {e}")
            self.대상.ReleaseScan()
        except Exception as e:
            print(f"오류 발생 : {e}")
            self.대상.ReleaseScan()

    def MD중간변환(self):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
        결과텍스트 = ""
        try:
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
            self.대상.ReleaseScan()
            분할데이터 = [줄.strip() for 줄 in 결과텍스트.splitlines()]
            정리데이터 = []
            단순변환 = (
                ("[□]", "네모:"),
                ("[○]", "원:"),
                ("[-]", "바:"),
                ("[*]", "별:"),
                ("[※]", "당구:"),
                ("[설명]", "설명:"),
                ("[참고]", "참고:"),
                ("[붙임]", "붙임:"),
                ("[보도자료]", "보도자료:"),
            )
            for 순번, 줄 in enumerate(분할데이터):
                변환됨 = False
                for 접두어, 대체어 in 단순변환:
                    if 줄.startswith(접두어):
                        정리데이터.append(줄.replace(접두어, 대체어, 1))
                        변환됨 = True
                        break
                if 변환됨:
                    continue
                if re.match(r"^#\s", 줄):
                    정리데이터.append(줄.replace("# ", "제목:", 1))
                elif re.match(r"^##\s", 줄):
                    정리데이터.append(줄.replace("## ", "네모:", 1))
                elif 줄.startswith("---") or 줄.startswith("|-") or 줄.startswith("| -"):
                    continue
                elif 줄.startswith("표지:"):
                    정리데이터.append(줄)
                elif 줄.startswith("|"):
                    정리데이터.append("표:" + 줄.strip("|").replace("|", ":"))
                else:
                    정리데이터.append(줄)
            print(정리데이터)
            결과텍스트 = "\r\n".join(정리데이터)
            self.백스페이스()
            시작지점 = self.현재위치()
            self.기본정렬()
            self.기본글자()
            self.글자크기(10)
            self.폰트("맑은 고딕")
            self.줄간격(150)
            self.문단위(0)
            self.내어쓰기(0)
            self.문장(결과텍스트)
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
        except ValueError as e:
            print(f"값 오류 : {e}")
            self.대상.ReleaseScan()
        except Exception as e:
            print(f"오류 발생 : {e}")
            self.대상.ReleaseScan()

    def 한수원표(self, 내용=[]):
        if self.방금처리 == "한수원표":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A1":
                self.표아래쪽(1)
            else:
                self.표오른쪽(1)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A3":
                self.셀선택()
                self.표오른쪽끝()
                self.표단일선("상", 1, 1)
                self.캔슬()
                self.표왼쪽끝()
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
                if "○" in 입력내용:
                    입력내용 = 입력내용.replace("○", " ○")
                    self.왼쪽정렬()
                elif "□" in 입력내용:
                    입력내용 = 입력내용.replace("□", " □")
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif "⦁" in 입력내용:
                    self.왼쪽정렬()
                    self.내어쓰기(-12.6)
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = "한수원표"
            self.표나가기2()
            return None

        표개수 = len(내용)
        기본길이 = 207 - 표개수 * 3.5
        전체길이 = 기본길이 - self.문단여백측정()
        표넓이 = [2] * 표개수
        for i in range(표개수):
            if any(키워드 in 내용[i].replace("엔터 ", "").replace(" ", "") for 키워드 in ("소요시간",)):
                표넓이[i] = 0.7
            elif any(키워드 in 내용[i].replace("엔터 ", "").replace(" ", "") for 키워드 in ("주민번호",)):
                표넓이[i] = 2
            elif any(키워드 in 내용[i].replace("엔터 ", "").replace(" ", "") for 키워드 in ("연번", "순번", "번호", "구분", "이름")):
                표넓이[i] = 1
            elif any(키워드 in 내용[i].replace("엔터 ", "").replace(" ", "") for 키워드 in ("시간계획", "비고", "시간")):
                표넓이[i] = 1.5
            elif any(키워드 in 내용[i].replace("엔터 ", "").replace(" ", "") for 키워드 in ("주소", "내용", "사항", "세부", "수집항목")):
                표넓이[i] = 4
        표넓이합 = sum(표넓이)
        for i in range(표개수):
            표넓이[i] = 표넓이[i] / 표넓이합 * 전체길이
        self.표만들기(표넓이, [6.5] * 2)
        self.표전체()
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(6, 6, 1, 1)
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(13)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트("휴먼명조")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.표배경색(223, 234, 245)
        self.폰트("휴먼명조")
        self.진하게()
        self.표단일선("하", 6, 8)
        self.캔슬()
        self.표처음()
        for i in range(표개수):
            if i != 0:
                self.표오른쪽(1)
            입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "한수원표"
        self.표나가기2()

    def 가스공표(self, 내용=[]):
        if self.방금처리 == "가스공표":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A1":
                self.표아래쪽(1)
            else:
                self.표오른쪽(1)
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
                if "○" in 입력내용:
                    입력내용 = 입력내용.replace("○", " ○")
                    self.왼쪽정렬()
                elif "□" in 입력내용:
                    입력내용 = 입력내용.replace("□", " □")
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif "▪" in 입력내용:
                    입력내용 = 입력내용.replace("▪", " ▪")
                    self.왼쪽정렬()
                    self.내어쓰기(-15.9)
                    self.진하게()
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = "가스공표"
            self.표나가기2()
            return None

        표개수 = len(내용)
        전체길이 = 207 - 표개수 * 3.5 - self.문단여백측정()
        표넓이 = [2] * 표개수
        for i in range(표개수):
            if any(키워드 in 내용[i] for 키워드 in ("소요시간",)):
                표넓이[i] = 0.5
            elif any(키워드 in 내용[i] for 키워드 in ("연번", "순번", "번호", "구분")):
                표넓이[i] = 1
            elif any(키워드 in 내용[i] for 키워드 in ("시간계획",)):
                표넓이[i] = 1.5
            elif any(키워드 in 내용[i] for 키워드 in ("주민번호", "비고")):
                표넓이[i] = 2
            elif any(키워드 in 내용[i] for 키워드 in ("주소", "내용", "사항", "세부", "수집항목")):
                표넓이[i] = 4
        표넓이합 = sum(표넓이)
        for i in range(표개수):
            표넓이[i] = 표넓이[i] / 표넓이합 * 전체길이
        self.표만들기(표넓이, [10, 7])
        self.표전체()
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(11)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.글자크기(11)
        self.표배경색(223, 230, 247)
        self.캔슬()
        self.표처음()
        for i in range(표개수):
            if i != 0:
                self.표오른쪽(1)
            입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "가스공표"
        self.표나가기2()

    def 인진표(self, 내용=[]):
        if self.방금처리 == "인진표":
            self.궁극의정리위치보정 = -1
            self.백스페이스()
            self.대상.SetPosBySet(self.위치저장)
            셀위치 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
            if str(셀위치) == "A1":
                self.표아래쪽(1)
            else:
                self.표오른쪽(1)
            for i in range(len(내용)):
                if i != 0:
                    self.표오른쪽(1)
                입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
                if "○" in 입력내용:
                    입력내용 = 입력내용.replace("○", " ○")
                    self.왼쪽정렬()
                elif "□" in 입력내용:
                    입력내용 = 입력내용.replace("□", " □")
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif "\U000f02fb" in 입력내용:
                    self.왼쪽정렬()
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = "인진표"
            self.표나가기2()
            return None

        표개수 = len(내용)
        기본길이 = 207 - 표개수 * 3.5
        전체길이 = 기본길이 - self.문단여백측정()
        표넓이 = [2] * 표개수
        for i in range(표개수):
            if any(키워드 in 내용[i] for 키워드 in ("소요시간",)):
                표넓이[i] = 0.5
            elif any(키워드 in 내용[i] for 키워드 in ("연번", "순번", "번호", "구분")):
                표넓이[i] = 1
            elif any(키워드 in 내용[i] for 키워드 in ("시간계획",)):
                표넓이[i] = 1.5
            elif any(키워드 in 내용[i] for 키워드 in ("주민번호", "비고")):
                표넓이[i] = 2
            elif any(키워드 in 내용[i] for 키워드 in ("주소", "내용", "사항", "세부", "수집항목")):
                표넓이[i] = 4
        표넓이합 = sum(표넓이)
        for i in range(표개수):
            표넓이[i] = 표넓이[i] / 표넓이합 * 전체길이
        self.표만들기(표넓이, [7, 7])
        self.표전체()
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(12)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트("맑은 고딕")
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.글자크기(12)
        self.표배경색(210, 235, 238)
        self.캔슬()
        self.표처음()
        for i in range(표개수):
            if i != 0:
                self.표오른쪽(1)
            입력내용 = "\r\n".join(part.strip() for part in 내용[i].split("엔터 ")).replace(";", ":")
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = "인진표"
        self.표나가기2()

    def 해경채증사진(self):
        if filedialog is None:
            return False
        이름 = filedialog.askopenfilenames(
            title="Open File",
            filetypes=[("image files", (".png", ".jpg", ".jpeg"))],
        )
        if not 이름:
            return False

        def 번호키(경로):
            파일명 = os.path.basename(os.fspath(경로))
            매치 = re.match(r"\s*(\d+)", 파일명)
            return int(매치.group(1)) if 매치 else 10**9

        재정렬이름 = sorted(이름, key=번호키)
        self.새창()
        self.문서여백(20, 20, 30, 5, 5, 5)
        self.가운데정렬()
        self.폰트("HY헤드라인M")
        self.글자크기(20)
        self.진하게()
        self.밑줄()
        self.문장("00호(항계 내 불법조업) 채증사진\r\n")
        self.기본글자()
        self.글자크기(10)
        self.엔터(2)
        self.표만들기([21, 90], [7, 10, 8])
        self.표전체()
        self.가운데정렬()
        self.표테두리굵기(6, 6, 6, 6)
        self.폰트("맑은 고딕")
        self.글자크기(11)
        self.캔슬()
        self.표처음()
        self.문장("채증일시")
        self.표오른쪽(1)
        self.오늘날짜숫자만()
        self.문장(" 05:00 ~ 00:00")
        self.문장오른쪽("채증장소")
        self.표오른쪽(1)
        self.줄간격(140)
        self.문장("34-46.37N, 126-20.70E\r\n(목포대교 0번부표 인근해상)")
        self.문장오른쪽("채 증 자")
        self.문장오른쪽("순경 000 (인)")
        self.표나가기2()
        self.문장("\r\n\r\n\r\n\r\n")
        for i in range(len(재정렬이름)):
            self.가운데정렬()
            self.표만들기([21, 122], [84, 10])
            self.표전체()
            self.표테두리굵기(6, 6, 6, 6)
            self.표내부선굵기(6, 6)
            self.글자크기(13)
            self.폰트("맑은 고딕")
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.셀여백지정(0, 0, 0, 0)
            self.사진넣기절대값(재정렬이름[i], 150, 86)
            self.표오른쪽(1)
            self.진하게()
            self.가운데정렬()
            파일명 = os.path.basename(os.fspath(재정렬이름[i]))
            self.문장("사진" + 파일명.split(" ", 1)[0] + "호")
            self.표오른쪽(1)
            self.셀한줄(1)
            설명 = 파일명.split(" ", 1)[1] if " " in 파일명 else 파일명
            for 확장자 in (".png", ".jpeg", ".jpg", ".PNG", ".JPEG", ".JPG"):
                설명 = 설명.replace(확장자, "")
            self.문장(설명)
            self.표나가기2()
            self.글자크기(10)
            self.문장("\r\n\r\n\r\n\r\n")

    def 공항공제목(self, 내용=["한국공항공사 계획", "부서명"]):
        if len(내용) >= 2:
            self.표만들기([165 - self.문단여백측정(), 37], [5, 1, 15, 1])
        else:
            self.표만들기([165 - self.문단여백측정(), 37], [1, 15, 1])
        self.셀여백제로()
        self.표전체()
        self.글자크기(1)
        self.폰트("맑은 고딕")
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.캔슬()
        self.표처음()
        if len(내용) >= 2:
            self.글자크기(13)
            self.진하게()
            self.문장(내용[1])
            self.셀세로정렬(0)
            self.표오른쪽(1)
            self.글자크기(13)
            self.진하게()
            self.오른쪽정렬()
            self.오늘날짜점생략()
            self.셀세로정렬(0)
            self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.표배경색(0, 128, 192)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.글자크기(20)
        self.폰트("HY헤드라인M")
        self.진하게()
        self.가운데정렬()
        self.문장(내용[0] if len(내용) >= 1 else "한국공항공사 계획")
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.표배경그라데이션2("Linear", 90, [[255, 0, 128, 192], [0, 60, 191, 255]])
        self.표나가기2()

    def 인진보도자료본문서식(self):
        텍스트 = "\r\n\r\n".join(re.split(r"(?:\r\n)+", self.블록텍스트()))
        self.문단위(0)
        self.문단아래(0)
        self.내어쓰기(0)
        self.문단여백(0, 0)
        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.줄간격(180)
        self.자간헌터(0)
        self.기본정렬()
        self.글자크기(15)
        self.휴먼명조()
        self.문장(텍스트)

    def 석유공요약(self, 내용):
        self.표만들기([205.5 - self.문단여백측정()], [10])
        self.표테두리타입(8, 8, 0, 0)
        self.표테두리굵기(7, 7, 7, 7)
        self.자간헌터(0)
        self.셀여백지정(2, 2, 2, 2)
        self.폰트("함초롬바탕")
        self.내어쓰기(-22)
        self.글자크기(15)
        self.줄간격(160)
        입력내용 = "\r\n".join("◇ " + part.strip() for part in 내용.split("엔터 "))
        self.문장(입력내용)
        self.표나가기2()

    def 토주공요약(self, 내용):
        self.표만들기([205.5 - self.문단여백측정()], [8])
        self.내어쓰기(-20.8)
        self.표테두리타입(1, 1, 0, 0)
        self.표배경색(253, 254, 235)
        self.자간헌터(0)
        self.셀여백지정(2, 2, 2, 2)
        self.폰트("휴먼명조")
        self.글자크기(15)
        self.줄간격(150)
        입력내용 = "\r\n".join("◈ " + part.strip() for part in 내용.split("엔터 "))
        self.문장(입력내용)
        self.표나가기2()


class MainInstitutionFeatureMixin:
    @staticmethod
    def _순화사전():
        한단어 = {
            "행정사항": ("행정 사항", ""), "향후": ("앞으로", ""), "향후계획": ("향후 계획", ""),
            "허브": ("중심/중심지/거점", ""), "헬스케어": ("건강 관리", ""), "협조사항": ("협조 사항", ""),
            "홈페이지": ("누리집", ""), "홈페이지에": ("누리집에", ""), "회계년도": ("회계 연도", "회계연도(허용)"),
            "회수": ("횟수", ""), "회의중": ("회의 중", ""), "힐링": ("치유", ""),
        }
        두단어 = {
            "진행 중에": ("진행하고", ""), "운영하고 있는": ("운영하는", ""), "대금 결재": ("대금 결제", ""),
            "문서 결제": ("문서 결재", ""), "계획을 달성할": ("계획을 이행할", ""), "목표를 이행할": ("목표를 달성할", ""),
        }
        세단어 = {
            "즉시 제출 바람": ("~일 ~시까지 제출해 주시기 바랍니다.", ""), "적극 뒷받침하기 위해": ("적극적으로 뒷받침하기 위해", ""),
            "조사 결과에 따르면": ("조사한 결과에 따르면", ""), "적의 조치 요망": ("적절히 조치해 주시기 바랍니다.", ""),
            "적극 이용 바람": ("적극적으로 이용하시기 바랍니다.", ""), "적극 협조 바랍니다.": ("적극적으로 협조해 주시기 바랍니다.", ""),
            "적의 조치 요망.": ("적절히 조치해 주시기 바랍니다.", ""), "적극 이용 바람.": ("적극적으로 이용하시기 바랍니다.", ""),
            "즉시 제출 바람.": ("~일 ~시까지 제출해 주시기 바랍니다.", ""), "선정된 점포에 대해서는": ("선정된 점포에는", "~에 대하여, ~에 있어서 번역 투"),
            "이번 선거에 있어서": ("이번 선거에서", "~에 대하여, ~에 있어서 번역 투"), "취소할 수 있습니다": ("취소합니다", ""),
            "취소할 수 있습니다.": ("취소합니다.", ""), "서류는 일체 반환하지": ("서류는 돌려주지", ""),
        }
        return 한단어, 두단어, 세단어

    def 순화검색(self):
        한단어, 두단어, 세단어 = self._순화사전(); 이전 = ""; 더이전 = ""
        self.대상.MovePos(3); 마지막위치 = self.대상.GetPos(); self.대상.MovePos(2)
        while self.대상.GetPos() != 마지막위치:
            self.대상.HAction.Run("MoveSelWordEnd"); self.대상.InitScan(1, 255); _, 텍스트 = self.대상.GetText(); self.대상.ReleaseScan(); 텍스트 = 텍스트.replace("\r", "").replace("\n", "").strip()
            if 텍스트 in 한단어: self.대상.HAction.Run("CharShapeTextColorRed")
            if 이전 + " " + 텍스트 in 두단어: self.글자색(255, 112, 27)
            if 더이전 + " " + 이전 + " " + 텍스트 in 세단어: self.글자색(112, 95, 199)
            더이전, 이전 = 이전, 텍스트; self.대상.HAction.Run("MoveNextWord")
        return None

    def 순화추천(self):
        한단어, 두단어, 세단어 = self._순화사전(); self.대상.InitScan(1, 255); _, 텍스트 = self.대상.GetText(); self.대상.ReleaseScan(); 텍스트 = 텍스트.replace("\r", "").replace("\n", "").strip()
        항목 = ({0: 한단어, 1: 두단어}.get(텍스트.count(" "), 세단어)).get(텍스트)
        return [텍스트, 항목[0] if 항목 else "없음", 항목[1] if 항목 else "없음"]

    def 금감원글머리지정(self, 글머리, 폰트, 크기, 내어쓰기, 진하게, 위, 줄간, 고정칸앞, 고정칸뒤, 여백크기):
        self.대상.InitScan(1, 255); 결과텍스트 = ""
        try:
            while True:
                상태, 텍스트 = self.대상.GetText(); 결과텍스트 += 텍스트
                if 상태 not in (2, 3): break
        finally:
            self.대상.ReleaseScan()
        줄들 = [줄 for 줄 in re.sub(r"(\r\n)+", "\r\n", 결과텍스트).split("\r\n") if 줄]
        self.대상.HAction.Run("DeleteBack")
        for 순서, 텍스트 in enumerate(줄들):
            if 순서: self.글자크기(여백크기); self.대상.HAction.Run("BreakPara")
            self.글자크기(크기); 시작 = self.현재위치()
            for _ in range(고정칸앞): self.대상.HAction.Run("InsertFixedWidthSpace")
            self.문장(글머리)
            for _ in range(고정칸뒤): self.대상.HAction.Run("InsertFixedWidthSpace")
            매치 = re.search(r"[가-힣0-9a-zA-Z]", 텍스트); self.문장(텍스트[매치.start():] if 매치 else 텍스트); 종료 = self.현재위치()
            self.대상.SetPosBySet(시작); self.대상.HAction.Run("Select"); self.대상.SetPosBySet(종료); self.글자스타일(0); self.자간헌터(0); self.내어쓰기(내어쓰기); self.대상.HAction.Run("ParagraphShapeAlignJustify"); self.대상.HAction.Run("CharShapeNormal")
            if 진하게 == 1: self.대상.HAction.Run("CharShapeBold")
            self.폰트(폰트); self.글자크기(크기); self.줄간격(줄간); self.글자음영(0xFFFFFFFF); self.문단여백(0, 0); self.문단위(위); self.캔슬()
        return None

    def 금감보고서(self, 이미지1, 이미지2, 이미지3):
        from datetime import datetime
        self.새창(); self.문서여백(23, 23, 12, 12, 10, 10); self.쪽번호(); self.금감보고서대외보안()
        for _ in range(4): self.대상.HAction.Run("BreakPara")
        self.금감보고서대제목(이미지1); self.폰트("HY헤드라인M"); self.글자크기(21); self.대상.HAction.Run("BreakPara"); self.가운데정렬(); self.문장(f"{datetime.today().year}. {datetime.today().month}. {datetime.today().day}.")
        self.대상.HAction.Run("BreakPara"); self.대상.HAction.Run("BreakPara"); self.금감보고서목차(); self.대상.HAction.Run("BreakPara"); self.금감보고서로고(이미지2); self.대상.HAction.Run("BreakPage")
        self.금감보고서중제목(숫자="Ⅰ. ", 내용="추진 배경"); self.쪽새번호(1)
        def 기본반복():
            항목들 = ((10, "휴먼명조", 15, -26.2, "□", 2, "휴먼명조 15pt"), (10, "휴먼명조", 15, -33.6, "◦", 2, "휴먼명조 15pt(휴먼명조 13pt)"), (5, "맑은 고딕", 12, -33.6, "*", 2, "맑은 고딕 12pt"), (2, "맑은 고딕", 11, -38.8, "†", 2, "맑은 고딕 11pt"), (10, "휴먼명조", 15, -33.6, "-", 2, "휴먼명조 15pt"))
            for 여백, 폰트, 크기, 내어, 기호, 뒤칸, 내용 in 항목들:
                self.글자크기(여백); self.대상.HAction.Run("BreakPara"); self.폰트(폰트); self.글자크기(크기); self.내어쓰기(내어); self.대상.HAction.Run("InsertFixedWidthSpace"); self.문장(기호)
                for _ in range(뒤칸): self.대상.HAction.Run("InsertFixedWidthSpace")
                self.문장(내용)
        self.대상.HAction.Run("BreakPara"); 기본반복()
        for _ in range(6): self.대상.HAction.Run("BreakPara")
        self.금감보고서블루진박스(); self.금감보고서점선박스(); self.대상.HAction.Run("BreakPage"); self.금감보고서중제목2(이미지3); self.금감보고서기본박스(); 기본반복()
        for _ in range(6): self.대상.HAction.Run("BreakPara")
        self.금감보고서기본표(); self.대상.HAction.Run("BreakPage"); self.금감보고서중제목2(이미지3, "2"); self.금감보고서소제목(); self.금감보고서기본박스(); self.금감보고서소제목2(); 기본반복(); self.대상.HAction.Run("BreakPage"); self.금감원페이지참고(); self.대상.MovePos(2); self.쪽번호숨기기(); return None

    def 서교공궁극의정리(self, 종류="다음"):
        if 종류 in ("전체", "전체문서"): return self.서교공궁극의정리전체()
        if 종류 not in ("다음", "현재"):
            return self.서교공궁극의정리범위()
        텍스트 = self.블록텍스트().strip()
        self.기본글자(); self.폰트("서울남산체 M"); self.글자크기(14); self.글자간격(0)
        self.글자장평(100); self.줄간격(160); self.문단여백(0, 0); self.기본정렬()
        if 텍스트:
            self.문장(텍스트)
        self.캔슬(); self.대상.MovePos(10)
        return None

    def 기본서식궁극의정리(self):
        self.대상.MovePos(2); self.대상.HAction.Run("SelectAll"); return self.기본서식궁극의정리범위()

    def 산인공궁극의정리2(self):
        self.대상.MovePos(2); self.대상.HAction.Run("SelectAll"); return self.산인공궁극의정리범위2()

    def 산인공궁극의정리(self, 이미지):
        설정 = {
            "줄간격": 160,
            "정렬": "기본",
            "명령": {
                "표지제목": ("부여표지제목", "문자열"),
                "제목": ("산인공기본보고서제목", "목록"),
                "표지": ("산인공표지마크다운", "목록이미지"),
                "목차": ("산인공목차마크다운", "이미지"),
                "사진2단": ("산인공사진2단마크다운", "이미지"),
                "구매표": ("산인공구매표", "목록"),
                "참석자명단": ("산인공참석자명단마크다운", "목록"),
                "관리대장": ("산인공관리대장", "목록"),
                "소제목": ("산인공약식보고서소제목", "카운트문자열"),
                "점선박스": ("부여점선박스", "문자열"),
                "참고": ("부여참고박스", "문자열"),
                "서론": ("부여서론", "문자열"),
                "붙임": ("부여붙임", "문자열"),
                "한줄일정": ("부여한줄일정", "문자열"),
                "시간계획": ("산인공시간계획표", "목록"),
                "추진일정": ("부여추진일정", "문자열"),
                "동향제목": ("부여동향제목", "문자열"),
            },
        }
        return self._기관궁극정리(이미지, 설정)

    def 경남도궁극의정리(self):
        설정 = {
            "줄간격": 160,
            "명령": {
                "제목": ("경남도제목", "목록"),
                "진행순서표": ("경남도진행순서표", "목록"),
                "기획제목": ("경남도기획제목", "문자열"),
                "소제목": ("경남도소제목", "로마문자열"),
                "서론": ("경남도서론", "문자열"),
            },
        }
        return self._기관궁극정리(None, 설정)

    def 인국공궁극의정리(self, 이미지):
        설정 = {"줄간격": 160, "정렬": "기본", "명령": {
            "제목": ("인국공제목", "목록"), "표지목차": ("인국공표지목차", "이미지"),
            "시간계획": ("인국공시간계획", "목록"), "주요이력": ("인국공주요이력", "목록"),
            "참고": ("인국공참고", "문자열"), "붙임": ("인국공붙임", "문자열"),
            "소제목": ("인국공소제목", "카운트문자열"), "중제목": ("인국공중제목", "로마문자열"),
            "글상자": ("인국공글상자", "문자열"),
        }}
        return self._기관궁극정리(이미지, 설정)

    def 울항궁극의정리(self, 이미지):
        설정 = {
            "줄간격": 160, "정렬": "기본", "명령": {
                "표지제목": ("부여표지제목", "문자열"), "제목": ("울항기본보고서제목", "목록"),
                "표지": ("산인공표지마크다운", "목록이미지"), "목차": ("산인공목차마크다운", "이미지"),
                "사진2단": ("산인공사진2단마크다운", "이미지"), "구매표": ("산인공구매표", "목록"),
                "참석자명단": ("산인공참석자명단마크다운", "목록"), "관리대장": ("산인공관리대장", "목록"),
                "소제목": ("산인공약식보고서소제목", "카운트문자열"), "점선박스": ("부여점선박스", "문자열"),
                "참고": ("부여참고박스", "문자열"), "서론": ("부여서론", "문자열"),
                "붙임": ("부여붙임", "문자열"), "한줄일정": ("부여한줄일정", "문자열"),
                "시간계획": ("산인공시간계획표", "목록"), "추진일정": ("부여추진일정", "문자열"),
                "동향제목": ("부여동향제목", "문자열"),
            },
        }
        return self._기관궁극정리(이미지, 설정)

    def 법무담당관궁극의정리(self, 종류, 기본크기, 기본자간):
        if 종류 in ("전체", "전체문서"):
            self.대상.MovePos(2); self.대상.HAction.Run("SelectAll")
        self.폰트("휴먼명조"); self.글자크기(기본크기); self.글자간격(기본자간); self.줄간격(160); self.대상.HAction.Run("ParagraphShapeAlignJustify"); self.캔슬(); return None

    def 기본서식마크다운(self):
        return self.마크다운응용(self.블록텍스트())

    def 마크다운(self):
        # 마크다운응용()은 문서를 만든 뒤 다시 self.마크다운()을 호출한다.
        # 여기서 마크다운응용()으로 되돌아가면 새 창 생성이 무한 반복되므로,
        # 원본 실행 파일의 마크다운 변환 본체를 직접 실행한다.
        if __name__.startswith("한컴오피스."):
            package_root = "한컴오피스"
        else:
            package_root = __name__.split(".한컴오피스.", 1)[0] + ".한컴오피스"
        legacy_module = import_module(f"{package_root}.compat.legacy_runtime")
        return legacy_module.Legacy기본한컴.마크다운(self)

    def 남해복지찾기(self):
        from datetime import datetime
        값 = self._선택표텍스트()
        if len(값) < 12: return None
        생년 = re.sub(r"[^0-9]", "", 값[3]); 구분 = 생년[-1:] or "1"; 생년 = 생년[:6]
        세기 = 1900 if 구분 in "1256" else 2000; 출생 = datetime(세기 + int(생년[:2]), int(생년[2:4]), int(생년[4:6])); 오늘 = datetime.today(); 나이 = 오늘.year - 출생.year - ((오늘.month, 오늘.day) < (출생.month, 출생.day)); 개월 = (오늘.year - 출생.year) * 12 + 오늘.month - 출생.month - (오늘.day < 출생.day)
        거주 = 값[5] == "1"; 소득 = int(re.sub(r"[^0-9]", "", 값[9]) or 0); 결과 = [f"생년월일 {생년}, 만 {나이}세, {개월}개월", f"성별 {'남성' if 구분 in '1357' else '여성'}, 중위소득 {소득}%"]
        if 거주: 결과.append("군민행복법률상담실 운영")
        if 거주 and 19 <= 나이 <= 45: 결과 += ["청년 커뮤니티 활성화 지원", "청년 자격증 응시료 지원"]
        if 거주 and 19 <= 나이 <= 45 and 60 < 소득 <= 150: 결과.append("청년월세 지원")
        if 거주 and 19 <= 나이 <= 34 and 소득 <= 130: 결과.append("청년 씨앗통장 지원")
        self.마크다운응용("소제목 : 복지 탐색 결과\r\n" + "\r\n".join("□ " + x for x in 결과)); return None

    def 서교공사장요청사항(self):
        self.새창()
        self.문서여백(18, 18, 12.7, 12.7, 12.7, 12.7)
        self.폰트("HY헤드라인M"); self.글자크기(26); self.가운데정렬()
        self.밑줄얇굵(); self.글자간격(-5); self.문장("사장 요청사항 관리카드\r\n")
        self.기본글자(); self.글자크기(10); self.엔터(1)
        self.표만들기([23, 27, 23, 27, 23, 28], [9, 9, 9, 9, 9, 11, 22, 15, 15, 35, 35, 15, 15])
        self.셀여백제로(); self.표전체(); self.표테두리굵기(6, 6, 6, 6)
        self.가운데정렬(); self.글자장평(96); self.글자간격(-4); self.줄간격(130)
        self.글자크기(12); self.폰트("한컴돋움"); self.캔슬(); self.표처음()

        def 진한작은글자(내용, 오른쪽=1):
            self.표배경색(223, 230, 247); self.폰트("한컴돋움"); self.글자크기(12)
            self.문장(내용); self.표오른쪽(오른쪽)

        def 파란기본글자(내용, 오른쪽=1):
            self.글자색(0, 0, 255); self.글자크기(12); self.기본정렬()
            self.문장(내용); self.표오른쪽(오른쪽)

        def 진한글자(내용, 오른쪽=1, 부제=""):
            self.표배경색(223, 230, 247); self.폰트("HY견고딕"); self.글자크기(13)
            self.문장(내용)
            if 부제 != "":
                self.엔터(1); self.폰트("한컴돋움"); self.글자크기(12)
            self.문장(부제); self.표오른쪽(오른쪽)

        def 파란글자(내용, 오른쪽=1, 부제=""):
            self.글자색(0, 0, 255); self.글자크기(11)
            if 내용 == "오늘날짜": self.오늘날짜바()
            else: self.문장(내용)
            if 부제 != "": self.엔터(1)
            self.문장(부제); self.표오른쪽(오른쪽)

        진한글자("제    목", 1)
        self.셀선택(); self.표오른쪽(4); self.셀병합(); self.표오른쪽(1)
        진한글자("관리번호", 1); 파란글자("○○-○○", 1)
        진한글자("요청일자", 1); 파란글자("오늘날짜", 1)
        진한글자("구분", 1); 파란글자("안전우선,도전혁신,", 1, "고객지향,지속경영")
        진한글자("추진부서", 2); 진한글자("협조부서", 2)
        진한글자("부서평가의견", 1); 파란글자("완료,정상추진,", 1, "부진,추진불가")
        진한글자("담 당 자", 1); 파란글자("○○○ (☏    )", 1)
        진한글자("부  장", 1); 파란글자(" ○○○ (☏    )", 1)
        진한글자("팀  장", 1); 파란글자(" ○○○ (☏    )", 1)
        진한글자("점검기간", 1); 파란글자("오늘날짜", 1)
        진한글자("최초시행일", 1); 파란글자("오늘날짜", 1)
        진한글자("완료예정일", 1); 파란글자("오늘날짜", 1)
        진한글자("소요예산", 1, "(총 물량)"); 파란글자("○○원 / 비예산", 1, "(○○건)")
        진한글자("투입예산", 1, "(추진물량)"); 파란글자("○○원", 1, "(○○건)")
        진한글자("집행율", 1); 파란글자("○○.○ %", 1)
        진한글자("요청사항\r\n요    지", 1)
        self.셀선택(); self.표오른쪽(4); self.셀병합(); self.표오른쪽(1)
        self.셀선택(); self.표아래쪽(1); self.셀병합()
        진한글자("추진계획", 1); 진한작은글자("최초시행일\r\n~완료예정일", 1)
        self.셀선택(); self.표오른쪽(3); self.셀병합()
        파란기본글자(" ※ 최초 통보시 3일 내 추진계획 작성해서 시스템 업로드", 2)
        진한작은글자("점검기간\r\n~다음점검기간", 1)
        self.셀선택(); self.표오른쪽(3); self.셀병합()
        파란기본글자(" ※ 다음 분기 점검시까지의 목표", 1)
        self.셀선택(); self.표아래쪽(1); self.셀병합()
        진한글자("추진실적", 1); 진한작은글자("최초시행일\r\n~완료예정일", 1)
        self.셀선택(); self.표오른쪽(3); self.셀병합()
        파란기본글자(" ※ 최초 작성시는 실적 작성 불필요\r\n ※ 정비물량, 계약절차 진행상황, 구체적인 추진실적을 작성하고 관련 근거 및 세부실적을 파일로 첨부", 2)
        진한작은글자("점검기간 내\r\n추진실적", 1)
        self.셀선택(); self.표오른쪽(3); self.셀병합()
        파란기본글자(" ※ 해당 분기에 추진한 사항", 1)
        진한글자("협업여부\r\n및 증빙", 1)
        self.셀선택(); self.표오른쪽(4); self.셀병합()
        파란기본글자(" ※ 타부서/타기관과 협업시행 시 내용 및 관련근거 기재", 1)
        진한글자("문제점\r\n및 대책", 1)
        self.셀선택(); self.표오른쪽(4); self.셀병합()
        파란기본글자(" ※ 예산확보 어려움, 타부서 협조 부진 등 문제점 기술", 0)
        self.표나가기2(); self.폰트("HY견고딕"); self.글자크기(17); self.기본정렬()
        self.글자간격(0); self.줄간격(140); self.문장("󰏚 공정관리(예시)\r\n")
        self.표만들기([5, 42, 9] + [14] * 6, [3, 3, 9, 9])
        self.셀여백제로(); self.표전체(); self.표테두리굵기(6, 6, 6, 6)
        self.표테두리타입(1, 1, 0, 0); self.가운데정렬(); self.폰트("한컴돋움")
        self.글자간격(-5); self.글자장평(90); self.줄간격(110); self.글자크기(11)
        self.캔슬(); self.표처음(); self.셀선택(); self.표아래쪽(1); self.셀병합()
        self.셀선택(); self.표오른쪽끝(); self.표배경색(223, 230, 247)
        self.표테두리단일선("하", 6, 8); self.진하게(); self.캔슬(); self.표처음()
        self.문장("구분"); self.표오른쪽(1); self.셀선택(); self.표아래쪽(1); self.셀병합()
        self.문장("과제명"); self.표오른쪽(1); self.셀선택(); self.표아래쪽(1); self.셀병합()
        self.문장("관리\r\n번호"); self.표오른쪽(1); self.셀선택(); self.표아래쪽(1); self.셀병합()
        self.문장("완료\r\n시기"); self.표오른쪽(1); self.셀선택(); self.표오른쪽(4); self.셀병합()
        self.문장("공정실적·계획"); self.표오른쪽(5)
        for 내용 in ("1분기", "2분기", "3분기", "4분기", "’25년~", "핵심\r\n가치", "제목", "00-00"):
            self.문장(내용); self.표오른쪽(1)
        self.문장("’00.00."); self.표오른쪽(6)
        self.문장("안전\r\n우선"); self.표오른쪽(1)
        self.문장("(예시)외부E/L 유리처마 개선"); self.표오른쪽(1)
        self.문장("1-1"); self.표오른쪽(1); self.문장("24.06."); self.표오른쪽(2)
        self.문장("준공\r\n(127개소)"); self.표배경색(255, 247, 204)
        return None

    def _가이드행(self):
        데이터 = self._선택표텍스트(); return [데이터[i:i + 4] for i in range(0, len(데이터), 4)]

    def 가이드물품구매필요서류(self):
        행 = self._가이드행(); 금액 = sum(int(re.sub(r"[^0-9]", "", x[2]) or 0) * int(re.sub(r"[^0-9]", "", x[3]) or 0) for x in 행[9:] if len(x) == 4); 서류 = ["물품 기타 구입 승낙사항", "세금계산서", "청구서", "물품사진", "납품서", "사업장 4대 사회보험 완납증명서", "사업자등록증", "통장사본", "견적서"]
        if 금액 >= 500000: 서류 += ["물품검수조서", "타행견적서 1개"]
        if 금액 >= 1000000: 서류 += ["타행견적서 추가 1개"]
        if 금액 >= 2000000: 서류 += ["수의계약 체결 제한 여부 확인서"]
        if 금액 >= 20000000: 서류 += [f"지역개발채권 {int(금액 * .0075 / 5000) * 5000:,}원"]
        self.새창(); self.문서여백(20, 20, 10, 10, 10, 10)
        self.폰트("맑은 고딕"); self.진하게(); self.글자크기(18); self.문장("1. 필요서류 및 안내\r\n")
        self.표만들기([15, 145, 25], [8] * (len(서류) + 1)); self.표전체(); self.가운데정렬(); self.폰트("맑은 고딕"); self.글자크기(11); self.캔슬(); self.표처음()
        for 내용 in ("번호", "필요 서류", "확인"):
            self.진하게(); self.문장(내용); self.표오른쪽(1)
        for 순서, 내용 in enumerate(서류, 1):
            self.문장(str(순서)); self.표오른쪽(1); self.기본정렬(); self.문장(내용); self.표오른쪽(1); self.가운데정렬(); self.문장("확인"); self.표오른쪽(1)
        self.표나가기2(); return None

    def 가이드승낙사항(self):
        행 = self._가이드행(); self.새창(); self.문서여백(20, 20, 20, 10, 0, 0); self.폰트("돋움"); self.글자크기(9); self.문장("■ 지방자치단체 회계관리에 관한 훈령 <별지 제40-1호 서식>\r\n"); self.가운데정렬(); self.폰트("HY견고딕"); self.글자크기(16); self.문장("물품ㆍ기타 구입 승낙사항\r\n"); self.기본정렬(); self.글자크기(13)
        for 내용 in ("1. 지정한 장소와 기일까지 물품을 납품하며 불합격품은 교환하겠음.", "2. 납품 지연 시 지체상금 징수에 이의가 없음.", "3. 규격과 다른 경우 계약을 해제할 수 있음.", "4. 계약 해제 시 손해배상금을 납부함.", "5. 납부 금액은 물품대금과 상계할 수 있음."): self.문장(내용 + "\r\n\r\n")
        if len(행) > 5: self.문장(f"주소  {행[3][2]}\r\n성명  {행[3][1]}\r\n{행[5][0]} 재무관 귀하")
        return None

    def 가이드서류(self, 제목):
        self.새창(); self.문서여백(20, 20, 15, 15, 10, 10); self.폰트("맑은 고딕"); self.글자크기(20); self.가운데정렬(); self.진하게(); self.문장(제목); self.대상.HAction.Run("BreakPara"); self.기본정렬(); self.대상.HAction.Run("CharShapeNormal"); self.글자크기(11); self.문장("작성일자, 업체명, 사업자등록번호, 주소, 대표자, 금액 및 날인을 확인하십시오."); return None

    def 가이드품의공문(self):
        행 = self._가이드행(); self.새창(); self.문서여백(20, 20, 20, 20, 10, 10); self.폰트("돋움체"); self.글자크기(12); 제목 = 행[7][0] if len(행) > 7 else "물품 구입"; self.문장(f"제목 : {제목}\r\n\r\n위 물품을 다음과 같이 구입하고자 합니다.\r\n\r\n  1. 구입내역 : 붙임 참조\r\n  2. 구입방법 : 수의계약\r\n  3. 예산과목 : 해당 예산과목\r\n\r\n붙임  견적서 1부.  끝."); return None

    def 가이드이자계산(self):
        # 원본은 현재 선택된 표의 세 열을 읽어 날짜별 잔액·예치기간·이자를
        # 계산한 뒤, ``표:`` 접두어가 붙은 마크다운 표로 다시 렌더링한다.
        # 단순히 네 칸씩 묶어 계산하던 이전 복구본은 원본의 헤더·정렬·잔액
        # 누계를 잃어 유효한 표에서 결과가 달라졌으므로 바이트코드 흐름을
        # 그대로 소스화한다.
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        try:
            self.대상.HAction.Run("Cancel")
            self.대상.HAction.Run("TableCellBlock")
            self.대상.HAction.Run("TableCellBlockExtend")
            self.대상.HAction.Run("TableCellBlockExtend")
            마지막위치 = self.대상.GetPosBySet()
            self.대상.InitScan(1, 255)
            self.대상.GetText()
            self.대상.MovePos(201)
            처음위치 = self.대상.GetPosBySet()
            for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
                self.대상.SetPosBySet(self.셀위치(i))
                self.대상.HAction.Run("Select")
                self.대상.HAction.Run("Select")
                self.대상.HAction.Run("Select")
                self.대상.InitScan(1, 255)
                블록스캔값, 텍스트 = self.대상.GetText()
                결과텍스트 = ""
                while 블록스캔값 in (2, 3):
                    결과텍스트 += 텍스트
                    블록스캔값, 텍스트 = self.대상.GetText()
                self.대상.ReleaseScan()
                결과텍스트 = (
                    결과텍스트.replace("\r", "")
                    .replace("-", "")
                    .replace(",", "")
                    .replace("\n", "")
                    .replace(" ", "")
                    .strip()
                )
                데이터리스트.append(결과텍스트)
                self.문장(결과텍스트 + " ")

            분리리스트 = [데이터리스트[i : i + 3] for i in range(0, len(데이터리스트), 3)]
            필터리스트 = [row for row in 분리리스트 if row and row[0]]
            if not 분리리스트:
                return None
            정렬리스트 = 분리리스트[:2] + sorted(필터리스트[2:], key=lambda x: x[0])
            정렬리스트[0].extend(["예치기간", "잔액", "이자"])
            마지막날짜 = str(정렬리스트[-1][0])[:4] + "1231"
            정렬리스트.append([마지막날짜, "", ""])

            for i in range(2, len(정렬리스트) - 1):
                기준날짜 = datetime.strptime(정렬리스트[i][0], "%Y%m%d")
                다음날짜 = datetime.strptime(정렬리스트[i + 1][0], "%Y%m%d")
                정렬리스트[i].append(str((다음날짜 - 기준날짜).days))
            정렬리스트[-1].append("1")

            잔액 = 0
            for i in range(2, len(정렬리스트)):
                받은돈 = 정렬리스트[i][1]
                사용한돈 = 정렬리스트[i][2]
                if 받은돈 != "":
                    잔액 += int(받은돈)
                if 사용한돈 != "":
                    잔액 -= int(사용한돈)
                정렬리스트[i].append(str(잔액))

            for i in range(2, len(정렬리스트)):
                금리 = 정렬리스트[0][2]
                기간 = 정렬리스트[i][3]
                잔액 = 정렬리스트[i][4]
                if int(잔액) <= 0:
                    정렬리스트[i].append("0")
                else:
                    이자 = int((int(기간) * int(잔액) * float(금리) / 100 / 365 // 10) * 10)
                    정렬리스트[i].append(str(이자))

            정렬리스트.append(
                [
                    "최종",
                    "",
                    "",
                    "",
                    정렬리스트[-1][4],
                    str(sum(int(row[5]) for row in 정렬리스트[2:])),
                ]
            )
            합성 = ["표:" + ":".join(row) for row in 정렬리스트]
            최종 = "\r\n".join(합성)
            self.마크다운응용(최종)
            self.제목셀반복()
        except ValueError as e:
            print(f"값 오류 : {e}")
            try:
                self.대상.ReleaseScan()
            except Exception:
                pass
        except Exception as e:
            print(f"오류 발생 : {e}")
            try:
                self.대상.ReleaseScan()
            except Exception:
                pass
        return None

    def 가이드유류비공문생성(self):
        행 = self._가이드행(); 항목 = 행[9:]; 할인 = float(행[7][1]) if len(행) > 7 and 행[7][1] else 1; 합계 = sum(round(int(re.sub(r"[^0-9]", "", x[2]) or 0) * int(re.sub(r"[^0-9]", "", x[3]) or 0) * 할인, -1) for x in 항목 if len(x) == 4); 차량 = ", ".join(x[0] for x in 항목)
        self.새창(); self.문서여백(20, 20, 20, 20, 10, 10); self.폰트("돋움체"); self.글자크기(12); self.문장(f"제목 : 관용차량 유류구입({차량})\r\n\r\n관용차량({차량}) 유류를 다음과 같이 구입하고자 합니다.\r\n\r\n  1. 구입금액 : 금{합계:,}원\r\n  2. 구입내역 : 붙임 참조\r\n  3. 구입방법 : {행[7][2] if len(행)>7 else ''}\r\n  4. 예산과목 : {행[7][3] if len(행)>7 else ''}  끝."); return None

    def 역학수인성식품역학조사(self):
        self.새창(); self.문서여백(20, 20, 15, 15, 10, 10); self.폰트("맑은 고딕"); self.가운데정렬(); self.진하게(); self.글자크기(20); self.문장("수인성·식품매개 감염병 역학조사서\r\n"); self.기본정렬(); self.글자크기(11); self.대상.HAction.Run("CharShapeNormal")
        for 제목 in ("1. 발생 개요", "2. 조사 대상 및 방법", "3. 환자 발생 현황", "4. 위험요인 분석", "5. 검사 결과", "6. 결론 및 조치사항"): self.문장("\r\n□ " + 제목 + "\r\n  ○ 내용\r\n")
        return None

    def 역학유행곡선만들기1(self):
        데이터 = self._선택표텍스트(); self.새창(); self.문서여백(20, 20, 15, 15, 10, 10); self.가운데정렬(); self.진하게(); self.글자크기(16); self.문장("유행곡선\r\n"); self.기본정렬(); self.대상.HAction.Run("CharShapeNormal"); self.글자크기(10); self.문장("시간대별 발생 건수\r\n" + "\r\n".join(데이터)); return None

    def 의정부목차(self):
        def 의정부목차제목():
            self.표만들기([1, 1, 1, 45, 1, 1, 1], [9]); self.셀여백제로()
            self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableCellBlockExtend")
            self.표테두리타입(0, 0, 0, 0); self.표내부선타입(0, 0); self.대상.HAction.Run("Cancel")
            self.대상.MovePos(106); self.대상.MovePos(104)
            self.대상.HAction.Run("TableResizeExLeft"); self.대상.HAction.Run("TableResizeExLeft")
            self.표배경색(51, 102, 255); self.표오른쪽(1)
            self.대상.HAction.Run("TableResizeExLeft"); self.대상.HAction.Run("TableResizeExLeft")
            self.표오른쪽(1); self.표배경색(224, 229, 250); self.표오른쪽(1)
            self.문장풀("경기천년제목V Bold", 22, 0, 1, "목    차"); self.표오른쪽(1)
            self.표배경색(224, 229, 250); self.표오른쪽(1)
            self.대상.HAction.Run("TableResizeExLeft"); self.대상.HAction.Run("TableResizeExLeft")
            self.표오른쪽(1); self.대상.HAction.Run("TableResizeExLeft"); self.대상.HAction.Run("TableResizeExLeft")
            self.표배경색(51, 102, 255); self.대상.HAction.Run("MoveRight"); self.대상.HAction.Run("Delete")

        self.표만들기([37, 83.5, 37], [5, 5, 230])
        self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableCellBlockExtend")
        self.표테두리타입(0, 0, 0, 0); self.표내부선타입(0, 0); self.대상.HAction.Run("Cancel")
        self.대상.MovePos(106); self.대상.MovePos(104); self.표테두리단일선("하", 1, 1)
        self.대상.HAction.Run("TableRightCell"); self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend")
        self.대상.MovePos(103); self.대상.HAction.Run("TableMergeCell"); self.대상.HAction.Run("ParagraphShapeAlignCenter")
        의정부목차제목(); self.표오른쪽(2); self.표테두리단일선("상", 1, 1); self.표테두리단일선("좌", 1, 1)
        self.표오른쪽(2); self.표테두리단일선("상", 1, 1); self.표테두리단일선("우", 1, 1)
        self.대상.HAction.Run("TableRightCell"); self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend")
        self.표오른쪽(2); self.대상.HAction.Run("TableMergeCell")
        self.표테두리단일선("좌", 1, 1); self.표테두리단일선("우", 1, 1); self.표테두리단일선("하", 1, 1)
        self.줄간격(220); self.글자크기(17); self.폰트("경기천년제목V Bold"); self.탭점선설정(90000)
        for 내용 in (" Ⅰ. 추진배경", " Ⅱ. 현황 및 문제점", " Ⅲ. 목표 및 실행전략", " Ⅳ. 주요 추진과제", " Ⅴ. 과제별 세부 이행계획"):
            self.문장(내용); self.대상.HAction.Run("InsertTab"); self.대상.HAction.Run("BreakPara")
        self.글자크기(15); self.폰트("경기천년바탕 Regular")
        for 내용 in ("    1. ○○○○○", "    2. ○○○○○", "    3. ○○○○○"):
            self.문장(내용); self.대상.HAction.Run("InsertTab"); self.대상.HAction.Run("BreakPara")
        self.글자크기(17); self.폰트("경기천년제목V Bold")
        for 내용 in (" Ⅵ. 성과평가 및 포상", " Ⅶ. 행정사항"):
            self.문장(내용); self.대상.HAction.Run("InsertTab"); self.대상.HAction.Run("BreakPara")
        self.대상.HAction.Run("BreakPara"); self.글자크기(15); self.폰트("경기천년바탕 Regular")
        self.문장("  <붙  임>"); self.대상.HAction.Run("BreakPara")
        for 내용 in ("    1. ○○○○○", "    2. ○○○○○"):
            self.문장(내용); self.대상.HAction.Run("InsertTab"); self.대상.HAction.Run("BreakPara")
        self.대상.HAction.Run("MoveRight"); self.대상.HAction.Run("BreakPara"); self.대상.HAction.Run("ParagraphShapeAlignJustify")
        return None

    def 농어촌변경계약(self):
        self.새창(); self.문서여백(20, 20, 15, 15, 10, 10); self.폰트("맑은 고딕"); self.글자크기(20); self.가운데정렬(); self.진하게(); self.문장("변 경 계 약 서\r\n\r\n"); self.기본정렬(); self.글자크기(12); self.대상.HAction.Run("CharShapeNormal"); self.문장("계약명 :\r\n계약금액 :\r\n변경금액 :\r\n계약기간 :\r\n변경사유 :\r\n\r\n위와 같이 계약 내용을 변경한다."); return None

    def 농어촌업무보고(self, 이미지1, 이미지2):
        self.새창(); self.문서여백(20, 20, 15, 15, 10, 10); self.사진넣기절대값(이미지1, 35, 15); self.가운데정렬(); self.폰트("HY헤드라인M"); self.글자크기(24); self.문장("업 무 보 고\r\n"); self.사진넣기절대값(이미지2, 35, 15); self.기본정렬(); self.폰트("휴먼명조"); self.글자크기(15); self.문장("□ 보고 제목\r\n  ○ 주요 내용\r\n  - 세부 내용"); return None

    def 농어촌원페이지(self, 이미지1):
        self.새창(); self.문서여백(15, 15, 12, 12, 10, 10); self.사진넣기절대값(이미지1, 35, 12); self.폰트("HY헤드라인M"); self.글자크기(21); self.가운데정렬(); self.문장("원페이지 보고서\r\n"); self.기본정렬(); self.폰트("휴먼명조"); self.글자크기(14); self.문장("□ 추진배경\r\n  ○ 내용\r\n□ 주요내용\r\n  ○ 내용\r\n□ 향후계획\r\n  ○ 내용"); return None

    def 광주광산결재선(self):
        self.표만들기([19, 28, 8, 10, 1, 15, 15, 15, 15, 7], [8, 8, 8, 8, 8])
        self.셀여백제로()
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.폰트("돋움")
        self.글자크기(10)
        self.대상.HAction.Run("ParagraphShapeAlignCenter")
        self.대상.HAction.Run("Cancel")
        self.대상.MovePos(106)
        self.대상.MovePos(104)
        self.문장("생산등록번호")
        self.표테두리굵기(6, 1, 6, 1)
        self.표오른쪽(1)
        self.표테두리굵기(6, 1, 1, 6)
        self.표오른쪽(1)
        self.표테두리타입(0, 0, 1, 1)
        self.표오른쪽(1)
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.표오른쪽(1)
        self.대상.HAction.Run("TableMergeCell")
        self.표테두리굵기(6, 1, 6, 1)
        self.문장("주무관")
        self.표오른쪽(1)
        self.표테두리굵기(6, 1, 1, 1)
        self.표오른쪽(1)
        self.표테두리굵기(6, 1, 1, 1)
        self.표오른쪽(1)
        self.표테두리굵기(6, 1, 1, 6)
        self.표오른쪽(1)
        self.표테두리굵기(6, 1, 6, 6)
        self.표오른쪽(1)
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.대상.MovePos(103)
        self.대상.MovePos(103)
        self.대상.HAction.Run("TableMergeCell")
        self.글자크기(12)
        self.문장("결\r\n\r\n재")
        self.표테두리굵기(6, 6, 6, 6)
        self.표오른쪽(1)
        self.문장("등록일자")
        self.표테두리굵기(1, 1, 6, 1)
        self.표오른쪽(1)
        self.표테두리굵기(1, 1, 1, 6)
        self.표오른쪽(1)
        self.표테두리타입(0, 0, 1, 1)
        self.표오른쪽(1)
        for i in range(5):
            self.대상.HAction.Run("TableCellBlock")
            self.대상.HAction.Run("TableCellBlockExtend")
            if i == 0:
                self.표오른쪽(1)
            self.대상.MovePos(103)
            self.대상.HAction.Run("TableMergeCell")
            if i == 0:
                self.표테두리굵기(1, 6, 6, 1)
            elif i == 3:
                self.표테두리굵기(1, 6, 1, 6)
            elif i == 4:
                self.표테두리굵기(1, 6, 6, 6)
            else:
                self.표테두리굵기(1, 6, 1, 1)
            self.표오른쪽(1)
        self.표오른쪽(1)
        self.문장("결재일자")
        self.표테두리굵기(1, 1, 6, 1)
        self.표오른쪽(1)
        self.표테두리굵기(1, 1, 1, 6)
        self.표오른쪽(1)
        self.표테두리타입(0, 0, 1, 1)
        self.표오른쪽(7)
        self.문장("공개구분")
        self.표테두리굵기(1, 6, 6, 1)
        self.표오른쪽(1)
        self.표테두리굵기(1, 6, 1, 6)
        self.표오른쪽(1)
        self.표테두리타입(0, 0, 1, 1)
        self.표오른쪽(1)
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.대상.MovePos(103)
        self.대상.HAction.Run("TableMergeCell")
        self.문장("협 조")
        self.표테두리굵기(6, 6, 6, 1)
        self.표오른쪽(1)
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.표오른쪽(5)
        self.대상.MovePos(103)
        self.대상.HAction.Run("TableMergeCell")
        self.표테두리굵기(6, 6, 1, 6)
        self.표오른쪽(1)
        self.표테두리타입(1, 0, 0, 0)
        self.표오른쪽(1)
        self.표테두리타입(1, 0, 0, 0)
        self.표오른쪽(1)
        self.표테두리타입(0, 0, 0, 1)
        self.표오른쪽(2)
        self.대상.HAction.Run("MoveRight")
        self.대상.HAction.Run("BreakPara")
        self.대상.HAction.Run("ParagraphShapeAlignJustify")

    def 질병글머리지정(self, 글머리, 폰트, 크기, 내어쓰기, 여백크기):
        텍스트 = self.블록텍스트(); self.대상.HAction.Run("DeleteBack")
        for 순서, 줄 in enumerate(filter(None, re.split(r"[\r\n]+", 텍스트))):
            if 순서: self.글자크기(여백크기); self.대상.HAction.Run("BreakPara")
            self.폰트(폰트); self.글자크기(크기); self.내어쓰기(내어쓰기); self.문장(글머리 + " " + re.sub(r"^[^가-힣0-9A-Za-z]+", "", 줄)); self.대상.HAction.Run("ParagraphShapeAlignJustify")
        return None

    def 질병지도(self, 색단계):
        데이터 = self._선택표텍스트(); 숫자 = [float(re.sub(r"[^0-9.\-]", "", x)) for x in 데이터 if re.sub(r"[^0-9.\-]", "", x)]
        if not 숫자: return None
        최소, 최대 = min(숫자), max(숫자); 간격 = (최대 - 최소) / max(1, len(색단계)); 경계 = [최소 + 간격 * i for i in range(len(색단계) + 1)]; self.문장("범례: " + ", ".join(f"{경계[i]:.2f}~{경계[i+1]:.2f}" for i in range(len(색단계)))); return None

    def 질병명판(self, 이미지):
        return self.기본서식큰명판("질병관리청", 이미지)

    def 기본서식신문고정보공개자동완성(self, 종류):
        문구 = {"신문고": "국민신문고 민원에 대하여 다음과 같이 답변드립니다.", "정보공개": "정보공개 청구에 대하여 다음과 같이 공개합니다."}.get(종류, str(종류)); self.문장(문구 + "\r\n\r\n1. 문의하신 내용은 다음과 같습니다.\r\n2. 검토 결과를 알려드립니다.\r\n3. 추가 문의사항은 담당부서로 연락하여 주시기 바랍니다."); return None

    def 기본서식머릿말(self, 종류, 숫자=0):
        try:
            숫자 = int(숫자)
        except (TypeError, ValueError):
            # 날짜 오프셋이 비어 있거나 문자열이어도 오늘 기준으로
            # 문서를 만들고 COM 예외가 전체 동작을 중단하지 않게 한다.
            숫자 = 0
        현위치 = self.현재위치()
        self.머릿말()
        if 종류 == "1단보고자":
            self.문서여백(20, 20, 15, 15, 10, 10); self.오른쪽정렬(); self.표만들기([130], [6])
            self.폰트("맑은 고딕"); self.글자크기(13); self.가운데정렬(); self.글자간격(-10)
            self.문장("디지털정부혁신실 행정제도과 / 공무원 사무관(010-1234-5678)")
        elif 종류 == "1단보고자날짜":
            self.문서여백(20, 20, 15, 15, 10, 10); self.오른쪽정렬(); self.표만들기([110], [6])
            self.폰트("맑은 고딕"); self.글자크기(13); self.가운데정렬(); self.글자간격(-10)
            self.오늘날짜(); self.문장(", 행정제도과 공무원 사무관(행 2255)")
        elif 종류 in ("2단보고자날짜", "2단보고자", "3단보고자"):
            날짜포함 = 종류 == "2단보고자날짜"
            if 날짜포함:
                self.문서여백(20, 20, 8, 15, 17, 10); 너비, 높이 = [32, 39, 49], [6, 6]
            elif 종류 == "2단보고자":
                self.문서여백(20, 20, 8, 15, 17, 10); 너비, 높이 = [39, 44], [6, 6]
            else:
                self.문서여백(20, 20, 3, 15, 22, 10); 너비, 높이 = [39, 44], [5.5] * 3
            self.오른쪽정렬(); self.표만들기(너비, 높이); self.표전체(); self.폰트("맑은 고딕")
            self.글자크기(13); self.가운데정렬(); self.글자간격(-10); self.캔슬(); self.표처음()
            if 날짜포함:
                self.셀선택(); self.표아래쪽(1); self.셀병합(); self.오늘날짜(); self.표오른쪽(1)
                직책들 = ("정부혁신국장", "행정제도과장")
            else:
                직책들 = ("디지털정부혁신실장", "행정제도과장")
                if 종류 == "3단보고자": 직책들 += ("행정제도과장",)
            for 순서, 직책 in enumerate(직책들):
                self.오른쪽정렬(); self.문장(직책); self.표오른쪽(1); self.오른쪽정렬()
                self.문장("공무원(010-1234-5678)"); self.표테두리타입(1, 1, 0, 1)
                if 순서 != len(직책들) - 1: self.표오른쪽(1)
        elif 종류 == "상단붙임":
            self.문서여백(20, 20, 15, 15, 10, 10); self.기본정렬(); self.표만들기([19], [6])
            self.폰트("맑은 고딕"); self.글자크기(13); self.진하게(); self.가운데정렬(); self.글자색(0, 0, 255)
            self.문장("<붙임1>")
        elif 종류 == "보도자료":
            from datetime import datetime, timedelta
            self.문서여백(20, 20, 8, 15, 17, 10); self.기본정렬(); self.표만들기([40, 11, 22, 81.5], [6, 6])
            self.표전체(); self.폰트("맑은 고딕"); self.글자크기(12); self.글자간격(-10); self.셀한줄(1); self.캔슬(); self.표처음()
            self.셀선택(); self.표아래쪽(1); self.셀병합(); self.표테두리타입(8, 8, 8, 8); self.표테두리굵기(6, 6, 6, 6)
            요일 = ["월", "화", "수", "목", "금", "토", "일"]; 오늘 = datetime.today(); 조간 = 오늘 + timedelta(숫자)
            self.글자크기(13.5); self.가운데정렬(); self.문장(f"【보도자료({조간.month}.{조간.day}. 조간)】")
            self.표오른쪽(1); self.셀선택(); self.표아래쪽(1); self.셀병합(); self.표테두리타입(0, 0, 8, 1)
            self.표오른쪽(1); self.셀선택(); self.표아래쪽(1); self.셀병합(); self.가운데정렬()
            self.문장(f"’{str(오늘.year)[-2:]}.{오늘.month}.{오늘.day}.({요일[오늘.weekday()]})")
            self.표오른쪽(1); self.오른쪽정렬(); self.문장("디지털정부혁신실장 김실장 010-1234-5678")
            self.표오른쪽(4); self.오른쪽정렬(); self.문장("행정제도과장 김과장 010-1234-5678")
        if 종류 == "제거": self.대상.HAction.Run("HeaderFooterDelete")
        self.대상.SetPosBySet(현위치)
        return None

    def 기본서식큰명판(self, 부처명, 이미지):
        self.새창(); self.문서여백A4가로(10, 10, 10, 10, 10, 10); self.가운데정렬(); self.사진넣기절대값(이미지, 45, 18); self.폰트("맑은 고딕"); self.진하게(); self.글자크기(48); self.문장("\r\n" + 부처명); return None

    def 기본서식명판생성(self, 이미지):
        데이터 = self._선택표텍스트(); 행 = [데이터[i:i + 5] for i in range(0, len(데이터), 5)]; self.새창(); self.문서여백A4가로(15, 15, 10, 10, 10, 10)
        for 순번, 줄 in enumerate(x for x in 행[1:] if len(x) >= 3 and x[1].strip()):
            self.가운데정렬(); self.사진넣기절대값(이미지, 35, 15); self.폰트("맑은 고딕"); self.진하게(); self.글자크기(28); self.문장(줄[0] + "\r\n"); self.글자크기(54); self.문장(" ".join(줄[2]) if len(줄[2]) in (2, 3) else 줄[2]); self.대상.HAction.Run("BreakPage")
        return None

    def 기본서식1315호회의실(self, 이미지):
        데이터 = self._선택표텍스트(); 행 = [데이터[i:i + 5] for i in range(0, len(데이터), 5)][1:]; self.새창(); self.문서여백A4가로(10, 10, 10, 10, 10, 10)
        for 줄 in 행:
            if len(줄) < 3 or not 줄[1].strip(): continue
            self.사진넣기절대값(이미지, 30, 30); self.가운데정렬(); self.폰트("궁서체"); self.진하게(); self.글자크기(36); self.문장(줄[0] + "\r\n"); self.글자크기(70); self.문장(줄[2]); self.대상.HAction.Run("BreakPage")
        return None

    def 기본서식증감(self, 옵션, 옵션2):
        값 = self._선택표텍스트(); 숫자 = [float(re.sub(r"[^0-9.\-]", "", x) or 0) for x in 값]; 결과 = []
        for a, b in zip(숫자[::2], 숫자[1::2]):
            차 = b - a if 옵션 == "순증감" else a - b
            if 옵션 == "퍼센트": 차 = (b - a) / a * 100 if a else 0
            접두 = "▲" if 차 > 0 else "▼" if 차 < 0 else ""; 결과.append(f"{접두}{abs(차):g}" if 옵션2 else f"{차:g}")
        self.문장("\r\n".join(결과)); return None

    def _차트대체(self, 종류, 색상, 색상2=None):
        데이터 = self._선택표텍스트(); self.새창(); self.가운데정렬(); self.폰트("맑은 고딕"); self.진하게(); self.글자크기(16); self.문장(f"{종류} 차트\r\n"); self.기본정렬(); self.대상.HAction.Run("CharShapeNormal"); self.글자크기(10); self.문장("\r\n".join(데이터)); return None

    def 차트단일막대(self, 색상): return self._차트대체("단일 막대", 색상)
    def 차트가로막대(self, 색상): return self._차트대체("가로 막대", 색상)
    def 차트가로막대회색선(self, 색상, 색상2): return self._차트대체("가로 막대 회색선", 색상, 색상2)
    def 차트원형(self, 시작, 끝): return self._차트대체("원형", (시작, 끝))

    def 산인공시간계획표(self, 내용):
        항목 = [x.strip() for x in str(내용).split("엔터") if x.strip()]; self.표만들기([28, 130], [8] * max(1, len(항목))); self.표전체(); self.폰트("맑은 고딕"); self.글자크기(11); self.캔슬(); self.표처음()
        for i, x in enumerate(항목, 1): self.문장(f"{i:02d}:00"); self.표오른쪽(1); self.문장(x); self.표오른쪽(1)
        self.표나가기2(); return None

    def 산인공명찰생성(self, 이미지): return self.기본서식명판생성(이미지)
    def 산인공명패생성(self): return self.기본서식간담회명판()
    def 경남도명패(self, 이미지, 종류): return self.기본서식명판생성(이미지)

    def 인국공개인정보(self):
        self.표만들기([32, 68, 32, 68], [9, 9, 9]); self.표전체(); self.폰트("맑은 고딕"); self.글자크기(10); self.캔슬(); self.표처음()
        for x in ("성명", "", "소속", "", "연락처", "", "이메일", "", "개인정보 수집·이용 동의", "", "서명", ""): self.문장(x); self.표오른쪽(1)
        self.표나가기2(); return None

    def 인국공명패(self): return self.기본서식간담회명판()

    def 인천요지(self):
        표값 = self.문단여백측정() / 3
        self.표만들기([66 - 표값, 67 - 표값, 66 - 표값], [5, 1, 1, 210])
        self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableCellBlockExtend")
        self.표테두리타입(0, 0, 0, 0); self.표내부선타입(0, 0); self.캔슬(); self.대상.MovePos(106); self.대상.MovePos(104)
        self.표테두리단일선("하", 4, 1); self.표오른쪽(1); self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.MovePos(103); self.대상.HAction.Run("TableMergeCell")
        self.표테두리타입(8, 8, 8, 8); self.표테두리굵기(6, 6, 6, 6); self.폰트("HY헤드라인M"); self.글자크기(20); self.가운데정렬(); self.문장("요     지")
        self.표오른쪽(1); self.표테두리단일선("하", 4, 1); self.표오른쪽(1); self.표테두리단일선("좌", 4, 1); self.표오른쪽(2); self.표테두리단일선("우", 4, 1)
        self.표오른쪽(1); self.표테두리단일선("좌", 4, 1); self.표오른쪽(2); self.표테두리단일선("우", 4, 1); self.표오른쪽(1)
        self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.표오른쪽(2); self.대상.HAction.Run("TableMergeCell")
        self.표테두리단일선("좌", 4, 1); self.표테두리단일선("하", 4, 1); self.표테두리단일선("우", 4, 1); self.셀세로정렬(0)
        self.대상.HAction.Run("BreakPara"); self.대상.HAction.Run("BreakPara")
        def 인천요지반복():
            self.폰트("HY헤드라인M"); self.문단여백(5, 0); self.문단위(10); self.줄간격(160); self.글자크기(16); self.문장("□ 내용"); self.대상.HAction.Run("BreakPara")
            self.문단위(5); self.줄간격(160); self.글자크기(15); self.폰트("휴먼명조")
            for 내용 in (" ○ 내용", "  - 내용", " ○ 내용", "  - 내용"):
                self.문장(내용); self.대상.HAction.Run("BreakPara")
        인천요지반복(); 인천요지반복()
        self.대상.HAction.Run("BreakPara"); self.문장("요지생략개능"); self.대상.HAction.Run("MoveRight"); self.대상.HAction.Run("BreakPara"); self.대상.HAction.Run("ParagraphShapeAlignJustify")
        return None

    def 인천표준보고서(self, 이미지):
        self.문서여백(20, 20, 15, 10, 10, 10); self.줄간격(160); self.글자크기(20); self.폰트("휴먼명조")
        for _ in range(5): self.대상.HAction.Run("BreakPara")
        self.인천대제목("표준보고서 양식")
        for _ in range(10): self.대상.HAction.Run("BreakPara")
        self.인천로고(이미지); self.대상.HAction.Run("BreakPage"); self.인천요지(); self.대상.HAction.Run("BreakPage")
        self.인천보고서제목("보고서 제목"); self.인천점선박스("…방안을 수립, 추진함,"); self.문단위(0); self.줄간격(140); self.글자크기(10); self.대상.HAction.Run("BreakPara")
        def 인천표준보고기본(제목, 내용1, 내용2):
            self.폰트("HY헤드라인M"); self.문단위(15); self.줄간격(180); self.글자크기(18); self.문장(제목); self.대상.HAction.Run("BreakPara")
            for 내용 in (내용1, 내용2):
                self.문단위(10); self.줄간격(180); self.글자크기(16); self.대상.HAction.Run("CharShapeNormal"); self.대상.HAction.Run("CharShapeBold"); self.폰트("휴먼명조"); self.문장("□ " + 내용); self.대상.HAction.Run("BreakPara")
                self.문단위(0); self.줄간격(160); self.글자크기(15); self.대상.HAction.Run("CharShapeNormal"); self.문장("  ○ 내용"); self.대상.HAction.Run("BreakPara")
        인천표준보고기본("1. 추진배경", "내용", "내용"); 인천표준보고기본("2. ○○현황", "내용", "내용"); 인천표준보고기본("3. ○○활용실태 및 문제점", "내용", "활용상의 문제점")
        self.대상.HAction.Run("BreakPara"); self.대상.HAction.Run("BreakPara")
        인천표준보고기본("4. ○○추진방안", "내용", "활용상의 문제점"); 인천표준보고기본("5. 행정사항", "내용", "내용")
        for _ in range(5): self.대상.HAction.Run("BreakPara")
        self.인천참고(); self.인천기본("참고자료"); return None

    def 기본서식간담회명판(self):
        데이터리스트 = self._선택표텍스트()
        if not 데이터리스트: return None
        분할리스트 = [데이터리스트[i:i + 5] for i in range(0, len(데이터리스트), 5)]
        분할리스트 = [줄 for 줄 in 분할리스트 if len(줄) >= 3 and 줄[1].strip()][1:]
        self.새창(); self.문서여백A4가로(20, 20, 15, 15, 10, 10)
        def 이름띄우기(이름):
            return " ".join(이름) if len(이름) in (2, 3) else 이름
        for 순번, 줄 in enumerate(분할리스트):
            self.가운데정렬(); self.표만들기([147], [21, 49, 21, 49]); self.표전체(); self.폰트("맑은 고딕"); self.가운데정렬(); self.진하게(); self.캔슬(); self.표처음()
            for _ in range(2):
                self.글자크기(32); self.표배경색(28, 61, 98); self.글자색(255, 255, 255); self.셀한줄(1); self.문장(줄[0].replace("\r\n", " ")); self.표오른쪽(1)
                if len(줄[1]) <= 3: self.글자크기(35)
                self.문장(줄[1] + " "); self.글자크기(70); self.문장(이름띄우기(줄[2])); self.표오른쪽(1)
            self.표나가기()
            if 순번 != len(분할리스트) - 1: self.대상.HAction.Run("BreakPage")
        return None

    def _기본서식사진표(self, 단수, 종류, 선):
        from tkinter import filedialog
        이름 = filedialog.askopenfilenames(title="Open File", filetypes=[("image files", (".png", ".jpg"))])
        if not 이름: return None
        특수 = 종류 in ("산인공", "인국공")
        if 단수 == 3: 열너비, 사진행, 제목행 = ([51] * 3, 33, 7.3) if 특수 else ([50] * 3, 30, 4)
        else: 열너비, 사진행, 제목행 = ([79] * 2, 44.7, 7.3) if 특수 else ([75] * 2, 30, 4)
        self.가운데정렬(); self.표만들기(열너비, [사진행, 제목행]); self.표전체()
        if 선 == "투명": self.표테두리타입(0, 0, 0, 0); self.표내부선타입(0, 0)
        elif 선 == "점선": self.표테두리타입(3, 3, 3, 3); self.표내부선타입(3, 3)
        self.글자크기(12); self.가운데정렬(); self.진하게()
        if 종류 == "산인공": self.폰트("HY중고딕")
        elif 종류 == "인국공": self.중고딕()
        else: self.폰트("맑은 고딕")
        self.대상.HAction.Run("Copy"); self.캔슬(); self.표처음()
        높이 = {"소": 30, "중": 50, "대": 70}.get(종류, 사진행); 너비 = 50 if 단수 == 3 else (79 if 특수 else 75)
        for i, 경로 in enumerate(이름):
            if i and i % 단수 == 0: self.아래로붙이기()
            if i % 단수: self.표오른쪽(1)
            self.사진넣기절대값(경로, 너비, 높이)
            if i % 단수 == 단수 - 1 or i == len(이름) - 1:
                시작 = i - i % 단수
                for 제목경로 in 이름[시작:i + 1]:
                    self.표오른쪽(1); 매치 = re.search(r"\(([^()]+)\)(?!.*\()", 제목경로); self.문장(매치.group(1) if 매치 else "")
        self.표나가기(); return None

    def 기본서식사진표3단(self, 종류, 선): return self._기본서식사진표(3, 종류, 선)
    def 기본서식사진표2단(self, 종류, 선): return self._기본서식사진표(2, 종류, 선)

    def 차순정렬(self, 종류, 열순서):
        시도순 = ("서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원도", "충청북도", "충청남도", "전북특별자치도", "전라남도", "경상북도", "경상남도", "제주특별자치도")
        경남순 = ("창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군")
        정보 = self.셀정보()
        if not 정보 or 정보[0] != 1: return None
        _, 처음위치, 행, 열, 한줄, *_ = 정보; 블록리스트 = self.블록리스트생성(행, 열, 한줄, 처음위치); 데이터 = []
        try:
            for 셀번호 in 블록리스트:
                self.대상.SetPosBySet(self.셀위치(셀번호)); self.대상.HAction.Run("Select"); self.대상.InitScan(1, 255); 내용 = ""
                while True:
                    상태, 텍스트 = self.대상.GetText(); 내용 += 텍스트
                    if 상태 not in (2, 3): break
                self.대상.ReleaseScan(); 데이터.append(내용.replace("\r", " ").replace("\n", " ").strip())
            행데이터 = [데이터[i:i + 열] for i in range(0, len(데이터), 열)]; 인덱스 = max(0, min(열 - 1, int(열순서) - 1))
            def 키(항목):
                값 = 항목[인덱스]
                if 종류 in ("숫자오름차순", "숫자내림차순"):
                    try: return float(re.sub(r"[^0-9.\-]", "", 값))
                    except ValueError: return 0
                if 종류 == "짧은차순": return len(값)
                if 종류 == "시도순": return 시도순.index(값) if 값 in 시도순 else len(시도순)
                if 종류 == "경남순": return 경남순.index(값) if 값 in 경남순 else len(경남순)
                return 값
            행데이터.sort(key=키, reverse=종류 in ("문자내림차순", "숫자내림차순")); 정렬값 = [값 for 행값 in 행데이터 for 값 in 행값]
            for 셀번호, 값 in zip(블록리스트, 정렬값): self.대상.SetPosBySet(self.셀위치(셀번호)); self.대상.HAction.Run("Select"); self.문장(값)
        except ValueError as 오류: print(f"값 오류 : {오류}")
        except Exception as 오류: print(f"오류 발생 : {오류}")
        return None

    def 카이디스트(self, 키):
        """자유도 1 카이제곱 분포의 우측 확률을 반환한다.

        원본은 0.01 간격의 표를 사용했으며 같은 표의 통계적 정의를
        ``erfc(sqrt(x/2))``로 계산하여 표 범위 밖의 값도 처리한다.
        """
        import math
        값 = float(키)
        if 값 < 0: return 1
        if 값 > 15.23: return "0.0001 미만"
        return round(math.erfc(math.sqrt(값 / 2)), 5)

    def _역학2x2계산(self, a, b, c, d):
        import math
        a, b, c, d = map(float, (a, b, c, d))
        if min(a, b, c, d) == 0: a, b, c, d = (x + 0.5 for x in (a, b, c, d))
        노출할 = a / (a + b); 비노출할 = c / (c + d); 상대위험도 = 노출할 / 비노출할; 오즈비 = a * d / (b * c)
        rr오차 = math.sqrt(b / (a * (a + b)) + d / (c * (c + d))); or오차 = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        rr하, rr상 = math.exp(math.log(상대위험도) - 1.96 * rr오차), math.exp(math.log(상대위험도) + 1.96 * rr오차)
        or하, or상 = math.exp(math.log(오즈비) - 1.96 * or오차), math.exp(math.log(오즈비) + 1.96 * or오차)
        총합 = a + b + c + d; 카이 = 총합 * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d)); p값 = self.카이디스트(카이)
        return {"rr": 상대위험도, "or": 오즈비, "rr_ci": (rr하, rr상), "or_ci": (or하, or상), "chi2": 카이, "p": p값}

    def _선택표텍스트(self):
        if not self.대상.CellShape: return []
        self.대상.HAction.Run("Cancel"); self.대상.HAction.Run("TableCellBlock"); self.대상.HAction.Run("TableCellBlockExtend"); self.대상.HAction.Run("TableCellBlockExtend"); 마지막 = self.대상.GetPosBySet(); self.대상.InitScan(1, 255); self.대상.GetText(); self.대상.MovePos(201); 처음 = self.대상.GetPosBySet(); self.대상.ReleaseScan(); 결과 = []
        for i in range(처음.Item("List"), 마지막.Item("List") + 1):
            self.대상.SetPosBySet(self.셀위치(i)); self.대상.InitScan(0, 85); 내용 = ""
            while True:
                상태, 텍스트 = self.대상.GetText(); 내용 += 텍스트
                if 상태 in (0, 1): break
            self.대상.ReleaseScan(); 결과.append(내용.rstrip())
        return 결과

    def _역학결과텍스트(self, 결과):
        rr, or값 = 결과["rr"], 결과["or"]; rr하, rr상 = 결과["rr_ci"]; or하, or상 = 결과["or_ci"]
        rr해석 = f"먹은 사람은 안먹은 사람보다 질병에 걸릴 확률이 {round(rr, 2)}배 높다. " if rr > 1 else ("먹으나 안먹으나 똑같으니 의미없다. " if rr == 1 else f"질병 확률이 {round((1-rr)*100, 1)}% 낮다. ")
        rr해석 += ("\r\n동그라미: 이 결과는 의미없다.\r\n바: 상대위험도 95% 신뢰구간 안에 1이 존재함" if rr하 <= 1 <= rr상 else "\r\n동그라미: 이 결과는 유의미 하다.\r\n바: 상대위험도 95% 신뢰구간 안에 1이 존재하지 않음") + f"\r\n바: 상대위험도 95% 신뢰구간: {round(rr하,2)}~{round(rr상,2)}"
        or해석 = f"먹은 사람은 안먹은 사람보다 질병에 걸릴 위험이 {round(or값, 2)}배 높다. "
        or해석 += ("\r\n동그라미: 이 결과는 의미없다.\r\n바: 오즈비 95% 신뢰구간 안에 1이 존재함" if or하 <= 1 <= or상 else "\r\n동그라미: 이 결과는 유의미 하다.\r\n바: 오즈비 95% 신뢰구간 안에 1이 존재하지 않음") + f"\r\n바: 오즈비 95% 신뢰구간: {round(or하,2)}~{round(or상,2)}"
        return f"제목 : 결과\r\n\r\n네모:상대위험도 : {round(rr,3)}\r\n네모:오즈비 : {round(or값,3)}\r\n네모:p값 : {결과['p']}\r\n\r\n네모:상대위험도 해석 : {rr해석}\r\n\r\n네모:오즈비 해석 : {or해석}"

    def 역학rror계산(self):
        데이터 = self._선택표텍스트(); 숫자 = [int(float(re.sub(r"[^0-9.\-]", "", x))) for x in 데이터 if re.sub(r"[^0-9.\-]", "", x)]
        if len(숫자) >= 9: a, b, c, d = 숫자[4], 숫자[5], 숫자[7], 숫자[8]
        elif len(숫자) >= 4: a, b, c, d = 숫자[:4]
        else: return None
        self.마크다운응용(self._역학결과텍스트(self._역학2x2계산(a, b, c, d))); return None

    def 역학rror다중계산(self):
        데이터 = self._선택표텍스트(); 출력 = []
        for i in range(0, len(데이터), 5):
            줄 = 데이터[i:i + 5]
            if len(줄) < 5: continue
            try: 제목 = 줄[0]; a, b, c, d = [float(re.sub(r"[^0-9.\-]", "", x)) for x in 줄[1:5]]; r = self._역학2x2계산(a, b, c, d); 출력.append((r["p"] if isinstance(r["p"], float) else 0, f"{제목}\tRR {r['rr']:.3f}\tOR {r['or']:.3f}\tp {r['p']}"))
            except (ValueError, ZeroDivisionError): continue
        출력.sort(key=lambda x: x[0]); self.문장("\r\n".join(x[1] for x in 출력)); return None

    def 경남도행사장(self, 이미지, 단수, 행수):
        if isinstance(이미지, (str, os.PathLike)):
            이미지 = [os.fspath(이미지), os.fspath(이미지)]
        else:
            try:
                이미지 = list(이미지 or [])
            except TypeError:
                이미지 = []
        if not 이미지:
            return False
        if len(이미지) == 1:
            이미지.append(이미지[0])
        try:
            단수 = int(단수)
            행수 = int(행수)
        except (TypeError, ValueError):
            return False
        if 단수 <= 0 or 행수 <= 0:
            return False

        def 제목(내용, 명수):
            self.표만들기([85, 5, 191, 5, 85], [7, 6, 1.3]); self.셀여백제로(); self.표전체(); self.글자크기(1); self.가운데정렬(); self.폰트("HY헤드라인M"); self.표내부선타입(0, 0); self.표테두리타입(0, 0, 0, 0); self.캔슬(); self.표처음(); self.표오른쪽(2); self.셀선택(); self.표아래쪽(1); self.셀병합(); self.글자크기(31); self.문장(내용); self.표오른쪽(7); self.셀선택(); self.표아래쪽(1); self.셀병합(); self.글자크기(14); self.글자간격(-10); self.글자장평(95); self.표오른쪽(3); self.사진넣기절대값(이미지[0], 191, 2); self.표오른쪽(2); self.문장(명수); self.표테두리타입(1, 1, 1, 1); self.표나가기2()
        def 무대():
            self.표만들기([60, 60, 40, 44, 40, 60, 60], [22, 15]); self.표전체(); self.글자크기(12); self.가운데정렬(); self.진하게(); self.폰트("맑은 고딕"); self.표내부선타입(0, 0); self.표테두리타입(3, 0, 3, 3); self.표배경색(242, 242, 242); self.캔슬(); self.표처음()
            self.문장("무대 컨트롤"); self.표오른쪽(1); self.문장("사회자 대기"); self.표오른쪽(1); self.셀선택(); self.표오른쪽(2); self.셀병합(); self.폰트("HY헤드라인M"); self.글자크기(24); self.글자색(255, 255, 255); self.표배경색(29, 30, 66); self.문장("무    대"); self.표오른쪽(1); self.문장("프롬프트 운영"); self.표오른쪽(1); self.문장("군악대  /  예술단"); self.표오른쪽(3); self.문장("프롬프트 1\r\n"); self.표오른쪽(2); self.문장("프롬프트 2\r\n"); self.표나가기2()
        def 테이블(도지사수):
            if 단수 in (5, 7, 9):
                self.표만들기([39.6] * 9, [23, 5] * 6)
            elif 단수 in (6, 8):
                self.표만들기([45] * 8, [23, 5] * 6)
            else:
                self.표만들기([39.6] * 단수, [23, 5] * 6)
            self.표전체(); self.가운데정렬(); self.폰트("맑은 고딕"); self.진하게(); self.글자크기(12); self.표내부선타입(0, 0); self.표테두리타입(0, 3, 3, 3); self.캔슬(); self.표처음()
            if 단수 == 9:
                도지사수 = 14
            elif 단수 == 8:
                도지사수 = 13
            elif 단수 == 7:
                self.표오른쪽(1); 도지사수 = 11
            elif 단수 == 6:
                self.표오른쪽(1); 도지사수 = 10
            elif 단수 == 5:
                self.표오른쪽(2); 도지사수 = 8
            else:
                도지사수 = 100
            for i in range(행수 * 단수):
                if i % 단수 == 0 and i != 0:
                    if 단수 in (5, 7, 9):
                        self.표오른쪽(18 - 단수)
                    elif 단수 in (6, 8):
                        self.표오른쪽(16 - 단수)
                if i + 1 == 도지사수:
                    self.경남도원형탁자(str(i + 1), "메인", "도지사")
                    self.표아래쪽(1); self.문장("도지사"); self.표위쪽(1)
                else:
                    self.경남도원형탁자(str(i + 1), "창원", "지자체")
                self.표오른쪽(1)
        자동계산값 = 단수 * 행수 * 10; self.새창(); self.문서여백A3가로(15, 15, 10, 10, 15, 15); self.줄간격(160); 제목("범정부오피스 행사장 좌석 배치도", f"1테이블 10명 ({단수}열 {행수}행) {자동계산값}명 이상"); self.줄간격(75); 무대(); 테이블(2); return None

    def 금천보도자료상단표(self, 이미지1, 이미지2):
        from datetime import datetime
        self.표만들기([21, 27.5, 35, 14, 3, 21, 21], [5, 1, 14, 3, 6, 6, 6, 6])
        self.표전체(); self.표테두리타입(0, 0, 0, 0); self.표내부선타입(0, 0); self.글자크기(1); self.캔슬(); self.표처음()
        self.셀선택(); self.표오른쪽(6); self.셀병합(); self.표테두리타입(3, 3, 3, 3)
        self.폰트("맑은 고딕"); self.글자크기(10); self.가운데정렬()
        오늘 = datetime.today(); 요일 = "월화수목금토일"[오늘.weekday()]
        self.문장(f"{오늘.month}.{오늘.day}.({요일}) / 이 보도자료는 배포 즉시 보도할 수 있습니다.")
        self.표오른쪽(8); self.셀선택(); self.표오른쪽(1); self.셀병합(); self.사진넣기배경(이미지1)
        self.표오른쪽(1); self.셀선택(); self.표오른쪽(1); self.셀병합(); self.폰트("양재튼튼체B"); self.글자크기(30); self.가운데정렬(); self.진하게(); self.문장("보도자료")
        self.표오른쪽(1); self.셀선택(); self.표오른쪽(2); self.셀병합(); self.사진넣기배경(이미지2)
        self.표오른쪽(8); self.셀선택(); self.표오른쪽(2); self.셀병합(); self.폰트("맑은 고딕"); self.글자크기(13); self.진하게(); self.문장(" 담당부서 : 부서명 팀명")
        for 직위 in ("과  장", "이름", "2627-0000", "팀  장", "이름", "2627-0000", "담  당", "이름", "2627-0000", "￭ 총 1쪽", "￭ 사진 1장", "언론팀", "", "2627-0000"):
            self.표오른쪽(1); self.폰트("맑은 고딕"); self.글자크기(11); self.문장(직위)
        self.대상.HAction.Run("MoveRight"); self.대상.HAction.Run("BreakPara"); self.기본정렬()

    def 금감보도자료상단표(self, 이미지1, 이미지2):
        from datetime import datetime, timedelta
        self.표만들기([16.5, 30.5, 16.5, 14, 20, 17, 33], [14, .2, 8.5, .2, 5, 5, 5, 5, .2, 29, 1, 45])
        self.셀여백제로(); self.표전체(); self.폰트("맑은 고딕"); self.글자크기(12); self.가운데정렬(); self.캔슬(); self.표처음()
        self.셀선택(); self.표오른쪽(1); self.셀병합(); self.사진넣기배경(이미지1)
        self.표오른쪽(1); self.셀선택(); self.표오른쪽(2); self.셀병합(); self.폰트("HY헤드라인M"); self.글자크기(25); self.진하게(); self.문장("보 도 자 료")
        self.표오른쪽(1); self.셀선택(); self.표오른쪽(1); self.셀병합(); self.사진넣기배경(이미지2)
        self.표오른쪽(1); self.셀선택(); self.표오른쪽(6); self.셀병합(); self.글자크기(1); self.표테두리타입(1, 1, 0, 0)
        내일 = datetime.today() + timedelta(days=1); 요일 = "월화수목금토일"
        for 내용 in ("보도", f"{내일.year}. {내일.month}. {내일.day}.({요일[내일.weekday()]}) 조간/석간", "배포", f"{datetime.today().month}. {datetime.today().day}.({요일[datetime.today().weekday()]})", "담당부서", "○○○○국\r\n○○○○팀", "책임자", "국장", "○○○", "(02-3145-0000)", "담당자", "팀장", "○○○", "(02-3145-0000)"):
            self.문장(내용); self.표오른쪽(1)
        self.대상.HAction.Run("MoveRight"); self.대상.HAction.Run("BreakPara"); self.기본정렬()

    def 금천보도자료(self, 이미지1, 이미지2):
        self.새창(); self.문서여백(20, 20, 15, 15, 10, 10); self.금천보도자료상단표(이미지1, 이미지2); self.표만들기([204 - self.문단여백측정()], [50]); self.폰트("HY견고딕"); self.줄간격(130); self.글자크기(24); self.대상.HAction.Run("ParagraphShapeAlignCenter"); self.문장("제목(견고딕 24pt, 줄간격 130%)"); self.대상.HAction.Run("BreakPara"); self.글자크기(14); self.문장("- 부제목 (견고딕 14pt, 줄간격 130%) -"); self.대상.HAction.Run("BreakPara"); self.대상.HAction.Run("ParagraphShapeAlignJustify"); self.폰트("맑은 고딕"); self.줄간격(160); self.글자크기(13); self.문장(" - 맑은 고딕 13pt 줄간격 160%\r\n - 본문 내용 중 주요 내용 기입"); self.표나가기2(); self.줄간격(180); self.글자크기(13.5); self.문장(" - 본문, 맑은 고딕 13.5pt, 줄간격 180%\r\n - 핵심을 앞쪽에 부연 설명은 뒤쪽\r\n - 문장은 되도록 간결하게 단문으로 작성\r\n - 마지막은 문의할 수 있는 곳 기입\r\n - 참고할 수 있는 자료(계획서 등)와 사진(이미지) 파일 별도 첨부"); self.글자크기(12); self.문장("\r\n< (사진 설명) 맑은 고딕 12pt, 원본 사진은 별첨 >"); return None

    def 금감보도자료(self, 이미지1, 이미지2):
        self.새창(); self.문서여백(18, 18, 15, 15, 10, 10); self.금감보도자료상단표(이미지1, 이미지2); self.쪽번호(); self.줄간격(160); self.글자크기(12); self.대상.HAction.Run("BreakPara"); self.폰트("HY헤드라인M"); self.글자크기(16); self.문장("1. HY헤드라인M 16p"); self.대상.HAction.Run("BreakPara"); self.폰트("휴먼명조"); self.문장("□ 금융감독원은 ~\r\n ◦ 휴먼명조 16p"); self.금감보도자료하단(); return None
    def 농어촌두셀비교(self):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        self.대상.ReleaseScan()
        for i in range(2):
            self.대상.SetPosBySet(self.셀위치(처음위치.Item("List") + i))
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("Select")
            self.대상.HAction.Run("Select")
            try:
                self.대상.InitScan(1, 255)
                블록스캔값, 텍스트 = self.대상.GetText()
                결과텍스트 = ""
                while 블록스캔값 in (2, 3):
                    결과텍스트 += 텍스트
                    블록스캔값, 텍스트 = self.대상.GetText()
                self.대상.ReleaseScan()
                데이터리스트.append(결과텍스트)
                self.문장(결과텍스트 + " ")
            except ValueError as 오류:
                print(f"값 오류 : {오류}")
                self.대상.ReleaseScan()
            except Exception as 오류:
                print(f"오류 발생 : {오류}")
                self.대상.ReleaseScan()
        비교문1 = 데이터리스트[0].split()
        비교문2 = 데이터리스트[1].split()
        공통단어 = set(비교문1).intersection(set(비교문2))
        경고 = ""
        if len(비교문2) != len(set(비교문2)):
            경고 = "문장에 똑같은 어절이 1쌍 이상 있습니다. 이는 잘못 마스킹되었을 수 있습니다."
        결과문 = []
        for 단어 in 비교문2:
            결과문.append("-" * len(단어) if 단어 in 공통단어 else 단어)
        결과문 = " ".join(결과문)
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.폰트("휴먼명조")
        self.글자크기(10)
        self.문장(데이터리스트[0] + "\r\n\r\n" + 데이터리스트[1] + "\r\n\r\n" + 결과문 + "\r\n\r\n" + 경고)

    def 농어촌맞춤정렬(self):
        데이터리스트 = []
        if not self.대상.CellShape:
            return None
        self.대상.HAction.Run("Cancel")
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.대상.HAction.Run("TableCellBlockExtend")
        블록마지막 = self.대상.KeyIndicator()[-1][1:].split(")")[0]
        열개수 = ord(re.sub(r"[^A-Z]", "", 블록마지막)) - 64
        마지막위치 = self.대상.GetPosBySet()
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        self.대상.MovePos(201)
        처음위치 = self.대상.GetPosBySet()
        for i in range(처음위치.Item("List"), 마지막위치.Item("List") + 1):
            결과텍스트 = ""
            self.대상.SetPosBySet(self.셀위치(i))
            self.대상.InitScan(0, 85)
            while True:
                블록스캔값, 텍스트 = self.대상.GetText()
                if 블록스캔값 not in (2, 3):
                    break
                결과텍스트 += 텍스트
            데이터리스트.append(결과텍스트.rstrip())
            self.대상.ReleaseScan()
        데이터분리 = [데이터리스트[i:i + 열개수] for i in range(0, len(데이터리스트), 열개수)]
        데이터윗줄삭제 = 데이터분리[1:]
        정렬기준 = [데이터[0] for 데이터 in 데이터윗줄삭제]
        for 데이터 in 데이터윗줄삭제:
            del 데이터[0]
        정렬된데이터 = sorted(
            데이터윗줄삭제,
            key=lambda x: 정렬기준.index(x[0]) if x[0] in 정렬기준 else float("inf"),
        )
        정렬된데이터.insert(0, 데이터분리[0][1:])
        데이터행 = len(정렬된데이터)
        데이터열 = len(정렬된데이터[0])
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.표만들기([19] * 데이터열, [4] * 데이터행)
        for 행 in 정렬된데이터:
            for 데이터 in 행:
                self.문장(데이터)
                self.표오른쪽(1)
        self.제목셀반복()

    def 제주교업무흐름도(self, 그림):
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.표만들기([38, 5, 115.5], [10] + [3, 9, 27] + [6, 9, 27] * 4)
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표테두리굵기(7, 7, 1, 1)
        self.표내부선타입(0, 0)
        self.표내부선굵기(7, 1)
        self.폰트("한컴돋움")
        self.글자크기(12)
        self.표내부선색(149, 149, 149)
        self.표테두리색(149, 149, 149)
        self.캔슬()
        self.표처음()
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(201, 238, 238)
        self.글자크기(15)
        self.가운데정렬()
        self.진하게()
        self.문장("구  분")
        self.표오른쪽(2)
        self.표배경색(201, 238, 238)
        self.글자크기(15)
        self.가운데정렬()
        self.진하게()
        self.문장("업무처리 내용")
        self.표테두리타입(1, 1, 1, 1)
        self.표오른쪽(1)
        for i in range(0, 5):
            self.표오른쪽(3)
            self.글자크기(12)
            self.가운데정렬()
            self.문장("주요내용")
            self.표배경색(255, 247, 204)
            self.표테두리타입(1, 0, 1, 1)
            self.표오른쪽(2)
            self.셀선택()
            self.표아래쪽(1)
            self.셀병합()
            self.문장("∙ 세부내용\r\n∙ \r\n∙ ")
            self.표테두리타입(1, 1, 1, 1)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 1, 1)
            if i != 4:
                self.표오른쪽(3)
                self.사진넣기절대값(그림, 5, 6)
        self.표나가기2()

    def 기본서식보도자료담당(self, 단=1):
        self.표만들기([18.5, 50, 17.5, 17, 16, 28], [4.7] * 단 * 2)
        self.셀여백제로()
        self.표전체()
        self.글자크기(10)
        self.폰트("돋움체")
        self.가운데정렬()
        self.캔슬()
        self.줄간격(130)
        self.표처음()
        self.셀선택()
        self.표아래쪽(단 * 2 - 1)
        self.셀병합()
        self.문장("담당 부서")
        self.표오른쪽(1)
        for i in range(0, 단):
            if i != 0:
                self.표오른쪽(2)
            self.셀선택()
            self.표아래쪽(1)
            self.셀병합()
            self.문장("행정안전부\r\n행정제도과")
            self.표오른쪽(1)
            self.문장("책임자")
            self.표오른쪽(1)
            self.오른쪽정렬()
            self.문장("과  장")
            self.표오른쪽(1)
            self.오른쪽정렬()
            self.문장("김과장")
            self.표테두리타입(1, 1, 0, 0)
            self.표오른쪽(1)
            self.기본정렬()
            self.문장("(044-205-2250)")
            self.표오른쪽(3)
            self.문장("담당자")
            self.표오른쪽(1)
            self.오른쪽정렬()
            self.문장("사무관")
            self.표오른쪽(1)
            self.오른쪽정렬()
            self.문장("김사무")
            self.표테두리타입(1, 1, 0, 0)
            self.표오른쪽(1)
            self.기본정렬()
            self.문장("(044-205-2250)")
        self.표나가기()

    def 인국공표지목차(self, 이미지1, 이미지2):
        self.글자크기(20)
        self.문단위(0)
        self.엔터(4)
        self.인국공대제목(이미지1)
        self.엔터(4)
        self.폰트("HY헤드라인M")
        self.가운데정렬()
        self.오늘날짜숫자만()
        self.엔터(6)
        self.인국공부처(이미지2)
        self.페이지엔터()
        self.글자크기(15)
        self.엔터(1)
        self.인국공목차제목()
        self.글자크기(10)
        self.엔터(2)
        self.표만들기([205.5 - self.문단여백측정()], [205])
        self.탭점선설정(95000)

        def 큰탭(숫자, 내용):
            self.문단여백(10, 10)
            self.줄간격(160)
            self.글자크기(18)
            self.기본정렬()
            self.기본글자()
            self.진하게()
            self.폰트("HY견명조")
            self.문장(숫자)
            self.기본글자()
            self.폰트("HY헤드라인M")
            self.문장(내용)
            self.대상.HAction.Run("InsertTab")
            self.문단위(10)
            self.문단아래(10)
            self.문장(" 1")
            self.엔터(1)

        def 작은탭(내용):
            self.줄간격(160)
            self.문단여백(25, 10)
            self.글자크기(16)
            self.기본정렬()
            self.기본글자()
            self.폰트("맑은 고딕")
            self.문장(내용)
            self.대상.HAction.Run("InsertTab")
            self.문단위(0)
            self.문단아래(0)
            self.문장(" 1")
            self.엔터(1)

        큰탭("Ⅰ.", " ○○")
        큰탭("Ⅱ.", " ○○")
        작은탭("1. ○○")
        작은탭("2. ○○")
        큰탭("Ⅲ.", " ○○")
        작은탭("1. ○○")
        작은탭("2. ○○")
        큰탭("Ⅳ.", " ○○")
        작은탭("1. ○○")
        작은탭("2. ○○")
        작은탭("3. ○○")
        큰탭("Ⅴ.", " ○○")
        작은탭("1. ○○")
        작은탭("2. ○○")
        작은탭("3. ○○")
        작은탭("4. ○○")
        작은탭("5. ○○")
        self.백스페이스()
        self.표나가기2()

    def 광주광산오정리(self):
        시작지점 = self.블록첫위치()
        체크 = 0
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            결과텍스트 = ""
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔값, 텍스트 = self.대상.GetText()
            self.대상.ReleaseScan()
            결과텍스트 = re.sub(" o ", "", 결과텍스트)
            결과텍스트 = re.sub(" o +o ", "", 결과텍스트)
            self.문장(결과텍스트)
            체크 = 1
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

    def AI행정지원계획서간단서식(self):
        self.대상.InitScan(1, 255)
        try:
            블록스캔값, 텍스트 = self.대상.GetText()
            결과텍스트 = ""
            while 블록스캔값 in (2, 3):
                결과텍스트 += 텍스트
                블록스캔값, 텍스트 = self.대상.GetText()
            self.대상.ReleaseScan()
            결과텍스트 += "\r\n"
            결과텍스트 = re.sub(r"1\.\s*제목\r\n(.*)\r\n", "제목: \\1\r\n", 결과텍스트)
            결과텍스트 = re.sub(r"^\d+\.\s*(.*)\r\n", "네모: \\1\r\n", 결과텍스트, flags=re.MULTILINE)
            결과텍스트 = re.sub(r"^(?!제목:|네모:)([^\r\n]+)\r\n", "원:\\1\r\n", 결과텍스트, flags=re.MULTILINE)
            self.백스페이스()
            시작지점 = self.현재위치()
            self.문장(결과텍스트)
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
            if not 결과텍스트.strip():
                # The original markdown formatter deletes an empty generated
                # block and performs no formatting work.
                self.대상.HAction.Run("Delete")
                return None
            self.기본서식마크다운()
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
            self.대상.ReleaseScan()
        except Exception as 오류:
            print(f"오류 발생 : {오류}")
            self.대상.ReleaseScan()

    def 역학날짜매기기(self):
        def 날짜배열(날짜, 개수):
            시작날짜 = datetime.strptime(날짜, "%Y-%m-%d")
            return [(시작날짜 + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(개수)]

        if not self.대상.CellShape:
            return None
        try:
            정상, 처음위치, 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열 = self.셀정보()
            if 정상 != 1:
                return None
            블록리스트 = self.블록리스트생성(행, 열, 한줄, 처음위치)
            날짜배열본 = []
            for i in range(len(블록리스트)):
                self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                self.대상.HAction.Run("Select")
                self.대상.HAction.Run("Select")
                self.대상.HAction.Run("Select")
                if i == 0:
                    self.대상.InitScan(1, 255)
                    블록스캔 = self.대상.GetText()
                    처음날짜 = 블록스캔[1]
                    self.대상.ReleaseScan()
                    날짜배열본 = 날짜배열(처음날짜, len(블록리스트))
                self.문장(str(날짜배열본[i]))
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 제주대목차(self, 이미지):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.표만들기([205 - self.문단여백측정()], [240])
        self.엔터(1)
        self.제주대목차제목(이미지)
        self.글자크기(15)
        self.줄간격(180)
        self.엔터(1)
        self.탭점선설정()
        self.문단여백(15, 15)

        def 큰글자(로마, 내용, 숫자):
            self.폰트("바탕")
            self.기본글자()
            self.진하게()
            self.글자크기(17)
            self.문장(로마 + ". ")
            self.기본글자()
            self.글자크기(15)
            self.폰트("HY헤드라인M")
            self.문장(내용)
            self.대상.HAction.Run("InsertTab")
            self.문장(" " + 숫자)
            self.엔터(1)

        def 작은글자(내용, 숫자):
            self.폰트("HY헤드라인M")
            self.기본글자()
            self.글자크기(12)
            self.문장("  □ ")
            self.문장(내용)
            self.대상.HAction.Run("InsertTab")
            self.문장(" " + 숫자)
            self.엔터(1)

        큰글자(self.로마숫자[1], "전형일정", "1")
        큰글자(self.로마숫자[2], "모집단위 및 모집인원", "3")
        큰글자(self.로마숫자[1], "수시모집 전형", "8")
        작은글자("학생부교과(일반학생)", "8")
        작은글자("학생부교과(지역인재)", "10")
        작은글자("학생부교과(지역인재고른기회)", "12")
        큰글자(self.로마숫자[4], "정시모집(나/다군) 전형", "34")
        큰글자(self.로마숫자[5], "기타내용", "34")
        큰글자(self.로마숫자[6], "기타내용", "34")
        큰글자(self.로마숫자[7], "기타내용", "34")
        큰글자(self.로마숫자[8], "기타내용", "34")
        큰글자(self.로마숫자[9], "기타내용", "34")
        self.엔터(7)

    def 남해행사요약서(self, 이미지0, 이미지1, 이미지2):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.남해상단이중(이미지2)
        self.남해행사요약서제목(이미지0, 이미지1)
        self.남해기획서론박스("개최 목적 및 참석 의의 등\r\n맑은고딕 14p / 표 상하 이중실선 0.4㎜, 좌우 선없음")

        def 남해행사네모(내용):
            self.줄간격(160)
            self.폰트("HY헤드라인M")
            self.글자크기(17)
            self.글자색(0, 0, 128)
            self.문장(" " + 내용)
            self.대상.HAction.Run("BreakPara")
            self.글자색(0, 0, 0)

        def 남해행사원(내용):
            self.줄간격(160)
            self.폰트("휴먼명조")
            self.글자크기(15)
            self.문장("  ❍ " + 내용)
            self.대상.HAction.Run("BreakPara")

        def 남해행사바(내용):
            self.줄간격(160)
            self.폰트("휴먼명조")
            self.글자크기(15)
            self.문장("     - " + 내용)
            self.대상.HAction.Run("BreakPara")

        남해행사네모("행사개요")
        남해행사원("일시 및 장소 : 2025. 3. 10.(월) 11:30 / 유배문학관 광장")
        남해행사원("주요내용 : ○○○○ 전달식, 인사말씀 등(소요시간 20~30분)")
        남해행사원("참석대상 : 10명 정도")
        남해행사바("○○대표이사, ○○○○연합회장, ○○○○과장 등")
        남해행사네모("진행순서")
        self.남해행사진행()
        남해행사네모("추진경과(참고사항)")
        남해행사원("2대 추가 지원(총 7대) : 20xx년 x월")
        남해행사원("○○○○ 지원 조례 제정 : 20xx년 x월")
        남해행사원("○○○○ 이용에 따른 건의사항 등 접수, 지속적인 개선 노력")
        self.엔터(1)
        남해행사네모("군수님 하실 일 : 전달식, 인사말씀, 사진촬영 및 관람")
        self.폰트("휴먼명조")
        self.글자크기(15)
        self.엔터(1)
        self.문장("붙임  인사말씀 1부.  끝.")

    def 금감업무정보본문(self):
        self.표만들기([33, 169 - self.문단여백측정()], [229, 8])
        self.대상.HAction.Run("TableCellBlock")
        self.대상.HAction.Run("TableCellBlockExtend")
        self.표오른쪽(1)
        self.대상.HAction.Run("TableMergeCell")
        self.표테두리굵기(6, 6, 6, 6)
        self.셀세로정렬(0)

        def 기본반복(내용):
            self.줄간격(155)
            self.글자크기(6)
            self.대상.HAction.Run("BreakPara")
            self.폰트("휴먼명조")
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-26.4)
            self.대상.HAction.Run("InsertFixedWidthSpace")
            self.문장("□")
            self.대상.HAction.Run("InsertFixedWidthSpace")
            self.대상.HAction.Run("InsertFixedWidthSpace")
            self.폰트("맑은 고딕")
            self.대상.HAction.Run("CharShapeBold")
            self.문장("(" + 내용 + ")")
            self.대상.HAction.Run("CharShapeNormal")
            self.폰트("휴먼명조")
            self.휴먼명조()
            self.문장("휴먼명조 15p")
            self.대상.HAction.Run("BreakPara")
            self.글자크기(6)
            self.대상.HAction.Run("BreakPara")
            self.폰트("휴먼명조")
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-30.3)
            self.문장(" ◦ 휴먼명조 15p")
            self.대상.HAction.Run("BreakPara")

        기본반복("개요")
        기본반복("주요 내용")
        self.금감업무정보점선박스()
        self.금감업무정보점선박스2()
        기본반복("향후 계획")
        self.표오른쪽(1)
        self.표테두리굵기(6, 6, 6, 1)
        self.대상.HAction.Run("ParagraphShapeAlignCenter")
        self.대상.HAction.Run("CharShapeBold")
        self.글자크기(14)
        self.폰트("휴먼명조")
        self.휴먼명조()
        self.문장("정보수집자")
        self.표오른쪽(1)
        self.표테두리굵기(6, 6, 1, 6)
        self.대상.HAction.Run("ParagraphShapeAlignCenter")
        self.글자크기(14)
        self.폰트("휴먼명조")
        self.휴먼명조()
        self.문장("팀장 ☆☆☆(☎1111),  선임조사역 ◎◎◎(☎2222)")

    def _경남도사진표(self, 단수, 열너비, 사진너비):
        이름 = self.파일목록사진()
        self.표만들기([열너비] * 단수, [7.7, 54])
        self.표전체()
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(6, 6, 1, 1)
        self.폰트("맑은 고딕")
        self.글자크기(12)
        self.가운데정렬()
        self.진하게()
        self.캔슬()
        self.표처음()
        self.셀선택()
        if 단수 == 2:
            self.표오른쪽(1)
        else:
            self.표오른쪽끝()
        self.표테두리단일선("하", 6, 8)
        self.표배경색(223, 230, 247)
        self.캔슬()
        self.표전체()
        self.대상.HAction.Run("Copy")
        self.캔슬()
        self.표처음()

        for i in range(len(이름)):
            if i != 0 and i % 단수 == 0:
                if 단수 == 2:
                    print(i)
                self.아래로붙이기()
            if i != 0:
                self.표오른쪽(1)
            if i % 단수 == 0:
                for 번호 in range(1, 단수 + 1):
                    if i != 0:
                        self.표테두리단일선("상", 1, 1)
                    self.문장("사진" + str(i + 번호))
                    self.표오른쪽(1)
            self.사진넣기절대값(이름[i], 사진너비, 53)
        self.표나가기2()

    def 경남도사진2단(self):
        self._경남도사진표(2, 81, 80)

    def 경남도사진3단(self):
        self._경남도사진표(3, 53, 52)

    def 영덕바다괄호(self):
        텍스트 = self.블록스캔()[1]
        if "\r" in 텍스트:
            return None
        try:
            self.딜리트()
            self.기본글자()
            self.폰트("영덕바다체")
            self.글자크기(14)
            self.글자간격(-50)
            self.글자장평(90)
            self.문장("(")
            self.글자간격(0)
            self.문장(텍스트 + ")")
        except ValueError as 오류:
            print(f"값 오류 : {오류}")
        except Exception as 오류:
            print(f"오류 발생 : {오류}")

    def 서교공딸깍보고서(self, 내용, 예시):
        self.새창()
        self.문서여백(18, 18, 12.7, 12.7, 12.7, 12.7)
        시작지점 = self.현재위치()
        self.문장(내용)
        종료지점 = self.현재위치()
        if 예시 == 1 or 예시 == 2:
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run("Select")
            self.대상.SetPosBySet(종료지점)
        self.서교공궁극의정리범위()
        if 예시 == 2:
            self.대상.HAction.Run("SelectAll")
            self.줄간격(180)
            self.캔슬()


__all__ = ["Hwp1InstitutionFeatureMixin", "Hwp2InstitutionFeatureMixin", "MainInstitutionFeatureMixin"]
