import inspect
import json
import unittest
from pathlib import Path

from 한컴오피스.한컴라이브러리 import 기본한컴
from 한컴오피스.한컴라이브러리_1 import 한컴1
from 한컴오피스.한컴라이브러리_2 import 한컴2
from 한컴오피스.한컴라이브러리_기본 import 한컴기본


class 기록함수:
    def __init__(self):
        self.호출 = []

    def __call__(self, *args, **kwargs):
        self.호출.append((args, kwargs))


class 원본API시험(unittest.TestCase):
    def test_1511개_메서드의_이름과_시그니처를_보존한다(self):
        manifest = json.loads(
            (Path(__file__).resolve().parents[1] / "metadata" / "hwp_api_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        classes = {
            "한컴라이브러리_기본": 한컴기본,
            "한컴라이브러리_1": 한컴1,
            "한컴라이브러리_2": 한컴2,
            "한컴라이브러리": 기본한컴,
        }
        checked = 0
        for module_name, module_data in manifest["modules"].items():
            cls = classes[module_name]
            for method in module_data["methods"]:
                actual = getattr(cls, method["name"])
                actual_args = list(inspect.signature(actual).parameters)
                self.assertEqual(actual_args, method["args"], method["name"])
                checked += 1
        self.assertEqual(checked, 1511)

    def test_한컴1_바이트코드_메서드가_복구된_기반API를_호출한다(self):
        대상 = 한컴1()
        대상.새창 = 기록함수()
        대상.문서여백 = 기록함수()
        대상.문장 = 기록함수()
        대상.홍성예시()
        self.assertTrue(대상.새창.호출)
        self.assertTrue(대상.문서여백.호출)
        self.assertTrue(대상.문장.호출)

    def test_한컴2_바이트코드_메서드가_복구된_서식API를_호출한다(self):
        대상 = 한컴2()
        대상.글자크기 = 기록함수()
        대상.문단위 = 기록함수()
        대상.문단아래 = 기록함수()
        대상.폰트 = 기록함수()
        대상.문장 = 기록함수()
        대상.가스공소제목("1", "내용")
        self.assertTrue(대상.글자크기.호출)
        self.assertTrue(대상.문장.호출)

    def test_기본한컴_바이트코드_메서드가_상속API를_호출한다(self):
        대상 = 기본한컴()
        대상.폰트 = 기록함수()
        대상.문장 = 기록함수()
        대상.질병좌따()
        self.assertTrue(대상.폰트.호출)
        self.assertTrue(대상.문장.호출)


if __name__ == "__main__":
    unittest.main()
