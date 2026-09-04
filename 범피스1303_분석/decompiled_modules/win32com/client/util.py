# Source Generated with Decompyle++
# File: util.marshal (Python 3.13)

'''General client side utilities.

This module contains utility functions, used primarily by advanced COM
programmers, or other COM modules.
'''
import pythoncom
from win32com.client import _get_good_object_
PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
if (lambda ob, resultCLSID: if isinstance(ob, pythoncom.TypeIIDs[pythoncom.IID_IEnumVARIANT]):
passif not isinstance(ob, pythoncom.TypeIIDs[pythoncom.IID_IEnumVARIANT]):
passob = ob.QueryInterface(pythoncom.IID_IEnumVARIANT)EnumVARIANT(ob, resultCLSID)):
    
    def WrapEnum(ob, resultCLSID):
        '''Wrap an object in a VARIANT enumerator.

All VT_DISPATCHs returned by the enumerator are converted to wrapper objects
(which may be either a class instance, or a dynamic.Dispatch type object).

'''
        if isinstance(ob, pythoncom.TypeIIDs[pythoncom.IID_IEnumVARIANT]):
            pass
        if not isinstance(ob, pythoncom.TypeIIDs[pythoncom.IID_IEnumVARIANT]):
            pass
        ob = ob.QueryInterface(pythoncom.IID_IEnumVARIANT)
        return EnumVARIANT(ob, resultCLSID)


def Enumerator():
    '''Enumerator'''
    __firstlineno__ = 25
    __doc__ = 'A class that provides indexed access into an Enumerator\n\nBy wrapping a PyIEnum* object in this class, you can perform\nnatural looping and indexing into the Enumerator.\n\nLooping is very efficient, but it should be noted that although random\naccess is supported, the underlying object is still an enumerator, so\nthis will force many reset-and-seek operations to find the requested index.\n\n'
    
    def __init__(self, enum):
        self._oleobj_ = enum
        self.index = -1

    
    def __getitem__(self, index):
        return self.__GetIndex(index)

    
    def __call__(self, index):
        return self.__GetIndex(index)

    
    def __GetIndex(self, index):
        if isinstance(index, int):
            pass
        if not isinstance(index, int):
            pass
        raise TypeError('Only integer indexes are supported for enumerators')
        if index != self.index + 1:
            self._oleobj_.Reset()
            if index:
                pass
            if index:
                pass
        self._oleobj_.Skip(index)
        self.index = index
        result = self._oleobj_.Next(1)
        if len(result):
            pass
        if len(result):
            pass
        return self._make_retval_(result[0])
        raise IndexError('list index out of range')

    if (lambda self, count: ret = self._oleobj_.Next(count)realRets = []for r in ret:
realRets.append(self._make_retval_(r))tuple(realRets)):
        
        def Next(self, count):
            ret = self._oleobj_.Next(count)
            realRets = []
            for r in ret:
                realRets.append(self._make_retval_(r))
            return tuple(realRets)

    
    def Reset(self):
        return self._oleobj_.Reset()

    
    def Clone(self):
        return self.__class__(self._oleobj_.Clone(), self.resultCLSID)

    
    def _make_retval_(self, result):
        return result

    __static_attributes__ = ('_oleobj_', 'index')

Enumerator = None(Enumerator, 'Enumerator')

def EnumVARIANT():
    '''EnumVARIANT'''
    __firstlineno__ = 85
    if (lambda self, enum, resultCLSID: self.resultCLSID = resultCLSIDEnumerator.__init__(self, enum)):
        
        def __init__(self, enum, resultCLSID):
            self.resultCLSID = resultCLSID
            Enumerator.__init__(self, enum)

    
    def _make_retval_(self, result):
        return _get_good_object_(result, resultCLSID = self.resultCLSID)

    __static_attributes__ = ('resultCLSID',)

EnumVARIANT = None(EnumVARIANT, 'EnumVARIANT', Enumerator)

def Iterator():
    '''Iterator'''
    __firstlineno__ = 94
    if (lambda self, enum, resultCLSID: self.resultCLSID = resultCLSIDself._iter_ = iter(enum.QueryInterface(pythoncom.IID_IEnumVARIANT))):
        
        def __init__(self, enum, resultCLSID):
            self.resultCLSID = resultCLSID
            self._iter_ = iter(enum.QueryInterface(pythoncom.IID_IEnumVARIANT))

    
    def __iter__(self):
        return self

    
    def __next__(self):
        return _get_good_object_(next(self._iter_), resultCLSID = self.resultCLSID)

    __static_attributes__ = ('_iter_', 'resultCLSID')

Iterator = None(Iterator, 'Iterator')
