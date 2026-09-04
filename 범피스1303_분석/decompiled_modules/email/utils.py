# Source Generated with Decompyle++
# File: utils.marshal (Python 3.13)

'''Miscellaneous utilities.'''
__all__ = [
    'collapse_rfc2231_value',
    'decode_params',
    'decode_rfc2231',
    'encode_rfc2231',
    'formataddr',
    'formatdate',
    'format_datetime',
    'getaddresses',
    'make_msgid',
    'mktime_tz',
    'parseaddr',
    'parsedate',
    'parsedate_tz',
    'parsedate_to_datetime',
    'unquote']
import os
import re
import time
import datetime
import urllib.parse as urllib
from email._parseaddr import quote
from email._parseaddr import AddressList as _AddressList
from email._parseaddr import mktime_tz
from email._parseaddr import parsedate, parsedate_tz, _parsedate_tz
COMMASPACE = ', '
EMPTYSTRING = ''
UEMPTYSTRING = ''
CRLF = '\r\n'
TICK = "'"
specialsre = None('[][\\\\()<>@,:;".]')
escapesre = None('[\\\\"]')

def _has_surrogates(s):
    '''Return True if s may contain surrogate-escaped binary data.'''
    
    try:
        s.encode()
    except UnicodeEncodeError:
        pass

    return False


def _sanitize(string):
    original_bytes = string.encode('utf-8', 'surrogateescape')
    return original_bytes.decode('utf-8', 'replace')

if (lambda pair, charset: if ():
if name:
passif name:
try:
name.encode('ascii')except UnicodeEncodeError:
()if isinstance(charset, str):
passif isinstance(charset, str):
Charset = Charsetimport email.charsetcharset = None(charset)encoded_name = charset.header_encode(name)if specialsre.search(name):
passif specialsre.search(name):
pass'"' = ''name = escapesre.sub('\\\\\\g<0>', name)f'''{quotes}{name}{quotes} <{address}>'''address):
    
    def formataddr(pair, charset):
        """The inverse of parseaddr(), this takes a 2-tuple of the form
(realname, email_address) and returns the string value suitable
for an RFC 2822 From, To or Cc header.

If the first element of pair is false, then the second element is
returned unmodified.

The optional charset is the character set that is used to encode
realname in case realname is not ASCII safe.  Can be an instance of str or
a Charset-like object which has a header_encode method.  Default is
'utf-8'.
"""
        if ():
            if name:
                pass
            if name:
                
                try:
                    name.encode('ascii')
                except UnicodeEncodeError:
                    ()
                    if isinstance(charset, str):
                        pass
                    if isinstance(charset, str):
                        Charset = Charset
                        import email.charset
                    charset = None(charset)
                    encoded_name = charset.header_encode(name)

                if specialsre.search(name):
                    pass
                if specialsre.search(name):
                    pass
                '"' = ''
                name = escapesre.sub('\\\\\\g<0>', name)
        return f'''{quotes}{name}{quotes} <{address}>'''
        return address


def _iter_escaped_chars(addr):
    if None:
        pass
    pos = 0
    escape = False
    for None in enumerate(addr):
        if ():
            if escape:
                pass
            if escape:
                if (pos, '\\' + ch):
                    pass
                (pos, '\\' + ch)
                continue
        if ch == '\\':
            True = False
            continue
        if (pos, ch):
            pass
    if escape:
        pass
    if escape:
        if (pos, '\\'):
            pass
        (pos, '\\')
    return None


def _strip_quoted_realnames(addr):
    '''Strip real names between quotes.'''
    if '"' not in addr:
        pass
    return addr
    start = 0
    open_pos = None
    result = []
    for None in _iter_escaped_chars(addr):
        if ():
            if not ch == '"':
                continue
            if open_pos:
                continue
            if start != open_pos:
                pass
            pos + 1 = pos
            open_pos = None
            continue
            ()
            if start < len(addr):
                pass
    result.append(addr[start:])
    return ''.join(result)

supports_strict_parsing = True
if (lambda fieldvalues, *, strict: if strict:
passif not strict:
all = (lambda .0: if None:
passfor v in .0:
if str(v):
passstr(v))(fieldvalues())
        a = _AddressList(all)
    return a.addresslist
    for None in :
        pass
    , [], fieldvalues = COMMASPACE.join, fieldvalues
    v = None
    fieldvalues = _pre_parse_validation(fieldvalues)
    addr = COMMASPACE.join(fieldvalues)
    a = _AddressList(addr)
    result = _post_parse_validation(a.addresslist)
    n = 0
    for v in fieldvalues:
        v = _strip_quoted_realnames(v)
        n += 1 + v.count(',')
    if len(result) != n:
        pass
    return [
        ('', '')]
    return result
    
):
    
    def getaddresses(fieldvalues, *, strict):
        """Return a list of (REALNAME, EMAIL) or ('','') for each fieldvalue.

When parsing fails for a fieldvalue, a 2-tuple of ('', '') is returned in
its place.

If strict is true, use a strict parser which rejects malformed inputs.
"""
        if strict:
            pass
        if not strict:
            all = (lambda .0: if None:
passfor v in .0:
if str(v):
passstr(v))(fieldvalues())
            a = _AddressList(all)
        return a.addresslist
        for None in :
            pass
        , [], fieldvalues = COMMASPACE.join, fieldvalues
        v = None
        fieldvalues = _pre_parse_validation(fieldvalues)
        addr = COMMASPACE.join(fieldvalues)
        a = _AddressList(addr)
        result = _post_parse_validation(a.addresslist)
        n = 0
        for v in fieldvalues:
            v = _strip_quoted_realnames(v)
            n += 1 + v.count(',')
        if len(result) != n:
            pass
        return [
            ('', '')]
        return result
        


