"""Inspect native memo serialization using an exclusively owned document copy."""
from pathlib import Path
import sys,json,tempfile,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.adapters.com_worker_cache import configure_worker_cache

def main():
    with tempfile.TemporaryDirectory(prefix='govoffice_memo_probe_') as temp:
        configure_worker_cache(Path(temp)/'gen_py')
        from govoffice.adapters.recovered_hwp import 복구한글어댑터
        project=Path(__file__).resolve().parents[2]
        source=project/'config/document_authoring/templates/838b4a1891be475892d49dbee2d07e70/template.hwp'
        working=Path(temp)/'owned.hwp';shutil.copy2(source,working)
        adapter=복구한글어댑터()
        try:
            adapter.관리문서열기(working,표시=False);app=adapter.원본.대상
            app.HAction.Run('MoveDocEnd')
            app.HAction.Run('BreakPara')
            def insert(text):
                app.HAction.GetDefault('InsertText',app.HParameterSet.HInsertText.HSet)
                app.HParameterSet.HInsertText.Text=text
                app.HAction.Execute('InsertText',app.HParameterSet.HInsertText.HSet)
            insert('MEMO_ANCHOR_TEST')
            app.HAction.Run('MoveLineBegin');app.HAction.Run('MoveSelLineEnd')
            ok=app.HAction.Run('InsertFieldMemo')
            insert('확인할 내용: 실제 기관명\r\n확인 방법: 협약서와 대조해 주세요.')
            app.HAction.Run('CloseEx')
            app.HAction.Run('MoveDocEnd');app.HAction.Run('BreakPara')
            insert('SECOND_MEMO_TEST')
            app.HAction.Run('MoveLineBegin');app.HAction.Run('MoveSelLineEnd')
            app.HAction.Run('InsertFieldMemo');insert('두 번째 독립 메모');app.HAction.Run('CloseEx')
            dest=project/'development/artifacts/memo_probe';dest.mkdir(parents=True,exist_ok=True)
            (dest/'native_memo.hml').write_text(app.GetTextFile('HWPML2X',''),encoding='utf-8')
            import xml.etree.ElementTree as ET
            print([n.attrib for n in ET.fromstring(app.GetTextFile('HWPML2X','')).iter('FIELDBEGIN') if n.get('Type')=='Memo'])
            print(json.dumps({'inserted':bool(ok),'xml':str(dest/'native_memo.hml')},ensure_ascii=False))
        finally:
            if adapter.문서상태().get('managed'):adapter.관리문서닫기(저장여부=False)

if __name__=='__main__':main()
