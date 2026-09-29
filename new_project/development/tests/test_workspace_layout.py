"""Directory reorganization must not break launchers or source assets."""
import ast
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]


class WorkspaceLayoutTests(unittest.TestCase):
    def test_bundled_python_native_extensions_are_not_treated_as_cache(self):
        runtime = ROOT / '범피스1303_분석/python313'
        for filename in ('unicodedata.pyd', '_ssl.pyd', '_elementtree.pyd', '_sqlite3.pyd', '_ctypes.pyd', '_socket.pyd'):
            self.assertTrue((runtime / filename).is_file(), filename)
        self.assertNotIn('*.py[cod]', (ROOT / '.gitignore').read_text(encoding='utf-8'))
        self.assertNotIn('*.py[cod]', (ROOT / 'new_project/.gitignore').read_text(encoding='utf-8'))

    def test_preserved_execution_roots(self):
        for relative in (
            'new_project/src/govoffice', 'new_project/config', 'recovered',
            '범피스1303_분석/python313/python.exe', 'runtime/HwpAutomation',
            'docs/AUTHORING_REFERENCE_MEMORY.md', 'exa-results',
        ):
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_document_and_original_locations(self):
        for relative in (
            'originals/범피스1303.exe', 'originals/범피스가이드북.pdf',
            'materials/examples/범피스 예시1.hwp', 'materials/examples/범피스 예시2.hwp',
            'materials/attachments', 'materials/validation',
            'materials/submission-reference/제출서류',
        ):
            self.assertTrue((ROOT / relative).exists(), relative)
        for relative in ('범피스1303.exe', '범피스가이드북.pdf', '범피스 예시1.hwp',
                         '범피스 예시2.hwp', '예시 문서', '3. 제출서류 및 참고',
                         '첨부자료', 'AI 문서 작성 실검증 결과'):
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_root_launcher_delegates_without_new_runtime_logic(self):
        text = (ROOT / '범정부오피스_실행.cmd').read_text(encoding='utf-8')
        self.assertIn('call "%~dp0new_project\\launch_govoffice.cmd"', text)
        self.assertIn('exit /b %errorlevel%', text)
        self.assertTrue((ROOT / 'new_project/launch_govoffice.cmd').is_file())

    def test_climate_tools_reference_existing_sources(self):
        source_dir = ROOT / 'materials/submission-reference/제출서류'
        self.assertTrue(any(source_dir.glob('*.hwp')))
        for name in ('extract_climate_template.py', 'prepare_climate_assets.py'):
            code = (ROOT / 'new_project/development/tools' / name).read_text(encoding='utf-8')
            ast.parse(code)
            self.assertIn('materials/submission-reference/제출서류', code)
            self.assertNotIn("ROOT.parent / '3. 제출서류 및 참고", code)

    def test_new_navigation_links_exist(self):
        for relative in ('README.md', 'docs/README.md', 'docs/DIRECTORY_LAYOUT.md',
                         'materials/README.md', 'originals/README.md',
                         'new_project/development/docs/README.md'):
            path = ROOT / relative
            text = path.read_text(encoding='utf-8')
            for match in re.finditer(r'\]\((?:<([^>]+)>|([^\s)]+))\)', text):
                target = unquote(match.group(1) or match.group(2))
                if target.startswith(('https://', 'http://', '#')):
                    continue
                self.assertTrue((path.parent / target.split('#')[0]).exists(), (relative, target))


if __name__ == '__main__':
    unittest.main()
