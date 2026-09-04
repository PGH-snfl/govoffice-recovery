from __future__ import annotations

import contextlib
import gc
import io
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import uuid4


# Windows 리디렉션 파이프에서 시스템 CP949와 UTF-8이 섞이지 않게 고정한다.
for _스트림 in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_스트림, "reconfigure"):
        _스트림.reconfigure(encoding="utf-8", errors="strict")


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from govoffice.adapters.recovered_hwp import 복구한글어댑터
from govoffice.adapters.json_style_presets import JSON서식프리셋저장소
from govoffice.adapters.json_user_profile import JSON사용자프로필저장소
from govoffice.app.function_catalog import 검증완료기능목록, 필수인자목록
from govoffice.domain.user_profile import 기본사용자정보필드
from govoffice.services.format_copy import 서식복사서비스
from govoffice.services.hwpml_table_analysis import (
    HWPMLTableFieldAnalyzer,
    apply_candidate_field_overrides,
    group_related_candidates,
    select_review_candidates,
)
from govoffice.services.style_presets import HWPML등록필드분류기, 서식프리셋서비스
from govoffice.services.user_profile import 사용자프로필서비스


핵심기능 = {"한컴열기", "불러오기", "새창", "취소"}
허용기능 = {item.이름 for item in 검증완료기능목록() if item.검증상태 in {"static_exact", "dynamic_exact"}} | 핵심기능
한글: 복구한글어댑터 | None = None
서식복사 = 서식복사서비스()
서식프리셋: 서식프리셋서비스 | None = None
서식프리셋저장소 = JSON서식프리셋저장소(ROOT / "config" / "style_presets")
사용자프로필저장소 = JSON사용자프로필저장소(ROOT / "config" / "user_profile.json")
_프로토콜출력 = sys.stdout
_서식초안: dict[str, object] | None = None
_최근선택: dict[str, object] | None = None
_수동선택세션: dict[str, object] | None = None
_최근선택유효초 = 300.0
_서식초안유효초 = 900.0
_프로필안정화완료 = False
_최대미확정추천후보 = 10


def 인자해석(value):
    if isinstance(value, dict) and set(value) == {"asset"}:
        relative = str(value["asset"]).replace("\\", "/")
        if relative.startswith("아이콘/"):
            relative = relative[len("아이콘/") :]
        path = (ROOT / "assets" / "icons" / relative).resolve()
        assets_root = (ROOT / "assets" / "icons").resolve()
        if assets_root not in path.parents or not path.is_file():
            raise ValueError(f"기관 이미지 파일을 찾을 수 없습니다: {relative}")
        return str(path)
    if isinstance(value, list):
        return [인자해석(item) for item in value]
    if isinstance(value, dict):
        return {key: 인자해석(item) for key, item in value.items()}
    return value


def 응답(ok: bool, message: str, **extra) -> None:
    # 프로토콜은 ASCII 이스케이프를 사용해 외부 셸의 코드페이지와도 독립시킨다.
    print(json.dumps({"ok": ok, "message": message, **extra}, ensure_ascii=True), file=_프로토콜출력, flush=True)


def 서식프리셋준비() -> None:
    """서비스 객체만 준비하며 한글을 새로 실행하지 않는다."""

    global 한글, 서식프리셋
    if 한글 is None:
        한글 = 복구한글어댑터()
    if 서식프리셋 is None:
        서식프리셋 = 서식프리셋서비스(
            한글,
            서식프리셋저장소,
            개인정보제공=lambda: 사용자프로필서비스(사용자프로필저장소).자동입력값(),
            등록필드제공=lambda: 사용자프로필서비스(사용자프로필저장소).분류입력값(),
        )


def 안정사용자프로필():
    """v2 프로필의 임시 UUID를 첫 사용 시 v3 파일에 한 번 고정한다."""

    global _프로필안정화완료
    서비스 = 사용자프로필서비스(사용자프로필저장소)
    프로필 = 서비스.불러오기()
    if not _프로필안정화완료:
        사용자프로필저장소.저장(프로필)
        프로필 = 서비스.불러오기()
        _프로필안정화완료 = True
    return 프로필


def 선택HWPML본문텍스트(hwpml: str) -> str:
    """현재 수동 드래그 블록에서 문서 본문 글자만 원형대로 이어 붙인다."""

    try:
        루트 = ET.fromstring(str(hwpml).lstrip("\ufeff"))
    except ET.ParseError as 오류:
        raise ValueError(f"직접 선택한 한글 영역을 읽지 못했습니다: {오류}") from 오류
    본문 = next(
        (요소 for 요소 in 루트.iter() if 요소.tag.rsplit("}", 1)[-1].upper() == "BODY"),
        루트,
    )
    조각 = [
        "".join(요소.itertext())
        for 요소 in 본문.iter()
        if 요소.tag.rsplit("}", 1)[-1].upper() == "CHAR"
    ]
    값 = "".join(조각).strip()
    if not 값:
        raise ValueError("한글에서 필드로 지정할 실제 값만 드래그해 선택하세요.")
    if len(값) > 1000 or "\n" in 값 or "\r" in 값:
        raise ValueError("한 번에 한 값만 정확히 드래그해 선택하세요.")
    return 값


def 후보locator겹침(왼쪽: dict[str, object], 오른쪽: dict[str, object]) -> bool:
    def 구간목록(후보: dict[str, object]):
        locator = 후보.get("locator", {})
        if not isinstance(locator, dict):
            return []
        결과 = []
        for 조각 in locator.get("segments", []):
            if not isinstance(조각, dict):
                continue
            결과.append(
                (
                    tuple(조각.get("element_path", [])),
                    str(조각.get("text_slot", "")),
                    int(조각.get("start", 0)),
                    int(조각.get("end", 0)),
                )
            )
        return 결과

    for 왼쪽경로, 왼쪽슬롯, 왼쪽시작, 왼쪽끝 in 구간목록(왼쪽):
        for 오른쪽경로, 오른쪽슬롯, 오른쪽시작, 오른쪽끝 in 구간목록(오른쪽):
            if (
                왼쪽경로 == 오른쪽경로
                and 왼쪽슬롯 == 오른쪽슬롯
                and max(왼쪽시작, 오른쪽시작) < min(왼쪽끝, 오른쪽끝)
            ):
                return True
    return False


def 의미필드키(필드명: object) -> str:
    """셀 관계 확정 뒤 같은 의미의 표시 필드를 보수적으로 묶는 키."""

    이름 = re.sub(r"[\s\-_/·:：()\[\]{}]+", "", str(필드명 or "").casefold())
    for 접미사 in ("기본정보", "상세정보", "정보", "사항", "현황", "내용", "항목", "내역"):
        if 이름.endswith(접미사) and len(이름) > len(접미사) + 1:
            이름 = 이름[: -len(접미사)]
            break
    return 이름


def 연결(*, 관리작업: bool = True) -> None:
    서식프리셋준비()
    assert 한글 is not None
    # 프로그램이 경로로 연 관리 문서가 있으면 ROT의 다른 수동 문서보다 먼저
    # 원본 연결 대상으로 되돌린다.
    한글.문서상태()
    # 복구 코드의 진단 print가 JSON 줄 프로토콜에 섞이지 않게 한다.
    with contextlib.redirect_stdout(io.StringIO()):
        한글.기능실행("한컴열기")
    if 한글.원본.대상 is None:
        raise RuntimeError("한글 COM 객체를 가져오지 못했습니다.")
    # 실제 변경 명령은 앱이 연 관리 원문서의 DocumentID를 명시 활성화하고,
    # COM의 활성 ID가 일치하는지 재확인한 뒤에만 실행한다. 상태 폴링에서는
    # 이 경로를 호출하지 않으므로 사용자가 보고 있는 한글 탭을 빼앗지 않는다.
    if 관리작업:
        한글.관리작업문서활성화()


