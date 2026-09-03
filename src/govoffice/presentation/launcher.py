from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import dataclass
from typing import TextIO

from ..adapters.recovered_hwp import 복구한글어댑터
from ..app.function_catalog import 실행기능, 검증완료기능목록, 필수인자목록


@dataclass(slots=True)
class 런처상태:
    한글: 복구한글어댑터 | None = None


class 기능런처:
    """번들 Python만으로 실행되는 단일 연결 콘솔 런처."""

    def __init__(self, 출력: TextIO | None = None) -> None:
        import sys
        self.출력 = 출력 or sys.stdout
        self.상태 = 런처상태()
        self.기능 = 검증완료기능목록()
        self._이름별 = {item.이름: item for item in self.기능}

    def 쓰기(self, 내용: str = "") -> None:
        print(내용, file=self.출력)

    def 검색(self, 검색어: str = "") -> tuple[실행기능, ...]:
        query = 검색어.strip().casefold()
        if not query:
            return self.기능
        return tuple(item for item in self.기능 if query in f"{item.모듈} {item.클래스} {item.이름} {item.분류}".casefold())

    def 목록출력(self, 검색어: str = "", 제한: int = 50) -> None:
        matches = self.검색(검색어)
        for index, item in enumerate(matches[:제한], 1):
            self.쓰기(f"{index:4}. {item.이름}  [{item.모듈}/{item.클래스}] {item.분류} · {item.검증상태}")
        self.쓰기(f"표시 {min(len(matches), 제한):,} / 검색 결과 {len(matches):,}개")

    def 한글연결(self) -> None:
        if self.상태.한글 is None:
            self.상태.한글 = 복구한글어댑터()
        self.상태.한글.기능실행("한컴열기")
        if self.상태.한글.원본.대상 is None:
            raise RuntimeError("한글 COM 객체를 가져오지 못했습니다.")
        self.쓰기("한글 연결 완료: 이 런처가 종료될 때까지 같은 연결을 사용합니다.")

    def 기능실행(self, 이름: str, 인자: list | None = None):
        if 이름 not in self._이름별:
            raise ValueError(f"검증 완료 실행 목록에 없는 기능입니다: {이름}")
        if self.상태.한글 is None:
            self.한글연결()
        assert self.상태.한글 is not None
        arguments = 인자 or []
        required = 필수인자목록(self.상태.한글.원본, 이름)
        if len(arguments) < len(required):
            raise ValueError(f"필수 인자가 필요합니다: {', '.join(required)}")
        result = self.상태.한글.기능실행(이름, *arguments)
        self.쓰기(f"실행 완료: {이름}")
        return result

    def 대화형실행(self) -> None:
        self.쓰기("범정부오피스 복구 기능 런처")
        self.쓰기(f"검증 완료 기능 {len(self.기능):,}개 · 도움말은 help")
        while True:
            try:
                parts = shlex.split(input("govoffice> ").strip())
                if not parts:
                    continue
                command, arguments = parts[0].casefold(), parts[1:]
                if command in {"quit", "exit", "종료"}:
                    return
                if command in {"help", "도움말"}:
                    self.쓰기("list [검색어] [개수] | connect | run 기능명 [JSON배열] | exit")
                elif command in {"list", "목록", "search", "검색"}:
                    self.목록출력(arguments[0] if arguments else "", int(arguments[1]) if len(arguments) > 1 else 50)
                elif command in {"connect", "연결"}:
                    self.한글연결()
                elif command in {"run", "실행"}:
                    if not arguments:
                        raise ValueError("실행할 기능명이 필요합니다.")
                    parsed = json.loads(arguments[1]) if len(arguments) > 1 else []
                    if not isinstance(parsed, list):
                        raise ValueError("인자는 JSON 배열이어야 합니다.")
                    self.기능실행(arguments[0], parsed)
                else:
                    self.쓰기("알 수 없는 명령입니다. 도움말은 help")
            except (EOFError, KeyboardInterrupt):
                self.쓰기()
                return
            except Exception as error:
                self.쓰기(f"오류: {error}")


def 실행(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="범정부오피스 복구 기능 런처")
    parser.add_argument("--list", action="store_true", help="검증 완료 기능 목록 출력")
    parser.add_argument("--search", default="", help="기능 검색어")
    parser.add_argument("--limit", type=int, default=50, help="목록 표시 개수")
    parser.add_argument("--run", metavar="기능명", help="검증 완료 기능 실행")
    parser.add_argument("--args", default="[]", help="실행 인자 JSON 배열")
    parser.add_argument("--cli", action="store_true", help="콘솔 대화형 런처 사용")
    options = parser.parse_args(argv)
    launcher = 기능런처()
    if options.list or options.search:
        launcher.목록출력(options.search, options.limit)
    elif options.run:
        arguments = json.loads(options.args)
        if not isinstance(arguments, list):
            parser.error("--args는 JSON 배열이어야 합니다.")
        launcher.기능실행(options.run, arguments)
    elif options.cli:
        launcher.대화형실행()
    else:
        import subprocess
        from pathlib import Path
        script = Path(__file__).resolve().parents[3] / "launch_gui.ps1"
        raise SystemExit(subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)]).returncode)
