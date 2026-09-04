"""manifest 기반 동적 기관탭.

Tkinter는 GUI 생성 시점에만 가져오므로 분석·시험 환경에서는 기관 모델과
실행 로더를 GUI 없이 검증할 수 있다.
"""

from __future__ import annotations

from institution_system import 기관기능실행, 기관탭목록, 즐겨찾기실행


def 기관탭생성(master, 등록부, 한컴, 즐겨찾기저장소=None, 오류처리=None):
    import tkinter as tk
    from tkinter import ttk

    노트북 = ttk.Notebook(master)
    즐겨찾기프레임들 = []

    def 오류알림(기능, 오류):
        if 오류처리 is not None:
            오류처리(기능, 오류)
            return None
        raise 오류

    def 즐겨찾기새로고침():
        if 즐겨찾기저장소 is None:
            return
        항목들 = 즐겨찾기저장소.전체()
        for 즐겨찾기프레임 in 즐겨찾기프레임들:
            for 위젯 in 즐겨찾기프레임.winfo_children():
                위젯.destroy()
            if not 항목들:
                ttk.Label(
                    즐겨찾기프레임,
                    text="자주 쓰는 기본 기능이나 기관 기능을 이 영역으로 끌어오세요.",
                ).grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="w")
                continue
            for 순서, 항목 in enumerate(항목들):
                행, 열 = divmod(순서, 4)

                def 실행(선택항목=항목):
                    try:
                        return 즐겨찾기실행(선택항목, 한컴)
                    except Exception as e:
                        return 오류알림(선택항목, e)

                버튼 = ttk.Button(즐겨찾기프레임, text=항목.name, command=실행)
                버튼._favorite_id = 항목.id
                버튼._favorite_index = 순서
                버튼.bind("<ButtonPress-1>", lambda _e, 항목id=항목.id: setattr(노트북, "_drag_favorite", 항목id))

                def 순서이동(event, 목표=순서):
                    항목id = getattr(노트북, "_drag_favorite", None)
                    if 항목id and 즐겨찾기저장소.이동(항목id, 목표):
                        즐겨찾기새로고침()
                    노트북._drag_favorite = None

                버튼.bind("<ButtonRelease-1>", 순서이동, add="+")
                버튼.grid(row=행, column=열, padx=4, pady=4, sticky="ew")
            for 열 in range(4):
                즐겨찾기프레임.columnconfigure(열, weight=1)

    for 기관 in 기관탭목록(등록부):
        프레임 = ttk.Frame(노트북)
        노트북.add(프레임, text=기관.name)

        즐겨찾기영역 = ttk.LabelFrame(프레임, text="즐겨찾기 · 한글 기본 기능")
        즐겨찾기영역.pack(fill=tk.X, padx=8, pady=(8, 4))
        즐겨찾기프레임들.append(즐겨찾기영역)

        기관영역 = ttk.LabelFrame(프레임, text=f"{기관.name} 자체 기능")
        기관영역.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))

        if not 기관.functions:
            ttk.Label(기관영역, text="등록된 기관 전용 기능이 없습니다.").grid(
                row=0, column=0, padx=12, pady=12, sticky="w"
            )
            continue

        for 순서, 기능 in enumerate(기관.functions):
            행, 열 = divmod(순서, 4)

            def 실행(기관id=기관.id, 선택기능=기능):
                try:
                    return 기관기능실행(기관id, 선택기능, 한컴)
                except Exception as e:
                    if 오류처리 is not None:
                        오류처리(선택기능, e)
                        return None
                    raise

            버튼 = ttk.Button(기관영역, text=기능.name, command=실행)
            if not 기능.ui_ready:
                버튼.state(["disabled"])
            elif 즐겨찾기저장소 is not None:
                버튼.bind(
                    "<ButtonPress-1>",
                    lambda _e, 기관id=기관.id, 선택기능=기능: setattr(
                        노트북, "_drag_institution", (기관id, 선택기능)
                    ),
                )

                def 즐겨찾기에놓기(event, 목표영역=즐겨찾기영역):
                    드래그 = getattr(노트북, "_drag_institution", None)
                    노트북._drag_institution = None
                    if not 드래그:
                        return
                    대상 = event.widget.winfo_containing(event.x_root, event.y_root)
                    if 대상 is None:
                        return
                    부모 = 대상
                    while 부모 is not None and 부모 is not 목표영역:
                        부모이름 = 부모.winfo_parent()
                        부모 = 부모._nametowidget(부모이름) if 부모이름 else None
                    if 부모 is 목표영역:
                        기관id, 선택기능 = 드래그
                        if 즐겨찾기저장소.기관기능추가(기관id, 선택기능):
                            즐겨찾기새로고침()

                버튼.bind("<ButtonRelease-1>", 즐겨찾기에놓기, add="+")
            버튼.grid(
                row=행,
                column=열,
                padx=4,
                pady=4,
                sticky="ew",
            )
        for 열 in range(4):
            기관영역.columnconfigure(열, weight=1)

    즐겨찾기새로고침()
    노트북.pack(fill=tk.BOTH, expand=True)
    return 노트북
