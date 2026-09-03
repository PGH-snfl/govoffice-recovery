from ..domain.documents import 공문
from ..ports.hwp import 한글문서포트


class 공문작성서비스:
    def __init__(self, 한글: 한글문서포트) -> None:
        self._한글 = 한글

    def 작성(self, 문서: 공문) -> None:
        self._한글.문장(문서.제목)
        self._한글.줄바꿈()
        self._한글.문장(문서.본문)

