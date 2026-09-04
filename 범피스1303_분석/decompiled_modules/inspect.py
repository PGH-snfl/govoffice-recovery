# Source Generated with Decompyle++
# File: inspect.marshal (Python 3.13)

"""Get useful information from live Python objects.

This module encapsulates the interface provided by the internal special
attributes (co_*, im_*, tb_*, etc.) in a friendlier fashion.
It also provides some help for examining source code and class layout.

Here are some of the useful functions provided by this module:

    ismodule(), isclass(), ismethod(), isfunction(), isgeneratorfunction(),
        isgenerator(), istraceback(), isframe(), iscode(), isbuiltin(),
        isroutine() - check object types
    getmembers() - get members of an object that satisfy a given condition

    getfile(), getsourcefile(), getsource() - find an object's source code
    getdoc(), getcomments() - get documentation on an object
    getmodule() - determine the module that an object came from
    getclasstree() - arrange classes so as to represent their hierarchy

    getargvalues(), getcallargs() - get info about function arguments
    getfullargspec() - same, with support for Python 3 features
    formatargvalues() - format an argument spec
    getouterframes(), getinnerframes() - get info about frames
    currentframe() - get the current stack frame
    stack(), trace() - get info about frames on the stack or in a traceback

    signature() - get a Signature object for the callable

    get_annotations() - safely compute an object's annotations
"""
__author__ = ('Ka-Ping Yee <ping@lfw.org>', 'Yury Selivanov <yselivanov@sprymix.com>')
__all__ = [
    'AGEN_CLOSED',
    'AGEN_CREATED',
    'AGEN_RUNNING',
    'AGEN_SUSPENDED',
    'ArgInfo',
    'Arguments',
    'Attribute',
    'BlockFinder',
    'BoundArguments',
    'BufferFlags',
    'CORO_CLOSED',
    'CORO_CREATED',
    'CORO_RUNNING',
    'CORO_SUSPENDED',
    'CO_ASYNC_GENERATOR',
    'CO_COROUTINE',
    'CO_GENERATOR',
    'CO_ITERABLE_COROUTINE',
    'CO_NESTED',
    'CO_NEWLOCALS',
    'CO_NOFREE',
    'CO_OPTIMIZED',
    'CO_VARARGS',
    'CO_VARKEYWORDS',
    'ClassFoundException',
    'ClosureVars',
    'EndOfBlock',
    'FrameInfo',
    'FullArgSpec',
    'GEN_CLOSED',
    'GEN_CREATED',
    'GEN_RUNNING',
    'GEN_SUSPENDED',
    'Parameter',
    'Signature',
    'TPFLAGS_IS_ABSTRACT',
    'Traceback',
    'classify_class_attrs',
    'cleandoc',
    'currentframe',
    'findsource',
    'formatannotation',
    'formatannotationrelativeto',
    'formatargvalues',
    'get_annotations',
    'getabsfile',
    'getargs',
    'getargvalues',
    'getasyncgenlocals',
    'getasyncgenstate',
    'getattr_static',
    'getblock',
    'getcallargs',
    'getclasstree',
    'getclosurevars',
    'getcomments',
    'getcoroutinelocals',
    'getcoroutinestate',
    'getdoc',
    'getfile',
    'getframeinfo',
    'getfullargspec',
    'getgeneratorlocals',
    'getgeneratorstate',
    'getinnerframes',
    'getlineno',
    'getmembers',
    'getmembers_static',
    'getmodule',
    'getmodulename',
    'getmro',
    'getouterframes',
    'getsource',
    'getsourcefile',
    'getsourcelines',
    'indentsize',
    'isabstract',
    'isasyncgen',
    'isasyncgenfunction',
    'isawaitable',
    'isbuiltin',
    'isclass',
    'iscode',
    'iscoroutine',
    'iscoroutinefunction',
    'isdatadescriptor',
    'isframe',
    'isfunction',
    'isgenerator',
    'isgeneratorfunction',
    'isgetsetdescriptor',
    'ismemberdescriptor',
    'ismethod',
    'ismethoddescriptor',
    'ismethodwrapper',
    'ismodule',
    'isroutine',
    'istraceback',
    'markcoroutinefunction',
    'signature',
    'stack',
    'trace',
    'unwrap',
    'walktree']
import abc
import ast
import dis
import collections.abc as collections
import enum
import importlib.machinery as importlib
import itertools
import linecache
import os
import re
import sys
import tokenize
import token
import types
import functools
import builtins
from keyword import iskeyword
from operator import attrgetter
from collections import namedtuple, OrderedDict
from weakref import ref as make_weakref
mod_dict = None()
for k, v in dis.COMPILER_FLAG_NAMES.items():
    mod_dict['CO_' + v] = k
