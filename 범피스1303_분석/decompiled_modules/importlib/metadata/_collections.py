# Source Generated with Decompyle++
# File: _collections.marshal (Python 3.13)

import collections

def FreezableDefaultDict():
    '''FreezableDefaultDict'''
    __firstlineno__ = 5
    __doc__ = "\nOften it is desirable to prevent the mutation of\na default dict after its initial construction, such\nas to prevent mutation during iteration.\n\n>>> dd = FreezableDefaultDict(list)\n>>> dd[0].append('1')\n>>> dd.freeze()\n>>> dd[1]\n[]\n>>> len(dd)\n1\n"
    if (lambda self, key: None(key)):
        
        def __missing__(self, key):
            return None(key)

        
        def freeze(self):
            if (lambda key: self.default_factory()):
                
                self._frozen = lambda key: self.default_factory()
                return None

        __static_attributes__ = ('_frozen',)
    __classcell__ = __class__
    return __class__

FreezableDefaultDict = None(FreezableDefaultDict, 'FreezableDefaultDict', collections.defaultdict)
Pair = (lambda : __firstlineno__ = 27parse = (lambda cls, text: None(map(str.strip, text.split('=', 1))))()
    __static_attributes__ = ()
)('Pair', collections.namedtuple, None('Pair', 'name value'))
