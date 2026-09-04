# Source Generated with Decompyle++
# File: util.marshal (Python 3.13)

'''General Server side utilities'''
import pythoncom
import winerror
from  import policy
from exception import COMException
if (lambda ob, iid, usePolicy, useDispatcher: if usePolicy:
passusePolicy = policy.DefaultPolicyif useDispatcher == 1:
import win32com.server.dispatcher as win32comuseDispatcher = win32com.server.dispatcher.DefaultDebugDispatcherob = None(ob)if iid:
passob = ob.QueryInterface(iid)ob):
    
    def wrap(ob, iid, usePolicy, useDispatcher):
        '''Wraps an object in a PyGDispatch gateway.

Returns a client side PyI{iid} interface.

Interface and gateway support must exist for the specified IID, as
the QueryInterface() method is used.

'''
        if usePolicy:
            pass
        usePolicy = policy.DefaultPolicy
        if useDispatcher == 1:
            import win32com.server.dispatcher as win32com
        useDispatcher = win32com.server.dispatcher.DefaultDebugDispatcher
        ob = None(ob)
        if iid:
            pass
        ob = ob.QueryInterface(iid)
        return ob


def unwrap(ob):
    '''Unwraps an interface.

Given an interface which wraps up a Gateway, return the object behind
the gateway.
'''
    ob = None(ob)
    if hasattr(ob, 'policy'):
        pass
    if hasattr(ob, 'policy'):
        pass
    ob = ob.policy
    return ob._obj_


def ListEnumerator():
    '''ListEnumerator'''
    __firstlineno__ = 50
    __doc__ = 'A class to expose a Python sequence as an EnumVARIANT.\n\nCreate an instance of this class passing a sequence (list, tuple, or\nany sequence protocol supporting object) and it will automatically\nsupport the EnumVARIANT interface for the object.\n\nSee also the @NewEnum@ function, which can be used to turn the\ninstance into an actual COM server.\n'
    _public_methods_ = [
        'Next',
        'Skip',
        'Reset',
        'Clone']
    if (lambda self, data, index, iid: self._list_ = dataself.index = indexself._iid_ = iid):
        
        def __init__(self, data, index, iid):
            self._list_ = data
            self.index = index
            self._iid_ = iid

    
    def _query_interface_(self, iid):
        if iid == self._iid_:
            pass
        return 1

    
    def Next(self, count):
        result = self._list_[self.index:self.index + count]
        self.Skip(count)
        return result

    
    def Skip(self, count):
        end = self.index + count
        if end > len(self._list_):
            pass
        end = len(self._list_)
        self.index = end

    
    def Reset(self):
        self.index = 0

    
    def Clone(self):
        return self._wrap(self.__class__(self._list_, self.index))

    
    def _wrap(self, ob):
        return wrap(ob)

    __static_attributes__ = ('_iid_', '_list_', 'index')

ListEnumerator = None(ListEnumerator, 'ListEnumerator')

def ListEnumeratorGateway():
    '''ListEnumeratorGateway'''
    __firstlineno__ = 93
    __doc__ = "A List Enumerator which wraps a sequence's items in gateways.\n\nIf a sequence contains items (objects) that have not been wrapped for\nreturn through the COM layers, then a ListEnumeratorGateway can be\nused to wrap those items before returning them (from the Next() method).\n\nSee also the @ListEnumerator@ class and the @NewEnum@ function.\n"
    
    def Next(self, count):
        result = self._list_[self.index:self.index + count]
        self.Skip(count)
        return map(self._wrap, result)

    __static_attributes__ = ()

