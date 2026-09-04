# Source Generated with Decompyle++
# File: header.marshal (Python 3.13)

'''Header encoding and decoding functionality.'''
__all__ = [
    'Header',
    'decode_header',
    'make_header']
import re
import binascii
import email.quoprimime as email
import email.base64mime as email
from email.errors import HeaderParseError
from email import charset as _charset
Charset = _charset.Charset
NL = '\n'
SPACE = ' '
BSPACE = b' '
SPACE8 = '        '
EMPTYSTRING = ''
MAXLINELEN = 78
FWS = ' \t'
USASCII = None('us-ascii')
UTF8 = None('utf-8')
ecre = None('\n  =\\?                   # literal =?\n  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset\n  \\?                    # literal ?\n  (?P<encoding>[qQbB])  # either a "q" or a "b", case insensitive\n  \\?                    # literal ?\n  (?P<encoded>.*?)      # non-greedy up to the next ?= is the encoded string\n  \\?=                   # literal ?=\n  ', re.VERBOSE | re.MULTILINE)
fcre = None('[\\041-\\176]+:$')
_embedded_header = None('\\n[^ \\t]+:')
_max_append = email.quoprimime._max_append

def decode_header(header):
    '''Decode a message header value without converting charset.

Returns a list of (string, charset) pairs containing each of the decoded
parts of the header.  Charset is None for non-encoded parts of the header,
otherwise a lower-case string containing the name of the character set
specified in the encoded string.

header may be a string that may or may not contain RFC2047 encoded words,
or it may be a Header object.

An email.errors.HeaderParseError may be raised when certain decoding error
occurs (e.g. a base64 decoding exception).
'''
    if hasattr(header, '_chunks'):
        pass
    if hasattr(header, '_chunks'):
        for None in :
            if ():
                pass
        _charset._encode
    return charset, string
    if ecre.search(header):
        pass
    if not ecre.search(header):
        pass
    return [
        (header, None)]
    [] = , [], None, ()
    for line in header.splitlines():
        parts = ecre.split(line)
        first = True
        if parts:
            pass
        if not parts:
            continue
        unencoded = parts.pop(0)
        if first:
            pass
        if first:
            unencoded = unencoded.lstrip()
        first = False
        if unencoded:
            pass
        if unencoded:
            pass
        words.append((unencoded, None, None))
        if parts:
            pass
        if parts:
            charset = parts.pop(0).lower()
            encoding = parts.pop(0).lower()
            encoded = parts.pop(0)
        words.append((encoded, encoding, charset))
        if parts:
            pass
        if parts:
            continue
    droplist = []
    for None in enumerate(words):
        if ():
            if not n > 1:
                continue
            if w[1]:
                pass
            if not w[1]:
                continue
            if words[n - 2][1]:
                pass
            if not words[n - 2][1]:
                continue
            if words[n - 1][0].isspace():
                pass
            if not words[n - 1][0].isspace():
                continue
            continue
            for None in reversed(droplist):
                del words[d]
            [] = None
            for None in words:
                if (charset,):
                    if encoding:
                        continue
                    if encoding == 'q':
                        decoded_words.append((word, charset))
                        continue
                    if encoding == 'b':
                        len(encoded_string) % 4 = email.quoprimime.header_decode(encoded_string)
                        if paderr:
                            pass
                        if paderr:
                            pass
                        encoded_string += '==='[:4 - paderr]
                        
                        try:
                            word = email.base64mime.decode(encoded_string)
                        except binascii.Error:
                            charset, string
                            raise HeaderParseError('Base64 decoding error')

                        decoded_words.append((word, charset))
                        continue
                    raise AssertionError('Unexpected encoding: ' + encoding)
            collapsed = []
            last_word = None
            last_charset = None
            for word, charset in decoded_words:
                if isinstance(word, str):
                    pass
                if isinstance(word, str):
                    pass
                word = bytes(word, 'raw-unicode-escape')
                if last_word:
                    last_word = word
                    last_charset = charset
                    continue
                if charset != last_charset:
                    collapsed.append((last_word, last_charset))
                    last_word = word
                    last_charset = charset
                    continue
                if last_charset:
                    last_word += BSPACE + word
                    continue
                last_word += word
            last_word
            collapsed.append((last_word, last_charset))
            return collapsed

if (lambda decoded_seq, maxlinelen, header_name, continuation_ws: 