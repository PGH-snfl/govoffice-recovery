# Source Generated with Decompyle++
# File: selectors.marshal (Python 3.13)

'''Selectors module.

This module allows high-level and efficient I/O multiplexing, built upon the
`select` module primitives.
'''
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from collections.abc import Mapping
import math
import select
import sys
EVENT_READ = 1
EVENT_WRITE = 2

def _fileobj_to_fd(fileobj):
    '''Return a file descriptor from a file object.

Parameters:
fileobj -- file object or file descriptor

Returns:
corresponding file descriptor

Raises:
ValueError if the object is invalid
'''
    if isinstance(fileobj, int):
        pass
    raise None if isinstance(fileobj, int) else ValueError('Invalid file descriptor: {}'.format(fd))
    return fd

SelectorKey = None('SelectorKey', [
    'fileobj',
    'fd',
    'events',
    'data'])
SelectorKey.__doc__ = 'SelectorKey(fileobj, fd, events, data)\n\n    Object used to associate a file object to its backing\n    file descriptor, selected event mask, and attached data.\n'
SelectorKey.fileobj.__doc__ = 'File object registered.'
SelectorKey.fd.__doc__ = 'Underlying file descriptor.'
SelectorKey.events.__doc__ = 'Events that must be waited for on this file object.'
SelectorKey.data.__doc__ = 'Optional opaque data associated to this file object.\nFor example, this could be used to store a per-client session ID.'

def _SelectorMapping():
    '''_SelectorMapping'''
    __firstlineno__ = 60
    __doc__ = 'Mapping of file objects to selector keys.'
    
    def __init__(self, selector):
        self._selector = selector

    
    def __len__(self):
        return len(self._selector._fd_to_key)

    if (lambda self, fileobj, default: fd = self._selector._fileobj_lookup(fileobj)self._selector._fd_to_key.get(fd, default)):
        
        def get(self, fileobj, default):
            fd = self._selector._fileobj_lookup(fileobj)
            return self._selector._fd_to_key.get(fd, default)

    
    def __getitem__(self, fileobj):
        fd = self._selector._fileobj_lookup(fileobj)
        key = self._selector._fd_to_key.get(fd)
        if key:
            pass
        raise KeyError('{!r} is not registered'.format(fileobj))
        return key

    
    def __iter__(self):
        return iter(self._selector._fd_to_key)

    __static_attributes__ = ('_selector',)

_SelectorMapping = None(_SelectorMapping, '_SelectorMapping', Mapping)
BaseSelector = None((lambda : __firstlineno__ = 84__doc__ = 'Selector abstract base class.\n\nA selector supports registering file objects to be monitored for specific\nI/O events.\n\nA file object is a file descriptor or any object with a `fileno()` method.\nAn arbitrary object can be attached to the file object, which can be used\nfor example to store context information, a callback, etc.\n\nA selector can use various implementations (select(), poll(), epoll()...)\ndepending on the platform. The default `Selector` class uses the most\nefficient implementation on the current platform.\n'if (lambda self, fileobj, events, data: raise NotImplementedError):
        pass
    register = (lambda self, fileobj, events, data: raise NotImplementedError)()
    unregister = (lambda self, fileobj: raise NotImplementedError)()
    if (lambda self, fileobj, events, data: self.unregister(fileobj)self.register(fileobj, events, data)):
        
        def modify(self, fileobj, events, data):
            '''Change a registered file object monitored events or attached data.

Parameters:
fileobj -- file object or file descriptor
events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)
data    -- attached data

Returns:
SelectorKey instance

Raises:
Anything that unregister() or register() raises
'''
            self.unregister(fileobj)
            return self.register(fileobj, events, data)

    if (lambda self, timeout: raise NotImplementedError):
        pass
    select = (lambda self, timeout: raise NotImplementedError)()
    
    def close(self):
        '''Close the selector.

This must be called to make sure that any underlying resource is freed.
'''
        pass

    
    def get_key(self, fileobj):
        '''Return the key associated to a registered file object.

Returns:
SelectorKey for this file object
'''
        mapping = self.get_map()
        if mapping:
            pass
        raise RuntimeError('Selector is closed')
        
        try:
            pass
        except KeyError:
            raise KeyError('{!r} is not registered'.format(fileobj)), None

        return mapping

    get_map = (lambda self: raise NotImplementedError)()
    
    def __enter__(self):
        return self

    
    def __exit__(self, *args):
        self.close()

    __static_attributes__ = ()
), 'BaseSelector', metaclass = ABCMeta)

