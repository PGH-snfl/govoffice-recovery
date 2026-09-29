"""Reopen the saved HWP in another isolated process and check its content."""
import json
from pathlib import Path
import re
import sys

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.adapters.hwp_template_import import extract_hwp
from govoffice.services.document_authoring import own_text,parse_source


def main():
    report_name=sys.argv[1] if len(sys.argv)>1 else 'input_slot_registration_2026-09-28_native'
    if not re.fullmatch(r'input_slot_(?:registration|recheck)_[a-zA-Z0-9_-]+',report_name):
        raise ValueError('잘못된 검증 보고서 폴더 이름입니다.')
    folder=PROJECT/'development/reports'/report_name
    report=json.loads((folder/'verification.json').read_text(encoding='utf-8'))
    source=Path(report['native_hwp']['path'])
    if source.parent.resolve()!=folder.resolve() or source.suffix.lower()!='.hwp':
        raise ValueError('검증할 한글 파일이 보고서 폴더 밖에 있습니다.')
    recovered=folder/'검증출력_재추출.hml'
    extract_hwp(source,recovered)
    root=parse_source(recovered)
    expected=parse_source(folder/'검증출력.hml')
    texts=[own_text(p) for p in root.iter('P')]
    if '검증' not in texts or any('〔P' in x for x in texts):
        raise AssertionError('저장된 HWP에서 검증값이 없거나 입력칸 표식이 남았습니다.')
    expected_page=expected.find('.//PAGEDEF');actual_page=root.find('.//PAGEDEF')
    page_preserved=(expected_page is not None and actual_page is not None
        and expected_page.attrib==actual_page.attrib
        and expected_page.find('PAGEMARGIN') is not None
        and actual_page.find('PAGEMARGIN') is not None
        and expected_page.find('PAGEMARGIN').attrib==actual_page.find('PAGEMARGIN').attrib)
    table_preserved=sum(1 for _ in expected.iter('TABLE'))==sum(1 for _ in root.iter('TABLE'))
    if not page_preserved or not table_preserved:
        raise AssertionError('저장된 HWP를 다시 열었을 때 쪽 설정 또는 표 개수가 달라졌습니다.')
    native=report.get('native_hwp',{}).get('verification',{})
    if native.get('hwp_bytes')!=source.stat().st_size:
        native['hwp_bytes_before_close']=native['hwp_bytes']
        native['hwp_bytes']=source.stat().st_size
    report['reopened_hwp']={'file_bytes':source.stat().st_size,
                            'paragraphs':len(texts),
                            'sample_value_found':True,'slot_marker_absent':True,
                            'page_setup_preserved':True,'table_count_preserved':True}
    (folder/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report['reopened_hwp'],ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
