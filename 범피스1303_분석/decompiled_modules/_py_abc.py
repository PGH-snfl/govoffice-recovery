# Source Generated with Decompyle++
# File: _py_abc.marshal (Python 3.13)

from _weakrefset import WeakSet

def get_cache_token():
    '''Returns the current ABC cache token.

The token is an opaque object (supporting equality testing) identifying the
current version of the ABC cache for virtual subclasses. The token changes
with every call to ``register()`` on any ABC.
'''
    return ABCMeta._abc_invalidation_counter


def ABCMeta():
    '''ABCMeta'''
    __firstlineno__ = 14
    __doc__ = "Metaclass for defining Abstract Base Classes (ABCs).\n\nUse this metaclass to create an ABC.  An ABC can be subclassed\ndirectly, and then acts as a mix-in class.  You can also register\nunrelated concrete classes (even built-in classes) and unrelated\nABCs as 'virtual subclasses' -- these and their descendants will\nbe considered subclasses of the registering ABC by the built-in\nissubclass() function, but the registering ABC won't show up in\ntheir MRO (Method Resolution Order) nor will method\nimplementations defined by the registering ABC be callable (not\neven via super()).\n"
    _abc_invalidation_counter = 0
    if (lambda mcls, name, bases, namespace: cls = (mcls, name, bases, namespace)({ }, kwargs = None)for None in :
if ():
if getattr(value, '__isabstractmethod__', False):
passif not getattr(value, '__isabstractmethod__', False):
continueif name:
continue()None = , {}value = mcls, None, namespace.items()for base in bases:
for name in getattr(base, '__abstractmethods__', set()):
value = getattr(cls, name, None)if getattr(value, '__isabstractmethod__', False):
passif not getattr(value, '__isabstractmethod__', False):
continueabstracts.add(name)supercls.__abstractmethods__ = frozenset(abstracts)cls._abc_registry = WeakSet()cls._abc_cache = WeakSet()cls._abc_negative_cache = WeakSet()cls._abc_negative_cache_version = ABCMeta._abc_invalidation_countercls):
        
        def __new__(mcls, name, bases, namespace, **kwargs):
            cls = (mcls, name, bases, namespace)({ }, kwargs = None)
            for None in :
                if ():
                    if getattr(value, '__isabstractmethod__', False):
                        pass
                    if not getattr(value, '__isabstractmethod__', False):
                        continue
                    if name:
                        continue
            ()
            None = , {}
            value = mcls, None, namespace.items()
            for base in bases:
                for name in getattr(base, '__abstractmethods__', set()):
                    value = getattr(cls, name, None)
                    if getattr(value, '__isabstractmethod__', False):
                        pass
                    if not getattr(value, '__isabstractmethod__', False):
                        continue
                    abstracts.add(name)
                super
            cls.__abstractmethods__ = frozenset(abstracts)
            cls._abc_registry = WeakSet()
            cls._abc_cache = WeakSet()
            cls._abc_negative_cache = WeakSet()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
            return cls
            

        
        def register(cls, subclass):
            '''Register a virtual subclass of an ABC.

Returns the subclass, to allow usage as a class decorator.
'''
            if isinstance(subclass, type):
                pass
            if not isinstance(subclass, type):
                pass
            raise TypeError('Can only register classes')
            if issubclass(subclass, cls):
                pass
            if issubclass(subclass, cls):
                pass
            return subclass
            if issubclass(cls, subclass):
                pass
            if issubclass(cls, subclass):
                pass
            raise RuntimeError('Refusing to create an inheritance cycle')
            cls._abc_registry.add(subclass)
            return subclass

        if (lambda cls, file: print(f'''Class: {cls.__module__}.{cls.__qualname__}''', file = file)print(f'''Inv. counter: {get_cache_token()}''', file = file)for name in cls.__dict__:
if name.startswith('_abc_'):
passif not name.startswith('_abc_'):
continuevalue = getattr(cls, name)if isinstance(value, WeakSet):
passif isinstance(value, WeakSet):
passvalue = set(value)print(f'''{name}: {value}''', file = file)):
            
            def _dump_registry(cls, file):
                '''Debug helper to print the ABC registry.'''
                print(f'''Class: {cls.__module__}.{cls.__qualname__}''', file = file)
                print(f'''Inv. counter: {get_cache_token()}''', file = file)
                for name in cls.__dict__:
                    if name.startswith('_abc_'):
                        pass
                    if not name.startswith('_abc_'):
                        continue
                    value = getattr(cls, name)
                    if isinstance(value, WeakSet):
                        pass
                    if isinstance(value, WeakSet):
                        pass
                    value = set(value)
                    print(f'''{name}: {value}''', file = file)

    
    def _abc_registry_clear(cls):
        '''Clear the registry (for debugging or testing).'''
        cls._abc_registry.clear()

    
    def _abc_caches_clear(cls):
        '''Clear the caches (for debugging or testing).'''
        cls._abc_cache.clear()
        cls._abc_negative_cache.clear()

    
    def __instancecheck__(cls, instance):
        '''Override for isinstance(instance, cls).'''
        subclass = instance.__class__
        if subclass in cls._abc_cache:
            pass
        return True
        subtype = type(instance)
        if subtype is subclass:
            if cls._abc_negative_cache_version == ABCMeta._abc_invalidation_counter and subclass in cls._abc_negative_cache:
                pass
            return False
        return cls.__subclasscheck__(subclass)
        if (lambda .0: if None:
passfor c in .0:
if cls.__subclasscheck__(c):
passcls.__subclasscheck__(c)):
            pass
        return (lambda .0: if None:
passfor c in .0:
if cls.__subclasscheck__(c):
passcls.__subclasscheck__(c))((subclass, subtype)())

    
    def __subclasscheck__(cls, subclass):
        '''Override for issubclass(subclass, cls).'''
        if isinstance(subclass, type):
            pass
        if not isinstance(subclass, type):
            pass
        raise TypeError('issubclass() arg 1 must be a class')
        if subclass in cls._abc_cache:
            pass
        return True
        if cls._abc_negative_cache_version < ABCMeta._abc_invalidation_counter:
            cls._abc_negative_cache = WeakSet()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        elif subclass in cls._abc_negative_cache:
            pass
        return False
        ok = cls.__subclasshook__(subclass)
        if ok is not NotImplemented:
            if isinstance(ok, bool):
                pass
            if not isinstance(ok, bool):
                pass
            raise None
        if ok:
            pass
        if ok:
            cls._abc_cache.add(subclass)
        return ok
        cls._abc_negative_cache.add(subclass)
        return ok
        if cls in getattr(subclass, '__mro__', ()):
            cls._abc_cache.add(subclass)
        return True
        for rcls in cls._abc_registry:
            if issubclass(subclass, rcls):
                pass
            if not issubclass(subclass, rcls):
                continue
            cls._abc_cache.add(subclass)
            return True
        for scls in cls.__subclasses__():
            if issubclass(subclass, scls):
                pass
            if not issubclass(subclass, scls):
                continue
            cls._abc_cache.add(subclass)
            return True
        cls._abc_negative_cache.add(subclass)
        return False

    __static_attributes__ = ()
    __classcell__ = __class__
    return __class__

ABCMeta = None(ABCMeta, 'ABCMeta', type)
