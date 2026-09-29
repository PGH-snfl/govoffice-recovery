"""Readable, evidence-level-aware index of the all-page audit and manual notes."""
import json
import ast
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
OUT = BASE/'followup-2026-09-26'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def cell(value):
    return str(value or '').replace('|', '\\|').replace('\n', ' ').replace('<', '&lt;').replace('>', '&gt;')


def main():
    audit = read(OUT/'all_page_audit.json')['records']
    memory = read(ROOT/'docs/authoring_visual_reference_memory.json')
    by_id = {r['id']:r for r in memory['records']}
    notes = read(OUT/'manual_observations.json')
    queue = read(OUT/'review_queue.json') + read(OUT/'missing_review_queue.json')
    requested = {(r['id'], r['pdf_page']) for r in queue}
    observed = {(r['id'], p) for r in notes for p in r['pages']}
    assert requested == observed, (requested-observed, observed-requested)
    assert len(audit) == len(by_id) == 90
    assert sum(r['pages'] for r in audit) == 10333
    assert sum(r['object_scan_errors'] for r in audit) == 0
    assert sum(r['caption_candidates'] for r in audit) == 9768
    assert len(requested) == 131
    (OUT/'reports').mkdir(exist_ok=True)
    followup_by_id = {}
    for item in queue:
        assert (OUT/item['sheet']).is_file()
        followup_by_id.setdefault(item['id'], []).append(item)
    index = [
        '# 2026-09-26 추가 조사 — 전체 쪽 점검과 삽입 기준', '',
        '[실제 작성에 적용할 삽입 기준](../../../docs/AUTHORING_REFERENCE_INSERTION_STANDARD.md)', '',
        '## 확인 범위', '',
        '- 90건 원문 10,333쪽의 텍스트와 PDF 내부 구성을 기계 점검했다. 문서 내부 이미지 객체 조사 오류는 0건이다.',
        '- 문서 내부 이미지 객체 15,509개는 사진·그림 15,509장을 뜻하지 않는다. 스캔 지면·로고·분할 이미지가 섞이고 선으로 그린 도식은 누락될 수 있다.',
        '- 확장 캡션 후보 9,768개에는 번호 없는 제목, 목차, 중복, 본문 언급, 소제목 오탐이 섞인다. 기존 공개 목록 4,947개에 합산하지 않는다.',
        '- 이번에 확인한 131쪽은 위치가 불확실한 후보/텍스트 희박 지면 89쪽과 공개 목록이 없는 13건의 추가 지면 42쪽이다.',
        '- 이전 473쪽과 겹치는 8쪽을 제외해 123쪽 증가했다. 누적 직접 확인은 596쪽, 미검토는 9,737쪽이다.',
        '- 직접 확인은 지면 모음의 배치·형식·목적 관찰이다. 모든 요소의 미세 수치·캡션 대응을 개별 확정한 것은 아니다.', '',
        '## 이번에 보완한 내용', '',
        '공개 그림 목록이 없는 보고서에도 번호 없는 괄호형 캡션, 계층별 구성도, 평가목표표, 데이터 정의표, 실제 시험 장면이 있었다. 반대로 괄호형 소제목을 그림 캡션으로 잘못 탐지한 사례도 있어 자동 분류와 실제 관찰을 분리했다. 스캔된 논문·공정표는 보고서의 성과 증빙이며, 그 안의 모든 도식을 본문 연구원리로 분류하지 않았다.', '',
        '각 보고서 아래 표에는 모든 쪽의 검색 단서가 있고, 이어 캡션 후보와 주변 문맥이 있다. 자동 추정 소주제는 위치 검색용이며 실제 절 제목·그림 의미의 확정값이 아니다.', '',
        '## 사례별 전체 쪽 점검', '',
        '| 번호 | 과제 | 원문 쪽 | 공개 목록 | 캡션 후보 | 이번 직접 확인 쪽 | 누적 직접 확인 쪽 |',
        '|---|---|---:|---:|---:|---:|---:|']
    for a in audit:
        rid = a['id']
        record = by_id[rid]
        pages = read(OUT/'pages'/(rid+'.json'))
        contexts = read(OUT/'contexts'/(rid+'.json'))
        assert len(pages) == a['pages']
        assert len(contexts) == a['public_listed_visuals']
        viewed = set(record['visually_reviewed_pdf_pages'])
        local_notes = [r for r in notes if r['id']==rid]
        index.append(f'| {rid} | [{cell(a["title"])}](reports/{rid}.md) | {a["pages"]} | {a["public_listed_visuals"]} | {a["caption_candidates"]} | {len(followup_by_id.get(rid, []))} | {len(viewed)} |')
        lines = [f'# {rid} — {a["title"]}', '',
                 f'[공식 출처]({record["source"]}) · [원문](../../pdfs/{rid}.pdf) · [누적 관찰 및 공개 목록](../../reports/{rid}.md)', '',
                 '쪽수는 PDF의 1부터 시작하는 쪽수다. 아래 자동 추정과 캡션 후보는 실제 시각자료별 검증이 아니다. ‘지면 개요 확인’도 개별 그림·수치 전수 검증을 뜻하지 않는다.', '',
                 '## 이번 직접 관찰', '']
        if not local_notes:
            lines += ['이번 추가 지면 관찰 없음. 이전 관찰은 위 누적 기록에 있다.', '']
        for n in local_notes:
            lines += ['PDF '+', '.join(map(str,n['pages']))+'쪽: '+n['observation'], '']
        sheets = sorted({r['sheet'] for r in followup_by_id.get(rid, [])})
        for sheet in sheets:
            lines.append(f'[확인한 지면 모음 {Path(sheet).stem}](../{sheet})')
        lines += ['', '## 전체 쪽 점검 색인', '',
                  '이미지 객체 개수는 고유 그림 수가 아니다. 이미지 객체 0개여도 선·글자로 만든 표/도식이 있을 수 있다. 소주제 후보는 앞쪽 제목이 계속 이어지는 것으로 잘못 추정되었을 수 있다.', '',
                  '| PDF 쪽 | 소주제 검색 단서(자동 추정) | 캡션 후보 수 | 큰 이미지 객체 수 | 지면 확인 수준 |',
                  '|---:|---|---:|---:|---|']
        for p in pages:
            state = '지면 개요 확인; 개별 요소 미검증' if p['pdf_page'] in viewed else '기계 점검만'
            lines.append(f'| {p["pdf_page"]} | {cell(p["section_context_candidate"])} | {len(p["caption_candidates"])} | {len(p["image_regions"])} | {state} |')
        lines += ['', '## 캡션 후보와 주변 문맥', '',
                  '다음 항목은 텍스트 검색 후보다. 목차/본문 중복, 소제목, 각주가 포함될 수 있다. 순번은 조사용이며 원문 그림 번호가 아니다. 앞뒤 문맥은 PDF 텍스트 추출 순서여서 다단·표 내부에서는 읽는 순서가 섞일 수 있다.', '']
        for p in pages:
            if not p['caption_candidates']:
                continue
            lines += [f'### PDF {p["pdf_page"]}쪽', '']
            for number, c in enumerate(p['caption_candidates'], 1):
                label = '목차 가능' if c['toc_like'] else '본문/제목/캡션 판별 필요'
                lines += [f'{number}. **후보 — {cell(c["text"])}** ({label})', '',
                          f'   앞 문맥: {cell(c["before"])}', '',
                          f'   뒤 문맥: {cell(c["after"])}', '']
        lines += ['## 원자료', '',
                  f'- [공개 목록 항목별 주변 문맥](../contexts/{rid}.json)',
                  f'- [모든 쪽의 기계 점검 결과](../pages/{rid}.json)',
                  f'- [원문 추출 텍스트](../../page_text/{rid}.json)', '']
        (OUT/'reports'/(rid+'.md')).write_text('\n'.join(lines),encoding='utf-8')
    index += ['', '## 검증 및 남은 범위', '',
              '[직접 관찰 기록](manual_observations.json) · [전체 쪽 기계 점검 집계](all_page_audit.json) · [검토 범위](../review_coverage.json) · [미검토 쪽](../remaining_review.json)', '',
              '다음 작업은 미검토 지면 확인, 각 시각자료의 실제 소주제·정확한 위치·형식·설명 목적 확정, 세부 수치 및 출처 대조다. 자료 개수가 많은 보고서는 부록/본문을 나눠 확인해야 한다. 전체 요소 전수 검증 완료로 표시하지 않는다.', '']
    (OUT/'README.md').write_text('\n'.join(index),encoding='utf-8')
    docs = [ROOT/'docs/AUTHORING_REFERENCE_INSERTION_STANDARD.md',
            ROOT/'docs/AUTHORING_REFERENCE_MEMORY.md',
            ROOT/'docs/AUTHORING_VISUAL_REFERENCE_MEMORY.md', OUT/'README.md',
            *list((OUT/'reports').glob('*.md'))]
    local_links = 0
    for path in docs:
        content = path.read_text(encoding='utf-8')
        assert '\ufffd' not in content, path
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if target.startswith(('https://', 'http://', '#')):
                continue
            local_links += 1
            assert (path.parent/target.split('#')[0]).exists(), (path,target)
    for name in ['audit_all_pages.py', 'render_followup.py', 'build_memory.py', 'build_followup_report.py']:
        ast.parse((BASE/name).read_text(encoding='utf-8'))
    pending = {r['id']:r['unreviewed_pdf_pages'] for r in read(BASE/'remaining_review.json')}
    assert sum(len(p) for p in pending.values()) == 9737
    for rid,r in by_id.items():
        assert set(r['visually_reviewed_pdf_pages']).isdisjoint(pending[rid])
        assert set(r['visually_reviewed_pdf_pages']) | set(pending[rid]) == set(range(1,r['pdf_pages']+1))
    validation = {'date':'2026-09-26','references':90,'all_pages_mechanically_checked':10333,
                  'object_scan_errors':0,'expanded_caption_candidates_not_unique_visual_count':9768,
                  'followup_reviewed_page_pairs':len(requested),
                  'followup_notes_match_review_queue':True,
                  'checked_markdown_files':len(docs),'valid_local_links':local_links,
                  'broken_local_links':0,'research_scripts_syntax_valid':True,
                  'cumulative_distinct_page_overviews':sum(len(r['visually_reviewed_pdf_pages']) for r in by_id.values()),
                  'all_visual_elements_verified':False}
    (OUT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(validation))


if __name__=='__main__':
    main()
