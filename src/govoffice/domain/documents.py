from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class 공문:
    제목: str
    본문: str

    def __post_init__(self) -> None:
        if not self.제목.strip():
            raise ValueError("공문 제목은 비어 있을 수 없습니다.")

