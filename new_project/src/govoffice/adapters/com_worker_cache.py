"""Give a fresh COM worker its own generated wrappers, not a shared temp cache."""
from pathlib import Path
import sys


def configure_worker_cache(folder):
    # Must precede importing win32com.client and the recovered HWP library.
    # Do not mutate caches/classes in a long-running application process.
    if 'win32com.client' in sys.modules:
        raise RuntimeError('한글 변환 전용 프로세스에서 연결 모듈을 먼저 초기화해야 합니다.')
    import win32com
    folder=Path(folder).resolve()
    folder.mkdir(parents=True,exist_ok=True)
    win32com.__gen_path__=str(folder)
    win32com.gen_py.__path__=[str(folder)]
    # gencache will now build fresh wrappers under this worker's private path.
    # Shared user caches are neither removed nor modified.
    return folder
