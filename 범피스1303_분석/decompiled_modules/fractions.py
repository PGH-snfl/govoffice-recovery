# Source Generated with Decompyle++
# File: fractions.marshal (Python 3.13)

'''Fraction, infinite-precision, rational numbers.'''
from decimal import Decimal
import functools
import math
import numbers
import operator
import re
import sys
__all__ = [
    'Fraction']
_PyHASH_MODULUS = sys.hash_info.modulus
_PyHASH_INF = sys.hash_info.inf
_hash_algorithm = (lambda numerator, denominator: try:
dinv = pow(denominator, -1, _PyHASH_MODULUS)except ValueError:
hash_ = _PyHASH_INFhash_ = hash(hash(abs(numerator)) * dinv)result = hash_ if numerator >= 0 else -hash_if result == -1:
pass-2result)()
_RATIONAL_FORMAT = None('\n    \\A\\s*                                  # optional whitespace at the start,\n    (?P<sign>[-+]?)                        # an optional sign, then\n    (?=\\d|\\.\\d)                            # lookahead for digit or .digit\n    (?P<num>\\d*|\\d+(_\\d+)*)                # numerator (possibly empty)\n    (?:                                    # followed by\n       (?:\\s*/\\s*(?P<denom>\\d+(_\\d+)*))?   # an optional denominator\n    |                                      # or\n       (?:\\.(?P<decimal>\\d*|\\d+(_\\d+)*))?  # an optional fractional part\n       (?:E(?P<exp>[-+]?\\d+(_\\d+)*))?      # and optional exponent\n    )\n    \\s*\\Z                                  # and optional whitespace to finish\n', re.VERBOSE | re.IGNORECASE)
if (lambda n, d, exponent, no_neg_zero: 