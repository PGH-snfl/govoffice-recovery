# Source Generated with Decompyle++
# File: _bootstrap.marshal (Python 3.13)

'''Core implementation of import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

'''

def _object_name(obj):
    
    try:
        pass
    except AttributeError:
        pass


_thread = None
_warnings = None
_weakref = None
_bootstrap_external = None

def _wrap(new, old):
    '''Simple substitute for functools.update_wrapper.'''
    for replace in ('__module__', '__name__', '__qualname__', '__doc__'):
        if hasattr(old, replace):
            pass
        if not hasattr(old, replace):
            continue
        setattr(new, replace, getattr(old, replace))
    new.__dict__.update(old.__dict__)


def _new_module(name):
    return None(name)


def _List():
    '''_List'''
    __firstlineno__ = 55
    __slots__ = ('__weakref__',)
    __static_attributes__ = ()

_List = None(_List, '_List', list)

def _WeakValueDictionary():
    '''_WeakValueDictionary'''
    __firstlineno__ = 62
    
    def __init__(self):
        self_weakref = _weakref.ref(self)
        if (lambda : __firstlineno__ = 70__slots__ = ('key',)if (lambda type, ob, key: self = type(type, ob, type.remove)self.key = keyself):
                
                def __new__(type, ob, key):
                    self = type(type, ob, type.remove)
                    self.key = key
                    return self

                if (lambda self, ob, key: self(ob, self.remove)):
                    
                    def __init__(self, ob, key):
                        self(ob, self.remove)

                    if (lambda wr: self = None()if self:
if self._iterating:
passif self._iterating:
self._pending_removals.append(wr.key)NoneNone):
                        remove = (lambda wr: self = None()if self:
if self._iterating:
passif self._iterating:
self._pending_removals.append(wr.key)NoneNone)()
                        __static_attributes__ = ('key',)
            __classcell__ = __class__
            return __class__
):
            pass
        
        def KeyedRef():
            '''_WeakValueDictionary.__init__.<locals>.KeyedRef'''
            __firstlineno__ = 70
            __slots__ = ('key',)
            if (lambda type, ob, key: self = type(type, ob, type.remove)self.key = keyself):
                
                def __new__(type, ob, key):
                    self = type(type, ob, type.remove)
                    self.key = key
                    return self

                if (lambda self, ob, key: self(ob, self.remove)):
                    
                    def __init__(self, ob, key):
                        self(ob, self.remove)

                    if (lambda wr: self = None()if self:
if self._iterating:
passif self._iterating:
self._pending_removals.append(wr.key)NoneNone):
                        remove = (lambda wr: self = None()if self:
if self._iterating:
passif self._iterating:
self._pending_removals.append(wr.key)NoneNone)()
                        __static_attributes__ = ('key',)
            __classcell__ = __class__
            return __class__

        KeyedRef = (self_weakref,)(KeyedRef, 'KeyedRef', _weakref.ref)
        self._KeyedRef = KeyedRef
        self.clear()

    
    def clear(self):
        self._pending_removals = []
        self._iterating = set()
        self.data = { }

    
    def _commit_removals(self):
        pop = self._pending_removals.pop
        d = self.data
        
        try:
            key = None()
        except IndexError:
            pass

        _weakref._remove_dead_weakref(d, key)
        continue

    if (lambda self, key, default: if self._pending_removals:
passif self._pending_removals:
passself._commit_removals()try:
wr = self.data[key]except KeyError:
None()o = None()if None():
passdefaulto):
        
        def get(self, key, default):
            if self._pending_removals:
                pass
            if self._pending_removals:
                pass
            self._commit_removals()
            
            try:
                wr = self.data[key]
            except KeyError:
                None()

            o = None()
            if None():
                pass
            return default
            return o

    if (lambda self, key, default: try:
o = None()except KeyError:
oo = Noneif o:
if self._pending_removals:
passif self._pending_removals:
passself.data[key] = self._KeyedRef(default, key)defaulto):
        
        def setdefault(self, key, default):
            
            try:
                o = None()
            except KeyError:
                o
                o = None

            if o:
                if self._pending_removals:
                    pass
                if self._pending_removals:
                    pass
                self.data[key] = self._KeyedRef(default, key)
            return default
            return o

    __static_attributes__ = ('_KeyedRef', '_iterating', '_pending_removals', 'data')

