"""Recheck only previously uncertain slots in the approved test form."""
import json
from pathlib import Path
import sys
import threading

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.adapters.codex_author import CodexAuthor
from govoffice.services.ai_input_slots import analyze_input_slots
from govoffice.services.document_authoring import parse_source


def main():
    old=PROJECT/'development/reports/input_slot_registration_live_2026-09-28/templates/d82ee035689045b3a48141faddd8cb7f'
    report=PROJECT/'development/reports/input_slot_recheck_2026-09-28'
    report.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((old/'manifest.json').read_text(encoding='utf-8'))
    saved=json.loads((old/'입력칸판정.json').read_text(encoding='utf-8'))
    original={x['index']:x for x in saved['slots']}
    class ReplayFirstPass:
        def __init__(self,real):self.real=real;self.real_calls=0;self.replayed=0
        def generate(self,prompt,schema,cancel):
            slots=json.loads(prompt.rsplit('\n',1)[1])['slots']
            if slots and 'first_pass' in slots[0]:
                self.real_calls+=1
                return self.real.generate(prompt,schema,cancel)
            self.replayed+=1
            return {'slots':[original[x['index']] for x in slots]}
    real=CodexAuthor(report)
    try:
        if not real.account()['connected']:
            raise RuntimeError('Codex 계정에 로그인되어 있지 않습니다.')
        agent=ReplayFirstPass(real)
        result=analyze_input_slots(parse_source(old/'source_original.hwpml'),
            manifest['guide_outline'],agent,threading.Event(),
            lambda phase,done,total:print(f'{phase} ({done}/{total})',flush=True))
    finally:real.close()
    current={x['index']:x for x in result['slots']}
    old_reviews=set(saved['audit']['review_indices'])
    resolved=sorted(i for i in old_reviews if current[i]['confidence']=='high')
    if any(current[i]!=row for i,row in original.items() if i not in old_reviews):
        raise AssertionError('확정된 기존 판정이 재검토 중 변경되었습니다.')
    output={'result':'passed','first_pass_replayed_calls':agent.replayed,
        'real_ai_recheck_calls':agent.real_calls,
        'old_review_count':len(old_reviews),
        'new_review_count':len(result['audit']['review_indices']),
        'resolved_count':len(resolved),'resolved_indices':resolved,
        'remaining_indices':result['audit']['review_indices'],
        'role_counts':result['audit']['role_counts']}
    (report/'verification.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    (report/'slot_decisions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
