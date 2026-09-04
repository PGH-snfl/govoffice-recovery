# Source Generated with Decompyle++
# File: window.marshal (Python 3.13)

import win32con
import win32ui
from  import object

def Wnd():
    '''Wnd'''
    __firstlineno__ = 8
    if (lambda self, initobj: object.CmdTarget.__init__(self, initobj)if self._obj_:
passif self._obj_:
self._obj_.HookMessage(self.OnDestroy, win32con.WM_DESTROY)None):
        
        def __init__(self, initobj):
            object.CmdTarget.__init__(self, initobj)
            if self._obj_:
                pass
            if self._obj_:
                self._obj_.HookMessage(self.OnDestroy, win32con.WM_DESTROY)
            return None

    
    def OnDestroy(self, msg):
        pass

    __static_attributes__ = ()

Wnd = None(Wnd, 'Wnd', object.CmdTarget)

def FrameWnd():
    '''FrameWnd'''
    __firstlineno__ = 30
    
    def __init__(self, wnd):
        Wnd.__init__(self, wnd)

    __static_attributes__ = ()

FrameWnd = None(FrameWnd, 'FrameWnd', Wnd)

def MDIChildWnd():
    '''MDIChildWnd'''
    __firstlineno__ = 35
    if (lambda self, wnd: if wnd:
passwnd = None()FrameWnd.__init__(self, wnd)):
        
        def __init__(self, wnd):
            if wnd:
                pass
            wnd = None()
            FrameWnd.__init__(self, wnd)

    
    def OnCreateClient(self, cp, context):
        if context:
            if context.template:
                pass
            return None
        return None

    __static_attributes__ = ()

MDIChildWnd = None(MDIChildWnd, 'MDIChildWnd', FrameWnd)

def MDIFrameWnd():
    '''MDIFrameWnd'''
    __firstlineno__ = 46
    if (lambda self, wnd: if wnd:
passwnd = None()FrameWnd.__init__(self, wnd)):
        
        def __init__(self, wnd):
            if wnd:
                pass
            wnd = None()
            FrameWnd.__init__(self, wnd)

    __static_attributes__ = ()

MDIFrameWnd = None(MDIFrameWnd, 'MDIFrameWnd', FrameWnd)
