"""Bounded installation diagnostics. Does not open or close any HWP documents."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from govoffice.app.deployment import data_directory, hwp_executable, pe_machine, register_security, security_dll


def check(register=False, offline=False):
    checks = []
    def run(name, operation):
        try:
            detail = operation()
            checks.append(dict(name=name, ok=True, detail=str(detail or "확인 완료")))
        except Exception as error:
            checks.append(dict(name=name, ok=False, detail=str(error)))

    def resources():
        required = ("launch_gui.ps1", "favorites_ui.ps1", "gui_backend.py", "config/original_layout.json",
                    "src/govoffice/runtime/recovered_hwp/catalog/verified_methods.json")
        for name in required:
            if not (ROOT / name).is_file():
                raise RuntimeError(f"설치 파일 누락: {name}")
        if not any((ROOT / "assets/icons").rglob("*.png")):
            raise RuntimeError("화면 이미지가 없습니다.")
        return "화면 및 기능 파일 확인"

    def writable():
        directory = data_directory(ROOT)
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=directory) as stream:
            stream.write(b"GovOffice")
        return directory

    def runtime():
        if sys.version_info[:2] != (3, 13):
            raise RuntimeError("배포판 Python 3.13으로 실행하세요.")
        import pythoncom
        import win32com.client
        import pywintypes
        return sys.version.split()[0]

    def dll_load():
        dll = security_dll(ROOT)
        machine = pe_machine(dll)
        if machine != pe_machine(hwp_executable()):
            raise RuntimeError("한글과 보안 모듈 비트수가 일치하지 않습니다.")
        windows = Path(os.environ["SystemRoot"])
        host = windows / ("SysWOW64" if machine == 0x14C else "System32") / "WindowsPowerShell/v1.0/powershell.exe"
        result = subprocess.run([str(host), "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File",
                                 str(ROOT / "product/support/probe_security_dll.ps1"), "-DllPath", str(dll)],
                                capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
        output = result.stdout.decode("utf-8", errors="replace").strip()
        if result.returncode or "DLL_OK" not in output:
            raise RuntimeError("보안 DLL 로딩 실패: " + output + " (126: 파일/의존 DLL 누락, 193: 비트수 불일치)")
        return "DLL 로딩 및 IsAccessiblePath 함수 확인"

    run("필수 파일", resources)
    run("Python/COM 라이브러리", runtime)
    run("사용자 데이터 저장", writable)
    if not offline:
        run("한글 설치", hwp_executable)
        run("보안 모듈 로딩", dll_load)
        if register and all(item["ok"] for item in checks):
            run("현재 사용자 보안 모듈 등록", lambda: register_security(ROOT))
    return dict(ok=all(item["ok"] for item in checks), checks=checks,
                hwp_execution_tested=False, offline=offline)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--offline", action="store_true", help="파일 및 런타임만 확인; 한글과 레지스트리는 접근하지 않음")
    args = parser.parse_args()
    report = check(args.register, args.offline)
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(0 if report["ok"] else 1)
