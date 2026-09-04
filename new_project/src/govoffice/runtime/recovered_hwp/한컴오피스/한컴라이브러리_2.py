"""원본 `한컴2` 공개 API 호환 계층."""

from .recovered_source.generated.hwp2 import Generated한컴2CompositionMixin
from .recovered_source.common.range_cleanup import Hwp2RangeCleanupMixin
from .recovered_source.common.range_format import Hwp2RangeFormatMixin
from .recovered_source.common.institution_features import Hwp2InstitutionFeatureMixin
from .recovered_source.common.signature_defaults import apply_signature_defaults
from .한컴라이브러리_기본 import 한컴기본


class 한컴2(Hwp2InstitutionFeatureMixin, Hwp2RangeFormatMixin, Hwp2RangeCleanupMixin, Generated한컴2CompositionMixin, 한컴기본):
    pass


apply_signature_defaults(한컴2)

BYTECODE_BACKED_METHODS = frozenset()
__all__ = ["한컴2"]
