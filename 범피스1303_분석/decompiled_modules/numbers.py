# Source Generated with Decompyle++
# File: numbers.marshal (Python 3.13)

'''Abstract Base Classes (ABCs) for numbers, according to PEP 3141.

TODO: Fill out more detailed documentation on the operators.'''
from abc import ABCMeta, abstractmethod
__all__ = [
    'Number',
    'Complex',
    'Real',
    'Rational',
    'Integral']
Number = None((lambda : __firstlineno__ = 37__doc__ = 'All numbers inherit from this class.\n\nIf you just want to check if an argument x is a number, without\ncaring what kind, use isinstance(x, Number).\n'__slots__ = ()__hash__ = None__static_attributes__ = ()), 'Number', metaclass = ABCMeta)

def Complex():
    '''Complex'''
    __firstlineno__ = 57
    __doc__ = "Complex defines the operations that work on the builtin complex type.\n\nIn short, those are: a conversion to complex, .real, .imag, +, -,\n*, /, **, abs(), .conjugate, ==, and !=.\n\nIf it is given heterogeneous arguments, and doesn't have special\nknowledge about them, it should fall back to the builtin complex\ntype as described below.\n"
    __slots__ = ()
    __complex__ = (lambda self: pass)()
    
    def __bool__(self):
        '''True if self != 0. Called for bool(self).'''
        return self != 0

    real = (lambda self: raise NotImplementedError)()()
    imag = (lambda self: raise NotImplementedError)()()
    __add__ = (lambda self, other: raise NotImplementedError)()
    __radd__ = (lambda self, other: raise NotImplementedError)()
    __neg__ = (lambda self: raise NotImplementedError)()
    __pos__ = (lambda self: raise NotImplementedError)()
    
    def __sub__(self, other):
        '''self - other'''
        return self + -other

    
    def __rsub__(self, other):
        '''other - self'''
        return -self + other

    __mul__ = (lambda self, other: raise NotImplementedError)()
    __rmul__ = (lambda self, other: raise NotImplementedError)()
    __truediv__ = (lambda self, other: raise NotImplementedError)()
    __rtruediv__ = (lambda self, other: raise NotImplementedError)()
    __pow__ = (lambda self, exponent: raise NotImplementedError)()
    __rpow__ = (lambda self, base: raise NotImplementedError)()
    __abs__ = (lambda self: raise NotImplementedError)()
    conjugate = (lambda self: raise NotImplementedError)()
    __eq__ = (lambda self, other: raise NotImplementedError)()
    __static_attributes__ = ()

Complex = None(Complex, 'Complex', Number)
<NODE:12>

def Real():
    '''Real'''
    __firstlineno__ = 172
    __doc__ = 'To Complex, Real adds the operations that work on real numbers.\n\nIn short, those are: a conversion to float, trunc(), divmod,\n%, <, <=, >, and >=.\n\nReal also provides defaults for the derived operations.\n'
    __slots__ = ()
    __float__ = (lambda self: raise NotImplementedError)()
    __trunc__ = (lambda self: raise NotImplementedError)()
    __floor__ = (lambda self: raise NotImplementedError)()
    __ceil__ = (lambda self: raise NotImplementedError)()
    if (lambda self, ndigits: raise NotImplementedError):
        pass
    __round__ = (lambda self, ndigits: raise NotImplementedError)()
    
    def __divmod__(self, other):
        '''divmod(self, other): The pair (self // other, self % other).

Sometimes this can be computed faster than the pair of
operations.
'''
        return (self // other, self % other)

    
    def __rdivmod__(self, other):
        '''divmod(other, self): The pair (other // self, other % self).

Sometimes this can be computed faster than the pair of
operations.
'''
        return (other // self, other % self)

    __floordiv__ = (lambda self, other: raise NotImplementedError)()
    __rfloordiv__ = (lambda self, other: raise NotImplementedError)()
    __mod__ = (lambda self, other: raise NotImplementedError)()
    __rmod__ = (lambda self, other: raise NotImplementedError)()
    __lt__ = (lambda self, other: raise NotImplementedError)()
    __le__ = (lambda self, other: raise NotImplementedError)()
    
    def __complex__(self):
        '''complex(self) == complex(float(self), 0)'''
        return complex(float(self))

    real = (lambda self: None(self))()
    imag = (lambda self: 0)()
    
    def conjugate(self):
        '''Conjugate is a no-op for Reals.'''
        return None(self)

    __static_attributes__ = ()

Real = None(Real, 'Real', Complex)
Real.register(float)

def Rational():
    '''Rational'''
    __firstlineno__ = 292
    __doc__ = '.numerator and .denominator should be in lowest terms.'
    __slots__ = ()
    numerator = (lambda self: raise NotImplementedError)()()
    denominator = (lambda self: raise NotImplementedError)()()
    
    def __float__(self):
        '''float(self) = self.numerator / self.denominator

It\'s important that this conversion use the integer\'s "true"
division rather than casting one side to float before dividing
so that ratios of huge integers convert without overflowing.

'''
        return int(self.numerator) / int(self.denominator)

    __static_attributes__ = ()

Rational = None(Rational, 'Rational', Real)

def Integral():
    '''Integral'''
    __firstlineno__ = 319
    __doc__ = 'Integral adds methods that work on integral numbers.\n\nIn short, these are conversion to int, pow with modulus, and the\nbit-string operations.\n'
    __slots__ = ()
    __int__ = (lambda self: raise NotImplementedError)()
    
    def __index__(self):
        '''Called whenever an index is needed, such as in slicing'''
        return int(self)

    if (lambda self, exponent, modulus: raise NotImplementedError):
        pass
    __pow__ = (lambda self, exponent, modulus: raise NotImplementedError)()
    __lshift__ = (lambda self, other: raise NotImplementedError)()
    __rlshift__ = (lambda self, other: raise NotImplementedError)()
    __rshift__ = (lambda self, other: raise NotImplementedError)()
    __rrshift__ = (lambda self, other: raise NotImplementedError)()
    __and__ = (lambda self, other: raise NotImplementedError)()
    __rand__ = (lambda self, other: raise NotImplementedError)()
    __xor__ = (lambda self, other: raise NotImplementedError)()
    __rxor__ = (lambda self, other: raise NotImplementedError)()
    __or__ = (lambda self, other: raise NotImplementedError)()
    __ror__ = (lambda self, other: raise NotImplementedError)()
    __invert__ = (lambda self: raise NotImplementedError)()
    
    def __float__(self):
        '''float(self) == float(int(self))'''
        return float(int(self))

    numerator = (lambda self: None(self))()
    denominator = (lambda self: 1)()
    __static_attributes__ = ()

Integral = None(Integral, 'Integral', Rational)
<NODE:12>
