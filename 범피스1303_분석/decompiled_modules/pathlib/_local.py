# Source Generated with Decompyle++
# File: _local.marshal (Python 3.13)

import io
import ntpath
import operator
import os
import posixpath
import sys
import warnings
from glob import _StringGlobber
from itertools import chain
from _collections_abc import Sequence

try:
    import pwd
except ImportError:
    <NODE:27>
    pwd = None


try:
    import grp
except ImportError:
    <NODE:27>
    grp = None

from _abc import UnsupportedOperation, PurePathBase, PathBase
__all__ = [
    'PurePath',
    'PurePosixPath',
    'PureWindowsPath',
    'Path',
    'PosixPath',
    'WindowsPath']

def _PathParents():
    '''_PathParents'''
    __firstlineno__ = 30
    __doc__ = "This object provides sequence-like access to the logical ancestors\nof a path.  Don't try to construct it yourself."
    __slots__ = ('_path', '_drv', '_root', '_tail')
    
    def __init__(self, path):
        self._path = path
        self._drv = path.drive
        self._root = path.root
        self._tail = path._tail

    
    def __len__(self):
        return len(self._tail)

    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            pass
        if isinstance(idx, slice):
            if (lambda .0: if None:
passfor i in .0:
if self[i]:
passself[i]):
                pass
        return (lambda .0: if None:
passfor i in .0:
if self[i]:
passself[i])(range(idx.indices(len(self)))())
        if idx >= len(self) or idx < -len(self):
            pass
        raise IndexError(idx)
        if idx < 0:
            pass
        idx += len(self)
        return self._path._from_parsed_parts(self._drv, self._root, self._tail[:-idx - 1])

    
    def __repr__(self):
        return '<{}.parents>'.format(type(self._path).__name__)

    __static_attributes__ = ('_drv', '_path', '_root', '_tail')

_PathParents = None(_PathParents, '_PathParents', Sequence)

def PurePath():
    '''PurePath'''
    __firstlineno__ = 59
    __doc__ = "Base class for manipulating paths without I/O.\n\nPurePath represents a filesystem path and offers operations which\ndon't imply any actual filesystem I/O.  Depending on your system,\ninstantiating a PurePath will return either a PurePosixPath or a\nPureWindowsPath object.  You can also instantiate either of these classes\ndirectly, regardless of your system.\n"
    __slots__ = ('_raw_paths', '_drv', '_root', '_tail_cached', '_str', '_str_normcase_cached', '_parts_normcase_cached', '_hash')
    parser = os.path
    _globber = _StringGlobber
    
    def __new__(cls, *args, **kwargs):
        '''Construct a PurePath from one or several strings and or existing
PurePath objects.  The strings and path objects are combined so as
to yield a canonicalized path, which is incorporated into the
new PurePath object.
'''
        if cls is PurePath:
            pass
        cls = PureWindowsPath if os.name == 'nt' else PurePosixPath
        return object.__new__(cls)

    
    def __init__(self, *args):
        paths = []
        for arg in args:
            if isinstance(arg, PurePath):
                pass
            if isinstance(arg, PurePath):
                if arg.parser is not self.parser:
                    paths.append(arg.as_posix())
                    continue
                paths.extend(arg._raw_paths)
                continue
            
            try:
                path = None(arg)
            except TypeError:
                path = arg

            if isinstance(path, str):
                pass
            if not isinstance(path, str):
                pass
            raise TypeError(f'''argument should be a str or an os.PathLike object where __fspath__ returns a str, not {type(path).__name__}''')
            paths.append(path)
        self._raw_paths = paths

    
    def joinpath(self, *pathsegments):
        '''Combine this path with one or several arguments, and return a
new path representing either a subpath (if all arguments are relative
paths) or a totally different path (if one of the arguments is
anchored).
'''
        return self.with_segments(None(None))

    
    def __truediv__(self, key):
        
        try:
            pass
        except TypeError:
            pass


    
    def __rtruediv__(self, key):
        
        try:
            pass
        except TypeError:
            pass


    
    def __reduce__(self):
        return (self.__class__, tuple(self._raw_paths))

    
    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.as_posix())

    
    def __fspath__(self):
        return str(self)

    
    def __bytes__(self):
        '''Return the bytes representation of the path.  This is only
recommended to use under Unix.'''
        return None(self)

    _str_normcase = (lambda self: try:
passexcept AttributeError:
if self.parser is posixpath:
self._str_normcase_cached = str(self)else:
self._str_normcase_cached = str(self).lower())()
    
    def __hash__(self):
        
        try:
            pass
        except AttributeError:
            self._hash = hash(self._str_normcase)


    
    def __eq__(self, other):
        if isinstance(other, PurePath):
            pass
        if not isinstance(other, PurePath):
            pass
        return NotImplemented
        if self._str_normcase == other._str_normcase:
            pass
        if self._str_normcase == other._str_normcase:
            self._str_normcase == other._str_normcase
        return self.parser is other.parser

    _parts_normcase = (lambda self: try:
passexcept AttributeError:
self._parts_normcase_cached = self._str_normcase.split(self.parser.sep))()
    
    def __lt__(self, other):
        if isinstance(other, PurePath):
            pass
        if isinstance(other, PurePath) or self.parser is not other.parser:
            pass
        return NotImplemented
        return self._parts_normcase < other._parts_normcase

    
    def __le__(self, other):
        if isinstance(other, PurePath):
            pass
        if isinstance(other, PurePath) or self.parser is not other.parser:
            pass
        return NotImplemented
        return self._parts_normcase <= other._parts_normcase

    
    def __gt__(self, other):
        if isinstance(other, PurePath):
            pass
        if isinstance(other, PurePath) or self.parser is not other.parser:
            pass
        return NotImplemented
        return self._parts_normcase > other._parts_normcase

    
    def __ge__(self, other):
        if isinstance(other, PurePath):
            pass
        if isinstance(other, PurePath) or self.parser is not other.parser:
            pass
        return NotImplemented
        return self._parts_normcase >= other._parts_normcase

    
    def __str__(self):
        '''Return the string representation of the path, suitable for
passing to system calls.'''
        
        try:
            pass
        except AttributeError:
            if self._format_parsed_parts(self.drive, self.root, self._tail):
                pass
            if not self._format_parsed_parts(self.drive, self.root, self._tail):
                self._format_parsed_parts(self.drive, self.root, self._tail)
            self._str = '.'


    _format_parsed_parts = (lambda cls, drv, root, tail: if drv:
passif not drv:
if root:
passif root:
passdrv + root + cls.parser.sep.join(tail)if tail:
passif tail:
if cls.parser.splitdrive(tail[0])[0]:
passif cls.parser.splitdrive(tail[0])[0]:
passtail = [
'.'] + tailcls.parser.sep.join(tail))()
    
    def _from_parsed_parts(self, drv, root, tail):
        path = self._from_parsed_string(self._format_parsed_parts(drv, root, tail))
        path._drv = drv
        path._root = root
        path._tail_cached = tail
        return path

    
    def _from_parsed_string(self, path_str):
        path = self.with_segments(path_str)
        if path_str:
            pass
        if not path_str:
            path_str
        path._str = '.'
        return path

    _parse_path = (lambda cls, path: if path:
passif not path:
pass('', '', [])sep = cls.parser.sepaltsep = cls.parser.altsepif altsep:
passif altsep:
passpath = path.replace(altsep, sep)if (rel,):
if root:
passif not root:
if drv.startswith(sep):
pa