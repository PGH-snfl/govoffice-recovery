"""Export the specified application form through an owned Hancom document only."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from govoffice.adapters.recovered_hwp import 복구한글어댑터


def main():
    source = ROOT.parent / 'materials/submission-reference/제출서류/[제출서류1] 신청용 연구개발계획서(2026)-기후부(수정_재공고).hwp'
    target = ROOT / 'src/govoffice/institutions/packages/seoultech/climate_2026'
    target.mkdir(parents=True, exist_ok=True)
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    working = Path(tempfile.mkdtemp(prefix='govoffice_climate_extract_')) / source.name
    shutil.copy2(source, working)
    adapter = 복구한글어댑터()
    try:
        print('OPEN_OWNED_COPY', flush=True)
        adapter.관리문서열기(working, 표시=False)
        app = adapter.원본.대상
        print('EXPORT_HWPML', flush=True)
        xml = app.GetTextFile('HWPML2X', '')
        text = app.GetTextFile('TEXT', '')
        if not xml or not text:
            raise RuntimeError('Empty document export')
        root = ET.fromstring(xml)
        rows = []
        for index, paragraph in enumerate(root.iter('P')):
            # Do not repeat nested table paragraphs inside their host paragraph.
            chunks = []
            for child in paragraph:
                if child.tag == 'TEXT':
                    for char in child:
                        if char.tag == 'CHAR':
                            chunks.append(''.join(char.itertext()))
            rows.append({'index': index, 'text': ''.join(chunks), 'para_shape': paragraph.get('ParaShape')})
        (target / 'source.hwpml').write_text(xml, encoding='utf-8')
        (target / 'source_text.txt').write_text(text, encoding='utf-8')
        (target / 'source_paragraphs.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
        metadata = {'source_name': source.name, 'sha256': before, 'paragraphs': len(rows), 'text_characters': len(text), 'pages': int(app.PageCount)}
        (target / 'source_manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(metadata, ensure_ascii=True), flush=True)
    finally:
        if adapter.문서상태().get('managed'):
            adapter.관리문서닫기(저장여부=False)
        if hashlib.sha256(source.read_bytes()).hexdigest() != before:
            raise RuntimeError('Source changed')


if __name__ == '__main__':
    main()