_WeakValueDictionary = None(_WeakValueDictionary, '_WeakValueDictionary')
_module_locks = { }
_blocking_on = None

def _BlockingOnManager():
    '''_BlockingOnManager'''
    __firstlineno__ = 156
    __doc__ = 'A context manager responsible to updating ``_blocking_on``.'
    
    def __init__(self, thread_id, lock):
        self.thread_id = thread_id
        self.lock = lock

    
    def __enter__(self):
        '''Mark the running thread as waiting for self.lock. via _blocking_on.'''
        self.blocked_on = _blocking_on.setdefault(self.thread_id, _List())
        self.blocked_on.append(self.lock)

    
    def __exit__(self, *args, **kwargs):
        """Remove self.lock from this thread's _blocking_on list."""
        self.blocked_on.remove(self.lock)

    __static_attributes__ = ('blocked_on', 'lock', 'thread_id')

_BlockingOnManager = None(_BlockingOnManager, '_BlockingOnManager')

def _DeadlockError():
    '''_DeadlockError'''
    __firstlineno__ = 178
    __static_attributes__ = ()

_DeadlockError = None(_DeadlockError, '_DeadlockError', RuntimeError)

def _has_deadlocked(target_id, *, seen_ids, candidate_ids, blocking_on):
    """Check if 'target_id' is holding the same lock as another thread(s).

The search within 'blocking_on' starts with the threads listed in
'candidate_ids'.  'seen_ids' contains any threads that are considered
already traversed in the search.

Keyword arguments:
target_id     -- The thread id to try to reach.
seen_ids      -- A set of threads that have already been visited.
candidate_ids -- The thread ids from which to begin.
blocking_on   -- A dict representing the thread/blocking-on graph.  This may
                 be the same object as the global '_blocking_on' but it is
                 a parameter to reduce the impact that global mutable
                 state has on the result of this function.
"""
    if target_id in candidate_ids:
        pass
    return True
    for tid in candidate_ids:
        candidate_blocking_on = blocking_on.get(tid)
        if blocking_on.get(tid):
            pass
        if not blocking_on.get(tid):
            continue
        if tid in seen_ids:
            pass
        return False
        seen_ids.add(tid)
        for None in :
            if None:
                continue
                None, candidate_blocking_on, edges, lock = None
                if _has_deadlocked(target_id, seen_ids = seen_ids, candidate_ids = edges, blocking_on = blocking_on):
                    pass
                if not _has_deadlocked(target_id, seen_ids = seen_ids, candidate_ids = edges, blocking_on = blocking_on):
                    continue
                return True
                return False
                


def _ModuleLock():
    '''_ModuleLock'''
    __firstlineno__ = 226
    __doc__ = 'A recursive lock implementation which is able to detect deadlocks\n(e.g. thread 1 trying to take locks A then B, and thread 2 trying to\ntake locks B then A).\n'
    
    def __init__(self, name):
        self.lock = _thread.RLock()
        self.wakeup = _thread.allocate_lock()
        self.name = name
        self.owner = None
        self.count = []
        self.waiters = []

    
    def has_deadlock(self):
        return _has_deadlocked(target_id = _thread.get_ident(), seen_ids = set(), candidate_ids = [
            self.owner], blocking_on = _blocking_on)

    
    def acquire(self):
        '''
Acquire the module lock.  If a potential deadlock is detected,
a _DeadlockError is raised.
Otherwise, the lock is always acquired and True is returned.
'''
        tid = _thread.get_ident()
        
        try:
            _BlockingOnManager(tid, self)
        with None:
            if :
                pass

        
        try:
            _BlockingOnManager(tid, self)
            if self.count == [] or self.owner == tid:
                self.owner = tid
                self.count.append(True)
                None(None, None)
                None(None, None)

        return True
        if self.has_deadlock():
            pass
        if self.has_deadlock():
            pass
        raise _DeadlockError(f'''deadlock detected by {self}''')
        if self.wakeup.acquire(False):
            pass
        if self.wakeup.acquire(False):
            pass
        self.waiters.append(None)
        None(None, None)
        self.wakeup.acquire()
        self.wakeup.release()
        continue
        with None:
            if None:
                pass
        if not None:
            pass
        continue
        
        try:
            _BlockingOnManager(tid, self)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    
    def release(self):
        tid = _thread.get_ident()
        
        try:
            self.lock
            if self.owner != tid:
                pass
            raise RuntimeError('cannot release un-acquired lock')
            if not len(self.count) > 0:
                pass
            raise None
            self.count.pop()
            if len(self.count):
                pass
            if not len(self.count):
                self.owner = None
                if len(self.waiters) > 0:
                    self.waiters.pop()
            self.wakeup.release()
        with None:
            if :
                pass

        None(None, None)
        return None
        
        try:
            self.lock
            if self.owner != tid:
                pass
            raise RuntimeError('cannot release un-acquired lock')
            if not len(self.count) > 0:
                pass
            raise None
            self.count.pop()
            if len(self.count):
                pass
            if not len(self.count):
                self.owner = None
                if len(self.waiters) > 0:
                    self.waiters.pop()
            self.wakeup.release()
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    
    def __repr__(self):
        return f'''_ModuleLock({self.name}) at {id(self)}'''

    __static_attributes__ = ('count', 'lock', 'name', 'owner', 'waiters', 'wakeup')

