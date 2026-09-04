# Source Generated with Decompyle++
# File: abc.marshal (Python 3.13)

'''Abstract base classes related to import.'''
from  import _bootstrap_external
from  import machinery

try:
    import _frozen_importlib
except ImportError:
    exc = <NODE:27>
    if exc.name != '_frozen_importlib':
        pass
    raise 
    _frozen_importlib = None


try:
    import _frozen_importlib_external
except ImportError:
    _frozen_importlib_external = _bootstrap_external

from _abc import Loader
import abc
import warnings
from resources import abc as _resources_abc
__all__ = [
    'Loader',
    'MetaPathFinder',
    'PathEntryFinder',
    'ResourceLoader',
    'InspectLoader',
    'ExecutionLoader',
    'FileLoader',
    'SourceLoader']

def __getattr__(name):
    '''
For backwards compatibility, continue to make names
from _resources_abc available through this module. #93963
'''
    if name in _resources_abc.__all__:
        obj = getattr(_resources_abc, name)
        None(f'''{__name__}.{name}''', remove = (3, 14))
        globals()[name] = obj
    return obj
    raise AttributeError(f'''module {__name__} has no attribute {name}''')


def _register(abstract_cls, *classes):
    for cls in classes:
        abstract_cls.register(cls)
        if _frozen_importlib:
            continue
        
        try:
            frozen_cls = getattr(_frozen_importlib, cls.__name__)
        except AttributeError:
            frozen_cls = getattr(_frozen_importlib_external, cls.__name__)

        abstract_cls.register(frozen_cls)

MetaPathFinder = None((lambda : __firstlineno__ = 52__doc__ = 'Abstract base class for import finders on sys.meta_path.'
def invalidate_caches(self):
"""An optional method for clearing the finder's cache, if any.
This method is used by importlib.invalidate_caches().
"""
pass__static_attributes__ = ()), 'MetaPathFinder', metaclass = abc.ABCMeta)
<NODE:12>
PathEntryFinder = None((lambda : __firstlineno__ = 68__doc__ = 'Abstract base class for path entry finders used by PathFinder.'
def invalidate_caches(self):
"""An optional method for clearing the finder's cache, if any.
This method is used by PathFinder.invalidate_caches().
"""
pass__static_attributes__ = ()), 'PathEntryFinder', metaclass = abc.ABCMeta)
<NODE:12>

def ResourceLoader():
    '''ResourceLoader'''
    __firstlineno__ = 80
    __doc__ = 'Abstract base class for loaders which can return data from their\nback-end storage.\n\nThis ABC represents one of the optional protocols specified by PEP 302.\n\n'
    get_data = (lambda self, path: raise OSError)()
    __static_attributes__ = ()

ResourceLoader = None(ResourceLoader, 'ResourceLoader', Loader)

def InspectLoader():
    '''InspectLoader'''
    __firstlineno__ = 96
    __doc__ = 'Abstract base class for loaders which support inspection about the\nmodules they can load.\n\nThis ABC represents one of the optional protocols specified by PEP 302.\n\n'
    
    def is_package(self, fullname):
        '''Optional method which when implemented should return whether the
module is a package.  The fullname is a str.  Returns a bool.

Raises ImportError if the module cannot be found.
'''
        raise ImportError

    
    def get_code(self, fullname):
        '''Method which returns the code object for the module.

The fullname is a str.  Returns a types.CodeType if possible, else
returns None if a code object does not make sense
(e.g. built-in module). Raises ImportError if the module cannot be
found.
'''
        source = self.get_source(fullname)
        if source:
            pass
        return None
        return self.source_to_code(source)

    get_source = (lambda self, fullname: raise ImportError)()
    if (lambda data, path: compile(data, path, 'exec', dont_inherit = True)):
        pass
    source_to_code = (lambda data, path: compile(data, path, 'exec', dont_inherit = True))()
    exec_module = _bootstrap_external._LoaderBasics.exec_module
    load_module = _bootstrap_external._LoaderBasics.load_module
    __static_attributes__ = ()

InspectLoader = None(InspectLoader, 'InspectLoader', Loader)
<NODE:12>

def ExecutionLoader():
    '''ExecutionLoader'''
    __firstlineno__ = 149
    __doc__ = 'Abstract base class for loaders that wish to support the execution of\nmodules as scripts.\n\nThis ABC represents one of the optional protocols specified in PEP 302.\n\n'
    get_filename = (lambda self, fullname: raise ImportError)()
    
    def get_code(self, fullname):
        '''Method to return the code object for fullname.

Should return None if not applicable (e.g. built-in module).
Raise ImportError if the module cannot be found.
'''
        source = self.get_source(fullname)
        if source:
            pass
        return None
        
        try:
            path = self.get_filename(fullname)
        except ImportError:
            source

        return self.source_to_code(source, path)

    __static_attributes__ = ()

ExecutionLoader = None(ExecutionLoader, 'ExecutionLoader', InspectLoader)
<NODE:12>

def FileLoader():
    '''FileLoader'''
    __firstlineno__ = 190
    __doc__ = 'Abstract base class partially implementing the ResourceLoader and\nExecutionLoader ABCs.'
    __static_attributes__ = ()

FileLoader = None(FileLoader, 'FileLoader', _bootstrap_external.FileLoader, ResourceLoader, ExecutionLoader)
<NODE:12>

def SourceLoader():
    '''SourceLoader'''
    __firstlineno__ = 199
    __doc__ = 'Abstract base class for loading source code (and optionally any\ncorresponding bytecode).\n\nTo support loading from source code, the abstractmethods inherited from\nResourceLoader and ExecutionLoader need to be implemented. To also support\nloading from bytecode, the optional methods specified directly by this ABC\nis required.\n\nInherited abstractmethods not implemented in this ABC:\n\n    * ResourceLoader.get_data\n    * ExecutionLoader.get_filename\n\n'
    
    def path_mtime(self, path):
        '''Return the (int) modification time for the path (str).'''
        if self.path_stats.__func__ is SourceLoader.path_stats:
            pass
        raise OSError
        return int(self.path_stats(path)['mtime'])

    
    def path_stats(self, path):
        """Return a metadata dict for the source pointed to by the path (str).
Possible keys:
- 'mtime' (mandatory) is the numeric timestamp of last source
  code modification;
- 'size' (optional) is the size in bytes of the source code.
"""
        if self.path_mtime.__func__ is SourceLoader.path_mtime:
            pass
        raise OSError
        return {
            'mtime': self.path_mtime(path) }

    
    def set_data(self, path, data):
        '''Write the bytes to the path (if possible).

Accepts a str path and data as bytes.

Any needed intermediary directories are to be created. If for some
reason the file cannot be written because of permissions, fail
silently.
'''
        pass

    __static_attributes__ = ()

SourceLoader = None(SourceLoader, 'SourceLoader', _bootstrap_external.SourceLoader, ResourceLoader, ExecutionLoader)
<NODE:12>
