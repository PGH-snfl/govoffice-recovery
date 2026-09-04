# Source Generated with Decompyle++
# File: _compat_pickle.marshal (Python 3.13)

IMPORT_MAPPING = {
    'test.test_support': 'test.support',
    'commands': 'subprocess',
    'urlparse': 'urllib.parse',
    'robotparser': 'urllib.robotparser',
    'urllib2': 'urllib.request',
    'anydbm': 'dbm',
    '_abcoll': 'collections.abc' }
NAME_MAPPING = ('urllib.error', 'URLError')
PYTHON2_EXCEPTIONS = ('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError')

try:
    WindowsError
except NameError:
    ('urllib', 'urlretrieve')

PYTHON2_EXCEPTIONS += ('WindowsError',)
for excname in PYTHON2_EXCEPTIONS:
    NAME_MAPPING[('exceptions', excname)] = ('builtins', excname)
('urllib.error', 'HTTPError')
MULTIPROCESSING_EXCEPTIONS = ('AuthenticationError', 'BufferTooShort', 'ProcessError', 'TimeoutError')
for excname in MULTIPROCESSING_EXCEPTIONS:
    NAME_MAPPING[('multiprocessing', excname)] = ('multiprocessing.context', excname)
('urllib.request', 'urlretrieve')
REVERSE_IMPORT_MAPPING = (lambda .0: if None:
passfor None in .0:
if ():
if (v, k):
passcontinueNone)(IMPORT_MAPPING.items()())
if not len == None(IMPORT_MAPPING):
    pass
raise None(REVERSE_IMPORT_MAPPING)
REVERSE_NAME_MAPPING = (lambda .0: if None:
passfor None in .0:
if ():
if (v, k):
passcontinueNone)(NAME_MAPPING.items()())
if not len == None(NAME_MAPPING):
    pass
raise None(REVERSE_NAME_MAPPING)
IMPORT_MAPPING.update({
    'cPickle': 'pickle',
    '_elementtree': 'xml.etree.ElementTree',
    'FileDialog': 'tkinter.filedialog',
    'SimpleDialog': 'tkinter.simpledialog',
    'DocXMLRPCServer': 'xmlrpc.server',
    'SimpleHTTPServer': 'http.server',
    'CGIHTTPServer': 'http.server',
    'UserDict': 'collections',
    'UserList': 'collections',
    'UserString': 'collections',
    'whichdb': 'dbm',
    'StringIO': 'io',
    'cStringIO': 'io' })
REVERSE_IMPORT_MAPPING.update({
    '_bz2': 'bz2',
    '_dbm': 'dbm',
    '_functools': 'functools',
    '_gdbm': 'gdbm',
    '_pickle': 'pickle' })
NAME_MAPPING.update({
    ('__builtin__', 'basestring'): ('builtins', 'str'),
    ('exceptions', 'StandardError'): ('builtins', 'Exception'),
    ('UserDict', 'UserDict'): ('collections', 'UserDict'),
    ('socket', '_socketobject'): ('socket', 'SocketType') })
REVERSE_NAME_MAPPING.update({
    ('_functools', 'reduce'): ('__builtin__', 'reduce'),
    ('tkinter.filedialog', 'FileDialog'): ('FileDialog', 'FileDialog'),
    ('tkinter.filedialog', 'LoadFileDialog'): ('FileDialog', 'LoadFileDialog'),
    ('tkinter.filedialog', 'SaveFileDialog'): ('FileDialog', 'SaveFileDialog'),
    ('tkinter.simpledialog', 'SimpleDialog'): ('SimpleDialog', 'SimpleDialog'),
    ('xmlrpc.server', 'ServerHTMLDoc'): ('DocXMLRPCServer', 'ServerHTMLDoc'),
    ('xmlrpc.server', 'XMLRPCDocGenerator'): ('DocXMLRPCServer', 'XMLRPCDocGenerator'),
    ('xmlrpc.server', 'DocXMLRPCRequestHandler'): ('DocXMLRPCServer', 'DocXMLRPCRequestHandler'),
    ('xmlrpc.server', 'DocXMLRPCServer'): ('DocXMLRPCServer', 'DocXMLRPCServer'),
    ('xmlrpc.server', 'DocCGIXMLRPCRequestHandler'): ('DocXMLRPCServer', 'DocCGIXMLRPCRequestHandler'),
    ('http.server', 'SimpleHTTPRequestHandler'): ('SimpleHTTPServer', 'SimpleHTTPRequestHandler'),
    ('http.server', 'CGIHTTPRequestHandler'): ('CGIHTTPServer', 'CGIHTTPRequestHandler'),
    ('_socket', 'socket'): ('socket', '_socketobject') })
PYTHON3_OSERROR_EXCEPTIONS = ('BrokenPipeError', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'FileExistsError', 'FileNotFoundError', 'InterruptedError', 'IsADirectoryError', 'NotADirectoryError', 'PermissionError', 'ProcessLookupError', 'TimeoutError')
for excname in PYTHON3_OSERROR_EXCEPTIONS:
    REVERSE_NAME_MAPPING[('builtins', excname)] = ('exceptions', 'OSError')
dict
PYTHON3_IMPORTERROR_EXCEPTIONS = ('ModuleNotFoundError',)
for excname in PYTHON3_IMPORTERROR_EXCEPTIONS:
    REVERSE_NAME_MAPPING[('builtins', excname)] = ('exceptions', 'ImportError')
dict
del excname
