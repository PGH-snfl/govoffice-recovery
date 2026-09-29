"""Validate saved responses and finish export offline, with no AI calls."""
from pathlib import Path
import json
import shutil
import sys
import threading
from datetime import datetime

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import AuthoringService,read_json,validate_result,render_draft
from govoffice.adapters.hwp_form_export import export_generated_hwp


def recover(job_folder):
    folder=Path(job_folder).resolve(strict=True)
    state=read_json(folder/'state.json')
    if state['status'] not in {'failed','paused','interrupted'}:
        raise ValueError('오류 또는 중단된 작업만 복구합니다.')
    manifest=read_json(folder/'template/manifest.json')
    results={t['id']:validate_result(t,read_json(folder/'responses'/(t['id']+'.json')))
             for t in manifest['topics']}
    xml,fields=render_draft(folder/'template',manifest,results,state.get('local_values',{}))
    if xml!=(folder/'작성중.hml').read_text(encoding='utf-8'):
        raise ValueError('저장된 본문과 응답 재구성 내용이 다릅니다. 자동 복구를 중단합니다.')
    if fields!=read_json(folder/'입력필드.json'):
        raise ValueError('입력 필드 기록이 일치하지 않습니다.')
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2(folder/'state.json',folder/('state.before_recovery_'+stamp+'.json'))
    def no_ai(_):raise RuntimeError('복구 중 새 AI 호출은 허용하지 않습니다.')
    service=AuthoringService(folder.parent.parent.parent,no_ai,export_generated_hwp)
    if service.job_path(state['id']).resolve()!=folder:raise ValueError('작업 경로 불일치')
    service.stops[state['id']]=threading.Event()
    service._run(state['id'])
    final=read_json(folder/'state.json')
    if final['status']!='completed':raise RuntimeError(final.get('error','변환 실패'))
    final.pop('error',None)
    from govoffice.services.document_authoring import write_json
    write_json(folder/'state.json',final)
    print(json.dumps({'hwp':final['hwp_path'],'topics':len(results),'fields':len(fields),
                      'native':final['native'],'review_count':len(final['review'])},ensure_ascii=False))


if __name__=='__main__':recover(sys.argv[1])