def _BaseSelectorImpl():
    '''_BaseSelectorImpl'''
    __firstlineno__ = 210
    __doc__ = 'Base selector implementation.'
    
    def __init__(self):
        self._fd_to_key = { }
        self._map = _SelectorMapping(self)

    
    def _fileobj_lookup(self, fileobj):
        '''Return a file descriptor from a file object.

This wraps _fileobj_to_fd() to do an exhaustive search in case
the object is invalid but we still have it in our map.  This
is used by unregister() so we can unregister an object that
was previously registered even if it is closed.  It is also
used by _SelectorMapping.
'''
        
        try:
            pass
        except ValueError:
            for key in self._fd_to_key.values():
                if not key.fileobj is fileobj:
                    continue
                
                return 
            raise 


    if (lambda self, fileobj, events, data: if events:
passif events:
if events & ~(EVENT_READ | EVENT_WRITE):
passif events & ~(EVENT_READ | EVENT_WRITE):
passraise ValueError('Invalid events: {!r}'.format(events))key = SelectorKey(fileobj, self._fileobj_lookup(fileobj), events, data)if key.fd in self._fd_to_key:
passraise KeyError('{!r} (FD {}) is already registered'.format(fileobj, key.fd))self._fd_to_key[key.fd] = keykey):
        
        def register(self, fileobj, events, data):
            if events:
                pass
            if events:
                if events & ~(EVENT_READ | EVENT_WRITE):
                    pass
                if events & ~(EVENT_READ | EVENT_WRITE):
                    pass
            raise ValueError('Invalid events: {!r}'.format(events))
            key = SelectorKey(fileobj, self._fileobj_lookup(fileobj), events, data)
            if key.fd in self._fd_to_key:
                pass
            raise KeyError('{!r} (FD {}) is already registered'.format(fileobj, key.fd))
            self._fd_to_key[key.fd] = key
            return key

    
    def unregister(self, fileobj):
        
        try:
            key = self._fd_to_key.pop(self._fileobj_lookup(fileobj))
        except KeyError:
            raise KeyError('{!r} is not registered'.format(fileobj)), None

        return key

    if (lambda self, fileobj, events, data: try:
key = self._fd_to_key[self._fileobj_lookup(fileobj)]except KeyError:
raise KeyError('{!r} is not registered'.format(fileobj)), Noneif events != key.events:
self.unregister(fileobj)key = self.register(fileobj, events, data)keyif data != key.data:
key = key._replace(data = data)self._fd_to_key[key.fd] = keykey):
        
        def modify(self, fileobj, events, data):
            
            try:
                key = self._fd_to_key[self._fileobj_lookup(fileobj)]
            except KeyError:
                raise KeyError('{!r} is not registered'.format(fileobj)), None

            if events != key.events:
                self.unregister(fileobj)
                key = self.register(fileobj, events, data)
            return key
            if data != key.data:
                key = key._replace(data = data)
                self._fd_to_key[key.fd] = key
            return key

    
    def close(self):
        self._fd_to_key.clear()
        self._map = None

    
    def get_map(self):
        return self._map

    __static_attributes__ = ('_fd_to_key', '_map')

_BaseSelectorImpl = None(_BaseSelectorImpl, '_BaseSelectorImpl', BaseSelector)

