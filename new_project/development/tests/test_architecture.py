import ast
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[2] / "src" / "govoffice"


class 프로젝트경계시험(unittest.TestCase):
    def test_복구패키지는_어댑터에서만_import한다(self):
        violations = []
        for source in SOURCE.rglob("*.py"):
            if source.name == "recovered_hwp.py" or "runtime" in source.parts:
                continue
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.startswith("한컴오피스"):
                        violations.append(str(source))
                if isinstance(node, ast.Import):
                    if any(name.name.startswith("한컴오피스") for name in node.names):
                        violations.append(str(source))
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
