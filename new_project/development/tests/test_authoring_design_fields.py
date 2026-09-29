import unittest
import xml.etree.ElementTree as ET
import tempfile
from pathlib import Path
from govoffice.services.authoring_design_fields import remove_decorative_fields, safe_writing_manifest, title_strip_tables
from govoffice.services.saved_authoring_responses import collapse_review_values
from govoffice.services.document_authoring import render_draft, own_text
from govoffice.services.authoring_cell_budget import attach_cell_budgets
from govoffice.services.saved_authoring_responses import binding_hash


def p(text=''):
    return '<P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR>'+text+'</CHAR></TEXT></P>'


def cell(width,text):
    return f'<CELL Width="{width}" Height="1800"><PARALIST>'+p(text)+'</PARALIST></CELL>'


def banner():
    return ET.fromstring('<HWPML><HEAD/><BODY><SECTION><P><TEXT><TABLE><ROW>'+
        cell(3000,'2')+cell(500,'')+cell(40000,'연구개발 목표 및 내용')+
        '</ROW></TABLE></TEXT></P>'+p('본문 자리')+'</SECTION></BODY></HWPML>')


def manifest_for(root,index,label,insert=True):
    return {'paragraph_count':len(list(root.iter('P'))),'topics':[{'id':'s','title':label,'start':index,
        'fields':[{'id':f'P{index:04d}','index':index,'label':label,'original':own_text(list(root.iter('P'))[index]),
            'insert_after':insert,'role':'body','in_table':True,'max_chars':3000,'multiline':True}]}],
        'render_policy':{'readable_body':True,'preserve_layout':True,'review_memos':True}}


