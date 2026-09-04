# Source Generated with Decompyle++
# File: abc.marshal (Python 3.13)

import abc
import io
import itertools
import os
import pathlib
from typing import Any, BinaryIO, Iterable, Iterator, NoReturn, Text, Optional
from typing import runtime_checkable, Protocol
from typing import Union
StrPath = Union[(str, os.PathLike[str])]
__all__ = [
    'ResourceReader',
    'Traversable',
    'TraversableResources']
ResourceReader = None((lambda : __firstlineno__ = 16__doc__ = 'Abstract base class for loaders to provide resource reading support.'if (lambda self, resource: raise FileNotFoundError):
        pass
    open_resource = (lambda self, resource: raise FileNotFoundError)()
    if (lambda self, resource: raise FileNotFoundError):
        pass
    resource_path = (lambda self, resource: raise FileNotFoundError)()
    if (lambda self, path: raise FileNotFoundError):
        pass
    is_resource = (lambda self, path: raise FileNotFoundError)()
    if (lambda self: raise FileNotFoundError):
        pass
    contents = (lambda self: raise FileNotFoundError)()
    __static_attributes__ = ()
), 'ResourceReader', metaclass = abc.ABCMeta)

def TraversalError():
    '''TraversalError'''
    __firstlineno__ = 58
    __static_attributes__ = ()

TraversalError = None(TraversalError, 'TraversalError', Exception)

def Traversable():
    '''Traversable'''
    __firstlineno__ = 62
    __doc__ = '\nAn object with a subset of pathlib.Path methods suitable for\ntraversing directories and opening files.\n\nAny exceptions that occur when accessing the backing resource\nmay propagate unaltered.\n'
    if (lambda self: pass):
        pass
    iterdir = (lambda self: pass)()
    if (lambda self: try:
strm = self.open('rb')with None:
if :
passNone(None, None)try:
strm = self.open('rb')with None:
if :
passif not :
passexcept:
pass):
        
        def read_bytes(self):
            '''
Read contents of self as bytes
'''
            
            try:
                strm = self.open('rb')
            with None:
                if :
                    pass

            None(None, None)
            return 
            
            try:
                strm = self.open('rb')
            with None:
                if :
                    pass

            if not :
                pass
            except:
                pass

    if (lambda self, encoding: try:
strm = self.open(encoding = encoding)with None:
if :
passNone(None, None)try:
strm = self.open(encoding = encoding)with None:
if :
passif not :
passexcept:
pass):
        if (lambda self, encoding: try:
strm = self.open(encoding = encoding)with None:
if :
passNone(None, None)try:
strm = self.open(encoding = encoding)with None:
if :
passif not :
passexcept:
pass):
            
            def read_text(self, encoding):
                '''
Read contents of self as text
'''
                
                try:
                    strm = self.open(encoding = encoding)
                with None:
                    if :
                        pass

                None(None, None)
                return 
                
                try:
                    strm = self.open(encoding = encoding)
                with None:
                    if :
                        pass

                if not :
                    pass
                except:
                    pass

    if (lambda self: pass):
        pass
    is_dir = (lambda self: pass)()
    if (lambda self: pass):
        pass
    is_file = (lambda self: pass)()
    if (lambda self: if descendants:
passif not descendants:
passselfnames = (lambda .0: if None:
passfor None in .0:
if None:
if None.parts:
passcontinue)(map(pathlib.PurePosixPath, descendants)())
        target = next(names)
        if (lambda .0: if None:
passfor None in .0:
if None:
if not None.name == target:
continueif traversable:
pass):
            pass
        matches = self.iterdir()()
        
        try:
            match = next(matches)
        except StopIteration:
            match.joinpath
            raise TraversalError('Target not found during traversal.', target, list(names))

        return None(names)
):
        
        def joinpath(self, *descendants):
            '''
Return Traversable resolved with any descendants applied.

Each descendant should be a path segment relative to self
and each may contain multiple levels separated by
``posixpath.sep`` (``/``).
'''
            if descendants:
                pass
            if not descendants:
                pass
            return self
            names = (lambda .0: if None:
passfor None in .0:
if None:
if None.parts:
passcontinue)(map(pathlib.PurePosixPath, descendants)())
            target = next(names)
            if (lambda .0: if None:
passfor None in .0:
if None:
if not None.name == target:
continueif traversable:
pass):
                pass
            matches = self.iterdir()()
            
            try:
                match = next(matches)
            except StopIteration:
                match.joinpath
                raise TraversalError('Target not found during traversal.', target, list(names))

            return None(names)

    if (lambda self, child: self.joinpath(child)):
        
        def __truediv__(self, child):
            '''
Return Traversable child in self
'''
            return self.joinpath(child)

    if (lambda self, mode: pass):
        pass
    open = (lambda self, mode: pass)()
    if (lambda self: pass):
        pass
    name = (lambda self: pass)()()
    __static_attributes__ = ()

Traversable = None(Traversable, 'Traversable', Protocol)()

def TraversableResources():
    '''TraversableResources'''
    __firstlineno__ = 153
    __doc__ = '\nThe required interface for providing traversable\nresources.\n'
    if (lambda self: pass):
        pass
    files = (lambda self: pass)()
    if (lambda self, resource: self.files().joinpath(resource).open('rb')):
        
        def open_resource(self, resource):
            return self.files().joinpath(resource).open('rb')

    if (lambda self, resource: raise FileNotFoundError(resource)):
        
        def resource_path(self, resource):
            raise FileNotFoundError(resource)

    if (lambda self, path: self.files().joinpath(path).is_file()):
        
        def is_resource(self, path):
            return self.files().joinpath(path).is_file()

    if (lambda self: self.files().iterdir()()):
        
        def contents(self):
            return self.files().iterdir()()

        __static_attributes__ = ()
        return None

TraversableResources = None(TraversableResources, 'TraversableResources', ResourceReader)
