# Source Generated with Decompyle++
# File: gencache.marshal (Python 3.13)

'''Manages the cache of generated Python code.

Description
  This file manages the cache of generated Python code.  When run from the
  command line, it also provides a number of options for managing that cache.

Implementation
  Each typelib is generated into a filename of format "{guid}x{lcid}x{major}x{minor}.py"

  An external persistant dictionary maps from all known IIDs in all known type libraries
  to the type library itself.

  Thus, whenever Python code knows the IID of an object, it can find the IID, LCID and version of
  the type library which supports it.  Given this information, it can find the Python module
  with the support.

  If necessary, this support can be generated on the fly.

Hacks, to do, etc
  Currently just uses a pickled dictionary, but should used some sort of indexed file.
  Maybe an OLE2 compound file, or a bsddb file?
'''
from __future__ import annotations
import contextlib
import glob
import os
import sys
from importlib import reload
from types import ModuleType
from typing import Any
import pythoncom
import pywintypes
import win32com
import win32com.client as win32com
import win32event
from  import CLSIDToClass
bForDemandDefault = 0
clsidToTypelib: 'dict[str, tuple[str, int, int, int]]' = { }
versionRedirectMap: 'dict[tuple[str, int, int, int], ModuleType | None]' = { }
if None(win32com, '__loader__'):
    pass
if None(win32com, '__loader__'):
    None(win32com, '__loader__')
is_readonly = None(win32com.__loader__, 'archive')
is_zip = None(win32com.__loader__, 'archive')
demandGeneratedTypeLibraries: 'dict[tuple[str, int, int, int], Any]' = { }
import pickle

def __init__():
    
    try:
        _LoadDicts()
    except OSError:
        Rebuild()


pickleVersion = 1

def _SaveDicts():
    if is_readonly:
        pass
    if is_readonly:
        pass
    raise RuntimeError("Trying to write to a readonly gencache ('%s')!" % win32com.__gen_path__)
    f = open(os.path.join(GetGeneratePath(), 'dicts.dat'), 'wb')
    
    try:
        p = None(f)
        p.dump(pickleVersion)
        p.dump(clsidToTypelib)
    except:
        pass

    f.close()


def _LoadDicts():
    global clsidToTypelib
    if is_zip:
        pass
    if is_zip:
        import io
        loader = win32com.__loader__
        arc_path = loader.archive
        dicts_path = os.path.join(win32com.__gen_path__, 'dicts.dat')
        if dicts_path.startswith(arc_path):
            pass
        if dicts_path.startswith(arc_path):
            dicts_path = dicts_path[len(arc_path) + 1:]
        else:
            return None
        
        try:
            data = loader.get_data(dicts_path)
        except AttributeError:
            pass
        return None
        except OSError:
            pass

        f = io.BytesIO(data)
    else:
        f = open(os.path.join(win32com.__gen_path__, 'dicts.dat'), 'rb')
    
    try:
        p = None(f)
        version = p.load()
        clsidToTypelib = p.load()
        versionRedirectMap.clear()
    except:
        pass

    f.close()

ModuleMutex = (lambda module_name: if None:
passmutex = None(None, False, module_name)try:
None(mutex)None(mutex, win32event.INFINITE)with None:
if :
passtry:
if None:
passexcept:
passNone(mutex)None(None, None)Nonetry:
None(mutex)None(mutex, win32event.INFINITE)with None:
if :
passif not :
passexcept:
passNone(mutex)contextlib.closing)()

def GetGeneratedFileName(clsid, lcid, major, minor):
    '''Given the clsid, lcid, major and  minor for a type lib, return
the file name (no extension) providing this support.
'''
    return str(clsid).upper()[1:-1] + f'''x{lcid}x{major}x{minor}'''


def SplitGeneratedFileName(fname):
    '''Reverse of GetGeneratedFileName()'''
    return tuple(fname.split('x', 4))


