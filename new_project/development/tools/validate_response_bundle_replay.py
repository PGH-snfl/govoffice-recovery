"""Exercise a migrated response packet through the offline HWP output path."""
import argparse
import json
from pathlib import Path
import sys
import time

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from govoffice.adapters.hwp_form_export import export_generated_hwp
from govoffice.services.document_authoring import AuthoringService, TemplateRegistry, write_json
from govoffice.services.saved_authoring_responses import create_replay


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.template.parent.parent
    service = AuthoringService(root.parent, lambda _: (_ for _ in ()).throw(
        AssertionError("저장 응답 재사용 중 AI를 호출했습니다.")), export_generated_hwp)
    service.root = root
    service.registry = TemplateRegistry(root / "templates")
    service.jobs = root / "jobs"
    service.jobs.mkdir(exist_ok=True)
    state = create_replay(service, args.template.name, args.bundle)
    service.start(state["id"])
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        current = service.status(state["id"])
        if current["status"] in {"completed", "failed", "paused", "interrupted"}:
            break
        time.sleep(0.5)
    else:
        service.close()
        raise TimeoutError("저장 응답으로 한글 출력이 4분 안에 끝나지 않았습니다.")
    report = {
        "status": current["status"], "job_id": state["id"],
        "hwp_path": current.get("hwp_path"), "error": current.get("error"),
        "execution_mode": current.get("execution_mode"),
        "completed_topics": len(current.get("completed", [])),
        "total_topics": current.get("total"),
        "native": current.get("native"),
    }
    write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if current["status"] != "completed":
        raise RuntimeError("저장 응답으로 한글 출력에 실패했습니다.")


if __name__ == "__main__":
    main()
