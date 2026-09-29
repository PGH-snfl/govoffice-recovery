import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from copy import deepcopy

from govoffice.services.authoring_review_memos import build_memo, memo_body, original_packets
from govoffice.services.document_authoring import render_draft
from govoffice.adapters.hwp_review_memos import compose_memos, verify_memos, body_paragraphs, memo_fields, paragraph_text


def source():
    return ET.fromstring('''<HWPML><HEAD><MAPPINGTABLE>
    <CHARSHAPELIST Count="1"><CHARSHAPE Id="0" Height="1100" TextColor="0"/></CHARSHAPELIST>
    <PARASHAPELIST Count="1"><PARASHAPE Id="0" Align="Justify"/></PARASHAPELIST>
    <STYLELIST><STYLE Id="0" EngName="Memo" CharShape="0" ParaShape="0"/></STYLELIST>
    </MAPPINGTABLE></HEAD><BODY><SECTION>
    <P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR>본문 문장</CHAR></TEXT></P>
    <P ParaShape="0" Style="0"><TEXT CharShape="0"><TABLE><ROW><CELL><PARALIST>
    <P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR/></TEXT></P>
    </PARALIST></CELL></ROW></TABLE></TEXT></P>
    </SECTION></BODY></HWPML>''')


def prototype(base):
    root=deepcopy(base)
    run=list(root.iter('P'))[0].find('TEXT')
    run.insert(0,ET.fromstring('''<FIELDBEGIN Command="MEMO/65535/1/111/222/test/\\;;" Dirty="true" Editable="true"
       FieldId="623209829" InstId="900" Property="0" Type="Memo" Zorder="1">
       <PARALIST><P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR>시험 메모</CHAR></TEXT></P></PARALIST>
       </FIELDBEGIN>'''))
    return root


