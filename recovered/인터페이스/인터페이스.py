"""범피스 공통 Tkinter 위젯 복구본.

원본 Python 3.13 바이트코드의 디스어셈블을 기준으로 공개 클래스명과
생성자 시그니처를 보존했다.
"""

import os
import sys
import tkinter as tk


설명창변수 = None


def 이미지(파일이름):
    기본경로 = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(기본경로, 파일이름)


class 배경(tk.Label):
    def __init__(self, master, x좌표, y좌표, 이미지경로):
        super().__init__(master)
        self.아이콘 = tk.PhotoImage(file=이미지(이미지경로))
        self["image"] = self.아이콘
        self.place(x=x좌표, y=y좌표)
        self.configure(relief="flat", borderwidth=0, highlightthickness=0, bg="#ffffff")


class 버튼(tk.Button):
    def __init__(self, master, x좌표, y좌표, 이미지경로, 함수):
        super().__init__(master)
        self.configure(
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            bg="#ffffff",
            activebackground="#ffffff",
        )
        self.아이콘 = tk.PhotoImage(file=이미지(이미지경로))
        self["image"] = self.아이콘
        self["command"] = 함수
        self.place(x=x좌표, y=y좌표)


class 버튼더블클릭(tk.Button):
    마지막버튼 = None

    def __init__(self, master, x좌표, y좌표, 이미지경로, 함수1, 함수2, 실행여부):
        super().__init__(master)
        self.함수1 = 함수1
        self.함수2 = 함수2
        self.실행여부 = 실행여부
        self.아이콘 = tk.PhotoImage(file=이미지(이미지경로))
        self.configure(
            image=self.아이콘,
            command=self.클릭처리,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            bg="#ffffff",
            activebackground="#ffffff",
        )
        self.place(x=x좌표, y=y좌표)

    def 클릭처리(self):
        if 버튼더블클릭.마지막버튼 is self and self.실행여부:
            self.함수2()
            버튼더블클릭.마지막버튼 = None
        else:
            self.함수1()
            버튼더블클릭.마지막버튼 = self


class 토글버튼(tk.Button):
    def __init__(self, master, x좌표, y좌표, 이미지경로, 이미지경로2):
        super().__init__(master)
        self.아이콘 = tk.PhotoImage(file=이미지(이미지경로))
        self.아이콘2 = tk.PhotoImage(file=이미지(이미지경로2))
        self.토글상태 = False
        self.configure(
            image=self.아이콘,
            command=self.토글,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            bg="#ffffff",
            activebackground="#ffffff",
        )
        self.place(x=x좌표, y=y좌표)

    def 토글(self):
        self.토글상태 = not self.토글상태
        self.configure(image=self.아이콘2 if self.토글상태 else self.아이콘)


class 입력창(tk.Entry):
    def __init__(self, master, x좌표, y좌표):
        super().__init__(master, font="맑은고딕 13 bold", width=15)
        self.place(x=x좌표, y=y좌표)


class 입력창넓이(tk.Entry):
    def __init__(self, master, x좌표, y좌표, 넓이):
        super().__init__(master, font="맑은고딕 13 bold", width=넓이)
        self.place(x=x좌표, y=y좌표)


class 입력창넓이높이(tk.Text):
    def __init__(self, master, x좌표, y좌표, 넓이, 높이):
        super().__init__(master, font="맑은고딕 13 bold", width=넓이, height=높이)
        self.place(x=x좌표, y=y좌표)


class 입력창넓이크기(tk.Entry):
    def __init__(self, master, x좌표, y좌표, 넓이, 크기):
        super().__init__(master, font=("맑은고딕", 크기, "bold"), width=넓이)
        self.place(x=x좌표, y=y좌표)


class 프레임(tk.Frame):
    def __init__(self, master, x좌표, y좌표, 가로, 세로):
        super().__init__(master, width=가로, height=세로, bg="#ffffff")
        self.place(x=x좌표, y=y좌표)


class 프레임색(tk.Frame):
    def __init__(self, master, x좌표, y좌표, 가로, 세로, 배경색):
        super().__init__(master, width=가로, height=세로, bg=배경색)
        self.place(x=x좌표, y=y좌표)


class 상단바(tk.Frame):
    def __init__(self, master, x좌표, y좌표, 가로, 세로, 배경):
        super().__init__(master, width=가로, height=세로, bg=배경)
        self.place(x=x좌표, y=y좌표)
        self.bind("<ButtonPress-1>", self._이동시작)
        self.bind("<B1-Motion>", self._이동)

    def _이동시작(self, event):
        self._시작_x = event.x
        self._시작_y = event.y

    def _이동(self, event):
        창 = self.winfo_toplevel()
        x = 창.winfo_x() + event.x - self._시작_x
        y = 창.winfo_y() + event.y - self._시작_y
        창.geometry(f"+{x}+{y}")


class 새탭(tk.Toplevel):
    def __init__(self, master, x좌표, y좌표, 가로, 세로):
        super().__init__(master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 2)
        self.configure(bg="#ffffff")
        self.geometry(f"{가로}x{세로}+{x좌표}+{y좌표}")
        버튼(self, 가로 - 50, 0, r"아이콘\상단바\닫기.PNG", self.destroy)
        상단바(self, 0, 0, 가로 - 50, 50, "#ffffff")


class 우측새탭(tk.Toplevel):
    def __init__(self, master, x좌표, y좌표, 가로, 세로):
        super().__init__(master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 2)
        self.configure(bg="#ffffff")
        self.geometry(f"{가로}x{세로}-{x좌표}+{y좌표}")
        버튼(self, 가로 - 50, 0, r"아이콘\상단바\닫기.PNG", self.destroy)
        상단바(self, 0, 0, 가로 - 50, 50, "#ffffff")


class 설명창(tk.Toplevel):
    def __init__(self, master, 내용=""):
        super().__init__(master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 2)
        self.configure(bg="#ffffff")
        self.geometry("300x400-400+50")
        버튼(self, 250, 0, r"아이콘\상단바\닫기.PNG", self._닫기)
        상단바(self, 0, 0, 250, 50, "#ffffff")
        self.설명 = tk.Text(self, font="맑은고딕 13 bold", width=30, height=17)
        self.설명.place(x=10, y=60)
        self.내용갱신(내용)

    def _닫기(self):
        global 설명창변수
        설명창변수 = None
        self.destroy()

    def 내용갱신(self, 새내용):
        self.설명.delete("1.0", tk.END)
        self.설명.insert("1.0", str(새내용))


class 설명버튼(버튼):
    def __init__(self, master, x좌표, y좌표, 이미지경로, 함수, 설명=""):
        super().__init__(master, x좌표, y좌표, 이미지경로, 함수)
        self.설명내용 = 설명
        self.bind("<Button-3>", self._설명창확인)

    def _설명창확인(self, _event=None):
        global 설명창변수
        if 설명창변수 is not None:
            설명창변수.내용갱신(self.설명내용)
        else:
            설명창변수 = 설명창(self.master, self.설명내용)


# 원본의 ``from tkinter import *`` 사용 방식과 호환되는 이름들.
Tk = tk.Tk
END = tk.END

