"""Open an output in its own verified HWP instance, off the GUI thread."""
import json
from pathlib import Path
import subprocess
import sys


def open_output_hwp(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file() or path.suffix.lower() != '.hwp':
        raise ValueError('열 수 있는 최종 출력 한글 파일이 아닙니다.')
    try:
        run = subprocess.run(
            [sys.executable, '-X', 'utf8', str(Path(__file__).resolve()), str(path)],
            capture_output=True, encoding='utf-8', timeout=45,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('한글 파일 열기 응답시간을 초과했습니다. 기존 한글 창은 닫지 않았습니다.') from exc
    try:
        reply = json.loads(run.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError) as exc:
        raise RuntimeError('한글 파일 열기 결과를 확인하지 못했습니다. '+run.stderr[-600:]) from exc
    if run.returncode or not reply.get('ok'):
        raise RuntimeError(reply.get('error') or '한글 파일 열기에 실패했습니다.')
    result = reply['result']
    if (not result.get('document_open') or not result.get('visible')
            or Path(result.get('path', '')).resolve() != path):
        raise RuntimeError('요청한 출력본이 실제 한글 창에 열렸는지 확인하지 못했습니다.')
    return result


def _worker(path, adapter_factory=None):
    if adapter_factory is None:
        from govoffice.adapters.recovered_hwp import 복구한글어댑터
        adapter_factory = 복구한글어댑터
    adapter = adapter_factory()
    # This never attaches to, clears, or closes a user's existing HWP document.
    # A successful visible instance remains available after this helper exits.
    state = adapter.관리문서열기(path, 표시=True)
    if not state.get('document_open') or not state.get('visible'):
        raise RuntimeError('한글 출력 문서 창을 표시하지 못했습니다.')
    if Path(state.get('path', '')).resolve() != Path(path).resolve():
        raise RuntimeError('한글에 열린 문서가 요청한 출력본과 다릅니다.')
    return {key: state.get(key) for key in ('document_open', 'visible', 'path', 'title', 'editable')}


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    try:
        import tempfile
        from govoffice.adapters.com_worker_cache import configure_worker_cache
        # This helper is a NEW Python process: the desktop backend's private
        # win32com path is not inherited. Configure before loading the adapter.
        # Keep the user's shared cache and all existing HWP documents untouched.
        with tempfile.TemporaryDirectory(prefix='govoffice_output_open_com_') as cache:
            configure_worker_cache(Path(cache)/'gen_py')
            result = _worker(sys.argv[1])
        print(json.dumps({'ok': True, 'result': result}, ensure_ascii=True))
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=True))
        sys.exit(1)
