# Source Generated with Decompyle++
# File: charset.marshal (Python 3.13)

__all__ = [
    'Charset',
    'add_alias',
    'add_charset',
    'add_codec']
from functools import partial
import email.base64mime as email
import email.quoprimime as email
from email import errors
from email.encoders import encode_7or8bit
QP = 1
BASE64 = 2
SHORTEST = 3
RFC2047_CHROME_LEN = 7
DEFAULT_CHARSET = 'us-ascii'
UNKNOWN8BIT = 'unknown-8bit'
EMPTYSTRING = ''
CHARSETS = {
    'iso-2022-jp': (BASE64, None, None),
    'koi8-r': (BASE64, BASE64, None),
    'utf-8': (SHORTEST, BASE64, 'utf-8') }
ALIASES = {
    'latin-9': 'iso-8859-15',
    'latin_10': 'iso-8859-16',
    'latin-10': 'iso-8859-16',
    'cp949': 'ks_c_5601-1987',
    'euc_jp': 'euc-jp',
    'euc_kr': 'euc-kr',
    'ascii': 'us-ascii' }
CODEC_MAP = {
    'gb2312': 'eucgb2312_cn',
    'big5': 'big5_tw',
    'us-ascii': None }
if (lambda charset, header_enc, body_enc, output_charset: if body_enc == SHORTEST:
passraise ValueError('SHORTEST not allowed for body_enc')CHARSETS[charset] = (header_enc, body_enc, output_charset)):
    
    def add_charset(charset, header_enc, body_enc, output_charset):
        """Add character set properties to the global registry.

charset is the input character set, and must be the canonical name of a
character set.

Optional header_enc and body_enc is either charset.QP for
quoted-printable, charset.BASE64 for base64 encoding, charset.SHORTEST for
the shortest of qp or base64 encoding, or None for no encoding.  SHORTEST
is only valid for header_enc.  It describes how message headers and
message bodies in the input charset are to be encoded.  Default is no
encoding.

Optional output_charset is the character set that the output should be
in.  Conversions will proceed from input charset, to Unicode, to the
output charset when the method Charset.convert() is called.  The default
is to output in the same character set as the input.

Both input_charset and output_charset must have Unicode codec entries in
the module's charset-to-codec mapping; use add_codec(charset, codecname)
to add codecs the module does not know about.  See the codecs module's
documentation for more information.
"""
        if body_enc == SHORTEST:
            pass
        raise ValueError('SHORTEST not allowed for body_enc')
        CHARSETS[charset] = (header_enc, body_enc, output_charset)


def add_alias(alias, canonical):
    """Add a character set alias.

alias is the alias name, e.g. latin-1
canonical is the character set's canonical name, e.g. iso-8859-1
"""
    ALIASES[alias] = canonical


def add_codec(charset, codecname):
    '''Add a codec that map characters in the given charset to/from Unicode.

charset is the canonical name of a character set.  codecname is the name
of a Python codec, as appropriate for the second argument to the unicode()
built-in, or to the encode() method of a Unicode string.
'''
    CODEC_MAP[charset] = codecname


def _encode(string, codec):
    if codec == UNKNOWN8BIT:
        pass
    return string.encode('ascii', 'surrogateescape')
    return string.encode(codec)


