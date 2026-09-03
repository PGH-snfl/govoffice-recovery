"""새 정확 후보 기반 서식 프리셋을 실제 한글 COM에서 왕복 검증한다.

이 스크립트는 독립된 ``DispatchEx`` 인스턴스와 합성 검증값만 사용한다.
실행 중 오류가 나더라도 생성한 문서를 저장하지 않는 상태로 표시한 뒤
``Quit()``과 COM 참조 해제를 수행하고, 새 Hwp.exe 프로세스가 실제로
종료됐는지 확인한다. 개인정보 원문은 요약 JSON 보고서에 남기지 않는다.
"""

from __future__ import annotations

import gc
import contextlib
import ctypes
import json
import os
import subprocess
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

import pythoncom  # noqa: E402
from win32com.client import DispatchEx  # noqa: E402
from win32com.client.gencache import EnsureDispatch  # noqa: E402

from govoffice.domain.presets import 서식프리셋  # noqa: E402
from govoffice.services.hwpml_table_analysis import HWPMLTableFieldAnalyzer  # noqa: E402
from govoffice.services.style_presets import (  # noqa: E402
    HWPML등록필드분류기,
    HWPML서식치환기,
)


REPORT = PROJECT / "reports" / "dynamic_validation" / "style_preset_roundtrip.json"
MAX_HWP_PROCESSES = 10
GUI_MUTEX_NAME = r"Local\GovOfficeRecoveredApplication"
WAIT_OBJECT_0 = 0x00000000
WAIT_ABANDONED = 0x00000080
WAIT_TIMEOUT = 0x00000102


class _검증단독잠금:
    """GUI와 실제 HWP 검증기가 동시에 COM을 제어하지 못하게 한다."""

    def __init__(self) -> None:
        self.handle = None
        self.acquired = False
        self.abandoned = False

    def acquire(self) -> None:
        if sys.platform != "win32":
            raise RuntimeError("한글 COM 검증은 Windows에서만 실행할 수 있습니다.")
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
        kernel32.CreateMutexW.restype = ctypes.c_void_p
        kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel32.WaitForSingleObject.restype = ctypes.c_uint32
        kernel32.ReleaseMutex.argtypes = [ctypes.c_void_p]
        kernel32.ReleaseMutex.restype = ctypes.c_bool
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_bool

        self.handle = kernel32.CreateMutexW(None, False, GUI_MUTEX_NAME)
        if not self.handle:
            raise OSError(ctypes.get_last_error(), "범정부오피스 실행 잠금을 만들지 못했습니다.")
        wait_result = int(kernel32.WaitForSingleObject(self.handle, 0))
        if wait_result in (WAIT_OBJECT_0, WAIT_ABANDONED):
            self.acquired = True
            self.abandoned = wait_result == WAIT_ABANDONED
            return
        kernel32.CloseHandle(self.handle)
        self.handle = None
        if wait_result == WAIT_TIMEOUT:
            raise RuntimeError(
                "범정부오피스 GUI 또는 다른 실제 HWP 검증이 실행 중입니다. "
                "해당 작업이 완전히 종료된 뒤 다시 검증하세요."
            )
        raise OSError(wait_result, "범정부오피스 실행 잠금을 획득하지 못했습니다.")

    def release(self) -> None:
        if not self.handle:
            return
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.ReleaseMutex.argtypes = [ctypes.c_void_p]
        kernel32.ReleaseMutex.restype = ctypes.c_bool
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_bool
        try:
            if self.acquired and not kernel32.ReleaseMutex(self.handle):
                raise OSError(ctypes.get_last_error(), "범정부오피스 실행 잠금을 해제하지 못했습니다.")
        finally:
            kernel32.CloseHandle(self.handle)
            self.handle = None
            self.acquired = False


def _hwp_process_snapshot() -> dict[int, int]:
    """Hwp.exe의 PID와 UTC 시작 시각 tick을 읽기 전용으로 반환한다."""

    if sys.platform != "win32":
        return {}
    완료 = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "Get-Process -Name Hwp -ErrorAction SilentlyContinue | ForEach-Object { "
            "$ticks = -1; try { $ticks = $_.StartTime.ToUniversalTime().Ticks } catch {}; "
            "'{0}|{1}' -f $_.Id, $ticks }",
        ],
        capture_output=True,
        check=False,
        text=True,
        encoding="mbcs",
        errors="replace",
        creationflags=0x08000000,  # CREATE_NO_WINDOW
    )
    결과: dict[int, int] = {}
    for 행 in 완료.stdout.splitlines():
        try:
            pid문자열, 시작문자열 = 행.strip().split("|", 1)
            결과[int(pid문자열)] = int(시작문자열)
        except (TypeError, ValueError):
            continue
    return 결과


def _hwp_process_ids() -> set[int]:
    """기존 호출자 호환용 PID 집합."""

    return set(_hwp_process_snapshot())


def _프로세스목록(snapshot: dict[int, int]) -> list[dict[str, int]]:
    return [
        {"pid": pid, "start_time_utc_ticks": snapshot[pid]}
        for pid in sorted(snapshot)
    ]


def _새프로세스확인(
    기존: dict[int, int],
    제한초: float = 5.0,
    안정초: float = 0.6,
) -> dict[int, int]:
    """DispatchEx 직후 정확히 하나의 새 Hwp 정체성이 안정됐을 때만 반환한다."""

    마감 = time.monotonic() + 제한초
    직전: dict[int, int] | None = None
    안정시작 = 0.0
    while time.monotonic() < 마감:
        현재 = _hwp_process_snapshot()
        신규 = {
            pid: 시작
            for pid, 시작 in 현재.items()
            if 기존.get(pid) != 시작
        }
        if len(신규) > 1:
            raise RuntimeError(
                "DispatchEx 전후에 새 Hwp.exe가 둘 이상 생겨 검증 인스턴스 소유권을 "
                "안전하게 판정할 수 없습니다."
            )
        if 신규 and any(시작 < 0 for 시작 in 신규.values()):
            raise RuntimeError(
                "새 Hwp.exe의 시작 시각을 읽지 못해 검증 인스턴스 소유권을 "
                "안전하게 판정할 수 없습니다."
            )
        if 신규 == 직전 and len(신규) == 1:
            if time.monotonic() - 안정시작 >= 안정초:
                return 신규
        else:
            직전 = 신규
            안정시작 = time.monotonic()
        time.sleep(0.1)
    raise RuntimeError(
        "DispatchEx가 만든 정확히 하나의 새 Hwp.exe PID와 시작 시각을 확인하지 못했습니다."
    )


