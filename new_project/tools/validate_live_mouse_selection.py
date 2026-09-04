"""실제 Hwp 창에서 마우스 드래그 후 선택 블록/HWPML을 검증한다."""

from __future__ import annotations

import ctypes
import gc
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from ctypes import wintypes
from pathlib import Path

import pythoncom
from win32com.client import DispatchEx
from win32com.client.gencache import EnsureDispatch


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

from govoffice.adapters.recovered_hwp import 복구한글어댑터  # noqa: E402


TEST_TEXT = "범정부오피스 실제 마우스 드래그 선택 영역 검증 문장입니다. 선택 성공 여부를 확인합니다."
SW_MAXIMIZE = 3
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hwndActive", wintypes.HWND),
        ("hwndFocus", wintypes.HWND),
        ("hwndCapture", wintypes.HWND),
        ("hwndMenuOwner", wintypes.HWND),
        ("hwndMoveSize", wintypes.HWND),
        ("hwndCaret", wintypes.HWND),
        ("rcCaret", RECT),
    ]


user32 = ctypes.WinDLL("user32", use_last_error=True)
user32.EnumWindows.restype = wintypes.BOOL
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.IsWindowVisible.restype = wintypes.BOOL
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowTextW.restype = ctypes.c_int
user32.ShowWindowAsync.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindowAsync.restype = wintypes.BOOL
user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.SetForegroundWindow.restype = wintypes.BOOL
user32.GetGUIThreadInfo.argtypes = [wintypes.DWORD, ctypes.POINTER(GUITHREADINFO)]
user32.GetGUIThreadInfo.restype = wintypes.BOOL
user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(POINT)]
user32.ClientToScreen.restype = wintypes.BOOL
user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SetCursorPos.restype = wintypes.BOOL
user32.mouse_event.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]


def visible_hwp_windows() -> list[tuple[int, int, int, str]]:
    result: list[tuple[int, int, int, str]] = []
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def collect(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        title_length = user32.GetWindowTextLengthW(hwnd)
        if title_length <= 0:
            return True
        title_buffer = ctypes.create_unicode_buffer(title_length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, len(title_buffer))
        pid = wintypes.DWORD()
        thread_id = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        try:
            import subprocess

            name = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", f"(Get-Process -Id {pid.value}).ProcessName"],
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=3,
            ).strip()
        except Exception:
            return True
        if name.casefold() == "hwp":
            result.append((int(hwnd), int(pid.value), int(thread_id), title_buffer.value))
        return True

    callback = callback_type(collect)
    user32.EnumWindows(callback, 0)
    return result


def caret_screen_point(thread_id: int) -> tuple[int, int, int]:
    info = GUITHREADINFO()
    info.cbSize = ctypes.sizeof(info)
    if not user32.GetGUIThreadInfo(thread_id, ctypes.byref(info)) or not info.hwndCaret:
        raise RuntimeError("한글 편집 창의 시스템 캐럿 위치를 가져오지 못했습니다.")
    point = POINT(info.rcCaret.left, (info.rcCaret.top + info.rcCaret.bottom) // 2)
    if not user32.ClientToScreen(info.hwndCaret, ctypes.byref(point)):
        raise RuntimeError("한글 캐럿 좌표를 화면 좌표로 변환하지 못했습니다.")
    return point.x, point.y, int(info.hwndCaret)


def selected_positions(hwp) -> tuple[bool, tuple[int, int, int], tuple[int, int, int]]:
    start = hwp.CreateSet("ListParaPos")
    end = hwp.CreateSet("ListParaPos")
    ok = bool(hwp.GetSelectedPosBySet(start, end))
    start_pos = tuple(int(start.Item(name)) for name in ("List", "Para", "Pos"))
    end_pos = tuple(int(end.Item(name)) for name in ("List", "Para", "Pos"))
    return ok, start_pos, end_pos


def drag_from_caret(caret_x: int, caret_y: int) -> tuple[tuple[int, int], tuple[int, int]]:
    start = (caret_x - 2, caret_y)
    end = (max(20, caret_x - 360), caret_y)
    user32.SetCursorPos(*start)
    time.sleep(0.2)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    for index in range(1, 31):
        x = round(start[0] + (end[0] - start[0]) * index / 30)
        user32.SetCursorPos(x, caret_y)
        time.sleep(0.018)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.5)
    return start, end


