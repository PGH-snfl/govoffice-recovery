"""Local-only request count and exact guidance coverage check on the bundled form."""
from pathlib import Path
import json
import sys
import threading
import time

sys.path[:0]=[str(Path(__file__).resolve().parents[2]/'src')]
from govoffice.services.document_authoring import parse_source,own_text
from govoffice.services.template_analysis import source_records,analyze,fallback_row
from govoffice.services.template_topic_analysis import analyze_topics,TITLE
from govoffice.services.writing_guides import blue_annotations


class Counter:
    def __init__(self):self.prompts=[]
    def generate(self,prompt,schema,cancel):
        self.prompts.append(prompt);data=json.loads(prompt.split('\n',1)[1])
        if data.get('mode')=='headings':
            return {'items':[dict(index=h['index'],chapter_anchor=h['index'],accepted=bool(TITLE.match(h['text'])),uncertain=False,reason='') for h in data['targets']]}
        if data.get('mode')=='guides':
            return {'items':[dict(id=b['id'],topic_anchors=([data['headings'][0]['index']] if data['headings'] else []),
                scope='common',accepted=True,uncertain=False,reason='',assignments=[]) for b in data['targets']]}
        return {'items':[fallback_row(r,'','preserve') for r in data['분석대상']]}


def main():
    project=Path(__file__).resolve().parents[2]
    root=parse_source(project/'src/govoffice/institutions/packages/seoultech/climate_2026/source.hwpml')
    records=source_records(root);old=Counter();new=Counter();cancel=threading.Event()
    analyze(records,old,cancel,lambda *args:None)
    started=time.monotonic();decisions,audit=analyze_topics(root,records,new,cancel,lambda *args:None)
    ps=list(root.iter('P'));ids={id(p):i for i,p in enumerate(ps)}
    tables=[t for t in root.iter('TABLE') if '작성요령' in ''.join(own_text(p) for p in list(t.iter('P'))[:2]).replace(' ','')]
    table_ids={ids[id(p)] for t in tables for p in t.iter('P')};blue,_,_=blue_annotations(root,ps,table_ids)
    expected={i:own_text(ps[i]) for i in table_ids if own_text(ps[i]).strip()}|blue
    actual={p['index']:p['text'] for b in audit['guide_blocks'] for p in b['paragraphs']}
    report={'external_ai_called':False,'semantic_accuracy_measured':False,'elapsed_local_mock_seconds':round(time.monotonic()-started,3),
        'source_paragraphs':len(records),'heading_candidates':len(audit['headings']),'guide_blocks':len(audit['guide_blocks']),
        'guide_tables':sum(b['kind']=='table' for b in audit['guide_blocks']),'original_guidance_paragraphs':len(expected),
        'all_original_guidance_text_preserved':expected==actual,
        'original_positions_preserved':[r['index'] for r in records]==[r['index'] for r in decisions],
        'previous_ai_requests':len(old.prompts),'new_ai_requests':len(new.prompts),
        'previous_prompt_characters':sum(map(len,old.prompts)),'new_prompt_characters':sum(map(len,new.prompts)),
        'unprocessed_guide_blocks':audit['unprocessed_guide_blocks'],
        'note':'동일 양식의 모의 분류 기준 요청량 비교입니다. 실제 AI 소요 시간과 의미 분류의 정확도를 측정한 것이 아닙니다.'}
    output=project/'development/reports/template_topic_analysis_benchmark.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
