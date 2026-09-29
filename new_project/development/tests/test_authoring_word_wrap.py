import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from govoffice.services.authoring_word_wrap import (balanced_tracking,needs_character_wrap,
                                                    middle_dot_breaks,visible_text,SOFT_BREAK,
                                                    WORD_WRAP,CHARACTER_WRAP)
from govoffice.services.authoring_cell_budget import line_count
from govoffice.services.document_authoring import render_draft
from govoffice.services.authoring_validation import audit_layout
from test_authoring_font_flow import document, flow_manifest
from test_authoring_output_polish import p, cell, table


class WordWrapTests(unittest.TestCase):
    def test_tracking_can_expand_or_compress_without_stretching_short_text(self):
        self.assertEqual(-2,balanced_tracking('가나다 라마',5.5,0))
        self.assertEqual(0,balanced_tracking('가나다라',5,0))
        self.assertEqual(3,balanced_tracking('가나다라마바 가나다 가나다',9.7,0))
        self.assertEqual(0,balanced_tracking('가',40,0))
        self.assertEqual(-8,balanced_tracking('가나다라',5,-8))
        self.assertEqual(8,balanced_tracking('가나다라',5,8))

    def test_word_packing_counts_unusable_line_ends(self):
        self.assertEqual(3,line_count('가나다 가나다 가나다',5))
        self.assertEqual(2,line_count('가나다 라마',5))
        self.assertEqual(3,line_count('가'*11,5))
        self.assertEqual(2,line_count('가나다\n라마',10))
        self.assertEqual(1,line_count('',10))

    def test_long_symbol_token_can_break_without_changing_ordinary_word_rules(self):
        self.assertTrue(needs_character_wrap('https://example.org/research/project?id=12345',12))
        self.assertFalse(needs_character_wrap('긴 연구 문장을 어절대로 나눕니다.',12))
        root=document(p('1. 제목')+p(controls=table([cell(p('고정 항목'))+cell(p(shape='0'))])))
        m=flow_manifest(root,[3]);value='https://example.org/research/project?id=12345'
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,logs=render_draft(folder,m,{},local_values={'P0003':value})
        out=ET.fromstring(xml);ps=list(out.iter('P'))
        shapes={s.get('Id'):s for s in out.iter('PARASHAPE')}
        generated=ps[logs[0]['output_index']]
        self.assertEqual(value,''.join(generated.itertext()))
        self.assertTrue(all(shapes[generated.get('ParaShape')].get(k)==v for k,v in CHARACTER_WRAP.items()))
        fixed=next(p for p in ps if ''.join(p.itertext())=='고정 항목')
        self.assertEqual('0',fixed.get('ParaShape'))

    def test_middle_dot_group_has_invisible_breaks_at_separator_only(self):
        value='연구·개발·검증·실증'
        marked=middle_dot_breaks(value)
        self.assertEqual('연구·'+SOFT_BREAK+'개발·'+SOFT_BREAK+'검증·'+SOFT_BREAK+'실증',marked)
        self.assertEqual(marked,middle_dot_breaks(marked))
        self.assertEqual(value,visible_text(marked))
        self.assertFalse(needs_character_wrap(marked,5))
        self.assertEqual(4,line_count(value,3))
        root=document(p('1. 제목')+p(controls=table([cell(p('고정·항목'))+cell(p(shape='0'))])))
        m=flow_manifest(root,[3])
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,logs=render_draft(folder,m,{},local_values={'P0003':value})
        out=ET.fromstring(xml);ps=list(out.iter('P'))
        generated=ps[logs[0]['output_index']]
        self.assertEqual(marked,''.join(generated.itertext()))
        self.assertEqual([value],logs[0]['paragraph_values'])
        self.assertEqual([],audit_layout(xml,logs)['issues'])
        style={s.get('Id'):s for s in out.iter('PARASHAPE')}[generated.get('ParaShape')]
        self.assertEqual('KeepWord',style.get('BreakLatinWord'))
        self.assertIn('고정·항목',[ ''.join(p.itertext()) for p in ps ])

    def test_body_and_table_keep_words_without_modifying_text_or_fixed_labels(self):
        root=document(p('1. 제목',shape='3')+p('원래 본문 내용입니다.',shape='1')+
                      p(controls=table([cell(p('고정 항목',shape='3'))+cell(p(shape='0'))])))
        original=ET.tostring(root.find('.//CHARSHAPELIST'))
        m=flow_manifest(root,[1,4]);value='수소핵융합에너지를 검증합니다. international cooperation\n다음 문단 내용입니다.'
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            (folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,logs=render_draft(folder,m,{},local_values={f['id']:value for f in m['topics'][0]['fields']})
        out=ET.fromstring(xml);ps=list(out.iter('P'))
        paras={s.get('Id'):s for s in out.iter('PARASHAPE')}
        chars={s.get('Id'):s for s in out.iter('CHARSHAPE')}
        for log in logs:
            self.assertEqual(value.split('\n'),log['paragraph_values'])
            for i in log['output_indices']:
                self.assertTrue(all(paras[ps[i].get('ParaShape')].get(k)==v for k,v in WORD_WRAP.items()))
                shape=chars[ps[i].find('TEXT').get('CharShape')]
                self.assertEqual('1000' if log['field_id']=='P0004' else '1200',shape.get('Height'))
                self.assertTrue(all(-5<=int(v)<=5 for v in shape.find('CHARSPACING').attrib.values()))
        fixed=next(p for p in ps if ''.join(p.itertext())=='고정 항목')
        self.assertEqual('3',fixed.find('TEXT').get('CharShape'))
        self.assertEqual(original,ET.tostring(root.find('.//CHARSHAPELIST')))

    def test_fixed_table_subheading_stays_with_generated_text(self):
        root=document(p('1. 제목')+p(controls=table([cell(p('o 핵심 기술',shape='3')+p()+p())])))
        m=flow_manifest(root,[4])
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,_=render_draft(folder,m,{},local_values={'P0004':'실제 작성한 본문입니다.'})
        out=ET.fromstring(xml);paras={s.get('Id'):s for s in out.iter('PARASHAPE')}
        ps=next(out.iter('CELL')).findall('PARALIST/P')
        self.assertEqual('3',ps[0].find('TEXT').get('CharShape'))
        self.assertTrue(all(paras[p.get('ParaShape')].get('KeepWithNext')=='true' for p in ps[:2]))


if __name__=='__main__':unittest.main()