ListEnumeratorGateway = None(ListEnumeratorGateway, 'ListEnumeratorGateway', ListEnumerator)
if (lambda seq, cls, iid, usePolicy, useDispatcher: ob = None(seq, iid = iid)wrap(ob, iid, usePolicy = usePolicy, useDispatcher = useDispatcher)):
    
    def NewEnum(seq, cls, iid, usePolicy, useDispatcher):
        '''Creates a new enumerator COM server.

This function creates a new COM Server that implements the
IID_IEnumVARIANT interface.

A COM server that can enumerate the passed in sequence will be
created, then wrapped up for return through the COM framework.
Optionally, a custom COM server for enumeration can be passed
(the default is @ListEnumerator@), and the specific IEnum
interface can be specified.
'''
        ob = None(seq, iid = iid)
        return wrap(ob, iid, usePolicy = usePolicy, useDispatcher = useDispatcher)


def Collection():
    '''Collection'''
    __firstlineno__ = 131
    __doc__ = 'A collection of VARIANT values.'
    _public_methods_ = [
        'Item',
        'Count',
        'Add',
        'Remove',
        'Insert']
    if (lambda self, data, readOnly: if data:
passdata = []self.data = dataif readOnly:
passif readOnly:
self._public_methods_ = [
'Item',
'Count']None):
        
        def __init__(self, data, readOnly):
            if data:
                pass
            data = []
            self.data = data
            if readOnly:
                pass
            if readOnly:
                self._public_methods_ = [
                    'Item',
                    'Count']
            return None

    
    def Item(self, *args):
        if len(args) != 1:
            pass
        raise COMException(scode = winerror.DISP_E_BADPARAMCOUNT)
        
        try:
            pass
        except IndexError:
            desc = None
            raise COMException(scode = winerror.DISP_E_BADINDEX, desc = str(desc))
            desc = None
            del desc


    _value_ = Item
    
    def Count(self):
        return len(self.data)

    
    def Add(self, value):
        self.data.append(value)

    
    def Remove(self, index):
        
        try:
            del self.data[index]
        except IndexError:
            desc = None
            raise COMException(scode = winerror.DISP_E_BADINDEX, desc = str(desc))
            desc = None
            del desc


    
    def Insert(self, index, value):
        
        try:
            index = int(index)
        except (ValueError, TypeError):
            raise COMException(scode = winerror.DISP_E_TYPEMISMATCH)

        self.data.insert(index, value)

    
    def _NewEnum(self):
        return NewEnum(self.data)

    __static_attributes__ = ('_public_methods_', 'data')

Collection = None(Collection, 'Collection')
if (lambda seq, cls: policy.DefaultPolicy(cls(None(seq)), pythoncom.IID_IDispatch, pythoncom.IID_IDispatch)):
    
    def NewCollection(seq, cls):
        '''Creates a new COM collection object

This function creates a new COM Server that implements the
common collection protocols, including enumeration. (_NewEnum)

A COM server that can enumerate the passed in sequence will be
created, then wrapped up for return through the COM framework.
Optionally, a custom COM server for enumeration can be passed
(the default is @Collection@).
'''
        return policy.DefaultPolicy(cls(None(seq)), pythoncom.IID_IDispatch, pythoncom.IID_IDispatch)


def FileStream():
    '''FileStream'''
    __firstlineno__ = 200
    _public_methods_ = [
        'Read',
        'Write',
        'Clone',
        'CopyTo',
        'Seek']
    _com_interfaces_ = [
        pythoncom.IID_IStream]
    
    def __init__(self, file):
        self.file = file

    
    def Read(self, amount):
        return self.file.read(amount)

    
    def Write(self, data):
        self.file.write(data)
        return len(data)

    
    def Clone(self):
        return self._wrap(self.__class__(self.file))

    
    def CopyTo(self, dest, cb):
        data = self.file.read(cb)
        cbread = len(data)
        dest.Write(data)
        return (cbread, cbread)

    
    def Seek(self, offset, origin):
        self.file.seek(offset, origin)
        return self.file.tell()

    
    def _wrap(self, ob):
        return wrap(ob)

    __static_attributes__ = ('file',)

FileStream = None(FileStream, 'FileStream')
