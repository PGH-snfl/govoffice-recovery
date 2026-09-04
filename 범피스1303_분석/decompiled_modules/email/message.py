# Source Generated with Decompyle++
# File: message.marshal (Python 3.13)

'''Basic message object for the email package object model.'''
__all__ = [
    'Message',
    'EmailMessage']
import binascii
import re
import quopri
from io import BytesIO, StringIO
from email import utils
from email import errors
from email._policybase import compat32
from email import charset as _charset
from email._encoded_words import decode_b
Charset = _charset.Charset
SEMISPACE = '; '
tspecials = None('[ \\(\\)<>@,;:\\\\"/\\[\\]\\?=]')

def _splitparam(param):
    if (b,):
        if sep:
            pass
        if not sep:
            pass
    return (a.strip(), None)
    return (a.strip(), b.strip())

if (lambda param, value, quote: if value and len(value) > 0:
if isinstance(value, tuple):
passif isinstance(value, tuple):
param += '*'value = None(value[2], value[0], value[1])f'''{param}={value}'''try:
value.encode('ascii')except UnicodeEncodeError:
paramparam += '*'value = None(value, 'utf-8', '')if quote:
passif not quote:
if tspecials.search(value):
passif tspecials.search(value):
passf'''="{utils.quote}{None(value)}"'''f'''{param}={value}'''param):
    
    def _formatparam(param, value, quote):
        '''Convenience function to format and return a key=value pair.

This will quote the value if needed or if quote is true.  If value is a
three tuple (charset, language, value), it will be encoded according
to RFC2231 rules.  If it contains non-ascii characters it will likewise
be encoded according to RFC2231 rules, using the utf-8 charset and
a null language.
'''
        if value and len(value) > 0:
            if isinstance(value, tuple):
                pass
            if isinstance(value, tuple):
                param += '*'
                value = None(value[2], value[0], value[1])
            return f'''{param}={value}'''
        
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            param
            param += '*'
            value = None(value, 'utf-8', '')

        if quote:
            pass
        if not quote:
            if tspecials.search(value):
                pass
            if tspecials.search(value):
                pass
        return f'''="{utils.quote}{None(value)}"'''
        return f'''{param}={value}'''
        return param