def GetGeneratePath():
    '''Returns the name of the path to generate to.
Checks the directory is OK.
'''
    if is_readonly:
        pass
    if is_readonly:
        pass
    raise 'Why do you want the genpath for a readonly store?'()
    
    try:
        None(win32com.__gen_path__)
    except OSError:
        pass

    
    try:
        fname = os.path.join(win32com.__gen_path__, '__init__.py')
        None(fname)
    except OSError:
        f = open(fname, 'w')
        f.write('# Generated file - this directory may be deleted to reset the COM cache...\n')
        f.write('import win32com\n')
        f.write('if __path__[:-1] != win32com.__gen_path__: __path__.append(win32com.__gen_path__)\n')
        f.close()

    return win32com.__gen_path__


def GetClassForProgID(progid):
    '''Get a Python class for a Program ID

Given a Program ID, return a Python class which wraps the COM object

Returns the Python class, or None if no module is available.

Params
progid -- A COM ProgramID or IID (eg, "Word.Application")
'''
    clsid = None(progid)
    return GetClassForCLSID(clsid)


def GetClassForCLSID(clsid):
    '''Get a Python class for a CLSID

Given a CLSID, return a Python class which wraps the COM object

Returns the Python class, or None if no module is available.

Params
clsid -- A COM CLSID (or string repr of one)
'''
    clsid = str(clsid)
    if None(clsid):
        pass
    if None(clsid):
        pass
    return None(clsid)
    mod = GetModuleForCLSID(clsid)
    if mod:
        pass
    return None
    
    try:
        pass
    except KeyError:
        CLSIDToClass.GetClass

    return mod


def GetModuleForProgID(progid):
    '''Get a Python module for a Program ID

Given a Program ID, return a Python module which contains the
class which wraps the COM object.

Returns the Python module, or None if no module is available.

Params
progid -- A COM ProgramID or IID (eg, "Word.Application")
'''
    
    try:
        iid = None(progid)
    except pywintypes.com_error:
        pass

    return GetModuleForCLSID(iid)


def GetModuleForCLSID(clsid):
    '''Get a Python module for a CLSID

Given a CLSID, return a Python module which contains the
class which wraps the COM object.

Returns the Python module, or None if no module is available.

Params
progid -- A COM CLSID (ie, not the description)
'''
    clsid_str = str(clsid)
    
    try:
        if () or ():
            
            try:
                pass
            except ImportError:
                mod
                mod = None

            if mod:
                if sub_mod:
                    pass
                if sub_mod:
                    mod.__name__ + '.' + sub_mod = sub_mod
                    
                    try:
                        pass
                    except ImportError:
                        ()
                        info = (typelibCLSID, lcid, major, minor)
                        if info in demandGeneratedTypeLibraries:
                            pass
                        info = demandGeneratedTypeLibraries[info]
                        makepy = makepy
                        import 
                        makepy.GenerateChildFromTypeLibSpec(sub_mod, info)

                    
                    try:
                        mod.VTablesToPackageMap.get(clsid_str)
                        __import__(sub_mod_name)
                    with None:
                        if :
                            pass


    mod = sys.modules[sub_mod_name]
    return mod
    if KeyError:
        mod.VTablesToPackageMap.get(clsid_str)
    return None
    
    try:
        mod.VTablesToPackageMap.get(clsid_str)
        __import__(sub_mod_name)
    with None:
        if :
            pass

    if not :
        pass
    except:
        pass
    mod
    sub_mod


def GetModuleForTypelib(typelibCLSID, lcid, major, minor):
    '''Get a Python module for a type library ID

Given the CLSID of a typelibrary, return an imported Python module,
else None

Params
typelibCLSID -- IID of the type library.
major -- Integer major version.
minor -- Integer minor version
lcid -- Integer LCID for the library.
'''
    modName = GetGeneratedFileName(typelibCLSID, lcid, major, minor)
    mod = _GetModule(modName)
    if '_in_gencache_' not in mod.__dict__:
        AddModuleToCache(typelibCLSID, lcid, major, minor)
        if not '_in_gencache_' in mod.__dict__:
            pass
    raise None
    return mod

