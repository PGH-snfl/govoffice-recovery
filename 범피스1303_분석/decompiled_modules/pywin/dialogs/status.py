# Source Generated with Decompyle++
# File: status.marshal (Python 3.13)

import threading
import time
import win32api
import win32con
import win32ui
from pywin.mfc import dialog
from pywin.mfc.thread import WinThread
if (lambda caption, staticText: style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONTcs = win32con.WS_CHILD | win32con.WS_VISIBLEw = 215h = 36h = 40dlg = [
[
caption,
(0, 0, w, h),
style,
None,
(8, 'MS Sans Serif')]]s = win32con.WS_TABSTOP | csdlg.append([
130,
staticText,
1000,
(7, 7, w - 7, h - 32),
cs | win32con.SS_LEFT])dlg):
    
    def MakeProgressDlgTemplate(caption, staticText):
        style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
        cs = win32con.WS_CHILD | win32con.WS_VISIBLE
        w = 215
        h = 36
        h = 40
        dlg = [
            [
                caption,
                (0, 0, w, h),
                style,
                None,
                (8, 'MS Sans Serif')]]
        s = win32con.WS_TABSTOP | cs
        dlg.append([
            130,
            staticText,
            1000,
            (7, 7, w - 7, h - 32),
            cs | win32con.SS_LEFT])
        return dlg


def CStatusProgressDialog():
    '''CStatusProgressDialog'''
    __firstlineno__ = 44
    if (lambda self, title, msg, maxticks, tickincr: self.initMsg = msgtempl = MakeProgressDlgTemplate(title, msg)dialog.Dialog.__init__(self, templ)self.maxticks = maxticksself.tickincr = tickincrself.pbar = None):
        
        def __init__(self, title, msg, maxticks, tickincr):
            self.initMsg = msg
            templ = MakeProgressDlgTemplate(title, msg)
            dialog.Dialog.__init__(self, templ)
            self.maxticks = maxticks
            self.tickincr = tickincr
            self.pbar = None

    
    def OnInitDialog(self):
        rc = dialog.Dialog.OnInitDialog(self)
        self.static = self.GetDlgItem(1000)
        self.pbar = None()
        self.pbar.CreateWindow(win32con.WS_CHILD | win32con.WS_VISIBLE, (10, 30, 310, 44), self, 1001)
        self.pbar.SetRange(0, self.maxticks)
        self.pbar.SetStep(self.tickincr)
        self.progress = 0
        self.pincr = 5
        return rc

    
    def Close(self):
        self.EndDialog(0)

    
    def SetMaxTicks(self, maxticks):
        if self.pbar:
            pass
        return None

    
    def Tick(self):
        if self.pbar:
            pass
        return None

    
    def SetTitle(self, text):
        self.SetWindowText(text)

    
    def SetText(self, text):
        self.SetDlgItemText(1000, text)

    if (lambda self, pos, max: if self.pbar:
if max:
passNoneNone):
        
        def Set(self, pos, max):
            if self.pbar:
                if max:
                    pass
                return None
            return None

    __static_attributes__ = ('initMsg', 'maxticks', 'pbar', 'pincr', 'progress', 'static', 'tickincr')

CStatusProgressDialog = None(CStatusProgressDialog, 'CStatusProgressDialog', dialog.Dialog)
MYWM_SETTITLE = win32con.WM_USER + 10
MYWM_SETMSG = win32con.WM_USER + 11
MYWM_TICK = win32con.WM_USER + 12
MYWM_SETMAXTICKS = win32con.WM_USER + 13
MYWM_SET = win32con.WM_USER + 14

