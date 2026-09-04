# Source Generated with Decompyle++
# File: gzip.marshal (Python 3.13)

"""Functions that read and write gzipped files.

The user of the file doesn't have to worry about the compression,
but random access is not allowed."""
import _compression
import builtins
import io
import os
import struct
import sys
import time
import weakref
import zlib
__all__ = [
    'BadGzipFile',
    'GzipFile',
    'open',
    'compress',
    'decompress']
(FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT) = (1, 2, 4, 8, 16)
READ = 'rb'
WRITE = 'wb'
_COMPRESS_LEVEL_FAST = 1
_COMPRESS_LEVEL_TRADEOFF = 6
_COMPRESS_LEVEL_BEST = 9
READ_BUFFER_SIZE = 131072
_WRITE_BUFFER_SIZE = 4 * io.DEFAULT_BUFFER_SIZE
if (lambda filename, mode, compresslevel, encoding, errors, newline: if 't' in mode:
if 'b' in mode:
passraise ValueError(f'''Invalid mode: {mode}''')if encoding:
passraise ValueError("Argument 'encoding' not supported in binary mode")if errors:
passraise ValueError("Argument 'errors' not supported in binary mode")if newline:
passraise ValueError("Argument 'newline' not supported in binary mode")gz_mode = mode.replace('t', '')if isinstance(filename, (str, bytes, os.PathLike)):
passif isinstance(filename, (str, bytes, os.PathLike)):
binary_file = GzipFile(filename, gz_mode, compresslevel)elif hasattr(filename, 'read'):
passif not hasattr(filename, 'read'):
if hasattr(filename, 'write'):
passif hasattr(filename, 'write'):
binary_file = GzipFile(None, gz_mode, compresslevel, filename)else:
raise TypeError('filename must be a str or bytes object, or a file')if 't' in mode:
encoding = None(encoding)None(binary_file, encoding, errors, newline)binary_file):
    
    def open(filename, mode, compresslevel, encoding, errors, newline):
        '''Open a gzip-compressed file in binary or text mode.

The filename argument can be an actual filename (a str or bytes object), or
an existing file object to read from or write to.

The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or "ab" for
binary mode, or "rt", "wt", "xt" or "at" for text mode. The default mode is
"rb", and the default compresslevel is 9.

For binary mode, this function is equivalent to the GzipFile constructor:
GzipFile(filename, mode, compresslevel). In this case, the encoding, errors
and newline arguments must not be provided.

For text mode, a GzipFile object is created, and wrapped in an
io.TextIOWrapper instance with the specified encoding, error handling
behavior, and line ending(s).

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
        gz_mode = mode.replace('t', '')
        if isinstance(filename, (str, bytes, os.PathLike)):
            pass
        if isinstance(filename, (str, bytes, os.PathLike)):
            binary_file = GzipFile(filename, gz_mode, compresslevel)
        elif hasattr(filename, 'read'):
            pass
        if not hasattr(filename, 'read'):
            if hasattr(filename, 'write'):
                pass
            if hasattr(filename, 'write'):
                binary_file = GzipFile(None, gz_mode, compresslevel, filename)
            else:
                raise TypeError('filename must be a str or bytes object, or a file')
            if 't' in mode:
                encoding = None(encoding)
        return None(binary_file, encoding, errors, newline)
        return binary_file


def write32u(output, value):
    struct.pack(None('<L', value))


def _PaddedFile():
    '''_PaddedFile'''
    __firstlineno__ = 83
    __doc__ = "Minimal read-only file object that prepends a string to the contents\nof an actual file. Shouldn't be used outside of gzip.py, as it lacks\nessential functionality."
    if (lambda self, f, prepend: self._buffer = prependself._length = len(prepend)self.file = fself._read = 0):
        
        def __init__(self, f, prepend):
            self._buffer = prepend
            self._length = len(prepend)
            self.file = f
            self._read = 0

    
    def read(self, size):
        if self._read:
            pass
        return self.file.read(size)
        if self._read + size <= self._length:
            read = self._read
        return self._buffer[read:self._read]
        self._read = self, self._read += size, ._read
        self._read = None
        return self._buffer[read:] + self.file.read((size - self._length) + read)

    if (lambda self, prepend: len(self._buffer) = self._read if self._read else self, self._read -= len(prepend), ._readself._read = 0):
        
        def prepend(self, prepend):
            len(self._buffer) = self._read if self._read else self, self._read -= len(prepend), ._read
            self._read = 0

    
    def seek(self, off):
        self._read = None
        self._buffer = None
        return self.file.seek(off)

    
    def seekable(self):
        return True

    __static_attributes__ = ('_buffer', '_length', '_read', 'file')

_PaddedFile = None(_PaddedFile, '_PaddedFile')

def BadGzipFile():
    '''BadGzipFile'''
    __firstlineno__ = 125
    __doc__ = 'Exception raised in some cases for invalid gzip files.'
    __static_attributes__ = ()

BadGzipFile = None(BadGzipFile, 'BadGzipFile', OSError)

def _WriteBufferStream():
    '''_WriteBufferStream'''
    __firstlineno__ = 129
    __doc__ = 'Minimal object to pass WriteBuffer flushes into GzipFile'
    
    def __init__(self, gzip_file):
        self.gzip_file = None(gzip_file)

    
    def write(self, data):
        gzip_file = self.gzip_file()
        if gzip_file:
            pass
        raise RuntimeError('lost gzip_file')
        return gzip_file._write_raw(data)

    
    def seekable(self):
        return False

    
    def writable(self):
        return True

    __static_attributes__ = ('gzip_file',)

_WriteBufferStream = None(_WriteBufferStream, '_WriteBufferStream', io.RawIOBase)

def GzipFile():
    '''GzipFile'''
    __firstlineno__ = 147
    __doc__ = 'The GzipFile class simulates most of the methods of a file object with\nthe exception of the truncate() method.\n\nThis class only supports opening files in binary mode. If you need to open a\ncompressed file in text mode, use the gzip.open() function.\n\n'
    myfileobj = None
    if (lambda self, filename, mode, compresslevel, fileobj, mtime: if mode:
passif mode:
if 't' in mode or 'U' in mode:
passraise ValueError('Invalid mode: {!r}'.format(mode))if mode:
passif mode and 'b' not in mode:
passmode += 'b'try:
if fileobj:
if mode:
passif not mode:
modeif None(filename, 'rb'):
None(filename, 'rb').myfileobj = None(filename, 'rb')origmode = modeif mode:
passmode = getattr(fileobj, 'mode', 'rb')if mode.startswith('r'):
passif mode.startswith('r'):
self.mode = READraw = _GzipReader(fileobj)self._buffer = None(raw)self.name = filenameelif mode.startswith(('w', 'a', 'x')):
passif mode.startswith(('w', 'a', 'x')):
if origmode:
import warningswarnings.warn('GzipFile was opened for writing, but this will change in future Python releases.  Specify the mode argument for opening it for writing.', FutureWarning, 2)self.mode = WRITEself._init_write(filename)self.compress = None(compresslevel, zlib.DEFLATED, -(zlib.MAX_WBITS), zlib.DEF_MEM_LEVEL, 0)self._write_mtime = mtimeself._buffer_size = _WRITE_BUFFER_SIZEself._buffer = None(_WriteBufferStream(self), buffer_size = self._buffer_size)else:
raise ValueError('Invalid mode: {!r}'.format(mode))self.fileobj = fileobjif self.mode == WRITE:
self._write_gzip_header(compresslevel)NoneNoneio.BufferedWriterself._close()raise ):
        
        def __init__(self, filename, mode, compresslevel, fileobj, mtime):
            """Constructor for the GzipFile class.

At least one of fileobj and filename must be given a
non-trivial value.

The new class instance is based on fileobj, which can be a regular
file, an io.BytesIO object, or any other object which simulates a file.
It defaults to None, in which case filename is opened to provide
a file object.

When fileobj is not None, the filename argument is only used to be
included in the gzip file header, which may include the original
filename of the uncompressed file.  It defaults to the filename of
fileobj, if discernible; otherwise, it defaults to the empty string,
and in this case the original filename is not included in the header.

The mode argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb', 'x', or
'xb' depending on whether the file will be read or written.  The default
is the mode of fileobj if discernible; otherwise, the default is 'rb'.
A mode of 'r' is equivalent to one of 'rb', and similarly for 'w' and
'wb', 'a' and 'ab', and 'x' and 'xb'.

The compresslevel argument is an integer from 0 to 9 controlling the
level of compression; 1 is fastest and produces the least compression,
and 9 is slowest and produces the most compression. 0 is no compression
at all. The default is 9.

The optional mtime argument is the timestamp requested by gzip. The time
is in Unix format, i.e., seconds since 00:00:00 UTC, January 1, 1970.
If mtime is omitted or None, the current time is used. Use mtime = 0
to generate a compressed stream that does not depend on creation time.

"""
            if mode:
                pass
            if mode:
                if 't' in mode or 'U' in mode:
                    pass
            raise ValueError('Invalid mode: {!r}'.format(mode))
            if mode:
                pass
            if mode and 'b' not in mode:
                pass
            mode += 'b'
            
            try:
                if fileobj:
                    if mode:
                        pass
                    if not mode:
                        mode
                    if None(filename, 'rb'):
                        None(filename, 'rb').myfileobj = None(filename, 'rb')
                origmode = mode
                if mode:
                    pass
                mode = getattr(fileobj, 'mode', 'rb')
                if mode.startswith('r'):
                    pass
                if mode.startswith('r'):
                    self.mode = READ
                    raw = _GzipReader(fileobj)
                    self._buffer = None(raw)
                    self.name = filename
                elif mode.startswith(('w', 'a', 'x')):
                    pass
                if mode.startswith(('w', 'a', 'x')):
                    if origmode:
                        import warnings
                    warnings.warn('GzipFile was opened for writing, but this will change in future Python releases.  Specify the mode argument for opening it for writing.', FutureWarning, 2)
                    self.mode = WRITE
                    self._init_write(filename)
                    self.compress = None(compresslevel, zlib.DEFLATED, -(zlib.MAX_WBITS), zlib.DEF_MEM_LEVEL, 0)
                    self._write_mtime = mtime
                    self._buffer_size = _WRITE_BUFFER_SIZE
                    self._buffer = None(_WriteBufferStream(self), buffer_size = self._buffer_size)
                else:
                    raise ValueError('Invalid mode: {!r}'.format(mode))
                self.fileobj = fileobj
                if self.mode == WRITE:
                    self._write_gzip_header(compresslevel)

            return None
            return None
            io.BufferedWriter
            self._close()
            raise 

    mtime = (lambda self: self._buffer.raw._last_mtime)()
    
    def __repr__(self):
        s = repr(self.fileobj)
        return '<gzip ' + s[1:-1] + ' ' + hex(id(self)) + '>'

    
    def _init_write(self, filename):
        self.name = filename
        self.crc = None(b'')
        self.size = 0
        self.writebuf = []
        self.bufsize = 0
        self.offset = 0

    if (lambda self: self._check_not_closed()self._buffer.flush()self()):
        
        def tell(self):
            self._check_not_closed()
            self._buffer.flush()
            return self()

        
        def _write_gzip_header(self, compresslevel):
            self.fileobj.write(b'\x1f\x8b')
            self.fileobj.write(b'\x08')
            
            try:
                fname = os.path.basename(self.name)
                if isinstance(fname, bytes):
                    pass
                if not isinstance(fname, bytes):
                    pass
                fname = fname.encode('latin-1')
                if fname.endswith(b'.gz'):
                    pass
                if fname.endswith(b'.gz'):
                    pass
                fname = fname[:-3]
            except UnicodeEncodeError:
                time.time
                fname = b''

            flags = 0
            if fname:
                pass
            if fname:
                pass
            flags = FNAME
            self.fileobj.write(chr(flags).encode('latin-1'))
            mtime = self._write_mtime
            if mtime:
                pass
            mtime = None()
            write32u(self.fileobj, int(mtime))
            if compresslevel == _COMPRESS_LEVEL_BEST:
                xfl = b'\x02'
            elif compresslevel == _COMPRESS_LEVEL_FAST:
                xfl = b'\x04'
            else:
                xfl = b'\x00'
            self.fileobj.write(xfl)
            self.fileobj.write(b'\xff')
            if fname:
                pass
            if fname:
                self.fileobj.write(fname + b'\x00')
            return None

        
        def write(self, data):
            self._check_not_closed()
            if self.mode != WRITE:
                import errno
            raise OSError(errno.EBADF, 'write() on read-only GzipFile object')
            if self.fileobj:
                pass
            raise ValueError('write() on closed GzipFile object')
            return self._buffer.write(data)

    
    def _write_raw(self, data):
        if isinstance(data, (bytes, bytearray)):
            pass
        if isinstance(data, (bytes, bytearray)):
            length = len(data)
        else:
            data = memoryview(data)
            length = data.nbytes
        if length > 0:
            self.fileobj.write(self.compress.compress(data))
            None(data, self.crc) = zlib.crc32
        return length

    if (lambda self, size: self._check_not_closed()if self.mode != READ:
import errnoraise OSError(errno.EBADF, 'read() on write-only GzipFile object')self._buffer.read(size)):
        
        def read(self, size):
            self._check_not_closed()
            if self.mode != READ:
                import errno
            raise OSError(errno.EBADF, 'read() on write-only GzipFile object')
            return self._buffer.read(size)

    if (lambda self, size: self._check_not_closed()if self.mode != READ:
import errnoraise OSError(errno.EBADF, 'read1() on write-only GzipFile object')if size < 0:
passsize = io.DEFAULT_BUFFER_SIZEself._buffer.read1(size)):
        
        def read1(self, size):
            """Implements BufferedIOBase.read1()

Reads up to a buffer's worth of data if size is negative."""
            self._check_not_closed()
            if self.mode != READ:
                import errno
            raise OSError(errno.EBADF, 'read1() on write-only GzipFile object')
            if size < 0:
                pass
            size = io.DEFAULT_BUFFER_SIZE
            return self._buffer.read1(size)

    
    def peek(self, n):
        self._check_not_closed()
        if self.mode != READ:
            import errno
        raise OSError(errno.EBADF, 'peek() on write-only GzipFile object')
        return self._buffer.peek(n)

    closed = (lambda self: self.fileobj is None)()
    
    def close(self):
        fileobj = self.fileobj
        if fileobj:
            if self._buffer.closed:
                pass
            if self._buffer.closed:
                pass
        return None
        
        try:
            if self.mode == WRITE:
                self._buffer.flush()
                fileobj.write(self.compress.flush())
                write32u(fileobj, self.crc)
                write32u(fileobj, self.size & 0xFFFFFFFF)
            elif self.mode == READ:
                pass
            self._buffer.close()
        except:
            pass

        self._close()

    
    def _close(self):
        self.fileobj = None
        myfileobj = self.myfileobj
        if myfileobj:
            self.myfileobj = None
        return None

    if (lambda self, zlib_mode: self._check_not_closed()if self.mode == WRITE:
self._buffer.flush()self.fileobj.write(self.compress.flush(zlib_mode))self.fileobj.flush()None):
        
        def flush(self, zlib_mode):
            self._check_not_closed()
            if self.mode == WRITE:
                self._buffer.flush()
                self.fileobj.write(self.compress.flush(zlib_mode))
                self.fileobj.flush()
            return None

    
    def fileno(self):
        """Invoke the underlying file object's fileno() method.

This will raise AttributeError if the underlying file object
doesn't support fileno().
"""
        return self.fileobj.fileno()

    
    def rewind(self):
        '''Return the uncompressed stream file position indicator to the
