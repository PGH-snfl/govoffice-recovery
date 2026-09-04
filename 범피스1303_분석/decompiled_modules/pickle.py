# Source Generated with Decompyle++
# File: pickle.marshal (Python 3.13)

'''Create portable serialized representations of Python objects.

See module copyreg for a mechanism for registering custom picklers.
See module pickletools source for extensive comments.

Classes:

    Pickler
    Unpickler

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(bytes) -> object

Misc variables:

    __version__
    format_version
    compatible_formats

'''
from types import FunctionType
from copyreg import dispatch_table
from copyreg import _extension_registry, _inverted_registry, _extension_cache
from itertools import islice
from functools import partial
import sys
from sys import maxsize
from struct import pack, unpack
import re
import io
import codecs
import _compat_pickle
__all__ = [
    'PickleError',
    'PicklingError',
    'UnpicklingError',
    'Pickler',
    'Unpickler',
    'dump',
    'dumps',
    'load',
    'loads']

try:
    from _pickle import PickleBuffer
    __all__.append('PickleBuffer')
    _HAVE_PICKLE_BUFFER = True
except ImportError:
    load
    _HAVE_PICKLE_BUFFER = False

bytes_types = (bytes, bytearray)
format_version = '4.0'
compatible_formats = [
    '1.0',
    '1.1',
    '1.2',
    '1.3',
    '2.0',
    '3.0',
    '4.0',
    '5.0']
HIGHEST_PROTOCOL = 5
DEFAULT_PROTOCOL = 4

def PickleError():
    '''PickleError'''
    __firstlineno__ = 73
    __doc__ = 'A common base class for the other pickling exceptions.'
    __static_attributes__ = ()

PickleError = None(PickleError, 'PickleError', Exception)

def PicklingError():
    '''PicklingError'''
    __firstlineno__ = 77
    __doc__ = 'This exception is raised when an unpicklable object is passed to the\ndump() method.\n\n'
    __static_attributes__ = ()

PicklingError = None(PicklingError, 'PicklingError', PickleError)

def UnpicklingError():
    '''UnpicklingError'''
    __firstlineno__ = 84
    __doc__ = 'This exception is raised when there is a problem unpickling an object,\nsuch as a security violation.\n\nNote that other exceptions may also be raised during unpickling, including\n(but not necessarily limited to) AttributeError, EOFError, ImportError,\nand IndexError.\n\n'
    __static_attributes__ = ()

UnpicklingError = None(UnpicklingError, 'UnpicklingError', PickleError)

def _Stop():
    '''_Stop'''
    __firstlineno__ = 97
    
    def __init__(self, value):
        self.value = value

    __static_attributes__ = ('value',)

_Stop = None(_Stop, '_Stop', Exception)
MARK = b'('
STOP = b'.'
POP = b'0'
POP_MARK = b'1'
DUP = b'2'
FLOAT = b'F'
INT = b'I'
BININT = b'J'
BININT1 = b'K'
LONG = b'L'
BININT2 = b'M'
NONE = b'N'
PERSID = b'P'
BINPERSID = b'Q'
REDUCE = b'R'
STRING = b'S'
BINSTRING = b'T'
SHORT_BINSTRING = b'U'
UNICODE = b'V'
BINUNICODE = b'X'
APPEND = b'a'
BUILD = b'b'
GLOBAL = b'c'
DICT = b'd'
EMPTY_DICT = b'}'
APPENDS = b'e'
GET = b'g'
BINGET = b'h'
INST = b'i'
LONG_BINGET = b'j'
LIST = b'l'
EMPTY_LIST = b']'
OBJ = b'o'
PUT = b'p'
BINPUT = b'q'
LONG_BINPUT = b'r'
SETITEM = b's'
TUPLE = b't'
EMPTY_TUPLE = b')'
SETITEMS = b'u'
BINFLOAT = b'G'
TRUE = b'I01\n'
FALSE = b'I00\n'
PROTO = b'\x80'
NEWOBJ = b'\x81'
EXT1 = b'\x82'
EXT2 = b'\x83'
EXT4 = b'\x84'
TUPLE1 = b'\x85'
TUPLE2 = b'\x86'
TUPLE3 = b'\x87'
NEWTRUE = b'\x88'
NEWFALSE = b'\x89'
LONG1 = b'\x8a'
LONG4 = b'\x8b'
_tuplesize2code = [
    EMPTY_TUPLE,
    TUPLE1,
    TUPLE2,
    TUPLE3]
BINBYTES = b'B'
SHORT_BINBYTES = b'C'
SHORT_BINUNICODE = b'\x8c'
BINUNICODE8 = b'\x8d'
BINBYTES8 = b'\x8e'
EMPTY_SET = b'\x8f'
ADDITEMS = b'\x90'
FROZENSET = b'\x91'
NEWOBJ_EX = b'\x92'
STACK_GLOBAL = b'\x93'
MEMOIZE = b'\x94'
FRAME = b'\x95'
BYTEARRAY8 = b'\x96'
NEXT_BUFFER = b'\x97'
READONLY_BUFFER = b'\x98'
for None in :
    if re.match('[A-Z][A-Z0-9_]+$', x):
        pass
    if not re.match('[A-Z][A-Z0-9_]+$', x):
        continue
dir, None(), , [](x,)

