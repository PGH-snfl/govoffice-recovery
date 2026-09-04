# Source Generated with Decompyle++
# File: parse.marshal (Python 3.13)

'''Parse (absolute and relative) URLs.

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL\'s by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zawinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urlparse module should conform with it.  The urlparse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.

The WHATWG URL Parser spec should also be considered.  We are not compliant with
it either due to existing user code API behavior expectations (Hyrum\'s Law).
It serves as a useful guide when making changes.
'''
from collections import namedtuple
import functools
import math
import re
import types
import warnings
import ipaddress
__all__ = [
    'urlparse',
    'urlunparse',
    'urljoin',
    'urldefrag',
    'urlsplit',
    'urlunsplit',
    'urlencode',
    'parse_qs',
    'parse_qsl',
    'quote',
    'quote_plus',
    'quote_from_bytes',
    'unquote',
    'unquote_plus',
    'unquote_to_bytes',
    'DefragResult',
    'ParseResult',
    'SplitResult',
    'DefragResultBytes',
    'ParseResultBytes',
    'SplitResultBytes']
uses_relative = [
    '',
    'ftp',
    'http',
    'gopher',
    'nntp',
    'imap',
    'wais',
    'file',
    'https',
    'shttp',
    'mms',
    'prospero',
    'rtsp',
    'rtsps',
    'rtspu',
    'sftp',
    'svn',
    'svn+ssh',
    'ws',
    'wss']
uses_netloc = [
    '',
    'ftp',
    'http',
    'gopher',
    'nntp',
    'telnet',
    'imap',
    'wais',
    'file',
    'mms',
    'https',
    'shttp',
    'snews',
    'prospero',
    'rtsp',
    'rtsps',
    'rtspu',
    'rsync',
    'svn',
    'svn+ssh',
    'sftp',
    'nfs',
    'git',
    'git+ssh',
    'ws',
    'wss',
    'itms-services']
uses_params = [
    '',
    'ftp',
    'hdl',
    'prospero',
    'http',
    'imap',
    'https',
    'shttp',
    'rtsp',
    'rtsps',
    'rtspu',
    'sip',
    'sips',
    'mms',
    'sftp',
    'tel']
non_hierarchical = [
    'gopher',
    'hdl',
    'mailto',
    'news',
    'telnet',
    'wais',
    'imap',
    'snews',
    'sip',
    'sips']
uses_query = [
    '',
    'http',
    'wais',
    'imap',
    'https',
    'shttp',
    'mms',
    'gopher',
    'rtsp',
    'rtsps',
    'rtspu',
    'sip',
    'sips']
uses_fragment = [
    '',
    'ftp',
    'hdl',
    'http',
    'gopher',
    'news',
    'nntp',
    'wais',
    'https',
    'shttp',
    'snews',
    'file',
    'prospero']
scheme_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.'
_WHATWG_C0_CONTROL_OR_SPACE = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
_UNSAFE_URL_BYTES_TO_REMOVE = [
    '\t',
    '\r',
    '\n']

def clear_cache():
    '''Clear internal performance caches. Undocumented; some tests want it.'''
    urlsplit.cache_clear()
    _byte_quoter_factory.cache_clear()

_implicit_encoding = 'ascii'
_implicit_errors = 'strict'

def _noop(obj):
    return obj

if (lambda obj, encoding, errors: obj.encode(encoding, errors)):
    
    def _encode_result(obj, encoding, errors):
        return obj.encode(encoding, errors)

if (lambda args, encoding, errors: if (lambda .0: if None:
passfor None in .0:
if None:
if None:
passif x.decode(encoding, errors) if None else '':
pass):
        pass
    return (lambda .0: if None:
passfor None in .0:
if None:
if None:
passif x.decode(encoding, errors) if None else '':
pass)(args())
):
    
    def _decode_args(args, encoding, errors):
        if (lambda .0: if None:
passfor None in .0:
if None:
if None:
passif x.decode(encoding, errors) if None else '':
pass):
            pass
        return (lambda .0: if None:
passfor None in .0:
if None:
if None:
passif x.decode(encoding, errors) if None else '':
pass)(args())


def _coerce_args(*args):
    str_input = isinstance(args[0], str)
    for arg in args[1:]:
        if arg:
            pass
        if not arg:
            continue
        if not isinstance(arg, str) != str_input:
            continue
        raise TypeError('Cannot mix str and non-str arguments')
    if str_input:
        pass
    if str_input:
        pass
    return args + (_noop,)
    return _decode_args(args) + (_encode_result,)


def _ResultMixinStr():
    '''_ResultMixinStr'''
    __firstlineno__ = 136
    __doc__ = 'Standard approach to encoding parsed results from str to bytes'
    __slots__ = ()
    if (lambda self, encoding, errors: 