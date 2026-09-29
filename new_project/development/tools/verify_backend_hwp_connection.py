"""Exercise the real desktop backend with an owned copy and isolated test data."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def verify(source):
    project=Path(__file__).resolve().parents[2]
    source=Path(source).resolve(strict=True)
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='govoffice_connection_probe_') as temp:
        copied=Path(temp)/'owned_connection_test.hwp';shutil.copy2(source,copied)
        env=os.environ.copy();env['GOVOFFICE_DATA_DIR']=str(Path(temp)/'data')
        commands=[{'action':'hwp_document_open','path':str(copied),'visible':False},
                  {'action':'hwp_document_status'},
                  {'action':'hwp_document_close','save_changes':False},
                  {'action':'shutdown'}]
        result=subprocess.run([sys.executable,'-X','utf8',str(project/'gui_backend.py')],
            input=''.join(json.dumps(c,ensure_ascii=True)+'\n' for c in commands),
            cwd=project.parent,env=env,encoding='utf-8',capture_output=True,timeout=45,
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        replies=[json.loads(line) for line in result.stdout.splitlines()]
        assert len(replies)==5,(replies,result.stderr)
        assert result.returncode==0 and all(r['ok'] for r in replies),(replies,result.stderr)
        assert replies[2]['document']['managed'],replies[2]
        assert hashlib.sha256(source.read_bytes()).hexdigest()==before
        assert hashlib.sha256(copied.read_bytes()).hexdigest()==before
        print(json.dumps({'ok':True,'real_backend_open_status_close':True,'source_unchanged':True,
                          'messages':[r['message'] for r in replies]},ensure_ascii=False))


if __name__=='__main__':verify(sys.argv[1])
