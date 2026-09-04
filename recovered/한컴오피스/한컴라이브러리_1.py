"""원본 `한컴1` 공개 API 호환 계층."""

from .recovered_source.generated.hwp1 import Generated한컴1CompositionMixin
from .recovered_source.validated.hwp1 import Validated한컴1Mixin
from .recovered_source.common.range_cleanup import Hwp1RangeCleanupMixin
from .recovered_source.common.range_format import Hwp1RangeFormatMixin
from .recovered_source.common.institution_features import Hwp1InstitutionFeatureMixin
from .recovered_source.common.signature_defaults import apply_signature_defaults
from .한컴라이브러리_기본 import 한컴기본


class 한컴1(Hwp1InstitutionFeatureMixin, Hwp1RangeFormatMixin, Hwp1RangeCleanupMixin, Validated한컴1Mixin, Generated한컴1CompositionMixin, 한컴기본):
    pass


apply_signature_defaults(한컴1)

BYTECODE_BACKED_METHODS = frozenset()
__all__ = ["한컴1"]
