import json
import threading
import unittest
import xml.etree.ElementTree as ET

from govoffice.services.ai_input_slots import (analyze_input_slots,collect_slot_candidates,
                                              reanalyze_saved_input_slots)
from govoffice.services.template_analysis import source_records


SOURCE='''<HWPML><BODY><SECTION>
<P><TEXT><CHAR>1. 연구개발 내용</CHAR></TEXT></P>
<P><TEXT><CHAR>____</CHAR></TEXT></P>
<P><TEXT><CHAR>고정 안내 문구</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW>
<CELL RowAddr="0" ColAddr="0"><PARALIST><P><TEXT><CHAR>담당자 이름</CHAR></TEXT></P></PARALIST></CELL>
<CELL RowAddr="0" ColAddr="1"><PARALIST><P><TEXT><CHAR/></TEXT></P><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>
</ROW></TABLE></TEXT></P>
</SECTION></BODY></HWPML>'''

SAMPLE_TABLE='''<HWPML><BODY><SECTION>
<P><TEXT><CHAR>1. 최종 목표</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW>
<CELL><PARALIST><P><TEXT><CHAR>최종목표</CHAR></TEXT></P></PARALIST></CELL>
<CELL><PARALIST>
<P><TEXT><CHAR>(예) 기존 사업의 목표</CHAR></TEXT></P>
<P><TEXT><CHAR>(예) 기존 사업의 산출물</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW><CELL><PARALIST>
<P><TEXT><CHAR>기준</CHAR></TEXT></P><P><TEXT><CHAR>200건/초</CHAR></TEXT></P>
</PARALIST></CELL></ROW></TABLE></TEXT></P>
</PARALIST></CELL></ROW></TABLE></TEXT></P>
<P><TEXT><CHAR>YYYY. MM. DD - YYYY. MM. DD</CHAR></TEXT></P>
<P><TEXT><CHAR>yy</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW><CELL><PARALIST>
<P><TEXT><CHAR>작성요령</CHAR></TEXT></P>
<P><TEXT><CHAR>(예) 안내 문구</CHAR></TEXT></P>
<P><TEXT><CHAR>(예) 추가 안내</CHAR></TEXT></P>
</PARALIST></CELL></ROW></TABLE></TEXT></P>
</SECTION></BODY></HWPML>'''


class FakeAgent:
    def __init__(self):self.prompts=[]
    def generate(self,prompt,schema,cancel):
        self.prompts.append(prompt)
        data=json.loads(prompt[prompt.rfind('\n')+1:])
        slots=[]
        for candidate in data['slots']:
            role='body' if candidate['text']=='____' else 'personal' if candidate['label_hint']=='담당자 이름' else 'preserve'
            slots.append({'index':candidate['index'],'role':role,'topic_index':0 if role=='body' else -1,
                          'label':candidate['label_hint'],'confidence':'high','reason':'주변 항목명과 문맥으로 확인'})
        return {'slots':slots}


