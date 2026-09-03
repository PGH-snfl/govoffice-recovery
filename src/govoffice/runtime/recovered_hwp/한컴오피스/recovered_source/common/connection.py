"""한글(HWP) COM 실행 객체 연결 계층."""

import os
import time

try:
    import pythoncom
    from win32com.client import DispatchEx
    from win32com.client.gencache import EnsureDispatch
except ImportError:  # 비-Windows/비-COM 환경에서도 소스 검증을 허용한다.
    pythoncom = None
    DispatchEx = None
    EnsureDispatch = None


class HwpConnectionMixin:
    대상 = None
    _전용Automation대상 = None
    _전용Automation프로세스식별자 = None
    보안모듈종류 = "FilePathCheckDLL"
    보안모듈이름 = "FilePathCheckerModuleExample"

    @staticmethod
    def _com확인():
        if pythoncom is None or DispatchEx is None or EnsureDispatch is None:
            raise RuntimeError("한글 자동화에는 pywin32와 한글 오피스가 필요합니다.")

    def _실행중인_한글목록(self):
        """ROT에 공개된 실행 중 한글 Automation 객체를 모두 반환한다."""

        바인딩내용 = pythoncom.CreateBindCtx(0)
        실행중객체테이블 = pythoncom.GetRunningObjectTable()
        실행중객체이름들 = 실행중객체테이블.EnumRunning()
        결과 = []

        for 실행중객체이름 in 실행중객체이름들:
            try:
                이름 = 실행중객체이름.GetDisplayName(바인딩내용, 실행중객체이름)
                if 이름.startswith("!HwpObject"):
                    찾은객체 = 실행중객체테이블.GetObject(실행중객체이름)
                    결과.append(EnsureDispatch(찾은객체.QueryInterface(pythoncom.IID_IDispatch)))
            except ValueError as e:
                print(f"값 오류 : {e}")
            except Exception as 오류:
                print(f"[오류] 실행중 객체 확인 중 문제 발생: {오류}")
        return tuple(결과)

    def _실행중인_한글찾기(self):
        실행중목록 = self._실행중인_한글목록()
        return 실행중목록[0] if 실행중목록 else None

    @staticmethod
    def _정상한글창존재() -> bool:
        """오류 대화상자나 숨은 잔류 프로세스가 아닌 실제 Hwp 문서 창을 찾는다."""
        if os.name != "nt":
            return False
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.WinDLL("user32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
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
        user32.IsWindowVisible.argtypes = [wintypes.HWND]
        user32.IsWindowVisible.restype = wintypes.BOOL
        user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
        user32.GetWindowTextLengthW.restype = ctypes.c_int
        user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        user32.GetWindowTextW.restype = ctypes.c_int
        user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        user32.GetWindowThreadProcessId.restype = wintypes.DWORD
        프로세스조회 = 0x1000  # PROCESS_QUERY_LIMITED_INFORMATION
        발견 = False

        def 실행파일이름(pid: int) -> str:
            핸들 = kernel32.OpenProcess(프로세스조회, False, pid)
            if not 핸들:
                return ""
            try:
                버퍼 = ctypes.create_unicode_buffer(32768)
                길이 = wintypes.DWORD(len(버퍼))
                if not kernel32.QueryFullProcessImageNameW(핸들, 0, 버퍼, ctypes.byref(길이)):
                    return ""
                return os.path.basename(버퍼.value).casefold()
            finally:
                kernel32.CloseHandle(핸들)

        콜백형 = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows.argtypes = [콜백형, wintypes.LPARAM]
        user32.EnumWindows.restype = wintypes.BOOL

        def 창확인(hwnd, _):
            nonlocal 발견
            if not user32.IsWindowVisible(hwnd):
                return True
            제목길이 = user32.GetWindowTextLengthW(hwnd)
            if 제목길이 <= 0:
                return True
            제목버퍼 = ctypes.create_unicode_buffer(제목길이 + 1)
            user32.GetWindowTextW(hwnd, 제목버퍼, len(제목버퍼))
            제목 = 제목버퍼.value
            if "응용 프로그램 오류" in 제목 or "application error" in 제목.casefold():
                return True
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if 실행파일이름(pid.value) == "hwp.exe":
                발견 = True
                return False
            return True

        user32.EnumWindows(콜백형(창확인), 0)
        return 발견

    def _보안모듈등록(self):
        """레지스트리에 등록된 한글 Automation 파일 보안 모듈을 연결한다."""
        if self.대상 is None:
            raise RuntimeError("한글 COM 객체가 없어 보안 모듈을 등록할 수 없습니다.")
        try:
            등록됨 = self.대상.RegisterModule(self.보안모듈종류, self.보안모듈이름)
        except Exception as 오류:
            raise RuntimeError(
                "한글 Automation 보안 모듈 등록 중 오류가 발생했습니다. "
                "FilePathCheckerModuleExample.dll과 HKCU\\Software\\HNC\\HwpAutomation\\Modules "
                "레지스트리 값을 확인하세요."
            ) from 오류
        # 한글은 같은 인스턴스에 이미 등록된 모듈을 다시 등록하면 False를
        # 반환할 수 있다. 예외가 없었다면 기존 등록을 유효한 상태로 본다.
        return True

    @staticmethod
    def _한글프로세스식별자목록():
        """실행 중인 Hwp.exe를 ``(PID, 시작시각)``으로 식별한다.

        PID만 비교하면 아주 짧은 시간에도 재사용된 프로세스를 프로그램이 만든
        인스턴스로 오인할 수 있다. Windows FILETIME 시작 시각까지 읽되, 운영체제가
        시작 시각 조회를 허용하지 않은 프로세스는 ``None``으로 남긴다. 프로세스
        목록 자체를 신뢰성 있게 읽지 못한 경우에는 빈 목록과 구별되는 ``None``을
        반환한다.
        """

        if os.name != "nt":
            return None
        try:
            import ctypes
            from ctypes import wintypes

            class PROCESSENTRY32W(ctypes.Structure):
                _fields_ = [
                    ("dwSize", wintypes.DWORD),
                    ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.c_size_t),
                    ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD),
                    ("szExeFile", wintypes.WCHAR * 260),
                ]

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
            kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
            kernel32.Process32FirstW.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(PROCESSENTRY32W),
            ]
            kernel32.Process32FirstW.restype = wintypes.BOOL
            kernel32.Process32NextW.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(PROCESSENTRY32W),
            ]
            kernel32.Process32NextW.restype = wintypes.BOOL
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.GetProcessTimes.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(wintypes.FILETIME),
                ctypes.POINTER(wintypes.FILETIME),
                ctypes.POINTER(wintypes.FILETIME),
                ctypes.POINTER(wintypes.FILETIME),
            ]
            kernel32.GetProcessTimes.restype = wintypes.BOOL
            kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel32.CloseHandle.restype = wintypes.BOOL

            스냅샷 = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)  # TH32CS_SNAPPROCESS
            잘못된핸들 = ctypes.c_void_p(-1).value
            if not 스냅샷 or int(스냅샷) == 잘못된핸들:
                return None
            결과 = []
            try:
                항목 = PROCESSENTRY32W()
                항목.dwSize = ctypes.sizeof(PROCESSENTRY32W)
                계속 = bool(kernel32.Process32FirstW(스냅샷, ctypes.byref(항목)))
                while 계속:
                    if 항목.szExeFile.casefold() == "hwp.exe":
                        pid = int(항목.th32ProcessID)
                        시작시각 = None
                        프로세스 = kernel32.OpenProcess(0x1000, False, pid)
                        if 프로세스:
                            try:
                                생성 = wintypes.FILETIME()
                                종료 = wintypes.FILETIME()
                                커널 = wintypes.FILETIME()
                                사용자 = wintypes.FILETIME()
                                if kernel32.GetProcessTimes(
                                    프로세스,
                                    ctypes.byref(생성),
                                    ctypes.byref(종료),
                                    ctypes.byref(커널),
                                    ctypes.byref(사용자),
                                ):
                                    시작시각 = (int(생성.dwHighDateTime) << 32) | int(
                                        생성.dwLowDateTime
                                    )
                            finally:
                                kernel32.CloseHandle(프로세스)
                        결과.append((pid, 시작시각))
                    계속 = bool(kernel32.Process32NextW(스냅샷, ctypes.byref(항목)))
            finally:
                kernel32.CloseHandle(스냅샷)
            return tuple(결과)
        except Exception:
            return None

    @classmethod
    def _프로세스식별자실행중(cls, 식별자):
        """같은 PID *및* 시작 시각의 Hwp.exe가 살아 있는지 확인한다."""

        if not isinstance(식별자, tuple) or len(식별자) != 2:
            return None
        try:
            pid = int(식별자[0])
        except (TypeError, ValueError):
            return None
        현재목록 = cls._한글프로세스식별자목록()
        if 현재목록 is None:
            return None
        기대시각 = 식별자[1]
        같은pid = [현재 for 현재 in 현재목록 if int(현재[0]) == pid]
        if not 같은pid:
            return False
        if 기대시각 is None:
            # 시작 시각을 얻지 못한 환경에서도 생성 전 스냅샷에 없던 단 하나의
            # 신규 PID라면 제한적으로 추적할 수 있다.
            return len(같은pid) == 1
        return any(현재[1] == 기대시각 for 현재 in 같은pid)

    @classmethod
    def _프로세스식별자종료대기(cls, 식별자, 제한초=3.0):
        마감 = time.monotonic() + max(0.0, float(제한초))
        while True:
            실행중 = cls._프로세스식별자실행중(식별자)
            if 실행중 is False:
                return True
            if 실행중 is None or time.monotonic() >= 마감:
                return False
            time.sleep(0.05)

    @staticmethod
    def _문서ID(문서):
        for 이름 in ("DocumentID", "DocumentId"):
            try:
                값 = getattr(문서, 이름)
                if callable(값):
                    값 = 값()
            except Exception:
                continue
            if 값 is not None and str(값).strip():
                return str(값).strip()
        return None

    @classmethod
    def _문서전체열거(cls, 대상):
        """문서 컬렉션을 완전히 읽고 각 문서의 안정 ID를 검증한다."""

        try:
            컬렉션 = 대상.XHwpDocuments
            개수 = int(컬렉션.Count)
        except Exception as 오류:
            raise RuntimeError("전용 한글의 문서 목록 전체를 읽지 못했습니다.") from 오류
        if 개수 < 0:
            raise RuntimeError("전용 한글이 잘못된 문서 개수를 보고했습니다.")
        if 개수 == 0:
            return ()

        성공후보 = []
        for 시작인덱스 in (0, 1):
            문서들 = []
            try:
                for 순번 in range(개수):
                    문서들.append(컬렉션.Item(시작인덱스 + 순번))
            except Exception:
                continue
            문서ids = [cls._문서ID(문서) for 문서 in 문서들]
            if any(문서id is None for 문서id in 문서ids):
                continue
            if len(set(문서ids)) != 개수:
                continue
            성공후보.append((tuple(문서들), tuple(문서ids)))

        if not 성공후보:
            raise RuntimeError(
                "전용 한글의 모든 문서를 DocumentID로 입증하지 못했습니다."
            )
        첫ids = 성공후보[0][1]
        if any(set(후보ids) != set(첫ids) for _, 후보ids in 성공후보[1:]):
            raise RuntimeError("전용 한글 문서 인덱스 기준이 모호해 안전 정리를 중단했습니다.")
        return 성공후보[0][0]

    @classmethod
    def _활성문서ID(cls, 대상):
        """COM이 실제 활성 상태로 보고하는 문서의 안정 ID를 반환한다."""

        try:
            문서컬렉션 = 대상.XHwpDocuments
            활성문서 = 문서컬렉션.Active_XHwpDocument
            if callable(활성문서):
                활성문서 = 활성문서()
        except Exception as 오류:
            raise RuntimeError("전용 한글의 활성 문서를 확인하지 못했습니다.") from 오류
        활성문서id = cls._문서ID(활성문서)
        if 활성문서id is None:
            raise RuntimeError("전용 한글의 Active DocumentID를 확인하지 못했습니다.")
        return 활성문서id

    @classmethod
    def _문서활성화확인(cls, 대상, 문서, 문서id):
        """닫을 문서를 명시 활성화하고 COM의 활성 ID를 다시 대조한다.

        일부 한글 버전은 ``IXHwpDocument.Close``를 호출한 수신 객체가 아니라
        현재 활성 문서를 닫는다. 따라서 DocumentID가 일치하기 전에는 Close를
        호출하면 안 된다.
        """

        활성화 = getattr(문서, "SetActive_XHwpDocument", None)
        if not callable(활성화):
            raise RuntimeError("IXHwpDocument.SetActive_XHwpDocument를 제공하지 않습니다.")
        try:
            활성화()
        except Exception as 오류:
            raise RuntimeError(f"소유 문서({문서id})를 활성화하지 못했습니다.") from 오류
        if cls._활성문서ID(대상) != 문서id:
            raise RuntimeError(
                f"소유 문서({문서id}) 활성화 뒤 Active DocumentID가 일치하지 않습니다."
            )

    @classmethod
    def _문서소멸대기(cls, 대상, 문서id, 제한초=1.0):
        """Close가 비동기로 반영되는 버전에서도 대상 ID의 소멸을 제한 대기한다."""

        마감 = time.monotonic() + 제한초
        while True:
            남은ids = tuple(cls._문서ID(문서) for 문서 in cls._문서전체열거(대상))
            if 문서id not in 남은ids:
                return 남은ids
            if time.monotonic() >= 마감:
                raise RuntimeError(
                    f"IXHwpDocument.Close(False) 뒤 소유 문서({문서id})가 남아 있습니다."
                )
            if pythoncom is not None:
                try:
                    pythoncom.PumpWaitingMessages()
                except Exception:
                    pass
            time.sleep(0.05)

    @classmethod
    def _전용Automation대상안전종료(cls, 대상, 프로세스식별자, 제한초=3.0):
        """소유권이 입증된 전용 인스턴스만 문서별로 닫은 뒤 종료한다.

        이 함수는 검증을 모두 마치기 전에는 ``Close``나 ``Quit``을 단 한 번도
        호출하지 않는다. 인스턴스 전체에 영향을 주는 ``Clear``는 사용하지 않는다.
        """

        if cls._프로세스식별자실행중(프로세스식별자) is not True:
            raise RuntimeError(
                "전용 Hwp.exe의 PID/시작 시각 소유권을 확인하지 못해 "
                "Close/Quit을 실행하지 않았습니다."
            )
        문서들 = cls._문서전체열거(대상)
        문서ids = tuple(cls._문서ID(문서) for 문서 in 문서들)
        if not 문서ids:
            raise RuntimeError("전용 한글의 소유 문서가 없어 안전하게 종료할 수 없습니다.")
        남길문서id = 문서ids[0]
        예상문서ids = set(문서ids)
        # 위 열거가 성공했으므로 여기부터는 모두 새 전용 프로세스의 소유 문서다.
        # HWP의 IXHwpDocument.Close는 수신 객체 대신 활성 문서를 닫는 버전이
        # 있으므로 매번 새 프록시를 얻고 활성 DocumentID를 재검증한다.
        # 마지막 한 문서는 Close(False)로 빈 컬렉션이 되지 않고 기본 빈 문서로
        # 남는 HWP 버전이 있다. 따라서 출력/추가 문서만 닫고, 정확히 확인된 원본
        # 하나는 Modified=False로 만든 뒤 격리 인스턴스의 Quit이 닫도록 남긴다.
        for 문서id in reversed(문서ids[1:]):
            if cls._프로세스식별자실행중(프로세스식별자) is not True:
                raise RuntimeError(
                    "문서 종료 직전 전용 Hwp.exe의 PID/시작 시각 소유권을 "
                    "재확인하지 못해 추가 Close/Quit을 실행하지 않았습니다."
                )
            현재문서들 = cls._문서전체열거(대상)
            현재문서맵 = {cls._문서ID(문서): 문서 for 문서 in 현재문서들}
            현재ids = set(현재문서맵)
            if 현재ids != 예상문서ids:
                raise RuntimeError(
                    "전용 한글의 DocumentID 집합이 예상과 달라져 "
                    "추가 Close/Quit을 실행하지 않습니다."
                )
            문서 = 현재문서맵.get(문서id)
            if 문서 is None:
                continue
            try:
                cls._문서활성화확인(대상, 문서, 문서id)
                문서.Modified = False
                닫기 = getattr(문서, "Close", None)
                if not callable(닫기):
                    raise RuntimeError("IXHwpDocument.Close를 제공하지 않습니다.")
                닫기결과 = 닫기(False)
                # BOOL이 Python int(0/1)로 노출되는 COM 래퍼도 있으므로
                # ``is False``만으로 실패를 판정하지 않는다. 반환값이 없는 구형
                # 래퍼는 아래 DocumentID 상태 대조를 최종 증거로 사용한다.
                if 닫기결과 is not None and not bool(닫기결과):
                    raise RuntimeError("IXHwpDocument.Close(False)가 실패했습니다.")
            except Exception as 오류:
                raise RuntimeError(
                    f"소유 문서({문서id})를 저장 질문 없이 닫지 못했습니다: {오류}"
                ) from 오류
            예상문서ids.remove(문서id)
            닫은뒤ids = set(cls._문서소멸대기(대상, 문서id))
            if 닫은뒤ids != 예상문서ids:
                raise RuntimeError(
                    "소유 문서를 닫은 뒤 예상과 다른 DocumentID가 남아 있어 "
                    "추가 Close/Quit을 실행하지 않습니다."
                )

        남은문서 = cls._문서전체열거(대상)
        남은문서맵 = {cls._문서ID(문서): 문서 for 문서 in 남은문서}
        if set(남은문서맵) != {남길문서id}:
            raise RuntimeError(
                "소유권이 입증되지 않은 문서 상태가 남아 있어 전용 한글 Quit을 중단했습니다."
            )
        남길문서 = 남은문서맵[남길문서id]
        try:
            cls._문서활성화확인(대상, 남길문서, 남길문서id)
            남길문서.Modified = False
        except Exception as 오류:
            raise RuntimeError(
                f"마지막 소유 문서({남길문서id})를 안전한 Quit 상태로 만들지 "
                f"못했습니다: {오류}"
            ) from 오류
        if cls._프로세스식별자실행중(프로세스식별자) is not True:
            raise RuntimeError(
                "Quit 직전 전용 Hwp.exe의 PID/시작 시각 소유권을 재확인하지 못해 "
                "Quit을 실행하지 않았습니다."
            )
        try:
            종료결과 = 대상.Quit()
            if 종료결과 is not None and not bool(종료결과):
                raise RuntimeError("HwpObject.Quit이 실패를 반환했습니다.")
        except Exception as 오류:
            raise RuntimeError("전용 한글 Automation 인스턴스를 종료하지 못했습니다.") from 오류
        if not cls._프로세스식별자종료대기(프로세스식별자, 제한초):
            raise RuntimeError(
                f"전용 Hwp.exe(PID {프로세스식별자[0]}) 종료를 확인하지 못했습니다."
            )
        return {
            "closed_document_ids": list(reversed(문서ids[1:])),
            "retained_document_id": 남길문서id,
            "process_exited": True,
        }

    @classmethod
    def _신규프로세스식별자(cls, 이전목록, 이후목록):
        if 이전목록 is None or 이후목록 is None:
            return None
        이전집합 = set(이전목록)
        이전pid = {int(항목[0]) for 항목 in 이전목록}
        신규 = [
            항목
            for 항목 in 이후목록
            if 항목 not in 이전집합 and int(항목[0]) not in 이전pid
        ]
        return 신규[0] if len(신규) == 1 else None

    def _새한글(self):
        # DispatchEx로 전용 Automation 객체를 요청해 화면 없는 잔류 Hwp.exe에
        # 암묵적으로 재접속하는 상황을 피한다.
        새대상 = None
        이전프로세스목록 = self._한글프로세스식별자목록()
        if 이전프로세스목록 is None:
            raise RuntimeError(
                "Hwp.exe 생성 전 프로세스 목록을 확인하지 못해 DispatchEx를 실행하지 않았습니다."
            )
        프로세스식별자 = None
        try:
            새대상 = EnsureDispatch(DispatchEx("hwpframe.hwpobject"))
            이후프로세스목록 = self._한글프로세스식별자목록()
            프로세스식별자 = self._신규프로세스식별자(
                이전프로세스목록, 이후프로세스목록
            )
            if 프로세스식별자 is None:
                raise RuntimeError(
                    "DispatchEx 뒤 새 Hwp.exe를 정확히 하나로 식별하지 못했습니다. "
                    "기존 사용자 문서를 보호하기 위해 Close/Quit을 실행하지 않습니다."
                )
            self.대상 = 새대상
            self._전용Automation대상 = 새대상
            self._전용Automation프로세스식별자 = 프로세스식별자
            self._보안모듈등록()
            새대상.XHwpWindows.Item(0).Visible = True
            return 새대상
        except Exception as 원인:
            정리오류 = None
            if 새대상 is not None:
                if 프로세스식별자 is None:
                    정리오류 = RuntimeError(
                        "새 Hwp.exe 소유권이 모호하여 Clear/Close/Quit을 0회 호출했습니다."
                    )
                else:
                    try:
                        self._전용Automation대상안전종료(
                            새대상, 프로세스식별자
                        )
                    except Exception as 오류:
                        정리오류 = 오류
            self.대상 = None
            self._전용Automation대상 = None
            self._전용Automation프로세스식별자 = None
            if 정리오류 is not None:
                raise RuntimeError(
                    "전용 한글 초기화 실패 후 안전 정리를 완료하지 못했습니다. "
                    f"{정리오류}"
                ) from 원인
            raise

    def 관리전용한컴열기(self):
        """경로로 불러올 한 문서만 담는 새 Automation 인스턴스를 만든다."""

        self._com확인()
        try:
            return self._새한글()
        except Exception as 오류:
            self.대상 = None
            self._전용Automation대상 = None
            self._전용Automation프로세스식별자 = None
            raise RuntimeError(
                "관리 문서용 한글 Automation 인스턴스를 만들지 못했습니다. "
                "남아 있는 Hwp.exe 오류 창을 닫고 다시 실행하세요. "
                f"안전 진단: {오류}"
            ) from 오류

    def 전용한컴열기(self):
        """이 프로그램만 사용하는 Automation 인스턴스를 반환한다.

        ``한컴열기``는 사용자가 수동으로 연 문서에 연결할 수 있지만, 파일 경로를
        받아 여는 기능은 그 문서를 임의로 바꾸거나 닫으면 안 된다. 따라서 기존
        대상이 전용 인스턴스일 때만 재사용하고 그 밖에는 DispatchEx로 새 인스턴스를
        만든다.
        """

        self._com확인()
        전용대상 = getattr(self, "_전용Automation대상", None)
        if 전용대상 is not None:
            try:
                if int(전용대상.XHwpWindows.Count) > 0:
                    self.대상 = 전용대상
                    return 전용대상
            except Exception:
                if self.대상 is 전용대상:
                    self.대상 = None
                self._전용Automation대상 = None
                self._전용Automation프로세스식별자 = None
        try:
            return self._새한글()
        except Exception as 오류:
            self.대상 = None
            self._전용Automation대상 = None
            self._전용Automation프로세스식별자 = None
            raise RuntimeError(
                "전용 한글 Automation 인스턴스를 만들지 못했습니다. "
                "남아 있는 Hwp.exe 오류 창을 닫고 다시 실행하세요. "
                f"안전 진단: {오류}"
            ) from 오류

    def 한컴열기(self):
        self._com확인()
        if self.대상 is not None:
            return self.대상
        # 정상 문서 창이 보일 때는 사용자가 선택한 기존 문서에 연결한다.
        # 숨은 잔류 Hwp.exe나 오류 대화상자만 있으면 ROT 접근을 생략한다.
        기존연결요청 = os.environ.get("GOVOFFICE_ATTACH_RUNNING_HWP") == "1"
        if 기존연결요청 or self._정상한글창존재():
            self.대상 = self._실행중인_한글찾기()
            if self.대상 is not None:
                self._보안모듈등록()
                return self.대상
        try:
            결과 = self._새한글()
            self.문서여백(20, 20, 15, 15, 10, 10)
            return 결과
        except Exception as 오류:
            self.대상 = None
            self._전용Automation대상 = None
            self._전용Automation프로세스식별자 = None
            raise RuntimeError(
                "전용 한글 Automation 인스턴스를 만들지 못했습니다. "
                "남아 있는 Hwp.exe 오류 창을 닫고 다시 실행하세요. "
                f"안전 진단: {오류}"
            ) from 오류

    def 불러오기(self):
        try:
            self.대상.HAction.Run("FileOpen")
        except (ValueError, Exception) as e:
            print(f"오류 발생 : {e}")
            self._com확인()
            self._새한글()
            self.대상.HAction.Run("FileOpen")

    def 새창(self):
        try:
            self.대상.HAction.Run("FileNew")
            self.문서여백(20, 20, 15, 15, 10, 10)
        except (ValueError, Exception) as e:
            print(f"오류 발생 : {e}")
            self._com확인()
            self._새한글()
            self.문서여백(20, 20, 15, 15, 10, 10)