def 안전문서상태() -> dict[str, object]:
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
    try:
        return 한글.문서상태()
    except Exception as 오류:
        return {
            "connected": False,
            "document_open": False,
            "managed": False,
            "document_id": None,
            "active_document_id": None,
            "output_document_count": 0,
            "output_document_count_exact": False,
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
            "state_error": str(오류),
        }


def 현재선택문서키() -> tuple[object, ...] | None:
    """선택 캐시가 다른 한글 문서에 재사용되지 않게 문서 신원을 묶는다."""

    if 한글 is None:
        return None
    대상 = getattr(한글.원본, "대상", None)
    if 대상 is None:
        return None
    상태 = 안전문서상태()
    활성문서id = 상태.get("active_document_id")
    if not isinstance(활성문서id, str) or not 활성문서id.strip():
        # 활성 문서를 COM DocumentID로 입증하지 못하면 경로/제목/Item(0)을
        # 문서 신원으로 추측하지 않는다. 이 경우 선택 캐시와 초안은 재사용 불가다.
        return None
    return (
        id(대상),
        활성문서id.strip(),
        bool(상태.get("managed")),
        str(상태.get("document_id") or ""),
    )


def 문서키가현재문서인가(문서키: object) -> bool:
    현재문서키 = 현재선택문서키()
    return 문서키 is not None and 현재문서키 is not None and 문서키 == 현재문서키


def 선택캐시가현재문서인가(선택: dict[str, object] | None) -> bool:
    return bool(
        선택 is not None
        and 문서키가현재문서인가(선택.get("document_key"))
    )


def 선택상태무효화() -> None:
    """문서를 바꿀 수 있는 명령 전에 모든 선택 기반 상태를 폐기한다."""

    global _최근선택, _수동선택세션, _서식초안
    _최근선택 = None
    _수동선택세션 = None
    _서식초안 = None


def 서식복사취소() -> None:
    """다른 기능이 실행될 때 남아 있는 모양 복사 모드를 안전하게 해제한다."""

    if not 서식복사.초기화() or 한글 is None or 한글.원본.대상 is None:
        return
    with contextlib.suppress(Exception):
        한글.원본.대상.HAction.Run("Cancel")


def 종료정리() -> None:
    """인터프리터 종료 전에 한글 COM 프록시를 살아 있는 런타임에서 해제한다."""
    global 한글, 서식프리셋
    서식복사취소()
    서식프리셋 = None
    어댑터 = 한글
    한글 = None
    if 어댑터 is None:
        return
    원본 = 어댑터.원본
    대상 = getattr(원본, "대상", None)
    # 사용자가 연 한글 문서는 닫지 않고 이 백엔드가 가진 COM 참조만 끊는다.
    원본.대상 = None
    del 대상
    del 원본
    del 어댑터
    gc.collect()


