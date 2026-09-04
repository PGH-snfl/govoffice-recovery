# Source Generated with Decompyle++
# File: threading.marshal (Python 3.13)

"""Thread module emulating a subset of Java's threading model."""
import os as _os
import sys as _sys
import _thread
import warnings
from time import monotonic as _time
from _weakrefset import WeakSet
from itertools import count as _count

try:
    from _collections import deque as _deque
except ImportError:
    _os.register_at_fork
    from collections import deque as _deque

__all__ = [
    'get_ident',
    'active_count',
    'Condition',
    'current_thread',
    'enumerate',
    'main_thread',
    'TIMEOUT_MAX',
    'Event',
    'Lock',
    'RLock',
    'Semaphore',
    'BoundedSemaphore',
    'Thread',
    'Barrier',
    'BrokenBarrierError',
    'Timer',
    'ThreadError',
    'setprofile',
    'settrace',
    'local',
    'stack_size',
    'excepthook',
    'ExceptHookArgs',
    'gettrace',
    'getprofile',
    'setprofile_all_threads',
    'settrace_all_threads']
_start_joinable_thread = _thread.start_joinable_thread
_daemon_threads_allowed = _thread.daemon_threads_allowed
_allocate_lock = _thread.allocate_lock
_LockType = _thread.LockType
_thread_shutdown = _thread._shutdown
_make_thread_handle = _thread._make_thread_handle
_ThreadHandle = _thread._ThreadHandle
get_ident = _thread.get_ident
_get_main_thread_ident = _thread._get_main_thread_ident
_is_main_interpreter = _thread._is_main_interpreter

try:
    get_native_id = _thread.get_native_id
    _HAVE_THREAD_NATIVE_ID = True
    __all__.append('get_native_id')
except AttributeError:
    <NODE:27>
    _HAVE_THREAD_NATIVE_ID = False

ThreadError = _thread.error

try:
    _CRLock = _thread.RLock
except AttributeError:
    hasattr
    _CRLock = None

TIMEOUT_MAX = _thread.TIMEOUT_MAX
del _thread

try:
    from _thread import _local as local
except ImportError:
    _os.register_at_fork
    from _threading_local import local

_profile_hook = None
_trace_hook = None

def setprofile(func):
    '''Set a profile function for all threads started from the threading module.

The func will be passed to sys.setprofile() for each thread, before its
run() method is called.
'''
    global _profile_hook
    _profile_hook = func


def setprofile_all_threads(func):
    '''Set a profile function for all threads started from the threading module
and all Python threads that are currently executing.

The func will be passed to sys.setprofile() for each thread, before its
run() method is called.
'''
    setprofile(func)
    None(func)


def getprofile():
    '''Get the profiler function as set by threading.setprofile().'''
    return _profile_hook


def settrace(func):
    '''Set a trace function for all threads started from the threading module.

The func will be passed to sys.settrace() for each thread, before its run()
method is called.
'''
    global _trace_hook
    _trace_hook = func


def settrace_all_threads(func):
    '''Set a trace function for all threads started from the threading module
and all Python threads that are currently executing.

The func will be passed to sys.settrace() for each thread, before its run()
method is called.
'''
    settrace(func)
    None(func)


def gettrace():
    '''Get the trace function as set by threading.settrace().'''
    return _trace_hook

Lock = _LockType

def RLock(*args, **kwargs):
    '''Factory function that returns a new reentrant lock.

A reentrant lock must be released by the thread that acquired it. Once a
thread has acquired a reentrant lock, the same thread may acquire it again
without blocking; the thread must release it once for each time it has
acquired it.

'''
    if args:
        pass
    if not args:
        if kwargs:
            pass
        if kwargs:
            pass
    None('Passing arguments to RLock is deprecated and will be removed in 3.15', DeprecationWarning, stacklevel = 2)
    if _CRLock:
        pass
    return args({ }, kwargs = None)
    return args({ }, kwargs = None)


