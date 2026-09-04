import ast
import json
import unittest
from pathlib import Path


RECOVERED = Path(__file__).resolve().parents[1]
HWP = RECOVERED / "한컴오피스"
SOURCE = HWP / "recovered_source"
COMPAT = HWP / "compat"


class 복구경계시험(unittest.TestCase):
    def test_복구완료소스는_marshal이나_compat에_의존하지_않는다(self):
        violations = []
        for path in SOURCE.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [item.name for item in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or ""]
                else:
                    continue
                if any(name == "marshal" or "compat" in name for name in names):
                    violations.append(str(path.relative_to(RECOVERED)))
        self.assertEqual([], violations)

    def test_compat에는_미복구_런타임만_존재한다(self):
        python_files = sorted(path.name for path in COMPAT.glob("*.py"))
        self.assertEqual(["__init__.py", "legacy_runtime.py"], python_files)

    def test_상태목록은_복구와_미복구를_동시에_표시하지_않는다(self):
        coverage = json.loads(
            (RECOVERED / "metadata" / "hwp_coverage.json").read_text(encoding="utf-8")
        )
        for module in coverage["modules"].values():
            source = set(module["source_recovered"])
            bytecode = set(module["bytecode_backed"])
            self.assertFalse(source & bytecode)
            self.assertEqual(set(module["recovered"]), source | bytecode)


if __name__ == "__main__":
    unittest.main()

