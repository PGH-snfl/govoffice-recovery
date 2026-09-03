from __future__ import annotations

import json
import importlib.util
import os
import shutil
import stat
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent
SOURCE_PACKAGE = WORKSPACE / "recovered" / "한컴오피스"
SOURCE_STATUS = WORKSPACE / "recovered" / "metadata" / "hwp_equivalence_latest.json"
RUNTIME_ROOT = PROJECT / "src" / "govoffice" / "runtime" / "recovered_hwp"
TARGET_PACKAGE = RUNTIME_ROOT / "한컴오피스"
CATALOG_ROOT = RUNTIME_ROOT / "catalog"
BYTECODE_ROOT = RUNTIME_ROOT / "bytecode" / "한컴오피스"

VERIFIED_STATUSES = {"static_exact", "dynamic_exact", "same_error"}
EXTRACTED = WORKSPACE / "범피스1303_분석" / "extracted" / "resources"
GUI_RUNTIME = PROJECT / "runtime" / "tk"
GUI_ASSETS = PROJECT / "assets" / "icons"


def _remove_readonly(function, path, excinfo) -> None:
    """번들에서 복사된 읽기 전용 파일을 프로젝트 내부에서만 제거한다."""
    os.chmod(path, stat.S_IWRITE)
    function(path)


def _replace_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target, onexc=_remove_readonly)
    shutil.copytree(source, target)


def _copy_source() -> int:
    if not SOURCE_PACKAGE.is_dir():
        raise FileNotFoundError(f"복구 소스 패키지가 없습니다: {SOURCE_PACKAGE}")
    if TARGET_PACKAGE.exists():
        shutil.rmtree(TARGET_PACKAGE, onexc=_remove_readonly)
    shutil.copytree(SOURCE_PACKAGE, TARGET_PACKAGE, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
    return sum(1 for path in TARGET_PACKAGE.rglob("*.py") if path.is_file())


def _write_catalogs() -> tuple[int, int]:
    report = json.loads(SOURCE_STATUS.read_text(encoding="utf-8"))
    methods = report.get("methods", [])
    verified = [item for item in methods if item.get("status") in VERIFIED_STATUSES]
    deferred = [item for item in methods if item.get("status") not in VERIFIED_STATUSES]

    CATALOG_ROOT.mkdir(parents=True, exist_ok=True)
    common = {
        "source": str(SOURCE_STATUS.relative_to(WORKSPACE)),
        "policy": "런처는 verified_methods.json 항목만 실행 대상으로 사용한다.",
    }
    (CATALOG_ROOT / "verified_methods.json").write_text(
        json.dumps({**common, "count": len(verified), "methods": verified}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (CATALOG_ROOT / "deferred_methods.json").write_text(
        json.dumps({**common, "count": len(deferred), "methods": deferred}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (CATALOG_ROOT / "snapshot.json").write_text(
        json.dumps(
            {
                "source_package": str(SOURCE_PACKAGE.relative_to(WORKSPACE)),
                "verified_statuses": sorted(VERIFIED_STATUSES),
                "verified": len(verified),
                "deferred": len(deferred),
                "total": len(methods),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return len(verified), len(deferred)


def _copy_compat_bytecode() -> int:
    source = WORKSPACE / "범피스1303_분석" / "pyz_modules" / "한컴오피스"
    BYTECODE_ROOT.mkdir(parents=True, exist_ok=True)
    for filename in ("한컴라이브러리_기본.marshal", "한컴라이브러리_1.marshal", "한컴라이브러리_2.marshal", "한컴라이브러리.marshal"):
        shutil.copy2(source / filename, BYTECODE_ROOT / filename)
    return 4


def _copy_gui_runtime() -> tuple[int, int]:
    GUI_RUNTIME.mkdir(parents=True, exist_ok=True)
    for name in ("_tkinter.pyd", "tcl86t.dll", "tk86t.dll", "zlib1.dll"):
        shutil.copy2(EXTRACTED / name, GUI_RUNTIME / name)
    for name in ("_tcl_data", "_tk_data"):
        _replace_tree(EXTRACTED / name, GUI_RUNTIME / name)

    marshal_source = WORKSPACE / "범피스1303_분석" / "pyz_modules"
    shutil.copy2(marshal_source / "tkinter.marshal", GUI_RUNTIME / "tkinter.marshal")
    shutil.copy2(marshal_source / "tkinter" / "constants.marshal", GUI_RUNTIME / "constants.marshal")

    source_icons = EXTRACTED / "아이콘"
    _replace_tree(source_icons, GUI_ASSETS)
    return sum(1 for p in GUI_RUNTIME.rglob("*") if p.is_file()), sum(1 for p in GUI_ASSETS.rglob("*") if p.is_file())


def _refresh_gui_layout() -> None:
    # 아이콘 원본이 갱신될 때 실제 PNG 크기도 레이아웃에 함께 반영한다.
    module_path = Path(__file__).with_name("extract_original_layout.py")
    spec = importlib.util.spec_from_file_location("govoffice_extract_original_layout", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"레이아웃 추출기를 불러올 수 없습니다: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()


def main() -> None:
    copied = _copy_source()
    verified, deferred = _write_catalogs()
    bytecode_files = _copy_compat_bytecode()
    runtime_files, icon_files = _copy_gui_runtime()
    _refresh_gui_layout()
    print(f"복구 소스 {copied}개 파일 복사 완료")
    print(f"검증 완료 {verified}개 / 별도 분류 {deferred}개")
    print(f"호환 바이트코드 {bytecode_files}개 파일 복사 완료")
    print(f"GUI 런타임 {runtime_files}개 / 아이콘 {icon_files}개 복사 완료")


if __name__ == "__main__":
    main()