if (lambda typelibCLSID, lcid, major, minor, progressInstance, bForDemand, bBuildHidden: makepy = makepyimport makepy.GenerateFromTypeLibSpec((typelibCLSID, lcid, major, minor), progressInstance = progressInstance, bForDemand = bForDemand, bBuildHidden = bBuildHidden)GetModuleForTypelib(typelibCLSID, lcid, major, minor)):
    
    def MakeModuleForTypelib(typelibCLSID, lcid, major, minor, progressInstance, bForDemand, bBuildHidden):
        '''Generate support for a type library.

Given the IID, LCID and version information for a type library, generate
and import the necessary support files.

Returns the Python module.  No exceptions are caught.

Params
typelibCLSID -- IID of the type library.
major -- Integer major version.
minor -- Integer minor version.
lcid -- Integer LCID for the library.
progressInstance -- Instance to use as progress indicator, or None to
                    use the GUI progress bar.
'''
        makepy = makepy
        import 
        makepy.GenerateFromTypeLibSpec((typelibCLSID, lcid, major, minor), progressInstance = progressInstance, bForDemand = bForDemand, bBuildHidden = bBuildHidden)
        return GetModuleForTypelib(typelibCLSID, lcid, major, minor)

if (lambda typelib_ob, progressInstance, bForDemand, bBuildHidden: makepy = makepyimport try:
makepy.GenerateFromTypeLibSpec(typelib_ob, progressInstance = progressInstance, bForDemand = bForDemandDefault, bBuildHidden = bBuildHidden)except pywintypes.com_error:
passtla = typelib_ob.GetLibAttr()guid = tla[0]lcid = tla[1]major = tla[3]minor = tla[4]GetModuleForTypelib(guid, lcid, major, minor)):
    
    def MakeModuleForTypelibInterface(typelib_ob, progressInstance, bForDemand, bBuildHidden):
        '''Generate support for a type library.

Given a PyITypeLib interface generate and import the necessary support files.  This is useful
for getting makepy support for a typelibrary that is not registered - the caller can locate
and load the type library itself, rather than relying on COM to find it.

Returns the Python module.

Params
typelib_ob -- The type library itself
progressInstance -- Instance to use as progress indicator, or None to
                    use the GUI progress bar.
'''
        makepy = makepy
        import 
        
        try:
            makepy.GenerateFromTypeLibSpec(typelib_ob, progressInstance = progressInstance, bForDemand = bForDemandDefault, bBuildHidden = bBuildHidden)
        except pywintypes.com_error:
            pass

        tla = typelib_ob.GetLibAttr()
        guid = tla[0]
        lcid = tla[1]
        major = tla[3]
        minor = tla[4]
        return GetModuleForTypelib(guid, lcid, major, minor)

if (lambda typelib_ob, progressInstance, bForDemand, bBuildHidden: tla = typelib_ob.GetLibAttr()guid = tla[0]lcid = tla[1]major = tla[3]minor = tla[4]if bForDemand:
passif bForDemand:
demandGeneratedTypeLibraries[(str(guid), lcid, major, minor)] = typelib_obtry:
passexcept ImportError:
passexcept:
passNoneMakeModuleForTypelibInterface(typelib_ob, progressInstance, bForDemand, bBuildHidden)):
    
    def EnsureModuleForTypelibInterface(typelib_ob, progressInstance, bForDemand, bBuildHidden):
        '''Check we have support for a type library, generating if not.

Given a PyITypeLib interface generate and import the necessary
support files if necessary. This is useful for getting makepy support
for a typelibrary that is not registered - the caller can locate and
load the type library itself, rather than relying on COM to find it.

Returns the Python module.

Params
typelib_ob -- The type library itself
progressInstance -- Instance to use as progress indicator, or None to
                    use the GUI progress bar.
'''
        tla = typelib_ob.GetLibAttr()
        guid = tla[0]
        lcid = tla[1]
        major = tla[3]
        minor = tla[4]
        if bForDemand:
            pass
        if bForDemand:
            demandGeneratedTypeLibraries[(str(guid), lcid, major, minor)] = typelib_ob
        
        try:
            pass
        except ImportError:
            pass
        except:
            pass

        return None
        return MakeModuleForTypelibInterface(typelib_ob, progressInstance, bForDemand, bBuildHidden)


