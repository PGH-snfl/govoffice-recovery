"""원본 ``한컴오피스.한컴라이브러리_기본`` 호환 진입점."""

from .recovered_source.generated.common import (
    GeneratedSimpleCommandMixin,
    Generated한컴기본CompositionMixin,
)
from .recovered_source.common.commands import HwpCommandMixin
from .recovered_source.common.connection import HwpConnectionMixin
from .recovered_source.common.formatting import HwpFormattingMixin
from .recovered_source.common.search import HwpSearchFeatureMixin
from .recovered_source.common.block import HwpBlockFeatureMixin
from .recovered_source.common.table import HwpTableFeatureMixin
from .recovered_source.common.text import HwpTextFeatureMixin
from .recovered_source.common.signature_defaults import apply_signature_defaults


class 한컴기본(
    HwpConnectionMixin,
    HwpTableFeatureMixin,
    HwpTextFeatureMixin,
    HwpBlockFeatureMixin,
    HwpSearchFeatureMixin,
    Generated한컴기본CompositionMixin,
    GeneratedSimpleCommandMixin,
    HwpCommandMixin,
    HwpFormattingMixin,
):
    대상 = None
    글머리 = "  - "
    셀높이 = 1000
    셀넓이 = 1000
    문서용지 = [0, 0, 0, 0, 0, 0]
    임시요일 = ["월", "화", "수", "목", "금", "토", "일"]
    임시카운트 = 0
    로마숫자 = ["", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ"]
    원숫자 = ["", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮"]
    가숫자 = ["", "가", "나", "다", "라", "마", "바", "사", "아", "자", "차", "카", "타", "파", "하"]
    패브릭스바옵션 = 1
    중제목카운트 = 0
    소제목카운트 = 0
    참고카운트 = 0
    붙임카운트 = 0
    가제목카운트 = 0
    원숫자카운트 = 0
    네모숫자카운트 = 0
    궁극의정리위치보정 = 0
    위치저장 = 0
    방금처리 = 0

    def 방금처리0(self):
        self.방금처리 = 0


apply_signature_defaults(한컴기본)

BYTECODE_BACKED_METHODS = frozenset()
__all__ = ["한컴기본"]
