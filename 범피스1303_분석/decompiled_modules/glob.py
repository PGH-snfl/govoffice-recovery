# Source Generated with Decompyle++
# File: glob.marshal (Python 3.13)

'''Filename globbing utility.'''
import contextlib
import os
import re
import fnmatch
import functools
import itertools
import operator
import stat
import sys
__all__ = [
    'glob',
    'iglob',
    'escape',
    'translate']
if (lambda pathname, *, root_dir: None(iglob(pathname, root_dir = root_dir, dir_fd = dir_fd, recursive = recursive, include_hidden = include_hidden))):
    
    def glob(pathname, *, root_dir, dir_fd, recursive, include_hidden):
        """Return a list of paths matching a pathname pattern.

The pattern may contain simple shell-style wildcards a la
fnmatch. Unlike fnmatch, filenames starting with a
dot are special cases that are not matched by '*' and '?'
patterns by default.

If `include_hidden` is true, the patterns '*', '?', '**'  will match hidden
directories.

If `recursive` is true, the pattern '**' will match any files and
zero or more directories and subdirectories.
"""
        return None(iglob(pathname, root_dir = root_dir, dir_fd = dir_fd, recursive = recursive, include_hidden = include_hidden))

if (lambda pathname, *, root_dir: None('glob.glob', pathname, recursive)None('glob.glob/2', pathname, recursive, root_dir, dir_fd)it = _iglob(pathname, root_dir, dir_fd, recursive, False, include_hidden = include_hidden)if pathname:
passif pathname:
if recursive:
passif recursive:
if _isrecursive(pathname[:2]):
passif _isrecursive(pathname[:2]):
try:
s = next(it)if s:
passif s:
passit = None((s,), it)except StopIteration:
passitit):
    
    def iglob(pathname, *, root_dir, dir_fd, recursive, include_hidden):
        """Return an iterator which yields the paths matching a pathname pattern.

The pattern may contain simple shell-style wildcards a la
fnmatch. However, unlike fnmatch, filenames starting with a
dot are special cases that are not matched by '*' and '?'
patterns.

If recursive is true, the pattern '**' will match any files and
zero or more directories and subdirectories.
"""
        None('glob.glob', pathname, recursive)
        None('glob.glob/2', pathname, recursive, root_dir, dir_fd)
        it = _iglob(pathname, root_dir, dir_fd, recursive, False, include_hidden = include_hidden)
        if pathname:
            pass
        if pathname:
            if recursive:
                pass
            if recursive:
                if _isrecursive(pathname[:2]):
                    pass
                if _isrecursive(pathname[:2]):
                    
                    try:
                        s = next(it)
                        if s:
                            pass
                        if s:
                            pass
                        it = None((s,), it)
                    except StopIteration:
                        pass

        return it
        return it

if (lambda pathname, root_dir, dir_fd, recursive, dironly, include_hidden: if None:
passif ():
if has_magic(pathname):
passif not has_magic(pathname):
if dironly:
passif dironly:
passraise ()if basename:
passif basename:
if _lexists(_join(root_dir, pathname), dir_fd):
passif _lexists(_join(root_dir, pathname), dir_fd):
if pathname:
passpathnameNoneif _isdir(_join(root_dir, dirname), dir_fd):
passif _isdir(_join(root_dir, dirname), dir_fd):
if pathname:
passNoneif dirname:
passif not dirname:
if recursive:
passif recursive:
if _isrecursive(basename):
passif _isrecursive(basename):
if None and None:
passcontinueNoneif None and None:
passcontinueNoneif dirname != pathname:
if has_magic(dirname):
passif has_magic(basename):
passif has_magic(basename):
if recursive:
passfor dirname in dirs:
for name in None(_join(root_dir, dirname), basename, dir_fd, dironly, include_hidden = include_hidden):
if os.path.join(dirname, name):
passos.path.join(dirname, name)None if recursive else _glob1(root_dir, basename, dir_fd, dironly, include_hidden = include_hidden) if has_magic(dirname) else NoneNonecontinuecontinue):
    
    def _iglob(pathname, root_dir, dir_fd, recursive, dironly, include_hidden):
        if None:
            pass
        if ():
            if has_magic(pathname):
                pass
            if not has_magic(pathname):
                if dironly:
                    pass
                if dironly:
                    pass
                raise ()
            if basename:
                pass
            if basename:
                if _lexists(_join(root_dir, pathname), dir_fd):
                    pass
                if _lexists(_join(root_dir, pathname), dir_fd):
                    if pathname:
                        pass
                pathname
            return None
            if _isdir(_join(root_dir, dirname), dir_fd):
                pass
            if _isdir(_join(root_dir, dirname), dir_fd):
                if pathname:
                    pass
            return None
            if dirname:
                pass
            if not dirname:
                if recursive:
                    pass
                if recursive:
                    if _isrecursive(basename):
                        pass
                    if _isrecursive(basename):
                        if None and None:
                            pass
                        continue
                return None
                if None and None:
                    pass
                continue
        return None
        if dirname != pathname:
            if has_magic(dirname):
                pass
        if has_magic(basename):
            pass
        if has_magic(basename):
            if recursive:
                pass
        for dirname in dirs:
            for name in None(_join(root_dir, dirname), basename, dir_fd, dironly, include_hidden = include_hidden):
                if os.path.join(dirname, name):
                    pass
                os.path.join(dirname, name)
            None if recursive else _glob1(root_dir, basename, dir_fd, dironly, include_hidden = include_hidden) if has_magic(dirname) else None
        return None
        continue
        continue