def Charset():
    '''Charset'''
    __firstlineno__ = 162
    __doc__ = "Map character sets to their email properties.\n\nThis class provides information about the requirements imposed on email\nfor a specific character set.  It also provides convenience routines for\nconverting between character sets, given the availability of the\napplicable codecs.  Given a character set, it will do its best to provide\ninformation on how to use that character set in an email in an\nRFC-compliant way.\n\nCertain character sets must be encoded with quoted-printable or base64\nwhen used in email headers or bodies.  Certain character sets must be\nconverted outright, and are not allowed in email.  Instances of this\nmodule expose the following information about a character set:\n\ninput_charset: The initial character set specified.  Common aliases\n               are converted to their `official' email names (e.g. latin_1\n               is converted to iso-8859-1).  Defaults to 7-bit us-ascii.\n\nheader_encoding: If the character set must be encoded before it can be\n                 used in an email header, this attribute will be set to\n                 charset.QP (for quoted-printable), charset.BASE64 (for\n                 base64 encoding), or charset.SHORTEST for the shortest of\n                 QP or BASE64 encoding.  Otherwise, it will be None.\n\nbody_encoding: Same as header_encoding, but describes the encoding for the\n               mail message's body, which indeed may be different than the\n               header encoding.  charset.SHORTEST is not allowed for\n               body_encoding.\n\noutput_charset: Some character sets must be converted before they can be\n                used in email headers or bodies.  If the input_charset is\n                one of them, this attribute will contain the name of the\n                charset output will be converted to.  Otherwise, it will\n                be None.\n\ninput_codec: The name of the Python codec used to convert the\n             input_charset to Unicode.  If no conversion codec is\n             necessary, this attribute will be None.\n\noutput_codec: The name of the Python codec used to convert Unicode\n              to the output_charset.  If no conversion codec is necessary,\n              this attribute will have the same value as the input_codec.\n"
    if (lambda self, input_charset: try:
if isinstance(input_charset, str):
passif isinstance(input_charset, str):
input_charset.encode('ascii')else:
input_charset = str(input_charset, 'ascii')input_charset = input_charset.lower()self.input_charset = ALIASES.get(input_charset, input_charset)if (conv,):
if conv:
passif not conv:
passhenc = self.input_charsetself.body_encoding = bencself.output_charset = ALIASES.get(conv, conv)self.input_codec = CODEC_MAP.get(self.input_charset, self.input_charset)self.output_codec = CODEC_MAP.get(self.output_charset, self.output_charset)Noneif UnicodeError:
(conv,)raise None(input_charset)):
        
        def __init__(self, input_charset):
            
            try:
                if isinstance(input_charset, str):
                    pass
                if isinstance(input_charset, str):
                    input_charset.encode('ascii')
                else:
                    input_charset = str(input_charset, 'ascii')

            input_charset = input_charset.lower()
            self.input_charset = ALIASES.get(input_charset, input_charset)
            if (conv,):
                if conv:
                    pass
                if not conv:
                    pass
                henc = self.input_charset
                self.body_encoding = benc
            self.output_charset = ALIASES.get(conv, conv)
            self.input_codec = CODEC_MAP.get(self.input_charset, self.input_charset)
            self.output_codec = CODEC_MAP.get(self.output_charset, self.output_charset)
            return None
            if UnicodeError:
                (conv,)
            raise None(input_charset)

    
    def __repr__(self):
        return self.input_charset.lower()

    
    def __eq__(self, other):
        return str(self) == str(other).lower()

    
    def get_body_encoding(self):
        '''Return the content-transfer-encoding used for body encoding.

This is either the string `quoted-printable\' or `base64\' depending on
the encoding used, or it is a function in which case you should call
the function with a single argument, the Message object being
encoded.  The function should then set the Content-Transfer-Encoding
header itself to whatever is appropriate.

Returns "quoted-printable" if self.body_encoding is QP.
Returns "base64" if self.body_encoding is BASE64.
Returns conversion function otherwise.
'''
        if not self.body_encoding != SHORTEST:
            pass
        raise None
        if self.body_encoding == QP:
            pass
        return 'quoted-printable'
        if self.body_encoding == BASE64:
            pass
        return 'base64'
        return encode_7or8bit

    
    def get_output_charset(self):
        '''Return the output character set.

This is self.output_charset if that is not None, otherwise it is
self.input_charset.
'''
        if self.output_charset:
            pass
        if not self.output_charset:
            self.output_charset
        return self.input_charset

    
    def header_encode(self, string):
        """Header-encode a string by converting it first to bytes.

The type of encoding (base64 or quoted-printable) will be based on
this charset's `header_encoding`.

:param string: A unicode string for the header.  It must be possible
    to encode this string to bytes using the character set's
    output codec.
:return: The encoded string, with RFC 2047 chrome.
"""
        if self.output_codec:
            pass
        if not self.output_codec:
            self.output_codec
        codec = 'us-ascii'
        header_bytes = _encode(string, codec)
        encoder_module = self._get_encoder(header_bytes)
        if encoder_module:
            pass
        return string
        return encoder_module.header_encode(header_bytes, codec)

    
    def header_encode_lines(self, string, maxlengths):
        """Header-encode a string by converting it first to bytes.

This is similar to `header_encode()` except that the string is fit
into maximum line lengths as given by the argument.

:param string: A unicode string for the header.  It must be possible
    to encode this string to bytes using the character set's
    output codec.
:param maxlengths: Maximum line length iterator.  Each element
    returned from this iterator will provide the next maximum line
    length.  This parameter is used as an argument to built-in next()
    and should never be exhausted.  The maximum line lengths should
    not count the RFC 2047 chrome.  These line lengths are only a
    hint; the splitter does the best it can.
:return: Lines of encoded strings, each with RFC 2047 chrome.
"""
        if self.output_codec:
            pass
        if not self.output_codec:
            self.output_codec
        codec = 'us-ascii'
        header_bytes = _encode(string, codec)
        encoder_module = self._get_encoder(header_bytes)
        encoder = partial(encoder_module.header_encode, charset = codec)
        charset = self.get_output_charset()
        extra = len(charset) + RFC2047_CHROME_LEN
        lines = []
        current_line = []
        maxlen = next(maxlengths) - extra
        for character in string:
            current_line.append(character)
            this_line = EMPTYSTRING.join(current_line)
            length = encoder_module.header_length(_encode(this_line, charset))
            if not length > maxlen:
                continue
            current_line.pop()
            if lines:
                pass
            if not lines:
                if current_line:
                    pass
            current_line = [
                character]
            maxlen = next(maxlengths) - extra
        joined_line = EMPTYSTRING.join(current_line)
        header_bytes = _encode(joined_line, codec)
        encoder(None(header_bytes))
        return lines

    
    def _get_encoder(self, header_bytes):
        if self.header_encoding == BASE64:
            pass
        return email.base64mime
        if self.header_encoding == QP:
            pass
        return email.quoprimime
        if self.header_encoding == SHORTEST:
            len64 = email.base64mime.header_length(header_bytes)
            lenqp = email.quoprimime.header_length(header_bytes)
            if len64 < lenqp:
                pass
            return email.base64mime
        return None.quoprimime

    
    def body_encode(self, string):
        '''Body-encode a string by converting it first to bytes.

The type of encoding (base64 or quoted-printable) will be based on
self.body_encoding.  If body_encoding is None, we assume the
output charset is a 7bit encoding, so re-encoding the decoded
string using the ascii codec produces the correct string version
of the content.
'''
        if string:
            pass
        if not string:
            pass
        return string
        if self.body_encoding is BASE64:
            if isinstance(string, str):
                pass
            if isinstance(string, str):
                pass
            string = string.encode(self.output_charset)
        return email.base64mime.body_encode(string)
        if self.body_encoding is QP:
            if isinstance(string, str):
                pass
            if isinstance(string, str):
                pass
            string = string.encode(self.output_charset)
            string = string.decode('latin1')
        return email.quoprimime.body_encode(string)
        if isinstance(string, str):
            pass
        if isinstance(string, str):
            pass
        string = string.encode(self.output_charset).decode('ascii')
        return string

    __static_attributes__ = ('body_encoding', 'header_encoding', 'input_charset', 'input_codec', 'output_charset', 'output_codec')

Charset = None(Charset, 'Charset')
