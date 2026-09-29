import copy
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from govoffice.services.numbered_topics import group_numbered,flatten,guide_markdown
from govoffice.services.template_guide_registration import bind_local_slots
from govoffice.services.document_authoring import render_draft,own_text,validate_result
from govoffice.services.authoring_validation import audit_layout


def p(text):return '<P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR>'+text+'</CHAR></TEXT></P>'


class ReadableTests(unittest.TestCase):
    def test_roman_chapter_contains_numeric_middle_topics(self):
        nodes=[{'index':n,'title':t,'instructions':[]} for n,t in enumerate(
            ['Ⅰ. 연구','1. 목표','1-1. 정량 목표','2. 방법','Ⅱ. 결과'])]
        tree=group_numbered(nodes)
        self.assertEqual(['Ⅰ. 연구','Ⅱ. 결과'],[n['title'] for n in tree])
        self.assertEqual(['1. 목표','2. 방법'],[n['title'] for n in tree[0]['subtopics']])

    def test_numbering_preserves_order_and_attaches_rules(self):
        titles=['1. 연구','1-1. 목표','가. 정량 목표','나. 정성 목표','1-2. 방법','2. 결과','2.1. 평가']
        sections=[{'index':n,'title':title,'instructions':[{'index':100+n,'text':title+' 요령'}],'subtopics':[]} for n,title in enumerate(titles)]
        grouped=group_numbered(sections)
        self.assertEqual(['1. 연구','2. 결과'],[x['title'] for x in grouped])
        self.assertEqual(['1-1. 목표','1-2. 방법'],[x['title'] for x in grouped[0]['subtopics']])
        self.assertEqual(['가. 정량 목표','나. 정성 목표'],[x['title'] for x in grouped[0]['subtopics'][0]['subtopics']])
        self.assertEqual(titles,[x['title'] for x in flatten(grouped)])
        md=guide_markdown('시험',grouped)
        self.assertNotIn('<!--',md);self.assertNotIn('AI가',md)
        self.assertIn('#### 가. 정량 목표',md)

    def test_missing_numeric_parent_does_not_invent_source_location(self):
        tree=group_numbered([{'index':10,'title':'2-1. 목표','instructions':[]},
                             {'index':12,'title':'2-2. 방법','instructions':[]}])
        self.assertEqual(1,len(tree));self.assertIsNone(tree[0]['index'])
        self.assertEqual([10,12],[x['index'] for x in tree[0]['subtopics']])

    def test_paragraphs_blue_review_and_inherited_font_spacing(self):
        source=('<HWPML><HEAD><MAPPINGTABLE><CHARSHAPELIST Count="1"><CHARSHAPE Id="0" Height="1100" TextColor="0">'
                '<FONTID Hangul="2"/><CHARSPACING Hangul="-3"/></CHARSHAPE></CHARSHAPELIST>'
                '<PARASHAPELIST Count="1"><PARASHAPE Id="0" Align="Justify"/></PARASHAPELIST></MAPPINGTABLE></HEAD>'
                '<BODY><SECTION>'+p('1. 연구')+p('1-1. 목표')+p('____')+p('1-2. 방법')+p('기존 내용 보존')+'</SECTION></BODY></HWPML>')
        root=ET.fromstring(source)
        outline={'chapters':group_numbered([{'index':i,'title':own_text(list(root.iter('P'))[i]),'instructions':[]}
                                            for i in [0,1,3]]),'unassigned_indices':[]}
        manifest=bind_local_slots(root,outline)
        results={t['id']:{'topic_id':t['id'],'values':{f['id']:'첫 문단\n\n둘째 문단 확인 필요' for f in t['fields']},
                            'needs_review':[]} for t in manifest['topics']}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(source,encoding='utf-8')
            xml,log=render_draft(folder,manifest,results)
        rendered=ET.fromstring(xml);paragraphs=list(rendered.iter('P'))
        self.assertEqual([],audit_layout(xml,log)['issues'])
        self.assertIn('기존 내용 보존',[own_text(x) for x in paragraphs])
        self.assertIn('1-2. 방법',[own_text(x) for x in paragraphs])
        self.assertEqual(2,len(log));self.assertTrue(all(len(f['output_indices'])==2 for f in log))
        shapes={s.get('Id'):s for s in rendered.iter('CHARSHAPE')}
        for field in log:
            for n,index in enumerate(field['output_indices']):
                par=paragraphs[index];shape=shapes[par.find('TEXT').get('CharShape')]
                self.assertEqual('0' if n==0 else '16711680',shape.get('TextColor'))
                self.assertEqual('1100',shape.get('Height'))
                # No page width is specified in this fixture, so keep the
                # inherited spacing instead of guessing a line-fit change.
                self.assertEqual('-3',shape.find('CHARSPACING').get('Hangul'))
                para=next(s for s in rendered.iter('PARASHAPE') if s.get('Id')==par.get('ParaShape'))
                self.assertEqual('Justify',para.get('Align'))
                self.assertEqual('KeepWord',para.get('BreakLatinWord'))
                self.assertEqual('false',para.get('BreakNonLatinWord'))

    def test_legacy_single_paragraph_still_normalizes_newlines(self):
        field={'id':'P0000','max_chars':100}
        topic={'id':'s','fields':[field]};result={'topic_id':'s','values':{'P0000':'a\n\nb'},'needs_review':[]}
        self.assertEqual('a b',validate_result(topic,result)['values']['P0000'])
        field['multiline']=True
        self.assertEqual('a\n\nb',validate_result(topic,result)['values']['P0000'])


if __name__=='__main__':unittest.main()