def _프로세스종료대기(
    프로세스목록: dict[int, int],
    제한초: float = 20.0,
) -> dict[int, int]:
    남음 = dict(프로세스목록)
    마감 = time.monotonic() + 제한초
    while 남음 and time.monotonic() < 마감:
        현재 = _hwp_process_snapshot()
        남음 = {
            pid: 시작
            for pid, 시작 in 남음.items()
            if 현재.get(pid) == 시작
        }
        if 남음:
            time.sleep(0.25)
    현재 = _hwp_process_snapshot()
    return {
        pid: 시작
        for pid, 시작 in 남음.items()
        if 현재.get(pid) == 시작
    }


def _이전보고서읽기() -> dict[str, object]:
    if not REPORT.exists():
        return {}
    try:
        내용 = json.loads(REPORT.read_text(encoding="utf-8"))
    except Exception as 오류:
        raise RuntimeError(
            "이전 실제 HWP 검증 보고서를 읽지 못해 잔류 프로세스 여부를 "
            "안전하게 확인할 수 없습니다."
        ) from 오류
    if not isinstance(내용, dict):
        raise RuntimeError("이전 실제 HWP 검증 보고서 형식이 올바르지 않습니다.")
    return 내용


def _프로세스레코드해석(값: object) -> dict[int, int]:
    결과: dict[int, int] = {}
    if not isinstance(값, list):
        return 결과
    for 항목 in 값:
        if not isinstance(항목, dict):
            continue
        try:
            pid = int(항목["pid"])
            시작 = int(항목["start_time_utc_ticks"])
        except (KeyError, TypeError, ValueError):
            continue
        결과[pid] = 시작
    return 결과


def _이전검증잔류확인(
    이전보고서: dict[str, object],
    현재: dict[int, int],
) -> dict[int, int]:
    """PID 재사용을 구별해 이전 검증 소유 프로세스만 찾는다."""

    후보 = _프로세스레코드해석(
        이전보고서.get("remaining_validation_hwp_processes")
    )
    if not 후보 and 이전보고서.get("process_exit_confirmed") is False:
        후보 = _프로세스레코드해석(이전보고서.get("validation_hwp_processes"))
    잔류 = {
        pid: 시작
        for pid, 시작 in 후보.items()
        if 현재.get(pid) == 시작
    }

    # 시작 시각을 기록하기 전 구형 보고서는 PID가 현재도 살아 있을 때만
    # 보수적으로 차단한다. 해당 프로세스에 종료 명령을 보내지는 않는다.
    if not 잔류:
        legacy = 이전보고서.get("remaining_validation_hwp_process_ids")
        if isinstance(legacy, list):
            for 값 in legacy:
                try:
                    pid = int(값)
                except (TypeError, ValueError):
                    continue
                if pid in 현재:
                    잔류[pid] = 현재[pid]
    return 잔류


def _문서id목록(hwp: object) -> list[int]:
    문서목록 = hwp.XHwpDocuments
    문서수 = int(문서목록.Count)
    결과: list[int] = []
    try:
        for index in range(문서수):
            문서 = 문서목록.Item(index)
            try:
                문서id = int(문서.DocumentID)
            finally:
                문서 = None
            if 문서id in 결과:
                raise RuntimeError("한글이 중복된 DocumentID를 반환했습니다.")
            결과.append(문서id)
    finally:
        문서목록 = None
    return 결과


def _활성문서id(hwp: object) -> int:
    문서목록 = hwp.XHwpDocuments
    문서 = None
    try:
        문서 = 문서목록.Active_XHwpDocument
        if 문서 is None:
            raise RuntimeError("한글의 활성 검증 문서를 확인하지 못했습니다.")
        return int(문서.DocumentID)
    finally:
        문서 = None
        문서목록 = None


def _검증프로세스생존확인(검증프로세스: dict[int, int]) -> tuple[int, int]:
    """소유권을 확정한 단일 PID와 시작 시각이 지금도 같은지 확인한다."""

    if len(검증프로세스) != 1:
        raise RuntimeError(
            "검증 Hwp.exe의 PID 소유권이 정확히 하나로 확정되지 않아 "
            "문서나 프로세스를 종료하지 않습니다."
        )
    pid, 시작시각 = next(iter(검증프로세스.items()))
    if 시작시각 < 0:
        raise RuntimeError(
            "검증 Hwp.exe의 시작 시각을 확인하지 못해 문서나 프로세스를 "
            "종료하지 않습니다."
        )
    현재 = _hwp_process_snapshot()
    if 현재.get(pid) != 시작시각:
        raise RuntimeError(
            "소유권을 확인한 검증 Hwp.exe의 PID 또는 시작 시각이 달라져 "
            "문서나 프로세스를 종료하지 않습니다."
        )
    return pid, 시작시각


def _문서찾기(hwp: object, 대상id: int) -> object:
    """전체 컬렉션에서 정확한 DocumentID 하나만 찾아 반환한다."""

    문서목록 = hwp.XHwpDocuments
    대상 = None
    try:
        for index in range(int(문서목록.Count)):
            문서 = 문서목록.Item(index)
            try:
                if int(문서.DocumentID) != 대상id:
                    continue
                if 대상 is not None:
                    raise RuntimeError(
                        f"한글이 중복된 DocumentID {대상id}를 반환했습니다."
                    )
                대상 = 문서
                문서 = None
            finally:
                문서 = None
    finally:
        문서목록 = None
    if 대상 is None:
        raise RuntimeError(f"검증 문서 {대상id}를 정확히 찾지 못했습니다.")
    return 대상


def _문서활성화확인(hwp: object, 문서: object, 문서id: int) -> None:
    """대상 문서를 활성화하고 COM이 보고하는 활성 ID까지 재검증한다."""

    활성화결과 = 문서.SetActive_XHwpDocument()
    if 활성화결과 is not None and not bool(활성화결과):
        raise RuntimeError(f"검증 문서 {문서id}를 활성화하지 못했습니다.")
    with contextlib.suppress(Exception):
        pythoncom.PumpWaitingMessages()
    활성id = _활성문서id(hwp)
    if 활성id != 문서id:
        raise RuntimeError(
            f"검증 문서 {문서id} 활성화 뒤 실제 활성 DocumentID가 "
            f"{활성id}로 달라 문서를 닫지 않습니다."
        )


