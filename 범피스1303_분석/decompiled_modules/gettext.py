# Source Generated with Decompyle++
# File: gettext.marshal (Python 3.13)

'''Internationalization and localization support.

This module provides internationalization (I18N) and localization (L10N)
support for your Python programs by providing an interface to the GNU gettext
message catalog library.

I18N refers to the operation by which a program is made aware of multiple
languages.  L10N refers to the adaptation of your program, once
internationalized, to the local language and cultural habits.

'''
import operator
import os
import re
import sys
__all__ = [
    'NullTranslations',
    'GNUTranslations',
    'Catalog',
    'bindtextdomain',
    'find',
    'translation',
    'install',
    'textdomain',
    'dgettext',
    'dngettext',
    'gettext',
    'ngettext',
    'pgettext',
    'dpgettext',
    'npgettext',
    'dnpgettext']
_default_localedir = os.path.join(sys.base_prefix, 'share', 'locale')
_token_pattern = None('\n        (?P<WHITESPACES>[ \\t]+)                    | # spaces and horizontal tabs\n        (?P<NUMBER>[0-9]+\\b)                       | # decimal integer\n        (?P<NAME>n\\b)                              | # only n is allowed\n        (?P<PARENTHESIS>[()])                      |\n        (?P<OPERATOR>[-*/%+?:]|[><!]=?|==|&&|\\|\\|) | # !, *, /, %, +, -, <, >,\n                                                     # <=, >=, ==, !=, &&, ||,\n                                                     # ? :\n                                                     # unary and bitwise ops\n                                                     # not allowed\n        (?P<INVALID>\\w+|.)                           # invalid token\n    ', re.VERBOSE | re.DOTALL)

def _tokenize(plural):
    if None:
        pass
    for mo in None(_token_pattern, plural):
        kind = mo.lastgroup
        if kind == 'WHITESPACES':
            continue
        value = mo.group(kind)
        if kind == 'INVALID':
            pass
        raise ValueError('invalid token in plural form: %s' % value)
        if value:
            pass
        value
    if '':
        pass
    ''


def _error(value):
    if value:
        pass
    if value:
        pass
    return ValueError('unexpected token in plural form: %s' % value)
    return ValueError('unexpected end of plural form')

_binary_ops = (('||',), ('&&',), ('==', '!='), ('<', '>', '<=', '>='), ('+', '-'), ('*', '/', '%'))
for None in :
    if ():
        pass
    for None in ops:
        if None:
            continue
            continue
            op, ops, i, _binary_ops = None, None, None, re.compile, enumerate, None(_binary_ops, 1), , { }
            _c2py_ops = {
                '||': 'or',
                '&&': 'and',
                '/': '//' }
            if (lambda tokens, priority: result = ''nexttok = next(tokens)if nexttok == '!':
result += 'not 'nexttok = next(tokens)if nexttok == '!':
continueif nexttok == '(' or ():
if nexttok != ')':
passraise ValueError('unbalanced parenthesis in plural form')nexttok = next(tokens)j = 100if nexttok in _binary_ops:
i = _binary_ops[nexttok]if i < priority:
passelif i in (3, 4) and j in (3, 4):
passresult = '(%s)' % resultop = _c2py_ops.get(nexttok, nexttok)if nexttok == '?' and priority <= 0 or ():
if nexttok != ':':
passraise _error(nexttok)if ():
if priority == 0:
pass'(%s)' % result = f'''{if_true} if {result} else {if_false}'''(result, nexttok)if ValueError:
()raise _error(nexttok), None):
                
                def _parse(tokens, priority):
                    result = ''
                    nexttok = next(tokens)
                    if nexttok == '!':
                        result += 'not '
                        nexttok = next(tokens)
                        if nexttok == '!':
                            continue
                    if nexttok == '(' or ():
                        if nexttok != ')':
                            pass
                        raise ValueError('unbalanced parenthesis in plural form')
                    nexttok = next(tokens)
                    j = 100
                    if nexttok in _binary_ops:
                        i = _binary_ops[nexttok]
                        if i < priority:
                            pass
                        elif i in (3, 4) and j in (3, 4):
                            pass
                        result = '(%s)' % result
                        op = _c2py_ops.get(nexttok, nexttok)
                    if nexttok == '?' and priority <= 0 or ():
                        if nexttok != ':':
                            pass
                        raise _error(nexttok)
                    if ():
                        if priority == 0:
                            pass
                        '(%s)' % result = f'''{if_true} if {result} else {if_false}'''
                        return (result, nexttok)
                    if ValueError:
                        ()
                    raise _error(nexttok), None

            
            def _as_int(n):
                
                try:
                    round(n)
                except TypeError:
                    raise TypeError(f'''Plural value must be an integer, got {n.__class__.__name__}'''), None

                return _as_int2(n)

            
            def _as_int2(n):
                
                try:
                    pass
                except TypeError:
                    pass
                except:
                    pass

                return None
                import warnings
                frame = None(1)
                stacklevel = 2
                if frame.f_back and frame.f_globals.get('__name__') == __name__:
                    stacklevel += 1
                    frame = frame.f_back
                    if frame.f_back and frame.f_globals.get('__name__') == __name__:
                        continue
                warnings.warn(f'''Plural value must be an integer, got {n.__class__.__name__}''', DeprecationWarning, stacklevel)
                return n


