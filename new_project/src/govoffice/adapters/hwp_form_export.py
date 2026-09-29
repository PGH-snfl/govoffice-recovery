"""Export generated HWPML using a separately owned Hancom instance."""
from __future__ import annotations
from pathlib import Path
import json
import os
import subprocess
import sys


def export_generated_hwp(template: Path, hml: Path, destination: Path):
    # A dedicated process isolates the user's active document and bounds COM hangs.
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path(__file__).resolve().parents[2]) + os.pathsep + env.get('PYTHONPATH','')
    env['GOVOFFICE_DIAG_COM'] = '1'
    command = [sys.executable, '-X', 'utf8', str(Path(__file__).resolve()),
               str(template), str(hml), str(destination)]
    try:
        result = subprocess.run(command, capture_output=True, encoding='utf-8',
                                timeout=50, env=env,
                                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    except subprocess.TimeoutExpired as exc:
        output = exc.stderr or b''
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='replace')
        import re
        stages = re.findall(r'GOVOFFICE_STAGE=([a-z_]+)', output)
        stage = stages[-1] if stages else 'worker_not_started'
        if stage == 'dispatching_hwp':
            raise RuntimeError(
                '한글 자동화 연결이 응답하지 않아 변환을 중단했습니다. '
                '작성 내용은 유지됐으며, 열려 있는 한글 문서는 닫거나 수정하지 않았습니다. '
                '작업 중인 문서를 저장한 뒤 한글을 모두 종료하고 다시 시도해 주세요. '
                f'진단 단계: {stage}.'
            ) from exc
        raise RuntimeError('한글 변환 응답시간을 초과했습니다. '
                           f'마지막 단계: {stage}. 임의로 다른 한글 창을 닫지는 않았습니다.') from exc
    lines = result.stdout.strip().splitlines()
    if not lines:
        raise RuntimeError((result.stderr or result.stdout or '한글 변환 실패')[-1600:])
    try:
        data = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError((result.stderr or result.stdout)[-1600:]) from exc
    if not data.get('ok'):
        raise RuntimeError(data.get('error','한글 변환 실패'))
    if result.returncode:
        raise RuntimeError('한글 변환 작업이 정상 종료되지 않았습니다.')
    # HWP may finish flushing its compound file while the owned process closes.
    # The caller sees the final on-disk size, not the earlier in-worker size.
    if not destination.is_file() or destination.stat().st_size < 1024:
        raise RuntimeError('한글 변환 후 최종 출력 파일을 확인할 수 없습니다.')
    data['result']['hwp_bytes']=destination.stat().st_size
    return data['result']


