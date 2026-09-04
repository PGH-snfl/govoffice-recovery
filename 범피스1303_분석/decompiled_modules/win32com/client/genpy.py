# Source Generated with Decompyle++
# File: genpy.marshal (Python 3.13)

'''genpy.py - The worker for makepy.  See makepy.py for more details

This code was moved simply to speed Python in normal circumstances.  As the makepy.py
is normally run from the command line, it reparses the code each time.  Now makepy
is nothing more than the command line handler and public interface.

The makepy command line etc handling is also getting large enough in its own right!
'''
import os
import sys
import time
from itertools import chain
import pythoncom
from  import build, gencache
makepy_version = '0.5.01'
GEN_FULL = 'full'
GEN_DEMAND_BASE = 'demand(base)'
GEN_DEMAND_CHILD = 'demand(child)'
mapVTToTypeString = 'int'

def MakeDefaultArgsForPropertyPut(argsDesc):
    ret = []
    for desc in argsDesc[1:]:
        default = None(desc)
        if default:
            pass
        
    return tuple(ret)


def MakeMapLineEntry(dispid, wFlags, retType, argTypes, user, resultCLSID):
    for None in :
        if None:
            continue
            None, tuple, argTypes(what,) = None
            return '(%s, %d, %s, %s, "%s", %s)' % (dispid, wFlags, retType[:2], argTypes, user, resultCLSID)


def MakeEventMethodName(eventName):
    if eventName[:2] == 'On':
        pass
    return eventName
    return 'On' + eventName


def WriteSinkEventMap(obj, stream):
    print('\t_dispid_to_func_ = {', file = stream)
    for entry in chain(obj.propMapGet.values(), obj.propMapPut.values(), obj.mapFuncs.values()):
        memid = entry.desc.memid
        print('\t\t%9d : "%s",' % (memid, MakeEventMethodName(entry.names[0])), file = stream)
    print('\t\t}', file = stream)


def WritableItem():
    '''WritableItem'''
    __firstlineno__ = 108
    
    def __lt__(self, other):
        if self.order == other.order:
            pass
        return self.doc < other.doc
        return self.order < other.order

    
    def __repr__(self):
        return f'''OleItem: doc={self.doc}, order={self.order}'''

    __static_attributes__ = ()

WritableItem = None(WritableItem, 'WritableItem')

def RecordItem():
    '''RecordItem'''
    __firstlineno__ = 118
    order = 9
    typename = 'RECORD'
    if (lambda self, typeInfo, typeAttr, doc, bForUser: build.OleItem.__init__(self, doc)self.clsid = typeAttr[0]):
        
        def __init__(self, typeInfo, typeAttr, doc, bForUser):
            build.OleItem.__init__(self, doc)
            self.clsid = typeAttr[0]

    
    def WriteClass(self, generator):
        pass

    __static_attributes__ = ('clsid',)

RecordItem = None(RecordItem, 'RecordItem', build.OleItem, WritableItem)

def WriteAliasesForItem(item, aliasItems, stream):
    for alias in aliasItems.values():
        if item.doc:
            pass
        if not item.doc:
            continue
        if alias.aliasDoc:
            pass
        if not alias.aliasDoc:
            continue
        if not alias.aliasDoc[0] == item.doc[0]:
            continue
        alias.WriteAliasItem(aliasItems, stream)


