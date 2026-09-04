# Source Generated with Decompyle++
# File: object.marshal (Python 3.13)

import win32ui

def Object():
    '''Object'''
    __firstlineno__ = 6
    if (lambda self, initObj: self.__dict__['_obj_'] = initObjif initObj:
passNone):
        
        def __init__(self, initObj):
            self.__dict__['_obj_'] = initObj
            if initObj:
                pass
            return None

    
    def __del__(self):
        self.close()

    
    def __getattr__(self, attr):
        if attr.startswith('__'):
            pass
        if not attr.startswith('__'):
            
            try:
                o = self.__dict__['_obj_']
                if o:
                    pass

            return getattr(o, attr)
        if None[0] != '_' and attr[-1] != '_':
            pass
        raise None('The MFC object has died.')
        raise AttributeError(attr)
        if KeyError:
            win32ui.error
        continue

    
    def OnAttachedObjectDeath(self):
        self._obj_ = None

    
    def close(self):
        if '_obj_' in self.__dict__:
            if self._obj_:
                self._obj_ = None
            return None
        return None

    __static_attributes__ = ('_obj_',)

Object = None(Object, 'Object')

def CmdTarget():
    '''CmdTarget'''
    __firstlineno__ = 46
    
    def __init__(self, initObj):
        Object.__init__(self, initObj)

    
    def HookNotifyRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookNotify(handler, i))
        return oldhandlers

    
    def HookCommandRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookCommand(handler, i))
        return oldhandlers

    
    def HookCommandUpdateRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookCommandUpdate(handler, i))
        return oldhandlers

    __static_attributes__ = ()

CmdTarget = None(CmdTarget, 'CmdTarget', Object)