class ReviewMemoTests(unittest.TestCase):
    def setUp(self):
        self.topic={'id':'s0000','title':'경쟁기관 현황'}
        self.field={'id':'P0000','label':'국외 경쟁기관'}

    def test_prose_preserved_only_annotation_removed(self):
        self.assertEqual('핵융합 열회수를 제안한다.\n목표는 아직 미확정이다.',
            memo_body('핵융합 열회수를 제안한다.\n(확인 필요: 목표값)\n목표는 아직 미확정이다.'))
        self.assertEqual('',memo_body('확인 필요'))
        self.assertEqual('추가 확인 필요 없음',memo_body('추가 확인 필요 없음'))

    def test_recover_original_reasons_and_method(self):
        old={'values':{'P0000':'내용 [확인 필요: 실제 제품·납품 실적]'},
             'needs_review':['P0000, P0002: 비교 기준일이 제공되지 않음.']}
        memo=build_memo(self.topic,self.field,'내용 [확인 필요]',[],old)
        self.assertIn('실제 제품·납품 실적',memo['text'])
        self.assertIn('공식 자료',memo['method'])
        self.assertNotIn('P0000',memo['text'])
        self.assertNotIn('- ,',memo['text'])

    def test_resolved_values_do_not_restore_stale_reasons(self):
        self.assertIsNone(build_memo(self.topic,self.field,'확정된 기관',[],
                                    {'needs_review':['P0000: 확인 필요: 기관명'],'values':{}}))

    def test_fallback_does_not_invent_evidence(self):
        memo=build_memo(self.topic,self.field,'실증시험을 추진한다. [확인 필요]',[])
        self.assertIn('본문에 제시된 사실·수치·계획',memo['text'])

    def test_empty_or_placeholder_fields_never_get_memos(self):
        for value in ('', '확인 필요', '[확인 필요: 성명]', '?', '미정', '____'):
            with self.subTest(value=value):
                self.assertIsNone(build_memo(self.topic,self.field,value,
                    ['P0000: 담당자 성명을 입력해 주세요.']))

    def test_personal_and_factual_slots_excluded_but_table_prose_kept(self):
        for field in ({**self.field,'role':'personal'},
                      {**self.field,'in_table':True,'label':'사업명'},
                      {**self.field,'in_table':False,'label':'성명'},
                      {**self.field,'kind':'schedule_marker'}):
            self.assertIsNone(build_memo(self.topic,field,'가상의 정보 [확인 필요]',[]))
        field={**self.field,'in_table':True,'label':'추진계획'}
        self.assertIsNotNone(build_memo(self.topic,field,'열회수 시험을 제안한다. [확인 필요]',[]))

    def test_simple_fill_note_removed_from_mixed_prose(self):
        memo=build_memo(self.topic,self.field,'역할 배정을 제안한다. [확인 필요]',
            ['P0000: 성명과 연락처를 입력해 주세요.', 'P0000: 제안된 역할이 실제 업무 배정과 맞는지 확인 필요'])
        self.assertNotIn('연락처',memo['text'])
        self.assertIn('역할',memo['text'])
        self.assertIsNone(build_memo(self.topic,self.field,'보존할 본문 [확인 필요]',
            ['P0000: 성명을 입력해 주세요.']))

    def test_packets_latest_numeric_attempt_and_replay(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);(p/'responses').mkdir()
            old={'topic_id':'s0000','values':{'P0000':'old'}}
            (p/'저장응답_원본.json').write_text(json.dumps({'ai_attempts':{'s0000.attempt2.json':old}}),encoding='utf8')
            new={**old,'values':{'P0000':'new'}}
            (p/'responses/s0000.attempt10.json').write_text(json.dumps(new),encoding='utf8')
            self.assertEqual(new,original_packets(p)['s0000'])

    def test_two_independent_memos_including_empty_cell(self):
        base=source();proto=prototype(base)
        entries=[{'output_indices':[i],'review_memo':{'field_id':'P'+str(i),'text':'확인할 내용\n값 '+str(i)}} for i in (0,2)]
        root,records=compose_memos(base,proto,entries)
        self.assertEqual(2,len(memo_fields(root)))
        self.assertEqual(2,len({n.get('InstId') for n in memo_fields(root)}))
        self.assertEqual(['1','2'],[n.get('Command').split('/')[2] for n in memo_fields(root)])
        self.assertEqual(['본문 문장','',''],[paragraph_text(p) for p in body_paragraphs(root)])
        verify_memos(root,records,base)
        memo_fields(root)[0].find('.//CHAR').text='changed'
        with self.assertRaises(RuntimeError):verify_memos(root,records,base)

    def test_existing_memo_indices_and_contents_preserved(self):
        base=prototype(source())
        # Existing memo P shifts global indices, but not main-body coordinates.
        root,records=compose_memos(base,prototype(base),[{'output_indices':[3],
            'review_memo':{'field_id':'P0003','text':'빈칸 확인'}}])
        self.assertEqual(2,records[0]['anchor_index'])
        verify_memos(root,records,base)

    def test_render_metadata_and_user_value_protection(self):
        root=source();field={'id':'P0000','index':0,'original':'본문 문장','label':'목표','max_chars':500,'multiline':True}
        topic={**self.topic,'start':0,'fields':[field]}
        manifest={'paragraph_count':3,'topics':[topic], 'render_policy':{'readable_body':True,'blue_review':True,'review_memos':True}}
        packet={'topic_id':topic['id'],'values':{'P0000':'작성된 본문\n(확인 필요: 목표값)'},'needs_review':[]}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/'template';folder.mkdir()
            (folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf8')
            xml,log=render_draft(folder,manifest,{topic['id']:packet})
            self.assertEqual(['작성된 본문'],log[0]['paragraph_values'])
            self.assertIn('목표값',log[0]['review_memo']['text'])
            _,log=render_draft(folder,manifest,{topic['id']:packet},{'P0000':'사용자 확정값'})
            self.assertNotIn('review_memo',log[0])
            packet['values']['P0000']='확인 필요'
            _,log=render_draft(folder,manifest,{topic['id']:packet})
            self.assertNotIn('review_memo',log[0])
            self.assertEqual([''],log[0]['paragraph_values'])


if __name__=='__main__':unittest.main()
