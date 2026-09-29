import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from govoffice.services.authoring_table_width import rebalance_written_tables
from govoffice.services.document_authoring import render_draft


def fixture(long_value='가나다 라마바 사아자',merged=False,donor='항목'):
    span='2' if merged else '1'
    def cell(text,col):
        return (f'<CELL Width="10000" Height="1600" ColSpan="{span if col==1 else 1}" RowSpan="1">'
                f'<PARALIST><P><TEXT CharShape="0"><CHAR>{text}</CHAR></TEXT></P></PARALIST></CELL>')
    rows=[cell(donor,0)+cell(long_value,1),cell('기타',0)+cell('보조',1)]
    xml=('<HWPML><HEAD><CHARSHAPELIST><CHARSHAPE Id="0" Height="1000"><FONTID Hangul="1"/>'
         '</CHARSHAPE></CHARSHAPELIST></HEAD><BODY><SECTION><P><TEXT><TABLE ColCount="2">'
         '<INSIDEMARGIN Left="200" Right="200" Top="100" Bottom="100"/>'
         +''.join('<ROW>'+row+'</ROW>' for row in rows)+
         '</TABLE></TEXT></P></SECTION></BODY></HWPML>')
    root=ET.fromstring(xml)
    generated=root.find('.//TABLE/ROW/CELL[2]/PARALIST/P')
    return root,[({'field_id':'P0000'},[generated],[long_value])]


class TableWidthTests(unittest.TestCase):
    def test_overflow_borrows_from_spare_column_without_growing_table(self):
        root,refs=fixture();table=next(root.iter('TABLE'))
        changed=rebalance_written_tables(root,refs,{})
        self.assertEqual(1,len(changed))
        for row in table.findall('ROW'):
            widths=[int(cell.get('Width')) for cell in row.findall('CELL')]
            self.assertEqual(20000,sum(widths))
            self.assertLess(widths[0],10000)
            self.assertGreater(widths[1],10000)
        self.assertEqual('항목',''.join(table.find('ROW/CELL/PARALIST/P').itertext()))

    def test_merged_or_already_fitting_table_keeps_original_widths(self):
        for options in ({'merged':True},{'long_value':'짧음'}):
            root,refs=fixture(**options)
            self.assertEqual([],rebalance_written_tables(root,refs,{}))
            self.assertTrue(all(cell.get('Width')=='10000' for cell in root.iter('CELL')))

    def test_donor_with_long_fixed_content_is_not_squeezed(self):
        root,refs=fixture(donor='가나다 라마바 사아')
        self.assertEqual([],rebalance_written_tables(root,refs,{}))

    def test_graphic_cell_is_not_resized(self):
        root,refs=fixture()
        root.find('.//TABLE/ROW/CELL/PARALIST/P/TEXT').append(ET.Element('CONTAINER'))
        self.assertEqual([],rebalance_written_tables(root,refs,{}))

    def test_normal_document_render_applies_width_change(self):
        root,_=fixture(long_value='____')
        manifest={'paragraph_count':len(list(root.iter('P'))),
                  'render_policy':{'readable_body':True},
                  'topics':[{'id':'s','start':0,'fields':[{'id':'P0002','index':2,'original':'____',
                             'label':'연구 내용','role':'body','max_chars':200,'multiline':True}]}]}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,log=render_draft(folder,manifest,{},local_values={'P0002':'가나다 라마바 사아자'})
        out=ET.fromstring(xml);rows=next(out.iter('TABLE')).findall('ROW')
        self.assertTrue(all(int(row.findall('CELL')[1].get('Width'))>10000 for row in rows))
        self.assertEqual('가나다 라마바 사아자',log[0]['value'])


if __name__=='__main__':unittest.main()
