"""Build auditable memory from downloaded inventories and manually reviewed pages."""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent

def read(name):
    return json.loads((BASE/name).read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def candidate(caption):
    # Caption-based navigation aid ONLY. Never promote to verified observations.
    rules = [
        (r'로드맵|일정|연차|단계별.*목표','연차/단계 도표 후보','기간별 작업·목표의 순서와 연결'),
        (r'추진.*체계|협력|협의체|역할','기관/역할 관계도 후보','참여주체와 업무·협업 관계'),
        (r'구성도|구조도|아키텍처|architecture|시스템.*구성','구조도 후보','구성요소·기능·연결 범위'),
        (r'흐름|순서|절차|프로세스|과정|pipeline','흐름도 또는 단계별 자료 후보','입력에서 처리·출력으로 이어지는 순서'),
        (r'사진|실물|시제품|장착|현장','사진 후보','대상·장치·현장 상태(자체/외부 자료 여부 별도 확인)'),
        (r'화면|인터페이스|GUI|캡처','화면/인터페이스 이미지 후보','사용 절차 또는 구현 상태'),
        (r'현미경|TEM|SEM|형광|단면','관찰 영상/모식도 후보','미세구조·위치·조건별 관찰 차이'),
        (r'분포|곡선|스펙트럼|변화|확률','그래프/분포도 후보','변수·조건에 따른 변화와 분포'),
        (r'비교|성능|평가|정확|실험.*결과|측정.*결과','비교표/그래프/영상 후보','조건·대안별 결과 차이'),
        (r'현황|사양|규격|지표|목록|요구사항','항목표/요약 도표 후보','범위·기준·대상·수량의 대응'),
        (r'개념|모델|원리','개념도 후보','연구 개념·작동 원리'),
    ]
    for pattern, form, purpose in rules:
        if re.search(pattern,caption,re.I):
            return {'format_candidate':form,'explanatory_purpose_candidate':purpose,
                    'evidence':'caption_rule_inference_not_visual_verification'}
    return {'format_candidate':'미확정','explanatory_purpose_candidate':'캡션과 실제 지면의 추가 해석 필요',
            'evidence':'not_determined'}

def esc(value):
    return str(value).replace('|','\\|').replace('\n',' ')

def main():
    rows = read('page_visual_index.json')
    reviews = read('manual_review.json')
    extra = read('additional_review.json')
    selections = {x['id']:x for x in read('review_selection.json')}
    additional = read('additional_selection.json')
    followup_name = 'followup-2026-09-26'
    followup_path = BASE/followup_name
    followups = read(followup_name+'/manual_observations.json') if followup_path.exists() else []
    audit = read(followup_name+'/all_page_audit.json')['records'] if followup_path.exists() else []
    audit_by_id = {r['id']:r for r in audit}
    sources = {x['id']:x for x in read('pdf_manifest.json')}
    original = {x['id']:x for x in json.loads((ROOT/'docs/authoring_reference_memory.json').read_text(encoding='utf-8'))['records']}
    assert len(rows)==len(reviews)==90
    assert set(reviews)==set(original)
    (BASE/'reports').mkdir(exist_ok=True)
    memory, visuals, pending = [], [], []
    for row in rows:
        rid = row['id']
        viewed = sorted({x['pdf_page'] for x in selections[rid]['selected_pages']} | set(additional.get(rid,[])))
        new_notes = [r for r in followups if r['id']==rid]
        viewed = sorted(set(viewed) | {p for r in new_notes for p in r['pages']})
        assert all(1<=p<=row['pdf_page_count'] for p in viewed)
        notes = reviews[rid] + ('\n\n'+extra[rid] if rid in extra else '')
        if new_notes:
            notes += '\n\n### 2026-09-26 추가 지면 확인\n\n' + '\n\n'.join(
                'PDF '+', '.join(map(str,r['pages']))+'쪽: '+r['observation'] for r in new_notes)
        entry = {'id':rid,'title':row['title'],'source':row['source'],'task_type':row['task_type'],
                 'pdf_pages':row['pdf_page_count'],'public_listed_visuals':len(row['images']),
                 'pdf_path':f'exa-results/{BASE.name}/pdfs/{rid}.pdf',
                 'inventory_path':f'exa-results/{BASE.name}/reports/{rid}.md',
                 'visually_reviewed_pdf_pages':viewed,'observed_location_format_purpose':notes,
                 'reference_section_use':original[rid].get('section_use'),
                 'review_scope':'selected_page_layout_review_not_exhaustive_element_review',
                 'all_visual_elements_verified':False}
        memory.append(entry)
        if rid in audit_by_id:
            entry['all_page_mechanical_audit'] = audit_by_id[rid]
            entry['page_context_inventory_path'] = f'exa-results/{BASE.name}/{followup_name}/reports/{rid}.md'
        missing = [p for p in range(1,row['pdf_page_count']+1) if p not in viewed]
        pending.append({'id':rid,'unreviewed_pdf_pages':missing,'all_visual_elements_verified':False,
                        'next_step':'미검토 쪽 시각 확인, 미등재 시각자료 추가, 요소별 위치·형식·설명 목적 확정'})
        lines = [f'# {rid} — {row["title"]}', '', f'[공식 출처]({row["source"]}) · [로컬 원문](../pdfs/{rid}.pdf)', '',
                 f'원문 {row["pdf_page_count"]}쪽. 공개 목록 {len(row["images"])}건. 쪽수는 모두 PDF의 1부터 시작하는 쪽수.', '',
                 '## 실제 지면에서 확인한 배치·형식·설명 목적', '', notes, '',
                 '직접 검토한 쪽: '+', '.join(map(str,viewed)), '',
                 f'[대표 지면 모음](../review_sheets/{rid}.jpg)', '']
        if rid in extra:
            lines += [f'[추가 지면 모음](../review_sheets/{rid}-extra.jpg)', '']
        lines += ['## 공개 표·그림 목록', '',
                  '아래는 공개 목록 전 항목이다. 캡션 일치는 위치에 대한 텍스트 확인일 뿐, 실제 배치·형식 검증이 아니다. 형식·목적 후보는 캡션 규칙으로 추정했으며 확정된 사실로 인용하지 않는다. 원문에 더 많은 시각자료가 있을 수 있다.', '',
                  '| 식별번호 | 원문 캡션 | PDF 쪽/위치 근거 | 형식 후보 | 설명 목적 후보 |',
                  '|---|---|---|---|---|']
        for v in row['images']:
            item = dict(v)
            item.update(candidate(v['caption']))
            p = v.get('pdf_page')
            item.update({'reference_id':rid,'parent_page_overview_reviewed':p in viewed,
                         'visual_review':'individual_element_not_fully_verified'})
            visuals.append(item)
            loc = f'{p} / 캡션 텍스트 일치' if p and v['location_evidence']=='caption_text_match' else f'{v.get("filename_page_hint")} / 파일명 추정·미확정'
            lines.append('| '+ ' | '.join([v['visual_id'],f'[{esc(v["caption"])}]({v["url"]})',loc,esc(item['format_candidate']),esc(item['explanatory_purpose_candidate'])])+' |')
        if not row['images']:
            lines += ['', '**공개 목록 없음 — 그림/표가 없다는 뜻이 아니다. 위 직접 검토 내용과 원문을 참고한다.**']
        lines += ['', f'[PDF 텍스트 캡션 후보](../caption_candidates/{rid}.json) — 중복·목차·본문 언급이 섞인 미검증 후보이며 그림 수로 합산하지 않는다.',
                  f'[쪽별 원문 텍스트](../page_text/{rid}.json)', '']
        if rid in audit_by_id:
            lines += [f'[전체 쪽 점검 및 확장 캡션 후보](../{followup_name}/reports/{rid}.md) — 기계 점검과 직접 관찰을 분리한다.', '']
        (BASE/'reports'/(rid+'.md')).write_text('\n'.join(lines),encoding='utf-8')
    stats = {'references':len(rows),'pdf_pages':sum(r['pdf_page_count'] for r in rows),
             'references_with_public_visual_list':sum(bool(r['images']) for r in rows),
             'public_listed_visuals':len(visuals),
             'caption_text_matched_visuals':sum(v['location_evidence']=='caption_text_match' for v in visuals),
             'visually_reviewed_pages':sum(len(r['visually_reviewed_pdf_pages']) for r in memory),
             'unreviewed_pages':sum(len(r['unreviewed_pdf_pages']) for r in pending),
             'caption_candidates_not_unique_visual_count':sum(s['caption_candidate_count'] for s in selections.values()),
             'exhaustive_visual_audit_complete':False}
    if audit:
        stats.update({'whole_page_mechanical_audit_pages':sum(r['pages'] for r in audit),
                      'expanded_caption_candidates_not_unique_visual_count':sum(r['caption_candidates'] for r in audit),
                      'large_pdf_image_objects_not_unique_visual_count':sum(r['large_image_objects'] for r in audit),
                      'image_object_scan_errors':sum(r['object_scan_errors'] for r in audit),
                      'previous_visually_reviewed_pages_2026_09_25':473})
    write(BASE/'visual_inventory.json',{'saved_on':'2026-09-25','scope':stats,'items':visuals})
    write(BASE/'remaining_review.json',pending)
    write(BASE/'review_coverage.json',stats)
    write(ROOT/'docs/authoring_visual_reference_memory.json',{'saved_on':'2026-09-25','updated_on':'2026-09-26' if audit else '2026-09-25','scope':stats,'records':memory})
    index = ['# 레퍼런스별 시각자료 조사 색인','',
             '90건 원문 확보 및 공개 목록 수집 완료. 대표 지면 검토이며, 모든 쪽·모든 시각자료의 전수 검증 완료가 아니다.','',
             '| 번호 | 과제 | 원문 쪽수 | 공개 목록 | 직접 검토 쪽수 |','|---|---|---:|---:|---:|']
    for r in memory:
        index.append(f'| {r["id"]} | [{esc(r["title"])}](reports/{r["id"]}.md) | {r["pdf_pages"]} | {r["public_listed_visuals"]} | {len(r["visually_reviewed_pdf_pages"])} |')
    (BASE/'README.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    print(json.dumps(stats))

if __name__=='__main__':
    main()
