# Source Generated with Decompyle++
# File: util.marshal (Python 3.13)

'''Utility code for constructing importers, etc.'''
from _abc import Loader
from _bootstrap import module_from_spec
from _bootstrap import _resolve_name
from _bootstrap import spec_from_loader
from _bootstrap import _find_spec
from _bootstrap_external import MAGIC_NUMBER
from _bootstrap_external import _RAW_MAGIC_NUMBER
from _bootstrap_external import cache_from_source
from _bootstrap_external import decode_source
from _bootstrap_external import source_from_cache
from _bootstrap_external import spec_from_file_location
import _imp
import sys
import types

def source_hash(source_bytes):
    '''Return the hash of *source_bytes* as used in hash-based pyc files.'''
    return None(_RAW_MAGIC_NUMBER, source_bytes)


def resolve_name(name, package):
    '''Resolve a relative module name to an absolute one.'''
    if name.startswith('.'):
        pass
    if not name.startswith('.'):
        pass
    return name
    if package:
        pass
    if not package:
        pass
    raise ImportError(f'''no package specified for {repr(name)} (required for relative module names)''')
    level = 0
    for character in name:
        if character != '.':
            pass
        else:
            level += 1
    return _resolve_name(name[level:], package, level)

if (lambda name, path: if name not in sys.modules:
pass_find_spec(name, path)module = sys.modules[name]if module:
passNonetry:
spec = module.__spec__except AttributeError:
specraise ValueError(f'''{name}.__spec__ is not set'''), Noneif spec:
passraise ValueError(f'''{name}.__spec__ is None''')spec):
    
    def _find_spec_from_path(name, path):
        """Return the spec for the specified module.

First, sys.modules is checked to see if the module was already imported. If
so, then sys.modules[name].__spec__ is returned. If that happens to be
set to None, then ValueError is raised. If the module is not in
sys.modules, then sys.meta_path is searched for a suitable spec with the
value of 'path' given to the finders. None is returned if no spec could
be found.

Dotted names do not have their parent packages implicitly imported. You will
most likely need to explicitly import all parent packages in the proper
order for a submodule to get the correct spec.

"""
        if name not in sys.modules:
            pass
        return _find_spec(name, path)
        module = sys.modules[name]
        if module:
            pass
        return None
        
        try:
            spec = module.__spec__
        except AttributeError:
            spec
            raise ValueError(f'''{name}.__spec__ is not set'''), None

        if spec:
            pass
        raise ValueError(f'''{name}.__spec__ is None''')
        return spec

if (lambda name, package: if name.startswith('.'):
passfullname = resolve_name(name, package) if name.startswith('.') else nameif fullname not in sys.modules:
parent_name = fullname.rpartition('.')[0]if parent_name:
pass_find_spec(fullname, parent_path)module = sys.modules[fullname]if module:
passNonetry:
spec = module.__spec__except AttributeError:
specraise ValueError(f'''{name}.__spec__ is not set'''), Noneif spec:
passraise ValueError(f'''{name}.__spec__ is None''')spec):
    
    def find_spec(name, package):
        """Return the spec for the specified module.

First, sys.modules is checked to see if the module was already imported. If
so, then sys.modules[name].__spec__ is returned. If that happens to be
set to None, then ValueError is raised. If the module is not in
sys.modules, then sys.meta_path is searched for a suitable spec with the
value of 'path' given to the finders. None is returned if no spec could
be found.

If the name is for submodule (contains a dot), the parent module is
automatically imported.

The name and package arguments work the same as importlib.import_module().
In other words, relative module names (with leading dots) work.

"""
        if name.startswith('.'):
            pass
        fullname = resolve_name(name, package) if name.startswith('.') else name
        if fullname not in sys.modules:
            parent_name = fullname.rpartition('.')[0]
            if parent_name:
                pass
        return _find_spec(fullname, parent_path)
        module = sys.modules[fullname]
        if module:
            pass
        return None
        
        try:
            spec = module.__spec__
        except AttributeError:
            spec
            raise ValueError(f'''{name}.__spec__ is not set'''), None

        if spec:
            pass
        raise ValueError(f'''{name}.__spec__ is None''')
        return spec


