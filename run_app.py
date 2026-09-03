from __future__ import annotations

import sys
from pathlib import Path


for _스트림 in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_스트림, "reconfigure"):
        _스트림.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from govoffice.presentation.launcher import 실행


if __name__ == "__main__":
    실행()
