# Source Generated with Decompyle++
# File: metadata.marshal (Python 3.13)

from __future__ import annotations
import os
import re
import abc
import sys
import json
import email
import types
import inspect
import pathlib
import zipfile
import operator
import textwrap
import warnings
import functools
import itertools
import posixpath
import collections
from  import _meta
from _collections import FreezableDefaultDict, Pair
from _functools import method_cache, pass_none
from _itertools import always_iterable, unique_everseen
from _meta import PackageMetadata, SimplePath
from contextlib import suppress
from importlib import import_module
from importlib.abc import MetaPathFinder
from itertools import starmap
from typing import Any, Iterable, List, Mapping, Match, Optional, Set, cast
__all__ = [
    'Distribution',
    'DistributionFinder',
    'PackageMetadata',
    'PackageNotFoundError',
    'distribution',
    'distributions',
    'entry_points',
    'files',
    'metadata',
    'packages_distributions',
    'requires',
    'version']

def PackageNotFoundError():
    '''PackageNotFoundError'''
    __firstlineno__ = 49
    __doc__ = 'The package was not found.'
    if (lambda self: f'''No package metadata was found for {self.name}'''):
        
        def __str__(self):
            return f'''No package metadata was found for {self.name}'''

    if (lambda self: (name,) = self.argsname):
        pass
    name = (lambda self: (name,) = self.argsname)()
    __static_attributes__ = ()

PackageNotFoundError = None(PackageNotFoundError, 'PackageNotFoundError', ModuleNotFoundError)

def Sectioned():
    '''Sectioned'''
    __firstlineno__ = 61
    __doc__ = "\nA simple entry point config parser for performance\n\n>>> for item in Sectioned.read(Sectioned._sample):\n...     print(item)\nPair(name='sec1', value='# comments ignored')\nPair(name='sec1', value='a = 1')\nPair(name='sec1', value='b = 2')\nPair(name='sec2', value='a = 2')\n\n>>> res = Sectioned.section_pairs(Sectioned._sample)\n>>> item = next(res)\n>>> item.name\n'sec1'\n>>> item.value\nPair(name='a', value='1')\n>>> item = next(res)\n>>> item.value\nPair(name='b', value='2')\n>>> item = next(res)\n>>> item.name\n'sec2'\n>>> item.value\nPair(name='a', value='2')\n>>> list(res)\n[]\n"
    _sample = None('\n        [sec1]\n        # comments ignored\n        a = 1\n        b = 2\n\n        [sec2]\n        a = 2\n        ').lstrip()
    section_pairs = (lambda cls, text: cls.read(text, filter_ = cls.valid)())()
    if (lambda text, filter_: if None:
passlines = filter(filter_, map(str.strip, text.splitlines()))name = Nonefor value in lines:
if value.startswith('['):
passif value.startswith('['):
value.startswith('[')section_match = value.endswith(']')if section_match:
passif section_match:
name = value.strip('[]')continueif Pair(name, value):
passPair(name, value)):
        pass
    read = (lambda text, filter_: if None:
passlines = filter(filter_, map(str.strip, text.splitlines()))name = Nonefor value in lines:
if value.startswith('['):
passif value.startswith('['):
value.startswith('[')section_match = value.endswith(']')if section_match:
passif section_match:
name = value.strip('[]')continueif Pair(name, value):
passPair(name, value))()
    if (lambda line: if line:
passif line:
lineif line.startswith('#'):
passnot line.startswith('#')):
        pass
    valid = (lambda line: if line:
passif line:
lineif line.startswith('#'):
passnot line.startswith('#'))()
    __static_attributes__ = ()

Sectioned = None(Sectioned, 'Sectioned')

def EntryPoint():
    '''EntryPoint'''
    __firstlineno__ = 126
    __doc__ = "An entry point as defined by Python packaging conventions.\n\nSee `the packaging docs on entry points\n<https://packaging.python.org/specifications/entry-points/>`_\nfor more information.\n\n>>> ep = EntryPoint(\n...     name=None, group=None, value='package.module:attr [extra1, extra2]')\n>>> ep.module\n'package.module'\n>>> ep.attr\n'attr'\n>>> ep.extras\n['extra1', 'extra2']\n"
    group: 'str' = None('(?P<module>[\\w.]+)\\s*(:\\s*(?P<attr>[\\w.]+)\\s*)?((?P<extras>\\[.*\\])\\s*)?$')
    dist: 'Optional[Distribution]' = None
    if (lambda self, name, value, group: vars(self).update(name = name, value = value, group = group)):
        
        def __init__(self, name, value, group):
            vars(self).update(name = name, value = value, group = group)

    if (lambda self: match = cast(Match, self.pattern.match(self.value))module = import_module(match.group('module'))if match.group('attr'):
passif not match.group('attr'):
match.group('attr')attrs = filter(None, ''.split('.'))None(getattr, attrs, module)):
        
        def load(self):
            '''Load the entry point from its definition. If only a module
is indicated by the value, return that module. Otherwise,
return the named object.
'''
            match = cast(Match, self.pattern.match(self.value))
            module = import_module(match.group('module'))
            if match.group('attr'):
                pass
            if not match.group('attr'):
                match.group('attr')
            attrs = filter(None, ''.split('.'))
            return None(getattr, attrs, module)

    if (lambda self: match = self.pattern.match(self.value)if match:
passraise matchmatch.group('module')):
        pass
    module = (lambda self: match = self.pattern.match(self.value)if match:
passraise matchmatch.group('module'))()
    if (lambda self: match = self.pattern.match(self.value)if match:
passraise matchmatch.group('attr')):
        pass
    attr = (lambda self: match = self.pattern.match(self.value)if match:
passraise matchmatch.group('attr'))()
    if (lambda self: match = self.pattern.match(self.value)if match:
passraise matchif match.group('extras'):
passif not match.group('extras'):
match.group('extras')None('\\w+', '')):
        pass
    extras = (lambda self: match = self.pattern.match(self.value)if match:
passraise matchif match.group('extras'):
passif not match.group('extras'):
match.group('extras')None('\\w+', ''))()
    
    def _for(self, dist):
        vars(self).update(dist = dist)
        return self

    
    def matches(self, **params):
        """
EntryPoint matches the given parameters.

>>> ep = EntryPoint(group='foo', name='bar', value='bing:bong [extra1, extra2]')
>>> ep.matches(group='foo')
True
>>> ep.matches(name='bar', value='bing:bong [extra1, extra2]')
True
>>> ep.matches(group='foo', name='other')
False
>>> ep.matches()
True
>>> ep.matches(extras=['extra1', 'extra2'])
True
>>> ep.matches(module='bing')
True
>>> ep.matches(attr='bong')
True
"""
        if (lambda .0: if None:
passfor param in .0:
if getattr(self, param):
passgetattr(self, param)):
            attrs = params()
        return all(map(operator.eq, params.values(), attrs))

    
    def _key(self):
        return (self.name, self.value, self.group)

    
    def __lt__(self, other):
        return self._key() < other._key()

    
    def __eq__(self, other):
        return self._key() == other._key()

    
    def __setattr__(self, name, value):
        raise AttributeError('EntryPoint objects are immutable.')

    
    def __repr__(self):
        return f'''EntryPoint(name={self.name}, value={self.value}, group={self.group})'''

    if (lambda self: hash(self._key())):
        
        def __hash__(self):
            return hash(self._key())

        __static_attributes__ = ()
        return None