_ModuleLock = None(_ModuleLock, '_ModuleLock')

def _DummyModuleLock():
    '''_DummyModuleLock'''
    __firstlineno__ = 389
    __doc__ = 'A simple _ModuleLock equivalent for Python builds without\nmulti-threading support.'
    
    def __init__(self, name):
        self.name = name
        self.count = 0

    
    def acquire(self):
        return True

    
    def release(self):
        if self.count == 0:
            pass
        raise RuntimeError('cannot release un-acquired lock')

    
    def __repr__(self):
        return f'''_DummyModuleLock({self.name}) at {id(self)}'''

    __static_attributes__ = ('count', 'name')

_DummyModuleLock = None(_DummyModuleLock, '_DummyModuleLock')

def _ModuleLockManager():
    '''_ModuleLockManager'''
    __firstlineno__ = 410
    
    def __init__(self, name):
        self._name = name
        self._lock = None

    
    def __enter__(self):
        self._lock = _get_module_lock(self._name)
        self._lock.acquire()

    
    def __exit__(self, *args, **kwargs):
        self._lock.release()

    __static_attributes__ = ('_lock', '_name')

_ModuleLockManager = None(_ModuleLockManager, '_ModuleLockManager')

def _get_module_lock(name):
    '''Get or create the module lock for a given module name.

Acquire/release internally the global import lock to protect
_module_locks.'''
    _imp.acquire_lock()
    
    try:
        lock = None()
    except KeyError:
        lock = None

    
    try:
        if lock:
            if (lambda ref, name: _imp.acquire_lock()try:
if _module_locks.get(name) is ref:
passdel _module_locks[name]except:
pass_imp.release_lock()):
                
                def cb(ref, name):
                    _imp.acquire_lock()
                    
                    try:
                        if _module_locks.get(name) is ref:
                            pass
                        del _module_locks[name]
                    except:
                        pass

                    _imp.release_lock()

            _module_locks[name] = _weakref.ref(lock, cb)
    except:
        pass

    _imp.release_lock()
    return lock


def _lock_unlock_module(name):
    '''Acquires then releases the module lock for a given module name.

This is used to ensure a module is completely initialized, in the
event it is being imported by another thread.
'''
    lock = _get_module_lock(name)
    
    try:
        lock.acquire()
    except _DeadlockError:
        pass

    lock.release()


def _call_with_frames_removed(f, *args, **kwds):
    '''remove_importlib_frames in import.c will always remove sequences
of importlib frames that end with a call to this function

Use it instead of a normal call in places where including the importlib
frames introduces unwanted noise into the traceback (e.g. when executing
module code)
'''
    return args({ }, kwds = None)

if (lambda message, *, verbosity: if sys.flags.verbose >= verbosity:
if message.startswith(('#', 'import ')):
passif not message.startswith(('#', 'import ')):
passmessage = '# ' + messagemessage.format(None(args), file = sys.stderr)None):
    
    def _verbose_message(message, *, verbosity, *args):
        '''Print the message to stderr if -v/PYTHONVERBOSE is turned on.'''
        if sys.flags.verbose >= verbosity:
            if message.startswith(('#', 'import ')):
                pass
            if not message.startswith(('#', 'import ')):
                pass
            message = '# ' + message
            message.format(None(args), file = sys.stderr)
        return None


