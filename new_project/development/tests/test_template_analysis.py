import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock,patch
import xml.etree.ElementTree as ET

from govoffice.services.template_analysis import source_records,validate_batch,analyze,register_analyzed,resolve_reviews,compact_record,analysis_prompt,partial_batch
from govoffice.services.document_authoring import TemplateRegistry,AuthoringService,read_json,make_prompt,topic_guide_text,render_draft
from govoffice.services.authoring_research import make_research_prompt
from test_document_authoring import FakeAgent,fake_export

SOURCE='''<HWPML><HEAD><CHARSHAPELIST><CHARSHAPE Id="0" TextColor="0"/><CHARSHAPE Id="1" TextColor="16711680"/></CHARSHAPELIST></HEAD><BODY><SECTION>
<P><TEXT><CHAR>1. 사업 계획</CHAR></TEXT></P>
<P><TEXT CharShape="1"><CHAR>※ 공개 근거와 실행 절차를 작성</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW><CELL RowAddr="0" ColAddr="0"><PARALIST><P><TEXT><CHAR>이름</CHAR></TEXT></P></PARALIST></CELL><CELL RowAddr="0" ColAddr="1"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL></ROW></TABLE></TEXT></P>
<P><TEXT><CHAR>____</CHAR></TEXT></P><P><TEXT><CHAR>그대로 유지할 고정 문구</CHAR></TEXT></P>
</SECTION></BODY></HWPML>'''