def _Framer():
    '''_Framer'''
    __firstlineno__ = 194
    _FRAME_SIZE_MIN = 4
    _FRAME_SIZE_TARGET = 65536
    
    def __init__(self, file_write):
        self.file_write = file_write
        self.current_frame = None

    
    def start_framing(self):
        self.current_frame = None()

    
    def end_framing(self):
        if self.current_frame:
            pass
        if self.current_frame:
            if self.current_frame.tell() > 0:
                self.commit_frame(force = True)
                self.current_frame = None
            return None
        return None

    if (lambda self, force: if self.current_frame:
passif self.current_frame:
f = self.current_frameif not f.tell() >= self._FRAME_SIZE_TARGET:
if force:
passif force:
data = f.getbuffer()write = self.file_writeif len(data) >= self._FRAME_SIZE_MIN:
passNone(FRAME + pack('<Q', len(data)))None(data)self.current_frame = None()NoneNone):
        
        def commit_frame(self, force):
            if self.current_frame:
                pass
            if self.current_frame:
                f = self.current_frame
                if not f.tell() >= self._FRAME_SIZE_TARGET:
                    if force:
                        pass
                    if force:
                        data = f.getbuffer()
                        write = self.file_write
                        if len(data) >= self._FRAME_SIZE_MIN:
                            pass
                        None(FRAME + pack('<Q', len(data)))
                        None(data)
                        self.current_frame = None()
                return None
            return None

    
    def write(self, data):
        if self.current_frame:
            pass
        if self.current_frame:
            pass
        return self.current_frame.write(data)
        return self.file_write(data)

    
    def write_large_bytes(self, header, payload):
        write = self.file_write
        if self.current_frame:
            pass
        if self.current_frame:
            pass
        self.commit_frame(force = True)
        None(header)
        None(payload)

    __static_attributes__ = ('current_frame', 'file_write')

None(_Framer, '_Framer') = <NODE:27>

def _Unframer():
    '''_Unframer'''
    __firstlineno__ = 257
    if (lambda self, file_read, file_readline, file_tell: self.file_read = file_readself.file_readline = file_readlineself.current_frame = None):
        
        def __init__(self, file_read, file_readline, file_tell):
            self.file_read = file_read
            self.file_readline = file_readline
            self.current_frame = None

    
    def readinto(self, buf):
        if self.current_frame:
            pass
        if self.current_frame:
            n = self.current_frame.readinto(buf)
            if n == 0 and len(buf) != 0:
                self.current_frame = None
                n = len(buf)
                buf[:] = self.file_read(n)
            return n
        if None < len(buf):
            pass
        raise UnpicklingError('pickle exhausted before end of frame')
        return n
        n = len(buf)
        buf[:] = self.file_read(n)
        return n

    
    def read(self, n):
        if self.current_frame:
            pass
        if self.current_frame:
            data = self.current_frame.read(n)
            if data:
                pass
            if data and n != 0:
                self.current_frame = None
            return self.file_read(n)
        if None(data) < n:
            pass
        raise UnpicklingError('pickle exhausted before end of frame')
        return data
        return self.file_read(n)

    
    def readline(self):
        if self.current_frame:
            pass
        if self.current_frame:
            data = self.current_frame.readline()
            if data:
                pass
            if not data:
                self.current_frame = None
            return self.file_readline()
        if None[-1] != 10:
            pass
        raise UnpicklingError('pickle exhausted before end of frame')
        return data
        return self.file_readline()

    
    def load_frame(self, frame_size):
        if self.current_frame:
            pass
        if self.current_frame and self.current_frame.read() != b'':
            pass
        raise UnpicklingError('beginning of a new frame before end of current frame')
        self.current_frame = None(self.file_read(frame_size))

    __static_attributes__ = ('current_frame', 'file_read', 'file_readline')

_Unframer = None(_Unframer, '_Unframer')

def _getattribute(obj, name):
    top = obj
    for subpath in name.split('.'):
        if subpath == '<locals>':
            pass
        raise AttributeError("Can't get local attribute {!r} on {!r}".format(name, top))
        
        try:
            parent = obj
            obj = getattr(obj, subpath)
        except AttributeError:
            raise AttributeError("Can't get attribute {!r} on {!r}".format(name, top)), None

    return (obj, parent)


def whichmodule(obj, name):
    '''Find the module an object belong to.'''
    module_name = getattr(obj, '__module__', None)
    if module_name:
        pass
    return module_name
    for None in sys.modules.copy().items():
        if ():
            if module_name == '__main__' and module_name == '__mp_main__' or module:
                continue
            
            try:
                if _getattribute(module, name)[0] is obj:
                    

        return module, module_name
    return '__main__'
    if AttributeError:
        module_name
        continue


def encode_long(x):
    """Encode a long to a two's complement little-endian binary string.
Note that 0 is a special case, returning an empty string, to save a
byte in the LONG1 pickling context.

>>> encode_long(0)
b''
>>> encode_long(255)
b'\\xff\\x00'
>>> encode_long(32767)
b'\\xff\\x7f'
>>> encode_long(-256)
b'\\x00\\xff'
>>> encode_long(-32768)
b'\\x00\\x80'
>>> encode_long(-128)
b'\\x80'
>>> encode_long(127)
b'\\x7f'
>>>
"""
    if x == 0:
        pass
    return b''
    nbytes = (x.bit_length() >> 3) + 1
    result = x.to_bytes(nbytes, byteorder = 'little', signed = True)
    if x < 0 and nbytes > 1 and result[-1] == 255 and result[-2] & 128 != 0:
        pass
    result = result[:-1]
    return result


def decode_long(data):
    '''Decode a long from a two\'s complement little-endian binary string.

>>> decode_long(b\'\')
0
>>> decode_long(b"\\xff\\x00")
255
>>> decode_long(b"\\xff\\x7f")
32767
>>> decode_long(b"\\x00\\xff")
-256
>>> decode_long(b"\\x00\\x80")
-32768
>>> decode_long(b"\\x80")
-128
>>> decode_long(b"\\x7f")
127
'''
    return int.from_bytes(data, byteorder = 'little', signed = True)


class _NoValue:
