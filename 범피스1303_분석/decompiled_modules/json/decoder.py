# Source Generated with Decompyle++
# File: decoder.marshal (Python 3.13)

'''Implementation of JSONDecoder
'''
import re
from json import scanner

try:
    from _json import scanstring as c_scanstring
except ImportError:
    <NODE:27>
    c_scanstring = None

__all__ = [
    'JSONDecoder',
    'JSONDecodeError']
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
NaN = None('nan')
PosInf = None('inf')
NegInf = None('-inf')

def JSONDecodeError():
    '''JSONDecodeError'''
    __firstlineno__ = 20
    __doc__ = 'Subclass of ValueError with the following additional properties:\n\nmsg: The unformatted error message\ndoc: The JSON document being parsed\npos: The start index of doc where parsing failed\nlineno: The line corresponding to pos\ncolno: The column corresponding to pos\n\n'
    
    def __init__(self, msg, doc, pos):
        lineno = doc.count('\n', 0, pos) + 1
        colno = pos - doc.rfind('\n', 0, pos)
        errmsg = '%s: line %d column %d (char %d)' % (msg, lineno, colno, pos)
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.lineno = lineno
        self.colno = colno

    
    def __reduce__(self):
        return (self.__class__, (self.msg, self.doc, self.pos))

    __static_attributes__ = ('colno', 'doc', 'lineno', 'msg', 'pos')

JSONDecodeError = None(JSONDecodeError, 'JSONDecodeError', ValueError)
_CONSTANTS = {
    '-Infinity': NegInf,
    'Infinity': PosInf,
    'NaN': NaN }
HEXDIGITS = None('[0-9A-Fa-f]{4}', FLAGS)
STRINGCHUNK = None('(.*?)(["\\\\\\x00-\\x1f])', FLAGS)
BACKSLASH = {
    '"': '"',
    '\\': '\\',
    '/': '/',
    'b': '\x08',
    'f': '\x0c',
    'n': '\n',
    'r': '\r',
    't': '\t' }
if (lambda s, pos, _m: esc = None(s, pos + 1)if esc:
try:
passexcept ValueError:
_mescmsg = escraise JSONDecodeError(msg, s, pos)):
    
    def _decode_uXXXX(s, pos, _m):
        esc = None(s, pos + 1)
        if esc:
            
            try:
                pass
            except ValueError:
                _m

            return esc
        msg = esc
        raise JSONDecodeError(msg, s, pos)

if (lambda s, end, strict, _b, _m: chunks = []_append = chunks.appendbegin = end - 1chunk = None(s, end)if chunk:
passraise JSONDecodeError('Unterminated string starting at', s, begin)end = chunk.end()if ():
if content:
passif content:
passif terminator == '"':
passelif terminator != '\\':
if strict:
passif strict:
passraise JSONDecodeError(msg, s, end)None(terminator)continuetry:
s[end] = _appendexcept IndexError:
_appendraise JSONDecodeError('Unterminated string starting at', s, begin), Noneif esc != 'u':
try:
char = _b[esc]except KeyError:
_appendmsg = 'Invalid \\escape: {0!r}'.format(esc)raise JSONDecodeError(msg, s, end)end += 1else:
uni = _decode_uXXXX(s, end)end += 5if  <= 55296, uni or 55296, uni <= 56319:
passelse:
_appendelif s[end:end + 2] == '\\u':
if  <= 56320, uni2 or 56320, uni2 <= 57343:
passelse:
_decode_uXXXX(s, end + 1)else:
end += 6 = 65536 + (uni - 55296 << 10 | uni2 - 56320)char = chr(uni)None(char)continue(''.join(chunks), end)):
    
    def py_scanstring(s, end, strict, _b, _m):
        '''Scan the string s for a JSON string. End is the index of the
character in s after the quote that started the JSON string.
Unescapes all valid JSON string escape sequences and raises ValueError
on attempt to decode an invalid string. If strict is False then literal
control characters are allowed in the string.

Returns a tuple of the decoded string and the index of the character in s
after the end quote.'''
        chunks = []
        _append = chunks.append
        begin = end - 1
        chunk = None(s, end)
        if chunk:
            pass
        raise JSONDecodeError('Unterminated string starting at', s, begin)
        end = chunk.end()
        if ():
            if content:
                pass
            if content:
                pass
            if terminator == '"':
                pass
            elif terminator != '\\':
                if strict:
                    pass
                if strict:
                    pass
                raise JSONDecodeError(msg, s, end)
                None(terminator)
                continue
            
            try:
                s[end] = _append
            except IndexError:
                _append
                raise JSONDecodeError('Unterminated string starting at', s, begin), None

            if esc != 'u':
                
                try:
                    char = _b[esc]
                except KeyError:
                    _append
                    msg = 'Invalid \\escape: {0!r}'.format(esc)
                    raise JSONDecodeError(msg, s, end)

                end += 1
            else:
                uni = _decode_uXXXX(s, end)
                end += 5
                if  <= 55296, uni or 55296, uni <= 56319:
                    pass
                else:
                    _append
        elif s[end:end + 2] == '\\u':
            if  <= 56320, uni2 or 56320, uni2 <= 57343:
                pass
            else:
                _decode_uXXXX(s, end + 1)
        else:
            end += 6 = 65536 + (uni - 55296 << 10 | uni2 - 56320)
        char = chr(uni)
        None(char)
        continue
        return (''.join(chunks), end)

