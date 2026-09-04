# Source Generated with Decompyle++
# File: _pydecimal.marshal (Python 3.13)

'''Python decimal arithmetic module'''
__all__ = [
    'Decimal',
    'Context',
    'DecimalTuple',
    'DefaultContext',
    'BasicContext',
    'ExtendedContext',
    'DecimalException',
    'Clamped',
    'InvalidOperation',
    'DivisionByZero',
    'Inexact',
    'Rounded',
    'Subnormal',
    'Overflow',
    'Underflow',
    'FloatOperation',
    'DivisionImpossible',
    'InvalidContext',
    'ConversionSyntax',
    'DivisionUndefined',
    'ROUND_DOWN',
    'ROUND_HALF_UP',
    'ROUND_HALF_EVEN',
    'ROUND_CEILING',
    'ROUND_FLOOR',
    'ROUND_UP',
    'ROUND_HALF_DOWN',
    'ROUND_05UP',
    'setcontext',
    'getcontext',
    'localcontext',
    'MAX_PREC',
    'MAX_EMAX',
    'MIN_EMIN',
    'MIN_ETINY',
    'HAVE_THREADS',
    'HAVE_CONTEXTVAR']
__xname__ = __name__
__name__ = 'decimal'
__version__ = '1.70'
__libmpdec_version__ = '2.4.2'
import math as _math
import numbers as _numbers
import sys

try:
    from collections import namedtuple as _namedtuple
    DecimalTuple = None('DecimalTuple', 'sign digits exponent', module = 'decimal')
except ImportError:
    pow
    
    DecimalTuple = lambda *args: args

ROUND_DOWN = 'ROUND_DOWN'
ROUND_HALF_UP = 'ROUND_HALF_UP'
ROUND_HALF_EVEN = 'ROUND_HALF_EVEN'
ROUND_CEILING = 'ROUND_CEILING'
ROUND_FLOOR = 'ROUND_FLOOR'
ROUND_UP = 'ROUND_UP'
ROUND_HALF_DOWN = 'ROUND_HALF_DOWN'
ROUND_05UP = 'ROUND_05UP'
HAVE_THREADS = True
HAVE_CONTEXTVAR = True
if sys.maxsize == 0x7FFFFFFFFFFFFFFF:
    MAX_PREC = 0xDE0B6B3A763FFFF
    MAX_EMAX = 0xDE0B6B3A763FFFF
    MIN_EMIN = -0xDE0B6B3A763FFFF
else:
    MAX_PREC = 425000000
    MAX_EMAX = 425000000
    MIN_EMIN = -425000000
MIN_ETINY = MIN_EMIN - MAX_PREC - 1

def DecimalException():
    '''DecimalException'''
    __firstlineno__ = 95
    __doc__ = "Base exception class.\n\nUsed exceptions derive from this.\nIf an exception derives from another exception besides this (such as\nUnderflow (Inexact, Rounded, Subnormal)) that indicates that it is only\ncalled if the others are present.  This isn't actually used for\nanything, though.\n\nhandle  -- Called when context._raise_error is called and the\n           trap_enabler is not set.  First argument is self, second is the\n           context.  More arguments can be given, those being after\n           the explanation in _raise_error (For example,\n           context._raise_error(NewError, '(-x)!', self._sign) would\n           call NewError().handle(context, self._sign).)\n\nTo define a new exception, it should be sufficient to have it derive\nfrom DecimalException.\n"
    
    def handle(self, context, *args):
        pass

    __static_attributes__ = ()

DecimalException = None(DecimalException, 'DecimalException', ArithmeticError)

def Clamped():
    '''Clamped'''
    __firstlineno__ = 118
    __doc__ = 'Exponent of a 0 changed to fit bounds.\n\nThis occurs and signals clamped if the exponent of a result has been\naltered in order to fit the constraints of a specific concrete\nrepresentation.  This may occur when the exponent of a zero result would\nbe outside the bounds of a representation, or when a large normal\nnumber would have an encoded exponent that cannot be represented.  In\nthis latter case, the exponent is reduced to fit and the corresponding\nnumber of zero digits are appended to the coefficient ("fold-down").\n'
    __static_attributes__ = ()

Clamped = None(Clamped, 'Clamped', DecimalException)

def InvalidOperation():
    '''InvalidOperation'''
    __firstlineno__ = 130
    __doc__ = 'An invalid operation was performed.\n\nVarious bad things cause this:\n\nSomething creates a signaling NaN\n-INF + INF\n0 * (+-)INF\n(+-)INF / (+-)INF\nx % 0\n(+-)INF % x\nx._rescale( non-integer )\nsqrt(-x) , x > 0\n0 ** 0\nx ** (non-integer)\nx ** (+-)INF\nAn operand is invalid\n\nThe result of the operation after this is a quiet positive NaN,\nexcept when the cause is a signaling NaN, in which case the result is\nalso a quiet NaN, but with the original sign, and an optional\ndiagnostic information.\n'
    
    def handle(self, context, *args):
        if args:
            pass
        if args:
            ans = _dec_from_triple(args[0]._sign, args[0]._int, 'n', True)
        return ans._fix_nan(context)
        return _NaN

    __static_attributes__ = ()

InvalidOperation = None(InvalidOperation, 'InvalidOperation', DecimalException)

def ConversionSyntax():
    '''ConversionSyntax'''
    __firstlineno__ = 159
    __doc__ = 'Trying to convert badly formed string.\n\nThis occurs and signals invalid-operation if a string is being\nconverted to a number and it does not conform to the numeric string\nsyntax.  The result is [0,qNaN].\n'
    
    def handle(self, context, *args):
        return _NaN

    __static_attributes__ = ()

ConversionSyntax = None(ConversionSyntax, 'ConversionSyntax', InvalidOperation)

def DivisionByZero():
    '''DivisionByZero'''
    __firstlineno__ = 169
    __doc__ = 'Division by 0.\n\nThis occurs and signals division-by-zero if division of a finite number\nby zero was attempted (during a divide-integer or divide operation, or a\npower operation with negative right-hand operand), and the dividend was\nnot zero.\n\nThe result of the operation is [sign,inf], where sign is the exclusive\nor of the signs of the operands for divide, or is 1 for an odd power of\n-0, for power.\n'
    
    def handle(self, context, sign, *args):
        return _SignedInfinity[sign]

    __static_attributes__ = ()

