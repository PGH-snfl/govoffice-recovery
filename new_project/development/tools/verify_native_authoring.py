"""Re-render a saved response in a dedicated HWP instance for native QA.

Run this helper elevated, matching the desktop launcher. It never opens or
closes an already-running user document and writes only to a new report folder.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import sys
import traceback
from uuid import uuid4
import xml.etree.ElementTree as ET

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'src'))

from govoffice.adapters.hwp_form_export import export_generated_hwp
from govoffice.services.authoring_validation import audit_layout
from govoffice.services.document_authoring import read_json, render_draft


def main():
    report_root = (Path(sys.argv[1]) if len(sys.argv) > 1 else
                   PROJECT / 'development/reports/native_authoring_20260929')
    report = report_root / (datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + uuid4().hex[:8])
    report.mkdir(parents=True, exist_ok=False)
    result_path = report_root / 'latest_result.json'
    template_id = sys.argv[2] if len(sys.argv) > 2 else '2e7a7203e86040c2b75b1b52676c0cfa'
    template = PROJECT / 'config/document_authoring/templates' / template_id
    bundle = (Path(sys.argv[3]) if len(sys.argv) > 3 else
              PROJECT / 'ai_response_library/수소핵융합에너지_20260919_응답묶음_등록양식용.json')
    result = {'status': 'running', 'report': str(report), 'template': str(template),
              'bundle': str(bundle)}
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    try:
        packet = read_json(bundle)
        xml, fields = render_draft(template, read_json(template / 'manifest.json'),
                                   packet['responses'], packet.get('local_values'))
        (report / '작성중.hml').write_text(xml, encoding='utf-8')
        (report / '입력필드.json').write_text(json.dumps(fields, ensure_ascii=False, indent=2), encoding='utf-8')
        parsed = ET.fromstring(xml)
        preflight = audit_layout(xml, fields)
        result.update(status='rendered', field_count=len(fields),
                      equations=len(list(parsed.iter('EQUATION'))),
                      subscript_shapes=len(list(parsed.iter('SUBSCRIPT'))),
                      superscript_shapes=len(list(parsed.iter('SUPERSCRIPT'))),
                      soft_breaks=xml.count('\u200b'),
                      preflight_issues=preflight['issues'],
                      preflight_guide_tables=preflight['remaining_guide_tables'])
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        native = export_generated_hwp(template / 'template.hwp', report / '작성중.hml',
                                      report / '최종출력_검증.hwp')
        result.update(status='completed', native=native)
    except Exception as exc:
        result.update(status='failed', error=str(exc), exception=type(exc).__name__)
        (report / '진단_예외.txt').write_text(traceback.format_exc(), encoding='utf-8')
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(result_path)
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
