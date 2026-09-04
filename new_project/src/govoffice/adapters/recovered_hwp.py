from __future__ import annotations

import contextlib
import io
import os
import stat
import time
from importlib import import_module
from pathlib import Path
from typing import Any


def _복구클래스() -> type:
    """새 프로젝트 내부에 고정한 검증 복구 패키지를 불러온다."""

    module = import_module("govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리")
    return module.기본한컴


class 복구한글어댑터:
    """새 업무 코드에서 원본 호환 API로 넘어가는 격리 경계."""

    def __init__(self, 대상: Any | None = None) -> None:
        self._대상 = 대상 if 대상 is not None else _복구클래스()()
        # 사용자가 수동으로 연 Hwp 객체와 이 프로그램이 경로로 연 객체를
        # 구분한다. 관리 대상이 있으면 이후 기능도 항상 이 객체를 우선한다.
        self._관리대상: Any | None = None
        self._관리문서경로: Path | None = None
        self._관리문서id: str | None = None
        self._출력문서ids: set[str] = set()
        self._관리이전대상: Any | None = None
        self._관리이전전용대상: Any | None = None
        self._관리이전전용프로세스식별자: tuple[int, int | None] | None = None
        self._관리창핸들: int | None = None
        self._관리창프로세스id: int | None = None
        self._관리프로세스식별자: tuple[int, int | None] | None = None
        self._관리전창핸들: set[int] = set()
        self._관리전프로세스ids: set[int] = set()
        self._관리전프로세스식별자들: set[tuple[int, int | None]] = set()
        # 소유권이 모호해 파괴적 종료를 거부한 COM 프록시는 진단/수동 정리 전까지
        # 참조를 유지한다. 이를 정상 관리 대상으로 재사용하지는 않는다.
        self._안전정리보류대상: Any | None = None
        self._안전정리보류프로세스식별자: tuple[int, int | None] | None = None
        self._창최소화됨 = False

    @property
    def 원본(self) -> Any:
        return self._대상

    def 문장(self, 내용: str) -> None:
        self._대상.문장(내용)

    def 줄바꿈(self) -> None:
        self._대상.대상.HAction.Run("BreakPara")

    def 기능실행(self, 메서드: str, *args, **kwargs):
        return getattr(self._대상, 메서드)(*args, **kwargs)

    @staticmethod
    def _속성(대상: Any, 이름: str, 기본값: Any = None) -> Any:
        try:
            값 = getattr(대상, 이름)
            return 값() if callable(값) and 이름.startswith("Get") else 값
        except Exception:
            return 기본값

    @classmethod
    def _문서객체(cls, 한글: Any) -> Any | None:
        창목록 = cls._속성(한글, "XHwpWindows")
        if 창목록 is not None:
            활성창 = cls._속성(창목록, "Active_XHwpWindow")
            if 활성창 is None:
                try:
                    활성창 = 창목록.Item(0)
                except Exception:
                    pass
            활성문서 = cls._속성(활성창, "Active_XHwpDocument") if 활성창 is not None else None
            if 활성문서 is not None:
                return 활성문서
        문서목록 = cls._속성(한글, "XHwpDocuments")
        if 문서목록 is None:
            return None
        활성문서 = cls._속성(문서목록, "Active_XHwpDocument")
        if 활성문서 is None:
            활성문서 = cls._속성(문서목록, "ActiveDocument")
        if 활성문서 is not None:
            return 활성문서
        try:
            return 문서목록.Item(0)
        except Exception:
            return None

    @classmethod
    def _활성문서객체(cls, 한글: Any) -> Any | None:
        """COM이 명시적으로 보고한 현재 활성 문서만 반환한다.

        ``Item(0)``은 첫 문서일 뿐 활성 문서라는 보장이 없다. 선택 영역 캐시의
        소속 문서를 판정할 때 이를 대신 쓰면 다른 문서의 선택을 재사용할 수
        있으므로, 활성 문서 속성을 읽지 못한 경우에는 보수적으로 ``None``을
        반환한다.
        """

        창목록 = cls._속성(한글, "XHwpWindows")
        if 창목록 is not None:
            활성창 = cls._속성(창목록, "Active_XHwpWindow")
            if 활성창 is not None:
                활성문서 = cls._속성(활성창, "Active_XHwpDocument")
                if 활성문서 is not None:
                    return 활성문서

        문서목록 = cls._속성(한글, "XHwpDocuments")
        if 문서목록 is not None:
            for 이름 in ("Active_XHwpDocument", "ActiveDocument"):
                활성문서 = cls._속성(문서목록, 이름)
                if 활성문서 is not None:
                    return 활성문서
        return None

    @classmethod
    def _문서ID(cls, 문서: Any | None) -> str | None:
        """IXHwpDocument의 안정 ID만 소유권 판단에 사용한다."""

        if 문서 is None:
            return None
        for 이름 in ("DocumentID", "DocumentId"):
            try:
                값 = getattr(문서, 이름)
                if callable(값):
                    값 = 값()
            except Exception:
                continue
            if 값 is None:
                continue
            정리값 = str(값).strip()
            if 정리값:
                return 정리값
        return None

    @classmethod
    def _문서목록(cls, 한글: Any) -> tuple[Any, ...]:
        """0/1 기반 COM 컬렉션을 모두 허용하되 DocumentID로 중복 제거한다."""

        문서컬렉션 = cls._속성(한글, "XHwpDocuments")
        후보: list[Any] = []
        활성문서 = cls._문서객체(한글)
        if 활성문서 is not None:
            후보.append(활성문서)
        if 문서컬렉션 is not None:
            try:
                개수 = int(getattr(문서컬렉션, "Count"))
            except Exception:
                개수 = -1
            if 개수 >= 0:
                for 순번 in range(개수):
                    for 인덱스 in (순번, 순번 + 1):
                        try:
                            문서 = 문서컬렉션.Item(인덱스)
                        except Exception:
                            continue
                        if 문서 is not None:
                            후보.append(문서)

        결과: list[Any] = []
        본ID: set[str] = set()
        본객체: set[int] = set()
        for 문서 in 후보:
            문서id = cls._문서ID(문서)
            if 문서id is not None:
                if 문서id in 본ID:
                    continue
                본ID.add(문서id)
            else:
                객체id = id(문서)
                if 객체id in 본객체:
                    continue
                본객체.add(객체id)
            결과.append(문서)
        return tuple(결과)

    @classmethod
    def _문서ID로찾기(cls, 한글: Any, 문서id: str | None) -> Any | None:
        if not 문서id:
            return None
        return next(
            (문서 for 문서 in cls._문서목록(한글) if cls._문서ID(문서) == 문서id),
            None,
        )

    @staticmethod
    def _문서활성화(문서: Any | None) -> bool:
        if 문서 is None:
            return False
        try:
            활성화 = getattr(문서, "SetActive_XHwpDocument", None)
            if not callable(활성화):
                return False
            결과 = 활성화()
            return 결과 is not False
        except Exception:
            return False

    @classmethod
    def _창객체(cls, 한글: Any) -> Any | None:
        창목록 = cls._속성(한글, "XHwpWindows")
        if 창목록 is None:
            return None
        # 관리 DocumentID를 SetActive한 직후에는 그 문서의 활성 창을 우선한다.
        # Item(0)은 첫 창일 뿐 현재 관리 원문서의 창이라는 보장이 없다.
        for 이름 in ("Active_XHwpWindow", "ActiveWindow"):
            활성창 = cls._속성(창목록, 이름)
            if 활성창 is not None:
                return 활성창
        try:
            return 창목록.Item(0)
        except Exception:
            return None

    @staticmethod
    def _실제COM객체(대상: Any) -> bool:
        """pywin32 프록시인지 확인한다. 가짜 객체 테스트에는 Win32 탐색을 하지 않는다."""

        try:
            return getattr(대상, "_oleobj_", None) is not None
        except Exception:
            return False

    @staticmethod
    def _한글창목록() -> list[dict[str, Any]]:
        """현재 최상위 Hwp.exe 창의 HWND/PID/제목/표시 상태를 반환한다."""

        if os.name != "nt":
            return []
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            콜백형 = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
            user32.EnumWindows.argtypes = [콜백형, wintypes.LPARAM]
            user32.EnumWindows.restype = wintypes.BOOL
            user32.IsWindowVisible.argtypes = [wintypes.HWND]
            user32.IsWindowVisible.restype = wintypes.BOOL
            user32.IsIconic.argtypes = [wintypes.HWND]
            user32.IsIconic.restype = wintypes.BOOL
            user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
            user32.GetWindowTextLengthW.restype = ctypes.c_int
            user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
            user32.GetWindowTextW.restype = ctypes.c_int
            user32.GetWindowThreadProcessId.argtypes = [
                wintypes.HWND,
                ctypes.POINTER(wintypes.DWORD),
            ]
            user32.GetWindowThreadProcessId.restype = wintypes.DWORD
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.QueryFullProcessImageNameW.argtypes = [
                wintypes.HANDLE,
                wintypes.DWORD,
                wintypes.LPWSTR,
                ctypes.POINTER(wintypes.DWORD),
            ]
            kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
            kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel32.CloseHandle.restype = wintypes.BOOL
            프로세스조회 = 0x1000  # PROCESS_QUERY_LIMITED_INFORMATION
            결과: list[dict[str, Any]] = []

            def 실행파일이름(pid: int) -> str:
                프로세스 = kernel32.OpenProcess(프로세스조회, False, pid)
                if not 프로세스:
                    return ""
                try:
                    버퍼 = ctypes.create_unicode_buffer(32768)
                    길이 = wintypes.DWORD(len(버퍼))
                    if not kernel32.QueryFullProcessImageNameW(
                        프로세스, 0, 버퍼, ctypes.byref(길이)
                    ):
                        return ""
                    return os.path.basename(버퍼.value).casefold()
                finally:
                    kernel32.CloseHandle(프로세스)

            def 창수집(hwnd, _):
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if 실행파일이름(pid.value) != "hwp.exe":
                    return True
                제목길이 = user32.GetWindowTextLengthW(hwnd)
                제목버퍼 = ctypes.create_unicode_buffer(max(1, 제목길이 + 1))
                if 제목길이:
                    user32.GetWindowTextW(hwnd, 제목버퍼, len(제목버퍼))
                결과.append(
                    {
                        "hwnd": int(hwnd),
                        "pid": int(pid.value),
                        "title": 제목버퍼.value,
                        "visible": bool(user32.IsWindowVisible(hwnd)),
                        "minimized": bool(user32.IsIconic(hwnd)),
                    }
                )
                return True

            콜백 = 콜백형(창수집)
            user32.EnumWindows(콜백, 0)
            return 결과
        except Exception:
            return []

    @staticmethod
    def _네이티브창정보(핸들: int | None) -> dict[str, bool] | None:
        if os.name != "nt" or not 핸들:
            return None
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            user32.IsWindow.argtypes = [wintypes.HWND]
            user32.IsWindow.restype = wintypes.BOOL
            user32.IsWindowVisible.argtypes = [wintypes.HWND]
            user32.IsWindowVisible.restype = wintypes.BOOL
            user32.IsIconic.argtypes = [wintypes.HWND]
            user32.IsIconic.restype = wintypes.BOOL
            if not user32.IsWindow(핸들):
                return None
            return {
                "visible": bool(user32.IsWindowVisible(핸들)),
                "minimized": bool(user32.IsIconic(핸들)),
            }
        except Exception:
            return None

    @staticmethod
    def _네이티브창명령(핸들: int | None, 명령: int, *, 활성화: bool = False) -> bool:
        if os.name != "nt" or not 핸들:
            return False
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            user32.IsWindow.argtypes = [wintypes.HWND]
            user32.IsWindow.restype = wintypes.BOOL
            user32.ShowWindowAsync.argtypes = [wintypes.HWND, ctypes.c_int]
            user32.ShowWindowAsync.restype = wintypes.BOOL
            user32.SetForegroundWindow.argtypes = [wintypes.HWND]
            user32.SetForegroundWindow.restype = wintypes.BOOL
            if not user32.IsWindow(핸들):
                return False
            user32.ShowWindowAsync(핸들, 명령)
            if 활성화:
                user32.SetForegroundWindow(핸들)
            return bool(user32.IsWindow(핸들))
        except Exception:
            return False

    @staticmethod
    def _프로세스실행중(프로세스id: int | None) -> bool | None:
        """PID 존재 여부를 확인한다. 조회 자체가 불가능하면 None이다."""

        if os.name != "nt" or not 프로세스id:
            return None
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
            kernel32.WaitForSingleObject.restype = wintypes.DWORD
            kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel32.CloseHandle.restype = wintypes.BOOL
            동기화권한 = 0x00100000
            즉시반환 = 0
            대기시간초과 = 0x00000102
            프로세스 = kernel32.OpenProcess(동기화권한, False, int(프로세스id))
            if not 프로세스:
                오류코드 = ctypes.get_last_error()
                if any(
                    int(항목.get("pid", 0)) == int(프로세스id)
                    for 항목 in 복구한글어댑터._한글창목록()
                ):
                    return True
                # ERROR_INVALID_PARAMETER는 해당 PID가 더 이상 없음을 뜻한다.
                # 접근 거부 등은 종료로 추측하지 않는다.
                return False if 오류코드 == 87 else None
            try:
                return kernel32.WaitForSingleObject(프로세스, 즉시반환) == 대기시간초과
            finally:
                kernel32.CloseHandle(프로세스)
        except Exception:
            return None

    @classmethod
    def _프로세스종료대기(cls, 프로세스id: int | None, 제한초: float = 3.0) -> bool:
        if not 프로세스id:
            return False
        마감 = time.monotonic() + max(0.0, 제한초)
        while True:
            실행중 = cls._프로세스실행중(프로세스id)
            if 실행중 is False:
                return True
            if 실행중 is None or time.monotonic() >= 마감:
                return False
            time.sleep(0.05)

    def _한글프로세스식별자목록(self) -> tuple[tuple[int, int | None], ...] | None:
        """복구 연결 계층의 PID/시작 시각 스냅샷을 안전 경계에서 재사용한다."""

        조회 = getattr(self._대상, "_한글프로세스식별자목록", None)
        if not callable(조회):
            return None
        try:
            결과 = 조회()
        except Exception:
            return None
        if 결과 is None:
            return None
        정리 = []
        try:
            for 항목 in 결과:
                if not isinstance(항목, tuple) or len(항목) != 2:
                    return None
                pid = int(항목[0])
                시작시각 = None if 항목[1] is None else int(항목[1])
                if pid <= 0:
                    return None
                정리.append((pid, 시작시각))
        except (TypeError, ValueError):
            return None
        return tuple(정리)

    def _신규전용프로세스소유권확인(
        self,
        식별자: Any,
        이전목록: tuple[tuple[int, int | None], ...] | None,
    ) -> tuple[int, int | None]:
        """전용 COM 반환 뒤 새 Hwp.exe가 정확히 하나인지 다시 확인한다."""

        if not isinstance(식별자, tuple) or len(식별자) != 2:
            raise RuntimeError(
                "전용 Hwp.exe의 PID/시작 시각 식별자가 없어 소유권을 입증하지 못했습니다."
            )
        try:
            정규식별자 = (int(식별자[0]), None if 식별자[1] is None else int(식별자[1]))
        except (TypeError, ValueError) as 오류:
            raise RuntimeError("전용 Hwp.exe 프로세스 식별자가 올바르지 않습니다.") from 오류
        현재목록 = self._한글프로세스식별자목록()
        if 이전목록 is None or 현재목록 is None:
            raise RuntimeError(
                "Hwp.exe 생성 전후 프로세스 목록을 확인하지 못해 소유권을 입증하지 못했습니다."
            )
        이전집합 = set(이전목록)
        이전pid = {pid for pid, _ in 이전목록}
        신규 = [
            항목
            for 항목 in 현재목록
            if 항목 not in 이전집합 and 항목[0] not in 이전pid
        ]
        if len(신규) != 1 or 신규[0] != 정규식별자:
            raise RuntimeError(
                "DispatchEx 뒤 새 Hwp.exe를 정확히 하나로 확인하지 못해 소유권을 입증하지 못했습니다."
            )
        실행중확인 = getattr(self._대상, "_프로세스식별자실행중", None)
        if not callable(실행중확인) or 실행중확인(정규식별자) is not True:
            raise RuntimeError(
                "전용 Hwp.exe의 PID/시작 시각 일치를 재확인하지 못했습니다."
            )
        return 정규식별자

    def _문서열기실패안전정리(
        self,
        한글: Any | None,
        프로세스식별자: tuple[int, int | None] | None,
        *,
        소유권입증됨: bool,
        이전대상: Any,
        이전전용: Any,
    ) -> Exception | None:
        """열기 실패 대상이 입증된 새 전용 인스턴스일 때만 정리한다."""

        if 한글 is None or 한글 is 이전대상 or 한글 is 이전전용:
            return None
        if not self._실제COM객체(한글):
            # 가짜/복구 검증 객체에도 Clear 기반 추측 정리는 하지 않는다.
            return None
        if not 소유권입증됨 or 프로세스식별자 is None:
            self._안전정리보류대상 = 한글
            self._안전정리보류프로세스식별자 = 프로세스식별자
            return RuntimeError(
                "전용 Hwp.exe 소유권이 모호하여 Clear/Close/Quit을 0회 호출했습니다. "
                "남은 창이 있으면 사용자가 직접 확인해 닫아야 합니다."
            )
        안전종료 = getattr(self._대상, "_전용Automation대상안전종료", None)
        if not callable(안전종료):
            self._안전정리보류대상 = 한글
            self._안전정리보류프로세스식별자 = 프로세스식별자
            return RuntimeError(
                "DocumentID 기반 안전 종료 기능이 없어 Clear/Close/Quit을 0회 호출했습니다."
            )
        try:
            안전종료(한글, 프로세스식별자)
            return None
        except Exception as 오류:
            self._안전정리보류대상 = 한글
            self._안전정리보류프로세스식별자 = 프로세스식별자
            return 오류

    def _관리창찾기(self, 경로: str | None = None) -> int | None:
        """열 때 분리한 PID/HWND 범위에서만 관리 창을 찾는다."""
        창목록 = self._한글창목록()
        if self._관리창핸들 is not None and self._관리창프로세스id is not None:
            기존 = [
                항목
                for 항목 in 창목록
                if int(항목["hwnd"]) == self._관리창핸들
                and int(항목["pid"]) == self._관리창프로세스id
            ]
            if len(기존) == 1:
                return self._관리창핸들
            # HWND 재사용을 다른 한글 창으로 오인하지 않는다.
            self._관리창핸들 = None

        후보 = [
            항목
            for 항목 in 창목록
            if int(항목["hwnd"]) not in self._관리전창핸들
            and int(항목["pid"]) not in self._관리전프로세스ids
        ]
        if self._관리창프로세스id is not None:
            후보 = [
                항목
                for 항목 in 후보
                if int(항목["pid"]) == self._관리창프로세스id
            ]
        if not 후보:
            return None
        파일명 = Path(경로).name.casefold() if 경로 else ""
        제목일치 = [항목 for 항목 in 후보 if 파일명 and 파일명 in 항목["title"].casefold()]
        if len(제목일치) == 1:
            선택 = 제목일치[0]
        elif len(제목일치) > 1 or len(후보) != 1:
            # 동시에 생긴 여러 Hwp 창 중 하나를 임의로 제어하면 사용자가 연
            # 문서를 최소화하거나 닫을 수 있으므로 모호성 자체를 오류로 둔다.
            return None
        else:
            선택 = 후보[0]
        self._관리창핸들 = int(선택["hwnd"])
        self._관리창프로세스id = int(선택["pid"])
        return self._관리창핸들

    def _관리상태초기화(self, *, 이전복원: bool) -> None:
        관리대상 = self._관리대상
        이전대상 = self._관리이전대상 if 이전복원 else None
        이전전용 = self._관리이전전용대상 if 이전복원 else None
        이전전용프로세스식별자 = (
            self._관리이전전용프로세스식별자 if 이전복원 else None
        )
        if getattr(self._대상, "대상", None) is 관리대상:
            self._대상.대상 = 이전대상
        if getattr(self._대상, "_전용Automation대상", None) is 관리대상:
            self._대상._전용Automation대상 = 이전전용
            if hasattr(self._대상, "_전용Automation프로세스식별자"):
                self._대상._전용Automation프로세스식별자 = 이전전용프로세스식별자
        self._관리대상 = None
        self._관리문서경로 = None
        self._관리문서id = None
        self._출력문서ids = set()
        self._관리이전대상 = None
        self._관리이전전용대상 = None
        self._관리이전전용프로세스식별자 = None
        self._관리창핸들 = None
        self._관리창프로세스id = None
        self._관리프로세스식별자 = None
        self._관리전창핸들 = set()
        self._관리전프로세스ids = set()
        self._관리전프로세스식별자들 = set()
        self._창최소화됨 = False

    def _관리대상정상(self, 대상: Any) -> bool:
        if not self._실제COM객체(대상):
            return True
        try:
            창수 = int(getattr(getattr(대상, "XHwpWindows"), "Count"))
            문서수 = int(getattr(getattr(대상, "XHwpDocuments"), "Count"))
            if 창수 <= 0 or 문서수 <= 0:
                return False
            if self._관리문서id:
                return self._문서ID로찾기(대상, self._관리문서id) is not None
            return True
        except Exception:
            return False

    def _현재대상(self) -> Any | None:
        if self._관리대상 is not None:
            if not self._관리대상정상(self._관리대상):
                self._관리상태초기화(이전복원=True)
                return getattr(self._대상, "대상", None)
            # 다른 복구 기능이 ROT 후보로 대상을 바꾸더라도 앱이 연 문서를 복원한다.
            self._대상.대상 = self._관리대상
            return self._관리대상
        return getattr(self._대상, "대상", None)

    def 관리작업문서활성화(self) -> dict[str, Any]:
        """사용자 작업 직전에만 관리 원문서를 명시적으로 활성화한다.

        상태 폴링은 사용자가 편집 중인 한글 탭의 포커스를 바꾸면 안 된다.
        따라서 ``문서상태``에서는 활성화를 하지 않고, 실제로 문서를 변경할
        명령 직전에 이 메서드를 별도로 호출한다. ``Item(0)``이나 제목으로
        대상을 추측하지 않고, 열 때 기록한 DocumentID의 IXHwpDocument만
        활성화한 뒤 COM이 보고하는 활성 DocumentID를 다시 대조한다.
        """

        if self._관리대상 is None:
            raise PermissionError(
                "프로그램의 '문서 열기'로 불러온 관리 문서에서만 이 작업을 실행할 수 있습니다."
            )
        한글 = self._현재대상()
        if 한글 is None or 한글 is not self._관리대상:
            raise RuntimeError("프로그램이 불러온 한글 문서가 이미 종료되었습니다.")
        if not self._관리문서id:
            raise RuntimeError("관리 문서의 DocumentID를 확인할 수 없어 작업을 중단했습니다.")
        관리문서 = self._문서ID로찾기(한글, self._관리문서id)
        if 관리문서 is None:
            raise RuntimeError("프로그램이 연 관리 원문서를 찾지 못해 작업을 중단했습니다.")
        if not self._문서활성화(관리문서):
            raise RuntimeError("관리 원문서를 활성화하지 못해 작업을 중단했습니다.")
        활성문서id = self._문서ID(self._활성문서객체(한글))
        if 활성문서id != self._관리문서id:
            raise RuntimeError(
                "관리 원문서의 활성 DocumentID를 재확인하지 못해 작업을 중단했습니다."
            )
        self._대상.대상 = 한글
        return self.문서상태()

    def _추적출력문서상태(self, 한글: Any) -> tuple[set[str], bool]:
        """살아 있는 출력 DocumentID와 완전 열거 여부를 반환한다.

        완전 열거가 입증됐을 때만 이미 닫힌 출력 ID를 추적 목록에서 제거한다.
        목록이나 DocumentID가 모호하면 기존 추적 ID를 그대로 살아 있는 것으로
        간주해 이후 종료 경로가 보수적으로 거부되게 한다.
        """

        if not self._출력문서ids:
            return set(), True
        문서목록 = self._문서목록(한글)
        문서ids: set[str] = set()
        완전열거 = True
        for 문서 in 문서목록:
            문서id = self._문서ID(문서)
            if 문서id is None:
                완전열거 = False
                continue
            문서ids.add(문서id)
        try:
            문서컬렉션 = getattr(한글, "XHwpDocuments")
            보고된개수 = int(getattr(문서컬렉션, "Count"))
        except Exception:
            완전열거 = False
        else:
            if 보고된개수 != len(문서목록):
                완전열거 = False
        if 완전열거:
            살아있는ids = self._출력문서ids & 문서ids
            self._출력문서ids = set(살아있는ids)
            return 살아있는ids, True
        return set(self._출력문서ids), False

    def 문서상태(self) -> dict[str, Any]:
        """현재 연결 문서 상태를 JSON 직렬화 가능한 값으로 반환한다."""

        한글 = self._현재대상()
        if 한글 is None:
            return {
                "connected": False,
                "document_open": False,
                "managed": False,
                "document_id": None,
                "active_document_id": None,
                "output_document_count": 0,
                "output_document_count_exact": True,
                "title": None,
                "path": None,
                "editable": None,
                "edit_mode": None,
                "edit_mode_label": None,
                "distribution": False,
                "file_writable": None,
                "modified": None,
                "visible": None,
                "minimized": None,
            }

        관리됨 = 한글 is self._관리대상
        출력문서ids, 출력문서정확 = (
            self._추적출력문서상태(한글) if 관리됨 else (set(), True)
        )
        활성문서 = self._활성문서객체(한글)
        문서 = (
            self._문서ID로찾기(한글, self._관리문서id)
            if 관리됨 and self._관리문서id
            else self._문서객체(한글)
        )
        # 다른 이름으로 저장하거나 새 문서로 전환한 경우를 즉시 반영하도록
        # 캐시보다 살아 있는 COM의 경로를 먼저 읽는다. 읽은 값이 빈 문자열이면
        # 제목 없는 새 문서이므로 이전 경로로 되돌리지 않는다.
        경로: str | None = None
        경로관찰됨 = False
        for 후보 in (문서, 한글):
            if 후보 is None:
                continue
            for 이름 in ("FullName", "Path", "FileName"):
                try:
                    값 = getattr(후보, 이름)
                    if callable(값) and 이름.startswith("Get"):
                        값 = 값()
                except Exception:
                    continue
                경로관찰됨 = True
                if isinstance(값, str) and 값.strip():
                    경로 = 값.strip()
                    break
            if 경로:
                break
        if not 경로관찰됨 and 관리됨 and self._관리문서경로:
            경로 = str(self._관리문서경로)
        if 관리됨 and 경로:
            with contextlib.suppress(OSError, RuntimeError, ValueError):
                self._관리문서경로 = Path(경로).expanduser().resolve(strict=False)

        제목: str | None = None
        for 후보 in (문서, 한글):
            if 후보 is None:
                continue
            for 이름 in ("Title", "Name"):
                값 = self._속성(후보, 이름)
                if isinstance(값, str) and 값.strip():
                    제목 = 값.strip()
                    break
            if 제목:
                break
        if not 제목 and 경로:
            제목 = Path(경로).name

        편집가능: bool | None = None
        편집모드값: int | str | None = None
        편집모드설명: str | None = None
        배포용 = False
        for 후보 in (문서, 한글):
            if 후보 is None:
                continue
            편집모드 = self._속성(후보, "EditMode")
            if isinstance(편집모드, str):
                정규화 = 편집모드.strip().casefold()
                if 정규화:
                    편집모드값 = 편집모드.strip()
                    if any(표현 in 정규화 for 표현 in ("read", "view", "읽기")):
                        편집가능 = False
                        편집모드설명 = "읽기 전용"
                    elif any(표현 in 정규화 for 표현 in ("normal", "edit", "일반", "편집")):
                        편집가능 = True
                        편집모드설명 = "편집 가능"
                    elif any(표현 in 정규화 for 표현 in ("form", "양식")):
                        편집가능 = True
                        편집모드설명 = "일부만 편집 가능"
                    break
            elif isinstance(편집모드, (bool, int)):
                편집모드값 = int(편집모드)
                # 하위 4비트가 기본 모드(0=읽기, 1=일반, 2=양식)이고
                # 16은 배포용 플래그다. 17/18은 각각 16|1, 16|2다.
                기본모드 = int(편집모드) & 0x0F
                배포용 = bool(int(편집모드) & 16)
                편집가능 = 기본모드 in (1, 2)
                편집모드설명 = {
                    0: "읽기 전용",
                    1: "편집 가능",
                    2: "일부만 편집 가능",
                }.get(기본모드, "편집 상태 확인 불가")
                if 기본모드 not in (0, 1, 2):
                    편집가능 = None
                break
        if 편집가능 is None:
            for 후보 in (문서, 한글):
                if 후보 is None:
                    continue
                for 이름 in ("ReadOnly", "IsReadOnly"):
                    읽기전용 = self._속성(후보, 이름)
                    if isinstance(읽기전용, (bool, int)):
                        편집가능 = not bool(읽기전용)
                        편집모드설명 = "편집 가능" if 편집가능 else "읽기 전용"
                        break
                if 편집가능 is not None:
                    break
        파일쓰기가능: bool | None = None
        if 경로:
            try:
                파일쓰기가능 = bool(Path(경로).stat().st_mode & stat.S_IWRITE)
            except OSError:
                pass

        수정됨: bool | None = None
        for 후보 in (문서, 한글):
            if 후보 is None:
                continue
            for 이름 in ("Modified", "IsModified"):
                try:
                    수정값 = getattr(후보, 이름)
                    if callable(수정값):
                        수정값 = 수정값()
                except Exception:
                    continue
                if isinstance(수정값, (bool, int)):
                    수정됨 = bool(수정값)
                    break
            if 수정됨 is not None:
                break

        창 = self._창객체(한글)
        표시됨 = self._속성(창, "Visible") if 창 is not None else None
        표시됨 = bool(표시됨) if isinstance(표시됨, (bool, int)) else None
        네이티브상태 = None
        if 관리됨 and self._실제COM객체(한글):
            self._관리창찾기(경로)
            네이티브상태 = self._네이티브창정보(self._관리창핸들)
        if 네이티브상태 is not None:
            표시됨 = 네이티브상태["visible"]
            최소화됨: bool | None = 네이티브상태["minimized"]
        else:
            창상태 = self._속성(창, "WindowState") if 창 is not None else None
            if isinstance(창상태, str):
                최소화됨 = "min" in 창상태.casefold() or "최소" in 창상태
            elif isinstance(창상태, (bool, int)):
                최소화됨 = int(창상태) == 1
            elif 관리됨:
                최소화됨 = self._창최소화됨
            else:
                최소화됨 = None

        return {
            "connected": True,
            "document_open": bool(문서 is not None or 제목 or 경로),
            "managed": 관리됨,
            "document_id": self._문서ID(문서),
            "active_document_id": self._문서ID(활성문서),
            "output_document_count": len(출력문서ids),
            "output_document_count_exact": 출력문서정확,
            "title": 제목,
            "path": 경로,
            "editable": 편집가능,
            "edit_mode": 편집모드값,
            "edit_mode_label": 편집모드설명,
            "distribution": 배포용,
            "file_writable": 파일쓰기가능,
            "modified": 수정됨,
            "visible": 표시됨,
            "minimized": 최소화됨,
        }

    def 관리문서열기(self, 경로: str | os.PathLike[str], *, 표시: bool = True) -> dict[str, Any]:
        """경로의 문서를 프로그램 전용 Automation 객체로 연다."""

        if not isinstance(경로, (str, os.PathLike)) or not str(경로).strip():
            raise ValueError("열 한글 문서 경로가 비어 있습니다.")
        문서경로 = Path(경로).expanduser().resolve(strict=True)
        if not 문서경로.is_file():
            raise ValueError(f"한글 문서 파일이 아닙니다: {문서경로}")
        if 문서경로.suffix.casefold() not in {".hwp", ".hwpx"}:
            raise ValueError("불러올 수 있는 문서 형식은 .hwp와 .hwpx입니다.")

        if self._관리대상 is not None:
            현재상태 = self.문서상태()
            현재경로 = 현재상태.get("path") if 현재상태.get("managed") else None
            try:
                같은문서 = bool(현재경로) and Path(str(현재경로)).resolve(strict=False) == 문서경로
            except (OSError, RuntimeError, ValueError):
                같은문서 = False
            if 같은문서:
                self._대상.대상 = self._관리대상
                상태 = 현재상태
                상태.update({"opened": False, "reused": True})
                return 상태
        if self._관리대상 is not None:
            raise RuntimeError(
                "프로그램이 연 문서가 이미 있습니다. 먼저 hwp_document_close로 "
                "정상 종료한 뒤 다른 문서를 여세요."
            )

        이전대상 = getattr(self._대상, "대상", None)
        기존전용 = getattr(self._대상, "_전용Automation대상", None)
        기존전용프로세스식별자 = getattr(
            self._대상, "_전용Automation프로세스식별자", None
        )
        전용열기 = getattr(self._대상, "관리전용한컴열기", None)
        if not callable(전용열기):
            전용열기 = getattr(self._대상, "전용한컴열기", None)
        if not callable(전용열기):
            전용열기 = getattr(self._대상, "_새한글", None)
        if not callable(전용열기):
            raise RuntimeError("복구 한글 객체가 전용 Automation 연결을 지원하지 않습니다.")

        기존창 = self._한글창목록() if os.name == "nt" else []
        기존프로세스식별자들 = (
            self._한글프로세스식별자목록() if os.name == "nt" else None
        )
        self._관리전창핸들 = {int(항목["hwnd"]) for 항목 in 기존창}
        self._관리전프로세스식별자들 = set(기존프로세스식별자들 or ())
        self._관리전프로세스ids = {
            int(항목[0]) for 항목 in (기존프로세스식별자들 or ())
        } or {int(항목["pid"]) for 항목 in 기존창}
        한글 = None
        관리문서id: str | None = None
        전용프로세스식별자: tuple[int, int | None] | None = None
        프로세스소유권입증됨 = False
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                한글 = 전용열기()
            if 한글 is None:
                한글 = getattr(self._대상, "대상", None)
            if 한글 is None:
                raise RuntimeError("전용 한글 Automation 객체를 가져오지 못했습니다.")
            if self._실제COM객체(한글):
                전용프로세스식별자 = self._신규전용프로세스소유권확인(
                    getattr(self._대상, "_전용Automation프로세스식별자", None),
                    기존프로세스식별자들,
                )
                프로세스소유권입증됨 = True
            열기 = getattr(한글, "Open", None)
            if not callable(열기):
                raise RuntimeError("연결된 한글 Automation 객체가 경로 열기를 지원하지 않습니다.")
            try:
                결과 = 열기(str(문서경로), "", "")
            except TypeError:
                결과 = 열기(str(문서경로))
            if 결과 is False:
                raise RuntimeError(f"한글이 문서를 열지 못했습니다: {문서경로}")
            관리문서id = self._문서ID(self._문서객체(한글))
            if self._실제COM객체(한글) and 관리문서id is None:
                raise RuntimeError("프로그램이 연 한글 문서의 DocumentID를 확인하지 못했습니다.")
        except Exception as 원인:
            # 모든 소유권 검증이 완료된 새 전용 프로세스만 DocumentID별로 닫는다.
            # 모호한 경우에는 기존 사용자 HWP 보호를 위해 어떤 종료 호출도 하지 않는다.
            정리오류 = self._문서열기실패안전정리(
                한글,
                전용프로세스식별자,
                소유권입증됨=프로세스소유권입증됨,
                이전대상=이전대상,
                이전전용=기존전용,
            )
            self._대상.대상 = 이전대상
            if hasattr(self._대상, "_전용Automation대상"):
                self._대상._전용Automation대상 = 기존전용
            if hasattr(self._대상, "_전용Automation프로세스식별자"):
                self._대상._전용Automation프로세스식별자 = 기존전용프로세스식별자
            self._관리전창핸들 = set()
            self._관리전프로세스ids = set()
            self._관리전프로세스식별자들 = set()
            if 정리오류 is not None:
                raise RuntimeError(
                    "한글 문서 열기 실패 후 안전 정리를 완료하지 못했습니다. "
                    f"{정리오류}"
                ) from 원인
            raise

        self._관리대상 = 한글
        self._관리문서경로 = 문서경로
        self._관리문서id = 관리문서id
        self._출력문서ids = set()
        self._관리이전대상 = 이전대상 if 이전대상 is not 한글 else None
        self._관리이전전용대상 = 기존전용 if 기존전용 is not 한글 else None
        self._관리이전전용프로세스식별자 = (
            기존전용프로세스식별자 if 기존전용 is not 한글 else None
        )
        self._관리프로세스식별자 = 전용프로세스식별자
        if 전용프로세스식별자 is not None:
            self._관리창프로세스id = int(전용프로세스식별자[0])
        self._대상.대상 = 한글
        self._창최소화됨 = False
        try:
            if 표시:
                self.문서표시()
            elif self._실제COM객체(한글):
                self._관리창찾기(str(문서경로))
            상태 = self.문서상태()
            실제경로 = 상태.get("path")
            if 실제경로:
                열림경로일치 = Path(str(실제경로)).resolve(strict=False) == 문서경로
                if not 열림경로일치:
                    raise RuntimeError("한글에 열린 문서 경로가 선택한 파일과 일치하지 않습니다.")
        except Exception as 원인:
            # 열기 직후의 창 식별/경로 검증 실패는 아직 사용자 편집 전이므로
            # 소유권이 입증된 이번 요청의 전용 대상만 문서별로 닫는다.
            정리오류 = self._문서열기실패안전정리(
                한글,
                전용프로세스식별자,
                소유권입증됨=프로세스소유권입증됨,
                이전대상=이전대상,
                이전전용=기존전용,
            )
            self._관리상태초기화(이전복원=True)
            if 정리오류 is not None:
                raise RuntimeError(
                    "한글 문서 검증 실패 후 안전 정리를 완료하지 못했습니다. "
                    f"{정리오류}"
                ) from 원인
            raise
        상태.update({"opened": True, "reused": False})
        return 상태

    def 문서표시(self) -> dict[str, Any]:
        if self._관리대상 is None:
            raise PermissionError("프로그램에서 불러온 한글 문서만 화면에 표시할 수 있습니다.")
        한글 = self._현재대상()
        if 한글 is None or 한글 is not self._관리대상:
            raise RuntimeError("프로그램이 불러온 한글 문서가 이미 종료되었습니다.")
        # 출력 탭이 활성인 상태에서도 '표시'는 관리 원문서를 정확히 보여준다.
        self.관리작업문서활성화()
        창 = self._창객체(한글)
        if 창 is None:
            raise RuntimeError("한글 문서 창 객체를 가져오지 못했습니다.")

        try:
            창.Visible = True
        except Exception as 오류:
            raise RuntimeError("한글 문서 창을 표시하지 못했습니다.") from 오류

        if self._실제COM객체(한글):
            핸들 = self._관리창찾기(
                str(self._관리문서경로) if self._관리문서경로 else None
            )
            if 핸들 is None or not self._네이티브창명령(핸들, 9, 활성화=True):
                raise RuntimeError("프로그램이 연 한글 문서 창을 찾아 복원하지 못했습니다.")
        else:
            현재상태 = self._속성(창, "WindowState")
            최소상태 = (
                isinstance(현재상태, str)
                and ("min" in 현재상태.casefold() or "최소" in 현재상태)
            ) or (isinstance(현재상태, (bool, int)) and int(현재상태) == 1)
            복원 = self._속성(창, "Restore")
            if (self._창최소화됨 or 최소상태) and callable(복원):
                복원()
            elif self._창최소화됨 or 최소상태:
                try:
                    창.WindowState = 0
                except Exception as 오류:
                    raise RuntimeError("최소화된 한글 문서 창을 복원하지 못했습니다.") from 오류
        self._창최소화됨 = False
        return self.문서상태()

    def 문서최소화(self) -> dict[str, Any]:
        if self._관리대상 is None:
            raise PermissionError("프로그램에서 불러온 한글 문서만 최소화할 수 있습니다.")
        한글 = self._현재대상()
        if 한글 is None or 한글 is not self._관리대상:
            raise RuntimeError("프로그램이 불러온 한글 문서가 이미 종료되었습니다.")
        창 = self._창객체(한글)
        if 창 is None:
            raise RuntimeError("한글 문서 창 객체를 가져오지 못했습니다.")

        try:
            if self._실제COM객체(한글):
                핸들 = self._관리창찾기(
                    str(self._관리문서경로) if self._관리문서경로 else None
                )
                if 핸들 is None or not self._네이티브창명령(핸들, 6):
                    raise RuntimeError("프로그램이 연 한글 문서 창을 찾지 못했습니다.")
            else:
                최소화 = self._속성(창, "Minimize")
                if callable(최소화):
                    최소화()
                else:
                    창.WindowState = 1
        except Exception as 오류:
            raise RuntimeError("한글 문서 창을 최소화하지 못했습니다.") from 오류
        self._창최소화됨 = True
        return self.문서상태()

    def _소유문서목록(self, 한글: Any) -> tuple[Any, ...]:
        """현재 전용 인스턴스의 문서가 모두 앱 소유인지 확인한다."""

        문서목록 = self._문서목록(한글)
        if self._실제COM객체(한글):
            # Clear/Quit은 인스턴스 전체에 영향을 준다. COM 컬렉션의 일부만
            # 읽힌 상태를 "소유 문서만 있다"고 오판하면 사용자가 연 문서까지
            # 닫을 수 있으므로, 실제 COM에서는 완전 열거가 입증돼야 한다.
            try:
                문서컬렉션 = getattr(한글, "XHwpDocuments")
                보고된개수 = int(getattr(문서컬렉션, "Count"))
            except Exception as 오류:
                raise RuntimeError(
                    "한글 문서 목록 전체를 확인할 수 없어 안전한 종료를 중단했습니다."
                ) from 오류
            if 보고된개수 != len(문서목록):
                raise RuntimeError(
                    "한글 문서 목록을 완전히 열거하지 못해 안전한 종료를 중단했습니다."
                )
        if not self._관리문서id:
            if self._실제COM객체(한글):
                raise RuntimeError("관리 문서의 DocumentID가 없어 안전하게 종료할 수 없습니다.")
            return 문서목록
        소유id = {self._관리문서id, *self._출력문서ids}
        미확인: list[str] = []
        for 문서 in 문서목록:
            문서id = self._문서ID(문서)
            if 문서id is None:
                미확인.append("DocumentID 없음")
            elif 문서id not in 소유id:
                미확인.append(문서id)
        if 미확인:
            raise PermissionError(
                "프로그램 소유가 아닌 한글 문서가 같은 Automation 인스턴스에 있어 "
                "전체 종료를 중단했습니다. 해당 문서를 먼저 별도로 닫으세요."
            )
        if self._문서ID로찾기(한글, self._관리문서id) is None:
            raise RuntimeError("프로그램이 연 관리 문서를 찾지 못해 종료를 중단했습니다.")
        return 문서목록

    def _소유문서직접닫기(self, 한글: Any) -> None:
        """Clear가 실패했을 때 확인된 소유 문서만 저장 질문 없이 닫는다."""

        문서목록 = self._소유문서목록(한글)
        if not self._관리문서id:
            raise RuntimeError("DocumentID가 없어 Clear 실패 문서를 안전하게 정리할 수 없습니다.")
        소유id = {self._관리문서id, *self._출력문서ids}
        for 문서 in reversed(문서목록):
            문서id = self._문서ID(문서)
            if 문서id not in 소유id:
                continue
            try:
                문서.Modified = False
                닫기 = getattr(문서, "Close", None)
                if not callable(닫기):
                    raise RuntimeError("IXHwpDocument.Close를 제공하지 않습니다.")
                if 닫기(False) is False:
                    raise RuntimeError("IXHwpDocument.Close(False)가 실패했습니다.")
            except Exception as 오류:
                raise RuntimeError(
                    f"소유 문서({문서id})를 저장 질문 없이 닫지 못했습니다."
                ) from 오류

    def 관리문서닫기(self, 저장여부: bool | None = None) -> dict[str, Any]:
        """앱이 직접 연 문서만 명시된 저장 정책으로 대화상자 없이 닫는다."""

        한글 = self._관리대상
        if 한글 is None:
            if getattr(self._대상, "대상", None) is not None:
                raise PermissionError("사용자가 수동으로 연 한글 문서는 이 프로그램에서 닫지 않습니다.")
            raise RuntimeError("프로그램이 연 한글 문서가 없습니다.")

        이전상태 = self.문서상태()
        출력문서ids, 출력문서정확 = self._추적출력문서상태(한글)
        if not 출력문서정확:
            raise PermissionError(
                "출력 문서 상태를 정확히 확인할 수 없습니다. 출력 문서를 저장하거나 "
                "닫은 후 다시 시도하세요."
            )
        if 출력문서ids:
            raise PermissionError(
                f"출력 문서 {len(출력문서ids)}개가 별도로 열려 있습니다. 출력 문서를 "
                "저장하거나 닫은 후 다시 시도하세요."
            )
        # Clear(1)과 Quit은 인스턴스의 모든 문서에 영향을 준다. DocumentID로
        # 소유권이 입증되지 않은 문서가 하나라도 있으면 파괴적 종료를 거부한다.
        self._소유문서목록(한글)
        if 저장여부 is None and 이전상태.get("modified") is not False:
            return {
                **이전상태,
                "closed": False,
                "confirmation_required": True,
                "confirmation_reason": (
                    "modified" if 이전상태.get("modified") is True else "modified_state_unknown"
                ),
            }

        저장함 = 저장여부 is True
        if 저장함:
            관리문서 = self._문서ID로찾기(한글, self._관리문서id)
            활성문서id = self._문서ID(self._문서객체(한글))
            if (
                self._관리문서id
                and 활성문서id != self._관리문서id
                and not self._문서활성화(관리문서)
            ):
                raise RuntimeError("저장할 관리 문서를 활성화하지 못해 종료를 중단했습니다.")
            저장 = getattr(한글, "Save", None)
            try:
                if callable(저장):
                    try:
                        저장결과 = 저장(True)
                    except TypeError:
                        저장결과 = 저장()
                else:
                    액션 = getattr(한글, "HAction", None)
                    실행 = getattr(액션, "Run", None)
                    if not callable(실행):
                        raise RuntimeError("한글 Automation 객체가 저장 기능을 제공하지 않습니다.")
                    저장결과 = 실행("FileSave")
                if 저장결과 is False:
                    raise RuntimeError("한글이 문서 저장을 완료하지 못했습니다.")
                저장후상태 = self.문서상태()
                if 저장후상태.get("modified") is True:
                    raise RuntimeError("저장 후에도 한글이 문서를 수정됨 상태로 보고했습니다.")
            except Exception as 오류:
                raise RuntimeError("문서 저장에 실패해 종료를 중단했습니다.") from 오류
        try:
            # 저장 여부가 명시됐거나 미수정 상태임을 확인한 뒤 Clear(1)로 저장
            # 확인 대화상자를 막는다.
            한글.Clear(1)
        except Exception as Clear오류:
            # RPC 서버 오류처럼 Clear가 실패해도 임의의 활성 탭을 닫지 않는다.
            # DocumentID가 추적된 소유 문서만 IXHwpDocument로 직접 닫는다.
            try:
                self._소유문서직접닫기(한글)
            except Exception as 직접닫기오류:
                raise RuntimeError(
                    "한글 Clear 실패 후 소유 문서를 안전하게 정리하지 못해 종료를 중단했습니다."
                ) from 직접닫기오류

        프로세스id = self._관리창프로세스id
        종료오류: Exception | None = None
        try:
            한글.Quit()
        except Exception as 오류:
            종료오류 = 오류

        if self._실제COM객체(한글):
            if not 프로세스id:
                raise RuntimeError(
                    "관리 Hwp.exe의 PID를 확인할 수 없어 종료 성공으로 처리하지 않았습니다."
                ) from 종료오류
            if not self._프로세스종료대기(프로세스id):
                raise RuntimeError(
                    f"관리 Hwp.exe(PID {프로세스id})가 종료되지 않아 연결 상태를 유지합니다."
                ) from 종료오류
        elif 종료오류 is not None:
            raise RuntimeError("한글 Automation 인스턴스를 정상 종료하지 못했습니다.") from 종료오류

        self._관리상태초기화(이전복원=True)
        상태 = self.문서상태()
        상태.update(
            {
                "closed": True,
                "saved_changes": 저장함,
                "discarded_changes": 저장여부 is False and 이전상태.get("modified") is True,
                "confirmation_required": False,
                "previous_document": 이전상태,
            }
        )
        return 상태

    def _정확문서ID집합(self, 한글: Any) -> set[str]:
        문서목록 = self._문서목록(한글)
        try:
            보고된개수 = int(getattr(getattr(한글, "XHwpDocuments"), "Count"))
        except Exception as 오류:
            raise RuntimeError("한글 문서 목록 개수를 확인하지 못했습니다.") from 오류
        if 보고된개수 != len(문서목록):
            raise RuntimeError("한글 문서 목록을 완전히 열거하지 못했습니다.")
        문서ids = {self._문서ID(문서) for 문서 in 문서목록}
        if None in 문서ids or len(문서ids) != len(문서목록):
            raise RuntimeError("모든 한글 문서의 고유 DocumentID를 확인하지 못했습니다.")
        return {str(문서id) for 문서id in 문서ids}

    def 관리작업추적실행(self, 실행):
        """복구 기능 전후 문서 집합을 대조해 모든 새 출력 문서를 추적한다."""

        한글 = self._관리대상
        if 한글 is None:
            raise PermissionError(
                "프로그램의 '문서 열기'로 불러온 관리 문서에서만 이 작업을 실행할 수 있습니다."
            )
        # 실행 전부터 소유권이 모호한 문서가 있으면 사용자 코드를 전혀 호출하지 않는다.
        self._소유문서목록(한글)
        이전문서ids = self._정확문서ID집합(한글)
        결과: Any = None
        실행오류: Exception | None = None
        try:
            결과 = 실행()
        except Exception as 오류:
            실행오류 = 오류

        try:
            이후문서ids = self._정확문서ID집합(한글)
            self._출력문서ids.update(이후문서ids - 이전문서ids)
            # 새 ID를 등록한 다음 다시 전체 소유권을 검증한다. 원문서가 사라졌거나
            # 한 번에 둘 이상의 불명 문서가 생긴 경우에도 성공으로 보고하지 않는다.
            self._소유문서목록(한글)
        except Exception as 추적오류:
            raise RuntimeError(
                "기능 실행 후 한글 문서 수명주기를 안전하게 확인하지 못했습니다."
            ) from 추적오류
        if 실행오류 is not None:
            raise 실행오류
        return 결과

    def 빈출력문서생성(self):
        """관리 원문서에서 새 빈 문서를 만들고 DocumentID를 출력물로 추적한다."""

        self.관리작업문서활성화()
        assert self._관리대상 is not None
        if len(self._소유문서목록(self._관리대상)) >= 10:
            raise RuntimeError("한글 문서는 한 번에 최대 10개까지만 열 수 있습니다.")
        결과 = self.관리작업추적실행(lambda: self._관리대상.HAction.Run("FileNew"))
        if 결과 is False:
            raise RuntimeError("한글 새 출력 문서를 만들지 못했습니다.")
        return 결과

    def 선택영역서식내보내기(self) -> str:
        한글 = self._현재대상()

        def 선택범위확인(후보: Any) -> bool | None:
            """블록 시작·끝을 직접 확인한다. API 미지원 때만 None을 반환한다."""

            try:
                시작 = 후보.CreateSet("ListParaPos")
                끝 = 후보.CreateSet("ListParaPos")
                if 후보.GetSelectedPosBySet(시작, 끝) is False:
                    return False
                시작위치 = tuple(int(시작.Item(이름)) for 이름 in ("List", "Para", "Pos"))
                끝위치 = tuple(int(끝.Item(이름)) for 이름 in ("List", "Para", "Pos"))
                return 시작위치 != 끝위치
            except Exception:
                # 구형/가짜 COM 객체는 위치 API를 제공하지 않을 수 있다. 이때는
                # 기존 saveblock 반환값 검사로 호환한다.
                return None

        def 선택영역읽기(후보: Any) -> str | None:
            if 선택범위확인(후보) is False:
                return None
            try:
                결과 = 후보.GetTextFile("HWPML2X", "saveblock")
            except Exception:
                return None
            return 결과 if isinstance(결과, str) and 결과.strip() else None

        # 원래 정상 동작하던 경로처럼 현재 연결 문서를 가장 먼저 읽는다.
        # 선택이 있는데도 ROT 열거를 먼저 하면 다른 Hwp 객체 호출과 진단 출력
        # 때문에 선택 확인이 늦거나 GUI JSON 프로토콜이 깨질 수 있다.
        if 한글 is not None:
            현재선택 = 선택영역읽기(한글)
            if 현재선택 is not None:
                return 현재선택

        # 앱이 경로로 연 문서가 있으면 다른 수동 Hwp 창으로 연결 대상을 바꾸지
        # 않는다. 선택이 없다는 오류를 그대로 반환해 관리 문서를 지속 유지한다.
        if self._관리대상 is not None:
            raise ValueError(
                "프로그램이 연 문서에서 선택 영역을 찾지 못했습니다. 저장할 영역을 "
                "선택한 상태로 '선택 영역 저장'을 다시 누르세요."
            )

        # 현재 연결 문서에 선택이 없을 때만 실행 중인 다른 문서를 보조 검색한다.
        # 복구 코드의 진단 print는 GUI 백엔드 stdout에 절대 섞이지 않게 막는다.
        후보목록 = []
        실행중목록가져오기 = getattr(self._대상, "_실행중인_한글목록", None)
        if callable(실행중목록가져오기):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    후보목록.extend(실행중목록가져오기())
            except Exception:
                # ROT 열거 실패가 현재 연결 객체의 정상 저장까지 막지 않게 한다.
                pass

        for 후보 in 후보목록:
            if 후보 is 한글:
                continue
            hwpml = 선택영역읽기(후보)
            if hwpml is not None:
                self._대상.대상 = 후보
                return hwpml

        raise ValueError(
            "선택 영역을 찾지 못했습니다. 저장할 영역을 선택한 상태로 "
            "'선택 영역 저장'을 다시 누르세요."
        )

    def 서식조각삽입(self, hwpml: str):
        한글 = getattr(self._대상, "대상", None)
        if 한글 is None:
            raise RuntimeError("연결된 한글 문서가 없습니다.")
        if not isinstance(hwpml, str) or not hwpml.strip():
            raise ValueError("삽입할 서식 조각이 비어 있습니다.")
        결과 = 한글.SetTextFile(hwpml, "HWPML2X", "insertfile")
        if 결과 is False:
            raise RuntimeError("한글이 서식 프리셋 삽입을 완료하지 못했습니다.")
        return 결과

    def 선택영역새문서생성(self, hwpml: str):
        """선택 영역과 함께 내보낸 쪽 서식을 새 문서에 적용한다."""
        한글 = getattr(self._대상, "대상", None)
        if 한글 is None:
            raise RuntimeError("연결된 한글 문서가 없습니다.")
        if not isinstance(hwpml, str) or not hwpml.strip():
            raise ValueError("새 문서로 만들 선택 영역 서식이 비어 있습니다.")
        원래활성문서 = self._문서객체(한글)
        원래문서id = self._문서ID(원래활성문서)
        이전문서ids = {
            문서id
            for 문서 in self._문서목록(한글)
            if (문서id := self._문서ID(문서)) is not None
        }
        새문서 = 한글.HAction.Run("FileNew")
        if 새문서 is False:
            raise RuntimeError("한글 새 문서를 만들지 못했습니다.")
        새활성문서 = self._문서객체(한글)
        새문서id = self._문서ID(새활성문서)
        새문서확정 = bool(
            새문서id
            and (
                새문서id not in 이전문서ids
                or (원래문서id is not None and 새문서id != 원래문서id)
            )
        )
        try:
            if self._실제COM객체(한글) and not 새문서확정:
                raise RuntimeError(
                    "FileNew 결과의 DocumentID를 확인하지 못해 새 문서에 내용을 적용하지 않았습니다."
                )
            결과 = 한글.SetTextFile(hwpml, "HWPML2X", "")
            if 결과 is False:
                raise RuntimeError("한글이 선택 영역 프리셋을 새 문서로 불러오지 못했습니다.")
        except Exception as 불러오기오류:
            롤백오류: Exception | None = None
            문서객체로닫음 = False
            if 새문서확정 and self._문서ID(새활성문서) == 새문서id:
                try:
                    # IXHwpDocument.Close(False)를 호출하기 전 Modified를
                    # 풀어 저장 확인 대화상자가 나오지 않게 한다.
                    새활성문서.Modified = False
                    문서닫기 = getattr(새활성문서, "Close", None)
                    if callable(문서닫기):
                        문서닫기결과 = 문서닫기(False)
                        if 문서닫기결과 is not False:
                            문서객체로닫음 = True
                except Exception as 문서닫기오류:
                    롤백오류 = 문서닫기오류
            if not 문서객체로닫음 and 새문서확정:
                try:
                    현재활성문서id = self._문서ID(self._문서객체(한글))
                    if 현재활성문서id != 새문서id:
                        raise RuntimeError(
                            "새 문서가 현재 활성 문서인지 확인할 수 없어 FileClose를 실행하지 않았습니다."
                        )
                    # DocumentID가 방금 만든 문서와 일치할 때만 구형 COM의
                    # FileClose를 최후 수단으로 사용한다.
                    닫기결과 = 한글.HAction.Run("FileClose")
                    if 닫기결과 is False:
                        raise RuntimeError("한글이 실패한 새 문서를 닫지 못했습니다.")
                    롤백오류 = None
                except Exception as 닫기오류:
                    롤백오류 = 닫기오류
            elif not 문서객체로닫음 and not 새문서확정:
                롤백오류 = RuntimeError(
                    "방금 만든 문서의 DocumentID를 확인하지 못해 FileClose를 실행하지 않았습니다."
                )

            if 원래문서id is not None:
                현재활성문서id = self._문서ID(self._문서객체(한글))
                if 현재활성문서id != 원래문서id and not self._문서활성화(원래활성문서):
                    롤백오류 = 롤백오류 or RuntimeError("원래 문서를 다시 활성화하지 못했습니다.")

            if 롤백오류 is not None:
                raise RuntimeError(
                    f"프리셋 출력 실패 후 새 문서 정리도 실패했습니다: {롤백오류}"
                ) from 불러오기오류
            raise
        if 새문서확정 and 새문서id is not None:
            self._출력문서ids.add(새문서id)
        return 결과
