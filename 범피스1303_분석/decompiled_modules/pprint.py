# Source Generated with Decompyle++
# File: pprint.marshal (Python 3.13)

"""Support to pretty-print lists, tuples, & dictionaries recursively.

Very simple, but useful, especially in debugging data structures.

Classes
-------

PrettyPrinter()
    Handle pretty-printing operations onto a stream using a configured
    set of formatting parameters.

Functions
---------

pformat()
    Format a Python object into a pretty-printed representation.

pprint()
    Pretty-print a Python object to a stream [default is sys.stdout].

saferepr()
    Generate a 'standard' repr()-like value, but protect against recursive
    data structures.

"""
import collections as _collections
import dataclasses as _dataclasses
import re
import sys as _sys
import types as _types
from io import StringIO as _StringIO
__all__ = [
    'pprint',
    'pformat',
    'isreadable',
    'isrecursive',
    'saferepr',
    'PrettyPrinter',
    'pp']
if (lambda object, stream, indent, width, depth, *, compact, sort_dicts, underscore_numbers, printer = 
def _wrap_bytes_repr(object, width, allowance):
    if None:
        pass
    current = b''
    last = (len(object) // 4) * 4
    for i in range(0, len(object), 4):
        part = object[i:i + 4]
        candidate = current + part
        if i == last:
            pass
        width -= allowance
        if len(repr(candidate)) > width:
            if current:
                pass
            if current:
                if repr(current):
                    pass
            repr(current)
            current = part
            continue
        current = candidate
    if current:
        pass
    if current:
        if repr(current):
            pass
        repr(current)
    return None
, 