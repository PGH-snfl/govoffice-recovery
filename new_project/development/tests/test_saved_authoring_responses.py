from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4
import xml.etree.ElementTree as ET
from govoffice.services.document_authoring import AuthoringService,write_json,read_json,digest,render_draft
from govoffice.services.saved_authoring_responses import export_bundle,prepare_bundle,create_replay
from test_authoring_cell_typography import HEAD,p,table


class SavedResponseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.calls=0;self.exports=0
        outer=self
        class Agent:
            def generate(self,prompt,schema,cancel):
                outer.calls+=1
                return {'topic_id':'s','values':{k:'목표 검증' for k in schema['properties']['values']['properties']},'needs_review':[]}
            def close(self):pass
        def export(template,xml,destination):outer.exports+=1;destination.write_bytes(b'test'*300);return {'test_only':True}
        self.service=AuthoringService(self.root,lambda _:Agent(),export);self.addCleanup(self.service.close)
        tid=uuid4().hex;self.tid=tid;folder=self.service.registry.path(tid);folder.mkdir()
        root=ET.fromstring('<HWPML>'+HEAD+'<BODY><SECTION>'+p('1. 목표')+'<P><TEXT CharShape="0">'+table()+'</TEXT></P></SECTION></BODY></HWPML>')
        for c in root.iter('CELL'):c.set('Height','7000')
        ps=list(root.iter('P'));fields=[]
        for n,index in enumerate(i for i,x in enumerate(ps) if ''.join(x.itertext())=='____'):
            fields.append({'id':f'P{index:04d}','index':index,'original':'____','label':'이름' if n else '목표',
                           'role':'personal' if n else 'body','context':'시험 입력','max_chars':800,'in_table':True,'allow_empty':True,'multiline':True})
        self.personal=fields[1]['id'];self.body=fields[0]['id']
        (folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8');(folder/'template.hwp').write_bytes(b'original')
        manifest={'id':tid,'name':'저장 응답 시험','topics':[{'id':'s','title':'1. 목표','start':0,'fields':fields,'instructions':[]}],
                  'paragraph_count':len(ps),'guide_mode':'ai_analysis','common_instructions':[],'notes':[],
                  'source_sha256':digest(folder/'source.hwpml'),'native_sha256':digest(folder/'template.hwp')}
        write_json(folder/'manifest.json',manifest)
        self.source=self.service.create(tid,{'title':'원래 과제','description':'원래 목표'},review_mode='final_output',external_consent=True,local_values={self.personal:'홍길동'})
        self.service.start(self.source['id']);self.wait(self.source)
        self.packet=self.root/'separate'/'응답.json';export_bundle(self.service,self.source['id'],self.packet)

    def wait(self,state):
        self.service.workers[state['id']].join(10)
        state=self.service.status(state['id']);self.assertEqual('completed',state['status'],state.get('error'));return state

    def forbid_ai(self,*args):raise AssertionError('AI must not be instantiated')

    def test_single_file_preserves_original_responses_attempts_prompts_and_inputs(self):
        data=read_json(self.packet);source=self.service.job_path(self.source['id'])
        self.assertEqual(read_json(source/'responses/s.json'),data['responses']['s'])
        self.assertEqual(read_json(source/'responses/s.attempt1.json'),data['ai_attempts']['s.attempt1.json'])
        self.assertTrue(data['prompts']);self.assertEqual('홍길동',data['local_values'][self.personal])

    def test_replay_uses_same_renderer_exporter_without_creating_agent(self):
        self.service.agent_factory=self.forbid_ai
        packet,info=prepare_bundle(self.service,self.tid,self.packet)
        state=create_replay(self.service,self.tid,self.packet,info['sha256']);self.service.start(state['id']);done=self.wait(state)
        self.assertEqual('saved_response',done['execution_mode']);self.assertFalse(done['external_consent'])
        self.assertEqual(1,self.calls);self.assertEqual(2,self.exports)
        a=self.service.job_path(self.source['id']);b=self.service.job_path(state['id'])
        self.assertEqual((a/'작성중.hml').read_text(encoding='utf-8'),(b/'작성중.hml').read_text(encoding='utf-8'))
        self.assertTrue((b/'저장응답_원본.json').is_file())

    def test_override_values_used_by_content_report_and_document(self):
        self.service.agent_factory=self.forbid_ai
        state=create_replay(self.service,self.tid,self.packet,local_values={self.personal:'김철수'},input_snapshot=[])
        self.service.start(state['id']);self.wait(state);folder=self.service.job_path(state['id'])
        self.assertEqual('김철수',read_json(folder/'responses/s.json')['values'][self.personal])
        self.assertIn('김철수',(folder/'주제별_작성내용.json').read_text(encoding='utf-8'))
        self.assertEqual('홍길동',read_json(self.packet)['local_values'][self.personal])

    def test_mismatch_missing_fields_and_changed_file_fail_before_job_creation(self):
        before=len(list(self.service.jobs.iterdir()));original=read_json(self.packet)
        for mutate in [lambda b:b['template'].update(source_sha256='wrong'),lambda b:b['responses'].pop('s'),
                       lambda b:b['responses']['s']['values'].pop(self.body)]:
            bad=deepcopy(original);mutate(bad);write_json(self.packet,bad)
            with self.assertRaises(ValueError):create_replay(self.service,self.tid,self.packet)
            self.assertEqual(before,len(list(self.service.jobs.iterdir())))
        write_json(self.packet,original);_,info=prepare_bundle(self.service,self.tid,self.packet)
        original['title']='changed';write_json(self.packet,original)
        with self.assertRaisesRegex(ValueError,'변경'):create_replay(self.service,self.tid,self.packet,info['sha256'])

    def test_missing_cached_response_never_falls_back_to_ai(self):
        self.service.agent_factory=self.forbid_ai
        state=create_replay(self.service,self.tid,self.packet)
        (self.service.job_path(state['id'])/'responses/s.json').unlink()
        self.service.start(state['id']);self.service.workers[state['id']].join(10)
        status=self.service.status(state['id']);self.assertEqual('failed',status['status']);self.assertIn('AI를 호출하지',status['error'])

    def test_legacy_oversize_kept_and_reported_not_silently_truncated(self):
        data=read_json(self.packet);long='저장된 설명을 그대로 보존합니다. '*12
        data['responses']['s']['values'][self.body]=long.strip();write_json(self.packet,data)
        self.service.agent_factory=self.forbid_ai;state=create_replay(self.service,self.tid,self.packet)
        self.service.start(state['id']);done=self.wait(state)
        self.assertTrue(any('최종 표 높이' in note for note in done['review']))
        self.assertEqual(long.strip(),read_json(self.service.job_path(state['id'])/'responses/s.json')['values'][self.body])

    def test_duplicate_keys_rejected(self):
        self.packet.write_text('{"format":"govoffice.saved-ai-responses","format":"again","version":1}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'중복'):prepare_bundle(self.service,self.tid,self.packet)

if __name__=='__main__':unittest.main()
