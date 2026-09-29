import ast
import os
from pathlib import Path
import re
import shutil
import subprocess
import unittest


PROJECT = Path(__file__).resolve().parents[2]


class NormalWindowTests(unittest.TestCase):
    def test_no_product_window_forces_always_on_top(self):
        for path in PROJECT.glob('*.ps1'):
            source = path.read_text(encoding='utf-8-sig')
            self.assertIsNone(re.search(r'(?i)\.Topmost\s*=\s*\$true\b|Topmost\s*=\s*[\"\x27]True[\"\x27]', source), path.name)
        source = (PROJECT / 'src/govoffice/presentation/gui_launcher.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        settings = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute) and node.func.attr == 'attributes'
                    and node.args and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == '-topmost']
        self.assertEqual(2, len(settings))
        for setting in settings:
            self.assertIs(setting.args[1].value, False)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows required')
    def test_native_window_settings_and_process_identity_without_showing_ui(self):
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(PROJECT / 'development/tests/normal_window_probe.ps1'),
            '-Project', str(PROJECT),
        ], capture_output=True, timeout=25)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'NORMAL_WINDOW_OK', result.stdout)