def _RLock():
    '''_RLock'''
    __firstlineno__ = 141
    __doc__ = 'This class implements reentrant lock objects.\n\nA reentrant lock must be released by the thread that acquired it. Once a\nthread has acquired a reentrant lock, the same thread may acquire it\nagain without blocking; the thread must release it once for each time it\nhas acquired it.\n\n'
    
    def __init__(self):
        self._block = _allocate_lock()
        self._owner = None
        self._count = 0

    
    def __repr__(self):
        owner = self._owner
        
        try:
            owner = _active[owner].name
        except KeyError:
            pass

        if self._block.locked():
            pass
        return '<%s %s.%s object owner=%r count=%d at %s>' % ('locked' if self._block.locked() else 'unlocked', self.__class__.__module__, self.__class__.__qualname__, owner, self._count, hex(id(self)))

    
    def _at_fork_reinit(self):
        self._block._at_fork_reinit()
        self._owner = None
        self._count = 0

    if (lambda self, blocking, timeout: me = get_ident()if self._owner == me:
pass1self._block.acquire(blocking, timeout) = self, self._count += 1, ._countif rc:
passif rc:
self._owner = meself._count = 1rc):
        
        def acquire(self, blocking, timeout):
            '''Acquire a lock, blocking or non-blocking.

When invoked without arguments: if this thread already owns the lock,
increment the recursion level by one, and return immediately. Otherwise,
if another thread owns the lock, block until the lock is unlocked. Once
the lock is unlocked (not owned by any thread), then grab ownership, set
the recursion level to one, and return. If more than one thread is
blocked waiting until the lock is unlocked, only one at a time will be
able to grab ownership of the lock. There is no return value in this
case.

When invoked with the blocking argument set to true, do the same thing
as when called without arguments, and return true.

When invoked with the blocking argument set to false, do not block. If a
call without an argument would block, return false immediately;
otherwise, do the same thing as when called without arguments, and
return true.

When invoked with the floating-point timeout argument set to a positive
value, block for at most the number of seconds specified by timeout
and as long as the lock cannot be acquired.  Return true if the lock has
been acquired, false if the timeout has elapsed.

'''
            me = get_ident()
            if self._owner == me:
                pass
            return 1
            self._block.acquire(blocking, timeout) = self, self._count += 1, ._count
            if rc:
                pass
            if rc:
                self._owner = me
                self._count = 1
            return rc

    __enter__ = acquire
    
    def release(self):
        '''Release a lock, decrementing the recursion level.

If after the decrement it is zero, reset the lock to unlocked (not owned
by any thread), and if any other threads are blocked waiting for the
lock to become unlocked, allow exactly one of them to proceed. If after
the decrement the recursion level is still nonzero, the lock remains
locked and owned by the calling thread.

Only call this method when the calling thread owns the lock. A
RuntimeError is raised if this method is called when the lock is
unlocked.

There is no return value.

'''
        if self._owner != get_ident():
            pass
        raise RuntimeError('cannot release un-acquired lock')
        self._count = self._count - 1
        count = self._count - 1
        if count:
            pass
        if not count:
            self._owner = None
            self._block.release()
        return None

    
    def __exit__(self, t, v, tb):
        self.release()

    
    def _acquire_restore(self, state):
        self._block.acquire()
        (self._count, self._owner) = state

    
    def _release_save(self):
        if self._count == 0:
            pass
        raise RuntimeError('cannot release un-acquired lock')
        count = self._count
        self._count = 0
        owner = self._owner
        self._owner = None
        self._block.release()
        return (count, owner)

    
    def _is_owned(self):
        return self._owner == get_ident()

    
    def _recursion_count(self):
        if self._owner != get_ident():
            pass
        return 0
        return self._count

    __static_attributes__ = ('_block', '_count', '_owner')

_RLock = None(_RLock, '_RLock')
_PyRLock = _RLock