def render(root,manifest,value='AI가 작성한 본문입니다.'):
    field=manifest['topics'][0]['fields'][0]
    with tempfile.TemporaryDirectory() as temp:
        folder=Path(temp)/'template';folder.mkdir()
        (folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf8')
        xml,log=render_draft(folder,manifest,{'s':{'topic_id':'s','values':{field['id']:value},'needs_review':[]}})
    return ET.fromstring(xml),log


class DesignFieldTests(unittest.TestCase):
    def test_entire_numbered_banner_is_preserved_and_body_goes_outside(self):
        root=banner();manifest=manifest_for(root,3,'연구개발 목표 및 내용')
        before=ET.tostring(root.find('.//TABLE'))
        output,log=render(root,manifest)
        self.assertEqual(before,ET.tostring(output.find('.//TABLE')))
        self.assertEqual('AI가 작성한 본문입니다.',own_text(output.find('BODY/SECTION')[1]))
        self.assertEqual('P0003',log[0]['field_id'])
        self.assertEqual(0,log[0]['input_index'])

    def test_badge_separator_replay_is_blocked(self):
        root=banner();manifest=manifest_for(root,2,'2',insert=False)
        output,log=render(root,manifest)
        self.assertEqual([],log)
        self.assertNotIn('AI가 작성한',ET.tostring(output,encoding='unicode'))

    def test_fixed_label_routes_to_content_cell_even_if_guide_is_cleared(self):
        root=ET.fromstring('<HWPML><HEAD/><BODY><SECTION><P><TEXT><TABLE><ROW>'+
            cell(4000,'최종목표')+cell(40000,'작성예시')+'</ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>')
        manifest=manifest_for(root,1,'최종목표');manifest['clear_guide_indices']=[2]
        output,log=render(root,manifest)
        cells=output.findall('.//ROW/CELL')
        self.assertEqual(['최종목표'],[own_text(p) for p in cells[0].iter('P')])
        self.assertIn('AI가 작성한 본문입니다.',[own_text(p) for p in cells[1].iter('P')])
        self.assertEqual(2,log[0]['input_index'])

    def test_real_single_cell_body_and_numeric_data_row_are_not_design(self):
        root=ET.fromstring('<HWPML><HEAD/><BODY><SECTION><P><TEXT><TABLE><ROW>'+
            cell(40000,'')+'</ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>')
        manifest=manifest_for(root,1,'작성 내용',insert=False)
        self.assertEqual([],title_strip_tables(root))
        output,_=render(root,manifest)
        self.assertIn('AI가 작성한 본문입니다.',[own_text(p) for p in output.find('.//TABLE').iter('P')])
        data=ET.fromstring('<HWPML><TABLE><ROW>'+cell(3000,'1')+cell(30000,'')+'</ROW></TABLE></HWPML>')
        self.assertEqual([],title_strip_tables(data))

    def test_new_registration_keeps_body_binding_but_not_design_destination(self):
        root=banner();manifest=manifest_for(root,3,'연구개발 목표 및 내용')
        self.assertEqual([],remove_decorative_fields(root,manifest))
        self.assertEqual('design',manifest['table_roles'][0]['role'])
        self.assertEqual(0,manifest['topics'][0]['fields'][0]['write_target']['index'])

    def test_budgets_use_safe_target_without_changing_response_identity(self):
        root=banner();manifest=manifest_for(root,3,'연구개발 목표 및 내용')
        fingerprint=binding_hash(manifest)
        attach_cell_budgets(root,manifest)
        field=manifest['topics'][0]['fields'][0]
        self.assertNotIn('table_fit',field)
        self.assertFalse(field['write_target']['in_table'])
        self.assertEqual(fingerprint,binding_hash(manifest))
        # Incoming metadata cannot bypass the source-based protection.
        field['write_target']={'index':3}
        safe=safe_writing_manifest(root,manifest)
        self.assertEqual(0,safe['topics'][0]['fields'][0]['index'])

    def test_narrow_number_badge_is_not_a_writing_field(self):
        root=ET.fromstring('<HWPML><BODY><SECTION><P><TEXT><TABLE><ROW>'
            '<CELL Width="565"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>'
            '<CELL Width="9000"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>'
            '</ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>')
        manifest={'topics':[{'title':'시험','fields':[
            {'id':'P0001','index':1,'label':'2'},{'id':'P0002','index':2,'label':'내용'}]}],'notes':[]}
        removed=remove_decorative_fields(root,manifest)
        self.assertEqual(['P0001'],[f['id'] for f in removed])
        self.assertEqual(['P0002'],[f['id'] for f in manifest['topics'][0]['fields']])
        self.assertEqual('mixed',manifest['table_roles'][0]['role'])

    def test_wide_numeric_value_cell_is_kept(self):
        root=ET.fromstring('<HWPML><BODY><SECTION><P><TEXT><TABLE><ROW>'
            '<CELL Width="5000"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>'
            '</ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>')
        manifest={'topics':[{'title':'시험','fields':[{'id':'P0001','index':1,'label':'1'}]}],'notes':[]}
        self.assertEqual([],remove_decorative_fields(root,manifest))
        self.assertEqual('input',manifest['table_roles'][0]['role'])

    def test_review_field_keeps_prose_and_marks_fact(self):
        bundle={'responses':{'s':{'values':{'P0001':'정상 본문','P0002':'설명\n[확인 필요: 금액]\n임시 내용',
                                                   'P0003':'임시 값'},
                                  'needs_review':['P0003: 근거 확인 필요']}}}
        root=ET.fromstring('<HWPML><BODY><SECTION><P><TEXT><CHAR/></TEXT></P>'
                           '<P><TEXT><CHAR/></TEXT></P><P><TEXT><CHAR/></TEXT></P>'
                           '</SECTION></BODY></HWPML>')
        manifest={'topics':[{'id':'s','fields':[
            {'id':'P0001','index':0,'label':'본문','role':'body','in_table':False},
            {'id':'P0002','index':1,'label':'작성 내용','role':'body','in_table':False},
            {'id':'P0003','index':2,'label':'시장 규모','role':'body','in_table':True}]}]}
        changed=collapse_review_values(bundle,manifest,root)
        self.assertEqual('정상 본문',bundle['responses']['s']['values']['P0001'])
        self.assertIn('임시 내용',bundle['responses']['s']['values']['P0002'])
        self.assertIn('[확인 필요]',bundle['responses']['s']['values']['P0002'])
        self.assertEqual('확인 필요',bundle['responses']['s']['values']['P0003'])
        self.assertEqual([],bundle['responses']['s']['needs_review'])
        self.assertEqual(2,len(changed))
