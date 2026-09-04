# Source Generated with Decompyle++
# File: random.marshal (Python 3.13)

'''Random variable generators.

    bytes
    -----
           uniform bytes (values between 0 and 255)

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           pick weighted random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

    discrete distributions
    ----------------------
           binomial


General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

'''
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from math import tau as TWOPI, floor as _floor, isfinite as _isfinite
from math import lgamma as _lgamma, fabs as _fabs, log2 as _log2
from os import urandom as _urandom
from _collections_abc import Sequence as _Sequence
from operator import index as _index
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
import os as _os
import _random
__all__ = [
    'Random',
    'SystemRandom',
    'betavariate',
    'binomialvariate',
    'choice',
    'choices',
    'expovariate',
    'gammavariate',
    'gauss',
    'getrandbits',
    'getstate',
    'lognormvariate',
    'normalvariate',
    'paretovariate',
    'randbytes',
    'randint',
    'random',
    'randrange',
    'sample',
    'seed',
    'setstate',
    'shuffle',
    'triangular',
    'uniform',
    'vonmisesvariate',
    'weibullvariate']
NV_MAGICCONST = _sqrt / None(2)
LOG4 = None(4)
SG_MAGICCONST = _log + None(4.5)
BPF = 53
RECIP_BPF = 2 ** (-BPF)
_ONE = 1
_sha512 = None

