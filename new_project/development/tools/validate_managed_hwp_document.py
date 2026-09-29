"""프로그램 전용 한글 문서의 열기/창 제어/폐기 종료를 실제 COM에서 검증한다.

이 스크립트는 원본 자산을 직접 열거나 저장하지 않는다. 고유한 임시 디렉터리에
복사한 문서만 ``복구한글어댑터.관리문서열기``로 열며, 검증 전에 존재하던 Hwp.exe
프로세스에는 닫기나 강제 종료 명령을 보내지 않는다.

실행 결과는 표준 출력에 JSON 한 건으로 출력하며 성공은 종료 코드 0, 실패는 1이다.
실제 한글 COM을 실행하므로 자동 단위 테스트에서는 호출하지 않는다.
"""

from __future__ import annotations

import argparse
import ctypes
import gc
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
import traceback
import uuid
from ctypes import wintypes
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from govoffice.adapters.recovered_hwp import 복구한글어댑터  # noqa: E402


TH32CS_SNAPPROCESS = 0x00000002
MAX_PATH = 260
DEFAULT_TIMEOUT_SECONDS = 12.0
SUPPORTED_EXTENSIONS = {".hwp", ".hwpx"}


class 검증실패(RuntimeError):
    """기능 동작이 검증 조건과 다를 때 사용한다."""


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", wintypes.WPARAM),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * MAX_PATH),
    ]


def _windows_api() -> tuple[Any, Any]:
    if os.name != "nt":
        raise RuntimeError("이 검증은 Windows 한글 COM 환경에서만 실행할 수 있습니다.")
    return ctypes.WinDLL("kernel32", use_last_error=True), ctypes.WinDLL(
        "user32", use_last_error=True
    )


def hwp_process_ids() -> set[int]:
    """Toolhelp 스냅샷으로 현재 Hwp.exe PID만 반환한다."""

    kernel32, _ = _windows_api()
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32FirstW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL

    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    invalid_handle = ctypes.c_void_p(-1).value
    if snapshot in (None, 0, invalid_handle):
        raise OSError(ctypes.get_last_error(), "프로세스 스냅샷을 만들지 못했습니다.")

    result: set[int] = set()
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(entry)
    try:
        has_entry = bool(kernel32.Process32FirstW(snapshot, ctypes.byref(entry)))
        while has_entry:
            if entry.szExeFile.casefold() == "hwp.exe":
                result.add(int(entry.th32ProcessID))
            has_entry = bool(kernel32.Process32NextW(snapshot, ctypes.byref(entry)))
    finally:
        kernel32.CloseHandle(snapshot)
    return result


def hwp_windows() -> list[dict[str, Any]]:
    """Hwp.exe 소유 최상위 창을 열거한다.

    기존 사용자 문서 제목은 결과 보고서에 기록하지 않는다. 제목은 고유한 테스트
    사본의 창을 찾는 동안 메모리에서만 비교한다.
    """

    _, user32 = _windows_api()
    hwp_pids = hwp_process_ids()
    result: list[dict[str, Any]] = []

    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowTextW.restype = ctypes.c_int
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.IsIconic.restype = wintypes.BOOL

    def collect(hwnd: int, _lparam: int) -> bool:
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if int(pid.value) not in hwp_pids:
            return True
        title_length = int(user32.GetWindowTextLengthW(hwnd))
        title_buffer = ctypes.create_unicode_buffer(max(1, title_length + 1))
        if title_length:
            user32.GetWindowTextW(hwnd, title_buffer, len(title_buffer))
        result.append(
            {
                "hwnd": int(hwnd),
                "pid": int(pid.value),
                "title": title_buffer.value,
                "visible": bool(user32.IsWindowVisible(hwnd)),
                "minimized": bool(user32.IsIconic(hwnd)),
            }
        )
        return True

    callback = callback_type(collect)
    if not user32.EnumWindows(callback, 0):
        raise OSError(ctypes.get_last_error(), "한글 창을 열거하지 못했습니다.")
    return result


