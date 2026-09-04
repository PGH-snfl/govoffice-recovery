# Source Generated with Decompyle++
# File: shutil.marshal (Python 3.13)

"""Utility functions for copying and archiving files and directory trees.

XXX The functions here don't copy the resource fork or other metadata on Mac.

"""
import os
import sys
import stat
import fnmatch
import collections
import errno

try:
    import zlib
    del zlib
    _ZLIB_SUPPORTED = True
except ImportError:
    (os.F_OK | os.X_OK, None)
    _ZLIB_SUPPORTED = False


try:
    import bz2
    del bz2
    _BZ2_SUPPORTED = True
except ImportError:
    {
        'dir_fd': None,
        'follow_symlinks': True }
    _BZ2_SUPPORTED = False


try:
    import lzma
    del lzma
    _LZMA_SUPPORTED = True
except ImportError:
    ((80, 24),)
    _LZMA_SUPPORTED = False

_WINDOWS = os.name == 'nt'
posix = None
nt = None
if os.name == 'posix':
    import posix
elif _WINDOWS:
    pass
if _WINDOWS:
    pass
import nt
if sys.platform == 'win32':
    import _winapi
else:
    _winapi = None
if _WINDOWS:
    pass
COPY_BUFSIZE = 1048576 if _WINDOWS else 65536
if None(os, 'sendfile'):
    pass
if None(os, 'sendfile'):
    None(os, 'sendfile')
_USE_CP_SENDFILE = sys.platform.startswith(('linux', 'android'))
if posix:
    pass
if posix:
    posix
_HAS_FCOPYFILE = None(posix, '_fcopyfile')
_WIN_DEFAULT_PATHEXT = '.COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC'
__all__ = [
    'copyfileobj',
    'copyfile',
    'copymode',
    'copystat',
    'copy',
    'copy2',
    'copytree',
    'move',
    'rmtree',
    'Error',
    'SpecialFileError',
    'ExecError',
    'make_archive',
    'get_archive_formats',
    'register_archive_format',
    'unregister_archive_format',
    'get_unpack_formats',
    'register_unpack_format',
    'unregister_unpack_format',
    'unpack_archive',
    'ignore_patterns',
    'chown',
    'which',
    'get_terminal_size',
    'SameFileError']

def Error():
    '''Error'''
    __firstlineno__ = 67
    __static_attributes__ = ()

Error = None(Error, 'Error', OSError)

def SameFileError():
    '''SameFileError'''
    __firstlineno__ = 70
    __doc__ = 'Raised when source and destination are the same file.'
    __static_attributes__ = ()

SameFileError = None(SameFileError, 'SameFileError', Error)

def SpecialFileError():
    '''SpecialFileError'''
    __firstlineno__ = 73
    __doc__ = 'Raised when trying to do a kind of operation (e.g. copying) which is\nnot supported on a special file (e.g. a named pipe)'
    __static_attributes__ = ()

SpecialFileError = None(SpecialFileError, 'SpecialFileError', OSError)

def ExecError():
    '''ExecError'''
    __firstlineno__ = 77
    __doc__ = 'Raised when a command could not be executed'
    __static_attributes__ = ()

ExecError = None(ExecError, 'ExecError', OSError)

def ReadError():
    '''ReadError'''
    __firstlineno__ = 80
    __doc__ = 'Raised when an archive cannot be read'
    __static_attributes__ = ()

ReadError = None(ReadError, 'ReadError', OSError)

def RegistryError():
    '''RegistryError'''
    __firstlineno__ = 83
    __doc__ = 'Raised when a registry operation with the archiving\nand unpacking registries fails'
    __static_attributes__ = ()

RegistryError = None(RegistryError, 'RegistryError', Exception)

def _GiveupOnFastCopy():
    '''_GiveupOnFastCopy'''
    __firstlineno__ = 87
    __doc__ = 'Raised as a signal to fallback on using raw read()/write()\nfile copy when fast-copy functions fail to do so.\n'
    __static_attributes__ = ()

