from pathlib import Path
import subprocess
import sys
import unittest


@unittest.skipUnless(sys.platform == 'win32', 'Windows WPF guard')
class WindowPollGuardTests(unittest.TestCase):
    def test_native_move_loop_skips_scripts_and_restores_polling(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass',
                                 '-File',str(project/'development/tests/window_poll_guard_probe.ps1')],
                                capture_output=True,timeout=30)
        self.assertEqual(0,result.returncode,(result.stdout+result.stderr).decode('utf-8',errors='replace'))
        self.assertIn(b'WINDOW_POLL_GUARD_OK',result.stdout)

    def test_internal_build_includes_guard(self):
        project = Path(__file__).resolve().parents[2]
        self.assertIn('"gui_poll_guard.cs"',(project/'packaging/build_internal_release.py').read_text(encoding='utf-8'))
