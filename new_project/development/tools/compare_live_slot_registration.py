"""Compare live AI slot decisions with the prior registered form's field map."""
import json
from pathlib import Path
import sys

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.services.document_authoring import own_text,parse_source
from govoffice.services.numbered_topics import flatten


def main():
    prior=PROJECT/'development/reports/template_layout_validation/layout_9450dc0d/config/document_authoring/templates/838b4a1891be475892d49dbee2d07e70'
    live=PROJECT/'development/reports/input_slot_registration_live_2026-09-28'
    report=json.loads((live/'verification.json').read_text(encoding='utf-8'))
    folder=live/'templates'/report['template_id']
    previous=json.loads((prior/'manifest.json').read_text(encoding='utf-8'))
    current=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    decisions=json.loads((folder/'입력칸판정.json').read_text(encoding='utf-8'))['slots']
    source_texts=[own_text(p).strip() for p in parse_source(prior/'source.hwpml').iter('P')]
    known={f['index']:(t,f) for t in previous['topics'] for f in t['fields']}
    candidate_indices={row['index'] for row in decisions}
    confirmed={row['index']:row for row in decisions
               if row['confidence']=='high' and row['role'] in {'body','factual','personal'}}
    known_candidates=set(known)&candidate_indices
    matched=known_candidates&set(confirmed)
    ai_only=sorted(set(confirmed)-set(known))
    missed=sorted(known_candidates-set(confirmed))
    changed=[]
    for index in sorted(matched):
        recorded=known[index][1]['role']
        actual=confirmed[index]['role']
        if (recorded=='personal')!=(actual=='personal'):
            changed.append(index)
    def sample(indices,limit=30):
        return [{'index':i,'ai_role':confirmed[i]['role'] if i in confirmed else
                    next((x['role'] for x in decisions if x['index']==i),'not_candidate'),
                 'label':confirmed[i]['label'] if i in confirmed else known[i][1].get('label',''),
                 'source_text':source_texts[i][:80]} for i in indices[:limit]]
    old_topics={x['index'] for x in flatten(previous['guide_outline']['chapters']) if x['index'] is not None}
    new_topics={x['index'] for x in flatten(current['guide_outline']['chapters']) if x['index'] is not None}
    comparison={'reference':'prior registered field map, not verified ground truth',
        'candidate_count':len(candidate_indices),'prior_known_candidates':len(known_candidates),
        'confirmed_count':len(confirmed),'matched_prior_count':len(matched),
        'prior_missed_count':len(missed),'ai_only_count':len(ai_only),
        'personal_vs_body_changed_count':len(changed),
        'prior_topic_count':len(old_topics),'ai_topic_count':len(new_topics),
        'topic_index_overlap':len(old_topics&new_topics),
        'ai_only_sample':sample(ai_only),'prior_missed_sample':sample(missed),
        'role_changed_sample':sample(changed)}
    (live/'classification_comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in comparison.items() if not k.endswith('_sample')},ensure_ascii=False,indent=2),flush=True)
    print('AI-only examples: '+json.dumps(comparison['ai_only_sample'][:12],ensure_ascii=False),flush=True)
    print('Missed examples: '+json.dumps(comparison['prior_missed_sample'][:12],ensure_ascii=False),flush=True)


if __name__=='__main__':main()
