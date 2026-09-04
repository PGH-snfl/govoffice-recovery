import tempfile
import unittest
from pathlib import Path

from institution_system import 즐겨찾기실행, 즐겨찾기저장소


class 즐겨찾기시험(unittest.TestCase):
    def setUp(self):
        self.임시폴더 = tempfile.TemporaryDirectory()
        self.저장소 = 즐겨찾기저장소(Path(self.임시폴더.name) / "favorites.json")

    def tearDown(self):
        self.임시폴더.cleanup()

    def test_한글_기본기능을_저장하고_다시_읽는다(self):
        self.assertTrue(self.저장소.한글기본기능추가("엔터", args=(2,)))
        항목 = self.저장소.전체()[0]
        self.assertEqual(항목.name, "엔터")
        self.assertEqual(항목.hwp_method, "엔터")
        self.assertEqual(항목.args, (2,))

    def test_중복_즐겨찾기는_추가하지_않는다(self):
        self.assertTrue(self.저장소.한글기본기능추가("오늘날짜"))
        self.assertFalse(self.저장소.한글기본기능추가("오늘날짜"))
        self.assertEqual(len(self.저장소.전체()), 1)

    def test_즐겨찾기_순서를_바꾼다(self):
        self.저장소.한글기본기능추가("엔터")
        self.저장소.한글기본기능추가("오늘날짜")
        self.assertTrue(self.저장소.이동("hwp:오늘날짜", 0))
        self.assertEqual([항목.hwp_method for 항목 in self.저장소.전체()], ["오늘날짜", "엔터"])

    def test_즐겨찾기는_저장된_인자로_한컴을_호출한다(self):
        self.저장소.한글기본기능추가("엔터", args=(3,))

        class 가짜한컴:
            def 엔터(self, 횟수):
                return 횟수

        self.assertEqual(즐겨찾기실행(self.저장소.전체()[0], 가짜한컴()), 3)


if __name__ == "__main__":
    unittest.main()