EntryPoint = None(EntryPoint, 'EntryPoint')

def EntryPoints():
    '''EntryPoints'''
    __firstlineno__ = 250
    __doc__ = '\nAn immutable collection of selectable EntryPoint objects.\n'
    __slots__ = ()
    if (lambda self, name: try:
passexcept StopIteration:
raise KeyError(name)):
        
        def __getitem__(self, name):
            '''
Get the EntryPoint in self matching name.
'''
            
            try:
                pass
            except StopIteration:
                raise KeyError(name)


        
        def __repr__(self):
            '''
Repr with classname and tuple constructor to
signal that we deviate from regular tuple behavior.
'''
            return f'''{self.__class__.__name__}({tuple(self)})'''

    if (lambda self: if (lambda .0: if None:
passfor None in .0:
if None and ()({ }, params = None):
passif not ()({ }, params = None):
continueif ep:
passNone.matches):
            pass
        return (lambda .0: if None:
passfor None in .0:
if None and ()({ }, params = None):
passif not ()({ }, params = None):
continueif ep:
passNone.matches)(self())
):
        
        def select(self, **params):
            '''
Select entry points from self that match the
given parameters (typically group and/or name).
'''
            if (lambda .0: if None:
passfor None in .0:
if None and ()({ }, params = None):
passif not ()({ }, params = None):
continueif ep:
passNone.matches):
                pass
            return (lambda .0: if None:
passfor None in .0:
if None and ()({ }, params = None):
passif not ()({ }, params = None):
continueif ep:
passNone.matches)(self())

    if (lambda self: for None in :
if None:
if None.name:
continueep,):
        pass
    names = (lambda self: for None in :
if None:
if None.name:
continueep,)()
    if (lambda self: for None in :
if None:
if None.group:
continueep,):
        pass
    groups = (lambda self: for None in :
if None:
if None.group:
continueep,)()
    _from_text_for = (lambda cls, text, dist: if (lambda .0: if None:
passfor None in .0:
if None:
if None._for(dist):
pass):
            pass
        return (lambda .0: if None:
passfor None in .0:
if None:
if None._for(dist):
pass)(cls._from_text(text)())
)()
    _from_text = (lambda text: if text:
passif not text:
textSectioned.section_pairs('')())()
    __static_attributes__ = ()

EntryPoints = None(EntryPoints, 'EntryPoints', tuple)

def PackagePath():
    '''PackagePath'''
    __firstlineno__ = 306
    dist: 'Distribution' = 'A reference to a path in a package'
    if (lambda self, encoding: self.locate().read_text(encoding = encoding)):
        if (lambda self, encoding: self.locate().read_text(encoding = encoding)):
            
            def read_text(self, encoding):
                return self.locate().read_text(encoding = encoding)

    if (lambda self: self.locate().read_bytes()):
        
        def read_binary(self):
            return self.locate().read_bytes()

    if (lambda self: self.dist.locate_file(self)):
        
        def locate(self):
            '''Return a path-like object for this path'''
            return self.dist.locate_file(self)

        __static_attributes__ = ()
        return None

PackagePath = None(PackagePath, 'PackagePath', pathlib.PurePosixPath)

def FileHash():
    '''FileHash'''
    __firstlineno__ = 324
    if (lambda self, spec: if (self.mode,):
None):
        
        def __init__(self, spec):
            if (self.mode,):
                return None

    if (lambda self: f'''<FileHash mode: {self.mode} value: {self.value}>'''):
        
        def __repr__(self):
            return f'''<FileHash mode: {self.mode} value: {self.value}>'''

        __static_attributes__ = ('mode', 'value')
        return None

FileHash = None(FileHash, 'FileHash')

def DeprecatedNonAbstract():