def CThreadedStatusProcessDialog():
    '''CThreadedStatusProcessDialog'''
    __firstlineno__ = 99
    if (lambda self, title, msg, maxticks, tickincr: self.title = titleself.msg = msgself.threadid = None()CStatusProgressDialog.__init__(self, title, msg, maxticks, tickincr)):
        
        def __init__(self, title, msg, maxticks, tickincr):
            self.title = title
            self.msg = msg
            self.threadid = None()
            CStatusProgressDialog.__init__(self, title, msg, maxticks, tickincr)

    
    def OnInitDialog(self):
        rc = CStatusProgressDialog.OnInitDialog(self)
        self.HookMessage(self.OnTitle, MYWM_SETTITLE)
        self.HookMessage(self.OnMsg, MYWM_SETMSG)
        self.HookMessage(self.OnTick, MYWM_TICK)
        self.HookMessage(self.OnMaxTicks, MYWM_SETMAXTICKS)
        self.HookMessage(self.OnSet, MYWM_SET)
        return rc

    
    def _Send(self, msg):
        
        try:
            self.PostMessage(msg)
        except win32ui.error:
            pass


    
    def OnTitle(self, msg):
        CStatusProgressDialog.SetTitle(self, self.title)

    
    def OnMsg(self, msg):
        CStatusProgressDialog.SetText(self, self.msg)

    
    def OnTick(self, msg):
        CStatusProgressDialog.Tick(self)

    
    def OnMaxTicks(self, msg):
        CStatusProgressDialog.SetMaxTicks(self, self.maxticks)

    
    def OnSet(self, msg):
        CStatusProgressDialog.Set(self, self.pos, self.max)

    
    def Close(self):
        if self.threadid:
            pass
        if not self.threadid:
            pass
        raise 'No thread!'()
        None(self.threadid, win32con.WM_QUIT, 0, 0)

    
    def SetMaxTicks(self, maxticks):
        self.maxticks = maxticks
        self._Send(MYWM_SETMAXTICKS)

    
    def SetTitle(self, title):
        self.title = title
        self._Send(MYWM_SETTITLE)

    
    def SetText(self, text):
        self.msg = text
        self._Send(MYWM_SETMSG)

    
    def Tick(self):
        self._Send(MYWM_TICK)

    if (lambda self, pos, max: self.pos = posself.max = maxself._Send(MYWM_SET)):
        
        def Set(self, pos, max):
            self.pos = pos
            self.max = max
            self._Send(MYWM_SET)

    __static_attributes__ = ('max', 'maxticks', 'msg', 'pos', 'threadid', 'title')

CThreadedStatusProcessDialog = None(CThreadedStatusProcessDialog, 'CThreadedStatusProcessDialog', CStatusProgressDialog)

def ProgressThread():
    '''ProgressThread'''
    __firstlineno__ = 163
    if (lambda self, title, msg, maxticks, tickincr: self.title = titleself.msg = msgself.maxticks = maxticksself.tickincr = tickincrself.dialog = NoneNone(self)self.createdEvent = None()):
        
        def __init__(self, title, msg, maxticks, tickincr):
            self.title = title
            self.msg = msg
            self.maxticks = maxticks
            self.tickincr = tickincr
            self.dialog = None
            None(self)
            self.createdEvent = None()

    
    def InitInstance(self):
        self.dialog = CThreadedStatusProcessDialog(self.title, self.msg, self.maxticks, self.tickincr)
        self.dialog.CreateWindow()
        
        try:
            self.dialog.SetForegroundWindow()
        except win32ui.error:
            WinThread.InitInstance

        self.createdEvent.set()
        return None(self)

    
    def ExitInstance(self):
        return 0

    __static_attributes__ = ('createdEvent', 'dialog', 'maxticks', 'msg', 'tickincr', 'title')

ProgressThread = None(ProgressThread, 'ProgressThread', WinThread)
if (lambda title, msg, maxticks, parent: d = CStatusProgressDialog(title, msg, maxticks)d.CreateWindow(parent)d):
    
    def StatusProgressDialog(title, msg, maxticks, parent):
        d = CStatusProgressDialog(title, msg, maxticks)
        d.CreateWindow(parent)
        return d

if (lambda title, msg, maxticks: t = ProgressThread(title, msg, maxticks)t.CreateThread()end_time = None() + 10if None() < end_time:
if t.createdEvent.is_set():
passif t.createdEvent.is_set():
passt.dialogNone()None(0.1)if None() < end_time:
continuet.dialog):
    
    def ThreadedStatusProgressDialog(title, msg, maxticks):
        t = ProgressThread(title, msg, maxticks)
        t.CreateThread()
        end_time = None() + 10
        if None() < end_time:
            if t.createdEvent.is_set():
                pass
            if t.createdEvent.is_set():
                pass
            return t.dialog
        None()
        None(0.1)
        if None() < end_time:
            continue
        return t.dialog


def demo():
    d = StatusProgressDialog('A Demo', 'Doing something...')
    import win32api
    for i in range(100):
        if i == 50:
            pass
        d.SetText('Getting there...')
        if i == 90:
            pass
        d.SetText('Nearly done...')
        None(20)
        d.Tick()
    d.Close()


def thread_demo():
    d = ThreadedStatusProgressDialog('A threaded demo', 'Doing something')
    import win32api
    for i in range(100):
        if i == 50:
            pass
        d.SetText('Getting there...')
        if i == 90:
            pass
        d.SetText('Nearly done...')
        None(20)
        d.Tick()
    d.Close()

if __name__ == '__main__':
    None()
return None
