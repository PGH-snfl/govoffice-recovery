# Source Generated with Decompyle++
# File: contentmanager.marshal (Python 3.13)

import binascii
import email.charset as email
import email.message as email
import email.errors as email
from email import quoprimime

def ContentManager():
    '''ContentManager'''
    __firstlineno__ = 7
    
    def __init__(self):
        self.get_handlers = { }
        self.set_handlers = { }

    
    def add_get_handler(self, key, handler):
        self.get_handlers[key] = handler

    
    def get_content(self, msg, *args, **kw):
        content_type = msg.get_content_type()
        if content_type in self.get_handlers:
            pass
        return None(None)({ }, kw = None)
        maintype = msg.get_content_maintype()
        if maintype in self.get_handlers:
            pass
        return None(None)({ }, kw = None)
        if '' in self.get_handlers:
            pass
        return None(None)({ }, kw = None)
        raise KeyError(content_type)

    
    def add_set_handler(self, typekey, handler):
        self.set_handlers[typekey] = handler

    
    def set_content(self, msg, obj, *args, **kw):
        if msg.get_content_maintype() == 'multipart':
            pass
        raise TypeError('set_content not valid on multipart')
        handler = self._find_set_handler(msg, obj)
        msg.clear_content()
        None(None)({ }, kw = None)

    
    def _find_set_handler(self, msg, obj):
        full_path_for_error = None
        for typ in type(obj).__mro__:
            if typ in self.set_handlers:
                
            return None, self.set_handlers[typ]
            getattr(typ, '__module__', '') = typ.__qualname__
            if modname:
                pass
            full_path = '.'.join((modname, qname)) if modname else qname
            if full_path_for_error:
                pass
            full_path_for_error = full_path
            if full_path in self.set_handlers:
                
            return full_path_for_error, self.set_handlers[full_path]
            if qname in self.set_handlers:
                
            return None, self.set_handlers[qname]
            if not name in self.set_handlers:
                continue
            
            return typ.__name__, self.set_handlers[name]
        if None in self.set_handlers:
            pass
        return self.set_handlers[None]
        raise KeyError(full_path_for_error)

    __static_attributes__ = ('get_handlers', 'set_handlers')

ContentManager = None(ContentManager, 'ContentManager')

class raw_data_manager:
