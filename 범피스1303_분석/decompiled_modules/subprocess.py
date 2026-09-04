# Source Generated with Decompyle++
# File: subprocess.marshal (Python 3.13)

'''Subprocesses with accessible I/O streams

This module allows you to spawn processes, connect to their
input/output/error pipes, and obtain their return codes.

For a complete description of this module see the Python documentation.

Main API
========
run(...): Runs a command, waits for it to complete, then returns a
          CompletedProcess instance.
Popen(...): A class for flexibly executing a command in a new process

Constants
---------
DEVNULL: Special value that indicates that os.devnull should be used
PIPE:    Special value that indicates a pipe should be created
STDOUT:  Special value that indicates that stderr should go to stdout


Older API
=========
call(...): Runs a command, waits for it to complete, then returns
    the return code.
check_call(...): Same as call() but raises CalledProcessError()
    if return code is not 0
check_output(...): Same as check_call() but returns the contents of
    stdout instead of a return code
getoutput(...): Runs a command in the shell, waits for it to complete,
    then returns the output
getstatusoutput(...): Runs a command in the shell, waits for it to complete,
    then returns a (exitcode, output) tuple
'''
import builtins
import errno
import io
import locale
import os
import time
import signal
import sys
import threading
import warnings
import contextlib
from time import monotonic as _time
import types

try:
    import fcntl
except ImportError:
    <NODE:27>
    fcntl = None

__all__ = [
    'Popen',
    'PIPE',
    'STDOUT',
    'call',
    'check_call',
    'getstatusoutput',
    'getoutput',
    'check_output',
    'run',
    'CalledProcessError',
    'DEVNULL',
    'SubprocessError',
    'TimeoutExpired',
    'CompletedProcess']

try:
    import msvcrt
except ModuleNotFoundError:
    _use_posix_spawn
    _mswindows = False

_mswindows = True
_can_fork_exec = sys.platform not in frozenset({'ios', 'tvos', 'wasi', 'watchos', 'emscripten'})
if _mswindows:
    pass
if _mswindows:
    import _winapi
    from _winapi import CREATE_NEW_CONSOLE, CREATE_NEW_PROCESS_GROUP, STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE, SW_HIDE, STARTF_USESTDHANDLES, STARTF_USESHOWWINDOW, STARTF_FORCEONFEEDBACK, STARTF_FORCEOFFFEEDBACK, ABOVE_NORMAL_PRIORITY_CLASS, BELOW_NORMAL_PRIORITY_CLASS, HIGH_PRIORITY_CLASS, IDLE_PRIORITY_CLASS, NORMAL_PRIORITY_CLASS, REALTIME_PRIORITY_CLASS, CREATE_NO_WINDOW, DETACHED_PROCESS, CREATE_DEFAULT_ERROR_MODE, CREATE_BREAKAWAY_FROM_JOB
    __all__.extend([
        'CREATE_NEW_CONSOLE',
        'CREATE_NEW_PROCESS_GROUP',
        'STD_INPUT_HANDLE',
        'STD_OUTPUT_HANDLE',
        'STD_ERROR_HANDLE',
        'SW_HIDE',
        'STARTF_USESTDHANDLES',
        'STARTF_USESHOWWINDOW',
        'STARTF_FORCEONFEEDBACK',
        'STARTF_FORCEOFFFEEDBACK',
        'STARTUPINFO',
        'ABOVE_NORMAL_PRIORITY_CLASS',
        'BELOW_NORMAL_PRIORITY_CLASS',
        'HIGH_PRIORITY_CLASS',
        'IDLE_PRIORITY_CLASS',
        'NORMAL_PRIORITY_CLASS',
        'REALTIME_PRIORITY_CLASS',
        'CREATE_NO_WINDOW',
        'DETACHED_PROCESS',
        'CREATE_DEFAULT_ERROR_MODE',
        'CREATE_BREAKAWAY_FROM_JOB'])
elif _can_fork_exec:
    pass
import select
import selectors

def SubprocessError():
    '''SubprocessError'''
    __firstlineno__ = 129
    __static_attributes__ = ()

SubprocessError = None(SubprocessError, 'SubprocessError', Exception)

def CalledProcessError():
    '''CalledProcessError'''
    __firstlineno__ = 132
    __doc__ = 'Raised when run() is called with check=True and the process\nreturns a non-zero exit status.\n\nAttributes:\n  cmd, returncode, stdout, stderr, output\n'
    if (lambda self, returncode, cmd, output, stderr: self.returncode = returncodeself.cmd = cmdself.output = outputself.stderr = stderr):
        
        def __init__(self, returncode, cmd, output, stderr):
            self.returncode = returncode
            self.cmd = cmd
            self.output = output
            self.stderr = stderr

    
    def __str__(self):
        if self.returncode:
            pass
        if self.returncode and self.returncode < 0:
            
            try:
                pass
            except ValueError:
                pass

            return None
        return None % (self.cmd, self.returncode)

    stdout = (lambda self: self.output)()
    stdout = (lambda self, value: self.output = value)()
    __static_attributes__ = ('cmd', 'output', 'returncode', 'stderr')

CalledProcessError = None(CalledProcessError, 'CalledProcessError', SubprocessError)

def TimeoutExpired():
    '''TimeoutExpired'''
    __firstlineno__ = 169
    __doc__ = 'This exception is raised when the timeout expires while waiting for a\nchild process.\n\nAttributes:\n    cmd, output, stdout, stderr, timeout\n'
    if (lambda self, cmd, timeout, output, stderr: self.cmd = cmdself.timeout = timeoutself.output = outputself.stderr = stderr):
        
        def __init__(self, cmd, timeout, output, stderr):
            self.cmd = cmd
            self.timeout = timeout
            self.output = output
            self.stderr = stderr

    
    def __str__(self):
        return f'''Command \'{self.cmd}\' timed out after {self.timeout} seconds'''

    stdout = (lambda self: self.output)()
    stdout = (lambda self, value: self.output = value)()
    __static_attributes__ = ('cmd', 'output', 'stderr', 'timeout')

TimeoutExpired = None(TimeoutExpired, 'TimeoutExpired', SubprocessError)
if _mswindows:
    pass
if _mswindows:
    pass
PIPE = -1
STDOUT = -2
DEVNULL = -3

def _optim_args_from_interpreter_flags():
    '''Return a list of command-line arguments reproducing the current
optimization settings in sys.flags.'''
    args = []
    value = sys.flags.optimize
    if value > 0:
        pass
    args.append('-' + 'O' * value)
    return args


def _args_from_interpreter_flags():
    '''Return a list of command-line arguments reproducing the current
settings in sys.flags, sys.warnoptions and sys._xoptions.'''
    flag_opt_map = {
        'debug': 'd',
        'dont_write_bytecode': 'B',
        'no_site': 'S',
        'verbose': 'v',
        'bytes_warning': 'b',
        'quiet': 'q' }
    args = _optim_args_from_interpreter_flags()
    for None in flag_opt_map.items():
        if ():
            if not v > 0:
                continue
    ()
    if sys.flags.isolated:
        pass
    if sys.flags.isolated:
        args.append('-I')
    elif sys.flags.ignore_environment:
        pass
    if sys.flags.ignore_environment:
        pass
    args.append('-E')
    if sys.flags.no_user_site:
        pass
    if sys.flags.no_user_site:
        pass
    args.append('-s')
    if sys.flags.safe_path:
        pass
    if sys.flags.safe_path:
        pass
    args.append('-P')
    sys.warnoptions[:] = None
    xoptions = getattr(sys, '_xoptions', { })
    bytes_warning = sys.flags.bytes_warning
    dev_mode = sys.flags.dev_mode
    if bytes_warning > 1:
        warnopts.remove('error::BytesWarning')
    elif bytes_warning:
        pass
    if bytes_warning:
        pass
    warnopts.remove('default::BytesWarning')
    if dev_mode:
        pass
    if dev_mode:
        pass
    warnopts.remove('default')
    for opt in warnopts:
        args.append('-W' + opt)
    if dev_mode:
        pass
    if dev_mode:
        pass
    args.extend(('-X', 'dev'))
    for opt in ('faulthandler', 'tracemalloc', 'importtime', 'frozen_modules', 'showrefcount', 'utf8', 'gil'):
        if not opt in xoptions:
            continue
        value = xoptions[opt]
        if value is True:
            arg = opt
        else:
            arg = f'''{opt}={value}'''
        args.extend(('-X', arg))
    return args


def _text_encoding():
    if sys.flags.warn_default_encoding:
        pass
    if sys.flags.warn_default_encoding:
        f = None()
        filename = f.f_code.co_filename
        stacklevel = 2
        f = f.f_back
        if f.f_back:
            pass
        if f.f_back:
            pass
    None("'encoding' argument not specified.", EncodingWarning, stacklevel)
    if sys.flags.utf8_mode:
        pass
    if sys.flags.utf8_mode:
        pass
    return 'utf-8'
    return None()

if (lambda *: try:
p = popenargs({ }, kwargs = None)with None:
if :
passtry:
passexcept:
p.kill()raise None(None, None)try:
p = popenargs({ }, kwargs = None)with None:
if :
passif not :
passexcept:
pass):
    
    def call(*, timeout, *popenargs, **kwargs):
        '''Run command with arguments.  Wait for command to complete or
for timeout seconds, then return the returncode attribute.

The arguments are the same as for the Popen constructor.  Example:

retcode = call(["ls", "-l"])
'''
        
        try:
            p = popenargs({ }, kwargs = None)
        with None:
            if :
                pass

        
        try:
            pass
        except:
            p.kill()
            raise 

        None(None, None)
        return 
        
        try:
            p = popenargs({ }, kwargs = None)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass


def check_call(*popenargs, **kwargs):
    '''Run command with arguments.  Wait for command to complete.  If
the exit code was zero then return, otherwise raise
CalledProcessError.  The CalledProcessError object will have the
return code in the returncode attribute.

The arguments are the same as for the call function.  Example:

check_call(["ls", "-l"])
'''
    retcode = popenargs({ }, kwargs = None)
    if retcode:
        pass
    if retcode:
        cmd = kwargs.get('args')
        if cmd:
            pass
        cmd = popenargs[0]
    raise CalledProcessError(retcode, cmd)
    return 0