def _parseparam(s):
    s = ';' + str(s)
    plist = []
    if s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        if end > 0:
            if (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
                pass
            if (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
                end = s.find(';', end + 1)
                if end > 0:
                    if (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
                        pass
                    if (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
                        continue
        if end < 0:
            pass
        end = len(s)
        f = s[:end]
        if '=' in f:
            i = f.index('=')
        f = f[:i].strip().lower() + '=' + f[i + 1:].strip()
        plist.append(f.strip())
        s = s[end:]
        if s[:1] == ';':
            continue
    return plist


def _unquotevalue(value):
    if isinstance(value, tuple):
        pass
    if isinstance(value, tuple):
        pass
    return (value[1], utils.unquote, None(value[2]))
    return None(value)


def _decode_uu(encoded):
    '''Decode uuencoded data.'''
    decoded_lines = []
    encoded_lines_iter = iter(encoded.splitlines())
    for line in encoded_lines_iter:
        if line.startswith(b'begin '):
            pass
        if not line.startswith(b'begin '):
            continue
        if (path,):
            
            try:
                int(mode, base = 8)
            except ValueError:
                pass

        else:
            raise ValueError('`begin` line not found')
        for None in encoded_lines_iter:
            if line:
                pass
            if not line:
                pass
            raise ValueError('Truncated input')
            if line.strip(b' \t\r\n\x0c') == b'end':
                pass
            else:
                
                try:
                    None(line) = binascii.a2b_uu
                except binascii.Error:
                    nbytes = ((line[0] - 32 & 63) * 4 + 5) // 3
                    decoded_line = None(line[:nbytes])

                decoded_lines.append(decoded_line)
        return b''.join(decoded_lines)


def Message():
    '''Message'''
    __firstlineno__ = 135
    __doc__ = "Basic message object.\n\nA message object is defined as something that has a bunch of RFC 2822\nheaders and a payload.  It may optionally have an envelope header\n(a.k.a. Unix-From or From_ header).  If the message is a container (i.e. a\nmultipart or a message/rfc822), then the payload is a list of Message\nobjects, otherwise it is a string.\n\nMessage objects implement part of the `mapping' interface, which assumes\nthere is exactly one occurrence of the header per message.  Some headers\ndo in fact appear multiple times (e.g. Received) and for those headers,\nyou must use the explicit API to set or get all the headers.  Not all of\nthe mapping methods are implemented.\n"
    if (lambda self, policy: self.policy = policyself._headers = []self._unixfrom = Noneself._payload = Noneself._charset = Noneself.preamble = Noneself.epilogue = Noneself.defects = []self._default_type = 'text/plain'):
        
        def __init__(self, policy):
            self.policy = policy
            self._headers = []
            self._unixfrom = None
            self._payload = None
            self._charset = None
            self.preamble = None
            self.epilogue = None
            self.defects = []
            self._default_type = 'text/plain'

    
    def __str__(self):
        '''Return the entire formatted message as a string.
        '''
        return self.as_string()

    if (lambda self, unixfrom, maxheaderlen, policy: Generator = Generatorimport email.generatorpolicy = self.policy if policy else policyfp = StringIO()g = None(fp, mangle_from_ = False, maxheaderlen = maxheaderlen, policy = policy)g.flatten(self, unixfrom = unixfrom)fp.getvalue()):
        
        def as_string(self, unixfrom, maxheaderlen, policy):
            '''Return the entire formatted message as a string.

Optional \'unixfrom\', when true, means include the Unix From_ envelope
header.  For backward compatibility reasons, if maxheaderlen is
not specified it defaults to 0, so you must override it explicitly
if you want a different maxheaderlen.  \'policy\' is passed to the
Generator instance used to serialize the message; if it is not
specified the policy associated with the message instance is used.

If the message object contains binary data that is not encoded
according to RFC standards, the non-compliant data will be replaced by
unicode "unknown character" code points.
'''
            Generator = Generator
            import email.generator
            policy = self.policy if policy else policy
            fp = StringIO()
            g = None(fp, mangle_from_ = False, maxheaderlen = maxheaderlen, policy = policy)
            g.flatten(self, unixfrom = unixfrom)
            return fp.getvalue()

    
    def __bytes__(self):
        '''Return the entire formatted message as a bytes object.
        '''
        return self.as_bytes()

    if (lambda self, unixfrom, policy: BytesGenerator = BytesGeneratorimport email.generatorpolicy = self.policy if policy else policyfp = BytesIO()g = None(fp, mangle_from_ = False, policy = policy)g.flatten(self, unixfrom = unixfrom)fp.getvalue()):
        
        def as_bytes(self, unixfrom, policy):
            """Return the entire formatted message as a bytes object.

Optional 'unixfrom', when true, means include the Unix From_ envelope
header.  'policy' is passed to the BytesGenerator instance used to
serialize the message; if not specified the policy associated with
the message instance is used.
"""
            BytesGenerator = BytesGenerator
            import email.generator
            policy = self.policy if policy else policy
            fp = BytesIO()
            g = None(fp, mangle_from_ = False, policy = policy)
            g.flatten(self, unixfrom = unixfrom)
            return fp.getvalue()

    
    def is_multipart(self):
        '''Return True if the message consists of multiple parts.'''
        return isinstance(self._payload, list)

    
    def set_unixfrom(self, unixfrom):
        self._unixfrom = unixfrom

    
    def get_unixfrom(self):
        return self._unixfrom

    
    def attach(self, payload):
        '''Add the given payload to the current payload.

The current payload will always be a list of objects after this method
is called.  If you want to set the payload to a scalar object, use
set_payload() instead.
'''
        if self._payload:
            self._payload = [
                payload]
        return None
        
        try:
            self._payload.append(payload)
        except AttributeError:
            self._payload
            raise TypeError('Attach is not valid on a message with a non-multipart payload')


    if (lambda self, i, decode: if self.is_multipart():
passif self.is_multipart():
if decode:
passif decode:
passNoneif i:
passself._payloadNone._payload[i]if i:
if isinstance(self._payload, list):
passif not isinstance(self._payload, list):
passraise TypeError('Expected list, got %s' % type(self._payload))payload = self._payloadcte = self.get('content-transfer-encoding', '')if hasattr(cte, 'cte'):
passif decode:
passif not decode:
if isinstance(payload, str):
passif isinstance(payload, str):
if None(payload):
passif None(payload):
try:
bpayload = payload.encode('ascii', 'surrogateescape')except UnicodeEncodeError:
passtry:
payload = bpayload.decode(self.get_content_charset('ascii'), 'replace')except LookupError:
quopri.decodestringbpayload.decode('ascii', 'replace') = NonepayloadNone if hasattr(cte, 'cte') else iif isinstance(payload, str):
passif isinstance(payload, str):
try:
bpayload = payload.encode('ascii', 'surrogateescape')except UnicodeEncodeError:
bpayload = payload.encode('raw-unicode-escape')if cte == 'quoted-printable':
passNone(bpayload)if cte == 'base64' or ():
for None in defects:
passvalueif () in ('x-uuencode', 'uuencode', 'uue', 'x-uue'):
try:
passexcept ValueError:
quopri.decodestringdecode_b(b''.join(bpayload.splitlines()))if decode_b(b''.join(bpayload.splitlines()))(payload, str):
passif decode_b(b''.join(bpayload.splitlines()))(payload, str):
passbpayloadpayload):
        
        def get_payload(self, i, decode):
            """Return a reference to the payload.

The payload will either be a list object or a string.  If you mutate
the list object, you modify the message's payload in place.  Optional
i returns that index into the payload.

Optional decode is a flag indicating whether the payload should be
decoded or not, according to the Content-Transfer-Encoding header
(default is False).

When True and the message is not a multipart, the payload will be
decoded if this header's value is `quoted-printable' or `base64'.  If
some other encoding is used, or the header is missing, or if the
payload has bogus data (i.e. bogus base64 or uuencoded data), the
payload is returned as-is.

If the message is a multipart and the decode flag is True, then None
is returned.
"""
            if self.is_multipart():
                pass
            if self.is_multipart():
                if decode:
                    pass
                if decode:
                    pass
                return None
                if i:
                    pass
                return self._payload
            return None._payload[i]
            if i:
                if isinstance(self._payload, list):
                    pass
                if not isinstance(self._payload, list):
                    pass
            raise TypeError('Expected list, got %s' % type(self._payload))
            payload = self._payload
            cte = self.get('content-transfer-encoding', '')
            if hasattr(cte, 'cte'):
                pass
            if decode:
                pass
            if not decode:
                if isinstance(payload, str):
                    pass
                if isinstance(payload, str):
                    if None(payload):
                        pass
                    if None(payload):
                        
                        try:
                            bpayload = payload.encode('ascii', 'surrogateescape')
                        except UnicodeEncodeError:
                            pass

                        
                        try:
                            payload = bpayload.decode(self.get_content_charset('ascii'), 'replace')
                        except LookupError:
                            quopri.decodestring
                            bpayload.decode('ascii', 'replace') = None

                return payload
            return None if hasattr(cte, 'cte') else i
            if isinstance(payload, str):
                pass
            if isinstance(payload, str):
                
                try:
                    bpayload = payload.encode('ascii', 'surrogateescape')
                except UnicodeEncodeError:
                    bpayload = payload.encode('raw-unicode-escape')

                if cte == 'quoted-printable':
                    pass
            return None(bpayload)
            if cte == 'base64' or ():
                for None in defects:
                    pass
                return value
            if () in ('x-uuencode', 'uuencode', 'uue', 'x-uue'):
                
                try:
                    pass
                except ValueError:
                    quopri.decodestring

                return decode_b(b''.join(bpayload.splitlines()))
            if decode_b(b''.join(bpayload.splitlines()))(payload, str):
                pass
            if decode_b(b''.join(bpayload.splitlines()))(payload, str):
                pass
            return bpayload
            return payload

    if (lambda self, payload, charset: if hasattr(payload, 'encode'):
passif hasattr(payload, 'encode'):
if charset:
self._payload = payloadNoneif isinstance(charset, Charset):
passif not isinstance(charset, Charset):
passcharset = Charset(charset)payload = payload.encode(charset.output_charset, 'surrogateescape')if hasattr(payload, 'decode'):
passif charset:
passNone):
        
        def set_payload(self, payload, charset):
            """Set the payload to the given value.

Optional charset sets the message's default character set.  See
set_charset() for details.
"""
            if hasattr(payload, 'encode'):
                pass
            if hasattr(payload, 'encode'):
                if charset:
                    self._payload = payload
                return None
                if isinstance(charset, Charset):
                    pass
                if not isinstance(charset, Charset):
                    pass
                charset = Charset(charset)
            payload = payload.encode(charset.output_charset, 'surrogateescape')
            if hasattr(payload, 'decode'):
                pass
            if charset:
                pass
            return None

    
    def set_charset(self, charset):
        '''Set the charset of the payload to a given character set.

charset can be a Charset instance, a string naming a character set, or
None.  If it is a string it will be converted to a Charset instance.
If charset is None, the charset parameter will be removed from the
Content-Type field.  Anything else will generate a TypeError.

The message will be assumed to be of type text/* encoded with
charset.input_charset.  It will be converted to charset.output_charset
and encoded properly, if needed, when generating the plain text
representation of the message.  MIME headers (MIME-Version,
Content-Type, Content-Transfer-Encoding) will be added as needed.
'''
        if charset:
            self._charset = None
        return None
        if isinstance(charset, Charset):
            pass
        if not isinstance(charset, Charset):
            pass
        charset = Charset(charset)
        self._charset = charset
        if 'MIME-Version' not in self:
            pass
        self.add_header('MIME-Version', '1.0')
        if charset != charset.get_output_charset():
            self._payload = charset.body_encode(self._payload)
        if 'Content-Transfer-Encoding' not in self:
            cte = charset.get_body_encoding()
            
            try:
                None(self)
            except TypeError:
                charset if 'Content-Type' not in self else None
                payload = self._payload
                if payload:
                    pass
                if payload:
                    
                    try:
                        payload = payload.encode('ascii', 'surrogateescape')
                    except UnicodeError:
                        payload = payload.encode(charset.output_charset)
                    except:
                        pass

                
                self._payload = charset.body_encode(payload)
                self.add_header('Content-Transfer-Encoding', cte)

            return None
            return None

    
    def get_charset(self):
        """Return the Charset instance associated with the message's payload.
        """
        return self._charset

    
    def __len__(self):
        '''Return the total number of headers, including duplicates.'''
        return len(self._headers)

    
    def __getitem__(self, name):
        '''Get a header value.

Return None if the header is missing instead of raising an exception.

Note that if the header appeared multiple times, exactly which
occurrence gets returned is undefined.  Use get_all() to get all
the values matching a header field name.
'''
        return self.get(name)

    
    def __setitem__(self, name, val):
        '''Set the value of a header.

Note: this does not overwrite an existing header with the same field
name.  Use __delitem__() first to delete any existing headers.
'''
        max_count = self.policy.header_max_count(name)
        if max_count:
            pass
        if max_count:
            lname = name.lower()
            found = 0
            for None in self._headers:
                if ():
                    if not k.lower() == lname:
                        continue
                    if not found >= max_count:
                        continue
                    raise ValueError('There may be at most {} {} headers in a message'.format(max_count, name))
        self._headers.append(self.policy.header_store_parse(name, val))

    
    def __delitem__(self, name):
        '''Delete all occurrences of a header, if present.

Does not raise an exception if the header is missing.
'''
        name = name.lower()
        newheaders = []
        for None in self._headers:
            if ():
                if not k.lower() != name:
                    continue
                continue
                return None

    
    def __contains__(self, name):
        name_lower = name.lower()
        for None in self._headers:
            if ():
                if not name_lower == k.lower():
                    continue
                return True
                return False

    
    def __iter__(self):
        if None:
            pass
        for None in self._headers:
            if ():
                if field:
                    pass
                continue
                return None

    
    def keys(self):
        """Return a list of all the message's header field names.

These will be sorted in the order they appeared in the original
message, or were added to the message, and may contain duplicates.
Any fields deleted and re-inserted are always appended to the header
list.
"""
        for None in :
            if ():
                continue
                return v, k

    
    def values(self):
        """Return a list of all the message's header values.

These will be sorted in the order they appeared in the original
message, or were added to the message, and may contain duplicates.
Any fields deleted and re-inserted are always appended to the header
list.
"""
        for None in :
            if ():
                pass
        ()
        return v, k
        

    
    def items(self):
        """Get all the message's header fields and values.

These will be sorted in the order they appeared in the original
message, or were added to the message, and may contain duplicates.
Any fields deleted and re-inserted are always appended to the header
list.
"""
        for None in :
            if ():
                pass
        ()
        return v, k
        

    if (lambda self, name, failobj: name = name.lower()for None in self._headers:
if ():
if not k.lower() == name:
continue(), self.policy.header_fetch_parse(k, v)failobj):
        
        def get(self, name, failobj):
            '''Get a header value.

Like __getitem__() but return failobj instead of None when the field
is missing.
'''
            name = name.lower()
            for None in self._headers:
                if ():
                    if not k.lower() == name:
                        continue
                    return (), self.policy.header_fetch_parse(k, v)
                return failobj

    
    def set_raw(self, name, value):
        '''Store name and value in the model without modification.

This is an "internal" API, intended only for use by a parser.
'''
        self._headers.append((name, value))

    
    def raw_items(self):
        '''Return the (name, value) header pairs without modification.

This is an "internal" API, intended only for use by a generator.
'''
        return iter(self._headers.copy())

    if (lambda self, name, failobj: values = []name = name.lower()for None in self._headers:
if ():
if not k.lower() == name:
continuecontinueif values:
passif not values:
passfailobjvalues):
        
        def get_all(self, name, failobj):
            '''Return a list of all the values for the named field.

These will be sorted in the order they appeared in the original
message, and may contain duplicates.  Any fields deleted and
re-inserted are always appended to the header list.

If no such fields exist, failobj is returned (defaults to None).
'''
            values = []
            name = name.lower()
            for None in self._headers:
                if ():
                    if not k.lower() == name:
                        continue
                    continue
            if values:
                pass
            if not values:
                pass
            return failobj
            return values

    
    def add_header(self, _name, _value, **_params):
        '''Extended header setting.

name is the header field to add.  keyword arguments can be used to set
additional parameters for the header field, with underscores converted
to dashes.  Normally the parameter will be added as key="value" unless
value is None, in which case only the key will be added.  If a
parameter value contains non-ASCII characters it can be specified as a
three-tuple of (charset, language, value), in which case it will be
encoded according to RFC2231 rules.  Otherwise it will be encoded using
the utf-8 charset and a language of \'\'.

Examples:

msg.add_header(\'content-disposition\', \'attachment\', filename=\'bud.gif\')
msg.add_header(\'content-disposition\', \'attachment\',
               filename=(\'utf-8\', \'\', Fußballer.ppt\'))
msg.add_header(\'content-disposition\', \'attachment\',
               filename=\'Fußballer.ppt\'))
'''
        parts = []
        for None in _params.items():
            if ():
                if v:
                    continue
                continue
                ()
        if _value:
            pass
        parts.insert(0, _value)

    
    def replace_header(self, _name, _value):
        '''Replace a header.

Replace the first matching header found in the message, retaining
header order and case.  If no matching header was found, a KeyError is
raised.
'''
        _name = _name.lower()
        for None in zip(range(len(self._headers)), self._headers):
            if ():
                if not k.lower() == _name:
                    continue
                return None
                (i,)
        raise KeyError(_name)

    
    def get_content_type(self):
        """Return the message's content type.

The returned string is coerced to lower case of the form
`maintype/subtype'.  If there was no Content-Type header in the
message, the default type as given by get_default_type() will be
returned.  Since according to RFC 2045, messages always have a default
type this will always return a value.

RFC 2045 defines a message's default type to be text/plain unless it
appears inside a multipart/digest container, in which case it would be
message/rfc822.
"""
        missing = object()
        value = self.get('content-type', missing)
        if value is missing:
            pass
        return self.get_default_type()
        ctype = _splitparam(value)[0].lower()
        if ctype.count('/') != 1:
            pass
        return 'text/plain'
        return ctype

    
    def get_content_maintype(self):
        """Return the message's main content type.

This is the `maintype' part of the string returned by
get_content_type().
"""
        ctype = self.get_content_type()
        return ctype.split('/')[0]

    
    def get_content_subtype(self):
        """Returns the message's sub-content type.

This is the `subtype' part of the string returned by
get_content_type().
"""
        ctype = self.get_content_type()
        return ctype.split('/')[1]

    
    def get_default_type(self):
        """Return the `default' content type.

Most messages have a default content type of text/plain, except for
messages that are subparts of multipart/digest containers.  Such
subparts have a default content type of message/rfc822.
"""
        return self._default_type

    
    def set_default_type(self, ctype):
        '''Set the `default\' content type.

ctype should be either "text/plain" or "message/rfc822", although this
is not enforced.  The default content type is not stored in the
Content-Type header.
'''
        self._default_type = ctype

    
    def _get_params_preserve(self, failobj, header):
        missing = object()
        value = self.get(header, missing)
        if value is missing:
            pass
        return failobj
        params = []
        for p in _parseparam(value):
            
            try:
                if ():
                    val.strip() = name.strip()
                    continue
                    p.split('=', 1)
                    params = None(params)
                    return params

            if ValueError:
                name = p.strip()
                val = ''
        continue

    if (lambda self, failobj, header, unquote: missing = object()params = self._get_params_preserve(missing, header)if params is missing:
passfailobjif unquote:
passif unquote:
for None in :
if ():
continuev, k()):
        
        def get_params(self, failobj, header, unquote):
            """Return the message's Content-Type parameters, as a list.

The elements of the returned list are 2-tuples of key/value pairs, as
split on the `=' sign.  The left hand side of the `=' is the key,
while the right hand side is the value.  If there is no `=' sign in
the parameter the value is the empty string.  The value is as
described in the get_param() method.

Optional failobj is the object to return if there is no Content-Type
header.  Optional header is the header to search instead of
Content-Type.  If unquote is True, the value is unquoted.
"""
            missing = object()
            params = self._get_params_preserve(missing, header)
            if params is missing:
                pass
            return failobj
            if unquote:
                pass
            if unquote:
                for None in :
                    if ():
                        continue
                        return v, k
                    return ()

    if (lambda self, param, failobj, header, unquote: if header not in self:
passfailobjfor None in self._get_params_preserve(failobj, header):
if ():
if not k.lower() == param.lower():
continueif unquote:
passif unquote:
(), _unquotevalue(v)None, ()failobj):
        
        def get_param(self, param, failobj, header, unquote):
            """Return the parameter value if found in the Content-Type header.

Optional failobj is the object to return if there is no Content-Type
header, or the Content-Type header has no such parameter.  Optional
header is the header to search instead of Content-Type.

Parameter keys are always compared case insensitively.  The return
value can either be a string, or a 3-tuple if the parameter was RFC
2231 encoded.  When it's a 3-tuple, the elements of the value are of
the form (CHARSET, LANGUAGE, VALUE).  Note that both CHARSET and
LANGUAGE can be None, in which case you should consider VALUE to be
encoded in the us-ascii charset.  You can usually ignore LANGUAGE.
The parameter value (either the returned string, or the VALUE item in
the 3-tuple) is always unquoted, unless unquote is set to False.

If your application doesn't care whether the parameter was RFC 2231
encoded, it can turn the return value into a string as follows:

    rawparam = msg.get_param('foo')
    param = email.utils.collapse_rfc2231_value(rawparam)

"""
            if header not in self:
                pass
            return failobj
            for None in self._get_params_preserve(failobj, header):
                if ():
                    if not k.lower() == param.lower():
                        continue
                    if unquote:
                        pass
                    if unquote:
                        
                    return (), _unquotevalue(v)
                return None, ()
            return failobj

    if (lambda self, param, value, header, requote, charset, language, replace: if isinstance(value, tuple):
passif not isinstance(value, tuple):
if charset:
passif charset:
passvalue = (charset, language, value)if header not in self and header.lower() == 'content-type':
ctype = 'text/plain'else:
ctype = self.get(header)if self.get_param(param, header = header):
passif not self.get_param(param, header = header):
if ctype:
passif not ctype:
ctype = _formatparam(param, value, requote)else:
ctype = SEMISPACE.join([
ctype,
_formatparam(param, value, requote)])else:
ctype = ''for None in self.get_params(header = header, unquote = requote):
if ():
if ctype:
passif not ctype:
ctype = append_paramcontinuectype = SEMISPACE.join([
ctype,
append_param])continueif ctype != self.get(header):
if replace:
passif replace:
self.replace_header(header, ctype)Nonedel self[header]self[header] = ctypeNoneNone):
        
        def set_param(self, param, value, header, requote, charset, language, replace):
            '''Set a parameter in the Content-Type header.

If the parameter already exists in the header, its value will be
replaced with the new value.

If header is Content-Type and has not yet been defined for this
message, it will be set to "text/plain" and the new parameter and
value will be appended as per RFC 2045.

An alternate header can be specified in the header argument, and all
parameters will be quoted as necessary unless requote is False.

If charset is specified, the parameter will be encoded according to RFC
2231.  Optional language specifies the RFC 2231 language, defaulting
to the empty string.  Both charset and language should be strings.
'''
            if isinstance(value, tuple):
                pass
            if not isinstance(value, tuple):
                if charset:
                    pass
                if charset:
                    pass
            value = (charset, language, value)
            if header not in self and header.lower() == 'content-type':
                ctype = 'text/plain'
            else:
                ctype = self.get(header)
            if self.get_param(param, header = header):
                pass
            if not self.get_param(param, header = header):
                if ctype:
                    pass
                if not ctype:
                    ctype = _formatparam(param, value, requote)
                else:
                    ctype = SEMISPACE.join([
                        ctype,
                        _formatparam(param, value, requote)])
            else:
                ctype = ''
                for None in self.get_params(header = header, unquote = requote):
                    if ():
                        if ctype:
                            pass
                        if not ctype:
                            ctype = append_param
                            continue
                        ctype = SEMISPACE.join([
                            ctype,
                            append_param])
                        continue
                        if ctype != self.get(header):
                            if replace:
                                pass
                            if replace:
                                self.replace_header(header, ctype)
                            return None
                            del self[header]
                            self[header] = ctype
                        return None
                        return None

    if (lambda self, param, header, requote: if header not in self:
passNonenew_ctype = ''for SEMISPACE.join([
new_ctype,
_formatparam(p, v, requote)]) in self.get_params(header = header, unquote = requote):
if ():
if not p.lower() != param.lower():
continueif new_ctype:
passif not new_ctype:
continueif new_ctype != self.get(header):
del self[header]self[header] = new_ctypeNone):
        
        def del_param(self, param, header, requote):
            '''Remove the given parameter completely from the Content-Type header.

The header will be re-written in place without the parameter or its
value. All values will be quoted as necessary unless requote is
False.  Optional header specifies an alternative to the Content-Type
header.
'''
            if header not in self:
                pass
            return None
            new_ctype = ''
            for SEMISPACE.join([
                new_ctype,
                _formatparam(p, v, requote)]) in self.get_params(header = header, unquote = requote):
                if ():
                    if not p.lower() != param.lower():
                        continue
                    if new_ctype:
                        pass
                    if not new_ctype:
                        continue
            if new_ctype != self.get(header):
                del self[header]
                self[header] = new_ctype
            return None

    if (lambda self, type, header, requote: if not type.count('/') == 1:
passraise ValueErrorif header.lower() == 'content-type':
del self['mime-version']self['MIME-Version'] = '1.0'if header not in self:
self[header] = typeNoneparams = self.get_params(header = header, unquote = requote)del self[header]self[header] = typefor None in params[1:]:
if ():
continueNone):
        
        def set_type(self, type, header, requote):
            '''Set the main type and subtype for the Content-Type header.

type must be a string in the form "maintype/subtype", otherwise a
ValueError is raised.

This method replaces the Content-Type header, keeping all the
parameters in place.  If requote is False, this leaves the existing
header\'s quoting as is.  Otherwise, the parameters will be quoted (the
default).

An alternative header can be specified in the header argument.  When
the Content-Type header is set, we\'ll always also add a MIME-Version
header.
'''
            if not type.count('/') == 1:
                pass
            raise ValueError
            if header.lower() == 'content-type':
                del self['mime-version']
                self['MIME-Version'] = '1.0'
            if header not in self:
                self[header] = type
            return None
            params = self.get_params(header = header, unquote = requote)
            del self[header]
            self[header] = type
            for None in params[1:]:
                if ():
                    continue
                    return None

    if (lambda self, failobj: missing = object()filename = self.get_param('filename', missing, 'content-disposition')if filename is missing:
passfilename = self.get_param('name', missing, 'content-type')if filename is missing:
passfailobjNone(filename).strip()):
        
        def get_filename(self, failobj):
            """Return the filename associated with the payload if present.

The filename is extracted from the Content-Disposition header's
`filename' parameter, and it is unquoted.  If that header is missing
the `filename' parameter, this method falls back to looking for the
`name' parameter.
"""
            missing = object()
            filename = self.get_param('filename', missing, 'content-disposition')
            if filename is missing:
                pass
            filename = self.get_param('name', missing, 'content-type')
            if filename is missing:
                pass
            return failobj
            return None(filename).strip()

    if (lambda self, failobj: missing = object()boundary = self.get_param('boundary', missing)if boundary is missing:
passfailobjNone(boundary).rstrip()):
        
        def get_boundary(self, failobj):
            """Return the boundary associated with the payload if present.

The boundary is extracted from the Content-Type header's `boundary'
parameter, and it is unquoted.
"""
            missing = object()
            boundary = self.get_param('boundary', missing)
            if boundary is missing:
                pass
            return failobj
            return None(boundary).rstrip()

    
    def set_boundary(self, boundary):
        """Set the boundary parameter in Content-Type to 'boundary'.

This is subtly different than deleting the Content-Type header and
adding a new one with a new boundary parameter via add_header().  The
main difference is that using the set_boundary() method preserves the
order of the Content-Type header in the original message.

HeaderParseError is raised if the message has no Content-Type header.
"""
        missing = object()
        params = self._get_params_preserve(missing, 'content-type')
        if params is missing:
            pass
        raise None('No Content-Type header found')
        newparams = []
        foundp = False
        for None in params:
            if ():
                if pk.lower() == 'boundary':
                    newparams.append(('boundary', '"%s"' % boundary))
                    continue
                continue
                ()
                if foundp:
                    pass
                if not foundp:
                    pass
                newparams.append(('boundary', '"%s"' % boundary))
                [] = None
        for None in self._headers:
            if ():
                if h.lower() == 'content-type':
                    for None in newparams:
                        if ():
                            if v == '':
                                parts.append(k)
                                continue
                            continue
                            newheaders.append(self.policy.header_store_parse(h, val))
                            continue
                            newheaders.append((h, v))
                            continue
                            []
                            newheaders = ()
                            return None

    if (lambda self, failobj: missing = object()charset = self.get_param('charset', missing)if charset is missing:
passfailobjif isinstance(charset, tuple):
passif isinstance(charset, tuple):
if charset[0]:
passif not charset[0]:
charset[0]pcharset = 'us-ascii'try:
as_bytes = charset[2].encode('raw-unicode-escape')charset = str(as_bytes, pcharset)try:
charset.encode('us-ascii')except UnicodeError:
passcharset.lower()if (LookupError, UnicodeError):
charset = charset[2]continue):
        
        def get_content_charset(self, failobj):
            '''Return the charset parameter of the Content-Type header.

The returned string is always coerced to lower case.  If there is no
Content-Type header, or if that header has no charset parameter,
failobj is returned.
'''
            missing = object()
            charset = self.get_param('charset', missing)
            if charset is missing:
                pass
            return failobj
            if isinstance(charset, tuple):
                pass
            if isinstance(charset, tuple):
                if charset[0]:
                    pass
                if not charset[0]:
                    charset[0]
                pcharset = 'us-ascii'
                
                try:
                    as_bytes = charset[2].encode('raw-unicode-escape')
                    charset = str(as_bytes, pcharset)

                
                try:
                    charset.encode('us-ascii')
                except UnicodeError:
                    pass

                return charset.lower()
            if (LookupError, UnicodeError):
                charset = charset[2]
            continue

    if (lambda self, failobj: for None in :
if None:
continuepart,):
        
        def get_charsets(self, failobj):
            '''Return a list containing the charset(s) used in this message.

The returned list of items describes the Content-Type headers\'
charset parameter for this message and all the subparts in its
payload.

Each item will either be a string (the value of the charset parameter
in the Content-Type header of that part) or the value of the
\'failobj\' parameter (defaults to None), if the part does not have a
main MIME type of "text", or the charset is not defined.

The list will contain one string for each part of the message, plus
one for the container message (i.e. self), so that a non-multipart
message will still return a list of length 1.
'''
            for None in :
                if None:
                    continue
                    return part,

    
    def get_content_disposition(self):
        """Return the message's content-disposition if it exists, or None.

The return values can be either 'inline', 'attachment' or None
according to the rfc2183.
"""
        value = self.get('content-disposition')
        if value:
            pass
        return None
        c_d = _splitparam(value)[0].lower()
        return c_d

    from email.iterators import walk
    __static_attributes__ = ('_charset', '_default_type', '_headers', '_payload', '_unixfrom', 'defects', 'epilogue', 'policy', 'preamble')

Message = None(Message, 'Message')

def MIMEPart():
    '''MIMEPart'''
    __firstlineno__ = 981
    if (lambda self, policy: if policy:
default = defaultpolicy = defaultself(policy)):
        if (lambda self, policy: if policy:
default = defaultpolicy = defaultself(policy)):
            
            def __init__(self, policy):
                if policy:
                    default = default
                policy = default
                self(policy)

        if (lambda self, unixfrom, maxheaderlen, policy: policy = self.policy if policy else policyif maxheaderlen:
passmaxheaderlen = policy.max_line_lengthself(unixfrom, maxheaderlen, policy)):
            if (lambda self, unixfrom, maxheaderlen, policy: policy = self.policy if policy else policyif maxheaderlen:
passmaxheaderlen = policy.max_line_lengthself(unixfrom, maxheaderlen, policy)):
                
                def as_string(self, unixfrom, maxheaderlen, policy):
                    """Return the entire formatted message as a string.

Optional 'unixfrom', when true, means include the Unix From_ envelope
header.  maxheaderlen is retained for backward compatibility with the
base Message class, but defaults to None, meaning that the policy value
for max_line_length controls the header maximum length.  'policy' is
passed to the Generator instance used to serialize the message; if it
is not specified the policy associated with the message instance is
used.
"""
                    policy = self.policy if policy else policy
                    if maxheaderlen:
                        pass
                    maxheaderlen = policy.max_line_length
                    return self(unixfrom, maxheaderlen, policy)

            
            def __str__(self):
                return None(policy = self.policy.clone(utf8 = True))

            
            def is_attachment(self):
                c_d = self.get('content-disposition')
                if c_d:
                    pass
                return False
                return c_d.content_disposition == 'attachment'

    
    def _find_body(self, part, preferencelist):
        if None:
            pass
        if part.is_attachment():
            pass
        if part.is_attachment():
            pass
        return None
        if ():
            if maintype == 'text':
                if subtype in preferencelist:
                    if (preferencelist.index(subtype), part):
                        pass
                (preferencelist.index(subtype), part)
            return None
            if not maintype != 'multipart':
                if self.is_multipart():
                    pass
                if not self.is_multipart():
                    pass
        return None
        if subtype != 'related':
            for None in part.iter_parts():
                if None and None:
                    pass
        return None
        if 'related' in preferencelist:
            if (preferencelist.index('related'), part):
                pass
        (preferencelist.index('related'), part)
        None = ()
        start = part.get_param('start')
        if start:
            pass
        if start:
            for subpart in part.iter_parts():
                if not subpart['content-id'] == start:
                    continue
                candidate = subpart
                part.get_content_type().split('/')
        if candidate:
            subparts = part.get_payload()
            if subparts:
                pass
        candidate = subparts[0] if subparts else None
        if candidate:
            if None and None:
                pass
            continue
        return None
        return None
        continue
        continue

    if (lambda self, preferencelist: best_prio = len(preferencelist)body = Nonefor None in self._find_body(self, preferencelist):
if ():
if not prio < best_prio:
continuepart = prioif not prio == 0:
continuebodybody):
        
        def get_body(self, preferencelist):
            """Return best candidate mime part for display as 'body' of message.

Do a depth first search, starting with self, looking for the first part
matching each of the items in preferencelist, and return the part
corresponding to the first item that has a match, or None if no items
have a match.  If 'related' is not included in preferencelist, consider
the root part of any multipart/related encountered as a candidate
match.  Ignore parts with 'Content-Disposition: attachment'.
"""
            best_prio = len(preferencelist)
            body = None
            for None in self._find_body(self, preferencelist):
                if ():
                    if not prio < best_prio:
                        continue
                    part = prio
                    if not prio == 0:
                        continue
                    return body
                return body

    _body_types = {
        ('text', 'html'),
        ('text', 'plain'),
        ('multipart', 'related'),
        ('multipart', 'alternative')}
    
    def iter_attachments(self):
        """Return an iterator over the non-main parts of a multipart.

Skip the first of each occurrence of text/plain, text/html,
multipart/related, or multipart/alternative in the multipart (unless
they have a 'Content-Disposition: attachment' header) and include all
remaining subparts in the returned iterator.  When applied to a
multipart/related, return all parts except the root part.  Return an
empty iterator when applied to a multipart/alternative or a
non-multipart.
"""
        if None:
            pass
        if ():
            if maintype != 'multipart' or subtype == 'alternative':
                pass
            return None
        
        try:
            payload.copy() = self.get_payload()
        except AttributeError:
            parts

        if maintype == 'multipart' and subtype == 'related':
            start = self.get_param('start')
            if start:
                pass
            if start:
                found = False