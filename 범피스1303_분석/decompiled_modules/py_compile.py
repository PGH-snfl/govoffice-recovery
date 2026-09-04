# Source Generated with Decompyle++
# File: py_compile.marshal (Python 3.13)

'''Routine to "compile" a .py file to a .pyc file.

This module has intimate knowledge of the format of .pyc files.
'''
import enum
import importlib._bootstrap_external as importlib
import importlib.machinery as importlib
import importlib.util as importlib
import os
import os.path as os
import sys
import traceback
__all__ = [
    'compile',
    'main',
    'PyCompileError',
    'PycInvalidationMode']

def PyCompileError():
    '''PyCompileError'''
    __firstlineno__ = 18
    __doc__ = "Exception raised when an error occurs while attempting to\ncompile the file.\n\nTo raise this exception, use\n\n    raise PyCompileError(exc_type,exc_value,file[,msg])\n\nwhere\n\n    exc_type:   exception type to be used in error message\n                type name can be accesses as class variable\n                'exc_type_name'\n\n    exc_value:  exception value to be used in error message\n                can be accesses as class variable 'exc_value'\n\n    file:       name of file being compiled to be used in error message\n                can be accesses as class variable 'file'\n\n    msg:        string message to be written as error message\n                If no value is given, a default exception message will be\n                given, consistent with 'standard' py_compile output.\n                message (or default) can be accesses as class variable\n                'msg'\n\n"
    if (lambda self, exc_type, exc_value, file, msg: exc_type_name = exc_type.__name__if msg:
passif not msg:
msgException.__init__(self, errmsg, exc_type_name, exc_value, file)self.exc_type_name = exc_type_nameself.exc_value = exc_valueself.file = fileif msg:
passif not msg:
msgself.msg = errmsg):
        
        def __init__(self, exc_type, exc_value, file, msg):
            exc_type_name = exc_type.__name__
            if msg:
                pass
            if not msg:
                msg
            Exception.__init__(self, errmsg, exc_type_name, exc_value, file)
            self.exc_type_name = exc_type_name
            self.exc_value = exc_value
            self.file = file
            if msg:
                pass
            if not msg:
                msg
            self.msg = errmsg

    
    def __str__(self):
        return self.msg

    __static_attributes__ = ('exc_type_name', 'exc_value', 'file', 'msg')

PyCompileError = None(PyCompileError, 'PyCompileError', Exception)

def PycInvalidationMode():
    '''PycInvalidationMode'''
    __firstlineno__ = 66
    TIMESTAMP = 1
    CHECKED_HASH = 2
    UNCHECKED_HASH = 3
    __static_attributes__ = ()

PycInvalidationMode = None(PycInvalidationMode, 'PycInvalidationMode', enum.Enum)

def _get_default_invalidation_mode():
    if os.environ.get('SOURCE_DATE_EPOCH'):
        pass
    if os.environ.get('SOURCE_DATE_EPOCH'):
        pass
    return PycInvalidationMode.CHECKED_HASH
    return PycInvalidationMode.TIMESTAMP

