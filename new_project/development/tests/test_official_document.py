import unittest

from govoffice.domain.documents import 공문
from govoffice.services.official_document import 공문작성서비스


class 기록한글:
    def __init__(self):
        self.호출 = []

    def 문장(self, 내용):
        self.호출.append(("문장", 내용))

    def 줄바꿈(self):
        self.호출.append(("줄바꿈",))


class 공문서비스시험(unittest.TestCase):
    def test_업무코드는_복구API없이_시험할_수_있다(self):
        한글 = 기록한글()
        공문작성서비스(한글).작성(공문("제목", "본문"))
        self.assertEqual(
            [("문장", "제목"), ("줄바꿈",), ("문장", "본문")],
            한글.호출,
        )


if __name__ == "__main__":
    unittest.main()