def _문서소멸대기(
    hwp: object,
    문서id: int,
    *,
    제한초: float = 2.0,
    간격초: float = 0.05,
) -> list[int]:
    """Close 뒤 대상 ID가 사라질 때까지 메시지를 펌프하며 제한 대기한다."""

    마감 = time.monotonic() + 제한초
    while True:
        현재id = _문서id목록(hwp)
        if 문서id not in 현재id:
            return 현재id
        if time.monotonic() >= 마감:
            raise RuntimeError(
                f"검증 출력 문서 {문서id}가 Close(False) 뒤에도 남아 있습니다."
            )
        with contextlib.suppress(Exception):
            pythoncom.PumpWaitingMessages()
        time.sleep(간격초)


def _소유문서닫기(hwp: object, 소유문서id: list[int]) -> list[int]:
    """출력 문서만 역순으로 닫고 마지막 원본은 안전한 Quit용으로 남긴다."""

    if not 소유문서id or len(set(소유문서id)) != len(소유문서id):
        raise RuntimeError("검증 소유 DocumentID 목록이 비어 있거나 중복됐습니다.")
    현재id = _문서id목록(hwp)
    if len(현재id) != len(소유문서id) or set(현재id) != set(소유문서id):
        알수없는id = sorted(set(현재id) - set(소유문서id))
        누락id = sorted(set(소유문서id) - set(현재id))
        raise RuntimeError(
            "검증 인스턴스의 현재 DocumentID가 소유 목록과 정확히 일치하지 않아 "
            "어떤 문서도 자동 종료하지 않습니다: "
            f"알 수 없음={알수없는id}, 누락={누락id}"
        )

    원본문서id = 소유문서id[0]
    예상id = set(소유문서id)
    닫은id: list[int] = []
    for 문서id in reversed(소유문서id[1:]):
        # 각 파괴적 호출 직전에도 집합을 다시 확인한다. 도중에 사용자가 만든
        # 문서나 예기치 않은 문서가 나타나면 남은 문서는 건드리지 않는다.
        호출직전id = _문서id목록(hwp)
        if len(호출직전id) != len(예상id) or set(호출직전id) != 예상id:
            raise RuntimeError(
                "출력 문서를 닫기 직전 DocumentID 집합이 달라져 추가 문서와 "
                "Quit을 실행하지 않습니다."
            )
        문서 = None
        try:
            문서 = _문서찾기(hwp, 문서id)
            _문서활성화확인(hwp, 문서, 문서id)
            활성화후id = _문서id목록(hwp)
            if len(활성화후id) != len(예상id) or set(활성화후id) != 예상id:
                raise RuntimeError(
                    "출력 문서 활성화 중 DocumentID 집합이 달라져 문서를 "
                    "닫지 않습니다."
                )
            문서.Modified = False
            닫기결과 = 문서.Close(False)
            if 닫기결과 is not None and not bool(닫기결과):
                raise RuntimeError(f"검증 출력 문서 {문서id}를 닫지 못했습니다.")
        finally:
            문서 = None
            gc.collect()
        예상id.remove(문서id)
        닫은뒤id = _문서소멸대기(hwp, 문서id)
        if len(닫은뒤id) != len(예상id) or set(닫은뒤id) != 예상id:
            raise RuntimeError(
                "출력 문서를 닫은 뒤 예상과 다른 DocumentID가 남아 있어 "
                "추가 문서와 Quit을 실행하지 않습니다."
            )
        닫은id.append(문서id)

    남은id = _문서id목록(hwp)
    if len(남은id) != 1 or set(남은id) != {원본문서id}:
        raise RuntimeError(
            "출력 문서 정리 뒤 정확한 원본 문서 하나만 남지 않아 Quit을 "
            "호출하지 않습니다: "
            f"{남은id}"
        )
    원본문서 = None
    try:
        원본문서 = _문서찾기(hwp, 원본문서id)
        _문서활성화확인(hwp, 원본문서, 원본문서id)
        if set(_문서id목록(hwp)) != {원본문서id}:
            raise RuntimeError(
                "원본 문서 활성화 중 다른 문서가 나타나 Quit을 호출하지 않습니다."
            )
        # 마지막 문서는 Close(False)로 빈 컬렉션이 되지 않는 HWP 버전이
        # 있으므로 저장 질문만 막고, 격리 PID에 대한 Quit이 닫도록 남긴다.
        원본문서.Modified = False
    finally:
        원본문서 = None
        gc.collect()
    return 닫은id

# 실제 사용자 프로필과 무관한 합성값만 사용한다. 아래 값 자체도 보고서에는
# 기록하지 않고 성공 여부와 개수만 남긴다.
SOURCE_VALUES = {
    "이름": "검증사용자",
    "전화번호": "010-0000-0000",
    "책임자": "동일검증값",
    "연구자": "동일검증값",
    "과제명": "기존 검증 과제",
}
OUTPUT_VALUES = {
    "이름": "출력사용자",
    "전화번호": "010-1111-2222",
    "책임자": "책임자출력값",
    "연구자": "연구자출력값",
    "과제명": "갱신 검증 과제",
}
PROFILE_IDS = {
    "이름": "profile_field_name_validation",
    "전화번호": "profile_field_phone_validation",
    "책임자": "profile_field_owner_validation",
    "연구자": "profile_field_researcher_validation",
    "과제명": "profile_field_project_validation",
}
ALIASES = {
    "이름": ("성명", "성함"),
    "전화번호": ("연락처", "휴대전화"),
}
TABLE_ROWS = (
    # 같은 대표필드가 대표명과 별칭 위치에서 하나의 출력 선택을 공유한다.
    ("성명", SOURCE_VALUES["이름"]),
    ("이름", SOURCE_VALUES["이름"]),
    ("연락처", SOURCE_VALUES["전화번호"]),
    # 같은 원문 리터럴이어도 서로 다른 대표필드는 별도 토큰이어야 한다.
    ("책임자", SOURCE_VALUES["책임자"]),
    ("연구자", SOURCE_VALUES["연구자"]),
    ("과제명", SOURCE_VALUES["과제명"]),
)
LABELS = tuple(label for label, _ in TABLE_ROWS)


def _root(hwpml: str) -> ET.Element:
    return ET.fromstring(str(hwpml).lstrip("\ufeff"))


def _tag_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1].upper()


