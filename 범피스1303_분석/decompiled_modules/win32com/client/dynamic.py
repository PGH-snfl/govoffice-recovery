# Source Generated with Decompyle++
# File: dynamic.marshal (Python 3.13)

'''Support for dynamic COM client support.

Introduction
 Dynamic COM client support is the ability to use a COM server without
 prior knowledge of the server.  This can be used to talk to almost all
 COM servers, including much of MS Office.

 In general, you should not use this module directly - see below.

Example
 >>> import win32com.client
 >>> xl = win32com.client.Dispatch("Excel.Application")
 # The line above invokes the functionality of this class.
 # xl is now an object we can use to talk to Excel.
 >>> xl.Visible = 1 # The Excel window becomes visible.

'''
import traceback
from itertools import chain
from types import MethodType
import pythoncom
import win32com.client as win32com
import winerror
from pywintypes import IIDType
from  import build
debugging = 0
debugging_attr = 0
LCID = 0
ERRORS_BAD_CONTEXT = [
    winerror.DISP_E_MEMBERNOTFOUND,
    winerror.DISP_E_BADPARAMCOUNT,
    winerror.DISP_E_PARAMNOTOPTIONAL,
    winerror.DISP_E_TYPEMISMATCH,
    winerror.E_INVALIDARG]
ALL_INVOKE_TYPES = [
    pythoncom.INVOKE_PROPERTYGET,
    pythoncom.INVOKE_PROPERTYPUT,
    pythoncom.INVOKE_PROPERTYPUTREF,
    pythoncom.INVOKE_FUNC]

def debug_print(*args):
    if debugging:
        pass
    if debugging:
        for arg in args:
            print(arg, end = ' ')
        print()
    return None


def debug_attr_print(*args):
    if debugging_attr:
        pass
    if debugging_attr:
        for arg in args:
            print(arg, end = ' ')
        print()
    return None

PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
PyIUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
_GoodDispatchTypes = (str, IIDType)
if (lambda IDispatch, clsctx: if isinstance(IDispatch, PyIDispatchType):
passif isinstance(IDispatch, PyIDispatchType):
passIDispatchif isinstance(IDispatch, _GoodDispatchTypes):
passif isinstance(IDispatch, _GoodDispatchTypes):
try:
IDispatch = None(IDispatch)except pythoncom.ole_error:
IDispatch = None(IDispatch, None, clsctx, pythoncom.IID_IDispatch)IDispatchIDispatch = getattr(IDispatch, '_oleobj_', IDispatch)IDispatch):
    
    def _GetGoodDispatch(IDispatch, clsctx):
        if isinstance(IDispatch, PyIDispatchType):
            pass
        if isinstance(IDispatch, PyIDispatchType):
            pass
        return IDispatch
        if isinstance(IDispatch, _GoodDispatchTypes):
            pass
        if isinstance(IDispatch, _GoodDispatchTypes):
            
            try:
                IDispatch = None(IDispatch)
            except pythoncom.ole_error:
                IDispatch = None(IDispatch, None, clsctx, pythoncom.IID_IDispatch)

        return IDispatch
        IDispatch = getattr(IDispatch, '_oleobj_', IDispatch)
        return IDispatch


def _GetGoodDispatchAndUserName(IDispatch, userName, clsctx):
    return (_GetGoodDispatch(IDispatch, clsctx), userName)


def _GetDescInvokeType(entry, invoke_type):
    if entry:
        pass
    if entry:
        if entry.desc:
            pass
        if not entry.desc:
            pass
    return invoke_type
    if entry.desc.desckind == pythoncom.DESCKIND_VARDESC:
        pass
    return invoke_type
    return entry.desc.invkind

if (lambda IDispatch, userName, createClass, typeinfo, clsctx: if ():
passif createClass:
passNone = CDispatchtry:
if typeinfo:
passtypeinfo = IDispatch.GetTypeInfo()olerepr = MakeOleRepr(IDispatch, typeinfo, lazydata)None(IDispatch, olerepr, userName, lazydata = lazydata)if pythoncom.com_error:
createClasstypeinfo = Nonecontinue):
    
    def Dispatch(IDispatch, userName, createClass, typeinfo, clsctx):
        if ():
            pass
        if createClass:
            pass
        None = CDispatch
        
        try:
            if typeinfo:
                pass
            typeinfo = IDispatch.GetTypeInfo()

        olerepr = MakeOleRepr(IDispatch, typeinfo, lazydata)
        return None(IDispatch, olerepr, userName, lazydata = lazydata)
        if pythoncom.com_error:
            createClass
            typeinfo = None
        continue