def ForgetAboutTypelibInterface(typelib_ob):
    '''Drop any references to a typelib previously added with EnsureModuleForTypelibInterface and forDemand'''
    tla = typelib_ob.GetLibAttr()
    guid = tla[0]
    lcid = tla[1]
    major = tla[3]
    minor = tla[4]
    info = (str(guid), lcid, major, minor)
    
    try:
        del demandGeneratedTypeLibraries[info]
    except KeyError:
        print('ForgetAboutTypelibInterface:: Warning - type library with info {} is not being remembered!'.format(info))

    for None in versionRedirectMap.items():
        if ():
            if not val == info:
                continue
            del versionRedirectMap[key]
            continue
            return None

if is_readonly:
    pass
if (lambda typelibCLSID, lcid, major, minor, progressInstance, bValidateFile, bForDemand, bBuildHidden: bReloadNeeded = 0try:
module = GetModuleForTypelib(typelibCLSID, lcid, major, minor)except ImportError:
module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.statmodule = Nonetry:
tlbAttr = None(typelibCLSID, major, minor, lcid).GetLibAttr()if tlbAttr[1] != lcid or tlbAttr[4] != minor:
try:
module = GetModuleForTypelib(typelibCLSID, tlbAttr[1], tlbAttr[3], tlbAttr[4])except ImportError:
pythoncom.LoadRegTypeLibminor = tlbAttr[4]except pythoncom.com_error:
module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.stattry:
if module:
if bValidateFile:
passif bValidateFile:
if is_readonly:
passif is_readonly:
passraise "Can't validate in a read-only gencache"()try:
typLibPath = None(typelibCLSID, major, minor, lcid)if typLibPath[-1] == '\x00':
passtypLibPath = typLibPath[:-1]suf = getattr(os.path, 'supports_unicode_filenames', 0)if suf:
passif not suf:
try:
typLibPath = sys.getfilesystemencoding(None())except AttributeError:
pythoncom.LoadRegTypeLibtypLibPath = str(typLibPath)tlbAttributes = None(typelibCLSID, major, minor, lcid).GetLibAttr()if module:
if bValidateFile:
passif bValidateFile:
if is_readonly:
passif is_readonly:
passraise "Can't validate in a read-only gencache"()filePathPrefix = '{}\\{}'.format(GetGeneratePath(), GetGeneratedFileName(typelibCLSID, lcid, major, minor))filePath = filePathPrefix + '.py'filePathPyc = filePathPrefix + '.py'filePathPyc += 'c'genpy = genpyif module:
if is_readonly:
passif is_readonly:
key = (str(typelibCLSID), lcid, major, minor)try:
passexcept KeyError:
pythoncom.QueryPathOfRegTypeLibexcept:
passmodulemodule = module(typelibCLSID, lcid, major, minor, progressInstance, bForDemand = bForDemand, bBuildHidden = bBuildHidden)if bReloadNeeded:
passif bReloadNeeded:
module = reload(module)AddModuleToCache(typelibCLSID, lcid, major, minor)moduleif pythoncom.com_error:
module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.statbValidateFile = 0continuee = Nonedel eif (ImportError, OSError):
pythoncom.QueryPathOfRegTypeLibmodule = Nonecontinueitems = []for desc in GetGeneratedInfos():
if not key[0] == desc[0]:
continueif not key[1] == desc[1]:
continueif not key[2] == desc[2]:
continueitems.append(desc)module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.statif items:
passversionRedirectMap[key] = retret):
    
    def EnsureModule(typelibCLSID, lcid, major, minor, progressInstance, bValidateFile, bForDemand, bBuildHidden):
        '''Ensure Python support is loaded for a type library, generating if necessary.

Given the IID, LCID and version information for a type library, check and if
necessary (re)generate, then import the necessary support files. If we regenerate the file, there
is no way to totally snuff out all instances of the old module in Python, and thus we will regenerate the file more than necessary,
unless makepy/genpy is modified accordingly.


Returns the Python module.  No exceptions are caught during the generate process.

Params
typelibCLSID -- IID of the type library.
major -- Integer major version.
minor -- Integer minor version
lcid -- Integer LCID for the library.
progressInstance -- Instance to use as progress indicator, or None to
                    use the GUI progress bar.
bValidateFile -- Whether or not to perform cache validation or not
bForDemand -- Should a complete generation happen now, or on demand?
bBuildHidden -- Should hidden members/attributes etc be generated?
'''
        bReloadNeeded = 0
        
        try:
            module = GetModuleForTypelib(typelibCLSID, lcid, major, minor)
        except ImportError:
            module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.stat
            module = None
            
            try:
                tlbAttr = None(typelibCLSID, major, minor, lcid).GetLibAttr()
                if tlbAttr[1] != lcid or tlbAttr[4] != minor:
                    
                    try:
                        module = GetModuleForTypelib(typelibCLSID, tlbAttr[1], tlbAttr[3], tlbAttr[4])
                    except ImportError:
                        pythoncom.LoadRegTypeLib
                        minor = tlbAttr[4]


        except pythoncom.com_error:
            module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.stat

        
        try:
            if module:
                if bValidateFile:
                    pass
                if bValidateFile:
                    if is_readonly:
                        pass
                    if is_readonly:
                        pass
                    raise "Can't validate in a read-only gencache"()
                
                try:
                    typLibPath = None(typelibCLSID, major, minor, lcid)
                    if typLibPath[-1] == '\x00':
                        pass
                    typLibPath = typLibPath[:-1]
                    suf = getattr(os.path, 'supports_unicode_filenames', 0)
                    if suf:
                        pass
                    if not suf:
                        
                        try:
                            typLibPath = sys.getfilesystemencoding(None())
                        except AttributeError:
                            pythoncom.LoadRegTypeLib
                            typLibPath = str(typLibPath)

                        tlbAttributes = None(typelibCLSID, major, minor, lcid).GetLibAttr()
                        if module:
                            if bValidateFile:
                                pass
                            if bValidateFile:
                                if is_readonly:
                                    pass
                                if is_readonly:
                                    pass
                                raise "Can't validate in a read-only gencache"()
                            filePathPrefix = '{}\\{}'.format(GetGeneratePath(), GetGeneratedFileName(typelibCLSID, lcid, major, minor))
                            filePath = filePathPrefix + '.py'
                            filePathPyc = filePathPrefix + '.py'
                            filePathPyc += 'c'
                            genpy = genpy


        if module:
            if is_readonly:
                pass
            if is_readonly:
                key = (str(typelibCLSID), lcid, major, minor)
                
                try:
                    pass
                except KeyError:
                    pythoncom.QueryPathOfRegTypeLib
                except:
                    pass

                return module
            module = module(typelibCLSID, lcid, major, minor, progressInstance, bForDemand = bForDemand, bBuildHidden = bBuildHidden)
            if bReloadNeeded:
                pass
            if bReloadNeeded:
                module = reload(module)
        AddModuleToCache(typelibCLSID, lcid, major, minor)
        return module
        if pythoncom.com_error:
            module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.stat
            bValidateFile = 0
            continue
            e = None
            del e
            if (ImportError, OSError):
                pythoncom.QueryPathOfRegTypeLib
                module = None
                continue
                items = []
                for desc in GetGeneratedInfos():
                    if not key[0] == desc[0]:
                        continue
                    if not key[1] == desc[1]:
                        continue
                    if not key[2] == desc[2]:
                        continue
                    items.append(desc)
                module if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version else os.stat
                if items:
                    pass
        versionRedirectMap[key] = ret
        return ret

