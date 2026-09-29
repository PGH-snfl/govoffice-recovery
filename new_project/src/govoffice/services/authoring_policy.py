"""Apply current output defaults only to a new job's private template snapshot."""
from .numbered_topics import group_numbered


def prepare_new_job(manifest):
    policy=manifest.setdefault('render_policy',{})
    policy.update(readable_body=True,blue_review=True,preserve_layout=True,review_memos=True,polished_output=True,
                  uniform_content_fonts=False,flowing_content_fonts=True)
    limit=manifest.get('research_policy',{}).get('max_groups',3)
    manifest['research_policy']={'mode':'minimal','max_groups':min(3,max(0,int(limit)))}
    topics=manifest['topics']
    grouped=group_numbered([{'index':t['start'],'title':t['title'],'instructions':[]}
                           for t in topics if t['id']!='sfront'])
    by_index={t['start']:t for t in topics if t['id']!='sfront'}
    def visit(nodes,level=0,group=None):
        for node in nodes:
            topic=by_index.get(node['index']);next_group=group
            if topic:
                if group is None or level==1:next_group=topic['id']
                topic.setdefault('research_group',next_group)
            visit(node.get('subtopics',[]),level+1,next_group)
    visit(grouped)
    for topic in topics:
        for f in topic['fields']:
            if f.get('role')!='personal' and f.get('kind')!='schedule_marker':f['multiline']=True
    return manifest
