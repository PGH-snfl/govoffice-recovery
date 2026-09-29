import unittest
from types import SimpleNamespace
import xml.etree.ElementTree as ET

from govoffice.adapters.recovered_hwp import 복구한글어댑터
from govoffice.services.cell_selection import crop_scanned_cells, cell_cursor
from govoffice.services.hwpml_table_analysis import HWPMLTableFieldAnalyzer


def cell(row, col, text, rs=1, cs=1):
    return f'<CELL RowAddr="{row}" ColAddr="{col}" RowSpan="{rs}" ColSpan="{cs}"><P><TEXT><CHAR>{text}</CHAR></TEXT></P></CELL>'


def table(rows):
    return '<HWPML><BODY><SECTION><TABLE>' + ''.join('<ROW>'+r+'</ROW>' for r in rows) + '</TABLE></SECTION></BODY></HWPML>'


SOURCE = table([
    cell(0,0,'선택 밖 위쪽',cs=3),
    cell(1,0,'연구자',rs=2)+cell(1,1,'성명')+cell(1,2,'홍길동'),
    cell(2,1,'전화번호')+cell(2,2,'010-1234-5678'),
    cell(3,0,'선택 밖 기간',cs=3),
])
SCAN = '연구자성명홍길동전화번호010-1234-5678'


class NativeCellBlock:
    SelectionMode = 19

    def __init__(self):
        self.calls = []
        self.records = iter([(2, SCAN), (1, '')])
        self.pos = (4,0,0)

    def GetPos(self): return self.pos
    def KeyIndicator(self): return (0, '(C3): 문자 입력')
    def InitScan(self, option, range):
        self.calls.append(('scan', option, range))
        return True
    def GetText(self): return next(self.records)
    def ReleaseScan(self): self.calls.append(('release',))
    def GetTextFile(self, fmt, option):
        assert (fmt, option) == ('HWPML2X', 'saveblock')
        self.calls.append(('export',fmt,option))
        return SOURCE  # Reproduce the real bug: returns the enclosing WHOLE table.


class CellSelectionTest(unittest.TestCase):
    def test_real_failure_shape_crops_before_existing_analyzer(self):
        doc = NativeCellBlock()
        adapter = 복구한글어댑터(SimpleNamespace(대상=doc))
        xml = adapter.선택영역서식내보내기(선택텍스트검증=True)
        self.assertNotIn('선택 밖',xml)
        self.assertIn('RowSpan="2"',xml)
        self.assertEqual(5,adapter.최근선택진단['selected_cell_count'])
        self.assertEqual([1,0,3,3],adapter.최근선택진단['selected_bounds'])
        self.assertEqual(('scan',7,255),doc.calls[0])
        self.assertEqual(1,doc.calls.count(('release',)))
        result = HWPMLTableFieldAnalyzer().analyze(xml).as_dict()
        self.assertTrue(any(c['value']=='홍길동' for c in result['candidates']))
        self.assertFalse(any('선택 밖' in str(c) for c in result['candidates']))

    def test_column_subset_and_reverse_drag_cursor(self):
        source=table([ ''.join(cell(r,c,f'R{r}C{c}') for c in range(4)) for r in range(4)])
        selected='R1C1R1C2R2C1R2C2'
        for cursor in ((1,1),(2,2)):
            xml, info=crop_scanned_cells(source,selected,cursor)
            self.assertEqual([1,1,3,3],info['selected_bounds'])
            self.assertEqual(4,len(list(ET.fromstring(xml).iter('CELL'))))
            self.assertNotIn('R1C0',xml)

    def test_duplicate_blocks_require_cursor_and_never_take_first_match(self):
        source=table([cell(r,0,'성명')+cell(r,1,'홍길동') for r in range(2)])
        with self.assertRaises(ValueError):crop_scanned_cells(source,'성명홍길동',None)
        _, info=crop_scanned_cells(source,'성명홍길동',(1,1))
        self.assertEqual([1,0,2,2],info['selected_bounds'])

    def test_blank_cells_inside_are_preserved(self):
        source=table([cell(0,0,'A')+cell(0,1,'')+cell(0,2,'B')])
        xml,info=crop_scanned_cells(source,'AB',(0,2))
        self.assertEqual(3,info['selected_cell_count'])
        self.assertEqual(3,len(list(ET.fromstring(xml).iter('CELL'))))

    def test_empty_mismatched_partial_cell_and_cut_merge_fail_closed(self):
        for scan,cursor in [('',(1,1)),('없는내용',(1,1)),('홍길',(1,2)),('전화번호010-1234-5678',(2,0))]:
            with self.subTest(scan=scan),self.assertRaises(ValueError):
                crop_scanned_cells(SOURCE,scan,cursor)

    def test_scan_errors_release_and_do_not_export_whole_table(self):
        for records in [[(101,'')],[(2,'part'),(102,'')]]:
            doc=NativeCellBlock();doc.records=iter(records)
            with self.assertRaises(ValueError):
                복구한글어댑터(SimpleNamespace(대상=doc)).선택영역서식내보내기(선택텍스트검증=True)
            self.assertEqual([('scan',7,255),('release',)],doc.calls)

    def test_modes_three_and_nineteen_both_read_cells(self):
        for mode in (3,19):
            doc=NativeCellBlock();doc.SelectionMode=mode
            self.assertNotIn('선택 밖',복구한글어댑터(SimpleNamespace(대상=doc)).선택영역서식내보내기(선택텍스트검증=True))

    def test_multiline_and_split_scan_chunks_do_not_define_cell_boundaries(self):
        doc=NativeCellBlock()
        doc.records=iter([(2,'연구자'),(3,'성명\r\n'),(2,'홍길동'),(2,''),(2,'전화번호'),(2,'010-1234-5678'),(1,'')])
        xml=복구한글어댑터(SimpleNamespace(대상=doc)).선택영역서식내보내기(선택텍스트검증=True)
        self.assertEqual(5,len(list(ET.fromstring(xml).iter('CELL'))))

    def test_indicator_does_not_invent_a_cell_address(self):
        self.assertEqual((15,28),cell_cursor('(AC16): 문자 입력'))
        self.assertIsNone(cell_cursor('본문'))


if __name__ == '__main__':unittest.main()
