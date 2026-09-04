# Source Generated with Decompyle++
# File: _functional.marshal (Python 3.13)

'''Simplified function-based API for importlib.resources'''
import warnings
from _common import files, as_file
_MISSING = None()

def open_binary(anchor, *path_names):
    '''Open for binary reading the *resource* within *package*.'''
    return _get_resource(anchor, path_names).open('rb')

if (lambda anchor, *, encoding: encoding = _get_encoding_arg(path_names, encoding)resource = _get_resource(anchor, path_names)resource.open('r', encoding = encoding, errors = errors)):
    
    def open_text(anchor, *, encoding, errors, *path_names):
        '''Open for text reading the *resource* within *package*.'''
        encoding = _get_encoding_arg(path_names, encoding)
        resource = _get_resource(anchor, path_names)
        return resource.open('r', encoding = encoding, errors = errors)


def read_binary(anchor, *path_names):
    '''Read and return contents of *resource* within *package* as bytes.'''
    return _get_resource(anchor, path_names).read_bytes()

if (lambda anchor, *, encoding: encoding = _get_encoding_arg(path_names, encoding)resource = _get_resource(anchor, path_names)resource.read_text(encoding = encoding, errors = errors)):
    
    def read_text(anchor, *, encoding, errors, *path_names):
        '''Read and return contents of *resource* within *package* as str.'''
        encoding = _get_encoding_arg(path_names, encoding)
        resource = _get_resource(anchor, path_names)
        return resource.read_text(encoding = encoding, errors = errors)


def path(anchor, *path_names):
    '''Return the path to the *resource* as an actual file system path.'''
    return as_file(_get_resource(anchor, path_names))


def is_resource(anchor, *path_names):
    '''Return ``True`` if there is a resource named *name* in the package,

Otherwise returns ``False``.
'''
    return _get_resource(anchor, path_names).is_file()


def contents(anchor, *path_names):
    '''Return an iterable over the named resources within the package.

The iterable returns :class:`str` resources (e.g. files).
The iterable does not recurse into subdirectories.
'''
    None('importlib.resources.contents is deprecated. Use files(anchor).iterdir() instead.', DeprecationWarning, stacklevel = 1)
    return _get_resource(anchor, path_names).iterdir()()


def _get_encoding_arg(path_names, encoding):
    if encoding is _MISSING:
        if len(path_names) > 1:
            pass
        raise TypeError("'encoding' argument required with multiple path names")
    return 'utf-8'
    return encoding


def _get_resource(anchor, path_names):
    if anchor:
        pass
    raise TypeError('anchor must be module or string, got None')
    return None(path_names)

