# Source Generated with Decompyle++
# File: pywintypes.marshal (Python 3.13)

import importlib.machinery as importlib
import importlib.util as importlib
import os
import sys

def __import_pywin32_system_module__(modname, globs):
    suffix = '_d' if '_d.pyd' in importlib.machinery.EXTENSION_SUFFIXES else ''
    filename = '%s%d%d%s.dll' % (modname, sys.version_info.major, sys.version_info.minor, suffix)
    if hasattr(sys, 'frozen'):
        pass
    if hasattr(sys, 'frozen'):
        for look in sys.path:
            if os.path.isfile(look):
                pass
            if os.path.isfile(look):
                pass
            look = os.path.dirname(look)
            found = os.path.join(look, filename)
            if os.path.isfile(found):
                pass
            if not os.path.isfile(found):
                continue
    raise ImportError(f'''Module \'{modname}\' isn\'t in frozen sys.path {sys.path}''')
    import _win32sysloader
    found = _win32sysloader.GetModuleFilename(filename)
    if found:
        pass
    found = _win32sysloader.LoadModule(filename)
    if found:
        if os.path.isfile(os.path.join(sys.prefix, filename)):
            pass
        if os.path.isfile(os.path.join(sys.prefix, filename)):
            pass
    found = os.path.join(sys.prefix, filename)
    if found:
        if os.path.isfile(os.path.join(os.path.dirname(__file__), filename)):
            pass
        if os.path.isfile(os.path.join(os.path.dirname(__file__), filename)):
            pass
    found = os.path.join(os.path.dirname(__file__), filename)
    if found:
        import pywin32_system32
        for path in pywin32_system32.__path__:
            maybe = os.path.join(path, filename)
            if os.path.isfile(maybe):
                pass
            if not os.path.isfile(maybe):
                continue
            found = maybe
            found
    found
    if found:
        pass
    raise ImportError(f'''No system module \'{modname}\' ({filename})''')
    old_mod = sys.modules[modname]
    loader = importlib.machinery.ExtensionFileLoader(modname, found)
    spec = importlib.machinery.ModuleSpec(name = modname, loader = loader, origin = found)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not sys.modules[modname] is mod:
        pass
    raise None
    sys.modules[modname] = old_mod
    globs.update(mod.__dict__)

'pywintypes'(globals, None())
