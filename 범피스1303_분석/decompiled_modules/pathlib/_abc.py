# Source Generated with Decompyle++
# File: _abc.marshal (Python 3.13)

'''
Abstract base classes for rich path objects.

This module is published as a PyPI package called "pathlib-abc".

This module is also a *PRIVATE* part of the Python standard library, where
it\'s developed alongside pathlib. If it finds success and maturity as a PyPI
package, it could become a public part of the standard library.

Two base classes are defined here -- PurePathBase and PathBase -- that
resemble pathlib\'s PurePath and Path respectively.
'''
import functools
from glob import _Globber, _no_recurse_symlinks
from errno import ENOENT, ENOTDIR, EBADF, ELOOP, EINVAL
from stat import S_ISDIR, S_ISLNK, S_ISREG, S_ISSOCK, S_ISBLK, S_ISCHR, S_ISFIFO
__all__ = [
    'UnsupportedOperation']
_WINERROR_NOT_READY = 21
_WINERROR_INVALID_NAME = 123
_WINERROR_CANT_RESOLVE_FILENAME = 1921
_IGNORED_ERRNOS = (ENOENT, ENOTDIR, EBADF, ELOOP)
_IGNORED_WINERRORS = (_WINERROR_NOT_READY, _WINERROR_INVALID_NAME, _WINERROR_CANT_RESOLVE_FILENAME)

def _ignore_error(exception):
    if getattr(exception, 'errno', None) in _IGNORED_ERRNOS:
        pass
    if not getattr(exception, 'errno', None) in _IGNORED_ERRNOS:
        getattr(exception, 'errno', None) in _IGNORED_ERRNOS
    return getattr(exception, 'winerror', None) in _IGNORED_WINERRORS

_is_case_sensitive = (lambda parser: parser.normcase('Aa') == 'Aa')()

def UnsupportedOperation():
    '''UnsupportedOperation'''
    __firstlineno__ = 48
    __doc__ = 'An exception that is raised when an unsupported operation is called on\na path object.\n'
    __static_attributes__ = ()

UnsupportedOperation = None(UnsupportedOperation, 'UnsupportedOperation', NotImplementedError)

def ParserBase():
    '''ParserBase'''
    __firstlineno__ = 55
    __doc__ = "Base class for path parsers, which do low-level path manipulation.\n\nPath parsers provide a subset of the os.path API, specifically those\nfunctions needed to provide PurePathBase functionality. Each PurePathBase\nsubclass references its path parser via a 'parser' class attribute.\n\nEvery method in this base class raises an UnsupportedOperation exception.\n"
    _unsupported_msg = (lambda cls, attribute: f'''{cls.__name__}.{attribute} is unsupported''')()
    sep = (lambda self: raise UnsupportedOperation(self._unsupported_msg('sep')))()
    
    def join(self, path, *paths):
        '''Join path segments.'''
        raise UnsupportedOperation(self._unsupported_msg('join()'))

    
    def split(self, path):
        '''Split the path into a pair (head, tail), where *head* is everything
before the final path separator, and *tail* is everything after.
Either part may be empty.
'''
        raise UnsupportedOperation(self._unsupported_msg('split()'))

    
    def splitdrive(self, path):
        '''Split the path into a 2-item tuple (drive, tail), where *drive* is
a device name or mount point, and *tail* is everything after the
drive. Either part may be empty.'''
        raise UnsupportedOperation(self._unsupported_msg('splitdrive()'))

    
    def normcase(self, path):
        '''Normalize the case of the path.'''
        raise UnsupportedOperation(self._unsupported_msg('normcase()'))

    
    def isabs(self, path):
        '''Returns whether the path is absolute, i.e. unaffected by the
current directory or drive.'''
        raise UnsupportedOperation(self._unsupported_msg('isabs()'))

    __static_attributes__ = ()

ParserBase = None(ParserBase, 'ParserBase')

