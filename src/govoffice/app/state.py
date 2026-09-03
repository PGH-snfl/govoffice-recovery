from dataclasses import dataclass

from ..ports.hwp import 한글문서포트


@dataclass(slots=True)
class 애플리케이션상태:
    """새 프로젝트가 관리하는 실행 의존성."""

    한글: 한글문서포트