def AliasItem():
    '''AliasItem'''
    __firstlineno__ = 145
    order = 2
    typename = 'ALIAS'
    if (lambda self, typeinfo, attr, doc, bForUser: build.OleItem.__init__(self, doc)ai = attr[14]self.attr = attrif isinstance(ai, tuple):
passif isinstance(ai, tuple):
if isinstance(ai[1], int):
passif isinstance(ai[1], int):
href = ai[1]alinfo = typeinfo.GetRefTypeInfo(href)self.aliasDoc = alinfo.GetDocumentation(-1)self.aliasAttr = alinfo.GetTypeAttr()Noneself.aliasDoc = Noneself.aliasAttr = None):
        
        def __init__(self, typeinfo, attr, doc, bForUser):
            build.OleItem.__init__(self, doc)
            ai = attr[14]
            self.attr = attr
            if isinstance(ai, tuple):
                pass
            if isinstance(ai, tuple):
                if isinstance(ai[1], int):
                    pass
                if isinstance(ai[1], int):
                    href = ai[1]
                    alinfo = typeinfo.GetRefTypeInfo(href)
                    self.aliasDoc = alinfo.GetDocumentation(-1)
                    self.aliasAttr = alinfo.GetTypeAttr()
            return None
            self.aliasDoc = None
            self.aliasAttr = None

    
    def WriteAliasItem(self, aliasDict, stream):
        if self.bWritten:
            pass
        if self.bWritten:
            pass
        return None
        if self.aliasDoc:
            pass
        if self.aliasDoc:
            depName = self.aliasDoc[0]
            if depName in aliasDict:
                pass
            aliasDict[depName].WriteAliasItem(aliasDict, stream)
            print(self.doc[0] + ' = ' + depName, file = stream)
        else:
            ai = self.attr[14]
            if isinstance(ai, int):
                pass
            if isinstance(ai, int):
                
                try:
                    typeStr = mapVTToTypeString[ai]
                    print(f'''# {self.doc[0]}={typeStr}''', file = stream)
                except KeyError:
                    print(self.doc[0] + " = None # Can't convert alias info " + str(ai), file = stream)

                print(file = stream)
                self.bWritten = 1
                return None

    __static_attributes__ = ('aliasAttr', 'aliasDoc', 'attr', 'bWritten')

AliasItem = None(AliasItem, 'AliasItem', build.OleItem, WritableItem)

def EnumerationItem():
    '''EnumerationItem'''
    __firstlineno__ = 189
    order = 1
    typename = 'ENUMERATION'
    if (lambda self, typeinfo, attr, doc, bForUser: build.OleItem.__init__(self, doc)self.clsid = attr[0]self.mapVars = { }typeFlags = attr[11]if typeFlags & pythoncom.TYPEFLAG_FHIDDEN:
passif not typeFlags & pythoncom.TYPEFLAG_FHIDDEN:
typeFlags & pythoncom.TYPEFLAG_FHIDDENself.hidden = typeFlags & pythoncom.TYPEFLAG_FRESTRICTEDfor j in range(attr[7]):
vdesc = typeinfo.GetVarDesc(j)name = typeinfo.GetNames(vdesc[0])[0]self.mapVars[name] = None(vdesc)):
        
        def __init__(self, typeinfo, attr, doc, bForUser):
            build.OleItem.__init__(self, doc)
            self.clsid = attr[0]
            self.mapVars = { }
            typeFlags = attr[11]
            if typeFlags & pythoncom.TYPEFLAG_FHIDDEN:
                pass
            if not typeFlags & pythoncom.TYPEFLAG_FHIDDEN:
                typeFlags & pythoncom.TYPEFLAG_FHIDDEN
            self.hidden = typeFlags & pythoncom.TYPEFLAG_FRESTRICTED
            for j in range(attr[7]):
                vdesc = typeinfo.GetVarDesc(j)
                name = typeinfo.GetNames(vdesc[0])[0]
                self.mapVars[name] = None(vdesc)

    
    def WriteEnumerationItems(self, stream):
        num = 0
        enumName = self.doc[0]
        for name in sorted(self.mapVars):
            entry = self.mapVars[name]
            vdesc = entry.desc
            if not vdesc[4] == pythoncom.VAR_CONST:
                continue
            val = vdesc[1]
            use = repr(val)
            
            try:
                compile(use, '<makepy>', 'eval')
            except SyntaxError:
                print
                use = use.replace('"', "'")
                use = f'''"{use}" # This VARIANT type cannot be converted automatically'''

            None(name, True)(f'''30={use}10 # from enum {enumName}''', file = stream)
            num += 1
        '\t'
        return num

    __static_attributes__ = ('clsid', 'hidden', 'mapVars')

