from __future__ import annotations

import sys
import unittest
from pathlib import Path


for _스트림 in (sys.stdout, sys.stderr):
    if hasattr(_스트림, "reconfigure"):
        _스트림.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
