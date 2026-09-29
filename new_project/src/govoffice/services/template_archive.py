"""Verified, recoverable archival when Windows refuses a directory rename."""
from pathlib import Path
import hashlib
import os
import shutil


def _inventory(folder):
    result={}
    for parent,dirs,files in os.walk(folder,followlinks=False):
        for name in dirs+files:
            path=Path(parent)/name
            if path.is_symlink() or path.is_junction():
                raise ValueError('연결된 파일/폴더가 있는 양식은 삭제할 수 없습니다: '+str(path))
            result[path.relative_to(folder)]=None if path.is_dir() else hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _check_delete_sharing(folder, entries):
    if os.name!='nt':return
    import ctypes
    from ctypes import wintypes as w
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.CreateFileW.argtypes=[w.LPCWSTR,w.DWORD,w.DWORD,ctypes.c_void_p,w.DWORD,w.DWORD,w.HANDLE]
    kernel.CreateFileW.restype=w.HANDLE
    kernel.CloseHandle.argtypes=[w.HANDLE]
    for path in [folder,*(folder/entry for entry in entries)]:
        handle=kernel.CreateFileW(str(path),0x10000,7,None,3,0x02000000,None)
        if handle==ctypes.c_void_p(-1).value:
            error=ctypes.WinError(ctypes.get_last_error());error.filename=str(path)
            raise error
        kernel.CloseHandle(handle)


def archive_after_rename_denial(source, destination, registry_root):
    source=Path(source);destination=Path(destination);root=Path(registry_root).resolve()
    # Validate absolute targets again immediately before any recursive removal.
    if (source.is_symlink() or source.is_junction() or source.resolve().parent!=root
            or len(source.name)!=32 or any(c not in '0123456789abcdef' for c in source.name)):
        raise ValueError('등록 폴더 범위 밖의 삭제는 허용하지 않습니다.')
    archive=root.parent/'deleted_templates'
    if (archive.is_symlink() or archive.is_junction() or destination.exists()
            or destination.resolve().parent!=archive.resolve()
            or archive.resolve().parent!=root.parent):
        raise ValueError('안전한 삭제 보관 위치가 아닙니다.')
    before=_inventory(source)
    # An exclusive file lock is not the directory-handle case: fail before
    # touching the registration. Do not forcibly close other programs.
    _check_delete_sharing(source,before)
    shutil.copytree(source,destination)
    if _inventory(destination)!=before or _inventory(source)!=before:
        raise ValueError('삭제 보관본 검증에 실패했습니다. 등록 폴더는 삭제하지 않았습니다. 보관 경로: '+str(destination))
    try:
        shutil.rmtree(source)
    except OSError as exc:
        # Preserve the verified archive and restore missing registration entries;
        # never overwrite a surviving file, which may have been edited elsewhere.
        try:
            source.mkdir(exist_ok=True)
            for rel,value in before.items():
                target=source/rel
                if value is None:target.mkdir(parents=True,exist_ok=True)
                elif not target.exists():
                    target.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(destination/rel,target)
        except OSError as restore_exc:
            raise ValueError('등록 폴더 정리를 완료하지 못했습니다. 전체 보관본은 다음 위치에 보존됩니다: '
                             +str(destination)+'\n복원 오류: '+str(restore_exc)) from exc
        raise ValueError('등록 폴더 정리에 실패하여 삭제를 완료하지 않았습니다. 보관 경로: '
                         +str(destination)+'\nWindows 오류: '+str(exc)) from exc
    if source.exists():raise ValueError('등록 폴더가 남아 있어 삭제 완료로 처리하지 않았습니다: '+str(source))
