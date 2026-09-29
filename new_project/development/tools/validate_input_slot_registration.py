"""Register one real form with recorded decisions, without external AI egress."""
import json
from pathlib import Path
import re
import shutil
import sys
import threading
from unittest.mock import patch
import xml.etree.ElementTree as ET

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.services.document_authoring import (
    TemplateRegistry,digest,own_text,parse_source,render_draft,replace_text)
from govoffice.services.template_guide_registration import register_guided


class RecordedDecisionAgent:
    def __init__(self, baseline):
        self.fields={field['index']:(topic,field)
                     for topic in baseline['topics'] for field in topic['fields']}
        self.requests=0

    def generate(self,prompt,schema,cancel):
        if set(schema['properties'])!={'slots'}:
            raise AssertionError('기록된 작성요령을 사용하므로 다른 AI 요청은 필요하지 않습니다.')
        self.requests+=1
        payload=json.loads(prompt.rsplit('\n',1)[1])
        rows=[]
        for candidate in payload['slots']:
            pair=self.fields.get(candidate['index'])
            if pair:
                topic,field=pair
                role=('personal' if field['role']=='personal' else
                      'factual' if field.get('kind')=='factual_cell' else 'body')
                rows.append({'index':candidate['index'],'role':role,
                    'topic_index':-1 if role=='personal' else topic['start'],
                    'label':field.get('label',''), 'confidence':'high',
                    'reason':'기존 등록에서 확인된 입력 위치'})
            else:
                rows.append({'index':candidate['index'],'role':'preserve',
                    'topic_index':-1,'label':'','confidence':'review',
                    'reason':'기존 등록에 입력 위치로 기록되지 않아 보존'})
        return {'slots':rows}


def main():
    source=PROJECT/'development/reports/template_layout_validation/layout_9450dc0d/config/document_authoring/templates/838b4a1891be475892d49dbee2d07e70'
    report_name=sys.argv[1] if len(sys.argv)>1 else 'input_slot_registration_2026-09-28'
    if not re.fullmatch(r'input_slot_registration_[a-zA-Z0-9_-]+',report_name):
        raise ValueError('잘못된 검증 보고서 폴더 이름입니다.')
    destination=PROJECT/'development/reports'/report_name
    baseline=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    destination.mkdir(parents=True,exist_ok=True)
    registry=TemplateRegistry(destination/'templates')
    agent=RecordedDecisionAgent(baseline)
    def recorded_guides(source_xml,guide_folder,name,agent,cancel,progress):
        shutil.copytree(source/'guides',guide_folder)
        return {'outline':baseline['guide_outline'],'ai_requests':0}
    with patch('govoffice.services.template_guide_registration.export_ai_guides',recorded_guides):
        manifest=register_guided(registry,source/'source.hwpml',source/'template.hwp',
                                 '연구개발제안서 · 빈칸 등록 로컬 검증',agent,
                                 threading.Event(),lambda *args:None)
    folder=registry.path(manifest['id'])
    loaded=registry.load(manifest['id'])
    original=parse_source(folder/'source_original.hwpml')
    marked=parse_source(folder/'source.hwpml')
    original_ps=list(original.iter('P'))
    marked_ps=list(marked.iter('P'))
    fields=[field for topic in loaded['topics'] for field in topic['fields']]
    marker_fields=[field for field in fields if field.get('slot_marker')]
    for field in marker_fields:
        replace_text(original_ps[field['index']],field['slot_marker'])
    if ET.tostring(original)!=ET.tostring(marked):
        raise AssertionError('표식 외에도 원본 XML 구조가 변경되었습니다.')
    if digest(source/'source.hwpml')!=loaded['original_source_sha256']:
        raise AssertionError('원본 양식 보관본의 해시가 일치하지 않습니다.')
    if any(own_text(marked_ps[f['index']])!=f['slot_marker'] for f in marker_fields):
        raise AssertionError('확정된 입력칸의 표식이 원문 위치와 다릅니다.')
    body=next((f for f in fields if f['role']=='body' and not f.get('write_blocked')
               and not f.get('insert_after') and f.get('max_chars',0)>=2),None)
    values={body['id']:'검증'} if body else {}
    rendered,field_log=render_draft(folder,loaded,{},local_values=values)
    if '〔P' in rendered or (body and not any(x['field_id']==body['id'] and x['value']=='검증' for x in field_log)):
        raise AssertionError('출력 시 입력칸 표식이 제거되지 않았거나 검증값이 기록되지 않았습니다.')
    (destination/'검증출력.hml').write_text(rendered,encoding='utf-8')
    report={'result':'passed','classification_source':'recorded prior registration; no live AI',
            'template_id':loaded['id'],'template_path':str(folder),
            'paragraphs':loaded['paragraph_count'],'topic_count':len(loaded['topics']),
            'field_count':len(fields),'marked_slot_count':len(marker_fields),
            'analysis_status':loaded['analysis_status'],
            'slot_audit':loaded['input_slot_analysis'],
            'simulated_classification_requests':agent.requests,'real_ai_requests':0,
            'sample_written_field':body['id'] if body else None,
            'original_xml_structure_preserved':True,'rendered_marker_absent':True}
    (destination/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