def 태그수(hwpml: str, 이름: str) -> int:
    wanted = 이름.upper()
    return sum(1 for element in _root(hwpml).iter() if _tag_name(element) == wanted)


def 태그속성목록(hwpml: str, 이름: str) -> list[dict[str, str]]:
    wanted = 이름.upper()
    return [
        dict(element.attrib)
        for element in _root(hwpml).iter()
        if _tag_name(element) == wanted
    ]


def _비텍스트구조(element: ET.Element) -> tuple:
    """텍스트 값만 제외하고 태그/속성/자식 순서를 보존한 서명."""

    return (
        _tag_name(element),
        tuple(sorted(element.attrib.items())),
        tuple(_비텍스트구조(child) for child in element),
    )


def 태그구조목록(hwpml: str, 이름: str) -> list[tuple]:
    wanted = 이름.upper()
    return [
        _비텍스트구조(element)
        for element in _root(hwpml).iter()
        if _tag_name(element) == wanted
    ]


def _다중집합포함(원본: list[tuple], 결과: list[tuple]) -> bool:
    """결과 문서에 기본 정의가 추가되어도 원본 정의는 모두 있어야 한다."""

    return not (Counter(원본) - Counter(결과))


def _후보위치목록(후보목록: list[dict[str, object]]) -> list[dict[str, object]]:
    """보고서에 값은 싣지 않고 후보의 안정 위치와 대표필드만 남긴다."""

    return [
        {
            "candidate_id": candidate["candidate_id"],
            "canonical_field": candidate["canonical_field"],
            "table": candidate["table"],
            "row": candidate["row"],
            "col": candidate["col"],
            "value_row": candidate["value_row"],
            "value_col": candidate["value_col"],
            "direction": candidate["direction"],
        }
        for candidate in 후보목록
    ]


def _실행필수(hwp: object, action_name: str) -> object:
    """HAction.Run의 조용한 False 반환을 검증 실패로 바꾼다."""

    result = hwp.HAction.Run(action_name)
    if result is False:
        raise RuntimeError(f"한글 작업을 실행하지 못했습니다: {action_name}")
    return result


def _기본값필수(action: object, parameter_set: object, action_name: str) -> None:
    result = action.GetDefault(parameter_set)
    if result is False:
        raise RuntimeError(f"한글 작업 기본값을 가져오지 못했습니다: {action_name}")


def _실행세트필수(action: object, parameter_set: object, action_name: str) -> object:
    result = action.Execute(parameter_set)
    if result is False:
        raise RuntimeError(f"한글 작업을 적용하지 못했습니다: {action_name}")
    return result


def _텍스트삽입(hwp: object, text: str) -> None:
    """실제 동작 검증에 사용된 HInsertText 경로로 문자열을 넣는다."""

    parameter_set = hwp.HParameterSet.HInsertText
    default_result = hwp.HAction.GetDefault("InsertText", parameter_set.HSet)
    if default_result is False:
        raise RuntimeError("한글 InsertText 기본값을 가져오지 못했습니다.")
    parameter_set.Text = text
    result = hwp.HAction.Execute("InsertText", parameter_set.HSet)
    if result is False:
        raise RuntimeError("한글 문서에 검증 문자열을 입력하지 못했습니다.")


def _글자모양(
    hwp: object,
    *,
    size: int,
    color: tuple[int, int, int],
    bold: bool,
) -> None:
    action = hwp.CreateAction("CharShape")
    parameter_set = action.CreateSet()
    _기본값필수(action, parameter_set, "CharShape")
    parameter_set.SetItem("Height", size * 100)
    parameter_set.SetItem("TextColor", hwp.RGBColor(*color))
    parameter_set.SetItem("Bold", int(bold))
    _실행세트필수(action, parameter_set, "CharShape")


def _문서여백(hwp: object) -> None:
    parameter_set = hwp.HParameterSet.HSecDef
    default_result = hwp.HAction.GetDefault("PageSetup", parameter_set.HSet)
    if default_result is False:
        raise RuntimeError("한글 쪽 설정 기본값을 가져오지 못했습니다.")
    page = parameter_set.PageDef
    page.LeftMargin = hwp.MiliToHwpUnit(27)
    page.RightMargin = hwp.MiliToHwpUnit(13)
    page.TopMargin = hwp.MiliToHwpUnit(19)
    page.BottomMargin = hwp.MiliToHwpUnit(11)
    page.HeaderLen = hwp.MiliToHwpUnit(8)
    page.FooterLen = hwp.MiliToHwpUnit(9)
    page.Landscape = 0
    parameter_set.HSet.SetItem("ApplyTo", 3)
    result = hwp.HAction.Execute("PageSetup", parameter_set.HSet)
    if result is False:
        raise RuntimeError("한글 문서의 쪽 설정을 적용하지 못했습니다.")


def _표만들기(hwp: object) -> None:
    widths = (31, 74)
    heights = (11,) * len(TABLE_ROWS)
    parameter_set = hwp.HParameterSet.HTableCreation
    default_result = hwp.HAction.GetDefault("TableCreate", parameter_set.HSet)
    if default_result is False:
        raise RuntimeError("한글 표 만들기 기본값을 가져오지 못했습니다.")
    parameter_set.Rows = len(heights)
    parameter_set.Cols = len(widths)
    parameter_set.WidthType = 2
    parameter_set.HeightType = 1
    parameter_set.CreateItemArray("ColWidth", len(widths))
    for index, width in enumerate(widths):
        parameter_set.ColWidth.SetItem(index, hwp.MiliToHwpUnit(width))
    parameter_set.CreateItemArray("RowHeight", len(heights))
    for index, height in enumerate(heights):
        parameter_set.RowHeight.SetItem(index, hwp.MiliToHwpUnit(height))
    parameter_set.TableProperties.TreatAsChar = 1
    result = hwp.HAction.Execute("TableCreate", parameter_set.HSet)
    if result is False:
        raise RuntimeError("한글 문서에 검증 표를 만들지 못했습니다.")


def _셀배경색(hwp: object, red: int, green: int, blue: int) -> None:
    parameter_set = hwp.HParameterSet.HCellBorderFill
    default_result = hwp.HAction.GetDefault("CellFill", parameter_set.HSet)
    if default_result is False:
        raise RuntimeError("한글 셀 채우기 기본값을 가져오지 못했습니다.")
    fill = parameter_set.FillAttr
    fill.type = hwp.BrushType("NullBrush|WinBrush")
    fill.WinBrushFaceColor = hwp.RGBColor(red, green, blue)
    fill.WinBrushHatchColor = hwp.RGBColor(red, green, blue)
    fill.WinBrushFaceStyle = hwp.HatchStyle("None")
    fill.WindowsBrush = 1
    result = hwp.HAction.Execute("CellFill", parameter_set.HSet)
    if result is False:
        raise RuntimeError("한글 표 셀의 배경색을 적용하지 못했습니다.")


