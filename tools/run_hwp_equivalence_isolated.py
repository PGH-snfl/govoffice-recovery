"""Run each HWP differential case in its own timed process tree."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import win32com.client


ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "tools" / "validate_hwp_equivalence_batch.py"


def automation_hwp_pids():
    service = win32com.client.GetObject("winmgmts:")
    result = set()
    for process in service.ExecQuery("SELECT ProcessId, CommandLine FROM Win32_Process WHERE Name='Hwp.exe'"):
        command = str(process.CommandLine or "").lower()
        if "-automation" in command and "-embedding" in command:
            result.add(int(process.ProcessId))
    return result


def terminate_exact_pids(pids):
    for pid in sorted(pids):
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )


def wait_until_gone(pids, timeout=8.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        remaining = automation_hwp_pids() & set(pids)
        if not remaining:
            return True
        time.sleep(0.25)
    return False


def require_no_automation_hwp(stage):
    """Do not start a new case while any validation HWP is still alive.

    A previous worker can outlive its Python parent for a short period (and a
    crashed worker can leave the COM server behind).  Counting only up to the
    configured cap would allow the next case to run beside that stale server,
    which makes the result non-deterministic and violates the sequential
    cleanup contract.  Validation workers are filtered by both ``-automation``
    and ``-embedding`` so a user's interactive HWP window is not included.
    """
    pids = automation_hwp_pids()
    if pids:
        raise RuntimeError(
            f"{stage}: 이전 검증용 한글 프로세스가 남아 있어 새 기능을 실행하지 않습니다: "
            + ", ".join(map(str, sorted(pids)))
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True)
    parser.add_argument("--status", default="pending_dynamic")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--max-hwp", type=int, default=10, choices=range(1, 11))
    parser.add_argument("--method-list", type=Path)
    parser.add_argument("--include-content", action="store_true")
    parser.add_argument("--recovered-runtime", choices=("canonical", "new-project"), default="canonical")
    args = parser.parse_args()

    inventory = json.loads(
        (ROOT / "recovered" / "metadata" / "hwp_equivalence_inventory.json").read_text(encoding="utf-8")
    )
    selected = [
        row for row in inventory["methods"]
        if row["category"] == args.category and row["status"] == args.status
    ]
    if args.method_list:
        requested = {
            (item["module"], item["method"])
            for item in json.loads(args.method_list.read_text(encoding="utf-8"))
        }
        selected = [row for row in selected if (row["module"], row["method"]) in requested]
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "category": args.category, "selected": len(selected), "start": args.start,
        "completed": 0, "results": [],
    }
    require_no_automation_hwp("검증 시작 전")
    with tempfile.TemporaryDirectory(prefix="hwp_equivalence_") as temp_dir:
        temp_path = Path(temp_dir) / "one.json"
        for index in range(args.start, len(selected)):
            require_no_automation_hwp(f"{index + 1}번째 기능 시작 전")
            before = automation_hwp_pids()
            command = [
                sys.executable, str(WORKER), "--category", args.category,
                "--status", args.status, "--start", str(index), "--limit", "1",
                "--output", str(temp_path), "--max-hwp", str(args.max_hwp),
                "--recovered-runtime", args.recovered_runtime,
            ]
            if args.method_list:
                command.extend(["--method-list", str(args.method_list.resolve())])
            if args.include_content:
                command.append("--include-content")
            proc = subprocess.Popen(
                command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
            try:
                stdout, _ = proc.communicate(timeout=args.timeout)
                if temp_path.exists():
                    one = json.loads(temp_path.read_text(encoding="utf-8"))
                    if one.get("results"):
                        result = one["results"][0]
                    else:
                        result = {"module": selected[index]["module"], "method": selected[index]["method"], "harness_error": stdout[-2000:]}
                else:
                    result = {"module": selected[index]["module"], "method": selected[index]["method"], "harness_error": stdout[-2000:]}
            except subprocess.TimeoutExpired as timeout_error:
                partial = timeout_error.stdout or ""
                if isinstance(partial, bytes):
                    partial = partial.decode(errors="replace")
                subprocess.run(
                    ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
                )
                final_stdout, _ = proc.communicate()
                if final_stdout:
                    partial += final_stdout
                result = {
                    "module": selected[index]["module"], "method": selected[index]["method"],
                    "timed_out": True, "timeout_seconds": args.timeout,
                    "worker_output": partial[-2000:],
                }
            finally:
                # HWP may detach from the worker and appear shortly after the
                # Python process exits. Include that delayed start in cleanup.
                time.sleep(1.5)
                created = automation_hwp_pids() - before
                if created:
                    terminate_exact_pids(created)
                if not wait_until_gone(created):
                    raise RuntimeError(
                        "검증용 한글 프로세스 종료 확인 실패. 다음 기능을 실행하지 않습니다: "
                        + ", ".join(map(str, sorted(created)))
                    )
                remaining = automation_hwp_pids()
                if remaining:
                    raise RuntimeError(
                        "이전 기능의 한글 자동화 프로세스가 모두 종료되지 않아 다음 기능을 실행하지 않습니다: "
                        + ", ".join(map(str, sorted(remaining)))
                    )
            report["results"].append(result)
            report["completed"] = index + 1
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"index": index + 1, "method": selected[index]["method"], "timed_out": result.get("timed_out", False)}, ensure_ascii=False), flush=True)
            temp_path.unlink(missing_ok=True)
            if result.get("harness_error"):
                raise RuntimeError(
                    "검증 실행기 오류가 발생해 다음 기능을 실행하지 않습니다: "
                    + selected[index]["method"]
                )


if __name__ == "__main__":
    main()
