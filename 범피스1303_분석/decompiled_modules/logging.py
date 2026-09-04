# Source Generated with Decompyle++
# File: logging.marshal (Python 3.13)

"""
Logging package for Python. Based on PEP 282 and comments thereto in
comp.lang.python.

Copyright (C) 2001-2022 Vinay Sajip. All Rights Reserved.

To use, simply 'import logging' and log away!
"""
import sys
import os
import time
import io
import re
import traceback
import warnings
import weakref
import collections.abc as collections
from types import GenericAlias
from string import Template
from string import Formatter as StrFormatter
__all__ = [
    'BASIC_FORMAT',
    'BufferingFormatter',
    'CRITICAL',
    'DEBUG',
    'ERROR',
    'FATAL',
    'FileHandler',
    'Filter',
    'Formatter',
    'Handler',
    'INFO',
    'LogRecord',
    'Logger',
    'LoggerAdapter',
    'NOTSET',
    'NullHandler',
    'StreamHandler',
    'WARN',
    'WARNING',
    'addLevelName',
    'basicConfig',
    'captureWarnings',
    'critical',
    'debug',
    'disable',
    'error',
    'exception',
    'fatal',
    'getLevelName',
    'getLogger',
    'getLoggerClass',
    'info',
    'log',
    'makeLogRecord',
    'setLoggerClass',
    'shutdown',
    'warn',
    'warning',
    'getLogRecordFactory',
    'setLogRecordFactory',
    'lastResort',
    'raiseExceptions',
    'getLevelNamesMapping',
    'getHandlerByName',
    'getHandlerNames']
import threading
__author__ = 'Vinay Sajip <vinay_sajip@red-dove.com>'
__status__ = 'production'
__version__ = '0.5.1.2'
__date__ = '07 February 2010'
_startTime = None()
raiseExceptions = True
logThreads = True
logMultiprocessing = True
logProcesses = True
logAsyncioTasks = True
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
_levelToName = {
    NOTSET: 'NOTSET',
    DEBUG: 'DEBUG',
    INFO: 'INFO',
    WARNING: 'WARNING',
    ERROR: 'ERROR',
    CRITICAL: 'CRITICAL' }
_nameToLevel = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET }

def getLevelNamesMapping():
    return _nameToLevel.copy()


def getLevelName(level):
    """
Return the textual or numeric representation of logging level 'level'.

If the level is one of the predefined levels (CRITICAL, ERROR, WARNING,
INFO, DEBUG) then you get the corresponding string. If you have
associated levels with names using addLevelName then the name you have
associated with 'level' is returned.

If a numeric value corresponding to one of the defined levels is passed
in, the corresponding string representation is returned.

If a string representation of the level is passed in, the corresponding
numeric value is returned.

If no matching numeric or string value is passed in, the string
'Level %s' % level is returned.
"""
    result = _levelToName.get(level)
    if result:
        pass
    return result
    result = _nameToLevel.get(level)
    if result:
        pass
    return result
    return 'Level %s' % level


def addLevelName(level, levelName):
    """
Associate 'levelName' with 'level'.

This is used when converting levels to text during message formatting.
"""
    
    try:
        _lock
        _levelToName[level] = levelName
        _nameToLevel[levelName] = level
    with None:
        if :
            pass

    None(None, None)
    return None
    
    try:
        _lock
        _levelToName[level] = levelName
        _nameToLevel[levelName] = level
    with None:
        if :
            pass

    if not :
        pass
    except:
        pass

if None(sys, '_getframe'):
    pass
_srcfile = os.path.normcase(addLevelName.__code__.co_filename)

def _is_internal_frame(frame):
    '''Signal whether the frame is a CPython or logging module internal.'''
    filename = os.path.normcase(frame.f_code.co_filename)
    if filename == _srcfile:
        pass
    if not filename == _srcfile:
        filename == _srcfile
        if 'importlib' in filename:
            pass
        if 'importlib' in filename:
            'importlib' in filename
    return '_bootstrap' in filename


def _checkLevel(level):
    if isinstance(level, int):
        pass
    if isinstance(level, int):
        rv = level
    return rv
    if str(level) == level:
        if level not in _nameToLevel:
            pass
        raise ValueError('Unknown level: %r' % level)
    rv = _nameToLevel[level]
    return rv
    raise TypeError(f'''Level not an integer or a valid string: {level}''')

_lock = None()

def _prepareFork():
    '''
Prepare to fork a new child process by acquiring the module-level lock.

This should be used in conjunction with _afterFork().
'''
    
    try:
        _lock.acquire()
    except BaseException:
        _lock.release()
        raise 



def _afterFork():
    '''
After a new child process has been forked, release the module-level lock.

This should be used in conjunction with _prepareFork().
'''
    _lock.release()

if None(os, 'register_at_fork'):
    pass