EnumerationItem = None(EnumerationItem, 'EnumerationItem', build.OleItem, WritableItem)

def VTableItem():
    '''VTableItem'''
    __firstlineno__ = 246
    order = 4
    
    def WriteClass(self, generator):
        self.WriteVTableMap(generator)
        self.bWritten = 1

    
    def WriteVTableMap(self, generator):
        stream = generator.file
        print('%s_vtables_dispatch_ = %d' % (self.python_name, self.bIsDispatch), file = stream)
        print(f'''{self.python_name}_vtables_ = [''', file = stream)
        for v in self.vtableFuncs:
            if (desc,):
                if not desc.desckind == pythoncom.DESCKIND_FUNCDESC:
                    pass
                raise (desc,)
            0 = []
            print('\t((', end = ' ', file = stream)
            for name in names:
                print(repr(name), ',', end = ' ', file = stream)
                item_num += 1
                if not item_num % 5 == 0:
                    continue
                print('\n\t\t\t', end = ' ', file = stream)
            print('), %d, (%r, %r, [' % (dispid, desc.memid, desc.scodeArray), end = ' ', file = stream)
            for arg in desc.args:
                item_num += 1
                if item_num % 5 == 0:
                    pass
                print('\n\t\t\t', end = ' ', file = stream)
                defval = None(arg)
                print(repr((arg[0], arg[1], defval, arg3_repr)), ',', end = ' ', file = stream)
            build.MakeDefaultArgRepr if arg[3] else arg[3]
            print('],', end = ' ', file = stream)
            print(repr(desc.funckind), ',', end = ' ', file = stream)
            print(repr(desc.invkind), ',', end = ' ', file = stream)
            print(repr(desc.callconv), ',', end = ' ', file = stream)
            print(repr(desc.cParamsOpt), ',', end = ' ', file = stream)
            print(repr(desc.oVft), ',', end = ' ', file = stream)
            print(repr(desc.rettype), ',', end = ' ', file = stream)
            print(repr(desc.wFuncFlags), ',', end = ' ', file = stream)
            print(')),', file = stream)
        print(']', file = stream)
        print(file = stream)

    __static_attributes__ = ('bWritten',)

VTableItem = None(VTableItem, 'VTableItem', build.VTableItem, WritableItem)

