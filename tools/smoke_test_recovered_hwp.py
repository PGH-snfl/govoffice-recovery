"""복구된 한글 기능 하나를 실제 COM에서 안전하게 점검한다."""

from __future__ import annotations

import json
import gc
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "recovered"))

import win32com.client  # noqa: E402

from 한컴오피스.한컴라이브러리 import 기본한컴  # noqa: E402


def main():
    output_dir = ROOT / "recovered" / "test_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "의정부목차_복구테스트.json"
    hwp = None
    report = {"method": "의정부목차", "ok": False}
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")
        report["file_new"] = bool(hwp.HAction.Run("FileNew"))
        instance = 기본한컴()
        instance.대상 = hwp
        report["security_module_registered"] = bool(instance._보안모듈등록())
        result = instance.의정부목차()
        text = hwp.GetTextFile("TEXT", "") or ""
        report.update(
            {
                "ok": True,
                "return_value": result,
                "text": text,
                "text_length": len(text),
                "file_io_attempted": False,
                "message": "파일 접근 없이 Python/COM 메모리 실행 완료",
            }
        )
    except Exception as exc:
        report.update(
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "message": "Python/COM 예외 발생",
            }
        )
    finally:
        if hwp is not None:
            try:
                hwp.Clear(1)
                report["clear_ok"] = True
            except Exception as exc:
                report["clear_ok"] = False
                report["clear_error"] = str(exc)
            try:
                hwp.Quit()
                report["quit_ok"] = True
            except Exception as exc:
                report["quit_ok"] = False
                report["quit_error"] = str(exc)
            hwp = None
            gc.collect()
            report["com_released"] = True
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=True))


if __name__ == "__main__":
    main()
