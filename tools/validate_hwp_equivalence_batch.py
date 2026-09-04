"""Batch differential HWP execution with progress saved after every method."""

from __future__ import annotations

import argparse
import gc
import inspect
import json
import subprocess
import sys
import time
import traceback
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "recovered"
sys.path[:0] = [str(ROOT / "tools"), str(RECOVERED)]

# The embedded Python has no Tk. Supply a non-UI filedialog module before
# importing recovered/legacy modules so methods can receive deterministic paths.
tk_filedialog = types.ModuleType("tkinter.filedialog")
tk_filedialog.askopenfilenames = lambda *a, **k: ()
tk_filedialog.askopenfilename = lambda *a, **k: ""
tk_filedialog.asksaveasfilename = lambda *a, **k: ""
tkinter_stub = types.ModuleType("tkinter")
tkinter_stub.filedialog = tk_filedialog
sys.modules.setdefault("tkinter", tkinter_stub)
sys.modules.setdefault("tkinter.filedialog", tk_filedialog)

import win32com.client  # noqa: E402
from validate_hwp_equivalence import digest, normalize_hwpml, normalize_text  # noqa: E402
from 한컴오피스.compat.legacy_runtime import (  # noqa: E402
    Legacy기본한컴, Legacy한컴1, Legacy한컴2, Legacy한컴기본,
)
from 한컴오피스.한컴라이브러리 import 기본한컴  # noqa: E402
from 한컴오피스.한컴라이브러리_1 import 한컴1  # noqa: E402
from 한컴오피스.한컴라이브러리_2 import 한컴2  # noqa: E402
from 한컴오피스.한컴라이브러리_기본 import 한컴기본  # noqa: E402


CLASS_MAP = {
    "한컴라이브러리_기본": (Legacy한컴기본, 한컴기본),
    "한컴라이브러리_1": (Legacy한컴1, 한컴1),
    "한컴라이브러리_2": (Legacy한컴2, 한컴2),
    "한컴라이브러리": (Legacy기본한컴, 기본한컴),
}
IMAGE_FIXTURE = ROOT / "범피스1303_분석" / "extracted" / "resources" / "아이콘" / "표탭" / "그림4.png"
TEXT_SELECTION_METHODS = {"역학조사본문"}
TABLE_SELECTION_METHODS = {"전체표스타일제거"}
BLANK_DOCUMENT_METHODS = {
    "소제목", "남해소제목", "서울소제목", "서울소제목블랙", "광주북구표준붙임",
    "합천본문큰제목", "강원소제목", "충남소제목", "부여소제목", "세종소제목",
    "남해소제목2", "광주북구표준소제목", "남양주소제목", "경남도소제목",
    "충남청소제목", "경남도붙임",
}


def new_hwp():
    hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")
    try:
        # A module that is already registered can return False even though it
        # remains usable. An actual COM failure is raised as an exception.
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")
        return hwp
    except Exception:
        close_hwp(hwp)
        raise


def automation_hwp_pids():
    service = win32com.client.GetObject("winmgmts:")
    result = set()
    for process in service.ExecQuery("SELECT ProcessId, CommandLine FROM Win32_Process WHERE Name='Hwp.exe'"):
        command = str(process.CommandLine or "").lower()
        if "-automation" in command and "-embedding" in command:
            result.add(int(process.ProcessId))
    return result


def ensure_created_hwp_gone(before, timeout=5.0):
    created = automation_hwp_pids() - before
    deadline = time.monotonic() + timeout
    while created and time.monotonic() < deadline:
        time.sleep(0.25)
        created &= automation_hwp_pids()
    if created:
        for pid in sorted(created):
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
            )
        deadline = time.monotonic() + 3.0
        while created and time.monotonic() < deadline:
            time.sleep(0.25)
            created &= automation_hwp_pids()
    if created:
        raise RuntimeError(
            "한글 프로세스 종료 확인 실패. 다음 인스턴스를 만들지 않습니다: "
            + ", ".join(map(str, sorted(created)))
        )


def serializable(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def insert_text(hwp, text):
    hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HParameterSet.HInsertText.Text = text
    hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)


def create_table_fixture(hwp):
    creation = hwp.HParameterSet.HTableCreation
    hwp.HAction.GetDefault("TableCreate", creation.HSet)
    creation.Rows = 2
    creation.Cols = 2
    creation.WidthType = 2
    creation.HeightType = 1
    creation.CreateItemArray("ColWidth", 2)
    creation.ColWidth.SetItem(0, hwp.MiliToHwpUnit(30))
    creation.ColWidth.SetItem(1, hwp.MiliToHwpUnit(30))
    creation.CreateItemArray("RowHeight", 2)
    creation.RowHeight.SetItem(0, hwp.MiliToHwpUnit(10))
    creation.RowHeight.SetItem(1, hwp.MiliToHwpUnit(10))
    creation.TableProperties.TreatAsChar = 1
    hwp.HAction.Execute("TableCreate", creation.HSet)
    insert_text(hwp, "100")


