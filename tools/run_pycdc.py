from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit("usage: run_pycdc.py PYCDC INPUT OUTPUT ERROR_LOG")
    tool, source, output, errors = map(Path, sys.argv[1:])
    result = subprocess.run(
        [str(tool), "-c", "-v", "3.13", str(source)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output.write_bytes(result.stdout)
    errors.write_bytes(result.stderr)
    print(f"exit={result.returncode} stdout={len(result.stdout)} stderr={len(result.stderr)}")


if __name__ == "__main__":
    main()
