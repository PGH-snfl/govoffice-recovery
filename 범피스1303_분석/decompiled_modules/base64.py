# Source Generated with Decompyle++
# File: base64.marshal (Python 3.13)

'''Base16, Base32, Base64 (RFC 3548), Base85 and Ascii85 data encodings'''
import re
import struct
import binascii
__all__ = [
    'encode',
    'decode',
    'encodebytes',
    'decodebytes',
    'b64encode',
    'b64decode',
    'b32encode',
    'b32decode',
    'b32hexencode',
    'b32hexdecode',
    'b16encode',
    'b16decode',
    'b85encode',
    'b85decode',
    'a85encode',
    'a85decode',
    'z85encode',
    'z85decode',
    'standard_b64encode',
    'standard_b64decode',
    'urlsafe_b64encode',
    'urlsafe_b64decode']
bytes_types = (bytes, bytearray)

def _bytes_from_decode_data(s):
    if isinstance(s, str):
        pass
    if isinstance(s, str):
        
        try:
            pass
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')

        return None
    if None(s, bytes_types):
        pass
    if None(s, bytes_types):
        pass
    return s
    
    try:
        pass
    except TypeError:
        raise TypeError('argument should be a bytes-like object or ASCII string, not %r' % s.__class__.__name__), None


if (lambda s, altchars: encoded = None(s, newline = False)if altchars:
if not len(altchars) == 2:
passraise repr(altchars)()encoded.translate(bytes.maketrans(b'+/', altchars))encoded):
    
    def b64encode(s, altchars):
        """Encode the bytes-like object s using Base64 and return a bytes object.

Optional altchars should be a byte string of length 2 which specifies an
alternative alphabet for the '+' and '/' characters.  This allows an
application to e.g. generate url or filesystem safe Base64 strings.
"""
        encoded = None(s, newline = False)
        if altchars:
            if not len(altchars) == 2:
                pass
            raise repr(altchars)()
        return encoded.translate(bytes.maketrans(b'+/', altchars))
        return encoded

if (lambda s, altchars, validate: s = _bytes_from_decode_data(s)if altchars:
altchars = _bytes_from_decode_data(altchars)if not len(altchars) == 2:
passraise repr(altchars)()s = s.translate(bytes.maketrans(altchars, b'+/'))None(s, strict_mode = validate)):
    
    def b64decode(s, altchars, validate):
        """Decode the Base64 encoded bytes-like object or ASCII string s.

Optional altchars must be a bytes-like object or ASCII string of length 2
which specifies the alternative alphabet used instead of the '+' and '/'
characters.

The result is returned as a bytes object.  A binascii.Error is raised if
s is incorrectly padded.

If validate is False (the default), characters that are neither in the
normal base-64 alphabet nor the alternative alphabet are discarded prior
to the padding check.  If validate is True, these non-alphabet characters
in the input result in a binascii.Error.
For more information about the strict base64 check, see:

https://docs.python.org/3.11/library/binascii.html#binascii.a2b_base64
"""
        s = _bytes_from_decode_data(s)
        if altchars:
            altchars = _bytes_from_decode_data(altchars)
            if not len(altchars) == 2:
                pass
            raise repr(altchars)()
        s = s.translate(bytes.maketrans(altchars, b'+/'))
        return None(s, strict_mode = validate)


def standard_b64encode(s):
    '''Encode bytes-like object s using the standard Base64 alphabet.

The result is returned as a bytes object.
'''
    return b64encode(s)


def standard_b64decode(s):
    '''Decode bytes encoded with the standard Base64 alphabet.

Argument s is a bytes-like object or ASCII string to decode.  The result
is returned as a bytes object.  A binascii.Error is raised if the input
is incorrectly padded.  Characters that are not in the standard alphabet
are discarded prior to the padding check.
'''
    return b64decode(s)