def backend_selection_status() -> dict[str, object]:
    process = subprocess.Popen(
        [sys.executable, str(PROJECT / "gui_backend.py")],
        cwd=PROJECT.parent,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        assert process.stdin is not None and process.stdout is not None
        ready = json.loads(process.stdout.readline())
        if not ready.get("ok"):
            raise RuntimeError(f"백엔드 준비 실패: {ready}")
        process.stdin.write(json.dumps({"action": "style_preset_selection_status", "probe": True}) + "\n")
        process.stdin.flush()
        status = json.loads(process.stdout.readline())
        process.stdin.write(json.dumps({"action": "shutdown"}) + "\n")
        process.stdin.flush()
        process.stdout.readline()
        process.wait(timeout=10)
        return status
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)


def main() -> int:
    pythoncom.CoInitialize()
    hwp = None
    result: dict[str, object] = {"ok": False, "test": "actual_mouse_drag"}
    try:
        before_handles = {item[0] for item in visible_hwp_windows()}
        hwp = EnsureDispatch(DispatchEx("HWPFrame.HwpObject"))
        hwp.XHwpWindows.Item(0).Visible = True

        insert = hwp.HParameterSet.HInsertText
        hwp.HAction.GetDefault("InsertText", insert.HSet)
        insert.Text = TEST_TEXT
        if hwp.HAction.Execute("InsertText", insert.HSet) is False:
            raise RuntimeError("한글 테스트 문장을 입력하지 못했습니다.")
        hwp.HAction.Run("MoveDocEnd")
        time.sleep(1.0)

        candidates = [item for item in visible_hwp_windows() if item[0] not in before_handles]
        if not candidates:
            raise RuntimeError("새 테스트 한글 창을 찾지 못했습니다.")
        hwnd, pid, thread_id, title = candidates[-1]
        user32.ShowWindowAsync(hwnd, SW_MAXIMIZE)
        user32.SetForegroundWindow(hwnd)
        time.sleep(1.0)
        hwp.HAction.Run("MoveDocEnd")
        time.sleep(0.4)

        caret_x, caret_y, caret_hwnd = caret_screen_point(thread_id)
        drag_start, drag_end = drag_from_caret(caret_x, caret_y)
        position_ok, start_pos, end_pos = selected_positions(hwp)
        adapter = 복구한글어댑터(type("LiveOriginal", (), {"대상": hwp})())
        hwpml = adapter.선택영역서식내보내기()
        try:
            selected_text = "".join(ET.fromstring(hwpml.lstrip("\ufeff")).itertext())
        except ET.ParseError:
            selected_text = ""
        backend_status = backend_selection_status()

        result.update(
            {
                "ok": (
                    position_ok
                    and start_pos != end_pos
                    and bool(hwpml.strip())
                    and bool(backend_status.get("selection_ready"))
                ),
                "window_pid": pid,
                "window_title": title,
                "caret_hwnd": caret_hwnd,
                "drag_start": drag_start,
                "drag_end": drag_end,
                "selection_start": start_pos,
                "selection_end": end_pos,
                "hwpml_length": len(hwpml),
                "selected_text": selected_text[:120],
                "backend_status": backend_status,
            }
        )
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
    finally:
        print(json.dumps(result, ensure_ascii=False), flush=True)
        if hwp is not None:
            try:
                hwp.Clear(1)
            except Exception:
                pass
            try:
                hwp.Quit()
            except Exception:
                pass
        hwp = None
        gc.collect()
        pythoncom.CoUninitialize()
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
