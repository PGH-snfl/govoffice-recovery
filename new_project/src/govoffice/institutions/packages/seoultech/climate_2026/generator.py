"""Offline template rendering and a one-click institution workflow.

No COM imports, no network, no overwrite of the user's original. Native export
is an injected adapter so content/layout tests can run without Hancom installed.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Callable
from uuid import uuid4
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET

from .example_content import TITLE, BUDGET, YEARS, example_fields

ASSETS = Path(__file__).resolve().parent
SOURCE_SHA256 = 'c7e44301ef3868479353fd8833e77ffec90ccc773a9e661b11becb4fbeaff294'
XML_SHA256 = '351e77c3c69eafb626c6cf60c19e0f96bafdcc07468b389d502f9ec4b02cbc4a'
REVIEW_ITEMS = (
    ('공고 적합성', '공고번호·내역사업·선정방식·제안요청서 필수 성능·신청자격을 실제 공고로 확인'),
    ('연구내용', '예시 주제와 목표를 실제 연구계획으로 교체; 시장·경쟁기술·선행특허의 출처 확보'),
    ('기관 및 인력', '신청기관 법적 명칭·등록번호·연구자번호·경력·학력·참여기간·계상률 확인'),
    ('공동기관', '참여기관·수요기업·국외기관 확정 후 관련 행과 조건부 양식 정리'),
    ('연구비', '지원·부담비율, 인건비, 간접비, 단가·수량 및 연차별 합계 검토; 예시 금액은 지원 적격성을 보증하지 않음'),
    ('실증 및 보안', '실증장소 승인·안전계획·보안등급·설비 사용권 확인'),
    ('증빙서류', '참여의사 확인서·재직증명서·개인정보 동의서 등 실제 발급·서명 서류 준비'),
    ('편집 마무리', '표·그림·자동 쪽번호·목차·빈 행·미확정 표시 검토, 실제 신청본에서 예시 표기 제거'),
)


def own_text(p):
    return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag == 'CHAR')


def replace_text(p, value):
    """Replace only characters; never delete shapes, fields, tables or section controls."""
    texts = p.findall('TEXT')
    if not texts:
        texts = [ET.SubElement(p, 'TEXT', {'CharShape': '0'})]
    for t in texts:
        for child in list(t):
            if child.tag == 'CHAR':
                t.remove(child)
    ET.SubElement(texts[0], 'CHAR').text = str(value)


def render_example():
    if hashlib.sha256((ASSETS/'template.hwp').read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError('원본 양식 버전이 변경되었습니다. 필드 위치를 다시 검증해야 합니다.')
    if hashlib.sha256((ASSETS/'source.hwpml').read_bytes()).hexdigest() != XML_SHA256:
        raise ValueError('추출 양식이 변경되었습니다. 위치 연결 검증이 필요합니다.')
    root = ET.fromstring((ASSETS/'source.hwpml').read_text(encoding='utf-8'))
    ps = list(root.iter('P'))
    if len(ps) != 7419 or own_text(ps[118]) != '연구개발계획서':
        raise ValueError('양식 문단 구조가 예상과 달라 생성을 중단했습니다.')
    indices = {id(p): i for i,p in enumerate(ps)}
    parents = {id(c): p for p in root.iter() for c in p}
    tables = list(root.iter('TABLE'))
    guide_tables = [t for t in tables if '작성요령' in ''.join(own_text(p) for p in list(t.iter('P'))[:2]).replace(' ','')]
    if len(guide_tables) != 23:
        raise ValueError('작성요령 표 개수가 원본과 다릅니다.')
    guide_ids = {id(p) for t in guide_tables for p in t.iter('P')}
    fields = example_fields()
    field_log = []
    # Fill fixed positions before any structure changes, including duplicate labels.
    for i,value in fields.items():
        if i >= len(ps) or id(ps[i]) in guide_ids:
            raise ValueError(f'잘못된 입력 필드: P{i:04d}')
        field_log.append({'field_id': f'P{i:04d}', 'original': own_text(ps[i]), 'value': value, 'source': 'example'})
        replace_text(ps[i], value)

    # Bring the original section/page controls with us when dropping instruction pages.
    section = root.find('BODY/SECTION')
    # SECDEF must be in the FIRST paragraph and precede COLDEF. Putting it in
    # the cover's second paragraph makes Hancom synthesize a default-margin
    # section before it, clipping wide tables and producing blank pages.
    target_text = ps[116].find('TEXT')
    controls=[]
    for t in ps[0].findall('TEXT'):
        for c in list(t):
            if c.tag != 'CHAR':
                controls.append(deepcopy(c))
    for n,c in enumerate(controls):
        target_text.insert(n,c)
    ps[117].set('PageBreak', 'false')
    for p in list(section):
        if p.tag == 'P' and indices[id(p)] < 116:
            section.remove(p)
    guide_hosts=[]
    for table in guide_tables:
        host=parents[id(parents[id(table)])]
        if host.tag=='P' and host in list(section): guide_hosts.append(host)
        parents[id(table)].remove(table)
    # Empty table hosts can carry a forced page break. Remove those hosts only.
    for p in guide_hosts:
        if not own_text(p).strip() and not list(p.iter('TABLE')):
            section.remove(p)

    # Strip blue author notes, but keep mixed-run headings and every filled value.
    shapes = {s.get('Id'): s for s in root.iter('CHARSHAPE')}
    shape_list=root.find('.//CHARSHAPELIST')
    black_shapes={}
    for i in fields:
        t=ps[i].find('TEXT')
        old=t.get('CharShape')
        if shapes[old].get('TextColor','0')!='0':
            if old not in black_shapes:
                new=deepcopy(shapes[old]); new_id=str(max(map(int,shapes))+1)
                new.set('Id',new_id); new.set('TextColor','0'); shape_list.append(new)
                shapes[new_id]=new; black_shapes[old]=new_id
            t.set('CharShape',black_shapes[old])
    shape_list.set('Count',str(len(shape_list)))
    # Long tables must be allowed to split by cell. Inline-object treatment in
    # Hancom 2018 makes a full-page cover jump to an empty second page and can
    # hide a summary's last rows after filling text.
    for table in root.iter('TABLE'):
        if table not in (ps[117].find('.//TABLE'),ps[404].find('.//TABLE')):
            continue
        position=table.find('SHAPEOBJECT/POSITION')
        if position is not None:
            position.set('TreatAsChar','false')
            position.set('VertRelTo','Para');position.set('VertOffset','0')
            position.set('FlowWithText','true');position.set('AllowOverlap','false')
        table.set('PageBreak','Cell')
    def is_blue(t):
        color = int(shapes[t.get('CharShape')].get('TextColor','0'))
        return (color >> 16 & 255) > 120 and (color & 255) < 100
    removed_notes = []
    for p in list(root.iter('P')):
        i = indices[id(p)]
        if i in fields:
            continue
        before = own_text(p)
        for t in p.findall('TEXT'):
            if is_blue(t):
                for c in list(t):
                    if c.tag == 'CHAR': t.remove(c)
        if own_text(p) != before:
            removed_notes.append(i)
        text = own_text(p).strip()
        if i >= 116 and text in {'o','ㅇ','-','⋅','·'}:
            replace_text(p, 'o 세부 내용 확인 필요' if text in {'o','ㅇ'} else '')
        if i >= 116 and re.fullmatch(r'(?:[A-Z]{5,}|[Xx]{4,}|○+|ㅇㅇㅇ|00\.0)',text):
            replace_text(p,'확인 필요')
        # Dates and fabricated source examples are not institution facts.
        if i >= 116 and ('YYYY' in text or 'yy.mm' in text or text in {'2021','2022','2023','2024','20XX','20xx','20××년'}):
            replace_text(p,'확인 필요')
        if i >= 116 and '기관명 기입' in text:
            replace_text(p, text.replace('기관명 기입','서울과학기술대학교' if '주관' in text else '참여 여부 확인'))

    # Original demonstration chart labels must match the new example subject.
    chart_labels = {'계획수립 및 자료조사':'자료 정의·기준선 확보', '계획 수립 및 자료조사':'자료 정의·기준선 확보',
                    '설계도면 작성':'계측·연동 설계', '진공펌프 설치':'수집 모듈 구현', '진공폄프 설치':'수집 모듈 구현',
                    '전체시스템 구성':'예측·운전계획 통합', '전체 시스템 구성':'예측·운전계획 통합',
                    '1차 시제품 설계도면 작성':'통합 시제품 설계', '1차 시제품 설계 도면 작성':'통합 시제품 설계',
                    '2차 시제품 설계도면 작성':'검증·인계 자료 확정',
                    '기관명A':'서울과기대', '기관명B':'참여 확인', '기관명C':'참여 확인'}
    for p in root.iter('P'):
        if own_text(p).strip() in chart_labels:
            replace_text(p,chart_labels[own_text(p).strip()])

    # Original 8-1 table includes a fictional SME with 800,000/20,000/180,000.
    # Replace those example facts with a pending decision, not an asserted university rate.
    for i in range(5421,5443):
        if i in (5421,5422,5423,5424):
            replace_text(ps[i], {5421:'서울과학',5422:'기술대학교',5423:'대학',5424:'확인'}[i])
        elif own_text(ps[i]).strip():
            replace_text(ps[i],'확인')
    for i in (511,517,3652,3658): replace_text(ps[i],'참여기관 확인')

    # Add complete, consistent schedule to the section heading. Existing charts
    # remain editable and are explicitly described as examples, not actual progress.
    replace_text(ps[1466], '2-3. 수행일정 및 주요결과물 (예시: 6개월+9개월+9개월)')
    replace_text(ps[1465], '1차: 자료사전·수집 시제품 → 2차: 통합 시제품·모의시험 → 3차: 현장평가·운영매뉴얼')
    # A concrete single-university example does not need empty enterprise,
    # overseas-institution or additional-stage demonstration blocks. This is
    # an EXAMPLE configuration, never an eligibility decision about a real bid.
    omit_ranges = [(749,757),(1349,1361),(1366,1376),(1383,1394),(1399,1409),
                   (1419,1429),(1434,1451),(1833,3221),
                   (3416,3472),(3484,3537),(3548,3555),
                   (3807,4320),(4628,4832),(5077,5169),(5241,5386),
                   (6266,6671),(6748,6768),(7108,7418)]
    for p in list(section):
        if p.tag=='P' and any(a<=indices[id(p)]<=b for a,b in omit_ranges):
            section.remove(p)
    replace_text(ps[3806], '5-2. 사업화 연계 검토 (예시: 대학 단독, 참여기업 없음)')
    new_p=deepcopy(ps[3244]); replace_text(new_p,'o 시설 운영부서의 수요를 확인하고 기술이전·공동 활용 가능성을 검토한다. 기업 전용 매출·재무·투자 표는 이 대학 단독 예시에서 제외했다. 실제 참여기업이 정해지면 원본 양식의 해당 표를 작성해야 한다.')
    section.insert(list(section).index(ps[3806])+1,new_p)
    replace_text(ps[5076],'(4) 관계 기관: 이 예시는 별도 관계 기관을 설정하지 않음')
    replace_text(ps[5240],'기업 현황: 이 대학 단독 예시에서는 미설정. 실제 참여기관 확정 시 검토.')
    replace_text(ps[3398],'자료 수집·예측·운전계획·성능 검증 총괄')
    # Remove untouched fictional equipment purchases from the original sample.
    replace_text(ps[6690],'서울과기대'); replace_text(ps[6694],'계측·연동 시험장치(예시)')
    replace_text(ps[6696],'자료 수집 시험'); replace_text(ps[6698],'10,000')
    replace_text(ps[6699],'2026.12.(예시)'); replace_text(ps[6700],'승인 장소 확인')
    for p in root.iter('P'):
        txt=own_text(p)
        if any(x in txt for x in ('4m급','KETEP 공장','25,000','30,000')) and indices.get(id(p),0)>6795:
            replace_text(p,'실제 계획 확인')
    for i in (1341,1446):
        if ps[i] in list(section): replace_text(ps[i],'1단계 / 대학 단독 예시')
    replace_text(ps[1465],'')
    for i in range(1477,1482): replace_text(ps[i],'—')
    for start, spans in ((1483,(0,1)),(1533,(0,1)),(1583,(0,1)),(1633,(2,3)),
                         (1683,(0,1,2)),(1733,(2,3)),(1783,(4,5))):
        for n in range(16): replace_text(ps[start+1+n],'■' if n in spans else '')

    # Preserve the original page design, but apply its explicit typography rule:
    # body 12pt, table 8pt. Original empty bullets were 13pt bold and example
    # field styles as small as 5pt, which are not appropriate for filled prose.
    table_p_ids={id(p) for t in root.iter('TABLE') for p in t.iter('P')}
    fonts={}
    for face in root.findall('.//FACENAMELIST/FONTFACE'):
        match=next((f for f in face.findall('FONT') if f.get('Name')=='돋움'),None)
        if match is not None: fonts[face.get('Lang')]=match.get('Id')
    formatted={}
    for p in root.iter('P'):
        i=indices.get(id(p))
        in_table=id(p) in table_p_ids
        if not in_table and i not in fields and p is not new_p: continue
        for t in p.findall('TEXT'):
            old=t.get('CharShape'); height=800 if in_table else 1200
            if i==118: height=1200
            key=(old,height,i==118)
            if key not in formatted:
                new=deepcopy(shapes[old]); new_id=str(max(map(int,shapes))+1)
                new.set('Id',new_id);new.set('Height',str(height));new.set('TextColor','0')
                if i!=118:
                    for bold in list(new.findall('BOLD')):new.remove(bold)
                for lang,font_id in fonts.items():
                    if new.find('FONTID') is not None and lang in new.find('FONTID').attrib:
                        new.find('FONTID').set(lang,font_id)
                shape_list.append(new);shapes[new_id]=new;formatted[key]=new_id
            t.set('CharShape',formatted[key])
    shape_list.set('Count',str(len(shape_list)))
    # Drop truly empty top-level paragraphs; keep those carrying page/section,
    # field or drawing controls. Do not collapse blank cells in a table.
    for p in list(section):
        if p.tag=='P' and not own_text(p).strip() and all(c.tag=='CHAR' for t in p for c in t):
            section.remove(p)
    # Move section controls into the cover's first paragraph, removing the
    # standalone carrier which otherwise pushes the near-full-page cover down.
    if ps[116] in list(section):
        carrier=ps[116].find('TEXT');cover=ps[117].find('TEXT')
        for n,c in enumerate([c for c in carrier if c.tag!='CHAR']): cover.insert(n,deepcopy(c))
        section.remove(ps[116])
    # Source template's TOC has no page fields. Replace obsolete enterprise
    # subheadings with a compact section index; never invent page numbers.
    for p in list(section):
        if p.tag=='P' and 573<=indices.get(id(p),-1)<=637:section.remove(p)
    replace_text(ps[572], '목차 · 예시 검토본')
    for title in reversed(('1. 연구개발과제의 필요성','2. 연구개발과제의 목표 및 내용',
                            '3. 추진전략·방법 및 추진체계','4. 활용방안 및 기대효과',
                            '5. 사업화 전략 및 계획','6. 안전 및 보안조치 이행계획',
                            '7. 연구개발기관 현황','8. 연구개발비 사용계획',
                            '※ 대학 단독·단일단계 24개월 예시. 조건부 첨부양식은 원본 대조본에서 확인.')):
        para=deepcopy(ps[3244]);replace_text(para,title)
        section.insert(list(section).index(ps[572])+1,para)
    xml = ET.tostring(root, encoding='unicode')
    surviving={id(p) for p in root.iter('P')}
    field_log=[{**entry,'value':own_text(ps[int(entry['field_id'][1:])])}
               for entry in field_log if id(ps[int(entry['field_id'][1:])]) in surviving]
    report = {'mode':'example', 'submission_ready':False, 'ai_connected':False,
              'source_sha256':SOURCE_SHA256, 'source_pages':60,
              'filled_fields':len(field_log), 'removed_guide_tables':len(guide_tables),
              'removed_blue_note_paragraphs':len(removed_notes),
              'output_tables':len(list(root.iter('TABLE'))),
              'years_months':[6,9,9], 'annual_budget_thousand_krw':list(BUDGET),
              'example_assumptions':['주관대학 단독','단일단계 24개월','참여기업·국외기관 미설정'],
              'total_budget_thousand_krw':sum(BUDGET),
              'review_items':[{'area':a,'check':b} for a,b in REVIEW_ITEMS]}
    return xml, report, field_log


def generate(output_root: Path, export_native: Callable | None = None):
    xml, report, field_log = render_example()
    folder = Path(output_root)/('기후부_2026_예시_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid4().hex[:6])
    folder.mkdir(parents=True, exist_ok=False)
    hml = folder/'연구개발계획서_예시.hml'
    hml.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+xml,encoding='utf-8')
    for name in ('작성요령.md','전체원문_대조본.md','extraction_audit.json'):
        shutil.copy2(ASSETS/name,folder/name)
    (folder/'입력필드_예시값.json').write_text(json.dumps(field_log,ensure_ascii=False,indent=2),encoding='utf-8')
    checklist = ['# 기후부 2026 연구개발계획서 — 제출 전 점검표', '',
                 '**예시 검토본 / 실제 제출 불가 / 인공지능 미연결 / 자동 제출하지 않음**', '',
                 '제공된 양식의 서식으로 연구개발계획서 초안을 생성했다. 별도 확인서·동의서·증명서를 발급하거나 서명하지 않는다.', '',
                 '## 예시 조건', '', f'- 과제: {TITLE}',
                 '- 기관: 서울과학기술대학교(신청 법적 명칭은 확인 필요)',
                 '- 기간: 2026.10.01.~2028.09.30.; 1차 6개월, 2차 9개월, 3차 9개월',
                 '- 연구비: 150,000 + 225,000 + 225,000 = 600,000천원(6억원, 예시)',
                 '- 표지·요약문·사용계획 총괄표의 예시 금액은 연동됨. 8-1의 지원기준·부담비율과 인력별/장비별 세부 산출내역은 실제 정보 확인이 필요함.', '',
                 '## 확인할 항목', '']
    checklist.extend(f'- [ ] **{a}**: {b}' for a,b in REVIEW_ITEMS)
    checklist.extend(['', '## 원본에 기재된 제출서류 (실제 자료 별도 준비)', '',
                      '1. 연구개발계획서: 이번 기능의 생성 대상. 예시를 실제 자료로 수정한 후 한글 파일로 제출.',
                      '2. 연구개발기관 대표 참여의사 확인서: 해당 기관의 실제 확인·날인 자료.',
                      '3. 연구책임자 재직증명서: 주관·공동기관의 실제 발급 자료.',
                      '4. 과제 참여자 개인정보·과세정보 동의: 참여자의 실제 동의 자료.',
                      '5. 수요기업 확약서: 해당 시.',
                      '6. 외부기술도입비 현물산정 신청서: 필요 시.',
                      '7. 사업자등록증: 원본 안내의 대상·면제 조건 확인.',
                      '8. 회계감사보고서 또는 재무제표: 원본 안내의 대상·면제 조건 확인.', '',
                      '자세한 예외·제출 경로·시스템 대체 서류는 함께 저장된 작성요령.md의 원문을 확인한다.', '',
                      '## 이후 인공지능 연결 위치', '',
                      '입력필드_예시값.json은 원본 위치와 글 내용을 연결한 목록이다. 인공지능은 이 글 값을 생성하고 프로그램은 서식 유지·길이·필수값·합계를 검증하도록 확장한다. 현재는 예시 공급자만 사용한다.', ''])
    (folder/'제출전_점검표.md').write_text('\n'.join(checklist),encoding='utf-8')
    report.update({'output_dir':str(folder.resolve()), 'hml_path':str(hml.resolve()),'hwp_path':None,'native_verified':False})
    try:
        if export_native is not None:
            hwp = folder/'연구개발계획서_예시.hwp'
            native = export_native(ASSETS/'template.hwp', hml, hwp)
            if not hwp.is_file() or hwp.stat().st_size < 1024:
                raise RuntimeError('한글 파일 저장이 확인되지 않았습니다.')
            report.update(native)
            report['hwp_path']=str(hwp.resolve())
            report['native_verified']=True
    except Exception as exc:
        report['native_error']=str(exc)
        raise RuntimeError(f'한글 파일 변환 실패: {exc}\n작성 자료는 보존했습니다: {folder}') from exc
    finally:
        (folder/'생성결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report