def wait_for(
    probe: Callable[[], Any],
    predicate: Callable[[Any], bool],
    *,
    timeout: float,
    description: str,
) -> Any:
    deadline = time.monotonic() + timeout
    last_value: Any = None
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            last_value = probe()
            if predicate(last_value):
                return last_value
        except Exception as error:  # COM/창 상태 전환 중의 일시적 오류는 재시도한다.
            last_error = error
        time.sleep(0.2)
    detail = f" 마지막 값={last_value!r}"
    if last_error is not None:
        detail += f", 마지막 오류={last_error}"
    raise 검증실패(f"{description} 확인 시간이 초과되었습니다.{detail}")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def select_sample(argument: str | None) -> Path:
    if argument:
        sample = Path(argument).expanduser().resolve(strict=True)
    else:
        preferred = PROJECT / "assets" / "icons" / "지자체탭" / "인천" / "인천참석명단.hwp"
        if preferred.is_file():
            sample = preferred.resolve(strict=True)
        else:
            candidates = [
                path
                for path in (PROJECT / "assets").rglob("*")
                if path.is_file() and path.suffix.casefold() in SUPPORTED_EXTENSIONS
            ]
            if not candidates:
                raise FileNotFoundError("검증에 사용할 .hwp/.hwpx 자산을 찾지 못했습니다.")
            sample = min(candidates, key=lambda path: path.stat().st_size).resolve(strict=True)
    if not sample.is_file() or sample.suffix.casefold() not in SUPPORTED_EXTENSIONS:
        raise ValueError("검증 문서는 존재하는 .hwp 또는 .hwpx 파일이어야 합니다.")
    return sample


def state_path_matches(state: dict[str, Any], expected: Path) -> bool:
    value = state.get("path")
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        return Path(value).resolve(strict=False) == expected.resolve(strict=False)
    except (OSError, ValueError):
        return False


def find_managed_window(
    windows: list[dict[str, Any]],
    *,
    copy_path: Path,
    before_handles: set[int],
    new_pids: set[int],
) -> dict[str, Any] | None:
    """고유 사본 제목을 우선하고, 새 PID/새 핸들은 보조 조건으로 사용한다."""

    stem = copy_path.stem.casefold()
    title_matches = [window for window in windows if stem in str(window["title"]).casefold()]
    isolated_matches = [
        window
        for window in title_matches
        if int(window["pid"]) in new_pids or int(window["hwnd"]) not in before_handles
    ]
    candidates = isolated_matches or title_matches
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        fallback = [
            window
            for window in windows
            if int(window["pid"]) in new_pids and int(window["hwnd"]) not in before_handles
        ]
        if len(fallback) == 1:
            return fallback[0]
    return None


def check(report: dict[str, Any], name: str, condition: bool, message: str) -> None:
    report.setdefault("checks", {})[name] = bool(condition)
    if not condition:
        raise 검증실패(message)