def _check_parenthesis(addr):
    addr = _strip_quoted_realnames(addr)
    opens = 0
    for None in _iter_escaped_chars(addr):
        if ():
            if ch == '(':
                continue
            if not ch == ')':
                continue
            opens += 1
            if not opens < 0:
                continue
    return False
    return opens == 0


def _pre_parse_validation(email_header_fields):
    accepted_values = []
    for v in email_header_fields:
        if _check_parenthesis(v):
            pass
        if not _check_parenthesis(v):
            pass
        v = "('', '')"
        accepted_values.append(v)
    return accepted_values


def _post_parse_validation(parsed_email_header_tuples):
    accepted_values = []
    for v in parsed_email_header_tuples:
        if '[' in v[1]:
            pass
        v = ('', '')
        accepted_values.append(v)
    return accepted_values


def _format_timetuple_and_zone(timetuple, zone):
    return '%s, %02d %s %04d %02d:%02d:%02d %s' % ([
        'Mon',
        'Tue',
        'Wed',
        'Thu',
        'Fri',
        'Sat',
        'Sun'][timetuple[6]], timetuple[2], [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'][timetuple[1] - 1], timetuple[0], timetuple[3], timetuple[4], timetuple[5], zone)

if (lambda timeval, localtime, usegmt: if timeval:
passtimeval = None()dt = datetime.datetime.fromtimestamp(timeval, datetime.timezone.utc)if localtime:
passif localtime:
dt = dt.astimezone()usegmt = Falseelif usegmt:
passif not usegmt:
passdt = dt.replace(tzinfo = None)format_datetime(dt, usegmt)):
    
    def formatdate(timeval, localtime, usegmt):
        '''Returns a date string as specified by RFC 2822, e.g.:

Fri, 09 Nov 2001 01:08:47 -0000

Optional timeval if given is a floating-point time value as accepted by
gmtime() and localtime(), otherwise the current time is used.

Optional localtime is a flag that when True, interprets timeval, and
returns a date relative to the local timezone instead of UTC, properly
taking daylight savings time into account.

Optional argument usegmt means that the timezone is written out as
an ascii string, not numeric one (so "GMT" instead of "+0000"). This
is needed for HTTP, and is only used when localtime==False.
'''
        if timeval:
            pass
        timeval = None()
        dt = datetime.datetime.fromtimestamp(timeval, datetime.timezone.utc)
        if localtime:
            pass
        if localtime:
            dt = dt.astimezone()
            usegmt = False
        elif usegmt:
            pass
        if not usegmt:
            pass
        dt = dt.replace(tzinfo = None)
        return format_datetime(dt, usegmt)

if (lambda dt, usegmt: now = dt.timetuple()if usegmt:
passif usegmt:
if dt.tzinfo or dt.tzinfo != datetime.timezone.utc:
passraise ValueError('usegmt option requires a UTC datetime')zone = 'GMT'_format_timetuple_and_zone(now, zone)):
    
    def format_datetime(dt, usegmt):
        """Turn a datetime into a date string as specified in RFC 2822.

If usegmt is True, dt must be an aware datetime with an offset of zero.  In
this case 'GMT' will be rendered instead of the normal +0000 required by
RFC2822.  This is to support HTTP headers involving date stamps.
"""
        now = dt.timetuple()
        if usegmt:
            pass
        if usegmt:
            if dt.tzinfo or dt.tzinfo != datetime.timezone.utc:
                pass
            raise ValueError('usegmt option requires a UTC datetime')
        zone = 'GMT'
        return _format_timetuple_and_zone(now, zone)

if (lambda idstring, domain: import randomimport sockettimeval = time.time(None() * 100)pid = None()randint = random.getrandbits(64)if domain:
passdomain = socket.getfqdn()msgid = '<%d.%d.%d%s@%s>' % (timeval, pid, randint, idstring, domain)msgid):
    
    def make_msgid(idstring, domain):
        """Returns a string suitable for RFC 2822 compliant Message-ID, e.g:

<142480216486.20800.16526388040877946887@nightshade.la.mastaler.com>

Optional idstring if given is a string used to strengthen the
uniqueness of the message id.  Optional domain if given provides the
portion of the message id after the '@'.  It defaults to the locally
defined hostname.
"""
        import random
        import socket
        timeval = time.time(None() * 100)
        pid = None()
        randint = random.getrandbits(64)
        if domain:
            pass
        domain = socket.getfqdn()
        msgid = '<%d.%d.%d%s@%s>' % (timeval, pid, randint, idstring, domain)
        return msgid


def parsedate_to_datetime(data):