_urlsafe_encode_translation = bytes.maketrans(b'+/', b'-_')
_urlsafe_decode_translation = bytes.maketrans(b'-_', b'+/')

def urlsafe_b64encode(s):
    """Encode bytes using the URL- and filesystem-safe Base64 alphabet.

Argument s is a bytes-like object to encode.  The result is returned as a
bytes object.  The alphabet uses '-' instead of '+' and '_' instead of
'/'.
"""
    return b64encode(s).translate(_urlsafe_encode_translation)


def urlsafe_b64decode(s):
    """Decode bytes using the URL- and filesystem-safe Base64 alphabet.

Argument s is a bytes-like object or ASCII string to decode.  The result
is returned as a bytes object.  A binascii.Error is raised if the input
is incorrectly padded.  Characters that are not in the URL-safe base-64
alphabet, and are not a plus '+' or slash '/', are discarded prior to the
padding check.

The alphabet uses '-' instead of '+' and '_' instead of '/'.
"""
    s = _bytes_from_decode_data(s)
    s = s.translate(_urlsafe_decode_translation)
    return b64decode(s)

_B32_ENCODE_DOCSTRING = '\nEncode the bytes-like objects using {encoding} and return a bytes object.\n'
_B32_DECODE_DOCSTRING = '\nDecode the {encoding} encoded bytes-like object or ASCII string s.\n\nOptional casefold is a flag specifying whether a lowercase alphabet is\nacceptable as input.  For security purposes, the default is False.\n{extra_args}\nThe result is returned as a bytes object.  A binascii.Error is raised if\nthe input is incorrectly padded or if there are non-alphabet\ncharacters present in the input.\n'
_B32_DECODE_MAP01_DOCSTRING = '\nRFC 3548 allows for optional mapping of the digit 0 (zero) to the\nletter O (oh), and for optional mapping of the digit 1 (one) to\neither the letter I (eye) or letter L (el).  The optional argument\nmap01 when not None, specifies which letter the digit 1 should be\nmapped to (when map01 is not None, the digit 0 is always mapped to\nthe letter O).  For security purposes the default is None, so that\n0 and 1 are not allowed in the input.\n'
_b32alphabet = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
_b32hexalphabet = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
_b32tab2 = { }
_b32rev = { }

def _b32encode(alphabet, s):
    if alphabet not in _b32tab2:
        for None in :
            pass
        , [], b32tab = None, alphabet
        i = None
        for None in :
            if None:
                for None in None:
                    if None:
                        continue
                        continue
                        b, a, _b32tab2[alphabet] = None, None, None
                        b32tab = None
                        if isinstance(s, bytes_types):
                            pass
                        if not isinstance(s, bytes_types):
                            pass
                        s = memoryview(s).tobytes()
    leftover = len(s) % 5
    if leftover:
        pass
    if leftover:
        pass
    s = s + b'\x00' * (5 - leftover)
    encoded = bytearray()
    from_bytes = int.from_bytes
    b32tab2 = _b32tab2[alphabet]
    for i in range(0, len(s), 5):
        c = None(s[i:i + 5])
        encoded += b32tab2[c >> 30] + b32tab2[c >> 20 & 1023] + b32tab2[c >> 10 & 1023] + b32tab2[c & 1023]
    if leftover == 1:
        encoded[-6:] = b'======'
    elif leftover == 2:
        encoded[-4:] = b'===='
    elif leftover == 3:
        encoded[-3:] = b'==='
    elif leftover == 4:
        pass
    encoded[-1:] = b'='
    return bytes(encoded)
    
    

