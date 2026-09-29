"""Versioned, local SQLite separation of immutable layout and writable content.

Each database travels with its template (including job snapshots and archives).
Only source-bound, verified destinations may be used for writing. Unknown areas
are preserved, not guessed to be either decorative or writable.
"""
from collections import Counter
from contextlib import closing
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import xml.etree.ElementTree as ET
from uuid import uuid4

VERSION = 1
BINDING_KEYS = ('id','index','original','label','context','role','kind','insert_after','in_table','style_from_index')
TARGET_KEYS = ('index','original','insert_after','in_table','style_from_index','write_blocked')


def packed(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def binding_digest(manifest):
    return sha(packed({'topics':[{'id':t['id'],'start':t.get('start'),
        'fields':[{k:f[k] for k in BINDING_KEYS if k in f} for f in t.get('fields',[])]}
        for t in manifest['topics']], 'clear_guide_indices':manifest.get('clear_guide_indices',[]),
        'guide_groups':manifest.get('guide_groups',[]), 'blank_indices':manifest.get('blank_indices',[])}).encode())


def save_layout_database(folder, root, manifest, *, classification_root=None):
    """Create a new immutable version; publish its pointer only after commit."""
    from .authoring_design_fields import safe_writing_manifest
    folder=Path(folder)
    # Visible internal slot markers must not change the interpretation of a
    # previously empty design/label cell. Classify against the exact original.
    effective=safe_writing_manifest(classification_root if classification_root is not None else root,manifest)
    protected=set(effective['protected_design_indices'])
    ps=list(root.iter('P'));tables=list(root.iter('TABLE'));cells=list(root.iter('CELL'))
    parents={id(c):p for p in root.iter() for c in p}
    paths={id(root):'/HWPML'}
    for parent in root.iter():
        counts=Counter()
        for child in parent:
            paths[id(child)]=paths[id(parent)]+'/'+child.tag+'['+str(counts[child.tag])+']'
            counts[child.tag]+=1
    pids={id(p):i for i,p in enumerate(ps)}
    tids={id(t):i for i,t in enumerate(tables)};cids={id(c):i for i,c in enumerate(cells)}
    def ancestor(node, tag):
        node=parents.get(id(node))
        while node is not None:
            if node.tag==tag:return node
            node=parents.get(id(node))
    def own(p):
        return ''.join(''.join(c.itertext()) for t in p.findall('TEXT') for c in t if c.tag=='CHAR')
    fields=[(t['id'],f) for t in effective['topics'] for f in t.get('fields',[])]
    targets={f['index'] for _,f in fields if not f.get('write_blocked') and not f.get('insert_after')}
    anchors={f['index'] for _,f in fields if not f.get('write_blocked') and f.get('insert_after')}
    guides=set(manifest.get('clear_guide_indices',[]))
    guides.update(i for group in manifest.get('guide_groups',[]) for i in group)
    guides.update(r['index'] for t in manifest['topics'] for r in t.get('instructions',[]) if 'index' in r)
    headings={t.get('start') for t in manifest['topics']}
    # A label shares a cell only with fixed text; mixed prose/label cells remain
    # conservative. Cell/table borders and graphics always stay in the skeleton.
    content_tables={id(ancestor(ps[i],'TABLE')) for i in targets|anchors}
    regions=[]
    for i,p in enumerate(ps):
        cell=ancestor(p,'CELL');table=ancestor(p,'TABLE');text=own(p)
        fixed_label=(cell is not None and id(table) in content_tables and bool(text.strip())
                     and len(text.strip())<=80 and not any(pids[id(q)] in targets for q in cell.findall('PARALIST/P')))
        if i in protected:role,reason='design','번호 배지·제목 막대·보호된 고정 항목'
        elif i in targets:role,reason='content','등록 시 확인된 내용 입력 위치'
        elif i in anchors:role,reason='anchor','원문 뒤에 새 내용 삽입; 원문은 보존'
        elif i in guides:role,reason='instruction','양식에 기록된 작성요령'
        elif i in headings or fixed_label:role,reason='design','소주제 제목 또는 입력 표의 고정 항목'
        else:role,reason='preserve','자동 입력 미지정; 원본 유지'
        regions.append((i,paths[id(p)],tids.get(id(table)),cids.get(id(cell)),role,reason,text,
                        packed({'paragraph':p.attrib,'runs':[t.attrib for t in p.findall('TEXT')]})))
    skeleton=deepcopy(root);sps=list(skeleton.iter('P'))
    for i in (targets|(guides-anchors-headings))-protected:
        if not 0<=i<len(sps):continue
        for t in sps[i].findall('TEXT'):
            for c in t.findall('CHAR'):t.remove(c)
    def container_role(rows):
        roles={r[4] for r in rows}
        writable=bool(roles&{'content','anchor'})
        return ('mixed' if roles-{'content','anchor'} else 'content') if writable else ('design' if 'design' in roles else 'instruction' if roles=={'instruction'} else 'preserve')
    counts=dict(Counter(r[4] for r in regions))
    filename='layout_'+uuid4().hex+'.sqlite3'
    path=folder/filename
    metadata={'schema_version':VERSION,'classifier_version':VERSION,'template_id':manifest['id'],
              'source_sha256':manifest['source_sha256'],'native_sha256':manifest['native_sha256'],
              'xml_sha256':sha(ET.tostring(root)), 'binding_sha256':binding_digest(manifest),
              'created_at':datetime.now(timezone.utc).isoformat(),'protected_indices':sorted(protected)}
    try:
        with closing(sqlite3.connect(path)) as db, db:
            db.executescript('''
                CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
                CREATE TABLE design_layout(id INTEGER PRIMARY KEY CHECK(id=1),xml TEXT NOT NULL);
                CREATE TABLE regions(paragraph_index INTEGER PRIMARY KEY,element_path TEXT NOT NULL UNIQUE,
                    table_index INTEGER,cell_index INTEGER,role TEXT NOT NULL,reason TEXT NOT NULL,
                    original_text TEXT NOT NULL,style_json TEXT NOT NULL);
                CREATE TABLE content_fields(field_id TEXT PRIMARY KEY,topic_id TEXT NOT NULL,
                    source_index INTEGER NOT NULL,target_index INTEGER NOT NULL,write_mode TEXT NOT NULL,
                    target_json TEXT NOT NULL,field_json TEXT NOT NULL);
                CREATE TABLE tables(table_index INTEGER PRIMARY KEY,parent_cell_index INTEGER,
                    element_path TEXT NOT NULL,role TEXT NOT NULL,properties_json TEXT NOT NULL);
                CREATE TABLE cells(cell_index INTEGER PRIMARY KEY,table_index INTEGER,
                    element_path TEXT NOT NULL,role TEXT NOT NULL,properties_json TEXT NOT NULL);
                CREATE INDEX region_role ON regions(role);
                CREATE INDEX field_target ON content_fields(target_index);
            ''')
            db.executemany('INSERT INTO metadata VALUES (?,?)',[(k,packed(v)) for k,v in metadata.items()])
            db.execute('INSERT INTO design_layout VALUES (1,?)',(ET.tostring(skeleton,encoding='unicode'),))
            db.executemany('INSERT INTO regions VALUES (?,?,?,?,?,?,?,?)',regions)
            originals={f['id']:f for t in manifest['topics'] for f in t.get('fields',[])}
            db.executemany('INSERT INTO content_fields VALUES (?,?,?,?,?,?,?)',[
                (f['id'],topic,originals[f['id']]['index'],f['index'],
                 'blocked' if f.get('write_blocked') else 'insert_after' if f.get('insert_after') else 'replace',
                 packed({k:f[k] for k in TARGET_KEYS if k in f}),packed(originals[f['id']])) for topic,f in fields])
            for i,table in enumerate(tables):
                # Include nested cell regions so an outer layout wrapper is not
                # misrepresented as a pure decorative table.
                inside={pids[id(p)] for p in table.iter('P')}
                db.execute('INSERT INTO tables VALUES (?,?,?,?,?)',(i,cids.get(id(ancestor(table,'CELL'))),
                    paths[id(table)],container_role([r for r in regions if r[0] in inside]),
                    packed({'attributes':table.attrib,'layout':[ET.tostring(c,encoding='unicode') for c in table if c.tag!='ROW']})))
            for i,cell in enumerate(cells):
                inside={pids[id(p)] for p in cell.iter('P')}
                db.execute('INSERT INTO cells VALUES (?,?,?,?,?)',(i,tids.get(id(ancestor(cell,'TABLE'))),paths[id(cell)],
                    container_role([r for r in regions if r[0] in inside]),packed({'attributes':cell.attrib,
                    'layout':[ET.tostring(c,encoding='unicode') for c in cell if c.tag!='PARALIST']})))
    except Exception:
        # Only our newly allocated file; never remove a previous usable version.
        path.unlink(missing_ok=True)
        raise
    manifest['layout_database']={'file':filename,'sha256':sha(path.read_bytes()),'version':VERSION,
                                 'counts':counts,'table_count':len(tables),'cell_count':len(cells),
                                 'field_count':len(fields)}
    return manifest['layout_database']


def stored_writing_manifest(folder, root, manifest):
    """Read saved destinations, fail closed on corruption; legacy stays supported."""
    info=manifest.get('layout_database')
    if info is None:
        from .authoring_design_fields import safe_writing_manifest
        return safe_writing_manifest(root,manifest)
    try:
        filename=info['file']
        if not re.fullmatch(r'layout_[a-f0-9]{32}\.sqlite3',filename):raise ValueError('파일명')
        path=Path(folder)/filename
        if path.is_symlink() or sha(path.read_bytes())!=info['sha256']:raise ValueError('파일 검증')
        with closing(sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True)) as db:
            meta={k:json.loads(v) for k,v in db.execute('SELECT key,value FROM metadata')}
            if (meta['schema_version']!=VERSION or info['version']!=VERSION
                    or meta['template_id']!=manifest['id'] or meta['source_sha256']!=manifest['source_sha256']
                    or meta['native_sha256']!=manifest['native_sha256']
                    or meta['xml_sha256']!=sha(ET.tostring(root)) or meta['binding_sha256']!=binding_digest(manifest)):
                raise ValueError('원본·입력 위치 버전 불일치')
            targets={fid:json.loads(target) for fid,target in db.execute('SELECT field_id,target_json FROM content_fields')}
        effective=deepcopy(manifest)
        for topic in effective['topics']:
            for field in topic.get('fields',[]):
                for key in (*TARGET_KEYS,'write_target'):field.pop(key,None)
                field.update(targets[field['id']])
        effective['protected_design_indices']=meta['protected_indices']
        return effective
    except (OSError,sqlite3.Error,KeyError,TypeError,ValueError) as exc:
        raise ValueError('양식의 디자인·내용 분리 데이터베이스를 확인할 수 없습니다. 양식을 다시 등록해 주세요. '+str(exc)) from exc