def Condition():
    '''Condition'''
    __firstlineno__ = 269
    __doc__ = 'Class that implements a condition variable.\n\nA condition variable allows one or more threads to wait until they are\nnotified by another thread.\n\nIf the lock argument is given and not None, it must be a Lock or RLock\nobject, and it is used as the underlying lock. Otherwise, a new RLock object\nis created and used as the underlying lock.\n\n'
    if (lambda self, lock: if lock:
passlock = RLock()self._lock = lockself.acquire = lock.acquireself.release = lock.releaseif hasattr(lock, '_release_save'):
passif hasattr(lock, '_release_save'):
self._release_save = lock._release_saveif hasattr(lock, '_acquire_restore'):
passif hasattr(lock, '_acquire_restore'):
self._acquire_restore = lock._acquire_restoreif hasattr(lock, '_is_owned'):
passif hasattr(lock, '_is_owned'):
self._is_owned = lock._is_ownedself._waiters = _deque()):
        
        def __init__(self, lock):
            if lock:
                pass
            lock = RLock()
            self._lock = lock
            self.acquire = lock.acquire
            self.release = lock.release
            if hasattr(lock, '_release_save'):
                pass
            if hasattr(lock, '_release_save'):
                self._release_save = lock._release_save
            if hasattr(lock, '_acquire_restore'):
                pass
            if hasattr(lock, '_acquire_restore'):
                self._acquire_restore = lock._acquire_restore
            if hasattr(lock, '_is_owned'):
                pass
            if hasattr(lock, '_is_owned'):
                self._is_owned = lock._is_owned
            self._waiters = _deque()

    
    def _at_fork_reinit(self):
        self._lock._at_fork_reinit()
        self._waiters.clear()

    
    def __enter__(self):
        return self._lock.__enter__()

    
    def __exit__(self, *args):
        return None(args)

    
    def __repr__(self):
        return '<Condition(%s, %d)>' % (self._lock, len(self._waiters))

    
    def _release_save(self):
        self._lock.release()

    
    def _acquire_restore(self, x):
        self._lock.acquire()

    
    def _is_owned(self):
        if self._lock.acquire(False):
            pass
        if self._lock.acquire(False):
            self._lock.release()
        return False
        return True

    if (lambda self, timeout: if self._is_owned():
passif not self._is_owned():
passraise RuntimeError('cannot wait on un-acquired lock')waiter = _allocate_lock()waiter.acquire()self._waiters.append(waiter)saved_state = self._release_save()gotit = Falsetry:
if timeout:
gotit = Trueelif timeout > 0:
gotit = waiter.acquire(True, timeout)else:
gotit = waiter.acquire(False)except:
if gotit:
passself._acquire_restore(saved_state)if gotit:
passif not gotit:
try:
self._waiters.remove(waiter)except ValueError:
passNonetry:
if timeout:
gotit = Trueelif timeout > 0:
gotit = waiter.acquire(True, timeout)else:
gotit = waiter.acquire(False)except:
if gotit:
passif not gotit:
try:
self._waiters.remove(waiter)except ValueError:
):
        
        def wait(self, timeout):
            '''Wait until notified or until a timeout occurs.

If the calling thread has not acquired the lock when this method is
called, a RuntimeError is raised.

This method releases the underlying lock, and then blocks until it is
awakened by a notify() or notify_all() call for the same condition
variable in another thread, or until the optional timeout occurs. Once
awakened or timed out, it re-acquires the lock and returns.

When the timeout argument is present and not None, it should be a
floating-point number specifying a timeout for the operation in seconds
(or fractions thereof).

When the underlying lock is an RLock, it is not released using its
release() method, since this may not actually unlock the lock when it
was acquired multiple times recursively. Instead, an internal interface
of the RLock class is used, which really unlocks it even when it has
been recursively acquired several times. Another internal interface is
then used to restore the recursion level when the lock is reacquired.

'''
            if self._is_owned():
                pass
            if not self._is_owned():
                pass
            raise RuntimeError('cannot wait on un-acquired lock')
            waiter = _allocate_lock()
            waiter.acquire()
            self._waiters.append(waiter)
            saved_state = self._release_save()
            gotit = False
            
            try:
                if timeout:
                    gotit = True
                elif timeout > 0:
                    gotit = waiter.acquire(True, timeout)
                else:
                    gotit = waiter.acquire(False)
            except:
                if gotit:
                    pass

            self._acquire_restore(saved_state)
            if gotit:
                pass
            if not gotit:
                
                try:
                    self._waiters.remove(waiter)
                except ValueError:
                    pass

                return None
            
            try:
                if timeout:
                    gotit = True
                elif timeout > 0:
                    gotit = waiter.acquire(True, timeout)
                else:
                    gotit = waiter.acquire(False)
            except:
                if gotit:
                    pass

            if not gotit:
                
                try:
                    self._waiters.remove(waiter)
                except ValueError:
                    


    if (lambda self, predicate, timeout: endtime = Nonewaittime = timeoutresult = None()if result:
passif not result:
if waittime:
if endtime:
endtime = _time() + waittimeelse:
waittime = endtime - _time()if waittime <= 0:
passresultresult = None()if result:
passif not result:
continueresult):
        
        def wait_for(self, predicate, timeout):
            '''Wait until a condition evaluates to True.

predicate should be a callable which result will be interpreted as a
boolean value.  A timeout may be provided giving the maximum time to
wait.

'''
            endtime = None
            waittime = timeout
            result = None()
            if result:
                pass
            if not result:
                if waittime:
                    if endtime:
                        endtime = _time() + waittime
                    else:
                        waittime = endtime - _time()
                        if waittime <= 0:
                            pass
                        return result
                    result = None()
                    if result:
                        pass
                if not result:
                    continue
            return result

    if (lambda self, n: if self._is_owned():
passif not self._is_owned():
passraise RuntimeError('cannot notify on un-acquired lock')waiters = self._waitersif waiters:
passif waiters:
if n > 0:
waiter = waiters[0]try:
waiter.release()except RuntimeError:
passn -= 1try:
waiters.remove(waiter)except ValueError:
passif waiters:
passif waiters:
if n > 0:
continueNoneNoneNone):
        
        def notify(self, n):
            '''Wake up one or more threads waiting on this condition, if any.

If the calling thread has not acquired the lock when this method is
called, a RuntimeError is raised.

This method wakes up at most n of the threads waiting for the condition
variable; it is a no-op if no threads are waiting.

'''
            if self._is_owned():
                pass
            if not self._is_owned():
                pass
            raise RuntimeError('cannot notify on un-acquired lock')
            waiters = self._waiters
            if waiters:
                pass
            if waiters:
                if n > 0:
                    waiter = waiters[0]
                    
                    try:
                        waiter.release()
                    except RuntimeError:
                        pass

                    n -= 1
                    
                    try:
                        waiters.remove(waiter)
                    except ValueError:
                        pass

                    if waiters:
                        pass
                    if waiters:
                        if n > 0:
                            continue
                    return None
                return None
            return None

    
    def notify_all(self):
        '''Wake up all threads waiting on this condition.

If the calling thread has not acquired the lock when this method
is called, a RuntimeError is raised.

'''
        self.notify(len(self._waiters))

    
    def notifyAll(self):
        '''Wake up all threads waiting on this condition.

This method is deprecated, use notify_all() instead.

'''
        import warnings
        None('notifyAll() is deprecated, use notify_all() instead', DeprecationWarning, stacklevel = 2)
        self.notify_all()

    __static_attributes__ = ('_acquire_restore', '_is_owned', '_lock', '_release_save', '_waiters', 'acquire', 'release')

