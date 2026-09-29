"""Restore AI prose from a verified backup; retain short review markers for facts."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import argparse
import json
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import parse_source,read_json,write_json
from govoffice.services.saved_authoring_responses import load_bundle,binding_hash
from govoffice.services.authoring_response_policy import normalize_response,source_cell_widths,prose_field


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('template_id');parser.add_argument('current_bundle');parser.add_argument('original_bundle')
    args=parser.parse_args();project=Path(__file__).resolve().parents[2]
    folder=project/'config/document_authoring/templates'/args.template_id
    manifest=read_json(folder/'manifest.json')
    current,path,_=load_bundle(args.current_bundle);original,_,_=load_bundle(args.original_bundle)
    fingerprint=binding_hash(manifest)
    if current['template']['binding_sha256']!=fingerprint or original['template']['binding_sha256']!=fingerprint:
        raise ValueError('응답과 양식의 입력 위치가 다릅니다. 파일을 변경하지 않았습니다.')
    if any(current['template'][k]!=original['template'][k] for k in ('source_sha256','native_sha256')):
        raise ValueError('원본 양식이 서로 다릅니다. 파일을 변경하지 않았습니다.')
    widths=source_cell_widths(parse_source(folder/'source.hwpml'),manifest)
    responses=deepcopy(original['responses']);counts={'prose':0,'factual_review':0,'other':0}
    for topic in manifest['topics']:
        tid=topic['id'];response=responses[tid]
        if set(response['values'])!={f['id'] for f in topic['fields']}:
            raise ValueError(tid+'의 원래 입력 필드가 현재 양식과 맞지 않습니다.')
        old_values=deepcopy(response['values'])
        changed=normalize_response(topic,response,widths)
        for field in topic['fields']:
            key=field['id']
            if prose_field(field,widths.get(key)) and response['values'][key] and response['values'][key]!='확인 필요':
                counts['prose']+=1
            elif key in changed or (old_values[key]!=response['values'][key]):counts['factual_review']+=1
            else:counts['other']+=1
    current['responses']=responses
    target=Path(path);backup=target.parent/'archive'/(target.stem+'_before_prose_restore_'+datetime.now().strftime('%Y%m%d_%H%M%S')+target.suffix)
    backup.parent.mkdir(parents=True,exist_ok=True)
    if backup.exists():raise FileExistsError(backup)
    shutil.copy2(target,backup)
    write_json(target,current)
    print(json.dumps({'bundle':str(target),'backup':str(backup),'counts':counts},ensure_ascii=False))


if __name__=='__main__':main()
