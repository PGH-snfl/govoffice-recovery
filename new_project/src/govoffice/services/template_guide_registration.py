"""AI extracts only headings/guides; local code binds safe writing placeholders."""
from bisect import bisect_right
from collections import Counter
from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import xml.etree.ElementTree as ET
from uuid import uuid4
import re

from .ai_guide_export import export_ai_guides
from .authoring_inputs import blank_candidates
from .document_authoring import digest, parse_source, read_json, write_json
from .template_analysis import build_manifest, fallback_row, source_records
from .template_topic_analysis import PERSONAL, PROSE, normalized
from .numbered_topics import flatten
from .ai_input_slots import (analyze_input_slots, collect_slot_candidates,
                             reanalyze_saved_input_slots)
from .document_authoring import replace_text


def bind_local_slots(root, outline, slot_decisions=None):
    records=source_records(root);ps=list(root.iter('P'));tables=list(root.iter('TABLE'))
    parents={id(c):p for p in root.iter() for c in p}
    sections={s['index']:s for s in flatten(outline['chapters']) if s['index'] is not None};anchors=sorted(sections)
    guide_ids={r['index'] for s in sections.values() for r in s['instructions']}
    guide_ids.update(outline.get('unassigned_indices',[]))
    excluded=guide_ids|set(anchors)
    ai_slots={x['index']:x for x in (slot_decisions or [])}
    # Empty spacing inside a dedicated writing-instructions table is not a body
    # slot. Never exclude an entire mixed table that also contains a heading.
    indices={id(p):i for i,p in enumerate(ps)}
    for table in root.iter('TABLE'):
        ids={indices[id(p)] for p in table.iter('P')}
        if not ids.intersection(anchors) and any(normalized(records[i]['text'])=='작성요령' for i in ids):
            excluded.update(ids)
    blanks=blank_candidates(root,ps,excluded)
    personal={normalized(x) for x in PERSONAL}
    rows=[fallback_row(r,'원본 보존','preserve') for r in records]
    for index,section in sections.items():
        rows[index].update(role='heading',topic_anchor=index,topic=section['title'],
                           chapter=section['title'],label=section['title'])
    for r in records:
        i=r['index'];text=r['text'].strip()
        if i in excluded or not r['writable']:continue
        decision=ai_slots.get(i)
        if decision is not None:
            # AI classification is authoritative for explicitly analyzed blanks:
            # uncertain/decorative blanks must not fall through to old heuristics.
            if decision['confidence']!='high' or decision['role']=='preserve':continue
            label=decision['label'].strip() or r['label_hint'].strip()
            row=rows[i]
            if decision['role']=='personal':
                row.update(role='personal',topic_anchor=-1,topic='기본정보',chapter='기본정보',
                           label=label or '개인정보')
            else:
                anchor=decision['topic_index']
                section=sections.get(anchor)
                title=section['title'] if section else '표지·과제 기본정보'
                row.update(role='body',topic_anchor=anchor,topic=title,
                           chapter=title,label=label or title,
                           guide_ids=[g['index'] for g in section['instructions']] if section else [])
                if decision['role']=='factual':row['kind']='factual_cell'
            continue
        if slot_decisions is not None and (not text or re.fullmatch(r'(?:[_＿]{2,}|\[\s*\]|\(\s*\)|□+|○+|ㅇ+|o+|·+|⋅+|-+)',text,re.I)):
            # AI did not return an explicit candidate decision: preserve rather
            # than reclassifying a blank through the legacy positional heuristic.
            continue
        pos=bisect_right(anchors,i)-1;anchor=anchors[pos] if pos>=0 else None
        explicit=i in blanks or text in {'o','ㅇ','○','-','⋅','·'}
        # A blank paragraph directly under a title in the same text container
        # is a usable slot, including a title and body within one table cell.
        same_container=anchor is not None and parents.get(id(ps[i])) is parents.get(id(ps[anchor]))
        direct_blank=(not text and same_container and all(
            j in guide_ids or (records[j]['writable'] and not records[j]['text'].strip())
            for j in range(anchor+1,i)))
        if not explicit and not direct_blank:continue
        parent=parents.get(id(ps[i]))
        if not text and parent is not None and parent.tag=='PARALIST':
            # Do not overwrite padding in a cell that contains fixed data.
            fixed=[indices[id(p)] for p in parent.findall('P')
                   if records[indices[id(p)]]['text'].strip() and indices[id(p)] not in excluded]
            if fixed:continue
        label=r['label_hint'].strip()
        if r['table'] is not None and re.search('서명|직인|날인|인감',label):continue
        single_prose_cell=(r['table'] is not None and anchor is not None and not label
                           and len(tables[r['table']].findall('ROW/CELL'))==1
                           and PROSE.search(sections[anchor]['title']))
        row=rows[i]
        if normalized(label) in personal:
            row.update(role='personal',topic_anchor=-1,topic='기본정보',chapter='기본정보',label=label)
        elif anchor is not None and (r['table'] is None or same_container or single_prose_cell or PROSE.search(label)
                                    or (r['table'] is not None and label and not re.search('서명|직인|날인|인감',label))
                                    or normalized(label)==normalized(sections[anchor]['title'])):
            # In unrelated budget/signature/numeric cells, an empty value alone
            # does not authorize prose. Leave those cells unchanged.
            row.update(role='body',topic_anchor=anchor,topic=sections[anchor]['title'],
                       chapter=sections[anchor]['title'],label=sections[anchor]['title'],
                       guide_ids=[g['index'] for g in sections[anchor]['instructions']])
    manifest=build_manifest('pending','pending',records,rows,'','')
    factual_indices={i for i,decision in ai_slots.items()
                     if decision['role']=='factual' and decision['confidence']=='high'}
    for topic in manifest['topics']:
        topic['instructions']=deepcopy(sections[topic['start']]['instructions']) if topic['id']!='sfront' else []
        for field in topic['fields']:
            if field['index'] in factual_indices:
                field.update(role='factual',kind='factual_cell',allow_empty=True,
                             multiline=False,max_chars=180)
                continue
            if field['role']=='body':
                field['multiline']=True
                field['max_chars']=800 if field['in_table'] else 3000
                decision=ai_slots.get(field['index'])
                # For a sample-filled cell, the reviewed semantic label is more
                # useful than the previous cell's text (often another sample).
                label=(decision.get('label','').strip() if decision and records[field['index']]['text'].strip()
                       else records[field['index']]['label_hint'])
                if label:field['label']=label;field['context']=label
                if re.search('금액|예산|수량|날짜|기간|실적|인원|비율',label):field['kind']='factual_cell'
    by_index={t['start']:t for t in manifest['topics'] if t['id']!='sfront'}
    def assign(nodes,ancestors=(),group=None):
        for node in nodes:
            current=by_index.get(node['index'])
            next_group=group
            if current:
                if group is None or len(ancestors)==1:next_group=current['id']
                current['research_group']=next_group
                current['instructions']=deepcopy([g for a in ancestors for g in a['instructions']]+node['instructions'])
                current['topic_path']=[a['title'] for a in ancestors]+[node['title']]
                # A leaf heading without a slot receives a new body paragraph,
                # never replacement text in the heading itself.
                if (not current['fields'] and not node.get('subtopics') and records[node['index']]['writable']
                        and (PROSE.search(node['title']) or re.search('서론|결론|논의|초록|고찰|문헌 검토',node['title']))):
                    current['fields']=[{'id':f"P{node['index']:04d}",'index':node['index'],
                        'original':records[node['index']]['text'],'insert_after':True,
                        'role':'body','label':node['title'],'context':node['title'],
                        'in_table':records[node['index']]['table'] is not None,'max_chars':3000,
                        'allow_empty':False,'multiline':True}]
            assign(node.get('subtopics',[]),(*ancestors,node),next_group)
    assign(outline['chapters'])
    manifest['render_policy']={'readable_body':True,'blue_review':True,'preserve_layout':True}
    manifest['research_policy']={'mode':'minimal','max_groups':3}
    manifest['guide_outline']=deepcopy(outline)
    manifest['common_instructions']=[]  # Unattached is not automatically common.
    manifest['unassigned_instructions']=[{'index':i,'text':records[i]['text']}
                                         for i in outline.get('unassigned_indices',[])]
    # Only the generated copy clears confirmed, separate instruction text.
    # Preserve headings, complex controls and unassigned notes; source stays intact.
    assigned={g['index'] for s in sections.values() for g in s['instructions']}
    manifest['clear_guide_indices']=sorted(i for i in assigned if i not in sections and records[i]['writable'])
    manifest['registration_mode']='guides_then_research_and_write'
    manifest['analysis_mode']='ai_guides_local_slots'
    leaf_starts={n['index'] for n in flatten(outline['chapters'])
                 if n.get('index') is not None and not n.get('subtopics')}
    manifest['manual_topics']=[t['title'] for t in manifest['topics']
                               if not t['fields'] and t['start'] in leaf_starts]
    if manifest['manual_topics']:
        manifest['notes'].append('일부 소주제는 안전한 본문 입력 위치가 없어 원본을 유지합니다: '+', '.join(manifest['manual_topics']))
    if manifest['unassigned_instructions']:
        manifest['notes'].append('소주제에 연결되지 않은 작성요령은 MD 파일에 별도 보존했습니다. 전체 공통 요령으로 임의 적용하지 않습니다.')
    from .authoring_design_fields import remove_decorative_fields
    remove_decorative_fields(root,manifest)
    return manifest