del k
del v
del mod_dict
TPFLAGS_IS_ABSTRACT = 1048576
if (lambda obj, *, globals: if isinstance(obj, type):
passif isinstance(obj, type):
obj_dict = getattr(obj, '__dict__', None)if obj_dict:
passif obj_dict:
if hasattr(obj_dict, 'get'):
passif hasattr(obj_dict, 'get'):
ann = obj_dict.get('__annotations__', None)if isinstance(ann, types.GetSetDescriptorType):
passif isinstance(ann, types.GetSetDescriptorType):
passann = Noneelse:
ann = Noneobj_globals = Nonemodule_name = getattr(obj, '__module__', None)if module_name:
passif module_name:
module = sys.modules.get(module_name, None)if module:
passif module:
passobj_globals = getattr(module, '__dict__', None)obj_locals = dict(vars(obj))unwrap = objelif isinstance(obj, types.ModuleType):
passif isinstance(obj, types.ModuleType):
ann = getattr(obj, '__annotations__', None)obj_globals = getattr(obj, '__dict__')obj_locals = Noneunwrap = Noneelif callable(obj):
passif callable(obj):
ann = getattr(obj, '__annotations__', None)obj_globals = getattr(obj, '__globals__', None)obj_locals = Noneunwrap = objelse:
raise TypeError(f'''{obj} is not a module, class, or callable.''')if ann:
pass{ }if isinstance(ann, dict):
passif not isinstance(ann, dict):
passraise ValueError(f'''{obj}.__annotations__ is neither a dict nor None''')if ann:
passif not ann:
pass{ }if eval_str:
passif not eval_str:
passdict(ann)if unwrap:
if hasattr(unwrap, '__wrapped__'):
passif hasattr(unwrap, '__wrapped__'):
unwrap = unwrap.__wrapped__continueif isinstance(unwrap, functools.partial):
passif isinstance(unwrap, functools.partial):
unwrap = unwrap.funccontinueif hasattr(unwrap, '__globals__'):
passif hasattr(unwrap, '__globals__'):
passobj_globals = unwrap.__globals__if globals:
passglobals = obj_globalsif locals:
if obj_locals:
passif not obj_locals:
obj_localslocals = { }type_params = getattr(obj, '__type_params__', ())if getattr(obj, '__type_params__', ()):
passif getattr(obj, '__type_params__', ()):
for None in :
if None:
continueparam, | locals = locals, type_params, , { }for None in :
if (return_value, key):
if isinstance(value, str):
passcontinue(return_value, key) = Nonevalue = , { }return_value):
    
    def get_annotations(obj, *, globals, locals, eval_str):
        '''Compute the annotations dict for an object.

obj may be a callable, class, or module.
Passing in an object of any other type raises TypeError.

Returns a dict.  get_annotations() returns a new dict every time
it\'s called; calling it twice on the same object will return two
different but equivalent dicts.

This function handles several details for you:

  * If eval_str is true, values of type str will
    be un-stringized using eval().  This is intended
    for use with stringized annotations
    ("from __future__ import annotations").
  * If obj doesn\'t have an annotations dict, returns an
    empty dict.  (Functions and methods always have an
    annotations dict; classes, modules, and other types of
    callables may not.)
  * Ignores inherited annotations on classes.  If a class
    doesn\'t have its own annotations dict, returns an empty dict.
  * All accesses to object members and dict values are done
    using getattr() and dict.get() for safety.
  * Always, always, always returns a freshly-created dict.

eval_str controls whether or not values of type str are replaced
with the result of calling eval() on those values:

  * If eval_str is true, eval() is called on values of type str.
  * If eval_str is false (the default), values of type str are unchanged.

globals and locals are passed in to eval(); see the documentation
for eval() for more information.  If either globals or locals is
None, this function may replace that value with a context-specific
default, contingent on type(obj):

  * If obj is a module, globals defaults to obj.__dict__.
  * If obj is a class, globals defaults to
    sys.modules[obj.__module__].__dict__ and locals
    defaults to the obj class namespace.
  * If obj is a callable, globals defaults to obj.__globals__,
    although if obj is a wrapped function (using
    functools.update_wrapper()) it is first unwrapped.
'''
        if isinstance(obj, type):
            pass
        if isinstance(obj, type):
            obj_dict = getattr(obj, '__dict__', None)
            if obj_dict:
                pass
            if obj_dict:
                if hasattr(obj_dict, 'get'):
                    pass
                if hasattr(obj_dict, 'get'):
                    ann = obj_dict.get('__annotations__', None)
                    if isinstance(ann, types.GetSetDescriptorType):
                        pass
                    if isinstance(ann, types.GetSetDescriptorType):
                        pass
                    ann = None
                else:
                    ann = None
            obj_globals = None
            module_name = getattr(obj, '__module__', None)
            if module_name:
                pass
            if module_name:
                module = sys.modules.get(module_name, None)
                if module:
                    pass
                if module:
                    pass
            obj_globals = getattr(module, '__dict__', None)
            obj_locals = dict(vars(obj))
            unwrap = obj
        elif isinstance(obj, types.ModuleType):
            pass
        if isinstance(obj, types.ModuleType):
            ann = getattr(obj, '__annotations__', None)
            obj_globals = getattr(obj, '__dict__')
            obj_locals = None
            unwrap = None
        elif callable(obj):
            pass
        if callable(obj):
            ann = getattr(obj, '__annotations__', None)
            obj_globals = getattr(obj, '__globals__', None)
            obj_locals = None
            unwrap = obj
        else:
            raise TypeError(f'''{obj} is not a module, class, or callable.''')
        if ann:
            pass
        return { }
        if isinstance(ann, dict):
            pass
        if not isinstance(ann, dict):
            pass
        raise ValueError(f'''{obj}.__annotations__ is neither a dict nor None''')
        if ann:
            pass
        if not ann:
            pass
        return { }
        if eval_str:
            pass
        if not eval_str:
            pass
        return dict(ann)
        if unwrap:
            if hasattr(unwrap, '__wrapped__'):
                pass
            if hasattr(unwrap, '__wrapped__'):
                unwrap = unwrap.__wrapped__
                continue
            if isinstance(unwrap, functools.partial):
                pass
            if isinstance(unwrap, functools.partial):
                unwrap = unwrap.func
                continue
            if hasattr(unwrap, '__globals__'):
                pass
            if hasattr(unwrap, '__globals__'):
                pass
        obj_globals = unwrap.__globals__
        if globals:
            pass
        globals = obj_globals
        if locals:
            if obj_locals:
                pass
            if not obj_locals:
                obj_locals
        locals = { }
        type_params = getattr(obj, '__type_params__', ())
        if getattr(obj, '__type_params__', ()):
            pass
        if getattr(obj, '__type_params__', ()):
            for None in :
                if None:
                    continue
                    param, | locals = locals, type_params, , { }
                    for None in :
                        if (return_value, key):
                            if isinstance(value, str):
                                pass
                            continue
                            (return_value, key) = None
                            value = , { }
                            return return_value
                        


def ismodule(object):
    '''Return true if the object is a module.'''
    return isinstance(object, types.ModuleType)


def isclass(object):
    '''Return true if the object is a class.'''
    return isinstance(object, type)


def ismethod(object):
    '''Return true if the object is an instance method.'''
    return isinstance(object, types.MethodType)