def DispatchItem():
    '''DispatchItem'''
    __firstlineno__ = 302
    order = 3
    if (lambda self, typeinfo, attr, doc: build.DispatchItem.__init__(self, typeinfo, attr, doc)self.type_attr = attrself.coclass_clsid = None):
        
        def __init__(self, typeinfo, attr, doc):
            build.DispatchItem.__init__(self, typeinfo, attr, doc)
            self.type_attr = attr
            self.coclass_clsid = None

    
    def WriteClass(self, generator):
        if self.bIsDispatch:
            pass
        if not self.bIsDispatch and self.type_attr.typekind == pythoncom.TKIND_DISPATCH:
            pass
        return None
        if self.bIsSink:
            pass
        if self.bIsSink:
            self.WriteEventSinkClassHeader(generator)
            self.WriteCallbackClassBody(generator)
        else:
            self.WriteClassHeader(generator)
            self.WriteClassBody(generator)
        print(file = generator.file)
        self.bWritten = 1

    
    def WriteClassHeader(self, generator):
        generator.checkWriteDispatchBaseClass()
        doc = self.doc
        stream = generator.file
        print('class ' + self.python_name + '(DispatchBaseClass):', file = stream)
        if doc[1]:
            pass
        if doc[1]:
            pass
        '\t'(build._makeDocString + None(doc[1]), file = stream)
        
        try:
            progId = None(self.clsid)
            print("\t# This class is creatable by the name '%s'" % progId, file = stream)
        except pythoncom.com_error:
            pass

        print(f'''\tCLSID = {self.clsid}''', file = stream)
        print(file = stream)
        self.bWritten = 1

    
    def WriteEventSinkClassHeader(self, generator):
        generator.checkWriteEventBaseClass()
        doc = self.doc
        stream = generator.file
        print('class ' + self.python_name + ':', file = stream)
        if doc[1]:
            pass
        if doc[1]:
            pass
        '\t'(build._makeDocString + None(doc[1]), file = stream)
        
        try:
            progId = None(self.clsid)
            print("\t# This class is creatable by the name '%s'" % progId, file = stream)
        except pythoncom.com_error:
            pass

        print(f'''\tCLSID = CLSID_Sink = {self.clsid}''', file = stream)
        print('\t_public_methods_ = [] # For COM Server support', file = stream)
        WriteSinkEventMap(self, stream)
        print(file = stream)
        print('\tdef __init__(self, oobj = None):', file = stream)
        print('\t\tif oobj is None:', file = stream)
        print('\t\t\tself._olecp = None', file = stream)
        print('\t\telse:', file = stream)
        print('\t\t\timport win32com.server.util', file = stream)
        print('\t\t\tfrom win32com.server.policy import EventHandlerPolicy', file = stream)
        print('\t\t\tcpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)', file = stream)
        print('\t\t\tcp=cpc.FindConnectionPoint(self.CLSID_Sink)', file = stream)
        print('\t\t\tcookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))', file = stream)
        print('\t\t\tself._olecp,self._olecp_cookie = cp,cookie', file = stream)
        print('\tdef __del__(self):', file = stream)
        print('\t\ttry:', file = stream)
        print('\t\t\tself.close()', file = stream)
        print('\t\texcept pythoncom.com_error:', file = stream)
        print('\t\t\tpass', file = stream)
        print('\tdef close(self):', file = stream)
        print('\t\tif self._olecp is not None:', file = stream)
        print('\t\t\tcp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None', file = stream)
        print('\t\t\tcp.Unadvise(cookie)', file = stream)
        print('\tdef _query_interface_(self, iid):', file = stream)
        print('\t\timport win32com.server.util', file = stream)
        print('\t\tif iid==self.CLSID_Sink: return win32com.server.util.wrap(self)', file = stream)
        print(file = stream)
        self.bWritten = 1

    
    def WriteCallbackClassBody(self, generator):
        stream = generator.file
        print('\t# Event Handlers', file = stream)
        print('\t# If you create handlers, they should have the following prototypes:', file = stream)
        for entry in chain(self.propMapGet.values(), self.propMapPut.values(), self.mapFuncs.values()):
            fdesc = entry.desc
            methName = MakeEventMethodName(entry.names[0])
            '#\tdef ' + methName + '(self'(build.BuildCallList + None(fdesc, entry.names, 'defaultNamedOptArg', 'defaultNamedNotOptArg', 'defaultUnnamedArg', 'pythoncom.Missing', is_comment = True) + '):', file = stream)
            if entry.doc:
                pass
            if not entry.doc:
                continue
            if entry.doc[1]:
                pass
            if not entry.doc[1]:
                continue
            '#\t\t'(build._makeDocString + None(entry.doc[1]), file = stream)
        print(file = stream)
        self.bWritten = 1

    
    def WriteClassBody(self, generator):
        stream = generator.file
        specialItems = {
            'count': None,
            'item': None,
            'value': None,
            '_newenum': None }
        for name in sorted(self.mapFuncs):
            entry = self.mapFuncs[name]
            if not entry.desc.desckind == pythoncom.DESCKIND_FUNCDESC:
                pass
            raise None
            dispid = entry.desc.memid
            if entry.desc.wFuncFlags & pythoncom.FUNCFLAG_FRESTRICTED:
                pass
            if entry.desc.wFuncFlags & pythoncom.FUNCFLAG_FRESTRICTED and dispid != pythoncom.DISPID_NEWENUM:
                continue
            if entry.desc.funckind != pythoncom.FUNC_DISPATCH:
                continue
            if dispid == pythoncom.DISPID_VALUE:
                lkey = 'value'
            elif dispid == pythoncom.DISPID_NEWENUM:
                specialItems['_newenum'] = (entry, entry.desc.invkind, None)
                continue
            lkey = name.lower()
            if lkey in specialItems and specialItems[lkey]:
                specialItems[lkey] = (entry, entry.desc.invkind, None)
            if generator.bBuildHidden:
                pass
            if not generator.bBuildHidden:
                if entry.hidden:
                    pass
                if entry.hidden:
                    continue
            if entry.GetResultName():
                pass
            if entry.GetResultName():
                pass
            print('\t# Result is of type ' + entry.GetResultName(), file = stream)
            if entry.wasProperty:
                pass
            if entry.wasProperty:
                pass
            print('\t# The method %s is actually a property, but must be used as a method to correctly pass the arguments' % name, file = stream)
            ret = entry(build.MakePublicAttributeName, None(name))
            for line in ret:
                print(line, file = stream)
            self.MakeFuncMethod
        print('\t_prop_map_get_ = {', file = stream)
        for key in sorted(self.propMap):
            entry = self.propMap[key]
            if generator.bBuildHidden:
                pass
            if not generator.bBuildHidden:
                if entry.hidden:
                    pass
                if entry.hidden:
                    continue
            resultName = entry.GetResultName()
            if resultName:
                pass
            if resultName:
                pass
            print(f'''\t\t# Property \'{key}\' is an object of type \'{resultName}\'''', file = stream)
            lkey = key.lower()
            details = entry.desc
            resultDesc = details[2]
            argDesc = ()
            mapEntry = MakeMapLineEntry(details.memid, pythoncom.DISPATCH_PROPERTYGET, resultDesc, argDesc, key, entry.GetResultCLSIDStr())
            if details.memid == pythoncom.DISPID_VALUE:
                lkey = 'value'
            elif details.memid == pythoncom.DISPID_NEWENUM:
                lkey = '_newenum'
            else:
                lkey = key.lower()
            if lkey in specialItems and specialItems[lkey]:
                specialItems[lkey] = (entry, pythoncom.DISPATCH_PROPERTYGET, mapEntry)
                if details.memid == pythoncom.DISPID_NEWENUM:
                    continue
            '\t\t"'(f'''{build.MakePublicAttributeName}{None(key)}": {mapEntry},''', file = stream)
        for key in sorted(self.propMapGet):
            entry = self.propMapGet[key]
            if generator.bBuildHidden:
                pass
            if not generator.bBuildHidden:
                if entry.hidden:
                    pass
                if entry.hidden:
                    continue
            if entry.GetResultName():
                pass
            if entry.GetResultName():
                pass
            print("\t\t# Method '{}' returns object of type '{}'".format(key, entry.GetResultName()), file = stream)
            details = entry.desc
            if not details.desckind == pythoncom.DESCKIND_FUNCDESC:
                pass
            raise None
            lkey = key.lower()
            argDesc = details[2]
            resultDesc = details[8]
            mapEntry = MakeMapLineEntry(details[0], pythoncom.DISPATCH_PROPERTYGET, resultDesc, argDesc, key, entry.GetResultCLSIDStr())
            if details.memid == pythoncom.DISPID_VALUE:
                lkey = 'value'
            elif details.memid == pythoncom.DISPID_NEWENUM:
                lkey = '_newenum'
            else:
                lkey = key.lower()
            if lkey in specialItems and specialItems[lkey]:
                specialItems[lkey] = (entry, pythoncom.DISPATCH_PROPERTYGET, mapEntry)
                if details.memid == pythoncom.DISPID_NEWENUM:
                    continue
            '\t\t"'(f'''{build.MakePublicAttributeName}{None(key)}": {mapEntry},''', file = stream)
        print('\t}', file = stream)
        print('\t_prop_map_put_ = {', file = stream)
        for key in sorted(self.propMap):
            entry = self.propMap[key]
            if generator.bBuildHidden:
                pass
            if not generator.bBuildHidden:
                if entry.hidden:
                    pass
                if entry.hidden:
                    continue
            lkey = key.lower()
            details = entry.desc
            defArgDesc = None(details[2])
            '\t\t"%s" : ((%s, LCID, %d, 0),(%s)),'(build.MakePublicAttributeName % (None(key), details[0], pythoncom.DISPATCH_PROPERTYPUT, defArgDesc), file = stream)
        for key in sorted(self.propMapPut):
            entry = self.propMapPut[key]
            if generator.bBuildHidden:
                pass
            if not generator.bBuildHidden:
                if entry.hidden:
                    pass
                if entry.hidden:
                    continue
            details = entry.desc
            defArgDesc = MakeDefaultArgsForPropertyPut(details[2])
            '\t\t"%s": ((%s, LCID, %d, 0),%s),'(build.MakePublicAttributeName % (None(key), details[0], details[4], defArgDesc), file = stream)
        print('\t}', file = stream)
        if specialItems['value']:
            pass
        if specialItems['value']:
            (entry, invoketype, propArgs) = specialItems['value']
            print(f'''\t# Default {typename} for this class is \'{entry.names[0]}\'''', file = stream)
            for line in ret:
                print(line, file = stream)
            print('\tdef __str__(self, *args):', file = stream)
            print('\t\treturn str(self.__call__(*args))', file = stream)
            print('\tdef __int__(self, *args):', file = stream)
        print('\t\treturn int(self.__call__(*args))', file = stream)
        if specialItems['_newenum']:
            pass
        if specialItems['_newenum']:
            (enumEntry, invoketype, propArgs) = specialItems['_newenum']
            if not enumEntry.desc.desckind == pythoncom.DESCKIND_FUNCDESC:
                pass
            raise None
        invkind = enumEntry.desc.invkind
        resultCLSID = enumEntry.GetResultCLSIDStr()
        invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
        resultCLSID = 'None'
        if resultCLSID == 'None' and 'Item' in self.mapFuncs:
            pass
        resultCLSID = self.mapFuncs['Item'].GetResultCLSIDStr()
        print('\tdef __iter__(self):', file = stream)
        print('\t\t"Return a Python iterator for this object"', file = stream)
        print('\t\ttry:', file = stream)
        print('\t\t\tob = self._oleobj_.InvokeTypes(%d,LCID,%d,(13, 10),())' % (pythoncom.DISPID_NEWENUM, invkind), file = stream)
        print('\t\texcept pythoncom.error:', file = stream)
        print('\t\t\traise TypeError("This object does not support enumeration")', file = stream)
        print('\t\treturn win32com.client.util.Iterator(ob, %s)' % resultCLSID, file = stream)
        if specialItems['item']:
            pass
        if specialItems['item']:
            (entry, invoketype, propArgs) = specialItems['item']
            resultCLSID = entry.GetResultCLSIDStr()
            print('\t#This class has Item property/method which allows indexed access with the object[key] syntax.', file = stream)
            print('\t#Some objects will accept a string or other type of key in addition to integers.', file = stream)
            print('\t#Note that many Office objects do not use zero-based indexing.', file = stream)
            print('\tdef __getitem__(self, key):', file = stream)
        print('\t\treturn self._get_good_object_(self._oleobj_.Invoke(*(%d, LCID, %d, 1, key)), "Item", %s)' % (entry.desc.memid, invoketype, resultCLSID), file = stream)
        if specialItems['count']:
            pass
        if specialItems['count']:
            (entry, invoketype, propArgs) = specialItems['count']
            print('\t#This class has Count() %s - allow len(ob) to provide this' % typename, file = stream)
            for line in ret:
                print(line, file = stream)
            print("\t#This class has a __len__ - this is needed so 'if object:' always returns TRUE.", file = stream)
            print('\tdef __bool__(self):', file = stream)
            print('\t\treturn True', file = stream)
        return None

    __static_attributes__ = ('bWritten', 'coclass_clsid', 'type_attr')

