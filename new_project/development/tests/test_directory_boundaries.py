from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[2]


class DirectoryBoundaryTests(unittest.TestCase):
    def test_product_development_and_packaging_are_physically_separated(self):
        for path in (
            "development/tests",
            "development/tools",
            "development/reports",
            "development/docs",
            "development/examples",
            "development/screenshots",
            "packaging/installer",
            "product/support",
        ):
            self.assertTrue((PROJECT / path).is_dir(), path)
        for legacy in ("tests", "tools", "reports", "docs", "examples", "deploy", "dist"):
            self.assertFalse((PROJECT / legacy).exists(), legacy)

    def test_release_allowlist_excludes_development_runtime_material(self):
        source = (PROJECT / "packaging/build_internal_release.py").read_text(encoding="utf-8")
        self.assertIn('"product/support/deployment_check.py"', source)
        self.assertIn('"packaging" / "installer"', source)
        for excluded in ('"pythonwin"', '"Demos"', '"demos"', '"scripts"', '"*.dist-info"'):
            self.assertIn(excluded, source)
        self.assertNotIn('shutil.copytree(PROJECT / "development"', source)

    def test_launcher_uses_product_support_and_development_only_logs(self):
        launcher = (PROJECT / "launch_gui.ps1").read_text(encoding="utf-8-sig")
        self.assertIn("product\\support\\deployment_check.py", launcher)
        self.assertIn("development\\reports\\runtime", launcher)


if __name__ == "__main__":
    unittest.main()
