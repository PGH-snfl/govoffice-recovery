"""Compare native selection exports in an owned, synthetic HWP instance only.

Never attaches to an existing document, uses the clipboard, or saves a file.
PID/start-time and DocumentID ownership must be proven before editing/closing.
"""
from __future__ import annotations

import gc
import faulthandler
import json
import xml.etree.ElementTree as ET
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_style_preset as v


def describe(hwp):
    result = {"mode": int(hwp.SelectionMode), "pos": hwp.GetPos()}
    for fmt, option in ((f, o) for o in ('saveblock', 'saveblock:true') for f in ('TEXT', 'UNICODE', 'HTML', 'HWPML2X')):
        data = hwp.GetTextFile(fmt, option)
        key = fmt + ':' + option
        if fmt != "HWPML2X":
            result[key] = data
        else:
            root = ET.fromstring(data) if data else ET.Element("EMPTY")
            result[key] = {
                "cells": ["".join(c.itertext()).strip() for c in root.iter("CELL")],
                "tables": [c.attrib for c in root.iter("TABLE")],
                "selection_tags": [
                    [c.tag, c.attrib] for c in root.iter()
                    if any(s in c.tag.upper() for s in ("SEL", "ZONE"))
                ],
            }
    try:
        start, end = hwp.CreateSet("ListParaPos"), hwp.CreateSet("ListParaPos")
        result["selected_pos_ok"] = hwp.GetSelectedPosBySet(start, end)
        result["selected_pos"] = [[s.Item(k) for k in ("List", "Para", "Pos")] for s in (start, end)]
    except Exception as exc:
        result["selected_pos_error"] = type(exc).__name__
    records = []
    try:
        result["scan_init"] = hwp.InitScan(7, 255)
        for _ in range(100):
            state, text = hwp.GetText()
            records.append([state, text])
            if state in (0, 1, 101, 102):
                break
    finally:
        hwp.ReleaseScan()
    result["scan"] = records
    return result


def main():
    faulthandler.dump_traceback_later(15, repeat=False)
    print("probe: process snapshot", flush=True)
    before = v._hwp_process_snapshot()
    if len(before) >= v.MAX_HWP_PROCESSES:
        raise RuntimeError("Too many HWP instances; not starting a probe.")
    v.pythoncom.CoInitialize()
    hwp, owned, documents = None, {}, []
    try:
        print("probe: DispatchEx", flush=True)
        hwp = v.DispatchEx("HWPFrame.HwpObject")
        print("probe: EnsureDispatch", flush=True)
        hwp = v.EnsureDispatch(hwp)
        print("probe: ownership", flush=True)
        owned = v._새프로세스확인(before)
        documents = v._문서id목록(hwp)
        if len(documents) != 1 or v._활성문서id(hwp) != documents[0]:
            documents = []
            raise RuntimeError("Cannot prove exclusive ownership of a blank document.")
        if str(hwp.XHwpDocuments.Active_XHwpDocument.Path or ""):
            documents = []
            raise RuntimeError("New document is not blank; no operations allowed.")
        v._검증프로세스생존확인(owned)
        print(json.dumps({"owned_process": owned, "owned_documents": documents}), flush=True)
        p = hwp.HParameterSet.HTableCreation
        hwp.HAction.GetDefault("TableCreate", p.HSet)
        p.Rows, p.Cols, p.WidthType, p.HeightType = 4, 3, 2, 1
        p.CreateItemArray("ColWidth", 3)
        p.CreateItemArray("RowHeight", 4)
        for i in range(3):
            p.ColWidth.SetItem(i, hwp.MiliToHwpUnit(35))
        for i in range(4):
            p.RowHeight.SetItem(i, hwp.MiliToHwpUnit(10))
        p.TableProperties.TreatAsChar = 1
        assert hwp.HAction.Execute("TableCreate", p.HSet) is not False
        positions = []
        for i in range(12):
            positions.append(hwp.GetPos())
            v._텍스트삽입(hwp, f"R{i // 3 + 1}C{i % 3 + 1}")
            if i != 11:
                v._실행필수(hwp, "TableRightCellAppend")
        for name, actions in (
            ("one_cell", ("TableCellBlock",)),
            ("two_cells", ("TableCellBlock", "TableCellBlockExtend", "MoveRight")),
            ("rectangle", ("TableCellBlock", "TableCellBlockExtend", "MoveRight", "MoveDown")),
        ):
            v._실행필수(hwp, "Cancel")
            assert hwp.SetPos(*positions[4]) is not False
            for action in actions:
                v._실행필수(hwp, action)
            print(json.dumps({"case": name, **describe(hwp)}, ensure_ascii=False), flush=True)
    finally:
        if hwp is not None and owned and documents:
            v._검증프로세스생존확인(owned)
            if v._문서id목록(hwp) != documents or v._활성문서id(hwp) != documents[0]:
                raise RuntimeError("Ownership changed; refusing to close HWP.")
            hwp.XHwpDocuments.Active_XHwpDocument.Modified = False
            hwp.Quit()
        hwp = None
        faulthandler.cancel_dump_traceback_later()
        gc.collect()
        v.pythoncom.CoUninitialize()
        if owned:
            print(json.dumps({"remaining_owned_processes": v._프로세스종료대기(owned, 제한초=5)}), flush=True)


if __name__ == "__main__":
    if '--report' in sys.argv:
        # This report contains only synthetic canaries generated in this script.
        report = Path(__file__).resolve().parents[2] / 'development/reports/dynamic_validation/native_cell_selection.txt'
        report.parent.mkdir(parents=True, exist_ok=True)
        with report.open('w', encoding='utf-8', buffering=1) as stream:
            sys.stdout = sys.stderr = stream
            try:
                main()
            except Exception:
                import traceback
                traceback.print_exc()
                raise
    else:
        main()
