# Source Generated with Decompyle++
# File: dispatcher.marshal (Python 3.13)

'''Dispatcher

Please see policy.py for a discussion on dispatchers and policies
'''
from __future__ import annotations
import traceback
from typing import NoReturn
import pythoncom
import win32api
import win32com
from win32com.server.exception import IsCOMServerException
from win32com.util import IIDToInterfaceName

def DispatcherBase():
    '''DispatcherBase'''
    __firstlineno__ = 18
    __doc__ = 'The base class for all Dispatchers.\n\nThis dispatcher supports wrapping all operations in exception handlers,\nand all the necessary delegation to the policy.\n\nThis base class supports the printing of "unexpected" exceptions.  Note, however,\nthat exactly where the output of print goes may not be useful!  A derived class may\nprovide additional semantics for this.\n'
    
    def __init__(self, policyClass, object):
        self.policy = None(object)
        self.logger = getattr(win32com, 'logger', None)

    
    def _CreateInstance_(self, clsid, reqIID):
        
        try:
            self.policy._CreateInstance_(clsid, reqIID)
        except:
            self._HandleException_()


    
    def _QueryInterface_(self, iid):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _Invoke_(self, dispid, lcid, wFlags, args):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetIDsOfNames_(self, names, lcid):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetTypeInfo_(self, index, lcid):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetTypeInfoCount_(self):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetDispID_(self, name, fdex):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _DeleteMemberByName_(self, name, fdex):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _DeleteMemberByDispID_(self, id):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetMemberProperties_(self, id, fdex):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetMemberName_(self, dispid):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetNextDispID_(self, fdex, flags):
        
        try:
            pass
        except:
            self._HandleException_()


    
    def _GetNameSpaceParent_(self):
        
        try:
            pass
        except:
            self._HandleException_()


    if (lambda self: if IsCOMServerException():
passif not IsCOMServerException():
if self.logger:
passraise None()raise ):
        
        def _HandleException_(self):
            '''Called whenever an exception is raised.

Default behaviour is to print the exception.
'''
            if IsCOMServerException():
                pass
            if not IsCOMServerException():
                if self.logger:
                    pass
                raise 
            None()
            raise 

        
        def _trace_(self, *args):
            if self.logger:
                record = ' '.join(map(str, args))
            return None
            for arg in args[:-1]:
                print(arg, end = ' ')
            self.logger
            print(args[-1])

    __static_attributes__ = ('logger', 'policy')

DispatcherBase = None(DispatcherBase, 'DispatcherBase')

def DispatcherTrace():
    '''DispatcherTrace'''
    __firstlineno__ = 146
    __doc__ = "A dispatcher, which causes a 'print' line for each COM function called."
    
    def _QueryInterface_(self, iid):
        rc = DispatcherBase._QueryInterface_(self, iid)
        if rc:
            pass
        if not rc:
            pass
        self._trace_('in {!r}._QueryInterface_ with unsupported IID {} ({})'.format(self.policy._obj_, IIDToInterfaceName(iid), iid))
        return rc

    
    def _GetIDsOfNames_(self, names, lcid):
        self._trace_("in _GetIDsOfNames_ with '%s' and '%d'\n" % (names, lcid))
        return DispatcherBase._GetIDsOfNames_(self, names, lcid)

    
    def _GetTypeInfo_(self, index, lcid):
        self._trace_('in _GetTypeInfo_ with index=%d, lcid=%d\n' % (index, lcid))
        return DispatcherBase._GetTypeInfo_(self, index, lcid)

    
    def _GetTypeInfoCount_(self):
        self._trace_('in _GetTypeInfoCount_\n')
        return DispatcherBase._GetTypeInfoCount_(self)

    
    def _Invoke_(self, dispid, lcid, wFlags, args):
        self._trace_('in _Invoke_ with', dispid, lcid, wFlags, args)
        return DispatcherBase._Invoke_(self, dispid, lcid, wFlags, args)

    
    def _GetDispID_(self, name, fdex):
        self._trace_('in _GetDispID_ with', name, fdex)
        return DispatcherBase._GetDispID_(self, name, fdex)

    
    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        self._trace_('in {!r}._InvokeEx_-{}{!r} [{:x},{},{!r}]'.format(self.policy._obj_, dispid, args, wFlags, lcid, serviceProvider))
        return DispatcherBase._InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider)

    
    def _DeleteMemberByName_(self, name, fdex):
        self._trace_('in _DeleteMemberByName_ with', name, fdex)
        return DispatcherBase._DeleteMemberByName_(self, name, fdex)

    
    def _DeleteMemberByDispID_(self, id):
        self._trace_('in _DeleteMemberByDispID_ with', id)
        return DispatcherBase._DeleteMemberByDispID_(self, id)

    
    def _GetMemberProperties_(self, id, fdex):
        self._trace_('in _GetMemberProperties_ with', id, fdex)
        return DispatcherBase._GetMemberProperties_(self, id, fdex)

    
    def _GetMemberName_(self, dispid):
        self._trace_('in _GetMemberName_ with', dispid)
        return DispatcherBase._GetMemberName_(self, dispid)

    
    def _GetNextDispID_(self, fdex, flags):
        self._trace_('in _GetNextDispID_ with', fdex, flags)
        return DispatcherBase._GetNextDispID_(self, fdex, flags)

    
    def _GetNameSpaceParent_(self):
        self._trace_('in _GetNameSpaceParent_')
        return DispatcherBase._GetNameSpaceParent_(self)

    __static_attributes__ = ()

DispatcherTrace = None(DispatcherTrace, 'DispatcherTrace', DispatcherBase)

def DispatcherWin32trace():
    '''DispatcherWin32trace'''
    __firstlineno__ = 214
    __doc__ = 'A tracing dispatcher that sends its output to the win32trace remote collector.'
    
    def __init__(self, policyClass, object):
        DispatcherTrace.__init__(self, policyClass, object)
        if self.logger:
            pass
        import win32traceutil
        self._trace_(f'''Object with win32trace dispatcher created (object={object})''')

    __static_attributes__ = ()

DispatcherWin32trace = None(DispatcherWin32trace, 'DispatcherWin32trace', DispatcherTrace)

def DispatcherOutputDebugString():
    '''DispatcherOutputDebugString'''
    __firstlineno__ = 225
    __doc__ = 'A tracing dispatcher that sends its output to win32api.OutputDebugString'
    
    def _trace_(self, *args):
        for arg in args[:-1]:
            None(str(arg) + ' ')
        None(str(args[-1]) + '\n')

    __static_attributes__ = ()

DispatcherOutputDebugString = None(DispatcherOutputDebugString, 'DispatcherOutputDebugString', DispatcherTrace)

try:
    import win32trace
    DefaultDebugDispatcher: 'type[DispatcherTrace]' = DispatcherWin32trace
except ImportError:
    <NODE:27>
    DefaultDebugDispatcher = DispatcherTrace

