"""Minimal, source-bound chapter/subtopic/guidance tree; no field analysis data."""
from copy import deepcopy


def guide_outline(decisions):
    headings={r['index']:r for r in decisions if r['role']=='heading' and not r['uncertain']}
    nodes={i:dict(index=i,title=r['topic'] or r['label'],instructions=[],subtopics=[]) for i,r in headings.items()}
    roots=[];common=[];unassigned=[]
    for i,row in headings.items():
        parent=row.get('chapter_anchor',i)
        if parent==i:roots.append(nodes[i])
        elif parent in nodes:nodes[parent]['subtopics'].append(nodes[i])
        else:unassigned.append(i)
    for row in decisions:
        if row['role'] not in {'guide','heading'} or row['uncertain'] or not row.get('instruction_text'):continue
        instruction={'index':row['index'],'text':row['instruction_text']}
        if row['scope']=='common':common.append(instruction);continue
        targets=row.get('topic_anchors') or [row['topic_anchor']]
        for i in targets:
            if i not in nodes:unassigned.append(row['index']);continue
            nodes[i]['instructions'].append(deepcopy(instruction))
    # Keep source order, and identify headings by position, never by their names.
    for node in nodes.values():
        node['instructions'].sort(key=lambda r:r['index'])
        node['subtopics'].sort(key=lambda r:r['index'])
    return {'chapters':sorted(roots,key=lambda r:r['index']),
            'common_instructions':sorted(common,key=lambda r:r['index']),
            'unassigned_indices':sorted(set(unassigned))}


def apply_guide_outline(manifest,decisions):
    """Derive writing instructions from the same tree, avoiding cross-topic leaks."""
    outline=guide_outline(decisions);effective={}
    for chapter in outline['chapters']:
        effective[chapter['index']]=chapter['instructions']
        for child in chapter['subtopics']:
            # A chapter-wide rule applies to this chapter's children only.
            combined={r['index']:r for r in chapter['instructions']+child['instructions']}
            effective[child['index']]=[combined[i] for i in sorted(combined)]
    for topic in manifest['topics']:
        topic['instructions']=deepcopy(effective.get(topic['start'],[])) if topic['id']!='sfront' else []
    manifest['common_instructions']=deepcopy(outline['common_instructions'])
    manifest['guide_outline']=outline
    if outline['unassigned_indices']:
        manifest['requires_review']=True
        manifest['notes'].append('주제 계층에 연결되지 않은 요령·제목은 원문을 보존하며 자동 작성에서 제외합니다.')
    return outline
