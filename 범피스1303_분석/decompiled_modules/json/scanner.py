# Source Generated with Decompyle++
# File: scanner.marshal (Python 3.13)

'''JSON token scanner
'''
import re

try:
    from _json import make_scanner as c_make_scanner
except ImportError:
    re.compile
    c_make_scanner = None

__all__ = [
    'make_scanner']
NUMBER_RE = None('(-?(?:0|[1-9][0-9]*))(\\.[0-9]+)?([eE][-+]?[0-9]+)?', re.VERBOSE | re.MULTILINE | re.DOTALL)

def py_make_scanner(context):
