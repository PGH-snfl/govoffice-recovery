import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from govoffice.services.document_authoring import (
    TemplateRegistry, AuthoringService, read_json, write_json,
    make_prompt, render_draft, response_schema, validate_result, own_text,
)
from govoffice.institutions.packages.seoultech.climate_2026.authoring import register_climate
from govoffice.institutions.packages.seoultech.climate_2026.generator import ASSETS


def response(topic, text='확인 필요'):
    return {'topic_id': topic['id'], 'values': {f['id']: ('?' if f.get('kind') == 'schedule_marker' else text) for f in topic['fields']}, 'needs_review': []}


class FakeAgent:
    def __init__(self, fail_on=0, stop=None):
        self.prompts = []
        self.fail_on = fail_on
        self.stop = stop
        self.closed = False

    def generate(self, prompt, schema, cancel):
        self.prompts.append(prompt)
        if len(self.prompts) == self.fail_on:
            raise RuntimeError('모의 연결 실패')
        if self.stop is not None:
            self.stop.set()
        props = schema['properties']
        return {'topic_id': props['topic_id']['enum'][0],
                'values': {k: '작성 테스트' for k in props['values']['properties']}, 'needs_review': []}

    def close(self):
        self.closed = True


def fake_export(template, xml, destination):
    destination.write_bytes(b'fake-test-only-' * 100)
    return {'test_only': True}


class AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.agent = FakeAgent()
        self.service = AuthoringService(self.root, lambda folder: self.agent, fake_export)
        self.addCleanup(self.service.close)
        self.source = self.root/'source.hwpml'
        self.source.write_text('''<HWPML><HEAD><CHARSHAPELIST><CHARSHAPE Id="0" TextColor="0"/><CHARSHAPE Id="1" TextColor="16711680"/></CHARSHAPELIST></HEAD><BODY><SECTION>
<P><TEXT CharShape="0"><CHAR>공통 작성 조건</CHAR><SECDEF><PAGEDEF Width="59528"><PAGEMARGIN Left="5000"/></PAGEDEF></SECDEF></TEXT></P>
<P><TEXT CharShape="0"><CHAR>1-1. 동일 제목</CHAR></TEXT></P>
<P><TEXT CharShape="1"><CHAR>※ 필수 조건: 근거 제시</CHAR></TEXT></P>
<P><TEXT CharShape="0"><CHAR>o</CHAR></TEXT></P>
<P><TEXT CharShape="0"><CHAR>1-1. 동일 제목</CHAR></TEXT></P>
<P><TEXT CharShape="0"><CHAR>-</CHAR></TEXT></P>
<P><TEXT CharShape="0"><TABLE><ROW><CELL><PARALIST>
<P><TEXT CharShape="0"><CHAR>작성 요령</CHAR></TEXT></P>
<P><TEXT CharShape="0"><CHAR>표 안의 요령: 근거를 구체적으로 작성</CHAR></TEXT></P>
</PARALIST></CELL></ROW></TABLE></TEXT></P>
</SECTION></BODY></HWPML>''', encoding='utf-8')
        self.native = self.root/'source.hwp'
        self.native.write_bytes(b'original')
        self.m = self.service.registry.register(self.source, self.native, '시험 양식', shared_guides={1:[(7,8)]})
        self.folder = self.service.registry.path(self.m['id'])

    def create(self):
        return self.service.create(self.m['id'], {'title':'테스트 과제','description':'테스트 목표'}, reviewed=True, external_consent=True)

    def wait(self, job):
        self.service.workers[job['id']].join(timeout=10)
        self.assertFalse(self.service.workers[job['id']].is_alive())
        return self.service.status(job['id'])

    def test_duplicate_topic_titles_have_distinct_bindings_and_md(self):
        a, b = self.m['topics']
        self.assertEqual(a['title'], b['title'])
        self.assertNotEqual(a['id'], b['id'])
        self.assertNotEqual(a['fields'][0]['id'], b['fields'][0]['id'])
        guide = (self.folder/a['guide']).read_text(encoding='utf-8')
        self.assertIn('표 안의 요령: 근거를 구체적으로 작성', guide)
        self.assertIn('필수 조건: 근거 제시', guide)
        self.assertNotIn('필수 조건: 근거 제시', (self.folder/b['guide']).read_text(encoding='utf-8'))

    def test_prompt_has_actual_guide_text_brief_and_previous_content(self):
        prompt = make_prompt(self.folder, self.m, self.m['topics'][0], {'title':'사용자 과제'}, {'earlier':'앞선 목표'})
        for marker in ('사용자 과제','앞선 목표','표 안의 요령: 근거를 구체적으로 작성'):
            self.assertIn(marker, prompt)
        data = json.loads(prompt.split('\n\n',1)[1])
        self.assertNotIn('공통 작성 조건', data['공통작성요령'])
        self.assertIn('필수 조건: 근거 제시', data['소주제작성요령'])
        self.assertNotIn('original', data['입력필드'][0])

    def test_guide_mapping_rejects_paragraphs_outside_tables(self):
        with self.assertRaisesRegex(ValueError, '표 밖'):
            self.service.registry.register(self.source, self.native, '잘못된 연결', guide_overrides={1:[(2,3)]})

    def test_chapter_file_grouping_keeps_separate_subtopic_requests(self):
        m = self.service.registry.register(self.source,self.native,'대주제 시험',group_starts=[(1,'1. 통합 주제')])
        self.assertEqual(2,len(m['topics']))
        self.assertEqual(1,len(m['guide_documents']))
        self.assertEqual(m['topics'][0]['guide'],m['topics'][1]['guide'])
        job = self.service.create(m['id'],{'title':'과제','description':'목표'},reviewed=True,external_consent=True)
        self.service.start(job['id'])
        result = self.wait(job)
        self.assertEqual('completed',result['status'])
        self.assertEqual(2,len(self.agent.prompts))
        self.assertEqual(2,len(result['completed']))
        self.assertIn('필수 조건: 근거 제시',self.agent.prompts[0])
        self.assertNotIn('필수 조건: 근거 제시',self.agent.prompts[1])

    def test_live_ai_response_keeps_prose_and_simplifies_review_marker(self):
        def generated(prompt,schema,cancel):
            return {'topic_id':schema['properties']['topic_id']['enum'][0],
                    'values':{key:'AI가 작성한 연구 본문입니다.\n\n[확인 필요: 기간과 수행기관 검증]\n\n검증 방법을 기술했습니다.'
                              for key in schema['properties']['values']['properties']},'needs_review':[]}
        self.agent.generate=generated
        job=self.create();self.service.start(job['id']);state=self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        response=read_json(self.service.job_path(job['id'])/'responses'/
                           (self.m['topics'][0]['id']+'.json'))
        value=next(iter(response['values'].values()))
        self.assertIn('AI가 작성한 연구 본문입니다.',value)
        self.assertIn('검증 방법을 기술했습니다.',value)
        self.assertIn('[확인 필요]',value)
        self.assertNotIn('기간과 수행기관 검증',value)

    def test_missing_section_marker_stops_instead_of_sending_whole_chapter(self):
        m = self.service.registry.register(self.source,self.native,'구분 시험',group_starts=[(1,'1. 통합 주제')])
        t = m['topics'][0]
        folder = self.service.registry.path(m['id'])
        p = folder/t['guide']
        p.write_text(p.read_text(encoding='utf-8').replace('topic:'+t['id']+':start','missing'),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'소주제 구분'):
            make_prompt(folder,m,t,{}, {})

    def test_guide_and_binding_files_are_separate(self):
        self.assertTrue((self.folder/'입력위치.json').is_file())
        self.assertFalse((self.folder/'전체원문.md').exists())
        for p in (self.folder/'guides').glob('*.md'):
            self.assertNotIn('자동 입력 위치 후보', p.read_text(encoding='utf-8'))

    def test_local_inputs_written_before_ai_and_not_sent_or_overwritten(self):
        local_id = self.m['topics'][0]['fields'][0]['id']
        value = '사용자 직접입력 비공개값'
        job = self.service.create(self.m['id'],{'title':'과제','description':'본문 작성 내용'},
                                  reviewed=True,external_consent=True,local_values={local_id:value})
        generate = self.agent.generate
        def inspect(prompt,schema,cancel):
            p = self.service.job_path(job['id'])/'기본정보_입력완료.hml'
            self.assertTrue(p.exists())
            self.assertIn(value,p.read_text(encoding='utf-8'))
            self.assertNotIn(value,prompt)
            self.assertNotIn(local_id,schema['properties']['values']['properties'])
            return generate(prompt,schema,cancel)
        self.agent.generate = inspect
        self.service.start(job['id'])
        state = self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(1,len(self.agent.prompts))
        log = read_json(self.service.job_path(job['id'])/'입력필드.json')
        self.assertEqual({'field_id':local_id,'value':value,'source':'user'},
                         {k:log[0][k] for k in ('field_id','value','source')})
        self.assertEqual([value],log[0]['paragraph_values'])
        self.assertIn(value,(self.service.job_path(job['id'])/'작성중.hml').read_text(encoding='utf-8'))
        self.assertNotIn('allow_empty',self.service.registry.load(self.m['id'])['topics'][0]['fields'][0])

    def test_local_empty_values_remain_empty_and_all_manual_needs_no_agent(self):
        values = {f['id']:'' for t in self.m['topics'] for f in t['fields']}
        job = self.service.create(self.m['id'],{'title':'과제','description':'본문'},
                                  reviewed=True,external_consent=True,local_values=values)
        self.service.start(job['id'])
        state = self.wait(job)
        self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual([],self.agent.prompts)
        self.assertTrue(all(not x['value'] for x in read_json(self.service.job_path(job['id'])/'입력필드.json')))

    def test_invalid_local_fields_and_lengths_rejected_before_job_created(self):
        key = self.m['topics'][0]['fields'][0]['id']
        for values in ({'P9999':'값'},{key:'x'*10000},{key:123},{key:'x\x00'}):
            with self.subTest(values=str(values)[:40]), self.assertRaises(ValueError):
                self.service.create(self.m['id'],{'title':'과제','description':'본문'},
                                    reviewed=True,external_consent=True,local_values=values)

    def test_resume_keeps_local_inputs_after_ai_failure(self):
        key = self.m['topics'][0]['fields'][0]['id']
        self.agent.fail_on = 1
        job = self.service.create(self.m['id'],{'title':'과제','description':'본문'},
                                  reviewed=True,external_consent=True,local_values={key:'홍길동'})
        self.service.start(job['id'])
        self.assertEqual('failed',self.wait(job)['status'])
        self.agent.fail_on = 0
        self.service.start(job['id'])
        self.assertEqual('completed',self.wait(job)['status'])
        self.assertEqual('홍길동',read_json(self.service.job_path(job['id'])/'입력필드.json')[0]['value'])

    def test_blue_extraction_keeps_only_direct_blue_runs_and_audits_symbols(self):
        from govoffice.services.writing_guides import blue_annotations
        root = ET.fromstring('''<HWPML><CHARSHAPE Id="1" TextColor="16711680"/>
        <P><TEXT><CHAR>일반 본문</CHAR></TEXT><TEXT CharShape="1"><CHAR>※ 조건</CHAR>
        <TABLE><P><TEXT CharShape="1"><CHAR>표 안의 내용</CHAR></TEXT></P></TABLE></TEXT></P>
        <P><TEXT CharShape="1"><CHAR>√</CHAR></TEXT></P></HWPML>''')
        notes, candidates, omitted = blue_annotations(root, list(root.iter('P')), {1})
        self.assertEqual({0:'※ 조건'},notes)
        self.assertEqual({0:'※ 조건',2:'√'},candidates)
        self.assertIn(2,omitted)

    def test_template_digest_and_path_traversal(self):
        with self.assertRaises(ValueError):
            self.service.registry.load('../foo')
        (self.folder/'source.hwpml').write_text('changed', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.service.registry.load(self.m['id'])

    def test_external_consent_and_registration_review_are_required(self):
        for reviewed, consent in ((False, True), (True, False)):
            with self.assertRaises(ValueError):
                self.service.create(self.m['id'], {'title':'과제','description':'목표'}, reviewed=reviewed, external_consent=consent)

    def test_blank_project_information_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create(self.m['id'], {'title':'과제','description':''}, reviewed=True, external_consent=True)

    def test_result_wrong_topic_missing_extra_overlong_and_control_chars_rejected(self):
        topic = self.m['topics'][0]
        key = topic['fields'][0]['id']
        bad = [dict(response(topic), topic_id='other'), dict(response(topic), values={}),
               dict(response(topic), values={key:'x','P9999':'illegal'}), response(topic, 'x'*10000),
               response(topic, 'bad\x00text'), response(topic, '')]
        for value in bad:
            with self.subTest(value=str(value)[:80]), self.assertRaises(ValueError):
                validate_result(topic, value)

    def test_render_changes_only_bound_text_and_retains_page_setup(self):
        topic = self.m['topics'][0]
        xml, fields = render_draft(self.folder, self.m, {topic['id']:response(topic, '<홍길동 & 연구>')})
        before = ET.parse(self.source).getroot()
        after = ET.fromstring(xml)
        self.assertEqual(ET.tostring(before.find('.//PAGEDEF')), ET.tostring(after.find('.//PAGEDEF')))
        self.assertEqual('<홍길동 & 연구>', own_text(list(after.iter('P'))[3]))
        self.assertEqual('-', own_text(list(after.iter('P'))[5]))
        self.assertEqual(self.native.read_bytes(), b'original')

    def test_sequential_execution_saves_prompts_results_and_native(self):
        job = self.create()
        self.service.start(job['id'])
        result = self.wait(job)
        self.assertEqual('completed', result['status'])
        self.assertEqual(2, len(result['completed']))
        self.assertEqual(2, len(self.agent.prompts))
        self.assertIn('작성 테스트', self.agent.prompts[1])
        self.assertFalse(result['submission_ready'])
        self.assertTrue(self.agent.closed)
        self.assertTrue(Path(result['hwp_path']).is_file())

    def test_failure_resume_does_not_rewrite_completed_topic(self):
        self.agent.fail_on = 2
        job = self.create()
        self.service.start(job['id'])
        state = self.wait(job)
        self.assertEqual('failed', state['status'])
        self.assertEqual(1, len(state['completed']))
        saved = next((self.service.job_path(job['id'])/'responses').glob('*.json'))
        before = saved.read_bytes()
        self.agent = FakeAgent()
        self.service.start(job['id'])
        state = self.wait(job)
        self.assertEqual('completed', state['status'])
        self.assertEqual(1, len(self.agent.prompts))
        self.assertEqual(before, saved.read_bytes())

    def test_native_failure_keeps_all_results_without_success_claim(self):
        def fail(*args):
            raise RuntimeError('native failure')
        self.service.exporter = fail
        job = self.create()
        self.service.start(job['id'])
        state = self.wait(job)
        self.assertEqual('failed', state['status'])
        self.assertIsNone(state['hwp_path'])
        self.assertEqual(2, len(state['completed']))
        self.service.exporter = fake_export
        self.service.start(job['id'])
        self.assertEqual('completed', self.wait(job)['status'])
        self.assertEqual(2, len(self.agent.prompts))

    def test_interrupted_process_detected_and_job_snapshot_immutable(self):
        job = self.create()
        path = self.service.job_path(job['id'])
        job['status'] = 'running'
        write_json(path/'state.json', job)
        self.assertEqual('interrupted', self.service.status(job['id'])['status'])
        (self.folder/'guides/common.md').write_text('new rules', encoding='utf-8')
        self.assertNotEqual('new rules', (path/'template/guides/common.md').read_text(encoding='utf-8'))

    def test_cancel_does_not_commit_partial_response(self):
        job = self.create()
        self.service.stops[job['id']] = threading.Event()
        def factory(folder):
            return FakeAgent(stop=self.service.stops[job['id']])
        self.service.agent_factory = factory
        self.service.start(job['id'])
        state = self.wait(job)
        self.assertEqual('paused', state['status'])
        self.assertEqual([], state['completed'])

    def test_two_jobs_use_separate_paths(self):
        a, b = self.create(), self.create()
        self.assertNotEqual(a['output_dir'], b['output_dir'])

    def test_unrecognized_form_is_not_claimed_registered(self):
        self.source.write_text('<HWPML><BODY><SECTION><P/></SECTION></BODY></HWPML>', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, '소주제'):
            self.service.registry.register(self.source, self.native, '미분류')


class ClimateTopicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.registry = TemplateRegistry(Path(cls.temp.name))
        cls.m = register_climate(cls.registry,group_by_chapter=False)
        cls.folder = cls.registry.path(cls.m['id'])

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_table_and_selected_blue_paragraphs_preserved_without_body(self):
        docs = '\n'.join(p.read_text(encoding='utf-8') for p in (self.folder/'guides').glob('*.md'))
        allowed = {i for g in self.m['guide_groups'] for i in g}
        audit = read_json(self.folder/'작성요령_분류.json')
        blue = set(audit['blue_source_paragraphs'])
        for i, p in enumerate(ET.fromstring((ASSETS/'source.hwpml').read_text(encoding='utf-8')).iter('P')):
            if i in allowed and own_text(p).strip():
                self.assertIn(f'<!-- P{i:04d} -->', docs)
                self.assertIn(own_text(p), docs)
            elif i in blue:
                self.assertIn(f'<!-- P{i:04d} -->', docs)
                self.assertIn(audit['blue_candidates'][str(i)],docs)
            elif i not in allowed:
                self.assertNotIn(f'<!-- P{i:04d} -->', docs)
        audit = read_json(self.folder/'작성요령_분류.json')
        self.assertEqual(340,len(audit['table_source_paragraphs']))
        self.assertEqual([],audit['unassigned_paragraphs'])
        self.assertEqual(23,audit['table_count'])
        self.assertEqual(set(audit['blue_candidates']),
                         {str(i) for i in blue} | set(audit['excluded_blue_paragraphs']))
        self.assertGreater(len(blue),100)

    def test_every_binding_is_unique_and_not_a_heading_or_guide_table(self):
        fields = [f for t in self.m['topics'] for f in t['fields']]
        self.assertEqual(len(fields), len({f['id'] for f in fields}))
        guide_ids = {i for g in self.m['guide_groups'] for i in g}
        starts = {t['start'] for t in self.m['topics']}
        self.assertFalse({f['index'] for f in fields} & (guide_ids | starts))
        self.assertEqual(33, len(self.m['topics']))
        self.assertEqual(3074, self.m['nonempty_paragraphs'])

    def test_shared_guides_split_without_other_topics_leaking(self):
        topic = next(t for t in self.m['topics'] if t['start'] == 3676)
        self.assertIn('<!-- P3807 -->', (self.folder/topic['guide']).read_text(encoding='utf-8'))
        expected = {657:([713,714],[717,720]), 667:([717],[713,720]),
                    692:([720,721],[713,717]),3230:([3378,3379],[3382,3383]),
                    3249:([3382,3383],[3378,3379]),3592:([3627,3628],[3630,3631]),
                    3605:([3630,3631],[3627,3628]),3806:([],[3809,3810])}
        for start,(included,excluded) in expected.items():
            t = next(t for t in self.m['topics'] if t['start']==start)
            guide = (self.folder/t['guide']).read_text(encoding='utf-8')
            for i in included:
                self.assertIn(f'<!-- P{i:04d} -->',guide)
            for i in excluded:
                self.assertNotIn(f'<!-- P{i:04d} -->',guide)

    def test_topics_without_table_still_keep_their_blue_conditions(self):
        missing = [t for t in self.m['topics'] if not t['table_guide_paragraphs']]
        self.assertEqual(10,len(missing))
        for t in missing:
            guide=(self.folder/t['guide']).read_text(encoding='utf-8')
            self.assertIn('연결된 작성요령 표 내용이 없습니다.',guide)
            for i in t['blue_note_paragraphs']:
                self.assertIn(f'<!-- P{i:04d} -->',guide)

    def test_blue_conditions_attached_to_correct_topics_and_common_prompt(self):
        expected = {667:[667,669,676],692:[694,699,704],
                    3230:list(range(3231,3233))+list(range(3234,3243)),
                    3249:[3249],3806:[3806,3868,3906,3907]}
        for start, indices in expected.items():
            t = next(t for t in self.m['topics'] if t['start']==start)
            for i in indices:
                self.assertIn(i,t['blue_note_paragraphs'])
        for t in self.m['topics']:
            prompt = make_prompt(self.folder,self.m,t,{}, {})
            self.assertIn('본문 내용은 돋움체 12pt',prompt)
            self.assertIn('<!-- P0652 -->',prompt)
        common = (self.folder/'guides/common.md').read_text(encoding='utf-8')
        self.assertIn('<!-- P1337 -->',common)

    def test_every_builtin_binding_survives_render(self):
        results = {t['id']: response(t, '확인 필요') for t in self.m['topics']}
        xml, fields = render_draft(self.folder, self.m, results)
        ps = list(ET.fromstring(xml).iter('P'))
        for f in fields:
            self.assertEqual(f['value'], own_text(ps[f.get('output_index',int(f['field_id'][1:]))]))
        self.assertFalse([t for t in self.m['topics'] if not t['fields']])

    def test_cleaned_document_has_no_guide_tables_or_known_example_markers(self):
        from govoffice.services.authoring_validation import audit_layout
        results = {t['id']:response(t) for t in self.m['topics']}
        xml, fields = render_draft(self.folder, self.m, results)
        audit = audit_layout(xml, fields)
        self.assertEqual(0,audit['remaining_guide_tables'])
        self.assertEqual([],audit['remaining_examples'])
        self.assertEqual([],audit['issues'])

    def test_section_settings_remain_in_first_output_paragraph(self):
        xml, _ = render_draft(self.folder, self.m, {t['id']:response(t) for t in self.m['topics']})
        root = ET.fromstring(xml)
        original = ET.fromstring((ASSETS/'source.hwpml').read_text(encoding='utf-8'))
        page = root.find('BODY/SECTION/P/TEXT/SECDEF/PAGEDEF')
        self.assertIsNotNone(page)
        self.assertEqual(ET.tostring(original.find('.//PAGEDEF')), ET.tostring(page))


class ClimateChapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.registry = TemplateRegistry(Path(cls.temp.name))
        cls.fine = register_climate(cls.registry,group_by_chapter=False)
        cls.m = register_climate(cls.registry)
        cls.folder = cls.registry.path(cls.m['id'])

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_eight_numbered_chapters_with_separate_front_matter_and_appendix(self):
        self.assertEqual(33,len(self.m['topics']))
        self.assertEqual(12,len(self.m['guide_documents']))
        self.assertEqual('subtopic',self.m['topic_granularity'])
        self.assertEqual('chapter',self.m['guide_file_granularity'])
        chapters = self.m['guide_documents'][3:11]
        self.assertEqual([str(i)+'.' for i in range(1,9)],[t['title'].split()[0] for t in chapters])
        self.assertEqual(33,sum(len(t['topic_ids']) for t in self.m['guide_documents']))
        self.assertEqual(13,len(list((self.folder/'guides').glob('*.md'))))

    def test_fields_order_guidance_and_source_files_unchanged(self):
        self.assertEqual([f for t in self.fine['topics'] for f in t['fields']],
                         [f for t in self.m['topics'] for f in t['fields']])
        self.assertEqual(1698,sum(len(t['fields']) for t in self.m['topics']))
        before = read_json(self.registry.path(self.fine['id'])/'작성요령_분류.json')
        after = read_json(self.folder/'작성요령_분류.json')
        for k in ('source_paragraphs','common_paragraphs','table_source_paragraphs','blue_source_paragraphs'):
            self.assertEqual(before[k],after[k])
        self.assertEqual([],after['unassigned_paragraphs'])
        self.assertEqual(self.fine['source_sha256'],self.m['source_sha256'])
        self.assertEqual(self.fine['native_sha256'],self.m['native_sha256'])

    def test_first_chapter_contains_all_subtopics_but_prompt_selects_only_one(self):
        topic = self.m['topics'][3]
        guide = (self.folder/topic['guide']).read_text(encoding='utf-8')
        for title in ('## 1-1.','## 1-2.','## 1-3.'):
            self.assertIn(title,guide)
        for i in (713,717,720,667,669,694):
            self.assertIn(f'<!-- P{i:04d} -->',guide)
        self.assertNotIn('<!-- P0727 -->',guide)
        prompt = make_prompt(self.folder,self.m,topic,{}, {})
        data = json.loads(prompt.split('\n\n',1)[1])
        self.assertIn('## 1-1.',data['소주제작성요령'])
        self.assertNotIn('## 1-2.',data['소주제작성요령'])
        self.assertNotIn('<!-- P0717 -->',data['소주제작성요령'])

    def test_every_subtopic_preserves_its_full_original_guide_inside_shared_file(self):
        from govoffice.services.document_authoring import topic_guide_text
        for before,after in zip(self.fine['topics'],self.m['topics']):
            self.assertEqual(before['id'],after['id'])
            original = topic_guide_text(self.registry.path(self.fine['id']),before)
            actual = topic_guide_text(self.folder,after)
            original = '\n'.join('#'+line if line.startswith('#') else line for line in original.splitlines()).strip()
            self.assertEqual(original,actual)

    def test_grouped_and_fine_results_render_identical_document(self):
        def render(m):
            return render_draft(self.registry.path(m['id']),m,
                                {t['id']:response(t) for t in m['topics']})
        a, fields_a = render(self.fine)
        b, fields_b = render(self.m)
        self.assertEqual(a,b)
        self.assertEqual(fields_a,fields_b)


if __name__ == '__main__':
    unittest.main()
