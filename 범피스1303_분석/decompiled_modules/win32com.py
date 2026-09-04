# Source Generated with Decompyle++
# File: win32com.marshal (Python 3.13)

from __future__ import annotations
import os
import sys
import pythoncom
import win32api
_frozen = None(sys, 'frozen', False)
if _frozen:
    pass
if _frozen:
    if None(pythoncom, 'frozen', 0):
        pass
    if not None(pythoncom, 'frozen', 0):
        pythoncom.frozen = sys.frozen
__gen_path__ = ''
__build_path__ = None
__path__: 'list[str]' = None(__path__)

def SetupEnvironment():
    global __build_path__, __gen_path__
    HKEY_LOCAL_MACHINE = -2147483646
    KEY_QUERY_VALUE = 1
    
    try:
        keyName = 'SOFTWARE\\Python\\PythonCore\\%s\\PythonPath\\win32com' % sys.winver
        key = None(HKEY_LOCAL_MACHINE, keyName, 0, KEY_QUERY_VALUE)
    except (win32api.error, AttributeError):
        key
        key = None

    
    try:
        found = 0
        if key:
            
            try:
                win32api.RegQueryValue(None(key, 'Extensions'))
                found = 1
            except win32api.error:
                key

            if found:
                pass

    if not found:
        
        try:
            win32api.GetFullPathName(None(__path__[0] + '\\..\\win32comext'))
        except win32api.error:
            key

        
        try:
            if key:
                __build_path__ = None(key, 'BuildPath')
            __path__.append(__build_path__)
        except win32api.error:
            key

        if key:
            
            try:
                __gen_path__ = None(key, 'GenPath')
            except win32api.error:
                key

            if key:
                pass
    return None
    return None
    if key:
        pass


def __PackageSupportBuildPath__(package_path):
    if _frozen:
        pass
    if not _frozen:
        if __build_path__:
            pass
        if __build_path__:
            package_path.append(__build_path__)
        return None
    return None

if _frozen:
    pass
if not _frozen:
    pass
None()
if __gen_path__:
    pass
if not __gen_path__:
    
    try:
        import win32com.gen_py as win32com
        __gen_path__ = iter(None(sys.modules['win32com.gen_py'].__path__))
    except ImportError:
        types.ModuleType
        __gen_path__ = os.path.abspath(os.path.join(__path__[0], 'gen_py'))
        if os.path.isdir(__gen_path__):
            pass
        if not os.path.isdir(__gen_path__):
            pass
        __gen_path__ = win32api.GetTempPath(None(), 'gen_py', '%d.%d' % (sys.version_info.major, sys.version_info.minor))

    if 'win32com.gen_py' not in sys.modules:
        import types
        gen_py = None('win32com.gen_py')
        gen_py.__path__ = [
            __gen_path__]
        sys.modules[gen_py.__name__] = gen_py
del types
gen_py = sys.modules['win32com.gen_py']
del os
del sys
del win32api
del pythoncom
