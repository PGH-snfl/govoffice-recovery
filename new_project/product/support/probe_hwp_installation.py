"""Explicit, isolated HWP smoke test with a 40 second parent deadline.

Only the dedicated instance returned by the application connection is used.
An ambiguous timeout is reported, never retried; existing HWP processes are untouched.
"""
from __future__ import annotations
import ctypes
import gc
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if "--project" in sys.argv:
    ROOT = Path(sys.argv[sys.argv.index("--project") + 1]).resolve()
sys.path.insert(0, str(ROOT / "src"))
from govoffice.runtime.recovered_hwp.한컴오피스.recovered_source.common.connection import HwpConnectionMixin


def worker():
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    api.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
    api.CreateMutexW.restype = ctypes.c_void_p
    api.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    api.ReleaseMutex.argtypes = [ctypes.c_void_p]
    api.CloseHandle.argtypes = [ctypes.c_void_p]
    mutex = api.CreateMutexW(None, False, "Local\\GovOfficeRecoveredApplication")
    if not mutex:
        raise RuntimeError("실행 잠금을 확인하지 못했습니다.")
    acquired = api.WaitForSingleObject(mutex, 0) in (0, 0x80)
    if not acquired:
        api.CloseHandle(mutex)
        raise RuntimeError("범정부오피스가 실행 중입니다. 종료 후 설치 검증을 실행하세요.")
    import pythoncom
    pythoncom.CoInitialize()
    connection = HwpConnectionMixin()
    try:
        before = connection._한글프로세스식별자목록()
        if before is None or len(before) >= 10:
            raise RuntimeError("한글 프로세스 수를 확인할 수 없거나 10개 제한에 도달했습니다.")
        print(json.dumps(dict(stage="connecting", existing=len(before))), flush=True)
        hwp = connection._새한글()
        print(json.dumps(dict(stage="registered", identity=connection._전용Automation프로세스식별자)), flush=True)
        with tempfile.TemporaryDirectory(prefix="GovOffice-HWP-") as folder:
            action = hwp.CreateAction("InsertText")
            parameters = action.CreateSet()
            action.GetDefault(parameters)
            parameters.SetItem("Text", "GovOffice installation test")
            if not action.Execute(parameters):
                raise RuntimeError("문자 입력 실패")
            output = Path(folder) / "test.hwp"
            if not hwp.SaveAs(str(output), "HWP", "") or not output.is_file():
                raise RuntimeError("한글 파일 저장 실패")
            action = parameters = None
            identity = connection._전용Automation프로세스식별자
            connection._전용Automation대상안전종료(hwp, identity)
            connection.대상 = connection._전용Automation대상 = connection._보안등록성공대상 = None
            connection._전용Automation프로세스식별자 = None
            hwp = None
            print(json.dumps(dict(ok=True, registered=True, inserted=True, saved=True, process_exited=True)), flush=True)
    finally:
        if connection._전용Automation대상 is not None and connection._전용Automation프로세스식별자 is not None:
            connection._전용Automation대상안전종료(connection._전용Automation대상, connection._전용Automation프로세스식별자)
        gc.collect()
        pythoncom.CoUninitialize()
        api.ReleaseMutex(mutex)
        api.CloseHandle(mutex)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--worker" in sys.argv:
        try:
            worker()
        except Exception as error:
            print(json.dumps(dict(ok=False, error=str(error)), ensure_ascii=False), flush=True)
            raise SystemExit(1)
    else:
        try:
            result = subprocess.run([sys.executable, "-X", "utf8", __file__, *sys.argv[1:], "--worker"],
                                    capture_output=True, encoding="utf-8", timeout=40,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            raise SystemExit(result.returncode)
        except subprocess.TimeoutExpired as error:
            print(json.dumps(dict(ok=False, error="한글 응답 40초 초과. 자동 재시도하지 않습니다. 열린 한글 상태를 확인하세요.",
                                  stages=(error.stdout or b"").decode("utf-8", errors="replace")), ensure_ascii=False))
            raise SystemExit(1)
