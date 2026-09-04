from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: run_pycdc_batch.py PYCDC INPUT_DIR OUTPUT_DIR")
    tool = Path(sys.argv[1]).resolve()
    source_root = Path(sys.argv[2]).resolve()
    output_root = Path(sys.argv[3]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    results = []
    for source in source_root.rglob("*.marshal"):
        relative = source.relative_to(source_root)
        output = (output_root / relative).with_suffix(".py")
        errors = output.with_suffix(".errors.txt")
        output.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [str(tool), "-c", "-v", "3.13", str(source)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output.write_bytes(result.stdout)
        errors.write_bytes(result.stderr)
        results.append(
            {
                "input": str(relative),
                "output": str(output.relative_to(output_root)),
                "exit_code": result.returncode,
                "source_bytes": len(result.stdout),
                "error_bytes": len(result.stderr),
            }
        )
    (output_root / "decompile_manifest.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "files": len(results),
                "nonzero_exit": sum(item["exit_code"] != 0 for item in results),
                "source_bytes": sum(item["source_bytes"] for item in results),
                "error_bytes": sum(item["error_bytes"] for item in results),
            }
        )
    )


if __name__ == "__main__":
    main()