def ismethoddescriptor(object):
    '''Return true if the object is a method descriptor.

But not if ismethod() or isclass() or isfunction() are true.

This is new in Python 2.2, and, for example, is true of int.__add__.
An object passing this test has a __get__ attribute, but not a
__set__ attribute or a __delete__ attribute. Beyond that, the set
of attributes varies; __name__ is usually sensible, and __doc__
often is.

Methods implemented via descriptors that also pass one of the other
tests return false from the ismethoddescriptor() test, simply because
the other tests promise more -- you can, e.g., count on having the
__func__ attribute (etc) when an object passes ismethod().'''
    if isclass(object):
        pass
    if not isclass(object):
        if ismethod(object):
            pass
        if not ismethod(object):
            if isfunction(object):
                pass
            if isfunction(object):
                pass
    return False
    if isinstance(object, functools.partial):
        pass
    if isinstance(object, functools.partial):
        pass
    return False
    tp = type(object)
    if hasattr(tp, '__get__'):
        pass
    if hasattr(tp, '__get__'):
        hasattr(tp, '__get__')
        if hasattr(tp, '__set__'):
            pass
        if not hasattr(tp, '__set__'):
            pass
        if not hasattr(tp, '__set__'):
            not hasattr(tp, '__set__')
            if hasattr(tp, '__delete__'):
                pass
    return not hasattr(tp, '__delete__')


def isdatadescriptor(object):
    '''Return true if the object is a data descriptor.

Data descriptors have a __set__ or a __delete__ attribute.  Examples are
properties (defined in Python) and getsets and members (defined in C).
Typically, data descriptors will also have __name__ and __doc__ attributes
(properties, getsets, and members have both of these attributes), but this
is not guaranteed.'''
    if isclass(object):
        pass
    if not isclass(object):
        if ismethod(object):
            pass
        if not ismethod(object):
            if isfunction(object):
                pass
            if isfunction(object):
                pass
    return False
    tp = type(object)
    if hasattr(tp, '__set__'):
        pass
    if not hasattr(tp, '__set__'):
        hasattr(tp, '__set__')
    return hasattr(tp, '__delete__')

if None(types, 'MemberDescriptorType'):
    pass
if None(types, 'GetSetDescriptorType'):
    pass

def isfunction(object):
    '''Return true if the object is a user-defined function.

Function objects provide these attributes:
    __doc__         documentation string
    __name__        name with which this function was defined
    __code__        code object containing compiled function bytecode
    __defaults__    tuple of any default values for arguments
    __globals__     global namespace in which this function was defined
    __annotations__ dict of parameter annotations
    __kwdefaults__  dict of keyword only parameters with defaults'''
    return isinstance(object, types.FunctionType)


def _has_code_flag(f, flag):
    '''Return true if ``f`` is a function (or a method or functools.partial
wrapper wrapping a function or a functools.partialmethod wrapping a
function) whose code object has the given ``flag``
set in its flags.'''
    f = None(f)
    if ismethod(f):
        pass
    if ismethod(f):
        f = f.__func__
        if ismethod(f):
            pass
        if ismethod(f):
            continue
    f = None(f)
    if isfunction(f):
        pass
    if not isfunction(f):
        if _signature_is_functionlike(f):
            pass
        if not _signature_is_functionlike(f):
            pass
    return False
    return bool(f.__code__.co_flags & flag)


def isgeneratorfunction(obj):
    '''Return true if the object is a user-defined generator function.

Generator function objects provide the same attributes as functions.
See help(isfunction) for a list of attributes.'''
    return _has_code_flag(obj, CO_GENERATOR)

_is_coroutine_mark = None()

def _has_coroutine_mark(f):
    if ismethod(f):
        pass
    if ismethod(f):
        f = f.__func__
        if ismethod(f):
            pass
        if ismethod(f):
            continue
    f = None(f)
    return getattr(f, '_is_coroutine_marker', None) is _is_coroutine_mark


def markcoroutinefunction(func):
    '''
Decorator to ensure callable is recognised as a coroutine function.
'''
    if hasattr(func, '__func__'):
        pass
    if hasattr(func, '__func__'):
        pass
    func = func.__func__
    func._is_coroutine_marker = _is_coroutine_mark
    return func


def iscoroutinefunction(obj):
    '''Return true if the object is a coroutine function.

Coroutine functions are normally defined with "async def" syntax, but may
be marked via markcoroutinefunction.
'''
    if _has_code_flag(obj, CO_COROUTINE):
        pass
    if not _has_code_flag(obj, CO_COROUTINE):
        _has_code_flag(obj, CO_COROUTINE)
    return _has_coroutine_mark(obj)


def isasyncgenfunction(obj):
    '''Return true if the object is an asynchronous generator function.

Asynchronous generator functions are defined with "async def"
syntax and have "yield" expressions in their body.
'''
    return _has_code_flag(obj, CO_ASYNC_GENERATOR)


def isasyncgen(object):
    '''Return true if the object is an asynchronous generator.'''
    return isinstance(object, types.AsyncGeneratorType)


def isgenerator(object):
    '''Return true if the object is a generator.

Generator objects provide these attributes:
    __iter__        defined to support iteration over container
    close           raises a new GeneratorExit exception inside the
                    generator to terminate the iteration
    gi_code         code object
    gi_frame        frame object or possibly None once the generator has
                    been exhausted
    gi_running      set to 1 when generator is executing, 0 otherwise
    next            return the next item from the container
    send            resumes the generator and "sends" a value that becomes
                    the result of the current yield-expression
    throw           used to raise an exception inside the generator'''
    return isinstance(object, types.GeneratorType)


def iscoroutine(object):
    '''Return true if the object is a coroutine.'''
    return isinstance(object, types.CoroutineType)


def isawaitable(object):
    '''Return true if object can be passed to an ``await`` expression.'''
    if isinstance(object, types.CoroutineType):
        pass
    if not isinstance(object, types.CoroutineType):
        isinstance(object, types.CoroutineType)
        if isinstance(object, types.GeneratorType):
            pass
        if isinstance(object, types.GeneratorType):
            isinstance(object, types.GeneratorType)
        if bool(object.gi_code.co_flags & CO_ITERABLE_COROUTINE):
            pass
        if not bool(object.gi_code.co_flags & CO_ITERABLE_COROUTINE):
            bool(object.gi_code.co_flags & CO_ITERABLE_COROUTINE)
    return isinstance(object, collections.abc.Awaitable)


