# Source Generated with Decompyle++
# File: universal.marshal (Python 3.13)

import pythoncom
from win32com.client import gencache
com_error = pythoncom.com_error
if (lambda typelibGUID, lcid, major, minor, interface_names: ret = []try:
mod = None(typelibGUID, lcid, major, minor)except ImportError:
mod = Noneif mod:
import win32com.client.build as win32comtlb = None(typelibGUID, major, minor, lcid)typecomp_lib = tlb.GetTypeComp()if interface_names:
interface_names = []for i in range(tlb.GetTypeInfoCount()):
info = tlb.GetTypeInfo(i)doc = tlb.GetDocumentation(i)attr = info.GetTypeAttr()if not attr.typekind == pythoncom.TKIND_INTERFACE:
if not attr.typekind == pythoncom.TKIND_DISPATCH:
continueif attr.wTypeFlags & pythoncom.TYPEFLAG_FDUAL:
passif not attr.wTypeFlags & pythoncom.TYPEFLAG_FDUAL:
continueinterface_names.append(doc[0])for name in interface_names:
(type_info, type_comp) = typecomp_lib.BindType(name)if type_info:
passraise ValueError(f'''The interface \'{name}\' can not be located''')attr = type_info.GetTypeAttr()if attr.typekind == pythoncom.TKIND_DISPATCH:
refhtype = type_info.GetRefTypeOfImplType(-1)type_info = type_info.GetRefTypeInfo(refhtype)attr = type_info.GetTypeAttr()item = win32com.client.build.VTableItem(type_info, attr, type_info.GetDocumentation(-1))_doCreateVTable(item.clsid, item.python_name, item.bIsDispatch, item.vtableFuncs)for info in item.vtableFuncs:
(names, dispid, desc) = infoinvkind = desc[4]ret.append((dispid, invkind, names[0]))modretif interface_names:
passif not interface_names:
interface_namesfor name in mod.VTablesToClassMap.values():
try:
iid = mod.NamesToIIDMap[name]except KeyError:
raise ValueError(f'''Interface \'{name}\' does not exist in this cached typelib''')sub_mod = None(iid)is_dispatch = getattr(sub_mod, name + '_vtables_dispatch_', None)method_defs = getattr(sub_mod, name + '_vtables_', None)if is_dispatch or method_defs:
passraise ValueError(f'''Interface \'{name}\' is IDispatch only''')_doCreateVTable(iid, name, is_dispatch, method_defs)for info in method_defs:
(names, dispid, desc) = infoinvkind = desc[4]ret.append((dispid, invkind, names[0]))is_dispatchret):
    
    def RegisterInterfaces(typelibGUID, lcid, major, minor, interface_names):
        ret = []
        
        try:
            mod = None(typelibGUID, lcid, major, minor)
        except ImportError:
            mod = None

        if mod:
            import win32com.client.build as win32com
            tlb = None(typelibGUID, major, minor, lcid)
            typecomp_lib = tlb.GetTypeComp()
            if interface_names:
                interface_names = []
                for i in range(tlb.GetTypeInfoCount()):
                    info = tlb.GetTypeInfo(i)
                    doc = tlb.GetDocumentation(i)
                    attr = info.GetTypeAttr()
                    if not attr.typekind == pythoncom.TKIND_INTERFACE:
                        if not attr.typekind == pythoncom.TKIND_DISPATCH:
                            continue
                        if attr.wTypeFlags & pythoncom.TYPEFLAG_FDUAL:
                            pass
                        if not attr.wTypeFlags & pythoncom.TYPEFLAG_FDUAL:
                            continue
                    interface_names.append(doc[0])
            for name in interface_names:
                (type_info, type_comp) = typecomp_lib.BindType(name)
                if type_info:
                    pass
                raise ValueError(f'''The interface \'{name}\' can not be located''')
                attr = type_info.GetTypeAttr()
                if attr.typekind == pythoncom.TKIND_DISPATCH:
                    refhtype = type_info.GetRefTypeOfImplType(-1)
                    type_info = type_info.GetRefTypeInfo(refhtype)
                attr = type_info.GetTypeAttr()
                item = win32com.client.build.VTableItem(type_info, attr, type_info.GetDocumentation(-1))
                _doCreateVTable(item.clsid, item.python_name, item.bIsDispatch, item.vtableFuncs)
                for info in item.vtableFuncs:
                    (names, dispid, desc) = info
                    invkind = desc[4]
                    ret.append((dispid, invkind, names[0]))
                mod
        return ret
        if interface_names:
            pass
        if not interface_names:
            interface_names
        for name in mod.VTablesToClassMap.values():
            
            try:
                iid = mod.NamesToIIDMap[name]
            except KeyError:
                raise ValueError(f'''Interface \'{name}\' does not exist in this cached typelib''')

            sub_mod = None(iid)
            is_dispatch = getattr(sub_mod, name + '_vtables_dispatch_', None)
            method_defs = getattr(sub_mod, name + '_vtables_', None)
            if is_dispatch or method_defs:
                pass
            raise ValueError(f'''Interface \'{name}\' is IDispatch only''')
            _doCreateVTable(iid, name, is_dispatch, method_defs)
            for info in method_defs:
                (names, dispid, desc) = info
                invkind = desc[4]
                ret.append((dispid, invkind, names[0]))
            is_dispatch
        return ret


