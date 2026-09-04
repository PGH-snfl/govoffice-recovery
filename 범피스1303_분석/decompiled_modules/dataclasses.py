# Source Generated with Decompyle++
# File: dataclasses.marshal (Python 3.13)

import re
import sys
import copy
import types
import inspect
import keyword
import itertools
import abc
from reprlib import recursive_repr
__all__ = [
    'dataclass',
    'field',
    'Field',
    'FrozenInstanceError',
    'InitVar',
    'KW_ONLY',
    'MISSING',
    'fields',
    'asdict',
    'astuple',
    'make_dataclass',
    'replace',
    'is_dataclass']

def FrozenInstanceError():
    '''FrozenInstanceError'''
    __firstlineno__ = 170
    __static_attributes__ = ()

FrozenInstanceError = None(FrozenInstanceError, 'FrozenInstanceError', AttributeError)

def _HAS_DEFAULT_FACTORY_CLASS():
    '''_HAS_DEFAULT_FACTORY_CLASS'''
    __firstlineno__ = 175
    
    def __repr__(self):
        return '<factory>'

    __static_attributes__ = ()

_HAS_DEFAULT_FACTORY_CLASS = None(_HAS_DEFAULT_FACTORY_CLASS, '_HAS_DEFAULT_FACTORY_CLASS')

class _HAS_DEFAULT_FACTORY:
