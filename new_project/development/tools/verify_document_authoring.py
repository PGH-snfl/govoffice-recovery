"""Explicit smoke test: one synthetic topic may call Codex; others are test markers.

Never a real application. Output is confined to reports/runtime, not user jobs.
"""
import argparse
import json
from pathlib import Path
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'src'))
from govoffice.services.document_authoring import AuthoringService, read_json
from govoffice.institutions.packages.seoultech.climate_2026.authoring import register_climate
from govoffice.adapters.codex_author import CodexAuthor
from govoffice.adapters.hwp_form_export import export_generated_hwp


class ProbeAgent:
    def __init__(self, folder, live=False, all_live=False):
        self.folder = folder
        self.live = live
        self.all_live = all_live
        self.connection = None
        self.calls = 0
        self.real_calls = 0

    def generate(self, prompt, schema, cancel):
        self.calls += 1
        topic = schema['properties']['topic_id']['enum'][0]
        if self.all_live or self.live and topic.endswith('p0657'):
            if self.connection is None:
                self.connection = CodexAuthor(self.folder)
            result = self.connection.generate(prompt, schema, cancel)
            self.real_calls += 1
            return result
        manifest = read_json(self.folder/'template/manifest.json')
        fields = next(t['fields'] for t in manifest['topics'] if t['id'] == topic)
        return {'topic_id': topic,
                'values': {f['id']: ('?' if f.get('kind') == 'schedule_marker' else '시험 입력 ' + f['id']) for f in fields},
                'needs_review': ['자동화 연결 검증용 모의 응답입니다. 제출 내용이 아닙니다.']}

    def close(self):
        if self.connection:
            self.connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', action='store_true', help='Actually save and read back a new owned HWP')
    parser.add_argument('--agent', action='store_true', help='Send one synthetic-topic prompt to logged-in Codex')
    parser.add_argument('--all-agent', action='store_true', help='Send every synthetic topic to logged-in Codex')
    args = parser.parse_args()
    if not args.native:
        parser.error('This integration probe requires --native. Offline tests are in test_document_authoring.py.')
    base = ROOT/'development/reports/runtime/authoring_validation'
    agents = []
    def factory(folder):
        agent = ProbeAgent(folder, args.agent, args.all_agent)
        agents.append(agent)
        return agent
    service = AuthoringService(base, factory, export_generated_hwp)
    m = register_climate(service.registry)
    job = service.create(m['id'], {
        'title': '문서 자동작성 연결 검증용 가상 과제 — 제출 금지',
        'description': '가상 과제로 대학 연구실의 실험 예약 현황을 정리하는 소프트웨어의 개요를 작성한다. 실제 연구 실적·예산·인물 정보는 없으며 추정하지 않는다.',
        'facts': '연결 시험이다. 기간·예산·참여기관 미확정.',
        'references': '외부 자료 없음. 근거가 없으면 확인 필요로 남긴다.'},
        reviewed=True, external_consent=True)
    try:
        service.start(job['id'])
        last = None
        while service.workers[job['id']].is_alive():
            state = service.status(job['id'])
            current = (state['status'], len(state['completed']))
            if current != last:
                print(json.dumps({'status': current[0], 'completed': current[1], 'topic': state['current_topic']}, ensure_ascii=True), flush=True)
                last = current
            service.workers[job['id']].join(timeout=.5)
        state = service.status(job['id'])
        print(json.dumps({'status':state['status'], 'error':state['error'], 'hwp_path':state['hwp_path'],
                          'real_agent_topics':sum(a.real_calls for a in agents),
                          'completed_topics':len(state['completed']), 'native':state.get('native'),
                          'output_dir':state['output_dir'], 'test_only':True}, ensure_ascii=True), flush=True)
        return state['status'] == 'completed'
    finally:
        service.close()


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
