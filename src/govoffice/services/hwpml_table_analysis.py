from __future__ import annotations

import re
import hashlib
import json
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from difflib import SequenceMatcher
from typing import Literal


Direction = Literal["right", "below", "inline"]


def select_review_candidates(
    candidates: Iterable[Mapping[str, object]],
    unconfirmed_limit: int = 10,
) -> tuple[dict[str, object], ...]:
    """Keep confirmed/structural candidates and limit only generic uncertainty."""

    unique: dict[str, dict[str, object]] = {}
    for raw in candidates:
        if not isinstance(raw, Mapping):
            continue
        candidate_id = str(raw.get("candidate_id", "")).strip()
        if candidate_id and candidate_id not in unique:
            unique[candidate_id] = dict(raw)

    def sort_key(candidate: Mapping[str, object]) -> tuple[object, ...]:
        return (
            -int(bool(candidate.get("registered"))),
            -float(candidate.get("confidence", 0.0)),
            int(candidate.get("table", 0)),
            int(candidate.get("row", 0)),
            int(candidate.get("col", 0)),
            str(candidate.get("candidate_id", "")),
        )

    confirmed = sorted(
        (candidate for candidate in unique.values() if candidate.get("recommended")),
        key=sort_key,
    )
    structural_unconfirmed = sorted(
        (
            candidate
            for candidate in unique.values()
            if not candidate.get("recommended")
            and candidate.get("classification_basis") == "merged_structure"
        ),
        key=sort_key,
    )
    generic_unconfirmed = sorted(
        (
            candidate
            for candidate in unique.values()
            if not candidate.get("recommended")
            and candidate.get("classification_basis") != "merged_structure"
        ),
        key=sort_key,
    )
    return tuple(
        (
            *confirmed,
            *structural_unconfirmed,
            *generic_unconfirmed[: max(0, int(unconfirmed_limit))],
        )
    )


def apply_candidate_field_overrides(
    candidates: Iterable[Mapping[str, object]],
    overrides: Mapping[object, object],
) -> tuple[dict[str, object], ...]:
    """Apply user-approved hierarchy moves without mutating analysis results."""

    if not isinstance(overrides, Mapping):
        raise ValueError("후보 필드 병합 정보는 객체여야 합니다.")
    items = [dict(candidate) for candidate in candidates if isinstance(candidate, Mapping)]
    candidate_ids = {
        str(item.get("candidate_id", ""))
        for item in items
        if str(item.get("candidate_id", ""))
    }
    normalized: dict[str, tuple[str, str, str]] = {}
    for raw_candidate_id, raw_override in overrides.items():
        candidate_id = str(raw_candidate_id)
        if candidate_id not in candidate_ids:
            raise ValueError("분석 결과에 없는 후보를 이동할 수 없습니다.")
        if isinstance(raw_override, Mapping):
            field = str(raw_override.get("field", "")).strip()
            kind = str(raw_override.get("kind", "")).strip()
            target_parent = str(raw_override.get("target_parent", "")).strip()
        else:
            raise ValueError("필드 변경은 병합이 아닌 구조 이동 정보로 지정해야 합니다.")
        if not field or len(field) > 200 or "\n" in field or "\r" in field:
            raise ValueError("이동할 대상 필드명이 올바르지 않습니다.")
        if kind not in {"", "child", "representative"}:
            raise ValueError("지원하지 않는 필드 구조 이동 방식입니다.")
        if target_parent and (
            len(target_parent) > 200 or "\n" in target_parent or "\r" in target_parent
        ):
            raise ValueError("이동할 상위 대표필드 경로가 올바르지 않습니다.")
        normalized[candidate_id] = (field, kind, target_parent)

    for item in items:
        candidate_id = str(item.get("candidate_id", ""))
        override = normalized.get(candidate_id)
        if not override:
            continue
        field, kind, target_parent = override
        item["source_field_path"] = str(
            item.get("field_path", item.get("field", "")) or ""
        ).strip()
        if kind:
            field_parts = [part.strip() for part in field.split(">") if part.strip()]
            parent_parts = [
                part.strip() for part in target_parent.split(">") if part.strip()
            ]
            representative = str(
                item.get(
                    "semantic_representative_field",
                    item.get("representative_field", item["source_field_path"]),
                )
                or item["source_field_path"]
            ).strip()
            representative_leaf = next(
                (part.strip() for part in reversed(representative.split(">")) if part.strip()),
                "",
            )
            child_leaf = str(
                item.get("semantic_child_field", item.get("child_field", "")) or ""
            ).strip()
            if kind == "child":
                leaf = child_leaf or representative_leaf
                expected_parts = [*parent_parts, leaf]
            else:
                expected_parts = [*parent_parts, representative_leaf]
                if child_leaf:
                    expected_parts.append(child_leaf)
            if (
                not parent_parts
                or not all(expected_parts)
                or [part.casefold() for part in field_parts]
                != [part.casefold() for part in expected_parts]
            ):
                raise ValueError(
                    "구조 이동은 기존 필드명을 유지하고 상위 대표필드만 바꿀 수 있습니다."
                )
        item["source_profile_field_id"] = item.get("profile_field_id")
        item["source_parent_profile_field_id"] = item.get("parent_profile_field_id")
        item["field"] = field
        item["field_path"] = field
        item["canonical_field"] = field
        item["structure_move_kind"] = kind
        item["structure_target_parent"] = target_parent
        # The target path is resolved against the latest profile during save.
        # Retaining the source stable ID would create a false ID conflict.
        item["profile_field_id"] = None
        item["parent_profile_field_id"] = None
    return tuple(items)


