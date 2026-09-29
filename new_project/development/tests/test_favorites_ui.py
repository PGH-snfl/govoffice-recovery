import base64
import os
from pathlib import Path
import shutil
import subprocess
import unittest


@unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"), "Windows WPF required")
class FavoritesUITest(unittest.TestCase):
    def test_search_add_edit_run_remove_and_repeat_refresh(self):
        root = Path(__file__).resolve().parents[2]
        probe = str(root / "development" / "tests" / "favorites_ui_probe.ps1").replace("'", "''")
        source = str(root / "favorites_ui.ps1").replace("'", "''")
        script = f"& '{probe}' -Source '{source}'"
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-STA", "-ExecutionPolicy", "Bypass", "-EncodedCommand",
             base64.b64encode(script.encode("utf-16-le")).decode("ascii")], capture_output=True, timeout=40,
        )
        self.assertEqual(0, result.returncode, result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
        self.assertIn(b"FAVORITES_UI_OK", result.stdout)
