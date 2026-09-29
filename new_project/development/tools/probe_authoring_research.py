"""Opt-in live public-topic probe. Uses the existing login, never logs credentials."""
import json
from pathlib import Path
import sys
import tempfile
import threading

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.adapters.codex_author import CodexAuthor
from govoffice.services.authoring_research import make_research_prompt, research_schema, validate_research, research_markdown
from govoffice.services.document_authoring import make_prompt, response_schema, validate_result


def main():
    output=Path(__file__).resolve().parents[1]/'reports/research_live_example_2026-09-15'
    output.mkdir(exist_ok=True)
    topic={'id':'public-example','title':'1. 도시 열섬 완화 조사와 실행 방안','guide':'topic.md',
           'fields':[{'id':'body','context':'공개 근거와 실행 방안','max_chars':1800}]}
    manifest={'title':'공개 자료 조사 예제','topics':[topic],'common_guide':'common.md','review':[]}
    brief={'title':'도시 열섬 완화 조사 예제',
           'description':'공공시설 주변 그늘과 녹지의 효과를 공식 공개 자료로 확인하고 소규모 비교 관측 계획을 제안한다. '
                         '실제 과제가 아닌 시험이다. 공식 출처 2개 정도와 짧은 조사 결과면 충분하다.'}
    cancel=threading.Event()
    with tempfile.TemporaryDirectory(prefix='govoffice_public_research_') as directory:
        folder=Path(directory)
        (folder/'common.md').write_text('공개 근거에 따른 사실과 새롭게 제안하는 계획을 구분한다.',encoding='utf-8')
        (folder/'topic.md').write_text('공공기관 원문에서 그늘·녹지의 효과와 적용 한계를 확인하고, 비교 관측 절차 및 평가 지표를 제안한다.',encoding='utf-8')
        agent=CodexAuthor(folder)
        try:
            prompt=make_research_prompt(folder,manifest,topic,brief,[])
            research=validate_research(topic,agent.research(prompt,research_schema(topic),cancel,
                on_progress=lambda phase,count:print(f'{phase}: {count}',flush=True)))
            trace=list(agent.last_research_trace)
            (output/'research.json').write_text(json.dumps({'result':research,'web_trace':trace},ensure_ascii=False,indent=2),encoding='utf-8')
            (output/'자료조사_근거.md').write_text(research_markdown(topic,research),encoding='utf-8')
            print('조사 완료. 동일 근거를 본문 작성 요청에 전달합니다.',flush=True)
            writing=validate_result(topic,agent.generate(make_prompt(folder,manifest,topic,brief,{},research),response_schema(topic),cancel))
            (output/'writing.json').write_text(json.dumps(writing,ensure_ascii=False,indent=2),encoding='utf-8')
            (output/'작성결과.md').write_text('# 공개 주제 실제 AI 작성 예제\n\n'+writing['values']['body']+'\n\n## 확인 사항\n'+'\n'.join('- '+x for x in writing['needs_review']),encoding='utf-8')
            print(json.dumps({'research_web_actions':len(trace),'sources':len(research['sources']),
                              'received_characters':len(writing['values']['body']),'native_hwp_tested':False},ensure_ascii=False),flush=True)
        finally:
            agent.close()


if __name__=='__main__': main()