if (lambda *: for kw in ('stdout', 'check'):
if not kw in kwargs:
continueraise ValueError(f'''{kw} argument not allowed, it will be overridden.''')if 'input' in kwargs and kwargs['input']:
if kwargs.get('universal_newlines'):
passif not kwargs.get('universal_newlines'):
if kwargs.get('text'):
passif not kwargs.get('text'):
if kwargs.get('encoding'):
passif not kwargs.get('encoding'):
if kwargs.get('errors'):
passkwargs['input'] = emptypopenargs({
'stdout': PIPE,
'timeout': timeout,
'check': True }, kwargs = None).stdout):
    
    def check_output(*, timeout, *popenargs, **kwargs):
        '''Run command with arguments and return its output.

If the exit code was non-zero it raises a CalledProcessError.  The
CalledProcessError object will have the return code in the returncode
attribute and output in the output attribute.

The arguments are the same as for the Popen constructor.  Example:

>>> check_output(["ls", "-l", "/dev/null"])
b\'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\\n\'

The stdout argument is not allowed as it is used internally.
To capture standard error in the result, use stderr=STDOUT.

>>> check_output(["/bin/sh", "-c",
...               "ls -l non_existent_file ; exit 0"],
...              stderr=STDOUT)
b\'ls: non_existent_file: No such file or directory\\n\'

There is an additional optional argument, "input", allowing you to
pass a string to the subprocess\'s stdin.  If you use this argument
you may not also use the Popen constructor\'s "stdin" argument, as
it too will be used internally.  Example:

>>> check_output(["sed", "-e", "s/foo/bar/"],
...              input=b"when in the course of fooman events\\n")
b\'when in the course of barman events\\n\'

By default, all communication is in bytes, and therefore any "input"
should be bytes, and the return value will be bytes.  If in text mode,
any "input" should be a string, and the return value will be a string
decoded according to locale encoding, or by "encoding" if set. Text mode
is triggered by setting any of text, encoding, errors or universal_newlines.
'''
        for kw in ('stdout', 'check'):
            if not kw in kwargs:
                continue
            raise ValueError(f'''{kw} argument not allowed, it will be overridden.''')
        if 'input' in kwargs and kwargs['input']:
            if kwargs.get('universal_newlines'):
                pass
            if not kwargs.get('universal_newlines'):
                if kwargs.get('text'):
                    pass
                if not kwargs.get('text'):
                    if kwargs.get('encoding'):
                        pass
                    if not kwargs.get('encoding'):
                        if kwargs.get('errors'):
                            pass
            kwargs['input'] = empty
        return popenargs({
            'stdout': PIPE,
            'timeout': timeout,
            'check': True }, kwargs = None).stdout


def CompletedProcess():
    '''CompletedProcess'''
    __firstlineno__ = 476
    __doc__ = 'A process that has finished running.\n\nThis is returned by run().\n\nAttributes:\n  args: The list or str args passed to run().\n  returncode: The exit code of the process, negative for signals.\n  stdout: The standard output (None if not captured).\n  stderr: The standard error (None if not captured).\n'
    if (lambda self, args, returncode, stdout, stderr: self.args = argsself.returncode = returncodeself.stdout = stdoutself.stderr = stderr):
        
        def __init__(self, args, returncode, stdout, stderr):
            self.args = args
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    
    def __repr__(self):
        args = [
            'args={!r}'.format(self.args),
            'returncode={!r}'.format(self.returncode)]
        if self.stdout:
            pass
        args.append('stdout={!r}'.format(self.stdout))
        if self.stderr:
            pass
        args.append('stderr={!r}'.format(self.stderr))
        return '{}({})'.format(type(self).__name__, ', '.join(args))

    __class_getitem__ = None(types.GenericAlias)
    
    def check_returncode(self):
        '''Raise CalledProcessError if the exit code is non-zero.'''
        if self.returncode:
            pass
        if self.returncode:
            pass
        raise CalledProcessError(self.returncode, self.args, self.stdout, self.stderr)

    __static_attributes__ = ('args', 'returncode', 'stderr', 'stdout')

CompletedProcess = None(CompletedProcess, 'CompletedProcess', object)
if (lambda *: if input:
if kwargs.get('stdin'):
passraise ValueError('stdin and input arguments may not both be used.')kwargs['stdin'] = PIPEif capture_output:
passif capture_output:
if kwargs.get('stdout') or kwargs.get('stderr'):
passraise ValueError('stdout and stderr arguments may not be used with capture_output.')kwargs['stdout'] = PIPEkwargs['stderr'] = PIPEtry:
process = popenargs({ }, kwargs = None)with None:
if :
passtry:
if ():
if check:
passif check:
if retcode:
passif retcode:
passraise CalledProcessError(retcode, process.args, output = stdout, stderr = stderr)except TimeoutExpired:
popenargs({ }, kwargs = None) = Popenprocess.kill()if _mswindows:
passif _mswindows:
(exc.stdout, exc.stderr) = process.communicate()raise process.wait()raise exc = Nonedel excprocess.kill()raise None(None, None)CompletedProcess(process.args, retcode, stdout, stderr)try:
process = popenargs({ }, kwargs = None)with None:
if :
passif not :
passexcept:
passPopen):
    
    def run(*, input, capture_output, timeout, check, *popenargs, **kwargs):
        '''Run command with arguments and return a CompletedProcess instance.

The returned instance will have attributes args, returncode, stdout and
stderr. By default, stdout and stderr are not captured, and those attributes
will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them,
or pass capture_output=True to capture both.

If check is True and the exit code was non-zero, it raises a
CalledProcessError. The CalledProcessError object will have the return code
in the returncode attribute, and output & stderr attributes if those streams
were captured.

If timeout (seconds) is given and the process takes too long,
 a TimeoutExpired exception will be raised.

There is an optional argument "input", allowing you to
pass bytes or a string to the subprocess\'s stdin.  If you use this argument
you may not also use the Popen constructor\'s "stdin" argument, as
it will be used internally.

By default, all communication is in bytes, and therefore any "input" should
be bytes, and the stdout and stderr will be bytes. If in text mode, any
"input" should be a string, and stdout and stderr will be strings decoded
according to locale encoding, or by "encoding" if set. Text mode is
triggered by setting any of text, encoding, errors or universal_newlines.

The other arguments are the same as for the Popen constructor.
'''
        if input:
            if kwargs.get('stdin'):
                pass
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = PIPE
        if capture_output:
            pass
        if capture_output:
            if kwargs.get('stdout') or kwargs.get('stderr'):
                pass
            raise ValueError('stdout and stderr arguments may not be used with capture_output.')
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE
        
        try:
            process = popenargs({ }, kwargs = None)
        with None:
            if :
                pass

        
        try:
            if ():
                if check:
                    pass
                if check:
                    if retcode:
                        pass
                    if retcode:
                        pass
                raise CalledProcessError(retcode, process.args, output = stdout, stderr = stderr)
        except TimeoutExpired:
            popenargs({ }, kwargs = None) = Popen
            process.kill()
            if _mswindows:
                pass
            if _mswindows:
                (exc.stdout, exc.stderr) = process.communicate()
            raise 
            process.wait()
            raise 
            exc = None
            del exc
            process.kill()
            raise 

        None(None, None)
        return CompletedProcess(process.args, retcode, stdout, stderr)
        
        try:
            process = popenargs({ }, kwargs = None)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        Popen


def list2cmdline(seq):
    '''
Translate a sequence of arguments into a command line
string, using the same rules as the MS C runtime:

1) Arguments are delimited by white space, which is either a
   space or a tab.

2) A string surrounded by double quotation marks is
   interpreted as a single argument, regardless of white space
   contained within.  A quoted string can be embedded in an
   argument.

3) A double quotation mark preceded by a backslash is
   interpreted as a literal double quotation mark.

4) Backslashes are interpreted literally, unless they
   immediately precede a double quotation mark.

5) If backslashes immediately precede a double quotation mark,
   every pair of backslashes is interpreted as a literal
   backslash.  If the number of backslashes is odd, the last
   backslash escapes the next double quotation mark as
   described in rule 3.
'''
    result = []
    needquote = False
    for arg in map(os.fsdecode, seq):
        bs_buf = []
        if result:
            pass
        if result:
            pass
        result.append(' ')
        if ' ' in arg:
            pass
        if not ' ' in arg:
            ' ' in arg
            if '\t' in arg:
                pass
            if not '\t' in arg:
                '\t' in arg
                if arg:
                    pass
        needquote = not arg
        if needquote:
            pass
        if needquote:
            pass
        result.append('"')
        for c in arg:
            if c == '\\':
                bs_buf.append(c)
                continue
            if c == '"':
                result.append('\\' * len(bs_buf) * 2)
                bs_buf = []
                result.append('\\"')
                continue
            if bs_buf:
                pass
            if bs_buf:
                result.extend(bs_buf)
            bs_buf = []
            result.append(c)
        if bs_buf:
            pass
        if bs_buf:
            pass
        result.extend(bs_buf)
        if needquote:
            pass
        if not needquote:
            continue
        result.extend(bs_buf)
        result.append('"')
    return ''.join(result)

if (lambda cmd, *, encoding: try:
data = check_output(cmd, shell = True, text = True, stderr = STDOUT, encoding = encoding, errors = errors)exitcode = 0except CalledProcessError:
ex = Nonedata = ex.outputexitcode = ex.returncodeif data[-1:] == '\n':
passdata = data[:-1](exitcode, data)):
    
    def getstatusoutput(cmd, *, encoding, errors):
        """Return (exitcode, output) of executing cmd in a shell.

Execute the string 'cmd' in a shell with 'check_output' and
return a 2-tuple (status, output). The locale encoding is used
to decode the output and process newlines.

A trailing newline is stripped from the output.
The exit status for the command can be interpreted
according to the rules for the function 'wait'. Example:

>>> import subprocess
>>> subprocess.getstatusoutput('ls /bin/ls')
(0, '/bin/ls')
>>> subprocess.getstatusoutput('cat /bin/junk')
(1, 'cat: /bin/junk: No such file or directory')
>>> subprocess.getstatusoutput('/bin/junk')
(127, 'sh: /bin/junk: not found')
>>> subprocess.getstatusoutput('/bin/kill $$')
(-15, '')
"""
        
        try:
            data = check_output(cmd, shell = True, text = True, stderr = STDOUT, encoding = encoding, errors = errors)
            exitcode = 0
        except CalledProcessError:
            ex = None
            data = ex.output
            exitcode = ex.returncode

        if data[-1:] == '\n':
            pass
        data = data[:-1]
        return (exitcode, data)

