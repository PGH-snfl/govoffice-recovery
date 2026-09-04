from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class 서식복사결과:
    단계: str
    메시지: str
    실행결과: Any = None


class 서식복사서비스:
    """한글의 ShapeCopyPaste를 두 번 누르는 작업 흐름으로 감싼다.

    첫 실행은 원본 서식을 담고, 두 번째 실행은 사용자가 새로 선택한
    대상 영역에 담아 둔 서식을 적용한다. COM 호출에 실패하면 단계는
    바뀌지 않으므로 사용자가 같은 작업을 다시 시도할 수 있다.
    """

    def __init__(self) -> None:
        self._적용대기 = False

    @property
    def 적용대기(self) -> bool:
        return self._적용대기

    def 실행(self, 모양복사실행: Callable[[], Any]) -> 서식복사결과:
        실행결과 = 모양복사실행()
        if not self._적용대기:
            self._적용대기 = True
            return 서식복사결과(
                단계="captured",
                메시지="서식을 담았습니다. 적용할 글자나 문단을 선택한 뒤 같은 버튼을 다시 누르세요.",
                실행결과=실행결과,
            )

        self._적용대기 = False
        return 서식복사결과(
            단계="applied",
            메시지="선택 영역에 글자·문단 서식을 적용했습니다.",
            실행결과=실행결과,
        )

    def 초기화(self) -> bool:
        대기중이었음 = self._적용대기
        self._적용대기 = False
        return 대기중이었음