def mark_confirmed_slots(root, manifest):
    """Replace only AI-confirmed input slots with stable, style-preserving tokens."""
    from .authoring_design_fields import safe_writing_manifest
    routed=safe_writing_manifest(root,manifest)
    targets={f['id']:f for topic in routed['topics'] for f in topic['fields']}
    ps=list(root.iter('P'));marked=[]
    for topic in manifest['topics']:
        for field in topic['fields']:
            if field.get('write_blocked') or field.get('insert_after'):continue
            target=targets[field['id']]
            if target.get('write_blocked') or target.get('insert_after') or target['index']!=field['index']:
                continue
            index=field['index']
            marker=f'〔P{index:04d}〕'
            if index<0 or index>=len(ps):raise ValueError('AI가 지정한 입력 위치가 원문 범위를 벗어났습니다.')
            replace_text(ps[index],marker)
            field['original']=marker
            field['slot_marker']=marker
            marked.append(index)
    if len(marked)!=len(set(marked)):
        raise ValueError('서로 다른 입력항목이 같은 원문 위치를 가리킵니다.')
    return marked


def guided_review_items(root, outline, slots):
    candidates={x['index']:x for x in collect_slot_candidates(root,outline)}
    reviews=[]
    for row in slots:
        if row['confidence']=='high':continue
        candidate=candidates.get(row['index'])
        if candidate is None:continue
        section=candidate.get('section') or {}
        context=candidate['table_context']
        labels=list(dict.fromkeys(context['row_labels']+context['column_labels']))
        reviews.append({'index':row['index'],'text':candidate['text'],
            'label':row['label'] or candidate['label_hint'] or section.get('title',''),
            'reason':row['reason'],'writable':True,
            'section':section.get('title','양식 앞부분'),
            'topic_index':section.get('index') if isinstance(section.get('index'),int) else -1,
            'table_index':candidate['table_index'],
            'context':' · '.join(labels[:4])})
    return sorted(reviews,key=lambda x:x['index'])