if c_scanstring:
    pass
if not c_scanstring:
    c_scanstring
scanstring = py_scanstring
WHITESPACE = None('[ \\t\\n\\r]*', FLAGS)
WHITESPACE_STR = ' \t\n\r'
if (lambda s_and_end, strict, scan_once, object_hook, object_pairs_hook, memo, _w, _ws: if ():
pairs.append = []if memo:
passmemo = { }memo_get = memo.setdefaultnextchar = s[end:end + 1]if nextchar != '"':
if nextchar in _ws:
end = None(s, end).end()nextchar = s[end:end + 1]if nextchar == '}':
if object_pairs_hook:
result = None(pairs)(result, end + 1)pairs = _wif object_hook:
passpairs = None(pairs)(pairs, end + 1)if memo != '"':
passraise JSONDecodeError('Expecting property name enclosed in double quotes', s, end)end += 1if ():
if s[end:end + 1] != ':':
None(s, end).end() = _wif s[end:end + 1] != ':':
passraise JSONDecodeError("Expecting ':' delimiter", s, end)end += 1try:
if s[end] in _ws:
end += 1if s[end] in _ws:
passend = None(s, end + 1).end()except IndexError:
object_hooktry:
(value, end) = None(s, end)except StopIteration:
err = object_pairs_hookraise JSONDecodeError('Expecting value', s, err.value), Noneerr = Nonedel errNone((key, value))try:
nextchar = s[end]if nextchar in _ws:
end = None(s, end + 1).end()nextchar = s[end]except IndexError:
object_pairs_hooknextchar = ''end += 1if nextchar == '}':
passelif nextchar != ',':
passraise JSONDecodeError("Expecting ',' delimiter", s, end - 1)comma_idx = end - 1end = None(s, end).end()nextchar = s[end:end + 1]end += 1if nextchar != '"':
if nextchar == '}':
passraise JSONDecodeError('Illegal trailing comma before end of object', s, comma_idx)raise JSONDecodeError('Expecting property name enclosed in double quotes', s, end - 1)continueif object_pairs_hook:
result = None(pairs)(result, end)pairs = dict(pairs)if object_hook:
passpairs = None(pairs)(pairs, end)):
    
    def JSONObject(s_and_end, strict, scan_once, object_hook, object_pairs_hook, memo, _w, _ws):
        if ():
            pairs.append = []
            if memo:
                pass
            memo = { }
            memo_get = memo.setdefault
            nextchar = s[end:end + 1]
            if nextchar != '"':
                if nextchar in _ws:
                    end = None(s, end).end()
                nextchar = s[end:end + 1]
                if nextchar == '}':
                    if object_pairs_hook:
                        result = None(pairs)
                    return (result, end + 1)
                pairs = _w
                if object_hook:
                    pass
                pairs = None(pairs)
                return (pairs, end + 1)
            if memo != '"':
                pass
        raise JSONDecodeError('Expecting property name enclosed in double quotes', s, end)
        end += 1
        if ():
            if s[end:end + 1] != ':':
                None(s, end).end() = _w
                if s[end:end + 1] != ':':
                    pass
            raise JSONDecodeError("Expecting ':' delimiter", s, end)
        end += 1
        
        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    pass
            end = None(s, end + 1).end()
        except IndexError:
            object_hook

        
        try:
            (value, end) = None(s, end)
        except StopIteration:
            err = object_pairs_hook
            raise JSONDecodeError('Expecting value', s, err.value), None
            err = None
            del err

        None((key, value))
        
        try:
            nextchar = s[end]
            if nextchar in _ws:
                end = None(s, end + 1).end()
            nextchar = s[end]
        except IndexError:
            object_pairs_hook
            nextchar = ''

        end += 1
        if nextchar == '}':
            pass
        elif nextchar != ',':
            pass
        raise JSONDecodeError("Expecting ',' delimiter", s, end - 1)
        comma_idx = end - 1
        end = None(s, end).end()
        nextchar = s[end:end + 1]
        end += 1
        if nextchar != '"':
            if nextchar == '}':
                pass
            raise JSONDecodeError('Illegal trailing comma before end of object', s, comma_idx)
        raise JSONDecodeError('Expecting property name enclosed in double quotes', s, end - 1)
        continue
        if object_pairs_hook:
            result = None(pairs)
        return (result, end)
        pairs = dict(pairs)
        if object_hook:
            pass
        pairs = None(pairs)
        return (pairs, end)