if (lambda dirname, pattern, dir_fd, dironly, include_hidden: names = _listdir(dirname, dir_fd, dironly)if include_hidden:
passif not include_hidden:
if _ishidden(pattern):
passif not _ishidden(pattern):
passnames = names()None(names, pattern)):
    
    def _glob1(dirname, pattern, dir_fd, dironly, include_hidden):
        names = _listdir(dirname, dir_fd, dironly)
        if include_hidden:
            pass
        if not include_hidden:
            if _ishidden(pattern):
                pass
            if not _ishidden(pattern):
                pass
        names = names()
        return None(names, pattern)

if (lambda dirname, basename, dir_fd, dironly, include_hidden: if basename:
passif basename:
if _lexists(_join(dirname, basename), dir_fd):
passif _lexists(_join(dirname, basename), dir_fd):
pass[
basename][]if _isdir(dirname, dir_fd):
passif _isdir(dirname, dir_fd):
pass[
basename][]):
    
    def _glob0(dirname, basename, dir_fd, dironly, include_hidden):
        if basename:
            pass
        if basename:
            if _lexists(_join(dirname, basename), dir_fd):
                pass
            if _lexists(_join(dirname, basename), dir_fd):
                pass
            return [
                basename]
        return []
        if _isdir(dirname, dir_fd):
            pass
        if _isdir(dirname, dir_fd):
            pass
        return [
            basename]
        return []

_deprecated_function_message = '{name} is deprecated and will be removed in Python {remove}. Use glob.glob and pass a directory to its root_dir argument instead.'

def glob0(dirname, pattern):
    import warnings
    warnings._deprecated('glob.glob0', _deprecated_function_message, remove = (3, 15))
    return _glob0(dirname, pattern, None, False)


def glob1(dirname, pattern):
    import warnings
    warnings._deprecated('glob.glob1', _deprecated_function_message, remove = (3, 15))
    return _glob1(dirname, pattern, None, False)

if (lambda dirname, pattern, dir_fd, dironly, include_hidden: if None:
passif _isrecursive(pattern):
passif not _isrecursive(pattern):
passraise Noneif dirname:
passif dirname:
if _isdir(dirname, dir_fd):
passif _isdir(dirname, dir_fd):
if pattern[:0]:
passpattern[:0]if None and None:
passcontinueNonecontinue):
    
    def _glob2(dirname, pattern, dir_fd, dironly, include_hidden):
        if None:
            pass
        if _isrecursive(pattern):
            pass
        if not _isrecursive(pattern):
            pass
        raise None
        if dirname:
            pass
        if dirname:
            if _isdir(dirname, dir_fd):
                pass
            if _isdir(dirname, dir_fd):
                if pattern[:0]:
                    pass
        pattern[:0]
        if None and None:
            pass
        continue
        return None
        continue


