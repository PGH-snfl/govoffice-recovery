"""Archive a completed response packet; optionally register its verified snapshot."""
from pathlib import Path
from uuid import uuid4
import argparse
import json
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import AuthoringService,read_json,write_json,digest
from govoffice.services.saved_authoring_responses import export_bundle,prepare_bundle


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('job_id');parser.add_argument('destination');parser.add_argument('--restore-template',action='store_true')
    args=parser.parse_args();project=Path(__file__).resolve().parents[2]
    def forbidden(*args,**kwargs):raise AssertionError('Archive operation must not call AI or export HWP')
    service=AuthoringService(project/'config',forbidden,forbidden)
    folder=service.job_path(args.job_id);manifest=read_json(folder/'template/manifest.json')
    if any(digest(folder/'template'/name)!=manifest[key] for name,key in [('source.hwpml','source_sha256'),('template.hwp','native_sha256')]):
        raise ValueError('Saved template snapshot was modified')
    template_id=manifest['id']
    if args.restore_template:
        template_id=uuid4().hex;target=service.registry.path(template_id)
        shutil.copytree(folder/'template',target)
        manifest.update(id=template_id,name=manifest['name']+' · 저장응답 재사용용')
        if manifest.get('guide_file'):
            guide=target/Path(manifest['guide_file']).name
            if guide.is_file():manifest['guide_file']=str(guide)
            else:manifest.pop('guide_file',None)
        write_json(target/'manifest.json',manifest)
        service.registry.load(template_id)
    info=export_bundle(service,args.job_id,args.destination)
    _,prepared=prepare_bundle(service,template_id,info['path'])
    info.update(registered_template_id=template_id,registered_template_name=manifest['name'],verified=True)
    print(json.dumps(info,ensure_ascii=False))


if __name__=='__main__':main()
