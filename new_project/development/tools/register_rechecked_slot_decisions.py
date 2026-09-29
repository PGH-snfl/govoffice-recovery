"""Build an isolated test registration from the saved live second-pass decisions."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
from uuid import uuid4

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.services.document_authoring import TemplateRegistry,render_draft
from govoffice.services.template_guide_registration import _finish_guided_bundle


def main():
    old=PROJECT/'development/reports/input_slot_registration_live_2026-09-28/templates/d82ee035689045b3a48141faddd8cb7f'
    report=PROJECT/'development/reports/input_slot_recheck_2026-09-28'
    baseline=json.loads((old/'manifest.json').read_text(encoding='utf-8'))
    decisions=json.loads((report/'slot_decisions.json').read_text(encoding='utf-8'))
    verification=json.loads((report/'verification.json').read_text(encoding='utf-8'))
    registry=TemplateRegistry(report/'templates')
    template_id=uuid4().hex
    with tempfile.TemporaryDirectory(prefix='.rechecked-',dir=registry.folder) as temporary:
        folder=Path(temporary)/'bundle';folder.mkdir()
        shutil.copy2(old/'source_original.hwpml',folder/'source_original.hwpml')
        shutil.copy2(old/'template.hwp',folder/'template.hwp')
        shutil.copytree(old/'guides',folder/'guides')
        manifest=_finish_guided_bundle(folder,'연구개발제안서 · 입력칸 재검토 검증',template_id,
            baseline['guide_outline'],decisions,
            baseline['ai_analysis_requests']+verification['real_ai_recheck_calls'],baseline['id'])
        folder.rename(registry.path(template_id))
    loaded=registry.load(template_id)
    fields=[f for t in loaded['topics'] for f in t['fields']]
    facts=[f for f in fields if f['role']=='factual']
    if (len(loaded['analysis_reviews'])!=0 or
            len(loaded['covered_review_indices'])!=verification['new_review_count'] or len(facts)<30):
        raise AssertionError('검토 목록 또는 사실값 분류가 저장 결과와 맞지 않습니다.')
    body=next(f for f in fields if f['role']=='body' and f.get('slot_marker') and not f.get('write_blocked'))
    rendered,_=render_draft(registry.path(template_id),loaded,{},local_values={body['id']:'검증'})
    if '〔P' in rendered or '검증' not in rendered:
        raise AssertionError('재검토 양식에서 입력칸 표식 또는 검증값이 올바르지 않습니다.')
    (report/'검증출력.hml').write_text(rendered,encoding='utf-8')
    verification.update(template_id=template_id,template_path=str(registry.path(template_id)),
                        field_count=len(fields),factual_field_count=len(facts),
                        marked_slot_count=sum(bool(f.get('slot_marker')) for f in fields),
                        user_review_count=len(loaded['analysis_reviews']),
                        covered_review_count=len(loaded['covered_review_indices']),
                        sample_written_field=body['id'],analysis_status=loaded['analysis_status'],
                        registered_copy_verified=True,rendered_marker_absent=True)
    (report/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:verification[k] for k in ('template_id','field_count','factual_field_count',
        'marked_slot_count','new_review_count','user_review_count',
        'covered_review_count','registered_copy_verified')},ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
