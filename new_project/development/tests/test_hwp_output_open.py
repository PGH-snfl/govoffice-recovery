import json
from pathlib import Path
import subprocess
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch

from govoffice.adapters.hwp_output_open import _worker, open_output_hwp
from govoffice.services.authoring_commands import AuthoringCommands


class OutputOpenTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.path = self.folder / '공백 [괄호] 출력.hwp'
        self.path.write_bytes(b'test')
        self.state = dict(document_open=True, visible=True, path=str(self.path), editable=True)

    def test_worker_uses_owned_instance_without_closing_documents(self):
        adapter = Mock()
        adapter.관리문서열기.return_value = self.state
        result = _worker(self.path, lambda: adapter)
        adapter.관리문서열기.assert_called_once_with(self.path, 표시=True)
        adapter.관리문서닫기.assert_not_called()
        self.assertEqual(str(self.path), result['path'])

    def test_worker_rejects_wrong_or_invisible_document(self):
        for changed in ({'visible': False}, {'path': str(self.folder/'other.hwp')}):
            adapter = Mock()
            adapter.관리문서열기.return_value = self.state | changed
            with self.assertRaises(RuntimeError):
                _worker(self.path, lambda: adapter)

    def test_subprocess_arguments_and_verified_result(self):
        response = subprocess.CompletedProcess([], 0, json.dumps({'ok': True, 'result': self.state}), '')
        with patch('govoffice.adapters.hwp_output_open.subprocess.run', return_value=response) as run:
            self.assertTrue(open_output_hwp(self.path)['visible'])
        self.assertEqual(str(self.path), run.call_args.args[0][-1])
        self.assertEqual(45, run.call_args.kwargs['timeout'])
        self.assertNotIn('shell', run.call_args.kwargs)

    def test_timeout_and_failed_or_invalid_reply(self):
        with patch('govoffice.adapters.hwp_output_open.subprocess.run', side_effect=subprocess.TimeoutExpired('test', 45)):
            with self.assertRaisesRegex(RuntimeError, '응답시간'):
                open_output_hwp(self.path)
        for code, output in [(1, '{"ok":false,"error":"native failure"}'), (0, 'not json'),
                             (0, json.dumps({'ok': True, 'result': self.state | {'visible': False}}))]:
            with patch('govoffice.adapters.hwp_output_open.subprocess.run', return_value=subprocess.CompletedProcess([], code, output, '')):
                with self.assertRaises(RuntimeError):
                    open_output_hwp(self.path)

    def test_command_is_async_and_resolves_only_completed_job_output(self):
        commands = AuthoringCommands(self.folder)
        self.addCleanup(commands.close)
        job_id = 'a' * 32
        job = commands.service.job_path(job_id)
        job.mkdir(parents=True)
        path = job / 'final.hwp'
        path.write_bytes(b'test')
        statefile = job / 'state.json'
        statefile.write_text(json.dumps({'status': 'completed', 'hwp_path': str(path)}))
        release = threading.Event()
        self.addCleanup(release.set)
        def slow_open(actual):
            self.assertEqual(path, actual)
            release.wait(3)
            return self.state | {'path': str(path)}
        with patch('govoffice.services.authoring_commands.open_output_hwp', side_effect=slow_open):
            result = commands.handle({'action': 'authoring_open_output', 'job_id': job_id})
            self.assertEqual('running', commands.operations[result['operation_id']]['status'])
            release.set()
            for _ in range(100):
                op = commands.operations[result['operation_id']]
                if op['status'] != 'running':
                    break
                time.sleep(.01)
            self.assertEqual('completed', op['status'])
        for status, output in [('running', str(path)), ('completed', str(self.path))]:
            statefile.write_text(json.dumps({'status': status, 'hwp_path': output}))
            with self.assertRaises(ValueError):
                commands.handle({'action': 'authoring_open_output', 'job_id': job_id})


if __name__ == '__main__':
    unittest.main()