def group_related_candidates(
    candidates: Iterable[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    """Link reviewed cell pairs by equal/similar fields or values.

    This never changes the cell-derived field/value pair or its selection.
    It only adds relationship metadata so every source location can remain an
    independent checkbox in the review UI.
    """

    items = [dict(candidate) for candidate in candidates if isinstance(candidate, Mapping)]
    if not items:
        return ()

    parent = list(range(len(items)))
    edges: list[tuple[int, int, str]] = []

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int, reason: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
        edges.append((left, right, reason))

    def comparable_text(value: object) -> str:
        return "".join(character for character in str(value or "").casefold() if character.isalnum())

    def field_identity(item: Mapping[str, object]) -> str:
        profile_id = str(item.get("profile_field_id", "") or "").strip()
        if profile_id:
            return f"profile:{profile_id}"
        semantic_child = str(item.get("semantic_child_id", "") or "").strip()
        semantic_group = str(item.get("semantic_group_id", "") or "").strip()
        if semantic_child:
            return f"semantic:{semantic_group}>{semantic_child}"
        if semantic_group:
            return f"semantic:{semantic_group}"
        field_text = comparable_text(item.get("field_path", item.get("field", "")))
        return f"text:{field_text}" if field_text else ""

    field_ids = [field_identity(item) for item in items]
    field_texts = [
        comparable_text(item.get("field_path", item.get("field", item.get("label", ""))))
        for item in items
    ]
    value_texts = [comparable_text(item.get("value", "")) for item in items]

    def index_by(keys: Sequence[str]) -> dict[str, list[int]]:
        result: dict[str, list[int]] = {}
        for index, key in enumerate(keys):
            if key:
                result.setdefault(key, []).append(index)
        return result

    def union_same(groups: Mapping[str, Sequence[int]], reason: str) -> None:
        for indexes in groups.values():
            if len(indexes) < 2:
                continue
            anchor = indexes[0]
            for index in indexes[1:]:
                union(anchor, index, reason)

    def union_similar(
        groups: Mapping[str, Sequence[int]],
        reason: str,
        threshold: float,
        *,
        minimum_length: int = 3,
    ) -> None:
        # Compare distinct normalized strings, not every source cell.  Real
        # documents often repeat a field or value hundreds of times.
        keys = tuple(groups)
        for left_index, left in enumerate(keys):
            for right in keys[left_index + 1 :]:
                if _relationship_text_similar(
                    left,
                    right,
                    threshold,
                    minimum_length=minimum_length,
                ):
                    union(groups[left][0], groups[right][0], reason)

    field_identity_groups = index_by(field_ids)
    field_text_groups = index_by(field_texts)
    value_text_groups = index_by(value_texts)

    # Stable profile/semantic identity and visible normalized text both prove
    # equality.  Different stored IDs can still display the same field label,
    # which must remain visible to the user as a relationship candidate.
    union_same(field_identity_groups, "동일 필드")
    union_same(field_text_groups, "동일 필드")
    union_same(value_text_groups, "동일 값")
    union_similar(field_text_groups, "유사 필드", 0.82)
    union_similar(value_text_groups, "유사 값", 0.9, minimum_length=4)

    members: dict[int, list[int]] = {}
    for index in range(len(items)):
        members.setdefault(find(index), []).append(index)
    component_reasons: dict[int, set[str]] = {root: set() for root in members}
    for left, _right, reason in edges:
        component_reasons[find(left)].add(reason)

    ordered_roots = sorted(members, key=lambda root: min(members[root]))
    cluster_rank = {root: rank for rank, root in enumerate(ordered_roots)}
    for root in ordered_roots:
        indexes = members[root]
        ids = sorted(str(items[index].get("candidate_id", "")) for index in indexes)
        cluster_id = f"relation:{ids[0] or root}"
        representatives = list(
            dict.fromkeys(
                str(
                    items[index].get(
                        "semantic_representative_field",
                        items[index].get("representative_field", items[index].get("field", "")),
                    )
                    or ""
                ).strip()
                for index in indexes
            )
        )
        representatives = [name for name in representatives if name]
        title = representatives[0] if representatives else "개별 후보"
        if len(representatives) > 1:
            title = f"{title} 외 {len(representatives) - 1}개 대표필드"
        reasons = tuple(sorted(component_reasons[root]))
        related_ids = tuple(ids)
        for index in indexes:
            items[index]["relationship_cluster_id"] = cluster_id
            items[index]["relationship_title"] = title
            items[index]["relationship_reasons"] = reasons
            items[index]["related_candidate_ids"] = related_ids
            items[index]["relationship_size"] = len(indexes)
            items[index]["relationship_sort_rank"] = cluster_rank[root]
    return tuple(items)


def _relationship_text_similar(
    left: str,
    right: str,
    threshold: float,
    *,
    minimum_length: int = 3,
) -> bool:
    if not left or not right or left == right:
        return False
    if min(len(left), len(right)) < minimum_length:
        return False
    if abs(len(left) - len(right)) > max(2, int(max(len(left), len(right)) * 0.35)):
        return False
    if left[0] != right[0] and left not in right and right not in left:
        return False
    return SequenceMatcher(None, left, right, autojunk=False).ratio() >= threshold


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].upper()


def _attribute(element: ET.Element, *names: str) -> str | None:
    wanted = {name.casefold() for name in names}
    for key, value in element.attrib.items():
        if key.rsplit("}", 1)[-1].casefold() in wanted:
            return value
    return None


def _positive_int(value: str | None, default: int) -> int:
    try:
        converted = int(str(value).strip())
    except (TypeError, ValueError):
        return default
    return converted if converted > 0 else default


def _non_negative_int(value: str | None) -> int | None:
    try:
        converted = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return converted if converted >= 0 else None


def _normalized_label(value: str) -> str:
    value = re.sub(
        r"^[\s\[\]{}()<>《》〈〉【】]+|"
        r"[\s:\uff1a\[\]{}()<>《》〈〉【】]+$",
        "",
        value,
    )
    return re.sub(r"\s+", "", value).casefold()


def _display_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _field_name(value: str) -> str:
    text = re.sub(r"\s+", " ", value.strip(" \t\r\n:\uff1a"))
    wrappers = {
        "[": "]",
        "{": "}",
        "(": ")",
        "<": ">",
        "《": "》",
        "〈": "〉",
        "【": "】",
    }
    while len(text) >= 2 and wrappers.get(text[0]) == text[-1]:
        text = text[1:-1].strip()
    return text


@dataclass(frozen=True, slots=True)
class TextSlotLocator:
    """One exact substring in an ElementTree text or tail slot."""

    element_path: tuple[int, ...]
    text_slot: Literal["text", "tail"]
    start: int
    end: int
    text: str


@dataclass(frozen=True, slots=True)
class ValueLocator:
    """Stable value location in the original parsed HWPML tree.

    Concatenating ``segment.text`` in order always yields ``value_text``.
    ``occurrence`` is one-based within the value cell's visible text.
    """

    table_index: int
    row: int
    col: int
    value_text: str
    occurrence: int
    segments: tuple[TextSlotLocator, ...]


@dataclass(frozen=True, slots=True)
class CellStyleFingerprint:
    """시각적으로 같은 셀을 ID 차이와 무관하게 비교하는 정규화 서명."""

    signature: str
    cell: tuple[tuple[str, str], ...] = ()
    paragraph: tuple[tuple[str, str], ...] = ()
    character: tuple[tuple[str, str], ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "signature": self.signature,
            "cell": dict(self.cell),
            "paragraph": dict(self.paragraph),
            "character": dict(self.character),
        }


@dataclass(frozen=True, slots=True)
class FieldValueCandidate:
    candidate_id: str
    field: str
    label: str
    value: str
    table: int
    row: int
    col: int
    value_row: int
    value_col: int
    direction: Direction
    confidence: float
    registered: bool
    recommended: bool
    context_title: str | None
    locator: ValueLocator
    profile_field_id: str | None = None
    parent_field: str | None = None
    parent_profile_field_id: str | None = None
    field_path: str | None = None
    label_style: CellStyleFingerprint | None = None
    value_style: CellStyleFingerprint | None = None
    classification_basis: str = "semantic"
    structural_group_id: str | None = None
    structural_parent_field: str | None = None
    structural_parent_row: int | None = None
    structural_parent_col: int | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HWPMLTableAnalysis:
    registered_candidates: tuple[FieldValueCandidate, ...]
    unregistered_candidates: tuple[FieldValueCandidate, ...]
    style_rules: dict[str, tuple[str, ...]] | None = None

    @property
    def candidates(self) -> tuple[FieldValueCandidate, ...]:
        return (*self.registered_candidates, *self.unregistered_candidates)

    def as_dict(self) -> dict[str, object]:
        registered = [candidate.as_dict() for candidate in self.registered_candidates]
        unregistered = [candidate.as_dict() for candidate in self.unregistered_candidates]
        return {
            "candidates": [*registered, *unregistered],
            "registered_candidates": registered,
            "unregistered_candidates": unregistered,
            "style_rules": self.style_rules or {"field": (), "value": ()},
        }


@dataclass(frozen=True, slots=True)
class _TextSlot:
    element_path: tuple[int, ...]
    text_slot: Literal["text", "tail"]
    text: str
    global_start: int
    global_end: int


@dataclass(frozen=True, slots=True)
class _CellContent:
    text: str
    slots: tuple[_TextSlot, ...]

    @property
    def display(self) -> str:
        return _display_text(self.text)

    def trimmed_range(self) -> tuple[int, int]:
        start = len(self.text) - len(self.text.lstrip())
        end = len(self.text.rstrip())
        return start, end

    def segments(self, start: int, end: int) -> tuple[TextSlotLocator, ...]:
        result: list[TextSlotLocator] = []
        for slot in self.slots:
            overlap_start = max(start, slot.global_start)
            overlap_end = min(end, slot.global_end)
            if overlap_start >= overlap_end:
                continue
            local_start = overlap_start - slot.global_start
            local_end = overlap_end - slot.global_start
            result.append(
                TextSlotLocator(
                    element_path=slot.element_path,
                    text_slot=slot.text_slot,
                    start=local_start,
                    end=local_end,
                    text=slot.text[local_start:local_end],
                )
            )
        return tuple(result)


@dataclass(frozen=True, slots=True)
class _Cell:
    element: ET.Element
    row: int
    col: int
    rowspan: int
    colspan: int
    content: _CellContent
    style: CellStyleFingerprint

    @property
    def text(self) -> str:
        return self.content.display

    @property
    def row_end(self) -> int:
        return self.row + self.rowspan

    @property
    def col_end(self) -> int:
        return self.col + self.colspan


@dataclass(frozen=True, slots=True)
class _Relation:
    value_cell: _Cell
    direction: Direction
    score: float
    value_start: int
    value_end: int
    recommendable: bool = True


@dataclass(frozen=True, slots=True)
class _ScanRegion:
    table: int
    row: int
    col: int
    content: _CellContent
    probable_header: bool
    style: CellStyleFingerprint | None = None


@dataclass(frozen=True, slots=True)
class _ContextEvent:
    order: int
    kind: Literal["paragraph", "table", "break"]
    text: str = ""
    break_before: bool = False
    outline_level: int | None = None


@dataclass(frozen=True, slots=True)
class _RegisteredValue:
    field: str
    value: str
    profile_field_id: str | None


class _FieldRegistry:
    def __init__(
        self,
        registered_fields: Iterable[str] | Mapping[str, object],
        aliases: Mapping[str, Iterable[str]] | None,
    ) -> None:
        if isinstance(registered_fields, Mapping):
            names = [str(name).strip() for name in registered_fields]
        elif isinstance(registered_fields, (str, bytes)):
            names = [str(registered_fields).strip()]
        else:
            names = [str(name).strip() for name in registered_fields]
        alias_groups = aliases or {}
        names.extend(str(name).strip() for name in alias_groups)

        self._registered = {name for name in names if name}
        matches: dict[str, set[str]] = {}
        for canonical in self._registered:
            matches.setdefault(_normalized_label(canonical), set()).add(canonical)
        for canonical_source, raw_aliases in alias_groups.items():
            canonical = str(canonical_source).strip()
            if not canonical:
                continue
            values: Iterable[object]
            if isinstance(raw_aliases, (str, bytes)):
                values = (raw_aliases,)
            else:
                values = raw_aliases
            for alias_source in values:
                alias = str(alias_source).strip()
                if alias:
                    matches.setdefault(_normalized_label(alias), set()).add(canonical)
        self._matches = matches

    def resolve(self, label: str) -> tuple[str | None, bool]:
        matches = self._matches.get(_normalized_label(label), set())
        if len(matches) == 1:
            return next(iter(matches)), False
        # A conflicting alias must be confirmed by the user.
        return None, bool(matches)


class _StyleResolver:
    """HWPML 참조 ID를 실제 모양 속성으로 풀어 안정된 셀 서명을 만든다."""

    _IGNORED = {
        "id", "rowaddr", "row", "rowindex", "coladdr", "col", "colindex",
        "rowspan", "colspan", "width", "height",
    }

    def __init__(self, root: ET.Element) -> None:
        self._definitions: dict[tuple[str, str], ET.Element] = {}
        for element in root.iter():
            identifier = _attribute(element, "Id", "ID")
            if identifier:
                self._definitions[(_local_name(element.tag), identifier)] = element

    @classmethod
    def _flat(cls, element: ET.Element | None) -> tuple[tuple[str, str], ...]:
        if element is None:
            return ()
        values: list[tuple[str, str]] = []
        for node in element.iter():
            tag = _local_name(node.tag).casefold()
            for key, value in node.attrib.items():
                name = key.rsplit("}", 1)[-1].casefold()
                if name in cls._IGNORED:
                    continue
                values.append((f"{tag}.{name}", str(value).strip().casefold()))
            if node is not element and not node.attrib and not list(node):
                values.append((f"{tag}.present", "true"))
        return tuple(sorted(set(values)))

    def _reference(self, element: ET.Element, tag: str, *names: str) -> ET.Element | None:
        identifier = _attribute(element, *names)
        if identifier is None:
            for node in element.iter():
                identifier = _attribute(node, *names)
                if identifier is not None:
                    break
        return self._definitions.get((tag, identifier)) if identifier is not None else None

    def fingerprint(self, cell: ET.Element) -> CellStyleFingerprint:
        paragraph = next((e for e in cell.iter() if _local_name(e.tag) == "P"), None)
        character = next(
            (e for e in cell.iter() if _local_name(e.tag) in {"CHAR", "TEXT"}),
            None,
        )
        border = self._reference(cell, "BORDERFILL", "BorderFill", "BorderFillId")
        para_shape = (
            self._reference(paragraph, "PARASHAPE", "ParaShape", "ParaShapeId")
            if paragraph is not None else None
        )
        char_shape = (
            self._reference(character, "CHARSHAPE", "CharShape", "CharShapeId")
            if character is not None else None
        )
        cell_values = tuple(sorted(set((*self._flat(cell)[:0], *self._flat(border)))))
        # 셀 자체에서는 크기·주소와 참조 ID를 제외한 직접 속성만 사용한다.
        direct = tuple(
            sorted(
                (
                    key.rsplit("}", 1)[-1].casefold(),
                    str(value).strip().casefold(),
                )
                for key, value in cell.attrib.items()
                if key.rsplit("}", 1)[-1].casefold() not in self._IGNORED
                and "borderfill" not in key.casefold()
            )
        )
        cell_values = tuple(sorted(set((*direct, *cell_values))))
        paragraph_values = self._flat(para_shape)
        character_values = self._flat(char_shape)
        payload = json.dumps(
            [cell_values, paragraph_values, character_values],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        signature = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]
        return CellStyleFingerprint(signature, cell_values, paragraph_values, character_values)


_INLINE_PATTERN = re.compile(
    r"(?P<label>[^\r\n:\uff1a]{1,60}?)\s*[:\uff1a]\s*"
    r"(?P<value>[^\r\n]+?)\s*$",
    re.MULTILINE,
)
_VALUE_PATTERNS = (
    re.compile(r"^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$"),
    re.compile(r"^(?:\+?\d[\d .()/-]{5,}\d)$"),
    re.compile(
        r"^(?:19|20)\d{2}\s*[./-]\s*\d{1,2}"
        r"(?:\s*[./-]\s*\d{1,2})?\.?$"
    ),
    re.compile(r"^[\d,]+(?:\.\d+)?\s*(?:\uc6d0|\uba85|\uac1c|\uac74|%|\uc5b5\uc6d0|\ub9cc\uc6d0)?$"),
)
_COMMON_LABELS = {
    "\uad6c\ubd84", "\ud56d\ubaa9", "\ub0b4\uc6a9", "\ube44\uace0", "\ud569\uacc4", "\ucd1d\uacc4", "\uc774\ub984", "\uc131\uba85", "\uc131\ud568",
    "\uacfc\uc81c\uba85", "\uc0ac\uc5c5\uba85", "\ud504\ub85c\uc81d\ud2b8\uba85", "\uae30\uad00\uba85", "\ubd80\uc11c\uba85", "\uc18c\uc18d",
    "\ubd80\uc11c", "\uc9c1\uc704", "\uc9c1\uae09", "\uc8fc\uc18c", "\uc804\ud654", "\uc804\ud654\ubc88\ud638", "\uc5f0\ub77d\ucc98",
    "\ud734\ub300\uc804\ud654", "\uc774\uba54\uc77c", "\uc804\uc790\uc6b0\ud3b8", "\ucc45\uc784\uc790", "\uc5f0\uad6c\ucc45\uc784\uc790",
    "\uc5f0\uad6c\uc790", "\ub2f4\ub2f9\uc790", "\ub300\ud45c\uc790", "\uc791\uc131\uc790", "\uc2e0\uccad\uc778", "\uc81c\ubaa9", "\uc8fc\uc81c",
    "\ubaa9\uc801", "\uae30\uac04", "\uc2dc\uc791\uc77c", "\uc885\ub8cc\uc77c", "\uc77c\uc790", "\ub0a0\uc9dc", "\uae08\uc561", "\uc218\ub7c9",
    "\ub2e8\uac00", "\uc5f0\ub3c4", "\ub144\ub3c4", "\ucf54\ub4dc", "\ubc88\ud638", "\uc720\ud615", "\uc885\ub958",
    "\uad6d\ubb38", "\uc601\ubb38", "\uc9c1\uc7a5\uc804\ud654", "\uc5ed\ud560", "\uae30\uad00\uc720\ud615", "\ud604\uae08", "\ud604\ubb3c",
    "\uc804\uccb4", "\uc815\ubd80\uc9c0\uc6d0\uc5f0\uad6c\uac1c\ubc1c\ube44", "\uae30\uad00\ubd80\ub2f4\uc5f0\uad6c\uac1c\ubc1c\ube44",
    "\uadf8 \uc678 \uae30\uad00 \ub4f1\uc758 \uc9c0\uc6d0\uae08", "\uad6d\uac00\uacfc\ud559\uae30\uc220\ud45c\uc900\ubd84\ub958",
    "\uc9c0\ubc29\uc790\uce58\ub2e8\uccb4", "\uae30\ud0c0(\ud611\ub825\uae30\uc5c5)",
}
_COMMON_LABEL_KEYS = {_normalized_label(label) for label in _COMMON_LABELS}
_LABEL_SUFFIXES = tuple(
    sorted(
        _COMMON_LABELS
        - {"\ud56d\ubaa9", "\uc804\ud654", "\ud734\ub300\uc804\ud654", "\uc804\uc790\uc6b0\ud3b8"},
        key=len,
        reverse=True,
    )
)
_GENERIC_CONTEXT_LABELS = {
    "\uc774\ub984", "\uc131\uba85", "\uc131\ud568", "\uba85\uce6d", "\ubc88\ud638", "\uae30\uac04", "\uc77c\uc790", "\ub0a0\uc9dc",
    "\uae08\uc561", "\ub0b4\uc6a9", "\uad6c\ubd84", "\uc5f0\ub77d\ucc98", "\uc804\ud654", "\uc804\ud654\ubc88\ud638", "\uc9c1\uc7a5\uc804\ud654",
    "\ud734\ub300\uc804\ud654", "\uc804\uc790\uc6b0\ud3b8", "\uc774\uba54\uc77c", "\uc9c1\uc704", "\uc9c1\uae09", "\uc18c\uc18d", "\ubd80\uc11c",
    "\ubd80\uc11c\uba85", "\uae30\uad00\uba85", "\uc8fc\uc18c", "\uc0ac\uc5c5\uc790\ubc88\ud638", "\uc0ac\uc5c5\uc790\ub4f1\ub85d\ubc88\ud638",
    "\uad6d\uac00\uc5f0\uad6c\uc790\ubc88\ud638", "\uc720\ud615", "\uc885\ub958", "\ucf54\ub4dc",
}
_LOCAL_CONTEXT_QUALIFIERS = {
    "\uad6d\ubb38",
    "\uc601\ubb38",
    "\uc9c1\uc7a5\uc804\ud654",
    "\uc804\uccb4",
    "\ud604\uae08",
    "\ud604\ubb3c",
}
_DISTINCT_CONTEXT_LABELS = {
    *_LOCAL_CONTEXT_QUALIFIERS,
    "\ud734\ub300\uc804\ud654",
}
_ROLE_PATTERN = re.compile(
    r"(?:\uc5f0\uad6c\ucc45\uc784\uc790|\ucd1d\uad04\ucc45\uc784\uc790|\ucc45\uc784\uc790|\ucc38\uc5ec\uc5f0\uad6c\uc790|"
    r"\uc5f0\uad6c\uc790|\ub2f4\ub2f9\uc790|\ub300\ud45c\uc790|\uc791\uc131\uc790|\uc2e0\uccad\uc778)"
)
_PLACEHOLDER_PATTERN = re.compile(r"^[\s\-\u2010-\u2015_\u00b7\u2022]+$")
_PERIOD_HEADER_PATTERN = re.compile(
    r"^(?:\uc81c\s*)?\d+\s*(?:\ub2e8\uacc4|\ucc28\ub144\ub3c4|\ub144\ucc28|\ucc28)$"
)
_STRUCTURAL_HEADER_PATTERNS = (
    _PERIOD_HEADER_PATTERN,
    re.compile(
        r"^(?:(?:\uc8fc\uad00|\uacf5\ub3d9|\uc704\ud0c1|\ucc38\uc5ec|\uc804\ubb38)\s*)?"
        r"\uc5f0\uad6c\uac1c\ubc1c\uae30\uad00(?:\s*\(?\ud574\ub2f9\s*\uc2dc\)?)?$"
    ),
)
_GROUP_HEADER_PATTERN = re.compile(
    r"(?:\uae30\uad00|\uae30\uc5c5|\ub2e8\uccb4|\ubd80\uc11c|\uacfc\uc81c|\uc0ac\uc5c5|\uc5f0\uad6c\uac1c\ubc1c\ube44|"
    r"\uc5f0\uad6c\ucc45\uc784\uc790|\ucc45\uc784\uc790|\uc5f0\uad6c\uc790|\ub2f4\ub2f9\uc790|\ub300\ud45c\uc790|\uc791\uc131\uc790|"
    r"\uc2e0\uccad\uc778|\uc5f0\ub77d\ucc98|\uc8fc\uc18c|\uc815\ubcf4|\ud604\ud669)$"
)
_CONTEXT_SEPARATOR = " > "
_CONTEXT_MAX_PARAGRAPHS = 3
_CONTEXT_MAX_PARAGRAPH_LENGTH = 80
_CONTEXT_MAX_TOTAL_LENGTH = 160
_CONTEXT_MAX_SPACES = 12
_CONTEXT_REGION_TAGS = frozenset(
    {
        "CAPTION",
        "DRAWING",
        "DRAWINGOBJECT",
        "ENDNOTE",
        "FOOTER",
        "FOOTNOTE",
        "GSO",
        "HEADER",
        "MEMO",
        "NOTE",
        "SHAPE",
        "SHAPEOBJECT",
        "TEXTBOX",
    }
)
_CONTEXT_FALLBACK_REGION_TAGS = frozenset({"SECTION", "BODY"})
_CONTEXT_BREAK_TAGS = frozenset({"COLUMNBREAK", "PAGEBREAK", "SECTIONBREAK"})
_CONTEXT_SENTENCE_END_PATTERN = re.compile(
    r"(?:[.!?。！？]|"
    r"(?:습니다|합니다|됩니다|있습니다|없습니다|"
    r"하세요|하십시오|바랍니다|한다|된다|이다))$"
)


class HWPMLTableFieldAnalyzer:
    """Infer field/value pairs from each label cell in HWPML2X tables."""

    def analyze(
        self,
        hwpml: str,
        registered_fields: Iterable[str] | Mapping[str, object] = (),
        aliases: Mapping[str, Iterable[str]] | None = None,
        registered_values: Mapping[str, object] | Sequence[object] | None = None,
    ) -> HWPMLTableAnalysis:
        if not isinstance(hwpml, str) or not hwpml.strip():
            raise ValueError("Selected HWPML is empty.")
        try:
            root = ET.fromstring(hwpml.lstrip("\ufeff"))
        except ET.ParseError as error:
            raise ValueError(f"Selected HWPML cannot be parsed: {error}") from error

        value_entries = self._registered_value_entries(registered_values)
        value_fields = tuple(entry.field for entry in value_entries)
        if isinstance(registered_fields, Mapping):
            registry_fields: Iterable[str] | Mapping[str, object] = {
                **registered_fields,
                **{field: None for field in value_fields},
            }
        elif isinstance(registered_fields, (str, bytes)):
            registry_fields = (str(registered_fields), *value_fields)
        else:
            registry_fields = (*registered_fields, *value_fields)
        registry = _FieldRegistry(registry_fields, aliases)
        parents, paths, order = self._tree_indexes(root)
        style_resolver = _StyleResolver(root)
        tables = [element for element in root.iter() if _local_name(element.tag) == "TABLE"]
        candidates: list[FieldValueCandidate] = []
        scan_regions: list[_ScanRegion] = []

        for table_index, table in enumerate(tables):
            cells = self._table_cells(table, parents, paths, style_resolver)
            if not cells:
                continue
            table_candidate_start = len(candidates)
            scan_regions.extend(
                _ScanRegion(
                    table_index,
                    cell.row,
                    cell.col,
                    cell.content,
                    self._is_probable_header(cell, cells, registry),
                    cell.style,
                )
                for cell in cells
            )
            context_title = self._nearby_title(root, table, parents, order)
            local_context_cells: dict[int, _Cell] = {}
            merged_parent_elements: set[int] = set()
            for cell in cells:
                parent_cell = self._local_context_cell(cell, cells, registry)
                if parent_cell is not None:
                    local_context_cells[id(cell.element)] = parent_cell
                    merged_parent_elements.add(id(parent_cell.element))
            # 병합 셀이라고 모두 대표필드는 아니다. ``성명 | 홍길동``의
            # '성명'처럼 폭이 넓은 하위필드도 병합 셀일 수 있다. 반면
            # 자신의 자식 중 다시 다른 셀의 부모가 되는 셀이 있으면
            # ``연락처 > 직장전화 > 값`` 같은 실제 중간 그룹이다.
            context_child_counts: dict[int, int] = {}
            context_children: dict[int, list[_Cell]] = {}
            context_parent_cells: dict[int, _Cell] = {}
            cells_by_element_id = {id(cell.element): cell for cell in cells}
            for child_element_id, parent_cell in local_context_cells.items():
                parent_id = id(parent_cell.element)
                child_cell = cells_by_element_id[child_element_id]
                context_children.setdefault(parent_id, []).append(child_cell)
                context_parent_cells[parent_id] = parent_cell
            for parent_cell in local_context_cells.values():
                parent_id = id(parent_cell.element)
                context_child_counts[parent_id] = context_child_counts.get(parent_id, 0) + 1
            # 하나의 병합 셀이 여러 셀을 직접 지배하면 그 셀은 값을 가진
            # 하위필드가 아니라 하위필드들을 묶는 그룹 제목이다. 한 셀만
            # 지배하는 병합 라벨은 ``성명 -> 홍길동``처럼 정상 필드다.
            nested_group_elements = {
                parent_id
                for parent_id, child_count in context_child_counts.items()
                if child_count > 1
            }
            for parent_id, child_cells in context_children.items():
                if len(child_cells) != 1:
                    continue
                child_cell = child_cells[0]
                child_relations = self._structural_relations(
                    child_cell,
                    cells,
                    context_parent_cells[parent_id],
                )
                usable_child_relations = tuple(
                    relation
                    for relation in child_relations
                    if id(relation.value_cell.element) not in merged_parent_elements
                    and not self._is_placeholder(relation.value_cell.text)
                    and _normalized_label(child_cell.text)
                    != _normalized_label(relation.value_cell.text)
                )
                if (
                    any(
                        relation.direction == "below"
                        and child_cell.style.signature
                        != relation.value_cell.style.signature
                        for relation in usable_child_relations
                    )
                    and not any(
                        relation.direction == "right"
                        for relation in usable_child_relations
                    )
                ):
                    # 대표필드가 하위필드 하나만 가지는 경우도 있다.
                    # 그 하위필드가 다시 아래의 실제 값과 연결되면 부모는
                    # 값 후보가 아니라 1개짜리 그룹으로 유지한다.
                    nested_group_elements.add(parent_id)
            consumed_value_cells: set[int] = set()
            for label_cell in cells:
                local_parent = local_context_cells.get(id(label_cell.element))
                if (
                    id(label_cell.element) in consumed_value_cells
                    or (
                        id(label_cell.element) in merged_parent_elements
                        and local_parent is None
                    )
                    or id(label_cell.element) in nested_group_elements
                ):
                    continue
                local_context = local_parent.text if local_parent is not None else None
                inline_relations = self._inline_relations(label_cell)
                if inline_relations:
                    for inline_index, (label, relation) in enumerate(inline_relations, 1):
                        canonical, alias_collision = registry.resolve(label)
                        if (
                            _normalized_label(label) in {"http", "https"}
                            or (
                                local_context is None
                                and self._label_score(
                                    label,
                                    bool(canonical),
                                    alias_collision,
                                ) < 0.62
                            )
                        ):
                            continue
                        candidate = self._candidate(
                            registry,
                            table_index,
                            label_cell,
                            label,
                            relation,
                            context_title,
                            local_context,
                            inline_index,
                            local_parent,
                        )
                        if candidate is not None:
                            if local_context is not None:
                                candidate = replace(
                                    candidate,
                                    confidence=max(0.95, candidate.confidence),
                                    recommended=candidate.label != candidate.value,
                                    classification_basis="merged_structure",
                                )
                            candidates.append(candidate)
                            # 한 번 값으로 확정된 셀은 뒤에서 다시 필드로
                            # 해석하지 않는다. 병합 구조 안에서도 동일하다.
                            if local_context is not None or relation.recommendable:
                                consumed_value_cells.add(id(relation.value_cell.element))
                    continue

                label = label_cell.text
                canonical, alias_collision = registry.resolve(label)
                label_score = self._label_score(label, bool(canonical), alias_collision)
                if label_score < 0.62 and local_context is None:
                    continue
                relations = (
                    self._structural_relations(label_cell, cells, local_parent)
                    if local_context is not None
                    else (
                        self._best_relation(
                            label_cell,
                            cells,
                            registry,
                            max(label_score, 0.62),
                        ),
                    )
                )
                if local_context is not None:
                    usable_relations = tuple(
                        relation
                        for relation in relations
                        if relation is not None
                        and id(relation.value_cell.element) not in merged_parent_elements
                        and not self._is_placeholder(relation.value_cell.text)
                        and _normalized_label(label)
                        != _normalized_label(relation.value_cell.text)
                    )
                    # 가로형 표에서 오른쪽 값을 찾았으면 그 필드/값 쌍으로
                    # 끝낸다. 같은 라벨에서 다음 행의 하위필드까지 값으로
                    # 연결하지 않는다. 오른쪽 값이 없을 때만 세로형을 쓴다.
                    right_relations = tuple(
                        relation
                        for relation in usable_relations
                        if relation.direction == "right"
                    )
                    relations = right_relations or tuple(
                        relation
                        for relation in usable_relations
                        if relation.direction == "below"
                    )
                for relation_index, relation in enumerate(relations, 1):
                    if relation is None:
                        continue
                    # 다른 셀들을 지배하는 병합 셀은 값이 아니라 대표/중간
                    # 필드다. 이를 값으로 받아들이면 ``정부지원비 -> 기관부담비``
                    # 같은 필드명 연쇄가 다시 만들어진다.
                    if id(relation.value_cell.element) in merged_parent_elements:
                        continue
                    if (
                        local_context is not None
                        and label_cell.rowspan > 1
                        and label_cell.style.signature
                        == relation.value_cell.style.signature
                    ):
                        # 여러 행을 묶고 다음 셀과 동일한 필드 서식을 쓰는
                        # 셀은 ``1단계 > 1년차`` 같은 중간 그룹이다.
                        # 하위필드 이름을 값으로 소비하지 않는다.
                        continue
                    candidate = self._candidate(
                        registry,
                        table_index,
                        label_cell,
                        label,
                        relation,
                        context_title,
                        local_context,
                        relation_index,
                        local_parent,
                    )
                    if candidate is None:
                        continue
                    if local_context is not None:
                        candidate = replace(
                            candidate,
                            confidence=max(0.95, candidate.confidence),
                            recommended=candidate.label != candidate.value,
                            classification_basis="merged_structure",
                        )
                    candidates.append(candidate)
                    # 필드/값 쌍은 여기서 종결한다. 값 셀을 다음 필드의
                    # 라벨로 재사용하면 반복 계층이 만들어진다.
                    if local_context is not None or relation.recommendable:
                        consumed_value_cells.add(id(relation.value_cell.element))

            # 문서 안에서 이미 확실히 판별된 라벨/값 셀의 시각 서식을
            # 학습 표본으로 사용한다. 크기·방향이 다른 셀이어도 같은 실제
            # 셀/문단/글자 서명이면 의미가 불명확한 라벨을 보조 판별한다.
            table_candidates = candidates[table_candidate_start:]
            field_styles = {
                item.label_style.signature
                for item in table_candidates
                if item.label_style is not None and item.recommended
            }
            value_styles = {
                item.value_style.signature
                for item in table_candidates
                if item.value_style is not None and item.recommended
            }
            distinctive_field_styles = field_styles - value_styles
            distinctive_value_styles = value_styles - field_styles
            known_labels = {
                (item.row, item.col) for item in table_candidates
            }
            if distinctive_field_styles and distinctive_value_styles:
                for style_cell in cells:
                    if (
                        not style_cell.text
                        or (style_cell.row, style_cell.col) in known_labels
                        or id(style_cell.element) in consumed_value_cells
                        or style_cell.style.signature not in distinctive_field_styles
                    ):
                        continue
                    relation = self._best_relation(style_cell, cells, registry, 0.72)
                    if (
                        relation is None
                        or relation.value_cell.style.signature not in distinctive_value_styles
                    ):
                        continue
                    style_parent = self._local_context_cell(
                        style_cell,
                        cells,
                        registry,
                    )
                    style_candidate = self._candidate(
                        registry,
                        table_index,
                        style_cell,
                        style_cell.text,
                        relation,
                        context_title,
                        style_parent.text if style_parent is not None else None,
                        1,
                        style_parent,
                    )
                    if style_candidate is None:
                        continue
                    candidates.append(
                        replace(
                            style_candidate,
                            confidence=round(min(0.91, max(0.8, style_candidate.confidence)), 2),
                            recommended=relation.recommendable,
                            classification_basis="cell_style",
                        )
                    )
                    if relation.recommendable:
                        consumed_value_cells.add(id(relation.value_cell.element))

        paragraph_index = 0
        for paragraph in root.iter():
            if _local_name(paragraph.tag) != "P":
                continue
            if self._nearest_ancestor(paragraph, parents, "TABLE") is not None:
                continue
            content = self._paragraph_content(paragraph, parents, paths)
            paragraph_cell = _Cell(
                paragraph,
                paragraph_index,
                0,
                1,
                1,
                content,
                style_resolver.fingerprint(paragraph),
            )
            scan_regions.append(
                _ScanRegion(
                    -1,
                    paragraph_index,
                    0,
                    content,
                    probable_header=False,
                    style=paragraph_cell.style,
                )
            )
            paragraph_index += 1
            for inline_index, (label, relation) in enumerate(
                self._inline_relations(paragraph_cell),
                1,
            ):
                canonical, collision = registry.resolve(label)
                label_score = self._label_score(label, bool(canonical), collision)
                if label_score < 0.62 or _normalized_label(label) in {"http", "https"}:
                    continue
                explicit_enough = canonical is not None or label_score >= 0.74
                paragraph_relation = replace(
                    relation,
                    recommendable=relation.recommendable and explicit_enough,
                )
                candidate = self._candidate(
                    registry,
                    -1,
                    paragraph_cell,
                    label,
                    paragraph_relation,
                    None,
                    None,
                    inline_index,
                )
                if candidate is not None:
                    candidates.append(
                        replace(
                            candidate,
                            candidate_id=(
                                f"p{paragraph_cell.row:04d}-inline-o{inline_index:02d}"
                            ),
                        )
                    )

        candidates.extend(
            self._registered_value_candidates(scan_regions, value_entries)
        )

        unique: list[FieldValueCandidate] = []
        seen: dict[tuple[object, ...], int] = {}
        for candidate in candidates:
            key = (
                candidate.field.casefold(),
                tuple(
                    (segment.element_path, segment.text_slot, segment.start, segment.end)
                    for segment in candidate.locator.segments
                ),
            )
            existing_index = seen.get(key)
            if existing_index is not None:
                existing = unique[existing_index]
                if existing.profile_field_id is None and candidate.profile_field_id:
                    unique[existing_index] = replace(
                        existing,
                        profile_field_id=candidate.profile_field_id,
                    )
                continue
            seen[key] = len(unique)
            unique.append(candidate)

        unique = self._resolve_recommendation_overlaps(unique)

        registered = tuple(candidate for candidate in unique if candidate.registered)
        unregistered = tuple(candidate for candidate in unique if not candidate.registered)
        style_rules = {
            "field": tuple(sorted({
                candidate.label_style.signature
                for candidate in unique
                if candidate.label_style is not None and candidate.recommended
            })),
            "value": tuple(sorted({
                candidate.value_style.signature
                for candidate in unique
                if candidate.value_style is not None and candidate.recommended
            })),
        }
        return HWPMLTableAnalysis(registered, unregistered, style_rules)

    def find_exact_value(
        self,
        hwpml: str,
        value: str,
        field: str,
        profile_field_id: str | None = None,
    ) -> tuple[FieldValueCandidate, ...]:
        """Locate an explicitly chosen value without inference safeguards.

        This is the manual-selection counterpart to :meth:`analyze`.  It does
        not apply word boundaries, placeholder rejection, or label heuristics;
        every exact occurrence in a table cell or a non-table paragraph is
        returned with ``recommended=False`` for the caller to select.
        """

        if not isinstance(hwpml, str) or not hwpml.strip():
            raise ValueError("Selected HWPML is empty.")
        exact_value = str(value)
        canonical_field = str(field).strip()
        if not exact_value:
            raise ValueError("The exact value is empty.")
        if not canonical_field:
            raise ValueError("The canonical field is empty.")
        clean_profile_id = (
            str(profile_field_id).strip() if profile_field_id is not None else ""
        ) or None
        try:
            root = ET.fromstring(hwpml.lstrip("\ufeff"))
        except ET.ParseError as error:
            raise ValueError(f"Selected HWPML cannot be parsed: {error}") from error

        parents, paths, _ = self._tree_indexes(root)
        style_resolver = _StyleResolver(root)
        regions: list[_ScanRegion] = []
        tables = [element for element in root.iter() if _local_name(element.tag) == "TABLE"]
        for table_index, table in enumerate(tables):
            for cell in self._table_cells(table, parents, paths, style_resolver):
                regions.append(
                    _ScanRegion(
                        table_index,
                        cell.row,
                        cell.col,
                        cell.content,
                        probable_header=False,
                        style=cell.style,
                    )
                )

        paragraph_index = 0
        for paragraph in root.iter():
            if _local_name(paragraph.tag) != "P":
                continue
            if self._nearest_ancestor(paragraph, parents, "TABLE") is not None:
                continue
            regions.append(
                _ScanRegion(
                    -1,
                    paragraph_index,
                    0,
                    self._paragraph_content(paragraph, parents, paths),
                    probable_header=False,
                    style=style_resolver.fingerprint(paragraph),
                )
            )
            paragraph_index += 1

        result: list[FieldValueCandidate] = []
        for region_index, region in enumerate(regions):
            start_at = 0
            while True:
                start = region.content.text.find(exact_value, start_at)
                if start < 0:
                    break
                end = start + len(exact_value)
                start_at = start + 1
                segments = region.content.segments(start, end)
                if "".join(segment.text for segment in segments) != exact_value:
                    continue
                occurrence = self._occurrence(region.content.text, exact_value, start)
                scope = "p" if region.table < 0 else f"t{region.table:03d}-"
                candidate_id = (
                    f"exact-{scope}r{region.row:04d}-c{region.col:04d}-"
                    f"s{region_index:04d}-o{occurrence:02d}"
                )
                locator = ValueLocator(
                    table_index=region.table,
                    row=region.row,
                    col=region.col,
                    value_text=exact_value,
                    occurrence=occurrence,
                    segments=segments,
                )
                result.append(
                    FieldValueCandidate(
                        candidate_id=candidate_id,
                        field=canonical_field,
                        label=canonical_field,
                        value=exact_value,
                        table=region.table,
                        row=region.row,
                        col=region.col,
                        value_row=region.row,
                        value_col=region.col,
                        direction="inline",
                        confidence=0.99,
                        registered=True,
                        recommended=False,
                        context_title=None,
                        locator=locator,
                        profile_field_id=clean_profile_id,
                        value_style=region.style,
                        classification_basis="manual",
                    )
                )
        return tuple(result)

    # Existing application services expose Korean verbs; keep both call styles.
    분석 = analyze
    정확값찾기 = find_exact_value

    @classmethod
    def _registered_value_entries(
        cls,
        source: Mapping[str, object] | Sequence[object] | None,
    ) -> tuple[_RegisteredValue, ...]:
        """Normalize both profile value maps and richer field definitions.

        The application's current ``필드값목록()`` shape is
        ``{canonical_name: (value, ...)}``.  A caller that also has stable
        profile IDs may instead pass records such as
        ``{"id": "...", "대표필드명": "...", "값목록": [...]}``.
        """

        if source is None:
            return ()

        field_keys = (
            "대표필드명",
            "canonical_field",
            "canonical",
            "field",
            "필드명",
            "name",
        )
        value_keys = (
            "값목록",
            "values",
            "registered_values",
            "value",
            "값",
            "기본값",
        )
        id_keys = ("profile_field_id", "id", "필드ID", "field_id")

        records: list[tuple[str | None, object]] = []
        if isinstance(source, Mapping):
            # A mapping is always canonical-name -> value definition.  Rich
            # standalone definitions belong in a sequence; this keeps valid
            # canonical names such as "name" and "values" unambiguous.
            records.extend((str(field), raw) for field, raw in source.items())
        elif isinstance(source, (str, bytes)):
            return ()
        else:
            records.extend((None, raw) for raw in source)

        result: list[_RegisteredValue] = []
        for fallback_field, raw in records:
            field: object | None = fallback_field
            profile_field_id: object | None = None
            raw_values: object = raw

            if isinstance(raw, Mapping):
                field = next(
                    (raw[key] for key in field_keys if key in raw and raw[key] is not None),
                    fallback_field,
                )
                profile_field_id = next(
                    (raw[key] for key in id_keys if key in raw and raw[key] is not None),
                    None,
                )
                selected_values = [raw[key] for key in value_keys if key in raw]
                raw_values = selected_values if selected_values else ()
            elif fallback_field is None:
                field = next(
                    (getattr(raw, key) for key in field_keys if hasattr(raw, key)),
                    None,
                )
                profile_field_id = next(
                    (getattr(raw, key) for key in id_keys if hasattr(raw, key)),
                    None,
                )
                selected_values = [
                    getattr(raw, key) for key in value_keys if hasattr(raw, key)
                ]
                raw_values = selected_values

            clean_field = str(field).strip() if field is not None else ""
            if not clean_field:
                continue
            clean_id = (
                str(profile_field_id).strip() if profile_field_id is not None else ""
            ) or None

            flattened: list[object] = []

            def collect_values(value: object) -> None:
                if value is None:
                    return
                if isinstance(value, (str, bytes)):
                    flattened.append(value)
                    return
                if isinstance(value, Mapping):
                    flattened.extend(value.values())
                    return
                if isinstance(value, Sequence):
                    for item in value:
                        collect_values(item)
                    return
                flattened.append(value)

            collect_values(raw_values)
            for raw_value in flattened:
                value = str(raw_value).strip()
                if value and not cls._is_placeholder(value):
                    result.append(_RegisteredValue(clean_field, value, clean_id))

        ids_by_field: dict[str, set[str]] = {}
        for entry in result:
            if entry.profile_field_id:
                ids_by_field.setdefault(entry.field.casefold(), set()).add(
                    entry.profile_field_id
                )
        conflicting_id_fields = [
            field for field, ids in ids_by_field.items() if len(ids) > 1
        ]
        if conflicting_id_fields:
            raise ValueError(
                "One canonical field cannot have multiple profile field IDs."
            )

        deduplicated = {
            (entry.field.casefold(), entry.value, entry.profile_field_id): entry
            for entry in result
        }
        return tuple(
            sorted(
                deduplicated.values(),
                key=lambda entry: (
                    entry.field.casefold(),
                    -len(entry.value),
                    entry.value,
                    entry.profile_field_id or "",
                ),
            )
        )

    @classmethod
    def _registered_value_candidates(
        cls,
        regions: Sequence[_ScanRegion],
        entries: Sequence[_RegisteredValue],
    ) -> list[FieldValueCandidate]:
        if not entries:
            return []

        owners_by_value: dict[str, list[tuple[int, _RegisteredValue]]] = {}
        for entry_index, entry in enumerate(entries):
            owners_by_value.setdefault(entry.value, []).append((entry_index, entry))

        result: list[FieldValueCandidate] = []
        values = sorted(owners_by_value, key=lambda value: (-len(value), value))
        for region_index, region in enumerate(regions):
            text = region.content.text
            if not text:
                continue
            for value in values:
                start_at = 0
                occurrence = 0
                while True:
                    start = text.find(value, start_at)
                    if start < 0:
                        break
                    end = start + len(value)
                    start_at = start + 1
                    if not cls._has_value_boundaries(text, start, end):
                        continue
                    segments = region.content.segments(start, end)
                    if not segments or "".join(segment.text for segment in segments) != value:
                        continue
                    occurrence = cls._occurrence(text, value, start)
                    owners = owners_by_value[value]
                    unambiguous = len({entry.field.casefold() for _, entry in owners}) == 1
                    safe_length = len(value.strip()) >= 2 and not (
                        value.isdigit() and len(value) < 4
                    )
                    recommendable = (
                        unambiguous
                        and safe_length
                        and not region.probable_header
                        and not cls._is_placeholder(value)
                    )
                    confidence = 0.86 if recommendable else 0.68
                    locator = ValueLocator(
                        table_index=region.table,
                        row=region.row,
                        col=region.col,
                        value_text=value,
                        occurrence=occurrence,
                        segments=segments,
                    )
                    scope = "p" if region.table < 0 else f"t{region.table:03d}-"
                    for owner_index, entry in owners:
                        candidate_id = (
                            f"rv-{scope}r{region.row:04d}-c{region.col:04d}-"
                            f"s{region_index:04d}-o{occurrence:02d}-f{owner_index:04d}"
                        )
                        result.append(
                            FieldValueCandidate(
                                candidate_id=candidate_id,
                                field=entry.field,
                                label=entry.field,
                                value=value,
                                table=region.table,
                                row=region.row,
                                col=region.col,
                                value_row=region.row,
                                value_col=region.col,
                                direction="inline",
                                confidence=confidence,
                                registered=True,
                                recommended=recommendable,
                                context_title=None,
                                locator=locator,
                                profile_field_id=entry.profile_field_id,
                                value_style=region.style,
                                classification_basis="registered_value",
                            )
                        )
        return result

    @staticmethod
    def _has_value_boundaries(text: str, start: int, end: int) -> bool:
        """Reject a saved value found only inside a longer word or number."""

        def word_character(character: str) -> bool:
            return character.isalnum() or character == "_"

        if start > 0 and word_character(text[start]) and word_character(text[start - 1]):
            return False
        if end < len(text) and word_character(text[end - 1]) and word_character(text[end]):
            return False
        numeric_separators = "-./"
        if (
            start > 0
            and text[start].isdigit()
            and text[start - 1] in numeric_separators
        ):
            return False
        if (
            end < len(text)
            and text[end - 1].isdigit()
            and text[end] in numeric_separators
        ):
            return False
        return True

    @classmethod
    def _resolve_recommendation_overlaps(
        cls,
        candidates: Sequence[FieldValueCandidate],
    ) -> list[FieldValueCandidate]:
        """Keep every inferred candidate but make default selections disjoint.

        One candidate can span several XML text/tail slots. Direct conflicts
        are therefore detected from exact locator intervals, not from equal
        values or equal table coordinates. Candidates are considered from the
        strongest rank down, and only a candidate that directly overlaps an
        already selected candidate is suppressed. This lets two disjoint
        candidates survive even when a weaker candidate overlaps both of them.
        A direct exact-rank tie is intentionally left to the user.
        """

        if len(candidates) < 2:
            return list(candidates)

        adjacency: list[set[int]] = [set() for _ in candidates]
        by_slot: dict[
            tuple[tuple[int, ...], str],
            list[tuple[int, int, int]],
        ] = {}
        for candidate_index, candidate in enumerate(candidates):
            if not candidate.recommended:
                continue
            for segment in candidate.locator.segments:
                if segment.start >= segment.end:
                    continue
                key = (segment.element_path, segment.text_slot)
                by_slot.setdefault(key, []).append(
                    (segment.start, segment.end, candidate_index)
                )

        for intervals in by_slot.values():
            intervals.sort(key=lambda item: (item[0], item[1], item[2]))
            active: list[tuple[int, int, int]] = []
            for start, end, candidate_index in intervals:
                active = [item for item in active if item[1] > start]
                for other_start, other_end, other_index in active:
                    if other_index == candidate_index:
                        continue
                    if max(start, other_start) < min(end, other_end):
                        adjacency[candidate_index].add(other_index)
                        adjacency[other_index].add(candidate_index)
                active.append((start, end, candidate_index))

        eligible = [
            index for index, candidate in enumerate(candidates) if candidate.recommended
        ]
        ranks = {
            index: (
                2
                if candidates[index].classification_basis == "merged_structure"
                else (1 if candidates[index].registered else 0),
                candidates[index].confidence,
            )
            for index in eligible
        }
        rank_groups: dict[tuple[int, float], list[int]] = {}
        for index in eligible:
            rank_groups.setdefault(ranks[index], []).append(index)

        selected: set[int] = set()
        for rank in sorted(rank_groups, reverse=True):
            available = [
                index
                for index in rank_groups[rank]
                if adjacency[index].isdisjoint(selected)
            ]
            tied = {
                index
                for index in available
                if any(
                    other != index and other in adjacency[index]
                    for other in available
                )
            }
            selected.update(index for index in available if index not in tied)

        resolved = list(candidates)
        for index in eligible:
            should_recommend = index in selected
            if resolved[index].recommended != should_recommend:
                resolved[index] = replace(
                    resolved[index],
                    recommended=should_recommend,
                )
        return resolved

    @staticmethod
    def _tree_indexes(
        root: ET.Element,
    ) -> tuple[
        dict[ET.Element, ET.Element],
        dict[ET.Element, tuple[int, ...]],
        dict[ET.Element, int],
    ]:
        parents: dict[ET.Element, ET.Element] = {}
        paths: dict[ET.Element, tuple[int, ...]] = {root: ()}
        order: dict[ET.Element, int] = {}
        sequence = 0

        def visit(element: ET.Element) -> None:
            nonlocal sequence
            order[element] = sequence
            sequence += 1
            for index, child in enumerate(list(element)):
                parents[child] = element
                paths[child] = (*paths[element], index)
                visit(child)

        visit(root)
        return parents, paths, order

    @staticmethod
    def _nearest_ancestor(
        element: ET.Element,
        parents: Mapping[ET.Element, ET.Element],
        tag_name: str,
    ) -> ET.Element | None:
        current = parents.get(element)
        while current is not None:
            if _local_name(current.tag) == tag_name:
                return current
            current = parents.get(current)
        return None

    def _table_cells(
        self,
        table: ET.Element,
        parents: Mapping[ET.Element, ET.Element],
        paths: Mapping[ET.Element, tuple[int, ...]],
        style_resolver: _StyleResolver,
    ) -> list[_Cell]:
        raw_cells = [
            element
            for element in table.iter()
            if _local_name(element.tag) == "CELL"
            and self._nearest_ancestor(element, parents, "TABLE") is table
        ]
        if not raw_cells:
            return []

        row_elements = [
            element
            for element in table.iter()
            if _local_name(element.tag) == "ROW"
            and self._nearest_ancestor(element, parents, "TABLE") is table
        ]
        row_indexes = {row: index for index, row in enumerate(row_elements)}
        occupied: set[tuple[int, int]] = set()
        row_cursors: dict[int, int] = {}
        result: list[_Cell] = []

        for cell in raw_cells:
            row = _non_negative_int(_attribute(cell, "RowAddr", "Row", "RowIndex"))
            col = _non_negative_int(_attribute(cell, "ColAddr", "Col", "ColIndex"))
            row_element = self._nearest_ancestor(cell, parents, "ROW")
            if row is None:
                row = row_indexes.get(row_element, 0)
            rowspan = _positive_int(_attribute(cell, "RowSpan", "rowspan"), 1)
            colspan = _positive_int(_attribute(cell, "ColSpan", "colspan"), 1)
            explicit_col = col is not None
            if col is None:
                col = row_cursors.get(row, 0)
                while any((covered_row, col) in occupied for covered_row in range(row, row + rowspan)):
                    col += 1
            while any(
                (covered_row, covered_col) in occupied
                for covered_row in range(row, row + rowspan)
                for covered_col in range(col, col + colspan)
            ):
                if explicit_col:
                    break
                col += 1
            for covered_row in range(row, row + rowspan):
                for covered_col in range(col, col + colspan):
                    occupied.add((covered_row, covered_col))
            row_cursors[row] = max(row_cursors.get(row, 0), col + colspan)
            result.append(
                _Cell(
                    element=cell,
                    row=row,
                    col=col,
                    rowspan=rowspan,
                    colspan=colspan,
                    content=self._cell_content(cell, table, parents, paths),
                    style=style_resolver.fingerprint(cell),
                )
            )
        return sorted(result, key=lambda item: (item.row, item.col))

    def _cell_content(
        self,
        cell: ET.Element,
        table: ET.Element,
        parents: Mapping[ET.Element, ET.Element],
        paths: Mapping[ET.Element, tuple[int, ...]],
    ) -> _CellContent:
        chars = [
            element
            for element in cell.iter()
            if _local_name(element.tag) == "CHAR"
            and self._nearest_ancestor(element, parents, "CELL") is cell
            and self._nearest_ancestor(element, parents, "TABLE") is table
        ]
        pieces: list[tuple[ET.Element, Literal["text", "tail"], str]] = []

        def collect(element: ET.Element, include_tail: bool) -> None:
            if element.text:
                pieces.append((element, "text", element.text))
            for child in element:
                if self._nearest_ancestor(child, parents, "TABLE") is table:
                    collect(child, True)
            if include_tail and element.tail:
                pieces.append((element, "tail", element.tail))

        if chars:
            for char in chars:
                collect(char, False)
        else:
            # Tolerate small HWPML fixtures that omit CHAR.
            for element in cell.iter():
                if self._nearest_ancestor(element, parents, "TABLE") is not table:
                    continue
                if element.text and element.text.strip() and not list(element):
                    pieces.append((element, "text", element.text))
                if element is not cell and element.tail and element.tail.strip():
                    pieces.append((element, "tail", element.tail))

        text_parts: list[str] = []
        slots: list[_TextSlot] = []
        offset = 0
        seen_slots: set[tuple[int, str]] = set()
        for element, slot_name, text in pieces:
            key = (id(element), slot_name)
            if key in seen_slots:
                continue
            seen_slots.add(key)
            text_parts.append(text)
            slots.append(
                _TextSlot(
                    element_path=paths[element],
                    text_slot=slot_name,
                    text=text,
                    global_start=offset,
                    global_end=offset + len(text),
                )
            )
            offset += len(text)
        return _CellContent("".join(text_parts), tuple(slots))

    def _paragraph_content(
        self,
        paragraph: ET.Element,
        parents: Mapping[ET.Element, ET.Element],
        paths: Mapping[ET.Element, tuple[int, ...]],
    ) -> _CellContent:
        chars = [
            element
            for element in paragraph.iter()
            if _local_name(element.tag) == "CHAR"
            and self._nearest_ancestor(element, parents, "P") is paragraph
            and self._nearest_ancestor(element, parents, "TABLE") is None
        ]
        pieces: list[tuple[ET.Element, Literal["text", "tail"], str]] = []

        def collect(element: ET.Element, include_tail: bool) -> None:
            if element.text:
                pieces.append((element, "text", element.text))
            for child in element:
                if (
                    _local_name(child.tag) != "TABLE"
                    and self._nearest_ancestor(child, parents, "TABLE") is None
                ):
                    collect(child, True)
            if include_tail and element.tail:
                pieces.append((element, "tail", element.tail))

        for char in chars:
            collect(char, False)
        if not chars:
            # Tolerate simplified HWPML fixtures that omit CHAR while keeping
            # the same exact text/tail locator model as real documents.
            collect(paragraph, False)

        offset = 0
        slots: list[_TextSlot] = []
        text_parts: list[str] = []
        seen: set[tuple[int, str]] = set()
        for element, slot_name, text in pieces:
            key = (id(element), slot_name)
            if key in seen:
                continue
            seen.add(key)
            text_parts.append(text)
            slots.append(
                _TextSlot(
                    paths[element],
                    slot_name,
                    text,
                    offset,
                    offset + len(text),
                )
            )
            offset += len(text)
        return _CellContent("".join(text_parts), tuple(slots))

    def _nearby_title(
        self,
        root: ET.Element,
        table: ET.Element,
        parents: Mapping[ET.Element, ET.Element],
        order: Mapping[ET.Element, int],
    ) -> str | None:
        table_order = order[table]
        table_region = self._context_region(table, parents)
        table_ancestors: set[ET.Element] = set()
        current = parents.get(table)
        while current is not None:
            table_ancestors.add(current)
            current = parents.get(current)

        events: list[_ContextEvent] = []
        for element in root.iter():
            element_order = order[element]
            if element_order >= table_order:
                break
            tag_name = _local_name(element.tag)
            if tag_name not in {"P", "TABLE", *_CONTEXT_BREAK_TAGS}:
                continue
            if self._context_region(element, parents) is not table_region:
                continue
            if tag_name in _CONTEXT_BREAK_TAGS:
                events.append(_ContextEvent(element_order, "break"))
                continue
            if self._nearest_ancestor(element, parents, "TABLE") is not None:
                continue
            if tag_name == "TABLE":
                events.append(_ContextEvent(element_order, "table"))
                continue
            break_before, outline_level = self._paragraph_context_metadata(root, element)
            # A TABLE is commonly wrapped by a P in real HWPML. Reading that
            # wrapper would also read content after the table and reverse its
            # meaning into a title, so it is never a title candidate.
            if element in table_ancestors:
                if break_before:
                    events.append(_ContextEvent(element_order, "break"))
                continue
            events.append(
                _ContextEvent(
                    element_order,
                    "paragraph",
                    self._standalone_text(element),
                    break_before,
                    outline_level,
                )
            )

        # Read backwards from the table so an intervening table, body
        # paragraph, or independent region is a hard boundary.  Up to three
        # contiguous heading-like paragraphs form an outer-to-inner context,
        # for example "research lead > contact information".
        reverse_parts: list[str] = []
        seen: set[str] = set()
        blank_count = 0
        total_length = 0
        reverse_levels: list[int | None] = []
        selected_roles: set[str] = set()
        for event in reversed(events):
            if event.kind in {"table", "break"}:
                break
            text = event.text
            if not text:
                if event.break_before:
                    break
                blank_count += 1
                if blank_count > 1:
                    break
                continue
            if not self._is_context_paragraph(text):
                break

            normalized = _normalized_label(text)
            if normalized in seen:
                if event.break_before:
                    break
                continue
            current_roles = {
                match.group(0) for match in _ROLE_PATTERN.finditer(text)
            }
            if reverse_parts and not self._can_prepend_context(
                text,
                event.outline_level,
                reverse_parts[-1],
                reverse_levels[-1],
                current_roles,
                selected_roles,
            ):
                break
            added_length = len(text) + (len(_CONTEXT_SEPARATOR) if reverse_parts else 0)
            if total_length + added_length > _CONTEXT_MAX_TOTAL_LENGTH:
                break
            seen.add(normalized)
            reverse_parts.append(text)
            reverse_levels.append(event.outline_level)
            selected_roles.update(current_roles)
            total_length += added_length
            if event.break_before or len(reverse_parts) >= _CONTEXT_MAX_PARAGRAPHS:
                break

        reverse_parts.reverse()
        return _CONTEXT_SEPARATOR.join(reverse_parts) or None

    @staticmethod
    def _context_region(
        element: ET.Element,
        parents: Mapping[ET.Element, ET.Element],
    ) -> ET.Element | None:
        """Return the nearest independent text region containing *element*."""

        current: ET.Element | None = element
        fallback: ET.Element | None = None
        while current is not None:
            tag_name = _local_name(current.tag)
            if tag_name in _CONTEXT_REGION_TAGS:
                return current
            if fallback is None and tag_name in _CONTEXT_FALLBACK_REGION_TAGS:
                fallback = current
            current = parents.get(current)
        return fallback

    @staticmethod
    def _truthy_attribute(element: ET.Element, *names: str) -> bool:
        value = _attribute(element, *names)
        return value is not None and value.strip().casefold() not in {
            "",
            "0",
            "false",
            "no",
            "none",
            "off",
        }

    @classmethod
    def _paragraph_context_metadata(
        cls,
        root: ET.Element,
        paragraph: ET.Element,
    ) -> tuple[bool, int | None]:
        break_before = cls._truthy_attribute(
            paragraph,
            "PageBreak",
            "PageBreakBefore",
            "ColumnBreak",
            "SectionBreak",
        )
        outline_level = _non_negative_int(
            _attribute(paragraph, "OutlineLevel", "HeadingLevel")
        )
        heading_type = (_attribute(paragraph, "HeadingType") or "").casefold()
        if outline_level is None and "outline" in heading_type:
            outline_level = _non_negative_int(_attribute(paragraph, "Level"))

        shape_reference = _attribute(
            paragraph,
            "ParaShape",
            "ParaShapeID",
            "ParaShapeIdRef",
        )
        if shape_reference is None:
            return break_before, outline_level
        reference = shape_reference.strip()
        for element in root.iter():
            if _local_name(element.tag) != "PARASHAPE":
                continue
            if (_attribute(element, "Id", "ParaShapeID") or "").strip() != reference:
                continue
            break_before = break_before or cls._truthy_attribute(
                element,
                "PageBreak",
                "PageBreakBefore",
                "ColumnBreak",
                "SectionBreak",
            )
            shape_heading_type = (_attribute(element, "HeadingType") or "").casefold()
            if outline_level is None and "outline" in shape_heading_type:
                outline_level = _non_negative_int(
                    _attribute(element, "Level", "OutlineLevel", "HeadingLevel")
                )
            break
        return break_before, outline_level

    @staticmethod
    def _can_prepend_context(
        older_text: str,
        older_level: int | None,
        inner_text: str,
        inner_level: int | None,
        older_roles: set[str],
        selected_roles: set[str],
    ) -> bool:
        if older_roles and selected_roles and older_roles != selected_roles:
            return False
        if older_level is not None and inner_level is not None:
            return older_level < inner_level
        if older_level is not None:
            return True
        if inner_level is not None:
            return False
        if older_roles and not selected_roles:
            return True

        normalized = _normalized_label(older_text)
        return bool(_GROUP_HEADER_PATTERN.search(normalized)) or any(
            pattern.fullmatch(normalized) for pattern in _STRUCTURAL_HEADER_PATTERNS
        )

    def _is_context_paragraph(self, text: str) -> bool:
        if (
            len(text) > _CONTEXT_MAX_PARAGRAPH_LENGTH
            or text.count(" ") > _CONTEXT_MAX_SPACES
            or self._is_placeholder(text)
            or any(pattern.fullmatch(text) for pattern in _VALUE_PATTERNS)
            or _INLINE_PATTERN.fullmatch(text)
        ):
            return False
        return not bool(_CONTEXT_SENTENCE_END_PATTERN.search(text))

    def _local_context_cell(
        self,
        label_cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> _Cell | None:
        """Find the smallest merged header governing this label cell."""

        contexts: list[tuple[int, int, int, int, _Cell]] = []
        for cell in cells:
            if cell is label_cell or not cell.text:
                continue
            covers_row_from_left = (
                cell.col_end <= label_cell.col
                and cell.row <= label_cell.row < cell.row_end
                and cell.rowspan > 1
                and self._has_structural_children_right(cell, cells)
            )
            covers_col_from_top = (
                cell.row_end == label_cell.row
                and cell.col <= label_cell.col
                and cell.col_end >= label_cell.col_end
                and cell.colspan > 1
                and not any(
                    other is not cell
                    and other.text
                    and other.col == cell.col_end
                    and other.row == cell.row
                    and other.row_end > cell.row_end
                    for other in cells
                )
                and (
                    cell.rowspan > 1
                    or cell.colspan > label_cell.colspan
                    or bool(
                        _GROUP_HEADER_PATTERN.search(
                            _normalized_label(cell.text)
                        )
                    )
                )
            )
            if not covers_row_from_left and not covers_col_from_top:
                continue
            area = cell.rowspan * cell.colspan
            distance = (
                label_cell.col - cell.col_end
                if covers_row_from_left
                else label_cell.row - cell.row_end
            )
            # Smaller merged regions are the more specific local context.
            direction_priority = 0 if covers_col_from_top else 1
            same_row_left_priority = int(
                not (covers_row_from_left and cell.row == label_cell.row)
            )
            contexts.append(
                (same_row_left_priority, area, distance, direction_priority, cell)
            )
        if not contexts:
            return None
        # 사용자가 말하는 대표필드는 문맥 제목이 아니라 해당 라벨을
        # 직접 지배하는 병합 셀이다. 중첩 병합이 있으면 가장 작고 가까운
        # 병합 셀 하나만 부모로 택해 1단계 대표필드→하위필드를 유지한다.
        return min(
            contexts,
            key=lambda item: (
                item[0],
                item[1],
                item[2],
                item[3],
                -item[4].row,
                -item[4].col,
            ),
        )[4]

    def _local_context(
        self,
        label_cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> str | None:
        parent = self._local_context_cell(label_cell, cells, registry)
        return parent.text if parent is not None else None

    @staticmethod
    def _has_structural_children_right(
        merged_cell: _Cell,
        cells: Sequence[_Cell],
    ) -> bool:
        """Use only grid geometry to distinguish a group from a merged value pair."""

        children = [
            other
            for other in cells
            if other is not merged_cell
            and other.col == merged_cell.col_end
            and merged_cell.row <= other.row < merged_cell.row_end
        ]
        return len(children) >= 2 or any(
            child.rowspan < merged_cell.rowspan for child in children
        )

    def _has_direct_right_value(
        self,
        cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> bool:
        neighbors = [
            other
            for other in cells
            if other is not cell
            and other.text
            and other.col == cell.col_end
            and other.row < cell.row_end
            and other.row_end > cell.row
        ]
        if not neighbors:
            return False
        neighbor = min(neighbors, key=lambda other: (other.row, other.col))
        return not self._is_probable_header(neighbor, cells, registry)

    @staticmethod
    def _standalone_text(element: ET.Element) -> str:
        parts: list[str] = []

        def collect(current: ET.Element) -> None:
            if _local_name(current.tag) == "TABLE":
                return
            if current.text and (_local_name(current.tag) == "CHAR" or current.text.strip()):
                parts.append(current.text)
            for child in current:
                collect(child)
                if child.tail and child.tail.strip():
                    parts.append(child.tail)

        collect(element)
        return _display_text("".join(parts))

    @staticmethod
    def _inline_relations(cell: _Cell) -> list[tuple[str, _Relation]]:
        result: list[tuple[str, _Relation]] = []
        for match in _INLINE_PATTERN.finditer(cell.content.text):
            label = _field_name(match.group("label"))
            value_start, value_end = match.span("value")
            while value_end > value_start and cell.content.text[value_end - 1].isspace():
                value_end -= 1
            value = cell.content.text[value_start:value_end]
            parenthesized_unit = (
                label.count("(") > label.count(")") and value.rstrip().endswith(")")
            )
            if label and value_start < value_end and not parenthesized_unit:
                result.append(
                    (label, _Relation(cell, "inline", 0.96, value_start, value_end))
                )
        return result

    @staticmethod
    def _structural_relations(
        label_cell: _Cell,
        cells: Sequence[_Cell],
        structural_parent: _Cell | None,
    ) -> tuple[_Relation, ...]:
        """Return every exact adjacent relation inside a merged-cell group.

        A merged layout can legitimately continue both to the right and below.
        The review screen, not this analyzer, decides which relation the user
        wants to keep. Blank and placeholder values are rejected later by
        ``_candidate``.
        """

        relations: list[_Relation] = []
        right = [
            cell
            for cell in cells
            if cell is not label_cell
            and cell.text
            and cell.col == label_cell.col_end
            and cell.row < label_cell.row_end
            and cell.row_end > label_cell.row
        ]
        if right:
            cell = min(right, key=lambda item: (item.row, item.col))
            start, end = cell.content.trimmed_range()
            relations.append(
                _Relation(cell, "right", 0.96, start, end, recommendable=True)
            )

        if structural_parent is None or label_cell.row_end >= structural_parent.row_end:
            below = [
                cell
                for cell in cells
                if cell is not label_cell
                and cell.text
                and cell.row == label_cell.row_end
                and cell.col == label_cell.col
                and cell.col_end == label_cell.col_end
            ]
            if below:
                cell = min(below, key=lambda item: (item.col, item.row))
                if not relations or relations[0].value_cell is not cell:
                    start, end = cell.content.trimmed_range()
                    relations.append(
                        _Relation(
                            cell,
                            "below",
                            0.96,
                            start,
                            end,
                            recommendable=True,
                        )
                    )
        return tuple(relations)

    def _best_relation(
        self,
        label_cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
        label_score: float,
        *,
        structural_group: bool = False,
        structural_parent: _Cell | None = None,
    ) -> _Relation | None:
        options: list[_Relation] = []
        structural_below: _Cell | None = None
        if structural_group and (
            structural_parent is None
            or label_cell.row_end >= structural_parent.row_end
        ):
            immediate_below = [
                cell
                for cell in cells
                if cell is not label_cell
                and cell.text
                and cell.row == label_cell.row_end
                and cell.col == label_cell.col
                and cell.col_end == label_cell.col_end
            ]
            if immediate_below:
                structural_below = min(
                    immediate_below,
                    key=lambda item: (item.col, item.row),
                )
        right = [
            cell
            for cell in cells
            if cell is not label_cell
            and cell.text
            and cell.col == label_cell.col_end
            and cell.row < label_cell.row_end
            and cell.row_end > label_cell.row
        ]
        right_relation: _Relation | None = None
        if structural_group:
            structural_right = (
                min(
                    right,
                    key=lambda item: (
                        item.col - label_cell.col_end,
                        item.row,
                        item.col,
                    ),
                )
                if right
                else None
            )
            cell = structural_right
            direction = "right"
            if structural_below is not None and (
                structural_right is None
                or (
                    label_cell.style.signature
                    == structural_right.style.signature
                    and label_cell.style.signature
                    != structural_below.style.signature
                )
            ):
                cell = structural_below
                direction = "below"
            if cell is None:
                return None
            start, end = cell.content.trimmed_range()
            return _Relation(
                cell,
                direction,
                0.96,
                start,
                end,
                recommendable=True,
            )
        if right:
            cell = min(right, key=lambda item: (item.col - label_cell.col_end, item.row, item.col))
            distance = max(0, cell.col - label_cell.col_end)
            is_header = self._is_probable_header(cell, cells, registry)
            ambiguous_run = (
                not is_header
                and self._has_additional_right_value(cell, cells, registry)
            )
            recommendable = not is_header and not ambiguous_run
            score = 0.87 - min(distance, 3) * 0.04 + (label_score - 0.62) * 0.08
            start, end = cell.content.trimmed_range()
            right_relation = _Relation(
                cell,
                "right",
                score if recommendable else min(score, 0.69),
                start,
                end,
                recommendable=recommendable,
            )

        below = [
            cell
            for cell in cells
            if cell is not label_cell
            and cell.text
            and cell.row == label_cell.row_end
            and cell.col < label_cell.col_end
            and cell.col_end > label_cell.col
        ]
        below_relation: _Relation | None = None
        if below:
            cell = min(below, key=lambda item: (item.row - label_cell.row_end, item.col, item.row))
            distance = max(0, cell.row - label_cell.row_end)
            is_header = self._is_probable_header(cell, cells, registry)
            recommendable = not is_header and distance == 0
            score = 0.83 - min(distance, 3) * 0.04 + (label_score - 0.62) * 0.08
            start, end = cell.content.trimmed_range()
            below_relation = _Relation(
                cell,
                "below",
                score if recommendable else min(score, 0.69),
                start,
                end,
                recommendable=recommendable,
            )

        if right_relation is not None and not right_relation.recommendable:
            group_header = self._is_group_header(label_cell, cells, registry)
            if (
                not group_header
                and below_relation is not None
                and below_relation.recommendable
            ):
                return below_relation
            return right_relation
        if right_relation is not None:
            options.append(right_relation)
        if below_relation is not None:
            options.append(below_relation)
        if not options:
            return None
        return max(options, key=lambda relation: relation.score)

    def _is_probable_header(
        self,
        cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> bool:
        if self._is_placeholder(cell.text):
            return False
        canonical, collision = registry.resolve(cell.text)
        score = self._label_score(cell.text, bool(canonical), collision)
        if score >= 0.74:
            return True
        if score < 0.62:
            return False
        if self._is_structural_group_header(cell, cells, registry):
            return True
        immediate_right = [
            other
            for other in cells
            if other is not cell
            and other.text
            and other.col == cell.col_end
            and other.row < cell.row_end
            and other.row_end > cell.row
        ]
        if not immediate_right:
            return False
        neighbor = min(immediate_right, key=lambda item: (item.row, item.col))
        neighbor_canonical, neighbor_collision = registry.resolve(neighbor.text)
        neighbor_score = self._label_score(
            neighbor.text,
            bool(neighbor_canonical),
            neighbor_collision,
        )
        return neighbor_score < 0.62 or any(
            pattern.fullmatch(neighbor.text) for pattern in _VALUE_PATTERNS
        )

    def _is_structural_group_header(
        self,
        cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> bool:
        lexical_group = bool(_GROUP_HEADER_PATTERN.search(_field_name(cell.text)))
        if cell.rowspan > 1 and lexical_group:
            children = [
                other
                for other in cells
                if other is not cell
                and other.text
                and other.col == cell.col_end
                and cell.row <= other.row < cell.row_end
            ]
            if any(
                self._label_score(
                    other.text,
                    bool(registry.resolve(other.text)[0]),
                    registry.resolve(other.text)[1],
                )
                >= 0.62
                for other in children
            ):
                return True

        if cell.colspan <= 1:
            return False
        children = [
            other
            for other in cells
            if other is not cell
            and other.text
            and other.row == cell.row_end
            and other.col >= cell.col
            and other.col_end <= cell.col_end
        ]
        header_children = 0
        for other in children:
            canonical, collision = registry.resolve(other.text)
            if self._label_score(other.text, bool(canonical), collision) >= 0.62:
                header_children += 1
        return header_children >= (2 if lexical_group else 3)

    def _is_group_header(
        self,
        cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> bool:
        if cell.rowspan <= 1:
            return False
        return any(
            other is not cell
            and other.text
            and other.col >= cell.col_end
            and cell.row <= other.row < cell.row_end
            and self._is_probable_header(other, cells, registry)
            for other in cells
        )

    def _has_additional_right_value(
        self,
        value_cell: _Cell,
        cells: Sequence[_Cell],
        registry: _FieldRegistry,
    ) -> bool:
        later = sorted(
            (
                other
                for other in cells
                if other is not value_cell
                and other.text
                and other.col >= value_cell.col_end
                and other.row < value_cell.row_end
                and other.row_end > value_cell.row
            ),
            key=lambda item: (item.col, item.row),
        )
        for other in later:
            if self._is_probable_header(other, cells, registry):
                return False
            if not self._is_placeholder(other.text):
                return True
        return False

    @staticmethod
    def _label_score(label: str, registered: bool, alias_collision: bool = False) -> float:
        text = _field_name(_display_text(label))
        if not text or len(text) > 60:
            return 0.0
        if registered:
            return 1.0
        if alias_collision:
            return 0.88
        if any(pattern.fullmatch(text) for pattern in _VALUE_PATTERNS):
            return 0.0
        if any(pattern.fullmatch(text) for pattern in _STRUCTURAL_HEADER_PATTERNS):
            return 0.9
        if _normalized_label(text) in _COMMON_LABEL_KEYS:
            return 0.9
        if any(text.endswith(suffix) for suffix in _LABEL_SUFFIXES):
            return 0.8
        if any(char in text for char in ("?", "!", ".", "\u3002")):
            return 0.15
        if any(char.isdigit() for char in text):
            return 0.25
        if len(text.split()) <= 3 and len(text) <= 18:
            return 0.64
        return 0.35

    def _candidate(
        self,
        registry: _FieldRegistry,
        table_index: int,
        label_cell: _Cell,
        label: str,
        relation: _Relation,
        context_title: str | None,
        local_context: str | None,
        ordinal: int,
        structural_parent: _Cell | None = None,
    ) -> FieldValueCandidate | None:
        segments = relation.value_cell.content.segments(
            relation.value_start,
            relation.value_end,
        )
        if not segments:
            return None
        value = "".join(segment.text for segment in segments)
        if not value.strip() or self._is_placeholder(value):
            return None
        field, registered, alias_collision = self._resolve_candidate_field(
            registry,
            label,
            context_title,
            local_context,
        )
        if not field:
            return None
        confidence = relation.score
        if registered:
            confidence += 0.03
        elif context_title:
            confidence += 0.02
        if alias_collision:
            confidence -= 0.12
        confidence = round(max(0.0, min(confidence, 0.99)), 2)
        occurrence = self._occurrence(
            relation.value_cell.content.text,
            value,
            relation.value_start,
        )
        locator = ValueLocator(
            table_index=table_index,
            row=relation.value_cell.row,
            col=relation.value_cell.col,
            value_text=value,
            occurrence=occurrence,
            segments=segments,
        )
        candidate_id = (
            f"t{table_index:03d}-r{label_cell.row:03d}-c{label_cell.col:03d}-"
            f"{relation.direction}-vr{relation.value_cell.row:03d}-"
            f"vc{relation.value_cell.col:03d}-o{ordinal:02d}"
        )
        if structural_parent is not None:
            structural_group_id = (
                f"t{table_index:03d}-parent-r{structural_parent.row:03d}-"
                f"c{structural_parent.col:03d}-rs{structural_parent.rowspan:03d}-"
                f"cs{structural_parent.colspan:03d}"
            )
        elif table_index >= 0:
            structural_group_id = (
                f"t{table_index:03d}-pair-r{label_cell.row:03d}-"
                f"c{label_cell.col:03d}"
            )
        else:
            structural_group_id = f"p{label_cell.row:04d}"
        return FieldValueCandidate(
            candidate_id=candidate_id,
            field=field,
            label=_field_name(label),
            value=value,
            table=table_index,
            row=label_cell.row,
            col=label_cell.col,
            value_row=relation.value_cell.row,
            value_col=relation.value_cell.col,
            direction=relation.direction,
            confidence=confidence,
            registered=registered,
            recommended=(
                confidence >= 0.8
                and not alias_collision
                and relation.recommendable
                and not self._is_placeholder(label)
                and not self._is_placeholder(value)
                and _normalized_label(label) != _normalized_label(value)
            ),
            context_title=context_title,
            locator=locator,
            parent_field=_field_name(local_context) if local_context else None,
            field_path=field,
            label_style=label_cell.style,
            value_style=relation.value_cell.style,
            structural_group_id=structural_group_id,
            structural_parent_field=(
                _field_name(structural_parent.text)
                if structural_parent is not None
                else None
            ),
            structural_parent_row=(
                structural_parent.row if structural_parent is not None else None
            ),
            structural_parent_col=(
                structural_parent.col if structural_parent is not None else None
            ),
        )

    @staticmethod
    def _occurrence(haystack: str, needle: str, start: int) -> int:
        count = 0
        offset = 0
        while True:
            found = haystack.find(needle, offset)
            if found < 0 or found > start:
                break
            count += 1
            if found == start:
                break
            offset = found + 1
        return max(1, count)

    @staticmethod
    def _resolve_candidate_field(
        registry: _FieldRegistry,
        label: str,
        context_title: str | None,
        local_context: str | None,
    ) -> tuple[str, bool, bool]:
        clean_label = _field_name(label)
        title_role = HWPMLTableFieldAnalyzer._role_context(context_title)
        # 계층은 오직 실제 병합 셀에서만 만든다. 병합 셀이 대표필드,
        # 그 범위의 라벨 셀이 하위필드이며 문서 제목/본문 문맥은 부모로
        # 사용하지 않는다.
        if local_context:
            parent_label = _field_name(local_context)
            direct_path = f"{parent_label}{_CONTEXT_SEPARATOR}{clean_label}"
            canonical, direct_collision = registry.resolve(direct_path)
            if canonical is not None:
                return canonical, True, False
            # 부모와 하위 이름은 실제 병합 셀/라벨 셀의 표시문구를 보존한다.
            # 전역 별칭으로 정규화하면 '직장전화'와 '휴대전화'가 둘 다
            # '전화번호'로 뭉개져 서로 다른 하위 필드를 잃게 된다.
            return direct_path, False, direct_collision

        # 병합 셀이 없는 경우 제목은 평면 필드 이름을 보조하는 데만 쓴다.
        # 제목을 근거로 임의의 부모/자식 관계를 만들지는 않는다.
        if clean_label in {"\uc774\ub984", "\uc131\uba85", "\uc131\ud568"}:
            if title_role:
                canonical, collision = registry.resolve(title_role)
                if canonical is not None:
                    return canonical, True, False
                return title_role, False, collision

        # A merged row/column group is a namespace for generic child fields.
        # For example, two person blocks must not both collapse into the global
        # "phone number" token.  Prefer an already registered contextual field;
        # otherwise propose a new canonical such as "research lead phone".
        if title_role and clean_label in _GENERIC_CONTEXT_LABELS:
            leaf_canonical, leaf_collision = registry.resolve(label)
            leaf = (
                clean_label
                if clean_label in _DISTINCT_CONTEXT_LABELS
                else leaf_canonical or clean_label
            )
            contextual_field = f"{title_role} {leaf}".strip()
            canonical, context_collision = registry.resolve(contextual_field)
            if canonical is not None:
                return canonical, True, False
            return (
                contextual_field,
                False,
                leaf_collision or context_collision,
            )

        canonical, collision = registry.resolve(label)
        if canonical is not None:
            return canonical, True, False
        return HWPMLTableFieldAnalyzer._suggest_field(label, context_title), False, collision

    @staticmethod
    def _role_context(context: str | None) -> str | None:
        if not context:
            return None
        context_parts = HWPMLTableFieldAnalyzer._context_parts(context)
        role_parts = [part for part in context_parts if _ROLE_PATTERN.search(part)]
        if len(role_parts) == 1:
            context = role_parts[0]
        clean = re.sub(
            r"\s*(?:\uc815\ubcf4|\ud604\ud669|\ub0b4\uc6a9|\ud56d\ubaa9)\s*$",
            "",
            _field_name(context),
        ).strip()
        roles = list(dict.fromkeys(match.group(0) for match in _ROLE_PATTERN.finditer(clean)))
        if len(roles) != 1:
            return None
        role = roles[0]
        if clean.endswith(role) and len(clean) <= 60:
            return clean
        return role

    @staticmethod
    def _context_parts(context: str) -> tuple[str, ...]:
        return tuple(
            clean
            for part in context.split(_CONTEXT_SEPARATOR)
            if (clean := _field_name(part))
        )

    @staticmethod
    def _is_placeholder(value: str) -> bool:
        return bool(_PLACEHOLDER_PATTERN.fullmatch(value.strip()))

    @staticmethod
    def _suggest_field(label: str, context_title: str | None) -> str:
        clean_label = _field_name(label)
        if not context_title or clean_label not in _GENERIC_CONTEXT_LABELS:
            return clean_label
        clean_context = re.sub(
            r"\s*(?:\uc815\ubcf4|\ud604\ud669|\ub0b4\uc6a9|\ud56d\ubaa9)\s*$",
            "",
            context_title,
        ).strip()
        return f"{clean_context} {clean_label}".strip()


__all__ = [
    "FieldValueCandidate",
    "HWPMLTableAnalysis",
    "HWPMLTableFieldAnalyzer",
    "TextSlotLocator",
    "ValueLocator",
    "HWPML표필드분석기",
]


HWPML표필드분석기 = HWPMLTableFieldAnalyzer
