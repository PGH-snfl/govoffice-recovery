import copy
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4
import xml.etree.ElementTree as ET

from govoffice.services.authoring_cell_budget import attach_cell_budgets,CellContentTooLong,line_count,validate_fit_revision
from govoffice.services.document_authoring import validate_result,make_prompt,AuthoringService,read_json,write_json,render_draft,digest
from govoffice.services.authoring_validation import audit_layout
from test_authoring_cell_typography import HEAD,p,cell,table


class CellBudgetTests(unittest.TestCase):
    def fixture(self,width=14000,height=7000,count=1):
        root=ET.fromstring('<HWPML>'+HEAD+'<BODY><SECTION>'+p('1. 추진 목표')+
                          '<P><TEXT CharShape="0">'+table()+'</TEXT></P></SECTION></BODY></HWPML>')
        cells=list(root.iter('CELL'))
        for c in cells:c.set('Width',str(width));c.set('Height',str(height))
        for _ in range(count-1):cells[0].find('PARALIST').append(ET.fromstring(p('____')))
        ps=list(root.iter('P'))
        fields=[{'id':f'P{i:04d}','index':i,'original':'____','label':'추진 목표','context':'추진 목표',
                 'role':'body','max_chars':800,'multiline':True,'in_table':True}
                for i,x in enumerate(ps) if x in list(cells[0].find('PARALIST'))]
        manifest={'topics':[{'id':'s','start':0,'title':'1. 추진 목표','instructions':[],'fields':fields}],
                  'paragraph_count':len(ps),'render_policy':{'readable_body':True,'blue_review':True,'preserve_layout':True},
                  'guide_mode':'tables_and_blue_notes','common_guide':'common.md','notes':[]}
        return root,manifest

    def test_width_height_and_font_change_writing_budget(self):
        budgets=[]
        for width,height,font in [(14000,7000,1100),(28000,7000,1100),(14000,14000,1100),(14000,7000,1600)]:
            root,m=self.fixture(width,height);root.find('.//CHARSHAPE').set('Height',str(font))
            attach_cell_budgets(root,m);budgets.append(m['topics'][0]['fields'][0]['table_fit']['max_body_chars'])
        self.assertGreater(budgets[1],budgets[0]);self.assertGreater(budgets[2],budgets[0]);self.assertLess(budgets[3],budgets[0])

    def test_budget_accounts_for_paragraph_gaps_and_list_indentation(self):
        root,m=self.fixture();attach_cell_budgets(root,m)
        budget=m['topics'][0]['fields'][0]['table_fit']
        self.assertGreater(budget['paragraph_gap'],0)
        self.assertGreaterEqual(line_count('- '+('가'*25),10),line_count('가'*25,10))

    def test_multiple_fields_share_cell_and_fixed_text_uses_space(self):
        root,m=self.fixture();attach_cell_budgets(root,m);single=m['topics'][0]['fields'][0]['table_fit']['max_body_chars']
        root,m=self.fixture(count=2);attach_cell_budgets(root,m)
        self.assertLessEqual(sum(f['table_fit']['max_body_chars'] for f in m['topics'][0]['fields']),single)
        root,m=self.fixture();list(root.iter('CELL'))[0].find('PARALIST').append(ET.fromstring(p('기존 고정 설명')))
        attach_cell_budgets(root,m)
        self.assertLess(m['topics'][0]['fields'][0]['table_fit']['max_body_chars'],single)

    def test_protected_values_and_missing_dimensions_are_not_shortened(self):
        for kind in ['factual_cell','schedule_marker','personal','local','no_dimensions']:
            root,m=self.fixture();f=m['topics'][0]['fields'][0]
            if kind=='personal':f['role']='personal'
            elif kind=='no_dimensions':next(root.iter('CELL')).attrib.pop('Width')
            elif kind not in {'local'}:f['kind']=kind
            attach_cell_budgets(root,m,{f['id']:'긴 사용자 값'} if kind=='local' else {})
            self.assertNotIn('table_fit',f,kind)

    def test_line_and_character_limits_reject_without_truncating(self):
        root,m=self.fixture();attach_cell_budgets(root,m);topic=m['topics'][0];f=topic['fields'][0]
        raw={'topic_id':'s','values':{f['id']:'너무 긴 설명입니다. '*15},'needs_review':[]};before=copy.deepcopy(raw)
        with self.assertRaisesRegex(CellContentTooLong,'요약'):validate_result(topic,raw)
        self.assertEqual(before,raw)
        raw['values'][f['id']]='가\n나\n다\n라\n마\n바'
        with self.assertRaises(CellContentTooLong):validate_result(topic,raw)

    def test_prompt_contains_geometry_and_review_is_not_removed(self):
        root,m=self.fixture();attach_cell_budgets(root,m);t=m['topics'][0];fid=t['fields'][0]['id']
        raw={'topic_id':'s','values':{fid:'목표 검증\n(확인 필요: 참여기관 협의)'},'needs_review':[]}
        self.assertEqual(raw,validate_result(t,raw))
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'common.md').write_text('',encoding='utf-8')
            prompt=make_prompt(folder,m,t,{},{});data=json.loads(prompt.split('\n\n',1)[1])
        self.assertIn('table_fit',data['입력필드'][0]);self.assertIn('반복·배경 설명을 줄이세요',prompt)

    def test_fitting_output_keeps_original_table_size_and_anchor(self):
        root,m=self.fixture();attach_cell_budgets(root,m);f=m['topics'][0]['fields'][0]
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,logs=render_draft(folder,m,{'s':{'topic_id':'s','values':{f['id']:'목표 검증\n(확인 필요: 협의)'},'needs_review':[]}})
        rendered=ET.fromstring(xml);t=next(rendered.iter('TABLE'))
        self.assertEqual('true',t.find('SHAPEOBJECT/POSITION').get('TreatAsChar'))
        self.assertEqual('7000',next(rendered.iter('CELL')).get('Height'))
        self.assertEqual(['목표 검증','(확인 필요: 협의)'],logs[0]['paragraph_values'])

    def test_size_repair_cannot_drop_numbers_review_notes_or_other_values(self):
        topic={'fields':[{'id':'P0001','table_fit':{'max_body_chars':20}},{'id':'P0002','kind':'factual_cell'}]}
        old={'values':{'P0001':'2026년 목표 90% 달성을 검증합니다.\n(확인 필요: 협의)','P0002':'홍길동'},'needs_review':['협약 확인']}
        valid=copy.deepcopy(old);valid['values']['P0001']='2026년 목표 90% 검증\n(확인 필요: 협의)'
        validate_fit_revision(topic,old,valid)
        for fid,value in [('P0001','목표 검증\n(확인 필요: 협의)'),('P0001','2026년 목표 90% 검증'),('P0002','다른 이름')]:
            bad=copy.deepcopy(valid);bad['values'][fid]=value
            with self.assertRaises(ValueError):validate_fit_revision(topic,old,bad)
        bad=copy.deepcopy(valid);bad['needs_review']=[]
        with self.assertRaises(ValueError):validate_fit_revision(topic,old,bad)

    def test_long_mandatory_review_is_preserved_and_height_warning_reported(self):
        root,m=self.fixture(height=3500);attach_cell_budgets(root,m);f=m['topics'][0]['fields'][0]
        note='(확인 필요: '+('필수 협의 내용을 확인하세요. '*8).strip()+')'
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            xml,logs=render_draft(folder,m,{'s':{'topic_id':'s','values':{f['id']:'검증\n'+note},'needs_review':[]}})
        self.assertIn(note,logs[0]['paragraph_values'])
        self.assertIn('table_fit_warning',logs[0])
        self.assertTrue(any('최종 표 높이' in issue for issue in audit_layout(xml,logs)['issues']))

    def test_real_worker_requests_shorter_response_and_preserves_snapshot(self):
        root,m=self.fixture();prompts=[]
        class Agent:
            def generate(self,prompt,schema,cancel):
                prompts.append(prompt)
                return {'topic_id':'s','values':{k:('불필요한 설명을 길게 반복합니다. '*10 if len(prompts)==1 else '목표 검증')
                                                for k in schema['properties']['values']['properties']},'needs_review':[]}
            def close(self):pass
        def exporter(template,xml,destination):destination.write_bytes(b'test'*300);return {}
        with tempfile.TemporaryDirectory() as temp:
            service=AuthoringService(Path(temp),lambda _:Agent(),exporter)
            try:
                template_id=uuid4().hex
                m.update(id=template_id,name='셀 검증',source_sha256='',native_sha256='')
                folder=service.registry.path(template_id);folder.mkdir(parents=True)
                (folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
                (folder/'template.hwp').write_bytes(b'fixture');(folder/'common.md').write_text('',encoding='utf-8')
                m.update(source_sha256=digest(folder/'source.hwpml'),native_sha256=digest(folder/'template.hwp'))
                write_json(folder/'manifest.json',m)
                job=service.create(template_id,{'title':'검증','description':'목표'},reviewed=True,external_consent=True)
                service.start(job['id']);service.workers[job['id']].join(10)
                state=service.status(job['id']);self.assertEqual('completed',state['status'],state.get('error'))
                self.assertEqual(2,len(prompts));self.assertIn('직전 응답을 요약',prompts[1])
                saved=read_json(service.job_path(job['id'])/'responses/s.json')
                self.assertEqual(['목표 검증'],list(saved['values'].values()))
                self.assertNotIn('table_fit',read_json(folder/'manifest.json')['topics'][0]['fields'][0])
            finally:service.close()

if __name__=='__main__':unittest.main()