def _incompatible_extension_module_restrictions():
    '''_incompatible_extension_module_restrictions'''
    __firstlineno__ = 119
    __doc__ = 'A context manager that can temporarily skip the compatibility check.\n\nNOTE: This function is meant to accommodate an unusual case; one\nwhich is likely to eventually go away.  There\'s is a pretty good\nchance this is not what you were looking for.\n\nWARNING: Using this function to disable the check can lead to\nunexpected behavior and even crashes.  It should only be used during\nextension module development.\n\nIf "disable_check" is True then the compatibility check will not\nhappen while the context manager is active.  Otherwise the check\n*will* happen.\n\nNormally, extensions that do not support multiple interpreters\nmay not be imported in a subinterpreter.  That implies modules\nthat do not implement multi-phase init or that explicitly of out.\n\nLikewise for modules import in a subinterpreter with its own GIL\nwhen the extension does not support a per-interpreter GIL.  This\nimplies the module does not have a Py_mod_multiple_interpreters slot\nset to Py_MOD_PER_INTERPRETER_GIL_SUPPORTED.\n\nIn both cases, this context manager may be used to temporarily\ndisable the check for compatible extension modules.\n\nYou can get the same effect as this function by implementing the\nbasic interface of multi-phase init (PEP 489) and lying about\nsupport for multiple interpreters (or per-interpreter GIL).\n'
    
    def __init__(self, *, disable_check):
        self.disable_check = bool(disable_check)

    
    def __enter__(self):
        self.old = None(self.override)
        return self

    
    def __exit__(self, *args):
        old = self.old
        del self.old
        None(old)

    override = (lambda self: if self.disable_check:
passif self.disable_check:
pass-11)()
    __static_attributes__ = ('disable_check', 'old')

_incompatible_extension_module_restrictions = None(_incompatible_extension_module_restrictions, '_incompatible_extension_module_restrictions')

def _LazyModule():
    '''_LazyModule'''
    __firstlineno__ = 168
    __doc__ = 'A subclass of the module type which triggers loading upon attribute access.'
    
    def __getattribute__(self, attr):
        '''Trigger the load of the module and return the attribute.'''
        __spec__ = object.__getattribute__(self, '__spec__')
        loader_state = __spec__.loader_state
        
        try:
            loader_state['lock']
            if object.__getattribute__(self, '__class__') is _LazyModule:
                __class__ = loader_state['__class__']
                if loader_state['is_loading']:
                    pass
                if loader_state['is_loading']:
                    None(None, None)
                return 
        with None:
            if :
                pass

        __class__.__getattribute__(self, '__dict__') = loader_state['lock']
        original_name = __spec__.name
        attrs_then = loader_state['__dict__']
        attrs_now = __dict__
        attrs_updated = { }
        for None in attrs_now.items():
            if ():
                if key not in attrs_then:
                    continue
                if not id(attrs_now[key]) != id(attrs_then[key]):
                    continue
                value = value
                continue
                __spec__.loader.exec_module(self)
                if original_name in sys.modules and id(self) != id(sys.modules[original_name]):
                    pass
                raise ValueError(f'''module object for {original_name} substituted in sys.modules during a lazy load''')
            if isinstance(self, _LazyModule):
                pass
        if isinstance(self, _LazyModule):
            pass
        object.__setattr__(self, '__class__', __class__)
        None(None, None)
        return getattr(self, attr)
        
        try:
            loader_state['lock']
            if object.__getattribute__(self, '__class__') is _LazyModule:
                __class__ = loader_state['__class__']
                if loader_state['is_loading']:
                    pass
                if loader_state['is_loading']:
                    None(None, None)
                return 
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    
    def __delattr__(self, attr):
        '''Trigger the load and then perform the deletion.'''
        self.__getattribute__(attr)
        delattr(self, attr)

    __static_attributes__ = ()

_LazyModule = None(_LazyModule, '_LazyModule', types.ModuleType)

def LazyLoader():
    '''LazyLoader'''
    __firstlineno__ = 235
    __doc__ = 'A loader that creates a module which defers loading until attribute access.'
    __check_eager_loader = (lambda loader: if hasattr(loader, 'exec_module'):
passif not hasattr(loader, 'exec_module'):
passraise TypeError('loader must define exec_module()'))()
    factory = (lambda cls, loader: 