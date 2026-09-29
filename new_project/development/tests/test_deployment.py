import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from govoffice.app.deployment import data_directory, pe_machine, security_dll
from govoffice.runtime.recovered_hwp.한컴오피스.recovered_source.common.connection import HwpConnectionMixin


class DeploymentTests(unittest.TestCase):
    def test_development_data_stays_in_existing_config(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {}, clear=True):
            self.assertEqual(Path(folder) / "config", data_directory(Path(folder)))

    def test_installed_releases_share_user_data(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("old", "new"):
                (root / name).mkdir()
                (root / name / "deployment.json").write_text("{}")
            with patch.dict(os.environ, {"LOCALAPPDATA": str(root / "user")}, clear=True):
                self.assertEqual(data_directory(root / "old"), data_directory(root / "new"))
                self.assertEqual(root / "user/GovOffice/data", data_directory(root / "new"))

    def test_override_isolates_test_data(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"GOVOFFICE_DATA_DIR": folder}):
            self.assertEqual(Path(folder).resolve(), data_directory())

    def test_corrupt_dll_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            dll = Path(folder) / "broken.dll"
            dll.write_bytes(b"not a library")
            with self.assertRaises(RuntimeError):
                pe_machine(dll)

    def test_development_uses_sibling_runtime_but_release_requires_own_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root / 'new_project'
            project.mkdir()
            sibling = root / 'runtime/HwpAutomation/FilePathCheckerModuleExample.dll'
            sibling.parent.mkdir(parents=True)
            sibling.write_bytes(b'fixture')
            self.assertEqual(sibling, security_dll(project))
            (project / 'deployment.json').write_text('{}')
            self.assertEqual(project / 'runtime/HwpAutomation/FilePathCheckerModuleExample.dll',
                             security_dll(project))

    def test_false_registration_is_not_success(self):
        connection = HwpConnectionMixin()
        connection.대상 = Mock()
        connection.대상.RegisterModule.return_value = False
        with patch('govoffice.app.deployment.register_security', return_value='FilePathCheckerModuleExample'):
            with self.assertRaisesRegex(RuntimeError, "RegisterModule=False"):
                connection._보안모듈등록()
            connection.대상.RegisterModule.return_value = True
            self.assertTrue(connection._보안모듈등록())
        self.assertEqual(2, connection.대상.RegisterModule.call_count)

    def test_only_successful_exact_instance_is_cached(self):
        connection = HwpConnectionMixin()
        first = Mock()
        first.RegisterModule.return_value = True
        with patch('govoffice.app.deployment.register_security', return_value='FilePathCheckerModuleExample'):
            connection.대상 = first
            connection._보안모듈등록()
            connection._보안모듈등록()
            self.assertEqual(1, first.RegisterModule.call_count)
            second = Mock()
            second.RegisterModule.return_value = False
            connection.대상 = second
            with self.assertRaises(RuntimeError):
                connection._보안모듈등록()


if __name__ == "__main__":
    unittest.main()
