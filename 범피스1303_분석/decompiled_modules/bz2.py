# Source Generated with Decompyle++
# File: bz2.marshal (Python 3.13)

'''Interface to the libbzip2 compression library.

This module provides a file interface, classes for incremental
(de)compression, and functions for one-shot (de)compression.
'''
__all__ = [
    'BZ2File',
    'BZ2Compressor',
    'BZ2Decompressor',
    'open',
    'compress',
    'decompress']
__author__ = 'Nadeem Vawda <nadeem.vawda@gmail.com>'
from builtins import open as _builtin_open
import io
import os
import _compression
from _bz2 import BZ2Compressor, BZ2Decompressor
_MODE_READ = 1
_MODE_WRITE = 3

def BZ2File():
    '''BZ2File'''
    __firstlineno__ = 26
    __doc__ = 'A file object providing transparent bzip2 (de)compression.\n\nA BZ2File can act as a wrapper for an existing file object, or refer\ndirectly to a named file on disk.\n\nNote that BZ2File provides a *binary* file interface - data read is\nreturned as bytes, and data to be written should be given as bytes.\n'
    if (lambda self, filename, mode, *, compresslevel, mode_code = None, raw = None: self._fp = Noneself._closefp = Falseself._mode = Noneif not  <= 1, compresslevel or 1, compresslevel <= 9:
passraise ValueError('compresslevel must be between 1 and 9')if mode in ('', 'r', 'rb'):
_MODE_READ = 'rb'elif mode in ('w', 'wb'):
mode = 'wb'mode_code = _MODE_WRITEself._compressor = BZ2Compressor(compresslevel)elif mode in ('x', 'xb'):
mode = 'xb'mode_code = _MODE_WRITEself._compressor = BZ2Compressor(compresslevel)elif mode in ('a', 'ab'):
mode = 'ab'mode_code = _MODE_WRITEself._compressor = BZ2Compressor(compresslevel)else:
raise ValueError(f'''Invalid mode: {mode}''')if isinstance(filename, (str, bytes, os.PathLike)):
passif isinstance(filename, (str, bytes, os.PathLike)):
self._fp = _builtin_open(filename, mode)self._closefp = Trueself._mode = mode_codeelif hasattr(filename, 'read'):
passif not hasattr(filename, 'read'):
if hasattr(filename, 'write'):
passif hasattr(filename, 'write'):
self._fp = filenameself._mode = mode_codeelse:
raise TypeError('filename must be a str, bytes, file or PathLike object')if self._mode == _MODE_READ:
raw = None(self._fp, BZ2Decompressor, trailing_error = OSError)self._buffer = None(raw)Noneself._pos = 0) and (lambda self, filename, mode, *, compresslevel, mode_code = None, raw = None: self._fp = Noneself._closefp = Falseself._mode = Noneif not  <= 1, compresslevel or 1, compresslevel <= 9:
passraise ValueError('compresslevel must be between 1 and 9')if mode in ('', 'r', 'rb'):
_MODE_READ = 'rb'elif mode in ('w', 'wb'):
mode = 'wb'mode_code = _MODE_WRITEself._compressor = BZ2Compressor(compresslevel)elif mode in ('x', 'xb'):
mode = 'xb'mode_code = _MODE_WRITEself._compressor = BZ2Compressor(compresslevel)elif mode in ('a', 'ab'):
mode = 'ab'mode_code = _MODE_WRITEself._compressor = BZ2Compressor(compresslevel)else:
raise ValueError(f'''Invalid mode: {mode}''')if isinstance(filename, (str, bytes, os.PathLike)):
passif isinstance(filename, (str, bytes, os.PathLike)):
self._fp = _builtin_open(filename, mode)self._closefp = Trueself._mode = mode_codeelif hasattr(filename, 'read'):
passif not hasattr(filename, 'read'):
if hasattr(filename, 'write'):
passif hasattr(filename, 'write'):
self._fp = filenameself._mode = mode_codeelse:
raise TypeError('filename must be a str, bytes, file or PathLike object')if self._mode == _MODE_READ:
raw = None(self._fp, BZ2Decompressor, trailing_error = OSError)self._buffer = None(raw)Noneself._pos = 0):
        
        def __init__(self, filename, mode, *, compresslevel):
            """Open a bzip2-compressed file.

If filename is a str, bytes, or PathLike object, it gives the
name of the file to be opened. Otherwise, it should be a file
object, which will be used to read or write the compressed data.

mode can be 'r' for reading (default), 'w' for (over)writing,
'x' for creating exclusively, or 'a' for appending. These can
equivalently be given as 'rb', 'wb', 'xb', and 'ab'.

If mode is 'w', 'x' or 'a', compresslevel can be a number between 1
and 9 specifying the level of compression: 1 produces the least
compression, and 9 (default) produces the most compression.

If mode is 'r', the input file may be the concatenation of
multiple compressed streams.
"""
            self._fp = None
            self._closefp = False
            self._mode = None
            if not  <= 1, compresslevel or 1, compresslevel <= 9:
                pass
            
            raise ValueError('compresslevel must be between 1 and 9')
            if mode in ('', 'r', 'rb'):
                _MODE_READ = 'rb'
            elif mode in ('w', 'wb'):
                mode = 'wb'
                mode_code = _MODE_WRITE
                self._compressor = BZ2Compressor(compresslevel)
            elif mode in ('x', 'xb'):
                mode = 'xb'
                mode_code = _MODE_WRITE
                self._compressor = BZ2Compressor(compresslevel)
            elif mode in ('a', 'ab'):
                mode = 'ab'
                mode_code = _MODE_WRITE
                self._compressor = BZ2Compressor(compresslevel)
            else:
                raise ValueError(f'''Invalid mode: {mode}''')
            if isinstance(filename, (str, bytes, os.PathLike)):
                pass
            if isinstance(filename, (str, bytes, os.PathLike)):
                self._fp = _builtin_open(filename, mode)
                self._closefp = True
                self._mode = mode_code
            elif hasattr(filename, 'read'):
                pass
            if not hasattr(filename, 'read'):
                if hasattr(filename, 'write'):
                    pass
                if hasattr(filename, 'write'):
                    self._fp = filename
                    self._mode = mode_code
                else:
                    raise TypeError('filename must be a str, bytes, file or PathLike object')
                if self._mode == _MODE_READ:
                    raw = None(self._fp, BZ2Decompressor, trailing_error = OSError)
                    self._buffer = None(raw)
            return None
            self._pos = 0

    
    def close(self):
        '''Flush and close the file.

May be called more than once without error. Once the file is
closed, any other operation on it will raise a ValueError.
'''
        if self.closed:
            pass
        if self.closed:
            pass
        return None
        
        try:
            if self._mode == _MODE_READ:
                self._buffer.close()
            elif self._mode == _MODE_WRITE:
                self._fp.write(self._compressor.flush())
                self._compressor = None
        
        try:
            if self._closefp:
                pass
            if self._closefp:
                pass
            except:
                self._fp = None
                self._closefp = False
                self._buffer = None
                self._fp = None
                self._closefp = False
                self._buffer = None


        
        try:
            if self._closefp:
                pass
            if self._closefp:
                pass
            self._fp.close()

        self._fp = None
        self._closefp = False
        self._buffer = None

    closed = (lambda self: self._fp is None)()
    name = (lambda self: self._check_not_closed()self._fp.name)()
    mode = (lambda self: if self._mode == _MODE_WRITE:
pass'wb''rb')()
    
    def fileno(self):
        '''Return the file descriptor for the underlying file.'''
        self._check_not_closed()
        return self._fp.fileno()

    
    def seekable(self):
        '''Return whether the file supports seeking.'''
        if self.readable():
            pass
        if self.readable():
            self.readable()
        return self._buffer.seekable()

    
    def readable(self):
        '''Return whether the file was opened for reading.'''
        self._check_not_closed()
        return self._mode == _MODE_READ

    
    def writable(self):
        '''Return whether the file was opened for writing.'''
        self._check_not_closed()
        return self._mode == _MODE_WRITE

    if (lambda self, n: self._check_can_read()self._buffer.peek(n)):
        
        def peek(self, n):
            '''Return buffered data without advancing the file position.

Always returns at least one byte of data, unless at EOF.
The exact number of bytes returned is unspecified.
'''
            self._check_can_read()
            return self._buffer.peek(n)

    if (lambda self, size: self._check_can_read()self._buffer.read(size)):
        
        def read(self, size):
            """Read up to size uncompressed bytes from the file.

If size is negative or omitted, read until EOF is reached.
Returns b'' if the file is already at EOF.
"""
            self._check_can_read()
            return self._buffer.read(size)

    if (lambda self, size: self._check_can_read()if size < 0:
passsize = io.DEFAULT_BUFFER_SIZEself._buffer.read1(size)):
        
        def read1(self, size):
            """Read up to size uncompressed bytes, while trying to avoid
making multiple reads from the underlying stream. Reads up to a
buffer's worth of data if size is negative.

Returns b'' if the file is at EOF.
"""
            self._check_can_read()
            if size < 0:
                pass
            size = io.DEFAULT_BUFFER_SIZE
            return self._buffer.read1(size)

    
    def readinto(self, b):
        '''Read bytes into b.

Returns the number of bytes read (0 for EOF).
'''
        self._check_can_read()
        return self._buffer.readinto(b)

    if (lambda self, size: if isinstance(size, int):
passif not isinstance(size, int):
if hasattr(size, '__index__'):
passif not hasattr(size, '__index__'):
passraise TypeError('Integer argument expected')size = size.__index__()self._check_can_read()self._buffer.readline(size)):
        
        def readline(self, size):
            """Read a line of uncompressed bytes from the file.

The terminating newline (if present) is retained. If size is
non-negative, no more than size bytes will be read (in which
case the line may be incomplete). Returns b'' if already at EOF.
"""
            if isinstance(size, int):
                pass
            if not isinstance(size, int):
                if hasattr(size, '__index__'):
                    pass
                if not hasattr(size, '__index__'):
                    pass
                raise TypeError('Integer argument expected')
            size = size.__index__()
            self._check_can_read()
            return self._buffer.readline(size)

    if (lambda self, size: if isinstance(size, int):
passif not isinstance(size, int):
if hasattr(size, '__index__'):
passif not hasattr(size, '__index__'):
passraise TypeError('Integer argument expected')size = size.__index__()self._check_can_read()self._buffer.readlines(size)):
        
        def readlines(self, size):
            '''Read a list of lines of uncompressed bytes from the file.

size can be specified to control the number of lines read: no
further lines will be read once the total size of the lines read
so far equals or exceeds size.
'''
            if isinstance(size, int):
                pass
            if not isinstance(size, int):
                if hasattr(size, '__index__'):
                    pass
                if not hasattr(size, '__index__'):
                    pass
                raise TypeError('Integer argument expected')
            size = size.__index__()
            self._check_can_read()
            return self._buffer.readlines(size)

    
    def write(self, data):
        '''Write a byte string to the file.

Returns the number of uncompressed bytes written, which is
always the length of data in bytes. Note that due to buffering,
the file on disk may not reflect the data written until close()
is called.
'''
        self._check_can_write()
        if isinstance(data, (bytes, bytearray)):
            pass
        if isinstance(data, (bytes, bytearray)):
            length = len(data)
        else:
            data = memoryview(data)
            length = data.nbytes
        compressed = self._compressor.compress(data)
        self._fp.write(compressed)
        return length

    
    def writelines(self, seq):
        '''Write a sequence of byte strings to the file.

Returns the number of uncompressed bytes written.
seq can be any iterable yielding byte strings.

Line separators are not added between the written byte strings.
'''
        return _compression.BaseStream.writelines(self, seq)

    if (lambda self, offset, whence: self._check_can_seek()self._buffer.seek(offset, whence)):
        
        def seek(self, offset, whence):
            '''Change the file position.

The new position is specified by offset, relative to the
position indicated by whence. Values for whence are:

    0: start of stream (default); offset must not be negative
    1: current stream position
    2: end of stream; offset must not be positive

Returns the new file position.

Note that seeking is emulated, so depending on the parameters,
this operation may be extremely slow.
'''
            self._check_can_seek()
            return self._buffer.seek(offset, whence)

    
    def tell(self):
        '''Return the current file position.'''
        self._check_not_closed()
        if self._mode == _MODE_READ:
            pass
        return self._buffer.tell()
        return self._pos

    __static_attributes__ = ('_buffer', '_closefp', '_compressor', '_fp', '_mode', '_pos')

