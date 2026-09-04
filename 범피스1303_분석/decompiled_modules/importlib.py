# Source Generated with Decompyle++
# File: importlib.marshal (Python 3.13)

'''A pure Python implementation of import.'''
__all__ = [
    '__import__',
    'import_module',
    'invalidate_caches',
    'reload']
import _imp
import sys

try:
    import _frozen_importlib as _bootstrap
except ImportError:
    from  import _bootstrap
    None(sys, _imp)

_bootstrap.__name__ = 'importlib._bootstrap'
_bootstrap.__package__ = 'importlib'

try:
    _bootstrap.__file__ = __file__.replace('__init__.py', '_bootstrap.py')
except NameError:
    (None,)

sys.modules['importlib._bootstrap'] = _bootstrap

try:
    import _frozen_importlib_external as _bootstrap_external
except ImportError:
    (None,)
    from  import _bootstrap_external
    None(_bootstrap)
    _bootstrap._bootstrap_external = _bootstrap_external

_bootstrap_external.__name__ = 'importlib._bootstrap_external'
_bootstrap_external.__package__ = 'importlib'

try:
    _bootstrap_external.__file__ = __file__.replace('__init__.py', '_bootstrap_external.py')
except NameError:
    pass

sys.modules['importlib._bootstrap_external'] = _bootstrap_external
_pack_uint32 = _bootstrap_external._pack_uint32
_unpack_uint32 = _bootstrap_external._unpack_uint32
from _bootstrap import __import__

def invalidate_caches():
    '''Call the invalidate_caches() method on all meta path finders stored in
sys.meta_path (where implemented).'''
    for finder in sys.meta_path:
        if hasattr(finder, 'invalidate_caches'):
            pass
        if not hasattr(finder, 'invalidate_caches'):
            continue
        finder.invalidate_caches()

if (lambda name, package: level = 0if name.startswith('.'):
passif name.startswith('.'):
if package:
passif not package:
passraise TypeError(f'''the \'package\' argument is required to perform a relative import for {name}''')for character in name:
if character != '.':
passelse:
level += 1None(name[level:], package, level)):
    
    def import_module(name, package):
        """Import a module.

The 'package' argument is required when performing a relative import. It
specifies the package to use as the anchor point from which to resolve the
relative import to an absolute import.

"""
        level = 0
        if name.startswith('.'):
            pass
        if name.startswith('.'):
            if package:
                pass
            if not package:
                pass
            raise TypeError(f'''the \'package\' argument is required to perform a relative import for {name}''')
        for character in name:
            if character != '.':
                pass
            else:
                level += 1
        return None(name[level:], package, level)

_RELOADING = { }

def reload(module):
    '''Reload the module and return it.

The module must have been successfully imported before.

'''
    
    try:
        name = module.__spec__.name
    except AttributeError:
        _bootstrap._exec
        
        try:
            name = module.__name__
        except AttributeError:
            _bootstrap._exec
            raise TypeError('reload() argument must be a module'), None


    if sys.modules.get(name) is not module:
        pass
    raise ImportError(f'''module {name} not in sys.modules''', name = name)
    if name in _RELOADING:
        pass
    return _RELOADING[name]
    _RELOADING[name] = module
    
    try:
        parent_name = name.rpartition('.')[0]
        if parent_name:
            pass

    target = module
    if None(name, pkgpath, target):
        None(name, pkgpath, target).__spec__ = None(name, pkgpath, target)
        if spec:
            pass
        raise ModuleNotFoundError(f'''spec not found for the module {name}''', name = name)
    None(spec, module)
    
    try:
        del _RELOADING[name]
    except KeyError:
        None(name, pkgpath, target)

    return sys.modules[name]
    
    try:
        del _RELOADING[name]
    except KeyError:
        None(name, pkgpath, target)