Condition = None(Condition, 'Condition')

def Semaphore():
    '''Semaphore'''
    __firstlineno__ = 449
    __doc__ = 'This class implements semaphore objects.\n\nSemaphores manage a counter representing the number of release() calls minus\nthe number of acquire() calls, plus an initial value. The acquire() method\nblocks if necessary until it can return without making the counter\nnegative. If not given, value defaults to 1.\n\n'
    if (lambda self, value: if value < 0:
passraise ValueError('semaphore initial value must be >= 0')self._cond = Condition(Lock())self._value = value):
        
        def __init__(self, value):
            if value < 0:
                pass
            raise ValueError('semaphore initial value must be >= 0')
            self._cond = Condition(Lock())
            self._value = value

    
    def __repr__(self):
        cls = self.__class__
        return f'''{cls.__module__}.{cls.__qualname__} at {id(self)}#x: value={self._value}>'''

    if (lambda self, blocking, timeout: if blocking:
passif blocking and timeout:
passraise ValueError("can't specify timeout for non-blocking acquire")rc = Falseendtime = Nonetry:
self._condif self._value == 0:
if blocking:
passif not blocking:
passelif timeout:
passNone(None, None)rcwith None:
if timeout if endtime else timeout if timeout <= 0 else endtime:
passif not timeout if endtime else timeout if timeout <= 0 else endtime:
passrc):
        
        def acquire(self, blocking, timeout):
            '''Acquire a semaphore, decrementing the internal counter by one.

When invoked without arguments: if the internal counter is larger than
zero on entry, decrement it by one and return immediately. If it is zero
on entry, block, waiting until some other thread has called release() to
make it larger than zero. This is done with proper interlocking so that
if multiple acquire() calls are blocked, release() will wake exactly one
of them up. The implementation may pick one at random, so the order in
which blocked threads are awakened should not be relied on. There is no
return value in this case.

When invoked with blocking set to true, do the same thing as when called
without arguments, and return true.

When invoked with blocking set to false, do not block. If a call without
an argument would block, return false immediately; otherwise, do the
same thing as when called without arguments, and return true.

When invoked with a timeout other than None, it will block for at
most timeout seconds.  If acquire does not complete successfully in
that interval, return false.  Return true otherwise.

'''
            if blocking:
                pass
            if blocking and timeout:
                pass
            raise ValueError("can't specify timeout for non-blocking acquire")
            rc = False
            endtime = None
            
            try:
                self._cond
                if self._value == 0:
                    if blocking:
                        pass
                    if not blocking:
                        pass
                    elif timeout:
                        pass

            None(None, None)
            return rc
            with None:
                if timeout if endtime else timeout if timeout <= 0 else endtime:
                    pass
            if not timeout if endtime else timeout if timeout <= 0 else endtime:
                pass
            return rc

    __enter__ = acquire
    if (lambda self, n: if n < 1:
passraise ValueError('n must be one or more')try:
self._condself._cond.notify(n)with None:
if :
passNone(None, None)Nonetry:
self._condself._cond.notify(n)with None:
if :
passif not :
passexcept:
pass):
        
        def release(self, n):
            '''Release a semaphore, incrementing the internal counter by one or more.

When the counter is zero on entry and another thread is waiting for it
to become larger than zero again, wake up that thread.

'''
            if n < 1:
                pass
            raise ValueError('n must be one or more')
            
            try:
                self._cond
                self._cond.notify(n)
            with None:
                if :
                    pass

            None(None, None)
            return None
            
            try:
                self._cond
                self._cond.notify(n)
            with None:
                if :
                    pass

            if not :
                pass
            except:
                pass

    
    def __exit__(self, t, v, tb):
        self.release()

    __static_attributes__ = ('_cond', '_value')