DispatchItem = None(DispatchItem, 'DispatchItem', build.DispatchItem, WritableItem)

def CoClassItem():
    '''CoClassItem'''
    __firstlineno__ = 731
    order = 5
    typename = 'COCLASS'
    if (lambda self, typeinfo, attr, doc, sources, interfaces, bForUser: build.OleItem.__init__(self, doc)self.clsid = attr[0]self.sources = sourcesself.interfaces = interfacesself.bIsDispatch = 1):
        
        def __init__(self, typeinfo, attr, doc, sources, interfaces, bForUser):
            build.OleItem.__init__(self, doc)
            self.clsid = attr[0]
            self.sources = sources
            self.interfaces = interfaces
            self.bIsDispatch = 1

    
    def WriteClass(self, generator):
        generator.checkWriteCoClassBaseClass()
        doc = self.doc
        stream = generator.file
        if generator.generate_type == GEN_DEMAND_CHILD:
            referenced_items = []
            for None in self.sources:
                if ():
                    continue
                    for None in self.interfaces:
                        if ():
                            continue
                            print('import sys', file = stream)
                            for None in referenced_items:
                                print("{} = sys.modules['{}.{}'].{}".format(ref.python_name, generator.base_mod_name, ref.python_name, ref.python_name), file = stream)
                                1 = None
                            
                            try:
                                progId = None(self.clsid)
                                print("# This CoClass is known by the name '%s'" % progId, file = stream)
                            except pythoncom.com_error:
                                pass

                            print('class %s(CoClassBaseClass): # A CoClass' % self.python_name, file = stream)
                            if doc:
                                pass
        if doc:
            if doc[1]:
                pass
            if doc[1]:
                pass
        print('\t# ' + doc[1], file = stream)
        print(f'''\tCLSID = {self.clsid}''', file = stream)
        print('\tcoclass_sources = [', file = stream)
        defItem = None
        for None in self.sources:
            if ():
                if flag & pythoncom.IMPLTYPEFLAG_FDEFAULT:
                    pass
                if flag & pythoncom.IMPLTYPEFLAG_FDEFAULT:
                    pass
                if item.bWritten:
                    pass
                continue
                None if item.bWritten else ()
                print('\t]', file = stream)
                if defItem:
                    pass
                if defItem:
                    if defItem.bWritten:
                        pass
        print(f'''\tdefault_source = {defName}''', file = stream)
        print('\tcoclass_interfaces = [', file = stream)
        defItem = None
        for None in self.interfaces:
            if ():
                if flag & pythoncom.IMPLTYPEFLAG_FDEFAULT:
                    pass
                if flag & pythoncom.IMPLTYPEFLAG_FDEFAULT:
                    pass
                if item.bWritten:
                    pass
                continue
                None if item.bWritten else ()
                print('\t]', file = stream)
                if defItem:
                    pass
                if defItem:
                    if defItem.bWritten:
                        pass
        print(f'''\tdefault_interface = {defName}''', file = stream)
        self.bWritten = 1
        print(file = stream)

    __static_attributes__ = ('bIsDispatch', 'bWritten', 'clsid', 'interfaces', 'sources')