def 처리(command: dict) -> bool:
    global _최근선택, _수동선택세션, _서식초안
    action = command.get("action")
    if action == "shutdown":
        종료정리()
        응답(True, "백엔드 종료")
        return False
    if action == "connect":
        서식복사취소()
        # 연결 복구 자체는 외부 HWP 상태도 진단할 수 있게 하되, 문서 변경
        # 액션은 아래의 기본 연결() 경로에서 관리 문서를 반드시 요구한다.
        연결(관리작업=False)
        _최근선택 = None
        _수동선택세션 = None
        _서식초안 = None
        응답(True, "한글 연결 완료", document=안전문서상태())
        return True
    if action == "hwp_document_open":
        서식복사취소()
        서식프리셋준비()
        assert 한글 is not None
        경로 = command.get("path", "")
        표시 = command.get("visible", True) is not False
        문서 = 한글.관리문서열기(경로, 표시=표시)
        _최근선택 = None
        _수동선택세션 = None
        _서식초안 = None
        응답(True, "프로그램 전용 한글 문서 열기 완료", document=문서)
        return True
    if action == "hwp_document_status":
        서식프리셋준비()
        응답(True, "현재 한글 문서 상태", document=안전문서상태())
        return True
    if action in {"hwp_document_show", "hwp_window_show"}:
        서식프리셋준비()
        assert 한글 is not None
        문서 = 한글.문서표시()
        응답(True, "한글 문서 창 표시 완료", document=문서)
        return True
    if action in {"hwp_document_minimize", "hwp_window_minimize"}:
        서식프리셋준비()
        assert 한글 is not None
        문서 = 한글.문서최소화()
        응답(True, "한글 문서 창 최소화 완료", document=문서)
        return True
    if action == "hwp_document_close":
        서식복사취소()
        저장선택 = command.get("save_changes") if "save_changes" in command else None
        if 저장선택 is not None and not isinstance(저장선택, bool):
            raise ValueError("save_changes는 true, false 또는 생략 중 하나여야 합니다.")
        서식프리셋준비()
        assert 한글 is not None
        문서 = 한글.관리문서닫기(저장선택)
        if 문서.get("confirmation_required"):
            응답(
                False,
                "문서가 수정됐거나 수정 상태를 확인할 수 없습니다. 저장 여부를 선택해 다시 요청하세요.",
                error_type="ConfirmationRequired",
                action=action,
                confirmation_required=True,
                choices={"save_changes": [True, False]},
                document=문서,
            )
            return True
        _최근선택 = None
        _수동선택세션 = None
        _서식초안 = None
        응답(
            True,
            "프로그램 전용 한글 문서를 저장 확인 대화상자 없이 정상 종료했습니다.",
            document=문서,
        )
        return True
    if action == "user_profile_get":
        프로필 = 안정사용자프로필()
        응답(
            True,
            "사용자 정보 불러오기 완료",
            values=프로필.사전(),
            field_groups=[
                {
                    "id": 대표필드.id,
                    "name": 대표필드.대표필드명,
                    "path": 프로필.필드경로(대표필드),
                    "parent_id": 대표필드.상위필드id or None,
                    "parent_name": (
                        프로필.대표필드ID찾기(대표필드.상위필드id).대표필드명
                        if 대표필드.상위필드id
                        and 프로필.대표필드ID찾기(대표필드.상위필드id) is not None
                        else None
                    ),
                    "aliases": list(대표필드.별칭),
                    "values": list(대표필드.값목록),
                    "default": 대표필드.기본값,
                }
                for 대표필드 in 프로필.대표필드목록
            ],
            value_links=[
                {"value": 값, "fields": list(필드목록)}
                for 값, 필드목록 in 프로필.값별필드목록().items()
            ],
        )
        return True
    if action == "user_profile_save":
        값 = command.get("values", {})
        if not isinstance(값, dict):
            raise ValueError("개인정보 값은 JSON 객체여야 합니다.")
        프로필 = 사용자프로필서비스(사용자프로필저장소).저장(값)
        응답(True, "사용자 정보를 내부용 프로필에 저장했습니다.", values=프로필.사전())
        return True
    if action == "user_profile_basic_save":
        값 = command.get("values", {})
        if not isinstance(값, dict):
            raise ValueError("기본 사용자 정보는 JSON 객체여야 합니다.")
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        전체값 = 서비스.불러오기().사전()
        for 필드 in ("이름", "전화번호", "이메일"):
            전체값[필드] = 값.get(필드, "")
        프로필 = 서비스.저장(전체값)
        응답(True, "기본 사용자 정보를 저장했습니다.", values=프로필.사전())
        return True
    if action == "user_profile_entry_add":
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        이전 = 서비스.불러오기()
        필드명 = str(command.get("field_name", "")).strip()
        입력값 = str(command.get("value", "")).strip()
        if not 필드명:
            raise ValueError("필드 이름을 입력하세요.")
        상위필드ID = str(command.get("parent_field_id", "") or "").strip()
        별칭원본 = command.get("aliases", [])
        if not isinstance(별칭원본, list):
            raise ValueError("별칭은 배열이어야 합니다.")
        상위필드 = 이전.대표필드ID찾기(상위필드ID) if 상위필드ID else None
        if 상위필드ID and 상위필드 is None:
            raise ValueError("선택한 상위 대표필드를 찾지 못했습니다.")
        조회명 = (
            f"{이전.필드경로(상위필드)} > {필드명}"
            if 상위필드 is not None else 필드명
        )
        이전필드 = 이전.대표필드찾기(조회명)
        프로필 = 이전
        구조변경됨 = False
        if 이전필드 is None and 상위필드 is not None:
            # 과거에 독립 대표필드로 만든 이름이 실제로는 새 대표필드의
            # 하위필드였으면 새 필드를 복제하지 않고 기존 ID와 여러 값을
            # 보존한 채 계층만 이동한다.
            독립필드 = 이전.대표필드찾기(필드명)
            이동가능 = (
                독립필드 is not None
                and 독립필드.id != 상위필드.id
                and 독립필드.대표필드명.casefold() == 필드명.casefold()
                and 독립필드.대표필드명.casefold()
                not in {이름.casefold() for 이름 in 기본사용자정보필드}
            )
            if 이동가능:
                프로필 = 이전.대표필드상위변경(독립필드.id, 상위필드.id)
            else:
                프로필 = 이전.하위필드추가(상위필드.id, 필드명)
            구조변경됨 = True
        elif 이전필드 is None:
            # 병합 셀의 대표필드는 자체 값이 없는 구조용 필드일 수 있다.
            프로필 = 이전.대표필드추가(필드명)
            구조변경됨 = True
        대표필드 = 프로필.대표필드찾기(조회명)
        if 대표필드 is None:
            raise RuntimeError("입력한 대표필드를 저장하지 못했습니다.")
        이전값목록 = 대표필드.값목록
        if 입력값:
            프로필 = 프로필.대표필드값추가(대표필드.id, 입력값)
            대표필드 = 프로필.대표필드ID찾기(대표필드.id)
            assert 대표필드 is not None
        이전별칭 = 대표필드.별칭
        정리된별칭 = list(
            dict.fromkeys(str(별칭).strip() for 별칭 in 별칭원본 if str(별칭).strip())
        )
        for 별칭 in 정리된별칭:
            프로필 = 프로필.별칭추가(대표필드.id, 별칭)
            대표필드 = 프로필.대표필드ID찾기(대표필드.id)
            assert 대표필드 is not None
        사용자프로필저장소.저장(프로필)
        추가됨 = bool(입력값) and 입력값 not in 이전값목록
        별칭추가됨 = 대표필드.별칭 != 이전별칭
        if 구조변경됨 and 추가됨:
            메시지 = "필드 계층과 입력값을 저장했습니다."
        elif 구조변경됨:
            메시지 = "값이 없는 대표필드 구조 또는 새 상위 관계를 저장했습니다."
        elif 추가됨 and 별칭추가됨:
            메시지 = "입력값과 대표필드 별칭을 저장했습니다."
        elif 추가됨:
            메시지 = "기타 문서 입력값을 저장했습니다."
        elif 별칭추가됨:
            메시지 = "대표필드 별칭을 저장했습니다."
        else:
            메시지 = "같은 필드·값·별칭이 이미 있어 중복 저장하지 않았습니다."
        응답(
            True,
            메시지,
            added=추가됨,
            aliases_added=별칭추가됨,
            hierarchy_changed=구조변경됨,
            values=프로필.사전(),
        )
        return True
    if action == "user_profile_aliases_set":
        별칭원본 = command.get("aliases", [])
        if not isinstance(별칭원본, list):
            raise ValueError("별칭은 배열이어야 합니다.")
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        프로필 = 서비스.불러오기()
        대표필드 = 프로필.대표필드ID찾기(command.get("field_id", ""))
        if 대표필드 is None:
            raise ValueError("별칭을 수정할 대표필드를 찾지 못했습니다.")
        새별칭목록 = list(
            dict.fromkeys(str(별칭).strip() for 별칭 in 별칭원본 if str(별칭).strip())
        )
        for 기존별칭 in 대표필드.별칭:
            프로필 = 프로필.별칭삭제(대표필드.id, 기존별칭)
        for 새별칭 in 새별칭목록:
            프로필 = 프로필.별칭추가(대표필드.id, 새별칭)
        사용자프로필저장소.저장(프로필)
        응답(True, f"{대표필드.대표필드명} 대표필드의 별칭을 저장했습니다.")
        return True
    if action == "user_profile_default_set":
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        프로필 = 서비스.불러오기()
        대표필드 = 프로필.대표필드ID찾기(command.get("field_id", ""))
        if 대표필드 is None:
            raise ValueError("기본값을 지정할 대표필드를 찾지 못했습니다.")
        프로필 = 프로필.기본값지정(대표필드.id, command.get("value", ""))
        사용자프로필저장소.저장(프로필)
        응답(True, f"{대표필드.대표필드명}의 기본 출력값을 지정했습니다.")
        return True
    if action == "user_profile_field_parent_set":
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        프로필 = 서비스.불러오기()
        대상 = 프로필.대표필드ID찾기(command.get("field_id", ""))
        if 대상 is None:
            raise ValueError("상위를 변경할 필드를 찾지 못했습니다.")
        상위ID = str(command.get("parent_field_id", "") or "").strip()
        상위 = 프로필.대표필드ID찾기(상위ID) if 상위ID else None
        if 상위ID and 상위 is None:
            raise ValueError("새 상위 대표필드를 찾지 못했습니다.")
        결과 = 서비스.대표필드상위변경(대상.id, 상위.id if 상위 else None)
        변경필드 = 결과.대표필드ID찾기(대상.id)
        assert 변경필드 is not None
        새경로 = 결과.필드경로(변경필드)
        응답(
            True,
            f"필드 계층을 '{새경로}'(으)로 변경했습니다. 저장된 여러 값과 별칭은 유지됩니다.",
            field_path=새경로,
            values=결과.사전(),
        )
        return True
    if action == "user_profile_field_merge":
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        프로필 = 서비스.불러오기()
        원본 = 프로필.대표필드ID찾기(command.get("source_field_id", ""))
        대상 = 프로필.대표필드ID찾기(command.get("target_field_id", ""))
        if 원본 is None or 대상 is None:
            raise ValueError("병합할 원본 또는 대상 대표필드를 찾지 못했습니다.")
        결과 = 서비스.대표필드병합(원본.id, 대상.id)
        응답(
            True,
            f"{원본.대표필드명}의 값과 별칭을 {대상.대표필드명}에 병합했습니다.",
            values=결과.사전(),
        )
        return True
    if action == "user_profile_field_delete":
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        프로필 = 서비스.불러오기()
        대표필드 = 프로필.대표필드ID찾기(command.get("field_id", ""))
        if 대표필드 is None:
            raise ValueError("삭제할 대표필드를 찾지 못했습니다.")
        결과 = 서비스.대표필드삭제(대표필드.id)
        응답(
            True,
            f"{대표필드.대표필드명} 대표필드와 저장된 값·별칭을 삭제했습니다.",
            values=결과.사전(),
        )
        return True
    if action == "user_profile_entry_delete":
        서비스 = 사용자프로필서비스(사용자프로필저장소)
        이전 = 서비스.불러오기()
        프로필 = 서비스.문서항목삭제(command.get("field_name", ""), command.get("value", ""))
        삭제됨 = len(프로필.문서항목) < len(이전.문서항목)
        응답(True, "기타 문서 항목을 삭제했습니다." if 삭제됨 else "삭제할 항목을 찾지 못했습니다.", deleted=삭제됨)
        return True
    if action == "user_profile_insert":
        선택상태무효화()
        연결()
        assert 한글 is not None
        필드 = str(command.get("field", ""))
        값 = 한글.관리작업추적실행(
            lambda: 사용자프로필서비스(사용자프로필저장소, 한글).텍스트삽입(필드)
        )
        응답(True, f"{필드} 텍스트를 현재 커서에 삽입했습니다.", value=값)
        return True
    if action == "format_copy":
        선택상태무효화()
        연결()
        assert 한글 is not None
        결과 = 한글.관리작업추적실행(
            lambda: 서식복사.실행(lambda: 한글.기능실행("글자문단모양복사"))
        )
        응답(True, 결과.메시지, stage=결과.단계, result=repr(결과.실행결과))
        return True
    if action == "style_preset_selection_clear":
        _최근선택 = None
        _수동선택세션 = None
        응답(True, "이전 선택 영역을 지웠습니다.", captured=False)
        return True
    if action == "style_preset_manual_selection_begin":
        초안id = str(command.get("draft_id", ""))
        if _서식초안 is None or _서식초안.get("id") != 초안id:
            raise ValueError("서식 분석 초안이 만료되었습니다. 선택 영역을 다시 분석하세요.")
        if not 문서키가현재문서인가(_서식초안.get("document_key")):
            raise ValueError("한글 문서가 변경되었습니다. 저장할 영역을 다시 분석하세요.")
        # 분석 때 남아 있던 전체 선택 블록을 새 수동 선택으로 오인하지 않도록
        # 한글의 선택 상태도 함께 해제한다. 초안 HWPML은 이미 메모리에 있다.
        if 한글 is not None and getattr(한글.원본, "대상", None) is not None:
            with contextlib.suppress(Exception):
                한글.원본.대상.HAction.Run("Cancel")
        선택토큰 = f"manual_selection_{uuid4().hex}"
        _최근선택 = None
        _수동선택세션 = {
            "token": 선택토큰,
            "draft_id": 초안id,
            "started_at": time.monotonic(),
        }
        응답(
            True,
            "한글에서 필드로 지정할 실제 값만 드래그하세요.",
            selection_token=선택토큰,
            captured=False,
        )
        return True
    if action == "style_preset_manual_selection_cancel":
        선택토큰 = str(command.get("selection_token", ""))
        if _수동선택세션 is not None and _수동선택세션.get("token") == 선택토큰:
            _수동선택세션 = None
            _최근선택 = None
        응답(True, "직접 값 선택을 취소했습니다.", captured=False)
        return True
    if action == "style_preset_selection_probe":
        # 한글 창에서 마우스 드래그가 끝난 직후 호출된다. GUI로 포커스를
        # 옮기기 전에 선택 HWPML을 잡아 두어 저장 버튼에서 선택을 놓치지 않는다.
        서식프리셋준비()
        assert 한글 is not None
        문서상태 = 안전문서상태()
        관리문서id = 문서상태.get("document_id")
        관리선택가능 = bool(
            문서상태.get("managed")
            and 문서상태.get("document_open")
            and isinstance(관리문서id, str)
            and 관리문서id
            and 문서상태.get("active_document_id") == 관리문서id
        )
        if not 관리선택가능:
            _최근선택 = None
            응답(
                True,
                (
                    "프로그램의 '문서 열기'로 한글 문서를 불러오세요."
                    if not 문서상태.get("managed")
                    else "관리 원문서를 화면에 표시한 뒤 영역을 선택하세요."
                ),
                captured=False,
                managed_document_ready=False,
            )
            return True
        try:
            선택hwpml = 한글.선택영역서식내보내기()
        except (RuntimeError, ValueError):
            응답(True, "선택 영역 없음", captured=False, managed_document_ready=True)
            return True
        문서키 = 현재선택문서키()
        if 문서키 is None:
            응답(
                True,
                "현재 활성 한글 문서를 식별하지 못해 선택 영역을 저장하지 않았습니다.",
                captured=False,
                managed_document_ready=True,
            )
            return True
        선택시각 = time.monotonic()
        _최근선택 = {
            "hwpml": 선택hwpml,
            "captured_at": 선택시각,
            "document_key": 문서키,
            "manual_token": (
                _수동선택세션.get("token") if _수동선택세션 is not None else None
            ),
        }
        if _수동선택세션 is not None:
            _수동선택세션["captured_at"] = 선택시각
        응답(True, "선택 영역 감지 완료", captured=True, managed_document_ready=True)
        return True
    if action == "style_preset_selection_status":
        서식프리셋준비()
        assert 한글 is not None
        정상창확인 = getattr(한글.원본, "_정상한글창존재", None)
        try:
            한글실행중 = bool(정상창확인()) if callable(정상창확인) else 한글.원본.대상 is not None
        except Exception:
            한글실행중 = 한글.원본.대상 is not None
        문서상태 = 안전문서상태()
        관리문서id = 문서상태.get("document_id")
        관리문서준비 = bool(
            문서상태.get("managed")
            and 문서상태.get("document_open")
            and isinstance(관리문서id, str)
            and 관리문서id
        )
        관리선택가능 = bool(
            관리문서준비 and 문서상태.get("active_document_id") == 관리문서id
        )

        선택출처 = "none"
        선택준비 = False
        if (
            한글실행중
            and 관리선택가능
            and _수동선택세션 is None
            and command.get("probe", True) is not False
        ):
            try:
                선택hwpml = 한글.선택영역서식내보내기()
                문서키 = 현재선택문서키()
                if 문서키 is not None:
                    _최근선택 = {
                        "hwpml": 선택hwpml,
                        "captured_at": time.monotonic(),
                        "document_key": 문서키,
                    }
                    선택준비 = True
                    선택출처 = "live"
            except (RuntimeError, ValueError):
                pass
        if (
            한글실행중
            and 관리선택가능
            and not 선택준비
            and 선택캐시가현재문서인가(_최근선택)
        ):
            선택나이 = time.monotonic() - float(_최근선택.get("captured_at", 0.0))
            수동토큰일치 = (
                _수동선택세션 is None
                or _최근선택.get("manual_token") == _수동선택세션.get("token")
            )
            if 선택나이 <= _최근선택유효초 and 수동토큰일치:
                선택준비 = True
                선택출처 = "manual" if _수동선택세션 is not None else "cached"
        if not 한글실행중 or not 관리선택가능:
            _최근선택 = None

        if not 한글실행중:
            메시지 = "열린 한글 문서가 없습니다."
        elif not 관리문서준비:
            메시지 = "프로그램의 '문서 열기'로 한글 문서를 불러오세요."
        elif not 관리선택가능:
            메시지 = "관리 원문서를 화면에 표시한 뒤 영역을 선택하세요."
        elif 선택준비:
            메시지 = "선택 영역이 확인되었습니다. 바로 프리셋으로 저장할 수 있습니다."
        else:
            메시지 = "한글 문서는 열려 있지만 선택된 영역이 없습니다."
        응답(
            True,
            메시지,
            hwp_running=한글실행중,
            managed_document_ready=관리문서준비,
            managed_document_active=관리선택가능,
            selection_ready=선택준비,
            selection_source=선택출처,
        )
        return True
    if action == "table_edit":
        선택상태무효화()
        서식복사취소()
        연결()
        assert 한글 is not None
        명령표 = {
            "insert_lower_row": ("TableInsertLowerRow", "현재 셀 아래에 행을 추가했습니다."),
            "insert_left_column": ("TableInsertLeftColumn", "현재 셀 왼쪽에 열을 추가했습니다."),
            "insert_right_column": ("TableInsertRightColumn", "현재 셀 오른쪽에 열을 추가했습니다."),
        }
        작업 = str(command.get("operation", ""))
        if 작업 not in 명령표:
            raise ValueError(f"지원하지 않는 표 편집 작업입니다: {작업}")
        한글명령, 메시지 = 명령표[작업]
        결과 = 한글.관리작업추적실행(
            lambda: 한글.원본.대상.HAction.Run(한글명령)
        )
        if 결과 is False:
            raise RuntimeError("한글이 표 편집 명령을 완료하지 못했습니다. 표 셀에 커서를 놓고 다시 실행하세요.")
        응답(True, 메시지, result=repr(결과))
        return True
    if action == "style_preset_capture":
        서식복사취소()
        # 저장 기능은 이미 열린 선택 문서만 사용한다. 일반 연결()을 호출하면
        # 실행 중인 문서를 못 찾았을 때 불필요한 새 한글 문서가 만들어진다.
        서식프리셋준비()
        assert 서식프리셋 is not None
        초안id = str(command.get("draft_id", ""))
        if 초안id:
            if _서식초안 is None or _서식초안.get("id") != 초안id:
                raise ValueError("서식 분석 초안이 만료되었습니다. 선택 영역을 다시 분석하세요.")
            초안나이 = time.monotonic() - float(_서식초안.get("created_at", 0.0))
            if 초안나이 > _서식초안유효초:
                raise ValueError("서식 분석 초안이 만료되었습니다. 선택 영역을 다시 분석하세요.")
            if not 문서키가현재문서인가(_서식초안.get("document_key")):
                raise ValueError("한글 문서가 변경되었습니다. 저장할 영역을 다시 분석하세요.")
            선택후보id원본 = command.get("selected_candidate_ids", [])
            if not isinstance(선택후보id원본, list):
                raise ValueError("저장할 후보 ID 목록은 배열이어야 합니다.")
            선택후보id = list(dict.fromkeys(str(항목) for 항목 in 선택후보id원본))
            후보표 = {
                str(후보["candidate_id"]): 후보
                for 후보 in _서식초안.get("candidates", [])
                if isinstance(후보, dict) and 후보.get("candidate_id")
            }
            알수없는id = [후보id for 후보id in 선택후보id if 후보id not in 후보표]
            if 알수없는id:
                raise ValueError(
                    "분석 결과에 없는 필드 후보가 선택되었습니다. 선택 영역을 다시 분석하세요."
                )
            구조이동후보 = apply_candidate_field_overrides(
                후보표.values(),
                command.get("candidate_field_overrides", {}),
            )
            구조이동후보표 = {
                str(후보["candidate_id"]): 후보
                for 후보 in 구조이동후보
                if 후보.get("candidate_id")
            }
            선택후보 = [dict(구조이동후보표[후보id]) for 후보id in 선택후보id]

            프로필서비스 = 사용자프로필서비스(사용자프로필저장소)
            이전프로필 = 프로필서비스.불러오기()
            if 이전프로필.사전() != _서식초안.get("profile_snapshot"):
                raise ValueError(
                    "검토 중 사용자 필드 정보가 변경되었습니다. 선택 영역을 다시 분석하세요."
                )
            새프로필 = 이전프로필

            def 필드경로부분(경로: object) -> list[str]:
                부분 = [항목.strip() for 항목 in str(경로 or "").split(">") if 항목.strip()]
                if not 부분 or any(len(항목) > 100 for 항목 in 부분):
                    raise ValueError("필드 구조의 경로가 올바르지 않습니다.")
                return 부분

            def 필드경로확보(프로필, 경로: object):
                """임의 깊이의 대표필드 경로를 만들고 마지막 필드를 돌려준다."""

                누적: list[str] = []
                상위필드 = None
                현재프로필 = 프로필
                for 이름 in 필드경로부분(경로):
                    누적.append(이름)
                    현재경로 = " > ".join(누적)
                    현재필드 = 현재프로필.대표필드찾기(현재경로)
                    if 현재필드 is None:
                        현재프로필 = 현재프로필.대표필드추가(
                            이름,
                            상위필드=상위필드.id if 상위필드 else None,
                        )
                        현재필드 = 현재프로필.대표필드찾기(현재경로)
                    if 현재필드 is None:
                        raise RuntimeError(f"대표필드 경로 '{현재경로}'을 만들지 못했습니다.")
                    상위필드 = 현재필드
                return 현재프로필, 상위필드

            # 드래그는 값을 합치는 명령이 아니라 기존 필드 노드의 부모를
            # 바꾸는 명령이다. 안정 ID가 있는 등록 필드는 ID·값·별칭·후손을
            # 그대로 둔 채 먼저 이동하고, 신규 후보는 아래 루프에서 같은
            # 경로의 새 노드로 생성한다.
            처리한이동: set[tuple[str, str, str]] = set()
            이동후보 = sorted(
                선택후보,
                key=lambda 항목: 0
                if str(항목.get("structure_move_kind", "")) == "representative"
                else 1,
            )
            for 후보 in 이동후보:
                이동종류 = str(후보.get("structure_move_kind", "") or "").strip()
                대상상위경로 = str(
                    후보.get("structure_target_parent", "") or ""
                ).strip()
                if 이동종류 not in {"child", "representative"} or not 대상상위경로:
                    continue
                원본ID = (
                    후보.get("source_parent_profile_field_id")
                    if 이동종류 == "representative"
                    else 후보.get("source_profile_field_id")
                )
                원본ID = str(원본ID or "").strip()
                if not 원본ID and 이동종류 == "representative":
                    원본ID = str(후보.get("source_profile_field_id") or "").strip()
                if not 원본ID:
                    continue
                이동키 = (이동종류, 원본ID, 대상상위경로.casefold())
                if 이동키 in 처리한이동:
                    continue
                처리한이동.add(이동키)
                원본필드 = 새프로필.대표필드ID찾기(원본ID)
                if 원본필드 is None:
                    continue
                새프로필, 대상상위 = 필드경로확보(새프로필, 대상상위경로)
                if 대상상위.id == 원본필드.id:
                    raise ValueError("대표필드를 자기 자신 아래로 옮길 수 없습니다.")
                새프로필 = 새프로필.대표필드상위변경(원본필드.id, 대상상위.id)

            for 후보 in 선택후보:
                대표필드명 = str(후보.get("field", "")).strip()
                문서라벨 = str(후보.get("label", 대표필드명)).strip()
                입력값 = str(후보.get("value", "")).strip()
                if not 대표필드명 or not 입력값:
                    raise ValueError("선택한 후보의 필드명 또는 입력값이 비어 있습니다.")
                대표필드 = 새프로필.대표필드찾기(대표필드명)
                if 대표필드 is None:
                    # 표 위 문맥으로 더 구체적인 역할 필드를 추론했더라도
                    # ``성명``처럼 이미 다른 대표필드가 소유한 일반 라벨을
                    # 새 필드의 별칭으로 중복 등록하지 않는다.
                    라벨소유자 = 새프로필.대표필드찾기(문서라벨) if 문서라벨 else None
                    새별칭 = (
                        (문서라벨,)
                        if 문서라벨
                        and 문서라벨.casefold() != 대표필드명.casefold()
                        and 라벨소유자 is None
                        else ()
                    )
                    새프로필, 대표필드 = 필드경로확보(새프로필, 대표필드명)
                    if 대표필드 is None:
                        raise RuntimeError(f"대표필드 '{대표필드명}'을 저장하지 못했습니다.")
                    새프로필 = 새프로필.대표필드값추가(대표필드.id, 입력값)
                    for 별칭 in 새별칭:
                        새프로필 = 새프로필.별칭추가(대표필드.id, 별칭)
                    대표필드 = 새프로필.대표필드찾기(대표필드명)
                else:
                    새프로필 = 새프로필.대표필드값추가(대표필드.id, 입력값)
                    대표필드 = 새프로필.대표필드ID찾기(대표필드.id)
                    라벨소유자 = 새프로필.대표필드찾기(문서라벨) if 문서라벨 else None
                    if (
                        대표필드 is not None
                        and 문서라벨
                        and 문서라벨.casefold() != 대표필드.대표필드명.casefold()
                        and 라벨소유자 is None
                    ):
                        새프로필 = 새프로필.별칭추가(대표필드.id, 문서라벨)
                        대표필드 = 새프로필.대표필드ID찾기(대표필드.id)
                if 대표필드 is None:
                    raise RuntimeError(f"대표필드 '{대표필드명}'을 저장하지 못했습니다.")
                저장경로 = 새프로필.필드경로(대표필드)
                상위필드 = 새프로필.대표필드ID찾기(대표필드.상위필드id)
                후보["field"] = 저장경로
                후보["field_path"] = 저장경로
                후보["canonical_field"] = 저장경로
                후보["profile_field_id"] = 대표필드.id
                후보["representative_field"] = (
                    새프로필.필드경로(상위필드) if 상위필드 else 저장경로
                )
                후보["parent_field"] = (
                    새프로필.필드경로(상위필드) if 상위필드 else None
                )
                후보["parent_profile_field_id"] = 상위필드.id if 상위필드 else None
                후보["child_field"] = 대표필드.대표필드명 if 상위필드 else None

            # 파일을 변경하기 전에 모든 locator와 겹침을 먼저 검증한다.
            HWPML등록필드분류기().선택후보분류(
                str(_서식초안["hwpml"]),
                선택후보,
            )
            프로필변경됨 = 새프로필 != 이전프로필
            try:
                if 프로필변경됨:
                    사용자프로필저장소.저장(새프로필)
                프리셋 = 서식프리셋.선택후보저장(
                    str(command.get("name", "")),
                    str(_서식초안["hwpml"]),
                    선택후보,
                    셀서식규칙=_서식초안.get("style_rules", {}),
                )
            except Exception as 저장오류:
                if 프로필변경됨:
                    try:
                        사용자프로필저장소.저장(이전프로필)
                    except Exception as 복원오류:
                        raise RuntimeError(
                            f"프리셋 저장 실패 후 사용자 프로필 복원도 실패했습니다: {복원오류}"
                        ) from 저장오류
                raise
            _서식초안 = None
        else:
            프리셋 = 서식프리셋.선택영역저장(str(command.get("name", "")))
        응답(
            True,
            f"서식 프리셋 저장 완료: {프리셋.이름}",
            preset={
                "id": 프리셋.id,
                "name": 프리셋.이름,
                "field_count": 프리셋.필드수,
                "created_at": 프리셋.생성시각,
                "scope": 프리셋.범위,
                "content_policy": 프리셋.내용정책,
            },
        )
        return True
    if action == "style_preset_analyze":
        서식복사취소()
        # 사용자가 선택한 기존 문서를 찾되 새 문서를 생성하지 않는다.
        서식프리셋준비()
        assert 한글 is not None
        # 선택 상태 타이머는 활성화하지 않지만, 사용자가 저장을 확정한 분석
        # 액션은 관리 원문서를 DocumentID로 명시 활성화한 뒤 선택을 읽는다.
        한글.관리작업문서활성화()
        try:
            원본hwpml = 한글.선택영역서식내보내기()
            문서키 = 현재선택문서키()
            if 문서키 is None:
                raise ValueError(
                    "현재 활성 한글 문서를 식별하지 못했습니다. 프로그램에서 문서를 다시 불러오세요."
                )
            _최근선택 = {
                "hwpml": 원본hwpml,
                "captured_at": time.monotonic(),
                "document_key": 문서키,
            }
            분석문서키 = 문서키
        except (RuntimeError, ValueError):
            최근선택 = _최근선택
            if (
                not 선택캐시가현재문서인가(최근선택)
                or time.monotonic() - float(최근선택.get("captured_at", 0.0)) > _최근선택유효초
            ):
                raise ValueError(
                    "선택 영역을 찾지 못했습니다. 한글에서 저장할 영역을 "
                    "마우스로 드래그한 뒤 다시 저장하세요."
                )
            원본hwpml = str(최근선택["hwpml"])
            분석문서키 = 최근선택.get("document_key")
        # v2 프로필은 이 시점에 한 번 v3로 고정해 초안과 저장 단계가 같은
        # 안정 대표필드 ID를 사용하게 한다.
        프로필 = 안정사용자프로필()
        분석시작 = time.perf_counter()
        등록필드명 = [프로필.필드경로(필드) for 필드 in 프로필.대표필드목록]
        등록별칭: dict[str, tuple[str, ...]] = {}
        등록값: list[dict[str, object]] = []
        # v3의 평면 호출은 registered_values=[대표필드.사전() ...] 형태였다.
        # v4는 같은 정보에 부모 경로를 덧씌워 안정 ID와 함께 전달한다.
        for 필드 in 프로필.대표필드목록:
            경로 = 프로필.필드경로(필드)
            상위 = 프로필.대표필드ID찾기(필드.상위필드id)
            if 상위 is not None:
                상위경로 = 프로필.필드경로(상위)
                등록별칭[경로] = tuple(
                    dict.fromkeys(
                        (
                            f"{상위경로} > {별칭}",
                            f"{상위경로} {필드.대표필드명}",
                            *(f"{상위경로} {별칭}" for 별칭 in 필드.별칭),
                        )
                    )
                )
            else:
                등록별칭[경로] = 필드.별칭
            정의 = 필드.사전()
            정의["대표필드명"] = 경로
            등록값.append(정의)
        분석결과 = HWPMLTableFieldAnalyzer().analyze(
            원본hwpml,
            registered_fields=등록필드명,
            aliases=등록별칭,
            registered_values=등록값,
        ).as_dict()
        분석소요ms = round((time.perf_counter() - 분석시작) * 1000, 1)
        후보 = 분석결과["candidates"]
        for 항목 in 후보:
            대표필드 = 프로필.대표필드찾기(str(항목.get("field", "")))
            if 대표필드 is not None:
                경로 = 프로필.필드경로(대표필드)
                상위 = 프로필.대표필드ID찾기(대표필드.상위필드id)
                항목["field"] = 경로
                항목["field_path"] = 경로
                항목["canonical_field"] = 경로
                항목["profile_field_id"] = 대표필드.id
                항목["parent_field"] = 프로필.필드경로(상위) if 상위 else None
                항목["parent_profile_field_id"] = 상위.id if 상위 else None
                항목["representative_field"] = (
                    프로필.필드경로(상위) if 상위 else 경로
                )
                항목["child_field"] = 대표필드.대표필드명 if 상위 else None
            elif ">" in str(항목.get("field", "")):
                상위이름, 하위이름 = (
                    부분.strip() for 부분 in str(항목["field"]).rsplit(">", 1)
                )
                항목["field_path"] = str(항목["field"])
                항목["parent_field"] = 상위이름
                항목["representative_field"] = 상위이름
                항목["child_field"] = 하위이름
            else:
                항목["field_path"] = str(항목.get("field", ""))
                항목["representative_field"] = str(항목.get("field", ""))
                항목["child_field"] = None

            # 1단계의 structural_group_id는 셀 좌표로 필드/값 관계를
            # 입증한다. 2단계에서는 그 관계를 바꾸지 않고 등록 ID·별칭과
            # 대표필드명을 보강한다. 이후 같은/유사 필드 또는 값을 검토용
            # 관계 묶음으로만 연결하며 후보 선택 상태는 합치지 않는다.
            구조대표명 = str(항목.get("structural_parent_field", "") or "").strip()
            if 구조대표명:
                의미대표필드 = None
                상위ID = str(항목.get("parent_profile_field_id", "") or "").strip()
                if 상위ID:
                    의미대표필드 = 프로필.대표필드ID찾기(상위ID)
                if 의미대표필드 is None:
                    의미대표필드 = 프로필.대표필드찾기(구조대표명)
                    if 의미대표필드 is not None and 의미대표필드.상위필드id:
                        의미대표필드 = 프로필.대표필드ID찾기(
                            의미대표필드.상위필드id
                        )
                if 의미대표필드 is not None:
                    의미그룹ID = f"profile-parent:{의미대표필드.id}"
                    의미대표명 = 프로필.필드경로(의미대표필드)
                else:
                    의미그룹ID = f"text-parent:{의미필드키(구조대표명)}"
                    의미대표명 = 구조대표명

                if 대표필드 is not None:
                    의미하위ID = f"profile-field:{대표필드.id}"
                    의미하위명 = 대표필드.대표필드명
                else:
                    원문하위명 = str(항목.get("label", 항목.get("child_field", "")))
                    의미하위ID = f"text-field:{의미필드키(원문하위명)}"
                    의미하위명 = 원문하위명
            else:
                의미대표명 = str(
                    항목.get("representative_field", 항목.get("field", ""))
                )
                if 대표필드 is not None:
                    의미그룹ID = f"profile-field:{대표필드.id}"
                else:
                    의미그룹ID = f"text-field:{의미필드키(의미대표명)}"
                의미하위ID = ""
                의미하위명 = str(항목.get("child_field", "") or "")

            항목["semantic_group_id"] = 의미그룹ID
            항목["semantic_representative_field"] = 의미대표명
            항목["semantic_child_id"] = 의미하위ID
            항목["semantic_child_field"] = 의미하위명
        # 확정 추천은 개수 제한 없이 전부 전달하고, 충돌·저신뢰 등
        # 사용자가 판단해야 할 미확정 후보만 상위 10개로 제한한다.
        전체후보수 = len(후보)
        후보 = list(
            group_related_candidates(
                select_review_candidates(후보, _최대미확정추천후보)
            )
        )
        등록후보 = [항목 for 항목 in 후보 if bool(항목.get("registered"))]
        신규후보 = [항목 for 항목 in 후보 if not bool(항목.get("registered"))]
        확정후보수 = sum(bool(항목.get("recommended")) for 항목 in 후보)
        미확정후보수 = len(후보) - 확정후보수
        제외후보수 = 전체후보수 - len(후보)
        if not 문서키가현재문서인가(분석문서키):
            raise ValueError("분석 중 한글 문서가 변경되었습니다. 저장할 영역을 다시 선택하세요.")
        초안id = f"draft_{uuid4().hex}"
        _서식초안 = {
            "id": 초안id,
            "hwpml": 원본hwpml,
            "candidates": 후보,
            "profile_snapshot": 프로필.사전(),
            "document_key": 분석문서키,
            "created_at": time.monotonic(),
            "style_rules": 분석결과.get("style_rules", {}),
        }
        응답(
            True,
            (
                f"선택 영역 분석 완료: 확정 {확정후보수}개 전체 표시, "
                f"미확정 {미확정후보수}개 "
                f"(최대 {_최대미확정추천후보}개)"
            ),
            draft_id=초안id,
            candidates=후보,
            registered_candidates=등록후보,
            unregistered_candidates=신규후보,
            confirmed_candidate_count=확정후보수,
            unconfirmed_candidate_count=미확정후보수,
            excluded_candidate_count=제외후보수,
            unconfirmed_candidate_limit=_최대미확정추천후보,
            no_registered_fields=not any(대표필드.값목록 for 대표필드 in 프로필.대표필드목록),
            analysis_ms=분석소요ms,
            style_rules=분석결과.get("style_rules", {}),
        )
        return True
    if action == "style_preset_manual_candidate":
        초안id = str(command.get("draft_id", ""))
        if _서식초안 is None or _서식초안.get("id") != 초안id:
            raise ValueError("서식 분석 초안이 만료되었습니다. 선택 영역을 다시 분석하세요.")
        if time.monotonic() - float(_서식초안.get("created_at", 0.0)) > _서식초안유효초:
            raise ValueError("서식 분석 초안이 만료되었습니다. 선택 영역을 다시 분석하세요.")
        if not 문서키가현재문서인가(_서식초안.get("document_key")):
            raise ValueError("한글 문서가 변경되었습니다. 저장할 영역을 다시 분석하세요.")
        선택토큰 = str(command.get("selection_token", ""))
        if (
            _수동선택세션 is None
            or _수동선택세션.get("token") != 선택토큰
            or _수동선택세션.get("draft_id") != 초안id
        ):
            raise ValueError("직접 값 선택이 시작되지 않았습니다. 한글에서 값 선택을 다시 누르세요.")
        프로필 = 안정사용자프로필()
        if 프로필.사전() != _서식초안.get("profile_snapshot"):
            raise ValueError("검토 중 사용자 필드 정보가 변경되었습니다. 선택 영역을 다시 분석하세요.")
        입력필드명 = str(command.get("field_name", "")).strip()
        if not 입력필드명 or len(입력필드명) > 100:
            raise ValueError("직접 지정할 대표필드 이름을 입력하세요.")
        대표필드 = 프로필.대표필드찾기(입력필드명)
        대표필드명 = 프로필.필드경로(대표필드) if 대표필드 is not None else 입력필드명
        최근선택 = _최근선택
        if (
            not 선택캐시가현재문서인가(최근선택)
            or time.monotonic() - float(최근선택.get("captured_at", 0.0)) > _최근선택유효초
            or 최근선택.get("manual_token") != 선택토큰
            or float(최근선택.get("captured_at", 0.0))
            < float(_수동선택세션.get("started_at", 0.0))
        ):
            raise ValueError("한글에서 필드로 지정할 실제 값만 드래그한 뒤 다시 가져오세요.")
        직접값 = 선택HWPML본문텍스트(str(최근선택.get("hwpml", "")))
        일치후보 = [
            후보.as_dict()
            for 후보 in HWPMLTableFieldAnalyzer().find_exact_value(
                str(_서식초안["hwpml"]),
                직접값,
                대표필드명,
                대표필드.id if 대표필드 is not None else None,
            )
        ]
        if not 일치후보:
            raise ValueError(
                "직접 선택한 값이 처음 저장하려던 전체 영역에서 발견되지 않았습니다. "
                "전체 영역 안의 값만 정확히 드래그하세요."
            )
        기존후보 = [
            후보
            for 후보 in _서식초안.get("candidates", [])
            if isinstance(후보, dict)
        ]
        반환후보: list[dict[str, object]] = []
        단일위치 = len(일치후보) == 1
        for 새후보 in 일치후보:
            새후보["field"] = 대표필드명
            새후보["canonical_field"] = 대표필드명
            새후보["profile_field_id"] = 대표필드.id if 대표필드 is not None else None
            새후보["manual"] = True
            새후보["recommended"] = 단일위치
            같은후보 = next(
                (
                    후보
                    for 후보 in 기존후보
                    if str(후보.get("field", "")).casefold() == 대표필드명.casefold()
                    and 후보.get("locator") == 새후보.get("locator")
                ),
                None,
            )
            if 같은후보 is None:
                새후보["candidate_id"] = f"manual_{uuid4().hex}"
                기존후보.append(새후보)
                같은후보 = 새후보
            else:
                같은후보.update(
                    {
                        "canonical_field": 대표필드명,
                        "profile_field_id": 대표필드.id if 대표필드 is not None else None,
                        "manual": True,
                        "recommended": 단일위치,
                    }
                )
            반환후보.append(같은후보)

        반환ID = {str(후보["candidate_id"]) for 후보 in 반환후보}
        충돌ID: list[str] = []
        for 후보 in 기존후보:
            후보id = str(후보.get("candidate_id", ""))
            if not 후보id or 후보id in 반환ID:
                continue
            if any(후보locator겹침(후보, 직접후보) for 직접후보 in 반환후보):
                후보["recommended"] = False
                충돌ID.append(후보id)
        _서식초안["candidates"] = 기존후보
        _최근선택 = None
        _수동선택세션 = None
        응답(
            True,
            (
                "직접 선택한 값의 위치를 추가했습니다."
                if 단일위치
                else f"같은 값이 {len(반환후보)}곳에 있어 저장할 위치를 직접 체크해야 합니다."
            ),
            candidates=반환후보,
            conflicting_candidate_ids=충돌ID,
            multiple_locations=not 단일위치,
        )
        return True
    if action == "style_preset_list":
        목록 = [
            {
                "id": 항목.id,
                "name": 항목.이름,
                "field_count": 항목.필드수,
                "created_at": 항목.생성시각,
                "scope": 항목.범위,
                "content_policy": 항목.내용정책,
                "fields": [
                    {
                        "id": 필드.id,
                        "name": 필드.값유형,
                        "profile_field_id": 필드.프로필필드id,
                        "token": 필드.토큰,
                        "occurrence_count": 항목.hwpml.count(필드.토큰),
                    }
                    for 필드 in 항목.필드목록
                ],
            }
            for 항목 in 서식프리셋저장소.목록()
        ]
        응답(True, f"저장된 서식 프리셋 {len(목록)}개", presets=목록)
        return True
    if action == "style_preset_apply":
        선택상태무효화()
        서식복사취소()
        연결()
        assert 서식프리셋 is not None
        입력값 = command.get("values", {})
        if not isinstance(입력값, dict):
            raise ValueError("프리셋 입력값은 JSON 객체여야 합니다.")
        프리셋id = str(command.get("preset_id", ""))
        대상프리셋 = 서식프리셋저장소.불러오기(프리셋id)
        결과 = 한글.관리작업추적실행(
            lambda: 서식프리셋.출력(
                프리셋id, {str(k): str(v) for k, v in 입력값.items()}
            )
        )
        if 대상프리셋.범위 in {"selection_page", "document"}:
            메시지 = "선택 영역의 원본 내용·전체 서식·쪽 설정을 새 한글 문서로 출력했습니다."
        else:
            메시지 = "기존 선택 영역 프리셋을 현재 커서 위치에 출력했습니다."
        응답(True, 메시지, result=repr(결과))
        return True
    if action == "style_preset_delete":
        서식복사취소()
        프리셋id = str(command.get("preset_id", ""))
        삭제됨 = 서식프리셋저장소.삭제(프리셋id)
        if not 삭제됨:
            raise KeyError(f"서식 프리셋을 찾을 수 없습니다: {프리셋id}")
        응답(True, "서식 프리셋을 삭제했습니다.")
        return True
    if action == "run":
        선택상태무효화()
        서식복사취소()
        method = str(command.get("method", ""))
        args = command.get("args", [])
        if method not in 허용기능:
            raise ValueError(f"검증 완료 실행 목록에 없는 기능입니다: {method}")
        if not isinstance(args, list):
            raise ValueError("인자는 JSON 배열이어야 합니다.")
        연결()
        assert 한글 is not None
        required = 필수인자목록(한글.원본, method)
        if len(args) < len(required):
            raise ValueError(f"필수 인자: {', '.join(required)}")
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            result = 한글.관리작업추적실행(
                lambda: 한글.기능실행(method, *args)
            )
        응답(True, f"실행 완료: {method}", result=repr(result), log=captured.getvalue())
        return True
    if action == "h_action":
        선택상태무효화()
        서식복사취소()
        command = str(command.get("command", ""))
        if not command or not command.replace("_", "").isalnum():
            raise ValueError("허용되지 않은 한글 HAction 명령입니다.")
        연결()
        assert 한글 is not None
        result = 한글.관리작업추적실행(
            lambda: 한글.원본.대상.HAction.Run(command)
        )
        응답(True, f"실행 완료: {command}", result=repr(result))
        return True
    if action == "run_sequence":
        선택상태무효화()
        서식복사취소()
        operations = command.get("operations", [])
        if not isinstance(operations, list) or not operations:
            raise ValueError("실행할 버튼 동작이 없습니다.")
        연결()
        assert 한글 is not None
        results = []
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            for operation in operations:
                operation_type = operation.get("type")
                if operation_type == "method":
                    method = str(operation.get("method", ""))
                    args = 인자해석(operation.get("args", []))
                    if method not in 허용기능:
                        raise ValueError(f"실행 제외 기능이 포함됐습니다: {method}")
                    if not isinstance(args, list):
                        raise ValueError(f"복원되지 않은 인자가 있습니다: {method}")
                    required = 필수인자목록(한글.원본, method)
                    if len(args) < len(required):
                        raise ValueError(f"필수 인자가 부족합니다: {method} ({', '.join(required)})")
                    results.append(
                        한글.관리작업추적실행(
                            lambda: 한글.기능실행(method, *args)
                        )
                    )
                elif operation_type == "h_action":
                    hwp_command = str(operation.get("command", ""))
                    if not hwp_command or not hwp_command.replace("_", "").isalnum():
                        raise ValueError("허용되지 않은 HAction 명령입니다.")
                    results.append(
                        한글.관리작업추적실행(
                            lambda: 한글.원본.대상.HAction.Run(hwp_command)
                        )
                    )
                else:
                    raise ValueError(f"알 수 없는 버튼 동작입니다: {operation_type}")
        응답(True, "버튼 동작 실행 완료", result=repr(results), log=captured.getvalue())
        return True
    raise ValueError(f"알 수 없는 요청입니다: {action}")


응답(True, "READY")
try:
    for line in sys.stdin:
        # win32com/gencache가 출력하는 재생성 진단문이 JSON 라인 프로토콜을
        # 깨뜨리지 않도록 요청 처리 중 표준 출력을 격리한다.
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                계속 = 처리(json.loads(line))
            except Exception as error:
                계속 = True
                오류작업 = None
                try:
                    오류작업 = json.loads(line).get("action")
                except Exception:
                    pass
                추가상태 = {}
                if isinstance(오류작업, str) and 오류작업.startswith("hwp_"):
                    추가상태 = {"action": 오류작업, "document": 안전문서상태()}
                응답(False, str(error), error_type=type(error).__name__, **추가상태)
        if not 계속:
            break
finally:
    # GUI가 예기치 않게 닫혀 표준입력이 끊긴 경우에도 COM 프록시를 명시적으로 해제한다.
    종료정리()