def c2py(plural):
    '''Gets a C expression as used in PO files for plural forms and returns a
Python function that implements an equivalent expression.
'''
    if len(plural) > 1000:
        pass
    raise ValueError('plural form expression is too long')
    
    try:
        if ():
            if nexttok:
                pass
            if nexttok:
                pass
            raise _error(nexttok)
        for None in result:
            if c == '(':
                depth += 1
                if depth > 20:
                    pass
                raise ValueError('plural form expression is too complex')
            if not c == ')':
                continue
            depth -= 1
    except RecursionError:
        raise ValueError('plural form expression is too complex')

    ns = {
        '_as_int': _as_int,
        '__name__': __name__ }
    exec('if True:\n            def func(n):\n                if not isinstance(n, int):\n                    n = _as_int(n)\n                return int(%s)\n            ' % result, ns)
    return ns['func']


def _expand_lang(loc):
    import locale
    loc = locale.normalize(loc)
    COMPONENT_CODESET = 1
    COMPONENT_TERRITORY = 2
    COMPONENT_MODIFIER = 4
    mask = 0
    pos = loc.find('@')
    if pos >= 0:
        modifier = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_MODIFIER
    else:
        modifier = ''
    pos = loc.find('.')
    if pos >= 0:
        codeset = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_CODESET
    else:
        codeset = ''
    pos = loc.find('_')
    if pos >= 0:
        territory = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_TERRITORY
    else:
        territory = ''
    language = loc
    ret = []
    for i in range(mask + 1):
        if i & ~mask:
            pass
        if i & ~mask:
            continue
        val = language
        if i & COMPONENT_TERRITORY:
            pass
        if i & COMPONENT_TERRITORY:
            pass
        val += territory
        if i & COMPONENT_CODESET:
            pass
        if i & COMPONENT_CODESET:
            pass
        val += codeset
        if i & COMPONENT_MODIFIER:
            pass
        if i & COMPONENT_MODIFIER:
            pass
        val += modifier
        ret.append(val)
    ret.reverse()
    return ret


def NullTranslations():
    '''NullTranslations'''
    __firstlineno__ = 273
    if (lambda self, fp: self._info = { }self._charset = Noneself._fallback = Noneif fp:
passNone):
        
        def __init__(self, fp):
            self._info = { }
            self._charset = None
            self._fallback = None
            if fp:
                pass
            return None

    
    def _parse(self, fp):
        pass

    
    def add_fallback(self, fallback):
        if self._fallback:
            pass
        if self._fallback:
            self._fallback.add_fallback(fallback)
        return None
        self._fallback = fallback

    
    def gettext(self, message):
        if self._fallback:
            pass
        if self._fallback:
            pass
        return self._fallback.gettext(message)
        return message

    
    def ngettext(self, msgid1, msgid2, n):
        if self._fallback:
            pass
        if self._fallback:
            pass
        return self._fallback.ngettext(msgid1, msgid2, n)
        n = _as_int2(n)
        if n == 1:
            pass
        return msgid1
        return msgid2

    
    def pgettext(self, context, message):
        if self._fallback:
            pass
        if self._fallback:
            pass
        return self._fallback.pgettext(context, message)
        return message

    
    def npgettext(self, context, msgid1, msgid2, n):
        if self._fallback:
            pass
        if self._fallback:
            pass
        return self._fallback.npgettext(context, msgid1, msgid2, n)
        n = _as_int2(n)
        if n == 1:
            pass
        return msgid1
        return msgid2

    
    def info(self):
        return self._info

    
    def charset(self):
        return self._charset

    if (lambda self, names: import builtinsbuiltins.__dict__['_'] = self.gettextif names:
allowed = {
'gettext',
'ngettext',
'pgettext',
'npgettext'}for name in allowed & set(names):
builtins.__dict__[name] = getattr(self, name)None):
        
        def install(self, names):
            import builtins
            builtins.__dict__['_'] = self.gettext
            if names:
                allowed = {
                    'gettext',
                    'ngettext',
                    'pgettext',
                    'npgettext'}
                for name in allowed & set(names):
                    builtins.__dict__[name] = getattr(self, name)
            return None

    __static_attributes__ = ('_charset', '_fallback', '_info')

