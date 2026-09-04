# Source Generated with Decompyle++
# File: policy.marshal (Python 3.13)

'''Policies

Note that Dispatchers are now implemented in "dispatcher.py", but
are still documented here.

Policies

 A policy is an object which manages the interaction between a public
 Python object, and COM .  In simple terms, the policy object is the
 object which is actually called by COM, and it invokes the requested
 method, fetches/sets the requested property, etc.  See the
 @win32com.server.policy.CreateInstance@ method for a description of
 how a policy is specified or created.

 Exactly how a policy determines which underlying object method/property
 is obtained is up to the policy.  A few policies are provided, but you
 can build your own.  See each policy class for a description of how it
 implements its policy.

 There is a policy that allows the object to specify exactly which
 methods and properties will be exposed.  There is also a policy that
 will dynamically expose all Python methods and properties - even those
 added after the object has been instantiated.

Dispatchers

 A Dispatcher is a level in front of a Policy.  A dispatcher is the
 thing which actually receives the COM calls, and passes them to the
 policy object (which in turn somehow does something with the wrapped
 object).

 It is important to note that a policy does not need to have a dispatcher.
 A dispatcher has the same interface as a policy, and simply steps in its
 place, delegating to the real policy.  The primary use for a Dispatcher
 is to support debugging when necessary, but without imposing overheads
 when not (ie, by not using a dispatcher at all).

 There are a few dispatchers provided - "tracing" dispatchers which simply
 prints calls and args (including a variation which uses
 win32api.OutputDebugString), and a "debugger" dispatcher, which can
 invoke the debugger when necessary.

Error Handling

 It is important to realise that the caller of these interfaces may
 not be Python.  Therefore, general Python exceptions and tracebacks aren\'t
 much use.

 In general, there is an COMException class that should be raised, to allow
 the framework to extract rich COM type error information.

 The general rule is that the **only** exception returned from Python COM
 Server code should be an COMException instance.  Any other Python exception
 should be considered an implementation bug in the server (if not, it
 should be handled, and an appropriate COMException instance raised).  Any
 other exception is considered "unexpected", and a dispatcher may take
 special action (see Dispatchers above)

 Occasionally, the implementation will raise the policy.error error.
 This usually means there is a problem in the implementation that the
 Python programmer should fix.

 For example, if policy is asked to wrap an object which it can not
 support (because, eg, it does not provide _public_methods_ or _dynamic_)
 then policy.error will be raised, indicating it is a Python programmers
 problem, rather than a COM error.
'''
import sys
import types
import pythoncom
import pywintypes
import win32api
import win32con
import winerror
from pythoncom import DISPATCH_METHOD, DISPATCH_PROPERTYGET, DISPATCH_PROPERTYPUT, DISPATCH_PROPERTYPUTREF, DISPID_EVALUATE, DISPID_NEWENUM, DISPID_PROPERTYPUT, DISPID_STARTENUM, DISPID_VALUE
from exception import COMException
__author__ = 'Greg Stein and Mark Hammond'
S_OK = 0
IDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
IUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
regSpec = 'CLSID\\%s\\PythonCOM'
regPolicy = 'CLSID\\%s\\PythonCOMPolicy'
regDispatcher = 'CLSID\\%s\\PythonCOMDispatcher'
regAddnPath = 'CLSID\\%s\\PythonCOMPath'

def CreateInstance(clsid, reqIID):
    '''Create a new instance of the specified IID

The COM framework **always** calls this function to create a new
instance for the specified CLSID.  This function looks up the
registry for the name of a policy, creates the policy, and asks the
policy to create the specified object by calling the _CreateInstance_ method.

Exactly how the policy creates the instance is up to the policy.  See the
specific policy documentation for more details.
'''
    
    try:
        addnPaths = None(win32con.HKEY_CLASSES_ROOT, regAddnPath % clsid).split(';')
        for newPath in addnPaths:
            if not newPath not in sys.path:
                continue
            sys.path.insert(0, newPath)
    except win32api.error:
        dispatcher if dispatcher else policy

    
    try:
        policy = None(win32con.HKEY_CLASSES_ROOT, regPolicy % clsid)
        policy = resolve_func(policy)
    except win32api.error:
        policy = DefaultPolicy

    
    try:
        dispatcher = None(win32con.HKEY_CLASSES_ROOT, regDispatcher % clsid)
        if dispatcher:
            pass
        if dispatcher:
            pass
        dispatcher = resolve_func(dispatcher)
    except win32api.error:
        dispatcher = None

    if dispatcher:
        pass
    return retObj._CreateInstance_(clsid, reqIID)


