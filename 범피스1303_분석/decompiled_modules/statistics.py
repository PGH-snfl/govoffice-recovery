# Source Generated with Decompyle++
# File: statistics.marshal (Python 3.13)

'''
Basic statistics module.

This module provides functions for calculating statistics of data, including
averages, variance, and standard deviation.

Calculating averages
--------------------

==================  ==================================================
Function            Description
==================  ==================================================
mean                Arithmetic mean (average) of data.
fmean               Fast, floating-point arithmetic mean.
geometric_mean      Geometric mean of data.
harmonic_mean       Harmonic mean of data.
median              Median (middle value) of data.
median_low          Low median of data.
median_high         High median of data.
median_grouped      Median, or 50th percentile, of grouped data.
mode                Mode (most common value) of data.
multimode           List of modes (most common values of data).
quantiles           Divide data into intervals with equal probability.
==================  ==================================================

Calculate the arithmetic mean ("the average") of data:

>>> mean([-1.0, 2.5, 3.25, 5.75])
2.625


Calculate the standard median of discrete data:

>>> median([2, 3, 4, 5])
3.5


Calculate the median, or 50th percentile, of data grouped into class intervals
centred on the data values provided. E.g. if your data points are rounded to
the nearest whole number:

>>> median_grouped([2, 2, 3, 3, 3, 4])  #doctest: +ELLIPSIS
2.8333333333...

This should be interpreted in this way: you have two data points in the class
interval 1.5-2.5, three data points in the class interval 2.5-3.5, and one in
the class interval 3.5-4.5. The median of these data points is 2.8333...


Calculating variability or spread
---------------------------------

==================  =============================================
Function            Description
==================  =============================================
pvariance           Population variance of data.
variance            Sample variance of data.
pstdev              Population standard deviation of data.
stdev               Sample standard deviation of data.
==================  =============================================

Calculate the standard deviation of sample data:

>>> stdev([2.5, 3.25, 5.5, 11.25, 11.75])  #doctest: +ELLIPSIS
4.38961843444...

If you have previously calculated the mean, you can pass it as the optional
second argument to the four "spread" functions to avoid recalculating it:

>>> data = [1, 2, 2, 4, 4, 4, 5, 6]
>>> mu = mean(data)
>>> pvariance(data, mu)
2.5


Statistics for relations between two inputs
-------------------------------------------

==================  ====================================================
Function            Description
==================  ====================================================
covariance          Sample covariance for two variables.
correlation         Pearson\'s correlation coefficient for two variables.
linear_regression   Intercept and slope for simple linear regression.
==================  ====================================================

Calculate covariance, Pearson\'s correlation, and simple linear regression
for two inputs:

>>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> covariance(x, y)
0.75
>>> correlation(x, y)  #doctest: +ELLIPSIS
0.31622776601...
>>> linear_regression(x, y)  #doctest:
LinearRegression(slope=0.1, intercept=1.5)


Exceptions
----------

A single exception is defined: StatisticsError is a subclass of ValueError.

'''
__all__ = [
    'NormalDist',
    'StatisticsError',
    'correlation',
    'covariance',
    'fmean',
    'geometric_mean',
    'harmonic_mean',
    'kde',
    'kde_random',
    'linear_regression',
    'mean',
    'median',
    'median_grouped',
    'median_high',
    'median_low',
    'mode',
    'multimode',
    'pstdev',
    'pvariance',
    'quantiles',
    'stdev',
    'variance']
import math
import numbers
import random
import sys
from fractions import Fraction
from decimal import Decimal
from itertools import count, groupby, repeat
from bisect import bisect_left, bisect_right
from math import hypot, sqrt, fabs, exp, erf, tau, log, fsum, sumprod
from math import isfinite, isinf, pi, cos, sin, tan, cosh, asin, atan, acos
from functools import reduce
from operator import itemgetter
from collections import Counter, namedtuple, defaultdict
_SQRT2 = None(2)
_random = random

def StatisticsError():
    '''StatisticsError'''
    __firstlineno__ = 152
    __static_attributes__ = ()

StatisticsError = None(StatisticsError, 'StatisticsError', ValueError)

def _sum(data):
    '''_sum(data) -> (type, sum, count)

Return a high-precision sum of the given numeric data as a fraction,
together with the type to be converted to and the count of items.

Examples
--------

>>> _sum([3, 2.25, 4.5, -0.5, 0.25])
(<class \'float\'>, Fraction(19, 2), 5)

Some sources of round-off error will be avoided:

# Built-in sum returns zero.
>>> _sum([1e50, 1, -1e50] * 1000)
(<class \'float\'>, Fraction(1000, 1), 3000)

Fractions and Decimals are also supported:

>>> from fractions import Fraction as F
>>> _sum([F(2, 3), F(7, 5), F(1, 4), F(5, 6)])
(<class \'fractions.Fraction\'>, Fraction(63, 20), 4)

>>> from decimal import Decimal as D
>>> data = [D("0.1375"), D("0.2108"), D("0.3061"), D("0.0419")]
>>> _sum(data)
(<class \'decimal.Decimal\'>, Fraction(6963, 10000), 4)

Mixed types are currently treated as an error, except that int is
allowed.
'''
    count = 0
    types = set()
    types_add = types.add
    partials = { }
    partials_get = partials.get
    for None in groupby(data, type):
        if ():
            for None in map(_exact_ratio, values):
                pass
    T = reduce(_coerce, types, int)
    return (T, total, count)