beginning of the file'''
        if self.mode != READ:
            pass
        raise OSError("Can't rewind in write mode")
        self._buffer.seek(0)

    
    def readable(self):
        return self.mode == READ

    
    def writable(self):
        return self.mode == WRITE

    
    def seekable(self):
        return True

    if (lambda self, offset, whence: if self.mode == WRITE:
self._check_not_closed()self._buffer.flush()if whence != io.SEEK_SET:
if whence == io.SEEK_CUR:
offset = self.offset + offsetelse:
raise ValueError('Seek from end not supported')if offset < self.offset:
passraise OSError('Negative seek in write mode')count = offset - self.offsetchunk = b'\x00' * self._buffer_sizefor i in range(count // self._buffer_size):
self.write(chunk)self.write(b'\x00' * (count % self._buffer_size))self.offsetif self.mode == READ:
self._check_not_closed()self._buffer.seek(offset, whence)self.offset):
        
        def seek(self, offset, whence):
            if self.mode == WRITE:
                self._check_not_closed()
                self._buffer.flush()
                if whence != io.SEEK_SET:
                    if whence == io.SEEK_CUR:
                        offset = self.offset + offset
                    else:
                        raise ValueError('Seek from end not supported')
                    if offset < self.offset:
                        pass
                raise OSError('Negative seek in write mode')
            count = offset - self.offset
            chunk = b'\x00' * self._buffer_size
            for i in range(count // self._buffer_size):
                self.write(chunk)
            self.write(b'\x00' * (count % self._buffer_size))
            return self.offset
            if self.mode == READ:
                self._check_not_closed()
            return self._buffer.seek(offset, whence)
            return self.offset

    if (lambda self, size: self._check_not_closed()self._buffer.readline(size)):
        
        def readline(self, size):
            self._check_not_closed()
            return self._buffer.readline(size)

    __static_attributes__ = ('_buffer', '_buffer_size', '_write_mtime', 'bufsize', 'compress', 'crc', 'fileobj', 'mode', 'myfileobj', 'name', 'offset', 'size', 'writebuf')
    __classcell__ = __class__
    return __class__

GzipFile = None(GzipFile, 'GzipFile', _compression.BaseStream)

def _read_exact(fp, n):
    '''Read exactly *n* bytes from `fp`

