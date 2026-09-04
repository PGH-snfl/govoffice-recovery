# Source Generated with Decompyle++
# File: client.marshal (Python 3.13)

from __future__ import annotations
import sys
from itertools import chain
import pythoncom
import pywintypes
from  import dynamic, gencache
_PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
if (lambda dispatch, userName, resultCLSID, typeinfo, clsctx, WrapperClass: if resultCLSID:
try:
typeinfo = dispatch.GetTypeInfo()if typeinfo:
passresultCLSID = str(typeinfo.GetTypeAttr()[0])except (pythoncom.com_error, AttributeError):
dynamic.Dispatchif resultCLSID:
gencache = gencacheklass = None(resultCLSID)if klass:
passNone(dispatch)if WrapperClass:
passWrapperClass = CDispatchNone(dispatch, userName, WrapperClass, typeinfo, clsctx = clsctx)):
    
    def __WrapDispatch(dispatch, userName, resultCLSID, typeinfo, clsctx, WrapperClass):
        '''
Helper function to return a makepy generated class for a CLSID if it exists,
otherwise cope by using CDispatch.
'''
        if resultCLSID:
            
            try:
                typeinfo = dispatch.GetTypeInfo()
                if typeinfo:
                    pass
                resultCLSID = str(typeinfo.GetTypeAttr()[0])
            except (pythoncom.com_error, AttributeError):
                dynamic.Dispatch

            if resultCLSID:
                gencache = gencache
                klass = None(resultCLSID)
                if klass:
                    pass
        return None(dispatch)
        if WrapperClass:
            pass
        WrapperClass = CDispatch
        return None(dispatch, userName, WrapperClass, typeinfo, clsctx = clsctx)

if (lambda Pathname, Class, clsctx: if clsctx:
passclsctx = pythoncom.CLSCTX_ALLif (Pathname or Class or Pathname) and Class:
passraise ValueError('You must specify a value for Pathname or Class, but not both.')if Class:
passGetActiveObject(Class, clsctx)Moniker(Pathname, clsctx)):
    
    def GetObject(Pathname, Class, clsctx):
        '''
Mimic VB\'s GetObject() function.

ob = GetObject(Class = "ProgID") or GetObject(Class = clsid) will
connect to an already running instance of the COM object.

ob = GetObject(r"c:\\blah\\blah\\foo.xls") (aka the COM moniker syntax)
will return a ready to use Python wrapping of the required COM object.

Note: You must specifiy one or the other of these arguments. I know
this isn\'t pretty, but it is what VB does. Blech. If you don\'t
I\'ll throw ValueError at you. :)

This will most likely throw pythoncom.com_error if anything fails.
'''
        if clsctx:
            pass
        clsctx = pythoncom.CLSCTX_ALL
        if (Pathname or Class or Pathname) and Class:
            pass
        raise ValueError('You must specify a value for Pathname or Class, but not both.')
        if Class:
            pass
        return GetActiveObject(Class, clsctx)
        return Moniker(Pathname, clsctx)

if (lambda Class, clsctx: resultCLSID = None(Class)dispatch = None(resultCLSID)dispatch = dispatch.QueryInterface(pythoncom.IID_IDispatch)__WrapDispatch(dispatch, Class, resultCLSID = resultCLSID, clsctx = clsctx)):
    
    def GetActiveObject(Class, clsctx):
        """
Python friendly version of GetObject's ProgID/CLSID functionality.
"""
        resultCLSID = None(Class)
        dispatch = None(resultCLSID)
        dispatch = dispatch.QueryInterface(pythoncom.IID_IDispatch)
        return __WrapDispatch(dispatch, Class, resultCLSID = resultCLSID, clsctx = clsctx)

if (lambda Pathname, clsctx: if (bindCtx,):
pass__WrapDispatch(dispatch, Pathname, clsctx = clsctx)):
    
    def Moniker(Pathname, clsctx):
        """
Python friendly version of GetObject's moniker functionality.
"""
        if (bindCtx,):
            pass
        return __WrapDispatch(dispatch, Pathname, clsctx = clsctx)

if (lambda dispatch, userName, resultCLSID, typeinfo, clsctx: if ():
pass__WrapDispatch(dispatch, userName, resultCLSID, typeinfo, clsctx = clsctx)):
    
    def Dispatch(dispatch, userName, resultCLSID, typeinfo, clsctx):
        '''Creates a Dispatch based COM object.'''
        if ():
            pass
        return __WrapDispatch(dispatch, userName, resultCLSID, typeinfo, clsctx = clsctx)

