"""원본 `기본한컴` 공개 API 호환 계층."""

from .recovered_source.generated.main import Generated기본한컴CompositionMixin
from .recovered_source.validated.main import Validated기본한컴Mixin
from .recovered_source.common.range_cleanup import MainRangeCleanupMixin
from .recovered_source.common.range_format import MainRangeFormatMixin
from .recovered_source.common.search import MainSearchFeatureMixin
from .recovered_source.common.document_cleanup import MainDocumentCleanupMixin
from .recovered_source.common.institution_features import MainInstitutionFeatureMixin
from .recovered_source.common.block import MainBlockFeatureMixin
from .recovered_source.common.signature_defaults import apply_signature_defaults
from .한컴라이브러리_1 import 한컴1
from .한컴라이브러리_2 import 한컴2


class 기본한컴(MainBlockFeatureMixin, MainInstitutionFeatureMixin, MainDocumentCleanupMixin, MainRangeFormatMixin, MainSearchFeatureMixin, MainRangeCleanupMixin, Validated기본한컴Mixin, Generated기본한컴CompositionMixin, 한컴1, 한컴2):
    pass


apply_signature_defaults(기본한컴)

BYTECODE_BACKED_METHODS = frozenset()
__all__ = ["기본한컴"]