DivisionByZero = None(DivisionByZero, 'DivisionByZero', DecimalException, ZeroDivisionError)

def DivisionImpossible():
    '''DivisionImpossible'''
    __firstlineno__ = 185
    __doc__ = 'Cannot perform the division adequately.\n\nThis occurs and signals invalid-operation if the integer result of a\ndivide-integer or remainder operation had too many digits (would be\nlonger than precision).  The result is [0,qNaN].\n'
    
    def handle(self, context, *args):
        return _NaN

    __static_attributes__ = ()

DivisionImpossible = None(DivisionImpossible, 'DivisionImpossible', InvalidOperation)

def DivisionUndefined():
    '''DivisionUndefined'''
    __firstlineno__ = 196
    __doc__ = 'Undefined result of division.\n\nThis occurs and signals invalid-operation if division by zero was\nattempted (during a divide-integer, divide, or remainder operation), and\nthe dividend is also zero.  The result is [0,qNaN].\n'
    
    def handle(self, context, *args):
        return _NaN

    __static_attributes__ = ()

DivisionUndefined = None(DivisionUndefined, 'DivisionUndefined', InvalidOperation, ZeroDivisionError)

def Inexact():
    '''Inexact'''
    __firstlineno__ = 207
    __doc__ = 'Had to round, losing information.\n\nThis occurs and signals inexact whenever the result of an operation is\nnot exact (that is, it needed to be rounded and any discarded digits\nwere non-zero), or if an overflow or underflow condition occurs.  The\nresult in all cases is unchanged.\n\nThe inexact signal may be tested (or trapped) to determine if a given\noperation (or sequence of operations) was inexact.\n'
    __static_attributes__ = ()

Inexact = None(Inexact, 'Inexact', DecimalException)

def InvalidContext():
    '''InvalidContext'''
    __firstlineno__ = 219
    __doc__ = 'Invalid context.  Unknown rounding, for example.\n\nThis occurs and signals invalid-operation if an invalid context was\ndetected during an operation.  This can occur if contexts are not checked\non creation and either the precision exceeds the capability of the\nunderlying concrete representation or an unknown or unsupported rounding\nwas specified.  These aspects of the context need only be checked when\nthe values are required to be used.  The result is [0,qNaN].\n'
    
    def handle(self, context, *args):
        return _NaN

    __static_attributes__ = ()

InvalidContext = None(InvalidContext, 'InvalidContext', InvalidOperation)

def Rounded():
    '''Rounded'''
    __firstlineno__ = 233
    __doc__ = 'Number got rounded (not  necessarily changed during rounding).\n\nThis occurs and signals rounded whenever the result of an operation is\nrounded (that is, some zero or non-zero digits were discarded from the\ncoefficient), or if an overflow or underflow condition occurs.  The\nresult in all cases is unchanged.\n\nThe rounded signal may be tested (or trapped) to determine if a given\noperation (or sequence of operations) caused a loss of precision.\n'
    __static_attributes__ = ()

Rounded = None(Rounded, 'Rounded', DecimalException)

def Subnormal():
    '''Subnormal'''
    __firstlineno__ = 245
    __doc__ = 'Exponent < Emin before rounding.\n\nThis occurs and signals subnormal whenever the result of a conversion or\noperation is subnormal (that is, its adjusted exponent is less than\nEmin, before any rounding).  The result in all cases is unchanged.\n\nThe subnormal signal may be tested (or trapped) to determine if a given\nor operation (or sequence of operations) yielded a subnormal result.\n'
    __static_attributes__ = ()

Subnormal = None(Subnormal, 'Subnormal', DecimalException)

def Overflow():
    '''Overflow'''
    __firstlineno__ = 256
    __doc__ = 'Numerical overflow.\n\nThis occurs and signals overflow if the adjusted exponent of a result\n(from a conversion or from an operation that is not an attempt to divide\nby zero), after rounding, would be greater than the largest value that\ncan be handled by the implementation (the value Emax).\n\nThe result depends on the rounding mode:\n\nFor round-half-up and round-half-even (and for round-half-down and\nround-up, if implemented), the result of the operation is [sign,inf],\nwhere sign is the sign of the intermediate result.  For round-down, the\nresult is the largest finite number that can be represented in the\ncurrent precision, with the sign of the intermediate result.  For\nround-ceiling, the result is the same as for round-down if the sign of\nthe intermediate result is 1, or is [0,inf] otherwise.  For round-floor,\nthe result is the same as for round-down if the sign of the intermediate\nresult is 0, or is [1,inf] otherwise.  In all cases, Inexact and Rounded\nwill also be raised.\n'
    
    def handle(self, context, sign, *args):
        if context.rounding in (ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_HALF_DOWN, ROUND_UP):
            pass
        return _SignedInfinity[sign]
        if sign == 0:
            if context.rounding == ROUND_CEILING:
                pass
            return _SignedInfinity[sign]
        return None(sign, '9' * context.prec, (context.Emax - context.prec) + 1)
        if sign == 1:
            if context.rounding == ROUND_FLOOR:
                pass
            return _SignedInfinity[sign]
        return None(sign, '9' * context.prec, (context.Emax - context.prec) + 1)

    __static_attributes__ = ()

Overflow = None(Overflow, 'Overflow', Inexact, Rounded)

def Underflow():
    '''Underflow'''
    __firstlineno__ = 294
    __doc__ = 'Numerical underflow with result rounded to 0.\n\nThis occurs and signals underflow if a result is inexact and the\nadjusted exponent of the result would be smaller (more negative) than\nthe smallest value that can be handled by the implementation (the value\nEmin).  That is, the result is both inexact and subnormal.\n\nThe result after an underflow will be a subnormal number rounded, if\nnecessary, so that its exponent is not less than Etiny.  This may result\nin 0 with the sign of the intermediate result and an exponent of Etiny.\n\nIn all cases, Inexact, Rounded, and Subnormal will also be raised.\n'
    __static_attributes__ = ()

