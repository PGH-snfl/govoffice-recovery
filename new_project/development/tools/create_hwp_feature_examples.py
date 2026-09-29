# -*- coding: utf-8 -*-
"""범정부오피스 한글 기능 확인용 쌍둥이 예시 문서를 만든다."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--recovered-root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--first-file", type=Path)
    parser.add_argument("--second-file", type=Path)
    return parser.parse_args()


ARGS = parse_args()
PROJECT_ROOT = Path(__file__).resolve().parents[3]
RECOVERED_ROOT = (ARGS.recovered_root or PROJECT_ROOT / "recovered").resolve()
OUTPUT_DIR = (ARGS.output_dir or PROJECT_ROOT / "new_project" / "development" / "examples" / "hwp").resolve()
sys.path.insert(0, str(RECOVERED_ROOT))

from win32com.client import DispatchEx
from 한컴오피스.한컴라이브러리 import 기본한컴


PURPLE = (91, 59, 143)
LIGHT_PURPLE = (237, 231, 247)
LIGHT_GRAY = (245, 245, 245)


def open_hwp(target_path):
    print("  CREATE_WRAPPER", flush=True)
    app = 기본한컴()
    print("  CONNECT_HWP", flush=True)
    app.대상 = DispatchEx("HWPFrame.HwpObject")
    print("  REGISTER_SECURITY", flush=True)
    app._보안모듈등록()
    print("  HIDE_WINDOW", flush=True)
    app.대상.XHwpWindows.Item(0).Visible = False
    print("  OPEN_FILE", flush=True)
    opened = app.대상.Open(str(target_path), "HWP", "forceopen:true")
    print(f"  OPEN_RESULT {opened!r}", flush=True)
    if opened is False:
        raise RuntimeError(f"한글 파일 열기 실패: {target_path}")
    app.대상.MovePos(2, 0, 0)
    app.대상.HAction.Run("SelectAll")
    app.대상.HAction.Run("Delete")
    app.문서여백(20, 20, 18, 18, 10, 10)
    return app


def reset_text(app, size=10.5):
    app.대상.HAction.Run("CharShapeNormal")
    app.폰트("맑은 고딕")
    app.글자크기(size)
    app.글자색(0, 0, 0)
    app.기본정렬()
    app.줄간격(160)


def line_break(app, count=1):
    for _ in range(count):
        app.대상.HAction.Run("BreakPara")


def title(app, text, subtitle):
    app.가운데정렬()
    app.폰트("맑은 고딕")
    app.글자크기(22)
    app.글자색(*PURPLE)
    app.진하게()
    app.문장(text)
    line_break(app)
    reset_text(app, 10)
    app.가운데정렬()
    app.문장(subtitle)
    line_break(app, 2)
    reset_text(app)


def section(app, number, text):
    app.폰트("맑은 고딕")
    app.글자크기(14)
    app.글자색(*PURPLE)
    app.진하게()
    app.문장(f"{number}. {text}")
    line_break(app)
    reset_text(app)


def paragraph(app, text):
    app.문장(text)
    line_break(app)


def bullets(app, values):
    for value in values:
        app.문장(f"  • {value}")
        line_break(app)


def cell_style(app, row, col, numeric_columns):
    reset_text(app, 9.5)
    if row == 0:
        app.표배경색(*LIGHT_PURPLE)
        app.진하게()
        app.가운데정렬()
    elif col == 0:
        app.표배경색(*LIGHT_GRAY)
        app.가운데정렬()
    elif col in numeric_columns:
        app.오른쪽정렬()
    else:
        app.기본정렬()


def table(app, rows, widths, numeric_columns=()):
    heights = [8] * len(rows)
    app.표만들기(widths, heights)
    last = len(rows) * len(widths) - 1
    index = 0
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            cell_style(app, row_index, col_index, set(numeric_columns))
            app.문장(str(value))
            if index != last:
                app.표오른쪽(1)
            index += 1
    app.표탈출()
    line_break(app)
    reset_text(app)


def page_break(app):
    app.대상.HAction.Run("BreakPage")
    reset_text(app)


def build_document(data, output_path):
    print(f"START {output_path.name}", flush=True)
    app = open_hwp(output_path)
    print("  HWP_READY", flush=True)
    title(app, data["title"], "범정부오피스 통합 기능 확인용 예시 문서")
    print("  TITLE", flush=True)

    section(app, 1, "문서 기본정보 및 개인정보 치환")
    table(
        app,
        [
            ["항목", "입력된 예시값", "확인할 기능"],
            ["기관명", data["institution"], "기관 정보 자동 입력"],
            ["작성자", data["name"], "개인정보 치환"],
            ["전화번호", data["phone"], "텍스트만 붙여넣기"],
            ["전자우편", data["email"], "개인정보 치환"],
            ["작성일", data["date"], "날짜 자동 입력"],
        ],
        [30, 75, 65],
    )
    print("  SECTION_1", flush=True)

    section(app, 2, "글자·문단 기본 기능")
    paragraph(app, data["intro"])
    bullets(app, data["bullets"])
    paragraph(app, "[선택영역] 이 문장은 글꼴, 크기, 자간, 장평, 줄 간격과 정렬 기능을 시험하는 영역입니다.")
    line_break(app)
    print("  SECTION_2", flush=True)

    section(app, 3, "제목·목차·보기변환 확인")
    paragraph(app, "Ⅰ. 사업 개요")
    paragraph(app, "Ⅱ. 추진 계획")
    paragraph(app, "Ⅲ. 행정 사항")
    paragraph(app, "보기 ① 첫 번째 선택지  ② 두 번째 선택지  ③ 세 번째 선택지  ④ 네 번째 선택지")
    paragraph(app, "영문 보기 (A) Alpha  (B) Beta  (C) Gamma  (D) Delta")
    print("  SECTION_3", flush=True)

    section(app, 4, "표 서식·정렬·스타일 제거 확인")
    table(
        app,
        [
            ["순번", "세부 과제", "담당 부서", "예산(천원)", "진행률"],
            ["3", data["tasks"][0], data["departments"][0], data["budgets"][0], "40%"],
            ["1", data["tasks"][1], data["departments"][1], data["budgets"][1], "80%"],
            ["2", data["tasks"][2], data["departments"][2], data["budgets"][2], "60%"],
        ],
        [18, 62, 38, 28, 24],
        numeric_columns=(0, 3, 4),
    )
    paragraph(app, "※ 위 표는 차순정렬, 숫자 정리, 표 스타일 제거와 프리셋 적용 시험에 사용합니다.")
    print("  SECTION_4", flush=True)

    page_break(app)
    section(app, 5, "시간계획·일정표 확인")
    table(
        app,
        [
            ["시작", "종료", "소요", "내용", "담당"],
            ["09:00", "09:10", "10분", data["schedule"][0], data["name"]],
            ["09:10", "09:40", "30분", data["schedule"][1], data["departments"][0]],
            ["09:40", "10:00", "20분", data["schedule"][2], data["departments"][1]],
        ],
        [24, 24, 22, 70, 32],
        numeric_columns=(0, 1, 2),
    )
    print("  SECTION_5", flush=True)

    section(app, 6, "점수분배 시험")
    paragraph(app, "아래 배점 표시와 점수표의 개수는 동일하게 구성했습니다.")
    paragraph(app, "문항 1  [0점]")
    paragraph(app, "문항 2  [0점]")
    paragraph(app, "문항 3  [0점]")
    paragraph(app, "점수표 전체를 선택한 뒤 ‘학교시험문제 학시문 → 분배’를 실행합니다.")
    table(
        app,
        [["문항 1", "문항 2", "문항 3"], data["scores"]],
        [55, 55, 55],
        numeric_columns=(0, 1, 2),
    )
    print("  SECTION_6", flush=True)

    section(app, 7, "서식 복사·프리셋 저장 선택영역")
    paragraph(app, "아래 표 전체를 선택하여 서식 프리셋으로 저장하는 시험에 사용합니다.")
    table(
        app,
        [
            ["구분", "계획", "실적", "비고"],
            ["상반기", data["preset"][0], data["preset"][1], "가운데 정렬"],
            ["하반기", data["preset"][2], data["preset"][3], "오른쪽 값 정렬"],
            ["합계", data["preset"][4], data["preset"][5], "서식 유지"],
        ],
        [35, 45, 45, 40],
        numeric_columns=(1, 2),
    )
    print("  SECTION_7", flush=True)

    section(app, 8, "빈칸 유지 및 내용만 교체")
    table(
        app,
        [
            ["항목", "기존 내용", "교체 후 확인"],
            ["제목", data["keep_title"], "제목은 유지"],
            ["이름", data["name"], "사용자 정보로 교체"],
            ["전화번호", data["phone"], "사용자 정보로 교체"],
            ["빈칸", "", "원래 빈칸은 그대로 유지"],
        ],
        [35, 70, 60],
    )
    print("  SECTION_8", flush=True)

    paragraph(app, "문서 끝 — 두 예시 파일은 서식과 구조가 같고 입력 내용만 다릅니다.")
    app.대상.HAction.Run("FileSave")
    app.대상.HAction.Run("FileClose")
    app.대상.Quit()
    print(f"SAVED {output_path.name}", flush=True)
    return output_path


def main():
    first = {
        "title": "서울과학기술대학교 업무혁신 추진계획",
        "institution": "서울과학기술대학교",
        "name": "홍길동",
        "phone": "010-1234-1234",
        "email": "honggildong@seoultech.ac.kr",
        "date": "2026. 9. 4.",
        "intro": "업무 처리 절차를 표준화하고 반복 서식을 자동화하여 문서 작성 시간을 단축하고자 합니다.",
        "bullets": ["기관별 기능 라이브러리 구성", "사용자 개인정보 자동 입력", "선택영역 서식 프리셋 저장"],
        "tasks": ["기관 기능 등록", "한글 프리셋 적용", "개인정보 자동 입력"],
        "departments": ["정보전산원", "총무과", "기획처"],
        "budgets": ["12,000", "8,500", "5,000"],
        "schedule": ["개회 및 안내", "기능 시연", "질의응답"],
        "scores": ["10", "20", "30"],
        "preset": ["120", "108", "150", "143", "270", "251"],
        "keep_title": "업무혁신 추진계획",
    }
    second = {
        "title": "한빛연구원 문서자동화 운영계획",
        "institution": "한빛연구원",
        "name": "김하늘",
        "phone": "010-5678-9876",
        "email": "haneul.kim@example.org",
        "date": "2026. 10. 15.",
        "intro": "연구행정 문서의 형식은 그대로 유지하면서 기관명과 담당자 및 사업 내용만 교체하고자 합니다.",
        "bullets": ["연구보고서 서식 표준화", "담당자 정보 자동 치환", "기관 전용 표 양식 적용"],
        "tasks": ["연구과제 목록 정리", "회의자료 서식 적용", "담당자 연락처 치환"],
        "departments": ["연구지원실", "경영관리실", "성과확산실"],
        "budgets": ["9,800", "7,200", "4,500"],
        "schedule": ["참석자 소개", "운영계획 보고", "검토의견 정리"],
        "scores": ["15", "25", "20"],
        "preset": ["95", "91", "130", "126", "225", "217"],
        "keep_title": "문서자동화 운영계획",
    }
    first_file = (ARGS.first_file or OUTPUT_DIR / "01_통합기능확인_서울과기대.hwp").resolve()
    second_file = (ARGS.second_file or OUTPUT_DIR / "02_통합기능확인_내용변경본.hwp").resolve()
    for target in (first_file, second_file):
        if not target.exists():
            raise FileNotFoundError(f"수정할 한글 파일이 없습니다: {target}")
    files = [build_document(first, first_file), build_document(second, second_file)]
    for file in files:
        print(file)


if __name__ == "__main__":
    main()
