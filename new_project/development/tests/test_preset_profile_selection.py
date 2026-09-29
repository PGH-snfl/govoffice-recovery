"""Regression tests for reusing preset cell extraction, not a live HWP test."""
import ast
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

from govoffice.adapters.recovered_hwp import 복구한글어댑터
from govoffice.adapters.json_user_profile import JSON사용자프로필저장소
from govoffice.domain.user_profile import 사용자프로필
from govoffice.services.profile_table import ProfileTableCommands
from govoffice.services.hwpml_table_analysis import HWPMLTableFieldAnalyzer
from govoffice.services.style_review_fields import normalize_review_fields


def cell(text, **attrs):
    attributes = ' '.join(f'{key}="{value}"' for key, value in attrs.items())
    return f'<CELL {attributes}><P><TEXT><CHAR>{text}</CHAR></TEXT></P></CELL>'


SELECTED = ('<HWPML><BODY><SECTION><TABLE>'
    '<ROW>' + cell('연구책임자', RowSpan=2) + cell('성명') + cell('홍길동') + '</ROW>'
    '<ROW>' + cell('전화번호', ColAddr=1) + cell('010-1234-5678', ColAddr=2) + '</ROW>'
    '</TABLE></SECTION></BODY></HWPML>')


class PresetBlock:
    def __init__(self, mode=3):
        self.SelectionMode = mode
        self.calls = []

    def GetTextFile(self, format, option):
        self.calls.append((format, option))
        if (format, option) != ('HWPML2X', 'saveblock'):
            raise AssertionError('Do not read the whole table/document')
        return SELECTED

    def InitScan(self, *args):
        raise AssertionError('Personal import must reuse preset cell extraction')


class PresetProfileSelectionTest(unittest.TestCase):
    def test_same_exporter_preserves_selected_merged_cells_unchanged(self):
        for mode in (3, 19):
            document = PresetBlock(mode)
            adapter = 복구한글어댑터(SimpleNamespace(대상=document))
            source = adapter.선택영역서식내보내기()
            self.assertEqual(SELECTED, source)
            self.assertIn('RowSpan="2"', source)
            self.assertEqual([('HWPML2X', 'saveblock')], document.calls)
            self.assertFalse(hasattr(adapter, '선택영역데이터내보내기'))

    def test_personal_and_production_preset_analysis_have_same_cells_and_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = JSON사용자프로필저장소(Path(directory) / 'profile.json')
            profile = 사용자프로필.생성({}).대표필드추가('연구책임자')
            profile = profile.하위필드추가('연구책임자', '성명', ('이전 값',))
            repo.저장(profile)
            personal = ProfileTableCommands(repo).analyze(SELECTED, 'doc')['candidates']

            # Execute the actual preset analysis statements, not a copied algorithm.
            backend = ast.parse(Path(__file__).resolve().parents[2].joinpath('gui_backend.py').read_text(encoding='utf-8'))
            handler = next(n for n in backend.body if isinstance(n, ast.FunctionDef) and n.name == '처리')
            branch = next(n for n in handler.body if isinstance(n, ast.If) and 'style_preset_analyze' in ast.unparse(n.test))
            start = next(i for i, n in enumerate(branch.body) if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == '분석시작')
            end = next(i for i, n in enumerate(branch.body) if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == '후보')
            namespace = dict(프로필=profile, 원본hwpml=SELECTED, time=time,
                HWPMLTableFieldAnalyzer=HWPMLTableFieldAnalyzer, normalize_review_fields=normalize_review_fields)
            exec(compile(ast.Module(body=branch.body[start:end+1], type_ignores=[]), 'preset_analysis_test', 'exec'), namespace)
            expected = namespace['후보']
            self.assertTrue(any(c['value'] == '홍길동' for c in personal))
            self.assertTrue(any(c['value'] == '010-1234-5678' for c in personal))
            self.assertEqual({c['candidate_id']: c for c in expected},
                             {c['candidate_id']: c for c in personal})

    def test_review_writes_only_confirmed_values_to_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profile.json'
            repo = JSON사용자프로필저장소(path)
            repo.저장(사용자프로필.생성({}))
            original = path.read_bytes()
            commands = ProfileTableCommands(repo)
            result = commands.analyze(SELECTED, 'doc')
            self.assertEqual(original, path.read_bytes())
            selected = next(c for c in result['candidates'] if c['value'] == '홍길동')
            commands.save_selection(dict(draft_id=result['draft_id'], rows=[
                dict(candidate_id=selected['candidate_id'], field='연구책임자 > 이름', value=selected['value'])]), 'doc')
            self.assertIn('홍길동', repo.불러오기().대표필드찾기('연구책임자 > 이름').값목록)
            self.assertEqual(['profile.json'], [p.name for p in Path(directory).iterdir()])


if __name__ == '__main__':
    unittest.main()
