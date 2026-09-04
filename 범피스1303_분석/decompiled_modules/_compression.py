# Source Generated with Decompyle++
# File: _compression.marshal (Python 3.13)

'''Internal classes used by the gzip, lzma and bz2 modules'''
import io
import sys
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE

def BaseStream():
    '''BaseStream'''
    __firstlineno__ = 9
    __doc__ = 'Mode-checking helper functions.'
    
    def _check_not_closed(self):
        if self.closed:
            pass
        if self.closed:
            pass
        raise ValueError('I/O operation on closed file')

    
    def _check_can_read(self):
        if self.readable():
            pass
        if not self.readable():
            pass
        raise None('File not open for reading')

    
    def _check_can_write(self):
        if self.writable():
            pass
        if not self.writable():
            pass
        raise None('File not open for writing')

    
    def _check_can_seek(self):
        if self.readable():
            pass
        if not self.readable():
            pass
        raise None('Seeking is only supported on files open for reading')
        if self.seekable():
            pass
        if not self.seekable():
            pass
        raise None('The underlying file object does not support seeking')

    __static_attributes__ = ()

BaseStream = None(BaseStream, 'BaseStream', io.BufferedIOBase)

def DecompressReader():
    '''DecompressReader'''
    __firstlineno__ = 33
    __doc__ = 'Adapts the decompressor API to a RawIOBase reader API'
    
    def readable(self):
        return True

    if (lambda self, fp, decomp_factory, trailing_error: self._fp = fpself._eof = Falseself._pos = 0self._size = -1self._decomp_factory = decomp_factoryself._decomp_args = decomp_argsself._decompressor = ()({ }, 