from dataclasses import dataclass
from typing import Any


@dataclass
class 앱상태:
    """Office 연결과 현재 작업 대상을 한곳에서 관리한다."""

    한컴: Any | None = None
    엑셀: Any | None = None
    피피티: Any | None = None