def MakeOleRepr(IDispatch, typeinfo, typecomp):
    olerepr = None
    if typeinfo:
        
        try:
            attr = typeinfo.GetTypeAttr()
            if attr[5] == pythoncom.TKIND_INTERFACE:
                if attr[11] & pythoncom.TYPEFLAG_FDUAL:
                    pass
                if attr[11] & pythoncom.TYPEFLAG_FDUAL:
                    href = typeinfo.GetRefTypeOfImplType(-1)
                    typeinfo = typeinfo.GetRefTypeInfo(href)
            attr = typeinfo.GetTypeAttr()

    if olerepr:
        pass
    olerepr = None()
    return olerepr
    if pythoncom.ole_error:
        build.DispatchItem
    continue

if (lambda IDispatch, userName, createClass, clsctx: if ():
passif createClass:
passIDispatch(build.DispatchItem, None(), userName)):
    
    def DumbDispatch(IDispatch, userName, createClass, clsctx):
        '''Dispatch with no type info'''
        if ():
            pass
        if createClass:
            pass
        return IDispatch(build.DispatchItem, None(), userName)


def CDispatch():
    '''CDispatch'''
    __firstlineno__ = 187
    if (lambda self, IDispatch, olerepr, userName, lazydata: if userName:
passuserName = '<unknown>'self.__dict__['_oleobj_'] = IDispatchself.__dict__['_username_'] = userNameself.__dict__['_olerepr_'] = olereprself.__dict__['_mapCachedItems_'] = { }self.__dict__['_builtMethods_'] = { }self.__dict__['_enum_'] = Noneself.__dict__['_unicode_to_string_'] = Noneself.__dict__['_lazydata_'] = lazydata):
        
        def __init__(self, IDispatch, olerepr, userName, lazydata):
            if userName:
                pass
            userName = '<unknown>'
            self.__dict__['_oleobj_'] = IDispatch
            self.__dict__['_username_'] = userName
            self.__dict__['_olerepr_'] = olerepr
            self.__dict__['_mapCachedItems_'] = { }
            self.__dict__['_builtMethods_'] = { }
            self.__dict__['_enum_'] = None
            self.__dict__['_unicode_to_string_'] = None
            self.__dict__['_lazydata_'] = lazydata

    
    def __call__(self, *args):
        """Provide 'default dispatch' COM functionality - allow instance to be called"""
        if self._olerepr_.defaultDispatchName:
            pass
        if self._olerepr_.defaultDispatchName or ():
            pass
        elif pythoncom.DISPID_VALUE or invkind:
            pass
        return self._oleobj_.Invoke(None(allArgs), self._olerepr_.defaultDispatchName, None)
        raise TypeError('This dispatch object does not define a default method')

    
    def __bool__(self):
        return True

    
    def __repr__(self):
        return '<COMObject %s>' % self._username_

    
    def __str__(self):
        
        try:
            pass
        except pythoncom.com_error:
            details = None
            if details.hresult not in ERRORS_BAD_CONTEXT:
                pass
            raise 


    
    def __dir__(self):
        attributes = chain(self.__dict__, dir(self.__class__), self._dir_ole_())
        
        try:
            pass
        except AttributeError:
            p,

        for None in :
            if None:
                continue
                None(None, None, p,) = None
        return list(set(attributes))
        

    
    def _dir_ole_(self):
        items_dict = { }
        for iTI in range(0, self._oleobj_.GetTypeInfoCount()):
            typeInfo = self._oleobj_.GetTypeInfo(iTI)
            self._UpdateWithITypeInfo_(items_dict, typeInfo)
        return list(items_dict)

    
    def _UpdateWithITypeInfo_(self, items_dict, typeInfo):
        typeInfos = [
            typeInfo]
        inspectedIIDs = {
            pythoncom.IID_IDispatch: None }
        if len(typeInfos) > 0:
            typeInfo = typeInfos.pop()
            typeAttr = typeInfo.GetTypeAttr()
            if typeAttr.iid not in inspectedIIDs:
                inspectedIIDs[typeAttr.iid] = None
                for iFun in range(0, typeAttr.cFuncs):
                    funDesc = typeInfo.GetFuncDesc(iFun)
                    funName = typeInfo.GetNames(funDesc.memid)[0]
                    if not funName not in items_dict:
                        continue
                    items_dict[funName] = None
                for iImplType in range(0, typeAttr.cImplTypes):
                    iRefType = typeInfo.GetRefTypeOfImplType(iImplType)
                    refTypeInfo = typeInfo.GetRefTypeInfo(iRefType)
                    typeInfos.append(refTypeInfo)
            if len(typeInfos) > 0:
                continue
        return None

    
    def __eq__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ == other

    
    def __ne__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ != other

    
    def __int__(self):
        return int(self.__call__())

    
    def __len__(self):
        if ():
            if invkind:
                pass
            if invkind:
                pass
        return self._oleobj_.Invoke(dispid, LCID, invkind, 1)
        raise TypeError('This dispatch object does not define a Count method')

    
    def _NewEnum(self):
        
        try:
            invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
            enum = self._oleobj_.InvokeTypes(pythoncom.DISPID_NEWENUM, LCID, invkind, (13, 10), ())
        except pythoncom.com_error:
            pass

        util = util
        import 
        return util.WrapEnum(enum, None)

    
    def __getitem__(self, index):
        if isinstance(index, int):
            pass
        if isinstance(index, int):
            if self.__dict__['_enum_']:
                self.__dict__['_enum_'] = self._NewEnum()
            if self.__dict__['_enum_']:
                pass
        return self._get_good_object_(self._enum_.__getitem__(index))
        if () or invkind:
            pass
        return self._get_good_object_(self._oleobj_.Invoke(dispid, LCID, invkind, 1, index))
        raise TypeError('This object does not support enumeration')

    
    def __setitem__(self, index, *args):
        if self._olerepr_.defaultDispatchName:
            pass
        if self._olerepr_.defaultDispatchName or ():
            pass
        elif pythoncom.DISPID_VALUE or invkind:
            pass
        return self._oleobj_.Invoke(None(allArgs), self._olerepr_.defaultDispatchName, None)
        raise TypeError('This dispatch object does not define a default method')

    
    def _find_dispatch_type_(self, methodName):
        if methodName in self._olerepr_.mapFuncs:
            item = self._olerepr_.mapFuncs[methodName]
        return (item.desc[4], item.dispid)
        if methodName in self._olerepr_.propMapGet:
            item = self._olerepr_.propMapGet[methodName]
        return (item.desc[4], item.dispid)
        
        try:
            dispid = self._oleobj_.GetIDsOfNames(0, methodName)
        except:
            pass

        return (pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, dispid)

    
    def _ApplyTypes_(self, dispid, wFlags, retType, argTypes, user, resultCLSID, *args):
        result = None((dispid, LCID, wFlags, retType, argTypes) + args)
        return self._get_good_object_(result, user, resultCLSID)

    if (lambda self, ob, userName, returnCLSID: Dispatch(ob, userName)):
        
        def _wrap_dispatch_(self, ob, userName, returnCLSID):
            return Dispatch(ob, userName)

    if (lambda self, ob, userName, ReturnCLSID: if isinstance(ob, PyIDispatchType):
passif isinstance(ob, PyIDispatchType):
passself._wrap_dispatch_(ob, userName, ReturnCLSID)if isinstance(ob, PyIUnknownType):
passif isinstance(ob, PyIUnknownType):
try:
ob = ob.QueryInterface(pythoncom.IID_IDispatch)except pythoncom.com_error:
passself._wrap_dispatch_(ob, userName, ReturnCLSID)ob):
        
        def _get_good_single_object_(self, ob, userName, ReturnCLSID):
            if isinstance(ob, PyIDispatchType):
                pass
            if isinstance(ob, PyIDispatchType):
                pass
            return self._wrap_dispatch_(ob, userName, ReturnCLSID)
            if isinstance(ob, PyIUnknownType):
                pass
            if isinstance(ob, PyIUnknownType):
                
                try:
                    ob = ob.QueryInterface(pythoncom.IID_IDispatch)
                except pythoncom.com_error:
                    pass

            return self._wrap_dispatch_(ob, userName, ReturnCLSID)
            return ob

    if (lambda self, ob, userName, ReturnCLSID: if ob:
passNoneif isinstance(ob, tuple):
passif isinstance(ob, tuple):
if (lambda o, s, oun, rc: s._get_good_single_object_(o, oun, rc)):
                pass
        return map((self, userName, ReturnCLSID)((lambda o, s, oun, rc: s._get_good_single_object_(o, oun, rc)), ob))
        return self._get_good_single_object_(ob)
):
        
        def _get_good_object_(self, ob, userName, ReturnCLSID):
            '''Given an object (usually the retval from a method), make it a good object to return.
Basically checks if it is a COM object, and wraps it up.
Also handles the fact that a retval may be a tuple of retvals'''
            if ob:
                pass
            return None
            if isinstance(ob, tuple):
                pass
            if isinstance(ob, tuple):
                if (lambda o, s, oun, rc: s._get_good_single_object_(o, oun, rc)):
                    pass
            return map((self, userName, ReturnCLSID)((lambda o, s, oun, rc: s._get_good_single_object_(o, oun, rc)), ob))
            return self._get_good_single_object_(ob)

    
    def _make_method_(self, name):
        '''Make a method object - Assumes in olerepr funcmap'''
        methodName = None(name)
        methodCodeList = self._olerepr_.MakeFuncMethod(self._olerepr_.mapFuncs[name], methodName, 0)
        methodCode = '\n'.join(methodCodeList)
        
        try:
            codeObject = compile(methodCode, '<COMObject %s>' % self._username_, 'exec')
            tempNameSpace = { }
            globNameSpace = globals().copy()
            globNameSpace['Dispatch'] = win32com.client.Dispatch
            exec(codeObject, globNameSpace, tempNameSpace)
            name = methodName
            if tempNameSpace[name]:
                tempNameSpace[name]._builtMethods_[name] = tempNameSpace[name]
                return MethodType(fn, self)

        build.MakePublicAttributeName
        debug_print('Error building OLE definition for code ', methodCode)
        None()

    
    def _Release_(self):
        """Cleanup object - like a close - to force cleanup when you don't
want to rely on Python's reference counting."""
        for childCont in self._mapCachedItems_.values():
            childCont._Release_()
        self._mapCachedItems_ = { }
        if self._oleobj_:
            pass
        if self._oleobj_:
            self._oleobj_.Release()
            self.__dict__['_oleobj_'] = None
        if self._olerepr_:
            pass
        if self._olerepr_:
            self.__dict__['_olerepr_'] = None
        self._enum_ = None

    
    def _proc_(self, name, *args):
        '''Call the named method as a procedure, rather than function.
Mainly used by Word.Basic, which whinges about such things.'''
        
        try:
            item = self._olerepr_.mapFuncs[name]
            dispId = item.dispid
        except KeyError:
            raise AttributeError(name)


    
    def _print_details_(self):
        '''Debug routine - dumps what it knows about an object.'''
        print('AxDispatch container', self._username_)
        
        try:
            print('Methods:')
            for method in self._olerepr_.mapFuncs:
                print('\t', method)
            print('Props:')
            for None in self._olerepr_.propMap.items():
                if ():
                    continue
            print('Get Props:')
            for None in self._olerepr_.propMapGet.items():
                if ():
                    continue
            print('Put Props:')
            for None in self._olerepr_.propMapPut.items():
                if ():
                    continue
        except:
            None()


    
    def __LazyMap__(self, attr):
        
        try:
            if self._LazyAddAttr_(attr):
                pass
            if self._LazyAddAttr_(attr):
                debug_attr_print(f'''{self._username_}.__LazyMap__({attr}) added something''')

        return 1
        return None
        if AttributeError:
            pass
        return 0

    
    def _LazyAddAttr_(self, attr):
        if self._lazydata_:
            pass
        return 0
        res = 0
        if ():
            for None in ALL_INVOKE_TYPES:
                
                try:
                    if ():
                        if x == 0 and attr[:3] in ('Set', 'Get'):
                            pass
                        if ():
                            if x == pythoncom.DESCKIND_FUNCDESC:
                                pass
                            elif x == pythoncom.DESCKIND_VARDESC:
                                olerepr._AddVar_(typeinfo, t, 0) = olerepr._AddFunc_(typeinfo, t, 0)
                            else:
                                r = None
                            if r or r[1]:
                                item = map[key]
                                if map == olerepr.propMapPut:
                                    olerepr._propMapPutCheck_(key, item)
                                elif map == olerepr.propMapGet:
                                    pass
                                res = 1
                                continue
                                continue
                                r[0]
                                return res
                            continue


    
    def _FlagAsMethod(self, *methodNames):
        '''Flag these attribute names as being methods.
Some objects do not correctly differentiate methods and
properties, leading to problems when calling these methods.

Specifically, trying to say: ob.SomeFunc()
may yield an exception "None object is not callable"
In this case, an attempt to fetch the *property* has worked
and returned None, rather than indicating it is really a method.
Calling: ob._FlagAsMethod("SomeFunc")
should then allow this to work.
'''
        for name in methodNames:
            details = None(self.__AttrToID__(name), (name,))
            self._olerepr_.mapFuncs[name] = details

    
    def __AttrToID__(self, attr):
        debug_attr_print('Calling GetIDsOfNames for property {} in Dispatch container {}'.format(attr, self._username_))
        return self._oleobj_.GetIDsOfNames(0, attr)

    
    def __getattr__(self, attr):
        if attr == '__iter__':
            
            try:
                invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
                enum = self._oleobj_.InvokeTypes(pythoncom.DISPID_NEWENUM, LCID, invkind, (13, 10), ())
            except pythoncom.com_error:
                raise AttributeError('This object can not function as an iterator')

            
            def Factory():
                '''CDispatch.__getattr__.<locals>.Factory'''
                __firstlineno__ = 557
                
                def __init__(self, ob):
                    self.ob = ob

                
                def __call__(self):
                    import win32com.client.util as win32com
                    return win32com.client.util.Iterator(self.ob)

                __static_attributes__ = ('ob',)

            Factory = None(Factory, 'Factory')
        return <NODE:12>
        if attr.startswith('_'):
            pass
        if attr.startswith('_'):
            if attr.endswith('_'):
                pass
            if attr.endswith('_'):
                pass
        raise AttributeError(attr)
        
        try:
            pass
        except KeyError:
            pass
        except:
            pass

        return None
        if attr in self._olerepr_.mapFuncs:
            pass
        return self._make_method_(attr)
        retEntry = None
        if self._olerepr_:
            pass
        if self._olerepr_:
            if self._oleobj_:
                pass
            if self._oleobj_:
                retEntry = self._olerepr_.propMap.get(attr)
                if retEntry:
                    pass
                retEntry = self._olerepr_.propMapGet.get(attr)
        if retEntry:
            
            try:
                ret = self._mapCachedItems_[retEntry.dispid]
                debug_attr_print('Cached items has attribute!', ret)

            return retEntry
        debug_attr_print('OLE returned ', ret)
        return self._get_good_object_(ret)
        raise AttributeError(f'''{self._username_}.{attr}''')

    
    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
        return None
        debug_attr_print(f'''SetAttr called for {self._username_}.{attr}={value} on DispatchContainer''')
        if self._olerepr_:
            pass
        if self._olerepr_:
            if attr in self._olerepr_.propMap:
                entry = self._olerepr_.propMap[attr]
                invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
            return None
            if attr in self._olerepr_.propMapPut:
                entry = self._olerepr_.propMapPut[attr]
                invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
        return None
        if self._oleobj_:
            pass
        if self._oleobj_:
            if self.__LazyMap__(attr):
                pass
            if self.__LazyMap__(attr):
                if attr in self._olerepr_.propMap:
                    entry = self._olerepr_.propMap[attr]
                    invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                    self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                return None
                if attr in self._olerepr_.propMapPut:
                    entry = self._olerepr_.propMapPut[attr]
                    invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                    self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
            return None
            
            try:
                entry = None(self.__AttrToID__(attr), (attr,))
            except pythoncom.com_error:
                entry
                entry = None

            if entry:
                
                try:
                    invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                    self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                    self._olerepr_.propMap[attr] = entry
                    debug_attr_print('__setattr__ property {} (id=0x{:x}) in Dispatch container {}'.format(attr, entry.dispid, self._username_))
                except pythoncom.com_error:
                    pass

                return None
                raise AttributeError(f'''Property \'{self._username_}.{attr}\' can not be set.''')

    __static_attributes__ = ('_enum_', '_mapCachedItems_')

CDispatch = None(CDispatch, 'CDispatch')