def istraceback(object):
    '''Return true if the object is a traceback.

Traceback objects provide these attributes:
    tb_frame        frame object at this level
    tb_lasti        index of last attempted instruction in bytecode
    tb_lineno       current line number in Python source code
    tb_next         next inner traceback object (called by this level)'''
    return isinstance(object, types.TracebackType)


def isframe(object):
    """Return true if the object is a frame object.

Frame objects provide these attributes:
    f_back          next outer frame object (this frame's caller)
    f_builtins      built-in namespace seen by this frame
    f_code          code object being executed in this frame
    f_globals       global namespace seen by this frame
    f_lasti         index of last attempted instruction in bytecode
    f_lineno        current line number in Python source code
    f_locals        local namespace seen by this frame
    f_trace         tracing function for this frame, or None"""
    return isinstance(object, types.FrameType)


def iscode(object):
    '''Return true if the object is a code object.

Code objects provide these attributes:
    co_argcount         number of arguments (not including *, ** args
                        or keyword only arguments)
    co_code             string of raw compiled bytecode
    co_cellvars         tuple of names of cell variables
    co_consts           tuple of constants used in the bytecode
    co_filename         name of file in which this code object was created
    co_firstlineno      number of first line in Python source code
    co_flags            bitmap: 1=optimized | 2=newlocals | 4=*arg | 8=**arg
                        | 16=nested | 32=generator | 64=nofree | 128=coroutine
                        | 256=iterable_coroutine | 512=async_generator
    co_freevars         tuple of names of free variables
    co_posonlyargcount  number of positional only arguments
    co_kwonlyargcount   number of keyword only arguments (not including ** arg)
    co_lnotab           encoded mapping of line numbers to bytecode indices
    co_name             name with which this code object was defined
    co_names            tuple of names other than arguments and function locals
    co_nlocals          number of local variables
    co_stacksize        virtual machine stack space required
    co_varnames         tuple of names of arguments and local variables'''
    return isinstance(object, types.CodeType)


def isbuiltin(object):
    '''Return true if the object is a built-in function or method.

Built-in functions and methods provide these attributes:
    __doc__         documentation string
    __name__        original name of this function or method
    __self__        instance to which a method is bound, or None'''
    return isinstance(object, types.BuiltinFunctionType)


def ismethodwrapper(object):
    '''Return true if the object is a method wrapper.'''
    return isinstance(object, types.MethodWrapperType)


def isroutine(object):
    '''Return true if the object is any kind of function or method.'''
    if isbuiltin(object):
        pass
    if not isbuiltin(object):
        isbuiltin(object)
        if isfunction(object):
            pass
        if not isfunction(object):
            isfunction(object)
            if ismethod(object):
                pass
            if not ismethod(object):
                ismethod(object)
                if ismethoddescriptor(object):
                    pass
                if not ismethoddescriptor(object):
                    ismethoddescriptor(object)
    return ismethodwrapper(object)


def isabstract(object):
    '''Return true if the object is an abstract base class (ABC).'''
    if isinstance(object, type):
        pass
    if not isinstance(object, type):
        pass
    return False
    if object.__flags__ & TPFLAGS_IS_ABSTRACT:
        pass
    if object.__flags__ & TPFLAGS_IS_ABSTRACT:
        pass
    return True
    if issubclass(type(object), abc.ABCMeta):
        pass
    if not issubclass(type(object), abc.ABCMeta):
        pass
    return False
    if hasattr(object, '__abstractmethods__'):
        pass
    if hasattr(object, '__abstractmethods__'):
        pass
    return False
    for None in object.__dict__.items():
        if ():
            if getattr(value, '__isabstractmethod__', False):
                pass
            if not getattr(value, '__isabstractmethod__', False):
                continue
        return True
    for None in object.__bases__:
        for None in getattr(base, '__abstractmethods__', ()):
            value = getattr(object, name, None)
            if getattr(value, '__isabstractmethod__', False):
                pass
            if not getattr(value, '__isabstractmethod__', False):
                continue
            return True
    return False


def _getmembers(object, predicate, getter):
    results = []
    processed = set()
    names = dir(object)
    if isclass(object):
        pass
    if isclass(object):
        mro = getmro(object)
        
        try:
            for base in object.__bases__:
                for None in base.__dict__.items():
                    pass

    for None in names:
        
        try:
            value = None(object, key)
            if key in processed:
                pass
            raise AttributeError
        except AttributeError:
            for base in mro:
                if not key in base.__dict__:
                    continue
                value = base.__dict__[key]

        if predicate:
            pass
        if predicate:
            if None(value):
                pass
            if None(value):
                pass
        results.append((key, value))
        processed.add(key)
    results.sort(key = (lambda pair: pair[0]))
    return results
    if AttributeError:
        pass
    continue

if (lambda object, predicate: _getmembers(object, predicate, getattr)):
    
    def getmembers(object, predicate):
        '''Return all members of an object as (name, value) pairs sorted by name.
Optionally, only return members that satisfy a given predicate.'''
        return _getmembers(object, predicate, getattr)

if (lambda object, predicate: _getmembers(object, predicate, getattr_static)):
    
    def getmembers_static(object, predicate):
        """Return all members of an object as (name, value) pairs sorted by name
without triggering dynamic lookup via the descriptor protocol,
__getattr__ or __getattribute__. Optionally, only return members that
satisfy a given predicate.

Note: this function may not be able to retrieve all members
   that getmembers can fetch (like dynamically created attributes)
   and may find members that getmembers can't (like descriptors
   that raise AttributeError). It can also return descriptor objects
   instead of instance members in some cases.
"""
        return _getmembers(object, predicate, getattr_static)

Attribute = None('Attribute', 'name kind defining_class object')

