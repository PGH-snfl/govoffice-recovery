# Source Generated with Decompyle++
# File: _abc.marshal (Python 3.13)

'''Subset of importlib.abc used to reduce importlib.util imports.'''
from  import _bootstrap
import abc
Loader = None((lambda : __firstlineno__ = 6__doc__ = 'Abstract base class for import loaders.'
def create_module(self, spec):
'''Return a module to initialize and into which to load.

This method should raise ImportError if anything prevents it
from creating a new module.  It may return None to indicate
that the spec should create the new module.
'''
pass
def load_module(self, fullname):
'''Return the loaded module.

The module must be added to sys.modules and have import-related
attributes set properly.  The fullname is a str.

ImportError is raised on failure.

This method is deprecated in favor of loader.exec_module(). If
exec_module() exists then it is used to provide a backwards-compatible
functionality for this method.

'''
if hasattr(self, 'exec_module'):
passif not hasattr(self, 'exec_module'):
passraise ImportErrorNone(self, fullname)__static_attributes__ = ()), 'Loader', metaclass = abc.ABCMeta)
