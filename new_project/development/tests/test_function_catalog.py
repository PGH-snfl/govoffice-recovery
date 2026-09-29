import unittest

from govoffice.app.function_catalog import 검증완료기능목록, 필수인자목록


class 기능카탈로그시험(unittest.TestCase):
    def test_검증완료_기능만_노출한다(self):
        functions = 검증완료기능목록()
        self.assertEqual(1423, len(functions))
        self.assertTrue(all(item.검증상태 in {"static_exact", "dynamic_exact", "same_error"} for item in functions))

    def test_필수인자를_구분한다(self):
        class 대상:
            def 기능(self, 값, 선택=1):
                pass

        self.assertEqual(("값",), 필수인자목록(대상(), "기능"))


if __name__ == "__main__":
    unittest.main()