def partition_guided_reviews(manifest, reviews):
    """A safe insert-after body already covers ambiguous following spacers."""
    topics={t['start']:t for t in manifest['topics'] if t['id']!='sfront'}
    actionable=[];covered=[]
    for review in reviews:
        topic=topics.get(review['topic_index'])
        inserted=(topic is not None and any(f['index']==topic['start']
            and f.get('insert_after') and f['role']=='body' and not f.get('write_blocked')
            for f in topic['fields']))
        if review['table_index'] is None and inserted and review['index']>topic['start']:
            covered.append(review['index'])
        else:actionable.append(review)
    return actionable,covered


def registered_guided_reviews(registry, manifest):
    if manifest.get('registration_mode')!='guides_then_research_and_write':return []
    if 'analysis_reviews' in manifest:
        return partition_guided_reviews(manifest,manifest['analysis_reviews'])[0]
    if not manifest.get('input_slot_audit_file'):return []
    folder=registry.path(manifest['id'])
    audit=read_json(folder/manifest['input_slot_audit_file'])
    root=parse_source(folder/'source_original.hwpml')
    reviews=guided_review_items(root,manifest['guide_outline'],audit['slots'])
    return partition_guided_reviews(manifest,reviews)[0]


def _finish_guided_bundle(folder, name, template_id, outline, slot_result, ai_requests,
                          parent_template_id=None):
    original_root=parse_source(folder/'source_original.hwpml')
    all_reviews=guided_review_items(original_root,outline,slot_result['slots'])
    manifest=bind_local_slots(original_root,outline,slot_result['slots'])
    if not any(f['role']=='body' for t in manifest['topics'] for f in t['fields']):
        raise ValueError('소주제와 작성요령은 찾았지만 안전한 본문 작성 위치가 없습니다. 개인정보만 채우는 양식으로 등록하지 않았습니다.')
    reviews,covered=partition_guided_reviews(manifest,all_reviews)
    mark_confirmed_slots(original_root,manifest)
    (folder/'source.hwpml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+
        ET.tostring(original_root,encoding='unicode'),encoding='utf-8')
    slot_audit=slot_result['audit']
    slot_audit={**slot_audit,'covered_by_insert_after_indices':covered,
                'user_review_indices':[r['index'] for r in reviews]}
    unresolved=len(all_reviews)
    if unresolved:
        manifest['notes'].append(f'AI 판정이 불확실한 빈 입력 후보 {unresolved}곳은 자동 입력 대상으로 지정하지 않고 원문 그대로 보존했습니다.')
    manifest.update(id=template_id,name=name,source_sha256=digest(folder/'source.hwpml'),
                    original_source_sha256=digest(folder/'source_original.hwpml'),
                    native_sha256=digest(folder/'template.hwp'),
                    ai_analysis_requests=ai_requests,
                    input_slot_analysis=slot_audit,
                    input_slot_audit_file='입력칸판정.json',
                    analysis_reviews=reviews,requires_review=bool(reviews),
                    covered_review_indices=covered,
                    analysis_status='partial' if manifest['manual_topics'] or manifest['unassigned_instructions'] or reviews else 'completed',
                    guide_file='guides/소주제별_작성요령.md')
    if parent_template_id:manifest['derived_from_template_id']=parent_template_id
    manifest.pop('analysis_file',None)
    from .template_layout_store import save_layout_database,stored_writing_manifest
    saved_root=parse_source(folder/'source.hwpml')
    save_layout_database(folder,saved_root,manifest,
                         classification_root=parse_source(folder/'source_original.hwpml'))
    effective=stored_writing_manifest(folder,saved_root,manifest)
    effective_fields={f['id']:f for t in effective['topics'] for f in t['fields']}
    for topic in manifest['topics']:
        for field in topic['fields']:
            if not field.get('slot_marker'):continue
            target=effective_fields[field['id']]
            if (target.get('write_blocked') or target.get('insert_after')
                    or target['index']!=field['index']):
                raise ValueError('빈칸 표식의 실제 저장 위치가 바뀌었습니다: '+field['id'])
    write_json(folder/'manifest.json',manifest)
    write_json(folder/'입력위치.json',{t['id']:t['fields'] for t in manifest['topics']})
    write_json(folder/'입력칸판정.json',{'audit':slot_audit,
        'slots':[{k:x[k] for k in ('index','role','topic_index','label','confidence','reason')}
                 for x in slot_result['slots']]})
    return manifest