CoClassItem = None(CoClassItem, 'CoClassItem', build.OleItem, WritableItem)

def GeneratorProgress():
    '''GeneratorProgress'''
    __firstlineno__ = 822
    
    def __init__(self):
        pass

    
    def Starting(self, tlb_desc):
        '''Called when the process starts.'''
        self.tlb_desc = tlb_desc

    
    def Finished(self):
        '''Called when the process is complete.'''
        pass

    if (lambda self, desc, maxticks: pass):
        
        def SetDescription(self, desc, maxticks):
            '''We are entering a major step.  If maxticks, then this
is how many ticks we expect to make until finished
'''
            pass

    if (lambda self, desc: pass):
        
        def Tick(self, desc):
            '''Minor progress step.  Can provide new description if necessary'''
            pass

    
    def VerboseProgress(self, desc):
        '''Verbose/Debugging output.'''
        pass

    
    def LogWarning(self, desc):
        '''If a warning is generated'''
        pass

    
    def LogBeginGenerate(self, filename):
        pass

    
    def Close(self):
        pass

    __static_attributes__ = ('tlb_desc',)

GeneratorProgress = None(GeneratorProgress, 'GeneratorProgress')

def Generator():
    '''Generator'''
    __firstlineno__ = 854
    if (lambda self, typelib, sourceFilename, progressObject, bBuildHidden: self.bHaveWrittenDispatchBaseClass = 0self.bHaveWrittenCoClassBaseClass = 0self.bHaveWrittenEventBaseClass = 0self.typelib = typelibself.sourceFilename = sourceFilenameself.bBuildHidden = bBuildHiddenself.progress = progressObjectself.file = None):
        
        def __init__(self, typelib, sourceFilename, progressObject, bBuildHidden):
            self.bHaveWrittenDispatchBaseClass = 0
            self.bHaveWrittenCoClassBaseClass = 0
            self.bHaveWrittenEventBaseClass = 0
            self.typelib = typelib
            self.sourceFilename = sourceFilename
            self.bBuildHidden = bBuildHidden
            self.progress = progressObject
            self.file = None

    
    def CollectOleItemInfosFromType(self):
        ret = []
        for i in range(self.typelib.GetTypeInfoCount()):
            info = self.typelib.GetTypeInfo(i)
            infotype = self.typelib.GetTypeInfoType(i)
            doc = self.typelib.GetDocumentation(i)
            attr = info.GetTypeAttr()
            ret.append((info, infotype, doc, attr))
        return ret

    
    def _Build_CoClass(self, type_info_tuple):
        if () or ():
            for refAttr in range(attr[8]):
                
                try:
                    info.GetRefTypeInfo(info.GetRefTypeOfImplType(j)) = info.GetImplTypeFlags(j)

                child_infos.append((info, refAttr.typekind, refType, refType.GetDocumentation(-1), refAttr, flags))
            newItem = CoClassItem(info, attr, doc)
            return (newItem, child_infos)
        if pythoncom.com_error:
            ()
            continue

    
    def _Build_CoClassChildren(self, coclass, coclass_info, oleItems, vtableItems):
        sources = { }
        interfaces = { }
        for refType in coclass_info:
            if () or () or ():
                if not refAttr.typekind == pythoncom.TKIND_DISPATCH:
                    if not refAttr.typekind == pythoncom.TKIND_INTERFACE:
                        continue
                    if refAttr[11] & pythoncom.TYPEFLAG_FDISPATCHABLE:
                        pass
                    if not refAttr[11] & pythoncom.TYPEFLAG_FDISPATCHABLE:
                        continue
                if flags & pythoncom.IMPLTYPEFLAG_FSOURCE:
                    pass
            if not clsid not in vtableItems:
                continue
            if refAttr[11] & pythoncom.TYPEFLAG_FDUAL:
                pass
            if not refAttr[11] & pythoncom.TYPEFLAG_FDUAL:
                continue
            refAttr = refType.GetTypeAttr()
            if not refAttr.typekind == pythoncom.TKIND_INTERFACE:
                pass
            raise 'must be interface bynow!'()
            vtableItem = VTableItem(refType, refAttr, doc)
            vtableItems[clsid] = vtableItem
        refAttr[0]
        coclass.sources = list(sources.values())
        coclass.interfaces = list(interfaces.values())

    
    def _Build_Interface(self, type_info_tuple):
        if () or () or None:
            if infotype == pythoncom.TKIND_DISPATCH or infotype == pythoncom.TKIND_INTERFACE:
                if attr[11] & pythoncom.TYPEFLAG_FDISPATCHABLE:
                    pass
                if attr[11] & pythoncom.TYPEFLAG_FDISPATCHABLE:
                    if attr.wTypeFlags & pythoncom.TYPEFLAG_FDUAL:
                        pass
        if not infotype in (None, pythoncom.TKIND_INTERFACE):
            pass
        raise 'Must be a real interface at this point'()
        if infotype == pythoncom.TKIND_INTERFACE:
            pass
        vtableItem = VTableItem(info, attr, doc)
        return (oleItem, vtableItem)

    
    def BuildOleItemsFromType(self):