if (lambda data, c: if c:
if (lambda .0: if None:
passfor None in .0:
if None:
d = None - cif (None - c) * d:
passcontinueNone):
            pass
        if (count, count):
            return (T, ssd, c, count)
        set() = (count, count)
        types_add = types.add
        sx_partials = defaultdict(int)
        sxx_partials = defaultdict(int)
        for None in groupby(data, type):
            if ():
                for count in map(_exact_ratio, values):
                    (n, d) = None
                ()
                continue
                (lambda .0: if None:
passfor None in .0:
if None:
d = None - cif (None - c) * d:
passcontinueNone)(data())
                if count:
                    pass
                if not count:
                    Fraction(0) = Fraction(0)
                    c = (c, d)
                elif None in sx_partials:
                    ssd = sx_partials[None]
                    c = sx_partials[None]
                    if _isfinite(ssd):
                        pass
                    if _isfinite(ssd):
                        pass
                    raise _sum
                else:
                    sx = (lambda .0: if None:
passfor None in .0:
if ():
if Fraction(n, d):
passcontinueNone)(sx_partials.items()())
                    sxx = (lambda .0: if None:
passfor None in .0:
if ():
if Fraction(n, d * d):
passcontinue)(sxx_partials.items()())
                    ssd = (count * sxx - sx * sx) / count
                    c = sx / count
    T = reduce(_coerce, types, int)
    return (T, ssd, c, count)
):
    
    def _ss(data, c):
        '''Return the exact mean and sum of square deviations of sequence data.

Calculations are done in a single pass, allowing the input to be an iterator.

If given *c* is used the mean; otherwise, it is calculated from the data.
Use the *c* argument with care, as it can lead to garbage results.

'''
        if c:
            if (lambda .0: if None:
passfor None in .0:
if None:
d = None - cif (None - c) * d:
passcontinueNone):
                pass
            if (count, count):
                return (T, ssd, c, count)
            set() = (count, count)
            types_add = types.add
            sx_partials = defaultdict(int)
            sxx_partials = defaultdict(int)
            for None in groupby(data, type):
                if ():
                    for count in map(_exact_ratio, values):
                        (n, d) = None
                    ()
                    continue
                    (lambda .0: if None:
passfor None in .0:
if None:
d = None - cif (None - c) * d:
passcontinueNone)(data())
                    if count:
                        pass
                    if not count:
                        Fraction(0) = Fraction(0)
                        c = (c, d)
                    elif None in sx_partials:
                        ssd = sx_partials[None]
                        c = sx_partials[None]
                        if _isfinite(ssd):
                            pass
                        if _isfinite(ssd):
                            pass
                        raise _sum
                    else:
                        sx = (lambda .0: if None:
passfor None in .0:
if ():
if Fraction(n, d):
passcontinueNone)(sx_partials.items()())
                        sxx = (lambda .0: if None:
passfor None in .0:
if ():
if Fraction(n, d * d):
passcontinue)(sxx_partials.items()())
                        ssd = (count * sxx - sx * sx) / count
                        c = sx / count
        T = reduce(_coerce, types, int)
        return (T, ssd, c, count)


def _isfinite(x):
    
    try:
        pass
    except AttributeError:
        pass



def _coerce(T, S):
    '''Coerce types T and S to a common type, or raise TypeError.

Coercion rules are currently an implementation detail. See the CoerceTest
test class in test_statistics for details.
'''
    if not T is not bool:
        pass
    raise 'initial type T is bool'()
    if T is S:
        pass
    return T
    if S is int or S is bool:
        pass
    return T
    if T is int:
        pass
    return S
    if issubclass(S, T):
        pass
    if issubclass(S, T):
        pass
    return S
    if issubclass(T, S):
        pass
    if issubclass(T, S):
        pass
    return T
    if issubclass(T, int):
        pass
    if issubclass(T, int):
        pass
    return S
    if issubclass(S, int):
        pass
    if issubclass(S, int):
        pass
    return T
    if issubclass(T, Fraction):
        pass
    if issubclass(T, Fraction):
        if issubclass(S, float):
            pass
        if issubclass(S, float):
            pass
    return S
    if issubclass(T, float):
        pass
    if issubclass(T, float):
        if issubclass(S, Fraction):
            pass
        if issubclass(S, Fraction):
            pass
    return T
    msg = "don't know how to coerce %s and %s"
    raise TypeError(msg % (T.__name__, S.__name__))


def _exact_ratio(x):
    '''Return Real number x to exact (numerator, denominator) pair.

>>> _exact_ratio(0.25)
(1, 4)

x is expected to be an int, Fraction, Decimal or float.
'''
    
    try:
        pass
    except AttributeError:
        pass
    except (OverflowError, ValueError):
        if _isfinite(x):
            pass
        if _isfinite(x):
            pass
        raise None

    return None
    
    try:
        pass
    except AttributeError:
        raise TypeError(msg)



def _convert(value, T):
    '''Convert value to given numeric type T.'''
    if type(value) is T:
        pass
    return value
    if issubclass(T, int):
        pass
    if issubclass(T, int) and value.denominator != 1:
        pass
    T = float
    
    try:
        pass
    except TypeError:
        if issubclass(T, Decimal):
            pass
        if issubclass(T, Decimal):
            pass
        return 
        raise 


if (lambda values, errmsg: if None:
passfor x in values:
if x < 0:
passraise StatisticsError(errmsg)if x:
passx):
    
    def _fail_neg(values, errmsg):
        '''Iterate over values, failing if any are less than zero.'''
        if None:
            pass
        for x in values:
            if x < 0:
                pass
            raise StatisticsError(errmsg)
            if x:
                pass
            x

if (lambda data, *, key: 