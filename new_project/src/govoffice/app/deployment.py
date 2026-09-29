"""Deployment paths and per-user HWP Automation setup (no HWP launch)."""
from __future__ import annotations

import os
import hashlib
import shutil
import struct
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
MODULE_NAME = "FilePathCheckerModuleExample"
MODULE_KEY = r"Software\HNC\HwpAutomation\Modules"


def deployed(project: Path = PROJECT) -> bool:
    return (project / "deployment.json").is_file()


def data_directory(project: Path = PROJECT) -> Path:
    override = os.environ.get("GOVOFFICE_DATA_DIR")
    if override:
        return Path(override).resolve()
    if deployed(project):
        local = os.environ.get("LOCALAPPDATA")
        if not local:
            raise RuntimeError("사용자 저장 폴더를 찾을 수 없습니다. Windows 사용자 계정으로 실행하세요.")
        return Path(local) / "GovOffice" / "data"
    return project / "config"


def pe_machine(path: Path) -> int:
    with path.open("rb") as stream:
        header = stream.read(64)
        if len(header) != 64 or header[:2] != b"MZ":
            raise RuntimeError(f"올바른 Windows 실행 파일이 아닙니다: {path}")
        stream.seek(struct.unpack_from("<I", header, 60)[0])
        pe = stream.read(6)
        if len(pe) != 6 or pe[:4] != b"PE\0\0":
            raise RuntimeError(f"손상된 Windows 실행 파일입니다: {path}")
        return struct.unpack_from("<H", pe, 4)[0]


def hwp_executable() -> Path:
    import winreg
    # COM local servers can be cross-bitness; inspect both registration views.
    for view in (winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"HWPFrame.HwpObject\CLSID", 0, winreg.KEY_READ | view) as key:
                clsid = winreg.QueryValueEx(key, "")[0]
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "CLSID\\" + clsid + r"\LocalServer32", 0, winreg.KEY_READ | view) as key:
                command = os.path.expandvars(winreg.QueryValueEx(key, "")[0]).strip()
            if command.startswith('"'):
                filename = command.split('"', 2)[1]
            else:
                end = command.lower().find(".exe")
                filename = command[:end + 4] if end >= 0 else command
            path = Path(filename)
            if path.is_file():
                return path
        except OSError:
            continue
    raise RuntimeError("한글 Automation 등록을 찾지 못했습니다. 한글을 설치하거나 한컴오피스 설치 복구를 실행하세요.")


def security_dll(project: Path = PROJECT) -> Path:
    bundled = project / "runtime" / "HwpAutomation" / "FilePathCheckerModuleExample.dll"
    if bundled.is_file() or deployed(project):
        return bundled
    # The editable project lives one directory below the recovered local
    # runtime. An installed release always uses its own bundled copy above.
    development = project.parent / "runtime" / "HwpAutomation" / bundled.name
    return development if development.is_file() else bundled


def register_security(project: Path = PROJECT) -> str:
    """Use the official module name; preserve an existing valid registration."""
    import winreg
    source = security_dll(project).resolve(strict=True)
    hwp = hwp_executable()
    if pe_machine(source) != pe_machine(hwp):
        raise RuntimeError("한글과 보안 모듈의 32/64비트가 다릅니다. 설치된 한글에 맞는 모듈이 필요합니다.")
    # Keep native module paths short and stable across versioned installations.
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    dll = Path(os.environ["LOCALAPPDATA"]) / "GovOffice" / "modules" / digest[:12] / source.name
    dll.parent.mkdir(parents=True, exist_ok=True)
    if not dll.exists():
        shutil.copyfile(source, dll)
    if hashlib.sha256(dll.read_bytes()).hexdigest() != digest:
        raise RuntimeError(f"설치된 보안 모듈 파일이 손상되었습니다: {dll}")
    # Some installed HWP builds rejected an alternate module alias in live tests.
    # Reuse an existing working official registration instead of overwriting it.
    for view in (winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, MODULE_KEY, 0, winreg.KEY_READ | view) as key:
                existing, kind = winreg.QueryValueEx(key, MODULE_NAME)
            previous = Path(existing)
            if kind == winreg.REG_SZ and previous.is_file():
                if hashlib.sha256(previous.read_bytes()).hexdigest() != digest:
                    raise RuntimeError("다른 보안 모듈이 같은 이름으로 등록되어 있습니다. 기존 모듈 확인이 필요합니다.")
                dll = previous
                break
        except OSError:
            continue
    for view in (winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, MODULE_KEY, 0, winreg.KEY_WRITE | view) as key:
            winreg.SetValueEx(key, MODULE_NAME, 0, winreg.REG_SZ, str(dll))
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, MODULE_KEY + r"\Uses", 0, winreg.KEY_WRITE | view) as key:
            winreg.SetValueEx(key, MODULE_NAME, 0, winreg.REG_DWORD, 1)
    return MODULE_NAME
