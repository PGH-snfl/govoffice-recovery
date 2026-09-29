"""Rebind one saved response packet to a reanalysed copy of the same HWP form.

The source packet is never modified.  Only paragraph-identical prose and the
explicitly reviewed relocations below are inserted into the new form.  Factual
and personal cells receive saved user values only; omitted prose is retained in
the packet's migration record so it cannot silently disappear.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from govoffice.services.document_authoring import TemplateRegistry, read_json, write_json
from govoffice.services.saved_authoring_responses import (
    FORMAT, binding_hash, load_bundle, prepare_bundle,
)


# These moves were checked against the original form's heading and paragraph
# indices.  Do not infer moves from similar-looking field names.
RELOCATIONS = {
    "P0433": ("P0434", "P0435"),  # Domestic and overseas competitors.
    "P0437": ("P0438", "P0439"),  # Patent status and analysis plan.
    "P0441": ("P0442", "P0443"),  # Domestic and overseas certification.
    "P0502": ("P0506",),          # Core technology.
    "P0561": ("P0562",),          # Business strategy.
}
APPENDS = {
    "P0356": ("P0369",),  # Summary detail remains in the summary's whole-content cell.
}


def adapt(bundle, old_manifest, new_manifest, source_digest):
    old_identity = bundle.get("template", {})
    # The original job snapshot later acquired a few empty compatibility
    # fields.  Project it back to exactly the fields exported in the packet,
    # then require the packet's binding hash to match that projection.
    old_manifest = deepcopy(old_manifest)
    for topic in old_manifest["topics"]:
        response = bundle.get("responses", {}).get(topic["id"], {})
        exported = set(response.get("values", {}))
        known = {field["id"] for field in topic["fields"]}
        if not exported <= known:
            raise ValueError("기존 응답의 필드가 양식 기록에 없습니다: " + topic["id"])
        topic["fields"] = [field for field in topic["fields"] if field["id"] in exported]
    if (
        old_identity.get("source_sha256") != old_manifest.get("source_sha256")
        or old_identity.get("native_sha256") != old_manifest.get("native_sha256")
        or old_identity.get("binding_sha256") != binding_hash(old_manifest)
    ):
        raise ValueError("기존 응답과 기존 양식의 입력 위치가 일치하지 않습니다.")
    if old_manifest["native_sha256"] != new_manifest["native_sha256"]:
        raise ValueError("두 양식의 원본 한글 파일이 다릅니다. 위치 기준으로 옮길 수 없습니다.")

    old_fields = {}
    old_by_id = {}
    for topic in old_manifest["topics"]:
        response = bundle["responses"].get(topic["id"])
        if not isinstance(response, dict):
            raise ValueError("기존 응답의 소주제가 누락되었습니다: " + topic["id"])
        for field in topic["fields"]:
            value = response["values"].get(field["id"])
            if not isinstance(value, str):
                raise ValueError("기존 응답의 입력값이 누락되었습니다: " + field["id"])
            item = (topic, field, value)
            if field["index"] in old_fields or field["id"] in old_by_id:
                raise ValueError("기존 양식에 중복 입력 위치가 있습니다.")
            old_fields[field["index"]] = item
            old_by_id[field["id"]] = item

    new_fields = {f["id"]: f for t in new_manifest["topics"] for f in t["fields"]}
    local_values = {}
    for field_id, value in bundle.get("local_values", {}).items():
        if field_id in new_fields:
            old_field = old_by_id.get(field_id)
            if old_field and old_field[1]["index"] == new_fields[field_id]["index"]:
                local_values[field_id] = value
    # The project title was supplied as the writing brief, not inferred from
    # a table or an AI claim.  Preserve it in the new factual title cell.
    title = bundle.get("brief", {}).get("title", "")
    old_title = old_by_id.get("P0309")
    if title and old_title and old_title[2].strip() == title.strip() and "P0309" in new_fields:
        local_values["P0309"] = title.strip()

    consumed = set(local_values)
    copied = []
    relocated = []
    responses = {}
    for topic in new_manifest["topics"]:
        values = {}
        notes = list(bundle["responses"].get(topic["id"], {}).get("needs_review", []))
        for field in topic["fields"]:
            field_id = field["id"]
            value = local_values.get(field_id, "")
            if field.get("role") == "body":
                previous = old_fields.get(field["index"])
                if previous and previous[1].get("role") == "body":
                    value = previous[2]
                    consumed.add(previous[1]["id"])
                    copied.append(field_id)
                    if field_id in APPENDS:
                        for old_id in APPENDS[field_id]:
                            extra = old_by_id.get(old_id)
                            if not extra or extra[1].get("role") != "body":
                                raise ValueError("검증된 기존 추가 문단이 없습니다: " + old_id)
                            if extra[2].strip():
                                value = value.rstrip() + "\n\n" + extra[2].strip()
                            consumed.add(old_id)
                        relocated.append({"to": field_id, "from": list(APPENDS[field_id])})
                elif field_id in RELOCATIONS:
                    pieces = []
                    for old_id in RELOCATIONS[field_id]:
                        previous = old_by_id.get(old_id)
                        if not previous or previous[1].get("role") != "body":
                            raise ValueError("검증된 기존 본문 위치가 없습니다: " + old_id)
                        if previous[2].strip():
                            pieces.append(previous[2].strip())
                        consumed.add(old_id)
                    value = "\n\n".join(pieces)
                    relocated.append({"to": field_id, "from": list(RELOCATIONS[field_id])})
                if not value.strip():
                    value = "확인 필요"
                    notes.append(field["label"] + ": 기존 응답에 이 위치의 본문이 없습니다.")
            if len(value) > field["max_chars"]:
                raise ValueError(f"{field_id}: 새 양식의 최대 길이를 초과합니다. 내용을 임의로 자르지 않았습니다.")
            values[field_id] = value
        responses[topic["id"]] = {
            "topic_id": topic["id"], "values": values,
            "needs_review": list(dict.fromkeys(notes)),
        }

    unplaced = []
    for _, (topic, field, value) in old_fields.items():
        if field.get("role") != "body" or field["id"] in consumed:
            continue
        if not value.strip() or re.fullmatch(r"\[?확인\s*필요\]?", value.strip()):
            continue
        unplaced.append({
            "topic_id": topic["id"], "topic_title": topic["title"],
            "field_id": field["id"], "label": field.get("label", ""),
            "text": value, "reason": "새 양식에 안전하게 대응되는 본문 입력칸이 없음",
        })

    valid_topics = {t["id"] for t in new_manifest["topics"]}
    research = {key: value for key, value in bundle.get("research", {}).items()
                if key in valid_topics}
    result = {
        "format": FORMAT, "version": 1,
        "exported_at": datetime.now().astimezone().isoformat(),
        "source_job_id": bundle.get("source_job_id"),
        "title": bundle["title"],
        "template": {
            "id": new_manifest["id"], "name": new_manifest["name"],
            "source_sha256": new_manifest["source_sha256"],
            "native_sha256": new_manifest["native_sha256"],
            "binding_sha256": binding_hash(new_manifest),
        },
        "brief": bundle["brief"], "local_values": local_values,
        "input_snapshot": [], "responses": responses, "research": research,
        "ai_attempts": {}, "prompts": {},
        "migration": {
            "source_bundle_sha256": source_digest,
            "source_template_id": old_manifest["id"],
            "copied_body_fields": copied,
            "relocated_body_fields": relocated,
            "unplaced_prose": unplaced,
            "policy": "같은 원본 문단의 본문만 자동 복사하고 검증된 위치 이동만 허용. 사실·개인정보는 저장된 사용자값만 복사.",
        },
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-bundle", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--target-template", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.report.exists():
        raise ValueError("결과 파일이 이미 있습니다. 기존 결과는 덮어쓰지 않습니다.")
    bundle, _, source_digest = load_bundle(args.source_bundle)
    old_manifest = read_json(args.source_manifest)
    registry = TemplateRegistry(args.target_template.parent)
    new_manifest = registry.load(args.target_template.name)
    result = adapt(bundle, old_manifest, new_manifest, source_digest)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.output, result)
    try:
        _, info = prepare_bundle(registry_service(registry), new_manifest["id"], args.output)
    except Exception:
        args.output.unlink(missing_ok=True)
        raise
    report = {
        "result": "validated", "output": str(args.output.resolve()),
        "target_template_id": new_manifest["id"],
        "new_topics": len(new_manifest["topics"]),
        "copied_body_fields": len(result["migration"]["copied_body_fields"]),
        "relocated_body_fields": len(result["migration"]["relocated_body_fields"]),
        "saved_user_values": len(result["local_values"]),
        "unplaced_prose": [
            {k: item[k] for k in ("topic_id", "field_id", "label", "reason")}
            for item in result["migration"]["unplaced_prose"]
        ],
        "prepared_topics": info["topics"],
    }
    write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def registry_service(registry):
    class Service:
        pass
    service = Service()
    service.registry = registry
    return service


if __name__ == "__main__":
    main()
