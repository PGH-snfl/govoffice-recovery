"""Read-only Windows file-sharing/Restart Manager diagnostics. Never closes apps."""
import ctypes
from ctypes import wintypes as w
import json
from pathlib import Path
import sys


def inspect(folder):
    folder=Path(folder).resolve(strict=True)
    paths=[folder,*folder.rglob('*')]
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.CreateFileW.argtypes=[w.LPCWSTR,w.DWORD,w.DWORD,ctypes.c_void_p,w.DWORD,w.DWORD,w.HANDLE]
    kernel.CreateFileW.restype=w.HANDLE
    kernel.CloseHandle.argtypes=[w.HANDLE]
    result={'folder':str(folder),'sharing':[]}
    for path in paths:
        # Request DELETE access without deleting anything; share every access.
        handle=kernel.CreateFileW(str(path),0x10000,7,None,3,0x02000000,None)
        error=ctypes.get_last_error() if handle==ctypes.c_void_p(-1).value else 0
        if not error:kernel.CloseHandle(handle)
        result['sharing'].append({'path':str(path.relative_to(folder)),
            'attributes':path.stat().st_file_attributes,'delete_access_error':error})
    class UniqueProcess(ctypes.Structure):
        _fields_=[('pid',w.DWORD),('start',w.FILETIME)]
    class ProcessInfo(ctypes.Structure):
        _fields_=[('process',UniqueProcess),('name',w.WCHAR*256),('service',w.WCHAR*64),
                  ('type',w.DWORD),('status',w.ULONG),('session',w.DWORD),('restartable',w.BOOL)]
    rm=ctypes.WinDLL('rstrtmgr')
    rm.RmStartSession.argtypes=[ctypes.POINTER(w.DWORD),w.DWORD,w.LPWSTR]
    rm.RmRegisterResources.argtypes=[w.DWORD,w.UINT,ctypes.POINTER(w.LPCWSTR),w.UINT,ctypes.c_void_p,w.UINT,ctypes.c_void_p]
    rm.RmGetList.argtypes=[w.DWORD,ctypes.POINTER(w.UINT),ctypes.POINTER(w.UINT),ctypes.POINTER(ProcessInfo),ctypes.POINTER(w.DWORD)]
    rm.RmEndSession.argtypes=[w.DWORD]
    session=w.DWORD();key=ctypes.create_unicode_buffer(33)
    error=rm.RmStartSession(ctypes.byref(session),0,key)
    result['rm_start']=error
    if error:return result
    try:
        files=[str(p) for p in paths if p.is_file()]
        names=(w.LPCWSTR*len(files))(*files)
        error=rm.RmRegisterResources(session,len(files),names,0,None,0,None)
        result['rm_register']=error
        if error:return result
        needed=w.UINT();count=w.UINT();reasons=w.DWORD()
        error=rm.RmGetList(session,ctypes.byref(needed),ctypes.byref(count),None,ctypes.byref(reasons))
        if error==234:
            count=w.UINT(needed.value);entries=(ProcessInfo*count.value)()
            error=rm.RmGetList(session,ctypes.byref(needed),ctypes.byref(count),entries,ctypes.byref(reasons))
            if not error:result['processes']=[{'pid':p.process.pid,'name':p.name,'service':p.service} for p in entries[:count.value]]
        result['rm_list']=error
    finally:rm.RmEndSession(session)
    return result


if __name__=='__main__':
    print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
