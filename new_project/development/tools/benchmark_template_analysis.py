"""Offline request-volume comparison. No AI connection or document modification."""
from pathlib import Path
import json
import sys
import threading
import xml.etree.ElementTree as ET

sys.path[:0]=[str(Path(__file__).resolve().parents[2]/'src')]
from govoffice.services.document_authoring import parse_source
from govoffice.services.template_analysis import analyze,source_records,fallback_row


class CountingAgent:
    def __init__(self, retry_index=None):
        self.payloads=[];self.retry_index=retry_index

    def generate(self,prompt,schema,cancel):
        payload=json.loads(prompt.split('\n',1)[1]);self.payloads.append(payload)
        rows=[fallback_row(r,'','preserve') for r in payload['분석대상']]
        if self.retry_index is not None:
            for r in rows:
                if r['index']==self.retry_index:r.update(uncertain=True,reason='모의 재검토')
        return {'items':rows}


def compare(records,retry_index=None):
    batches=[];batch=[];size=0
    for r in records:
        length=len(json.dumps(r,ensure_ascii=False))
        if batch and (len(batch)>=70 or size+length>35000):batches.append(batch);batch=[];size=0
        batch.append(r);size+=length
    if batch:batches.append(batch)
    previous=[]
    for batch in batches:
        payload={'앞선제목':[],'앞뒤문맥':records[max(0,batch[0]['index']-8):batch[-1]['index']+9],
                 '분석대상':batch}
        previous.append(payload)
        if any(r['index']==retry_index for r in batch):previous.append(payload)
    agent=CountingAgent(retry_index)
    rows=analyze(records,agent,threading.Event(),lambda *args:None)
    old_chars=sum(len(json.dumps(p,ensure_ascii=False)) for p in previous)
    new_chars=sum(len(json.dumps(p,ensure_ascii=False,separators=(',',':'))) for p in agent.payloads)
    return {'paragraphs':len(records),'original_positions_retained':[r['index'] for r in records]==[r['index'] for r in rows],
        'ai_calls_before':len(previous),'ai_calls_after':len(agent.payloads),
        'target_paragraphs_before':sum(len(p['분석대상']) for p in previous),
        'target_paragraphs_after':sum(len(p['분석대상']) for p in agent.payloads),
        'payload_characters_before':old_chars,'payload_characters_after':new_chars,
        'payload_reduction_percent':round((1-new_chars/old_chars)*100,1)}


def main():
    project=Path(__file__).resolve().parents[2]
    text='※ 조건과 실행 요령을 빠짐없이 기록합니다. '*35
    source='<HWPML><BODY>'+''.join('<P><TEXT><CHAR>'+text+'</CHAR></TEXT></P>' for _ in range(70))+'</BODY></HWPML>'
    records=source_records(ET.fromstring(source))
    report={'external_ai_called':False,'measured_elapsed_ai_time':False,
        'method':'동일한 고정 모의 응답. 원문·문맥 데이터 문자 수 비교이며 토큰·요금·실제 AI 속도 측정이 아닙니다.',
        'long_guidance_example':compare(records),
        'long_guidance_one_uncertain':compare(records,69)}
    local_source=project/'src/govoffice/institutions/packages/seoultech/climate_2026/source.hwpml'
    if local_source.exists():report['existing_climate_form_local_only']=compare(source_records(parse_source(local_source)))
    output=project/'development/reports/template_analysis_optimization_benchmark.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
