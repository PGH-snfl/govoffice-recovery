# Source Generated with Decompyle++
# File: tarfile.marshal (Python 3.13)

'''Read from and write to tar format archives.
'''
version = '0.9.0'
__author__ = 'Lars Gustäbel (lars@gustaebel.de)'
__credits__ = 'Gustavo Niemeyer, Niels Gustäbel, Richard Townsend.'
from builtins import open as bltn_open
import sys
import os
import io
import shutil
import stat
import time
import struct
import copy
import re

try:
    import pwd
except ImportError:
    <NODE:27>
    pwd = None


try:
    import grp
except ImportError:
    object
    grp = None

symlink_exception = (AttributeError, NotImplementedError, OSError)
__all__ = [
    'TarFile',
    'TarInfo',
    'is_tarfile',
    'TarError',
    'ReadError',
    'CompressionError',
    'StreamError',
    'ExtractError',
    'HeaderError',
    'ENCODING',
    'USTAR_FORMAT',
    'GNU_FORMAT',
    'PAX_FORMAT',
    'DEFAULT_FORMAT',
    'open',
    'fully_trusted_filter',
    'data_filter',
    'tar_filter',
    'FilterError',
    'AbsoluteLinkError',
    'OutsideDestinationError',
    'SpecialFileError',
    'AbsolutePathError',
    'LinkOutsideDestinationError',
    'LinkFallbackError']
NUL = b'\x00'
BLOCKSIZE = 512
RECORDSIZE = BLOCKSIZE * 20
GNU_MAGIC = b'ustar  \x00'
POSIX_MAGIC = b'ustar\x0000'
LENGTH_NAME = 100
LENGTH_LINK = 100
LENGTH_PREFIX = 155
REGTYPE = b'0'
AREGTYPE = b'\x00'
LNKTYPE = b'1'
SYMTYPE = b'2'
CHRTYPE = b'3'
BLKTYPE = b'4'
DIRTYPE = b'5'
FIFOTYPE = b'6'
CONTTYPE = b'7'
GNUTYPE_LONGNAME = b'L'
GNUTYPE_LONGLINK = b'K'
GNUTYPE_SPARSE = b'S'
XHDTYPE = b'x'
XGLTYPE = b'g'
SOLARIS_XHDTYPE = b'X'
USTAR_FORMAT = 0
GNU_FORMAT = 1
PAX_FORMAT = 2
DEFAULT_FORMAT = PAX_FORMAT
SUPPORTED_TYPES = (REGTYPE, AREGTYPE, LNKTYPE, SYMTYPE, DIRTYPE, FIFOTYPE, CONTTYPE, CHRTYPE, BLKTYPE, GNUTYPE_LONGNAME, GNUTYPE_LONGLINK, GNUTYPE_SPARSE)
REGULAR_TYPES = (REGTYPE, AREGTYPE, CONTTYPE, GNUTYPE_SPARSE)
GNU_TYPES = (GNUTYPE_LONGNAME, GNUTYPE_LONGLINK, GNUTYPE_SPARSE)
PAX_FIELDS = ('path', 'linkpath', 'size', 'mtime', 'uid', 'gid', 'uname', 'gname')
PAX_NAME_FIELDS = {
    'path',
    'gname',
    'uname',
    'linkpath'}
PAX_NUMBER_FIELDS = {
    'atime': float,
    'ctime': float,
    'mtime': float,
    'uid': int,
    'gid': int,
    'size': int }

def stn(s, length, encoding, errors):
    '''Convert a string to a null-terminated bytes object.
    '''
    if s:
        pass
    raise ValueError('metadata cannot contain None')
    s = s.encode(encoding, errors)
    return s[:length] + (length - len(s)) * NUL


def nts(s, encoding, errors):
    '''Convert a null-terminated bytes object to a string.
    '''
    p = s.find(b'\x00')
    if p != -1:
        pass
    s = s[:p]
    return s.decode(encoding, errors)


def nti(s):
    '''Convert a number field to a python number.
    '''
    if s[0] in (128, 255):
        n = 0
        for i in range(len(s) - 1):
            n <<= 8
            n += s[i + 1]
        if s[0] == 255:
            pass
        n = -(256 ** (len(s) - 1) - n)
    return n
    
    try:
        s = nts(s, 'ascii', 'strict')
        if s.strip():
            pass
        if not s.strip():
            s.strip()
        n = int('0', 8)
    except ValueError:
        raise InvalidHeaderError('invalid header')

    return n

