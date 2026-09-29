"""Exercise the real installer and packaged backend without touching HWP or HKCU."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def verify(archive: Path):
    with tempfile.TemporaryDirectory(prefix="GovOffice-install-") as temporary:
        base = Path(temporary)
        extracted = base / "배포 파일"
        with zipfile.ZipFile(archive) as bundle:
            private = [name for name in bundle.namelist() if name in (
                "app/config/user_profile.json", "app/config/user_profile.dat", "app/config/favorites.json")
                       or name.startswith("app/config/style_presets/")]
            if private:
                raise AssertionError(f"User data included: {private}")
            bundle.extractall(extracted)
        environment = dict(os.environ, GOVOFFICE_DATA_DIR=str(base / "user-data"), PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        installer = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                                    str(extracted / "install.ps1"), "-NoLaunch", "-OfflineCheck", "-InstallRoot", str(base / "별도 설치")],
                                   env=environment, capture_output=True, encoding="utf-8", errors="replace", timeout=90)
        if installer.returncode:
            raise AssertionError(installer.stdout + installer.stderr)
        release = next((base / "별도 설치/releases").iterdir())
        python = release / "runtime/python/python.exe"
        commands = [dict(action="user_profile_get"), dict(action="user_profile_basic_save", values={"이름": "배포시험"}),
                    dict(action="style_preset_list"), dict(action="shutdown")]
        def backend(requests):
            result = subprocess.run([str(python), str(release / "gui_backend.py")], cwd=base,
                                    input="\n".join(json.dumps(row) for row in requests) + "\n", env=environment,
                                    capture_output=True, encoding="utf-8", timeout=25)
            if result.returncode:
                raise AssertionError(result.stderr)
            rows = [json.loads(line) for line in result.stdout.splitlines()]
            if not rows or any(not row.get("ok") for row in rows):
                raise AssertionError(rows)
            return rows
        first = backend(commands)
        second = backend([dict(action="user_profile_get"), dict(action="shutdown")])
        if "배포시험" not in json.dumps(second, ensure_ascii=False):
            raise AssertionError("Profile did not persist across backend restarts")
        if (release / "config/user_profile.json").exists():
            raise AssertionError("Profile was written in application directory")
        print(json.dumps(dict(ok=True, installer="passed", independent_backend="passed", profile_restart="passed",
                              user_data_excluded=True, hwp_execution_tested=False, responses=len(first) + len(second)), ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    verify(parser.parse_args().archive.resolve())
