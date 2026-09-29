import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

from govoffice.services.ai_guide_export import export_ai_guides


class GuideFinder:
    """Deterministic test double, never used by the product."""
    def __init__(self):self.prompts=[];self.closed=False
    def account(self):return {'connected':True}
    def close(self):self.closed=True
    def generate(self,prompt,schema,cancel):
        self.prompts.append(prompt);data=json.loads(prompt.split('\n',1)[1])
        previous=data['previous_topics'];head=previous[-1]['index'] if previous else None
        topics={};unattached=[]
        for row in data['paragraphs']:
            text=row['text']
            if text.startswith('1-') or text=='번호 없는 소주제':
                head=row['index'];topics.setdefault(head,[])
            elif text in {'작성요령','작성 요령','원문 요령','앞에 있는 요령','첫 요령을 그대로 작성','두 번째 위치의 요령','공익 목적을 설명','※ 목표를 구체적으로 작성'}:
                if head is None:unattached.append(row['index'])
                else:topics.setdefault(head,[]).append(row['index'])
        return {'topics':[{'heading_index':i,'instruction_indices':ids} for i,ids in topics.items()],
                'unattached_instruction_indices':unattached}


class AIGuideExportTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'source.hwpml'
        self.source.write_text('<HWPML><BODY><SECTION><P><TEXT><CHAR>번호 없는 소주제</CHAR></TEXT></P>'
            '<P><TEXT><CHAR>일반 본문</CHAR></TEXT></P><P><TEXT><CHAR>원문 요령</CHAR></TEXT></P>'
            '</SECTION></BODY></HWPML>',encoding='utf-8')
        self.agent=GuideFinder();self.cancel=threading.Event()

    def export(self):
        return export_ai_guides(self.source,self.root/'out','시험',self.agent,self.cancel)

    def test_ai_really_called_and_only_original_locations_are_copied(self):
        result=self.export();text=Path(result['guide_file']).read_text(encoding='utf-8')
        self.assertEqual(1,result['ai_requests']);self.assertEqual(1,len(self.agent.prompts))
        self.assertIn('## 번호 없는 소주제',text);self.assertIn('원문 요령',text)
        self.assertNotIn('일반 본문',text);self.assertNotIn('공통 작성요령',text)
        self.assertIn('일반 본문',self.agent.prompts[0])  # Not prefiltered by rules.
        self.assertIn('먼저 각 문구의 의미와 문서상 역할',self.agent.prompts[0])
        self.assertIn('문단 번호는 판단을 마친 뒤',self.agent.prompts[0])

    def test_invalid_locations_and_duplicate_assignments_publish_nothing(self):
        for indices in ([999],[2,2]):
            self.agent.generate=Mock(return_value={'topics':[{'heading_index':0,'instruction_indices':indices}],
                                                 'unattached_instruction_indices':[]})
            with self.assertRaises(ValueError):self.export()
            self.assertFalse((self.root/'out').exists())

    def test_no_topic_failure_is_not_common_only_success(self):
        self.agent.generate=Mock(return_value={'topics':[],'unattached_instruction_indices':[2]})
        with self.assertRaisesRegex(ValueError,'소주제를 찾지 못했습니다'):self.export()
        self.assertFalse((self.root/'out').exists())

    def test_transport_failure_or_cancellation_has_no_local_fallback(self):
        self.agent.generate=Mock(side_effect=RuntimeError('offline'))
        with self.assertRaises(RuntimeError):self.export()
        self.assertFalse((self.root/'out').exists())
        self.cancel.set()
        with self.assertRaises(InterruptedError):self.export()
        self.assertFalse((self.root/'out').exists())

    def test_chunk_continuation_keeps_previous_topic_and_original_order(self):
        with patch('govoffice.services.ai_guide_export.CHUNK_CHARS',70):result=self.export()
        self.assertGreater(result['ai_requests'],1)
        audit=json.loads((self.root/'out/원문위치.json').read_text(encoding='utf-8'))
        self.assertEqual([0,1,2],audit['source_paragraph_indices'])
        self.assertEqual([{'heading_index':0,'instruction_indices':[2]}],audit['topics'])
