"""Opt-in live AI mapping probe on a synthetic form; no native HWP export."""
from pathlib import Path
import sys
import tempfile
import threading
import json
import argparse
import time
sys.path[:0]=[str(Path(__file__).resolve().parents[2]/'src'),str(Path(__file__).resolve().parents[1]/'tests')]
from test_template_analysis import SOURCE
from govoffice.adapters.codex_author import CodexAuthor
from govoffice.services.document_authoring import TemplateRegistry,read_json
from govoffice.services.template_analysis import register_analyzed


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report-name',default='template_topic_analysis_live_example')
    parser.add_argument('--hierarchy',action='store_true')
    args=parser.parse_args()
    if Path(args.report_name).name!=args.report_name:raise ValueError('보고서 폴더 이름만 입력하세요.')
    output=Path(__file__).resolve().parents[1]/'reports'/args.report_name
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='govoffice_analysis_probe_') as temp:
        source=SOURCE
        if args.hierarchy:
            from test_template_guide_outline import FORM
            source=FORM.replace('전체 공통 규칙','전체 공통 규칙: 모든 주제는 공개 근거를 사용하세요.').replace(
                '첫 대주제 규칙','1. 첫 대주제 아래의 모든 소주제는 현황을 설명하세요.').replace(
                '소주제 A 전용','1-1. 같은 이름 항목에만 적용: 국내 현황을 작성하세요.').replace(
                '소주제 B 전용','1-2. 같은 이름 항목에만 적용: 해외 현황을 작성하세요.').replace(
                '다른 대주제 전용','2-1. 같은 이름 항목에만 적용: 실행 방안을 작성하세요.')
        folder=Path(temp);xml=folder/'source.hwpml';xml.write_text(source,encoding='utf-8')
        native=folder/'source.hwp';native.write_bytes(b'SYNTHETIC PLACEHOLDER - NOT A NATIVE HWP FILE')
        registry=TemplateRegistry(folder/'templates');agent=CodexAuthor(folder)
        responses=[];original_generate=agent.generate
        def recorded_generate(prompt,schema,cancel):
            result=original_generate(prompt,schema,cancel);responses.append(result);return result
        agent.generate=recorded_generate
        try:
            started=time.monotonic()
            m=register_analyzed(registry,xml,native,'가상 사업 신청서',agent,threading.Event(),
                lambda phase,done,total:print(phase,flush=True))
            analysis=read_json(registry.path(m['id'])/m['analysis_file'])
            report={'native_hwp_tested':False,'elapsed_seconds':round(time.monotonic()-started,2),'manifest':m,'analysis':analysis,'responses':responses}
            (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps({'elapsed_seconds':report['elapsed_seconds'],'ai_requests':m.get('ai_analysis_requests'),
                'roles':{r:sum(d['role']==r for d in analysis['decisions']) for r in ['body','personal','guide','heading','preserve','review']},
                'guide_markdown_created':bool(list(registry.path(m['id']).rglob('*.md')))},ensure_ascii=False),flush=True)
        finally:agent.close()


if __name__=='__main__':main()
