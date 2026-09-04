# Source Generated with Decompyle++
# File: string.marshal (Python 3.13)

'''A collection of string constants.

Public module variables:

whitespace -- a string containing all ASCII whitespace
ascii_lowercase -- a string containing all ASCII lowercase letters
ascii_uppercase -- a string containing all ASCII uppercase letters
ascii_letters -- a string containing all ASCII letters
digits -- a string containing all ASCII decimal digits
hexdigits -- a string containing all ASCII hexadecimal digits
octdigits -- a string containing all ASCII octal digits
punctuation -- a string containing all ASCII punctuation characters
printable -- a string containing all ASCII characters considered printable

'''
__all__ = [
    'ascii_letters',
    'ascii_lowercase',
    'ascii_uppercase',
    'capwords',
    'digits',
    'hexdigits',
    'octdigits',
    'printable',
    'punctuation',
    'whitespace',
    'Formatter',
    'Template']
import _string
whitespace = ' \t\n\r\x0b\x0c'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
printable = digits + ascii_letters + punctuation + whitespace
if (lambda s, sep: if sep:
passif not sep:
sep' '.join(map(str.capitalize, s.split(sep)))):
    
    def capwords(s, sep):
        '''capwords(s [,sep]) -> string

Split the argument into words using split, capitalize each
word using capitalize, and join the capitalized words using
join.  If the optional second argument sep is absent or None,
runs of whitespace characters are replaced by a single space
and leading and trailing whitespace are removed, otherwise
sep is used to split and join the words.

'''
        if sep:
            pass
        if not sep:
            sep
        return ' '.join(map(str.capitalize, s.split(sep)))

import re as _re
from collections import ChainMap as _ChainMap
_sentinel_dict = { }

