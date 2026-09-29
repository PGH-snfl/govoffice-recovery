import os
import shutil
import subprocess
import unittest
from pathlib import Path


class ProfileTableUITest(unittest.TestCase):
    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows WPF required')
    def test_modeless_workspaces_keep_other_windows_operable(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/workspace_windows_probe.ps1'),
        ], capture_output=True, timeout=20)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'WORKSPACE_WINDOWS_OK', result.stdout)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows WPF required')
    def test_new_value_manager_uses_shared_tree_and_keeps_existing_actions(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/document_field_manager_probe.ps1'),
        ], capture_output=True, timeout=20)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'DOCUMENT_FIELD_MANAGER_OK', result.stdout)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows WPF required')
    def test_resizable_headers_and_personal_tree(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/profile_layout_probe.ps1'),
            '-Project', str(project),
        ], capture_output=True, timeout=25)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'PROFILE_LAYOUT_OK', result.stdout)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows WPF required')
    def test_reopening_dialogs_across_dispatcher_turns_preserves_main_input(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/profile_reopen_lifecycle_probe.ps1'),
            '-Source', str(project / 'launch_gui.ps1'),
        ], capture_output=True, timeout=30)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'WINDOW_LIFECYCLE_OK', result.stdout)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows PowerShell required')
    def test_review_pauses_polling_and_restores_it_on_close_or_error(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/profile_review_isolation_probe.ps1'),
            '-Source', str(project / 'profile_table_ui.ps1'),
            '-Launcher', str(project / 'launch_gui.ps1'),
        ], capture_output=True, timeout=15)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'PROFILE_REVIEW_ISOLATION_OK', result.stdout)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows WPF required')
    def test_pending_backend_does_not_block_dispatcher_or_interleave_requests(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/backend_responsiveness_probe.ps1'),
            '-Source', str(project / 'launch_gui.ps1'),
        ], capture_output=True, timeout=15)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'BACKEND_RESPONSIVE_OK', result.stdout)

    @unittest.skipUnless(os.name == 'nt' and shutil.which('powershell.exe'), 'Windows WPF required')
    def test_production_merged_cells_drag_context_and_import_handlers(self):
        project = Path(__file__).resolve().parents[2]
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-STA', '-ExecutionPolicy', 'Bypass',
            '-File', str(project / 'development/tests/profile_table_ui_probe.ps1'),
            '-Source', str(project / 'profile_table_ui.ps1'),
        ], capture_output=True, timeout=30)
        self.assertEqual(0, result.returncode, (result.stdout + result.stderr).decode('utf-8', errors='replace'))
        self.assertIn(b'PROFILE_TABLE_UI_OK', result.stdout)

    def test_launcher_and_internal_copy_include_new_tools(self):
        project = Path(__file__).resolve().parents[2]
        source = (project / 'launch_gui.ps1').read_text(encoding='utf-8-sig')
        self.assertIn(". (Join-Path $ProjectDir 'profile_table_ui.ps1')", source)
        self.assertIn('Open-ProfileSelectionImport $Window', source)
        self.assertIn('Open-ProfileDataTable $Window', source)
        self.assertTrue((project / 'profile_table_ui.ps1').read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertIn('"profile_table_ui.ps1"', (project / 'packaging/build_internal_release.py').read_text(encoding='utf-8'))
