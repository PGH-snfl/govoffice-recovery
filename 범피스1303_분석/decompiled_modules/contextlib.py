# Source Generated with Decompyle++
# File: contextlib.marshal (Python 3.13)

'''Utilities for with-statement contexts.  See PEP 343.'''
import abc
import os
import sys
import _collections_abc
from collections import deque
from functools import wraps
from types import MethodType, GenericAlias
__all__ = [
    'asynccontextmanager',
    'contextmanager',
    'closing',
    'nullcontext',
    'AbstractContextManager',
    'AbstractAsyncContextManager',
    'AsyncExitStack',
    'ContextDecorator',
    'ExitStack',
    'redirect_stdout',
    'redirect_stderr',
    'suppress',
    'aclosing',
    'chdir']

def AbstractContextManager():
    '''AbstractContextManager'''
    __firstlineno__ = 17
    __doc__ = 'An abstract base class for context managers.'
    __class_getitem__ = None(GenericAlias)
    __slots__ = ()
    
    def __enter__(self):
        '''Return `self` upon entering the runtime context.'''
        return self

    __exit__ = (lambda self, exc_type, exc_value, traceback: pass)()
    __subclasshook__ = (lambda cls, C: if cls is AbstractContextManager:
passNone(C, '__enter__', '__exit__')NotImplemented)()
    __static_attributes__ = ()

AbstractContextManager = None(AbstractContextManager, 'AbstractContextManager', abc.ABC)

def AbstractAsyncContextManager():
    '''AbstractAsyncContextManager'''
    __firstlineno__ = 41
    __doc__ = 'An abstract base class for asynchronous context managers.'
    __class_getitem__ = None(GenericAlias)
    __slots__ = ()
    
    async def __aenter__(self):
        '''Return `self` upon entering the runtime context.'''
        if None:
            pass
        return self

    __aexit__ = (lambda self, exc_type, exc_value, traceback: if None:
pass)()
    __subclasshook__ = (lambda cls, C: if cls is AbstractAsyncContextManager:
passNone(C, '__aenter__', '__aexit__')NotImplemented)()
    __static_attributes__ = ()

AbstractAsyncContextManager = None(AbstractAsyncContextManager, 'AbstractAsyncContextManager', abc.ABC)

def ContextDecorator():
    '''ContextDecorator'''
    __firstlineno__ = 66
    __doc__ = 'A base class or mixin that enables context managers to work as decorators.'
    
    def _recreate_cm(self):
        '''Return a recreated instance of self.

Allows an otherwise one-shot context manager like
_GeneratorContextManager to support use as
a decorator via implicit recreation.

This is a private interface just for _GeneratorContextManager.
See issue #11647 for details.
'''
        return self

    
    def __call__(self, func):