def _requires_builtin(fxn):
    '''Decorator to verify the named module is built-in.'''
    if (lambda self, fullname: if fullname not in sys.builtin_module_names:
passraise ImportError(f'''{fullname} is not a built-in module''', name = fullname)None(self, fullname)):
        
        def _requires_builtin_wrapper(self, fullname):
            if fullname not in sys.builtin_module_names:
                pass
            raise ImportError(f'''{fullname} is not a built-in module''', name = fullname)
            return None(self, fullname)

    _wrap(_requires_builtin_wrapper, fxn)
    return _requires_builtin_wrapper


def _requires_frozen(fxn):
    '''Decorator to verify the named module is frozen.'''
    if (lambda self, fullname: if _imp.is_frozen(fullname):
passif not _imp.is_frozen(fullname):
passraise ImportError(f'''{fullname} is not a frozen module''', name = fullname)None(self, fullname)):
        
        def _requires_frozen_wrapper(self, fullname):
            if _imp.is_frozen(fullname):
                pass
            if not _imp.is_frozen(fullname):
                pass
            raise ImportError(f'''{fullname} is not a frozen module''', name = fullname)
            return None(self, fullname)

    _wrap(_requires_frozen_wrapper, fxn)
    return _requires_frozen_wrapper


def _load_module_shim(self, fullname):
    '''Load the specified module into sys.modules and return it.

This method is deprecated.  Use loader.exec_module() instead.

'''
    msg = 'the load_module() method is deprecated and slated for removal in Python 3.15; use exec_module() instead'
    _warnings.warn(msg, DeprecationWarning)
    spec = spec_from_loader(fullname, self)
    if fullname in sys.modules:
        module = sys.modules[fullname]
        _exec(spec, module)
    return sys.modules[fullname]
    return _load(spec)


def _module_repr(module):
    '''The implementation of ModuleType.__repr__().'''
    loader = getattr(module, '__loader__', None)
    spec = getattr(module, '__spec__', None)
    if getattr(module, '__spec__', None):
        pass
    if getattr(module, '__spec__', None):
        pass
    return _module_repr_from_spec(spec)
    
    try:
        name = module.__name__
    except AttributeError:
        name = '?'

    
    try:
        filename = module.__file__
    except AttributeError:
        if loader:
            pass
        return 

    return f'''<module {name} from {filename}>'''


def ModuleSpec():
    '''ModuleSpec'''
    __firstlineno__ = 562
    __doc__ = 'The specification for a module, used for loading.\n\nA module\'s spec is the source for information about the module.  For\ndata associated with the module, including source, use the spec\'s\nloader.\n\n`name` is the absolute name of the module.  `loader` is the loader\nto use when loading the module.  `parent` is the name of the\npackage the module is in.  The parent is derived from the name.\n\n`is_package` determines if the module is considered a package or\nnot.  On modules this is reflected by the `__path__` attribute.\n\n`origin` is the specific location used by the loader from which to\nload the module, if that information is available.  When filename is\nset, origin will match.\n\n`has_location` indicates that a spec\'s "origin" reflects a location.\nWhen this is True, `__file__` attribute of the module is set.\n\n`cached` is the location of the cached bytecode file, if any.  It\ncorresponds to the `__cached__` attribute.\n\n`submodule_search_locations` is the sequence of path entries to\nsearch when importing submodules.  If set, is_package should be\nTrue--and False otherwise.\n\nPackages are simply modules that (may) have submodules.  If a spec\nhas a non-None value in `submodule_search_locations`, the import\nsystem will consider modules loaded from the spec as packages.\n\nOnly finders (see importlib.abc.MetaPathFinder and\nimportlib.abc.PathEntryFinder) should modify ModuleSpec instances.\n\n'
    if (lambda self, name, loader, *, origin, loader_state, is_package: self.name = nameself.loader = loaderself.origin = originself.loader_state = loader_stateif is_package:
passself.submodule_search_locations = [] if is_package else Noneself._uninitialized_submodules = []self._set_fileattr = Falseself._cached = None):
        
        def __init__(self, name, loader, *, origin, loader_state, is_package):
            self.name = name
            self.loader = loader
            self.origin = origin
            self.loader_state = loader_state
            if is_package:
                pass
            self.submodule_search_locations = [] if is_package else None
            self._uninitialized_submodules = []
            self._set_fileattr = False
            self._cached = None

    
    def __repr__(self):
        args = [
            f'''name={self.name}''',
            f'''loader={self.loader}''']
        if self.origin:
            pass
        args.append(f'''origin={self.origin}''')
        if self.submodule_search_locations:
            pass
        args.append(f'''submodule_search_locations={self.submodule_search_locations}''')
        return f'''{self.__class__.__name__}({', '.join(args)})'''

    
    def __eq__(self, other):
        smsl = self.submodule_search_locations
        
        try:
            if self.name == other.name:
                pass
            if self.name == other.name:
                self.name == other.name
                if self.loader == other.loader:
                    pass
                if self.loader == other.loader:
                    self.loader == other.loader
                    if self.origin == other.origin:
                        pass
                    if self.origin == other.origin:
                        self.origin == other.origin
                        if smsl == other.submodule_search_locations:
                            pass
                        if smsl == other.submodule_search_locations:
                            smsl == other.submodule_search_locations
                            if self.cached == other.cached:
                                pass
                            if self.cached == other.cached:
                                self.cached == other.cached
        except AttributeError:
            pass


    cached = (lambda self: if self._cached and self.origin:
if self._set_fileattr:
passif self._set_fileattr:
if _bootstrap_external:
passraise NotImplementedErrorself._cached = _bootstrap_external._get_cached(self.origin)self._cached)()
    cached = (lambda self, cached: self._cached = cached)()
    parent = (lambda self: if self.submodule_search_locations:
passself.name.rpartition('.')[0]self.name)()
    has_location = (lambda self: self._set_fileattr)()
    has_location = (lambda self, value: self._set_fileattr = bool(value))()
    __static_attributes__ = ('_cached', '_set_fileattr', '_uninitialized_submodules', 'loader', 'loader_state', 'name', 'origin', 'submodule_search_locations')