Underflow = None(Underflow, 'Underflow', Inexact, Rounded, Subnormal)

def FloatOperation():
    '''FloatOperation'''
    __firstlineno__ = 309
    __doc__ = 'Enable stricter semantics for mixing floats and Decimals.\n\nIf the signal is not trapped (default), mixing floats and Decimals is\npermitted in the Decimal() constructor, context.create_decimal() and\nall comparison operators. Both conversion and comparisons are exact.\nAny occurrence of a mixed operation is silently recorded by setting\nFloatOperation in the context flags.  Explicit conversions with\nDecimal.from_float() or context.create_decimal_from_float() do not\nset the flag.\n\nOtherwise (the signal is trapped), only equality comparisons and explicit\nconversions are silent. All other mixed operations raise FloatOperation.\n'
    __static_attributes__ = ()

FloatOperation = None(FloatOperation, 'FloatOperation', DecimalException, TypeError)
_signals = [
    Clamped,
    DivisionByZero,
    Inexact,
    Overflow,
    Rounded,
    Underflow,
    InvalidOperation,
    Subnormal,
    FloatOperation]
_condition_map = {
    InvalidContext: InvalidOperation,
    DivisionUndefined: InvalidOperation,
    DivisionImpossible: InvalidOperation,
    ConversionSyntax: InvalidOperation }
_rounding_modes = (ROUND_DOWN, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, ROUND_UP, ROUND_HALF_DOWN, ROUND_05UP)
import contextvars
_current_context_var = None('decimal_context')
_context_attributes = None([
    'prec',
    'Emin',
    'Emax',
    'capitals',
    'clamp',
    'rounding',
    'flags',
    'traps'])

def getcontext():
    """Returns this thread's context.

If this thread does not yet have a context, returns
a new context and sets this thread's context.
New contexts are copies of DefaultContext.
"""
    
    try:
        pass
    except LookupError:
        context = Context()
        _current_context_var.set(context)



def setcontext(context):
    """Set this thread's context to context."""
    if context in (DefaultContext, BasicContext, ExtendedContext):
        context = context.copy()
    context.clear_flags()
    _current_context_var.set(context)

del contextvars
if (lambda ctx: if ctx:
passctx = getcontext()ctx_manager = _ContextManager(ctx)for None in kwargs.items():
if ():
if key not in _context_attributes:
passraise TypeError(f'''\'{key}\' is an invalid keyword argument for this function''')ctx_manager):
    
    def localcontext(ctx, **kwargs):
        '''Return a context manager for a copy of the supplied context

Uses a copy of the current context if no context is specified
The returned context manager creates a local decimal context
in a with statement:
    def sin(x):
         with localcontext() as ctx:
             ctx.prec += 2
             # Rest of sin calculation algorithm
             # uses a precision 2 greater than normal
         return +s  # Convert result to normal precision

     def sin(x):
         with localcontext(ExtendedContext):
             # Rest of sin calculation algorithm
             # uses the Extended Context from the
             # General Decimal Arithmetic Specification
         return +s  # Convert result to normal context

>>> setcontext(DefaultContext)
>>> print(getcontext().prec)
28
>>> with localcontext():
...     ctx = getcontext()
...     ctx.prec += 2
...     print(ctx.prec)
...
30
>>> with localcontext(ExtendedContext):
...     print(getcontext().prec)
...
9
>>> print(getcontext().prec)
28
'''
        if ctx:
            pass
        ctx = getcontext()
        ctx_manager = _ContextManager(ctx)
        for None in kwargs.items():
            if ():
                if key not in _context_attributes:
                    pass
                raise TypeError(f'''\'{key}\' is an invalid keyword argument for this function''')
        return ctx_manager