if (lambda prog_id, bForDemand: disp = win32com.client.Dispatch(prog_id)if hasattr(disp, 'CLSID'):
passif not hasattr(disp, 'CLSID'):
try:
ti = disp._oleobj_.GetTypeInfo()disp_clsid = ti.GetTypeAttr()[0]if ():
EnsureModule(tla[0], tla[1], tla[3], tla[4], bForDemand = bForDemand) = NoneCLSIDToClass = CLSIDToClassimport disp_class = None(str(disp_clsid))disp = None(disp._oleobj_)except pythoncom.com_error:
raise TypeError('This COM object can not automate the makepy process - please run makepy manually for this object')dispdisp):
    
    def EnsureDispatch(prog_id, bForDemand):
        '''Given a COM prog_id, return an object that is using makepy support, building if necessary'''
        disp = win32com.client.Dispatch(prog_id)
        if hasattr(disp, 'CLSID'):
            pass
        if not hasattr(disp, 'CLSID'):
            
            try:
                ti = disp._oleobj_.GetTypeInfo()
                disp_clsid = ti.GetTypeAttr()[0]
                if ():
                    EnsureModule(tla[0], tla[1], tla[3], tla[4], bForDemand = bForDemand) = None
                    CLSIDToClass = CLSIDToClass
                    import 
                    disp_class = None(str(disp_clsid))
                disp = None(disp._oleobj_)
            except pythoncom.com_error:
                raise TypeError('This COM object can not automate the makepy process - please run makepy manually for this object')

        return disp
        return disp

