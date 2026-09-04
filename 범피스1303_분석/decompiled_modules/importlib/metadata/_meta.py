# Source Generated with Decompyle++
# File: _meta.marshal (Python 3.13)

from __future__ import annotations
import os
from typing import Protocol
from typing import Any, Dict, Iterator, List, Optional, TypeVar, Union, overload
_T = None('_T')

def PackageMetadata():
    '''PackageMetadata'''
    __firstlineno__ = 11
    if (lambda self: pass):
        
        def __len__(self):
            pass

    if (lambda self, item: pass):
        
        def __contains__(self, item):
            pass

    if (lambda self, key: pass):
        
        def __getitem__(self, key):
            pass

    if (lambda self: pass):
        
        def __iter__(self):
            pass

    if (lambda self, name, failobj: pass):
        if (lambda self, name, failobj: pass):
            pass
    get = (lambda self, name, failobj: pass)()
    if (lambda self, name, failobj: pass):
        pass
    get = (lambda self, name, failobj: pass)()
    if (lambda self, name, failobj: pass):
        if (lambda self, name, failobj: pass):
            pass
    get_all = (lambda self, name, failobj: pass)()
    if (lambda self, name, failobj: pass):
        pass
    get_all = (lambda self, name, failobj: pass)()
    if (lambda self: pass):
        pass
    json = (lambda self: pass)()
    __static_attributes__ = ()

PackageMetadata = None(PackageMetadata, 'PackageMetadata', Protocol)

def SimplePath():
    '''SimplePath'''
    __firstlineno__ = 47
    __doc__ = '\nA minimal subset of pathlib.Path required by Distribution.\n'
    if (lambda self, other: pass):
        
        def joinpath(self, other):
            pass

    if (lambda self, other: pass):
        
        def __truediv__(self, other):
            pass

    if (lambda self: pass):
        pass
    parent = (lambda self: pass)()
    if (lambda self, encoding: pass):
        if (lambda self, encoding: pass):
            
            def read_text(self, encoding):
                pass

    if (lambda self: pass):
        
        def read_bytes(self):
            pass

    if (lambda self: pass):
        
        def exists(self):
            pass

        __static_attributes__ = ()
        return None

SimplePath = None(SimplePath, 'SimplePath', Protocol)
