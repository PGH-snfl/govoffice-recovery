# Source Generated with Decompyle++
# File: _threading_local.marshal (Python 3.13)

"""Thread-local objects.

(Note that this module provides a Python version of the threading.local
 class.  Depending on the version of Python you're using, there may be a
 faster one available.  You should always import the `local` class from
 `threading`.)
"""
from weakref import ref
from contextlib import contextmanager
__all__ = [
    'local']

def _localimpl():
    '''_localimpl'''
    __firstlineno__ = 24
    __doc__ = 'A class managing thread-local dicts'
    __slots__ = ('key', 'dicts', 'localargs', 'locallock', '__weakref__')
    
    def __init__(self):
        self.key = '_threading_local._localimpl.' + str(id(self))
        self.dicts = { }

    
    def get_dict(self):
        '''Return the dict for the current thread. Raises KeyError if none
defined.'''
        thread = current_thread()
        return self.dicts[id(thread)][1]

    
    def create_dict(self):
        '''Create a new dict for the current thread, and return it.'''
        localdict = { }
        key = self.key
        thread = current_thread()
        idt = id(thread)
        if (lambda _, key: thread = None()if thread:
del thread.__dict__[key]None):
            if (lambda _, key: thread = None()if thread:
del thread.__dict__[key]None):
                
                def local_deleted(_, key):
                    thread = None()
                    if thread:
                        del thread.__dict__[key]
                    return None

        if (lambda _, idt: local = None()if local:
dct = local.dicts.pop(idt)None):
            if (lambda _, idt: local = None()if local:
dct = local.dicts.pop(idt)None):
                
                def thread_deleted(_, idt):
                    local = None()
                    if local:
                        dct = local.dicts.pop(idt)
                    return None

        wrlocal = ref(self, local_deleted)
        wrthread = ref(thread, thread_deleted)
        thread.__dict__[key] = wrlocal
        self.dicts[idt] = (wrthread, localdict)
        return localdict

    __static_attributes__ = ('dicts', 'key')

_localimpl = None(_localimpl, '_localimpl')

class _patch:
