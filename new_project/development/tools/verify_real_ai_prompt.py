"""One-topic live verification: saved guide MD -> Codex -> validated JSON."""
from datetime import datetime
from pathlib import Path
import json
import sys
import threading
from uuid import uuid4

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from govoffice.adapters.codex_author import CodexAuthor
from govoffice.services.document_authoring import (
    TemplateRegistry, make_prompt, read_json, response_schema, topic_guide_text,
    validate_result, write_json,
)


def main():
    registry = TemplateRegistry(PROJECT / "config/document_authoring/templates")
    manifests = sorted(registry.folder.glob("*/manifest.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    manifest = next((read_json(p) for p in manifests if "v6 (\ub300\uc8fc\uc81c \ud30c\uc77c\u00b7\uc18c\uc8fc\uc81c\ubcc4 \uc694\ub839)" in read_json(p).get("name", "")), None)
    if manifest is None:
        raise RuntimeError("\uac80\uc99d\ud560 v6 \uc591\uc2dd\uc744 \ucc3e\uc9c0 \ubabb\ud588\uc2b5\ub2c8\ub2e4.")
    folder = registry.path(manifest["id"])
    topic = next(t for t in manifest["topics"] if t["title"].lstrip().startswith("1-2."))
    guide = topic_guide_text(folder, topic)
    required = ["\uc791\uc131\uc694\ub839 \ud45c", "\ud30c\ub780 \uc8fc\uc11d\u00b7\uc870\uac74", "\uacf5\uc9c0\ub41c \uae30\uc220 \uc218\uc900", "\uc9c1\uc811 \uad00\ub828\ub41c \uc2dc\uc7a5 \uaddc\ubaa8"]
    missing = [text for text in required if text not in guide]
    if missing:
        raise RuntimeError("MD \uc791\uc131\uc694\ub839 \ub204\ub77d: " + ", ".join(missing))
    brief = {
        "title": "\ub3c4\uc2dc \uacf5\uacf5\uac74\ubb3c \uc5d0\ub108\uc9c0\uc808\uac10 \uc9c0\uc6d0 \uc2dc\uc2a4\ud15c(\uc2e4\uc81c \uc5f0\uacb0 \uac80\uc99d\uc6a9 \uac00\uc0c1 \uacfc\uc81c)",
        "description": "\uacf5\uacf5\uac74\ubb3c\uc758 \uc804\ub825\u00b7\ub0c9\ub09c\ubc29 \uc0ac\uc6a9\ub7c9\uc744 \ubd84\uc11d\ud574 \uc6b4\uc601\uc790\uc5d0\uac8c \uc808\uac10 \uc81c\uc548\uc744 \uc81c\uacf5\ud558\ub294 \ub0b4\ubd80\uc6a9 \uc18c\ud504\ud2b8\uc6e8\uc5b4. \uc2e4\uc81c \uc131\uacfc\u00b7\uc2dc\uc7a5\uc870\uc0ac \uc790\ub8cc\ub294 \uc5c6\uc74c.",
        "facts": "\uc2e4\uc81c \uae30\uad00\u00b7\uc608\uc0b0\u00b7\uae30\uac04\u00b7\uc2dc\uc7a5 \uc218\uce58\ub294 \ubbf8\uc81c\uacf5. \uadfc\uac70 \uc5c6\ub294 \uc218\uce58\ub098 \uae30\uad00\uba85\uc740 \ucd94\uc815\ud558\uc9c0 \ub9d0 \uac83.",
        "references": "\uc678\ubd80 \ucc38\uace0\uc790\ub8cc \uc5c6\uc74c. \uc5c6\ub294 \uc790\ub8cc\ub294 '\ud655\uc778 \ud544\uc694'\ub85c \ub0a8\uae38 \uac83.",
    }
    prompt = make_prompt(folder, manifest, topic, brief, {})
    prompt_data = json.loads(prompt.split("\n\n", 1)[1])
    for text in required:
        if text not in prompt:
            raise RuntimeError("\uc2e4\uc81c \ud504\ub86c\ud504\ud2b8\uc5d0 MD \ub0b4\uc6a9 \ub204\ub77d: " + text)
    output = PROJECT / "development/reports/runtime/real_ai_prompt" / (datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid4().hex[:8])
    output.mkdir(parents=True)
    (output / "01_guide_section.md").write_text(guide, encoding="utf-8")
    (output / "02_prompt.md").write_text(prompt, encoding="utf-8")
    agent = CodexAuthor(output)
    try:
        account = agent.account()
        raw = agent.generate(prompt, response_schema(topic), threading.Event())
    finally:
        agent.close()
    write_json(output / "03_raw_response.json", raw)
    validated = validate_result(topic, raw)
    write_json(output / "04_validated_response.json", validated)
    report = {
        "verified_at": datetime.now().isoformat(),
        "connection": account,
        "template_id": manifest["id"],
        "template_name": manifest["name"],
        "topic_id": topic["id"],
        "topic_title": topic["title"],
        "guide_file": topic["guide"],
        "guide_section": topic.get("guide_section"),
        "guide_markers_verified": required,
        "prompt_contains_exact_guide_section": prompt_data["\uc18c\uc8fc\uc81c\uc791\uc131\uc694\ub839"] == guide,
        "expected_field_ids": [f["id"] for f in topic["fields"]],
        "received_field_ids": list(validated["values"]),
        "all_fields_received": set(validated["values"]) == {f["id"] for f in topic["fields"]},
        "nonempty_values": sum(bool(v) for v in validated["values"].values()),
        "needs_review_count": len(validated["needs_review"]),
        "output_folder": str(output.resolve()),
        "actual_ai_request": True,
        "hwp_exported": False,
    }
    write_json(output / "05_verification.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
