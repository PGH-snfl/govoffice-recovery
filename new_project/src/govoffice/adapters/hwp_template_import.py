"""Read a user-selected HWP through an owned copy, in a bounded child process."""
from pathlib import Path
import json
import subprocess
import sys


def extract_hwp(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if not source.is_file() or source.suffix.lower() != '.hwp':
        raise ValueError('등록할 .hwp 파일을 선택해 주세요.')
    result = subprocess.run([sys.executable, '-X', 'utf8', str(Path(__file__).resolve()),
                             str(source), str(destination)], capture_output=True,
                            text=True, encoding='utf-8', timeout=50,
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    try:
        reply = json.loads(result.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        raise RuntimeError('한글 양식을 읽지 못했습니다. 설치·권한·보안 모듈을 확인하세요.')
    if result.returncode or not reply.get('ok'):
        raise RuntimeError(reply.get('error', '한글 양식 읽기 실패'))
    return reply['path']


def worker(source, destination):
    import contextlib
    import hashlib
    import shutil
    import tempfile
    from govoffice.adapters.recovered_hwp import 복구한글어댑터
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='govoffice_import_') as temp:
        copied = Path(temp) / 'source.hwp'
        shutil.copy2(source, copied)
        adapter = 복구한글어댑터()
        with contextlib.redirect_stdout(sys.stderr):
            try:
                adapter.관리문서열기(copied, 표시=False)
                xml = adapter.원본.대상.GetTextFile('HWPML2X', '')
                if not xml:
                    raise RuntimeError('한글이 양식 내용을 반환하지 않았습니다.')
                destination.write_text(xml, encoding='utf-8')
            finally:
                if adapter.문서상태().get('managed'):
                    adapter.관리문서닫기(저장여부=False)
    if hashlib.sha256(source.read_bytes()).hexdigest() != before:
        raise RuntimeError('원본 파일 무결성 확인 실패')
    return str(destination)


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    try:
        import tempfile
        from govoffice.adapters.com_worker_cache import configure_worker_cache
        with tempfile.TemporaryDirectory(prefix='govoffice_import_com_') as cache:
            configure_worker_cache(Path(cache)/'gen_py')
            path=worker(*(Path(p) for p in sys.argv[1:3]))
        print(json.dumps({'ok': True, 'path': path}, ensure_ascii=True))
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=True))
        sys.exit(1)