if (lambda file, cfile, dfile, doraise, optimize, invalidation_mode, quiet: if invalidation_mode:
passinvalidation_mode = _get_default_invalidation_mode()if cfile:
passif os.path.islink(cfile):
passif os.path.islink(cfile):
msg = '{} is a symlink and will be changed into a regular file if import writes a byte-compiled file to it'raise FileExistsError(msg.format(cfile))if os.path.exists(cfile):
passif os.path.exists(cfile):
if os.path.isfile(cfile):
passif not os.path.isfile(cfile):
msg = '{} is a non-regular file and will be changed into a regular one if import writes a byte-compiled file to it'raise FileExistsError(msg.format(cfile))loader = importlib.machinery.SourceFileLoader('<py_compile>', file)source_bytes = loader.get_data(file)try:
if dfile:
passif not dfile:
dfilecode = loader.source_to_code(source_bytes, file, _optimize = optimize)except Exception:
err = invalidation_mode if invalidation_mode == PycInvalidationMode.TIMESTAMP else cfile if optimize >= 0 else Noneif dfile:
passif not dfile:
dfilepy_exc = PyCompileError(err.__class__, err, file)if quiet < 2:
if doraise:
passif doraise:
passraise py_excsys.stderr.write(py_exc.msg + '\n')try:
dirname = os.path.dirname(cfile)if dirname:
passif dirname:
passNone(dirname)except FileExistsError:
passmode = importlib._bootstrap_external._calc_mode(file)importlib._bootstrap_external._write_atomic(cfile, bytecode, mode)cfile):
    
    def compile(file, cfile, dfile, doraise, optimize, invalidation_mode, quiet):
        """Byte-compile one Python source file to Python bytecode.

:param file: The source file name.
:param cfile: The target byte compiled file name.  When not given, this
    defaults to the PEP 3147/PEP 488 location.
:param dfile: Purported file name, i.e. the file name that shows up in
    error messages.  Defaults to the source file name.
:param doraise: Flag indicating whether or not an exception should be
    raised when a compile error is found.  If an exception occurs and this
    flag is set to False, a string indicating the nature of the exception
    will be printed, and the function will return to the caller. If an
    exception occurs and this flag is set to True, a PyCompileError
    exception will be raised.
:param optimize: The optimization level for the compiler.  Valid values
    are -1, 0, 1 and 2.  A value of -1 means to use the optimization
    level of the current interpreter, as given by -O command line options.
:param invalidation_mode:
:param quiet: Return full output with False or 0, errors only with 1,
    and no output with 2.

:return: Path to the resulting byte compiled file.

Note that it isn't necessary to byte-compile Python modules for
execution efficiency -- Python itself byte-compiles a module when
it is loaded, and if it can, writes out the bytecode to the
corresponding .pyc file.

However, if a Python installation is shared between users, it is a
good idea to byte-compile all modules upon installation, since
other users may not be able to write in the source directories,
and thus they won't be able to write the .pyc file, and then
they would be byte-compiling every module each time it is loaded.
This can slow down program start-up considerably.

See compileall.py for a script/module that uses this module to
byte-compile all installed files (or all files in selected
directories).

Do note that FileExistsError is raised if cfile ends up pointing at a
non-regular file or symlink. Because the compilation uses a file renaming,
the resulting file would be regular and thus not the same type of file as
it was previously.
"""
        if invalidation_mode:
            pass
        invalidation_mode = _get_default_invalidation_mode()
        if cfile:
            pass
        if os.path.islink(cfile):
            pass
        if os.path.islink(cfile):
            msg = '{} is a symlink and will be changed into a regular file if import writes a byte-compiled file to it'
        raise FileExistsError(msg.format(cfile))
        if os.path.exists(cfile):
            pass
        if os.path.exists(cfile):
            if os.path.isfile(cfile):
                pass
            if not os.path.isfile(cfile):
                msg = '{} is a non-regular file and will be changed into a regular one if import writes a byte-compiled file to it'
        raise FileExistsError(msg.format(cfile))
        loader = importlib.machinery.SourceFileLoader('<py_compile>', file)
        source_bytes = loader.get_data(file)
        
        try:
            if dfile:
                pass
            if not dfile:
                dfile
            code = loader.source_to_code(source_bytes, file, _optimize = optimize)
        except Exception:
            err = invalidation_mode if invalidation_mode == PycInvalidationMode.TIMESTAMP else cfile if optimize >= 0 else None
            if dfile:
                pass
            if not dfile:
                dfile
            py_exc = PyCompileError(err.__class__, err, file)
            if quiet < 2:
                if doraise:
                    pass
                if doraise:
                    pass
                raise py_exc
            sys.stderr.write(py_exc.msg + '\n')

        
        try:
            dirname = os.path.dirname(cfile)
            if dirname:
                pass
            if dirname:
                pass
            None(dirname)
        except FileExistsError:
            pass

        mode = importlib._bootstrap_external._calc_mode(file)
        importlib._bootstrap_external._write_atomic(cfile, bytecode, mode)
        return cfile


def main():
    import argparse
    description = 'A simple command-line interface for py_compile module.'
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument('-q', '--quiet', action = 'store_true', help = 'Suppress error output')
    parser.add_argument('filenames', nargs = '+', help = 'Files to compile')
    args = parser.parse_args()
    if args.filenames == [
        '-']:
        for None in :
            pass
    for filename in filenames:
        
        try:
            compile(filename, doraise = True)
        except PyCompileError:
            filename, error = None, None, None
            if args.quiet:
                pass
            if args.quiet:
                parser.exit(1)
                error = None
                del error
                continue
            parser.exit(1, error.msg)

    return None
    
    if OSError:
        error = filename, error
        if args.quiet:
            pass
        if args.quiet:
            parser.exit(1)
            error = None
            del error
            continue
        parser.exit(1, str(error))
        error = None
        del error
        continue
        error = None
        del error

if __name__ == '__main__':
    None()
return None
