"""Deterministic checks; not a claim that research facts have been verified."""
from decimal import Decimal, InvalidOperation
import re


def number(value):
    if not isinstance(value, str):
        return None
    value = value.strip().replace(',', '')
    if not re.fullmatch(r'-?\d+(?:\.\d+)?', value):
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def audit_results(manifest, results):
    values = {k:v for r in results.values() for k,v in r['values'].items()}
    unresolved = [k for k,v in values.items() if any(w in v for w in ('확인 필요','미확정','미제공','?'))]
    issues = []
    checks = []
    def equal_sum(label, components, total):
        ns = [number(values.get(f'P{i:04d}')) for i in [*components,total]]
        if any(n is None for n in ns):
            checks.append({'name':label,'status':'not_enough_data'})
            return
        ok = sum(ns[:-1]) == ns[-1]
        checks.append({'name':label,'status':'passed' if ok else 'failed'})
        if not ok:
            issues.append(f'{label}: 구성 금액 합계 {sum(ns[:-1]):,}와 기재 합계 {ns[-1]:,}가 다릅니다.')
    if manifest.get('render_policy', {}).get('profile') == 'climate_2026_v2':
        for start in (234,244,253,263,272):
            equal_sum(f'표지 P{start:04d} 현금 합계', [start,start+1,start+3], start+5)
            equal_sum(f'표지 P{start:04d} 현물 합계', [start+2,start+4], start+6)
            equal_sum(f'표지 P{start:04d} 총액', [start+5,start+6], start+7)
        for start in (5656,5663,5671,5678,5685,5692,5707,5714,5723,5730,5739,5746,5753,5760,5767,5775,5782,5789):
            equal_sum(f'전체 예산 행 P{start:04d}', list(range(start,start+5)), start+5)
        for start in (5832,5840,5849,5857,5865,5874,5882,5890,5898,5907,5915,5923,5933,5941,5951,5959,5967,5983,5991,6000,6008,6024):
            equal_sum(f'기관 예산 행 P{start:04d}', list(range(start,start+6)), start+6)
        for other in (5794,6030):
            a,b=number(values.get('P0241')),number(values.get(f'P{other:04d}'))
            if a is not None and b is not None and a != b:
                issues.append(f'표지 총액 P0241과 예산표 P{other:04d} 총액이 다릅니다.')
    if unresolved:
        issues.append(f'확인 필요 또는 미확정 입력 {len(unresolved)}개: ' + ', '.join(unresolved[:20]))
    return {'numeric_checks':checks,'issues':issues,'unresolved_fields':unresolved,
            'facts_verified':False,'submission_ready':False}


def audit_layout(xml, field_log):
    import xml.etree.ElementTree as ET
    from .authoring_equations import logical_paragraph_text
    from .authoring_scientific_notation import display_value
    root = ET.fromstring(xml)
    ps = list(root.iter('P'))
    def own(p):
        return logical_paragraph_text(p)
    remaining_guides = [t for t in root.iter('TABLE')
                        if '작성요령' in re.sub(r'\s+', '', ''.join(own(p) for p in t.iter('P')))]
    issues = []
    for f in field_log:
        if f.get('table_fit_warning'):
            issues.append(f['field_id']+': '+f['table_fit_warning'])
        indices=f.get('output_indices',[f.get('output_index',int(f['field_id'][1:]))])
        expected=f.get('paragraph_values',[f['value']])
        if sum(len(list(ps[i].iter('EQUATION'))) for i in indices if i < len(ps)) != f.get('equation_count',0):
            issues.append('수식 개체 수 불일치: ' + f['field_id'])
        if len(indices)!=len(expected) or any(i>=len(ps) or own(ps[i]).replace('\u200b','')!=(display_value(value) if f.get('source')=='agent' else value).replace('\u200b','')
                                             for i,value in zip(indices,expected)):
            issues.append('출력 위치 불일치: ' + f['field_id'])
    prototype = [(i,own(p)) for i,p in enumerate(ps) if re.search(r'AAAAA|BBBBB|YYYY|yy\.mm|20um급|IS4010E|고성능 패킷',own(p))]
    if prototype:
        issues.append(f'연결되지 않은 원본 예시 표식 {len(prototype)}개가 남았습니다. 원본 예시 검토 목록을 확인하세요.')
    return {'remaining_guide_tables':len(remaining_guides),'issues':issues,
            'remaining_examples':[{'output_index':i,'text':t} for i,t in prototype],
            'visual_layout_verified':False}
