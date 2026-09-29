"""Build a self-contained, per-user Windows installation ZIP from an allowlist."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent


def build(output: Path, python_root: Path, dll: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    package = output / ("GovOffice-" + stamp)
    app = package / "app"
    app.mkdir(parents=True, exist_ok=False)
    excluded = shutil.ignore_patterns(
        "__pycache__", "*.pyc", "*.pyo", "*.log", "gen_py", "tests", "test",
        # The analysis interpreter also contains PyWin32 development tools.
        # Runtime COM support is retained; IDEs, demos, headers and build tools
        # are deliberately excluded from the user package.
        "Demos", "demos", "scripts", "HTML", "makegw", "include", "libs",
        "pythonwin", "isapi", "adodbapi", "win32comext", "bin", "*.chm", "*.dist-info",
        "pywin32.pth", "pywin32.version.txt",
    )
    for folder in ("src", "assets", "runtime/tk"):
        shutil.copytree(PROJECT / folder, app / folder, ignore=excluded)
    for filename in ("gui_backend.py", "run_app.py", "launch_gui.ps1", "gui_poll_guard.cs", "favorites_ui.ps1", "workspace_windows.ps1", "profile_table_ui.ps1", "document_authoring_ui.ps1", "document_authoring_flow_ui.ps1", "launch_govoffice.cmd", "범정부오피스_실행.cmd", "config/original_layout.json",
                     "product/support/deployment_check.py", "product/support/probe_security_dll.ps1", "product/support/probe_hwp_installation.py"):
        target = app / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT / filename, target)
    shutil.copytree(python_root, app / "runtime/python", ignore=excluded)
    target_dll = app / "runtime/HwpAutomation/FilePathCheckerModuleExample.dll"
    target_dll.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dll, target_dll)
    for filename in ("install.cmd", "install.ps1", "사용안내.txt"):
        shutil.copy2(PROJECT / "packaging" / "installer" / filename, package / filename)
    # Windows PowerShell 5.1 needs a BOM for Korean strings. CMD needs CRLF.
    for path in package.rglob("*"):
        if path.suffix.lower() in (".ps1", ".cmd"):
            content = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
            path.write_bytes((b"\xef\xbb\xbf" if path.suffix.lower() == ".ps1" else b"") + content.replace("\n", "\r\n").encode("utf-8"))
    hashes = {p.relative_to(app).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(app.rglob("*")) if p.is_file()}
    manifest = {"build": stamp, "python": "3.13", "scope": "internal-hwp", "files": hashes}
    (app / "deployment.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    archive = output / (package.name + ".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(package))
    print(json.dumps({"zip": str(archive), "package": str(package), "files": len(hashes), "bytes": archive.stat().st_size}, ensure_ascii=False))
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PROJECT / "packaging" / "releases")
    parser.add_argument("--python-root", type=Path, default=WORKSPACE / "범피스1303_분석/python313")
    parser.add_argument("--security-dll", type=Path, default=WORKSPACE / "runtime/HwpAutomation/FilePathCheckerModuleExample.dll")
    args = parser.parse_args()
    build(args.output.resolve(), args.python_root.resolve(), args.security_dll.resolve())
