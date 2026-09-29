"""Pinned form profile; no example text/budget is used in the authoring path."""
from pathlib import Path
import re
from govoffice.services.document_authoring import digest, parse_source, own_text
from .generator import ASSETS, SOURCE_SHA256, XML_SHA256


def register_climate(registry, *, group_by_chapter=True):
    if digest(ASSETS / 'template.hwp') != SOURCE_SHA256 or digest(ASSETS / 'source.hwpml') != XML_SHA256:
        raise ValueError('기후부 원본 양식 버전이 변경되었습니다.')
    root = parse_source(ASSETS / 'source.hwpml')
    ps = list(root.iter('P'))
    indices = {id(p): i for i, p in enumerate(ps)}
    starts = [(116, '표지·과제 기본정보'), (404, '요약문'), (640, '본문 과제정보')]
    starts += [(i, own_text(p).strip()) for i, p in enumerate(ps)
               if i > 637 and re.match(r'^\s*[1-8]-[1-9]\.', own_text(p))]
    starts += [(7108, '조건부 별첨 및 서명 서류 — 원문 확인 필요')]
    chapters = [(116, '표지·과제 기본정보'), (404, '요약문'), (640, '본문 과제정보')]
    chapters += [(i, own_text(ps[i]).strip()) for i in (655,724,3228,3590,3675,4353,4432,5387)]
    chapters += [(7108, '조건부 별첨 및 서명 서류 — 원문 확인 필요')]
    # Fixed input positions verified against the pinned source; headings/signatures
    # and example-only changes (such as adding another year) are not writable.
    fields = {128,133,135,139,140,143,145,167,169,172,174,177,179,181,183,185,
              188,190,193,195,197,199,202,206,208,211,213,215,325,327,330,332,334,336,340,
              408,411,413,415,435,437,439,443,448,449,461,463,465,467,470,472,474,
              479,482,487,490,496,644,646,650,732,735,736,737,740,751,752,756,757,
              1220,1221,1222,1224,1225,1226,1239,1348,1365,1382,1398,1417,1433,
              3252,3369,3372,3390,3396,3397,3398,3564,3565,3566,3956,4026,4028,4030,
              4442,4444,4446,4448,4451,4453,4455,4457,4459,4461,4463,4473,4491}
    for start, size in ((234,8),(244,8),(253,8),(263,8),(272,8),(525,5),(532,5),(936,5),(942,5)):
        fields.update(range(start, start+size))
    for start in range(800,926,14):
        fields.update(range(start,start+14))
    # The monetary tables require explicit supplied figures, otherwise 확인 필요.
    for start in (5656,5663,5671,5678,5685,5692,5707,5714,5723,5730,5739,5746,5753,5760,5767,5775,5782,5789):
        fields.update(range(start,start+6))
    for start in (5832,5840,5849,5857,5865,5874,5882,5890,5898,5907,5915,5923,5933,5941,5951,5959,5967,5983,5991,6000,6008,6024):
        fields.update(range(start,start+7))
    # Complete the previously unbound topics using actual table addresses. A
    # merged label is context, not an instruction to write into the label itself.
    options = {}
    table_rules = {3639:(2,0),3681:(2,0),3728:(1,0),3744:(2,0),3769:(3,0),
                   5172:(1,0),5212:(1,4),5242:(0,4),5392:(4,2)}
    schedules = {1468:3,1834:2,2528:2}
    schedule_clear = []
    for table in root.iter('TABLE'):
        table_ps = list(table.iter('P'))
        if not table_ps:
            continue
        first = indices[id(table_ps[0])]
        if first not in table_rules and first not in schedules:
            continue
        cells = [c for row in table.findall('ROW') for c in row.findall('CELL')]
        for cell in cells:
            row, col = int(cell.get('RowAddr', 0)), int(cell.get('ColAddr', 0))
            cp = list(cell.iter('P'))
            if not cp:
                continue
            i = indices[id(cp[0])]
            if first in schedules:
                if row < schedules[first] or col == 0:
                    continue
                if col >= 2 and col < int(table.get('ColCount'))-(0 if first == 1468 else 1):
                    schedule_clear.extend(indices[id(p)] for p in cp)
                    # The original graphic spans three physical rows. Use one
                    # row for editable markers, not three duplicated schedules.
                    if (row-schedules[first]) % 3:
                        continue
                    options[i] = {'kind':'schedule_marker','allow_empty':True,'max_chars':1}
                else:
                    options[i] = {'max_chars':65,'allow_empty':True}
            else:
                min_row, min_col = table_rules[first]
                if row < min_row or col < min_col:
                    continue
                options[i] = {'allow_empty':True,'max_chars':100}
            row_labels = [own_text(p) for c in cells if int(c.get('RowAddr',0)) == row
                          and int(c.get('ColAddr',0)) < col for p in c.iter('P') if own_text(p).strip()]
            col_labels = [own_text(p) for c in cells if int(c.get('RowAddr',0)) < row
                          and int(c.get('ColAddr',0)) <= col < int(c.get('ColAddr',0))+int(c.get('ColSpan',1))
                          for p in c.iter('P') if own_text(p).strip()]
            options[i]['context'] = f'표 P{first:04d}, 행 {row+1}, 열 {col+1}; 행 제목: ' + ' / '.join(row_labels[:4]) + '; 열 제목: ' + ' / '.join(col_labels[:8])
            options[i]['clear_indices'] = [indices[id(p)] for p in cp[1:]]
            fields.add(i)
    fields.update({4346,4351,7117,7119,7122,7124,7127,7129,7131,7133,7135,7137,
                   7139,7141,7143,7145,7151,7153,7154,7156,7157,7158,7161,7166,7169,7172,7175})
    options[4346] = {'context':'표준연구개발과제 해당 여부와 표준화전략. 해당하지 않으면 해당 없음.'}
    options[4351] = {'context':'규제샌드박스 적용 여부, 실제 규제와 연계방안. 미확정 근거는 확인 필요.'}
    for i, p in enumerate(ps):
        if i >= 116 and re.search(r'AAAAA|BBBBB|YYYY|yy\.mm|20um급|IS4010E|고성능 패킷|기관명[A-C]', own_text(p)):
            fields.add(i)
    # The guide under the first 5-2 heading describes 5-1, not 5-2.
    shared = {657:[(710,723)],667:[(710,723)],692:[(710,723)],
              3230:[(3375,3385)],3249:[(3375,3385)],
              3592:[(3625,3635)],3605:[(3625,3635)],3676:[(3807,3817)]}
    # Split multi-topic guide tables; blue annotations are separately attributed
    # by subtopic and combined in the same MD without surrounding black text.
    guide_overrides = {
        657:[(710,714),(723,723)],
        667:[(710,711),(716,717),(723,723)],
        692:[(710,711),(719,723)],
        3230:[(3375,3379),(3385,3385)],
        3249:[(3375,3376),(3381,3385)],
        3592:[(3625,3628)],
        3605:[(3625,3626),(3630,3635)],
        3676:[(3807,3817)],
        3806:[],
    }
    excluded_blue = {i:'작성 조건이 아닌 표 항목명·입력 예시' for i in
                     [214,305,313,320,2531,4606,4607,4608,4609,4610,4611,4612,4613,
                      4614,4615,4619,4625,4811,4812,4813,4814,4815,4816,4817,4818,
                      4819,4820,4824,4830,5404]}
    excluded_blue[606] = '목차에 반복된 제출 조건. 실제 해당 항목의 P4382 주석에 보존'
    return registry.register(ASSETS/'source.hwpml', ASSETS/'template.hwp',
        '기후부 2026 연구개발계획서 · 순차작성 v6 (대주제 파일·소주제별 요령)' if group_by_chapter
        else '기후부 2026 연구개발계획서 · 하위 분류 검증용', starts=starts, fixed_fields=fields,
        group_starts=chapters if group_by_chapter else [],
        field_options=options,
        guide_overrides=guide_overrides, common_guide_ranges=[(1337,1337)],
        common_blue=[652,653], excluded_blue=excluded_blue,
        render_policy={'clean_guidance':True,'remove_before':116,'remove_ranges':[[572,625]],
                       'schedule_cells':schedule_clear,'profile':'climate_2026_v2'},
        shared_guides=shared, excluded_guides={3806:[(3807,3817)]}, notes=[
            '작성요령 표 내용과 해당 소주제의 파란 주석·조건을 함께 사용합니다. 일반 본문은 제외합니다.',
            '5-2 두 양식은 원천기술형/혁신제품형·실증형 대안입니다. 해당 유형을 확인하세요.',
            '서명·직인과 실제 발급 증빙은 자동 생성하지 않습니다. 제출 전 사용자가 확인해야 합니다.',
            '양식의 조건부 항목은 과제 적용 여부와 증빙을 확인한 후 정리하세요.'])