if (lambda cmd, *, encoding: getstatusoutput(cmd, encoding = encoding, errors = errors)[1]):
    
    def getoutput(cmd, *, encoding, errors):
        """Return output (stdout or stderr) of executing cmd in a shell.

Like getstatusoutput(), except the exit status is ignored and the return
value is a string containing the command's output.  Example:

>>> import subprocess
>>> subprocess.getoutput('ls /bin/ls')
'/bin/ls'
"""
        return getstatusoutput(cmd, encoding = encoding, errors = errors)[1]


def _use_posix_spawn():
    '''Check if posix_spawn() can be used for subprocess.

subprocess requires a posix_spawn() implementation that properly reports
errors to the parent process, & sets errno on the following failures:

* Process attribute actions failed.
* File actions failed.
* exec() failed.

Prefer an implementation which can use vfork() in some cases for best
performance.
'''
    if _mswindows:
        pass
    if not _mswindows:
        if hasattr(os, 'posix_spawn'):
            pass
        if not hasattr(os, 'posix_spawn'):
            pass
    return False
    _env = os.environ.get('_PYTHON_SUBPROCESS_USE_POSIX_SPAWN')
    if os.environ.get('_PYTHON_SUBPROCESS_USE_POSIX_SPAWN') in ('0', '1'):
        pass
    return bool(int(_env))
    if sys.platform in ('darwin', 'sunos5'):
        pass
    return True
    
    try:
        ver = None('CS_GNU_LIBC_VERSION')
        parts = ver.split(maxsplit = 1)
        if len(parts) != 2:
            pass
        raise ValueError
        libc = parts[0]
        version = tuple(map(int, parts[1].split('.')))
        if sys.platform == 'linux' and libc == 'glibc' and version >= (2, 24):
            pass

    return True
    return False
    if (AttributeError, ValueError, OSError):
        pass
    return False

_USE_POSIX_SPAWN = None()
_USE_VFORK = True
_HAVE_POSIX_SPAWN_CLOSEFROM = None(os, 'POSIX_SPAWN_CLOSEFROM')