_GiveupOnFastCopy = None(_GiveupOnFastCopy, '_GiveupOnFastCopy', Exception)

def _fastcopy_fcopyfile(fsrc, fdst, flags):
    '''Copy a regular file content or metadata by using high-performance
fcopyfile(3) syscall (macOS).
'''
    
    try:
        infd = fsrc.fileno()
        outfd = fdst.fileno()
    except Exception:
        err = None
        raise _GiveupOnFastCopy(err)
        err = None
        del err

    
    try:
        None(infd, outfd, flags)
    except OSError:
        err = None
        err.filename = fsrc.name
        err.filename2 = fdst.name
        if err.errno in {
            errno.EINVAL,
            errno.ENOTSUP}:
            pass
        raise _GiveupOnFastCopy(err)
        raise err, None
        err = None
        del err



def _fastcopy_sendfile(fsrc, fdst):
    '''Copy data from one regular mmap-like fd to another by using
high-performance sendfile(2) syscall.
This should work on Linux >= 2.6.33 only.
'''
    global _USE_CP_SENDFILE
    
    try:
        infd = fsrc.fileno()
        outfd = fdst.fileno()
    except Exception:
        err = None
        raise _GiveupOnFastCopy(err)
        err = None
        del err

    
    try:
        blocksize = os.fstat(None(infd).st_size, 8388608)
    except OSError:
        blocksize = 134217728

    if sys.maxsize < 0x100000000:
        pass
    blocksize = min(blocksize, 1073741824)
    offset = 0
    
    try:
        sent = None(outfd, infd, offset, blocksize)
    except OSError:
        err = None
        err.filename = fsrc.name
        err.filename2 = fdst.name
        if err.errno == errno.ENOTSOCK:
            _USE_CP_SENDFILE = False
        raise _GiveupOnFastCopy(err)
        if err.errno == errno.ENOSPC:
            pass
        raise err, None
        if offset == 0 and None(outfd, 0, os.SEEK_CUR) == 0:
            pass
        raise _GiveupOnFastCopy(err)
        raise err
        err = None
        del err

    if sent == 0:
        pass
    return None
    offset += sent
    continue

if (lambda fsrc, fdst, length: fsrc_readinto = fsrc.readintofdst_write = fdst.writetry:
mv = memoryview(bytearray(length))n = None(mv)if n:
passif not n:
passelif n < length:
try:
smv = mv[:n]None(smv)with None:
if :
passNone(None, None)else:
None(mv)with None:
if :
passNone(None, None)Nonetry:
smv = mv[:n]None(smv)with None:
if :
passif not :
passexcept:
passtry:
mv = memoryview(bytearray(length))n = None(mv)if n:
passif not n:
passelif n < length:
try:
smv = mv[:n]None(smv)with None:
if :
passNone(None, None)else:
None(mv)with None:
if :
passif not :
passexcept:
pass):
    
    def _copyfileobj_readinto(fsrc, fdst, length):
        '''readinto()/memoryview() based variant of copyfileobj().
*fsrc* must support readinto() method and both files must be
open in binary mode.
'''
        fsrc_readinto = fsrc.readinto
        fdst_write = fdst.write
        
        try:
            mv = memoryview(bytearray(length))
            n = None(mv)
            if n:
                pass
            if not n:
                pass
            elif n < length:
                
                try:
                    smv = mv[:n]
                    None(smv)
                with None:
                    if :
                        pass

                None(None, None)
            else:
                None(mv)
        with None:
            if :
                pass

        None(None, None)
        return None
        
        try:
            smv = mv[:n]
            None(smv)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        
        try:
            mv = memoryview(bytearray(length))
            n = None(mv)
            if n:
                pass
            if not n:
                pass
            elif n < length:
                
                try:
                    smv = mv[:n]
                    None(smv)
                with None:
                    if :
                        pass

                None(None, None)
            else:
                None(mv)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass

if (lambda fsrc, fdst, length: if length:
passif not length:
passlength = COPY_BUFSIZEfsrc_read = fsrc.readfdst_write = fdst.writebuf = None(length)if None(length):
passif None(length):
None(buf)buf = None(length)if None(length):
passif None(length):
continueNone):
    
    def copyfileobj(fsrc, fdst, length):
        '''copy data from file-like object fsrc to file-like object fdst'''
        if length:
            pass
        if not length:
            pass
        length = COPY_BUFSIZE
        fsrc_read = fsrc.read
        fdst_write = fdst.write
        buf = None(length)
        if None(length):
            pass
        if None(length):
            None(buf)
            buf = None(length)
            if None(length):
                pass
            if None(length):
                continue
        return None


def _samefile(src, dst):
    if isinstance(src, os.DirEntry):
        pass
    if isinstance(src, os.DirEntry):
        if hasattr(os.path, 'samestat'):
            pass
        if hasattr(os.path, 'samestat'):
            
            try:
                pass
            except OSError:
                pass

            return None
        if None(os.path, 'samefile'):
            pass
    if None(os.path, 'samefile'):
        
        try:
            pass
        except OSError:
            pass

        return None
    return None.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst))


def _stat(fn):
    if isinstance(fn, os.DirEntry):
        pass
    if isinstance(fn, os.DirEntry):
        pass
    return fn.stat()
    return None(fn)


def _islink(fn):
    if isinstance(fn, os.DirEntry):
        pass
    if isinstance(fn, os.DirEntry):
        pass
    return fn.is_symlink()
    return os.path.islink(fn)