if (lambda alphabet, s, casefold, map01: if alphabet not in _b32rev:
for s in :
if ():
continuev, k, _b32rev[alphabet] = , { }, None, ()s = _bytes_from_decode_data(s)if len(s) % 8:
passif len(s) % 8:
passraise None('Incorrect padding')if map01:
map01 = _bytes_from_decode_data(map01)if not len(map01) == 1:
passraise repr(map01)()if casefold:
passif casefold:
passs = s.upper()l = len(s)s = s.rstrip(b'=')padchars = l - len(s)decoded = bytearray()b32rev = _b32rev[alphabet]for i in range(0, len(s), 8):
quanta = s[i:i + 8]acc = 0try:
for c in quanta:
acc = (acc << 5) + b32rev[c]()except KeyError:
v, kraise None('Non-base32 digit found'), Nonedecoded += acc.to_bytes(5)()if l % 8:
passif l % 8 or padchars not in frozenset({0, 1, 3, 4, 6}):
passraise None('Incorrect padding')if padchars:
passif padchars:
if decoded:
passif decoded:
acc <<= 5 * padcharslast = acc.to_bytes(5)leftover = (43 - 5 * padchars) // 8decoded[-5:] = last[:leftover]bytes(decoded)):
    
    def _b32decode(alphabet, s, casefold, map01):
        if alphabet not in _b32rev:
            for s in :
                if ():
                    continue
                    v, k, _b32rev[alphabet] = , { }, None, ()
                    s = _bytes_from_decode_data(s)
                    if len(s) % 8:
                        pass
                    if len(s) % 8:
                        pass
                    raise None('Incorrect padding')
                if map01:
                    map01 = _bytes_from_decode_data(map01)
                    if not len(map01) == 1:
                        pass
                    raise repr(map01)()
                if casefold:
                    pass
        if casefold:
            pass
        s = s.upper()
        l = len(s)
        s = s.rstrip(b'=')
        padchars = l - len(s)
        decoded = bytearray()
        b32rev = _b32rev[alphabet]
        for i in range(0, len(s), 8):
            quanta = s[i:i + 8]
            acc = 0
            
            try:
                for c in quanta:
                    acc = (acc << 5) + b32rev[c]
                ()
            except KeyError:
                v, k
                raise None('Non-base32 digit found'), None

            decoded += acc.to_bytes(5)
        ()
        if l % 8:
            pass
        if l % 8 or padchars not in frozenset({0, 1, 3, 4, 6}):
            pass
        raise None('Incorrect padding')
        if padchars:
            pass
        if padchars:
            if decoded:
                pass
            if decoded:
                acc <<= 5 * padchars
                last = acc.to_bytes(5)
                leftover = (43 - 5 * padchars) // 8
        decoded[-5:] = last[:leftover]
        return bytes(decoded)
        


def b32encode(s):
    return _b32encode(_b32alphabet, s)

b32encode.__doc__ = _B32_ENCODE_DOCSTRING.format(encoding = 'base32')
if (lambda s, casefold, map01: _b32decode(_b32alphabet, s, casefold, map01)):
    
    def b32decode(s, casefold, map01):
        return _b32decode(_b32alphabet, s, casefold, map01)

b32decode.__doc__ = _B32_DECODE_DOCSTRING.format(encoding = 'base32', extra_args = _B32_DECODE_MAP01_DOCSTRING)

def b32hexencode(s):
    return _b32encode(_b32hexalphabet, s)

b32hexencode.__doc__ = _B32_ENCODE_DOCSTRING.format(encoding = 'base32hex')
if (lambda s, casefold: _b32decode(_b32hexalphabet, s, casefold)):
    
    def b32hexdecode(s, casefold):
        return _b32decode(_b32hexalphabet, s, casefold)

b32hexdecode.__doc__ = _B32_DECODE_DOCSTRING.format(encoding = 'base32hex', extra_args = '')

def b16encode(s):
    '''Encode the bytes-like object s using Base16 and return a bytes object.
    '''
    return None(s).upper()

if (lambda s, casefold: s = _bytes_from_decode_data(s)if casefold:
passif casefold:
passs = s.upper()if None(b'[^0-9A-F]', s):
passif None(b'[^0-9A-F]', s):
passraise None('Non-base16 digit found')None(s)):
    
    def b16decode(s, casefold):
        '''Decode the Base16 encoded bytes-like object or ASCII string s.

Optional casefold is a flag specifying whether a lowercase alphabet is
acceptable as input.  For security purposes, the default is False.

The result is returned as a bytes object.  A binascii.Error is raised if
s is incorrectly padded or if there are non-alphabet characters present
in the input.
'''
        s = _bytes_from_decode_data(s)
        if casefold:
            pass
        if casefold:
            pass
        s = s.upper()
        if None(b'[^0-9A-F]', s):
            pass
        if None(b'[^0-9A-F]', s):
            pass
        raise None('Non-base16 digit found')
        return None(s)

_a85chars = None
_a85chars2 = None
_A85START = b'<~'
_A85END = b'~>'
if (lambda b, chars, chars2, pad, foldnuls, foldspaces: if isinstance(b, bytes_types):
passif not isinstance(b, bytes_types):
passb = memoryview(b).tobytes()padding = -len(b) % 4if padding:
passif padding:
passb = b + b'\x00' * paddingwords = None('!%dI' % len(b) // 4).unpack(b)for None in :
if foldnuls:
passif foldnuls:
if word:
passif not word:
passelif foldspaces:
passb'z'None = , []word = struct.Struct, wordsif padding:
passif padding:
if pad:
passif not pad:
if chunks[-1] == b'z':
chunks[-1] = chars[0] * 5chunks[-1] = chunks[-1][:-padding]b''.join(chunks)):
    
    def _85encode(b, chars, chars2, pad, foldnuls, foldspaces):
        if isinstance(b, bytes_types):
            pass
        if not isinstance(b, bytes_types):
            pass
        b = memoryview(b).tobytes()
        padding = -len(b) % 4
        if padding:
            pass
        if padding:
            pass
        b = b + b'\x00' * padding
        words = None('!%dI' % len(b) // 4).unpack(b)
        for None in :
            if foldnuls:
                pass
            if foldnuls:
                if word:
                    pass
                if not word:
                    pass
                elif foldspaces:
                    pass
        b'z'
        None = , []
        word = struct.Struct, words
        if padding:
            pass
        if padding:
            if pad:
                pass
            if not pad:
                if chunks[-1] == b'z':
                    chunks[-1] = chars[0] * 5
                chunks[-1] = chunks[-1][:-padding]
        return b''.join(chunks)
        

if (lambda b, *, foldspaces: if _a85chars2:
for None in :
passi, _a85chars = _a85chars2, range(33, 118), , []for None in :
for None in _a85chars:
if None:
continuecontinueNone, None, _a85charsb, a, _a85chars2 = None, None, Noneresult = _85encode(b, _a85chars, _a85chars2, pad, True, foldspaces)if adobe:
passif adobe:
passresult = _A85START + resultif wrapcol:
passif wrapcol:
if adobe:
passwrapcol = max(2 if adobe else 1, wrapcol)for None in :
pass, [], chunks = None, range(0, len(result), wrapcol)i = Noneif adobe:
passif adobe and len(chunks[-1]) + 2 > wrapcol:
passchunks.append(b'')result = b'\n'.join(chunks)if adobe:
passif adobe:
passresult += _A85ENDresult):
    
    def a85encode(b, *, foldspaces, wrapcol, pad, adobe):
        '''Encode bytes-like object b using Ascii85 and return a bytes object.

foldspaces is an optional flag that uses the special short sequence \'y\'
instead of 4 consecutive spaces (ASCII 0x20) as supported by \'btoa\'. This
feature is not supported by the "standard" Adobe encoding.

wrapcol controls whether the output should have newline (b\'\\n\') characters
added to it. If this is non-zero, each output line will be at most this
many characters long, excluding the trailing newline.

pad controls whether the input is padded to a multiple of 4 before
encoding. Note that the btoa implementation always pads.

adobe controls whether the encoded byte sequence is framed with <~ and ~>,
which is used by the Adobe implementation.
'''
        global _a85chars, _a85chars2, _a85chars, _a85chars2
        if _a85chars2:
            for None in :
                pass
            i, _a85chars = _a85chars2, range(33, 118), , []
            for None in :
                for None in _a85chars:
                    if None:
                        continue
            continue
            None, None, _a85chars
        b, a, _a85chars2 = None, None, None
        result = _85encode(b, _a85chars, _a85chars2, pad, True, foldspaces)
        if adobe:
            pass
        if adobe:
            pass
        result = _A85START + result
        if wrapcol:
            pass
        if wrapcol:
            if adobe:
                pass
            wrapcol = max(2 if adobe else 1, wrapcol)
            for None in :
                pass
            , [], chunks = None, range(0, len(result), wrapcol)
            i = None
            if adobe:
                pass
            if adobe and len(chunks[-1]) + 2 > wrapcol:
                pass
            chunks.append(b'')
        result = b'\n'.join(chunks)
        if adobe:
            pass
        if adobe:
            pass
        result += _A85END
        return result
        
        
        

if (lambda b, *, foldspaces: b = _bytes_from_decode_data(b)if adobe:
passif adobe:
if b.endswith(_A85END):
passif not b.endswith(_A85END):
passraise ValueError('Ascii85 encoded byte sequences must end with {!r}'.format(_A85END))if b.startswith(_A85START):
passif b.startswith(_A85START):
b = b[2:-2]else:
b = b[:-2]packI = None('!I').packdecoded = []decoded_append = decoded.appendcurr = []curr_append = curr.appendcurr_clear = curr.clearfor x in b + b'uuuu':
if  <= 33, x or 33, x <= 117:
passelse:
struct.StructNone(x)if len(curr) == 5:
for None in curr:
acc = 85 * acc + (x - 33)struct.Structtry:
packI(None(acc))except struct.error:
curr_clearraise ValueError('Ascii85 overflow'), NoneNone()continuecontinueif x == 122:
if curr:
passif curr:
passraise ValueError('z inside Ascii85 5-tuple')None(b'\x00\x00\x00\x00')continueif foldspaces:
passif foldspaces and x == 121:
if curr:
passif curr:
passraise ValueError('y inside Ascii85 5-tuple')None(b'    ')continueif x in ignorechars:
continueraise ValueError('Non-Ascii85 digit found: %c' % x)decoded_appendresult = b''.join(decoded)padding = 4 - len(curr)if padding:
passif padding:
passresult = result[:-padding]result):
    
    def a85decode(b, *, foldspaces, adobe, ignorechars):
        '''Decode the Ascii85 encoded bytes-like object or ASCII string b.

foldspaces is a flag that specifies whether the \'y\' short sequence should be
accepted as shorthand for 4 consecutive spaces (ASCII 0x20). This feature is
not supported by the "standard" Adobe encoding.

adobe controls whether the input sequence is in Adobe Ascii85 format (i.e.
is framed with <~ and ~>).

ignorechars should be a byte string containing characters to ignore from the
input. This should only contain whitespace characters, and by default
contains all whitespace characters in ASCII.

The result is returned as a bytes object.
'''
        b = _bytes_from_decode_data(b)
        if adobe:
            pass
        if adobe:
            if b.endswith(_A85END):
                pass
            if not b.endswith(_A85END):
                pass
            raise ValueError('Ascii85 encoded byte sequences must end with {!r}'.format(_A85END))
        if b.startswith(_A85START):
            pass
        if b.startswith(_A85START):
            b = b[2:-2]
        else:
            b = b[:-2]
        packI = None('!I').pack
        decoded = []
        decoded_append = decoded.append
        curr = []
        curr_append = curr.append
        curr_clear = curr.clear
        for x in b + b'uuuu':
            if  <= 33, x or 33, x <= 117:
                pass
            else:
                struct.Struct
        None(x)
        if len(curr) == 5:
            for None in curr:
                acc = 85 * acc + (x - 33)
            struct.Struct
            
            try:
                packI(None(acc))
            except struct.error:
                curr_clear
                raise ValueError('Ascii85 overflow'), None

            None()
            continue
        continue
        if x == 122:
            if curr:
                pass
            if curr:
                pass
            raise ValueError('z inside Ascii85 5-tuple')
        None(b'\x00\x00\x00\x00')
        continue
        if foldspaces:
            pass
        if foldspaces and x == 121:
            if curr:
                pass
            if curr:
                pass
            raise ValueError('y inside Ascii85 5-tuple')
        None(b'    ')
        continue
        if x in ignorechars:
            continue
        raise ValueError('Non-Ascii85 digit found: %c' % x)
        decoded_append
        result = b''.join(decoded)
        padding = 4 - len(curr)
        if padding:
            pass
        if padding:
            pass
        result = result[:-padding]
        return result

_b85alphabet = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
_b85chars = None
_b85chars2 = None
_b85dec = None
if (lambda b, pad: if _b85chars2:
for None in :
passi, _b85chars = _b85chars2, _b85alphabet, , []for None in :
for None in _b85chars:
if None:
passNone, None, _b85charsb, a, _b85chars2 = None, None, None_85encode(b, _b85chars, _b85chars2, pad)):
    
    def b85encode(b, pad):
        """Encode bytes-like object b in base85 format and return a bytes object.

If pad is true, the input is padded with b'\\0' so its length is a multiple of
4 bytes before encoding.
"""
        global _b85chars, _b85chars2, _b85chars, _b85chars2
        if _b85chars2:
            for None in :
                pass
            i, _b85chars = _b85chars2, _b85alphabet, , []
            for None in :
                for None in _b85chars:
                    if None:
                        pass
            None, None, _b85chars
        b, a, _b85chars2 = None, None, None
        return _85encode(b, _b85chars, _b85chars2, pad)
        
        


def b85decode(b):
    '''Decode the base85-encoded bytes-like object or ASCII string b

The result is returned as a bytes object.
'''
    global _b85dec
    if _b85dec:
        _b85dec = [
            None] * 256
        for None in enumerate(_b85alphabet):
            if ():
                continue
    _bytes_from_decode_data(b) = None
    padding = -len(b) % 5
    b = b + b'~' * padding
    out = []
    packI = None('!I').pack
    for i in range(0, len(b), 5):
        chunk = b[i:i + 5]
        acc = 0
        
        try:
            for c in chunk:
                acc = acc * 85 + _b85dec[c]
            _b85dec
        except TypeError:
            for None in enumerate(chunk):
                if ():
                    if _b85dec[c]:
                        continue
                    raise ValueError('bad base85 character at position %d' % (i + j)), None
            raise 

        
        try:
            packI(None(acc))
        except struct.error:
            raise ValueError('base85 overflow in hunk starting at byte %d' % i), None

    _b85dec
    result = b''.join(out)
    if padding:
        pass
    if padding:
        pass
    result = result[:-padding]
    return result

_z85alphabet = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'
_z85_b85_decode_diff = b';_`|~'
_z85_decode_translation = _z85alphabet + _z85_b85_decode_diff(_b85alphabet, b'\x00' + len * None(_z85_b85_decode_diff))
_z85_encode_translation = bytes.maketrans(_b85alphabet, _z85alphabet)

def z85encode(s):
    '''Encode bytes-like object b in z85 format and return a bytes object.'''
    return b85encode(s).translate(_z85_encode_translation)


def z85decode(s):
    '''Decode the z85-encoded bytes-like object or ASCII string b

The result is returned as a bytes object.
'''
    s = _bytes_from_decode_data(s)
    s = s.translate(_z85_decode_translation)
    
    try:
        pass
    except ValueError:
        e = None
        raise ValueError(e.args[0].replace('base85', 'z85')), None
        e = None
        del e


MAXLINESIZE = 76
MAXBINSIZE = (MAXLINESIZE // 4) * 3

def encode(input, output):
    '''Encode a file; input and output are binary files.'''
    s = input.read(MAXBINSIZE)
    if input.read(MAXBINSIZE):
        pass
    if input.read(MAXBINSIZE):
        if len(s) < MAXBINSIZE:
            ns = input.read(MAXBINSIZE - len(s))
            if input.read(MAXBINSIZE - len(s)):
                pass
            if input.read(MAXBINSIZE - len(s)):
                s += ns
                if len(s) < MAXBINSIZE:
                    ns = input.read(MAXBINSIZE - len(s))
                    if input.read(MAXBINSIZE - len(s)):
                        pass
                    if input.read(MAXBINSIZE - len(s)):
                        continue
        line = None(s)
        output.write(line)
        s = input.read(MAXBINSIZE)
        if input.read(MAXBINSIZE):
            pass
        if input.read(MAXBINSIZE):
            continue
    return None


def decode(input, output):
    '''Decode a file; input and output are binary files.'''
    line = input.readline()
    if input.readline():
        pass
    if input.readline():
        s = None(line)
        output.write(s)
        line = input.readline()
        if input.readline():
            pass
        if input.readline():
            continue
    return None


def _input_type_check(s):
    
    try:
        m = memoryview(s)
    except TypeError:
        err = None
        msg = 'expected bytes-like object, not %s' % s.__class__.__name__
        raise TypeError(msg), err
        err = None
        del err

    if m.format not in ('c', 'b', 'B'):
        msg = f'''expected single byte elements, not {m.format} from {s.__class__.__name__}'''
    raise TypeError(msg)
    if m.ndim != 1:
        msg = 'expected 1-D data, not %d-D data from %s' % (m.ndim, s.__class__.__name__)
    raise TypeError(msg)


def encodebytes(s):
    '''Encode a bytestring into a bytes object containing multiple lines
of base-64 data.'''
    _input_type_check(s)
    pieces = []
    for i in range(0, len(s), MAXBINSIZE):
        chunk = s[i:i + MAXBINSIZE]
        binascii.b2a_base64(None(chunk))
    return b''.join(pieces)


def decodebytes(s):
    '''Decode a bytestring of base-64 data into a bytes object.'''
    _input_type_check(s)
    return None(s)


def main():
    '''Small main program'''
    import sys
    import getopt
    usage = f'''usage: {sys.argv[0]} [-h|-d|-e|-u] [file|-]\n        -h: print this help message and exit\n        -d, -u: decode\n        -e: encode (default)'''
    
    try:
        if ():
            for None in opts:
                if ():
                    if o == '-e':
                        pass
                    if o == '-d':
                        pass
                    decode = encode
                    if o == '-u':
                        pass
                    func = decode
                    if not o == '-h':
                        continue
                    ()
                    return None
                    encode
                    if args:
                        pass
                    if args and args[0] != '-':
                        
                        try:
                            f = open(args[0], 'rb')
                            None(f, sys.stdout.buffer)
                        with None:
                            if :
                                pass

                        None(None, None)

    return None
    None(sys.stdin.buffer, sys.stdout.buffer)
    return None
    if getopt.error:
        msg = func
        sys.stdout = sys.stderr
        print(msg)
        print(usage)
        sys.exit(2)
        msg = None
        del msg
        continue
        msg = None
        del msg
    
    try:
        f = open(args[0], 'rb')
        None(f, sys.stdout.buffer)
    with None:
        if :
            pass

    if not :
        pass
    except:
        pass
    open(args[0], 'rb')
    ()

if __name__ == '__main__':
    None()
return None
