# Source Generated with Decompyle++
# File: fnmatch.marshal (Python 3.13)

'''Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)
'''
import os
import posixpath
import re
import functools
__all__ = [
    'filter',
    'fnmatch',
    'fnmatchcase',
    'translate']

def fnmatch(name, pat):
    """Test whether FILENAME matches PATTERN.

Patterns are Unix shell style:

*       matches everything
?       matches any single character
[seq]   matches any character in seq
[!seq]  matches any char not in seq

An initial period in FILENAME is not special.
Both FILENAME and PATTERN are first case-normalized
if the operating system requires it.
If you don't want this, use fnmatchcase(FILENAME, PATTERN).
"""
    name = os.path.normcase(name)
    pat = os.path.normcase(pat)
    return fnmatchcase(name, pat)

_compile_pattern = (lambda pat: if isinstance(pat, bytes):
passif isinstance(pat, bytes):
pat_str = str(pat, 'ISO-8859-1')res_str = translate(pat_str)res = bytes(res_str, 'ISO-8859-1')else:
res = translate(pat)None(res).match)()

def filter(names, pat):
    '''Construct a list from those elements of the iterable NAMES that match PAT.'''
    result = []
    pat = os.path.normcase(pat)
    match = _compile_pattern(pat)
    if os.path is posixpath:
        for name in names:
            if None(name):
                pass
            if not None(name):
                continue
            result.append(name)
    return result
    for name in names:
        if None(os.path.normcase(name)):
            pass
        if not None(os.path.normcase(name)):
            continue
        result.append(name)
    return result


def fnmatchcase(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

This is a version of fnmatch() which doesn't case-normalize
its arguments.
"""
    match = _compile_pattern(pat)
    return None(name) is not None


def translate(pat):
    '''Translate a shell PATTERN to a regular expression.

There is no way to quote meta-characters.
'''
    STAR = object()
    parts = _translate(pat, STAR, '.')
    return _join_translated_parts(parts, STAR)


def _translate(pat, STAR, QUESTION_MARK):
    res = []
    add = res.append
    if len(pat) or i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            if res:
                pass
            if res or res[-1] is not STAR:
                pass
            None(STAR)
        elif c == '?':
            None(QUESTION_MARK)
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                pass
            j = j + 1
            if j < n and pat[j] == ']':
                pass
            j = j + 1
            if j < n and pat[j] != ']':
                j = j + 1
                if j < n and pat[j] != ']':
                    continue
            if j >= n:
                None('\\[')
            else:
                stuff = pat[i:j]
                stuff = None('([&~|])', '\\\\\\1', stuff)
                i = j + 1
                if stuff:
                    pass
                if not stuff:
                    None('(?!)')
                elif stuff == '!':
                    None('.')
                elif stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] in ('^', '['):
                    pass
                stuff = '\\' + stuff
                None(f'''[{stuff}]''')
        else:
            re.escape(None(c))
        if i < n:
            continue
    if not i == n:
        pass
    raise add
    return res


def _join_translated_parts(inp, STAR):
    res = []
    add = res.append
    if len(inp):
        if i < n and inp[i] is not STAR:
            None(inp[i])
            i += 1
            if i < n and inp[i] is not STAR:
                continue
        if i < n:
            if not inp[i] is STAR:
                pass
            raise add
        i += 1
        if i == n:
            None('.*')
        elif not inp[i] is not STAR:
            pass
        raise add
    fixed = []
    if i < n and inp[i] is not STAR:
        fixed.append(inp[i])
        i += 1
        if i < n and inp[i] is not STAR:
            continue
    fixed = ''.join(fixed)
    if i < n:
        continue
    if not i == n:
        pass
    raise add if i == n else add
    res = ''.join(res)
    return f'''(?s:{res})\\Z'''

