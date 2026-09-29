"""Safety regressions, deliberately not presented as live HWP verification."""
import unittest
from types import SimpleNamespace

from govoffice.adapters.recovered_hwp import 복구한글어댑터
from govoffice.services.selection_scope import assert_same_selection_text


def block(*values):
    return '<HWPML><HEAD/><BODY><SECTION><TABLE><ROW>' + ''.join(
        '<CELL><P><TEXT><CHAR>' + value + '</CHAR></TEXT></P></CELL>'
        for value in values
    ) + '</ROW></TABLE></SECTION></BODY></HWPML>'


class NativeSelection:
    SelectionMode = 1

    def __init__(self, xml=None, text='성명\t홍길동\r\n'):
        self.xml = xml or block('성명', '홍길동')
        self.text = text
        self.calls = []
        self.pos = (2, 0, 0)
        self.change = False

    def GetPos(self):
        return self.pos

    def CreateSet(self, name):
        return SimpleNamespace(Item=lambda key: 0)

    def GetSelectedPosBySet(self, start, end):
        end.Item = lambda key: 1
        return True

    def GetTextFile(self, fmt, options):
        assert options == 'saveblock', 'Whole document reads are forbidden'
        self.calls.append((fmt, options))
        if fmt == 'UNICODE':
            if isinstance(self.text, Exception):
                raise self.text
            return self.text
        if self.change:
            self.pos = (3, 0, 0)
        return self.xml


class SelectionScopeTest(unittest.TestCase):
    def test_selection_keeps_format_data_unchanged(self):
        doc = NativeSelection()
        adapter = 복구한글어댑터(SimpleNamespace(대상=doc))
        self.assertEqual(doc.xml, adapter.선택영역서식내보내기(선택텍스트검증=True))
        self.assertEqual([('UNICODE', 'saveblock'), ('HWPML2X', 'saveblock')], doc.calls)
        self.assertTrue(adapter.최근선택진단['selection_text_matches'])

    def test_whole_table_is_rejected_before_analysis(self):
        doc = NativeSelection(xml=block('성명', '홍길동', '선택 밖', '가져오면 안 됨'))
        adapter = 복구한글어댑터(SimpleNamespace(대상=doc))
        with self.assertRaisesRegex(ValueError, '범위가 달라'):
            adapter.선택영역서식내보내기(선택텍스트검증=True)
        self.assertNotIn('가져오면 안 됨', str(adapter.최근선택진단))

    def test_duplicate_values_outside_and_reordering_do_not_pass_membership_check(self):
        for xml, text in [
            (block('성명', '홍길동', '성명', '홍길동'), '성명\t홍길동'),
            (block('홍길동', '성명'), '성명\t홍길동'),
        ]:
            with self.subTest(xml=xml), self.assertRaises(ValueError):
                assert_same_selection_text(xml, text)

    def test_unavailable_or_empty_text_is_not_replaced_with_xml(self):
        for text in (None, '', '  ', RuntimeError('COM unavailable')):
            with self.subTest(text=text), self.assertRaises(ValueError):
                doc = NativeSelection(text=text)
                복구한글어댑터(SimpleNamespace(대상=doc)).선택영역서식내보내기(선택텍스트검증=True)

    def test_selection_change_during_export_is_rejected(self):
        doc = NativeSelection()
        doc.change = True
        with self.assertRaisesRegex(ValueError, '선택 영역이 바뀌어'):
            복구한글어댑터(SimpleNamespace(대상=doc)).선택영역서식내보내기(선택텍스트검증=True)

    def test_no_selection_does_not_read_or_enumerate_another_document(self):
        doc = NativeSelection()
        doc.SelectionMode = 0
        def unrelated():
            self.fail('Must not read another HWP document')
        adapter = 복구한글어댑터(SimpleNamespace(대상=doc, _실행중인_한글목록=unrelated))
        with self.assertRaises(ValueError):
            adapter.선택영역서식내보내기(선택텍스트검증=True)
        self.assertEqual([], doc.calls)

    def test_preset_default_is_not_changed(self):
        doc = NativeSelection(text=RuntimeError('TEXT not supported'))
        adapter = 복구한글어댑터(SimpleNamespace(대상=doc))
        self.assertEqual(doc.xml, adapter.선택영역서식내보내기())
        self.assertEqual([('HWPML2X', 'saveblock')], doc.calls)


if __name__ == '__main__':
    unittest.main()
