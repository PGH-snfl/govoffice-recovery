import tempfile
import time
import unittest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, Mock
import xml.etree.ElementTree as ET

from govoffice.services.document_authoring import TemplateRegistry, read_json
from govoffice.services.authoring_inputs import blank_candidates, field_labels, input_rows, attach_input_paths, saved_profile_rows
from govoffice.services.authoring_commands import AuthoringCommands


SOURCE = '''<HWPML><HEAD><CHARSHAPELIST><CHARSHAPE Id="0" TextColor="0"/><CHARSHAPE Id="1" TextColor="16711680"/></CHARSHAPELIST></HEAD><BODY><SECTION>
<P><TEXT><CHAR>신청서</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW>
<CELL RowAddr="0" ColAddr="0"><PARALIST><P><TEXT><CHAR>이름</CHAR></TEXT></P></PARALIST></CELL>
<CELL RowAddr="0" ColAddr="1"><PARALIST><P><TEXT><CHAR/></TEXT></P><P><TEXT><CHAR/></TEXT></P></PARALIST></CELL>
</ROW></TABLE></TEXT></P>
<P><TEXT><CHAR>1. 사업 개요</CHAR></TEXT></P>
<P><TEXT><CHAR>1-1. 목적</CHAR></TEXT></P>
<P><TEXT CharShape="1"><CHAR>※ 목표를 구체적으로 작성</CHAR></TEXT></P>
<P><TEXT><CHAR>____</CHAR></TEXT></P>
<P><TEXT><TABLE><ROW><CELL><PARALIST>
<P><TEXT><CHAR>작성 요령</CHAR></TEXT></P><P><TEXT><CHAR>공익 목적을 설명</CHAR></TEXT></P>
</PARALIST></CELL></ROW></TABLE></TEXT></P>
<P><TEXT><CHAR>1-2. 추진 내용</CHAR></TEXT></P><P><TEXT><CHAR>____</CHAR></TEXT></P>
</SECTION></BODY></HWPML>'''


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.commands = AuthoringCommands(self.folder)
        self.addCleanup(self.commands.close)
        self.xml = self.folder/'source.hwpml'
        self.xml.write_text(SOURCE,encoding='utf-8')
        self.hwp = self.folder/'source.hwp'
        self.hwp.write_bytes(b'test form only')

    def finish(self, result):
        for _ in range(300):
            op = self.commands.handle({'action':'authoring_operation','operation_id':result['operation_id']})
            if op['status'] != 'running':
                self.assertEqual('completed',op['status'],op.get('error'))
                return op['result']
            time.sleep(.01)
        self.fail('operation timeout')

    def test_inaccessible_template_does_not_block_other_templates(self):
        from govoffice.services.document_authoring import write_json
        folder=self.commands.service.registry.folder
        for key in ('good','denied'):
            target=folder/key;target.mkdir()
            write_json(target/'manifest.json',{'id':key,'name':key,'topics':[]})
        def guarded(path):
            if path.parent.name=='denied':raise PermissionError('Access denied')
            return read_json(path)
        with patch('govoffice.services.authoring_commands.read_json',side_effect=guarded):
            result=self.commands.handle({'action':'authoring_overview'})
        self.assertEqual(['good'],[t['id'] for t in result['templates']])
        self.assertEqual('denied',result['template_warnings'][0]['template_id'])
        self.assertTrue((folder/'denied/manifest.json').exists())

    def test_import_profile_blank_detection_and_chapter_library(self):
        from test_ai_guide_export import GuideFinder
        from govoffice.services.document_authoring import topic_guide_text,common_guide_text
        agent=GuideFinder();self.commands.service.agent_factory=lambda folder:agent
        self.commands.profile.대표필드추가('부서',['기존 부서'])
        self.commands.handle({'action':'authoring_profile_save','values':{'이름':'홍길동','전화번호':'010-1234-1234','이메일':'sample@example.test'}})
        self.assertIsNotNone(self.commands.profile.대표필드찾기('부서'))
        def extract(source,destination):
            destination.write_text(SOURCE,encoding='utf-8')
        with patch('govoffice.services.authoring_commands.extract_hwp',side_effect=extract):
            m = self.finish(self.commands.handle({'action':'authoring_extract_guides','path':str(self.hwp)}))
        self.assertGreater(m['ai_requests'],0)
        self.assertTrue(agent.prompts)
        guide = Path(m['guide_file']).read_text(encoding='utf-8')
        self.assertIn('※ 목표를 구체적으로 작성',guide)
        self.assertIn('공익 목적을 설명',guide)
        self.assertNotIn('홍길동',guide)
        # Extraction no longer registers input fields. Existing independently
        # registered templates still support the original personal-fill flow.
        m = self.commands.service.registry.register(self.xml,self.hwp,'예시',discover_blanks=True)
        data = self.finish(self.commands.handle({'action':'authoring_prepare_inputs','template_id':m['id']}))
        name = next(r for r in data['rows'] if r['label']=='이름')
        self.assertFalse(name['ai'])
        self.assertEqual('홍길동',name['value'])
        self.assertEqual(1,len(data['rows']))
        self.assertGreaterEqual(data['total_fields'],3)
        self.assertIn(name['id'],name['field_ids'])
        checked = self.commands.handle({'action':'authoring_validate_inputs','template_id':m['id'],'local_values':{name['id']:'다른 사람'}})
        self.assertEqual('다른 사람',checked['values'][name['id']])
        self.assertEqual('홍길동',self.commands.profile.자동입력값()['이름'])

    def test_prepare_without_saved_profile_needs_no_extra_inputs(self):
        m = self.commands.service.registry.register(self.xml,self.hwp,'예시',discover_blanks=True)
        data = self.finish(self.commands.handle({'action':'authoring_prepare_inputs','template_id':m['id']}))
        self.assertEqual([],data['rows'])
        self.assertEqual(3,data['total_fields'])

    def test_two_inputs_defer_review_to_final_output_without_false_confirmation(self):
        m = self.commands.service.registry.register(self.xml,self.hwp,'예시',discover_blanks=True)
        with patch.object(self.commands.service,'start',side_effect=self.commands.service.status):
            job=self.commands.handle({'action':'authoring_create','template_id':m['id'],
                'brief':{'title':'작성 주제','description':'주제 세부 내용'},
                'review_mode':'final_output','external_consent':True})
        self.assertEqual('final_output',job['review_mode'])
        self.assertTrue(job['research_enabled'])
        self.assertFalse(job['preflight_reviewed'])
        self.assertFalse(job['submission_ready'])
        self.assertEqual({},job['local_values'])

    def test_saved_rows_deduplicate_targets_and_exclude_empty_unmatched_ambiguous(self):
        from govoffice.domain.user_profile import 사용자프로필
        profile = 사용자프로필.생성({'대표필드목록':[
            {'id':'p','대표필드명':'담당자'},
            {'id':'name','대표필드명':'업무성명','별칭':['신청자 성명'],'기본값':'홍길동','상위필드id':'p'},
            {'id':'empty','대표필드명':'부서','기본값':''},
            {'id':'other','대표필드명':'참여기관'},
            {'id':'a','대표필드명':'연구실','별칭':['공통'],'기본값':'동일값','상위필드id':'p'},
            {'id':'b','대표필드명':'기관','별칭':['공통'],'기본값':'동일값','상위필드id':'other'},
        ]})
        labels=['신청자 성명','부서','본문','업무성명','공통','연구실','기관','담당자 > 업무성명']
        fields=[dict(id=f'P{i}',label=label,max_chars=200) for i,label in enumerate(labels)]
        m={'topics':[{'fields':fields[:4]},{'fields':fields[4:]}]}
        rows=saved_profile_rows(m,profile)
        self.assertEqual(['name','a','b'],[r['profile_field_id'] for r in rows])
        self.assertEqual(['P0','P3','P7'],rows[0]['field_ids'])
        self.assertEqual(['담당자','업무성명'],rows[0]['path'])
        self.assertEqual('홍길동',rows[0]['value'])
        self.assertEqual('동일값',rows[1]['value'])
        self.assertEqual('동일값',rows[2]['value'])
        self.assertTrue(all(not r['ai'] and r['value'] for r in rows))

    def test_logout_updates_account_and_closes_connection(self):
        with patch('govoffice.services.authoring_commands.CodexAuthor') as factory:
            factory.return_value.logout.return_value = {'connected':False, 'email':None, 'login_required':True}
            result = self.finish(self.commands.handle({'action':'authoring_logout'}))
            self.assertFalse(result['connected'])
            self.assertEqual(result, self.commands.account)
            factory.return_value.close.assert_called_once()

    def test_account_change_blocked_during_writing_and_create_blocked_during_logout(self):
        worker = Mock()
        worker.is_alive.return_value = True
        self.commands.service.workers['fake'] = worker
        for action in ('authoring_logout', 'authoring_login'):
            with self.assertRaisesRegex(ValueError, '계정을 변경'):
                self.commands.handle({'action':action})
        self.commands.service.workers.clear()
        self.commands.operations['logout'] = {'status':'running'}
        for action in ('authoring_create', 'authoring_resume'):
            with self.assertRaisesRegex(ValueError, '계정 연결'):
                self.commands.handle({'action':action, 'job_id':'unused'})

    def test_job_progress_contains_immutable_input_snapshot(self):
        m = self.commands.service.registry.register(self.xml,self.hwp,'예시',discover_blanks=True)
        f = m['topics'][0]['fields'][0]
        job = self.commands.service.create(m['id'], {'title':'예시 과제','description':'예시 본문'},
                    reviewed=True,external_consent=True,local_values={f['id']:'예시 이름'})
        status = self.commands.service.status(job['id'])
        self.assertEqual(len(m['topics']), len(status['topic_progress']))
        self.assertTrue(all(t['status']=='대기' for t in status['topic_progress']))
        self.assertEqual('예시 이름', status['input_summary'][0]['value'])
        self.assertEqual('예시 이름', status['input_snapshot'][0]['value'])
        self.assertEqual('예시',status['template_name'])

    def test_job_preserves_input_grouping_and_uses_actual_validated_values(self):
        from govoffice.services.authoring_inputs import saved_input_snapshot
        from govoffice.services.document_authoring import write_json
        m = self.commands.service.registry.register(self.xml,self.hwp,'예시',discover_blanks=True)
        ids=[f['id'] for t in m['topics'] for f in t['fields']][:2]
        rows=[{'field_ids':ids,'label':'담당자명','path':['연구팀','담당자명'],'value':'잘못된 화면 값'}]
        values={fid:'  시작 당시 값  ' for fid in ids}
        job=self.commands.service.create(m['id'],{'title':'저장 주제','description':'저장 내용'},
                reviewed=True,external_consent=True,local_values=values,input_snapshot=rows)
        rows[0]['path'][0]='다른 팀'
        self.commands.profile.대표필드추가('담당자명',['현재 프로필 값'])
        state=self.commands.service.status(job['id'])
        self.assertEqual(1,len(state['input_snapshot']))
        self.assertEqual(['연구팀','담당자명'],state['input_snapshot'][0]['path'])
        self.assertEqual('시작 당시 값',state['input_snapshot'][0]['value'])
        self.assertEqual(ids,state['input_snapshot'][0]['field_ids'])
        # Older jobs without grouping still expose only their own saved inputs.
        state.pop('input_snapshot');write_json(self.commands.service.job_path(job['id'])/'state.json',state)
        restored=self.commands.service.status(job['id'])
        self.assertEqual(2,len(restored['input_snapshot']))
        self.assertTrue(all(r['value']=='시작 당시 값' for r in restored['input_snapshot']))
        with self.assertRaises(ValueError):
            saved_input_snapshot(m,{ids[0]:'a',ids[1]:'b'},rows)
        with self.assertRaises(ValueError):
            saved_input_snapshot(m,{ids[0]:'a'},[{'field_ids':['unknown'],'label':'x','path':['x']}])

    def test_only_first_blank_in_cell_detected_not_label_or_instruction_table(self):
        root = ET.fromstring(SOURCE)
        ps = list(root.iter('P'))
        ids = blank_candidates(root,ps,set())
        empty = [i for i,p in enumerate(ps) if not ''.join(p.itertext()).strip()]
        self.assertIn(empty[0],ids)
        self.assertNotIn(empty[1],ids)

    def test_non_numbered_form_keeps_blank_candidates(self):
        self.xml.write_text(SOURCE.replace('1. 사업 개요','사업 개요').replace('1-1. 목적','목적').replace('1-2. 추진 내용','추진 내용'),encoding='utf-8')
        m = self.commands.service.registry.register(self.xml,self.hwp,'번호 없는 양식',discover_blanks=True)
        self.assertEqual(1,len(m['topics']))
        self.assertEqual(3,len(m['topics'][0]['fields']))

    def test_similar_label_does_not_trigger_personal_autofill(self):
        m = {'topics':[{'title':'1-1. 본문','fields':[{'id':'P1','label':'참여자의 이름과 경력 설명','max_chars':180}]}]}
        row = input_rows(m,{'이름':'홍길동'})[0]
        self.assertEqual('',row['value'])
        self.assertTrue(row['ai'])

    def test_input_tree_uses_exact_personal_hierarchy_and_preserves_duplicate_ids(self):
        from govoffice.domain.user_profile import 사용자프로필
        profile = 사용자프로필.생성({'대표필드목록':[
            {'id':'parent','대표필드명':'연구책임자'},
            {'id':'email','대표필드명':'업무메일','상위필드id':'parent','별칭':['담당자 이메일']},
        ]})
        rows = [dict(id=f'P{i}',topic='기본정보',label='담당자 이메일',value=value,ai=False)
                for i,value in enumerate(['first@example.invalid','second@example.invalid'])]
        attach_input_paths(rows,profile)
        self.assertEqual(['기본정보','연구책임자','업무메일'],rows[0]['path'])
        self.assertEqual(rows[0]['path'],rows[1]['path'])
        self.assertNotEqual(rows[0]['id'],rows[1]['id'])
        self.assertEqual('second@example.invalid',rows[1]['value'])

    def test_input_tree_does_not_guess_ambiguous_or_similar_personal_parent(self):
        from govoffice.domain.user_profile import 사용자프로필
        profile = 사용자프로필.생성({'대표필드목록':[
            {'id':'p1','대표필드명':'책임자'}, {'id':'p2','대표필드명':'담당자'},
            {'id':'c1','대표필드명':'업무메일','상위필드id':'p1','별칭':['공통메일']},
            {'id':'c2','대표필드명':'별도메일','상위필드id':'p2','별칭':['공통메일']},
        ]})
        rows = [dict(id=f'P{i}',topic='기본정보',label=label,value='',ai=False)
                for i,label in enumerate(['공통메일','업무메일 설명','기관 > 주소'])]
        attach_input_paths(rows,profile)
        self.assertEqual(['기본정보','공통메일'],rows[0]['path'])
        self.assertEqual(['기본정보','업무메일 설명'],rows[1]['path'])
        self.assertEqual(['기본정보','기관','주소'],rows[2]['path'])

    def test_generic_render_cleans_guides_without_changing_table_flow_or_font_size(self):
        from govoffice.services.document_authoring import render_draft
        self.xml.write_text(SOURCE.replace('TextColor="0"','TextColor="0" Height="1750"').replace('<TEXT>','<TEXT CharShape="0">'),encoding='utf-8')
        m = self.commands.service.registry.register(self.xml,self.hwp,'일반 양식',discover_blanks=True,
                render_policy={'clean_guidance':True,'preserve_layout':True})
        results = {t['id']:{'topic_id':t['id'],'values':{f['id']:'검증 본문' for f in t['fields']},'needs_review':[]} for t in m['topics']}
        xml,log = render_draft(self.commands.service.registry.path(m['id']),m,results)
        root = ET.fromstring(xml)
        self.assertEqual(1,len(list(root.iter('TABLE'))))
        self.assertEqual(ET.fromstring(self.xml.read_text(encoding='utf-8')).find('.//TABLE').attrib,root.find('.//TABLE').attrib)
        ps = list(root.iter('P'))
        shapes = {s.get('Id'):s for s in root.iter('CHARSHAPE')}
        for field in log:
            style = ps[field['output_index']].find('TEXT').get('CharShape')
            self.assertEqual('1750',shapes[style].get('Height'))