def fixture_value(method, name):
    if any(token in name for token in ("이미지", "그림", "로고", "사진", "파일", "경로")):
        return str(IMAGE_FIXTURE)
    if name == "색상" and method in {"금천박스", "광주광산대제목"}:
        return [32, 96, 160]
    if name == "선색":
        return [32, 96, 160]
    if name.startswith("번호") and method in {"경기참고", "경기붙임", "기본서식참고", "충남한장제목"}:
        return "1"
    if name == "숫자" and method == "기본서식참고":
        return "1"
    if name == "데이터":
        return "2026-08-26" if "날짜" in method else "100 120"
    if name == "텍스트배열":
        return ["항목1", "항목2"]
    if name == "열순서":
        return [0, 1]
    if method == "글자폰트바꾸기간격" and name == "폰트1":
        return "함초롬바탕"
    if method == "글자폰트바꾸기간격" and name == "폰트2":
        return "맑은 고딕"
    if name.startswith("폰트"):
        return "맑은 고딕"
    if name in {"글머리", "특수문자", "문자", "표어", "경남표어"}:
        return "-"
    if any(token in name for token in ("내용", "제목", "이름", "찾기", "바꾸기")):
        return "항목1"
    if name in {"종류", "종류2"}:
        return "숫자만"
    if name in {"빨강", "초록", "파랑", "방향", "좌측", "우측", "왼쪽", "오른쪽", "위", "아래", "머리", "꼬리", "상", "하", "좌", "우", "행", "행수", "열수", "가로", "세로", "너비", "높이", "단", "간격"}:
        return 1
    if name.startswith("선색") or any(token in name for token in ("횟수", "개수", "크기", "여백", "내어쓰기", "진하게", "줄간", "자간", "키", "칸", "옵션", "번호", "색상", "숫자", "값", "선타입", "선굵기")):
        return 1
    return "테스트"