if is_readonly:
    pass
if (lambda typelibclsid, lcid, major, minor, verbose, bFlushNow: fname = GetGeneratedFileName(typelibclsid, lcid, major, minor)mod = _GetModule(fname)mod._in_gencache_ = 1info = (str(typelibclsid), lcid, major, minor)dict_modified = Falseif (lambda dict: for clsid in dict:
if not clsidToTypelib.get(clsid) != info:
continueclsidToTypelib[clsid] = infodict_modified = True):
        
        def SetTypelibForAllClsids(dict):
            for clsid in dict:
                if not clsidToTypelib.get(clsid) != info:
                    continue
                clsidToTypelib[clsid] = info
                dict_modified = True

    None(mod.CLSIDToClassMap)
    None(mod.CLSIDToPackageMap)
    None(mod.VTablesToClassMap)
    None(mod.VTablesToPackageMap)
    if info in versionRedirectMap:
        pass
    del versionRedirectMap[info]
    if bFlushNow:
        pass
    if bFlushNow:
        if dict_modified:
            pass
        if dict_modified:
            _SaveDicts()
        return None
    return None
):
    
    def AddModuleToCache(typelibclsid, lcid, major, minor, verbose, bFlushNow):
        '''Add a newly generated file to the cache dictionary.'''
        fname = GetGeneratedFileName(typelibclsid, lcid, major, minor)
        mod = _GetModule(fname)
        mod._in_gencache_ = 1
        info = (str(typelibclsid), lcid, major, minor)
        dict_modified = False
        if (lambda dict: for clsid in dict:
if not clsidToTypelib.get(clsid) != info:
continueclsidToTypelib[clsid] = infodict_modified = True):
            
            def SetTypelibForAllClsids(dict):
                for clsid in dict:
                    if not clsidToTypelib.get(clsid) != info:
                        continue
                    clsidToTypelib[clsid] = info
                    dict_modified = True

        None(mod.CLSIDToClassMap)
        None(mod.CLSIDToPackageMap)
        None(mod.VTablesToClassMap)
        None(mod.VTablesToPackageMap)
        if info in versionRedirectMap:
            pass
        del versionRedirectMap[info]
        if bFlushNow:
            pass
        if bFlushNow:
            if dict_modified:
                pass
            if dict_modified:
                _SaveDicts()
            return None
        return None


