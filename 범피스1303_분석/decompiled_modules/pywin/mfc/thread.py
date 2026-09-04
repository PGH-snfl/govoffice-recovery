# Source Generated with Decompyle++
# File: thread.marshal (Python 3.13)

import win32ui
from  import object

def WinThread():
    '''WinThread'''
    __firstlineno__ = 8
    if (lambda self, initObj: if initObj:
passinitObj = None()object.CmdTarget.__init__(self, initObj)):
        
        def __init__(self, initObj):
            if initObj:
                pass
            initObj = None()
            object.CmdTarget.__init__(self, initObj)

    
    def InitInstance(self):
        pass

    
    def ExitInstance(self):
        pass

    __static_attributes__ = ()

WinThread = None(WinThread, 'WinThread', object.CmdTarget)

def WinApp():
    '''WinApp'''
    __firstlineno__ = 21
    if (lambda self, initApp: if initApp:
passinitApp = None()WinThread.__init__(self, initApp)):
        
        def __init__(self, initApp):
            if initApp:
                pass
            initApp = None()
            WinThread.__init__(self, initApp)

    __static_attributes__ = ()

WinApp = None(WinApp, 'WinApp', WinThread)