def classify_class_attrs(cls):
    """Return list of attribute-descriptor tuples.

For each name in dir(cls), the return list contains a 4-tuple
with these elements:

    0. The name (a string).

    1. The kind of attribute this is, one of these strings:
           'class method'    created via classmethod()
           'static method'   created via staticmethod()
           'property'        created via property()
           'method'          any other flavor of method or descriptor
           'data'            not a method

    2. The class which defined this attribute (a class).

    3. The object as obtained by calling getattr; if this fails, or if the
       resulting object does not live anywhere in the class' mro (including
       metaclasses) then the object is looked up in the defining class's
       dict (found by walking the mro).

If one of the items in dir(cls) is stored in the metaclass it will now
be discovered and not have None be listed as the class in which it was
defined.  Any items whose home class cannot be discovered are skipped.
"""
    mro = getmro(cls)
    metamro = getmro(type(cls))
    metamro = (lambda .0: if None:
passfor None in .0:
if None:
if not None not in (type, object):
continueif cls:
pass)(metamro())
    class_bases = (cls,) + mro
    all_bases = class_bases + metamro
    names = dir(cls)
    for base in mro:
        for None in base.__dict__.items():
            if ():
                if isinstance(v, types.DynamicClassAttribute):
                    pass
                if not isinstance(v, types.DynamicClassAttribute):
                    continue
                if v.fget:
                    continue
                continue
                ()
                continue
                tuple
                set() = []
                for name in names:
                    homecls = None
                    get_obj = None
                    dict_obj = None
                    if name not in processed:
                        
                        try:
                            if name == '__dict__':
                                pass
                            raise Exception("__dict__ is special, don't want the proxy")
                            get_obj = getattr(cls, name)
                        except Exception:
                            pass

                        homecls = getattr(get_obj, '__objclass__', homecls)
                        if homecls not in class_bases:
                            homecls = None
                            last_cls = None
                            for srch_cls in class_bases:
                                srch_obj = getattr(srch_cls, name, None)
                                if not srch_obj is get_obj:
                                    continue
                                last_cls = srch_cls
                            for srch_cls in metamro:
                                
                                try:
                                    srch_obj = srch_cls.__getattr__(cls, name)
                                except AttributeError:
                                    pass

                                if not srch_obj is get_obj:
                                    continue
                                last_cls = srch_cls
                            if last_cls:
                                pass
                    homecls = last_cls
                    for base in all_bases:
                        if not name in base.__dict__:
                            continue
                        dict_obj = base.__dict__[name]
                        if homecls not in metamro:
                            pass
                        homecls = base
                        last_cls
                if homecls:
                    continue
    obj = get_obj if get_obj else dict_obj
    if isinstance(dict_obj, (staticmethod, types.BuiltinMethodType)):
        pass
    if isinstance(dict_obj, (staticmethod, types.BuiltinMethodType)):
        kind = 'static method'
        obj = dict_obj
    elif isinstance(dict_obj, (classmethod, types.ClassMethodDescriptorType)):
        pass
    if isinstance(dict_obj, (classmethod, types.ClassMethodDescriptorType)):
        kind = 'class method'
        obj = dict_obj
    elif isinstance(dict_obj, property):
        pass
    if isinstance(dict_obj, property):
        kind = 'property'
        obj = dict_obj
    elif isroutine(obj):
        pass
    result.append(Attribute(name, kind, homecls, obj))
    processed.add(name)
    continue
    tuple
    return result


def getmro(cls):
    '''Return tuple of base classes (including cls) in method resolution order.'''
    return cls.__mro__

if (lambda func, *, stop: f = funcmemo = {
id(f): f }recursion_limit = None()if isinstance(func, type):
passif not isinstance(func, type):
if hasattr(func, '__wrapped__'):
passif hasattr(func, '__wrapped__'):
if stop:
if None(func):
passif None(func):
passfuncfunc = sys.getrecursionlimit.__wrapped__id_func = id(func)if id_func in memo or len(memo) >= recursion_limit:
passraise ValueError('wrapper loop when unwrapping {!r}'.format(f))memo[id_func] = funcif isinstance(func, type):
passif not isinstance(func, type):
if hasattr(func, '__wrapped__'):
passif hasattr(func, '__wrapped__'):
continuefunc):
    
    def unwrap(func, *, stop):
        '''Get the object wrapped by *func*.

Follows the chain of :attr:`__wrapped__` attributes returning the last
object in the chain.

*stop* is an optional callback accepting an object in the wrapper chain
as its sole argument that allows the unwrapping to be terminated early if
the callback returns a true value. If the callback never returns a true
value, the last object in the chain is returned as usual. For example,
:func:`signature` uses this to stop unwrapping if any object in the
chain has a ``__signature__`` attribute defined.

:exc:`ValueError` is raised if a cycle is encountered.

 '''
        f = func
        memo = {
            id(f): f }
        recursion_limit = None()
        if isinstance(func, type):
            pass
        if not isinstance(func, type):
            if hasattr(func, '__wrapped__'):
                pass
            if hasattr(func, '__wrapped__'):
                if stop:
                    if None(func):
                        pass
                    if None(func):
                        pass
                return func
            func = sys.getrecursionlimit.__wrapped__
            id_func = id(func)
            if id_func in memo or len(memo) >= recursion_limit:
                pass
            raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
        memo[id_func] = func
        if isinstance(func, type):
            pass
        if not isinstance(func, type):
            if hasattr(func, '__wrapped__'):
                pass
            if hasattr(func, '__wrapped__'):
                continue
        return func


def indentsize(line):
    '''Return the indent size, in spaces, at the start of a line of text.'''
    expline = line.expandtabs()
    return len(expline) - len(expline.lstrip())


def _findclass(func):
    cls = sys.modules.get(func.__module__)
    if cls:
        pass
    return None
    for name in func.__qualname__.split('.')[:-1]:
        cls = getattr(cls, name)
    if isclass(cls):
        pass
    if not isclass(cls):
        pass
    return None
    return cls


