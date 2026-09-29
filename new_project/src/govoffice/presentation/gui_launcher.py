from __future__ import annotations

import json
from pathlib import Path

from ..app.function_catalog import 검증완료기능목록, 필수인자목록
from ..adapters.recovered_hwp import 복구한글어댑터
from ..runtime.tk_loader import tkinter불러오기


탭목록 = ("표", "표세부", "블록", "이동", "편리", "글자", "문자", "중앙", "지자체", "사용", "교직", "공기업", "기본서식", "국방", "가이드")


def _탭분류(이름: str, 모듈: str) -> str:
    if any(word in 이름 for word in ("서울", "세종", "충남", "광주", "경기", "경남", "제주", "인천", "용인", "부여", "부안", "구례", "남해", "남양주", "의정부", "영덕", "홍성", "합천", "금천")):
        return "지자체"
    if "국방" in 이름 or "군" in 이름:
        return "국방"
    if any(word in 이름 for word in ("교직", "학교", "시험")):
        return "교직"
    if any(word in 이름 for word in ("공기업", "공사", "출연")):
        return "공기업"
    if "기본서식" in 이름:
        return "기본서식"
    if any(word in 이름 for word in ("가이드", "역학", "감염", "차량")):
        return "가이드"
    if any(word in 이름 for word in ("블록", "누름", "필드")):
        return "블록"
    if any(word in 이름 for word in ("표", "셀", "행", "열")):
        return "표세부" if any(word in 이름 for word in ("테두리", "여백", "너비", "높이", "배경")) else "표"
    if any(word in 이름 for word in ("이동", "찾기", "페이지", "쪽", "처음", "끝")):
        return "이동"
    if any(word in 이름 for word in ("글자", "폰트", "자간", "장평", "진하게", "밑줄")):
        return "글자"
    if any(word in 이름 for word in ("문자", "문장", "문단", "텍스트")):
        return "문자"
    if any(word in 이름 for word in ("정렬", "가운데", "중앙")):
        return "중앙"
    if any(word in 이름 for word in ("날짜", "공문", "메일", "메모", "AI", "서식")):
        return "편리"
    return "사용"


