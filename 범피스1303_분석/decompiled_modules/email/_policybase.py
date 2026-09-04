# Source Generated with Decompyle++
# File: _policybase.marshal (Python 3.13)

'''Policy framework for the email package.

Allows fine grained feature control of how the package parses and emits data.
'''
import abc
from email import header
from email import charset as _charset
from email.utils import _has_surrogates
__all__ = [
    'Policy',
    'Compat32',
    'compat32']

def _PolicyBase():
    '''_PolicyBase'''
    __firstlineno__ = 18
    __doc__ = 'Policy Object basic framework.\n\nThis class is useless unless subclassed.  A subclass should define\nclass attributes with defaults for any values that are to be\nmanaged by the Policy object.  The constructor will then allow\nnon-default values to be set for these attributes at instance\ncreation time.  The instance will be callable, taking these same\nattributes keyword arguments, and returning a new instance\nidentical to the called instance except for those values changed\nby the keyword arguments.  Instances may be added, yielding new\ninstances with any non-default values from the right hand\noperand overriding those in the left hand operand.  That is,\n\n    A + B == A(<non-default values of B>)\n\nThe repr of an instance can be used to reconstruct the object\nif and only if the repr of the values can be used to reconstruct\nthose values.\n\n'
    if (lambda self: for None in kw.items():
if ():
if hasattr(self, name):
passif hasattr(self, name):
self(name, value)continueraise TypeError('{!r} is an invalid keyword argument for {}'.format(name, self.__class__.__name__))super):
        
        def __init__(self, **kw):
            '''Create new Policy, possibly overriding some defaults.

See class docstring for a list of overridable attributes.

'''
            for None in kw.items():
                if ():
                    if hasattr(self, name):
                        pass
                    if hasattr(self, name):
                        self(name, value)
                        continue
                raise TypeError('{!r} is an invalid keyword argument for {}'.format(name, self.__class__.__name__))
            super

        
        def __repr__(self):
            for None in :
                if ():
                    continue
            ()
            None = , []
            value = None, None, self.__dict__.items()
            return '{}({})'.format(self.__class__.__name__, ', '.join(args))
            

        
        def clone(self, **kw):