def register_guided(registry, source_xml, native, name, agent, cancel, progress):
    if cancel.is_set():raise InterruptedError('양식 등록을 중단했습니다.')
    template_id=uuid4().hex
    with tempfile.TemporaryDirectory(prefix='.guided-',dir=registry.folder) as temporary:
        folder=Path(temporary)/'bundle';folder.mkdir()
        shutil.copy2(source_xml,folder/'source_original.hwpml')
        shutil.copy2(source_xml,folder/'source.hwpml');shutil.copy2(native,folder/'template.hwp')
        result=export_ai_guides(folder/'source_original.hwpml',folder/'guides',name,agent,cancel,progress)
        original_root=parse_source(folder/'source_original.hwpml')
        progress('AI가 빈 입력 후보의 의미와 표 문맥을 확인하는 중',0,1)
        slot_result=analyze_input_slots(original_root,result['outline'],agent,cancel,progress)
        progress('판정된 입력 후보를 주제별 작성 위치에 연결하는 중',0,1)
        manifest=_finish_guided_bundle(folder,name,template_id,result['outline'],slot_result,
                                       result['ai_requests']+slot_result['ai_requests'])
        if digest(source_xml)!=manifest['original_source_sha256'] or digest(native)!=manifest['native_sha256']:
            raise ValueError('등록 도중 원본 양식이 변경되었습니다.')
        if cancel.is_set():raise InterruptedError('양식 등록을 중단했습니다.')
        folder.rename(registry.path(template_id))
    progress('양식 등록 완료 · 작성 내용을 입력하면 자료조사와 본문 작성을 시작합니다.',1,1)
    # Relative path stays portable in storage; the UI gets an actionable path.
    return {**manifest,'guide_file':str((registry.path(template_id)/manifest['guide_file']).resolve())}