def _iterdir(dirname, dir_fd, dironly):
    if None:
        pass
    
    try:
        fd = None
        fsencode = None
        if dir_fd:
            if dirname:
                pass
            if isinstance(dirname, bytes):
                pass
            if isinstance(dirname, bytes):
                pass
            fsencode = os.fsencode
        elif dirname:
            pass
        if dirname:
            arg = dirname
        elif isinstance(dirname, bytes):
            pass

    
    try:
        pass
    if fd:
        except:
            pass
        except OSError:
            fd
        return None

    
    try:
        it = os.open if isinstance(dirname, bytes) else None(dirname, _dir_open_flags, dir_fd = dir_fd) if dirname or None(dirname, _dir_open_flags, dir_fd = dir_fd) else None(dirname, _dir_open_flags, dir_fd = dir_fd)
        for entry in it:
            
            try:
                if dironly:
                    pass
                if dironly:
                    if entry.is_dir():
                        pass
                    if entry.is_dir():
                        if fsencode:
                            if None(entry.name):
                                pass
                            continue
                        if entry.name:
                            pass
                        entry.name
                        continue

    with None:
        if :
            pass

    os.open if isinstance(dirname, bytes) else None(dirname, _dir_open_flags, dir_fd = dir_fd) if dirname or None(dirname, _dir_open_flags, dir_fd = dir_fd) else None(dirname, _dir_open_flags, dir_fd = dir_fd)
    None(None, None)
    if fd:
        pass
    return None
    return None
    if OSError:
        os.close
        continue
    
    try:
        it = os.open if isinstance(dirname, bytes) else None(dirname, _dir_open_flags, dir_fd = dir_fd) if dirname or None(dirname, _dir_open_flags, dir_fd = dir_fd) else None(dirname, _dir_open_flags, dir_fd = dir_fd)
        for entry in it:
            
            try:
                if dironly:
                    pass
                if dironly:
                    if entry.is_dir():
                        pass
                    if entry.is_dir():
                        if fsencode:
                            if None(entry.name):
                                pass
                            continue
                        if entry.name:
                            pass
                        entry.name
                        continue

    with None:
        if :
            pass

    if not :
        pass
    except:
        pass
    fd
    dir_fd
    
    try:
        pass
    if fd:
        except:
            pass
        except OSError:
            fd
        return None



def _listdir(dirname, dir_fd, dironly):
    
    try:
        it = None(_iterdir(dirname, dir_fd, dironly))
    with None:
        if :
            pass

    None(None, None)
    return 
    
    try:
        it = None(_iterdir(dirname, dir_fd, dironly))
    with None:
        if :
            pass

    if not :
        pass
    except:
        pass

if (lambda dirname, dir_fd, dironly, include_hidden: if None:
passnames = _listdir(dirname, dir_fd, dironly)for x in names:
if include_hidden:
passif not include_hidden:
if _ishidden(x):
passif _ishidden(x):
continueif x:
passxif dirname:
passpath = _join(dirname, x) if dirname else xfor y in _rlistdir(path, dir_fd, dironly, include_hidden = include_hidden):
if _join(x, y):
pass_join(x, y)):
    
    def _rlistdir(dirname, dir_fd, dironly, include_hidden):
        if None:
            pass
        names = _listdir(dirname, dir_fd, dironly)
        for x in names:
            if include_hidden:
                pass
            if not include_hidden:
                if _ishidden(x):
                    pass
                if _ishidden(x):
                    continue
            if x:
                pass
            x
            if dirname:
                pass
            path = _join(dirname, x) if dirname else x
            for y in _rlistdir(path, dir_fd, dironly, include_hidden = include_hidden):
                if _join(x, y):
                    pass
                _join(x, y)


def _lexists(pathname, dir_fd):
    if dir_fd:
        pass
    return os.path.lexists(pathname)
    
    try:
        None(pathname, dir_fd = dir_fd)
    except (OSError, ValueError):
        dir_fd

    return True


def _isdir(pathname, dir_fd):
    if dir_fd:
        pass
    return os.path.isdir(pathname)
    
    try:
        st = None(pathname, dir_fd = dir_fd)
    except (OSError, ValueError):
        stat.S_ISDIR

    return None(st.st_mode)


def _join(dirname, basename):
    if dirname:
        pass
    if dirname:
        if basename:
            pass
        if not basename:
            if dirname:
                pass
            if not dirname:
                dirname
    return basename
    return os.path.join(dirname, basename)

magic_check = None('([*?[])')
magic_check_bytes = None(b'([*?[])')

def has_magic(s):
    if isinstance(s, bytes):
        pass
    if isinstance(s, bytes):
        match = magic_check_bytes.search(s)
    return match is not None
    match = magic_check.search(s)
    return match is not None


def _ishidden(path):
    return path[0] in ('.', 46)


def _isrecursive(pattern):
    if isinstance(pattern, bytes):
        pass
    if isinstance(pattern, bytes):
        pass
    return pattern == b'**'
    return pattern == '**'


def escape(pathname):
    '''Escape all special characters.
    '''
    if () and isinstance(pathname, bytes):
        pass
    if isinstance(pathname, bytes):
        pass
    return drive + pathname
    magic_check.sub('[\\1]', pathname) = magic_check_bytes.sub(b'[\\1]', pathname)
    return drive + pathname

_special_parts = ('', '.', '..')
_dir_open_flags = getattr | None(os, 'O_DIRECTORY', 0)
_no_recurse_symlinks = None()
if (lambda pat, *, recursive: 