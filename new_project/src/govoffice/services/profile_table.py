"""Selection-only profile import and ID-preserving table operations.

No preset repository or document writer is used here. Drafts live in memory.
"""
from __future__ import annotations

import time
from uuid import uuid4

from ..domain.user_profile import 사용자프로필, 기본사용자정보필드
from .hwpml_table_analysis import HWPMLTableFieldAnalyzer
from .style_review_fields import normalize_review_fields


class ProfileTableCommands:
    def __init__(self, repository):
        self.repository = repository
        self.draft = None

    def analyze(self, source, document_key):
        self.draft = None
        if document_key is None:
            raise ValueError("연결된 한글 문서를 확인한 뒤 다시 선택하세요.")
        profile = self.repository.불러오기()
        definitions = []
        aliases = {}
        for field in profile.대표필드목록:
            path = profile.필드경로(field)
            definition = field.사전()
            definition["대표필드명"] = path
            definitions.append(definition)
            parent = profile.대표필드ID찾기(field.상위필드id)
            if parent:
                parent_path = profile.필드경로(parent)
                aliases[path] = tuple(dict.fromkeys(
                    spelling for alias in field.별칭 for spelling in (
                        f"{parent_path} > {alias}",
                        f"{parent_path} {field.대표필드명}",
                        f"{parent_path} {alias}",
                    )))
            else:
                aliases[path] = field.별칭
        result = HWPMLTableFieldAnalyzer().analyze(
            source, registered_fields=[d["대표필드명"] for d in definitions],
            aliases=aliases, registered_values=definitions,
        ).as_dict()
        candidates = list(normalize_review_fields(result["candidates"], profile))
        # Unlike preset review, keep ALL low-confidence candidates for inspection.
        candidates.sort(key=lambda c: not bool(c.get("recommended")))
        self.draft = dict(id=uuid4().hex, document_key=document_key,
                          created_at=time.monotonic(), snapshot=profile.사전(),
                          candidates={c["candidate_id"]: c for c in candidates})
        return dict(draft_id=self.draft["id"], candidates=candidates)

    def save_selection(self, command, document_key):
        draft = self.draft
        if (not draft or command.get("draft_id") != draft["id"]
                or time.monotonic() - draft["created_at"] > 900):
            raise ValueError("개인정보 분석이 만료되었습니다. 영역을 다시 선택하세요.")
        if document_key != draft["document_key"]:
            raise ValueError("한글 문서가 변경되었습니다. 영역을 다시 선택하세요.")
        profile = self.repository.불러오기()
        if profile.사전() != draft["snapshot"]:
            raise ValueError("저장된 정보가 변경되었습니다. 선택 영역을 다시 분석하세요.")
        rows = command.get("rows")
        if not isinstance(rows, list) or not rows:
            raise ValueError("저장할 항목을 하나 이상 체크하세요.")
        seen = set()
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("저장할 항목 형식이 올바르지 않습니다.")
            identifier = row.get("candidate_id")
            if identifier not in draft["candidates"] or identifier in seen:
                raise ValueError("분석 결과에 없는 항목이거나 중복된 항목입니다.")
            seen.add(identifier)
            path = str(row.get("field", "")).strip()
            value = str(row.get("value", "")).strip()
            parts = [p.strip() for p in path.split(">")]
            if not value or not all(parts):
                raise ValueError("필드 이름과 저장할 값을 입력하세요.")
            parent = None
            for part in parts:
                lookup = f"{profile.필드경로(parent)} > {part}" if parent else part
                field = profile.대표필드찾기(lookup)
                if field is None:
                    profile = profile.대표필드추가(part, 상위필드=parent.id if parent else None)
                    field = profile.대표필드찾기(lookup)
                parent = field
            profile = profile.대표필드값추가(parent.id, value)
        # Validate everything before a single atomic repository write.
        self.repository.저장(profile)
        self.draft = None
        return len(rows)

    def mutate(self, command):
        profile = self.repository.불러오기()
        # The management page sends its last snapshot to avoid stale edits.
        if command.get("snapshot") != profile.사전():
            raise ValueError("다른 화면에서 정보가 변경되었습니다. 새로고침 후 다시 시도하세요.")
        field = profile.대표필드ID찾기(command.get("field_id", ""))
        if field is None:
            raise ValueError("변경할 필드를 찾지 못했습니다.")
        op = command.get("operation")
        value = str(command.get("value", ""))
        if op == "move_field":
            profile = profile.대표필드상위변경(field.id, command.get("target_id") or None)
        elif op == "delete_field":
            profile = profile.대표필드삭제(field.id)
        elif op == "default":
            profile = profile.기본값지정(field.id, value)
        elif op == "add_value":
            profile = profile.대표필드값추가(field.id, value)
        elif op in {"edit_value", "delete_value", "move_value"}:
            if value not in field.값목록:
                raise ValueError("수정할 값이 더 이상 존재하지 않습니다.")
            if op == "edit_value":
                replacement = str(command.get("new_value", "")).strip()
                if not replacement:
                    raise ValueError("빈 값은 저장할 수 없습니다. 삭제를 사용하세요.")
                definitions = [f.사전() for f in profile.대표필드목록]
                item = next(d for d in definitions if d["id"] == field.id)
                item["값목록"] = list(dict.fromkeys(replacement if v == value else v for v in field.값목록))
                if field.기본값 == value:
                    item["기본값"] = replacement
                profile = 사용자프로필.생성({"대표필드목록": definitions})
            else:
                if op == "move_value":
                    target = profile.대표필드ID찾기(command.get("target_id", ""))
                    if target is None or target.id == field.id:
                        raise ValueError("값을 옮길 다른 필드를 선택하세요.")
                    profile = profile.대표필드값추가(target.id, value)
                profile = profile.대표필드값삭제(field.id, value)
        elif op == "edit_field":
            name = str(command.get("name", "")).strip()
            if ">" in name:
                raise ValueError("필드 이름에 > 기호는 사용할 수 없습니다. 이동은 드래그를 이용하세요.")
            if not field.상위필드id and field.대표필드명 in 기본사용자정보필드 and name != field.대표필드명:
                raise ValueError("이름·전화번호·이메일 기본 항목의 이름은 변경할 수 없습니다.")
            aliases = command.get("aliases", list(field.별칭))
            if not isinstance(aliases, list):
                raise ValueError("별칭 형식이 올바르지 않습니다.")
            # Reject sibling collisions rather than silently merging stable IDs.
            names = {str(n).strip().casefold() for n in [name, *aliases]}
            for other in profile.대표필드목록:
                if other.id != field.id and other.상위필드id == field.상위필드id:
                    if names & {n.casefold() for n in [other.대표필드명, *other.별칭]}:
                        raise ValueError("같은 위치에 동일한 이름 또는 별칭이 있습니다.")
            definitions = [f.사전() for f in profile.대표필드목록]
            item = next(d for d in definitions if d["id"] == field.id)
            item.update(대표필드명=name, 별칭=aliases)
            profile = 사용자프로필.생성({"대표필드목록": definitions})
        else:
            raise ValueError("지원하지 않는 표 편집 작업입니다.")
        self.repository.저장(profile)
        return profile