if (lambda clsid, machine, userName, resultCLSID, typeinfo, clsctx: if clsctx:
clsctx = pythoncom.CLSCTX_SERVERif machine:
passclsctx &= ~(pythoncom.CLSCTX_INPROC)if userName:
passuserName = clsiddispatch = None(clsid, None, clsctx, serverInfo, (pythoncom.IID_IDispatch,))[0]Dispatch(dispatch, userName, resultCLSID, typeinfo, clsctx = clsctx)):
    
    def DispatchEx(clsid, machine, userName, resultCLSID, typeinfo, clsctx):
        '''Creates a Dispatch based COM object on a specific machine.'''
        if clsctx:
            clsctx = pythoncom.CLSCTX_SERVER
            if machine:
                pass
        clsctx &= ~(pythoncom.CLSCTX_INPROC)
        if userName:
            pass
        userName = clsid
        dispatch = None(clsid, None, clsctx, serverInfo, (pythoncom.IID_IDispatch,))[0]
        return Dispatch(dispatch, userName, resultCLSID, typeinfo, clsctx = clsctx)


def CDispatch():
    '''CDispatch'''
    __firstlineno__ = 148
    __doc__ = '\nThe dynamic class used as a last resort.\nThe purpose of this overriding of dynamic.CDispatch is to perpetuate the policy\nof using the makepy generated wrapper Python class instead of dynamic.CDispatch\nif/when possible.\n'
    if (lambda self, ob, userName, returnCLSID: Dispatch(ob, userName, returnCLSID)):
        
        def _wrap_dispatch_(self, ob, userName, returnCLSID):
            return Dispatch(ob, userName, returnCLSID)

    
    def __dir__(self):
        return dynamic.CDispatch.__dir__(self)

    __static_attributes__ = ()

CDispatch = None(CDispatch, 'CDispatch', dynamic.CDispatch)
if (lambda ob, target, typelib: mod = Noneif typelib:
mod = None(typelib.clsid, typelib.lcid, int(typelib.major, 16), int(typelib.minor, 16))if hasattr(mod, target):
passif not hasattr(mod, target):
passraise ValueError(f'''The interface name \'{target}\' does not appear in the specified library {typelib.ver_desc}''')if hasattr(target, 'index'):
passif hasattr(target, 'index'):
if 'CLSID' not in ob.__class__.__dict__:
passob = None(ob)if 'CLSID' not in ob.__class__.__dict__:
passraise ValueError('Must be a makepy-able object for this to work')clsid = ob.CLSIDmod = None(clsid)mod = None(mod.CLSID, mod.LCID, mod.MajorVersion, mod.MinorVersion)target_clsid = mod.NamesToIIDMap.get(target)if target_clsid:
passraise ValueError(f'''The interface name \'{target}\' does not appear in the same library as object \'{ob}\'''')mod = None(target_clsid)if mod:
target_class = getattr(mod, target)target_class = getattr(target_class, 'default_interface', target_class)None(ob)raise ValueError):
    
    def CastTo(ob, target, typelib):
        """'Cast' a COM object to another interface"""
        mod = None
        if typelib:
            mod = None(typelib.clsid, typelib.lcid, int(typelib.major, 16), int(typelib.minor, 16))
            if hasattr(mod, target):
                pass
            if not hasattr(mod, target):
                pass
            raise ValueError(f'''The interface name \'{target}\' does not appear in the specified library {typelib.ver_desc}''')
        if hasattr(target, 'index'):
            pass
        if hasattr(target, 'index'):
            if 'CLSID' not in ob.__class__.__dict__:
                pass
            ob = None(ob)
            if 'CLSID' not in ob.__class__.__dict__:
                pass
            raise ValueError('Must be a makepy-able object for this to work')
        clsid = ob.CLSID
        mod = None(clsid)
        mod = None(mod.CLSID, mod.LCID, mod.MajorVersion, mod.MinorVersion)
        target_clsid = mod.NamesToIIDMap.get(target)
        if target_clsid:
            pass
        raise ValueError(f'''The interface name \'{target}\' does not appear in the same library as object \'{ob}\'''')
        mod = None(target_clsid)
        if mod:
            target_class = getattr(mod, target)
            target_class = getattr(target_class, 'default_interface', target_class)
        return None(ob)
        raise ValueError


def Constants():
    '''Constants'''
    __firstlineno__ = 215
    __doc__ = 'A container for generated COM constants.'
    
    def __init__(self):
        self.__dicts__ = []

    
    def __getattr__(self, a):
        for d in self.__dicts__:
            if not a in d:
                continue
            
            return None, d[a]
        raise AttributeError(a)

    __static_attributes__ = ('__dicts__',)

Constants = None(Constants, 'Constants')

class constants:
