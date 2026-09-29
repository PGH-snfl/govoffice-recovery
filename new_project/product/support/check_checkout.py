"""Check a downloaded checkout without opening HWP or registering modules."""
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[2]
WORKSPACE = PROJECT.parent
sys.path.insert(0, str(PROJECT / 'src'))


def check(offline=False):
    checks = []

    def run(name, action):
        try:
            detail = action()
            checks.append({'name': name, 'ok': True, 'detail': str(detail)})
        except Exception as error:
            checks.append({'name': name, 'ok': False, 'detail': str(error)})

    def runtime():
        if os.name != 'nt' or sys.version_info[:2] != (3, 13) or struct.calcsize('P') != 8:
            raise RuntimeError('Windows 64비트의 포함된 Python 3.13 실행환경이 필요합니다.')
        for module in ('pythoncom', 'pywintypes', 'win32com.client'):
            importlib.import_module(module)
        return 'Windows / Python 3.13 64비트 / 한글 자동화 연결 라이브러리'

    def resources():
        required = (
            'launch_gui.ps1', 'gui_backend.py', 'gui_poll_guard.cs',
            'favorites_ui.ps1', 'workspace_windows.ps1', 'profile_table_ui.ps1',
            'document_authoring_ui.ps1', 'document_authoring_flow_ui.ps1',
            'config/original_layout.json', 'assets/icons',
            'src/govoffice/runtime/recovered_hwp/catalog/verified_methods.json',
            'src/govoffice/institutions/packages/seoultech/climate_2026/template.hwp',
            'src/govoffice/institutions/packages/seoultech/climate_2026/source.hwpml',
        )
        missing = [p for p in required if not (PROJECT / p).exists()]
        if missing:
            raise RuntimeError('누락: ' + ', '.join(missing))
        from govoffice.app.deployment import security_dll
        if not security_dll(PROJECT).is_file():
            raise RuntimeError('한글 보안 모듈이 없습니다.')
        from govoffice.app.function_catalog import 검증완료기능목록
        return f'필수 화면·양식·보안 모듈 확인, 기능 {len(검증완료기능목록())}개'

    def encoding():
        scripts = list(PROJECT.glob('*.ps1'))
        for path in scripts:
            data = path.read_bytes()
            text = data.decode('utf-8-sig')
            if any(ord(c) > 127 for c in text) and not data.startswith(b'\xef\xbb\xbf'):
                raise RuntimeError(f'Windows PowerShell용 한글 인코딩 표시 누락: {path.name}')
        return '한글 화면 스크립트 인코딩 확인'

    def writable():
        from govoffice.app.deployment import data_directory
        directory = data_directory(PROJECT)
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=directory) as stream:
            stream.write(b'GovOffice')
        return '사용자 데이터 저장 가능(기존 파일 변경 없음)'

    def powershell():
        host = Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
        result = subprocess.run(
            [str(host), '-NoProfile', '-NonInteractive', '-Command',
             "Add-Type -AssemblyName PresentationFramework; Write-Output 'WPF_OK'"],
            capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode or b'WPF_OK' not in result.stdout:
            raise RuntimeError('Windows 화면 구성 라이브러리를 불러오지 못했습니다.')
        return 'Windows 화면 구성 사용 가능'

    run('실행환경', runtime)
    run('프로젝트 필수 파일', resources)
    run('한글 인코딩', encoding)
    run('화면 환경', powershell)
    run('사용자 데이터 저장', writable)
    if not offline:
        from govoffice.app.deployment import hwp_executable, pe_machine, security_dll

        def hancom():
            executable = hwp_executable()
            if pe_machine(executable) != pe_machine(security_dll(PROJECT)):
                raise RuntimeError('설치된 한글과 포함된 보안 모듈의 32/64비트가 다릅니다.')
            return '한글 등록·보안 모듈 비트수 일치(실제 문서 작업은 별도 확인 필요)'
        run('한글 설치', hancom)
    from govoffice.adapters.codex_author import find_codex
    optional_ai = bool(find_codex())
    return {'ok': all(c['ok'] for c in checks), 'checks': checks,
            'optional_ai_executable_found': optional_ai, 'ai_login_checked': False,
            'hwp_document_execution_tested': False, 'offline': offline}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    report = check(args.offline)
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        for item in report['checks']:
            print(f"[{'통과' if item['ok'] else '확인 필요'}] {item['name']}: {item['detail']}")
        print('선택 기능: 인공지능 작성은 별도 Codex 설치·사용자 로그인 확인이 필요합니다.')
        print('한글 문서 열기·레지스트리 변경·인공지능 호출은 수행하지 않았습니다.')
        print('시작 안내: docs/GETTING_STARTED.md')
    raise SystemExit(0 if report['ok'] else 1)
