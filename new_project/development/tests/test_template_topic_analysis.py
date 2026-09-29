import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock,patch
import xml.etree.ElementTree as ET

from govoffice.services.template_analysis import source_records,register_analyzed,build_manifest,resolve_reviews
from govoffice.services.template_topic_analysis import extract_candidates,analyze_topics,checked_items
from govoffice.services.document_authoring import TemplateRegistry,read_json,render_draft,topic_guide_text,make_prompt
from test_template_analysis import SOURCE,AnalysisAgent
from test_authoring_workflow import SOURCE as MIXED


class TopicAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.cancel=threading.Event();self.agent=AnalysisAgent()
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name);self.registry=TemplateRegistry(self.folder/'templates')

    def analyze(self,source=SOURCE,**kwargs):
        root=ET.fromstring(source);records=source_records(root)
        decisions,audit=analyze_topics(root,records,self.agent,self.cancel,Mock(),**kwargs)
        return records,decisions,audit

    def register(self,source=SOURCE,**kwargs):
        xml=self.folder/'source.hwpml';xml.write_text(source,encoding='utf-8')
        native=self.folder/'source.hwp';native.write_bytes(b'synthetic native placeholder')
        return register_analyzed(self.registry,xml,native,'가상 양식',self.agent,self.cancel,Mock(),**kwargs)

    def test_ai_receives_only_headings_and_original_guides_not_fields(self):
        records,decisions,audit=self.analyze(MIXED)
        self.assertEqual(2,audit['ai_requests'])
        for prompt in self.agent.prompts:
            data=json.loads(prompt.split('\n',1)[1]);self.assertIn(data['mode'],{'headings','guides'})
            self.assertIn('먼저 문구의 의미와 문서상 역할',prompt)
            self.assertIn('보조 단서로만 사용',prompt)
            self.assertNotIn('____',prompt);self.assertNotIn('label_hint',prompt)
            self.assertNotIn('"text":"이름"',prompt)
        self.assertEqual(list(range(len(records))),[r['index'] for r in decisions])
        self.assertEqual(1,sum(r['role']=='personal' for r in decisions))
        self.assertEqual(2,sum(r['role']=='body' for r in decisions))
        self.assertTrue(all(records[i]['text'].strip() for i in audit['candidate_paragraphs']))

    def test_guide_table_nested_in_form_does_not_capture_entire_form(self):
        inner='<TABLE><ROW><CELL><PARALIST><P><TEXT><CHAR>작성 요령</CHAR></TEXT></P><P><TEXT><CHAR>꼭 지킬 조건</CHAR></TEXT></P></PARALIST></CELL></ROW></TABLE>'
        source='<HWPML><BODY><SECTION><P><TEXT><TABLE><ROW><CELL><PARALIST><P><TEXT><CHAR>기관 내부 값</CHAR></TEXT></P><P><TEXT>'+inner+'</TEXT></P></PARALIST></CELL></ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>'
        _,_,audit=self.analyze(source)
        text=json.dumps(audit['guide_blocks'],ensure_ascii=False)
        self.assertIn('꼭 지킬 조건',text);self.assertNotIn('기관 내부 값',text)

    def test_marker_with_delete_after_writing_suffix_is_still_a_guide_table(self):
        source=MIXED.replace('작성 요령','작성 요령(연구개발계획서 작성 후 작성 요령 표는 삭제)')
        _,_,audit=self.analyze(source)
        tables=[b for b in audit['guide_blocks'] if b['kind']=='table']
        self.assertEqual(1,len(tables))
        self.assertIn('공익 목적을 설명',json.dumps(tables,ensure_ascii=False))

    def test_existing_form_retains_all_previously_extracted_guidance(self):
        from govoffice.services.document_authoring import parse_source,own_text
        from govoffice.services.writing_guides import blue_annotations
        path=Path(__file__).resolve().parents[2]/'src/govoffice/institutions/packages/seoultech/climate_2026/source.hwpml'
        root=parse_source(path);ps=list(root.iter('P'));indices={id(p):i for i,p in enumerate(ps)}
        tables=[t for t in root.iter('TABLE') if '작성요령' in ''.join(own_text(p) for p in list(t.iter('P'))[:2]).replace(' ','')]
        table_ids={indices[id(p)] for t in tables for p in t.iter('P')}
        blue,_,_=blue_annotations(root,ps,table_ids)
        expected={i:own_text(ps[i]) for i in table_ids if own_text(ps[i]).strip()}|blue
        _,blocks,_,_=extract_candidates(root,source_records(root))
        actual={p['index']:p['text'] for b in blocks for p in b['paragraphs']}
        self.assertEqual(23,len(tables));self.assertEqual(526,len(expected))
        self.assertEqual(expected,actual)

    def test_inline_long_blue_conditions_preserve_black_heading_and_exact_note(self):
        note='※ 조건을 빠짐없이 지켜야 합니다. '*20
        source=SOURCE.replace('<P><TEXT><CHAR>1. 사업 계획</CHAR></TEXT></P>',
            '<P><TEXT><CHAR>1. 사업 계획</CHAR></TEXT><TEXT CharShape="1"><CHAR>'+note+'</CHAR></TEXT></P>')
        m=self.register(source);folder=self.registry.path(m['id']);audit=read_json(folder/m['analysis_file'])['audit']
        self.assertEqual('1. 사업 계획',audit['headings'][0]['text'])
        raw=json.dumps(m['common_instructions'],ensure_ascii=False);self.assertIn(note.strip(),raw)
        self.assertNotIn(0,m['clear_guide_indices'])
        output,_=render_draft(folder,m,{})
        self.assertIn('1. 사업 계획',output);self.assertIn(note.strip(),output)

    def test_multi_topic_guide_is_available_in_every_linked_topic(self):
        original=self.agent.generate
        def shared(prompt,schema,cancel):
            data=json.loads(prompt.split('\n',1)[1]);result=original(prompt,schema,cancel)
            if data['mode']=='guides':
                for row in result['items']:row.update(scope='topic',topic_anchors=[h['index'] for h in data['headings']])
            return result
        self.agent.generate=shared;m=self.register(MIXED)
        for topic in m['topics']:
            if topic['id']=='sfront':continue
            self.assertIn('공익 목적을 설명',topic_guide_text(self.registry.path(m['id']),topic))

    def test_program_uses_profile_labels_but_never_sends_saved_values(self):
        source=SOURCE.replace('이름','담당부서')
        m=self.register(source,personal_labels={'담당부서'})
        personal=[f for t in m['topics'] for f in t['fields'] if f['role']=='personal']
        self.assertEqual(['담당부서'],[f['label'] for f in personal])
        self.assertNotIn('담당부서',' '.join(self.agent.prompts))

    def test_only_first_blank_cell_paragraph_is_field_and_spacing_is_not(self):
        source=MIXED.replace('<CHAR>이름</CHAR>','<CHAR>이름</CHAR>')
        records,decisions,audit=self.analyze(source)
        blanks=[r['index'] for r in records if r['table']==0 and not r['text'] and r['writable']]
        self.assertEqual(2,len(blanks));self.assertEqual('personal',decisions[blanks[0]]['role'])
        self.assertEqual('preserve',decisions[blanks[1]]['role'])
        occupied=source.replace('<P><TEXT><CHAR/></TEXT></P><P><TEXT><CHAR/></TEXT></P>',
            '<P><TEXT><CHAR/></TEXT></P><P><TEXT><CHAR>기존 내용</CHAR></TEXT></P>')
        _,rows,_=self.analyze(occupied);self.assertEqual('preserve',rows[blanks[0]]['role'])

    def test_unknown_blank_stays_empty_and_is_reported_without_thousands_of_questions(self):
        m=self.register(SOURCE.replace('이름','알 수 없는 칸'))
        self.assertEqual(1,m['unmapped_input_count']);self.assertEqual('partial',m['analysis_status'])
        self.assertFalse(m['analysis_reviews']);self.assertTrue(any('빈칸 1개' in n for n in m['notes']))
        self.assertIn(4,m['blank_indices'])

    def test_no_automatic_retry_and_no_guessing_under_uncertain_heading(self):
        self.agent.generate=Mock(return_value={'items':[]})
        records,decisions,audit=self.analyze()
        self.assertEqual(2,self.agent.generate.call_count)
        self.assertEqual('review',decisions[0]['role']);self.assertEqual('review',decisions[5]['role'])
        self.assertEqual('personal',decisions[4]['role'])
        self.assertEqual(records[1]['text'],decisions[1]['candidate_instruction_text'])
        self.assertTrue(audit['unprocessed_guide_blocks'])

    def test_invalid_guide_destinations_and_duplicate_ids_are_not_accepted(self):
        targets=[{'id':'G0'},{'id':'G1'}]
        good=dict(id='G0',topic_anchors=[10],scope='topic',accepted=True,uncertain=False,reason='',assignments=[])
        bad={**good,'id':'G1','topic_anchors':[999]}
        self.assertEqual({'G0':good},checked_items({'items':[good,bad]},targets,'guides',{10}))
        self.assertEqual({},checked_items({'items':[good,good,bad]},targets,'guides',{10}))

    def test_separate_subtopic_instructions_in_one_table_are_not_broadcast(self):
        original=self.agent.generate
        def split(prompt,schema,cancel):
            data=json.loads(prompt.split('\n',1)[1]);result=original(prompt,schema,cancel)
            if data['mode']=='guides':
                for row,block in zip(result['items'],data['targets']):
                    row.update(scope='topic',topic_anchors=[data['headings'][0]['index']])
                    row['assignments']=[dict(paragraph_indices=[p['index']],topic_anchors=[data['headings'][-1]['index']],scope='topic')
                                        for p in block['paragraphs'] if p['text']=='공익 목적을 설명']
            return result
        self.agent.generate=split;m=self.register(MIXED)
        topics=[t for t in m['topics'] if t['id']!='sfront'];folder=self.registry.path(m['id'])
        self.assertNotIn('공익 목적을 설명',topic_guide_text(folder,topics[0]))
        self.assertIn('공익 목적을 설명',topic_guide_text(folder,topics[-1]))

    def test_headings_cannot_reference_rejected_chapter(self):
        original=self.agent.generate
        def rejected(prompt,schema,cancel):
            data=json.loads(prompt.split('\n',1)[1]);result=original(prompt,schema,cancel)
            if data['mode']=='headings':
                for r in result['items']:r.update(chapter_anchor=0)
            return result
        self.agent.generate=rejected
        records,rows,_=self.analyze(MIXED)
        self.assertFalse(any(r['role']=='heading' for r in rows))
        self.assertFalse(any(r['role']=='body' for r in rows))

    def test_request_limit_and_oversize_preserve_unprocessed_originals(self):
        huge='※ '+('아'*60000)
        source=SOURCE.replace('※ 공개 근거와 실행 절차를 작성',huge)
        records,rows,audit=self.analyze(source)
        self.assertEqual(1,audit['ai_requests']);self.assertTrue(audit['unprocessed_guide_blocks'])
        self.assertEqual(huge,rows[1]['candidate_instruction_text']);self.assertEqual('review',rows[1]['role'])

    def test_time_budget_partial_is_not_user_cancellation_or_false_completion(self):
        with patch('govoffice.services.template_topic_analysis.AI_BUDGET_SECONDS',0):m=self.register()
        self.assertEqual('partial',m['analysis_status']);self.assertEqual(0,m['ai_analysis_requests'])
        self.assertTrue(read_json(self.registry.path(m['id'])/m['analysis_file'])['audit']['deadline_reached'])
        self.cancel.set()
        with self.assertRaises(InterruptedError):self.register()

    def test_transport_failure_does_not_publish_and_review_retains_audit(self):
        self.agent.generate=Mock(side_effect=RuntimeError('접속 오류'))
        with self.assertRaises(RuntimeError):self.register()
        self.assertEqual([],list(self.registry.folder.iterdir()))
        self.agent.generate=Mock(return_value={'items':[]});m=self.register()
        updated=resolve_reviews(self.registry,m['id'],{'0':'preserve'})
        data=read_json(self.registry.path(m['id'])/updated['analysis_file'])
        self.assertIn('audit',data);self.assertEqual('topics_and_guides_only',updated['analysis_mode'])

    def test_guide_only_document_and_empty_document_never_invent_body_targets(self):
        source='<HWPML><BODY><SECTION><P><TEXT><CHAR>____</CHAR></TEXT></P></SECTION></BODY></HWPML>'
        _,rows,audit=self.analyze(source)
        self.assertEqual(0,audit['ai_requests']);self.assertEqual('review',rows[0]['role'])
        m=self.register('<HWPML><BODY><SECTION><P><TEXT><CHAR/></TEXT></P></SECTION></BODY></HWPML>')
        self.assertEqual([],m['topics']);self.assertEqual(0,m['ai_analysis_requests'])


if __name__=='__main__':unittest.main()
