import io
import unittest

from govoffice.presentation.launcher import 기능런처


class 런처시험(unittest.TestCase):
    def test_연결없이_검증완료목록을_검색한다(self):
        output = io.StringIO()
        launcher = 기능런처(output)
        result = launcher.검색("가운데정렬")
        self.assertTrue(any(item.이름 == "가운데정렬" for item in result))
        launcher.목록출력("가운데정렬", 10)
        self.assertIn("가운데정렬", output.getvalue())


if __name__ == "__main__":
    unittest.main()