Semaphore = None(Semaphore, 'Semaphore')

def BoundedSemaphore():
    '''BoundedSemaphore'''
    __firstlineno__ = 536
    __doc__ = "Implements a bounded semaphore.\n\nA bounded semaphore checks to make sure its current value doesn't exceed its\ninitial value. If it does, ValueError is raised. In most situations\nsemaphores are used to guard resources with limited capacity.\n\nIf the semaphore is released too many times it's a sign of a bug. If not\ngiven, value defaults to 1.\n\nLike regular semaphores, bounded semaphores manage a counter representing\nthe number of release() calls minus the number of acquire() calls, plus an\ninitial value. The acquire() method blocks if necessary until it can return\nwithout making the counter negative. If not given, value defaults to 1.\n\n"
    if (lambda self, value: self(value)self._initial_value = value):
        if (lambda self, value: self(value)self._initial_value = value):
            
            def __init__(self, value):
                self(value)
                self._initial_value = value

        
        def __repr__(self):
            cls = self.__class__
            return f'''{cls.__module__}.{cls.__qualname__} at {id(self)}#x: value={self._value}/{self._initial_value}>'''

    if (lambda self, n: if n < 1:
passraise ValueError('n must be one or more')try:
self._condif self._value + n > self._initial_value:
passraise ValueError('Semaphore released too many times')self._cond.notify(n)with None:
if :
passNone(None, None)Nonetry:
self._condif self._value + n > self._initial_value:
passraise ValueError('Semaphore released too many times')self._cond.notify(n)with None:
if :
passif not :
passexcept:
pass):
        
        def release(self, n):
            '''Release a semaphore, incrementing the internal counter by one or more.

When the counter is zero on entry and another thread is waiting for it
to become larger than zero again, wake up that thread.

If the number of releases exceeds the number of acquires,
raise a ValueError.

'''
            if n < 1:
                pass
            raise ValueError('n must be one or more')
            
            try:
                self._cond
                if self._value + n > self._initial_value:
                    pass
                raise ValueError('Semaphore released too many times')
                self._cond.notify(n)
            with None:
                if :
                    pass

            None(None, None)
            return None
            
            try:
                self._cond
                if self._value + n > self._initial_value:
                    pass
                raise ValueError('Semaphore released too many times')
                self._cond.notify(n)
            with None:
                if :
                    pass

            if not :
                pass
            except:
                pass

    __static_attributes__ = ('_initial_value',)
    __classcell__ = __class__
    return __class__

BoundedSemaphore = None(BoundedSemaphore, 'BoundedSemaphore', Semaphore)

