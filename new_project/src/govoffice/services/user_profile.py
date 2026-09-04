from __future__ import annotations

from typing import Mapping

from ..domain.user_profile import 사용자대표필드, 사용자정보필드, 사용자프로필
from ..ports.hwp import 한글문서포트
from ..ports.user_profile import 사용자프로필저장포트


class 사용자프로필서비스:
    def __init__(self, 저장소: 사용자프로필저장포트, 한글: 한글문서포트 | None = None) -> None:
        self._저장소 = 저장소
        self._한글 = 한글

    def 불러오기(self) -> 사용자프로필:
        return self._저장소.불러오기()

    def 저장(self, 값: Mapping[str, object]) -> 사용자프로필:
        프로필 = 사용자프로필.생성(값)
        self._저장소.저장(프로필)
        return 프로필

    def 문서항목추가(self, 필드명: object, 입력값: object) -> 사용자프로필:
        프로필 = self.불러오기().문서항목추가(필드명, 입력값)
        self._저장소.저장(프로필)
        return 프로필

    def 문서항목삭제(self, 필드명: object, 입력값: object) -> 사용자프로필:
        프로필 = self.불러오기().문서항목삭제(필드명, 입력값)
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드추가(
        self,
        대표필드명: object,
        값목록: object = (),
        별칭: object = (),
        기본값: object | None = None,
        필드ID: object | None = None,
    ) -> 사용자프로필:
        프로필 = self.불러오기().대표필드추가(
            대표필드명,
            값목록,
            별칭,
            기본값,
            필드ID,
        )
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드삭제(self, 대표필드: object) -> 사용자프로필:
        프로필 = self.불러오기().대표필드삭제(대표필드)
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드상위변경(
        self,
        대표필드: object,
        새상위필드: object | None = None,
    ) -> 사용자프로필:
        프로필 = self.불러오기().대표필드상위변경(대표필드, 새상위필드)
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드병합(self, 원본대표필드: object, 대상대표필드: object) -> 사용자프로필:
        프로필 = self.불러오기().대표필드병합(원본대표필드, 대상대표필드)
        self._저장소.저장(프로필)
        return 프로필

    def 별칭추가(self, 대표필드: object, 별칭: object) -> 사용자프로필:
        프로필 = self.불러오기().별칭추가(대표필드, 별칭)
        self._저장소.저장(프로필)
        return 프로필

    def 별칭삭제(self, 대표필드: object, 별칭: object) -> 사용자프로필:
        프로필 = self.불러오기().별칭삭제(대표필드, 별칭)
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드값추가(
        self,
        대표필드: object,
        입력값: object,
        *,
        기본값으로설정: bool = False,
    ) -> 사용자프로필:
        프로필 = self.불러오기().대표필드값추가(
            대표필드,
            입력값,
            기본값으로설정=기본값으로설정,
        )
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드값삭제(self, 대표필드: object, 입력값: object) -> 사용자프로필:
        프로필 = self.불러오기().대표필드값삭제(대표필드, 입력값)
        self._저장소.저장(프로필)
        return 프로필

    def 기본값지정(self, 대표필드: object, 입력값: object) -> 사용자프로필:
        프로필 = self.불러오기().기본값지정(대표필드, 입력값)
        self._저장소.저장(프로필)
        return 프로필

    def 대표필드목록(self) -> tuple[사용자대표필드, ...]:
        return self.불러오기().대표필드

    def 대표필드찾기(self, 필드명: object) -> 사용자대표필드 | None:
        return self.불러오기().대표필드찾기(필드명)

    def 대표필드ID찾기(self, 필드ID: object) -> 사용자대표필드 | None:
        return self.불러오기().대표필드ID찾기(필드ID)

    def 대표필드명찾기(self, 필드명: object) -> str | None:
        return self.불러오기().대표필드명찾기(필드명)

    def 필드ID찾기(self, 필드명: object) -> str | None:
        return self.불러오기().필드ID찾기(필드명)

    def 대표필드ID매핑(self) -> dict[str, str]:
        return self.불러오기().대표필드ID매핑()

    def 텍스트삽입(self, 필드: str) -> str:
        값 = self.불러오기().필드기본값찾기(필드)
        if not 값:
            raise ValueError(f"개인 탭에 {필드} 값을 먼저 저장하세요.")
        if self._한글 is None:
            raise RuntimeError("연결된 한글 문서가 없습니다.")
        self._한글.문장(값)
        return 값

    def 자동입력값(self) -> dict[str, str]:
        프로필 = self.불러오기()
        결과 = 프로필.별칭포함기본선택값()
        # 프리셋은 표시 이름이나 별칭이 바뀌어도 같은 대표필드를 찾도록
        # schema v3의 안정 ID도 자동 출력값 조회 키로 함께 제공한다.
        for 대표필드 in 프로필.대표필드목록:
            if 대표필드.기본값:
                결과[대표필드.id] = 대표필드.기본값
        return 결과

    def 분류입력값(self) -> dict[str, tuple[str, ...]]:
        return self.불러오기().필드값목록()

    def 별칭포함분류입력값(self) -> dict[str, tuple[str, ...]]:
        return self.불러오기().별칭포함필드값목록()

    def 별칭매핑(self) -> dict[str, tuple[str, ...]]:
        return self.불러오기().별칭매핑()

    def 별칭대표필드매핑(self) -> dict[str, str]:
        return self.불러오기().별칭대표필드매핑()