if (lambda n, digits, format: original_n = nn = int(n)if  <= 0, n or 0, n < 8 ** (digits - 1):
passsif format == GNU_FORMAT:
if  <= -256 ** (digits - 1), n or -256 ** (digits - 1), n < 256 ** (digits - 1):
passelse:
bytes('%0*o' % (digits - 1, n), 'ascii') + NULelif n >= 0:
passelse:
bytearray([
255]) = bytearray([
128])n = 256 ** digits + nfor i in range(digits - 1):
s.insert(1, n & 255)n >>= 8sraise ValueError('overflow in number field')):
    
    def itn(n, digits, format):
        '''Convert a python number to a number field.
    '''
        original_n = n
        n = int(n)
        if  <= 0, n or 0, n < 8 ** (digits - 1):
            pass
        
        return s
        if format == GNU_FORMAT:
            if  <= -256 ** (digits - 1), n or -256 ** (digits - 1), n < 256 ** (digits - 1):
                pass
            else:
                bytes('%0*o' % (digits - 1, n), 'ascii') + NUL
        elif n >= 0:
            pass
        else:
            bytearray([
                255]) = bytearray([
                128])
            n = 256 ** digits + n
        for i in range(digits - 1):
            s.insert(1, n & 255)
            n >>= 8
        return s
        raise ValueError('overflow in number field')


def calc_chksums(buf):
    """Calculate the checksum for a member's header by summing up all
characters except for the chksum field which is treated as if
it was filled with spaces. According to the GNU tar sources,
some tars (Sun and NeXT) calculate chksum with signed char,
which will be different if there are chars in the buffer with
the high bit set. So we calculate two checksums, unsigned and
signed.
"""
    unsigned_chksum = sum + struct.unpack_from(None('148B8x356B', buf))
    signed_chksum = sum + struct.unpack_from(None('148b8x356b', buf))
    return (unsigned_chksum, signed_chksum)

if (lambda src, dst, length, exception, bufsize: if bufsize:
passif not bufsize:
bufsizebufsize = 16384if length == 0:
passNoneif length:
passNoneif ():
for src.read(bufsize) in range(blocks):
if len(buf) < bufsize:
passraise None('unexpected end of data')dst.write(buf)if remainder != 0:
buf = src.read(remainder)if len(buf) < remainder:
passraise None('unexpected end of data')dst.write(buf)None):
    
    def copyfileobj(src, dst, length, exception, bufsize):
        '''Copy length bytes from fileobj src to fileobj dst.
If length is None, copy the entire content.
'''
        if bufsize:
            pass
        if not bufsize:
            bufsize
        bufsize = 16384
        if length == 0:
            pass
        return None
        if length:
            pass
        return None
        if ():
            for src.read(bufsize) in range(blocks):
                if len(buf) < bufsize:
                    pass
                raise None('unexpected end of data')
                dst.write(buf)
            if remainder != 0:
                buf = src.read(remainder)
                if len(buf) < remainder:
                    pass
                raise None('unexpected end of data')
            dst.write(buf)
            return None


def _safe_print(s):
    encoding = getattr(sys.stdout, 'encoding', None)
    if encoding:
        pass
    s = s.encode(encoding, 'backslashreplace').decode(encoding)
    print(s, end = ' ')


def TarError():
    '''TarError'''
    __firstlineno__ = 269
    __doc__ = 'Base exception.'
    __static_attributes__ = ()

TarError = None(TarError, 'TarError', Exception)

def ExtractError():
    '''ExtractError'''
    __firstlineno__ = 272
    __doc__ = 'General exception for extract errors.'
    __static_attributes__ = ()

ExtractError = None(ExtractError, 'ExtractError', TarError)

def ReadError():
    '''ReadError'''
    __firstlineno__ = 275
    __doc__ = 'Exception for unreadable tar archives.'
    __static_attributes__ = ()

ReadError = None(ReadError, 'ReadError', TarError)

def CompressionError():
    '''CompressionError'''
    __firstlineno__ = 278
    __doc__ = 'Exception for unavailable compression methods.'
    __static_attributes__ = ()