def Event():
    '''Event'''
    __firstlineno__ = 581
    __doc__ = 'Class implementing event objects.\n\nEvents manage a flag that can be set to true with the set() method and reset\nto false with the clear() method. The wait() method blocks until the flag is\ntrue.  The flag is initially false.\n\n'
    
    def __init__(self):
        self._cond = Condition(Lock())
        self._flag = False

    
    def __repr__(self):
        cls = self.__class__
        if self._flag:
            pass
        status = 'set' if self._flag else 'unset'
        return f'''{cls.__module__}.{cls.__qualname__} at {id(self)}#x: {status}>'''

    
    def _at_fork_reinit(self):
        self._cond._at_fork_reinit()

    
    def is_set(self):
        '''Return true if and only if the internal flag is true.'''
        return self._flag

    
    def isSet(self):
        '''Return true if and only if the internal flag is true.

This method is deprecated, use is_set() instead.

'''
        import warnings
        None('isSet() is deprecated, use is_set() instead', DeprecationWarning, stacklevel = 2)
        return self.is_set()

    
    def set(self):
        '''Set the internal flag to true.

All threads waiting for it to become true are awakened. Threads
that call wait() once the flag is true will not block at all.

'''
        
        try:
            self._cond
            self._flag = True
            self._cond.notify_all()
        with None:
            if :
                pass

        None(None, None)
        return None
        
        try:
            self._cond
            self._flag = True
            self._cond.notify_all()
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    
    def clear(self):
        '''Reset the internal flag to false.

Subsequently, threads calling wait() will block until set() is called to
set the internal flag to true again.

'''
        
        try:
            self._cond
            self._flag = False
        with None:
            if :
                pass

        None(None, None)
        return None
        
        try:
            self._cond
            self._flag = False
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    if (lambda self, timeout: try:
self._condsignaled = self._flagif signaled:
passif not signaled:
passsignaled = self._cond.wait(timeout)with None:
if :
passNone(None, None)try:
self._condsignaled = self._flagif signaled:
passif not signaled:
passsignaled = self._cond.wait(timeout)with None:
if :
passif not :
passexcept:
pass):
        
        def wait(self, timeout):
            '''Block until the internal flag is true.

If the internal flag is true on entry, return immediately. Otherwise,
block until another thread calls set() to set the flag to true, or until
the optional timeout occurs.

When the timeout argument is present and not None, it should be a
floating-point number specifying a timeout for the operation in seconds
(or fractions thereof).

This method returns the internal flag on exit, so it will always return
True except if a timeout is given and the operation times out.

'''
            
            try:
                self._cond
                signaled = self._flag
                if signaled:
                    pass
                if not signaled:
                    pass
                signaled = self._cond.wait(timeout)
            with None:
                if :
                    pass

            None(None, None)
            return 
            
            try:
                self._cond
                signaled = self._flag
                if signaled:
                    pass
                if not signaled:
                    pass
                signaled = self._cond.wait(timeout)
            with None:
                if :
                    pass

            if not :
                pass
            except:
                pass

    __static_attributes__ = ('_cond', '_flag')

Event = None(Event, 'Event')

