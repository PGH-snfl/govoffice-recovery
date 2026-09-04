"""Execute the extracted Python 3.13 bytecode without launching the original EXE."""

from __future__ import annotations

import importlib.abc
import importlib.util
import json
import marshal
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT / "extracted" / "resources"
MODULES = ROOT / "pyz_modules"
MAIN = ROOT / "extracted" / "code" / "메인.marshal"


class MarshalFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self) -> None:
        self.entries = json.loads((MODULES / "pyz_manifest.json").read_text(encoding="utf-8"))

    def find_spec(self, fullname, path=None, target=None):
        entry = self.entries.get(fullname)
        if entry is None:
            return None
        return importlib.util.spec_from_loader(fullname, self, is_package=entry["type"] == 1)

    def create_module(self, spec):
        return None

    def exec_module(self, module) -> None:
        entry = self.entries[module.__name__]
        if entry["output"] is None:
            module.__path__ = []
            return
        code_path = MODULES / entry["output"]
        module.__file__ = str(code_path)
        if entry["type"] == 1:
            module.__path__ = [str(code_path.parent)]
        exec(marshal.loads(code_path.read_bytes()), module.__dict__)


def main() -> None:
    if "--validate" in sys.argv:
        finder = MarshalFinder()
        missing = [name for name, entry in finder.entries.items() if entry["output"] and not (MODULES / entry["output"]).is_file()]
        main_code = marshal.loads(MAIN.read_bytes())
        print(f"main={type(main_code).__name__} modules={len(finder.entries)} missing={len(missing)}")
        raise SystemExit(1 if missing else 0)
    sys._MEIPASS = str(RESOURCES)  # type: ignore[attr-defined]
    sys.path.insert(0, str(RESOURCES))
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(str(RESOURCES))
    sys.meta_path.insert(0, MarshalFinder())
    namespace = {"__name__": "__main__", "__file__": str(MAIN), "__package__": None}
    exec(marshal.loads(MAIN.read_bytes()), namespace)


if __name__ == "__main__":
    main()