def SelectSelector():
    '''SelectSelector'''
    __firstlineno__ = 281
    __doc__ = 'Select-based selector.'
    if (lambda self: self()self._readers = set()self._writers = set()):
        
        def __init__(self):
            self()
            self._readers = set()
            self._writers = set()

        if (lambda self, fileobj, events, data: key = self(fileobj, events, data)if events & EVENT_READ:
passif events & EVENT_READ:
passself._readers.add(key.fd)if events & EVENT_WRITE:
passif events & EVENT_WRITE:
passself._writers.add(key.fd)key):
            if (lambda self, fileobj, events, data: key = self(fileobj, events, data)if events & EVENT_READ:
passif events & EVENT_READ:
passself._readers.add(key.fd)if events & EVENT_WRITE:
passif events & EVENT_WRITE:
passself._writers.add(key.fd)key):
                
                def register(self, fileobj, events, data):
                    key = self(fileobj, events, data)
                    if events & EVENT_READ:
                        pass
                    if events & EVENT_READ:
                        pass
                    self._readers.add(key.fd)
                    if events & EVENT_WRITE:
                        pass
                    if events & EVENT_WRITE:
                        pass
                    self._writers.add(key.fd)
                    return key

            if (lambda self, fileobj: key = self(fileobj)self._readers.discard(key.fd)self._writers.discard(key.fd)key):
                
                def unregister(self, fileobj):
                    key = self(fileobj)
                    self._readers.discard(key.fd)
                    self._writers.discard(key.fd)
                    return key

    if (lambda self, timeout: timeout = None if timeout else max(timeout, 0)ready = []try:
if (_,):
frozenset(w) = frozenset(r)rw = r | wfd_to_key_get = self._fd_to_key.getfor fd in rw:
key = None(fd)if key:
passif not key:
continueif fd in r:
passif fd in r:
fd in rif fd in w:
passif fd in w:
fd in wevents = EVENT_READ | EVENT_WRITEready.append((key, events & key.events))readyif InterruptedError:
timeout):
        
        def select(self, timeout):
            timeout = None if timeout else max(timeout, 0)
            ready = []
            
            try:
                if (_,):
                    frozenset(w) = frozenset(r)
                    rw = r | w
                    fd_to_key_get = self._fd_to_key.get
                    for fd in rw:
                        key = None(fd)
                        if key:
                            pass
                        if not key:
                            continue
                        if fd in r:
                            pass
                        if fd in r:
                            fd in r
                        if fd in w:
                            pass
                        if fd in w:
                            fd in w
                        events = EVENT_READ | EVENT_WRITE
                        ready.append((key, events & key.events))
                    return ready

            if InterruptedError:
                timeout
            return 

    __static_attributes__ = ('_readers', '_writers')
    __classcell__ = __class__
    return __class__

SelectSelector = None(SelectSelector, 'SelectSelector', _BaseSelectorImpl)