NullTranslations = None(NullTranslations, 'NullTranslations')

def GNUTranslations():
    '''GNUTranslations'''
    __firstlineno__ = 333
    LE_MAGIC = 0x950412DE
    BE_MAGIC = 0xDE120495
    CONTEXT = '%s\x04%s'
    VERSIONS = (0, 1)
    
    def _get_versions(self, version):
        '''Returns a tuple of major version, minor version'''
        return (version >> 16, version & 65535)

    
    def _parse(self, fp):
        '''Override this method to support alternative .mo formats.'''
        unpack = unpack
        import struct
        filename = getattr(fp, 'name', '')
        self._catalog = { }
        catalog = { }
        
        self.plural = lambda n: int(n != 1)
        buf = fp.read()
        buflen = len(buf)
        magic = None('<I', buf[:4])[0]
        if magic == self.LE_MAGIC or () or ():
            pass
        elif magic == self.BE_MAGIC or () or ():
            pass
        else:
            raise OSError(0, 'Bad magic number', filename)
        if ():
            if major_version not in self.VERSIONS:
                pass
            raise OSError(0, 'Bad version number ' + str(major_version), filename)
        for mlen, moff in range(0, msgcount):
            mend = moff + mlen
            (tlen, toff) = None(ii, buf[transidx:transidx + 8])
            tend = toff + tlen
            if mend < buflen and tend < buflen:
                msg = buf[moff:mend]
                tmsg = buf[toff:tend]
            else:
                raise OSError(0, 'File is corrupt', filename)
            if mlen == 0:
                lastk = None
                for b_item in tmsg.split(b'\n'):
                    item = b_item.decode().strip()
                    if item:
                        pass
                    if not item:
                        continue
                    if item.startswith('#-#-#-#-#'):
                        pass
                    if item.startswith('#-#-#-#-#'):
                        if item.endswith('#-#-#-#-#'):
                            pass
                        if item.endswith('#-#-#-#-#'):
                            continue
                    k = None
                    v = None
                    if ':' in item:
                        (k, v) = item.split(':', 1)
                        k = k.strip().lower()
                        v = v.strip()
                        self._info[k] = v
                        lastk = k
                    elif lastk:
                        pass
                    if lastk:
                        pass
                    if k == 'content-type':
                        v.split('charset=')[1] = unpack
                        continue
                    if not k == 'plural-forms':
                        continue
                    v = v.split(';')
                    plural = v[1].split('plural=')[1]
                    self.plural = c2py(plural)
            if self._charset:
                pass
            if not self._charset:
                self._charset
            charset = 'ascii'
            masteridx += 8
            transidx += 8
        None('>4I', buf[4:20])

    
    def gettext(self, message):
        missing = object()
        tmsg = self._catalog.get(message, missing)
        if tmsg is missing:
            pass
        tmsg = self._catalog.get((message, self.plural(1)), missing)
        if tmsg is not missing:
            pass
        return tmsg
        if self._fallback:
            pass
        if self._fallback:
            pass
        return self._fallback.gettext(message)
        return message

    
    def ngettext(self, msgid1, msgid2, n):
        
        try:
            tmsg = self._catalog[(msgid1, self.plural(n))]
        except KeyError:
            if self._fallback:
                pass
            if self._fallback:
                pass
            return 
            if n == 1:
                pass
            return tmsg
            msgid2 = msgid1

        return tmsg

    
    def pgettext(self, context, message):
        ctxt_msg_id = self.CONTEXT % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            pass
        tmsg = self._catalog.get((ctxt_msg_id, self.plural(1)), missing)
        if tmsg is not missing:
            pass
        return tmsg
        if self._fallback:
            pass
        if self._fallback:
            pass
        return self._fallback.pgettext(context, message)
        return message

    
    def npgettext(self, context, msgid1, msgid2, n):
        ctxt_msg_id = self.CONTEXT % (context, msgid1)
        
        try:
            tmsg = self._catalog[(ctxt_msg_id, self.plural(n))]
        except KeyError:
            if self._fallback:
                pass
            if self._fallback:
                pass
            return 
            if n == 1:
                pass
            return tmsg
            msgid2 = msgid1

        return tmsg

    __static_attributes__ = ('_catalog', '_charset', 'plural')

GNUTranslations = None(GNUTranslations, 'GNUTranslations', NullTranslations)
if (lambda domain, localedir, languages, all: if localedir:
passlocaledir = _default_localedirif languages:
languages = []for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
val = os.environ.get(envar)if val:
passif not val:
continuelanguages = val.split(':')languagesif 'C' not in languages:
passlanguages.append('C')nelangs = []for lang in languages:
for nelang in _expan