def execute(hwp, cls, row, method_args, category, include_content=False):
    original_dialogs = None
    try:
        hwp.Clear(1)
        hwp.HAction.Run("FileNew")
        if row["method"] in BLANK_DOCUMENT_METHODS:
            pass
        elif category == "table_fixture" or row["method"] in TABLE_SELECTION_METHODS:
            create_table_fixture(hwp)
        elif category in {"argument_fixture", "file_fixture"}:
            insert_text(hwp, "항목1\r\n항목2\r\n100")
        if row["method"] in TEXT_SELECTION_METHODS:
            insert_text(hwp, "역학조사 본문 첫째 줄\r\n역학조사 본문 둘째 줄")
            hwp.HAction.Run("SelectAll")
        instance = cls()
        instance.대상 = hwp
        if category == "isolated_interactive":
            original_dialogs = (
                tk_filedialog.askopenfilenames,
                tk_filedialog.askopenfilename,
                tk_filedialog.asksaveasfilename,
            )
            tk_filedialog.askopenfilenames = lambda *a, **k: (str(IMAGE_FIXTURE),)
            tk_filedialog.askopenfilename = lambda *a, **k: str(IMAGE_FIXTURE)
            tk_filedialog.asksaveasfilename = lambda *a, **k: str(ROOT / "recovered" / "metadata" / "dialog_fixture.hwp")
        returned = getattr(instance, row["method"])(*method_args)
        text = normalize_text(hwp.GetTextFile("TEXT", ""))
        hwpml = normalize_hwpml(hwp.GetTextFile("HWPML2X", ""))
        result = {
            "ok": True,
            "return_value": serializable(returned),
            "text_length": len(text),
            "text_sha256": digest(text),
            "hwpml_length": len(hwpml),
            "hwpml_sha256": digest(hwpml),
        }
        if include_content:
            result["text"] = text
            result["hwpml"] = hwpml
        return result
    except Exception as exc:
        return {
            "ok": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
    finally:
        if original_dialogs is not None:
            (
                tk_filedialog.askopenfilenames,
                tk_filedialog.askopenfilename,
                tk_filedialog.asksaveasfilename,
            ) = original_dialogs


def close_hwp(hwp):
    if hwp is None:
        return
    try:
        hwp.Clear(1)
    except Exception:
        pass
    try:
        hwp.Quit()
    except Exception:
        pass


def execute_isolated(cls, row, method_args, category, max_hwp, include_content=False):
    """Release this HWP instance before returning and enforce the window cap."""
    before = automation_hwp_pids()
    if before:
        raise RuntimeError(
            "이전 검증용 한글 프로세스가 남아 있어 새 인스턴스를 만들지 않습니다: "
            + ", ".join(map(str, sorted(before)))
        )
    if len(before) >= max_hwp:
        raise RuntimeError(
            f"한글 자동화 창 제한 {max_hwp}개에 도달해 새 창을 만들지 않습니다: "
            + ", ".join(map(str, sorted(before)))
        )
    last_start_error = None
    for attempt in range(3):
        hwp = None
        try:
            hwp = new_hwp()
            return execute(hwp, cls, row, method_args, category, include_content)
        except Exception as error:
            # Only retry failures that happen before an HWP object exists.
            if hwp is not None:
                raise
            last_start_error = error
        finally:
            close_hwp(hwp)
            hwp = None
            gc.collect()
            ensure_created_hwp_gone(before)
            remaining = automation_hwp_pids()
            if remaining:
                raise RuntimeError(
                    "검증 인스턴스 종료 뒤에도 한글 자동화 프로세스가 남아 있습니다: "
                    + ", ".join(map(str, sorted(remaining)))
                )
        if attempt < 2:
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError("한글 COM 서버를 3회 시도했지만 시작하지 못했습니다") from last_start_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="blank_document")
    parser.add_argument("--status", default="pending_dynamic")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--max-hwp", type=int, default=10, choices=range(1, 11))
    parser.add_argument("--method-list", type=Path)
    parser.add_argument("--include-content", action="store_true")
    parser.add_argument("--recovered-runtime", choices=("canonical", "new-project"), default="canonical")
    args = parser.parse_args()

    class_map = CLASS_MAP
    if args.recovered_runtime == "new-project":
        sys.path.insert(0, str(ROOT / "new_project" / "src"))
        from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리 import 기본한컴 as Project기본한컴
        from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리_1 import 한컴1 as Project한컴1
        from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리_2 import 한컴2 as Project한컴2
        from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리_기본 import 한컴기본 as Project한컴기본

        class_map = {
            "한컴라이브러리_기본": (Legacy한컴기본, Project한컴기본),
            "한컴라이브러리_1": (Legacy한컴1, Project한컴1),
            "한컴라이브러리_2": (Legacy한컴2, Project한컴2),
            "한컴라이브러리": (Legacy기본한컴, Project기본한컴),
        }

    inventory = json.loads(
        (RECOVERED / "metadata" / "hwp_equivalence_inventory.json").read_text(encoding="utf-8")
    )
    selected = [
        row for row in inventory["methods"]
        if row["category"] == args.category and row["status"] == args.status
    ]
    if args.method_list:
        requested = {
            (item["module"], item["method"])
            for item in json.loads(args.method_list.read_text(encoding="utf-8"))
        }
        selected = [row for row in selected if (row["module"], row["method"]) in requested]
    selected = selected[args.start:]
    if args.limit:
        selected = selected[: args.limit]
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {"category": args.category, "selected": len(selected), "completed": 0, "results": []}
    try:
        for index, row in enumerate(selected, 1):
            legacy_class, recovered_class = class_map[row["module"]]
            parameters = list(inspect.signature(getattr(legacy_class, row["method"])).parameters.values())
            method_args = [
                parameter.default
                if parameter.default is not inspect.Parameter.empty
                else fixture_value(row["method"], parameter.name)
                for parameter in parameters
                if parameter.name != "self"
            ]
            print(json.dumps({"phase": "legacy", "method": row["method"]}, ensure_ascii=False), flush=True)
            legacy = execute_isolated(legacy_class, row, method_args, args.category, args.max_hwp, args.include_content)
            print(json.dumps({"phase": "recovered", "method": row["method"]}, ensure_ascii=False), flush=True)
            recovered = execute_isolated(recovered_class, row, method_args, args.category, args.max_hwp, args.include_content)
            comparison = {
                "both_ok": bool(legacy.get("ok") and recovered.get("ok")),
                "outcome_equal": legacy.get("ok") == recovered.get("ok"),
                "text_equal": legacy.get("text_sha256") == recovered.get("text_sha256")
                if legacy.get("ok") and recovered.get("ok") else False,
                "hwpml_equal": legacy.get("hwpml_sha256") == recovered.get("hwpml_sha256")
                if legacy.get("ok") and recovered.get("ok") else False,
                "return_equal": legacy.get("return_value") == recovered.get("return_value")
                if legacy.get("ok") and recovered.get("ok") else False,
                "error_type_equal": legacy.get("error_type") == recovered.get("error_type")
                if not legacy.get("ok") and not recovered.get("ok") else False,
            }
            report["results"].append({
                "module": row["module"], "method": row["method"],
                "args": method_args,
                "legacy": legacy, "recovered": recovered, "comparison": comparison,
            })
            report["completed"] = index
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"index": index, "method": row["method"], **comparison}, ensure_ascii=False), flush=True)
    finally:
        gc.collect()


if __name__ == "__main__":
    main()