def BasicWrapPolicy():
    '''BasicWrapPolicy'''
    __firstlineno__ = 151
    __doc__ = "The base class of policies.\n\nNormally not used directly (use a child class, instead)\n\nThis policy assumes we are wrapping another object\nas the COM server.  This supports the delegation of the core COM entry points\nto either the wrapped object, or to a child class.\n\nThis policy supports the following special attributes on the wrapped object\n\n_query_interface_ -- A handler which can respond to the COM 'QueryInterface' call.\n_com_interfaces_ -- An optional list of IIDs which the interface will assume are\n    valid for the object.\n_invoke_ -- A handler which can respond to the COM 'Invoke' call.  If this attribute\n    is not provided, then the default policy implementation is used.  If this attribute\n    does exist, it is responsible for providing all required functionality - ie, the\n    policy _invoke_ method is not invoked at all (and nor are you able to call it!)\n_getidsofnames_ -- A handler which can respond to the COM 'GetIDsOfNames' call.  If this attribute\n    is not provided, then the default policy implementation is used.  If this attribute\n    does exist, it is responsible for providing all required functionality - ie, the\n    policy _getidsofnames_ method is not invoked at all (and nor are you able to call it!)\n\nIDispatchEx functionality:\n\n_invokeex_ -- Very similar to _invoke_, except slightly different arguments are used.\n    And the result is just the _real_ result (rather than the (hresult, argErr, realResult)\n    tuple that _invoke_ uses.\n    This is the new, prefered handler (the default _invoke_ handler simply called _invokeex_)\n_getdispid_ -- Very similar to _getidsofnames_, except slightly different arguments are used,\n    and only 1 property at a time can be fetched (which is all we support in getidsofnames anyway!)\n    This is the new, prefered handler (the default _invoke_ handler simply called _invokeex_)\n_getnextdispid_- uses self._name_to_dispid_ to enumerate the DISPIDs\n"
    
    def __init__(self, object):
        '''Initialise the policy object

Params:

object -- The object to wrap.  May be None *iff* @BasicWrapPolicy._CreateInstance_@ will be
called immediately after this to setup a brand new object
'''
        if object:
            pass
        return None

    
    def _CreateInstance_(self, clsid, reqIID):
        '''Creates a new instance of a **wrapped** object

This method looks up a "@win32com.server.policy.regSpec@" % clsid entry
in the registry (using @DefaultPolicy@)
'''
        
        try:
            classSpec = None(win32con.HKEY_CLASSES_ROOT, regSpec % clsid)
        except win32api.error:
            raise ValueError(f'''The object is not correctly registered - {regSpec % clsid} key can not be read''')

        myob = call_func(classSpec)
        self._wrap_(myob)
        
        try:
            pass
        except pythoncom.com_error:
            xxx_todo_changeme = None
            if () or ():
                raise None(hr, desc, exc, arg)
            del xxx_todo_changeme


    
    def _wrap_(self, object):
        '''Wraps up the specified object.

This function keeps a reference to the passed
object, and may interogate it to determine how to respond to COM requests, etc.
'''
        self._name_to_dispid_ = { }
        if object:
            object._obj_ = object
            if hasattr(ob, '_query_interface_'):
                pass
            if hasattr(ob, '_query_interface_'):
                self._query_interface_ = ob._query_interface_
        if hasattr(ob, '_invoke_'):
            pass
        if hasattr(ob, '_invoke_'):
            self._invoke_ = ob._invoke_
        if hasattr(ob, '_invokeex_'):
            pass
        if hasattr(ob, '_invokeex_'):
            self._invokeex_ = ob._invokeex_
        if hasattr(ob, '_getidsofnames_'):
            pass
        if hasattr(ob, '_getidsofnames_'):
            self._getidsofnames_ = ob._getidsofnames_
        if hasattr(ob, '_getdispid_'):
            pass
        if hasattr(ob, '_getdispid_'):
            self._getdispid_ = ob._getdispid_
        if hasattr(ob, '_com_interfaces_'):
            pass
        if hasattr(ob, '_com_interfaces_'):
            self._com_interfaces_ = []
            for i in ob._com_interfaces_:
                if isinstance(i, pywintypes.IIDType):
                    pass
                if not isinstance(i, pywintypes.IIDType):
                    pass
                self._com_interfaces_.append(i)
        return None
        self._com_interfaces_ = []

    
    def _QueryInterface_(self, iid):
        '''The main COM entry-point for QueryInterface.

This checks the _com_interfaces_ attribute and if the interface is not specified
there, it calls the derived helper _query_interface_
'''
        if iid in self._com_interfaces_:
            pass
        return 1
        return self._query_interface_(iid)

    
    def _query_interface_(self, iid):
        '''Called if the object does not provide the requested interface in _com_interfaces_,
and does not provide a _query_interface_ handler.

Returns a result to the COM framework indicating the interface is not supported.
'''
        return 0

    
    def _Invoke_(self, dispid, lcid, wFlags, args):
        '''The main COM entry-point for Invoke.

This calls the _invoke_ helper.
'''
        if isinstance(dispid, str):
            pass
        if isinstance(dispid, str):
            
            try:
                dispid = self._name_to_dispid_[dispid.lower()]

            return self._invoke_(dispid, lcid, wFlags, args)
        if KeyError:
            pass
        raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND, desc = 'Member not found')

    
    def _invoke_(self, dispid, lcid, wFlags, args):
        return (S_OK, -1, self._invokeex_(dispid, lcid, wFlags, args, None, None))

    
    def _GetIDsOfNames_(self, names, lcid):
        '''The main COM entry-point for GetIDsOfNames.

This checks the validity of the arguments, and calls the _getidsofnames_ helper.
'''
        if len(names) > 1:
            pass
        raise COMException(scode = winerror.DISP_E_INVALID, desc = 'Cannot support member argument names')
        return self._getidsofnames_(names, lcid)

    
    def _getidsofnames_(self, names, lcid):
        return (self._getdispid_(names[0], 0),)

    
    def _GetDispID_(self, name, fdex):
        return self._getdispid_(name, fdex)

    
    def _getdispid_(self, name, fdex):
        
        try:
            pass
        except KeyError:
            raise COMException(scode = winerror.DISP_E_UNKNOWNNAME)


    
    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        '''The main COM entry-point for InvokeEx.

This calls the _invokeex_ helper.
'''
        if isinstance(dispid, str):
            pass
        if isinstance(dispid, str):
            
            try:
                dispid = self._name_to_dispid_[dispid.lower()]

            return self._invokeex_(dispid, lcid, wFlags, args, kwargs, serviceProvider)
        if KeyError:
            pass
        raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND, desc = 'Member not found')

    
    def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        '''A stub for _invokeex_ - should never be called.

Simply raises an exception.
'''
        raise NotImplementedError('This class does not provide _invokeex_ semantics')

    
    def _DeleteMemberByName_(self, name, fdex):
        return self._deletememberbyname_(name, fdex)

    
    def _deletememberbyname_(self, name, fdex):
        raise COMException(scode = winerror.E_NOTIMPL)

    
    def _DeleteMemberByDispID_(self, id):
        return self._deletememberbydispid(id)

    
    def _deletememberbydispid_(self, id):
        raise COMException(scode = winerror.E_NOTIMPL)

    
    def _GetMemberProperties_(self, id, fdex):
        return self._getmemberproperties_(id, fdex)

    
    def _getmemberproperties_(self, id, fdex):
        raise COMException(scode = winerror.E_NOTIMPL)

    
    def _GetMemberName_(self, dispid):
        return self._getmembername_(dispid)

    
    def _getmembername_(self, dispid):
        raise COMException(scode = winerror.E_NOTIMPL)

    
    def _GetNextDispID_(self, fdex, dispid):
        return self._getnextdispid_(fdex, dispid)

    
    def _getnextdispid_(self, fdex, dispid):
        for None in :
            if None:
                if not None != DISPID_STARTENUM:
                    continue
                continue
                None, self._name_to_dispid_.values(), ids, id = None
                ids.sort()
                if dispid == DISPID_STARTENUM:
                    pass
                return ids[0]
            
            try:
                pass
            except ValueError:
                id,
                raise COMException(scode = winerror.E_UNEXPECTED)
                except IndexError:
                    None, None, self._name_to_dispid_.values(), ids, id, , []
                    raise COMException(scode = winerror.S_FALSE)

            return None
            
            try:
                pass
            except ValueError:
                id,
                raise COMException(scode = winerror.E_UNEXPECTED)
                except IndexError:
                    None, None, self._name_to_dispid_.values(), ids, id, , []
                    raise COMException(scode = winerror.S_FALSE)


    
    def _GetNameSpaceParent_(self):
        return self._getnamespaceparent()

    
    def _getnamespaceparent_(self):
        raise COMException(scode = winerror.E_NOTIMPL)

    __static_attributes__ = ('_com_interfaces_', '_getdispid_', '_getidsofnames_', '_invoke_', '_invokeex_', '_name_to_dispid_', '_obj_', '_query_interface_')

