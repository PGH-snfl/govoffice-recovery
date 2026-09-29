"""Register the approved research form with the signed-in Codex agent."""
import json
from pathlib import Path
import sys
import threading
import xml.etree.ElementTree as ET

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.adapters.codex_author import CodexAuthor
from govoffice.services.document_authoring import (
    TemplateRegistry,digest,own_text,parse_source,render_draft,replace_text)
from govoffice.services.template_guide_registration import register_guided


def main():
    source=PROJECT/'development/reports/template_layout_validation/layout_9450dc0d/config/document_authoring/templates/838b4a1891be475892d49dbee2d07e70'
    destination=PROJECT/'development/reports/input_slot_registration_live_2026-09-28'
    destination.mkdir(parents=True,exist_ok=True)
    registry=TemplateRegistry(destination/'templates')
    last_phase=[None]
    def progress(phase,done,total):
        if phase!=last_phase[0]:
            print(f'{phase} ({done}/{total})',flush=True)
            last_phase[0]=phase
    agent=CodexAuthor(destination)
    try:
        if not agent.account()['connected']:
            raise RuntimeError('Codex 계정에 로그인되어 있지 않습니다.')
        print('Codex 계정 연결 확인',flush=True)
        manifest=register_guided(registry,source/'source.hwpml',source/'template.hwp',
                                 '연구개발제안서 · 실제 AI 빈칸 판정 검증',agent,
                                 threading.Event(),progress)
    finally:
        agent.close()
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
    if body is None:
        raise AssertionError('실제 AI 분석에서 본문 입력칸이 확인되지 않았습니다.')
    rendered,field_log=render_draft(folder,loaded,{},local_values={body['id']:'검증'})
    if '〔P' in rendered or not any(x['field_id']==body['id'] and x['value']=='검증' for x in field_log):
        raise AssertionError('출력 시 입력칸 표식이 제거되지 않았거나 검증값이 기록되지 않았습니다.')
    (destination/'검증출력.hml').write_text(rendered,encoding='utf-8')
    report={'result':'passed','classification_source':'signed-in Codex agent',
            'template_id':loaded['id'],'template_path':str(folder),
            'paragraphs':loaded['paragraph_count'],'topic_count':len(loaded['topics']),
            'field_count':len(fields),'marked_slot_count':len(marker_fields),
            'analysis_status':loaded['analysis_status'],
            'slot_audit':loaded['input_slot_analysis'],
            'real_ai_requests':loaded['ai_analysis_requests'],
            'sample_written_field':body['id'],
            'original_xml_structure_preserved':True,'rendered_marker_absent':True}
    (destination/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='slot_audit'},ensure_ascii=False,indent=2),flush=True)
    print(json.dumps({'slot_audit':{k:v for k,v in report['slot_audit'].items() if k!='review_indices'}},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