def resolve_guided_reviews(registry, template_id, choices):
    """Publish a reviewed copy; leave the source registration and jobs intact."""
    manifest=registry.load(template_id)
    if manifest.get('registration_mode')!='guides_then_research_and_write':
        raise ValueError('입력칸 확인 대상 양식이 아닙니다.')
    if not isinstance(choices,dict) or not choices:
        raise ValueError('적용할 확인 항목을 선택해 주세요.')
    if not manifest.get('input_slot_audit_file'):
        raise ValueError('이 양식에는 입력칸 판정 기록이 없어 확인 항목을 변경할 수 없습니다. 다시 연결해 주세요.')
    source=registry.path(template_id)
    audit=read_json(source/manifest['input_slot_audit_file'])
    pending={r['index']:r for r in registered_guided_reviews(registry,manifest)}
    slots={r['index']:dict(r) for r in audit['slots']}
    for key,role in choices.items():
        try:i=int(key)
        except (TypeError,ValueError):raise ValueError('확인 항목 위치가 올바르지 않습니다.') from None
        if str(i)!=str(key) or i not in pending or role not in {'body','factual','personal','preserve'}:
            raise ValueError('허용되지 않은 확인 항목입니다.')
        topic=pending[i]['topic_index'] if role in {'body','factual'} else -1
        if role=='body' and topic not in {x['index'] for x in flatten(manifest['guide_outline']['chapters'])}:
            raise ValueError(f'문단 {i}의 작성 주제를 확인할 수 없어 본문 입력칸으로 지정하지 않았습니다.')
        slots[i].update(role=role,topic_index=topic,confidence='high',
                        label=pending[i]['label'],reason='사용자가 입력칸 용도를 확인했습니다.')
    rows=[slots[i] for i in sorted(slots)]
    counts=Counter(x['role'] if x['confidence']=='high' else 'review' for x in rows)
    updated_audit={**audit['audit'],'role_counts':dict(counts),
                   'review_indices':[x['index'] for x in rows if x['confidence']!='high'],
                   'user_resolved_count':audit['audit'].get('user_resolved_count',0)+len(choices)}
    new_id=uuid4().hex
    name=manifest['name'] if manifest['name'].endswith(' · 확인 반영') else manifest['name']+' · 확인 반영'
    with tempfile.TemporaryDirectory(prefix='.guided-review-',dir=registry.folder) as temporary:
        folder=Path(temporary)/'bundle';folder.mkdir()
        shutil.copy2(source/'source_original.hwpml',folder/'source_original.hwpml')
        shutil.copy2(source/'template.hwp',folder/'template.hwp')
        shutil.copytree(source/'guides',folder/'guides')
        updated=_finish_guided_bundle(folder,name,new_id,manifest['guide_outline'],
            {'slots':rows,'audit':updated_audit},manifest.get('ai_analysis_requests',0),template_id)
        if (updated['original_source_sha256']!=manifest['original_source_sha256']
                or updated['native_sha256']!=manifest['native_sha256']):
            raise ValueError('입력칸 확인 중 원본 양식이 변경되었습니다.')
        folder.rename(registry.path(new_id))
    return {**updated,'guide_file':str((registry.path(new_id)/updated['guide_file']).resolve())}