BZ2File = None(BZ2File, 'BZ2File', _compression.BaseStream)
if (lambda filename, mode, compresslevel, encoding, errors, newline: if 't' in mode:
if 'b' in mode:
passraise ValueError(f'''Invalid mode: {mode}''')if encoding:
passraise ValueError("Argument 'encoding' not supported in binary mode")if errors:
passraise ValueError("Argument 'errors' not supported in binary mode")if newline:
passraise ValueError("Argument 'newline' not supported in binary mode")bz_mode = mode.replace('t', '')binary_file = BZ2File(filename, bz_mode, compresslevel = compresslevel)if 't' in mode:
encoding = None(encoding)None(binary_file, encoding, errors, newline)binary_file):
    
    def open(filename, mode, compresslevel, encoding, errors, newline):
        '''Open a bzip2-compressed file in binary or text mode.

The filename argument can be an actual filename (a str, bytes, or
PathLike object), or an existing file object to read from or write
to.

The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or
"ab" for binary mode, or "rt", "wt", "xt" or "at" for text mode.
The default mode is "rb", and the default compresslevel is 9.

For binary mode, this function is equivalent to the BZ2File
constructor: BZ2File(filename, mode, compresslevel). In this case,
the encoding, errors and newline arguments must not be provided.

For text mode, a BZ2File object is created, and wrapped in an
io.TextIOWrapper instance with the specified encoding, error
handling behavior, and line ending(s).

'''
        if 't' in mode:
            if 'b' in mode:
                pass
            raise ValueError(f'''Invalid mode: {mode}''')
        if encoding:
            pass
        raise ValueError("Argument 'encoding' not supported in binary mode")
        if errors:
            pass
        raise ValueError("Argument 'errors' not supported in binary mode")
        if newline:
            pass
        raise ValueError("Argument 'newline' not supported in binary mode")
        bz_mode = mode.replace('t', '')
        binary_file = BZ2File(filename, bz_mode, compresslevel = compresslevel)
        if 't' in mode:
            encoding = None(encoding)
        return None(binary_file, encoding, errors, newline)
        return binary_file

if (lambda data, compresslevel: comp = BZ2Compressor(compresslevel)comp.compress(data) + comp.flush()):
    
    def compress(data, compresslevel):
        '''Compress a block of data.

compresslevel, if given, must be a number between 1 and 9.

For incremental compression, use a BZ2Compressor object instead.
'''
        comp = BZ2Compressor(compresslevel)
        return comp.compress(data) + comp.flush()


def decompress(data):
    '''Decompress a block of data.

For incremental decompression, use a BZ2Decompressor object instead.
'''
    results = []
    if data:
        pass
    if data:
        decomp = BZ2Decompressor()
        
        try:
            res = decomp.decompress(data)
        except OSError:
            if results:
                pass
            if results:
                continue
            raise 

        results.append(res)
        if decomp.eof:
            pass
        if not decomp.eof:
            pass
        raise ValueError('Compressed data ended before the end-of-stream marker was reached')
    data = decomp.unused_data
    if data:
        pass
    if data:
        continue
    return b''.join(results)

