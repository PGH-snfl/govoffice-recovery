# Source Generated with Decompyle++
# File: _text.marshal (Python 3.13)

import re
from _functools import method_cache

def FoldedCase():
    '''FoldedCase'''
    __firstlineno__ = 7
    __doc__ = '\nA case insensitive string class; behaves just like str\nexcept compares equal when the only variation is case.\n\n>>> s = FoldedCase(\'hello world\')\n\n>>> s == \'Hello World\'\nTrue\n\n>>> \'Hello World\' == s\nTrue\n\n>>> s != \'Hello World\'\nFalse\n\n>>> s.index(\'O\')\n4\n\n>>> s.split(\'O\')\n[\'hell\', \' w\', \'rld\']\n\n>>> sorted(map(FoldedCase, [\'GAMMA\', \'alpha\', \'Beta\']))\n[\'alpha\', \'Beta\', \'GAMMA\']\n\nSequence membership is straightforward.\n\n>>> "Hello World" in [s]\nTrue\n>>> s in ["Hello World"]\nTrue\n\nYou may test for set inclusion, but candidate and elements\nmust both be folded.\n\n>>> FoldedCase("Hello World") in {s}\nTrue\n>>> s in {FoldedCase("Hello World")}\nTrue\n\nString inclusion works as long as the FoldedCase object\nis on the right.\n\n>>> "hello" in FoldedCase("Hello World")\nTrue\n\nBut not if the FoldedCase object is on the left:\n\n>>> FoldedCase(\'hello\') in \'Hello World\'\nFalse\n\nIn that case, use in_:\n\n>>> FoldedCase(\'hello\').in_(\'Hello World\')\nTrue\n\n>>> FoldedCase(\'hello\') > FoldedCase(\'Hello\')\nFalse\n'
    
    def __lt__(self, other):
        return self.lower() < other.lower()

    
    def __gt__(self, other):
        return self.lower() > other.lower()

    
    def __eq__(self, other):
        return self.lower() == other.lower()

    
    def __ne__(self, other):
        return self.lower() != other.lower()

    
    def __hash__(self):
        return hash(self.lower())

    if (lambda self, other: self().__contains__(other.lower())):
        
        def __contains__(self, other):
            return self().__contains__(other.lower())

        
        def in_(self, other):
            '''Does self appear in other?'''
            return self in FoldedCase(other)

    if (lambda self: self()):
        lower = (lambda self: self())()
        
        def index(self, sub):
            return self.lower().index(sub.lower())

    if (lambda self, splitter, maxsplit: pattern = re.escape(None(splitter), re.I)pattern.split(self, maxsplit)):
        
        def split(self, splitter, maxsplit):
            pattern = re.escape(None(splitter), re.I)
            return pattern.split(self, maxsplit)

    __static_attributes__ = ()
    __classcell__ = __class__
    return __class__

FoldedCase = None(FoldedCase, 'FoldedCase', str)