class 범정부오피스GUI:
    def __init__(self) -> None:
        self.tk = tkinter불러오기()
        self.창 = self.tk.Tk()
        self.창.title("범정부오피스")
        self.창.geometry("300x680+0+0")
        self.창.resizable(False, False)
        self.창.attributes("-topmost", False)
        self.한글: 복구한글어댑터 | None = None
        self.전체기능 = 검증완료기능목록()
        self.현재탭 = "사용"
        self._화면생성()
        self._목록갱신()

    def _버튼(self, master, text, command, **kwargs):
        return self.tk.Button(master, text=text, command=command, relief="flat", bg="#f4f6f8", activebackground="#dce8f5", font=("맑은 고딕", 9), **kwargs)

    def _화면생성(self) -> None:
        상단 = self.tk.Frame(self.창, bg="#ffffff", height=50)
        상단.pack(fill="x")
        actions = (("열기", lambda: self._기능("불러오기")), ("재연결", self._연결), ("새 문서", lambda: self._기능("새창")), ("최소화", self.창.iconify), ("종료", self.창.destroy))
        for label, command in actions:
            self._버튼(상단, label, command, width=7, height=2).pack(side="left", fill="x", expand=True)

        검색 = self.tk.Frame(self.창, bg="#ffffff", height=50)
        검색.pack(fill="x", padx=5, pady=4)
        self.검색어 = self.tk.StringVar()
        entry = self.tk.Entry(검색, textvariable=self.검색어, font=("맑은 고딕", 10))
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<KeyRelease>", lambda _event: self._목록갱신())
        self._버튼(검색, "실행", self._선택실행, width=6).pack(side="right", padx=(4, 0))

        self.목록 = self.tk.Listbox(self.창, font=("맑은 고딕", 10), relief="flat", selectbackground="#2878c8", activestyle="none")
        self.목록.pack(fill="both", expand=True, padx=5)
        self.목록.bind("<Double-Button-1>", lambda _event: self._선택실행())

        인자줄 = self.tk.Frame(self.창, bg="#ffffff")
        인자줄.pack(fill="x", padx=5, pady=4)
        self.tk.Label(인자줄, text="인자", bg="#ffffff").pack(side="left")
        self.인자 = self.tk.Entry(인자줄, font=("맑은 고딕", 9))
        self.인자.insert(0, "[]")
        self.인자.pack(side="left", fill="x", expand=True, padx=(5, 0))

        네비 = self.tk.Frame(self.창, bg="#ffffff")
        네비.pack(fill="x")
        for index, name in enumerate(탭목록):
            button = self._버튼(네비, name, lambda value=name: self._탭변경(value), width=7, height=1)
            button.grid(row=index // 5, column=index % 5, sticky="nsew", padx=1, pady=1)
            네비.grid_columnconfigure(index % 5, weight=1)

        self.상태 = self.tk.StringVar(value=f"검증 완료 {len(self.전체기능):,}개 · 한글 연결 대기")
        self.tk.Label(self.창, textvariable=self.상태, anchor="w", bg="#e9eef3", font=("맑은 고딕", 8)).pack(fill="x")

    def _탭변경(self, name: str) -> None:
        self.현재탭 = name
        self._목록갱신()

    def _목록갱신(self) -> None:
        query = self.검색어.get().strip().casefold()
        self.표시기능 = [item for item in self.전체기능 if _탭분류(item.이름, item.모듈) == self.현재탭 and (not query or query in item.이름.casefold())]
        self.목록.delete(0, self.tk.END)
        for item in self.표시기능:
            self.목록.insert(self.tk.END, item.이름)
        self.상태.set(f"{self.현재탭} · {len(self.표시기능):,}개")

    def _연결(self) -> None:
        try:
            if self.한글 is None:
                self.한글 = 복구한글어댑터()
            self.한글.기능실행("한컴열기")
            if self.한글.원본.대상 is None:
                raise RuntimeError("한글 COM 객체를 가져오지 못했습니다.")
            self.상태.set("한글 연결 완료")
        except Exception as error:
            self._오류(str(error))

    def _기능(self, name: str, args: list | None = None) -> None:
        try:
            if self.한글 is None:
                self._연결()
            if self.한글 is None or self.한글.원본.대상 is None:
                return
            self.한글.기능실행(name, *(args or []))
            self.상태.set(f"실행 완료: {name}")
        except Exception as error:
            self._오류(f"{name}: {error}")

    def _선택실행(self) -> None:
        selected = self.목록.curselection()
        if not selected:
            return
        item = self.표시기능[selected[0]]
        try:
            args = json.loads(self.인자.get() or "[]")
            if not isinstance(args, list):
                raise ValueError("인자는 JSON 배열이어야 합니다.")
            if self.한글 is None:
                self._연결()
            if self.한글 is None or self.한글.원본.대상 is None:
                return
            required = 필수인자목록(self.한글.원본, item.이름)
            if len(args) < len(required):
                raise ValueError(f"필수 인자: {', '.join(required)}")
            self._기능(item.이름, args)
        except Exception as error:
            self._오류(str(error))

    def _오류(self, message: str) -> None:
        self.상태.set(f"오류: {message}")
        dialog = self.tk.Toplevel(self.창)
        dialog.title("범정부오피스 오류")
        dialog.geometry("360x140+320+100")
        dialog.attributes("-topmost", False)
        self.tk.Label(dialog, text=message, wraplength=330, justify="left").pack(fill="both", expand=True, padx=15, pady=10)
        self._버튼(dialog, "확인", dialog.destroy, width=10).pack(pady=(0, 10))

    def 실행(self) -> None:
        self.창.mainloop()


def GUI실행() -> None:
    범정부오피스GUI().실행()
