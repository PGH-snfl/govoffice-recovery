"""Migrate one registered template and saved-response bundle, preserving a backup."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import argparse
import json
import re
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import parse_source,read_json,write_json
from govoffice.services.authoring_design_fields import remove_decorative_fields
from govoffice.services.saved_authoring_responses import binding_hash,load_bundle,collapse_review_values


def main():
    parser=argparse.ArgumentParser();parser.add_argument('template');parser.add_argument('bundle');parser.add_argument('--confirmation-only',action='store_true');args=parser.parse_args()
    project=Path(__file__).resolve().parents[2];folder=project/'config/document_authoring/templates'/args.template
    manifest=read_json(folder/'manifest.json');original=deepcopy(manifest)
    removed=remove_decorative_fields(parse_source(folder/'source.hwpml'),manifest)
    packet,path,_=load_bundle(args.bundle);ids={f['id'] for f in removed}
    for response in packet['responses'].values():
        for field_id in ids:response.get('values',{}).pop(field_id,None)
        response['needs_review']=[n for n in response.get('needs_review',[]) if not any(re.search(r'(?<![A-Za-z0-9_])'+re.escape(fid)+r'(?!\d)',n) for fid in ids)]
    packet['template']['binding_sha256']=binding_hash(manifest)
    collapsed=(collapse_review_values(packet,manifest,parse_source(folder/'source.hwpml'))
               if args.confirmation_only else [])
    source=Path(path);backup=source.parent/'archive'/source.name
    backup.parent.mkdir(parents=True,exist_ok=True)
    if backup.exists():backup=backup.with_name(backup.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S')+backup.suffix)
    shutil.copy2(source,backup)
    write_json(folder/'manifest.json',manifest)
    write_json(folder/'입력위치.json',{t['id']:t['fields'] for t in manifest['topics']})
    write_json(source,packet)
    print(json.dumps({'removed':[{'id':f['id'],'label':f.get('label'),'index':f['index']} for f in removed],
                      'confirmation_only_fields':len(collapsed),
                      'backup':str(backup),'bundle':str(source),'template':args.template},ensure_ascii=False))


if __name__=='__main__':main()
