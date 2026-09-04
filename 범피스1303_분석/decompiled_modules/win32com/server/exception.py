# Source Generated with Decompyle++
# File: exception.marshal (Python 3.13)

'''Exception Handling

Exceptions

    To better support COM exceptions, the framework allows for an instance to be
    raised.  This instance may have a certain number of known attributes, which are
    translated into COM exception details.

    This means, for example, that Python could raise a COM exception that includes details
    on a Help file and location, and a description for the user.

    This module provides a class which provides the necessary attributes.
'''
import sys
import pythoncom

def COMException():
    '''COMException'''
    __firstlineno__ = 22
    __doc__ = 'An Exception object that is understood by the framework.\n\nIf the framework is presented with an exception of type class,\nit looks for certain known attributes on this class to provide rich\nerror information to the caller.\n\nIt should be noted that the framework supports providing this error\ninformation via COM Exceptions, or via the ISupportErrorInfo interface.\n\nBy using this class, you automatically provide rich error information to the\nserver.\n'
    if (lambda self, description, scode, source, helpfile, helpContext, desc, hresult: if scode:
passif not scode:
scodescode = hresultif scode:
passif scode and scode != 1 and scode >= -32768 and scode < 32768:
passscode = -2147024896 | scode & 65535self.scode = scodeif description:
passif not description:
descriptionself.description = descif scode == 1:
if self.description:
passif not self.description:
self.description = 'S_FALSE'elif scode:
passif scode:
if self.description:
passif not self.description:
self.description = None(scode)self.source = sourceself.helpfile = helpfileself.helpcontext = helpContextpythoncom.com_error.__init__(self, scode, self.description, None, -1)):
        
        def __init__(self, description, scode, source, helpfile, helpContext, desc, hresult):
            '''Initialize an exception
**Params**

description -- A string description for the exception.
scode -- An integer scode to be returned to the server, if necessary.
The pythoncom framework defaults this to be DISP_E_EXCEPTION if not specified otherwise.
source -- A string which identifies the source of the error.
helpfile -- A string which points to a help file which contains details on the error.
helpContext -- An integer context in the help file.
desc -- A short-cut for description.
hresult -- A short-cut for scode.
'''
            if scode:
                pass
            if not scode:
                scode
            scode = hresult
            if scode:
                pass
            if scode and scode != 1 and scode >= -32768 and scode < 32768:
                pass
            scode = -2147024896 | scode & 65535
            self.scode = scode
            if description:
                pass
            if not description:
                description
            self.description = desc
            if scode == 1:
                if self.description:
                    pass
                if not self.description:
                    self.description = 'S_FALSE'
                elif scode:
                    pass
            if scode:
                if self.description:
                    pass
                if not self.description:
                    self.description = None(scode)
            self.source = source
            self.helpfile = helpfile
            self.helpcontext = helpContext
            pythoncom.com_error.__init__(self, scode, self.description, None, -1)

    
    def __repr__(self):
        return f'''{self.__class__.__name__}(scode={self.scode}, desc={self.description})'''

    __static_attributes__ = ('description', 'helpcontext', 'helpfile', 'scode', 'source')

COMException = None(COMException, 'COMException', pythoncom.com_error)
if (lambda t: if t:
passt = None()[0]if t is not type:
passFalseissubclass(t, pythoncom.com_error)):
    
    def IsCOMException(t):
        if t:
            pass
        t = None()[0]
        if t is not type:
            pass
        return False
        return issubclass(t, pythoncom.com_error)

if (lambda t: if t:
passt = None()[0]if t is not type:
passFalseissubclass(t, COMException)):
    
    def IsCOMServerException(t):
        if t:
            pass
        t = None()[0]
        if t is not type:
            pass
        return False
        return issubclass(t, COMException)

