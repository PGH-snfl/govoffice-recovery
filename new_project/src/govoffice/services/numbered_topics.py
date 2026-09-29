"""Source-order numbering hierarchy; labels are never merged by visible name."""
from copy import deepcopy
import re


def numbering(title):
    value=title.strip()
    match=re.match(r'^(\d+(?:[.-]\d+)+)(?:[.)]?\s+)',value)
    if match:return tuple(match[1].replace('-','.').split('.'))
    match=re.match(r'^(?:제\s*)?(\d+)\s*(?:장|[.)])\s*',value)
    if match:return (match[1],)
    if re.match(r'^[IVXⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[.\s]',value):return ('roman',)
    if re.match(r'^[가-하][.)]\s*',value):return ('letter','sub','item')
    if re.match(r'^\(\d+\)',value):return ('paren','sub','item','detail')
    return ()


def flatten(chapters):
    for node in chapters:
        yield node
        yield from flatten(node.get('subtopics',[]))


def group_numbered(sections):
    roots=[];stack=[]
    for original in sections:
        node=deepcopy(original);node['subtopics']=[]
        parts=numbering(node['title']);depth=len(parts) or (stack[-1][0] if stack else 1)
        if parts and parts[0]!='roman' and any(s[2]==('roman',) for s in stack):depth+=1
        while stack and (stack[-1][0]>=depth or (
                parts and parts[0].isdigit() and stack[-1][2] and stack[-1][2][0].isdigit()
                and tuple(parts[:len(stack[-1][2])])!=stack[-1][2])):stack.pop()
        # Missing numeric parent: keep a clearly labelled grouping, never invent
        # semantic headings in the source document itself.
        if not stack and len(parts)>1 and parts[0].isdigit():
            parent={'index':None,'title':parts[0]+'번 중주제','instructions':[],
                    'subtopics':[],'synthetic':True}
            roots.append(parent);stack.append((1,parent,(parts[0],)))
        (stack[-1][1]['subtopics'] if stack else roots).append(node)
        stack.append((depth,node,parts))
    return roots


def guide_markdown(name, chapters, unattached=()):
    lines=['# '+name,'']
    def emit(nodes,depth):
        for node in nodes:
            lines.extend(['#'*min(depth,6)+' '+node['title'],''])
            for rule in node['instructions']:lines.extend([rule['text'],''])
            emit(node.get('subtopics',[]),depth+1)
    emit(chapters,2)
    if unattached:
        lines.extend(['## 연결되지 않은 작성요령',''])
        for text in unattached:lines.extend([text,''])
    return '\n'.join(lines)
