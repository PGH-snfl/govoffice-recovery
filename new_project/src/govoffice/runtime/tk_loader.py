from __future__ import annotations

import importlib.util
import ctypes
import marshal
import os
import shutil
import sys
import tempfile
import types
from pathlib import Path


_DLL_HANDLES: list[object] = []
_NATIVE_HANDLES: list[object] = []


def _runtime_root() -> Path:
    return Path(__file__).resolve().parents[3] / "runtime" / "tk"


def _ascii_runtime_root() -> Path:
    source = _runtime_root()
    target = Path(tempfile.gettempdir()) / "govoffice_tk_runtime_313"
    marker = target / ".ready"
    if not marker.exists() or marker.stat().st_mtime < (source / "_tkinter.pyd").stat().st_mtime:
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        marker.write_text("ready", encoding="ascii")
    return target


def tkinter불러오기():
    if "tkinter" in sys.modules:
        return sys.modules["tkinter"]

    root = _ascii_runtime_root()
    required = ("_tkinter.pyd", "tcl86t.dll", "tk86t.dll", "zlib1.dll", "tkinter.marshal", "constants.marshal")
    missing = [name for name in required if not (root / name).exists()]
    if missing:
        raise RuntimeError(f"GUI 런타임 파일이 없습니다: {', '.join(missing)}")

    os.environ["TCL_LIBRARY"] = (root / "_tcl_data").as_posix()
    os.environ["TK_LIBRARY"] = (root / "_tk_data").as_posix()
    if hasattr(os, "add_dll_directory"):
        _DLL_HANDLES.append(os.add_dll_directory(str(root)))

    _NATIVE_HANDLES.append(ctypes.WinDLL(str(root / "zlib1.dll")))
    tcl = ctypes.WinDLL(str(root / "tcl86t.dll"))
    _NATIVE_HANDLES.append(tcl)
    tcl.Tcl_FindExecutable.argtypes = [ctypes.c_char_p]
    tcl.Tcl_FindExecutable(str(sys.executable).encode("utf-8"))

    extension = importlib.util.spec_from_file_location("_tkinter", root / "_tkinter.pyd")
    if extension is None or extension.loader is None:
        raise RuntimeError("_tkinter 확장 모듈을 불러올 수 없습니다.")
    tk_extension = importlib.util.module_from_spec(extension)
    sys.modules["_tkinter"] = tk_extension
    extension.loader.exec_module(tk_extension)

    package = types.ModuleType("tkinter")
    package.__file__ = str(root / "tkinter.marshal")
    package.__package__ = "tkinter"
    package.__path__ = [str(root)]
    sys.modules["tkinter"] = package

    constants = types.ModuleType("tkinter.constants")
    constants.__file__ = str(root / "constants.marshal")
    constants.__package__ = "tkinter"
    sys.modules["tkinter.constants"] = constants
    exec(marshal.loads((root / "constants.marshal").read_bytes()), constants.__dict__)
    exec(marshal.loads((root / "tkinter.marshal").read_bytes()), package.__dict__)
    return package