def recheck_registered_guided(registry, template_id, agent, cancel, progress):
    """Retry only uncertain slots from a saved form; no HWP re-extraction."""
    manifest=registry.load(template_id)
    if manifest.get('registration_mode')!='guides_then_research_and_write' or not manifest.get('input_slot_audit_file'):
        raise ValueError('저장된 입력칸 판정 기록이 없어 전체 양식 다시 연결이 필요합니다.')
    old=registry.path(template_id)
    saved=read_json(old/manifest['input_slot_audit_file'])
    original=parse_source(old/'source_original.hwpml')
    progress('저장된 확정 판정을 유지하고 불확실한 칸만 재검토하는 중',0,1)
    result=reanalyze_saved_input_slots(original,manifest['guide_outline'],saved['slots'],
                                       agent,cancel,progress)
    old_indices={x['index'] for x in saved['slots']}
    previously={x['index'] for x in saved['slots'] if x['confidence']!='high'}
    resolved={x['index'] for x in result['slots'] if x['index'] in previously and x['confidence']=='high'}
    added={x['index'] for x in result['slots'] if x['index'] not in old_indices
           and x['confidence']=='high' and x['role']!='preserve'}
    if not resolved and not added:
        return {**manifest,'analysis_reviews':registered_guided_reviews(registry,manifest),
                'recheck_no_change':True,'recheck_ai_requests':result['ai_requests'],
                'guide_file':str((old/manifest['guide_file']).resolve())}
    if cancel.is_set():raise InterruptedError('빈 입력칸 재검토를 중단했습니다.')
    new_id=uuid4().hex
    with tempfile.TemporaryDirectory(prefix='.guided-recheck-',dir=registry.folder) as temporary:
        folder=Path(temporary)/'bundle';folder.mkdir()
        shutil.copy2(old/'source_original.hwpml',folder/'source_original.hwpml')
        shutil.copy2(old/'template.hwp',folder/'template.hwp')
        shutil.copytree(old/'guides',folder/'guides')
        name=(manifest['name'] if manifest['name'].endswith(' · 입력칸 재검토')
              else manifest['name']+' · 입력칸 재검토')
        updated=_finish_guided_bundle(folder,name,new_id,
            manifest['guide_outline'],result,
            manifest.get('ai_analysis_requests',0)+result['ai_requests'],template_id)
        if (updated['original_source_sha256']!=manifest['original_source_sha256']
                or updated['native_sha256']!=manifest['native_sha256']):
            raise ValueError('재검토 중 원본 양식이 변경되었습니다.')
        folder.rename(registry.path(new_id))
    progress('불확실한 입력칸만 재검토한 양식 등록 완료',1,1)
    return {**updated,'recheck_resolved_count':len(resolved),
            'recheck_added_sample_slots':len(added),
            'recheck_ai_requests':result['ai_requests'],
            'guide_file':str((registry.path(new_id)/updated['guide_file']).resolve())}
