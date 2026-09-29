from __future__ import annotations

import sys
import os
import tempfile
import unittest
from pathlib import Path


for _스트림 in (sys.stdout, sys.stderr):
    if hasattr(_스트림, "reconfigure"):
        _스트림.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
# A downloaded checkout and the owner's working checkout must use the same
# clean test state. Never let test subprocesses read/write personal config.
with tempfile.TemporaryDirectory(prefix='govoffice_tests_') as test_data:
    os.environ['GOVOFFICE_DATA_DIR'] = test_data
    suite = unittest.defaultTestLoader.discover(str(ROOT / "development" / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
