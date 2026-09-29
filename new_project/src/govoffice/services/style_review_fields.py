"""Resolve review groups by full field path, independently of extraction method.

This is a read-only view over a profile. Candidates, values and document locators
are never coalesced here; only their canonical field/group identities are shared.
"""

from collections.abc import Iterable, Mapping
from copy import deepcopy

from ..domain.user_profile import 사용자프로필


def _parts(value: object) -> list[str]:
    return [" ".join(part.split()) for part in str(value or "").split(">") if part.strip()]


def _key(parts: list[str]) -> str:
    return " > ".join(parts).casefold()


def normalize_review_fields(
    candidates: Iterable[Mapping[str, object]], profile: 사용자프로필,
) -> tuple[dict[str, object], ...]:
    """Reuse registered fields/aliases in their own parent scope, or draft paths.

    A table's structural parent is only a fallback for an unqualified candidate;
    the analyzer's full path retains outer roles such as lead/member > contact.
    """
    children: dict[str, list] = {}
    for field in profile.대표필드목록:
        children.setdefault(field.상위필드id or "", []).append(field)
    spellings: dict[str, str] = {}

    def resolve(parts: list[str]):
        canonical: list[str] = []
        parent_id: str | None = ""
        resolved = []
        for part in parts:
            matches = [
                field for field in children.get(parent_id, ())
                if part.casefold() in {
                    " ".join(str(name).split()).casefold()
                    for name in (field.대표필드명, *field.별칭)
                }
            ] if parent_id is not None else []
            field = matches[0] if len(matches) == 1 else None
            name = field.대표필드명 if field else part
            prefix = _key([*canonical, name])
            canonical.append(spellings.setdefault(prefix, name))
            resolved.append(field)
            parent_id = field.id if field else None
        return canonical, resolved

    result = []
    for raw in candidates:
        item = deepcopy(dict(raw))
        parts = _parts(item.get("field_path") or item.get("field"))
        structural = _parts(item.get("structural_parent_field"))
        if len(parts) <= 1 and structural:
            child = _parts(item.get("child_field") or item.get("label") or item.get("field"))
            parts = [*structural, *child]
        if not parts:
            result.append(item)
            continue
        parts, nodes = resolve(parts)
        field = nodes[-1]
        parent = nodes[-2] if len(nodes) > 1 else None
        path = " > ".join(parts)
        parent_path = " > ".join(parts[:-1]) if len(parts) > 1 else ""
        group_path = parent_path or path
        group_node = parent if parent_path else field
        # No table/body/structural distinction: the same full parent has one ID.
        group_id = f"profile-group:{group_node.id}" if group_node else f"path-group:{_key(_parts(group_path))}"
        child_id = (f"profile-field:{field.id}" if field else f"path-field:{_key(parts)}") if parent_path else ""
        item.update(
            field=path, field_path=path, canonical_field=path,
            profile_field_id=field.id if field else None,
            parent_profile_field_id=parent.id if parent else None,
            parent_field=parent_path or None,
            representative_field=group_path,
            child_field=parts[-1] if parent_path else None,
            registered=field is not None,
            semantic_group_id=group_id,
            semantic_representative_field=group_path,
            semantic_child_id=child_id,
            semantic_child_field=parts[-1] if parent_path else "",
        )
        result.append(item)
    return tuple(result)
