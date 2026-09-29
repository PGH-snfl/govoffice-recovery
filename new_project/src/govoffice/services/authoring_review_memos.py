"""Review metadata and display text, independent of Hancom and external AI."""
import json
import re

MARKER = re.compile(r'(?:확인|검토)\s*필요(?!\s*(?:없|하지\s*않))')
BRACKET = re.compile(r'\[[^\[\]]*\]|\([^()]*\)|【[^【】]*】')
FIELD_ID = re.compile(r'(?<![A-Za-z0-9_])P\d{4,}(?!\d)')


def memo_body(value):
    """Remove only explicit annotations; ordinary prose is never summarized."""
    value = BRACKET.sub(lambda m: '' if MARKER.search(m.group()) else m.group(), value)
    lines = []
    for line in value.split('\n'):
        if not line.strip():
            continue
        if re.fullmatch(r'\s*(?:(?:확인|검토)\s*필요(?:\s*[:：].*)?|\?)\s*', line):
            continue
        lines.append(line.rstrip())
    return '\n'.join(lines).strip()


def original_packets(job_folder):
    """Read only fixed job files. Packet names are never executed or opened."""
    packets = {}
    saved = job_folder / '저장응답_원본.json'
    if saved.is_file():
        bundle = json.loads(saved.read_text(encoding='utf-8'))
        if isinstance(bundle.get('ai_attempts'), dict):
            packets.update(bundle['ai_attempts'])
    response_dir = job_folder / 'responses'
    for path in response_dir.glob('*.attempt*.json'):
        packets[path.name] = json.loads(path.read_text(encoding='utf-8'))
    latest = {}
    for name, packet in packets.items():
        match = re.fullmatch(r'([A-Za-z0-9_-]+)\.attempt(\d+)\.json', name)
        if not match or not isinstance(packet, dict):
            continue
        topic, attempt = match[1], int(match[2])
        if packet.get('topic_id') != topic:
            continue
        if attempt >= latest.get(topic, (-1, None))[0]:
            latest[topic] = (attempt, packet)
    return {key: packet for key, (_, packet) in latest.items()}


def verification_method(reason):
    methods = []
    rules = [
        (r'기관|기업|업체|경쟁|제품|납품|시장|고객', '기관·기업의 공식 자료와 제품·실적 자료를 대조하고, 비교 기준일과 동일한 시험·운영 조건인지 확인하세요.'),
        (r'성명|이름|담당|연구자|인력|협약|역할|참여', '협약서·참여 인력 명단과 대조해 기관명, 담당자, 역할 및 참여 여부를 확인하세요.'),
        (r'예산|금액|사업비|투자|단가|매출|수량', '승인된 예산·견적·산출 근거와 대조해 금액, 단위, 수량과 합계를 확인하세요.'),
        (r'일정|기간|날짜|연도|개월|차년도', '공고·협약서와 실제 수행 계획을 대조해 시작·종료일과 연차별 일정을 확인하세요.'),
        (r'성능|수치|효율|출력|시험|실증|기술|목표|달성|KSTAR|ITER|핵융합', '원자료·시험성적서와 수치 및 측정 조건을 대조하세요. 이미 달성한 실적과 앞으로의 목표·제안을 구분하고 실제 과제 범위에 맞게 수정하세요.'),
        (r'인증|안전|규제|특허|지식재산|승인', '적용 기준과 보유 증빙을 담당자에게 확인하고, 취득·승인 완료 여부와 향후 계획을 구분하세요.'),
    ]
    for pattern, method in rules:
        if re.search(pattern, reason, re.I):
            methods.append(method)
    return '\n'.join(methods) or '실제 과제 계획과 보유 자료를 담당자와 대조해 확정하세요. 근거가 없는 값은 임의로 확정하지 말고 확인한 내용으로 해당 부분을 수정하세요.'


def has_reviewable_body(field, value, cell_width=None):
    """A missing fact/empty slot is not authored prose needing a review memo."""
    from .authoring_response_policy import prose_field, FACT_LABEL, PROSE_LABEL
    if field.get('role') == 'personal' or field.get('kind') == 'schedule_marker':
        return False
    body = memo_body(value).strip()
    if not body or re.fullmatch(r'[\s_\-—–?□○·.…]*|미정|미확정|미제공|입력\s*필요|작성\s*예정', body):
        return False
    label = str(field.get('label', '')).strip()
    if body.strip(' :：') == label.strip(' :：'):
        return False
    if FACT_LABEL.search(label) and not PROSE_LABEL.search(label):
        return False
    return prose_field(field, cell_width)


def simple_fill_reason(reason):
    # Keep caveats about authored claims/plans, even when evidence is missing.
    if re.search(r'본문|제안|가정|판단|비교|해석|추정|주장|과대|상충|최신성|적합성|타당성', reason):
        return False
    identifiers = r'성명|이름|연락처|전화번호|전자우편|이메일|주소|사업명|과제번호|등록번호|소속|직위|인적사항'
    if re.search(identifiers, reason):
        return True
    return bool(re.search(r'빈\s*칸|공란|미입력|직접\s*입력|입력해|기입해|채워', reason))


def build_memo(topic, field, value, notes, original=None, *, cell_width=None):
    if not has_reviewable_body(field, value, cell_width):
        return None
    original = original if isinstance(original, dict) else {}
    original_values = original.get('values', {})
    old = original_values.get(field['id'], '') if isinstance(original_values, dict) else ''
    old = old if isinstance(old, str) else ''
    reasons = list(notes)
    # Historical details apply only while a current explicit marker remains.
    # Resolved/current values must not regain stale review annotations.
    unresolved = bool(MARKER.search(value)) or value.strip() == '?'
    if unresolved:
        reasons += [n for n in original.get('needs_review', [])
                    if isinstance(n, str) and field['id'] in FIELD_ID.findall(n)]
    for text in (value, old if unresolved else ''):
        reasons += [m.group() for m in BRACKET.finditer(text) if MARKER.search(m.group())]
        reasons += [line for line in text.split('\n')
                    if re.match(r'^\s*(?:확인|검토)\s*필요\s*[:：]', line)]
    cleaned = []
    for reason in reasons:
        if not isinstance(reason, str) or re.search(r'확인\s*필요\s*없|(?:확인|검토)\s*(?:완료|불필요)', reason):
            continue
        reason = FIELD_ID.sub('', reason).strip(' [],，()【】:：-\t\r\n')
        reason = re.sub(r'^(?:확인|검토)\s*필요\s*[:：]?\s*', '', reason).strip()
        if reason and not simple_fill_reason(reason) and reason not in cleaned:
            cleaned.append(reason)
    if not unresolved and not cleaned:
        return None
    label = (field.get('label') or topic.get('title') or field['id']).strip()
    if not cleaned:
        # Do not turn a discarded blank-filling instruction into a generic memo.
        if any(isinstance(reason,str) and simple_fill_reason(reason) for reason in reasons):
            return None
        cleaned = [label + ' 본문에 제시된 사실·수치·계획이 실제 과제와 맞는지 확인']
    detail = '\n'.join('- ' + reason for reason in cleaned)
    method = verification_method(label + ' ' + ' '.join(cleaned))
    text = f"확인 필요 · {label}\n확인할 내용\n{detail}\n확인 방법\n{method}"
    return {'field_id': field['id'], 'topic': topic.get('title', ''),
            'label': label, 'reasons': cleaned, 'method': method, 'text': text}
