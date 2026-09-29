"""Build loss-audited Markdown references from the complete HWPML export."""
from pathlib import Path
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'src/govoffice/institutions/packages/seoultech/climate_2026'


def own_text(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')


def main():
    root = ET.fromstring((ASSETS / 'source.hwpml').read_text(encoding='utf-8'))
    paragraphs = list(root.iter('P'))
    indices = {id(p): i for i, p in enumerate(paragraphs)}
    tables = list(root.iter('TABLE'))
    guides = []
    for table in tables:
        texts = [own_text(p) for p in table.iter('P')]
        if texts and '작성요령' in ''.join(texts[:2]).replace(' ', ''):
            guides.append(table)
    guide_ids = {indices[id(p)] for t in guides for p in t.iter('P')}
    nonempty = [(i, own_text(p)) for i, p in enumerate(paragraphs) if own_text(p).strip()]
    full = ['# 기후부 2026 신청용 연구개발계획서 — 전체 원문 대조본', '',
            '원본의 모든 비어 있지 않은 문단을 순서대로 보존했다. P번호는 원본 HWPML 문단 위치이며 쪽번호가 아니다.',
            '표 셀 문단도 포함한다. 원문 오탈자는 고치지 않았다. 이 문서는 제출본이 아니라 누락 대조용이다.', '']
    for i, text in nonempty:
        full.extend([f'### P{i:04d}', '', text, ''])
    guide = ['# 기후부 2026 연구개발계획서 작성요령 — 원문 보존', '',
             '## 읽는 방법', '',
             '요약·의역하지 않은 작성요령 표 원문이다. 표 밖 유의사항 및 예외 조건 누락을 막기 위해 전체 원문 대조본을 함께 제공한다.',
             '[전체 원문 대조본](전체원문_대조본.md)에 모든 본문·표·주석 문단을 원래 순서대로 보관했다.',
             '법령·제출기준은 제공된 양식에 기재된 내용을 보존한 것으로 최신 법령 검토가 아니다.', '',
             '## 앞부분 제출서류·제출 유의사항·연차 산정', '']
    for i, text in nonempty:
        if i < 116:
            guide.extend([f'<!-- P{i:04d} -->', text, ''])
    for n, table in enumerate(guides, 1):
        table_ps = list(table.iter('P'))
        start = indices[id(table_ps[0])]
        guide.extend([f'## 작성요령 표 {n:02d} · P{start:04d}', ''])
        for p in table_ps:
            text = own_text(p)
            if text.strip():
                guide.extend([f'<!-- P{indices[id(p)]:04d} -->', text, ''])
    guide.extend(['## 표 밖 작성 안내·조건·주석 (누락 방지 보충)', ''])
    for i, text in nonempty:
        if i >= 116 and i not in guide_ids and any(k in text for k in ('작성', '기재', '제출', '삭제', '필수', '※', '주1)', '주2)', '주3)', '주4)', '주5)', '참조', '첨부')):
            guide.extend([f'<!-- P{i:04d} -->', text, ''])
    # Keyword detection cannot prove that a following continuation is not an
    # instruction. Preserve every remaining paragraph in this same MD as well.
    included = {i for i, _ in nonempty if f'<!-- P{i:04d} -->' in guide}
    guide.extend(['## 누락 방지 부록 — 나머지 본문·표의 문맥 원문', '',
                  '안내 문장의 다음 줄이나 표의 조건이 빠지지 않도록, 위에 수록되지 않은 원문도 전부 보존한다. P번호로 전체 대조본과 연결할 수 있다.', ''])
    for i, text in nonempty:
        if i not in included:
            guide.extend([f'<!-- P{i:04d} -->', text, ''])
    (ASSETS / '작성요령.md').write_text('\n'.join(guide), encoding='utf-8')
    (ASSETS / '전체원문_대조본.md').write_text('\n'.join(full), encoding='utf-8')
    manifest = json.loads((ASSETS / 'source_manifest.json').read_text(encoding='utf-8'))
    original = ROOT.parent / 'materials/submission-reference/제출서류' / manifest['source_name']
    shutil.copy2(original, ASSETS / 'template.hwp')
    body = root.find('BODY')
    mapping = []
    for p in body.iter('P'):
        i = indices[id(p)]
        text = own_text(p)
        if text.strip() and i not in guide_ids:
            mapping.append({'index':i, 'text':text})
    (ASSETS / 'content_inventory.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
    audit = {'source_sha256':manifest['sha256'], 'source_pages':manifest['pages'],
             'paragraph_count':len(paragraphs), 'nonempty_paragraphs':len(nonempty),
             'guide_tables':len(guides), 'guide_paragraphs':len(guide_ids),
             'missing_full_transcript_paragraphs':[i for i,t in nonempty if t not in '\n'.join(full)],
             'missing_guide_md_paragraphs':[i for i,t in nonempty if f'<!-- P{i:04d} -->' not in guide or t not in guide],
             'guide_table_ranges':[[min(indices[id(p)] for p in t.iter('P')), max(indices[id(p)] for p in t.iter('P'))] for t in guides],
             'table_count':len(tables)}
    (ASSETS / 'extraction_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == '__main__':
    main()