def _worker(template: Path, hml: Path, destination: Path):
    import contextlib
    import hashlib
    import shutil
    import tempfile
    from govoffice.adapters.recovered_hwp import 복구한글어댑터

    def stage(name):
        print('GOVOFFICE_STAGE='+name,file=sys.stderr,flush=True)

    stage('worker_started')
    if destination.exists():
        raise FileExistsError('기존 결과 파일을 덮어쓰지 않습니다.')
    original_hash = hashlib.sha256(template.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='govoffice_climate_export_') as work:
        working = Path(work)/'owned_template.hwp'
        shutil.copy2(template, working)
        adapter = 복구한글어댑터()
        with contextlib.redirect_stdout(sys.stderr):
            try:
                stage('opening_template')
                adapter.관리문서열기(working, 표시=False)
                stage('template_opened')
                app = adapter.원본.대상
                # COM passes a UTF-16 BSTR even though the editable .hml on disk
                # is UTF-8. Hancom rejects a UTF-8 declaration inside that BSTR.
                xml = hml.read_text(encoding='utf-8').replace('encoding="UTF-8"','encoding="UTF-16"',1)
                stage('setting_text')
                if not app.SetTextFile(xml, 'HWPML2X', ''):
                    raise RuntimeError('한글이 생성된 양식을 읽지 못했습니다.')
                stage('text_set')
                exported = app.GetTextFile('TEXT','') or ''
                stage('text_read_back')
                generic = (hml.parent/'입력필드.json').exists()
                markers = () if generic else ('예시·검토용','캠퍼스 태양광','600,000','서울과학기술대학교')
                for marker in markers:
                    if marker not in exported:
                        raise RuntimeError(f'한글 입력 검증 실패: {marker}')
                import re
                import xml.etree.ElementTree as ET
                from govoffice.services.authoring_equations import logical_paragraph_text
                from govoffice.services.authoring_scientific_notation import display_value
                rendered = ET.fromstring(app.GetTextFile('HWPML2X',''))
                stage('hwpml_read_back')
                compact = lambda value: re.sub(r'\s+','',value.replace('\u200b',''))
                actual = compact(''.join(logical_paragraph_text(p) for p in rendered.iter('P')))
                field_values = json.loads((hml.parent/('입력필드.json' if generic else '입력필드_예시값.json')).read_text(encoding='utf-8'))
                # Review annotations may move below the body and gain parentheses.
                # Verify every rendered paragraph, not the old contiguous input.
                missing = [f['field_id'] for f in field_values
                           if any(compact(display_value(v) if f.get('source')=='agent' else v) not in actual
                                  for v in f.get('paragraph_values',[f['value']]))]
                if missing:
                    raise RuntimeError('한글에서 입력값을 다시 확인하지 못했습니다: '+', '.join(missing[:8]))
                expected_equations=sum(field.get('equation_count',0) for field in field_values)
                if len(list(rendered.iter('EQUATION'))) < expected_equations:
                    raise RuntimeError('한글에서 수식 개체를 다시 확인하지 못했습니다.')
                if generic:
                    # Original paragraph positions are preserved in the draft path.
                    # A value occurring somewhere else is not sufficient evidence.
                    actual_ps = list(rendered.iter('P'))
                    expected_ps = list(ET.fromstring(xml).iter('P'))
                    if len(actual_ps) != len(expected_ps):
                        raise RuntimeError('한글 변환 후 문단 구조가 달라 입력 위치 재확인이 필요합니다.')
                    def paragraph_text(p):
                        return logical_paragraph_text(p)
                    for field in field_values:
                        indices=field.get('output_indices',[field.get('output_index',int(field['field_id'][1:]))])
                        values=field.get('paragraph_values',[field['value']])
                        if len(indices)!=len(values) or any(compact(paragraph_text(actual_ps[i]))!=
                                                            compact(display_value(v) if field.get('source')=='agent' else v)
                                                            for i,v in zip(indices,values)):
                            raise RuntimeError('한글 입력 위치 검증 실패: '+field['field_id'])
                expected_page = ET.fromstring(xml).find('.//PAGEDEF')
                actual_page = rendered.find('.//PAGEDEF')
                if expected_page.attrib != actual_page.attrib or expected_page.find('PAGEMARGIN').attrib != actual_page.find('PAGEMARGIN').attrib:
                    (destination.parent/'쪽설정_검증오류.json').write_text(json.dumps({
                        'expected':expected_page.attrib,'actual':actual_page.attrib,
                        'expected_margin':expected_page.find('PAGEMARGIN').attrib,
                        'actual_margin':actual_page.find('PAGEMARGIN').attrib},ensure_ascii=False,indent=2),encoding='utf-8')
                    raise RuntimeError('원본 쪽 설정이 변환 과정에서 달라졌습니다.')
                from govoffice.adapters.hwp_review_memos import attach_native_memos, verify_memos
                baseline = rendered
                rendered, memo_records = attach_native_memos(app, baseline, field_values)
                stage('saving_hwp')
                if app.SaveAs(str(destination.resolve()), 'HWP', '') is False:
                    raise RuntimeError('한글 저장 실패')
                stage('hwp_saved')
                if not destination.exists() or destination.stat().st_size < 1024:
                    raise RuntimeError('한글 저장 파일이 비어 있습니다.')
                pages = int(app.PageCount)
                if memo_records:
                    # Reopen the actual saved output in this owned instance, not
                    # a user document. Success requires persisted native memos.
                    if app.Open(str(destination.resolve()), 'HWP', 'forceopen:true') is False:
                        raise RuntimeError('메모가 저장된 한글 출력본을 다시 열지 못했습니다.')
                    rendered = ET.fromstring(app.GetTextFile('HWPML2X', ''))
                    verify_memos(rendered, memo_records, baseline)
                    (destination.parent/'확인메모.json').write_text(json.dumps(memo_records,ensure_ascii=False,indent=2),encoding='utf-8')
                    (destination.parent/'메모출력_재검증.hml').write_text(ET.tostring(rendered,encoding='unicode'),encoding='utf-8')
                # Read-back artifacts are for verification, not the primary output.
                (destination.parent/'한글출력_검증원문.txt').write_text(exported,encoding='utf-8')
                result = {'pages':pages, 'hwp_bytes':destination.stat().st_size,
                          'verified_markers':len(markers), 'verified_field_values':len(field_values),
                          'field_positions_verified':generic,
                          'page_setup_verified':True, 'original_unchanged':True,
                          'memo_count':len(memo_records), 'memos_verified':bool(memo_records)}
            finally:
                primary_error = sys.exc_info()[1]
                if adapter.문서상태().get('managed'):
                    try:
                        adapter.관리문서닫기(저장여부=False)
                    except Exception as cleanup_error:
                        if primary_error is None:
                            raise
                        # Do not hide the actual conversion error behind cleanup.
                        (destination.parent/'변환_정리경고.txt').write_text(str(cleanup_error),encoding='utf-8')
            if hashlib.sha256(template.read_bytes()).hexdigest() != original_hash:
                raise RuntimeError('원본 양식 무결성 검증 실패')
    return result


if __name__ == '__main__':
    # The bundled embedded Python intentionally ignores PYTHONPATH.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    try:
        import tempfile
        from govoffice.adapters.com_worker_cache import configure_worker_cache
        with tempfile.TemporaryDirectory(prefix='govoffice_export_com_') as cache:
            configure_worker_cache(Path(cache)/'gen_py')
            result = _worker(*(Path(p) for p in sys.argv[1:4]))
        print(json.dumps({'ok':True,'result':result},ensure_ascii=True))
    except Exception as exc:
        print(json.dumps({'ok':False,'error':str(exc)},ensure_ascii=True))
        sys.exit(1)
