# Source Generated with Decompyle++
# File: tokenize.marshal (Python 3.13)

'''Tokenization help for Python programs.

tokenize(readline) is a generator that breaks a stream of bytes into
Python tokens.  It decodes the bytes according to PEP-0263 for
determining source file encoding.

It accepts a readline-like method which is called repeatedly to get the
next line of input (or b"" for EOF).  It generates 5-tuples with these
members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators.  Additionally, all token lists start with an ENCODING token
which tells you which encoding was used to decode the bytes stream.
'''
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger, Trent Nelson, Michael Foord'
from builtins import open as _builtin_open
from codecs import lookup, BOM_UTF8
import collections
import functools
from io import TextIOWrapper
import itertools as _itertools
import re
import sys
None(import token)
from token import EXACT_TOKEN_TYPES
import _tokenize
cookie_re = None('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = None(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + [
    'tokenize',
    'generate_tokens',
    'detect_encoding',
    'untokenize',
    'TokenInfo',
    'open',
    'TokenError']
del token
TokenInfo = (lambda : __firstlineno__ = 47
def __repr__(self):
annotated_type = '%d (%s)' % (self.type, tok_name[self.type])None % self._replace(type = annotated_type)exact_type = (lambda self: if self.type == OP and self.string in EXACT_TOKEN_TYPES:
passEXACT_TOKEN_TYPES[self.string]self.type)()
    __static_attributes__ = ()
)('TokenInfo', collections.namedtuple, None('TokenInfo', 'type string start end line'))

def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(choices) + '*'


def maybe(*choices):
    return group(choices) + '?'

Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = maybe + None(Comment)
Name = '\\w+'
Hexnumber = '0[xX](?:_?[0-9a-fA-F])+'
Binnumber = '0[bB](?:_?[01])+'
Octnumber = '0[oO](?:_?[0-7])+'
Decnumber = '(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = None(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = maybe + None(Exponent)
Expfloat = '[0-9](?:_?[0-9])*' + Exponent
Floatnumber = None(Pointfloat, Expfloat)
Imagnumber = None('[0-9](?:_?[0-9])*[jJ]', Floatnumber + '[jJ]')
Number = None(Imagnumber, Floatnumber, Intnumber)

def _all_string_prefixes():
    _valid_string_prefixes = [
        'b',
        'r',
        'u',
        'f',
        'br',
        'fr']
    result = {
        ''}
    for prefix in _valid_string_prefixes:
        for t in None(prefix):
            for None in :
                if None:
                    continue
                    for None in _itertools.product, None, t(c,):
                        result.add(''.join(u))
                    continue
    return result
    

_compile = (lambda expr: None(expr, re.UNICODE))()
StringPrefix = _all_string_prefixes(None())
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = None(StringPrefix + "'''", StringPrefix + '"""')
String = None(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Special = map(re.escape(sorted, None(EXACT_TOKEN_TYPES, reverse = True)))
Funny = None('\\r?\\n', Special)
PlainToken = None(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group + None("'", '\\\\\\r?\\n')(StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*', group + None('"', '\\\\\\r?\\n'))
PseudoExtras = None('\\\\\\r?\\n|\\Z', Comment, Triple)
PseudoToken = group + None(PseudoExtras, Number, Funny, ContStr, Name)
endpats = { }
for _prefix in None():
    endpats[_prefix + "'"] = Single
    endpats[_prefix + '"'] = Double
    endpats[_prefix + "'''"] = Single3
    endpats[_prefix + '"""'] = Double3
Whitespace
del _prefix
single_quoted = None()
triple_quoted = None()
for t in None():
    for u in (t + '"', t + "'"):
        single_quoted.add(u)
    set
    for u in (t + '"""', t + "'''"):
        triple_quoted.add(u)
    group
del t
del u
tabsize = 8

def TokenError():
    '''TokenError'''
    __firstlineno__ = 162
    __static_attributes__ = ()

TokenError = None(TokenError, 'TokenError', Exception)

def Untokenizer():
    '''Untokenizer'''
    __firstlineno__ = 165
    
    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0
        self.prev_type = None
        self.prev_line = ''
        self.encoding = None

    
    def add_whitespace(self, start):
        if (() or row < self.prev_row or row == self.prev_row) and col < self.prev_col:
            pass
        raise ValueError('start ({},{}) precedes previous end ({},{})'.format(row, col, self.prev_row, self.prev_col))
        self.add_backslash_continuation(start)
        if col_offset:
            pass
        if col_offset:
            self.tokens.append(' ' * col_offset)
        return None

    
    def add_backslash_continuation(self, start):
        '''Add backslash continuation characters if the row has increased
without encountering a newline token.

This also inserts the correct amount of whitespace before the backslash.
'''
        row = start[0]
        row_offset = row - self.prev_row
        if row_offset == 0:
            pass
        return None
        if self.prev_line.endswith('\r\n'):
            pass
        newline = '\r\n' if self.prev_line.endswith('\r\n') else '\n'
        line = self.prev_line.rstrip('\\\r\n')
        ws = _itertools.takewhile(None(str.isspace, reversed(line)))
        self.tokens.append(ws + f'''\\{newline}''' * row_offset)
        self.prev_col = 0

    
    def escape_brackets(self, token):
        characters = []
        consume_until_next_bracket = False
        for character in token:
            if character == '}':
                if consume_until_next_bracket:
                    pass
                if consume_until_next_bracket:
                    consume_until_next_bracket = False
                else:
                    characters.append(character)
            if character == '{':
                n_backslashes = _itertools.takewhile(None('\\'.__eq__, characters[-2::-1])())
            characters.append(character)
        return ''.join(characters)

    
    def untokenize(self, iterable):
