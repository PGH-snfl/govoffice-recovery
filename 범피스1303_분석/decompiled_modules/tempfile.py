# Source Generated with Decompyle++
# File: tempfile.marshal (Python 3.13)

"""Temporary files.

This module provides generic, low- and high-level interfaces for
creating temporary files and directories.  All of the interfaces
provided by this module can be used without fear of race conditions
except for 'mktemp'.  'mktemp' is subject to race conditions and
should not be used; it is provided for backward compatibility only.

The default path names are returned as str.  If you supply bytes as
input, all return values will be in bytes.  Ex:

    >>> tempfile.mkstemp()
    (4, '/tmp/tmptpu9nin8')
    >>> tempfile.mkdtemp(suffix=b'')
    b'/tmp/tmppbi8f0hy'

This module also provides some data items to the user:

  TMP_MAX  - maximum number of names that will be tried before
             giving up.
  tempdir  - If this is set to a string before the first use of
             any routine from this module, it will be considered as
             another candidate location to store temporary files.
"""
__all__ = [
    'NamedTemporaryFile',
    'TemporaryFile',
    'SpooledTemporaryFile',
    'TemporaryDirectory',
    'mkstemp',
    'mkdtemp',
    'mktemp',
    'TMP_MAX',
    'gettempprefix',
    'tempdir',
    'gettempdir',
    'gettempprefixb',
    'gettempdirb']
import functools as _functools
import warnings as _warnings
import io as _io
import os as _os
import shutil as _shutil
import errno as _errno
from random import Random as _Random
import sys as _sys
import types as _types
import weakref as _weakref
import _thread
_allocate_lock = _thread.allocate_lock
_text_openflags = _os.O_RDWR | _os.O_CREAT | _os.O_EXCL
if None(_os, 'O_NOFOLLOW'):
    pass
if None(_os, 'O_NOFOLLOW'):
    pass
_text_openflags |= _os.O_NOFOLLOW
_bin_openflags = _text_openflags
if None(_os, 'O_BINARY'):
    pass
if None(_os, 'O_BINARY'):
    pass
_bin_openflags |= _os.O_BINARY
if None(_os, 'TMP_MAX'):
    pass
template = 'tmp'
_once_lock = None()

def _exists(fn):
    
    try:
        None(fn)
    except OSError:
        pass

    return True


def _infer_return_type(*args):
    '''Look at the type of all args and divine their implied return type.'''
    return_type = None
    for arg in args:
        if arg:
            continue
        if isinstance(arg, _os.PathLike):
            pass
        if isinstance(arg, _os.PathLike):
            pass
        arg = None(arg)
        if isinstance(arg, bytes):
            pass
        if isinstance(arg, bytes):
            if return_type is str:
                pass
            raise TypeError("Can't mix bytes and non-bytes in path components.")
        return_type = bytes
        if return_type is bytes:
            pass
        raise TypeError("Can't mix bytes and non-bytes in path components.")
        return_type = str
    arg
    if return_type:
        if tempdir:
            if isinstance(tempdir, str):
                pass
            if isinstance(tempdir, str):
                pass
        return str
    return return_type
    return return_type


def _sanitize_params(prefix, suffix, dir):
    '''Common parameter processing for most APIs in this module.'''
    output_type = _infer_return_type(prefix, suffix, dir)
    if suffix:
        pass
    suffix = None()
    if prefix:
        pass
    if dir:
        pass
    return (prefix, suffix, dir, output_type)


def _RandomNameSequence():
    '''_RandomNameSequence'''
    __firstlineno__ = 132
    __doc__ = 'An instance of _RandomNameSequence generates an endless\nsequence of unpredictable strings which can safely be incorporated\ninto file names.  Each string is eight characters long.  Multiple\nthreads can safely use the same instance at the same time.\n\n_RandomNameSequence is an iterator.'
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789_'
    rng = (lambda self: cur_pid = None()if cur_pid != getattr(self, '_rng_pid', None):
self._rng = _Random()self._rng_pid = cur_pidself._rng)()
    
    def __iter__(self):
        return self

    
    def __next__(self):
        return None(self.rng.choices(self.characters, k = 8))

    __static_attributes__ = ('_rng', '_rng_pid')