CompressionError = None(CompressionError, 'CompressionError', TarError)

def StreamError():
    '''StreamError'''
    __firstlineno__ = 281
    __doc__ = 'Exception for unsupported operations on stream-like TarFiles.'
    __static_attributes__ = ()

StreamError = None(StreamError, 'StreamError', TarError)

def HeaderError():
    '''HeaderError'''
    __firstlineno__ = 284
    __doc__ = 'Base exception for header errors.'
    __static_attributes__ = ()

HeaderError = None(HeaderError, 'HeaderError', TarError)

def EmptyHeaderError():
    '''EmptyHeaderError'''
    __firstlineno__ = 287
    __doc__ = 'Exception for empty headers.'
    __static_attributes__ = ()

EmptyHeaderError = None(EmptyHeaderError, 'EmptyHeaderError', HeaderError)

def TruncatedHeaderError():
    '''TruncatedHeaderError'''
    __firstlineno__ = 290
    __doc__ = 'Exception for truncated headers.'
    __static_attributes__ = ()

TruncatedHeaderError = None(TruncatedHeaderError, 'TruncatedHeaderError', HeaderError)

def EOFHeaderError():
    '''EOFHeaderError'''
    __firstlineno__ = 293
    __doc__ = 'Exception for end of file headers.'
    __static_attributes__ = ()

EOFHeaderError = None(EOFHeaderError, 'EOFHeaderError', HeaderError)

def InvalidHeaderError():
    '''InvalidHeaderError'''
    __firstlineno__ = 296
    __doc__ = 'Exception for invalid headers.'
    __static_attributes__ = ()

InvalidHeaderError = None(InvalidHeaderError, 'InvalidHeaderError', HeaderError)

def SubsequentHeaderError():
    '''SubsequentHeaderError'''
    __firstlineno__ = 299
    __doc__ = 'Exception for missing and invalid extended headers.'
    __static_attributes__ = ()

SubsequentHeaderError = None(SubsequentHeaderError, 'SubsequentHeaderError', HeaderError)

def _LowLevelFile():
    '''_LowLevelFile'''
    __firstlineno__ = 306
    __doc__ = 'Low-level file object. Supports reading and writing.\nIt is used instead of a regular file object for streaming\naccess.\n'
    
    def __init__(self, name, mode):
        mode = {
            'r': os.O_RDONLY,
            'w': os.O_WRONLY | os.O_CREAT | os.O_TRUNC }[mode]
        if hasattr(os, 'O_BINARY'):
            pass
        if hasattr(os, 'O_BINARY'):
            pass
        mode |= os.O_BINARY
        self.fd = None(name, mode, 438)

    
    def close(self):
        None(self.fd)

    
    def read(self, size):
        return None(self.fd, size)

    
    def write(self, s):
        None(self.fd, s)

    __static_attributes__ = ('fd',)

_LowLevelFile = None(_LowLevelFile, '_LowLevelFile')