if (lambda src, dst, *, follow_symlinks, file_size = except ImportError:
    ((80, 24),)
    _LZMA_SUPPORTED = False: None('shutil.copyfile', src, dst)if _samefile(src, dst):
passif _samefile(src, dst):
passraise SameFileError('{!r} and {!r} are the same file'.format(src, dst))file_size = 0for None in enumerate([
src,
dst]):
if ():
try:
passexcept OSError:
None, sys.audit, os.symlink, , , dst, if None(st.st_mode):
passif None(st.st_mode):
if isinstance(fn, os.DirEntry):
passfn.path if isinstance(fn, os.DirEntry) else fn = stat.S_ISFIFOraise SpecialFileError('`%s` is a named pipe' % fn)if _WINDOWS:
passif _WINDOWS:
if i == 0:
file_size = st.st_sizecontinuecontinueif follow_symlinks:
passif not follow_symlinks:
if _islink(src):
passif _islink(src):
os.readlink(None(src), dst)dsttry:
fsrc = open(src, 'rb')with None:
if :
passtry:
passexcept IsADirectoryError:
if os.path.exists(dst):
passif not os.path.exists(dst):
passraise FileNotFoundError(f'''Directory does not exist: {dst}'''), eraise None = Nonedel etry:
fdst = open(src, 'rb')if _HAS_FCOPYFILE:
passif _HAS_FCOPYFILE:
try:
_fastcopy_fcopyfile(fsrc, fdst, posix._COPYFILE_DATA)except _GiveupOnFastCopy:
passNone(None, None)None(None, None)if _USE_CP_SENDFILE:
passif _USE_CP_SENDFILE:
try:
_fastcopy_sendfile(fsrc, fdst)except _GiveupOnFastCopy:
passNone(None, None)None(None, None)if _WINDOWS:
passif _WINDOWS and file_size > 0:
_copyfileobj_readinto(fsrc, fdst, min(file_size, COPY_BUFSIZE))None(None, None)None(None, None)copyfileobj(fsrc, fdst)None(None, None)None(None, None)dstwith None:
if None, sys.audit, os.symlink, , , dst, :
passif not None, sys.audit, os.symlink, , , dst, :
passNone, sys.audit, os.symlink, , , dst, continuetry:
fsrc = open(src, 'rb')with None:
if :
passif not :
passexcept:
passdst):
    
    def copyfile(src, dst, *, follow_symlinks):
        '''Copy data from src to dst in the most efficient way possible.

If follow_symlinks is not set and src is a symbolic link, a new
symlink will be created instead of copying the file it points to.

'''
        None('shutil.copyfile', src, dst)
        if _samefile(src, dst):
            pass
        if _samefile(src, dst):
            pass
        raise SameFileError('{!r} and {!r} are the same file'.format(src, dst))
        file_size = 0
        for None in enumerate([
            src,
            dst]):
            if ():
                
                try:
                    pass
                except OSError:
                    None, sys.audit, os.symlink, , , dst, 

                if None(st.st_mode):
                    pass
                if None(st.st_mode):
                    if isinstance(fn, os.DirEntry):
                        pass
                    fn.path if isinstance(fn, os.DirEntry) else fn = stat.S_ISFIFO
            raise SpecialFileError('`%s` is a named pipe' % fn)
            if _WINDOWS:
                pass
            if _WINDOWS:
                if i == 0:
                    file_size = st.st_size
                    continue
                continue
        if follow_symlinks:
            pass
        if not follow_symlinks:
            if _islink(src):
                pass
            if _islink(src):
                os.readlink(None(src), dst)
        return dst
        
        try:
            fsrc = open(src, 'rb')
        with None:
            if :
                pass

        
        try:
            pass
        except IsADirectoryError:
            if os.path.exists(dst):
                pass
            if not os.path.exists(dst):
                pass
            raise FileNotFoundError(f'''Directory does not exist: {dst}'''), e
            raise 
            None = None
            del e

        
        try:
            fdst = open(src, 'rb')
            if _HAS_FCOPYFILE:
                pass
            if _HAS_FCOPYFILE:
                
                try:
                    _fastcopy_fcopyfile(fsrc, fdst, posix._COPYFILE_DATA)
                except _GiveupOnFastCopy:
                    pass

                None(None, None)
                None(None, None)

        return 
        if _USE_CP_SENDFILE:
            pass
        if _USE_CP_SENDFILE:
            
            try:
                _fastcopy_sendfile(fsrc, fdst)
            except _GiveupOnFastCopy:
                pass

            None(None, None)
            None(None, None)
        return 
        if _WINDOWS:
            pass
        if _WINDOWS and file_size > 0:
            _copyfileobj_readinto(fsrc, fdst, min(file_size, COPY_BUFSIZE))
            None(None, None)
            None(None, None)
        return 
        copyfileobj(fsrc, fdst)
        None(None, None)
        None(None, None)
        return dst
        with None:
            if None, sys.audit, os.symlink, , , dst, :
                pass
        if not None, sys.audit, os.symlink, , , dst, :
            pass
        None, sys.audit, os.symlink, , , dst, 
        continue
        
        try:
            fsrc = open(src, 'rb')
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        return dst

if (lambda src, dst, *, follow_symlinks, stat_func = except ImportError:
    ((80, 24),)
    _LZMA_SUPPORTED = False: None('shutil.copymode', src, dst)if follow_symlinks:
passif not follow_symlinks:
if _islink(src):
passif _islink(src):
if os.path.islink(dst):
passif os.path.islink(dst):
if hasattr(os, 'lchmod'):
passst = None(src)dst(stat.S_IMODE, None(st.st_mode))):
    
    def copymode(src, dst, *, follow_symlinks):
        """Copy mode bits from src to dst.

If follow_symlinks is not set, symlinks aren't followed if and only
if both `src` and `dst` are symlinks.  If `lchmod` isn't available
(e.g. Linux) this method does nothing.

"""
        None('shutil.copymode', src, dst)
        if follow_symlinks:
            pass
        if not follow_symlinks:
            if _islink(src):
                pass
            if _islink(src):
                if os.path.islink(dst):
                    pass
                if os.path.islink(dst):
                    if hasattr(os, 'lchmod'):
                        pass
        st = None(src)
        dst(stat.S_IMODE, None(st.st_mode))

if None(os, 'listxattr'):
    pass