class AnalysisAgent:
    def __init__(self):self.prompts=[];self.closed=False
    def account(self):return {'connected':True}
    def close(self):self.closed=True
    def generate(self,prompt,schema,cancel):
        self.prompts.append(prompt)
        data=json.JSONDecoder().raw_decode(prompt.split('\n',1)[1])[0]
        if data.get('mode')=='headings':
            return {'items':[dict(index=r['index'],chapter_anchor=r['index'],accepted=r['text'].startswith('1'),uncertain=False,reason='') for r in data['targets']]}
        if data.get('mode')=='guides':
            return {'items':[dict(id=r['id'],topic_anchors=([data['headings'][0]['index']] if data['headings'] else []),
                scope='common',accepted=True,uncertain=False,reason='',assignments=[]) for r in data['targets']]}
        rows=[];anchor=0
        for r in data['분석대상']:
            text=r['text']
            if text.startswith('1'):anchor=r['index']
            role=('preserve' if not r['writable'] else 'heading' if text.startswith('1') else
                  'guide' if text.startswith('※') or text in {'작성 요령','공익 목적을 설명'} else
                  'body' if text=='____' else 'personal' if not text and r['label_hint']=='이름' else 'preserve')
            rows.append(dict(index=r['index'],role=role,topic_anchor=anchor,chapter='사업 개요',topic='사업 계획',
                label='이름' if role=='personal' else '추진 내용',requirements='공개 근거와 실행 절차를 작성',
                guide_ids=[],scope='common' if role=='guide' else 'topic',uncertain=False,reason=''))
        return {'items':rows}


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.xml=self.root/'source.hwpml';self.xml.write_text(SOURCE,encoding='utf-8')
        self.native=self.root/'source.hwp';self.native.write_bytes(b'original sample')
        self.registry=TemplateRegistry(self.root/'templates');self.agent=AnalysisAgent();self.cancel=threading.Event()
    def register(self):return register_analyzed(self.registry,self.xml,self.native,'예제',self.agent,self.cancel,Mock())
    def test_registration_stores_analysis_no_markdown_and_binds_original_guidance(self):
        m=self.register();folder=self.registry.path(m['id'])
        self.assertEqual('ai_analysis',m['guide_mode']);self.assertFalse(list(folder.rglob('*.md')))
        self.assertEqual(self.native.read_bytes(),(folder/'template.hwp').read_bytes())
        self.assertEqual(2,sum(len(t['fields']) for t in m['topics']))
        self.assertIn('※ 공개 근거와 실행 절차',json.dumps(m['common_instructions'],ensure_ascii=False))
        self.assertNotIn('※ 공개 근거와 실행 절차',topic_guide_text(folder,m['topics'][0]))
        self.assertEqual(1,len(m['common_instructions']))
        for prompt in [make_prompt(folder,m,m['topics'][0],{},{}),make_research_prompt(folder,m,m['topics'][0],{},[])]:
            self.assertIn('공개 근거와 실행 절차',prompt)
    def test_real_mapping_missing_personal_never_goes_to_writer(self):
        service=AuthoringService(self.root,lambda p:FakeAgent(),fake_export);self.addCleanup(service.close)
        self.registry=service.registry;m=self.register();agent=FakeAgent();service.agent_factory=lambda p:agent
        job=service.create(m['id'],{'title':'가상 과제','description':'실행 방안'},review_mode='final_output',external_consent=True)
        service.start(job['id']);service.workers[job['id']].join(10);state=service.status(job['id'])
        self.assertEqual('completed',state['status'],state.get('error'))
        personal=next(f for t in m['topics'] for f in t['fields'] if f['role']=='personal')
        self.assertNotIn(personal['id'],' '.join(agent.prompts))
        self.assertTrue(any('저장 정보가 없어' in r for r in state['review']))
        fields=read_json(service.job_path(job['id'])/'입력필드.json')
        self.assertEqual('',next(f for f in fields if f['field_id']==personal['id'])['value'])
        draft=(service.job_path(job['id'])/'작성중.hml').read_text(encoding='utf-8')
        self.assertIn('그대로 유지할 고정 문구',draft)
        self.assertNotIn('※ 공개 근거',draft)
    def test_invalid_analysis_retries_then_preserves_unresolved_text(self):
        agent=Mock();agent.generate.return_value={'items':[]}
        records=source_records(ET.fromstring(SOURCE));rows=analyze(records,agent,self.cancel,Mock())
        self.assertEqual(2,agent.generate.call_count)
        self.assertTrue(all(r['role']==('preserve' if r['index']==2 else 'review') for r in rows))
    def test_duplicate_out_of_range_and_complex_write_are_rejected(self):
        records=source_records(ET.fromstring(SOURCE));result=self.agent.generate('test\n'+json.dumps({'분석대상':records}),{},self.cancel)
        invalid=json.loads(json.dumps(result));invalid['items'][0]['index']=999
        with self.assertRaises(ValueError):validate_batch(invalid,records,records)
        invalid=json.loads(json.dumps(result));invalid['items'][2]['role']='body'
        with self.assertRaises(ValueError):validate_batch(invalid,records,records)
        with self.assertRaises(ValueError):validate_batch({'items':result['items']+[result['items'][0]]},records,records)
    def test_unresolved_user_choice_saved_twice_without_overwriting_prior_analysis(self):
        self.agent.generate=Mock(return_value={'items':[]});m=self.register()
        first=resolve_reviews(self.registry,m['id'],{'0':'preserve'})
        second=resolve_reviews(self.registry,m['id'],{'5':'body'})
        self.assertNotEqual(first['analysis_file'],second['analysis_file'])
        self.assertNotEqual(first['layout_database']['file'],second['layout_database']['file'])
        self.assertTrue((self.registry.path(m['id'])/first['layout_database']['file']).is_file())
        self.assertEqual(second['layout_database'],self.registry.load(m['id'])['layout_database'])
        self.assertNotIn(0,{r['index'] for r in second['analysis_reviews']})
        self.assertTrue(any(f['index']==5 for t in second['topics'] for f in t['fields']))
        with self.assertRaises(ValueError):resolve_reviews(self.registry,m['id'],{'2':'body'})
    def test_cancel_and_transport_failure_publish_no_template(self):
        self.cancel.set()
        with self.assertRaises(InterruptedError):self.register()
        self.assertEqual([],list(self.registry.folder.iterdir()))
        self.cancel.clear();self.agent.generate=Mock(side_effect=RuntimeError('연결 실패'))
        with self.assertRaises(RuntimeError):self.register()
        self.assertEqual([],list(self.registry.folder.iterdir()))
    def test_chunking_covers_every_paragraph(self):
        records=source_records(ET.fromstring('<HWPML><BODY><SECTION>'+''.join('<P><TEXT><CHAR>고정</CHAR></TEXT></P>' for _ in range(145))+'</SECTION></BODY></HWPML>'))
        rows=analyze(records,self.agent,self.cancel,Mock())
        self.assertEqual(3,len(self.agent.prompts));self.assertEqual(list(range(145)),[r['index'] for r in rows])

    def test_nonempty_blank_role_requires_confirmation_and_semantic_retry(self):
        records=source_records(ET.fromstring(SOURCE));original=self.agent.generate
        def ambiguous(*args):
            result=original(*args);result['items'][-1]['role']='blank';return result
        self.agent.generate=ambiguous
        rows=analyze(records,self.agent,self.cancel,Mock())
        self.assertEqual(2,len(self.agent.prompts));self.assertEqual('review',rows[-1]['role'])
        retry=json.loads(self.agent.prompts[-1].split('\n',1)[1])
        self.assertEqual([6],[r['index'] for r in retry['분석대상']])

    def test_request_has_no_repeated_target_text_and_keeps_color_spans(self):
        xml=SOURCE.replace('1. 사업 계획','1. 사업 계획 🔎').replace('<P><TEXT><CHAR>____</CHAR></TEXT></P>',
            '<P><TEXT><CHAR>제목</CHAR></TEXT><TEXT CharShape="1"><CHAR>파란 조건</CHAR><CHAR> 추가 조건</CHAR></TEXT></P>')
        records=source_records(ET.fromstring(xml));compact=[compact_record(r) for r in records]
        self.assertEqual([[0,2,'0'],[2,13,'16711680']],compact[5]['color_spans'])
        self.assertEqual('제목파란 조건 추가 조건',compact[5]['text'])
        for i,r in enumerate(records):
            self.assertEqual(r['text'],compact[i]['text']);self.assertNotIn('runs',compact[i])
        prompt=analysis_prompt(records[1:6],compact,{})
        data=json.loads(prompt.split('\n',1)[1])
        self.assertFalse({r['index'] for r in data['앞뒤문맥']} & {r['index'] for r in data['분석대상']})
        self.assertEqual(1,prompt.count('제목파란 조건 추가 조건'))

    def test_only_empty_controls_are_excluded_not_blank_cells_or_guides(self):
        records=source_records(ET.fromstring(SOURCE.replace('</SECTION>','<P><TEXT><CHAR/></TEXT></P></SECTION>')))
        rows=analyze(records,self.agent,self.cancel,Mock())
        data=json.loads(self.agent.prompts[0].split('\n',1)[1]);ids={r['index'] for r in data['분석대상']}
        self.assertEqual({0,1,3,4,5,6,7},ids)
        self.assertEqual(list(range(8)),[r['index'] for r in rows])
        self.assertEqual('preserve',rows[2]['role'])
        self.assertEqual('personal',rows[4]['role'])
        self.assertEqual('guide',rows[1]['role'])

    def test_valid_rows_survive_partial_invalid_and_failed_retry(self):
        records=source_records(ET.fromstring(SOURCE));original=self.agent.generate
        def damaged(prompt,schema,cancel):
            response=original(prompt,schema,cancel)
            if len(self.agent.prompts)==1:
                # Duplicate ID 5, malformed ID 6, and an unrelated out-of-range row.
                response['items'].append(next(r.copy() for r in response['items'] if r['index']==5))
                next(r for r in response['items'] if r['index']==6)['scope']=[]
                response['items'].append({'index':999,'role':'body'})
                return response
            return {'items':[]}
        self.agent.generate=damaged
        rows=analyze(records,self.agent,self.cancel,Mock())
        retry=json.loads(self.agent.prompts[1].split('\n',1)[1])
        self.assertEqual([5,6],[r['index'] for r in retry['분석대상']])
        self.assertEqual(['heading','guide','preserve','preserve','personal','review','review'],[r['role'] for r in rows])
        self.assertEqual('공개 근거와 실행 절차를 작성',rows[1]['requirements'])

    def test_retry_can_fix_single_item_without_changing_other_decisions(self):
        records=source_records(ET.fromstring(SOURCE));original=self.agent.generate
        def uncertain_first(*args):
            response=original(*args)
            if len(self.agent.prompts)==1:
                next(r for r in response['items'] if r['index']==5).update(uncertain=True,reason='확인 필요')
            return response
        self.agent.generate=uncertain_first;progress=Mock()
        rows=analyze(records,self.agent,self.cancel,progress)
        self.assertEqual('body',rows[5]['role']);self.assertFalse(rows[5]['uncertain'])
        self.assertEqual(1,len(json.loads(self.agent.prompts[-1].split('\n',1)[1])['분석대상']))
        self.assertTrue(any('1개만 재검토' in call.args[0] for call in progress.call_args_list))
        self.assertEqual((7,7),progress.call_args_list[-1].args[1:])

    def test_cancel_after_response_never_starts_retry(self):
        original=self.agent.generate
        def cancel_response(*args):
            result=original(*args);self.cancel.set();return result
        self.agent.generate=cancel_response
        with self.assertRaises(InterruptedError):self.register()
        self.assertEqual(1,len(self.agent.prompts));self.assertEqual([],list(self.registry.folder.iterdir()))

    def test_all_control_document_needs_no_ai_or_empty_topics(self):
        records=source_records(ET.fromstring('<HWPML><BODY><P><TEXT><PICTURE/></TEXT></P></BODY></HWPML>'))
        rows=analyze(records,self.agent,self.cancel,Mock())
        self.assertEqual([],self.agent.prompts);self.assertEqual('preserve',rows[0]['role'])

    def test_long_boundary_context_does_not_truncate_instructions(self):
        records=source_records(ET.fromstring(SOURCE))
        records[1]['text']='※ 작성 조건 '+('긴 요령 '*5000)
        compact=[compact_record(r) for r in records]
        prompt=analysis_prompt([records[5]],compact,{})
        data=json.loads(prompt.split('\n',1)[1])
        self.assertEqual(records[1]['text'],next(r['text'] for r in data['앞뒤문맥'] if r['index']==1))
        self.assertEqual('____',data['분석대상'][0]['text'])
        full=json.loads(analysis_prompt([records[1]],compact,{}).split('\n',1)[1])
        self.assertEqual(records[1]['text'],full['분석대상'][0]['text'])

    def test_mixed_tables_preserve_original_guides_and_all_field_positions(self):
        records=source_records(ET.fromstring(SOURCE.replace('</SECTION>',SOURCE.split('<SECTION>',1)[1].split('</SECTION>',1)[0]+'</SECTION>')))
        baseline=self.agent.generate('baseline\n'+json.dumps({'분석대상':records}),{},self.cancel)['items']
        self.agent.prompts.clear();rows=analyze(records,self.agent,self.cancel,Mock())
        self.assertEqual([r['index'] for r in baseline],[r['index'] for r in rows])
        for role in ('guide','heading','body','personal'):
            self.assertEqual([r['index'] for r in baseline if r['role']==role],[r['index'] for r in rows if r['role']==role])
        targets=json.loads(self.agent.prompts[0].split('\n',1)[1])['분석대상']
        self.assertEqual({0,1},{r['table'] for r in targets if r['table'] is not None})

    def test_compaction_reduces_large_guidance_batch_count(self):
        text='※ 조건과 실행 요령을 빠짐없이 기록합니다. '*35
        records=source_records(ET.fromstring('<HWPML><BODY>'+''.join('<P><TEXT><CHAR>'+text+'</CHAR></TEXT></P>' for _ in range(70))+'</BODY></HWPML>'))
        old_batches=[];batch=[];size=0
        for r in records:
            length=len(json.dumps(r,ensure_ascii=False))
            if batch and (len(batch)>=70 or size+length>35000):old_batches.append(batch);batch=[];size=0
            batch.append(r);size+=length
        if batch:old_batches.append(batch)
        rows=analyze(records,self.agent,self.cancel,Mock())
        old_chars=sum(len(json.dumps({'분석대상':b,'앞뒤문맥':records[max(0,b[0]['index']-8):b[-1]['index']+9]},ensure_ascii=False)) for b in old_batches)
        new_chars=sum(len(p.split('\n',1)[1]) for p in self.agent.prompts)
        self.assertLess(len(self.agent.prompts),len(old_batches))
        self.assertLess(new_chars,old_chars*.6)
        self.assertEqual(70,len(rows));self.assertTrue(all(r['role']=='guide' for r in rows))

    def test_personal_profile_does_not_override_body_role(self):
        from govoffice.services.authoring_commands import AuthoringCommands
        from govoffice.services.authoring_inputs import saved_profile_rows
        m=self.register()
        for t in m['topics']:
            for f in t['fields']:f['label']='이름'
        commands=AuthoringCommands(self.root/'profile');self.addCleanup(commands.close)
        commands.handle({'action':'authoring_profile_save','values':{'이름':'저장된 이름'}})
        rows=saved_profile_rows(m,commands.profile.불러오기())
        personal=[f['id'] for t in m['topics'] for f in t['fields'] if f['role']=='personal']
        self.assertEqual(personal,[fid for r in rows for fid in r['field_ids']])

    def test_analysis_integrity_detects_changes(self):
        m=self.register();folder=self.registry.path(m['id'])
        (folder/m['analysis_file']).write_text('{}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'분석 결과'):self.registry.load(m['id'])


if __name__=='__main__':unittest.main()
