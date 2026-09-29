import copy
import unittest
import test_document_authoring as fixtures
from test_document_authoring import FakeAgent
from govoffice.services.authoring_research import validate_research, public_source_url
from govoffice.services.document_authoring import read_json, write_json


def evidence(topic_id):
    return {'topic_id':topic_id,'investigation_plan':['공식 연구와 유사 사례 조사'],
            'sources':[{'id':'S1','title':'예제 기술 연구','url':'https://example.org/research',
                        'publisher':'예제 연구기관','published_at':'2026-01-01','facts':['공개 근거 시험']}],
            'findings':[{'text':'공개 연구 결과 시험','source_ids':['S1']}],
            'proposals':[{'text':'검증 실험 단계 제안','basis_source_ids':['S1']}],
            'uncertainties':['실제 사업 예산은 확인 필요']}


class ResearchAgent(FakeAgent):
    def __init__(self):
        super().__init__();self.research_prompts=[];self.last_research_trace=[]

    def research(self,prompt,schema,cancel,on_progress=None):
        self.research_prompts.append(prompt)
        self.last_research_trace=[{'id':'fake-search','query':'public research'}]
        if on_progress:on_progress('공개 자료 검색 중',1)
        return evidence(schema['properties']['topic_id']['enum'][0])


class ResearchTests(unittest.TestCase):
    setUp=fixtures.AuthoringTests.setUp
    wait=fixtures.AuthoringTests.wait

    def job(self,local=None):
        self.agent=ResearchAgent()
        return self.service.create(self.m['id'],{'title':'공공시설 효율화','description':'기술과 사례를 조사하여 실행 방안 제안'},
                                   review_mode='final_output',external_consent=True,research_enabled=True,local_values=local)

    def test_investigation_evidence_reaches_writer_and_is_saved_with_sources(self):
        job=self.job();self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(2,len(self.agent.research_prompts));self.assertEqual(2,len(self.agent.prompts))
        self.assertIn('필수 조건: 근거 제시',self.agent.research_prompts[0])
        self.assertIn('공개 연구 결과 시험',self.agent.prompts[0])
        self.assertIn('검증 실험 단계 제안',self.agent.prompts[0])
        self.assertIn('실제 사업 예산은 확인 필요',state['review'])
        self.assertEqual({'completed_topics':2,'source_count':1,'web_actions':2},state['research_summary'])
        folder=self.service.job_path(job['id'])
        self.assertIn('https://example.org/research',(folder/'자료조사_근거.md').read_text(encoding='utf-8'))
        packet=read_json(folder/'research'/(self.m['topics'][0]['id']+'.json'))
        self.assertEqual('fake-search',packet['web_trace'][0]['id'])
        self.assertFalse(state['submission_ready'])

    def test_resume_reuses_completed_investigation_after_writing_failure(self):
        job=self.job();self.agent.fail_on=1;self.service.start(job['id'])
        self.assertEqual('failed',self.wait(job)['status']);self.assertEqual(1,len(self.agent.research_prompts))
        self.agent.fail_on=0;self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(2,len(self.agent.research_prompts))

    def test_minimal_research_reuses_group_and_keeps_sources_out_of_writer(self):
        path=self.service.registry.path(self.m['id'])/'manifest.json'
        m=read_json(path);m['research_policy']={'mode':'minimal','max_groups':3}
        for t in m['topics']:t['research_group']='one-group'
        write_json(path,m)
        job=self.job();self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(1,len(self.agent.research_prompts))
        self.assertEqual(2,len(self.agent.prompts))
        self.assertNotIn('https://example.org/research',' '.join(self.agent.prompts))
        folder=self.service.job_path(job['id'])
        self.assertIn('https://example.org/research',(folder/'자료출처.json').read_text(encoding='utf-8'))
        for row in read_json(folder/'주제별_작성내용.json'):
            self.assertEqual({'주제','작성내용'},set(row))

    def test_minimal_document_budget_stops_additional_research_not_writing(self):
        path=self.service.registry.path(self.m['id'])/'manifest.json'
        m=read_json(path);m['research_policy']={'mode':'minimal','max_groups':1};write_json(path,m)
        job=self.job();self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(1,len(self.agent.research_prompts));self.assertEqual(2,len(self.agent.prompts))
        self.assertIn('최소 조사 한도',self.agent.prompts[1])

    def test_saved_personal_values_never_enter_research_or_writing(self):
        private='비공개 개인 저장값'
        field=self.m['topics'][0]['fields'][0]['id'];job=self.job({field:private})
        self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(1,len(self.agent.research_prompts))
        self.assertNotIn(private,' '.join(self.agent.research_prompts+self.agent.prompts))

    def test_resume_rebuilds_missing_report_and_summary_from_completed_research(self):
        job=self.job();self.agent.fail_on=1;self.service.start(job['id'])
        state=self.wait(job);self.assertEqual('failed',state['status'])
        folder=self.service.job_path(job['id']);topic=self.m['topics'][0]
        packet=read_json(folder/'research'/(topic['id']+'.json'))
        (folder/'research'/(topic['id']+'.md')).unlink()
        state['research_summary']={};write_json(folder/'state.json',state)
        self.agent.fail_on=0;self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(2,len(self.agent.research_prompts))
        self.assertEqual(2,state['research_summary']['completed_topics'])
        self.assertIn(packet['retrieved_at'],(folder/'research'/(topic['id']+'.md')).read_text(encoding='utf-8'))

    def test_cancel_during_research_never_starts_writing(self):
        job=self.job();research=self.agent.research
        def stop(*args,**kwargs):
            result=research(*args,**kwargs);self.service.stops[job['id']].set();return result
        self.agent.research=stop
        self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('paused',state['status'])
        self.assertEqual([],self.agent.prompts)

    def test_corrupt_cached_research_blocks_resume(self):
        job=self.job();self.agent.fail_on=1;self.service.start(job['id']);self.wait(job)
        path=self.service.job_path(job['id'])/'research'/(self.m['topics'][0]['id']+'.json')
        packet=read_json(path);packet['result']['findings'][0]['source_ids']=['unknown'];write_json(path,packet)
        self.agent.fail_on=0;self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('failed',state['status'])
        self.assertEqual(1,len(self.agent.prompts))

    def test_invented_source_reference_private_url_and_uncited_fact_rejected(self):
        topic=self.m['topics'][0];valid=evidence(topic['id']);self.assertEqual(valid,validate_research(topic,valid))
        bad=copy.deepcopy(valid);bad['findings'][0]['source_ids']=['invented']
        with self.assertRaises(ValueError):validate_research(topic,bad)
        bad=copy.deepcopy(valid);bad['findings'][0]['source_ids']=[]
        with self.assertRaises(ValueError):validate_research(topic,bad)
        for url in ['file:///private','javascript:alert(1)','http://localhost/a','http://127.0.0.1/a','http://10.0.0.1/a']:
            self.assertFalse(public_source_url(url))
            bad=copy.deepcopy(valid);bad['sources'][0]['url']=url
            with self.assertRaises(ValueError):validate_research(topic,bad)

    def test_invalid_research_stops_instead_of_writing_unsupported_claims(self):
        job=self.job()
        self.agent.research=lambda *args,**kwargs:evidence('wrong-topic')
        self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('failed',state['status'])
        self.assertEqual([],self.agent.prompts)


if __name__=='__main__':unittest.main()
