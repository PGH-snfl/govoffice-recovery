"""Behavioral regression checks for the production WPF review dialog."""

import base64
import os
from pathlib import Path
import shutil
import subprocess
import unittest


@unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"), "Windows WPF required")
class StyleReviewBehaviorTest(unittest.TestCase):
    def test_group_moves_two_state_checkboxes_and_stable_initial_priority(self):
        root = Path(__file__).resolve().parents[2]
        launcher = str(root / "launch_gui.ps1").replace("'", "''")
        probe = str(root / "development" / "tests" / "style_review_behavior_probe.ps1").replace("'", "''")
        script = f"& '{probe}' -Launcher '{launcher}'"
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-STA", "-ExecutionPolicy", "Bypass",
             "-EncodedCommand", base64.b64encode(script.encode("utf-16-le")).decode("ascii")],
            capture_output=True, timeout=45,
        )
        self.assertEqual(
            0, result.returncode,
            result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"),
        )
        self.assertIn(b"REVIEW_BEHAVIOR_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
