from .state import 애플리케이션상태
from ..adapters.recovered_hwp import 복구한글어댑터


def 애플리케이션생성() -> 애플리케이션상태:
    """복구 API는 어댑터 뒤에 둔 채 새 애플리케이션을 구성한다."""

    return 애플리케이션상태(한글=복구한글어댑터())

