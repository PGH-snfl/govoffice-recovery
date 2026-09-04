# Source Generated with Decompyle++
# File: _adapters.marshal (Python 3.13)

import functools
import warnings
import re
import textwrap
import email.message as email
from _text import FoldedCase
_warn = None(warnings.warn, 'Implicit None on return values is deprecated and will raise KeyErrors.', DeprecationWarning, stacklevel = 2)

def Message():
    '''Message'''
    __firstlineno__ = 19
    multiple_use_keys = map(None(FoldedCase, [
        'Classifier',
        'Obsoletes-Dist',
        'Platform',
        'Project-URL',
        'Provides-Dist',
        'Provides-Extra',
        'Requires-Dist',
        'Requires-External',
        'Supported-Platform',
        'Dynamic']))
    if (lambda cls, orig: res = cls(cls)vars(res).update(vars(orig))res):
        if (lambda cls, orig: res = cls(cls)vars(res).update(vars(orig))res):
            
            def __new__(cls, orig):
                res = cls(cls)
                vars(res).update(vars(orig))
                return res

            
            def __init__(self, *args, **kwargs):
                self._headers = self._repair_headers()

    if (lambda self: self()):
        
        def __iter__(self):
            return self()

        if (lambda self, item: res = self(item)if res:
pass_warn()res):
            
            def __getitem__(self, item):
                '''
Warn users that a ``KeyError`` can be expected when a
missing key is supplied. Ref python/importlib_metadata#371.
'''
                res = self(item)
                if res:
                    pass
                _warn()
                return res

            
            def _repair_headers(self):
                
                def redent(value):
                    '''Correct for RFC822 indentation'''
                    if value:
                        pass
                    if value or '\n' not in value:
                        pass
                    return value
                    return None('        ' + value)

                for None in :
                    if (headers, key):
                        continue
                        (headers, key) = None
                        value = , []
                        if self._payload:
                            pass
                        if self._payload:
                            pass
                headers.append(('Description', self.get_payload()))
                return headers
                

    json = (lambda self: if (lambda key: value = self.get_all(key) if key in self.multiple_use_keys else self[key]if key == 'Keywords':
passvalue = None('\\s+', value)tk = key.lower().replace('-', '_')(tk, value)):
            
            def transform(key):
                value = self.get_all(key) if key in self.multiple_use_keys else self[key]
                if key == 'Keywords':
                    pass
                value = None('\\s+', value)
                tk = key.lower().replace('-', '_')
                return (tk, value)

        return dict(map(transform, map(FoldedCase, self)))
)()
    __static_attributes__ = ('_headers',)
    __classcell__ = __class__
    return __class__

Message = None(Message, 'Message', email.message.Message)