def _finddoc(obj):
    if isclass(obj):
        pass
    if isclass(obj):
        for base in obj.__mro__:
            if not base is not object:
                continue
            
            try:
                doc = base.__doc__
            except AttributeError:
                pass

            if doc:
                continue
            
            return doc, doc
    return None
    if ismethod(obj):
        pass
    if ismethod(obj):
        obj.__self__ = obj.__func__.__name__
        if isclass(self):
            pass
        if isclass(self) and getattr(getattr(self, name, None), '__func__') is obj.__func__:
            cls = self
        else:
            cls = self.__class__
    elif isfunction(obj):
        pass
    if isfunction(obj):
        name = obj.__name__
        cls = _findclass(obj)
        if cls or getattr(cls, name) is not obj:
            pass
        return None
    elif isbuiltin(obj):
        pass
    if isbuiltin(obj):
        name = obj.__name__
        self = obj.__self__
        if isclass(self):
            pass
        if isclass(self) and self.__qualname__ + '.' + name == obj.__qualname__:
            cls = self
        else:
            cls = self.__class__
    elif isinstance(obj, property):
        pass
    if isinstance(obj, property):
        name = obj.__name__
        cls = _findclass(obj.fget)
        if cls or getattr(cls, name) is not obj:
            pass
        return None
    elif ismethoddescriptor(obj):
        pass
    if not ismethoddescriptor(obj):
        if isdatadescriptor(obj):
            pass
        if isdatadescriptor(obj):
            name = obj.__name__
            cls = obj.__objclass__
            if getattr(cls, name) is not obj:
                pass
            return None
            if ismemberdescriptor(obj):
                pass
            if ismemberdescriptor(obj):
                slots = getattr(cls, '__slots__', None)
                if isinstance(slots, dict):
                    pass
                if isinstance(slots, dict) and name in slots:
                    pass
            return slots[name]
        return None
        for base in cls.__mro__:
            
            try:
                doc = getattr(base, name).__doc__
            except AttributeError:
                pass

            if doc:
                continue
            
            return doc, doc
        cls
        return None


def getdoc(object):
    '''Get the documentation string for an object.

All tabs are expanded to spaces.  To clean up docstrings that are
indented to line up with blocks of code, any whitespace than can be
uniformly removed from the second line onwards is removed.'''
    
    try:
        doc = object.__doc__
    except AttributeError:
        doc

    if doc:
        
        try:
            doc = _finddoc(object)
        except (AttributeError, TypeError):
            pass

        if isinstance(doc, str):
            pass
    if not isinstance(doc, str):
        pass
    return None
    return cleandoc(doc)


def cleandoc(doc):
    '''Clean up indentation from docstrings.

Any whitespace that can be uniformly removed from the second line
onwards is removed.'''
    lines = doc.expandtabs().split('\n')
    margin = sys.maxsize
    for line in lines[1:]:
        content = len(line.lstrip(' '))
        if content:
            pass
        if not content:
            continue
        indent = len(line) - content
        margin = min(margin, indent)
    if lines:
        pass
    if lines:
        lines[0] = lines[0].lstrip(' ')
    if margin < sys.maxsize:
        for i in range(1, len(lines)):
            lines[i] = lines[i][margin:]
    if lines:
        pass
    if lines:
        if lines[-1]:
            pass
        if not lines[-1]:
            lines.pop()
            if lines:
                pass
            if lines:
                if lines[-1]:
                    pass
                if not lines[-1]:
                    continue
    if lines:
        pass
    if lines:
        if lines[0]:
            pass
        if not lines[0]:
            lines.pop(0)
            if lines:
                pass
            if lines:
                if lines[0]:
                    pass
                if not lines[0]:
                    continue
    return '\n'.join(lines)


def getfile(object):
    '''Work out which source or compiled file an object was defined in.'''
    if ismodule(object):
        pass
    if ismodule(object):
        if getattr(object, '__file__', None):
            pass
        if getattr(object, '__file__', None):
            pass
        return object.__file__
    raise None('{!r} is a built-in module'.format(object))
    if isclass(object):
        pass
    if isclass(object):
        if hasattr(object, '__module__'):
            pass
        if hasattr(object, '__module__'):
            module = sys.modules.get(object.__module__)
            if getattr(module, '__file__', None):
                pass
            if getattr(module, '__file__', None):
                pass
            return module.__file__
        if None.__module__ == '__main__':
            pass
        raise OSError('source code not available')
    raise TypeError('{!r} is a built-in class'.format(object))
    if ismethod(object):
        pass
    if ismethod(object):
        pass
    object = object.__func__
    if isfunction(object):
        pass
    if isfunction(object):
        pass
    object = object.__code__
    if istraceback(object):
        pass
    if istraceback(object):
        pass
    object = object.tb_frame
    if isframe(object):
        pass
    if isframe(object):
        pass
    object = object.f_code
    if iscode(object):
        pass
    if iscode(object):
        pass
    return object.co_filename
    raise TypeError('module, class, method, function, traceback, frame, or code object was expected, got {}'.format(type(object).__name__))


def getmodulename(path):
    '''Return the module name for a given file, or None.'''
    fname = os.path.basename(path)
    for None in :
        pass
    , [], suffixes = None, importlib.machinery.all_suffixes()
    suffix = None
    suffixes.sort()
    for None in suffixes:
        if ():
            if fname.endswith(suffix):
                pass
            if not fname.endswith(suffix):
                continue
            return (), fname[:neglen]
        return None
        


def getsourcefile(object):
    """Return the filename that can be used to locate an object's source.
Return None if no way can be identified to get the source.
"""
    filename = getfile(object)
    all_bytecode_suffixes = importlib.machinery.DEBUG_BYTECODE_SUFFIXES[:]
    all_bytecode_suffixes += importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES[:]
    if (lambda .0: if None:
passfor s in .0:
if filename.endswith(s):
passfilename.endswith(s)):
        pass
    if (lambda .0: if None:
passfor s in .0:
if filename.endswith(s):
passfilename.endswith(s))(all_bytecode_suffixes()):
        pass
    if (lambda .0: if None:
passfor s in .0:
if filename.endswith(s):
passfilename.endswith(s))(all_bytecode_suffixes()):
        filename = os.path.splitext(filename)[0] + importlib.machinery.SOURCE_SUFFIXES[0]
    elif (lambda .0: if None:
passfor s in .0:
if filename.endswith(s):
passfilename.endswith(s)):
        pass
    if (lambda .0: if None:
passfor s in .0:
if filename.endswith(s):
passfilename.endswith(s))(importlib.machinery.EXTENSION_SUFFIXES()):
        pass
    if (lambda .0: if None:
passfor s in .0:
if filename.endswith(s):
passfilename.endswith(s))(importlib.machinery.EXTENSION_SUFFIXES()):
        pass
    return None
    if filename.endswith('.fwork'):
        pass
    if filename.endswith('.fwork'):
        pass
    return None
    if filename in linecache.cache:
        pass
    return filename
    if os.path.exists(filename):
        pass
    if os.path.exists(filename):
        pass
    return filename
    module = getmodule(object, filename)
    if getattr(module, '__loader__', None):
        pass
    return filename
    if getattr(getattr(module, '__spec__', None), 'loader', None):
        pass
    return filename

