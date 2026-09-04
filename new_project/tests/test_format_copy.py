import unittest

from govoffice.services.format_copy import 서식복사서비스


class 서식복사서비스시험(unittest.TestCase):
    def test_첫실행은_서식을_담고_두번째실행은_적용한다(self):
        서비스 = 서식복사서비스()
        호출 = []

        첫번째 = 서비스.실행(lambda: 호출.append("실행") or True)
        self.assertEqual("captured", 첫번째.단계)
        self.assertTrue(서비스.적용대기)

        두번째 = 서비스.실행(lambda: 호출.append("실행") or True)
        self.assertEqual("applied", 두번째.단계)
        self.assertFalse(서비스.적용대기)
        self.assertEqual(["실행", "실행"], 호출)

    def test_COM호출이_실패하면_단계를_진행하지_않는다(self):
        서비스 = 서식복사서비스()

        def 실패():
            raise RuntimeError("실행 실패")

        with self.assertRaisesRegex(RuntimeError, "실행 실패"):
            서비스.실행(실패)
        self.assertFalse(서비스.적용대기)

    def test_다른기능을_누르면_대기상태를_초기화한다(self):
        서비스 = 서식복사서비스()
        서비스.실행(lambda: None)
        self.assertTrue(서비스.초기화())
        self.assertFalse(서비스.적용대기)
        self.assertFalse(서비스.초기화())


if __name__ == "__main__":
    unittest.main()