def run_validation(sample_argument: str | None, timeout: float) -> tuple[dict[str, Any], int]:
    report: dict[str, Any] = {
        "feature": "managed_hwp_document_window_lifecycle",
        "ok": False,
        "exit_code": 1,
        "checks": {},
    }
    adapter: 복구한글어댑터 | None = None
    source: Path | None = None
    source_hash_before: str | None = None
    copy_path: Path | None = None
    work_dir: Path | None = None
    managed_hwnd: int | None = None
    before_pids: set[int] = set()
    new_pids: set[int] = set()
    closed_normally = False

    try:
        source = select_sample(sample_argument)
        source_hash_before = file_sha256(source)
        report.update(
            {
                "source": str(source),
                "source_sha256_before": source_hash_before,
                "timeout_seconds": timeout,
            }
        )

        temp_parent = PROJECT / "development" / "reports" / "dynamic_validation"
        temp_parent.mkdir(parents=True, exist_ok=True)
        work_dir = Path(tempfile.mkdtemp(prefix="managed_hwp_", dir=temp_parent))
        copy_path = work_dir / f"govoffice_managed_validation_{uuid.uuid4().hex[:12]}{source.suffix.lower()}"
        shutil.copy2(source, copy_path)
        report["temporary_copy"] = str(copy_path)
        check(report, "temporary_copy_is_distinct", copy_path != source, "원본과 다른 임시 사본을 만들지 못했습니다.")
        check(
            report,
            "temporary_copy_matches_source",
            file_sha256(copy_path) == source_hash_before,
            "임시 사본의 내용이 원본과 다릅니다.",
        )

        before_pids = hwp_process_ids()
        before_windows = hwp_windows()
        before_handles = {int(window["hwnd"]) for window in before_windows}
        # 개인정보가 될 수 있는 기존 문서 제목은 JSON에 포함하지 않는다.
        report["preexisting_hwp_pids"] = sorted(before_pids)
        report["preexisting_hwp_window_count"] = len(before_windows)

        adapter = 복구한글어댑터()
        opened = adapter.관리문서열기(copy_path, 표시=True)
        status = adapter.문서상태()
        report["opened_state"] = status
        check(report, "open_returned_managed", opened.get("managed") is True, "열기 결과가 관리 문서가 아닙니다.")
        check(report, "status_connected", status.get("connected") is True, "문서 상태가 연결됨이 아닙니다.")
        check(report, "status_managed", status.get("managed") is True, "문서 상태가 프로그램 관리 대상이 아닙니다.")
        check(report, "status_path_matches_copy", state_path_matches(status, copy_path), "문서 상태 경로가 테스트 사본과 다릅니다.")
        check(
            report,
            "dedicated_dispatch_target",
            getattr(adapter, "_관리대상", None)
            is getattr(adapter.원본, "_전용Automation대상", None),
            "관리 대상이 전용 DispatchEx Automation 대상과 일치하지 않습니다.",
        )
        check(
            report,
            "editable_state_is_known",
            isinstance(status.get("editable"), bool),
            "편집 가능 여부가 True/False로 확인되지 않았습니다.",
        )

        after_open_pids = hwp_process_ids()
        new_pids = after_open_pids - before_pids
        report["dedicated_candidate_pids"] = sorted(new_pids)

        managed_window = wait_for(
            lambda: find_managed_window(
                hwp_windows(),
                copy_path=copy_path,
                before_handles=before_handles,
                new_pids=new_pids,
            ),
            lambda value: value is not None,
            timeout=timeout,
            description="프로그램이 연 테스트 문서 창 식별",
        )
        managed_hwnd = int(managed_window["hwnd"])
        report["managed_window"] = {
            "hwnd": managed_hwnd,
            "pid": int(managed_window["pid"]),
            "title": str(managed_window["title"]),
        }
        check(
            report,
            "managed_window_isolated",
            managed_hwnd not in before_handles,
            "기존 사용자 한글 창이 관리 창으로 선택되었습니다.",
        )

        adapter.문서최소화()
        minimized = wait_for(
            lambda: (
                adapter.문서상태(),
                next((window for window in hwp_windows() if int(window["hwnd"]) == managed_hwnd), None),
            ),
            lambda value: value[0].get("minimized") is True
            and value[1] is not None
            and value[1]["minimized"] is True,
            timeout=timeout,
            description="관리 문서 최소화",
        )
        report["minimized_state"] = minimized[0]
        check(report, "window_minimized", True, "관리 문서가 최소화되지 않았습니다.")

        adapter.문서표시()
        restored = wait_for(
            lambda: (
                adapter.문서상태(),
                next((window for window in hwp_windows() if int(window["hwnd"]) == managed_hwnd), None),
            ),
            lambda value: value[0].get("minimized") is False
            and value[1] is not None
            and value[1]["minimized"] is False
            and value[1]["visible"] is True,
            timeout=timeout,
            description="관리 문서 복원 및 표시",
        )
        report["restored_state"] = restored[0]
        check(report, "window_restored_visible", True, "관리 문서가 화면에 복원되지 않았습니다.")

        marker = f"[범정부오피스 폐기 검증 {uuid.uuid4().hex}]"
        adapter.문장(marker)
        modified_state = wait_for(
            adapter.문서상태,
            lambda value: value.get("modified") is True,
            timeout=timeout,
            description="테스트 사본 수정 상태",
        )
        report["modified_state"] = modified_state
        check(report, "copy_became_modified", True, "테스트 사본의 수정 상태를 확인하지 못했습니다.")

        closed = adapter.관리문서닫기(False)
        closed_normally = closed.get("closed") is True
        report["closed_state"] = closed
        check(report, "closed_without_save", closed_normally, "관리 문서를 폐기 종료하지 못했습니다.")
        check(
            report,
            "changes_were_discarded",
            closed.get("saved_changes") is False and closed.get("discarded_changes") is True,
            "수정 내용을 저장하지 않고 폐기했다는 결과가 확인되지 않았습니다.",
        )

        wait_for(
            hwp_windows,
            lambda windows: all(int(window["hwnd"]) != managed_hwnd for window in windows),
            timeout=timeout,
            description="관리 문서 창 종료",
        )
        check(report, "managed_window_closed", True, "관리 문서 창이 종료되지 않았습니다.")

        if new_pids:
            wait_for(
                hwp_process_ids,
                lambda pids: not bool(new_pids & pids),
                timeout=timeout,
                description="전용 한글 프로세스 종료",
            )
        check(report, "dedicated_processes_closed", True, "전용 한글 프로세스가 종료되지 않았습니다.")

    except Exception as error:
        report.update(
            {
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
            }
        )
    finally:
        # 실패했더라도 이 어댑터가 직접 연 관리 문서만 폐기 종료한다. PID 기반
        # 강제 종료는 사용하지 않으므로 기존 사용자 문서는 이 경로로 닫히지 않는다.
        if adapter is not None and not closed_normally:
            try:
                emergency_close = adapter.관리문서닫기(False)
                report["failure_cleanup_close"] = emergency_close.get("closed") is True
            except Exception as cleanup_error:
                report["failure_cleanup_close"] = False
                report["failure_cleanup_close_error"] = str(cleanup_error)
        adapter = None
        gc.collect()

        try:
            final_pids = hwp_process_ids() if os.name == "nt" else set()
            manual_preserved = before_pids <= final_pids
            report["final_hwp_pids"] = sorted(final_pids)
            report["checks"]["preexisting_hwp_processes_preserved"] = manual_preserved
        except Exception as process_error:
            manual_preserved = False
            report["checks"]["preexisting_hwp_processes_preserved"] = False
            report["process_cleanup_check_error"] = str(process_error)

        source_unchanged = False
        if source is not None and source_hash_before is not None:
            try:
                source_hash_after = file_sha256(source)
                report["source_sha256_after"] = source_hash_after
                source_unchanged = source_hash_after == source_hash_before
            except Exception as hash_error:
                report["source_hash_after_error"] = str(hash_error)
        report["checks"]["source_file_unchanged"] = source_unchanged

        copy_removed = copy_path is None
        if copy_path is not None:
            try:
                copy_path.unlink(missing_ok=True)
                copy_removed = not copy_path.exists()
            except Exception as cleanup_error:
                report["temporary_copy_cleanup_error"] = str(cleanup_error)
                copy_removed = False
        report["checks"]["temporary_copy_removed"] = copy_removed

        work_dir_removed = work_dir is None
        if work_dir is not None:
            try:
                work_dir.rmdir()
                work_dir_removed = not work_dir.exists()
            except Exception as cleanup_error:
                report["temporary_directory_cleanup_error"] = str(cleanup_error)
                work_dir_removed = False
        report["checks"]["temporary_directory_removed"] = work_dir_removed

        report["ok"] = bool(report["checks"]) and all(report["checks"].values()) and "error" not in report
        report["exit_code"] = 0 if report["ok"] else 1

    return report, int(report["exit_code"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="복구한글어댑터의 전용 문서 열기·최소화·복원·폐기 종료를 검증합니다."
    )
    parser.add_argument(
        "sample",
        nargs="?",
        help="원본을 직접 수정하지 않고 임시 사본으로 사용할 .hwp/.hwpx 경로",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"각 창/COM 상태 전환 대기 시간(초, 기본 {DEFAULT_TIMEOUT_SECONDS:g})",
    )
    arguments = parser.parse_args()
    if arguments.timeout <= 0:
        parser.error("--timeout은 0보다 커야 합니다.")
    return arguments


def main() -> None:
    arguments = parse_args()
    report, exit_code = run_validation(arguments.sample, arguments.timeout)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
