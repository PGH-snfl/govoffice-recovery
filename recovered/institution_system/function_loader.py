"""기관 manifest에 등록된 내부 함수를 안전한 패키지 경로에서 불러온다."""

from __future__ import annotations

import importlib
import re

from .tab_model import 기관기능


_기관ID = re.compile(r"^[a-z][a-z0-9_]*$")
_모듈경로 = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_.]*$")


class 기관기능오류(RuntimeError):
    pass


def 실행함수불러오기(기관id: str, 기능: 기관기능):
    if not _기관ID.fullmatch(기관id):
        raise 기관기능오류(f"잘못된 기관 ID: {기관id}")
    try:
        모듈명, 함수명 = 기능.handler.split(":", 1)
    except ValueError as e:
        raise 기관기능오류(f"잘못된 handler: {기능.handler}") from e
    if not _모듈경로.fullmatch(모듈명) or not 함수명.isidentifier():
        raise 기관기능오류(f"잘못된 handler: {기능.handler}")

    전체모듈명 = f"institutions.{기관id}.{모듈명}"
    try:
        모듈 = importlib.import_module(전체모듈명)
        return getattr(모듈, 함수명)
    except (ImportError, AttributeError) as e:
        raise 기관기능오류(f"기관 기능을 불러올 수 없습니다: {기능.id}") from e


def 기관기능실행(기관id: str, 기능: 기관기능, 한컴, *args, **kwargs):
    함수 = 실행함수불러오기(기관id, 기능)
    if 기능.legacy_method:
        return 함수(한컴, 기능.legacy_method, *args, **kwargs)
    return 함수(한컴, *args, **kwargs)