def _doCreateVTable(iid, interface_name, is_dispatch, method_defs):
    defn = Definition(iid, is_dispatch, method_defs)
    vtbl = pythoncom._univgw.CreateVTable(defn, is_dispatch)
    pythoncom._univgw.RegisterVTable(vtbl, iid, interface_name)


def _CalcTypeSize(typeTuple):
    t = typeTuple[0]
    if t & (pythoncom.VT_BYREF | pythoncom.VT_ARRAY):
        pass
    if t & (pythoncom.VT_BYREF | pythoncom.VT_ARRAY):
        cb = pythoncom._univgw.SizeOfVT(pythoncom.VT_PTR)[1]
    return cb
    if t == pythoncom.VT_RECORD:
        cb = pythoncom._univgw.SizeOfVT(pythoncom.VT_PTR)[1]
    return cb
    cb = pythoncom._univgw.SizeOfVT(t)[1]
    return cb


def Arg():
    '''Arg'''
    __firstlineno__ = 111
    if (lambda self, arg_info, name: self.name = name(self.vt, self.inOut, self.default, self.clsid) = arg_infoself.size = _CalcTypeSize(arg_info)self.offset = 0):
        
        def __init__(self, arg_info, name):
            self.name = name
            (self.vt, self.inOut, self.default, self.clsid) = arg_info
            self.size = _CalcTypeSize(arg_info)
            self.offset = 0

    __static_attributes__ = ('clsid', 'default', 'inOut', 'name', 'offset', 'size', 'vt')

Arg = None(Arg, 'Arg')

def Method():
    '''Method'''
    __firstlineno__ = 120
    if (lambda self, method_info, isEventSink: if (desc,):
all_names[1:] = all_names[0]invkind = desc[4]arg_defs = desc[2]ret_def = desc[8]self.dispid = dispidself.invkind = invkindif isEventSink:
passif isEventSink and name[:2] != 'On':
passname = 'On%s' % nameself.name = namecbArgs = 0self.args = []for argDesc in arg_defs:
arg = Arg(argDesc)arg.offset = cbArgscbArgs += arg.sizeself.args.append(arg)method_infoself.cbArgs = cbArgsself._gw_in_args = self._GenerateInArgTuple()self._gw_out_args = self._GenerateOutArgTuple()):
        
        def __init__(self, method_info, isEventSink):
            if (desc,):
                all_names[1:] = all_names[0]
                invkind = desc[4]
                arg_defs = desc[2]
                ret_def = desc[8]
                self.dispid = dispid
                self.invkind = invkind
                if isEventSink:
                    pass
                if isEventSink and name[:2] != 'On':
                    pass
            name = 'On%s' % name
            self.name = name
            cbArgs = 0
            self.args = []
            for argDesc in arg_defs:
                arg = Arg(argDesc)
                arg.offset = cbArgs
                cbArgs += arg.size
                self.args.append(arg)
            method_info
            self.cbArgs = cbArgs
            self._gw_in_args = self._GenerateInArgTuple()
            self._gw_out_args = self._GenerateOutArgTuple()

    
    def _GenerateInArgTuple(self):
        l = []
        for arg in self.args:
            if arg.inOut & pythoncom.PARAMFLAG_FIN:
                pass
            if not arg.inOut & pythoncom.PARAMFLAG_FIN and arg.inOut == 0:
                continue
            l.append((arg.vt, arg.offset, arg.size))
        return tuple(l)

    
    def _GenerateOutArgTuple(self):
        l = []
        for arg in self.args:
            if arg.inOut & pythoncom.PARAMFLAG_FOUT:
                pass
            if not arg.inOut & pythoncom.PARAMFLAG_FOUT:
                if arg.inOut & pythoncom.PARAMFLAG_FRETVAL:
                    pass
                if not arg.inOut & pythoncom.PARAMFLAG_FRETVAL and arg.inOut == 0:
                    continue
            l.append((arg.vt, arg.offset, arg.size, arg.clsid))
        return tuple(l)

    __static_attributes__ = ('_gw_in_args', '_gw_out_args', 'args', 'cbArgs', 'dispid', 'invkind', 'name')

Method = None(Method, 'Method')

def Definition():
    '''Definition'''
    __firstlineno__ = 168
    
    def __init__(self, iid, is_dispatch, method_defs):
        self._iid = iid
        self._methods = []
        self._is_dispatch = is_dispatch
        for info in method_defs:
            entry = Method(info)
            self._methods.append(entry)

    
    def iid(self):
        return self._iid

    
    def vtbl_argsizes(self):
        for None in :
            if None:
                continue
        return m,
        

    
    def vtbl_argcounts(self):
        for None in :
            pass
        return m,
        

    if (lambda self, ob, index, argPtr, ReadFromInTuple, WriteFromOutTuple: 