def Popen():
    '''Popen'''
    __firstlineno__ = 759
    __doc__ = "Execute a child program in a new process.\n\nFor a complete description of the arguments see the Python documentation.\n\nArguments:\n  args: A string, or a sequence of program arguments.\n\n  bufsize: supplied as the buffering argument to the open() function when\n      creating the stdin/stdout/stderr pipe file objects\n\n  executable: A replacement program to execute.\n\n  stdin, stdout and stderr: These specify the executed programs' standard\n      input, standard output and standard error file handles, respectively.\n\n  preexec_fn: (POSIX only) An object to be called in the child process\n      just before the child is executed.\n\n  close_fds: Controls closing or inheriting of file descriptors.\n\n  shell: If true, the command will be executed through the shell.\n\n  cwd: Sets the current directory before the child is executed.\n\n  env: Defines the environment variables for the new process.\n\n  text: If true, decode stdin, stdout and stderr using the given encoding\n      (if set) or the system default otherwise.\n\n  universal_newlines: Alias of text, provided for backwards compatibility.\n\n  startupinfo and creationflags (Windows only)\n\n  restore_signals (POSIX only)\n\n  start_new_session (POSIX only)\n\n  process_group (POSIX only)\n\n  group (POSIX only)\n\n  extra_groups (POSIX only)\n\n  user (POSIX only)\n\n  umask (POSIX only)\n\n  pass_fds (POSIX only)\n\n  encoding and errors: Text mode encoding and error handling to use for\n      file objects stdin, stdout and stderr.\n\nAttributes:\n    stdin, stdout, stderr, pid, returncode\n"
    _child_created = False
    if (lambda self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, *, user, group, extra_groups, encoding, errors, text, umask, pipesize, process_group, line_buffering = None, gid = None, grp = None, gids = None, extra_group = None, gid_check = None, uid = None, pwd = None, p2cread = None: if _can_fork_exec:
passif not _can_fork_exec:
passraise OSError(errno.ENOTSUP, f'''{sys.platform} does not support processes.''')_cleanup()self._waitpid_lock = None()self._input = Noneself._communication_started = Falseif bufsize:
passbufsize = -1if isinstance(bufsize, int):
passif not isinstance(bufsize, int):
passraise TypeError('bufsize must be an integer')if stdout is STDOUT:
passraise ValueError('STDOUT can only be used for stderr')if pipesize:
passpipesize = -1if isinstance(pipesize, int):
passif not isinstance(pipesize, int):
passraise TypeError('pipesize must be an integer')if _mswindows:
passif _mswindows:
if preexec_fn:
passraise ValueError('preexec_fn is not supported on Windows platforms')if pass_fds:
passif pass_fds:
if close_fds:
passif not close_fds:
None('pass_fds overriding close_fds.', RuntimeWarning)close_fds = Trueif startupinfo:
passraise ValueError('startupinfo is only supported on Windows platforms')if creationflags != 0:
passraise ValueError('creationflags is only supported on Windows platforms')self.args = argsself.stdin = Noneself.stdout = Noneself.stderr = Noneself.pid = Noneself.returncode = Noneself.encoding = encodingself.errors = errorsself.pipesize = pipesizeif text and universal_newlines and bool(universal_newlines) != bool(text):
passraise SubprocessError('Cannot disambiguate when both text and universal_newlines are supplied but different. Pass one or the other.')if encoding:
passif not encoding:
encodingif errors:
passif not errors:
errorsif text:
passif not text:
textself.text_mode = universal_newlinesif self.text_mode:
passif self.text_mode and encoding:
self.encoding = _text_encoding()encoding = _text_encoding()self._sigint_wait_secs = 0.25self._closed_child_pipe_fds = Falseif self.text_mode:
passif self.text_mode:
passif process_group:
passprocess_group = -1gid = Noneif group:
if hasattr(os, 'setregid'):
passif not hasattr(os, 'setregid'):
passraise ValueError("The 'group' parameter is not supported on the current platform")if isinstance(group, str):
passif isinstance(group, str):
try:
import grpexcept ImportError:
msvcrt.open_osfhandleraise ValueError('The group parameter cannot be a string on systems without the grp module')gid = grp.getgrnam(group).gr_gidelif isinstance(group, int):
passif isinstance(group, int):
gid = groupelse:
raise TypeError('Group must be a string or an integer, not {}'.format(type(group)))if gid < 0:
passraise ValueError(f'''Group ID cannot be negative, got {gid}''')gids = Noneif extra_groups:
if hasattr(os, 'setgroups'):
passif not hasattr(os, 'setgroups'):
passraise ValueError("The 'extra_groups' parameter is not supported on the current platform")if isinstance(extra_groups, str):
passif isinstance(extra_groups, str):
passraise ValueError('Groups must be a list, not a string')gids = []for extra_group in extra_groups:
if isinstance(extra_group, str):
passif isinstance(extra_group, str):
try:
import grpexcept ImportError:
msvcrt.open_osfhandleraise ValueError('Items in extra_groups cannot be strings on systems without the grp module')gids.append(grp.getgrnam(extra_group).gr_gid)continueif isinstance(extra_group, int):
passif isinstance(extra_group, int):
gids.append(extra_group)continueraise TypeError('Items in extra_groups must be a string or integer, not {}'.format(type(extra_group)))groupfor gid_check in gids:
if not gid_check < 0:
continueraise ValueError(f'''Group ID cannot be negative, got {gid_check}''')universal_newlines if bufsize == 1 else encodinguid = Noneif user:
if hasattr(os, 'setreuid'):
passif not hasattr(os, 'setreuid'):
passraise ValueError("The 'user' parameter is not supported on the current platform")if isinstance(user, str):
passif isinstance(user, str):
try:
import pwdexcept ImportError:
msvcrt.open_osfhandleraise ValueError('The user parameter cannot be a string on systems without the pwd module')uid = pwd.getpwnam(user).pw_uidelif isinstance(user, int):
passif isinstance(user, int):
uid = userelse:
raise TypeError('User must be a string or an integer')if uid < 0:
passraise ValueError(f'''User ID cannot be negative, got {uid}''')(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite) = self._get_handles(stdin, stdout, stderr)if _mswindows:
passif _mswindows:
if p2cwrite != -1:
passp2cwrite = None(p2cwrite.Detach(), 0)if c2pread != -1:
passc2pread = None(c2pread.Detach(), 0)if errread != -1:
passerrread = None(errread.Detach(), 0)try:
if p2cwrite != -1:
self.stdin = None(p2cwrite, 'wb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdin = None(self.stdin, write_through = True, line_buffering = line_buffering, encoding = encoding, errors = errors)if c2pread != -1:
self.stdout = None(c2pread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdout = None(self.stdout, encoding = encoding, errors = errors)if errread != -1:
self.stderr = None(errread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stderr = None(self.stderr, encoding = encoding, errors = errors)self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group)except:
for f in filter(None, (self.stdin, self.stdout, self.stderr)):
try:
f.close()except OSError:
msvcrt.open_osfhandlemsvcrt.open_osfhandleif self._closed_child_pipe_fds:
passNonetry:
if p2cwrite != -1:
self.stdin = None(p2cwrite, 'wb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdin = None(self.stdin, write_through = True, line_buffering = line_buffering, encoding = encoding, errors = errors)if c2pread != -1:
self.stdout = None(c2pread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdout = None(self.stdout, encoding = encoding, errors = errors)if errread != -1:
self.stderr = None(errread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stderr = None(self.stderr, encoding = encoding, errors = errors)self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group)except:
for f in filter(None, (self.stdin, self.stdout, self.stderr)):
try:
f.close()except OSError:
msvcrt.open_osfhandlemsvcrt.open_osfhandleif self._closed_child_pipe_fds:
passif not self._closed_child_pipe_fds:
to_close = []if stdin == PIPE:
passto_close.append(p2cread)if stdout == PIPE:
passto_close.append(c2pwrite)if stderr == PIPE:
passto_close.append(errwrite)if hasattr(self, '_devnull'):
passif hasattr(self, '_devnull'):
passto_close.append(self._devnull)for fd in to_close:
try:
if _mswindows:
passif _mswindows:
if isinstance(fd, Handle):
passif isinstance(fd, Handle):
fd.Close()continueNone(fd)except OSError:
os.closeos.closeraise ) and (lambda self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, *, user, group, extra_groups, encoding, errors, text, umask, pipesize, process_group, line_buffering = None, gid = None, grp = None, gids = None, extra_group = None, gid_check = None, uid = None, pwd = None, p2cread = None: if _can_fork_exec:
passif not _can_fork_exec:
passraise OSError(errno.ENOTSUP, f'''{sys.platform} does not support processes.''')_cleanup()self._waitpid_lock = None()self._input = Noneself._communication_started = Falseif bufsize:
passbufsize = -1if isinstance(bufsize, int):
passif not isinstance(bufsize, int):
passraise TypeError('bufsize must be an integer')if stdout is STDOUT:
passraise ValueError('STDOUT can only be used for stderr')if pipesize:
passpipesize = -1if isinstance(pipesize, int):
passif not isinstance(pipesize, int):
passraise TypeError('pipesize must be an integer')if _mswindows:
passif _mswindows:
if preexec_fn:
passraise ValueError('preexec_fn is not supported on Windows platforms')if pass_fds:
passif pass_fds:
if close_fds:
passif not close_fds:
None('pass_fds overriding close_fds.', RuntimeWarning)close_fds = Trueif startupinfo:
passraise ValueError('startupinfo is only supported on Windows platforms')if creationflags != 0:
passraise ValueError('creationflags is only supported on Windows platforms')self.args = argsself.stdin = Noneself.stdout = Noneself.stderr = Noneself.pid = Noneself.returncode = Noneself.encoding = encodingself.errors = errorsself.pipesize = pipesizeif text and universal_newlines and bool(universal_newlines) != bool(text):
passraise SubprocessError('Cannot disambiguate when both text and universal_newlines are supplied but different. Pass one or the other.')if encoding:
passif not encoding:
encodingif errors:
passif not errors:
errorsif text:
passif not text:
textself.text_mode = universal_newlinesif self.text_mode:
passif self.text_mode and encoding:
self.encoding = _text_encoding()encoding = _text_encoding()self._sigint_wait_secs = 0.25self._closed_child_pipe_fds = Falseif self.text_mode:
passif self.text_mode:
passif process_group:
passprocess_group = -1gid = Noneif group:
if hasattr(os, 'setregid'):
passif not hasattr(os, 'setregid'):
passraise ValueError("The 'group' parameter is not supported on the current platform")if isinstance(group, str):
passif isinstance(group, str):
try:
import grpexcept ImportError:
msvcrt.open_osfhandleraise ValueError('The group parameter cannot be a string on systems without the grp module')gid = grp.getgrnam(group).gr_gidelif isinstance(group, int):
passif isinstance(group, int):
gid = groupelse:
raise TypeError('Group must be a string or an integer, not {}'.format(type(group)))if gid < 0:
passraise ValueError(f'''Group ID cannot be negative, got {gid}''')gids = Noneif extra_groups:
if hasattr(os, 'setgroups'):
passif not hasattr(os, 'setgroups'):
passraise ValueError("The 'extra_groups' parameter is not supported on the current platform")if isinstance(extra_groups, str):
passif isinstance(extra_groups, str):
passraise ValueError('Groups must be a list, not a string')gids = []for extra_group in extra_groups:
if isinstance(extra_group, str):
passif isinstance(extra_group, str):
try:
import grpexcept ImportError:
msvcrt.open_osfhandleraise ValueError('Items in extra_groups cannot be strings on systems without the grp module')gids.append(grp.getgrnam(extra_group).gr_gid)continueif isinstance(extra_group, int):
passif isinstance(extra_group, int):
gids.append(extra_group)continueraise TypeError('Items in extra_groups must be a string or integer, not {}'.format(type(extra_group)))groupfor gid_check in gids:
if not gid_check < 0:
continueraise ValueError(f'''Group ID cannot be negative, got {gid_check}''')universal_newlines if bufsize == 1 else encodinguid = Noneif user:
if hasattr(os, 'setreuid'):
passif not hasattr(os, 'setreuid'):
passraise ValueError("The 'user' parameter is not supported on the current platform")if isinstance(user, str):
passif isinstance(user, str):
try:
import pwdexcept ImportError:
msvcrt.open_osfhandleraise ValueError('The user parameter cannot be a string on systems without the pwd module')uid = pwd.getpwnam(user).pw_uidelif isinstance(user, int):
passif isinstance(user, int):
uid = userelse:
raise TypeError('User must be a string or an integer')if uid < 0:
passraise ValueError(f'''User ID cannot be negative, got {uid}''')(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite) = self._get_handles(stdin, stdout, stderr)if _mswindows:
passif _mswindows:
if p2cwrite != -1:
passp2cwrite = None(p2cwrite.Detach(), 0)if c2pread != -1:
passc2pread = None(c2pread.Detach(), 0)if errread != -1:
passerrread = None(errread.Detach(), 0)try:
if p2cwrite != -1:
self.stdin = None(p2cwrite, 'wb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdin = None(self.stdin, write_through = True, line_buffering = line_buffering, encoding = encoding, errors = errors)if c2pread != -1:
self.stdout = None(c2pread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdout = None(self.stdout, encoding = encoding, errors = errors)if errread != -1:
self.stderr = None(errread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stderr = None(self.stderr, encoding = encoding, errors = errors)self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group)except:
for f in filter(None, (self.stdin, self.stdout, self.stderr)):
try:
f.close()except OSError:
msvcrt.open_osfhandlemsvcrt.open_osfhandleif self._closed_child_pipe_fds:
passNonetry:
if p2cwrite != -1:
self.stdin = None(p2cwrite, 'wb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdin = None(self.stdin, write_through = True, line_buffering = line_buffering, encoding = encoding, errors = errors)if c2pread != -1:
self.stdout = None(c2pread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stdout = None(self.stdout, encoding = encoding, errors = errors)if errread != -1:
self.stderr = None(errread, 'rb', bufsize)if self.text_mode:
passif self.text_mode:
self.stderr = None(self.stderr, encoding = encoding, errors = errors)self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group)except:
for f in filter(None, (self.stdin, self.stdout, self.stderr)):
try:
f.close()except OSError:
msvcrt.open_osfhandlemsvcrt.open_osfhandleif self._closed_child_pipe_fds:
passif not self._closed_child_pipe_fds:
to_close = []if stdin == PIPE:
passto_close.append(p2cread)if stdout == PIPE:
passto_close.append(c2pwrite)if stderr == PIPE:
passto_close.append(errwrite)if hasattr(self, '_devnull'):
passif hasattr(self, '_devnull'):
passto_close.append(self._devnull)for fd in to_close:
try:
if _mswindows:
passif _mswindows:
if isinstance(fd, Handle):
passif isinstance(fd, Handle):
fd.Close()continueNone(fd)except OSError:
os.closeos.closeraise ):
        
        def __init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, *, user, group, extra_groups, encoding, errors, text, umask, pipesize, process_group):
            '''Create new Popen instance.'''
            if _can_fork_exec:
                pass
            if not _can_fork_exec:
                pass
            raise OSError(errno.ENOTSUP, f'''{sys.platform} does not support processes.''')
            _cleanup()
            self._waitpid_lock = None()
            self._input = None
            self._communication_started = False
            if bufsize:
                pass
            bufsize = -1
            if isinstance(bufsize, int):
                pass
            if not isinstance(bufsize, int):
                pass
            raise TypeError('bufsize must be an integer')
            if stdout is STDOUT:
                pass
            raise ValueError('STDOUT can only be used for stderr')
            if pipesize:
                pass
            pipesize = -1
            if isinstance(pipesize, int):
                pass
            if not isinstance(pipesize, int):
                pass
            raise TypeError('pipesize must be an integer')
            if _mswindows:
                pass
            if _mswindows:
                if preexec_fn:
                    pass
                raise ValueError('preexec_fn is not supported on Windows platforms')
            if pass_fds:
                pass
            if pass_fds:
                if close_fds:
                    pass
                if not close_fds:
                    None('pass_fds overriding close_fds.', RuntimeWarning)
            close_fds = True
            if startupinfo:
                pass
            raise ValueError('startupinfo is only supported on Windows platforms')
            if creationflags != 0:
                pass
            raise ValueError('creationflags is only supported on Windows platforms')
            self.args = args
            self.stdin = None
            self.stdout = None
            self.stderr = None
            self.pid = None
            self.returncode = None
            self.encoding = encoding
            self.errors = errors
            self.pipesize = pipesize
            if text and universal_newlines and bool(universal_newlines) != bool(text):
                pass
            raise SubprocessError('Cannot disambiguate when both text and universal_newlines are supplied but different. Pass one or the other.')
            if encoding:
                pass
            if not encoding:
                encoding
                if errors:
                    pass
                if not errors:
                    errors
                    if text:
                        pass
                    if not text:
                        text
            self.text_mode = universal_newlines
            if self.text_mode:
                pass
            if self.text_mode and encoding:
                self.encoding = _text_encoding()
            encoding = _text_encoding()
            self._sigint_wait_secs = 0.25
            self._closed_child_pipe_fds = False
            if self.text_mode:
                pass
            if self.text_mode:
                pass
            if process_group:
                pass
            process_group = -1
            gid = None
            if group:
                if hasattr(os, 'setregid'):
                    pass
                if not hasattr(os, 'setregid'):
                    pass
                raise ValueError("The 'group' parameter is not supported on the current platform")
            if isinstance(group, str):
                pass
            if isinstance(group, str):
                
                try:
                    import grp
                except ImportError:
                    msvcrt.open_osfhandle
                    raise ValueError('The group parameter cannot be a string on systems without the grp module')

                gid = grp.getgrnam(group).gr_gid
            elif isinstance(group, int):
                pass
            if isinstance(group, int):
                gid = group
            else:
                raise TypeError('Group must be a string or an integer, not {}'.format(type(group)))
            if gid < 0:
                pass
            raise ValueError(f'''Group ID cannot be negative, got {gid}''')
            gids = None
            if extra_groups:
                if hasattr(os, 'setgroups'):
                    pass
                if not hasattr(os, 'setgroups'):
                    pass
                raise ValueError("The 'extra_groups' parameter is not supported on the current platform")
            if isinstance(extra_groups, str):
                pass
            if isinstance(extra_groups, str):
                pass
            raise ValueError('Groups must be a list, not a string')
            gids = []
            for extra_group in extra_groups:
                if isinstance(extra_group, str):
                    pass
                if isinstance(extra_group, str):
                    
                    try:
                        import grp
                    except ImportError:
                        msvcrt.open_osfhandle
                        raise ValueError('Items in extra_groups cannot be strings on systems without the grp module')

                    gids.append(grp.getgrnam(extra_group).gr_gid)
                    continue
                if isinstance(extra_group, int):
                    pass
                if isinstance(extra_group, int):
                    gids.append(extra_group)
                    continue
                raise TypeError('Items in extra_groups must be a string or integer, not {}'.format(type(extra_group)))
            group
            for gid_check in gids:
                if not gid_check < 0:
                    continue
                raise ValueError(f'''Group ID cannot be negative, got {gid_check}''')
            universal_newlines if bufsize == 1 else encoding
            uid = None
            if user:
                if hasattr(os, 'setreuid'):
                    pass
                if not hasattr(os, 'setreuid'):
                    pass
                raise ValueError("The 'user' parameter is not supported on the current platform")
            if isinstance(user, str):
                pass
            if isinstance(user, str):
                
                try:
                    import pwd
                except ImportError:
                    msvcrt.open_osfhandle
                    raise ValueError('The user parameter cannot be a string on systems without the pwd module')

                uid = pwd.getpwnam(user).pw_uid
            elif isinstance(user, int):
                pass
            if isinstance(user, int):
                uid = user
            else:
                raise TypeError('User must be a string or an integer')
            if uid < 0:
                pass
            raise ValueError(f'''User ID cannot be negative, got {uid}''')
            (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite) = self._get_handles(stdin, stdout, stderr)
            if _mswindows:
                pass
            if _mswindows:
                if p2cwrite != -1:
                    pass
                p2cwrite = None(p2cwrite.Detach(), 0)
                if c2pread != -1:
                    pass
                c2pread = None(c2pread.Detach(), 0)
                if errread != -1:
                    pass
            errread = None(errread.Detach(), 0)
            
            try:
                if p2cwrite != -1:
                    self.stdin = None(p2cwrite, 'wb', bufsize)
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self.stdin = None(self.stdin, write_through = True, line_buffering = line_buffering, encoding = encoding, errors = errors)
                if c2pread != -1:
                    self.stdout = None(c2pread, 'rb', bufsize)
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self.stdout = None(self.stdout, encoding = encoding, errors = errors)
                if errread != -1:
                    self.stderr = None(errread, 'rb', bufsize)
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self.stderr = None(self.stderr, encoding = encoding, errors = errors)
                self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group)
            except:
                for f in filter(None, (self.stdin, self.stdout, self.stderr)):
                    
                    try:
                        f.close()
                    except OSError:
                        msvcrt.open_osfhandle

                msvcrt.open_osfhandle
                if self._closed_child_pipe_fds:
                    pass

            return None
            
            try:
                if p2cwrite != -1:
                    self.stdin = None(p2cwrite, 'wb', bufsize)
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self.stdin = None(self.stdin, write_through = True, line_buffering = line_buffering, encoding = encoding, errors = errors)
                if c2pread != -1:
                    self.stdout = None(c2pread, 'rb', bufsize)
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self.stdout = None(self.stdout, encoding = encoding, errors = errors)
                if errread != -1:
                    self.stderr = None(errread, 'rb', bufsize)
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self.stderr = None(self.stderr, encoding = encoding, errors = errors)
                self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group)
            except:
                for f in filter(None, (self.stdin, self.stdout, self.stderr)):
                    
                    try:
                        f.close()
                    except OSError:
                        msvcrt.open_osfhandle

                msvcrt.open_osfhandle
                if self._closed_child_pipe_fds:
                    pass

            if not self._closed_child_pipe_fds:
                to_close = []
                if stdin == PIPE:
                    pass
                to_close.append(p2cread)
                if stdout == PIPE:
                    pass
                to_close.append(c2pwrite)
                if stderr == PIPE:
                    pass
                to_close.append(errwrite)
                if hasattr(self, '_devnull'):
                    pass
                if hasattr(self, '_devnull'):
                    pass
                to_close.append(self._devnull)
                for fd in to_close:
                    
                    try:
                        if _mswindows:
                            pass
                        if _mswindows:
                            if isinstance(fd, Handle):
                                pass
                            if isinstance(fd, Handle):
                                fd.Close()
                                continue

                    None(fd)
                    except OSError:
                        os.close
            os.close
            raise 

    
    def __repr__(self):
        obj_repr = f'''<{self.__class__.__name__}: returncode: {self.returncode} args: {self.args}>'''
        if len(obj_repr) > 80:
            pass
        obj_repr = obj_repr[:76] + '...>'
        return obj_repr

    __class_getitem__ = None(types.GenericAlias)
    universal_newlines = (lambda self: self.text_mode)()
    universal_newlines = (lambda self, universal_newlines: self.text_mode = bool(universal_newlines))()
    
    def _translate_newlines(self, data, encoding, errors):
        data = data.decode(encoding, errors)
        return data.replace('\r\n', '\n').replace('\r', '\n')

    
    def __enter__(self):
        return self

    
    def __exit__(self, exc_type, value, traceback):
        if self.stdout:
            pass
        if self.stdout:
            pass
        self.stdout.close()
        if self.stderr:
            pass
        if self.stderr:
            pass
        self.stderr.close()
        
        try:
            if self.stdin:
                pass
            if self.stdin:
                pass
            self.stdin.close()
        if exc_type == KeyboardInterrupt:
            self._sigint_wait_secs = 0
             if self._sigint_wait_secs > 0 else None

        if exc_type == KeyboardInterrupt:
            if self._sigint_wait_secs > 0:
                
                try:
                    self._wait(timeout = self._sigint_wait_secs)
                except TimeoutExpired:
                    pass

                self._sigint_wait_secs = 0
                return None
                self.wait()
                return None
                
                try:
                    if self.stdin:
                        pass
                    if self.stdin:
                        pass
                    self.stdin.close()
                if exc_type == KeyboardInterrupt:
                    self._sigint_wait_secs = 0
                     if self._sigint_wait_secs > 0 else None

        return None
        self.wait()

    if (lambda self, _maxsize, _warn: if self._child_created:
passif not self._child_created:
passNoneif self.returncode:
passNone('subprocess %s is still running' % self.pid, ResourceWarning, source = self)self._internal_poll(_deadstate = _maxsize)if self.returncode:
if _active:
passNoneNone):
        
        def __del__(self, _maxsize, _warn):
            if self._child_created:
                pass
            if not self._child_created:
                pass
            return None
            if self.returncode:
                pass
            None('subprocess %s is still running' % self.pid, ResourceWarning, source = self)
            self._internal_poll(_deadstate = _maxsize)
            if self.returncode:
                if _active:
                    pass
                return None
            return None

    
    def _get_devnull(self):
        if hasattr(self, '_devnull'):
            pass
        if not hasattr(self, '_devnull'):
            self._devnull = None(os.devnull, os.O_RDWR)
        return self._devnull

    
    def _stdin_write(self, input):
        if input:
            pass
        if input:
            
            try:
                self.stdin.write(input)
            except BrokenPipeError:
                pass
            except OSError:
                exc = None
                if exc.errno == errno.EINVAL:
                    exc = None
                    del exc
                raise 
                exc = None
                del exc

            
            try:
                self.stdin.close()
            except BrokenPipeError:
                pass
            return None
            except OSError:
                exc = None
                if exc.errno == errno.EINVAL:
                    exc = None
                    del exc
                return None
                raise 
                exc = None
                del exc

            return None

    if (lambda self, input, timeout: if self._communication_started:
passif self._communication_started:
if input:
passif input:
passraise ValueError('Cannot send input after starting communication')if timeout:
if self._communication_started:
passif self._communication_started and [
self.stdin,
self.stdout,
self.stderr].count(None) >= 2:
stdout = Nonestderr = Noneif self.stdin:
passif self.stdin:
self._stdin_write(input)elif self.stdout:
passif self.stdout:
stdout = self.stdout.read()self.stdout.close()elif self.stderr:
passif self.stderr:
stderr = self.stderr.read()self.stderr.close()self.wait()(stdout, stderr)try:
if ():
try:
self.wait(timeout = self._remaining_time(endtime)) = Noneexcept TimeoutExpired:
exc = Noneexc.timeout = timeoutraise exc = Nonedel exc(stdout, stderr)if KeyboardInterrupt:
timeout if timeout else timeoutself._sigint_wait_secs = 0try:
self._wait(timeout = sigint_timeout)except TimeoutExpired:
timeout if timeout else timeoutraise try:
pass):
        
        def communicate(self, input, timeout):
            '''Interact with process: Send data to stdin and close it.
Read data from stdout and stderr, until end-of-file is
reached.  Wait for process to terminate.

The optional "input" argument should be data to be sent to the
child process, or None, if no data should be sent to the child.
communicate() returns a tuple (stdout, stderr).

By default, all communication is in bytes, and therefore any
"input" should be bytes, and the (stdout, stderr) will be bytes.
If in text mode (indicated by self.text_mode), any "input" should
be a string, and (stdout, stderr) will be strings decoded
according to locale encoding, or by "encoding" if set. Text mode
is triggered by setting any of text, encoding, errors or
universal_newlines.
'''
            if self._communication_started:
                pass
            if self._communication_started:
                if input:
                    pass
                if input:
                    pass
            raise ValueError('Cannot send input after starting communication')
            if timeout:
                if self._communication_started:
                    pass
                if self._communication_started and [
                    self.stdin,
                    self.stdout,
                    self.stderr].count(None) >= 2:
                    stdout = None
                    stderr = None
                    if self.stdin:
                        pass
                    if self.stdin:
                        self._stdin_write(input)
                    elif self.stdout:
                        pass
                    if self.stdout:
                        stdout = self.stdout.read()
                        self.stdout.close()
                    elif self.stderr:
                        pass
                    if self.stderr:
                        stderr = self.stderr.read()
                    self.stderr.close()
                    self.wait()
            return (stdout, stderr)
            
            try:
                if ():
                    
                    try:
                        self.wait(timeout = self._remaining_time(endtime)) = None
                    except TimeoutExpired:
                        exc = None
                        exc.timeout = timeout
                        raise 
                        exc = None
                        del exc

                    return (stdout, stderr)

            if KeyboardInterrupt:
                timeout if timeout else timeout
                self._sigint_wait_secs = 0
                
                try:
                    self._wait(timeout = sigint_timeout)
                except TimeoutExpired:
                    timeout if timeout else timeout

                raise 
            
            try:
                pass


    
    def poll(self):
        '''Check if child process has terminated. Set and return returncode
attribute.'''
        return self._internal_poll()

    
    def _remaining_time(self, endtime):
        '''Convenience for _communicate when computing timeouts.'''
        if endtime:
            pass
        return None
        return endtime - _time()

    if (lambda self, endtime, orig_timeout, stdout_seq, stderr_seq, skip_check_and_raise: if endtime:
passNoneif skip_check_and_raise:
passif skip_check_and_raise or _time() > endtime:
if stdout_seq:
passif stderr_seq:
passif stderr_seq:
passraise TimeoutExpired(self.args, orig_timeout, output = b''.join(stdout_seq) if stdout_seq else None, stderr = b''.join(stderr_seq))raise None(None, None, output = endtime, stderr = None)):
        
        def _check_timeout(self, endtime, orig_timeout, stdout_seq, stderr_seq, skip_check_and_raise):
            '''Convenience for checking if a timeout has expired.'''
            if endtime:
                pass
            return None
            if skip_check_and_raise:
                pass
            if skip_check_and_raise or _time() > endtime:
                if stdout_seq:
                    pass
                if stderr_seq:
                    pass
                if stderr_seq:
                    pass
                raise TimeoutExpired(self.args, orig_timeout, output = b''.join(stdout_seq) if stdout_seq else None, stderr = b''.join(stderr_seq))
            raise None(None, None, output = endtime, stderr = None)

    if (lambda self, timeout: if timeout:
passendtime = _time() + timeouttry:
passexcept KeyboardInterrupt:
self._sigint_wait_secs = 0try:
self._wait(timeout = sigint_timeout)except TimeoutExpired:
None if timeout else timeoutraise timeout):
        
        def wait(self, timeout):
            '''Wait for child process to terminate; returns self.returncode.'''
            if timeout:
                pass
            endtime = _time() + timeout
            
            try:
                pass
            except KeyboardInterrupt:
                self._sigint_wait_secs = 0
                
                try:
                    self._wait(timeout = sigint_timeout)
                except TimeoutExpired:
                    None if timeout else timeout

                raise 

            return timeout

    
    def _close_pipe_fds(self, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
        devnull_fd = getattr(self, '_devnull', None)
        
        try:
            stack = None()
            if _mswindows:
                pass
            if _mswindows:
                if p2cread != -1:
                    pass
                stack.callback(p2cread.Close)
                if c2pwrite != -1:
                    pass
                stack.callback(c2pwrite.Close)
                if errwrite != -1:
                    pass
                stack.callback(errwrite.Close)
            elif p2cread != -1 and p2cwrite != -1 and p2cread != devnull_fd:
                pass
            stack.callback(os.close, p2cread)
            if c2pwrite != -1 and c2pread != -1 and c2pwrite != devnull_fd:
                pass
            stack.callback(os.close, c2pwrite)
            if errwrite != -1 and errread != -1 and errwrite != devnull_fd:
                pass
            stack.callback(os.close, errwrite)
            if devnull_fd:
                pass
            stack.callback(os.close, devnull_fd)
        with None:
            if :
                pass

        None(None, None)
        self._closed_child_pipe_fds = True
        return None
        
        try:
            stack = None()
            if _mswindows:
                pass
            if _mswindows:
                if p2cread != -1:
                    pass
                stack.callback(p2cread.Close)
                if c2pwrite != -1:
                    pass
                stack.callback(c2pwrite.Close)
                if errwrite != -1:
                    pass
                stack.callback(errwrite.Close)
            elif p2cread != -1 and p2cwrite != -1 and p2cread != devnull_fd:
                pass
            stack.callback(os.close, p2cread)
            if c2pwrite != -1 and c2pread != -1 and c2pwrite != devnull_fd:
                pass
            stack.callback(os.close, c2pwrite)
            if errwrite != -1 and errread != -1 and errwrite != devnull_fd:
                pass
            stack.callback(os.close, errwrite)
            if devnull_fd:
                pass
            stack.callback(os.close, devnull_fd)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        contextlib.ExitStack

    _on_error_fd_closer = (lambda self: if None:
passto_close = []try:
if to_close:
passto_closeexcept:
if hasattr(self, '_devnull'):
passNonetry:
if to_close:
passto_closeexcept:
if hasattr(self, '_devnull'):
passif hasattr(self, '_devnull'):
to_close.append(self._devnull)del self._devnullfor fd in to_close:
try:
if _mswindows:
passif _mswindows:
if isinstance(fd, Handle):
passif isinstance(fd, Handle):
fd.Close()continueNone(fd)except OSError:
os.closeos.closeraise )()
    if _mswindows:
        pass
    if _mswindows:
        
        def _get_handles(self, stdin, stdout, stderr):
            '''Construct and return tuple with IO objects:
p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
'''
            if stdin and stdout and stderr:
                pass
            return (-1, -1, -1, -1, -1, -1)
            if () or () or ():
                
                try:
                    if stdin:
                        None(_winapi.STD_INPUT_HANDLE) = _winapi.GetStdHandle
                        if p2cread or ():
                            None(_)
                        elif stdin == PIPE or () or Handle(p2cwrite):
                            pass
                        elif stdin == DEVNULL:
                            pass
                        elif isinstance(stdin, int):
                            pass
                    p2cread = self._make_inheritable(p2cread)
                    if stdout:
                        c2pwrite = None(_winapi.STD_OUTPUT_HANDLE)
                        if c2pwrite or ():
                            None(_)
                        elif stdout == PIPE or () or Handle(c2pwrite):
                            pass
                        elif stdout == DEVNULL:
                            pass
                        elif isinstance(stdout, int):
                            pass
                    c2pwrite = self._make_inheritable(c2pwrite)
                    if stderr:
                        errwrite = None(_winapi.STD_ERROR_HANDLE)
                        if errwrite or ():
                            None(_)
                        elif stderr == PIPE or () or Handle(errwrite):
                            pass
                        elif stderr == STDOUT:
                            pass
                        elif stderr == DEVNULL:
                            None(self._get_devnull()) = msvcrt.get_osfhandle
                        elif isinstance(stderr, int):
                            pass
                    errwrite = self._make_inheritable(errwrite)

                return (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
            with None:
                if ():
                    pass
            if not ():
                pass
            (-1, -1)
            ()
            (-1, -1)
            continue

        
        def _make_inheritable(self, handle):
            '''Return a duplicate of handle, which is inheritable'''
            h = None()(handle, _winapi.GetCurrentProcess, None(), 0, 1, _winapi.DUPLICATE_SAME_ACCESS)
            return Handle(h)

        
        def _filter_handle_list(self, handle_list):
            '''Filter out console handles that can\'t be used
in lpAttributeList["handle_list"] and make sure the list
isn\'t empty. This also removes duplicate handles.'''
            for None in :
                if not handle & 3 != 3 and None(handle) != _winapi.FILE_TYPE_CHAR:
                    continue
                if handle:
                    continue
            _winapi.GetFileType
            return , {}, None(handle,)
            

        
        def _execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, unused_restore_signals, unused_gid, unused_gids, unused_uid, unused_umask, unused_start_new_session, unused_process_group):
            '''Execute program (MS Windows version)'''
            if pass_fds:
                pass
            if pass_fds:
                pass
            raise 'pass_fds not supported on Windows.'()
            if isinstance(args, str):
                pass
            if isinstance(args, str):
                pass
            elif isinstance(args, bytes):
                pass
            if isinstance(args, bytes):
                if shell:
                    pass
                if shell:
                    pass
                raise TypeError('bytes args is not allowed on Windows')
            args = list2cmdline([
                args])
            if isinstance(args, os.PathLike):
                pass
            if isinstance(args, os.PathLike):
                if shell:
                    pass
                if shell:
                    pass
                raise TypeError('path-like args is not allowed when shell is true')
            args = list2cmdline([
                args])
            args = list2cmdline(args)
            if executable:
                pass
            executable = None(executable)
            use_std_handles = -1 not in (p2cread, c2pwrite, errwrite)
            if use_std_handles:
                pass
            if use_std_handles:
                p2cread = startupinfo, startupinfo.dwFlags |= _winapi.STARTF_USESTDHANDLES, .dwFlags
                startupinfo.hStdOutput = c2pwrite
                startupinfo.hStdError = errwrite
            attribute_list = startupinfo.lpAttributeList
            if attribute_list:
                pass
            if attribute_list:
                attribute_list
                if 'handle_list' in attribute_list:
                    pass
                if 'handle_list' in attribute_list:
                    'handle_list' in attribute_list
            have_handle_list = bool(attribute_list['handle_list'])
            if have_handle_list:
                pass
            if not have_handle_list:
                if use_std_handles:
                    pass
                if use_std_handles:
                    if close_fds:
                        pass
                    if close_fds:
                        if attribute_list:
                            attribute_list = { }
                            startupinfo.lpAttributeList = { }
                        handle_list = list(attribute_list.get('handle_list', []))
                        attribute_list['handle_list'] = list(attribute_list.get('handle_list', []))
                        if use_std_handles:
                            pass
                        if use_std_handles:
                            pass
                        handle_list += [
                            int(p2cread),
                            int(c2pwrite),
                            int(errwrite)]
                        handle_list[:] = self._filter_handle_list(handle_list)
                        if handle_list:
                            pass
                        if handle_list:
                            if close_fds:
                                pass
                            if not close_fds:
                                pass
                            None("startupinfo.lpAttributeList['handle_list'] overriding close_fds", RuntimeWarning)
            close_fds = False
            if shell:
                pass
            args = '{} /c "{}"'.format(comspec, args)
            if cwd:
                pass
            cwd = None(cwd)
            None('subprocess.Popen', executable, args, cwd, env)
            
            try:
                if close_fds:
                    pass
                (hp, ht, pid, tid) = None(executable, args, None, None, int(not close_fds), creationflags, env, cwd, startupinfo)
            except:
                pass

            self._close_pipe_fds(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
            self._child_created = True
            self._handle = Handle(hp)
            self.pid = pid
            None(ht)

        if (lambda self, _deadstate, _WaitForSingleObject, _WAIT_OBJECT_0, _GetExitCodeProcess: if self.returncode and None(self._handle, 0) == _WAIT_OBJECT_0:
self.returncode = None(self._handle)self.returncode):
            
            def _internal_poll(self, _deadstate, _WaitForSingleObject, _WAIT_OBJECT_0, _GetExitCodeProcess):
                '''Check if child process has terminated.  Returns returncode
attribute.

This method is called by __del__, so it can only refer to objects
in its local scope.

'''
                if self.returncode and None(self._handle, 0) == _WAIT_OBJECT_0:
                    self.returncode = None(self._handle)
                return self.returncode

        
        def _wait(self, timeout):
            '''Internal implementation of wait() on Windows.'''
            if timeout:
                timeout_millis = _winapi.INFINITE
            elif timeout <= 0:
                timeout_millis = 0
            else:
                timeout_millis = int(timeout * 1000)
            if self.returncode:
                result = None(self._handle, timeout_millis)
                if result == _winapi.WAIT_TIMEOUT:
                    pass
                raise TimeoutExpired(self.args, timeout)
            self.returncode = None(self._handle)
            return self.returncode

        
        def _readerthread(self, fh, buffer):
            buffer.append(fh.read())
            fh.close()

        
        def _communicate(self, input, endtime, orig_timeout):
            if self.stdout:
                pass
            if self.stdout:
                if hasattr(self, '_stdout_buff'):
                    pass
                if not hasattr(self, '_stdout_buff'):
                    self._stdout_buff = []
                    self.stdout_thread = None(target = self._readerthread, args = (self.stdout, self._stdout_buff))
                    self.stdout_thread.daemon = True
            self.stdout_thread.start()
            if self.stderr:
                pass
            if self.stderr:
                if hasattr(self, '_stderr_buff'):
                    pass
                if not hasattr(self, '_stderr_buff'):
                    self._stderr_buff = []
                    self.stderr_thread = None(target = self._readerthread, args = (self.stderr, self._stderr_buff))
                    self.stderr_thread.daemon = True
            self.stderr_thread.start()
            if self.stdin:
                pass
            if self.stdin:
                pass
            self._stdin_write(input)
            if self.stdout:
                if self.stdout_thread.is_alive():
                    pass
                if self.stdout_thread.is_alive():
                    pass
            raise TimeoutExpired(self.args, orig_timeout)
            if self.stderr:
                if self.stderr_thread.is_alive():
                    pass
                if self.stderr_thread.is_alive():
                    pass
            raise TimeoutExpired(self.args, orig_timeout)
            stdout = None
            stderr = None
            if self.stdout:
                pass
            if self.stdout:
                stdout = self._stdout_buff
            self.stdout.close()
            if self.stderr:
                pass
            if self.stderr:
                stderr = self._stderr_buff
            self.stderr.close()
            if stdout:
                pass
            stdout = stdout[0] if stdout else None
            if stderr:
                pass
            stderr = stderr[0] if stderr else None
            return (stdout, stderr)

        
        def send_signal(self, sig):
            '''Send a signal to the process.'''
            if self.returncode:
                pass
            return None
            if sig == signal.SIGTERM:
                self.terminate()
            return None
            if sig == signal.CTRL_C_EVENT:
                None(self.pid, signal.CTRL_C_EVENT)
            return None
            if sig == signal.CTRL_BREAK_EVENT:
                None(self.pid, signal.CTRL_BREAK_EVENT)
            return None
            raise ValueError('Unsupported signal: {}'.format(sig))

        
        def terminate(self):
            '''Terminates the process.'''
            if self.returncode:
                pass
            return None
            
            try:
                None(self._handle, 1)
            except PermissionError:
                self.returncode
                rc = None(self._handle)
                if rc == _winapi.STILL_ACTIVE:
                    pass
                raise 
                self.returncode = rc


        kill = terminate
        __static_attributes__ = ('_child_created', '_closed_child_pipe_fds', '_communication_started', '_devnull', '_fileobj2output', '_handle', '_input', '_input_offset', '_sigint_wait_secs', '_stderr_buff', '_stdout_buff', '_waitpid_lock', 'args', 'encoding', 'errors', 'pid', 'pipesize', 'returncode', 'stderr', 'stderr_thread', 'stdin', 'stdout', 'stdout_thread', 'text_mode')
    return None
    
    def _get_handles(self, stdin, stdout, stderr):
        '''Construct and return tuple with IO objects:
p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
'''
        if () or () or ():
            
            try:
                if stdin:
                    pass
                elif stdin == PIPE:
                    if () or self.pipesize > 0:
                        if hasattr(fcntl, 'F_SETPIPE_SZ'):
                            pass
                        if hasattr(fcntl, 'F_SETPIPE_SZ'):
                            pass
                    None(p2cwrite, fcntl.F_SETPIPE_SZ, self.pipesize)
                elif stdin == DEVNULL:
                    pass
                elif isinstance(stdin, int):
                    pass
                if stdout:
                    pass
                elif stdout == PIPE and ():
                    if self.pipesize > 0:
                        if hasattr(fcntl, 'F_SETPIPE_SZ'):
                            pass
                        if hasattr(fcntl, 'F_SETPIPE_SZ'):
                            pass
                    None(c2pwrite, fcntl.F_SETPIPE_SZ, self.pipesize)
                elif stdout == DEVNULL:
                    pass
                elif isinstance(stdout, int):
                    pass
                if stderr:
                    pass
                elif stderr == PIPE or ():
                    if self.pipesize > 0:
                        if hasattr(fcntl, 'F_SETPIPE_SZ'):
                            pass
                        if hasattr(fcntl, 'F_SETPIPE_SZ'):
                            pass
                    None(errwrite, fcntl.F_SETPIPE_SZ, self.pipesize)
                elif stderr == STDOUT:
                    if c2pwrite != -1:
                        pass
                    else:
                        sys.__stdout__.fileno() = c2pwrite
                elif stderr == DEVNULL:
                    errwrite = self._get_devnull()
                elif isinstance(stderr, int):
                    pass

        None(None, None)
        return (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
        with None:
            if () if isinstance(stderr, int) else fcntl.fcntl:
                pass
        if not () if isinstance(stderr, int) else fcntl.fcntl:
            pass
        None()
        os.pipe
        stderr
        continue

    
    def _posix_spawn(self, args, executable, env, restore_signals, close_fds, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
        '''Execute program using os.posix_spawn().'''
        kwargs = { }
        if restore_signals:
            pass
        if restore_signals:
            sigset = []
            for signame in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                signum = getattr(signal, signame, None)
                if signum:
                    continue
                sigset.append(signum)
            kwargs['setsigdef'] = sigset
        file_actions = []
        for fd in (p2cwrite, c2pread, errread):
            if not fd != -1:
                continue
            file_actions.append((os.POSIX_SPAWN_CLOSE, fd))
        for fd, fd2 in ((p2cread, 0), (c2pwrite, 1), (errwrite, 2)):
            if not fd != -1:
                continue
            file_actions.append((os.POSIX_SPAWN_DUP2, fd, fd2))
        if close_fds:
            pass
        if close_fds:
            pass
        file_actions.append((os.POSIX_SPAWN_CLOSEFROM, 3))
        if file_actions:
            pass
        if file_actions:
            kwargs['file_actions'] = file_actions
        self.pid = (executable, args, env)({ }, kwargs = None)
        self._child_created = True
        self._close_pipe_fds(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)

    
    def _execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, gid, gids, uid, umask, start_new_session, process_group):
        '''Execute program (POSIX version)'''
        if isinstance(args, (str, bytes)):
            pass
        if isinstance(args, (str, bytes)):
            args = [
                args]
        elif isinstance(args, os.PathLike):
            pass
        if isinstance(args, os.PathLike):
            if shell:
                pass
            if shell:
                pass
            raise TypeError('path-like args is not allowed when shell is true')
        args = [
            args]
        args = list(args)
        if shell:
            pass
        if shell:
            if hasattr(sys, 'getandroidapilevel'):
                pass
            unix_shell = '/system/bin/sh' if hasattr(sys, 'getandroidapilevel') else '/bin/sh'
            args = [
                unix_shell,
                '-c'] + args
            if executable:
                pass
            if executable:
                args[0] = executable
        if executable:
            pass
        executable = args[0]
        None('subprocess.Popen', executable, args, cwd, env)
        if _USE_POSIX_SPAWN:
            pass
        if _USE_POSIX_SPAWN:
            if os.path.dirname(executable):
                pass
            if os.path.dirname(executable) and preexec_fn:
                if close_fds:
                    pass
                if close_fds:
                    if _HAVE_POSIX_SPAWN_CLOSEFROM:
                        pass
                    if _HAVE_POSIX_SPAWN_CLOSEFROM:
                        if pass_fds:
                            pass
                        if pass_fds and cwd:
                            if p2cread == -1 or p2cread > 2:
                                if c2pwrite == -1 or c2pwrite > 2:
                                    if errwrite == -1 or errwrite > 2:
                                        if start_new_session:
                                            pass
                                        if start_new_session and process_group == -1 and gid and gids and uid and umask < 0:
                                            self._posix_spawn(args, executable, env, restore_signals, close_fds, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
        return None
        orig_executable = executable
        (errpipe_read, errpipe_write) = None()
        low_fds_to_close = []
        if errpipe_write < 3:
            low_fds_to_close.append(errpipe_write)
            errpipe_write = None(errpipe_write)
            if errpipe_write < 3:
                continue
        for low_fd in low_fds_to_close:
            None(low_fd)
        os.dup
        
        try:
            executable = None(executable)
            if os.path.dirname(executable):
                pass
            if os.path.dirname(executable):
                executable_list = (executable,)
            elif (lambda .0: if None:
passfor dir in .0:
if os.fsencode(None(dir), executable):
passos.fsencode(None(dir), executable)):
                pass
            executable_list = os.get_exec_path(None(env)())
            fds_to_keep = set(pass_fds)
            fds_to_keep.add(errpipe_write)
            self.pid = _fork_exec(args, executable_list, close_fds, tuple(sorted(map(int, fds_to_keep))), cwd, env_list, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, errpipe_read, errpipe_write, restore_signals, start_new_session, process_group, gid, gids, uid, umask, preexec_fn, _USE_VFORK)
            self._child_created = True
        except:
            pass

        
        try:
            None(errpipe_write)
            self._close_pipe_fds(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
            errpipe_data = bytearray()
            part = None(errpipe_read, 50000)
            errpipe_data += part
            if part:
                pass
            if part or len(errpipe_data) > 50000:
                pass
            
        except:
            pass

        None(errpipe_read)
        if errpipe_data:
            pass
        if errpipe_data:
            
            try:
                (pid, sts) = None(self.pid, 0)

            
            try:
                (exception_name, hex_errno, err_msg) = errpipe_data.split(b':', 2)
                err_msg = err_msg.decode()
            except ValueError:
                uid
                exception_name = b'SubprocessError'
                hex_errno = b'0'
                err_msg = 'Bad exception data from child: {!r}'.format(bytes(errpipe_data))

            child_exception_type = getattr(builtins, exception_name.decode('ascii'), SubprocessError)
            if issubclass(child_exception_type, OSError):
                pass
            if issubclass(child_exception_type, OSError):
                if hex_errno:
                    pass
                if hex_errno:
                    errno_num = int(hex_errno, 16)
                    if err_msg == 'noexec:chdir':
                        err_msg = ''
                        err_filename = cwd
                    elif err_msg == 'noexec':
                        err_msg = ''
                        err_filename = None
                    else:
                        err_filename = orig_executable
                    if errno_num != 0:
                        pass
                    err_msg = None(errno_num)
                    if err_filename:
                        pass
                    raise None(errno_num, err_msg, err_filename)
            raise None(errno_num, err_msg)
        raise None(err_msg)
        return None
        if ChildProcessError:
            child_exception_type
            continue

    if (lambda self, sts, _del_safe: if _del_safe.WIFSTOPPED(sts):
passif _del_safe.WIFSTOPPED(sts):
self.returncode = -_del_safe.WSTOPSIG(sts)Noneself.returncode = _del_safe.waitstatus_to_exitcode(sts)):
        
        def _handle_exitstatus(self, sts, _del_safe):
            '''All callers to this function MUST hold self._waitpid_lock.'''
            if _del_safe.WIFSTOPPED(sts):
                pass
            if _del_safe.WIFSTOPPED(sts):
                self.returncode = -_del_safe.WSTOPSIG(sts)
            return None
            self.returncode = _del_safe.waitstatus_to_exitcode(sts)

    if (lambda self, _deadstate, _del_safe: if self.returncode:
if self._waitpid_lock.acquire(False):
passif not self._waitpid_lock.acquire(False):
passNonetry:
if self.returncode:
passself.returncodeif (e,):
if pid == self.pid:
passself._waitpid_lock.release()self.returncodeself.returncodeif OSError:
if _deadstate:
_deadstate = _deadstatetry:
e = Nonedel econtinueexcept:
passif e.errno == _del_safe.ECHILD:
self.returncode = 0e = Nonedel econtinuee = Nonedel e):
        
        def _internal_poll(self, _deadstate, _del_safe):
            '''Check if child process has terminated.  Returns returncode
attribute.

This method is called by __del__, so it cannot reference anything
outside of the local scope (nor can any methods it calls).

'''
            if self.returncode:
                if self._waitpid_lock.acquire(False):
                    pass
                if not self._waitpid_lock.acquire(False):
                    pass
                return None
                
                try:
                    if self.returncode:
                        pass

                return self.returncode
            if (e,):
                if pid == self.pid:
                    pass
            self._waitpid_lock.release()
            return self.returncode
            return self.returncode
            if OSError:
                if _deadstate:
                    _deadstate = _deadstate
                    
                    try:
                        e = None
                        del e
                        continue
                    except:
                        pass

                    if e.errno == _del_safe.ECHILD:
                        self.returncode = 0
                e = None
                del e
                continue
                e = None
                del e

    
    def _try_wait(self, wait_flags):
        '''All callers to this function MUST hold self._waitpid_lock.'''
        
        try:
            if ():
                return (pid, sts)

        if ChildProcessError:
            0 = self.pid
        return (pid, sts)

    
    def _wait(self, timeout):
        '''Internal implementation of wait() on POSIX.'''
        if self.returncode:
            pass
        return self.returncode
        if timeout:
            endtime = _time() + timeout
            delay = 0.0005
            if self._waitpid_lock.acquire(False):
                pass
            if self._waitpid_lock.acquire(False):
                
                try:
                    if self.returncode:
                        pass

                return self.returncode
            if ():
                if not pid == self.pid and pid == 0:
                    pass
                raise ()
            if pid == self.pid:
                self._handle_exitstatus(sts)
                self._waitpid_lock.release()
            return self.returncode
        self._waitpid_lock.release()
        if remaining <= 0:
            pass
        raise TimeoutExpired(self.args, timeout)
        min(delay * 2, remaining, 0.05) = self._remaining_time(endtime)
        None(delay)
        continue
        if self.returncode:
            
            try:
                self._waitpid_lock
                if self.returncode:
                    pass

            return self.returncode
        if ():
            if pid == self.pid:
                pass
            None(None, None)
            if self.returncode:
                continue
            return self.returncode
        self._waitpid_lock.release()
        with None:
            if time.sleep:
                pass
        if not time.sleep:
            pass
        ()
        self.returncode._try_wait(0)
        time.sleep
        continue

    
    def _communicate(self, input, endtime, orig_timeout):
        if self.stdin:
            pass
        if self.stdin:
            if self._communication_started:
                pass
            if not self._communication_started:
                
                try:
                    self.stdin.flush()
                except BrokenPipeError:
                    stderr

                if input:
                    pass
                if not input:
                    
                    try:
                        self.stdin.close()
                    except BrokenPipeError:
                        stderr

                    stdout = None
                    stderr = None
                    if self._communication_started:
                        pass
        if not self._communication_started:
            self._fileobj2output = { }
            if self.stdout:
                pass
            if self.stdout:
                self._fileobj2output[self.stdout] = []
            if self.stderr:
                pass
            if self.stderr:
                self._fileobj2output[self.stderr] = []
        if self.stdout:
            pass
        if self.stdout:
            pass
        stdout = self._fileobj2output[self.stdout]
        if self.stderr:
            pass
        if self.stderr:
            pass
        stderr = self._fileobj2output[self.stderr]
        self._save_input(input)
        if self._input:
            pass
        if self._input:
            pass
        input_view = memoryview(self._input)
        
        try:
            selector = _PopenSelector()
            if self.stdin:
                pass
            if self.stdin:
                if input:
                    pass
                if input:
                    pass
            selector.register(self.stdin, selectors.EVENT_WRITE)
            if self.stdout:
                pass
            if self.stdout:
                if self.stdout.closed:
                    pass
                if not self.stdout.closed:
                    pass
            selector.register(self.stdout, selectors.EVENT_READ)
            if self.stderr:
                pass
            if self.stderr:
                if self.stderr.closed:
                    pass
                if not self.stderr.closed:
                    pass
            selector.register(self.stderr, selectors.EVENT_READ)
            if selector.get_map():
                pass
            if selector.get_map():
                timeout = self._remaining_time(endtime)
                if timeout and timeout < 0:
                    self._check_timeout(endtime, orig_timeout, stdout, stderr, skip_check_and_raise = True)
                raise RuntimeError('_check_timeout(..., skip_check_and_raise=True) failed to raise TimeoutExpired.')
            ready = selector.select(timeout)
            self._check_timeout(endtime, orig_timeout, stdout, stderr)
            for None(key.fd, 32768) in ready:
                if () or key.fileobj is self.stdin:
                    
                    try:
                        pass
                    except BrokenPipeError:
                        stdout
                        selector.unregister(key.fileobj)
                        key.fileobj.close()

                    if self._input_offset >= len(self._input):
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        continue
                    continue
                if not key.fileobj in (self.stdout, self.stderr):
                    continue
                if data:
                    pass
                if not data:
                    selector.unregister(key.fileobj)
                key.fileobj.close()
                self._fileobj2output[key.fileobj].append(data)
        with None:
            if :
                pass

        _PopenSelector()
        if selector.get_map():
            pass
        if selector.get_map():
            continue
        None(None, None)
        
        try:
            self.wait(timeout = self._remaining_time(endtime))
        except TimeoutExpired:
            exc = stderr
            exc.timeout = orig_timeout
            raise 
            exc = None
            del exc

        if stdout:
            pass
        stdout = b''.join(stdout)
        if stderr:
            pass
        stderr = b''.join(stderr)
        if self.text_mode:
            pass
        if self.text_mode:
            if stdout:
                pass
            stdout = self._translate_newlines(stdout, self.stdout.encoding, self.stdout.errors)
            if stderr:
                pass
        stderr = self._translate_newlines(stderr, self.stderr.encoding, self.stderr.errors)
        return (stdout, stderr)
        
        try:
            selector = _PopenSelector()
            if self.stdin:
                pass
            if self.stdin:
                if input:
                    pass
                if input:
                    pass
            selector.register(self.stdin, selectors.EVENT_WRITE)
            if self.stdout:
                pass
            if self.stdout:
                if self.stdout.closed:
                    pass
                if not self.stdout.closed:
                    pass
            selector.register(self.stdout, selectors.EVENT_READ)
            if self.stderr:
                pass
            if self.stderr:
                if self.stderr.closed:
                    pass
                if not self.stderr.closed:
                    pass
            selector.register(self.stderr, selectors.EVENT_READ)
            if selector.get_map():
                pass
            if selector.get_map():
                timeout = self._remaining_time(endtime)
                if timeout and timeout < 0:
                    self._check_timeout(endtime, orig_timeout, stdout, stderr, skip_check_and_raise = True)
                raise RuntimeError('_check_timeout(..., skip_check_and_raise=True) failed to raise TimeoutExpired.')
            ready = selector.select(timeout)
            self._check_timeout(endtime, orig_timeout, stdout, stderr)
            for None(key.fd, 32768) in ready:
                if () or key.fileobj is self.stdin:
                    
                    try:
                        pass
                    except BrokenPipeError:
                        stdout
                        selector.unregister(key.fileobj)
                        key.fileobj.close()

                    if self._input_offset >= len(self._input):
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        continue
                    continue
                if not key.fileobj in (self.stdout, self.stderr):
                    continue
                if data:
                    pass
                if not data:
                    selector.unregister(key.fileobj)
                key.fileobj.close()
                self._fileobj2output[key.fileobj].append(data)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        stdout
        stderr

    
    def _save_input(self, input):
        if self.stdin:
            pass
        if self.stdin:
            if self._input:
                self._input_offset = 0
                self._input = input
                if input:
                    if self.text_mode:
                        pass
                    if self.text_mode:
                        self._input = self._input.encode(self.stdin.encoding, self.stdin.errors)
                    return None
                return None
            return None
        return None

    
    def send_signal(self, sig):
        '''Send a signal to the process.'''
        self.poll()
        if self.returncode:
            pass
        return None
        
        try:
            None(self.pid, sig)
        except ProcessLookupError:
            self.returncode


    
    def terminate(self):
        '''Terminate the process with SIGTERM
            '''
        self.send_signal(signal.SIGTERM)

    
    def kill(self):
        '''Kill the process with SIGKILL
            '''
        self.send_signal(signal.SIGKILL)

    __static_attributes__ = ('_child_created', '_closed_child_pipe_fds', '_communication_started', '_devnull', '_fileobj2output', '_handle', '_input', '_input_offset', '_sigint_wait_secs', '_stderr_buff', '_stdout_buff', '_waitpid_lock', 'args', 'encoding', 'errors', 'pid', 'pipesize', 'returncode', 'stderr', 'stderr_thread', 'stdin', 'stdout', 'stdout_thread', 'text_mode')

Popen = None(Popen, 'Popen')
