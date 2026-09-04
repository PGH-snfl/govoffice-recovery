# Source Generated with Decompyle++
# File: parser.marshal (Python 3.13)

'''A parser of RFC 2822 and MIME email messages.'''
__all__ = [
    'Parser',
    'HeaderParser',
    'BytesParser',
    'BytesHeaderParser',
    'FeedParser',
    'BytesFeedParser']
from io import StringIO, TextIOWrapper
from email.feedparser import FeedParser, BytesFeedParser
from email._policybase import compat32

def Parser():
    '''Parser'''
    __firstlineno__ = 16
    if (lambda self, _class, *, policy, 