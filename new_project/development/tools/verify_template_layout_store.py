"""Isolated real-template layout persistence/replay check; no AI requests."""
from copy import deepcopy
from pathlib import Path
import json
import shutil
import sys
from uuid import uuid4

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import AuthoringService, read_json, write_json, parse_source, render_draft, digest
from govoffice.services.template_layout_store import save_layout_database
from govoffice.services.authoring_policy import prepare_new_job
from govoffice.services.saved_authoring_responses import create_replay
from govoffice.adapters.hwp_form_export import export_generated_hwp


def forbidden(*args):raise AssertionError('Verification must not call AI')


def run(template_folder,bundle,output_parent):
    source=Path(template_folder).resolve()
    original={name:digest(source/name) for name in ('manifest.json','source.hwpml','template.hwp')}
    output=Path(output_parent).resolve()/('layout_'+uuid4().hex[:8])
    service=AuthoringService(output/'config',forbidden,export_generated_hwp)
    try:
        manifest=read_json(source/'manifest.json');folder=service.registry.path(manifest['id'])
        shutil.copytree(source,folder)
        info=save_layout_database(folder,parse_source(folder/'source.hwpml'),manifest)
        write_json(folder/'manifest.json',manifest)
        service.registry.load(manifest['id'])
        preview=deepcopy(manifest);prepare_new_job(preview)
        local={f['id']:('■' if f.get('kind')=='schedule_marker' else '입력 위치 검증') for t in preview['topics'] for f in t['fields']}
        stored_xml,stored_log=render_draft(folder,preview,{},local_values=local)
        legacy=deepcopy(preview);legacy.pop('layout_database')
        legacy_xml,legacy_log=render_draft(folder,legacy,{},local_values=local)
        assert stored_xml==legacy_xml and stored_log==legacy_log,'Database changed protected layout or writing destinations'
        job=create_replay(service,manifest['id'],str(Path(bundle).resolve()))
        service.start(job['id']);service.workers[job['id']].join(90)
        result=service.status(job['id'])
        assert result['status']=='completed',result.get('error') or result['status']
        assert original=={name:digest(source/name) for name in original},'Original registration changed'
        report={'template_id':manifest['id'],'database':str(folder/info['file']),**info,
                'legacy_render_identical':True,'source_unchanged':True,'ai_calls':0,
                'job_id':job['id'],'status':result['status'],'hwp_path':result.get('hwp_path')}
        write_json(output/'verification.json',report)
        print(json.dumps(report,ensure_ascii=False))
    finally:service.close()


if __name__=='__main__':run(*sys.argv[1:])