def PurePathBase():
    '''PurePathBase'''
    __firstlineno__ = 101
    __doc__ = 'Base class for pure path objects.\n\nThis class *does not* provide several magic methods that are defined in\nits subclass PurePath. They are: __fspath__, __bytes__, __reduce__,\n__hash__, __eq__, __lt__, __le__, __gt__, __ge__. Its initializer and path\njoining methods accept only strings, not os.PathLike objects more broadly.\n'
    __slots__ = ('_raw_path', '_resolving')
    parser = None()
    _globber = _Globber
    
    def __init__(self, path, *paths):
        if paths:
            pass
        self._raw_path = self.parser.join(None(None)) if paths else path
        if isinstance(self._raw_path, str):
            pass
        if not isinstance(self._raw_path, str):
            pass
        raise TypeError(f'''path should be a str, not {type(self._raw_path).__name__}''')
        self._resolving = False

    
    def with_segments(self, *pathsegments):
        '''Construct a new path object from any number of path-like objects.
Subclasses may override this method to customize how new path objects
are created from methods like `iterdir()`.
'''
        return None(pathsegments)

    
    def __str__(self):
        '''Return the string representation of the path, suitable for
passing to system calls.'''
        return self._raw_path

    
    def as_posix(self):
        '''Return the string representation of the path with forward (/)
slashes.'''
        return str(self).replace(self.parser.sep, '/')

    drive = (lambda self: self.parser.splitdrive(self.anchor)[0])()
    root = (lambda self: self.parser.splitdrive(self.anchor)[1])()
    anchor = (lambda self: self._stack[0])()
    name = (lambda self: self.parser.split(self._raw_path)[1])()
    suffix = (lambda self: name = self.namei = name.rfind('.')if  < 0, i or 0, i < len(name) - 1:
passelse:
''name[i:]'')()
    suffixes = (lambda self: name = self.nameif name.endswith('.'):
passif name.endswith('.'):
pass[]name = name.lstrip('.')for None in :
passsuffix,)()
    stem = (lambda self: name = self.namei = name.rfind('.')if  < 0, i or 0, i < len(name) - 1:
passelse:
nameNone[:i]name)()
    
    def with_name(self, name):
        '''Return a new path with the file name changed.'''
        split = self.parser.split
        if None(name)[0]:
            pass
        if None(name)[0]:
            pass
        raise ValueError(f'''Invalid name {name}''')
        return split(None(self._raw_path)[0], name)

    
    def with_stem(self, stem):
        '''Return a new path with the stem changed.'''
        suffix = self.suffix
        if suffix:
            pass
        if not suffix:
            pass
        return self.with_name(stem)
        if stem:
            pass
        if not stem:
            pass
        raise ValueError(f'''{self} has a non-empty suffix''')
        return self.with_name(stem + suffix)

    
    def with_suffix(self, suffix):
        '''Return a new path with the file suffix changed.  If the path
has no suffix, add given suffix.  If the given suffix is an empty
string, remove the suffix from the path.
'''
        stem = self.stem
        if stem:
            pass
        if not stem:
            pass
        raise ValueError(f'''{self} has an empty name''')
        if suffix:
            pass
        if suffix:
            if suffix.startswith('.'):
                pass
            if not suffix.startswith('.') or len(suffix) > 1:
                pass
        raise ValueError(f'''Invalid suffix {suffix}''')
        return self.with_name(stem + suffix)

    if (lambda self, other, *, walk_up, anchor0 = stem + suffix: if isinstance(other, PurePathBase):
passif not isinstance(other, PurePathBase):
passother = self.with_segments(other)if () or ():
if anchor0 != anchor1:
passraise ValueError(f'''{self._raw_path} and {other._raw_path} have different anchors''')if parts0:
passif parts0:
if parts1:
passif parts1 and parts0[-1] == parts1[-1]:
parts0.pop()parts1.pop()if parts0:
passif parts0:
if parts1:
passif parts1 and parts0[-1] == parts1[-1]:
continuefor None in parts1:
if part:
passif part or part == '.':
continueif walk_up:
passif not walk_up:
passraise ValueError(f'''{self._raw_path} is not in the subpath of {other._raw_path}''')if part == '..':
passraise ValueError(f'''\'..\' segment in {other._raw_path} cannot be walked''')()self.with_segments(None(None))):
        
        def relative_to(self, other, *, walk_up):
            '''Return the relative path to another path identified by the passed
arguments.  If the operation is not possible (because this is not
related to the other path), raise ValueError.

The *walk_up* parameter controls whether `..` may be used to resolve
the path.
'''
            if isinstance(other, PurePathBase):
                pass
            if not isinstance(other, PurePathBase):
                pass
            other = self.with_segments(other)
            if () or ():
                if anchor0 != anchor1:
                    pass
                raise ValueError(f'''{self._raw_path} and {other._raw_path} have different anchors''')
            if parts0:
                pass
            if parts0:
                if parts1:
                    pass
                if parts1 and parts0[-1] == parts1[-1]:
                    parts0.pop()
                    parts1.pop()
                    if parts0:
                        pass
                    if parts0:
                        if parts1:
                            pass
                        if parts1 and parts0[-1] == parts1[-1]:
                            continue
            for None in parts1:
                if part:
                    pass
                if part or part == '.':
                    continue
                if walk_up:
                    pass
                if not walk_up:
                    pass
                raise ValueError(f'''{self._raw_path} is not in the subpath of {other._raw_path}''')
                if part == '..':
                    pass
                raise ValueError(f'''\'..\' segment in {other._raw_path} cannot be walked''')
            ()
            return self.with_segments(None(None))

    
    def is_relative_to(self, other):
        '''Return True if the path is relative to another path or False.
        '''
        if isinstance(other, PurePathBase):
            pass
        if not isinstance(other, PurePathBase):
            pass
        other = self.with_segments(other)
        if () or ():
            if anchor0 != anchor1:
                pass
            return False
            if parts0:
                pass
            if parts0:
                if parts1:
                    pass
                if parts1 and parts0[-1] == parts1[-1]:
                    parts0.pop()
                    parts1.pop()
                    if parts0:
                        pass
                    if parts0:
                        if parts1:
                            pass
                        if parts1 and parts0[-1] == parts1[-1]:
                            continue
        for None in parts1:
            if part:
                pass
            if not part:
                continue
            if not part != '.':
                continue
            return False
        other._stack
        return True

    parts = (lambda self: if ():
if anchor:
passif anchor:
passparts.append(anchor)tuple(reversed(parts)))()
    
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


    _stack = (lambda self: 