# Source Generated with Decompyle++
# File: _encoded_words.marshal (Python 3.13)

'''Routines for manipulating RFC2047 encoded words.

This is currently a package-private API, but will be considered for promotion
to a public API if there is demand.

'''
import re
import base64
import binascii
import functools
from string import ascii_letters, digits
from email import errors
__all__ = [
    'decode_q',
    'encode_q',
    'decode_b',
    'encode_b',
    'len_q',
    'len_b',
    'decode',
    'encode']
_q_byte_subber = re.compile(None(b'=([a-fA-F0-9]{2})').sub, (lambda m: bytes.fromhex(m.group(1).decode())))

def decode_q(encoded):
    encoded = encoded.replace(b'_', b' ')
    return (_q_byte_subber(encoded), [])


def _QByteMap():
    '''_QByteMap'''
    __firstlineno__ = 73
    safe = digits.encode + None('ascii')
    
    def __missing__(self, key):
        if key in self.safe:
            self[key] = chr(key)
        return self[key]
        self[key] = '={:02X}'.format(key)
        return self[key]

    __static_attributes__ = ()

_QByteMap = None(_QByteMap, '_QByteMap', dict)

class _q_byte_map:
