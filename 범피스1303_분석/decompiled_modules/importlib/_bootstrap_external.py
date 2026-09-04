# Source Generated with Decompyle++
# File: _bootstrap_external.marshal (Python 3.13)

'''Core implementation of path-based import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

'''
_bootstrap = None
import _imp
import _io
import sys
import _warnings
import marshal
_MS_WINDOWS = sys.platform == 'win32'
if _MS_WINDOWS:
    pass
if _MS_WINDOWS:
    import nt as _os
    import winreg
else:
    import posix as _os
if _MS_WINDOWS:
    pass
if _MS_WINDOWS:
    path_separators = [
        '\\',
        '/']
else:
    path_separators = [
        '/']
if (lambda .0: if None:
passfor sep in .0:
if len(sep) == 1:
passlen(sep) == 1)(path_separators()):
    pass
if not (lambda .0: if None:
passfor sep in .0:
if len(sep) == 1:
passlen(sep) == 1)(path_separators()):
    pass
raise all
path_sep = path_separators[0]
path_sep_tuple = None(path_separators)
path_separators = ''.join(path_separators)
for None in :
    if f''':{s}''':
        continue
s, _pathseps_with_colon = tuple, path_separators, , {}
_CASE_INSENSITIVE_PLATFORMS_STR_KEY = ('win',)
_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY = ('cygwin', 'darwin', 'ios', 'tvos', 'watchos')
_CASE_INSENSITIVE_PLATFORMS = _CASE_INSENSITIVE_PLATFORMS_BYTES_KEY + _CASE_INSENSITIVE_PLATFORMS_STR_KEY

def _make_relax_case():
