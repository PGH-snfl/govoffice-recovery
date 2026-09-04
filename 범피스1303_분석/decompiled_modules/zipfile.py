# Source Generated with Decompyle++
# File: zipfile.marshal (Python 3.13)

'''
Read and write ZIP files.

XXX references to utf-8 need further investigation.
'''
import binascii
import importlib.util as importlib
import io
import os
import shutil
import stat
import struct
import sys
import threading
import time

try:
    import zlib
    crc32 = zlib.crc32
except ImportError:
    (None,)
    zlib = None
    crc32 = binascii.crc32


try:
    import bz2
except ImportError:
    <NODE:27>
    bz2 = None


try:
    import lzma
except ImportError:
    <NODE:27>
    lzma = None

__all__ = [
    'BadZipFile',
    'BadZipfile',
    'error',
    'ZIP_STORED',
    'ZIP_DEFLATED',
    'ZIP_BZIP2',
    'ZIP_LZMA',
    'is_zipfile',
    'ZipInfo',
    'ZipFile',
    'PyZipFile',
    'LargeZipFile',
    'Path']

def BadZipFile():
    '''BadZipFile'''
    __firstlineno__ = 39
    __static_attributes__ = ()

BadZipFile = None(BadZipFile, 'BadZipFile', Exception)

def LargeZipFile():
    '''LargeZipFile'''
    __firstlineno__ = 43
    __doc__ = '\nRaised when writing a zipfile, the zipfile requires ZIP64 extensions\nand those extensions are disabled.\n'
    __static_attributes__ = ()

LargeZipFile = None(LargeZipFile, 'LargeZipFile', Exception)
error = BadZipFile
BadZipfile = BadZipFile
ZIP64_LIMIT = 2147483647
ZIP_FILECOUNT_LIMIT = 65535
ZIP_MAX_COMMENT = 65535
ZIP_STORED = 0
ZIP_DEFLATED = 8
ZIP_BZIP2 = 12
ZIP_LZMA = 14
DEFAULT_VERSION = 20
ZIP64_VERSION = 45
BZIP2_VERSION = 46
LZMA_VERSION = 63
MAX_EXTRACT_VERSION = 63
structEndArchive = b'<4s4H2LH'
stringEndArchive = b'PK\x05\x06'

class sizeEndCentDir(structEndArchive):