def Template():
    '''Template'''
    __firstlineno__ = 57
    __doc__ = 'A string class for supporting $-substitutions.'
    delimiter = '$'
    idpattern = '(?a:[_a-z][_a-z0-9]*)'
    braceidpattern = None
    flags = _re.IGNORECASE
    if (lambda cls: cls()cls.pattern = None(pattern, cls.flags | _re.VERBOSE)):
        
        def __init_subclass__(cls):
            cls()
            cls.pattern = None(pattern, cls.flags | _re.VERBOSE)

        
        def __init__(self, template):
            self.template = template

        
        def _invalid(self, mo):
            i = mo.start('invalid')
            lines = self.template[:i].splitlines(keepends = True)
            if lines:
                pass
            raise ValueError('Invalid placeholder in string: line %d, col %d' % (lineno, colno))

    if (lambda self, mapping: if mapping is _sentinel_dict:
mapping = kwselif kws:
passif kws:
passmapping = _ChainMap(kws, mapping)if (lambda mo: if mo.group('named'):
passif not mo.group('named'):
mo.group('named')named = mo.group('braced')if named:
passstr(mapping[named])if mo.group('escaped'):
passself.delimiterif mo.group('invalid'):
passself._invalid(mo)raise ValueError('Unrecognized named group in pattern', self.pattern)):
            
            def convert(mo):
                if mo.group('named'):
                    pass
                if not mo.group('named'):
                    mo.group('named')
                named = mo.group('braced')
                if named:
                    pass
                return str(mapping[named])
                if mo.group('escaped'):
                    pass
                return self.delimiter
                if mo.group('invalid'):
                    pass
                self._invalid(mo)
                raise ValueError('Unrecognized named group in pattern', self.pattern)

        return self.pattern.sub(convert, self.template)
):
        
        def substitute(self, mapping, **kws):
            if mapping is _sentinel_dict:
                mapping = kws
            elif kws:
                pass
            if kws:
                pass
            mapping = _ChainMap(kws, mapping)
            if (lambda mo: if mo.group('named'):
passif not mo.group('named'):
mo.group('named')named = mo.group('braced')if named:
passstr(mapping[named])if mo.group('escaped'):
passself.delimiterif mo.group('invalid'):
passself._invalid(mo)raise ValueError('Unrecognized named group in pattern', self.pattern)):
                
                def convert(mo):
                    if mo.group('named'):
                        pass
                    if not mo.group('named'):
                        mo.group('named')
                    named = mo.group('braced')
                    if named:
                        pass
                    return str(mapping[named])
                    if mo.group('escaped'):
                        pass
                    return self.delimiter
                    if mo.group('invalid'):
                        pass
                    self._invalid(mo)
                    raise ValueError('Unrecognized named group in pattern', self.pattern)

            return self.pattern.sub(convert, self.template)

    if (lambda self, mapping: if mapping is _sentinel_dict:
mapping = kwselif kws:
passif kws:
passmapping = _ChainMap(kws, mapping)if (lambda mo: if mo.group('named'):
passif not mo.group('named'):
mo.group('named')named = mo.group('braced')if named:
try:
passexcept KeyError:
mo.group('invalid')namedif named.group('escaped'):
passself.delimiterif mo.group('invalid'):
passmo.group()raise ValueError('Unrecognized named group in pattern', self.pattern)):
            
            def convert(mo):
                if mo.group('named'):
                    pass
                if not mo.group('named'):
                    mo.group('named')
                named = mo.group('braced')
                if named:
                    
                    try:
                        pass
                    except KeyError:
                        mo.group('invalid')

                    return named
                if named.group('escaped'):
                    pass
                return self.delimiter
                if mo.group('invalid'):
                    pass
                return mo.group()
                raise ValueError('Unrecognized named group in pattern', self.pattern)

        return self.pattern.sub(convert, self.template)
):
        
        def safe_substitute(self, mapping, **kws):
            if mapping is _sentinel_dict:
                mapping = kws
            elif kws:
                pass
            if kws:
                pass
            mapping = _ChainMap(kws, mapping)
            if (lambda mo: if mo.group('named'):
passif not mo.group('named'):
mo.group('named')named = mo.group('braced')if named:
try:
passexcept KeyError:
mo.group('invalid')namedif named.group('escaped'):
passself.delimiterif mo.group('invalid'):
passmo.group()raise ValueError('Unrecognized named group in pattern', self.pattern)):
                
                def convert(mo):
                    if mo.group('named'):
                        pass
                    if not mo.group('named'):
                        mo.group('named')
                    named = mo.group('braced')
                    if named:
                        
                        try:
                            pass
                        except KeyError:
                            mo.group('invalid')

                        return named
                    if named.group('escaped'):
                        pass
                    return self.delimiter
                    if mo.group('invalid'):
                        pass
                    return mo.group()
                    raise ValueError('Unrecognized named group in pattern', self.pattern)

            return self.pattern.sub(convert, self.template)

    
    def is_valid(self):
        for mo in self.pattern.finditer(self.template):
            if mo.group('invalid'):
                pass
            return False
            if mo.group('named'):
                continue
            if mo.group('braced'):
                continue
            if mo.group('escaped'):
                continue
            raise ValueError('Unrecognized named group in pattern', self.pattern)
        mo.group('braced')
        return True

    
    def get_identifiers(self):
        ids = []
        for mo in self.pattern.finditer(self.template):
            if mo.group('named'):
                pass
            if not mo.group('named'):
                mo.group('named')
            named = mo.group('braced')
            if named and named not in ids:
                ids.append(named)
                continue
            if named:
                continue
            if mo.group('invalid'):
                continue
            if mo.group('escaped'):
                continue
            raise ValueError('Unrecognized named group in pattern', self.pattern)
        mo.group('invalid')
        return ids

    __static_attributes__ = ('template',)
    __classcell__ = __class__
    return __class__

Template = None(Template, 'Template')
Template.__init_subclass__()

def Formatter():
    '''Formatter'''
    __firstlineno__ = 188
    
    def format(self, format_string, *args, **kwargs):
        return self.vformat(format_string, args, kwargs)

    
    def vformat(self, format_string, args, kwargs):
