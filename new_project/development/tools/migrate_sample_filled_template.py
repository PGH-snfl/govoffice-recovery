"""Locally migrate the known climate form's sample-filled table to a new registration.

No external AI call is made. The original registration and its existing jobs
remain intact; every changed paragraph is enumerated and checked below.
"""
from pathlib import Path
import json
import sys
import threading

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'src'))

from govoffice.services.document_authoring import TemplateRegistry
from govoffice.services.template_guide_registration import recheck_registered_guided

SOURCE_ID = '2e7a7203e86040c2b75b1b52676c0cfa'
SOURCE_HASH = 'd31de45e6787e1862307cfce3a4a5cefc50a313fea1b36f1f73cabf68fd5f696'
DATE_INDICES = {86, 91, 93, 96, 98, 656, 661, 674, 678, 700, 701, 709, 710,
                726, 732, 767, 771}
BODY_LABELS = {
    466: '최종목표 1', 467: '최종목표 2',
    471: '최종 산출물 1', 472: '최종 산출물 2', 473: '최종 산출물 3',
    477: '주요 기능 1', 478: '주요 기능 2', 479: '주요 기능 3',
    482: '주요 성능치 1', 499: '주요 성능치 2', 500: '주요 성능치 3',
    503: '핵심 기술 1', 504: '핵심 기술 2',
    508: '적용 범위 1', 509: '적용 범위 2',
    **{i: f'성과 지표 표 항목 {i-484}' for i in range(485, 499)},
}
PRESERVE_INDICES = {463, 464, 465, 470, 475, 476, 481, 502, 507}
EXPECTED_NEW = DATE_INDICES | set(BODY_LABELS) | PRESERVE_INDICES


class LocalExampleClassifier:
    def __init__(self):
        self.seen = set()

    def generate(self, prompt, schema, cancel):
        batch = json.loads(prompt.rsplit('\n', 1)[1])['slots']
        rows = []
        for item in batch:
            index = item['index']
            if 'first_pass' in item:
                rows.append(item['first_pass'])
                continue
            if index not in EXPECTED_NEW:
                raise ValueError(f'확인하지 않은 예시 후보 {index}는 자동 변경하지 않습니다.')
            self.seen.add(index)
            if index in BODY_LABELS:
                role, anchor, label = 'body', 461, BODY_LABELS[index]
            elif index in DATE_INDICES:
                role, anchor, label = 'factual', -1, '연구개발 기간·일정'
            else:
                role, anchor, label = 'preserve', -1, item['text'][:80]
            rows.append({'index': index, 'role': role, 'topic_index': anchor,
                         'label': label, 'confidence': 'high',
                         'reason': '원본의 다른 과제 예시와 양식 고정 문구를 로컬에서 구분'})
        return {'slots': rows}


def main():
    registry = TemplateRegistry(PROJECT / 'config/document_authoring/templates')
    original = registry.load(SOURCE_ID)
    if original.get('original_source_sha256') != SOURCE_HASH:
        raise ValueError('예상한 원본 양식 버전이 아니어서 수정하지 않았습니다.')
    classifier = LocalExampleClassifier()
    result = recheck_registered_guided(registry, SOURCE_ID, classifier,
                                        threading.Event(), lambda *args: None)
    if classifier.seen != EXPECTED_NEW:
        raise ValueError('예시 후보 집합이 예상과 달라 결과를 사용하지 마세요.')
    if result.get('recheck_added_sample_slots') != len(DATE_INDICES | set(BODY_LABELS)):
        raise ValueError('예시 입력칸 등록 수가 예상과 다릅니다.')
    print(json.dumps({k: result.get(k) for k in
                      ('id', 'name', 'derived_from_template_id',
                       'recheck_added_sample_slots',
                       'analysis_status')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