This method is required because fp may be unbuffered,
i.e. return short reads.
'''
    data = fp.read(n)
    if len(data) < n:
        b = fp.read(n - len(data))
        if b:
            pass
        if not b:
            pass
        raise EOFError('Compressed file ended before the end-of-stream marker was reached')
    data += b
    if len(data) < n:
        continue
    return data


def _read_gzip_header(fp):
    '''Read a gzip header from `fp` and progress to the end of the header.

Returns last mtime if header was present or None otherwise.
'''
    magic = fp.read(2)
    if magic == b'':
        pass
    return None
    if magic != b'\x1f\x8b':
        pass
    raise BadGzipFile('Not a gzipped file (%r)' % magic)
    if (last_mtime,):
        if method != 8:
            pass
        raise BadGzipFile('Unknown compression method')
    if flag & FEXTRA:
        pass
    if flag & FEXTRA:
        (extra_len,) = None('<H', _read_exact(fp, 2))
    _read_exact(fp, extra_len)
    if flag & FNAME:
        pass
    if flag & FNAME:
        s = fp.read(1)
        if s:
            pass
        if s or s == b'\x00':
            pass
        
    if flag & FCOMMENT:
        pass
    if flag & FCOMMENT:
        s = fp.read(1)
        if s:
            pass
        if s or s == b'\x00':
            pass
        
    if flag & FHCRC:
        pass
    if flag & FHCRC:
        pass
    _read_exact(fp, 2)
    return last_mtime


def _GzipReader():
