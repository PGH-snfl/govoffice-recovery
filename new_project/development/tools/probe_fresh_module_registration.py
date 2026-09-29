"""Temporarily test the deployment DLL path under the official module name.

Restore the prior module path even on failure. No unrelated registry values are edited.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import winreg

root = Path(sys.argv[1]).resolve()
keyname = r"Software\HNC\HwpAutomation\Modules"
name = "FilePathCheckerModuleExample"
source = root / "runtime/HwpAutomation/FilePathCheckerModuleExample.dll"
digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
staged = Path(os.environ["LOCALAPPDATA"]) / "GovOffice/modules" / digest / source.name
if not staged.is_file():
    raise RuntimeError("Run deployment_check.py --register first to stage the DLL")
saved = []
try:
    for view in (winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyname, 0, winreg.KEY_READ | view) as key:
            saved.append((view, winreg.QueryValueEx(key, name)))
    for view, _ in saved:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyname, 0, winreg.KEY_WRITE | view) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(staged))
    result = subprocess.run([str(root / "runtime/python/python.exe"), "-X", "utf8", str(root / "tools/probe_hwp_installation.py")],
                            capture_output=True, encoding="utf-8", timeout=50)
    print(result.stdout)
    print(result.stderr)
    code = result.returncode
finally:
    for view, (value, kind) in saved:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyname, 0, winreg.KEY_WRITE | view) as key:
            winreg.SetValueEx(key, name, 0, kind, value)
raise SystemExit(code)