class InputSlotTests(unittest.TestCase):
    def setUp(self):
        self.root=ET.fromstring(SOURCE)
        self.outline={'chapters':[{'index':0,'title':'1. 연구개발 내용','instructions':[],'subtopics':[]}],
                      'unassigned_indices':[]}

    def test_candidates_focus_on_placeholders_and_real_blank_cells(self):
        candidates=collect_slot_candidates(self.root,self.outline)
        self.assertEqual([1,5],[x['index'] for x in candidates])
        self.assertEqual(['담당자 이름'],candidates[1]['table_context']['row_labels'])

    def test_sample_filled_table_and_nested_metric_are_candidates_not_guides(self):
        root=ET.fromstring(SAMPLE_TABLE)
        candidates=collect_slot_candidates(root,self.outline)
        texts={x['text'] for x in candidates}
        self.assertIn('(예) 기존 사업의 목표',texts)
        self.assertIn('200건/초',texts)
        self.assertIn('YYYY. MM. DD - YYYY. MM. DD',texts)
        self.assertIn('yy',texts)
        self.assertNotIn('(예) 안내 문구',texts)
        self.assertNotIn('(예) 추가 안내',texts)

    def test_recheck_analyzes_new_sample_candidates_without_reasking_old(self):
        root=ET.fromstring(SAMPLE_TABLE)
        candidates=collect_slot_candidates(root,self.outline)
        old_index=next(x['index'] for x in candidates if x['text']=='최종목표')
        saved=[{'index':old_index,'role':'preserve','topic_index':-1,'label':'',
                'confidence':'high','reason':'기존 확정'}]
        class NewOnlyAgent:
            def __init__(self):self.sent=[]
            def generate(self,prompt,schema,cancel):
                slots=json.loads(prompt.rsplit('\n',1)[1])['slots']
                self.sent.extend(x['index'] for x in slots)
                return {'slots':[{'index':x['index'],'role':'body' if '(예)' in x['text'] else 'preserve',
                    'topic_index':0 if '(예)' in x['text'] else -1,'label':'최종목표' if '(예)' in x['text'] else '',
                    'confidence':'high','reason':'표 문맥 확인'} for x in slots]}
        agent=NewOnlyAgent()
        result=reanalyze_saved_input_slots(root,self.outline,saved,agent,threading.Event())
        self.assertNotIn(old_index,agent.sent)
        self.assertEqual(len(candidates)-1,len(result['audit']['new_candidate_indices']))
        self.assertEqual(saved[0],next(x for x in result['slots'] if x['index']==old_index))

    def test_ai_classification_is_index_bound_and_audited(self):
        agent=FakeAgent()
        result=analyze_input_slots(self.root,self.outline,agent,threading.Event())
        self.assertEqual(1,result['ai_requests'])
        self.assertEqual(['body','personal'],[x['role'] for x in result['slots']])
        self.assertEqual({'body':1,'personal':1},result['audit']['role_counts'])
        self.assertEqual(2,len(result['slots']))

    def test_out_of_scope_ai_index_fails_closed(self):
        class BadAgent:
            def generate(self,*args):
                return {'slots':[{'index':777,'role':'body','topic_index':0,'label':'x','confidence':'high','reason':'x'}]}
        with self.assertRaises(ValueError):
            analyze_input_slots(self.root,self.outline,BadAgent(),threading.Event())

    def test_only_uncertain_slots_receive_contextual_second_pass(self):
        class RevisingAgent:
            def __init__(self):self.batches=[]
            def generate(self,prompt,schema,cancel):
                data=json.loads(prompt.rsplit('\n',1)[1]);self.batches.append(data['slots'])
                second=len(self.batches)>1
                rows=[]
                for slot in data['slots']:
                    index=slot['index']
                    rows.append({'index':index,'role':'body' if index==1 else 'personal',
                                 'topic_index':0 if index==1 else -1,'label':'본문' if index==1 else '이름',
                                 'confidence':'high' if second or index==5 else 'review',
                                 'reason':'문맥 재확인'})
                return {'slots':rows}
        agent=RevisingAgent()
        result=analyze_input_slots(self.root,self.outline,agent,threading.Event())
        self.assertEqual(2,result['ai_requests'])
        self.assertEqual([1],[slot['index'] for slot in agent.batches[1]])
        self.assertIn('same_container_blank_indices',agent.batches[1][0])
        self.assertEqual(1,result['audit']['second_pass_resolved_count'])
        self.assertEqual([],result['audit']['review_indices'])

    def test_second_pass_uncertainty_preserves_original_review(self):
        class UncertainAgent:
            def generate(self,prompt,schema,cancel):
                slots=json.loads(prompt.rsplit('\n',1)[1])['slots']
                return {'slots':[{'index':x['index'],'role':'preserve','topic_index':-1,
                                  'label':'','confidence':'review','reason':'구별 불가'} for x in slots]}
        result=analyze_input_slots(self.root,self.outline,UncertainAgent(),threading.Event())
        self.assertEqual([1,5],result['audit']['review_indices'])
        self.assertEqual(0,result['audit']['second_pass_resolved_count'])

    def test_saved_decisions_replay_locally_and_only_reviews_call_ai(self):
        saved=[{'index':1,'role':'preserve','topic_index':-1,'label':'',
                'confidence':'review','reason':'기존 불확실'},
               {'index':5,'role':'personal','topic_index':-1,'label':'담당자 이름',
                'confidence':'high','reason':'기존 확정'}]
        class RecheckAgent:
            def __init__(self):self.calls=0
            def generate(self,prompt,schema,cancel):
                self.calls+=1
                slots=json.loads(prompt.rsplit('\n',1)[1])['slots']
                self.assert_review=all('first_pass' in x for x in slots)
                return {'slots':[{'index':x['index'],'role':'body','topic_index':0,
                    'label':'연구 내용','confidence':'high','reason':'재검토 확정'} for x in slots]}
        agent=RecheckAgent()
        result=reanalyze_saved_input_slots(self.root,self.outline,saved,agent,threading.Event())
        self.assertEqual(1,agent.calls)
        self.assertTrue(agent.assert_review)
        self.assertEqual(1,result['ai_requests'])
        self.assertEqual(1,result['audit']['first_pass_replayed_batches'])
        self.assertEqual(saved[1],next(x for x in result['slots'] if x['index']==5))


if __name__=='__main__':unittest.main()
