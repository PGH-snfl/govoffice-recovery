import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from govoffice.services.authoring_commands import AuthoringCommands
from govoffice.services.document_authoring import read_json, render_draft, write_json
from test_template_analysis import SOURCE
from test_document_authoring import FakeAgent, fake_export
from test_authoring_research import ResearchAgent


class GuideRegistrationAgent:
    def __init__(self):self.prompts=[];self.closed=False
    def account(self):return {'connected':True}
    def close(self):self.closed=True
    def generate(self,prompt,schema,cancel):
        properties=set(schema['properties'])
        if properties=={'slots'}:
            data=json.loads(prompt.rsplit('\n',1)[1]);slots=[]
            for candidate in data['slots']:
                role='personal' if candidate['label_hint']=='이름' else 'body'
                slots.append({'index':candidate['index'],'role':role,
                    'topic_index':-1 if role=='personal' else 0,
                    'label':candidate['label_hint'] or '연구 내용',
                    'confidence':'high','reason':'검증 양식의 항목명과 입력 표시'})
            return {'slots':slots}
        # Research/writing must still wait for the user to supply a brief.
        assert properties=={'topics','unattached_instruction_indices'}
        self.prompts.append(prompt)
        data=json.loads(prompt.split('\n',1)[1]);topics=[];unattached=[]
        for row in data['paragraphs']:
            if row['text'].startswith('1.'):
                topics.append({'heading_index':row['index'],'instruction_indices':[]})
            elif row['text'].startswith('※'):
                if topics:topics[-1]['instruction_indices'].append(row['index'])
                else:unattached.append(row['index'])
        return {'topics':topics,'unattached_instruction_indices':unattached}


class BodyRestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.commands=AuthoringCommands(self.root/'data');self.addCleanup(self.commands.close)
        self.source=self.root/'form.hwp';self.source.write_bytes(b'original fixture')
        self.agent=GuideRegistrationAgent()
        self.commands.service.agent_factory=lambda folder:self.agent

    def wait(self, result):
        for _ in range(300):
            op=self.commands.handle({'action':'authoring_operation','operation_id':result['operation_id']})
            if op['status']!='running':return op
            time.sleep(.01)
        self.fail('operation timeout')

    def register(self, action='authoring_register_file', **kwargs):
        def extract(source,dest):dest.write_text(SOURCE,encoding='utf-8')
        with patch('govoffice.services.authoring_commands.extract_hwp',side_effect=extract):
            op=self.wait(self.commands.handle({'action':action,'path':str(self.source),**kwargs}))
        self.assertEqual('completed',op['status'],op.get('error'))
        return op['result']

    def test_registration_writes_body_and_exports_without_replacing_guide_flow(self):
        m=self.register()
        self.assertEqual('ai_guides_local_slots',m['analysis_mode'])
        fields=[f for t in m['topics'] for f in t['fields']]
        self.assertTrue(any(f['role']=='body' for f in fields))
        self.assertTrue(any(f['role']=='personal' for f in fields))
        self.assertTrue(Path(m['guide_file']).is_file())
        self.assertIn('※ 공개 근거와 실행 절차를 작성',Path(m['guide_file']).read_text(encoding='utf-8'))
        writer=ResearchAgent();self.commands.service.agent_factory=lambda folder:writer
        self.commands.service.exporter=fake_export
        job=self.commands.handle({'action':'authoring_create','template_id':m['id'],
            'brief':{'title':'검증 주제','description':'본문 작성 검증'},'review_mode':'final_output',
            'external_consent':True,'research_enabled':True})
        self.commands.service.workers[job['id']].join(10)
        status=self.commands.service.status(job['id'])
        self.assertEqual('completed',status['status'],status.get('error'))
        self.assertTrue(writer.prompts,'No body writing request was sent')
        self.assertTrue(writer.research_prompts,'No research request was sent')
        self.assertIn('검증 주제',writer.research_prompts[0])
        self.assertIn('본문 작성 검증',writer.research_prompts[0])
        self.assertIn('공개 근거와 실행 절차',writer.research_prompts[0])
        self.assertIn('공개 연구 결과 시험',writer.prompts[0])
        self.assertIn('공개 근거와 실행 절차',' '.join(writer.prompts))
        draft=(self.commands.service.job_path(job['id'])/'작성중.hml').read_text(encoding='utf-8')
        self.assertIn('작성 테스트',draft)
        self.assertIn('그대로 유지할 고정 문구',draft)
        self.assertTrue(Path(status['hwp_path']).is_file())

    def test_reconnect_skips_when_no_uncertain_slots_and_preserves_original(self):
        old=self.register();folder=self.commands.service.registry.path(old['id'])
        before=(folder/'manifest.json').read_bytes()
        new=self.register('authoring_reanalyze_template',template_id=old['id'])
        self.assertEqual(old['id'],new['id'])
        self.assertTrue(new['recheck_no_change'])
        self.assertEqual(0,new['recheck_ai_requests'])
        self.assertEqual(before,(folder/'manifest.json').read_bytes())
        self.assertEqual(b'original fixture',(folder/'template.hwp').read_bytes())

    def test_uncertain_slot_can_be_confirmed_without_reanalyzing_or_changing_original(self):
        base=self.agent
        class ReviewAgent:
            def __init__(self):self.slot_calls=0
            def account(self):return {'connected':True}
            def close(self):pass
            def generate(self,prompt,schema,cancel):
                if set(schema['properties'])!={'slots'}:
                    return base.generate(prompt,schema,cancel)
                self.slot_calls+=1
                candidates=json.loads(prompt.rsplit('\n',1)[1])['slots']
                return {'slots':[{'index':x['index'],
                    'role':'body' if x['text']=='____' else 'preserve',
                    'topic_index':0 if x['text']=='____' else -1,
                    'label':x['label_hint'] or '본문',
                    'confidence':'high' if x['text']=='____' else 'review',
                    'reason':'개인 정보칸인지 추가 확인'} for x in candidates]}
        agent=ReviewAgent();self.commands.service.agent_factory=lambda folder:agent
        old=self.register();old_folder=self.commands.service.registry.path(old['id'])
        before=(old_folder/'manifest.json').read_bytes()
        reviews=old['analysis_reviews']
        self.assertEqual(1,len(reviews))
        self.assertEqual(2,agent.slot_calls)
        overview=self.commands.handle({'action':'authoring_overview'})
        self.assertEqual(1,len(next(x for x in overview['templates'] if x['id']==old['id'])['analysis_reviews']))
        updated=self.commands.handle({'action':'authoring_analysis_resolve',
            'template_id':old['id'],'choices':{str(reviews[0]['index']):'personal'}})
        self.assertNotEqual(old['id'],updated['id'])
        self.assertEqual(old['id'],updated['derived_from_template_id'])
        self.assertEqual(before,(old_folder/'manifest.json').read_bytes())
        self.assertEqual(0,len(updated['analysis_reviews']))
        self.assertTrue(any(f['role']=='personal' and f['index']==reviews[0]['index']
                            for t in updated['topics'] for f in t['fields']))
        self.assertEqual(2,agent.slot_calls,'User confirmation must not call AI again')
        self.commands.service.registry.load(updated['id'])
        class RecheckAgent:
            def __init__(self):self.calls=0
            def account(self):return {'connected':True}
            def close(self):pass
            def generate(self,prompt,schema,cancel):
                self.calls+=1
                assert set(schema['properties'])=={'slots'}
                candidates=json.loads(prompt.rsplit('\n',1)[1])['slots']
                assert all('first_pass' in x for x in candidates)
                return {'slots':[{'index':x['index'],'role':'personal','topic_index':-1,
                    'label':'이름','confidence':'high','reason':'재검토로 확정'} for x in candidates]}
        rechecker=RecheckAgent();self.commands.service.agent_factory=lambda folder:rechecker
        op=self.wait(self.commands.handle({'action':'authoring_reanalyze_template','template_id':old['id']}))
        self.assertEqual('completed',op['status'],op.get('error'))
        self.assertEqual(1,rechecker.calls,'Confirmed first-pass slots must be replayed locally')
        self.assertEqual(1,op['result']['recheck_resolved_count'])
        self.assertNotEqual(old['id'],op['result']['id'])
        self.assertEqual([],op['result']['analysis_reviews'])
        self.assertEqual(before,(old_folder/'manifest.json').read_bytes())

    def test_front_budget_fact_is_saved_but_left_blank_without_evidence(self):
        budget='''<P><TEXT><TABLE><ROW><CELL RowAddr="0" ColAddr="0"><PARALIST><P><TEXT><CHAR>연구개발비 예산</CHAR></TEXT></P></PARALIST></CELL><CELL RowAddr="0" ColAddr="1"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL></ROW></TABLE></TEXT></P>'''
        source=SOURCE.replace('<P><TEXT><CHAR>1. 사업 계획</CHAR></TEXT></P>',
                              budget+'<P><TEXT><CHAR>1. 사업 계획</CHAR></TEXT></P>')
        base=self.agent
        class BudgetAgent:
            def account(self):return {'connected':True}
            def close(self):pass
            def generate(self,prompt,schema,cancel):
                if set(schema['properties'])!={'slots'}:
                    return base.generate(prompt,schema,cancel)
                data=json.loads(prompt.rsplit('\n',1)[1]);heading=data['title_topics'][0]['index']
                return {'slots':[{'index':x['index'],
                    'role':'factual' if '예산' in x['label_hint'] else 'body' if x['text']=='____' else 'personal',
                    'topic_index':-1 if '예산' in x['label_hint'] or x['text']!='____' else heading,
                    'label':x['label_hint'] or '본문','confidence':'high','reason':'양식 항목명'}
                    for x in data['slots']]}
        self.commands.service.agent_factory=lambda folder:BudgetAgent()
        with patch('govoffice.services.authoring_commands.extract_hwp',side_effect=lambda s,d:d.write_text(source,encoding='utf-8')):
            op=self.wait(self.commands.handle({'action':'authoring_register_file','path':str(self.source)}))
        self.assertEqual('completed',op['status'],op.get('error'))
        manifest=op['result'];folder=self.commands.service.registry.path(manifest['id'])
        factual=[f for t in manifest['topics'] for f in t['fields'] if f['role']=='factual']
        self.assertEqual(1,len(factual))
        self.assertEqual('factual_cell',factual[0]['kind'])
        self.assertTrue(factual[0]['allow_empty'])
        xml,_=render_draft(folder,manifest,{})
        self.assertNotIn(factual[0]['slot_marker'],xml)
        self.assertIn('연구개발비 예산',xml)
        writer=FakeAgent();self.commands.service.agent_factory=lambda folder:writer
        self.commands.service.exporter=fake_export
        job=self.commands.handle({'action':'authoring_create','template_id':manifest['id'],
            'brief':{'title':'예산 검증','description':'금액은 제공되지 않음'},
            'review_mode':'final_output','external_consent':True,'research_enabled':False})
        self.commands.service.workers[job['id']].join(10)
        status=self.commands.service.status(job['id'])
        self.assertEqual('completed',status['status'],status.get('error'))
        self.assertTrue(writer.prompts)
        self.assertTrue(all(factual[0]['id'] not in
            [field['id'] for field in json.loads(prompt.rsplit('\n\n',1)[1])['입력필드']]
            for prompt in writer.prompts))
        draft=(self.commands.service.job_path(job['id'])/'작성중.hml').read_text(encoding='utf-8')
        self.assertNotIn(factual[0]['slot_marker'],draft)

    def test_personal_only_template_cannot_fake_body_completion(self):
        m=self.register();folder=self.commands.service.registry.path(m['id'])
        for topic in m['topics']:
            topic['fields']=[f for f in topic['fields'] if f['role']=='personal']
        from govoffice.services.template_layout_store import save_layout_database
        from govoffice.services.document_authoring import parse_source
        save_layout_database(folder,parse_source(folder/'source.hwpml'),m)
        write_json(folder/'manifest.json',m)
        with self.assertRaisesRegex(ValueError,'본문 작성 위치'):
            self.commands.service.create(m['id'],{'title':'주제','description':'본문'},
                                         review_mode='final_output',external_consent=True)
        self.assertEqual([],list(self.commands.service.jobs.glob('*/state.json')))

    def test_missing_body_slot_gets_a_new_paragraph_not_replacement_of_fixed_text(self):
        source=SOURCE.replace('____','고정된 내용')
        with patch('govoffice.services.authoring_commands.extract_hwp',side_effect=lambda s,d:d.write_text(source,encoding='utf-8')):
            op=self.wait(self.commands.handle({'action':'authoring_register_file','path':str(self.source)}))
        self.assertEqual('completed',op['status'],op.get('error'))
        fields=[f for t in op['result']['topics'] for f in t['fields'] if f['role']=='body']
        self.assertTrue(fields)
        self.assertTrue(all(f.get('insert_after') for f in fields))
        self.assertNotIn('고정된 내용',[f['original'] for f in fields])

    def test_body_inside_table_is_not_lost_to_personal_only_mapping(self):
        source=SOURCE.replace('<P><TEXT><CHAR>____</CHAR></TEXT></P>',
            '<P><TEXT><TABLE><ROW><CELL><PARALIST><P><TEXT><CHAR>____</CHAR></TEXT></P></PARALIST></CELL></ROW></TABLE></TEXT></P>')
        with patch('govoffice.services.authoring_commands.extract_hwp',side_effect=lambda s,d:d.write_text(source,encoding='utf-8')):
            op=self.wait(self.commands.handle({'action':'authoring_register_file','path':str(self.source)}))
        self.assertEqual('completed',op['status'],op.get('error'))
        self.assertTrue(any(f['role']=='body' and f['in_table'] for t in op['result']['topics'] for f in t['fields']))

    def test_old_personal_only_job_cannot_resume_into_false_completion(self):
        m=self.register()
        job=self.commands.service.create(m['id'],{'title':'주제','description':'본문'},
                                         review_mode='final_output',external_consent=True)
        folder=self.commands.service.job_path(job['id'])
        saved=read_json(folder/'template/manifest.json')
        for topic in saved['topics']:
            topic['fields']=[f for f in topic['fields'] if f['role']=='personal']
        write_json(folder/'template/manifest.json',saved)
        self.commands.service.start(job['id']);self.commands.service.workers[job['id']].join(5)
        state=self.commands.service.status(job['id'])
        self.assertEqual('failed',state['status'])
        self.assertIn('본문 작성 위치',state['error'])
        self.assertFalse(state.get('hwp_path'))


if __name__=='__main__':unittest.main()