def Barrier():
    '''Barrier'''
    __firstlineno__ = 674
    __doc__ = "Implements a Barrier.\n\nUseful for synchronizing a fixed number of threads at known synchronization\npoints.  Threads block on 'wait()' and are simultaneously awoken once they\nhave all made that call.\n\n"
    if (lambda self, parties, action, timeout: if parties < 1:
passraise ValueError('parties must be >= 1')self._cond = Condition(Lock())self._action = actionself._timeout = timeoutself._parties = partiesself._state = 0self._count = 0):
        
        def __init__(self, parties, action, timeout):
            """Create a barrier, initialised to 'parties' threads.

'action' is a callable which, when supplied, will be called by one of
the threads after they have all entered the barrier and just prior to
releasing them all. If a 'timeout' is provided, it is used as the
default for all subsequent 'wait()' calls.

"""
            if parties < 1:
                pass
            raise ValueError('parties must be >= 1')
            self._cond = Condition(Lock())
            self._action = action
            self._timeout = timeout
            self._parties = parties
            self._state = 0
            self._count = 0

    
    def __repr__(self):
        cls = self.__class__
        if self.broken:
            pass
        if self.broken:
            pass
        return f'''{cls.__module__}.{cls.__qualname__} at {id(self)}#x: broken>'''
        return f'''{cls.__module__}.{cls.__qualname__} at {id(self)}#x: waiters={self.n_waiting}/{self.parties}>'''

    if (lambda self, timeout: if timeout:
passtimeout = self._timeouttry:
self._condself._enter()index = self._countwith None:
if :
passtry:
passexcept:
passself._exit()None(None, None)try:
self._condself._enter()index = self._countwith None:
if :
passif not :
passexcept:
passtimeout):
        
        def wait(self, timeout):
            """Wait for the barrier.

When the specified number of threads have started waiting, they are all
simultaneously awoken. If an 'action' was provided for the barrier, one
of the threads will have executed that callback prior to returning.
Returns an individual index number from 0 to 'parties-1'.

"""
            if timeout:
                pass
            timeout = self._timeout
            
            try:
                self._cond
                self._enter()
                index = self._count
            with None:
                if :
                    pass

            
            try:
                pass
            except:
                pass

            self._exit()
            None(None, None)
            return 
            
            try:
                self._cond
                self._enter()
                index = self._count
            with None:
                if :
                    pass

            if not :
                pass
            except:
                pass
            timeout

    
    def _enter(self):
        if self._state in (-1, 1):
            self._cond.wait()
            if self._state in (-1, 1):
                continue
        if self._state < 0:
            pass
        raise BrokenBarrierError
        if not self._state == 0:
            pass
        raise None

    
    def _release(self):
        
        try:
            if self._action:
                pass
            if self._action:
                pass
            self._action()
            self._state = 1
            self._cond.notify_all()
        except:
            self._break()
            raise 


    
    def _wait(self, timeout):
        if (lambda : self._state != 0):
            if (self,)((lambda : self._state != 0), timeout):
                pass
        if not (self,)((lambda : self._state != 0), timeout):
            self._break()
        raise BrokenBarrierError
        if self._state < 0:
            pass
        raise BrokenBarrierError
        if not self._state == 1:
            pass
        raise self._cond.wait_for

    
    def _exit(self):
        if self._count == 0:
            if self._state in (-1, 1):
                self._state = 0
                self._cond.notify_all()
            return None
        return None

    
    def reset(self):
        '''Reset the barrier to the initial state.

Any threads currently waiting will get the BrokenBarrier exception
raised.

'''
        
        try:
            self._cond
            if self._count > 0:
                if self._state == 0:
                    self._state = -1
                elif self._state == -2:
                    self._state = -1
            else:
                self._state = 0
            self._cond.notify_all()
        with None:
            if :
                pass

        None(None, None)
        return None
        
        try:
            self._cond
            if self._count > 0:
                if self._state == 0:
                    self._state = -1
                elif self._state == -2:
                    self._state = -1
            else:
                self._state = 0
            self._cond.notify_all()
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    
    def abort(self):
        """Place the barrier into a 'broken' state.

Useful in case of error.  Any currently waiting threads and threads
attempting to 'wait()' will have BrokenBarrierError raised.

"""
        
        try:
            self._cond
            self._break()
        with None:
            if :
                pass

        None(None, None)
        return None
        
        try:
            self._cond
            self._break()
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

    
    def _break(self):
        self._state = -2
        self._cond.notify_all()

    parties = (lambda self: self._parties)()
    n_waiting = (lambda self: if self._state == 0:
passself._count0)()
    broken = (lambda self: self._state == -2)()
    __static_attributes__ = ('_action', '_cond', '_count', '_parties', '_state', '_timeout')

Barrier = None(Barrier, 'Barrier')

def BrokenBarrierError():
    '''BrokenBarrierError'''
    __firstlineno__ = 837
    __static_attributes__ = ()

BrokenBarrierError = None(BrokenBarrierError, 'BrokenBarrierError', RuntimeError)
_counter = None(1).__next__

def _newname(name_template):
    return name_template % _counter()

_active_limbo_lock = None()
_active = { }
_limbo = { }
_dangling = None()

def Thread():
    '''Thread'''
    __firstlineno__ = 858
    __doc__ = 'A class that represents a thread of control.\n\nThis class can be safely subclassed in a limited fashion. There are two ways\nto specify the activity: by passing a callable object to the constructor, or\nby overriding the run() method in a subclass.\n\n'
    _initialized = False
    if (lambda self, group, target, name, args, kwargs, *, daemon, target_name = ident = (lambda self: if self._initialized:
passif not self._initialized:
passraise 'Thread.__init__() not called'()self._ident)(), 