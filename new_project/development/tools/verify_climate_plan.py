"""Read back a generated HWP in an owned instance; render PDF for visual QA."""
from pathlib import Path
import contextlib
import json
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from govoffice.adapters.recovered_hwp import 복구한글어댑터


def main():
    source = Path(sys.argv[1]).resolve()
    dest = Path(sys.argv[2]).resolve()
    dest.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='govoffice_climate_verify_') as work:
        copy = Path(work)/'verify.hwp'
        shutil.copy2(source,copy)
        adapter=복구한글어댑터()
        try:
            adapter.관리문서열기(copy,표시=False)
            app=adapter.원본.대상
            xml=app.GetTextFile('HWPML2X','')
            (dest.parent/'roundtrip.hwpml').write_text(xml,encoding='utf-8')
            pages=int(app.PageCount)
            if not app.SaveAs(str(dest),'PDF',''):
                raise RuntimeError('PDF 미리보기 생성 실패')
            print(json.dumps({'pages':pages,'pdf':str(dest)},ensure_ascii=False))
        finally:
            if adapter.문서상태().get('managed'):
                adapter.관리문서닫기(저장여부=False)


if __name__=='__main__': main()
