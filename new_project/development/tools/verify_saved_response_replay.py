"""Replay a verified archive through the real exporter, with AI forbidden."""
from pathlib import Path
import json
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import AuthoringService
from govoffice.services.saved_authoring_responses import create_replay
from govoffice.adapters.hwp_form_export import export_generated_hwp

def forbidden(*args):
    raise AssertionError('Offline replay must not instantiate an AI agent')

if __name__=='__main__':
    project=Path(__file__).resolve().parents[2]
    service=AuthoringService(project/'config',forbidden,export_generated_hwp)
    started=time.monotonic()
    try:
        state=create_replay(service,sys.argv[1],sys.argv[2])
        print(json.dumps({'job_id':state['id']},ensure_ascii=False),flush=True)
        service.start(state['id'])
        worker=service.workers[state['id']]
        while worker.is_alive():
            worker.join(10)
            current=service.status(state['id'])
            print(json.dumps({k:current.get(k) for k in ('status','phase','error')},ensure_ascii=False),flush=True)
        result=service.status(state['id'])
        print(json.dumps({'status':result['status'],'hwp_path':result.get('hwp_path'),'seconds':round(time.monotonic()-started,1),
                          'topics':len(result.get('completed',[])),'execution_mode':result.get('execution_mode'),
                          'ai_calls':0,'error':result.get('error')},ensure_ascii=False),flush=True)
        sys.exit(0 if result['status']=='completed' else 1)
    finally:service.close()