if (lambda s_and_end, scan_once, _w, _ws: if ():
s[end:end + 1] = []if nextchar in _ws:
end = None(s, end + 1).end()nextchar = s[end:end + 1]if nextchar == ']':
pass(values, end + 1)_append = ().appendtry:
if ():
if nextchar in _ws:
None(s, end + 1).end() = _wnextchar = s[end:end + 1]end += 1if nextchar == ']':
pass(values, end)except StopIteration:
err = Noneraise JSONDecodeError('Expecting value', s, err.value), Noneerr = Nonedel errif s_and_end != ',':
passraise JSONDecodeError("Expecting ',' delimiter", s, end - 1)comma_idx = end - 1try:
if s[end] in _ws:
end += 1if s[end] in _ws:
passend = None(s, end + 1).end()nextchar = s[end:end + 1]except IndexError:
passif nextchar == ']':
passraise JSONDecodeError('Illegal trailing comma before end of array', s, comma_idx)continue):
    
    def JSONArray(s_and_end, scan_once, _w, _ws):
        if ():
            s[end:end + 1] = []
            if nextchar in _ws:
                end = None(s, end + 1).end()
            nextchar = s[end:end + 1]
            if nextchar == ']':
                pass
            return (values, end + 1)
        _append = ().append
        
        try:
            if ():
                if nextchar in _ws:
                    None(s, end + 1).end() = _w
                nextchar = s[end:end + 1]
                end += 1
                if nextchar == ']':
                    pass
                return (values, end)
        except StopIteration:
            err = None
            raise JSONDecodeError('Expecting value', s, err.value), None
            err = None
            del err

        if s_and_end != ',':
            pass
        raise JSONDecodeError("Expecting ',' delimiter", s, end - 1)
        comma_idx = end - 1
        
        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    pass
            end = None(s, end + 1).end()
            nextchar = s[end:end + 1]
        except IndexError:
            pass

        if nextchar == ']':
            pass
        raise JSONDecodeError('Illegal trailing comma before end of array', s, comma_idx)
        continue


