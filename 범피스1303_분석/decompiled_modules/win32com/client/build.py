# Source Generated with Decompyle++
# File: build.marshal (Python 3.13)

'''Contains knowledge to build a COM object definition.

This module is used by both the @dynamic@ and @makepy@ modules to build
all knowledge of a COM object.

This module contains classes which contain the actual knowledge of the object.
This include parameter and return type information, the COM dispid and CLSID, etc.

Other modules may use this information to generate .py files, use the information
dynamically, or possibly even generate .html documentation for objects.
'''
import builtins
import datetime
import string
from itertools import chain
from keyword import iskeyword
import pythoncom
import winerror
from pywintypes import TimeType
_makeDocString = repr

def NotSupportedException():
    '''NotSupportedException'''
    __firstlineno__ = 35
    __static_attributes__ = ()

NotSupportedException = None(NotSupportedException, 'NotSupportedException', Exception)
DropIndirection = 'DropIndirection'
NoTranslateTypes = [
    pythoncom.VT_BOOL,
    pythoncom.VT_CLSID,
    pythoncom.VT_CY,
    pythoncom.VT_DATE,
    pythoncom.VT_DECIMAL,
    pythoncom.VT_EMPTY,
    pythoncom.VT_ERROR,
    pythoncom.VT_FILETIME,
    pythoncom.VT_HRESULT,
    pythoncom.VT_I1,
    pythoncom.VT_I2,
    pythoncom.VT_I4,
    pythoncom.VT_I8,
    pythoncom.VT_INT,
    pythoncom.VT_NULL,
    pythoncom.VT_R4,
    pythoncom.VT_R8,
    pythoncom.VT_NULL,
    pythoncom.VT_STREAM,
    pythoncom.VT_UI1,
    pythoncom.VT_UI2,
    pythoncom.VT_UI4,
    pythoncom.VT_UI8,
    pythoncom.VT_UINT,
    pythoncom.VT_VOID]

class NoTranslateMap(NoTranslateTypes):