BasicWrapPolicy = None(BasicWrapPolicy, 'BasicWrapPolicy')

def MappedWrapPolicy():
    '''MappedWrapPolicy'''
    __firstlineno__ = 407
    __doc__ = 'Wraps an object using maps to do its magic\n\nThis policy wraps up a Python object, using a number of maps\nwhich translate from a Dispatch ID and flags, into an object to call/getattr, etc.\n\nIt is the responsibility of derived classes to determine exactly how the\nmaps are filled (ie, the derived classes determine the map filling policy.\n\nThis policy supports the following special attributes on the wrapped object\n\n_dispid_to_func_/_dispid_to_get_/_dispid_to_put_ -- These are dictionaries\n  (keyed by integer dispid, values are string attribute names) which the COM\n  implementation uses when it is processing COM requests.  Note that the implementation\n  uses this dictionary for its own purposes - not a copy - which means the contents of\n  these dictionaries will change as the object is used.\n\n'
    
    def _wrap_(self, object):
        BasicWrapPolicy._wrap_(self, object)
        ob = self._obj_
        if hasattr(ob, '_dispid_to_func_'):
            pass
        if hasattr(ob, '_dispid_to_func_'):
            self._dispid_to_func_ = ob._dispid_to_func_
        else:
            self._dispid_to_func_ = { }
        if hasattr(ob, '_dispid_to_get_'):
            pass
        if hasattr(ob, '_dispid_to_get_'):
            self._dispid_to_get_ = ob._dispid_to_get_
        else:
            self._dispid_to_get_ = { }
        if hasattr(ob, '_dispid_to_put_'):
            pass
        if hasattr(ob, '_dispid_to_put_'):
            self._dispid_to_put_ = ob._dispid_to_put_
        return None
        self._dispid_to_put_ = { }

    
    def _getmembername_(self, dispid):
        if dispid in self._dispid_to_func_:
            pass
        return self._dispid_to_func_[dispid]
        if dispid in self._dispid_to_get_:
            pass
        return self._dispid_to_get_[dispid]
        if dispid in self._dispid_to_put_:
            pass
        return self._dispid_to_put_[dispid]
        raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND)

    __static_attributes__ = ('_dispid_to_func_', '_dispid_to_get_', '_dispid_to_put_')