def LogRecord():
    '''LogRecord'''
    __firstlineno__ = 286
    __doc__ = '\nA LogRecord instance represents an event being logged.\n\nLogRecord instances are created every time something is logged. They\ncontain all the information pertinent to the event being logged. The\nmain information passed in is in msg and args, which are combined\nusing str(msg) % args to create the message field of the record. The\nrecord also includes information such as when the record was created,\nthe source line where the logging call was made, and any exception\ninformation to be logged.\n'
    if (lambda self, name, level, pathname, lineno, msg, args, exc_info, func, sinfo: ct = None()self.name = nameself.msg = msgif args:
passif args and len(args) == 1:
if isinstance(args[0], collections.abc.Mapping):
passif isinstance(args[0], collections.abc.Mapping):
if args[0]:
passif args[0]:
passargs = args[0]self.args = argsself.levelname = getLevelName(level)self.levelno = levelself.pathname = pathnametry:
self.filename = os.path.basename(pathname)self.module = os.path.splitext(self.filename)[0]except (TypeError, ValueError, AttributeError):
threading.get_ident if logThreads else threading.current_thread if hasattr(os, 'getpid') else os.getpidself.filename = pathnameself.module = 'Unknown module'self.exc_info = exc_infoself.exc_text = Noneself.stack_info = sinfoself.lineno = linenoself.funcName = funcself.created = ct / 1e+09self.msecs = (ct % 1000000000) // 1000000 + 0if self.msecs == 999 and int(self.created) != ct // 1000000000:
self.msecs = 0self.relativeCreated = (ct - _startTime) / 1e+06if logThreads:
passif logMultiprocessing:
passif mp if not logMultiprocessing else logProcesses:
if hasattr(os, 'getpid'):
passself.taskName = Noneif logAsyncioTasks:
passif logAsyncioTasks:
asyncio = sys.modules.get('asyncio')if asyncio:
passif asyncio:
try:
self.taskName = asyncio.current_task().get_name()except Exception:
time.time_nsNoneNoneNone):
        
        def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func, sinfo, **kwargs):
            '''
Initialize a logging record with interesting information.
'''
            ct = None()
            self.name = name
            self.msg = msg
            if args:
                pass
            if args and len(args) == 1:
                if isinstance(args[0], collections.abc.Mapping):
                    pass
                if isinstance(args[0], collections.abc.Mapping):
                    if args[0]:
                        pass
                    if args[0]:
                        pass
            args = args[0]
            self.args = args
            self.levelname = getLevelName(level)
            self.levelno = level
            self.pathname = pathname
            
            try:
                self.filename = os.path.basename(pathname)
                self.module = os.path.splitext(self.filename)[0]
            except (TypeError, ValueError, AttributeError):
                threading.get_ident if logThreads else threading.current_thread if hasattr(os, 'getpid') else os.getpid
                self.filename = pathname
                self.module = 'Unknown module'

            self.exc_info = exc_info
            self.exc_text = None
            self.stack_info = sinfo
            self.lineno = lineno
            self.funcName = func
            self.created = ct / 1e+09
            self.msecs = (ct % 1000000000) // 1000000 + 0
            if self.msecs == 999 and int(self.created) != ct // 1000000000:
                self.msecs = 0
            self.relativeCreated = (ct - _startTime) / 1e+06
            if logThreads:
                pass
            if logMultiprocessing:
                pass
            if mp if not logMultiprocessing else logProcesses:
                if hasattr(os, 'getpid'):
                    pass
            self.taskName = None
            if logAsyncioTasks:
                pass
            if logAsyncioTasks:
                asyncio = sys.modules.get('asyncio')
                if asyncio:
                    pass
                if asyncio:
                    
                    try:
                        self.taskName = asyncio.current_task().get_name()
                    except Exception:
                        time.time_ns

                    return None
                    return None
                    return None

    
    def __repr__(self):
        return f'''<LogRecord: {self.name}, {self.levelno}, {self.pathname}, {self.lineno}, "{self.msg}">'''

    
    def getMessage(self):
        '''
Return the message for this LogRecord.

Return the message for this LogRecord after merging any user-supplied
arguments with the message.
'''
        msg = str(self.msg)
        if self.args:
            pass
        if self.args:
            pass
        msg = msg % self.args
        return msg

    __static_attributes__ = ('args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs', 'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated', 'stack_info', 'taskName', 'thread', 'threadName')

LogRecord = None(LogRecord, 'LogRecord', object)
_logRecordFactory = LogRecord

def setLogRecordFactory(factory):
    '''
Set the factory to be used when instantiating a log record.

:param factory: A callable which will be called to instantiate
a log record.
'''
    global _logRecordFactory
    _logRecordFactory = factory


def getLogRecordFactory():
    '''
Return the factory to be used when instantiating a log record.
'''
    return _logRecordFactory


def makeLogRecord(dict):
    '''
Make a LogRecord whose attributes are defined by the specified dictionary,
This function is useful for converting a logging event received over
a socket connection (which is sent as a dictionary) into a LogRecord
instance.
'''
    rv = _logRecordFactory(None, None, '', 0, '', (), None, None)
    rv.__dict__.update(dict)
    return rv


class _str_formatter:
