"""안내형 서식 복사를 실제 한글 COM 문서에서 검증한다."""

from __future__ import annotations

import gc
import json
import sys
import traceback
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

import win32com.client  # noqa: E402

from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리 import 기본한컴  # noqa: E402
from govoffice.services.format_copy import 서식복사서비스  # noqa: E402


REPORT = PROJECT / "development" / "reports" / "dynamic_validation" / "guided_format_copy.json"


def 매개변수값(세트, 이름):
    try:
        return 세트.Item(이름)
    except Exception:
        return getattr(세트, 이름, None)


def 현재서식(한글):
    글자액션 = 한글.CreateAction("CharShape")
    글자세트 = 글자액션.CreateSet()
    글자액션.GetDefault(글자세트)

    문단액션 = 한글.CreateAction("ParagraphShape")
    문단세트 = 문단액션.CreateSet()
    문단액션.GetDefault(문단세트)
    return {
        "text_color": 매개변수값(글자세트, "TextColor"),
        "height": 매개변수값(글자세트, "Height"),
        "bold": 매개변수값(글자세트, "Bold"),
        "align_type": 매개변수값(문단세트, "AlignType"),
    }


def main():
    hwp = None
    report = {"feature": "guided_format_copy", "ok": False}
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")
        report["file_new"] = bool(hwp.HAction.Run("FileNew"))
        recovered = 기본한컴()
        recovered.대상 = hwp
        report["security_module_registered"] = bool(recovered._보안모듈등록())

        recovered.문장("원본서식\r\n대상서식")

        # 첫 문단에 눈에 띄는 글자·문단 서식을 만든다.
        hwp.HAction.Run("MoveDocBegin")
        hwp.HAction.Run("ParagraphShapeAlignCenter")
        for _ in "원본서식":
            hwp.HAction.Run("MoveSelNextChar")
        recovered.글자색(220, 30, 30)
        recovered.글자크기(18)
        hwp.HAction.Run("CharShapeBold")

        hwp.HAction.Run("MoveDocBegin")
        source_shape = 현재서식(hwp)

        workflow = 서식복사서비스()
        captured = workflow.실행(recovered.글자문단모양복사)

        # 두 번째 문단 전체를 선택해 같은 버튼의 두 번째 단계로 적용한다.
        hwp.HAction.Run("MoveDocEnd")
        hwp.HAction.Run("MoveSelParaBegin")
        applied = workflow.실행(recovered.글자문단모양복사)
        hwp.HAction.Run("MoveDocEnd")
        target_shape = 현재서식(hwp)

        compared_fields = ("text_color", "height", "bold", "align_type")
        comparisons = {name: source_shape[name] == target_shape[name] for name in compared_fields}
        text = (hwp.GetTextFile("TEXT", "") or "").replace("\r\n", "\n").replace("\r", "\n")
        report.update(
            {
                "source_shape": source_shape,
                "target_shape": target_shape,
                "comparisons": comparisons,
                "content_preserved": "원본서식" in text and "대상서식" in text,
                "captured_stage": captured.단계,
                "applied_stage": applied.단계,
            }
        )
        report["ok"] = (
            all(comparisons.values())
            and report["content_preserved"]
            and captured.단계 == "captured"
            and applied.단계 == "applied"
        )
    except Exception as error:
        report.update(
            {
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
            }
        )
    finally:
        if hwp is not None:
            try:
                hwp.Clear(1)
                report["clear_ok"] = True
            except Exception as error:
                report["clear_ok"] = False
                report["clear_error"] = str(error)
            try:
                hwp.Quit()
                report["quit_ok"] = True
            except Exception as error:
                report["quit_ok"] = False
                report["quit_error"] = str(error)
            hwp = None
            gc.collect()
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(0 if report["ok"] and report.get("clear_ok") and report.get("quit_ok") else 1)


if __name__ == "__main__":
    main()