MappedWrapPolicy = None(MappedWrapPolicy, 'MappedWrapPolicy', BasicWrapPolicy)

def DesignatedWrapPolicy():
    '''DesignatedWrapPolicy'''
    __firstlineno__ = 453
    __doc__ = 'A policy which uses a mapping to link functions and dispid\n\n A MappedWrappedPolicy which allows the wrapped object to specify, via certain\n special named attributes, exactly which methods and properties are exposed.\n\n All a wrapped object need do is provide the special attributes, and the policy\n will handle everything else.\n\n Attributes:\n\n _public_methods_ -- Required, unless a typelib GUID is given -- A list\n              of strings, which must be the names of methods the object\n              provides.  These methods will be exposed and callable\n              from other COM hosts.\n _public_attrs_ A list of strings, which must be the names of attributes on the object.\n              These attributes will be exposed and readable and possibly writeable from other COM hosts.\n _readonly_attrs_ -- A list of strings, which must also appear in _public_attrs.  These\n              attributes will be readable, but not writable, by other COM hosts.\n _value_ -- A method that will be called if the COM host requests the "default" method\n              (ie, calls Invoke with dispid==DISPID_VALUE)\n _NewEnum -- A method that will be called if the COM host requests an enumerator on the\n              object (ie, calls Invoke with dispid==DISPID_NEWENUM.)\n              It is the responsibility of the method to ensure the returned\n              object conforms to the required Enum interface.\n\n_typelib_guid_ -- The GUID of the typelibrary with interface definitions we use.\n_typelib_version_ -- A tuple of (major, minor) with a default of 1,1\n_typelib_lcid_ -- The LCID of the typelib, default = LOCALE_USER_DEFAULT\n\n _Evaluate -- Dunno what this means, except the host has called Invoke with dispid==DISPID_EVALUATE!\n              See the COM documentation for details.\n'
    
    def _wrap_(self, ob):
        tlb_guid = getattr(ob, '_typelib_guid_', None)
        if tlb_guid:
            pass
        MappedWrapPolicy._wrap_(self, ob)
        if hasattr(ob, '_public_methods_'):
            pass
        if not hasattr(ob, '_public_methods_'):
            if hasattr(ob, '_typelib_guid_'):
                pass
            if not hasattr(ob, '_typelib_guid_'):
                pass
        raise ValueError('Object does not support DesignatedWrapPolicy, as it does not have either _public_methods_ or _typelib_guid_ attributes.')
        for None in self._dispid_to_func_.items():
            if ():
                continue
                for None in self._dispid_to_get_.items():
                    if ():
                        continue
                        for None in self._dispid_to_put_.items():
                            if ():
                                continue
                                for None in universal_data:
                                    if (name,):
                                        if invkind == DISPATCH_METHOD:
                                            name = dispid
                                            continue
                                        if invkind in (DISPATCH_PROPERTYPUT, DISPATCH_PROPERTYPUTREF):
                                            self._dispid_to_put_[dispid] = name
                                            continue
                                        if invkind == DISPATCH_PROPERTYGET:
                                            self._dispid_to_get_[dispid] = name
                                            continue
                                        raise ValueError('unexpected invkind: %d (%s)' % (invkind, name))
        if hasattr(ob, '_value_'):
            pass
        if hasattr(ob, '_value_'):
            self._dispid_to_get_[DISPID_VALUE] = '_value_'
            self._dispid_to_put_[DISPID_PROPERTYPUT] = '_value_'
        if hasattr(ob, '_NewEnum'):
            pass
        if hasattr(ob, '_NewEnum'):
            self._name_to_dispid_['_newenum'] = DISPID_NEWENUM
            self._dispid_to_func_[DISPID_NEWENUM] = '_NewEnum'
        if hasattr(ob, '_Evaluate'):
            pass
        if hasattr(ob, '_Evaluate'):
            self._name_to_dispid_['_evaluate'] = DISPID_EVALUATE
            self._dispid_to_func_[DISPID_EVALUATE] = '_Evaluate'
        next_dispid = self._allocnextdispid(999)
        if hasattr(ob, '_public_attrs_'):
            pass
        if hasattr(ob, '_public_attrs_'):
            if hasattr(ob, '_readonly_attrs_'):
                pass
            for name in ob._public_attrs_:
                dispid = self._name_to_dispid_.get(name.lower())
                if dispid:
                    dispid = next_dispid
                    self._name_to_dispid_[name.lower()] = dispid
                next_dispid = self._allocnextdispid(next_dispid)
                self._dispid_to_get_[dispid] = name
                if not name not in readonly:
                    continue
                self._dispid_to_put_[dispid] = name
        None if hasattr(ob, '_readonly_attrs_') else None
        for name in getattr(ob, '_public_methods_', []):
            dispid = self._name_to_dispid_.get(name.lower())
            if dispid:
                dispid = next_dispid
                self._name_to_dispid_[name.lower()] = dispid
            next_dispid = self._allocnextdispid(next_dispid)
            self._dispid_to_func_[dispid] = name
        self._typeinfos_ = None
        return None
        

    
    def _build_typeinfos_(self):
        tlb_guid = getattr(self._obj_, '_typelib_guid_', None)
        if tlb_guid:
            pass
        return []
        if ():
            pass
        tlb.GetTypeComp() = None(tlb_guid, tlb_major, tlb_minor)
        for iname in self._obj_._com_interfaces_:
            
            try:
                if ():
                    if type_info:
                        pass
                    return type_info, [
                        type_info]
            except pythoncom.com_error:
                getattr(self._obj_, '_typelib_version_', (1, 0))

        ()
        return []

    
    def _GetTypeInfoCount_(self):
        if self._typeinfos_:
            self._typeinfos_ = self._build_typeinfos_()
        return len(self._typeinfos_)

    
    def _GetTypeInfo_(self, index, lcid):
        if self._typeinfos_:
            self._typeinfos_ = self._build_typeinfos_()
        if index < 0 or index >= len(self._typeinfos_):
            pass
        raise COMException(scode = winerror.DISP_E_BADINDEX)
        return (0, self._typeinfos_[index])

    
    def _allocnextdispid(self, last_dispid):
        last_dispid += 1
        if last_dispid not in self._dispid_to_func_ and last_dispid not in self._dispid_to_get_ and last_dispid not in self._dispid_to_put_:
            pass
        return last_dispid
        continue

    
    def _invokeex_(self, dispid, lcid, wFlags, args, kwArgs, serviceProvider):
        if wFlags & DISPATCH_METHOD:
            pass
        if wFlags & DISPATCH_METHOD:
            
            try:
                funcname = self._dispid_to_func_[dispid]
            except KeyError:
                if wFlags & DISPATCH_PROPERTYGET:
                    pass
                if not wFlags & DISPATCH_PROPERTYGET:
                    pass
                raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND)

            
            try:
                func = getattr(self._obj_, funcname)
            except AttributeError:
                raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND)

            
            try:
                pass
            except TypeError:
                v = None
                if str(v).find('arguments') >= 0:
                    pass
                print(f'''** TypeError {v} calling function {func}({args})''')
                raise 
                v = None
                del v

            return None
        if None & DISPATCH_PROPERTYGET:
            pass
        if None & DISPATCH_PROPERTYGET:
            
            try:
                name = self._dispid_to_get_[dispid]
            except KeyError:
                retob
                raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND)

            retob = getattr(self._obj_, name)
            if isinstance(retob, types.MethodType):
                pass
            if isinstance(retob, types.MethodType):
                pass
            retob = None(args)
        return retob
        if wFlags & (DISPATCH_PROPERTYPUT | DISPATCH_PROPERTYPUTREF):
            pass
        if wFlags & (DISPATCH_PROPERTYPUT | DISPATCH_PROPERTYPUTREF):
            
            try:
                name = self._dispid_to_put_[dispid]
            except KeyError:
                retob
                raise COMException(scode = winerror.DISP_E_MEMBERNOTFOUND)

            fn = getattr(self._obj_, 'Set' + name, None)
            if isinstance(fn, types.MethodType):
                pass
            if isinstance(fn, types.MethodType):
                if isinstance(getattr(self._obj_, name, None), types.MethodType):
                    pass
                if isinstance(getattr(self._obj_, name, None), types.MethodType):
                    None(args)
            return None
            setattr(self._obj_, name, args[0])
        return None
        raise COMException(scode = winerror.E_INVALIDARG, desc = 'invalid wFlags')

    __static_attributes__ = ('_typeinfos_',)

