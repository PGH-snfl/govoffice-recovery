import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

from govoffice.services.source_guide_export import extract_source_guides
from govoffice.services.authoring_commands import AuthoringCommands
from govoffice.services.document_authoring import parse_source
from govoffice.services.template_analysis import source_records
from govoffice.services.template_topic_analysis import extract_candidates


def p(text):
    return f'<P><TEXT><CHAR>{text}</CHAR></TEXT></P>'


def guide(text):
    return '<P><TEXT><TABLE><ROW><CELL><PARALIST>'+p('작성요령')+p(text)+'</PARALIST></CELL></ROW></TABLE></TEXT></P>'


class SourceGuideExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.xml = self.root/'source.hwpml'

    def make_source(self):
        self.xml.write_text('<HWPML><BODY><SECTION>'+guide('앞에 있는 요령')+
            p('1-1. 첫 소주제')+guide('첫 요령을 그대로 작성')+p('복사하면 안 되는 일반 본문')+p('26.12')+p('10.0%')+
            p('1-1. 첫 소주제')+guide('두 번째 위치의 요령')+
            '</SECTION></BODY></HWPML>', encoding='utf-8')

    def test_literal_order_repeated_titles_and_unmatched_text(self):
        self.make_source()
        result = extract_source_guides(self.xml,self.root/'out','시험')
        text = Path(result['guide_file']).read_text(encoding='utf-8')
        self.assertEqual(2,text.count('## 1-1. 첫 소주제'))
        self.assertEqual(1,text.count('첫 요령을 그대로 작성'))
        self.assertLess(text.index('앞에 있는 요령'),text.index('첫 요령을 그대로 작성'))
        self.assertLess(text.index('첫 요령을 그대로 작성'),text.index('두 번째 위치의 요령'))
        self.assertNotIn('복사하면 안 되는 일반 본문',text)
        self.assertNotIn('공통 작성요령',text)
        self.assertEqual(0,result['ai_requests'])
        audit=json.loads((self.root/'out/원문위치.json').read_text(encoding='utf-8'))
        self.assertEqual(audit['source_indices'],audit['copied_indices'])

    def test_existing_file_never_overwritten_and_cancel_creates_nothing(self):
        self.make_source()
        extract_source_guides(self.xml,self.root/'out','시험')
        with self.assertRaises(FileExistsError):
            extract_source_guides(self.xml,self.root/'out','시험')
        cancel=threading.Event();cancel.set()
        with self.assertRaises(InterruptedError):
            extract_source_guides(self.xml,self.root/'cancelled','시험',cancel)
        self.assertFalse((self.root/'cancelled').exists())

    def test_no_title_preserves_guidance_and_no_guidance_does_not_fake_success(self):
        self.xml.write_text('<HWPML><BODY><SECTION>'+guide('제목 없는 원문')+'</SECTION></BODY></HWPML>',encoding='utf-8')
        result=extract_source_guides(self.xml,self.root/'out','시험')
        self.assertEqual(0,result['heading_count'])
        self.assertIn('제목 없는 원문',Path(result['guide_file']).read_text(encoding='utf-8'))
        self.xml.write_text('<HWPML><BODY><SECTION>'+p('1-1. 제목')+'</SECTION></BODY></HWPML>',encoding='utf-8')
        with self.assertRaises(ValueError):
            extract_source_guides(self.xml,self.root/'empty','시험')
        self.assertFalse((self.root/'empty').exists())

    def test_bundled_form_copies_every_extracted_instruction_once(self):
        source=Path(__file__).resolve().parents[2]/'src/govoffice/institutions/packages/seoultech/climate_2026/source.hwpml'
        root=parse_source(source)
        _,blocks,_,_=extract_candidates(root,source_records(root))
        expected={p['index']:p['text'] for b in blocks for p in b['paragraphs']}
        result=extract_source_guides(source,self.root/'out','기후부 양식')
        actual={r['index']:r['text'] for t in result['outline']['chapters'] for r in t['instructions']}
        self.assertEqual(expected,actual)
        self.assertEqual(526,len(actual))

    def test_gui_command_uses_ai_finder_without_template_registration(self):
        self.make_source()
        native=self.root/'sample.hwp';native.write_bytes(b'synthetic')
        command=AuthoringCommands(self.root/'data')
        from test_ai_guide_export import GuideFinder
        agent=GuideFinder();command.service.agent_factory=Mock(return_value=agent)
        command._operation=lambda fn: fn('test')
        command.operations['test']={};command.operation_stops['test']=threading.Event()
        def export_copy(_native,target):
            target.write_bytes(self.xml.read_bytes())
        with patch('govoffice.services.authoring_commands.extract_hwp',side_effect=export_copy):
            result=command.handle({'action':'authoring_extract_guides','path':str(native)})
        self.assertTrue(Path(result['guide_file']).is_file())
        self.assertEqual([],list(command.service.registry.folder.glob('*/manifest.json')))
        command.service.agent_factory.assert_called_once()
        self.assertTrue(agent.closed)
        self.assertGreater(result['ai_requests'],0)