def Random():
    '''Random'''
    __firstlineno__ = 103
    __doc__ = "Random number generator base class used by bound module functions.\n\nUsed to instantiate instances of Random to get generators that don't\nshare state.\n\nClass Random can also be subclassed if you want to use a different basic\ngenerator of your own devising: in that case, override the following\nmethods:  random(), seed(), getstate(), and setstate().\nOptionally, implement a getrandbits() method so that randrange()\ncan cover arbitrarily large ranges.\n\n"
    VERSION = 3
    if (lambda self, x: self.seed(x)self.gauss_next = None):
        
        def __init__(self, x):
            '''Initialize an instance.

Optional argument x controls seeding, as for Random.seed().
'''
            self.seed(x)
            self.gauss_next = None

    if (lambda self, a, version: if version == 1:
if isinstance(a, (str, bytes)):
passif isinstance(a, (str, bytes)):
if isinstance(a, bytes):
passa = a.decode('latin-1') if isinstance(a, bytes) else aif a:
passx = ord(a[0]) << 7 if a else 0for c in map(ord, a):
x = (1000003 * x ^ c) & 0xFFFFFFFFFFFFFFFFx ^= len(a)a = -2 if x == -1 else xelif version == 2:
if isinstance(a, (str, bytes, bytearray)):
passif isinstance(a, (str, bytes, bytearray)):
if _sha512:
try:
_sha512 = sha512import _sha2except ImportError:
__class___sha512 = sha512import hashlibif isinstance(a, str):
passif isinstance(a, str):
passa = a.encode()a = int.from_bytes(a + _sha512(a).digest())elif isinstance(a, (type(None), int, float, str, bytes, bytearray)):
passif not isinstance(a, (type(None), int, float, str, bytes, bytearray)):
passraise TypeError('The only supported seed types are:\nNone, int, float, str, bytes, and bytearray.')self(a)self.gauss_next = None):
        if (lambda self, a, version: if version == 1:
if isinstance(a, (str, bytes)):
passif isinstance(a, (str, bytes)):
if isinstance(a, bytes):
passa = a.decode('latin-1') if isinstance(a, bytes) else aif a:
passx = ord(a[0]) << 7 if a else 0for c in map(ord, a):
x = (1000003 * x ^ c) & 0xFFFFFFFFFFFFFFFFx ^= len(a)a = -2 if x == -1 else xelif version == 2:
if isinstance(a, (str, bytes, bytearray)):
passif isinstance(a, (str, bytes, bytearray)):
if _sha512:
try:
_sha512 = sha512import _sha2except ImportError:
__class___sha512 = sha512import hashlibif isinstance(a, str):
passif isinstance(a, str):
passa = a.encode()a = int.from_bytes(a + _sha512(a).digest())elif isinstance(a, (type(None), int, float, str, bytes, bytearray)):
passif not isinstance(a, (type(None), int, float, str, bytes, bytearray)):
passraise TypeError('The only supported seed types are:\nNone, int, float, str, bytes, and bytearray.')self(a)self.gauss_next = None):
            
            def seed(self, a, version):
                '''Initialize internal state from a seed.

The only supported seed types are None, int, float,
str, bytes, and bytearray.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If *a* is an int, all bits are used.

For version 2 (the default), all of the bits are used if *a* is a str,
bytes, or bytearray.  For version 1 (provided for reproducing random
sequences from older versions of Python), the algorithm for str and
bytes generates a narrower range of seeds.

'''
                global _sha512, _sha512, _sha512, _sha512, _sha512, _sha512
                if version == 1:
                    if isinstance(a, (str, bytes)):
                        pass
                    if isinstance(a, (str, bytes)):
                        if isinstance(a, bytes):
                            pass
                        a = a.decode('latin-1') if isinstance(a, bytes) else a
                        if a:
                            pass
                        x = ord(a[0]) << 7 if a else 0
                        for c in map(ord, a):
                            x = (1000003 * x ^ c) & 0xFFFFFFFFFFFFFFFF
                        x ^= len(a)
                        a = -2 if x == -1 else x
                    elif version == 2:
                        if isinstance(a, (str, bytes, bytearray)):
                            pass
                        if isinstance(a, (str, bytes, bytearray)):
                            if _sha512:
                                
                                try:
                                    _sha512 = sha512
                                    import _sha2
                                except ImportError:
                                    __class__
                                    _sha512 = sha512
                                    import hashlib

                                if isinstance(a, str):
                                    pass
                            if isinstance(a, str):
                                pass
                            a = a.encode()
                            a = int.from_bytes(a + _sha512(a).digest())
                        elif isinstance(a, (type(None), int, float, str, bytes, bytearray)):
                            pass
                if not isinstance(a, (type(None), int, float, str, bytes, bytearray)):
                    pass
                raise TypeError('The only supported seed types are:\nNone, int, float, str, bytes, and bytearray.')
                self(a)
                self.gauss_next = None

        if (lambda self: (__class__, self(), self.gauss_next)):
            
            def getstate(self):
                '''Return internal state; can be passed to setstate() later.'''
                return (__class__, self(), self.gauss_next)

            if (lambda self, state: version = state[0]if version == 3 or (self.gauss_next,):
Noneif version == 2:
if (self.gauss_next,):
try:
passexcept ValueError:
__class__ = superraise TypeError, ee = Nonedel eself(internalstate)Noneraise ValueError(f'''state with version {version} passed to Random.setstate() of version {self.VERSION}''')):
                
                def setstate(self, state):
                    '''Restore internal state from object returned by getstate().'''
                    version = state[0]
                    if version == 3 or (self.gauss_next,):
                        return None
                        if version == 2:
                            if (self.gauss_next,):
                                
                                try:
                                    pass
                                except ValueError:
                                    __class__ = super
                                    raise TypeError, e
                                    e = None
                                    del e

                            self(internalstate)
                    return None
                    raise ValueError(f'''state with version {version} passed to Random.setstate() of version {self.VERSION}''')

                
                def __getstate__(self):
                    return self.getstate()

                
                def __setstate__(self, state):
                    self.setstate(state)

    
    def __reduce__(self):
        return (self.__class__, (), self.getstate())

    
    def __init_subclass__(cls, **kwargs):
        '''Control how subclasses generate random integers.

The algorithm a subclass can use depends on the random() and/or
getrandbits() implementation available to it and determines
whether it can generate random integers from arbitrarily large
ranges.
'''
        for c in cls.__mro__:
            if '_randbelow' in c.__dict__:
                pass
            return None
            if 'getrandbits' in c.__dict__:
                cls._randbelow = cls._randbelow_with_getrandbits
            return None
            if not 'random' in c.__dict__:
                continue
            cls._randbelow = cls._randbelow_without_getrandbits
            return None

    
    def _randbelow_with_getrandbits(self, n):
        '''Return a random int in the range [0,n).  Defined for n > 0.'''
        getrandbits = self.getrandbits
        k = n.bit_length()
        r = None(k)
        if r >= n:
            r = None(k)
            if r >= n:
                continue
        return r

    if (lambda self, n, maxsize: random = self.randomif n >= maxsize:
warn = warnimport warningsNone('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.')random(None() * n)rem = maxsize % nlimit = (maxsize - rem) / maxsizer = None()if r >= limit:
r = None()if r >= limit:
continue_floor(r * maxsize) % n):
        
        def _randbelow_without_getrandbits(self, n, maxsize):
            '''Return a random int in the range [0,n).  Defined for n > 0.

The implementation does not use getrandbits, but only random.
'''
            random = self.random
            if n >= maxsize:
                warn = warn
                import warnings
                None('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.')
            return random(None() * n)
            rem = maxsize % n
            limit = (maxsize - rem) / maxsize
            r = None()
            if r >= limit:
                r = None()
                if r >= limit:
                    continue
            return _floor(r * maxsize) % n

    _randbelow = _randbelow_with_getrandbits
    
    def randbytes(self, n):
        '''Generate n random bytes.'''
        return self.getrandbits(n * 8).to_bytes(n, 'little')

    if (lambda self, start, stop, step: istart = _index(start)if stop:
if step is not _ONE:
passraise TypeError('Missing a non-None stop argument')if istart > 0:
passself._randbelow(istart)raise ValueError('empty range for randrange()')istop = _index(stop)width = istop - istartistep = _index(step)if istep == 1:
if width > 0:
passistart + self._randbelow(width)raise stop(f'''empty range in randrange({start}, {stop})''')if istep > 0:
n = (width + istep - 1) // istepelif istep < 0:
n = (width + istep + 1) // istepelse:
raise ValueError('zero step for randrange()')if n <= 0:
passraise ValueError(f'''empty range in randrange({start}, {stop}, {step})''')istart + istep * self._randbelow(n)):
        
        def randrange(self, start, stop, step):
            '''Choose a random item from range(stop) or range(start, stop[, step]).

Roughly equivalent to ``choice(range(start, stop, step))`` but
supports arbitrarily large ranges and is optimized for common cases.

'''
            istart = _index(start)
            if stop:
                if step is not _ONE:
                    pass
                raise TypeError('Missing a non-None stop argument')
            if istart > 0:
                pass
            return self._randbelow(istart)
            raise ValueError('empty range for randrange()')
            istop = _index(stop)
            width = istop - istart
            istep = _index(step)
            if istep == 1:
                if width > 0:
                    pass
                return istart + self._randbelow(width)
            raise stop(f'''empty range in randrange({start}, {stop})''')
            if istep > 0:
                n = (width + istep - 1) // istep
            elif istep < 0:
                n = (width + istep + 1) // istep
            else:
                raise ValueError('zero step for randrange()')
            if n <= 0:
                pass
            raise ValueError(f'''empty range in randrange({start}, {stop}, {step})''')
            return istart + istep * self._randbelow(n)

    
    def randint(self, a, b):
        '''Return random integer in range [a, b], including both end points.
        '''
        return self.randrange(a, b + 1)

    
    def choice(self, seq):
        '''Choose a random element from a non-empty sequence.'''
        if len(seq):
            pass
        if not len(seq):
            pass
        raise IndexError('Cannot choose from an empty sequence')
        return seq[self._randbelow(len(seq))]

    
    def shuffle(self, x):
        '''Shuffle list x in place, and return None.'''
        randbelow = self._randbelow
        for i in reversed(range(1, len(x))):
            j = None(i + 1)
            x[i], x[j] = x[j], x[i]

    if (lambda self, population, k, *, counts, n = b, cum_counts = b: if isinstance(population, _Sequence):
passif not isinstance(population, _Sequence):
passraise TypeError('Population must be a sequence.  For dicts or sets, use sorted(d).')n = len(population)if counts:
cum_counts = list(_accumulate(counts))if len(cum_counts) != n:
passraise ValueError('The number of counts does not match the population')if cum_counts:
passtotal = cum_counts.pop() if cum_counts else 0if isinstance(total, int):
passif not isinstance(total, int):
passraise TypeError('Counts must be integers')if total < 0:
passraise ValueError('Counts must be non-negative')selections = self.sample(range(total), k = k)bisect = _bisectfor None._randbelow in :
if None:
continues,raise ValueError('Sample larger than population or is negative')21 = [
None] * kif k > 5:
passsetsize += 4 ** _ceil(_log(k * 3, 4))if n <= setsize:
pool = list(population)for i in range(k):
j = None(n - i)result[i] = pool[j]pool[j] = pool[n - i - 1]None if not  <= 0, k or 0, k <= n else countsresultselected = set()selected_add = selected.addfor i in range(k):
j = None(n)if j in selected:
j = None(n)if j in selected:
continueNone(j)result[i] = population[j]randbelowresult):
        
        def sample(self, population, k, *, counts):
            """Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

Repeated elements can be specified one at a time or with the optional
counts parameter.  For example:

    sample(['red', 'blue'], counts=[4, 2], k=5)

is equivalent to:

    sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)

To choose a sample from a range of integers, use range() for the
population argument.  This is especially fast and space efficient
for sampling from a large population:

    sample(range(10000000), 60)

"""
            if isinstance(population, _Sequence):
                pass
            if not isinstance(population, _Sequence):
                pass
            raise TypeError('Population must be a sequence.  For dicts or sets, use sorted(d).')
            n = len(population)
            if counts:
                cum_counts = list(_accumulate(counts))
                if len(cum_counts) != n:
                    pass
                raise ValueError('The number of counts does not match the population')
            if cum_counts:
                pass
            total = cum_counts.pop() if cum_counts else 0
            if isinstance(total, int):
                pass
            if not isinstance(total, int):
                pass
            raise TypeError('Counts must be integers')
            if total < 0:
                pass
            raise ValueError('Counts must be non-negative')
            selections = self.sample(range(total), k = k)
            bisect = _bisect
            for None._randbelow in :
                if None:
                    continue
                    return s,
            raise ValueError('Sample larger than population or is negative')
            21 = [
                None] * k
            if k > 5:
                pass
            setsize += 4 ** _ceil(_log(k * 3, 4))
            if n <= setsize:
                pool = list(population)
                for i in range(k):
                    j = None(n - i)
                    result[i] = pool[j]
                    pool[j] = pool[n - i - 1]
                None if not  <= 0, k or 0, k <= n else counts
            return result
            selected = set()
            selected_add = selected.add
            for i in range(k):
                j = None(n)
                if j in selected:
                    j = None(n)
                    if j in selected:
                        continue
                None(j)
                result[i] = population[j]
            randbelow
            return result
            

    if (lambda self, population, weights, *, cum_weights, k, random = 
    def sample(self, population, k, *, counts):
        """Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

Repeated elements can be specified one at a time or with the optional
counts parameter.  For example:

    sample(['red', 'blue'], counts=[4, 2], k=5)

is equivalent to:

    sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)

To choose a sample from a range of integers, use range() for the
population argument.  This is especially fast and space efficient
for sampling from a large population:

    sample(range(10000000), 60)

"""
        if isinstance(population, _Sequence):
            pass
        if not isinstance(population, _Sequence):
            pass
        raise TypeError('Population must be a sequence.  For dicts or sets, use sorted(d).')
        n = len(population)
        if counts:
            cum_counts = list(_accumulate(counts))
            if len(cum_c