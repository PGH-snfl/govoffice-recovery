"""Rework the saved hydrogen-fusion answer into the form's sample-filled table.

This is a local, reviewed example for testing the corrected registration. It
does not claim measured results or submit a research proposal.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import sys

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapt_saved_response_bundle import registry_service
from govoffice.services.document_authoring import TemplateRegistry, read_json, write_json
from govoffice.services.saved_authoring_responses import binding_hash, load_bundle, prepare_bundle

SOURCE_ID = '2e7a7203e86040c2b75b1b52676c0cfa'
TARGET_ID = '0f5546b4e37e4f0db1eed5daf75abd06'
SOURCE = PROJECT / 'ai_response_library/수소핵융합에너지_20260919_응답묶음_등록양식용.json'
OUTPUT = PROJECT / 'ai_response_library/수소핵융합에너지_20260929_예시표복구용_v2.json'
REPORT = PROJECT / 'development/reports/sample_table_repair_20260929_v2.json'

# Only the research intent and proposed evaluation approach in the saved
# P0461 response are redistributed. No performance result is invented.
TABLE_VALUES = {
    'P0466': '수소핵융합 에너지 생산과 에너지 전환의 요구조건·시스템 경계를 정의하고 연계 성능을 검증한다.',
    'P0467': '비핵 모사열원 시험과 실제 핵융합 환경 실증을 구분하고 미검증 범위를 명시한다.',
    'P0471': '요구조건 정의서와 계통 설계서(SYS)',
    'P0472': '열수지·과도응답 해석모델(SW)',
    'P0473': '부품·통합시험 계획서 및 시험 후 결과보고서(SYS)',
    'P0477': '핵융합 발생에너지와 운전 지속시간의 계측 범위를 정의한다.',
    'P0478': '열회수부·전환부의 열수지와 과도응답을 해석한다.',
    'P0479': '과열·고압·누설을 감시하고 안전정지 조건을 설계한다.',
    'P0482': '생산·전환 성능은 계통 경계와 측정 불확실성을 함께 제시한다.',
    'P0499': '회수열량·압력손실·전환 출력을 평가한다.',
    'P0500': '내부소비전력과 연속운전시간을 평가한다.',
    'P0503': '생산부·열회수부·전환부의 연계 해석모델을 구성한다.',
    'P0504': '운전조건 변화에 대응하는 안전·제어 설계를 검토한다.',
    'P0508': '비핵 모사열원 시험으로 전환계통 성능을 평가한다.',
    'P0509': '시설·허가·계측체계가 확보되면 실제 핵융합 연계 실증을 별도로 검증한다.',
    'P0485': '평가 항목',
    'P0486': '목표값',
    'P0487': '검증 방법',
    'P0488': '확인 사항',
    'P0489': '에너지 생산',
    'P0490': '확인 필요',
    'P0491': '에너지 계측',
    'P0492': '경계·오차',
    'P0493': '시설 조건',
    'P0494': '에너지 전환',
    'P0495': '확인 필요',
    'P0496': '출력 계측',
    'P0497': '소비전력',
    'P0498': '시험 조건',
}


def main():
    if OUTPUT.exists() or REPORT.exists():
        raise FileExistsError('새 응답 묶음 또는 검증 보고서가 이미 있습니다. 덮어쓰지 않습니다.')
    registry = TemplateRegistry(PROJECT / 'config/document_authoring/templates')
    old = registry.load(SOURCE_ID)
    new = registry.load(TARGET_ID)
    packet, _, digest = load_bundle(SOURCE)
    identity = packet.get('template', {})
    if (identity.get('id') != SOURCE_ID or
            identity.get('source_sha256') != old['source_sha256'] or
            identity.get('native_sha256') != old['native_sha256'] or
            new['native_sha256'] != old['native_sha256']):
        raise ValueError('저장된 응답과 두 양식의 원본이 일치하지 않습니다.')
    if 'P0461' not in packet['responses']['s0461']['values']:
        raise ValueError('분배할 기존 목표 본문이 없습니다.')
    result = deepcopy(packet)
    result['template'] = {'id':TARGET_ID,'name':new['name'],
                          'source_sha256':new['source_sha256'],
                          'native_sha256':new['native_sha256'],
                          'binding_sha256':binding_hash(new)}
    new_ids = {f['id'] for t in new['topics'] for f in t['fields']}
    result['local_values'] = {k:v for k,v in packet.get('local_values',{}).items() if k in new_ids}
    result['input_snapshot'] = []
    for item in new['topics']:
        prior = packet['responses'].get(item['id'])
        if not isinstance(prior,dict):
            raise ValueError('기존 응답 소주제가 누락되었습니다: '+item['id'])
        values = {}
        for field in item['fields']:
            field_id = field['id']
            if field_id in TABLE_VALUES:
                value = TABLE_VALUES[field_id]
            elif field_id in prior['values']:
                value = prior['values'][field_id]
            elif field.get('role') in {'personal','factual'}:
                value = ''
            else:
                raise ValueError('본문 입력값을 임의로 비울 수 없습니다: '+field_id)
            if len(value)>field['max_chars']:
                raise ValueError('표 칸에 들어갈 글이 허용 길이를 넘습니다: '+field_id)
            values[field_id] = value
        result['responses'][item['id']] = {'topic_id':item['id'],'values':values,
                                          'needs_review':list(prior.get('needs_review',[]))}
    topic = result['responses']['s0461']
    field_ids = {field['id'] for item in new['topics'] if item['id']=='s0461'
                 for field in item['fields']}
    if field_ids != set(TABLE_VALUES):
        raise ValueError('목표 표의 입력 위치가 검토한 버전과 다릅니다.')
    topic['values'].update(TABLE_VALUES)
    topic['needs_review'].extend([
        'P0490: 생산 성능 목표값은 실제 시설·계측 조건 확정 후 입력해야 합니다.',
        'P0495: 전환 성능 목표값은 계통 경계와 시험 조건 확정 후 입력해야 합니다.',
    ])
    result['migration'] = {'source_bundle_sha256':digest,'source_template_id':SOURCE_ID,
                           'reworked_prose': [{
        'source_field_id':'P0461', 'target_field_ids':sorted(TABLE_VALUES),
        'method':'기존 본문 요지를 현 양식 표 항목에 맞춰 수작업 재구성',
        'unverified_values':['P0490','P0495'],
    }], 'policy':'같은 원본 양식의 동일 위치 응답은 보존하고, 예시 목표 표만 로컬 재구성. 미확정 수치와 기간은 확정값으로 쓰지 않음.'}
    result['exported_at'] = datetime.now().astimezone().isoformat()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT, result)
    try:
        _, info = prepare_bundle(registry_service(registry), TARGET_ID, OUTPUT)
    except Exception:
        OUTPUT.unlink(missing_ok=True)
        raise
    report = {'status':'validated','output':str(OUTPUT), 'template_id':TARGET_ID,
              'table_fields_filled':len(TABLE_VALUES), 'unverified_numeric_fields':['P0490','P0495'],
              'prepared_topics':info['topics'],
              'source_bundle_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    write_json(REPORT, report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
