"""원본 ``피피티.피피티라이브러리`` 공개 API 호환 계층."""

from datetime import datetime, timedelta

from .connection import PowerPointConnectionMixin
from .shapes import ShapeMixin
from .slides import SlideMixin
from .text import TextMixin


class 피피티(PowerPointConnectionMixin, ShapeMixin, TextMixin, SlideMixin):
    임시요일 = ["월", "화", "수", "목", "금", "토", "일"]
    객체높이 = 0


__all__ = ["피피티", "datetime", "timedelta"]