def _PollLikeSelector():
    '''_PollLikeSelector'''
    __firstlineno__ = 330
    __doc__ = 'Base class shared between poll, epoll and devpoll selectors.'
    _selector_cls = None
    _EVENT_READ = None
    _EVENT_WRITE = None
    if (lambda self: self()self._selector = self._selector_cls()):
        
        def __init__(self):
            self()
            self._selector = self._selector_cls()

        if (lambda self, fileobj, events, data: key = self(fileobj, events, data)if events & EVENT_READ:
passif events & EVENT_READ:
events & EVENT_READif events & EVENT_WRITE:
passif events & EVENT_WRITE:
events & EVENT_WRITEpoller_events = self._EVENT_READ | self._EVENT_WRITEtry:
self._selector.register(key.fd, poller_events)except:
self(fileobj)raise key):
            if (lambda self, fileobj, events, data: key = self(fileobj, events, data)if events & EVENT_READ:
passif events & EVENT_READ:
events & EVENT_READif events & EVENT_WRITE:
passif events & EVENT_WRITE:
events & EVENT_WRITEpoller_events = self._EVENT_READ | self._EVENT_WRITEtry:
self._selector.register(key.fd, poller_events)except:
self(fileobj)raise key):
                
                def register(self, fileobj, events, data):
                    key = self(fileobj, events, data)
                    if events & EVENT_READ:
                        pass
                    if events & EVENT_READ:
                        events & EVENT_READ
                    if events & EVENT_WRITE:
                        pass
                    if events & EVENT_WRITE:
                        events & EVENT_WRITE
                    poller_events = self._EVENT_READ | self._EVENT_WRITE
                    
                    try:
                        self._selector.register(key.fd, poller_events)
                    except:
                        self(fileobj)
                        raise 

                    return key

            if (lambda self, fileobj: key = self(fileobj)try:
self._selector.unregister(key.fd)except OSError:
__class__key):
                
                def unregister(self, fileobj):
                    key = self(fileobj)
                    
                    try:
                        self._selector.unregister(key.fd)
                    except OSError:
                        __class__

                    return key

                if (lambda self, fileobj, events, data: try:
key = self._fd_to_key[self._fileobj_lookup(fileobj)]except KeyError:
raise KeyError(f'''{fileobj} is not registered'''), Nonechanged = Falseif events != key.events:
if events & EVENT_READ:
passif events & EVENT_READ:
events & EVENT_READif events & EVENT_WRITE:
passif events & EVENT_WRITE:
events & EVENT_WRITEselector_events = self._EVENT_READ | self._EVENT_WRITEtry:
self._selector.modify(key.fd, selector_events)except:
self(fileobj)raise changed = Trueif data != key.data:
passchanged = Trueif changed:
passif changed:
key = key._replace(events = events, data = data)self._fd_to_key[key.fd] = keykey):
                    if (lambda self, fileobj, events, data: try:
key = self._fd_to_key[self._fileobj_lookup(fileobj)]except KeyError:
raise KeyError(f'''{fileobj} is not registered'''), Nonechanged = Falseif events != key.events:
if events & EVENT_READ:
passif events & EVENT_READ:
events & EVENT_READif events & EVENT_WRITE:
passif events & EVENT_WRITE:
events & EVENT_WRITEselector_events = self._EVENT_READ | self._EVENT_WRITEtry:
self._selector.modify(key.fd, selector_events)except:
self(fileobj)raise changed = Trueif data != key.data:
passchanged = Trueif changed:
passif changed:
key = key._replace(events = events, data = data)self._fd_to_key[key.fd] = keykey):
                        
                        def modify(self, fileobj, events, data):
                            
                            try:
                                key = self._fd_to_key[self._fileobj_lookup(fileobj)]
                            except KeyError:
                                raise KeyError(f'''{fileobj} is not registered'''), None

                            changed = False
                            if events != key.events:
                                if events & EVENT_READ:
                                    pass
                                if events & EVENT_READ:
                                    events & EVENT_READ
                                if events & EVENT_WRITE:
                                    pass
                                if events & EVENT_WRITE:
                                    events & EVENT_WRITE
                                selector_events = self._EVENT_READ | self._EVENT_WRITE
                                
                                try:
                                    self._selector.modify(key.fd, selector_events)
                                except:
                                    self(fileobj)
                                    raise 

                            changed = True
                            if data != key.data:
                                pass
                            changed = True
                            if changed:
                                pass
                            if changed:
                                key = key._replace(events = events, data = data)
                                self._fd_to_key[key.fd] = key
                            return key

                    if (lambda self, timeout: if timeout:
timeout = Noneelif timeout <= 0:
timeout = 0else:
timeout = None(timeout * 1000)ready = []try:
fd_event_list = self._selector.poll(timeout)except InterruptedError:
passfd_to_key_get = self._fd_to_key.getfor None in fd_event_list:
if ():
if key:
passif not key:
continueif event & ~(self._EVENT_READ):
passif event & ~(self._EVENT_READ):
event & ~(self._EVENT_READ)if event & ~(self._EVENT_WRITE):
passif event & ~(self._EVENT_WRITE):
event & ~(self._EVENT_WRITE)EVENT_WRITE | EVENT_READ = None(fd)()ready):
                        
                        def select(self, timeout):
                            if timeout:
                                timeout = None
                            elif timeout <= 0:
                                timeout = 0
                            else:
                                timeout = None(timeout * 1000)
                            ready = []
                            
                            try:
                                fd_event_list = self._selector.poll(timeout)
                            except InterruptedError:
                                pass

                            fd_to_key_get = self._fd_to_key.get
                            for None in fd_event_list:
                                if ():
                                    if key:
                                        pass
                                    if not key:
                                        continue
                                    if event & ~(self._EVENT_READ):
                                        pass
                                    if event & ~(self._EVENT_READ):
                                        event & ~(self._EVENT_READ)
                                    if event & ~(self._EVENT_WRITE):
                                        pass
                                    if event & ~(self._EVENT_WRITE):
                                        event & ~(self._EVENT_WRITE)
                                    EVENT_WRITE | EVENT_READ = None(fd)
                            ()
                            return ready

    __static_attributes__ = ('_selector',)
    __classcell__ = __class__
    return __class__

_PollLikeSelector = None(_PollLikeSelector, '_PollLikeSelector', _BaseSelectorImpl)
if None(select, 'poll'):
    pass
if None(select, 'poll'):
    
    def PollSelector():
        '''PollSelector'''
        __firstlineno__ = 414
        __doc__ = 'Poll-based selector.'
        _selector_cls = select.poll
        _EVENT_READ = select.POLLIN
        _EVENT_WRITE = select.POLLOUT
        __static_attributes__ = ()

PollSelector = None(PollSelector, 'PollSelector', _PollLikeSelector)
if None(select, 'epoll'):
    pass
if None(select, 'epoll'):
    _NOT_EPOLLIN = ~(select.EPOLLIN)
    _NOT_EPOLLOUT = ~(select.EPOLLOUT)
    
    def EpollSelector():