if (lambda object, _filename: if _filename:
if getsourcefile(object):
passif not getsourcefile(object):
getsourcefile(object)_filename = getfile(object)os.path.normcase(os.path.abspath(_filename))):
    
    def getabsfile(object, _filename):
        '''Return an absolute path to the source or compiled file for an object.

The idea is for each object to have a unique origin, so this routine
normalizes the result as much as possible.'''
        if _filename:
            if getsourcefile(object):
                pass
            if not getsourcefile(object):
                getsourcefile(object)
        _filename = getfile(object)
        return os.path.normcase(os.path.abspath(_filename))

modulesbyfile = { }
_filesbymodname = { }
if (lambda object, _filename: if ismodule(object):
passif ismodule(object):
passobjectif hasattr(object, '__module__'):
passif hasattr(object, '__module__'):
passsys.modules.get(object.__module__)if _filename and _filename in modulesbyfile:
passsys.modules.get(modulesbyfile[_filename])try:
file = getabsfile(object, _filename)except (TypeError, FileNotFoundError):
_filenameif file in modulesbyfile:
passsys.modules.get(modulesbyfile[file])for f in sys.modules.copy().items():
if ():
if ismodule(module):
passif not ismodule(module):
continueif hasattr(module, '__file__'):
passif not hasattr(module, '__file__'):
continueif f == _filesbymodname.get(modname, None):
continuef = module.__file__modulesbyfile[f] = module.__name__modulesbyfile[os.path.realpath(f)] = module.__name__if file in modulesbyfile:
passsys.modules.get(modulesbyfile[file])main = sys.modules['__main__']if hasattr(object, '__name__'):
passif not hasattr(object, '__name__'):
passNoneif hasattr(main, object.__name__):
passif hasattr(main, object.__name__):
mainobject = getattr(main, object.__name__)if mainobject is object:
passmainbuiltin = sys.modules['builtins']if hasattr(builtin, object.__name__):
passif hasattr(builtin, object.__name__):
builtinobject = getattr(builtin, object.__name__)if builtinobject is object:
passbuiltin):
    
    def getmodule(object, _filename):
        '''Return the module an object was defined in, or None if not found.'''
        if ismodule(object):
            pass
        if ismodule(object):
            pass
        return object
        if hasattr(object, '__module__'):
            pass
        if hasattr(object, '__module__'):
            pass
        return sys.modules.get(object.__module__)
        if _filename and _filename in modulesbyfile:
            pass
        return sys.modules.get(modulesbyfile[_filename])
        
        try:
            file = getabsfile(object, _filename)
        except (TypeError, FileNotFoundError):
            _filename

        if file in modulesbyfile:
            pass
        return sys.modules.get(modulesbyfile[file])
        for f in sys.modules.copy().items():
            if ():
                if ismodule(module):
                    pass
                if not ismodule(module):
                    continue
                if hasattr(module, '__file__'):
                    pass
                if not hasattr(module, '__file__'):
                    continue
            if f == _filesbymodname.get(modname, None):
                continue
            f = module.__file__
            modulesbyfile[f] = module.__name__
            modulesbyfile[os.path.realpath(f)] = module.__name__
        if file in modulesbyfile:
            pass
        return sys.modules.get(modulesbyfile[file])
        main = sys.modules['__main__']
        if hasattr(object, '__name__'):
            pass
        if not hasattr(object, '__name__'):
            pass
        return None
        if hasattr(main, object.__name__):
            pass
        if hasattr(main, object.__name__):
            mainobject = getattr(main, object.__name__)
            if mainobject is object:
                pass
        return main
        builtin = sys.modules['builtins']
        if hasattr(builtin, object.__name__):
            pass
        if hasattr(builtin, object.__name__):
            builtinobject = getattr(builtin, object.__name__)
            if builtinobject is object:
                pass
            return builtin


def ClassFoundException():
    '''ClassFoundException'''
    __firstlineno__ = 1048
    __static_attributes__ = ()

ClassFoundException = None(ClassFoundException, 'ClassFoundException', Exception)

def findsource(object):
    '''Return the entire source file and starting line number for an object.

The argument may be a module, class, method, function, traceback, frame,
or code object.  The source code is returned as a list of all the lines
in the file and the line number indexes a line in that list.  An OSError
is raised if the source code cannot be retrieved.'''
    file = getsourcefile(object)
    if file:
        pass
    if file:
        None(file)
    else:
        file = getfile(object)
        if file.startswith('<'):
            pass
        if file.startswith('<'):
            if file.endswith('>'):
                pass
            if file.endswith('>'):
                if file.endswith('.fwork'):
                    pass
                if file.endswith('.fwork'):
                    pass
        raise OSError('source code not available')
    module = getmodule(object, file)
    if module:
        pass
    if lines:
        pass
    if not lines:
        pass
    raise OSError('could not get source code')
    if ismodule(object):
        pass
    if ismodule(object):
        pass
    return (lines, 0)
    if isclass(object):
        pass
    if isclass(object):
        
        try:
            lnum = vars(object)['__firstlineno__'] - 1
        except (TypeError, KeyError):
            linecache._getlines_from_code if module else linecache.getlines
            raise OSError('source code not available')

        if lnum >= len(lines):
            pass
        raise OSError('lineno is out of bounds')
    return (lines, lnum)
    if ismethod(object):
        pass
    if ismethod(object):
        pass
    object = object.__func__
    if isfunction(object):
        pass
    if isfunction(object):
        pass
    object = object.__code__
    if istraceback(object):
        pass
    if istraceback(object):
        pass
    object = object.tb_frame
    if isframe(object):
        pass
    if isframe(object):
        pass
    object = object.f_code
    if iscode(object):
        pass
    if iscode(object):
        if hasattr(object, 'co_firstlineno'):
            pass
        if not hasattr(object, 'co_firstlineno'):
            pass
        raise OSError('could not find function definition')
    lnum = object.co_firstlineno - 1
    if lnum >= len(lines):
        pass
    raise OSError('lineno is out of bounds')
    return (lines, lnum)
    raise OSError('could not find code object')