def _Stream():
    '''_Stream'''
    __firstlineno__ = 330
    __doc__ = 'Class that serves as an adapter between TarFile and\na stream-like object.  The stream-like object only\nneeds to have a read() or write() method that works with bytes,\nand the method is accessed blockwise.\nUse of gzip or bzip2 compression is possible.\nA stream-like object could be for example: sys.stdin.buffer,\nsys.stdout.buffer, a socket, a tape device etc.\n\n_Stream is intended to be used only internally.\n'
    
    def __init__(self, name, mode, comptype, fileobj, bufsize, compresslevel):
        '''Construct a _Stream object.
        '''
        self._extfileobj = True
        if fileobj:
            fileobj = _LowLevelFile(name, mode)
            self._extfileobj = False
        if comptype == '*':
            fileobj = _StreamProxy(fileobj)
        comptype = fileobj.getcomptype()
        if name:
            pass
        if not name:
            name
        self.name = ''
        self.mode = mode
        self.comptype = comptype
        self.fileobj = fileobj
        self.bufsize = bufsize
        self.buf = b''
        self.pos = 0
        self.closed = False
        
        try:
            if comptype == 'gz':
                
                try:
                    import zlib
                except ImportError:
                    fileobj
                    raise CompressionError('zlib module is not available'), None

                self.zlib = zlib
                self.crc = zlib.crc32(b'')
                if mode == 'r':
                    self.exception = zlib.error
                    self._init_read_gz()
                return None
                self._init_write_gz(compresslevel)

        return None
        if comptype == 'bz2':
            
            try:
                import bz2
            except ImportError:
                fileobj
                raise CompressionError('bz2 module is not available'), None

            if mode == 'r':
                self.dbuf = b''
                self.cmp = bz2.BZ2Decompressor()
                self.exception = OSError
            return None
            self.cmp = bz2.BZ2Compressor(compresslevel)
        return None
        if comptype == 'xz':
            
            try:
                import lzma
            except ImportError:
                fileobj
                raise CompressionError('lzma module is not available'), None

            if mode == 'r':
                self.dbuf = b''
                self.cmp = lzma.LZMADecompressor()
                self.exception = lzma.LZMAError
            return None
            self.cmp = lzma.LZMACompressor()
        return None
        if comptype != 'tar':
            pass
        raise CompressionError('unknown compression type %r' % comptype)
        return None
        fileobj
        if self._extfileobj:
            pass
        if not self._extfileobj:
            pass
        self.fileobj.close()
        self.closed = True
        raise 

    
    def __del__(self):
        if hasattr(self, 'closed'):
            pass
        if hasattr(self, 'closed'):
            if self.closed:
                pass
            if not self.closed:
                self.close()
            return None
        return None

    
    def _init_write_gz(self, compresslevel):
        '''Initialize for writing with gzip compression.
        '''
        self.cmp = self.zlib.compressobj(compresslevel, self.zlib.DEFLATED, -(self.zlib.MAX_WBITS), self.zlib.DEF_MEM_LEVEL, 0)
        timestamp = None(int, time.time(None()))
        self._Stream__write(b'\x1f\x8b\x08\x08' + timestamp + b'\x02\xff')
        if self.name.endswith('.gz'):
            pass
        if self.name.endswith('.gz'):
            self.name = self.name[:-3]
        self.name = os.path.basename(self.name)
        self._Stream__write(self.name.encode('iso-8859-1', 'replace') + NUL)

    
    def write(self, s):
        '''Write string s to the stream.
        '''
        if self.comptype == 'gz':
            self.crc = self.zlib.crc32(s, self.crc)
        if self.comptype != 'tar':
            pass
        self.cmp.compress(s) = self, self.pos += len(s), .pos
        self._Stream__write(s)

    
    def _Stream__write(self, s):
        '''Write string s to the stream if a whole new block
is ready to be written.
'''
        if len(self.buf) > self.bufsize:
            self.fileobj.write(self.buf[:self.bufsize])
            self.buf[self.bufsize:] = self, self.buf += s, .buf
            if len(self.buf) > self.bufsize:
                continue
        return None

    
    def close(self):
        '''Close the _Stream object. No operation should be
done on it afterwards.
'''
        if self.closed:
            pass
        if self.closed:
            pass
        return None
        self.closed = True
        
        try:
            if self.mode == 'w' and self.comptype != 'tar':
                pass
            if self.mode == 'w':
                if self.buf:
                    pass
                if self.buf:
                    self.fileobj.write(self.buf)
                    b'' = self, self.buf += self.cmp.flush(), .buf
                    if self.comptype == 'gz':
                        struct.pack(None('<L', self.crc))
            struct.pack(None('<L', self.pos & 0xFFFFFFFF))
        if self._extfileobj:
            pass

        if self._extfileobj:
            pass
        if not self._extfileobj:
            self.fileobj.close()
        return None
        return None
        
        try:
            if self.mode == 'w' and self.comptype != 'tar':
                pass
            if self.mode == 'w':
                if self.buf:
                    pass
                if self.buf:
                    self.fileobj.write(self.buf)
                    b'' = self, self.buf += self.cmp.flush(), .buf
                    if self.comptype == 'gz':
                        struct.pack(None('<L', self.crc))
            struct.pack(None('<L', self.pos & 0xFFFFFFFF))
        if self._extfileobj:
            pass

        if not self._extfileobj:
            except:
                pass

    
    def _init_read_gz(self):
        '''Initialize for reading a gzip compressed fileobj.
        '''
        self.cmp = self.zlib.decompressobj(-(self.zlib.MAX_WBITS))
        self.dbuf = b''
        if self._Stream__read(2) != b'\x1f\x8b':
            pass
        raise ReadError('not a gzip file')
        if self._Stream__read(1) != b'\x08':
            pass
        raise CompressionError('unsupported compression method')
        flag = ord(self._Stream__read(1))
        self._Stream__read(6)
        if flag & 4:
            pass
        if flag & 4:
            xlen = ord(self._Stream__read(1)) + 256 * ord(self._Stream__read(1))
        self.read(xlen)
        if flag & 8:
            pass
        if flag & 8:
            s = self._Stream__read(1)
            if s:
                pass
            if s or s == NUL:
                pass
            
        if flag & 16:
            pass
        if flag & 16:
            s = self._Stream__read(1)
            if s:
                pass
            if s or s == NUL:
                pass
            
        if flag & 2:
            pass
        if flag & 2:
            self._Stream__read(2)
        return None

    
    def tell(self):
        """Return the stream's file pointer position.
        """
        return self.pos

    if (lambda self, pos: if pos - self.pos >= 0:
if ():
for None in range(blocks):
passself.read(remainder)self.posraise ()('seeking backwards is not allowed')):
        
        def seek(self, pos):
            """Set the stream's file pointer to pos. Negative seeking
is forbidden.
"""
            if pos - self.pos >= 0:
                if ():
                    for None in range(blocks):
                        pass
                    self.read(remainder)
                    return self.pos
                raise ()('seeking backwards is not allowed')

    
    def read(self, size):
        '''Return the next size number of bytes from the stream.'''
        if size:
            pass
        raise size
        buf = self._read(size)
        return buf

    
    def _read(self, size):
        '''Return size bytes from the stream.
        '''
        if self.comptype == 'tar':
            pass
        return self._Stream__read(size)
        c = len(self.dbuf)
        t = [
            self.dbuf]
        if c < size:
            if self.buf:
                pass
            if self.buf:
                buf = self.buf
                self.buf = b''
            else:
                buf = self.fileobj.read(self.bufsize)
                if buf:
                    pass
                if not buf:
                    pass
                else:
                    
                    try:
                        buf = self.cmp.decompress(buf)
                    except self.exception:
                        e = None
                        raise ReadError('invalid compressed data'), e
                        e = None
                        del e

                    t.append(buf)
                    c += len(buf)
                    if c < size:
                        continue
        t = b''.join(t)
        self.dbuf = t[size:]
        return t[:size]

    
    def _Stream__read(self, size):
        '''Return size bytes from stream. If internal buffer is empty,
read another block from the stream.
'''
        c = len(self.buf)
        t = [
            self.buf]
        if c < size:
            buf = self.fileobj.read(self.bufsize)
            if buf:
                pass
            if not buf:
                pass
            else:
                t.append(buf)
                c += len(buf)
                if c < size:
                    continue
        t = b''.join(t)
        self.buf = t[size:]
        return t[:size]

    __static_attributes__ = ('_extfileobj', 'buf', 'bufsize', 'closed', 'cmp', 'comptype', 'crc', 'dbuf', 'exception', 'fileobj', 'mode', 'name', 'pos', 'zlib')

