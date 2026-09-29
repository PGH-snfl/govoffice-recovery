"""Read-only probe of one explicitly identified running HWP window.

Does not activate, edit, save, register modules, create instances, or quit HWP.
Only counts/flags are printed; selection text and personal values stay in memory.
"""
import argparse
import json
import sys
import xml.etree.ElementTree as ET
import time
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
import pythoncom
import win32com.client
from govoffice.adapters.recovered_hwp import 복구한글어댑터
from govoffice.services.hwpml_table_analysis import HWPMLTableFieldAnalyzer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--document', required=True)
    parser.add_argument('--report', action='store_true')
    args = parser.parse_args()
    if args.report:
        report_path = Path(__file__).resolve().parents[2] / 'development/reports/dynamic_validation/current_selection_diagnostic.jsonl'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        sys.stdout = report_path.open('w', encoding='utf-8', buffering=1)
    pythoncom.CoInitialize()
    rot = pythoncom.GetRunningObjectTable()
    context = pythoncom.CreateBindCtx(0)
    matched = []
    for moniker in rot:
        if 'hwpobject' not in moniker.GetDisplayName(context, None).lower():
            continue
        try:
            obj = win32com.client.Dispatch(rot.GetObject(moniker).QueryInterface(pythoncom.IID_IDispatch))
            document_path = str(obj.Path)
        except Exception:
            continue
        if Path(document_path) == Path(args.document):
            matched.append(obj)
    if len(matched) != 1:
        print(json.dumps(dict(matched_objects=len(matched), status='exact document binding unavailable')))
        return
    obj = matched[0]
    report = dict(exact_document_matched=True, selection_mode=int(obj.SelectionMode))
    print(json.dumps(report), flush=True)
    if int(obj.SelectionMode) & 15 != 3:
        print(json.dumps({'status': 'no current cell selection; nothing read'}), flush=True)
        return
    before = (int(obj.SelectionMode), tuple(obj.GetPos()))
    labels = ('연구개발과제명', '주관연구개발기관', '연구책임자', '연구개발기간', '연구개발비')
    def summary(text):
        flat = ''.join(str(text).split())
        return dict(characters=len(text), compact_characters=len(flat),
                    labels={label: label in flat for label in labels})
    for option in ('saveblock', 'saveblock:true'):
        for fmt in ('TEXT', 'UNICODE', 'HTML', 'HWPML2X'):
            try:
                value = obj.GetTextFile(fmt, option)
                item = dict(format=fmt, option=option, **summary(value))
                if fmt == 'HWPML2X':
                    root = ET.fromstring(value)
                    body = root.find('BODY')
                    item['body_text'] = summary(''.join(''.join(c.itertext()) for c in body.iter('CHAR')))
                    item['tables'] = [dict(t.attrib) for t in body.iter('TABLE')]
                    item['cells'] = sum(1 for _ in body.iter('CELL'))
                print(json.dumps(item, ensure_ascii=True), flush=True)
            except Exception as exc:
                print(json.dumps(dict(format=fmt,option=option,error=type(exc).__name__)),flush=True)
    try:
        ok = obj.InitScan(7,255)
        if not ok:
            raise ValueError('selected scan initialization failed')
        parts=[];states=[];deadline=time.monotonic()+10
        while len(states)<10000 and time.monotonic()<deadline:
            state, value = obj.GetText()
            parts.append(value); states.append(state)
            if state in (0,1,101,102): break
        print(json.dumps(dict(scan=summary(''.join(parts)),records=len(states),states=states[:40],last_state=states[-1])),flush=True)
        grouped=[]; pending=''
        for state, text in zip(states,parts):
            pending += text
            if state == 2:
                grouped.append(pending);pending=''
        if pending.strip(): grouped.append(pending)
        normalize=lambda text: ''.join(text.split())
        native_cells=[c for c in body.iter('CELL')]
        matches=[]
        for text in grouped:
            found=[dict(c.attrib) for c in native_cells if normalize(''.join(''.join(ch.itertext()) for ch in c.iter('CHAR')))==normalize(text)]
            matches.append(dict(characters=len(text),matches=found))
        print(json.dumps(dict(grouped_cells=len(grouped),matching_cells=matches,indicator=obj.KeyIndicator()[-1]),ensure_ascii=True),flush=True)
    finally:
        obj.ReleaseScan()
    print(json.dumps(dict(selection_unchanged=before==(int(obj.SelectionMode),tuple(obj.GetPos())))),flush=True)
    try:
        start = obj.CreateSet('ListParaPos'); end = obj.CreateSet('ListParaPos')
        ok = obj.GetSelectedPosBySet(start, end)
        equal = all(start.Item(k) == end.Item(k) for k in ('List','Para','Pos'))
        report.update(text_range_api_ok=bool(ok), text_range_equal=equal,
                      old_guard_accepts=bool(ok) and not equal)
    except Exception as error:
        report['position_error'] = type(error).__name__
    adapter = 복구한글어댑터(SimpleNamespace(대상=obj))
    try:
        source = adapter.선택영역서식내보내기(선택텍스트검증=True)
        report['export_characters'] = len(source)
        report['cropped_text'] = summary(''.join(''.join(c.itertext()) for c in ET.fromstring(source).iter('CHAR')))
        report['analysis_candidate_count'] = len(HWPMLTableFieldAnalyzer().analyze(source).as_dict()['candidates'])
        report['new_guard_accepts'] = True
    except Exception as error:
        report['new_guard_accepts'] = False
        report['read_error'] = type(error).__name__
        report['read_message'] = str(error)
    report['diagnostic'] = adapter.최근선택진단
    print(json.dumps(report, ensure_ascii=True))


if __name__ == '__main__':
    main()
