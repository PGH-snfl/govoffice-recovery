"""텍스트 블록과 구조화된 텍스트 변환의 소스 복구본."""

import json
import re
from datetime import datetime


class HwpTextFeatureMixin:
    def 글머리지정(self, 글머리, 폰트, 크기, 내어쓰기, 진하게, 위=0, 줄간=160):
        시작지점 = self.블록첫위치()
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
        한글찾기 = re.compile(r"[(가-힣0-9a-zA-Z“]+")
        결과텍스트 = ""
        체크 = 0
        try:
            while 블록스캔값 in (2, 3):
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]
                결과텍스트 += 글머리 + 글꼬리
                블록스캔 = self.대상.GetText()
                블록스캔값, 텍스트 = 블록스캔[0], 블록스캔[1]
                체크 = 1
            self.대상.ReleaseScan()
            self.문장(결과텍스트)
        except ValueError as e:
            print(f"값 오류 : {e}")
            self.대상.ReleaseScan()
            체크 = 0
        except Exception as e:
            print(f"오류 발생 : {e}")
            self.대상.ReleaseScan()
            체크 = 0
            self.대상.ReleaseScan()
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트("맑은 고딕")
            self.문장("표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.")
        if 체크 != 1:
            return None
        종료지점 = self.현재위치()
        self.대상.SetPosBySet(시작지점)
        self.대상.HAction.Run("Select")
        self.대상.SetPosBySet(종료지점)
        self.글자스타일(0)
        self.자간헌터(0)
        self.내어쓰기(내어쓰기)
        self.글자간격(0)
        self.대상.HAction.Run("ParagraphShapeAlignJustify")
        self.대상.HAction.Run("CharShapeNormal")
        if 진하게 == 1:
            self.대상.HAction.Run("CharShapeBold")
        if 폰트 == "신명조":
            self.신명조()
        elif 폰트 == "중고딕":
            self.중고딕()
        elif 폰트 == "진휴먼명조":
            self.휴먼명조()
        else:
            self.폰트(폰트)
        self.글자크기(크기)
        self.줄간격(줄간)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(위)

    def 마크다운배열생성(self):
        def 콜론처리(배열):
            return [아이템 if ":" in 아이템 else "엔터:엔터" for 아이템 in 배열]

        def 엔터처리(배열):
            return [["엔터", "엔터"] if 아이템 == [""] else 아이템 for 아이템 in 배열]

        def 키워드처리(배열):
            오늘 = datetime.today().strftime("%Y%m%d")
            return [[아이템.replace("#오늘날짜", 오늘) for 아이템 in 내부배열] for 내부배열 in 배열]

        def 특수문자제거(배열):
            패턴 = re.compile(r"[^가-힣0-9\s]")
            return [[패턴.sub("", 아이템[0]), 아이템[1]] for 아이템 in 배열]

        def 배열공백제거(배열):
            return [[아이템.strip() for 아이템 in 내부배열] for 내부배열 in 배열]

        블록내용 = self.블록텍스트()
        줄나누기 = 콜론처리(블록내용.split("\r\n"))
        콜론나누기 = [s.split(":", 1) for s in 줄나누기]
        return 배열공백제거(특수문자제거(키워드처리(엔터처리(콜론나누기))))

    def 마크다운배열생성2(self):
        def 콜론처리(배열):
            return [아이템 if ":" in 아이템 else "엔터:엔터" for 아이템 in 배열]

        def 엔터처리(배열):
            return [["엔터", "엔터"] if 아이템 == [""] else 아이템 for 아이템 in 배열]

        def 키워드처리(배열):
            오늘 = datetime.today().strftime("%Y%m%d")
            return [[아이템.replace("#오늘날짜", 오늘) for 아이템 in 내부배열] for 내부배열 in 배열]

        def 특수문자제거(배열):
            패턴 = re.compile(r"[^가-힣0-9\s]")
            return [[패턴.sub("", 아이템[0]), 아이템[1]] for 아이템 in 배열]

        def 배열공백제거(배열):
            return [[아이템.strip() for 아이템 in 내부배열] for 내부배열 in 배열]

        중간처리 = []
        for 아이템 in self.블록텍스트().split("\r\n"):
            텍스트 = 아이템.strip()
            변환규칙 = (
                (("□", "네모 "), r"^(□|네모)\s*", "네모:"),
                (("○", "원 "), r"^(○|원)\s*", "원:"),
                (("-", "바 "), r"^(-|바)\s*", "바:"),
                (("※", "당구 ", "당구장 "), r"^(※|당구장|당구)\s*", "당구장:"),
                (("부서 ",), r"^(부서)\s*", "부서:"),
                (("제목 ",), r"^(제목)\s*", "제목:"),
            )
            for 접두어, 패턴, 대체어 in 변환규칙:
                if 텍스트.startswith(접두어):
                    텍스트 = 대체어 + re.sub(패턴, "", 텍스트, count=1)
                    break
            중간처리.append(텍스트)
        콜론나누기 = [s.split(":", 1) for s in 콜론처리(중간처리)]
        return 배열공백제거(특수문자제거(키워드처리(엔터처리(콜론나누기))))

    def 증감계산(self, 데이터, 종류):
        def 로으로(단어):
            if not 단어:
                return "으로"
            유니코드 = ord(단어[-1]) - ord("가")
            if 유니코드 < 0 or 유니코드 > 11171:
                return "으로"
            종성 = 유니코드 % 28
            return "로" if 종성 in (0, 8) else "으로"

        결과값 = ""
        데이터초기값 = str(데이터).split("로")[0]
        구분자 = "→" if "→" in 데이터초기값 else (">" if ">" in 데이터초기값 else None)
        if 구분자 is None:
            # 원본은 구분자가 없는 입력에서 미정 지역변수를 참조해
            # UnboundLocalError를 냈다. 버튼을 빈 값으로 눌러도 문서/GUI가
            # 중단되지 않도록 입력을 그대로 돌려준다.
            return 데이터초기값
        앞, 뒤 = (부분.strip() for 부분 in 데이터초기값.split(구분자, 1))
        단위 = re.sub(r"[\d.]", "", 앞)
        앞 = re.sub(r"[^0-9.]", "", 앞)
        뒤 = re.sub(r"[^0-9.]", "", 뒤)
        if not 앞 or not 뒤:
            return 데이터초기값
        try:
            앞값 = float(앞)
            뒤값 = float(뒤)
        except (TypeError, ValueError):
            return 데이터초기값
        if 앞값 == 0 and 뒤값 != 0:
            # 0을 기준으로 한 증가율은 정의되지 않으므로 원본 숫자만
            # 보존한다.  0→0은 아래의 변화없음 경로에서 처리한다.
            return 데이터초기값
        임시퍼센트 = 0
        임시증감 = ""
        임시증감기호 = ""
        소수자리기준 = len(앞.split(".")[1]) if "." in 앞 else 0
        소수자리기준2 = len(뒤.split(".")[1]) if "." in 앞 else 0
        소수자리기준 = max(소수자리기준, 소수자리기준2)
        if 앞값 < 뒤값 and 앞값 != 0:
            임시퍼센트 = ((뒤값 - 앞값) / 앞값) * 100
            임시절대값 = 뒤값 - 앞값
            임시증감, 임시증감기호 = "증가", "↑"
        elif 앞값 > 뒤값 and 앞값 != 0:
            임시퍼센트 = ((앞값 - 뒤값) / 앞값) * 100
            임시절대값 = 앞값 - 뒤값
            임시증감, 임시증감기호 = "감소", "↓"
        try:
            if 종류 in ("퍼센트정수", "퍼센트소수"):
                if 앞값 == 뒤값:
                    return 앞 + "%→" + 뒤 + "%로 변화없음"
                자리 = None if 종류 == "퍼센트정수" else 소수자리기준
                퍼센트 = round(임시퍼센트) if 자리 is None else round(임시퍼센트, 자리)
                절대값 = round(임시절대값) if 자리 is None else round(임시절대값, 자리)
                return 앞 + "%→" + 뒤 + "%로 " + str(퍼센트) + "% " + 임시증감 + "(" + str(절대값) + "%p" + 임시증감기호 + ")"
            if 종류 in ("단위정수", "단위소수"):
                앞뒤 = 앞 + 단위 + "→" + 뒤 + 단위 + 로으로(단위)
                if 앞값 == 뒤값:
                    return 앞뒤 + " 변화없음"
                자리 = None if 종류 == "단위정수" else 소수자리기준
                퍼센트 = round(임시퍼센트) if 자리 is None else round(임시퍼센트, 자리)
                절대값 = round(임시절대값) if 자리 is None else round(임시절대값, 자리)
                return 앞뒤 + " " + str(퍼센트) + "% " + 임시증감 + "(" + str(절대값) + 단위 + 임시증감기호 + ")"
            return 결과값
        except ValueError:
            return 데이터초기값

    def 날짜변환(self, 데이터, 종류):
        결과값 = ""
        데이터초기값 = 데이터
        데이터 = 데이터.replace(" ", "").replace("(월)", "").replace("월요일", "")
        데이터 = 데이터.replace("일", "").replace("년", "-").replace("월", "-")
        데이터 = re.sub(r"[가-힣]", "", 데이터).replace("(", "").replace(")", "")
        for 기호 in ("'", "`", "ʹ", "’", "‘"):
            데이터 = 데이터.replace(기호, "20")
        if re.match(r"^\d{8}$", 데이터):
            데이터 = f"{데이터[:4]}-{데이터[4:6]}-{데이터[6:]}"
        if re.match(r"^\d{6}$", 데이터):
            년 = int(데이터[:2])
            데이터 = ("19" if 년 > datetime.today().year % 100 else "20") + 데이터
            데이터 = f"{데이터[:4]}-{데이터[4:6]}-{데이터[6:]}"
        if re.match(r"^\d{4}$", 데이터):
            데이터 = f"{str(datetime.today().year)[:2]}{데이터[:2]}-{데이터[2:4]}-01"
        데이터 = re.sub(r"[./-]", "-", 데이터.rstrip("."))
        if len(데이터) < 8:
            데이터 = 데이터.rstrip("-")
            if re.fullmatch(r"\d{4}-\d{1,2}", 데이터):
                데이터 += "-01"
            elif re.fullmatch(r"\d{1,2}-\d{1,2}", 데이터):
                if int(데이터.split("-")[0]) <= 12:
                    if "년" in 데이터초기값:
                        데이터 = str(datetime.today().year)[:2] + 데이터 + "-01"
                    else:
                        데이터 = str(datetime.today().year) + "-" + 데이터
                else:
                    데이터 = str(datetime.today().year)[:2] + 데이터 + "-01"
        임시요일 = ["월", "화", "수", "목", "금", "토", "일"]
        try:
            날짜 = datetime.strptime(데이터, "%Y-%m-%d")
            if 종류 == "점": 결과값 = 날짜.strftime("%Y.%m.%d.")
            if 종류 == "점띄": 결과값 = 날짜.strftime("%Y.%m.%d.").replace(".", ". ").strip()
            if 종류 == "바": 결과값 = 날짜.strftime("%Y-%m-%d")
            if 종류 == "슬래시": 결과값 = 날짜.strftime("%Y/%m/%d")
            if 종류 == "바요일": 결과값 = 날짜.strftime("%Y-%m-%d") + "(" + 임시요일[날짜.weekday()] + ")"
            if 종류 == "점띄요일": 결과값 = f"{날짜.year}. {날짜.month}. {날짜.day}.({임시요일[날짜.weekday()]})"
            if 종류 == "한글": 결과값 = f"{날짜.year}년 {날짜.month}월 {날짜.day}일 {임시요일[날짜.weekday()]}요일"
            if 종류 == "없점": 결과값 = f"{날짜.year}.{날짜.month}.{날짜.day}."
            if 종류 == "없점띄": 결과값 = f"{날짜.year}. {날짜.month}. {날짜.day}."
            if 종류 == "없바": 결과값 = f"{날짜.year}-{날짜.month}-{날짜.day}"
            if 종류 == "없슬래시": 결과값 = f"{날짜.year}/{날짜.month}/{날짜.day}"
            if 종류 == "없바요일": 결과값 = f"{날짜.year}-{날짜.month}-{날짜.day}({임시요일[날짜.weekday()]})"
            if 종류 == "축약년월": 결과값 = f"'{str(날짜.year)[2:4]}. {날짜.month}."
            return 결과값
        except ValueError:
            return 데이터초기값

    def 한글화(self, 숫자):
        숫자문자열 = str(숫자)
        리턴값 = ""
        문자열길이 = len(숫자문자열)
        한글수 = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구", "십"]
        한글단 = ["", "십", "백", "천"] * 4
        for i in range(0, 문자열길이):
            중간값 = 한글수[int(숫자문자열[문자열길이 - 1 - i])]
            if 중간값 != "":
                중간값 += 한글단[i]
            if i == 4:
                중간값 += "만"
            if i == 8:
                중간값 += "억"
            if i == 12:
                중간값 += "조"
            리턴값 = 중간값 + 리턴값
        if 숫자 % 100000000 == 0:
            리턴값 = 리턴값.replace("만", "")
        if 숫자 % 1000000000000 == 0:
            리턴값 = 리턴값.replace("억", "")
        return 리턴값
    def 문장쌈(self, 앞, 뒤):
        블록스캔 = self.블록스캔()
        텍스트 = 블록스캔[1]
        if "\r" not in 텍스트:
            try:
                self.문장(앞 + 텍스트 + 뒤)
            except ValueError as e:
                print(f"값 오류 : {e}")
            except Exception as e:
                print(f"오류 발생 : {e}")

    def JSON에서변환(self):
        원문 = self.블록텍스트()
        if not str(원문 or "").strip():
            # 빈 문서에서 변환 버튼을 눌렀을 때 JSONDecodeError가
            # 자동화 프로세스까지 전파되지 않도록 조용히 종료한다.
            return False
        try:
            블록내용 = json.loads(원문)
        except (TypeError, ValueError):
            return False
        접두사 = {1: "네모:", 2: "원:", 3: "바:", 4: "점:"}
        보관함 = []

        def 변환기(블록내용, 레벨=1):
            접두 = 접두사.get(레벨, "")
            if isinstance(블록내용, dict):
                for key, value in 블록내용.items():
                    if isinstance(value, (dict, list)):
                        보관함.append(f"{접두}{key}")
                        변환기(value, 레벨 + 1)
                    else:
                        보관함.append(f"{접두}{key}:{value}")
            elif isinstance(블록내용, list):
                for item in 블록내용:
                    if isinstance(item, (dict, list)):
                        변환기(item, 레벨)
                    else:
                        보관함.append(f"{접두}{item}")

        변환기(블록내용)
        출력내용 = "\r\n".join(보관함)
        출력내용 = 출력내용.replace("네모:제목", "제목")
        self.문장(출력내용)
        # 원본 구현은 성공 경로에서 명시적으로 값을 반환하지 않는다(None).
        # 호출자가 반환값을 검사하는 경우에도 원본과 동일한 동작을 유지한다.
        return None


__all__ = ["HwpTextFeatureMixin"]