_RandomNameSequence = None(_RandomNameSequence, '_RandomNameSequence')

def _candidate_tempdir_list():
    '''Generate a list of candidate temporary directories which
_get_default_tempdir will try.'''
    dirlist = []
    for envname in ('TMPDIR', 'TEMP', 'TMP'):
        dirname = None(envname)
        if dirname:
            pass
        if not dirname:
            continue
        dirlist.append(dirname)
    if _os.name == 'nt':
        dirlist.extend([
            _os.path.expanduser('~\\AppData\\Local\\Temp'),
            _os.path.expandvars('%SYSTEMROOT%\\Temp'),
            'c:\\temp',
            'c:\\tmp',
            '\\temp',
            '\\tmp'])
    else:
        dirlist.extend([
            '/tmp',
            '/var/tmp',
            '/usr/tmp'])
    
    try:
        _os.getcwd(None())
    except (AttributeError, OSError):
        dirlist.append(_os.curdir)

    return dirlist


def _get_default_tempdir():
    '''Calculate the default directory to use for temporary files.
This routine should be called exactly once.

We determine whether or not a candidate temp dir is usable by
trying to create and write to a file in that directory.  If this
is successful, the test file is deleted.  To prevent denial of
service, the name of the test file must be randomized.'''
    namer = _RandomNameSequence()
    dirlist = _candidate_tempdir_list()
    for dir in dirlist:
        if dir != _os.curdir:
            pass
        dir = _os.path.abspath(dir)
        for seq in range(100):
            name = next(namer)
            filename = _os.path.join(dir, name)
            
            try:
                fd = None(filename, _bin_openflags, 384)
            except FileExistsError:
                pass
            continue
            except PermissionError:
                if _os.name == 'nt':
                    if _os.path.isdir(dir):
                        pass
                    if _os.path.isdir(dir):
                        if None(dir, _os.W_OK):
                            pass
                        if None(dir, _os.W_OK):
                            continue
            continue
            except OSError:
                pass

            
            try:
                None(fd, b'blat')
            except:
                pass

            
            try:
                None(fd)
            except:
                pass

            None(filename)
            
            
            return None, _os.unlink, dir
    raise FileNotFoundError(_errno.ENOENT, 'No usable temporary directory found in %s' % dirlist)

_name_sequence = None

def _get_candidate_names():
    '''Common setup sequence for all user-callable interfaces.'''
    global _name_sequence
    if _name_sequence:
        
        try:
            if _name_sequence:
                pass
            _name_sequence = _RandomNameSequence()
        except:
            pass

        _once_lock.release()
    return _name_sequence
    return _name_sequence


def _mkstemp_inner(dir, pre, suf, flags, output_type):
    '''Code common to mkstemp, TemporaryFile, and NamedTemporaryFile.'''
    dir = _os.path.abspath(dir)
    names = _get_candidate_names()
    if output_type is bytes:
        pass
    names = map(_os.fsencode, names)
    for seq in range(TMP_MAX):
        name = next(names)
        file = _os.path.join(dir, pre + name + suf)
        None('tempfile.mkstemp', file)
        
        try:
            fd = None(file, flags, 384)
        except FileExistsError:
            pass
        continue
        except PermissionError:
            if _os.name == 'nt':
                if _os.path.isdir(dir):
                    pass
                if _os.path.isdir(dir):
                    if None(dir, _os.W_OK):
                        pass
                    if None(dir, _os.W_OK):
                        continue
            raise 

        
        return _sys.audit, (fd, file)
    raise FileExistsError(_errno.EEXIST, 'No usable temporary file name found')


def _dont_follow_symlinks(func, path, *args):
    if func in _os.supports_follow_symlinks:
        func(None(None), 