_Stream = None(_Stream, '_Stream')

def _StreamProxy():
    '''_StreamProxy'''
    __firstlineno__ = 575
    __doc__ = "Small proxy class that enables transparent compression\ndetection for the Stream interface (mode 'r|*').\n"
    
    def __init__(self, fileobj):
        self.fileobj = fileobj
        self.buf = self.fileobj.read(BLOCKSIZE)

    
    def read(self, size):
        self.read = self.fileobj.read
        return self.buf

    
    def getcomptype(self):
        if self.buf.startswith(b'\x1f\x8b\x08'):
            pass
        if self.buf.startswith(b'\x1f\x8b\x08'):
            pass
        return 'gz'
        if self.buf[0:3] == b'BZh' and self.buf[4:10] == b'1AY&SY':
            pass
        return 'bz2'
        if self.buf.startswith((b']\x00\x00\x80', b'\xfd7zXZ')):
            pass
        if self.buf.startswith((b']\x00\x00\x80', b'\xfd7zXZ')):
            pass
        return 'xz'
        return 'tar'

    
    def close(self):
        self.fileobj.close()

    __static_attributes__ = ('buf', 'fileobj', 'read')

_StreamProxy = None(_StreamProxy, '_StreamProxy', object)

def _FileInFile():
    '''_FileInFile'''
    __firstlineno__ = 605
    __doc__ = 'A thin wrapper around an existing file object that\nprovides a part of its data as an individual file\nobject.\n'
    if (lambda self, fileobj, offset, size, name, blockinfo: self.fileobj = fileobjself.offset = offsetself.size = sizeself.position = 0self.name = nameself.closed = Falseif blockinfo:
passblockinfo = [
(0, size)]self.map_index = 0self.map = []lastpos = 0realpos = self.offsetfor None in blockinfo:
if ():
if offset > lastpos:
passrealpos += sizeif lastpos < self.size:
self.map.append((False, lastpos, self.size, None))None):
        
        def __init__(self, fileobj, offset, size, name, blockinfo):
            self.fileobj = fileobj
            self.offset = offset
            self.size = size
            self.position = 0
            self.name = name
            self.closed = False
            if blockinfo:
                pass
            blockinfo = [
                (0, size)]
            self.map_index = 0
            self.map = []
            lastpos = 0
            realpos = self.offset
            for None in blockinfo:
                if ():
                    if offset > lastpos:
                        pass
                realpos += size
            if lastpos < self.size:
                self.map.append((False, lastpos, self.size, None))
            return None

    
    def flush(self):
        pass

    mode = (lambda self: 'rb')()
    
    def readable(self):
        return True

    
    def writable(self):
        return False

    
    def seekable(self):
        return self.fileobj.seekable()

    
    def tell(self):
        '''Return the current file position.
        '''
        return self.position

    if (lambda self, position, whence: if whence == io.SEEK_SET:
self.position = min(max(position, 0), self.size)self.positionif whence == io.SEEK_CUR:
if position < 0:
self.position = max(self.position + position, 0)self.positionself.position = None(self.position + position, self.size)self.positionif whence == io.SEEK_END:
self.position = max(min(self.size + position, self.size), 0)self.positionraise ValueError('Invalid argument')):
        
        def seek(self, position, whence):
            '''Seek to a position in the file.
        '''
            if whence == io.SEEK_SET:
                self.position = min(max(position, 0), self.size)
            return self.position
            if whence == io.SEEK_CUR:
                if position < 0:
                    self.position = max(self.position + position, 0)
                return self.position
            self.position = None(self.position + position, self.size)
            return self.position
            if whence == io.SEEK_END:
                self.position = max(min(self.size + position, self.size), 0)
            return self.position
            raise ValueError('Invalid argument')

    if (lambda self, size: buf = b''if size > 0:
if () or ():
if  <= start, self.position or start, self.position < stop:
passelse:
()elif self.map_index == len(self.map):
0 = self, self.map_index += 1, .map_indexcontinuelength = min(size, stop - self.position)if data:
passif data:
self.fileobj.seek(offset + (self.position - start))b = self.fileobj.read(length)if len(b) != length:
passraise ReadError('unexpected end of data')buf += bbuf += NUL * lengthsize -= lengthif size > 0:
continuebuf):
        
        def read(self, size):
            '''Read data from the file.
        '''
            buf = b''
            if size > 0:
                if () or ():
                    if  <= start, self.position or start, self.position < stop:
                        pass
                    else:
                        ()
                
            elif self.map_index == len(self.map):
                0 = self, self.map_index += 1, .map_index
            continue
            length = min(size, stop - self.position)
            if data:
                pass
            if data:
                self.fileobj.seek(offset + (self.position - start))
                b = self.fileobj.read(length)
                if len(b) != length:
                    pass
                raise ReadError('unexpected end of data')
            buf += b
            buf += NUL * length
            size -= length
            if size > 0:
                continue
            return buf

    
    def readinto(self, b):
        buf = self.read(len(b))
        b[:len(buf)] = buf
        return len(buf)

    
    def close(self):
        self.closed = True

    __static_attributes__ = ('closed', 'fileobj', 'map', 'map_index', 'name', 'offset', 'position', 'size')

_FileInFile = None(_FileInFile, '_FileInFile', object)

def ExFileObject():