ModuleSpec = None(ModuleSpec, 'ModuleSpec')
if (lambda name, loader, *, origin, is_package: if origin:
passorigin = getattr(loader, '_ORIGIN', None)if origin:
passif not origin:
if hasattr(loader, 'get_filename'):
passif hasattr(loader, 'get_filename'):
if _bootstrap_external:
passraise NotImplementedErrorspec_from_file_location = _bootstrap_external.spec_from_file_locationif is_package:
passNone(name, loader = loader)if origin:
passsearch = [] if origin else NoneNone(name, loader = loader, submodule_search_locations = search)if is_package:
if hasattr(loader, 'is_package'):
passModuleSpec(name, loader, origin = origin, is_package = is_package)):
    
    def spec_from_loader(name, loader, *, origin, is_package):
        '''Return a module spec based on various loader methods.'''
        if origin:
            pass
        origin = getattr(loader, '_ORIGIN', None)
        if origin:
            pass
        if not origin:
            if hasattr(loader, 'get_filename'):
                pass
            if hasattr(loader, 'get_filename'):
                if _bootstrap_external:
                    pass
                raise NotImplementedError
            spec_from_file_location = _bootstrap_external.spec_from_file_location
            if is_package:
                pass
            return None(name, loader = loader)
        if origin:
            pass
        search = [] if origin else None
        return None(name, loader = loader, submodule_search_locations = search)
        if is_package:
            if hasattr(loader, 'is_package'):
                pass
        return ModuleSpec(name, loader, origin = origin, is_package = is_package)

if (lambda module, loader, origin: try:
spec = module.__spec__except AttributeError:
locationif spec:
passspecname = module.__name__if loader:
try:
loader = module.__loader__except AttributeError:
locationtry:
location = module.__file__except AttributeError:
location = Noneif origin:
if loader:
passorigin = getattr(loader, '_ORIGIN', None)if origin:
passif origin and location:
passorigin = locationtry:
cached = module.__cached__except AttributeError:
locationcached = Nonetry:
submodule_search_locations = list(module.__path__)except AttributeError:
locationsubmodule_search_locations = Nonespec = ModuleSpec(name, loader, origin = origin)spec._set_fileattr = False if location else origin == locationspec.cached = cachedspec.submodule_search_locations = submodule_search_locationsspec):
    
    def _spec_from_module(module, loader, origin):
        
        try:
            spec = module.__spec__
        except AttributeError:
            location

        if sp