DesignatedWrapPolicy = None(DesignatedWrapPolicy, 'DesignatedWrapPolicy', MappedWrapPolicy)

def EventHandlerPolicy():
    '''EventHandlerPolicy'''
    __firstlineno__ = 669
    __doc__ = 'The default policy used by event handlers in the win32com.client package.\n\nIn addition to the base policy, this provides argument conversion semantics for\nparams: dispatch params are converted to dispatch objects\n\nNOTE: Later, we may allow the object to override this process??\n'
    
    def _transform_args_(self, args, kwArgs, dispid, lcid, wFlags, serviceProvider):
        ret = []
        for arg in args:
            if isinstance(arg, IDispatchType):
                pass
            if isinstance(arg, IDispatchType):
                import win32com.client as win32com
                arg = win32com.client.Dispatch(arg)
            elif isinstance(arg, IUnknownType):
                pass
            if isinstance(arg, IUnknownType):
                
                try:
                    import win32com.client as win32com
                    arg = win32com.client.Dispatch(arg.QueryInterface(pythoncom.IID_IDispatch))

                ret.append(arg)
                continue
                return (tuple(ret), kwArgs)
            if pythoncom.error:
                pass
        continue

    
    def _invokeex_(self, dispid, lcid, wFlags, args, kwArgs, serviceProvider):
