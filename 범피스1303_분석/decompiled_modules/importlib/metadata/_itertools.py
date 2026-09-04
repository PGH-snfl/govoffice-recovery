# Source Generated with Decompyle++
# File: _itertools.marshal (Python 3.13)

from itertools import filterfalse
if (lambda iterable, key: if None:
passseen = set()seen_add = seen.addif key:
for element in filterfalse(seen.__contains__, iterable):
None(element)if element:
passelementNonefor element in iterable:
k = None(element)if not k not in seen:
continueNone(k)if element:
passelementkey):
    
    def unique_everseen(iterable, key):
        '''List unique elements, preserving order. Remember all elements ever seen.'''
        if None:
            pass
        seen = set()
        seen_add = seen.add
        if key:
            for element in filterfalse(seen.__contains__, iterable):
                None(element)
                if element:
                    pass
                element
        return None
        for element in iterable:
            k = None(element)
            if not k not in seen:
                continue
            None(k)
            if element:
                pass
            element
        key

if (lambda obj, base_type: if obj:
passiter(())if base_type:
if isinstance(obj, base_type):
passif isinstance(obj, base_type):
passiter((obj,))try:
passexcept TypeError:
objbase_type):
    
    def always_iterable(obj, base_type):
        """If *obj* is iterable, return an iterator over its items::

    >>> obj = (1, 2, 3)
    >>> list(always_iterable(obj))
    [1, 2, 3]

If *obj* is not iterable, return a one-item iterable containing *obj*::

    >>> obj = 1
    >>> list(always_iterable(obj))
    [1]

If *obj* is ``None``, return an empty iterable:

    >>> obj = None
    >>> list(always_iterable(None))
    []

By default, binary and text strings are not considered iterable::

    >>> obj = 'foo'
    >>> list(always_iterable(obj))
    ['foo']

If *base_type* is set, objects for which ``isinstance(obj, base_type)``
returns ``True`` won't be considered iterable.

    >>> obj = {'a': 1}
    >>> list(always_iterable(obj))  # Iterate over the dict's keys
    ['a']
    >>> list(always_iterable(obj, base_type=dict))  # Treat dicts as a unit
    [{'a': 1}]

Set *base_type* to ``None`` to avoid any special handling and treat objects
Python considers iterable as iterable:

    >>> obj = 'foo'
    >>> list(always_iterable(obj, base_type=None))
    ['f', 'o', 'o']
"""
        if obj:
            pass
        return iter(())
        if base_type:
            if isinstance(obj, base_type):
                pass
            if isinstance(obj, base_type):
                pass
        return iter((obj,))
        
        try:
            pass
        except TypeError:
            obj

        return base_type

