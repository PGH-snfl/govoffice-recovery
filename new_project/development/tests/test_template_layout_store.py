from contextlib import closing
from copy import deepcopy
from pathlib import Path
import shutil
import sqlite3
import tempfile
import threading
import unittest
from unittest.mock import patch, Mock
import xml.etree.ElementTree as ET

from govoffice.services.template_layout_store import save_layout_database, stored_writing_manifest
from govoffice.services.document_authoring import TemplateRegistry, digest, render_draft, own_text, parse_source, replace_text
from govoffice.services.template_guide_registration import register_guided
from govoffice.services.authoring_policy import prepare_new_job
from govoffice.services.authoring_cell_budget import attach_cell_budgets
from test_authoring_design_fields import banner, manifest_for
from test_template_analysis import SOURCE, AnalysisAgent


class LayoutStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)

    def store(self,root,manifest):
        (self.folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
        (self.folder/'template.hwp').write_bytes(b'fixture')
        manifest.update(id='a'*32,source_sha256=digest(self.folder/'source.hwpml'),native_sha256=digest(self.folder/'template.hwp'))
        info=save_layout_database(self.folder,root,manifest)
        return self.folder/info['file']

    def test_design_title_and_content_destination_are_separate_and_consumed(self):
        root=banner();m=manifest_for(root,3,'연구개발 목표 및 내용')
        before=ET.tostring(root);dbpath=self.store(root,m)
        with closing(sqlite3.connect(dbpath)) as db:
            row=db.execute('SELECT source_index,target_index,write_mode FROM content_fields').fetchone()
            self.assertEqual((3,0,'insert_after'),row)
            self.assertEqual('design',db.execute('SELECT role FROM tables').fetchone()[0])
            self.assertEqual('design',db.execute('SELECT role FROM regions WHERE paragraph_index=3').fetchone()[0])
            self.assertIn('연구개발 목표 및 내용',db.execute('SELECT xml FROM design_layout').fetchone()[0])
        with patch('govoffice.services.authoring_design_fields.safe_writing_manifest',side_effect=AssertionError('must use database')):
            self.assertEqual(0,stored_writing_manifest(self.folder,root,m)['topics'][0]['fields'][0]['index'])
        output,logs=render_draft(self.folder,m,{},local_values={'P0003':'저장된 입력 위치에 작성한 본문'})
        out=ET.fromstring(output)
        self.assertNotIn('저장된 입력 위치에 작성한 본문',ET.tostring(out.find('.//TABLE'),encoding='unicode'))
        self.assertEqual(0,logs[0]['input_index']);self.assertEqual(before,ET.tostring(root))

    def test_marker_does_not_turn_a_blank_cell_into_a_fixed_label(self):
        raw=ET.fromstring('<HWPML><BODY><SECTION><P><TEXT><TABLE><ROW>'
            '<CELL Width="3000"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>'
            '<CELL Width="9000"><PARALIST><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>'
            '</ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>')
        marked=deepcopy(raw);replace_text(list(marked.iter('P'))[1],'〔P0001〕')
        manifest=manifest_for(marked,1,'입력칸',insert=False)
        field=manifest['topics'][0]['fields'][0];field['slot_marker']='〔P0001〕'
        from govoffice.services.authoring_design_fields import safe_writing_manifest
        self.assertEqual(2,safe_writing_manifest(marked,manifest)['topics'][0]['fields'][0]['index'])
        (self.folder/'source.hwpml').write_text(ET.tostring(marked,encoding='unicode'),encoding='utf-8')
        (self.folder/'template.hwp').write_bytes(b'fixture')
        manifest.update(id='a'*32,source_sha256=digest(self.folder/'source.hwpml'),
                        native_sha256=digest(self.folder/'template.hwp'))
        save_layout_database(self.folder,marked,manifest,classification_root=raw)
        effective=stored_writing_manifest(self.folder,marked,manifest)
        self.assertEqual(1,effective['topics'][0]['fields'][0]['index'])
        xml,log=render_draft(self.folder,manifest,{},local_values={'P0001':'검증'})
        self.assertNotIn('〔P0001〕',xml)
        self.assertEqual('검증',log[0]['value'])

    def test_content_removed_from_skeleton_guides_separate_unknown_preserved(self):
        root=ET.fromstring('<HWPML><BODY><SECTION><P><TEXT><CHAR>1. 제목</CHAR></TEXT></P>'
            '<P><TEXT><CHAR>입력 예시</CHAR></TEXT></P><P><TEXT><CHAR>작성 지침</CHAR></TEXT></P>'
            '<P><TEXT><CHAR>판단하지 않은 원문</CHAR><PICTURE/></TEXT></P></SECTION></BODY></HWPML>')
        m=manifest_for(root,1,'본문',insert=False);m['clear_guide_indices']=[2]
        with closing(sqlite3.connect(self.store(root,m))) as db:
            rows=dict(db.execute('SELECT paragraph_index,role FROM regions'))
            self.assertEqual('content',rows[1]);self.assertEqual('instruction',rows[2]);self.assertEqual('preserve',rows[3])
            xml=db.execute('SELECT xml FROM design_layout').fetchone()[0]
            self.assertNotIn('입력 예시',xml);self.assertNotIn('작성 지침',xml)
            self.assertIn('판단하지 않은 원문',xml);self.assertIn('PICTURE',xml)
            self.assertEqual('입력 예시',db.execute('SELECT original_text FROM regions WHERE paragraph_index=1').fetchone()[0])

    def test_runtime_options_allowed_but_binding_or_source_changes_rejected(self):
        root=banner();m=manifest_for(root,3,'연구개발 목표 및 내용');self.store(root,m)
        changed=deepcopy(m);prepare_new_job(changed);attach_cell_budgets(root,changed)
        self.assertEqual(0,stored_writing_manifest(self.folder,root,changed)['topics'][0]['fields'][0]['index'])
        changed['topics'][0]['fields'][0]['index']=2
        with self.assertRaisesRegex(ValueError,'데이터베이스'):stored_writing_manifest(self.folder,root,changed)
        root.set('changed','true')
        with self.assertRaisesRegex(ValueError,'데이터베이스'):stored_writing_manifest(self.folder,root,m)

    def test_corruption_missing_and_unsafe_path_fail_closed(self):
        root=banner();m=manifest_for(root,3,'연구개발 목표 및 내용');path=self.store(root,m)
        path.write_bytes(b'corrupted')
        with self.assertRaisesRegex(ValueError,'데이터베이스'):stored_writing_manifest(self.folder,root,m)
        path.unlink()
        with self.assertRaisesRegex(ValueError,'데이터베이스'):stored_writing_manifest(self.folder,root,m)
        m['layout_database']['file']='../outside.sqlite3'
        with self.assertRaisesRegex(ValueError,'데이터베이스'):stored_writing_manifest(self.folder,root,m)

    def test_legacy_without_database_still_uses_safe_routes(self):
        root=banner();m=manifest_for(root,3,'연구개발 목표 및 내용')
        self.assertEqual(0,stored_writing_manifest(self.folder,root,m)['topics'][0]['fields'][0]['index'])

    def test_duplicate_labels_keep_separate_fields_and_nested_relationships(self):
        def p(text=''):return '<P><TEXT><CHAR>'+text+'</CHAR></TEXT></P>'
        inner='<P><TEXT><TABLE><ROW><CELL><PARALIST>'+p('내용')+p()+'</PARALIST></CELL></ROW></TABLE></TEXT></P>'
        root=ET.fromstring('<HWPML><BODY><SECTION>'+p('1. 제목')+'<P><TEXT><TABLE><ROW><CELL><PARALIST>'+inner+
                          '</PARALIST></CELL><CELL><PARALIST>'+p('내용')+p()+'</PARALIST></CELL></ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>')
        m=manifest_for(root,4,'내용',insert=False)
        f=deepcopy(m['topics'][0]['fields'][0]);f.update(id='P0006',index=6);m['topics'][0]['fields'].append(f)
        with closing(sqlite3.connect(self.store(root,m))) as db:
            self.assertEqual(2,db.execute('SELECT count(*) FROM content_fields').fetchone()[0])
            self.assertEqual([(0,None),(1,0)],db.execute('SELECT table_index,parent_cell_index FROM tables ORDER BY table_index').fetchall())
            self.assertEqual('mixed',db.execute('SELECT role FROM tables WHERE table_index=0').fetchone()[0])

    def test_registry_registration_copy_archive_and_atomic_failure(self):
        source=self.folder/'input.hml';source.write_text(SOURCE,encoding='utf-8')
        native=self.folder/'input.hwp';native.write_bytes(b'fixture')
        registry=TemplateRegistry(self.folder/'templates')
        m=registry.register(source,native,'시험',starts=[(0,'1. 사업 계획')],fixed_fields=[5])
        folder=registry.path(m['id']);self.assertIn('layout_database',registry.load(m['id']))
        copied=self.folder/'snapshot';shutil.copytree(folder,copied)
        stored_writing_manifest(copied,parse_source(copied/'source.hwpml'),m)
        archived=registry.delete(m['id'])
        self.assertTrue((Path(archived['archive_path'])/m['layout_database']['file']).exists())
        with patch('govoffice.services.template_layout_store.save_layout_database',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):registry.register(source,native,'실패',starts=[(0,'1. 사업 계획')])
        self.assertEqual([],list(registry.folder.iterdir()))

    def test_guided_registration_publishes_database_and_cancel_leaves_nothing(self):
        source=self.folder/'input.hml';source.write_text(SOURCE,encoding='utf-8')
        native=self.folder/'input.hwp';native.write_bytes(b'fixture')
        registry=TemplateRegistry(self.folder/'templates');cancel=threading.Event()
        result={'outline':{'chapters':[{'index':0,'title':'1. 사업 계획',
                    'instructions':[{'index':1,'text':'공개 근거와 실행 절차를 작성'}],'subtopics':[]}],
                    'unassigned_indices':[]},'ai_requests':1}
        class SlotAgent:
            def generate(self,prompt,schema,cancel):
                import json
                payload=json.loads(prompt[prompt.rfind('\n')+1:])
                slots=[]
                for item in payload['slots']:
                    role='personal' if item['label_hint']=='이름' else 'body'
                    slots.append({'index':item['index'],'role':role,'topic_index':-1 if role=='personal' else 0,
                                  'label':item['label_hint'] or '연구내용','confidence':'high','reason':'테스트 분류'})
                return {'slots':slots}
        agent=SlotAgent()
        with patch('govoffice.services.template_guide_registration.export_ai_guides',return_value=result):
            m=register_guided(registry,source,native,'시험',agent,cancel,Mock())
        self.assertTrue((registry.path(m['id'])/m['layout_database']['file']).is_file())
        self.assertIn('layout_database',registry.load(m['id']))
        bundle=registry.path(m['id'])
        marked=parse_source(bundle/'source.hwpml')
        markers=[p for p in marked.iter('P') if '〔P' in own_text(p)]
        self.assertEqual(2,len(markers))
        self.assertEqual(digest(source),m['original_source_sha256'])
        rendered,_=render_draft(bundle,m,{})
        self.assertNotIn('〔P',rendered)
        self.assertEqual(2,m['ai_analysis_requests'])
        self.assertTrue((bundle/'입력칸판정.json').is_file())
        existing=list(registry.folder.iterdir());cancel.set()
        with self.assertRaises(InterruptedError):register_guided(registry,source,native,'취소',None,cancel,Mock())
        self.assertEqual(existing,list(registry.folder.iterdir()))


if __name__=='__main__':unittest.main()