def _표채우기(hwp: object) -> None:
    """별칭과 동일 리터럴 충돌을 포함한 2열 검증 표를 만든다."""

    _표만들기(hwp)
    for index, (label, value) in enumerate(TABLE_ROWS):
        _실행필수(hwp, "ParagraphShapeAlignCenter")
        _글자모양(hwp, size=10, color=(25, 70, 145), bold=True)
        _셀배경색(hwp, 226, 236, 249)
        _텍스트삽입(hwp, label)

        _실행필수(hwp, "TableRightCellAppend")
        _실행필수(hwp, "ParagraphShapeAlignLeft")
        _글자모양(hwp, size=10, color=(35, 35, 35), bold=False)
        _텍스트삽입(hwp, value)
        if index < len(TABLE_ROWS) - 1:
            _실행필수(hwp, "TableRightCellAppend")


def _출력셀값검증(hwpml: str) -> tuple[bool, dict[str, int]]:
    """실제 한글이 다시 내보낸 표에서 대표필드별 값을 재분석한다."""

    result = HWPMLTableFieldAnalyzer().analyze(
        hwpml,
        registered_fields=tuple(PROFILE_IDS),
        aliases=ALIASES,
    )
    values_by_field: dict[str, list[str]] = defaultdict(list)
    for candidate in result.registered_candidates:
        values_by_field[candidate.field].append(candidate.value)

    counts = {field: len(values_by_field.get(field, ())) for field in PROFILE_IDS}
    correct = bool(
        values_by_field.get("이름") == [OUTPUT_VALUES["이름"], OUTPUT_VALUES["이름"]]
        and values_by_field.get("전화번호") == [OUTPUT_VALUES["전화번호"]]
        and values_by_field.get("책임자") == [OUTPUT_VALUES["책임자"]]
        and values_by_field.get("연구자") == [OUTPUT_VALUES["연구자"]]
        and values_by_field.get("과제명") == [OUTPUT_VALUES["과제명"]]
    )
    return correct, counts


