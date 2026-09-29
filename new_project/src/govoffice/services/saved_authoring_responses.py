"""Portable response data; never executable instructions or template paths."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import hashlib
import json
import re

FORMAT='govoffice.saved-ai-responses'
MAX_BYTES=64*1024*1024


def binding_hash(manifest):
    mapping=[{'id':t['id'],'start':t['start'],'fields':[
        {k:f.get(k) for k in ('id','index','original','role','kind','insert_after')}
        for f in t['fields']]} for t in manifest['topics']]
    return hashlib.sha256(json.dumps(mapping,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest()


def collapse_review_values(bundle,manifest,root):
    """Simplify cautions by field role without discarding narrative content."""
    from .authoring_response_policy import normalize_response,source_cell_widths
    widths=source_cell_widths(root,manifest);changed=[]
    for topic in manifest['topics']:
        for field_id in normalize_response(topic,bundle['responses'][topic['id']],widths):
            changed.append({'topic_id':topic['id'],'field_id':field_id})
    return changed


def export_bundle(service,job_id,destination):
    from .document_authoring import read_json,write_json,digest
    folder=service.job_path(job_id);state=read_json(folder/'state.json')
    if state.get('status')!='completed':raise ValueError('완료된 작업의 응답만 내보낼 수 있습니다.')
    manifest=read_json(folder/'template/manifest.json')
    responses={t['id']:read_json(folder/'responses'/(t['id']+'.json')) for t in manifest['topics']}
    bundle={'format':FORMAT,'version':1,'exported_at':datetime.now().isoformat(),
            'source_job_id':job_id,'title':state['title'],
            'template':{'id':manifest['id'],'name':manifest['name'],
                        'source_sha256':digest(folder/'template/source.hwpml'),
                        'native_sha256':digest(folder/'template/template.hwp'),
                        'binding_sha256':binding_hash(manifest)},
            'brief':state['brief'],'local_values':state.get('local_values',{}),
            'input_snapshot':state.get('input_snapshot',[]),'responses':responses,
            'ai_attempts':{p.name:read_json(p) for p in sorted((folder/'responses').glob('*.attempt*.json'))},
            'prompts':{p.name:p.read_text(encoding='utf-8') for p in sorted((folder/'prompts').glob('*.md'))},
            'research':{t['id']:read_json(folder/'research'/(t['id']+'.json')) for t in manifest['topics']
                        if (folder/'research'/(t['id']+'.json')).is_file()}}
    # Re-exported replay bundles must retain the original detailed review reasons.
    if (folder/'저장응답_원본.json').is_file():
        originals=read_json(folder/'저장응답_원본.json').get('ai_attempts',{})
        if isinstance(originals,dict):bundle['ai_attempts']={**originals,**bundle['ai_attempts']}
    destination=Path(destination).resolve()
    if destination.exists():raise ValueError('같은 이름의 파일이 이미 있습니다. 다른 파일명을 선택하세요.')
    destination.parent.mkdir(parents=True,exist_ok=True)
    write_json(destination,bundle)
    return {'path':str(destination),'topics':len(responses),'ai_attempts':len(bundle['ai_attempts'])}


def load_bundle(path):
    path=Path(path).resolve()
    if path.suffix.lower()!='.json' or not path.is_file():raise ValueError('저장된 AI 응답 묶음 JSON 파일을 선택하세요.')
    if path.stat().st_size>MAX_BYTES:raise ValueError('응답 파일은 64MB 이하만 불러올 수 있습니다.')
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('응답 파일에 중복된 항목이 있습니다: '+key)
            result[key]=value
        return result
    data=path.read_bytes()
    if len(data)>MAX_BYTES:raise ValueError('응답 파일이 너무 큽니다.')
    try:bundle=json.loads(data.decode('utf-8-sig'),object_pairs_hook=unique)
    except (UnicodeError,json.JSONDecodeError) as exc:raise ValueError('응답 파일을 읽지 못했습니다. JSON 형식을 확인하세요.') from exc
    if not isinstance(bundle,dict) or bundle.get('format')!=FORMAT or bundle.get('version')!=1:
        raise ValueError('범정부오피스에서 내보낸 AI 응답 묶음 파일이 아닙니다.')
    return bundle,str(path),hashlib.sha256(data).hexdigest()


def prepare_bundle(service,template_id,path,expected_digest=None):
    from .document_authoring import validate_result,parse_source
    from .authoring_inputs import validate_local_values,saved_input_snapshot
    from .authoring_policy import prepare_new_job
    from .authoring_cell_budget import attach_cell_budgets
    bundle,path,sha=load_bundle(path)
    if expected_digest and sha!=expected_digest:raise ValueError('확인한 이후 응답 파일이 변경되었습니다. 다시 불러오세요.')
    manifest=service.registry.load(template_id);identity=bundle.get('template',{})
    if not isinstance(identity,dict) or any(identity.get(k)!=manifest.get(k) for k in ('source_sha256','native_sha256')) or identity.get('binding_sha256')!=binding_hash(manifest):
        raise ValueError('선택한 양식의 원본 또는 입력 위치가 저장된 응답과 다릅니다. 응답을 생성했던 동일한 양식을 선택하세요.')
    brief=bundle.get('brief')
    if not isinstance(brief,dict) or any(not isinstance(brief.get(k),str) or not brief[k].strip() for k in ('title','description')) or len(json.dumps(brief,ensure_ascii=False))>60000:
        raise ValueError('응답 파일의 작성 주제·세부 내용이 올바르지 않습니다.')
    values=validate_local_values(manifest,bundle.get('local_values'))
    rows=saved_input_snapshot(manifest,values,bundle.get('input_snapshot'))
    prepare_new_job(manifest)
    attach_cell_budgets(parse_source(service.registry.path(template_id)/'source.hwpml'),manifest,values)
    for topic in manifest['topics']:
        for f in topic['fields']:
            if f['id'] in values:f['allow_empty']=True
            if f.get('table_fit'):f['table_fit']['offline_replay']=True
    responses=bundle.get('responses')
    if not isinstance(responses,dict) or set(responses)!={t['id'] for t in manifest['topics']}:
        raise ValueError('저장된 응답의 주제 수나 입력 위치가 양식과 맞지 않습니다. 누락된 내용을 AI로 자동 보충하지 않습니다.')
    if any(not re.fullmatch(r'[A-Za-z0-9_-]+',key) for key in responses):raise ValueError('잘못된 주제 식별번호입니다.')
    clean={t['id']:validate_result(t,responses[t['id']]) for t in manifest['topics']}
    research=bundle.get('research',{})
    if not isinstance(research,dict) or set(research)-set(clean):raise ValueError('조사 기록의 주제 연결이 올바르지 않습니다.')
    from .authoring_research import validate_research
    for topic in manifest['topics']:
        packet=research.get(topic['id'])
        if packet is not None:
            if not isinstance(packet,dict) or not packet.get('web_trace'):raise ValueError('저장된 조사 실행 기록을 확인할 수 없습니다.')
            validate_research(topic,packet.get('result'))
    bundle=deepcopy(bundle);bundle.update(responses=clean,local_values=values,input_snapshot=rows)
    return bundle,{'template_id':template_id,'path':path,'sha256':sha,'brief':brief,'rows':rows,
                   'topics':len(clean),'title':brief['title'],'replay':True,
                   'message':'AI 호출 없이 저장된 응답을 그대로 사용합니다. 현재 서식·문단·확인 메모·출력 검사는 동일하게 적용합니다. 새 요약은 하지 않으며 셀 분량 초과는 검토 사항으로 표시합니다.'}


def create_replay(service,template_id,path,expected_digest=None,local_values=None,input_snapshot=None):
    from .document_authoring import write_json
    # Validate the whole packet before creating a new job. Never fall back to AI.
    bundle,info=prepare_bundle(service,template_id,path,expected_digest)
    state=service.create(template_id,bundle['brief'],review_mode='final_output',
                         local_values=bundle['local_values'] if local_values is None else local_values,
                         input_snapshot=bundle['input_snapshot'] if input_snapshot is None else input_snapshot,
                         research_enabled=bool(bundle.get('research')),_offline=True)
    folder=service.job_path(state['id'])
    for topic_id,response in bundle['responses'].items():
        # IDs have been checked against the registered manifest, not used as paths
        # merely because the input file supplied them.
        if not re.fullmatch(r'[A-Za-z0-9_-]+',topic_id):raise ValueError('잘못된 주제 식별번호입니다.')
        response=deepcopy(response)
        response['values'].update({k:v for k,v in state['local_values'].items() if k in response['values']})
        write_json(folder/'responses'/(topic_id+'.json'),response)
    if bundle.get('research'):
        (folder/'research').mkdir()
        for topic_id,packet in bundle['research'].items():write_json(folder/'research'/(topic_id+'.json'),packet)
    write_json(folder/'저장응답_원본.json',bundle)
    state.update(saved_response_source=info['path'],saved_response_sha256=info['sha256'],
                 source_job_id=bundle.get('source_job_id'),phase='저장된 AI 응답 준비 완료')
    state['review'].append('저장 응답 재사용: 외부 AI 호출·새 자료조사·재요약 없이 기존 내용을 사용했습니다. 셀 분량 초과는 최종 표에서 확인하세요.')
    write_json(folder/'state.json',state)
    return state