def Decimal():
    '''Decimal'''
    __firstlineno__ = 426
    __doc__ = 'Floating-point class for decimal arithmetic.'
    __slots__ = ('_exp', '_int', '_sign', '_is_special')
    if (lambda cls, value, context: self = object.__new__(cls)if isinstance(value, str):
passif isinstance(value, str):
m = _parser(value.strip().replace('_', ''))if m:
if context:
passcontext = getcontext()context._raise_error(ConversionSyntax, 'Invalid literal for Decimal: %r' % value)if None.group('sign') == '-':
self._sign = 1else:
self._sign = 0intpart = m.group('int')if intpart:
if m.group('frac'):
passif not m.group('frac'):
m.group('frac')fracpart = ''if m.group('exp'):
passif not m.group('exp'):
m.group('exp')exp = int('0')self._int = str(int(intpart + fracpart))self._exp = exp - len(fracpart)self._is_special = Falseselfdiag = m.group('diag')self._is_special = Trueselfif isinstance(value, int):
passif isinstance(value, int):
self._exp = 0self._int = str(abs(value))self._is_special = Falseselfif isinstance(value, Decimal):
passif isinstance(value, Decimal):
self._exp = value._expself._sign = value._signself._int = value._intself._is_special = value._is_specialselfif isinstance(value, _WorkRep):
passif isinstance(value, _WorkRep):
self._sign = value.signself._int = str(value.int)self._exp = int(value.exp)self._is_special = Falseselfif isinstance(value, (list, tuple)):
passif isinstance(value, (list, tuple)):
if len(value) != 3:
passraise ValueError('Invalid tuple size in creation of Decimal from list or tuple.  The list or tuple should have exactly three elements.')if isinstance(value[0], int):
passif not isinstance(value[0], int) or value[0] in (0, 1):
passraise ValueError('Invalid sign.  The first value in the tuple should be an integer; either 0 for a positive number or 1 for a negative number.')self._sign = value[0]if value[2] == 'F':
self._int = '0'self._exp = value[2]self._is_special = Trueselfdigits = []for digit in value[1]:
if isinstance(digit, int):
passif isinstance(digit, int):
if  <= 0, digit or 0, digit <= 9:
passelse:
None if value >= 0 else intpart if diag else diagelif digits:
passif digits or digit != 0:
digits.append(digit)continueraise ValueError('The second value in the tuple must be composed of integers in the range 0 through 9.')if value[2] in ('n', 'N'):
value[2] = ''.join(map(str, digits))self._is_special = Trueselfif isinstance(value[2], int):
passif isinstance(value[2], int):
if digits:
passif not digits:
digitsself._int = ''.join(map(str, [
0]))self._exp = value[2]self._is_special = Falseselfraise ValueError("The third value in the tuple must be an integer, or one of the strings 'F', 'n', 'N'.")if isinstance(value, float):
passif isinstance(value, float):
if context:
passcontext = getcontext()context._raise_error(FloatOperation, 'strict semantics for mixing floats and Decimals are enabled')value = Decimal.from_float(value)self._exp = value._expself._sign = value._signself._int = value._intself._is_special = value._is_specialselfraise TypeError('Cannot convert %r to Decimal' % value)):
        
        def __new__(cls, value, context):
            """Create a decimal point instance.

>>> Decimal('3.14')              # string input
Decimal('3.14')
>>> Decimal((0, (3, 1, 4), -2))  # tuple (sign, digit_tuple, exponent)
Decimal('3.14')
>>> Decimal(314)                 # int
Decimal('314')
>>> Decimal(Decimal(314))        # another decimal instance
Decimal('314')
>>> Decimal('  3.14  \\n')        # leading and trailing whitespace okay
Decimal('3.14')
"""
            self = object.__new__(cls)
            if isinstance(value, str):
                pass
            if isinstance(value, str):
                m = _parser(value.strip().replace('_', ''))
                if m:
                    if context:
                        pass
                    context = getcontext()
                return context._raise_error(ConversionSyntax, 'Invalid literal for Decimal: %r' % value)
            if None.group('sign') == '-':
                self._sign = 1
            else:
                self._sign = 0
            intpart = m.group('int')
            if intpart:
                if m.group('frac'):
                    pass
                if not m.group('frac'):
                    m.group('frac')
                fracpart = ''
                if m.group('exp'):
                    pass
                if not m.group('exp'):
                    m.group('exp')
                exp = int('0')
                self._int = str(int(intpart + fracpart))
                self._exp = exp - len(fracpart)
                self._is_special = False
            return self
            diag = m.group('diag')
            self._is_special = True
            return self
            if isinstance(value, int):
                pass
            if isinstance(value, int):
                self._exp = 0
                self._int = str(abs(value))
                self._is_special = False
            return self
            if isinstance(value, Decimal):
                pass
            if isinstance(value, Decimal):
                self._exp = value._exp
                self._sign = value._sign
                self._int = value._int
                self._is_special = value._is_special
            return self
            if isinstance(value, _WorkRep):
                pass
            if isinstance(value, _WorkRep):
                self._sign = value.sign
                self._int = str(value.int)
                self._exp = int(value.exp)
                self._is_special = False
            return self
            if isinstance(value, (list, tuple)):
                pass
            if isinstance(value, (list, tuple)):
                if len(value) != 3:
                    pass
                raise ValueError('Invalid tuple size in creation of Decimal from list or tuple.  The list or tuple should have exactly three elements.')
            if isinstance(value[0], int):
                pass
            if not isinstance(value[0], int) or value[0] in (0, 1):
                pass
            raise ValueError('Invalid sign.  The first value in the tuple should be an integer; either 0 for a positive number or 1 for a negative number.')
            self._sign = value[0]
            if value[2] == 'F':
                self._int = '0'
                self._exp = value[2]
                self._is_special = True
            return self
            digits = []
            for digit in value[1]:
                if isinstance(digit, int):
                    pass
                if isinstance(digit, int):
                    if  <= 0, digit or 0, digit <= 9:
                        pass
                    else:
                        None if value >= 0 else intpart if diag else diag
                elif digits:
                    pass
                if digits or digit != 0:
                    digits.append(digit)
                    continue
                raise ValueError('The second value in the tuple must be composed of integers in the range 0 through 9.')
            if value[2] in ('n', 'N'):
                value[2] = ''.join(map(str, digits))
                self._is_special = True
            return self
            if isinstance(value[2], int):
                pass
            if isinstance(value[2], int):
                if digits:
                    pass
                if not digits:
                    digits
                self._int = ''.join(map(str, [
                    0]))
                self._exp = value[2]
                self._is_special = False
            return self
            raise ValueError("The third value in the tuple must be an integer, or one of the strings 'F', 'n', 'N'.")
            if isinstance(value, float):
                pass
            if isinstance(value, float):
                if context:
                    pass
                context = getcontext()
                context._raise_error(FloatOperation, 'strict semantics for mixing floats and Decimals are enabled')
                value = Decimal.from_float(value)
                self._exp = value._exp
                self._sign = value._sign
                self._int = value._int
                self._is_special = value._is_special
            return self
            raise TypeError('Cannot convert %r to Decimal' % value)

    from_float = (lambda cls, f: if isinstance(f, int):
passif isinstance(f, int):
sign = 0 if f >= 0 else 1k = 0coeff = str(abs(f))elif isinstance(f, float):
passif isinstance(f, float):
if None(f):
passif not None(f):
if None(f):
passif None(f):
passNone(repr(f))if ():
str(n * 5 ** k) = d.bit_length() - 1else:
raise TypeError('argument must be int or float.')result = _dec_from_triple(sign, coeff, -k)if cls is Decimal:
passresultNone(result))()
    
    def _isnan(self):
        '''Returns whether the number is not actually one.

0 if a number
1 if NaN
2 if sNaN
'''
        if self._is_special:
            pass
        if self._is_special:
            exp = self._exp
            if exp == 'n':
                pass
            return 1
            if exp == 'N':
                pass
        return 2
        return 0

    
    def _isinfinity(self):
        '''Returns whether the number is infinite

0 if finite or not a number
1 if +INF
-1 if -INF
'''
        if self._exp == 'F':
            if self._sign:
                pass
            if self._sign:
                pass
            return -1
        return 1
        return 0

    if (lambda self, other, context: self_is_nan = self._isnan()if self_is_nan:
passif not self_is_nan:
if other_is_nan:
passif other_is_nan:
if context:
passcontext = getcontext()if self_is_nan == 2:
passcontext._raise_error(InvalidOperation, 'sNaN', self)if None if other else other == 2:
passcontext._raise_error(InvalidOperation, 'sNaN', other)if self_is_nan:
passif self_is_nan:
passself._fix_nan(context)other._fix_nan(context)0):
        
        def _check_nans(self, other, context):
            '''Returns whether the number is not actually one.

if self, other are sNaN, signal
if self, other are NaN return nan
return 0

Done before operations.
'''
            self_is_nan = self._isnan()
            if self_is_nan:
                pass
            if not self_is_nan:
                if other_is_nan:
                    pass
                if other_is_nan:
                    if context:
                        pass
                    context = getcontext()
                    if self_is_nan == 2:
                        pass
                    return context._raise_error(InvalidOperation, 'sNaN', self)
                if None if other else other == 2:
                    pass
            return context._raise_error(InvalidOperation, 'sNaN', other)
            if self_is_nan:
                pass
            if self_is_nan:
                pass
            return self._fix_nan(context)
            return other._fix_nan(context)
            return 0

    
    def _compare_check_nans(self, other, context):
        '''Version of _check_nans used for the signaling comparisons
compare_signal, __le__, __lt__, __ge__, __gt__.

Signal InvalidOperation if either self or other is a (quiet
or signaling) NaN.  Signaling NaNs take precedence over quiet
NaNs.

Return 0 if neither operand is a NaN.

'''
        if context:
            pass
        context = getcontext()
        if self._is_special:
            pass
        if not self._is_special:
            if other._is_special:
                pass
            if other._is_special:
                if self.is_snan():
                    pass
                if self.is_snan():
                    pass
                return context._raise_error(InvalidOperation, 'comparison involving sNaN', self)
            if context.is_snan():
                pass
        if context.is_snan():
            pass
        return context._raise_error(InvalidOperation, 'comparison involving sNaN', other)
        if self.is_qnan():
            pass
        if self.is_qnan():
            pass
        return context._raise_error(InvalidOperation, 'comparison involving NaN', self)
        if other.is_qnan():
            pass
        if other.is_qnan():
            pass
        return context._raise_error(InvalidOperation, 'comparison involving NaN', other)
        return 0

    
    def __bool__(self):
        '''Return True if self is nonzero; otherwise return False.

NaNs and infinities are considered nonzero.
'''
        if self._is_special:
            pass
        if not self._is_special:
            self._is_special
        return self._int != '0'

    
    def _cmp(self, other):
        '''Compare the two non-NaN decimal instances self and other.

Returns -1 if self < other, 0 if self == other and 1
if self > other.  This routine is for internal use only.'''
        if self._is_special:
            pass
        if not self._is_special:
            if other._is_special:
                pass
            if other._is_special:
                self_inf = self._isinfinity()
                other_inf = other._isinfinity()
                if self_inf == other_inf:
                    pass
                return 0
                if self_inf < other_inf:
                    pass
                return -1
        return 1
        if self:
            pass
        if not self:
            if other:
                pass
            if not other:
                pass
            return 0
        return --1 ** other._sign
        if other:
            pass
        if not other:
            pass
        return -1 ** self._sign
        if other._sign < self._sign:
            pass
        return -1
        if self._sign < other._sign:
            pass
        return 1
        self_adjusted = self.adjusted()
        other_adjusted = other.adjusted()
        if self_adjusted == other_adjusted:
            self_padded = self._int + '0' * (self._exp - other._exp)
            other_padded = other._int + '0' * (other._exp - self._exp)
            if self_padded == other_padded:
                pass
            return 0
            if self_padded < other_padded:
                pass
            return --1 ** self._sign
        return None ** self._sign
        if self_adjusted > other_adjusted:
            pass
        return -1 ** self._sign
        return --1 ** self._sign

    if (lambda self, other, context: if ():
passif other is NotImplemented:
passotherif self._check_nans(other, context):
passif self._check_nans(other, context):
passFalseself._cmp(other) == 0):
        
        def __eq__(self, other, context):
            if ():
                pass
            if other is NotImplemented:
                pass
            return other
            if self._check_nans(other, context):
                pass
            if self._check_nans(other, context):
                pass
            return False
            return self._cmp(other) == 0

    if (lambda self, other, context: if ():
passif other is NotImplemented:
passotherif ans:
passif ans:
passFalseself._cmp(other) < 0):
        
        def __lt__(self, other, context):
            if ():
                pass
            if other is NotImplemented:
                pass
            return other
            if ans:
                pass
            if ans:
                pass
            return False
            return self._cmp(other) < 0

    if (lambda self, other, context: if ():
passif other is NotImplemented:
passotherif ans:
passif ans:
passFalseself._cmp(other) <= 0):
        
        def __le__(self, other, context):
            if ():
                pass
            if other is NotImplemented:
                pass
            return other
            if ans:
                pass
            if ans:
                pass
            return False
            return self._cmp(other) <= 0

    if (lambda self, other, context: if ():
passif other is NotImplemented:
passotherif ans:
passif ans:
passFalseself._cmp(other) > 0):
        
        def __gt__(self, other, context):
            if ():
                pass
            if other is NotImplemented:
                pass
            return other
            if ans:
                pass
            if ans:
                pass
            return False
            return self._cmp(other) > 0

    if (lambda self, other, context: if ():
passif other is NotImplemented:
passotherif ans:
passif ans:
passFalseself._cmp(other) >= 0):
        
        def __ge__(self, other, context):
            if ():
                pass
            if other is NotImplemented:
                pass
            return other
            if ans:
                pass
            if ans:
                pass
            return False
            return self._cmp(other) >= 0

    if (lambda self, other, context: other = _convert_other(other, raiseit = True)if self._is_special:
passif not self._is_special:
if other:
passif other:
if other._is_special:
passif other._is_special:
ans = self._check_nans(other, context)if ans:
passif ans:
passansDecimal(self._cmp(other))):
        
        def compare(self, other, context):
            """Compare self to other.  Return a decimal value:

a or b is a NaN ==> Decimal('NaN')
a < b           ==> Decimal('-1')
a == b          ==> Decimal('0')
a > b           ==> Decimal('1')
"""
            other = _convert_other(other, raiseit = True)
            if self._is_special:
                pass
            if not self._is_special:
                if other:
                    pass
                if other:
                    if other._is_special:
                        pass
                    if other._is_special:
                        ans = self._check_nans(other, context)
                        if ans:
                            pass
                        if ans:
                            pass
            return ans
            return Decimal(self._cmp(other))

    
    def __hash__(self):
        '''x.__hash__() <==> hash(x)'''
        if self._is_special:
            pass
        if self._is_special:
            if self.is_snan():
                pass
            if self.is_snan():
                pass
            raise TypeError('Cannot hash a signaling NaN value.')
        if self.is_nan():
            pass
        if self.is_nan():
            pass
        return object.__hash__(self)
        if self._sign:
            pass
        if self._sign:
            pass
        return -_PyHASH_INF
        return _PyHASH_INF
        if self._exp >= 0:
            exp_hash = pow(10, self._exp, _PyHASH_MODULUS)
        else:
            exp_hash = pow(_PyHASH_10INV, -(self._exp), _PyHASH_MODULUS)
        hash_ = int(self._int) * exp_hash % _PyHASH_MODULUS
        ans = hash_ if self >= 0 else -hash_
        if ans == -1:
            pass
        return -2
        return ans

    
    def as_tuple(self):
        '''Represents the number as a triple tuple.

To show the internals exactly as they are.
'''
        return DecimalTuple(self._sign, tuple(map(int, self._int)), self._exp)

    
    def as_integer_ratio(self):
        """Express a finite Decimal instance in the form n / d.

Returns a pair (n, d) of integers.  When called on an infinity
or NaN, raises OverflowError or ValueError respectively.

>>> Decimal('3.14').as_integer_ratio()
(157, 50)
>>> Decimal('-123e5').as_integer_ratio()
(-12300000, 1)
>>> Decimal('0.00').as_integer_ratio()
(0, 1)

"""
        if self._is_special:
            pass
        if self._is_special:
            if self.is_nan():
                pass
            if self.is_nan():
                pass
            raise ValueError('cannot convert NaN to integer ratio')
        raise OverflowError('cannot convert Infinity to integer ratio')
        if self:
            pass
        if not self:
            pass
        return (0, 1)
        n = int(self._int)
        if self._sign:
            pass
        if self._sign:
            pass
        n = -n
        return (n, d)

    
    def __repr__(self):
        '''Represents the number as an instance of Decimal.'''
        return "Decimal('%s')" % str(self)

    if (lambda self, eng, context: sign = [
'',
'-'][self._sign]if self._is_special:
passif self._is_special:
if self._exp == 'F':
passsign + 'Infinity'if None._exp == 'n':
passsign + 'NaN' + self._intsign + 'sNaN' + self._intleftdigits = self._exp + len(self._int)if self._exp <= 0 and leftdigits > -6:
dotplace = leftdigitselif eng:
passif not eng:
dotplace = 1elif self._int == '0':
dotplace = (leftdigits + 1) % 3 - 1else:
dotplace = (leftdigits - 1) % 3 + 1if dotplace <= 0:
intpart = '0'fracpart = '.' + '0' * -dotplace + self._intelif dotplace >= len(self._int):
intpart = self._int + '0' * (dotplace - len(self._int))fracpart = ''else:
intpart = self._int[:dotplace]fracpart = '.' + self._int[dotplace:]if leftdigits == dotplace:
exp = ''elif context:
passcontext = getcontext()exp = [
'e',
'E'][context.capitals] + '%+d' % (leftdigits - dotplace)sign + intpart + fracpart + exp):
        
        def __str__(self, eng, context):
            '''Return string representation of the number in scientific notation.

Captures all of the information in the underlying representation.
'''
            sign = [
                '',
                '-'][self._sign]
            if self._is_special:
                pass
            if self._is_special:
                if self._exp == 'F':
                    pass
                return sign + 'Infinity'
            if None._exp == 'n':
                pass
            return sign + 'NaN' + self._int
            return sign + 'sNaN' + self._int
            leftdigits = self._exp + len(self._int)
            if self._exp <= 0 and leftdigits > -6:
                dotplace = leftdigits
            elif eng:
                pass
            if not eng:
                dotplace = 1
            elif self._int == '0':
                dotplace = (leftdigits + 1) % 3 - 1
            else:
                dotplace = (leftdigits - 1) % 3 + 1
            if dotplace <= 0:
                intpart = '0'
                fracpart = '.' + '0' * -dotplace + self._int
            elif dotplace >= len(self._int):
                intpart = self._int + '0' * (dotplace - len(self._int))
                fracpart = ''
            else:
                intpart = self._int[:dotplace]
                fracpart = '.' + self._int[dotplace:]
            if leftdigits == dotplace:
                exp = ''
            elif context:
                pass
            context = getcontext()
            exp = [
                'e',
                'E'][context.capitals] + '%+d' % (leftdigits - dotplace)
            return sign + intpart + fracpart + exp

    if (lambda self, context: self.__str__(eng = True, context = context)):
        
        def to_eng_string(self, context):
            '''Convert to a string, using engineering notation if an exponent is needed.

Engineering notation has an exponent which is a multiple of 3.  This
can leave up to 3 digits to the left of the decimal place and may
require the addition of either one or two trailing zeros.
'''
            return self.__str__(eng = True, context = context)

    if (lambda self, context: if self._is_special:
passif self._is_special:
ans = self._check_nans(context = context)if ans:
passif ans:
passansif context:
passcontext = getcontext()if self:
passans._fix(context)):
        
        def __neg__(self, context):
            '''Returns a copy with the sign switched.

Rounds, if it has reason.
'''
            if self._is_special:
                pass
            if self._is_special:
                ans = self._check_nans(context = context)
                if ans:
                    pass
                if ans:
                    pass
            return ans
            if context:
                pass
            context = getcontext()
            if self:
                pass
            return ans._fix(context)

    if (lambda self, context: if self._is_special:
passif self._is_special:
ans = self._check_nans(context = context)if ans:
passif ans:
passansif context:
passcontext = getcontext()if self:
passans._fix(context)):
        
        def __pos__(self, context):
            '''Returns a copy, unless it is a sNaN.

Rounds the number (if more than precision digits)
'''
            if self._is_special:
                pass
            if self._is_special:
                ans = self._check_nans(context = context)
                if ans:
                    pass
                if ans:
                    pass
            return ans
            if context:
                pass
            context = getcontext()
            if self:
                pass
            return ans._fix(context)

    if (lambda self, round, context: if round:
passif not round:
passself.copy_abs()if self._is_special:
passif self._is_special:
ans = self._check_nans(context = context)if ans:
passif ans:
passansif self._sign:
passif self._sign:
ans = self.__neg__(context = context)ansans = self.__pos__(context = context)ans):
        
        def __abs__(self, round, context):
            """Returns the absolute value of self.

If the keyword argument 'round' is false, do not round.  The
expression self.__abs__(round=False) is equivalent to
self.copy_abs().
"""
            if round:
                pass
            if not round:
                pass
            return self.copy_abs()
            if self._is_special:
                pass
            if self._is_special:
                ans = self._check_nans(context = context)
                if ans:
                    pass
                if ans:
                    pass
            return ans
            if self._sign:
                pass
            if self._sign:
                ans = self.__neg__(context = context)
            return ans
            ans = self.__pos__(context = context)
            return ans

    if (lambda self, other, context: other = _convert_other(other)if other is NotImplemented:
passotherif context:
passcontext = getcontext()if self._is_special:
passif not self._is_special:
if other._is_special:
passif other._is_special:
ans = self._check_nans(other, context)if ans:
passif ans:
passansif context._isinfinity():
passif context._isinfinity():
if self._sign != other._sign:
if other._isinfinity():
passif other._isinfinity():
passcontext._raise_error(InvalidOperation, '-INF + INF')None(self)if other._isinfinity():
passif other._isinfinity():
passDecimal(other)exp = min(self._exp, other._exp)negativezero = 0if context.rounding == ROUND_FLOOR and self._sign != other._sign:
passnegativezero = 1if self:
passif not self:
if other:
passif not other:
sign = min(self._sign, other._sign)if negativezero:
passif negativezero:
passsign = 1ans = _dec_from_triple(sign, '0', exp)ans = ans._fix(context)ansif self:
passif not self:
exp = max(exp, other._exp - context.prec - 1)ans = other._rescale(exp, context.rounding)ans = ans._fix(context)ansif other:
passif not other:
exp = max(exp, self._exp - context.prec - 1)ans = self._rescale(exp, context.rounding)ans = ans._fix(context)ansop1 = _WorkRep(self)op2 = _WorkRep(other)if () or op1.sign != op2.sign:
if op1.int == op2.int:
_dec_from_triple(negativezero, '0', exp) = _WorkRep()ans = ans._fix(context)ansif _WorkRep().int < op2.int:
passif op1:
if op1.sign == 1:
result.sign = 1op1.sign, op2.sign = op2.sign, op1.signelse:
result.sign = 0elif op1.sign == 1:
result.sign = 1(op1.sign, op2.sign) = (0, 0)else:
result.sign = 0result.exp = op1.expans = Decimal(result)ans = ans._fix(context)ans):
        
        def __add__(self, other, context):
            '''Returns self + other.

-INF + INF (or the reverse) cause InvalidOperation errors.
'''
            other = _convert_other(other)
            if other is NotImplemented:
                pass
            return other
            if context:
                pass
            context = getcontext()
            if self._is_special:
                pass
            if not self._is_special:
                if other._is_special:
                    pass
                if other._is_special:
                    ans = self._check_nans(other, context)
                    if ans:
                        pass
                    if ans:
                        pass
                    return ans
                if context._isinfinity():
                    pass
            if context._isinfinity():
                if self._sign != other._sign:
                    if other._isinfinity():
                        pass
                    if other._isinfinity():
                        pass
                return context._raise_error(InvalidOperation, '-INF + INF')
            return None(self)
            if other._isinfinity():
                pass
            if other._isinfinity():
                pass
            return Decimal(other)
            exp = min(self._exp, other._exp)
            negativezero = 0
            if context.rounding == ROUND_FLOOR and self._sign != other._sign:
                pass
            negativezero = 1
            if self:
                pass
            if not self:
                if other:
                    pass
                if not other:
                    sign = min(self._sign, other._sign)
                    if negativezero:
                        pass
                    if negativezero:
                        pass
                    sign = 1
                    ans = _dec_from_triple(sign, '0', exp)
                    ans = ans._fix(context)
            return ans
            if self:
                pass
            if not self:
                exp = max(exp, other._exp - context.prec - 1)
                ans = other._rescale(exp, context.rounding)
                ans = ans._fix(context)
            return ans
            if other:
                pass
            if not other:
                exp = max(exp, self._exp - context.prec - 1)
                ans = self._rescale(exp, context.rounding)
                ans = ans._fix(context)
            return ans
            op1 = _WorkRep(self)
            op2 = _WorkRep(other)
            if () or op1.sign != op2.sign:
                if op1.int == op2.int:
                    _dec_from_triple(negativezero, '0', exp) = _WorkRep()
                    ans = ans._fix(context)
                return ans
            if _WorkRep().int < op2.int:
                pass
            if op1:
                if op1.sign == 1:
                    result.sign = 1
                    op1.sign, op2.sign = op2.sign, op1.sign
                else:
                    result.sign = 0
            elif op1.sign == 1:
                result.sign = 1
                (op1.sign, op2.sign) = (0, 0)
            else:
                result.sign = 0
            result.exp = op1.exp
            ans = Decimal(result)
            ans = ans._fix(context)
            return ans

    __radd__ = __add__
    if (lambda self, other, context: other = _convert_other(other)if other is NotImplemented:
passotherif self._is_special:
passif not self._is_special:
if other._is_special:
passif other._is_special:
ans = self._check_nans(other, context = context)if ans:
passif ans:
passansself.__add__(other.copy_negate(), context = context)):
        
        def __sub__(self, other, context):
            '''Return self - other'''
            other = _convert_other(other)
            if other is NotImplemented:
                pass
            return other
            if self._is_special:
                pass
            if not self._is_special:
                if other._is_special:
                    pass
                if other._is_special:
                    ans = self._check_nans(other, context = context)
                    if ans:
                        pass
                    if ans:
                        pass
            return ans
            return self.__add__(other.copy_negate(), context = context)

    if (lambda self, other, context: other = _convert_other(other)if other is NotImplemented:
passotherother.__sub__(self, context = context)):
        
        def __rsub__(self, other, context):
            '''Return other - self'''
            other = _convert_other(other)
            if other is NotImplemented:
                pass
            return other
            return other.__sub__(self, context = context)

    if (lambda self, other, context: other = _convert_other(other)if other is NotImplemented:
passotherif context:
passcontext = getcontext()resultsign = self._sign ^ other._signif self._is_special:
passif not self._is_special:
if other._is_special:
passif other._is_special:
ans = self._check_nans(other, context)if ans:
passif ans:
passansif context._isinfinity():
passif context._isinfinity():
if other:
passif not other:
passcontext._raise_error(InvalidOperation, '(+-)INF * 0')None[resultsign]if other._isinfinity():
passif other._isinfinity():
if self:
passif not self:
passcontext._raise_error(InvalidOperation, '0 * (+-)INF')None[resultsign]resultexp = self._exp + other._expif self:
passif self:
if other:
passif not other:
ans = _dec_from_triple(resultsign, '0', resultexp)ans = ans._fix(context)ansif self._int == '1':
ans = _dec_from_triple(resultsign, other._int, resultexp)ans = ans._fix(context)ansif other._int == '1':
ans = _dec_from_triple(resultsign, self._int, resultexp)ans = ans._fix(context)ansop1 = _WorkRep(self)op2 = _WorkRep(other)ans = _dec_from_triple(resultsign, str(op1.int * op2.int), resultexp)ans = ans._fix(context)ans):
        
        def __mul__(self, other, context):
            '''Return self * other.

(+-) INF * 0 (or its reverse) raise InvalidOperation.
'''
            other = _convert_other(other)
            if other is NotImplemented:
                pass
            return other
            if context:
                pass
            context = getcontext()
            resultsign = self._sign ^ other._sign
            if self._is_special:
                pass
            if not self._is_special:
                if other._is_special:
                    pass
                if other._is_special:
                    ans = self._check_nans(other, context)
                    if ans:
                        pass
                    if ans:
                        pass
                    return ans
                if context._isinfinity():
                    pass
            if context._isinfinity():
                if other:
                    pass
                if not other:
                    pass
                return context._raise_error(InvalidOperation, '(+-)INF * 0')
            return None[resultsign]
            if other._isinfinity():
                pass
            if other._isinfinity():
                if self:
                    pass
                if not self:
                    pass
                return context._raise_error(InvalidOperation, '0 * (+-)INF')
            return None[resultsign]
            resultexp = self._exp + other._exp
            if self:
                pass
            if self:
                if other:
                    pass
                if not other:
                    ans = _dec_from_triple(resultsign, '0', resultexp)
                    ans = ans._fix(context)
            return ans
            if self._int == '1':
                ans = _dec_from_triple(resultsign, other._int, resultexp)
                ans = ans._fix(context)
            return ans
            if other._int == '1':
                ans = _dec_from_triple(resultsign, self._int, resultexp)
                ans = ans._fix(context)
            return ans
            op1 = _WorkRep(self)
            op2 = _WorkRep(other)
            ans = _dec_from_triple(resultsign, str(op1.int * op2.int), resultexp)
            ans = ans._fix(context)
            return ans

    __rmul__ = __mul__
    if (lambda self, other, context: other = _convert_other(other)if other is NotImplemented:
passNotImplementedif context:
passcontext = getcontext()sign = self._sign ^ other._signif self._is_special:
passif not self._is_special:
if other._is_special:
passif other._is_special:
ans = self._check_nans(other, context)if ans:
passif ans:
passansif context._isinfinity():
passif context._isinfinity():
if other._isinfinity():
passif other._isinfinity():
passcontext._raise_error(InvalidOperation, '(+-)INF/(+-)INF')if self._isinfinity():
passif self._isinfinity():
pass_SignedInfinity[sign]if other._isinfinity():
passif other._isinfinity():
context._raise_error(Clamped, 'Division by infinity')_dec_from_triple(sign, '0', context.Etiny())if other:
passif not other:
if self:
passif not self:
passcontext._raise_error(DivisionUndefined, '0 / 0')None._raise_error(DivisionByZero, 'x / 0', sign)if self:
passans = divmod(op1.int, op2.int * 10 ** (-shift)) if remainder else () if not self else _dec_from_triple(sign, str(coeff), exp)ans._fix(context)):
        
        def __truediv__(self, other, context):
            '''Return self / other.'''
            other = _convert_other(other)
            if other is NotImplemented:
                pass
            return NotImplemented
            if context:
                pass
            context = getcontext()
            sign = self._sign ^ other._sign
            if self._is_special:
                pass
            if not self._is_special:
                if other._is_special:
                    pass
                if other._is_special:
                    ans = self._check_nans(other, context)
                    if ans:
                        pass
                    if ans:
                        pass
                    return ans
                if context._isinfinity():
                    pass
            if context._isinfinity():
                if other._isinfinity():
                    pass
                if other._isinfinity():
                    pass
            return context._raise_error(InvalidOperation, '(+-)INF/(+-)INF')
            if self._isinfinity():
                pass
            if self._isinfinity():
                pass
            return _SignedInfinity[sign]
            if other._isinfinity():
                pass
            if other._isinfinity():
                context._raise_error(Clamped, 'Division by infinity')
            return _dec_from_triple(sign, '0', context.Etiny())
            if other:
                pass
            if not other:
                if self:
                    pass
                if not self:
                    pass
                return context._raise_error(DivisionUndefined, '0 / 0')
            return None._raise_error(DivisionByZero, 'x / 0', sign)
            if self:
                pass
            ans = divmod(op1.int, op2.int * 10 ** (-shift)) if remainder else () if not self else _dec_from_triple(sign, str(coeff), exp)
            return ans._fix(context)

    
    def _divide(self, other, context):