@unittest.skipUnless(sys.platform == 'win32','WPF tests require Windows')
class WorkflowScreenTests(unittest.TestCase):
    def test_two_stage_module_is_loaded_and_included_in_internal_copy(self):
        project=Path(__file__).resolve().parents[2]
        self.assertIn(". (Join-Path $ProjectDir 'document_authoring_flow_ui.ps1')",
                      (project/'launch_gui.ps1').read_text(encoding='utf-8-sig'))
        self.assertIn('"document_authoring_flow_ui.ps1"',
                      (project/'packaging/build_internal_release.py').read_text(encoding='utf-8'))
        self.assertTrue((project/'document_authoring_flow_ui.ps1').read_bytes().startswith(b'\xef\xbb\xbf'))

    def test_screen_instantiation_and_input_binding(self):
        self.run_probe('document_authoring_ui_probe.ps1','"ok":true')

    def test_production_callbacks_with_mock_backend(self):
        self.run_probe('document_authoring_workflow_probe.ps1','AUTHORING_WORKFLOW_OK')

    def run_probe(self,name,marker):
        result = subprocess.run(['powershell','-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(Path(__file__).with_name(name))],capture_output=True,timeout=20)
        output = (result.stdout+result.stderr).decode('utf-8',errors='replace')
        self.assertEqual(0,result.returncode,output)
        self.assertIn(marker,output)


if __name__ == '__main__':
    unittest.main()