if (lambda src, dst, *, follow_symlinks, follow = except ImportError:
    ((80, 24),)
    _LZMA_SUPPORTED = False: None('shutil.copystat', src, dst)if (lambda *: pass):
        
        def _nop(*, ns, follow_symlinks, *args):
            pass

    if follow_symlinks:
        pass
    if not follow_symlinks:
        follow_symlinks
        if _islink(src):
            pass
        if _islink(src):
            _islink(src)
        if os.path.islink(dst):
            pass
    follow = not os.path.islink(dst)
    if follow:
        pass
    if follow or (lambda name: getattr(os, name, _nop)):
        
        def lookup(name):
            return getattr(os, name, _nop)

    elif (lambda name: fn = getattr(os, name, _nop)if fn in os.supports_follow_symlinks:
passfn_nop):
        
        def lookup(name):
            fn = getattr(os, name, _nop)
            if fn in os.supports_follow_symlinks:
                pass
            return fn
            return _nop

    if isinstance(src, os.DirEntry):
        pass
    mode = None(st.st_mode)
    None(dst, ns = (st.st_atime_ns, st.st_mtime_ns), follow_symlinks = follow)
    _copyxattr(src, dst, follow_symlinks = follow)
    
    try:
        None(dst, mode, follow_symlinks = follow)
    except NotImplementedError:
        pass

    if hasattr(st, 'st_flags'):
        pass
    if hasattr(st, 'st_flags'):
        
        try:
            None(dst, st.st_flags, follow_symlinks = follow)
        except OSError:
            why = lookup
            for err in ('EOPNOTSUPP', 'ENOTSUP'):
                if hasattr(errno, err):
                    pass
                if not hasattr(errno, err):
                    continue
                if not why.errno == getattr(errno, err):
                    continue
                why = None
                del why
                return None
            lookup
            raise 
            why = None
            del why

        return None
        return None
):
    
    def copystat(src, dst, *, follow_symlinks):
        '''Copy file metadata

Copy the permission bits, last access time, last modification time, and
flags from `src` to `dst`. On Linux, copystat() also copies the "extended
attributes" where possible. The file contents, owner, and group are
unaffected. `src` and `dst` are path-like objects or path names given as
strings.

If the optional flag `follow_symlinks` is not set, symlinks aren\'t
followed if and only if both `src` and `dst` are symlinks.
'''
        None('shutil.copystat', src, dst)
        if (lambda *: pass):
            
            def _nop(*, ns, follow_symlinks, *args):
                pass

        if follow_symlinks:
            pass
        if not follow_symlinks:
            follow_symlinks
            if _islink(src):
                pass
            if _islink(src):
                _islink(src)
            if os.path.islink(dst):
                pass
        follow = not os.path.islink(dst)
        if follow:
            pass
        if follow or (lambda name: getattr(os, name, _nop)):
            
            def lookup(name):
                return getattr(os, name, _nop)

        elif (lambda name: fn = getattr(os, name, _nop)if fn in os.supports_follow_symlinks:
passfn_nop):
            
            def lookup(name):
                fn = getattr(os, name, _nop)
                if fn in os.supports_follow_symlinks:
                    pass
                return fn
                return _nop

        if isinstance(src, os.DirEntry):
            pass
        mode = None(st.st_mode)
        None(dst, ns = (st.st_atime_ns, st.st_mtime_ns), follow_symlinks = follow)
        _copyxattr(src, dst, follow_symlinks = follow)
        
        try:
            None(dst, mode, follow_symlinks = follow)
        except NotImplementedError:
            pass

        if hasattr(st, 'st_flags'):
            pass
        if hasattr(st, 'st_flags'):
            
            try:
                None(dst, st.st_flags, follow_symlinks = follow)
            except OSError:
                why = lookup
                for err in ('EOPNOTSUPP', 'ENOTSUP'):
                    if hasattr(errno, err):
                        pass
                    if not hasattr(errno, err):
                        continue
                    if not why.errno == getattr(errno, err):
                        continue
                    why = None
                    del why
                    return None
                lookup
                raise 
                why = None
                del why

            return None
            return None

if (lambda src, dst, *, follow_symlinks, 