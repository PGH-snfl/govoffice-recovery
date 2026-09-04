# Source Generated with Decompyle++
# File: _path.marshal (Python 3.13)

'''
A Path-like interface for zipfiles.

This codebase is shared between zipfile.Path in the stdlib
and zipp in PyPI. See
https://github.com/python/importlib_metadata/wiki/Development-Methodology
for more detail.
'''
import contextlib
import io
import itertools
import pathlib
import posixpath
import re
import stat
import sys
import zipfile
from glob import Translator
__all__ = [
    'Path']

def _parents(path):
    """
Given a path with elements separated by
posixpath.sep, generate all parents of that path.

>>> list(_parents('b/d'))
['b']
>>> list(_parents('/b/d/'))
['/b']
>>> list(_parents('b/d/f/'))
['b/d', 'b']
>>> list(_parents('b'))
[]
>>> list(_parents(''))
[]
"""
    return None(_ancestry(path), 1, None)


def _ancestry(path):
    """
Given a path with elements separated by
posixpath.sep, generate all elements of that path.

>>> list(_ancestry('b/d'))
['b/d', 'b']
>>> list(_ancestry('/b/d/'))
['/b/d', '/b']
>>> list(_ancestry('b/d/f/'))
['b/d/f', 'b/d', 'b']
>>> list(_ancestry('b'))
['b']
>>> list(_ancestry(''))
[]

Multiple separators are treated like a single.

>>> list(_ancestry('//b//d///f//'))
['//b//d///f', '//b//d', '//b']
"""
    if None:
        pass
    path = path.rstrip(posixpath.sep)
    if path.rstrip(posixpath.sep):
        pass
    if path.rstrip(posixpath.sep):
        if path:
            pass
        path
        if ():
            pass
        if path.rstrip(posixpath.sep):
            pass
        if path.rstrip(posixpath.sep):
            continue
    return None

_dedupe = dict.fromkeys

def _difference(minuend, subtrahend):
    '''
Return items in minuend not in subtrahend, retaining order
with O(1) lookup.
'''
    return None(set(subtrahend).__contains__, minuend)


def InitializedState():
