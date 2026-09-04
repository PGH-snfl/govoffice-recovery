# Source Generated with Decompyle++
# File: generator.marshal (Python 3.13)

'''Classes to generate plain text from a message object tree.'''
__all__ = [
    'Generator',
    'DecodedGenerator',
    'BytesGenerator']
import re
import sys
import time
import random
from copy import deepcopy
from io import StringIO, BytesIO
from email.utils import _has_surrogates
from email.errors import HeaderWriteError
UNDERSCORE = '_'
NL = '\n'
NLCRE = None('\\r\\n|\\r|\\n')
fcre = None('^From ', re.MULTILINE)
NEWLINE_WITHOUT_FWSP = None('\\r\\n[^ \\t]|\\r[^ \\n\\t]|\\n[^ \\t]')

def Generator():
    '''Generator'''
    __firstlineno__ = 27
    __doc__ = 'Generates output from a Message object tree.\n\nThis basic generator writes the message to the given file object as plain\ntext.\n'
    if (lambda self, outfp, mangle_from_, maxheaderlen, *, policy, 