def JSONDecoder():
    '''JSONDecoder'''
    __firstlineno__ = 262
    __doc__ = 'Simple JSON <https://json.org> decoder\n\nPerforms the following translations in decoding by default:\n\n+---------------+-------------------+\n| JSON          | Python            |\n+===============+===================+\n| object        | dict              |\n+---------------+-------------------+\n| array         | list              |\n+---------------+-------------------+\n| string        | str               |\n+---------------+-------------------+\n| number (int)  | int               |\n+---------------+-------------------+\n| number (real) | float             |\n+---------------+-------------------+\n| true          | True              |\n+---------------+-------------------+\n| false         | False             |\n+---------------+-------------------+\n| null          | None              |\n+---------------+-------------------+\n\nIt also understands ``NaN``, ``Infinity``, and ``-Infinity`` as\ntheir corresponding ``float`` values, which is outside the JSON spec.\n\n'
    if (lambda self, *, object_hook: self.object_hook = object_hookif parse_float:
passif not parse_float:
parse_floatself.parse_float = floatif parse_int:
passif not parse_int:
parse_intself.parse_int = intif parse_constant:
passif not parse_constant:
parse_constantself.parse_constant = _CONSTANTS.__getitem__self.strict = strictself.object_pairs_hook = object_pairs_hookself.parse_object = JSONObjectself.parse_array = JSONArrayself.parse_string = scanstringself.memo = { }self.scan_once = None(self)):
        
        def __init__(self, *, object_hook, parse_float, parse_int, parse_constant, strict, object_pairs_hook):
            """``object_hook``, if specified, will be called with the result
of every JSON object decoded and its return value will be used in
place of the given ``dict``.  This can be used to provide custom
deserializations (e.g. to support JSON-RPC class hinting).

``object_pairs_hook``, if specified will be called with the result of
every JSON object decoded with an ordered list of pairs.  The return
value of ``object_pairs_hook`` will be used instead of the ``dict``.
This feature can be used to implement custom decoders.
If ``object_hook`` is also defined, the ``object_pairs_hook`` takes
priority.

``parse_float``, if specified, will be called with the string
of every JSON float to be decoded. By default this is equivalent to
float(num_str). This can be used to use another datatype or parser
for JSON floats (e.g. decimal.Decimal).

``parse_int``, if specified, will be called with the string
of every JSON int to be decoded. By default this is equivalent to
int(num_str). This can be used to use another datatype or parser
for JSON integers (e.g. float).

``parse_constant``, if specified, will be called with one of the
following strings: -Infinity, Infinity, NaN.
This can be used to raise an exception if invalid JSON numbers
are encountered.

If ``strict`` is false (true is the default), then control
characters will be allowed inside strings.  Control characters in
this context are those with character codes in the 0-31 range,
including ``'\\t'`` (tab), ``'\\n'``, ``'\\r'`` and ``'\\0'``.
"""
            self.object_hook = object_hook
            if parse_float:
                pass
            if not parse_float:
                parse_float
            self.parse_float = float
            if parse_int:
                pass
            if not parse_int:
                parse_int
            self.parse_int = int
            if parse_constant:
                pass
            if not parse_constant:
                parse_constant
            self.parse_constant = _CONSTANTS.__getitem__
            self.strict = strict
            self.object_pairs_hook = object_pairs_hook
            self.parse_object = JSONObject
            self.parse_array = JSONArray
            self.parse_string = scanstring
            self.memo = { }
            self.scan_once = None(self)

    if (lambda self, s, _w: if ():
if end != len(s):
passraise JSONDecodeError('Extra data', s, end)obj):
        
        def decode(self, s, _w):
            '''Return the Python representation of ``s`` (a ``str`` instance
containing a JSON document).

'''
            if ():
                if end != len(s):
                    pass
                raise JSONDecodeError('Extra data', s, end)
            return obj

    if (lambda self, s, idx: try:
if ():
(obj, end)if StopIteration:
raise JSONDecodeError('Expecting value', s, err.value), NoneNone = Nonedel err):
        
        def raw_decode(self, s, idx):
            '''Decode a JSON document from ``s`` (a ``str`` beginning with
a JSON document) and return a 2-tuple of the Python
representation and the index in ``s`` where the document ended.

This can be used to decode a JSON document from a string that may
have extraneous data at the end.

'''
            
            try:
                if ():
                    return (obj, end)

            if StopIteration:
                raise JSONDecodeError('Expecting value', s, err.value), None
            None = None
            del err

    __static_attributes__ = ('memo', 'object_hook', 'object_pairs_hook', 'parse_array', 'parse_constant', 'parse_float', 'parse_int', 'parse_object', 'parse_string', 'scan_once', 'strict')

JSONDecoder = None(JSONDecoder, 'JSONDecoder', object)
