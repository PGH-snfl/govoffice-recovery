from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock,patch
import os

from govoffice.services.authoring_commands import AuthoringCommands
from govoffice.services.template_analysis import register_analyzed
from test_template_analysis import SOURCE,AnalysisAgent
from test_document_authoring import FakeAgent,fake_export


class TemplateDeleteTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.commands=AuthoringCommands(self.root/'app');self.addCleanup(self.commands.close)
        self.xml=self.root/'original.hwpml';self.xml.write_text(SOURCE,encoding='utf-8')
        self.native=self.root/'original.hwp';self.native.write_bytes(b'original user file')
        self.registry=self.commands.service.registry
        self.m=register_analyzed(self.registry,self.xml,self.native,'삭제 시험',AnalysisAgent(),threading.Event(),Mock())

    def delete(self,**overrides):
        return self.commands.handle({'action':'authoring_delete_template','template_id':self.m['id'],'confirmed':True,**overrides})

    def test_removed_from_list_but_archive_and_external_original_remain(self):
        before={p.name:p.read_bytes() for p in self.registry.path(self.m['id']).iterdir() if p.is_file()}
        result=self.delete();archive=Path(result['archive_path'])
        self.assertTrue(result['deleted']);self.assertTrue(result['recoverable'])
        self.assertFalse(self.registry.path(self.m['id']).exists())
        self.assertEqual([],self.commands.handle({'action':'authoring_overview'})['templates'])
        self.assertEqual(before,{p.name:p.read_bytes() for p in archive.iterdir() if p.is_file()})
        self.assertEqual(b'original user file',self.native.read_bytes());self.assertEqual(SOURCE,self.xml.read_text(encoding='utf-8'))
        self.assertEqual(self.registry.folder.parent.resolve(),archive.parent.parent.resolve())

    def test_confirmation_is_required_and_cancel_changes_nothing(self):
        for value in (False,None,1,'true'):
            with self.assertRaisesRegex(ValueError,'확인'):self.delete(confirmed=value)
        self.assertTrue(self.registry.path(self.m['id']).is_dir())

    def test_existing_job_can_finish_from_its_snapshot_after_deletion(self):
        service=self.commands.service;service.agent_factory=lambda _:FakeAgent();service.exporter=fake_export
        job=service.create(self.m['id'],{'title':'가상 주제','description':'내용'},review_mode='final_output',external_consent=True)
        snapshot=service.job_path(job['id'])/'template/template.hwp';before=snapshot.read_bytes()
        output=service.job_path(job['id'])/'existing-output.hwp';output.write_bytes(b'prior output remains')
        self.delete();self.assertEqual(before,snapshot.read_bytes())
        service.start(job['id']);service.workers[job['id']].join(10)
        state=service.status(job['id']);self.assertEqual('completed',state['status'],state.get('error'))
        self.assertEqual(b'prior output remains',output.read_bytes())
        self.assertTrue(any(j['id']==job['id'] for j in self.commands.handle({'action':'authoring_overview'})['jobs']))

    def test_running_registration_and_writing_block_deletion(self):
        self.commands.operations['test']={'status':'running'}
        with self.assertRaises(ValueError):self.delete()
        self.commands.operations.clear()
        self.commands.service.workers['test']=Mock(is_alive=Mock(return_value=True))
        try:
            with self.assertRaisesRegex(ValueError,'문서 작성'):self.delete()
        finally:self.commands.service.workers.clear()
        self.assertTrue(self.registry.path(self.m['id']).exists())

    def test_bad_ids_and_missing_template_never_move_other_directories(self):
        for value in ('../','deleted_templates',str(self.registry.folder),'a'*32+'/..',None):
            with self.assertRaises(ValueError):self.delete(template_id=value)
        self.delete()
        with self.assertRaisesRegex(ValueError,'이미 삭제'):self.delete()
        self.assertTrue(self.native.exists())

    def test_modified_source_registration_is_still_removable(self):
        (self.registry.path(self.m['id'])/'template.hwp').write_bytes(b'changed registration')
        result=self.delete()
        self.assertEqual(b'changed registration',(Path(result['archive_path'])/'template.hwp').read_bytes())

    def test_junction_source_or_archive_is_refused(self):
        source=self.registry.path(self.m['id']);archive=self.registry.folder.parent/'deleted_templates'
        for target in (source,archive):
            with patch.object(Path,'is_junction',lambda p:p==target):
                with self.assertRaises(ValueError):self.delete()
        self.assertTrue(source.exists())

    def test_persistent_winerror5_never_hides_registration_or_reports_success(self):
        source=self.registry.path(self.m['id']);before=(source/'manifest.json').read_bytes()
        error=PermissionError(13,'액세스가 거부되었습니다.');error.winerror=5
        with patch.object(Path,'rename',side_effect=error) as move,patch('govoffice.services.document_authoring.time.sleep'),patch(
                'govoffice.services.template_archive._check_delete_sharing',side_effect=error):
            with self.assertRaisesRegex(ValueError,'등록 폴더 보관 및 정리') as context:self.delete()
        self.assertEqual(4,move.call_count)
        self.assertEqual(before,(source/'manifest.json').read_bytes())
        self.assertFalse((self.registry.folder.parent/'template_deletions').exists())
        self.assertEqual(1,len(self.commands.handle({'action':'authoring_overview'})['templates']))
        self.assertEqual(self.m['id'],self.registry.load(self.m['id'])['id'])
        self.assertIn(str(source),str(context.exception));self.assertIn('이동할 위치:',str(context.exception))
        self.assertEqual(b'original user file',self.native.read_bytes())

    def test_denied_archive_creation_keeps_registration(self):
        original=Path.mkdir;archive=self.registry.folder.parent/'deleted_templates'
        def deny_archive(path,*args,**kwargs):
            if path==archive:raise PermissionError(13,'거부')
            return original(path,*args,**kwargs)
        with patch.object(Path,'mkdir',deny_archive):
            with self.assertRaisesRegex(ValueError,'삭제 보관 폴더 준비'):self.delete()
        self.assertEqual(1,len(self.commands.handle({'action':'authoring_overview'})['templates']))

    def test_transient_windows_denial_retries_the_same_real_move(self):
        source=self.registry.path(self.m['id']);original=Path.rename
        error=PermissionError(13,'거부');error.winerror=5
        destinations=[]
        def transient(path,target):
            destinations.append(target)
            if len(destinations)<3:raise error
            return original(path,target)
        with patch.object(Path,'rename',transient),patch('govoffice.services.document_authoring.time.sleep'):
            result=self.delete()
        self.assertEqual(3,len(destinations));self.assertEqual(1,len(set(destinations)))
        self.assertFalse(source.exists());self.assertTrue((Path(result['archive_path'])/'template.hwp').is_file())
        self.assertEqual('archived',result['storage'])

    def test_metadata_read_denial_reports_the_stage_and_path(self):
        with patch('govoffice.services.document_authoring.read_json',side_effect=PermissionError(13,'거부')):
            with self.assertRaisesRegex(ValueError,'등록 정보 읽기') as context:self.delete()
        self.assertIn('manifest.json',str(context.exception))
        self.assertTrue(self.registry.path(self.m['id']).exists())

    @unittest.skipUnless(os.name=='nt','Windows sharing violation test')
    def test_actual_windows_lock_preserves_registration_then_unlock_allows_move(self):
        import ctypes
        from ctypes import wintypes
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
        kernel.CreateFileW.restype=wintypes.HANDLE;kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        source=self.registry.path(self.m['id']).resolve()
        handle=kernel.CreateFileW(str(source/'template.hwp'),0x80000000,1,None,3,0,None)
        self.assertNotEqual(ctypes.c_void_p(-1).value,handle)
        try:
            with self.assertRaisesRegex(ValueError,'등록 폴더 보관 및 정리') as context:self.delete()
            self.assertIn('오류 번호: 32',str(context.exception))
            self.assertTrue(source.exists())
            self.assertEqual(1,len(self.commands.handle({'action':'authoring_overview'})['templates']))
        finally:kernel.CloseHandle(handle)
        result=self.delete()
        self.assertFalse(source.exists());self.assertEqual('archived',result['storage'])

    @unittest.skipUnless(os.name=='nt','Windows directory handle test')
    def test_open_child_directory_is_really_archived_and_removed(self):
        import ctypes
        from ctypes import wintypes
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
        kernel.CreateFileW.restype=wintypes.HANDLE;kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        source=self.registry.path(self.m['id']).resolve();(source/'guides').mkdir(exist_ok=True)
        (source/'guides/probe.md').write_text('보존할 작성요령',encoding='utf-8')
        before={str(p.relative_to(source)):p.read_bytes() for p in source.rglob('*') if p.is_file()}
        handle=kernel.CreateFileW(str(source/'guides'),1,7,None,3,0x02000000,None)
        self.assertNotEqual(ctypes.c_void_p(-1).value,handle)
        try:
            with self.assertRaises(OSError) as caught:source.rename(source.with_name('probe_destination'))
            self.assertEqual(5,caught.exception.winerror)
            result=self.delete()
            self.assertFalse(source.exists())
            archive=Path(result['archive_path'])
            self.assertEqual(before,{str(p.relative_to(archive)):p.read_bytes() for p in archive.rglob('*') if p.is_file()})
            self.assertEqual([],self.commands.handle({'action':'authoring_overview'})['templates'])
        finally:kernel.CloseHandle(handle)

    def test_archive_copy_failure_preserves_registration(self):
        error=PermissionError(13,'거부');error.winerror=5
        source=self.registry.path(self.m['id'])
        with patch.object(Path,'rename',side_effect=error),patch('govoffice.services.document_authoring.time.sleep'),patch(
                'govoffice.services.template_archive.shutil.copytree',side_effect=OSError('disk full')):
            with self.assertRaisesRegex(ValueError,'등록 폴더 보관 및 정리'):self.delete()
        self.assertEqual(self.m['id'],self.registry.load(self.m['id'])['id'])
        self.assertTrue(source.exists())

    def test_partial_cleanup_failure_restores_missing_files(self):
        error=PermissionError(13,'거부');error.winerror=5
        source=self.registry.path(self.m['id'])
        before={str(p.relative_to(source)):p.read_bytes() for p in source.rglob('*') if p.is_file()}
        def partial_remove(path):
            (path/'source.hwpml').unlink()
            raise PermissionError('synthetic removal denied')
        with patch.object(Path,'rename',side_effect=error),patch('govoffice.services.document_authoring.time.sleep'),patch(
                'govoffice.services.template_archive.shutil.rmtree',side_effect=partial_remove):
            with self.assertRaisesRegex(ValueError,'등록 폴더 정리에 실패'):self.delete()
        self.assertEqual(before,{str(p.relative_to(source)):p.read_bytes() for p in source.rglob('*') if p.is_file()})
        self.assertEqual(1,len(self.commands.handle({'action':'authoring_overview'})['templates']))

    def test_changed_archive_never_removes_registration(self):
        from govoffice.services.template_archive import _inventory
        error=PermissionError(13,'거부');error.winerror=5
        source=self.registry.path(self.m['id'])
        def changed(folder):return _inventory(folder) if folder==source else {}
        with patch.object(Path,'rename',side_effect=error),patch('govoffice.services.document_authoring.time.sleep'),patch(
                'govoffice.services.template_archive._inventory',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'보관본 검증'):self.delete()
        self.assertEqual(self.m['id'],self.registry.load(self.m['id'])['id'])

    def test_nested_junction_blocks_copy_remove(self):
        error=PermissionError(13,'거부');error.winerror=5
        source=self.registry.path(self.m['id']);(source/'linked').mkdir()
        with patch.object(Path,'rename',side_effect=error),patch('govoffice.services.document_authoring.time.sleep'),patch.object(
                Path,'is_junction',lambda p:p==source/'linked'):
            with self.assertRaisesRegex(ValueError,'연결된 파일/폴더'):self.delete()
        self.assertTrue(source.exists())

    def test_failed_deletion_does_not_break_existing_job_snapshot(self):
        service=self.commands.service;service.agent_factory=lambda _:FakeAgent();service.exporter=fake_export
        job=service.create(self.m['id'],{'title':'가상 과제','description':'본문'},review_mode='final_output',external_consent=True)
        with patch.object(Path,'rename',side_effect=PermissionError(13,'거부')):
            with self.assertRaisesRegex(ValueError,'등록 폴더 이동'):self.delete()
        service.start(job['id']);service.workers[job['id']].join(10)
        self.assertEqual('completed',service.status(job['id'])['status'])


if __name__=='__main__':unittest.main()
