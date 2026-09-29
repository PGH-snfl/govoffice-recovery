"""Keep generated prose; reduce unsupported factual cells to one review marker."""
import re

REVIEW_MARKER='확인 필요'
PROSE_LABEL=re.compile(r'목표|내용|계획|전략|방안|효과|활용|적용범위|서비스|프로세스|추진체계|기술 동향|경쟁기관 현황|지식재산권.*현황|인증기준 현황|표준화 현황')
FACT_LABEL=re.compile(r'시장\s*규모|수요량|수요처|관련제품|금액|예산|사업명|과제번호|등록번호|국가명|국명|성명|직위|전화|전자우편|연구자번호|실적명|세부사업명|기관명|출원|등록일|게재지|연도|연월|^yy|^구분|^비고|기술료|사회문제해결|혁신도약형|경쟁형|표준화연계|공개SW|SW자산뱅크|연구데이터공개|일자리연계|규제샌드박스|정책지정|국제공동|사업화연계|소재부품장비')
REVIEW_RE=re.compile(r'(?:확인|검토)\s*필요|(?<![가-힣])(?:미확정|미제공|미정)(?![가-힣])')
BRACKET_RE=re.compile(r'\[[^\[\]]*?확인\s*필요[^\[\]]*?\]|\([^()]*?확인\s*필요[^()]*?\)|【[^【】]*?확인\s*필요[^【】]*?】')


def prose_field(field, cell_width=None):
    """Explicit content labels outrank table position; factual labels stay factual."""
    if field.get('role')=='personal':return False
    if not field.get('in_table'):return True
    label=str(field.get('label') or field.get('context') or '').strip()
    if FACT_LABEL.search(label):return False
    if PROSE_LABEL.search(label):return True
    return cell_width is not None and cell_width>=20000


def review_only(value,notes=()):
    if not isinstance(value,str):return False
    return bool(REVIEW_RE.search(value) or value.strip()=='?' or notes)


def simplify_prose_review(value):
    """Retain the body and replace detailed bracketed cautions with one marker."""
    text=BRACKET_RE.sub('[확인 필요]',value)
    text=re.sub(r'(?m)^\s*(?:확인|검토)\s*필요\s*[:：][^\n]*$', '[확인 필요]',text)
    return re.sub(r'(?:\[확인 필요\]\s*){2,}','[확인 필요]\n\n',text).strip()


def normalize_response_for_field(topic,response,field,cell_width=None):
    """Normalize one agent response before writing; never invent missing facts."""
    result=response['values'];key=field['id'];value=result[key]
    notes=[n for n in response.get('needs_review',[]) if re.search(r'(?<![A-Za-z0-9_])'+re.escape(key)+r'(?!\d)',n)]
    if not review_only(value,notes):return False
    if prose_field(field,cell_width):
        updated=simplify_prose_review(value)
        if notes and '[확인 필요]' not in updated and REVIEW_MARKER not in updated:
            updated=(updated+'\n\n[확인 필요]').strip()
        result[key]=updated if updated and updated!=REVIEW_MARKER else REVIEW_MARKER
    else:
        result[key]=REVIEW_MARKER
    return result[key]!=value


def normalize_response(topic,response,cell_widths=None,protected_ids=()):
    """Apply to new AI output and imported saved responses alike."""
    cell_widths=cell_widths or {};changed=[]
    for field in topic['fields']:
        if field['id'] in protected_ids or field.get('role')=='personal':continue
        if normalize_response_for_field(topic,response,field,cell_widths.get(field['id'])):
            changed.append(field['id'])
    # Field-specific explanations have been reduced to the visible marker.
    response['needs_review']=[n for n in response.get('needs_review',[]) if not any(
        re.search(r'(?<![A-Za-z0-9_])'+re.escape(f['id'])+r'(?!\d)',n) for f in topic['fields'])]
    return changed


def source_cell_widths(root,manifest):
    from .authoring_design_fields import safe_writing_manifest
    manifest=safe_writing_manifest(root,manifest)
    ps=list(root.iter('P'));parents={id(c):p for p in root.iter() for c in p}
    widths={}
    for topic in manifest['topics']:
        for field in topic['fields']:
            node=ps[field['index']]
            while id(node) in parents:
                node=parents[id(node)]
                if node.tag=='CELL':
                    widths[field['id']]=int(node.get('Width','0') or 0);break
    return widths