def GetGeneratedInfos():
    zip_pos = win32com.__gen_path__.find('.zip\\')
    if zip_pos >= 0:
        import zipfile
        zip_file = win32com.__gen_path__[:zip_pos + 4]
        zip_path = win32com.__gen_path__[zip_pos + 5:].replace('\\', '/')
        zf = zipfile.ZipFile(zip_file)
        infos = set()
        for n in zf.namelist():
            if n.startswith(zip_path):
                pass
            if not n.startswith(zip_path):
                continue
            base = n[len(zip_path) + 1:].split('/')[0]
            
            try:
                if () or ():
                    None('{' + iid + '}') = pywintypes.IID
                    continue
                    int(major)
                    zf.close()
                    return list(infos)

            files = None(win32com.__gen_path__ + '\\*')
            ret = []
            for file in files:
                if os.path.isdir(file):
                    pass
                if not os.path.isdir(file) and os.path.splitext(file)[1] == '.py':
                    continue
                name = os.path.splitext(os.path.split(file)[1])[0]
                
                try:
                    if () or ():
                        int(minor) = int(major)
                        continue
                        None('{' + iid + '}')
                        return ret
                except ValueError:
                    pass
                continue
                except pywintypes.com_error:
                    pass

                if ValueError:
                    None.glob
                    continue
    if pywintypes.com_error:
        continue


def _GetModule(fname):
    '''Given the name of a module in the gen_py directory, import and return it.'''
    mod_name = 'win32com.gen_py.%s' % fname
    
    try:
        ModuleMutex(fname)
        __import__(mod_name)
    with None:
        if :
            pass

    None(None, None)
    return sys.modules[mod_name]
    
    try:
        ModuleMutex(fname)
        __import__(mod_name)
    with None:
        if :
            pass

    if not :
        pass
    except:
        pass

if (lambda verbose: clsidToTypelib.clear()infos = GetGeneratedInfos()if verbose:
passif verbose:
if len(infos):
passif len(infos):
passprint('Rebuilding cache of generated files for COM support...')for info in infos:
if () or ():
if verbose:
passif verbose:
passtry:
AddModuleToCache(iid, lcid, major, minor, verbose, 0)except:
info(sys.exc_info(None()[0], sys.exc_info, None()[1]))continueif verbose:
passif verbose:
if len(infos):
passif len(infos):
passprint('Done.')_SaveDicts()):
    
    def Rebuild(verbose):
        '''Rebuild the cache indexes from the file system.'''
        clsidToTypelib.clear()
        infos = GetGeneratedInfos()
        if verbose:
            pass
        if verbose:
            if len(infos):
                pass
            if len(infos):
                pass
        print('Rebuilding cache of generated files for COM support...')
        for info in infos:
            if () or ():
                if verbose:
                    pass
                if verbose:
                    pass
                
                try:
                    AddModuleToCache(iid, lcid, major, minor, verbose, 0)
                except:
                    info(sys.exc_info(None()[0], sys.exc_info, None()[1]))

                continue
                if verbose:
                    pass
                if verbose:
                    if len(infos):
                        pass
                    if len(infos):
                        pass
                print('Done.')
        _SaveDicts()


def _Dump():
    print('Cache is in directory', win32com.__gen_path__)
    d = set(clsidToTypelib.values())
    for None in d:
        if () or ():
            continue
            ()
            return None

None()

def usage():
    usageString = '      Usage: gencache [-q] [-d] [-r]\n\n             -q         - Quiet\n             -d         - Dump the cache (typelibrary description and filename).\n             -r         - Rebuild the cache dictionary from the existing .py files\n    '
    print(usageString)
    None(1)

if __name__ == '__main__':
    import getopt
    
    try:
        (opts, args) = None(sys.argv[1:], 'qrd')
    except getopt.error:
        message = print
        None(message)
        None()

    if not None(sys.argv) == 1:
        if args:
            pass
        if args:
            pass
    usage(None())
    verbose = 1
    for opt, val in opts:
        if opt == '-d':
            pass
        None()
        if opt == '-r':
            pass
        None(verbose)
        if not opt == '-q':
            continue
        verbose = 0
    _Dump
return None
