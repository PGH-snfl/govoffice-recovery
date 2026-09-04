# Source Generated with Decompyle++
# File: copy.marshal (Python 3.13)

'''Generic (shallow and deep) copying operations.

Interface summary:

        import copy

        x = copy.copy(y)                # make a shallow copy of y
        x = copy.deepcopy(y)            # make a deep copy of y
        x = copy.replace(y, a=1, b=2)   # new object with fields replaced, as defined by `__replace__`

For module specific errors, copy.Error is raised.

The difference between shallow and deep copying is only relevant for
compound objects (objects that contain other objects, like lists or
class instances).

- A shallow copy constructs a new compound object and then (to the
  extent possible) inserts *the same objects* into it that the
  original contains.

- A deep copy constructs a new compound object and then, recursively,
  inserts *copies* into it of the objects found in the original.

Two problems often exist with deep copy operations that don\'t exist
with shallow copy operations:

 a) recursive objects (compound objects that, directly or indirectly,
    contain a reference to themselves) may cause a recursive loop

 b) because deep copy copies *everything* it may copy too much, e.g.
    administrative data structures that should be shared even between
    copies

Python\'s deep copy operation avoids these problems by:

 a) keeping a table of objects already copied during the current
    copying pass

 b) letting user-defined classes override the copying operation or the
    set of components copied

This version does not copy types like module, class, function, method,
nor stack trace, stack frame, nor file, socket, window, nor any
similar types.

Classes can use the same interfaces to control copying that they use
to control pickling: they can define methods called __getinitargs__(),
__getstate__() and __setstate__().  See the documentation for module
"pickle" for information on these methods.
'''
import types
import weakref
from copyreg import dispatch_table

def Error():
    '''Error'''
    __firstlineno__ = 56
    __static_attributes__ = ()

Error = None(Error, 'Error', Exception)
error = Error
__all__ = [
    'Error',
    'copy',
    'deepcopy',
    'replace']

def copy(x):
    """Shallow copy operation on arbitrary Python objects.

See the module's __doc__ string for more info.
"""
    cls = type(x)
    copier = _copy_dispatch.get(cls)
    if copier:
        pass
    if copier:
        pass
    return None(x)
    if issubclass(cls, type):
        pass
    if issubclass(cls, type):
        pass
    return _copy_immutable(x)
    copier = getattr(cls, '__copy__', None)
    if copier:
        pass
    return None(x)
    reductor = None(cls)
    if isinstance(rv, str):
        pass
    if isinstance(rv, str):
        pass
    return x
    return None(None(_reconstruct))

_copy_dispatch = { }
d = { }

def _copy_immutable(x):
    return x

for t in (types.NoneType, int, float, bool, complex, str, tuple, bytes, frozenset, type, range, slice, property, types.BuiltinFunctionType, types.EllipsisType, types.NotImplementedType, types.FunctionType, types.CodeType, weakref.ref):
    d[t] = _copy_immutable
d[list] = list.copy
d[dict] = dict.copy
d[set] = set.copy
d[bytearray] = bytearray.copy
del d
del t
if (lambda x, memo, _nil: d = id(x)if memo:
memo = { }else:
y = memo.get(d, _nil)if y is not _nil:
passycls = memo(x)copier = _deepcopy_dispatch.get(cls)if copier:
y = None(x, memo)elif issubclass(cls, type):
passif y is not x:
memo[d] = y_keep_alive(x, memo)y):
    
    def deepcopy(x, memo, _nil):
        """Deep copy operation on arbitrary Python objects.

See the module's __doc__ string for more info.
"""
        d = id(x)
        if memo:
            memo = { }
        else:
            y = memo.get(d, _nil)
            if y is not _nil:
                pass
            return y
        cls = memo(x)
        copier = _deepcopy_dispatch.get(cls)
        if copier:
            y = None(x, memo)
        elif issubclass(cls, type):
            pass
        if y is not x:
            memo[d] = y
        _keep_alive(x, memo)
        return y

_deepcopy_dispatch = { }
d = { }

def _deepcopy_atomic(x, memo):
    return x

d[types.NoneType] = _deepcopy_atomic
d[types.EllipsisType] = _deepcopy_atomic
d[types.NotImplementedType] = _deepcopy_atomic
d[int] = _deepcopy_atomic
d[float] = _deepcopy_atomic
d[bool] = _deepcopy_atomic
d[complex] = _deepcopy_atomic
d[bytes] = _deepcopy_atomic
d[str] = _deepcopy_atomic
d[types.CodeType] = _deepcopy_atomic
d[type] = _deepcopy_atomic
d[range] = _deepcopy_atomic
d[types.BuiltinFunctionType] = _deepcopy_atomic
d[types.FunctionType] = _deepcopy_atomic
d[weakref.ref] = _deepcopy_atomic
d[property] = _deepcopy_atomic
if (lambda x, memo, deepcopy: y = []memo[id(x)] = yappend = y.appendfor a in x:
deepcopy(None(a, memo))y):
    
    def _deepcopy_list(x, memo, deepcopy):
        y = []
        memo[id(x)] = y
        append = y.append
        for a in x:
            deepcopy(None(a, memo))
        return y

d[list] = _deepcopy_list
if (lambda x, memo, deepcopy: for None in :
if None:
continueNone, x, y, a = Nonetry:
passexcept KeyError:
a,except:
passNonefor None in zip(x, y):
if ():
if not k is not j:
continueyx = Noney):
    
    def _deepcopy_tuple(x, memo, deepcopy):
        for None in :
            if None:
                continue
                None, x, y, a = None
                
                try:
                    pass
                except KeyError:
                    a,
                except:
                    pass

                return None
            for None in zip(x, y):
                if ():
                    if not k is not j:
                        continue
                    return y
                x = None
                return y

d[tuple] = _deepcopy_tuple
if (lambda x, memo, deepcopy: 