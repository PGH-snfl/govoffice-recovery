"""Literal, position-based guide export. No agent, scoring or scope classification."""
from bisect import bisect_right
from pathlib import Path
import re

from .document_authoring import parse_source, write_json
from .template_analysis import source_records
from .template_topic_analysis import extract_candidates


SUBTOPIC = re.compile(r'^\s*\d+(?:[-.]\d+)+(?:[.)]\s*|\s+)(?=[가-힣A-Za-z(（\[])')
NUMBERED = re.compile(r'^\s*\d+[.)]\s*\S')


def extract_source_guides(source_xml, destination, name, cancel=None):
    """Copy recognized source headings/guidance in original paragraph order.

    Source numbering, not an AI verdict, marks topic boundaries. Duplicate
    headings remain separate. Tables spanning several subjects stay where the
    source placed them; their content is never reassigned by meaning.
    """
    def check_cancel():
        if cancel is not None and cancel.is_set():
            raise InterruptedError('작성요령 추출을 중단했습니다.')

    check_cancel()
    root = parse_source(source_xml)
    records = source_records(root)
    _, blocks, _, _ = extract_candidates(root, records)
    table_indices = {p['index'] for b in blocks if b['kind'] == 'table' for p in b['paragraphs']}
    candidates = [dict(index=r['index'], text=r['text']) for r in records
                  if r['index'] not in table_indices and not r['controls']]
    # Prefer the document's explicit subtopic numbering. Retain numbered
    # headings as a fallback for forms that have only one heading level.
    headings = [h for h in candidates if SUBTOPIC.match(h['text'])]
    if not headings:
        headings = [h for h in candidates if NUMBERED.match(h['text'])]
    headings.sort(key=lambda h: h['index'])
    starts = [h['index'] for h in headings]
    sections = [dict(index=h['index'], title=h['text'], instructions=[], subtopics=[])
                for h in headings]
    paragraphs = {p['index']: p['text'] for b in blocks for p in b['paragraphs']}
    before = []
    for index, text in sorted(paragraphs.items()):
        check_cancel()
        item = dict(index=index, text=text)
        position = bisect_right(starts, index) - 1
        (sections[position]['instructions'] if position >= 0 else before).append(item)
    if not paragraphs:
        raise ValueError('원문에서 작성요령 표나 파란 작성 안내를 찾지 못했습니다. 내용은 임의로 만들지 않았습니다.')
    # Preserve unmatched source text without calling it "common guidance".
    displayed = ([dict(index=-1, title='첫 소주제 앞의 작성요령 원문',
                       instructions=before, subtopics=[])] if before else []) + sections
    lines = [f'# {name} — 소주제와 작성요령 원문', '',
             '소주제 번호와 문단 위치 순서로 옮긴 원문입니다. 요약·공통 분류·중요도 판단을 하지 않았습니다.',
             '목차 등에 반복된 제목도 그대로 남습니다. 한 표의 요령은 원문에 놓인 위치를 유지합니다.', '']
    for section in displayed:
        lines += [f"## {section['title']}", '']
        if not section['instructions']:
            lines += ['<!-- 이 제목 아래에서 추출된 작성요령 없음 -->', '']
        for rule in section['instructions']:
            lines += [f"<!-- 원문 문단 P{rule['index']:04d} -->", rule['text'], '']
    audit = {'mode':'source_order_only', 'ai_requests':0, 'headings':headings,
             'source_indices':sorted(paragraphs), 'copied_indices':[
                 r['index'] for s in displayed for r in s['instructions']],
             'before_first_heading':[r['index'] for r in before]}
    if audit['copied_indices'] != audit['source_indices']:
        raise ValueError('작성요령 원문 순서 검사에 실패했습니다.')
    check_cancel()
    destination = Path(destination)
    # A fresh folder avoids overwriting any user's edited export.
    destination.mkdir(parents=True, exist_ok=False)
    filename = destination / '소주제별_작성요령.md'
    filename.write_text('\n'.join(lines), encoding='utf-8')
    write_json(destination/'원문위치.json', audit)
    return {'guide_file':str(filename.resolve()), 'heading_count':len(headings),
            'instruction_count':len(paragraphs), 'ai_requests':0,
            'outline':{'chapters':displayed, 'common_instructions':[], 'unassigned_indices':[]}}