def main() -> None:
    hwp = None
    실행잠금 = _검증단독잠금()
    com_initialized = False
    기능검증성공 = False
    기존hwp프로세스: dict[int, int] = {}
    검증hwp프로세스: dict[int, int] = {}
    소유문서id: list[int] = []
    검증인스턴스격리됨 = False
    보고서: dict[str, object] = {
        "feature": "exact_candidate_alias_and_distinct_role_hwp_roundtrip",
        "uses_synthetic_data_only": True,
        "ok": False,
        "document_cleanup_ok": False,
        "document_cleanup_prepared": False,
        "quit_ok": False,
        "quit_attempted": False,
        "quit_command_ok": False,
        "com_uninitialized": False,
        "process_exit_confirmed": False,
        "max_concurrent_hwp_processes": MAX_HWP_PROCESSES,
        "mutex_name": GUI_MUTEX_NAME,
        "mutex_acquired": False,
    }
    try:
        실행잠금.acquire()
        보고서["mutex_acquired"] = True
        보고서["mutex_was_abandoned"] = 실행잠금.abandoned

        기존hwp프로세스 = _hwp_process_snapshot()
        보고서["preexisting_hwp_process_ids"] = sorted(기존hwp프로세스)
        보고서["preexisting_hwp_processes"] = _프로세스목록(기존hwp프로세스)
        보고서["preexisting_hwp_process_count"] = len(기존hwp프로세스)
        이전잔류 = _이전검증잔류확인(_이전보고서읽기(), 기존hwp프로세스)
        if 이전잔류:
            보고서["blocked_by_previous_validation_residue"] = True
            보고서["remaining_validation_hwp_processes"] = _프로세스목록(이전잔류)
            보고서["remaining_validation_hwp_process_ids"] = sorted(이전잔류)
            raise RuntimeError(
                "이전 검증이 만든 Hwp.exe 프로세스가 아직 종료되지 않아 새 검증을 "
                "시작하지 않습니다. 기존 사용자 HWP에는 종료 명령을 보내지 않습니다."
            )
        if len(기존hwp프로세스) >= MAX_HWP_PROCESSES:
            raise RuntimeError(
                "한글 프로세스가 이미 10개 이상이라 새 검증을 시작하지 않습니다."
            )
        # 기존에 떠 있는 사용자의 한글 창에 연결하지 않는다.
        pythoncom.CoInitialize()
        com_initialized = True
        hwp = EnsureDispatch(DispatchEx("HWPFrame.HwpObject"))
        검증hwp프로세스 = _새프로세스확인(기존hwp프로세스)
        보고서["validation_hwp_process_ids"] = sorted(검증hwp프로세스)
        보고서["validation_hwp_processes"] = _프로세스목록(검증hwp프로세스)
        검증인스턴스격리됨 = True

        초기문서id = _문서id목록(hwp)
        if len(초기문서id) != 1:
            raise RuntimeError(
                "독립 검증 인스턴스의 초기 문서가 정확히 하나가 아니어서 "
                "소유권을 안전하게 판정할 수 없습니다."
            )
        원본문서id = 초기문서id[0]
        if _활성문서id(hwp) != 원본문서id:
            raise RuntimeError("초기 활성 문서와 검증 소유 DocumentID가 일치하지 않습니다.")
        소유문서id.append(원본문서id)
        보고서["source_document_id"] = 원본문서id
        보고서["owned_document_ids"] = list(소유문서id)

        생성후프로세스 = _hwp_process_snapshot()
        if any(생성후프로세스.get(pid) != 시작 for pid, 시작 in 검증hwp프로세스.items()):
            raise RuntimeError("소유권을 확인한 검증 Hwp.exe가 문서 작업 전에 종료되었습니다.")
        보고서["post_dispatch_hwp_process_count"] = len(생성후프로세스)
        보고서["post_dispatch_hwp_process_ids"] = sorted(생성후프로세스)
        if len(생성후프로세스) > MAX_HWP_PROCESSES:
            raise RuntimeError(
                "검증 인스턴스 생성 직후 한글 프로세스가 10개를 초과해 문서 작업을 "
                "시작하지 않습니다."
            )
        try:
            보안모듈결과 = hwp.RegisterModule(
                "FilePathCheckDLL", "FilePathCheckerModuleExample"
            )
        except Exception as 오류:
            raise RuntimeError("한글 Automation 보안 모듈 등록에 실패했습니다.") from 오류
        # 같은 인스턴스에 이미 등록되어 있으면 False가 올 수 있으므로 예외가
        # 없었다는 사실을 등록 성공으로 본다.
        보고서["security_module_registered"] = True
        보고서["security_module_return"] = repr(보안모듈결과)

        # DispatchEx 직후 이미 존재하는 빈 문서를 그대로 사용한다. 초기
        # FileNew는 활성 문서가 아닌 새 탭을 만들 수 있어 여기서는 호출하지 않는다.
        _문서여백(hwp)
        _실행필수(hwp, "ParagraphShapeAlignCenter")
        _글자모양(hwp, size=15, color=(15, 52, 96), bold=True)
        _텍스트삽입(hwp, "프리셋 실제 검증 문서")
        _실행필수(hwp, "BreakPara")
        _실행필수(hwp, "ParagraphShapeAlignLeft")
        _글자모양(hwp, size=10, color=(0, 0, 0), bold=False)
        _표채우기(hwp)

        # 선택 전에 전체 문서를 먼저 검사한다. 이 단계가 성공하고 saveblock에
        # TABLE이 없다면 문서 생성이 아니라 선택 범위 문제임을 즉시 구분한다.
        생성전체hwpml = str(hwp.GetTextFile("HWPML2X", "") or "")
        생성전체텍스트 = str(hwp.GetTextFile("TEXT", "") or "")
        if not 생성전체hwpml.strip():
            raise RuntimeError("COM 작업 후 생성 문서 HWPML이 비어 있습니다.")
        생성루트 = _root(생성전체hwpml)
        보고서["generated_document_hwpml_length"] = len(생성전체hwpml)
        보고서["generated_document_text_length"] = len(생성전체텍스트)
        보고서["generated_document_tag_counts"] = dict(
            sorted(Counter(_tag_name(element) for element in 생성루트.iter()).items())
        )
        if 태그수(생성전체hwpml, "TABLE") != 1:
            raise RuntimeError("원시 HAction으로 검증 표를 생성했지만 문서에서 찾지 못했습니다.")
        if 태그수(생성전체hwpml, "CELL") != len(TABLE_ROWS) * 2:
            raise RuntimeError("생성된 검증 표의 셀 개수가 예상과 다릅니다.")

        # 표 안에서 SelectAll을 실행하면 현재 셀만 선택될 수 있다. 커서를 표
        # 밖인 문서 맨 앞으로 옮긴 뒤 문서 전체를 선택하여 saveblock을 내보낸다.
        _실행필수(hwp, "MoveDocBegin")
        선택결과 = _실행필수(hwp, "SelectAll")
        원본hwpml = str(hwp.GetTextFile("HWPML2X", "saveblock") or "")
        _실행필수(hwp, "Cancel")
        if not 원본hwpml.strip():
            raise RuntimeError("선택 영역 HWPML 내보내기 결과가 비어 있습니다.")

        원본루트 = _root(원본hwpml)
        보고서["source_hwpml_length"] = len(원본hwpml)
        보고서["source_root_tag"] = _tag_name(원본루트)
        보고서["source_tag_counts"] = dict(
            sorted(Counter(_tag_name(element) for element in 원본루트.iter()).items())
        )
        if 태그수(원본hwpml, "TABLE") != 1:
            raise RuntimeError(
                "문서 전체에는 표가 있지만 선택 영역 HWPML에는 없습니다. "
                "문서 전체 선택 범위를 만들지 못했습니다."
            )

        분석 = HWPMLTableFieldAnalyzer().analyze(
            원본hwpml,
            registered_fields=tuple(PROFILE_IDS),
            aliases=ALIASES,
        )
        후보목록: list[dict[str, object]] = []
        for candidate in 분석.registered_candidates:
            payload = candidate.as_dict()
            payload["canonical_field"] = candidate.field
            payload["profile_field_id"] = PROFILE_IDS[candidate.field]
            후보목록.append(payload)

        # 실패 시에도 실제 사용자 값이나 본문을 기록하지 않고, 어떤 표 위치가
        # 어떤 대표필드로 판정됐는지만 남겨 분석기와 실제 HWPML의 차이를 진단한다.
        보고서["analysis_candidate_summary"] = [
            {
                "candidate_id": candidate.candidate_id,
                "field": candidate.field,
                "label": candidate.label,
                "registered": candidate.registered,
                "recommended": candidate.recommended,
                "table": candidate.table,
                "row": candidate.row,
                "col": candidate.col,
                "value_row": candidate.value_row,
                "value_col": candidate.value_col,
                "direction": candidate.direction,
                "context_title": candidate.context_title,
                "value_length": len(candidate.value),
            }
            for candidate in 분석.candidates
        ]
        보고서["registered_candidate_count"] = len(분석.registered_candidates)
        보고서["unregistered_candidate_count"] = len(분석.unregistered_candidates)
        if len(후보목록) != len(TABLE_ROWS) or 분석.unregistered_candidates:
            raise RuntimeError(
                "검증 표의 모든 필드/값 후보가 등록 대표필드로 분석되지 않았습니다."
            )

        분류결과 = HWPML등록필드분류기().선택후보분류(원본hwpml, 후보목록)
        프리셋 = 서식프리셋(
            id="style_live_exact_candidate_validation",
            이름="실제 정확 후보 검증",
            hwpml=분류결과.hwpml,
            필드목록=분류결과.필드목록,
            범위="selection_page",
            내용정책="registered_fields",
        )
        입력값 = {
            field.id: OUTPUT_VALUES[field.값유형]
            for field in 프리셋.필드목록
        }
        출력hwpml = HWPML서식치환기().출력용생성(프리셋, 입력값)

        # 독립 COM 인스턴스 안의 새 문서로 실제 로드하고 다시 HWPML을 받는다.
        출력생성전id = set(_문서id목록(hwp))
        출력새문서결과 = _실행필수(hwp, "FileNew")
        출력생성후id = set(_문서id목록(hwp))
        새출력id목록 = sorted(출력생성후id - 출력생성전id)
        # FileNew 직후 생긴 문서는 이후 검증이 실패해도 정확한 ID로 정리한다.
        for 문서id in 새출력id목록:
            if 문서id not in 소유문서id:
                소유문서id.append(문서id)
        보고서["owned_document_ids"] = list(소유문서id)
        if len(새출력id목록) != 1:
            raise RuntimeError(
                "FileNew 뒤 정확히 하나의 새 출력 DocumentID를 확인하지 못했습니다."
            )
        if 출력생성전id - 출력생성후id:
            raise RuntimeError("FileNew가 원본 검증 문서를 예상과 다르게 제거했습니다.")
        출력문서id = 새출력id목록[0]
        if _활성문서id(hwp) != 출력문서id:
            raise RuntimeError("FileNew 뒤 활성 문서가 새 출력 DocumentID와 다릅니다.")
        보고서["output_document_id"] = 출력문서id
        삽입결과 = hwp.SetTextFile(출력hwpml, "HWPML2X", "")
        if 삽입결과 is False:
            raise RuntimeError("정확 후보 출력 HWPML을 새 한글 문서로 불러오지 못했습니다.")
        출력텍스트 = str(hwp.GetTextFile("TEXT", "") or "")
        출력전체hwpml = str(hwp.GetTextFile("HWPML2X", "") or "")
        if not 출력전체hwpml.strip():
            raise RuntimeError("출력 문서 HWPML 재내보내기 결과가 비어 있습니다.")

        원본표수 = 태그수(원본hwpml, "TABLE")
        원본셀수 = 태그수(원본hwpml, "CELL")
        결과표수 = 태그수(출력전체hwpml, "TABLE")
        결과셀수 = 태그수(출력전체hwpml, "CELL")
        원본쪽설정 = 태그속성목록(원본hwpml, "PAGEDEF")
        결과쪽설정 = 태그속성목록(출력전체hwpml, "PAGEDEF")
        원본쪽여백 = 태그속성목록(원본hwpml, "PAGEMARGIN")
        결과쪽여백 = 태그속성목록(출력전체hwpml, "PAGEMARGIN")

        원본표구조 = 태그구조목록(원본hwpml, "TABLE")
        토큰표구조 = 태그구조목록(프리셋.hwpml, "TABLE")
        출력전표구조 = 태그구조목록(출력hwpml, "TABLE")
        결과표구조 = 태그구조목록(출력전체hwpml, "TABLE")
        XML표구조보존 = 원본표구조 == 토큰표구조 == 출력전표구조
        한글표구조보존 = _다중집합포함(원본표구조, 결과표구조)

        정의태그 = ("CHARSHAPE", "PARASHAPE", "BORDERFILL")
        XML서식보존 = all(
            태그구조목록(원본hwpml, tag) == 태그구조목록(출력hwpml, tag)
            for tag in 정의태그
        )
        한글서식보존 = all(
            _다중집합포함(
                태그구조목록(원본hwpml, tag),
                태그구조목록(출력전체hwpml, tag),
            )
            for tag in 정의태그
        )
        쪽서식보존 = bool(
            원본쪽설정
            and 원본쪽설정 == 결과쪽설정
            and 원본쪽여백
            and 원본쪽여백 == 결과쪽여백
        )
        라벨유지 = all(label in 출력텍스트 for label in LABELS)
        표위문맥유지 = "프리셋 실제 검증 문서" in 출력텍스트
        출력셀값정확, 출력후보수 = _출력셀값검증(출력전체hwpml)
        토큰없음 = (
            "{{GOVOFFICE_FIELD_" not in 출력hwpml
            and "{{GOVOFFICE_FIELD_" not in 출력전체hwpml
            and "{{GOVOFFICE_FIELD_" not in 출력텍스트
        )
        대표필드목록 = {field.값유형: field for field in 프리셋.필드목록}
        별칭토큰공유 = bool(
            "이름" in 대표필드목록
            and 프리셋.hwpml.count(대표필드목록["이름"].토큰) == 2
        )
        동일값역할분리 = bool(
            대표필드목록.get("책임자")
            and 대표필드목록.get("연구자")
            and 대표필드목록["책임자"].토큰 != 대표필드목록["연구자"].토큰
            and OUTPUT_VALUES["책임자"] in 출력텍스트
            and OUTPUT_VALUES["연구자"] in 출력텍스트
            and SOURCE_VALUES["책임자"] not in 출력텍스트
        )
        안정ID연결 = {
            field.값유형: field.프로필필드id for field in 프리셋.필드목록
        } == PROFILE_IDS
        후보위치고유 = len(
            {
                tuple(
                    (
                        tuple(segment["element_path"]),
                        segment["text_slot"],
                        segment["start"],
                        segment["end"],
                    )
                    for segment in candidate["locator"]["segments"]
                )
                for candidate in 후보목록
            }
        ) == len(후보목록)
        구조보존 = bool(
            원본표수 == 1
            and 원본셀수 == len(TABLE_ROWS) * 2
            and 결과표수 == 원본표수
            and 결과셀수 == 원본셀수
            and XML표구조보존
            and 한글표구조보존
        )
        서식보존 = XML서식보존 and 한글서식보존

        보고서.update(
            {
                "select_all_result": repr(선택결과),
                "output_file_new_result": repr(출력새문서결과),
                "insert_result": repr(삽입결과),
                "registered_candidate_count": len(분석.registered_candidates),
                "unregistered_candidate_count": len(분석.unregistered_candidates),
                "candidate_locations": _후보위치목록(후보목록),
                "candidate_locations_unique": 후보위치고유,
                "canonical_field_count": 프리셋.필드수,
                "canonical_fields": sorted(대표필드목록),
                "stable_profile_ids_attached": 안정ID연결,
                "alias_positions_share_one_token": 별칭토큰공유,
                "same_literal_distinct_roles_separated": 동일값역할분리,
                "output_candidate_counts": 출력후보수,
                "distinct_values_in_correct_cells": 출력셀값정확,
                "labels_retained": 라벨유지,
                "above_table_context_retained": 표위문맥유지,
                "tokens_removed": 토큰없음,
                "source_table_count": 원본표수,
                "source_cell_count": 원본셀수,
                "result_table_count": 결과표수,
                "result_cell_count": 결과셀수,
                "xml_table_structure_preserved": XML표구조보존,
                "hwp_table_structure_preserved": 한글표구조보존,
                "structure_preserved": 구조보존,
                "xml_format_preserved": XML서식보존,
                "hwp_format_preserved": 한글서식보존,
                "format_preserved": 서식보존,
                "page_format_preserved": 쪽서식보존,
            }
        )
        기능검증성공 = bool(
            삽입결과 is not False
            and len(분석.registered_candidates) == len(TABLE_ROWS)
            and not 분석.unregistered_candidates
            and 프리셋.필드수 == len(PROFILE_IDS)
            and 후보위치고유
            and 안정ID연결
            and 별칭토큰공유
            and 동일값역할분리
            and 출력셀값정확
            and 라벨유지
            and 표위문맥유지
            and 토큰없음
            and 구조보존
            and 서식보존
            and 쪽서식보존
        )
        보고서["functional_ok"] = 기능검증성공
    except Exception as 오류:
        보고서.update(
            {
                "functional_ok": False,
                "error_type": type(오류).__name__,
                "error": str(오류),
                "traceback": traceback.format_exc(),
            }
        )
    finally:
        if hwp is not None and 검증인스턴스격리됨:
            try:
                with contextlib.suppress(Exception):
                    hwp.HAction.Run("Cancel")
                _검증프로세스생존확인(검증hwp프로세스)
                닫은문서id = _소유문서닫기(hwp, 소유문서id)
                _검증프로세스생존확인(검증hwp프로세스)
                종료직전id = _문서id목록(hwp)
                if (
                    not 소유문서id
                    or len(종료직전id) != 1
                    or set(종료직전id) != {소유문서id[0]}
                ):
                    raise RuntimeError(
                        "Quit 직전 정확한 원본 DocumentID 하나만 남지 않아 "
                        "검증 인스턴스를 종료하지 않습니다."
                    )
                보고서["closed_document_ids"] = 닫은문서id
                보고서["cleanup_document_count"] = len(닫은문서id)
                보고서["retained_source_document_id"] = 소유문서id[0]
                보고서["pre_quit_document_ids"] = 종료직전id
                보고서["document_cleanup_prepared"] = True
            except Exception as 오류:
                보고서["document_cleanup_error"] = str(오류)

            if 보고서.get("document_cleanup_prepared"):
                마지막오류 = None
                for 시도 in range(1, 11):
                    try:
                        _검증프로세스생존확인(검증hwp프로세스)
                        재확인id = _문서id목록(hwp)
                        if (
                            len(재확인id) != 1
                            or set(재확인id) != {소유문서id[0]}
                        ):
                            raise RuntimeError(
                                "Quit 호출 직전 DocumentID가 달라져 검증 인스턴스를 "
                                "종료하지 않습니다."
                            )
                    except Exception as 안전오류:
                        if not 보고서.get("quit_attempted"):
                            보고서["quit_skipped_for_process_safety"] = True
                        else:
                            보고서["quit_retry_stopped_for_process_safety"] = True
                        보고서["quit_safety_error"] = str(안전오류)
                        break
                    보고서["quit_attempted"] = True
                    보고서["quit_attempts"] = 시도
                    try:
                        quit결과 = hwp.Quit()
                        if quit결과 is not None and not bool(quit결과):
                            raise RuntimeError("HWP Quit()이 실패를 반환했습니다.")
                        보고서["quit_command_ok"] = True
                        break
                    except Exception as 오류:
                        마지막오류 = 오류
                        pythoncom.PumpWaitingMessages()
                        time.sleep(0.15)
                if not 보고서.get("quit_command_ok") and 마지막오류 is not None:
                    보고서["quit_error"] = str(마지막오류)
            else:
                보고서["quit_skipped_for_document_safety"] = True
            hwp = None
            gc.collect()
            with contextlib.suppress(Exception):
                pythoncom.PumpWaitingMessages()
        elif hwp is not None:
            # 새 PID를 확인하지 못한 객체에는 기존 사용자 문서가 연결됐을 수
            # 있으므로 문서/프로세스 종료 명령을 절대 보내지 않고 참조만 놓는다.
            hwp = None
            gc.collect()
        if com_initialized:
            try:
                pythoncom.CoUninitialize()
                보고서["com_uninitialized"] = True
            except Exception as 오류:
                보고서["com_uninitialize_error"] = str(오류)
        try:
            if 검증hwp프로세스:
                남은검증프로세스 = _프로세스종료대기(검증hwp프로세스)
                보고서["remaining_validation_hwp_processes"] = _프로세스목록(남은검증프로세스)
                보고서["remaining_validation_hwp_process_ids"] = sorted(남은검증프로세스)
                보고서["process_exit_confirmed"] = not 남은검증프로세스
                if (
                    보고서.get("document_cleanup_prepared")
                    and 보고서.get("quit_attempted")
                    and 보고서.get("process_exit_confirmed")
                ):
                    보고서["document_cleanup_ok"] = True
                    보고서["quit_ok"] = True
                    if not 보고서.get("quit_command_ok"):
                        보고서["quit_completed_despite_com_error"] = True
        except Exception as 오류:
            보고서["process_exit_check_error"] = str(오류)
            보고서["process_exit_confirmed"] = False
        try:
            최종프로세스 = _hwp_process_snapshot() if sys.platform == "win32" else {}
            보고서["final_hwp_process_count"] = len(최종프로세스)
            보고서["final_hwp_process_ids"] = sorted(최종프로세스)
            보고서["post_cleanup_process_limit_ok"] = (
                len(최종프로세스) <= MAX_HWP_PROCESSES
            )
        except Exception as 오류:
            보고서["final_process_check_error"] = str(오류)
            보고서["post_cleanup_process_limit_ok"] = False
        보고서["ok"] = bool(
            기능검증성공
            and 보고서.get("document_cleanup_ok")
            and 보고서.get("quit_ok")
            and 보고서.get("com_uninitialized")
            and 보고서.get("process_exit_confirmed")
            and 보고서.get("post_cleanup_process_limit_ok")
        )
        try:
            REPORT.parent.mkdir(parents=True, exist_ok=True)
            임시보고서 = REPORT.with_name(f".{REPORT.name}.tmp")
            with 임시보고서.open("w", encoding="utf-8", newline="\n") as 스트림:
                json.dump(보고서, 스트림, ensure_ascii=False, indent=2)
                스트림.flush()
                os.fsync(스트림.fileno())
            임시보고서.replace(REPORT)
            print(json.dumps(보고서, ensure_ascii=False))
        finally:
            실행잠금.release()
    raise SystemExit(0 if 보고서["ok"] else 1)


if __name__ == "__main__":
    main()