def getcomments(object):
    """Get lines of comments immediately preceding an object's source code.

Returns None when source can't be found.
"""
    
    try:
        if ():
            if ismodule(object):
                pass
            if ismodule(object):
                if lines:
                    pass
                if lines and lines[0][:2] == '#!':
                    pass
                1 = 0
                if start < len(lines) and lines[start].strip() in ('', '#'):
                    start = start + 1
                    if start < len(lines) and lines[start].strip() in ('', '#'):
                        continue
                if start < len(lines):
                    if lines[start][:1] == '#':
                        comments = []
                        end = start
                        if end < len(lines) and lines[end][:1] == '#':
                            comments.append(lines[end].expandtabs())
                            end = end + 1
                            if end < len(lines) and lines[end][:1] == '#':
                                continue
                    return ''.join(comments)

    return None
    if lnum > 0:
        indent = indentsize(lines[lnum])
        end = lnum - 1
        if end >= 0:
            if lines[end].lstrip()[:1] == '#':
                if indentsize(lines[end]) == indent:
                    comments = [
                        lines[end].expandtabs().lstrip()]
                    if end > 0:
                        end = end - 1
                        comment = lines[end].expandtabs().lstrip()
                        if comment[:1] == '#' and indentsize(lines[end]) == indent:
                            comments[:0] = [
                                comment]
                            end = end - 1
                    if comments:
                        pass
                    if comments and comments[0].strip() == '#':
                        comments[:1] = []
                        if comments:
                            pass
                        if comments and comments[0].strip() == '#':
                            continue
                    if comments:
                        pass
                    if comments and comments[-1].strip() == '#':
                        comments[-1:] = []
                        if comments:
                            pass
                        if comments and comments[-1].strip() == '#':
                            continue
                return ''.join(comments)
        return None
    return None
    return None
    if (OSError, TypeError):
        ()


def EndOfBlock():
    '''EndOfBlock'''
    __firstlineno__ = 1156
    __static_attributes__ = ()

EndOfBlock = None(EndOfBlock, 'EndOfBlock', Exception)

def BlockFinder():
    '''BlockFinder'''
    __firstlineno__ = 1158
    __doc__ = 'Provide a tokeneater() method to detect the end of a code block.'
    
    def __init__(self):
        self.indent = 0
        self.islambda = False
        self.started = False
        self.passline = False
        self.indecorator = False
        self.last = 1
        self.body_col0 = None

    
    def tokeneater(self, type, token, srowcol, erowcol, line):
        if self.started:
            pass
        if not self.started:
            if self.indecorator:
                pass
            if not self.indecorator:
                if token == '@':
                    self.indecorator = True
                elif token in ('def', 'class', 'lambda'):
                    if token == 'lambda':
                        self.islambda = True
                    self.started = True
                self.passline = True
        return None
        if type == tokenize.NEWLINE:
            self.passline = False
            self.last = srowcol[0]
            if self.islambda:
                pass
            if self.islambda:
                pass
            raise EndOfBlock
        if self.indecorator:
            pass
        if self.indecorator:
            self.indecorator = False
        return None
        return None
        if self.passline:
            pass
        if self.passline:
            pass
        return None
        if type == tokenize.INDENT:
            if self.body_col0:
                if self.started:
                    pass
                if self.started:
                    self.body_col0 = erowcol[1]
            self.indent = self.indent + 1
            self.passline = True
        return None
        if type == tokenize.DEDENT:
            self.indent = self.indent - 1
            if self.indent <= 0:
                pass
            raise EndOfBlock
        return None
        if type == tokenize.COMMENT:
            if self.body_col0:
                if srowcol[1] >= self.body_col0:
                    self.last = srowcol[0]
                return None
            return None
        return None
        if self.indent == 0:
            if type not in (tokenize.COMMENT, tokenize.NL):
                pass
            raise EndOfBlock
        return None

    __static_attributes__ = ('body_col0', 'indecorator', 'indent', 'islambda', 'last', 'passline', 'started')

BlockFinder = None(BlockFinder, 'BlockFinder')

def getblock(lines):
    '''Extract the block of code at the top of the given list of lines.'''
    blockfinder = BlockFinder()
    
    try:
        tokens = None(iter(lines).__next__)
        for _token in tokens:
            None(_token)
        tokenize.generate_tokens
    except (EndOfBlock, IndentationError):
        pass
    except SyntaxError:
        e = None
        if 'unmatched' not in e.msg:
            pass
        raise e, None
        if _token or _token:
            
            try:
                blockfinder.tokeneater(None(None))
            except (EndOfBlock, IndentationError):
                _token

            e = None
            del e
            e = None
            del e

    return lines[:blockfinder.last]
    
    try:
        tokens = None(iter(lines).__next__)
        for _token in tokens:
            None(_token)
        tokenize.generate_tokens
    except (EndOfBlock, IndentationError):
        pass
    except SyntaxError:
        e = None
        if 'unmatched' not in e.msg:
            pass
        raise e, None
        if _token or _token:
            
            try:
                blockfinder.tokeneater(None(None))
            except (EndOfBlock, IndentationError):
                _token

            e = None
            del e
            e = None
            del e



def getsourcelines(object):
    '''Return a list of source lines and starting line number for an object.

The argument may be a module, class, method, function, traceback, frame,
or code object.  The source code is returned as a list of the lines
corresponding to the object and the line number indicates where in the
original source file the first line of code was found.  An OSError is
raised if the source code cannot be retrieved.'''
    object = unwrap(object)
    if ():
        if istraceback(object):
            pass
        if istraceback(object):
            pass
    if ismodule(object):
        pass
    if not ismodule(object):
        if isframe(object):
            pass
        if isframe(object) and object.f_code.co_name == '<module>':
            pass
    return (lines, 0)
    return (getblock(lines[lnum:]), lnum + 1)


def getsource(object):
