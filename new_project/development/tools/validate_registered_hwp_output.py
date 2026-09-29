"""Round-trip a locally registered form through an isolated Hancom instance."""
import json
from pathlib import Path
import re
import sys

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))

from govoffice.adapters.hwp_form_export import export_generated_hwp
from govoffice.services.document_authoring import TemplateRegistry,render_draft


def main():
    report_name=sys.argv[1] if len(sys.argv)>1 else 'input_slot_registration_2026-09-28'
    if not re.fullmatch(r'input_slot_(?:registration|recheck)_[a-zA-Z0-9_-]+',report_name):
        raise ValueError('잘못된 검증 보고서 폴더 이름입니다.')
    report_dir=PROJECT/'development/reports'/report_name
    report_file=report_dir/'verification.json'
    report=json.loads(report_file.read_text(encoding='utf-8'))
    registry=TemplateRegistry(report_dir/'templates')
    manifest=registry.load(report['template_id'])
    folder=registry.path(report['template_id'])
    field=next(f for topic in manifest['topics'] for f in topic['fields']
               if f['id']==report['sample_written_field'])
    xml,field_log=render_draft(folder,manifest,{},local_values={field['id']:'검증'})
    hml=report_dir/'검증출력.hml'
    hml.write_text(xml,encoding='utf-8')
    (report_dir/'입력필드.json').write_text(json.dumps(field_log,ensure_ascii=False,indent=2),encoding='utf-8')
    destination=report_dir/'검증출력.hwp'
    if destination.exists():destination=report_dir/f"검증출력_{manifest['id'][:8]}.hwp"
    native=export_generated_hwp(folder/'template.hwp',hml,destination)
    report['native_hwp']={'path':str(destination),'verification':native}
    report_file.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report['native_hwp'],ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
