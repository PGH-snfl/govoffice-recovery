import subprocess
import sys
import unittest
from pathlib import Path


class WorkerCacheTests(unittest.TestCase):
    def test_all_standalone_hwp_helpers_initialize_their_own_cache(self):
        adapters=Path(__file__).resolve().parents[2]/'src/govoffice/adapters'
        for name in ('hwp_form_export.py','hwp_template_import.py','hwp_output_open.py'):
            source=(adapters/name).read_text(encoding='utf-8').split("if __name__ == '__main__':",1)[1]
            with self.subTest(helper=name):
                self.assertIn('TemporaryDirectory(',source)
                self.assertLess(source.index('configure_worker_cache(Path('),source.index('worker('))

    def test_desktop_backend_configures_before_importing_hwp_libraries(self):
        source=(Path(__file__).resolve().parents[2]/'gui_backend.py').read_text(encoding='utf-8')
        self.assertLess(source.index('configure_worker_cache(Path('),source.index('from govoffice.adapters.recovered_hwp'))
        self.assertIn('_연결캐시.cleanup()',source)

    def test_fresh_process_isolates_generated_code_without_modifying_shared_cache(self):
        src=str(Path(__file__).resolve().parents[2]/'src')
        script=f'''
import sys,tempfile
from pathlib import Path
sys.path.insert(0,{src!r})
import win32com
shared=win32com.__gen_path__
from govoffice.adapters.com_worker_cache import configure_worker_cache
with tempfile.TemporaryDirectory() as t:
    target=configure_worker_cache(Path(t)/'gen_py')
    import win32com.client.gencache as cache
    assert win32com.__gen_path__==str(target)
    assert list(win32com.gen_py.__path__)==[str(target)]
    assert str(target)!=shared
    assert Path(cache.GetGeneratePath())==target
    try:configure_worker_cache(Path(t)/'other')
    except RuntimeError:pass
    else:raise AssertionError('Late cache changes must be refused')
print('PRIVATE_COM_CACHE_OK')
'''
        result=subprocess.run([sys.executable,'-X','utf8','-c',script],capture_output=True,text=True,timeout=15)
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertIn('PRIVATE_COM_CACHE_OK',result.stdout)


if __name__=='__main__':unittest.main()
