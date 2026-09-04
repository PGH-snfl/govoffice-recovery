# Source Generated with Decompyle++
# File: dialog.marshal (Python 3.13)

'''Base class for Dialogs.  Also contains a few useful utility functions
'''
import win32con
import win32ui
from  import window

def dllFromDll(dllid):
    """given a 'dll' (maybe a dll, filename, etc), return a DLL object"""
    if dllid:
        pass
    return None
    if isinstance(dllid, str):
        pass
    if isinstance(dllid, str):
        pass
    return None(dllid)
    
    try:
        dllid.GetFileName()
    except AttributeError:
        win32ui.LoadLibrary
        raise TypeError('DLL parameter must be None, a filename or a dll object')

    return dllid


def Dialog():
    '''Dialog'''
    __firstlineno__ = 28
    __doc__ = 'Base class for a dialog'
    if (lambda self, id, dllid: self.dll = dllFromDll(dllid)if isinstance(id, list):
passwindow.Wnd.__init__(self, dlg)self.HookCommands()self.bHaveInit = None):
        
        def __init__(self, id, dllid):
            '''id is the resource ID, or a template
dllid may be None, a dll object, or a string with a dll name'''
            self.dll = dllFromDll(dllid)
            if isinstance(id, list):
                pass
            window.Wnd.__init__(self, dlg)
            self.HookCommands()
            self.bHaveInit = None

    
    def HookCommands(self):
        pass

    
    def OnAttachedObjectDeath(self):
        self.data = self._obj_.data
        window.Wnd.OnAttachedObjectDeath(self)

    
    def OnOK(self):
        self._obj_.OnOK()

    
    def OnCancel(self):
        self._obj_.OnCancel()

    
    def OnInitDialog(self):
        self.bHaveInit = 1
        if self._obj_.data:
            pass
        if self._obj_.data:
            pass
        self._obj_.UpdateData(0)
        return 1

    
    def OnDestroy(self, msg):
        self.dll = None

    
    def AddDDX(self, *args):
        self._obj_.datalist.append(args)

    
    def __bool__(self):
        return True

    
    def __len__(self):
        return len(self.data)

    
    def __getitem__(self, key):
        return self.data[key]

    
    def __setitem__(self, key, item):
        self._obj_.data[key] = item

    
    def keys(self):
        return self.data.keys()

    
    def items(self):
        return self.data.items()

    
    def values(self):
        return self.data.values()

    
    def __contains__(self, key):
        return key in self.data

    has_key = __contains__
    __static_attributes__ = ('bHaveInit', 'data', 'dll')

Dialog = None(Dialog, 'Dialog', window.Wnd)

def PrintDialog():
    '''PrintDialog'''
    __firstlineno__ = 99
    __doc__ = 'Base class for a print dialog'
    if (lambda self, pInfo, dlgID, printSetupOnly, flags, parent, dllid: self.dll = dllFromDll(dllid)if isinstance(dlgID, list):
passif isinstance(dlgID, list):
passraise TypeError('dlgID parameter must be an integer resource ID')dlg = None(dlgID, printSetupOnly, flags, parent, self.dll)window.Wnd.__init__(self, dlg)self.HookCommands()self.bHaveInit = Noneself.pInfo = pInfoflags = pInfo.GetFlags()self['toFile'] = flags & win32ui.PD_PRINTTOFILE != 0self['direct'] = pInfo.GetDirect()self['preview'] = pInfo.GetPreview()self['continuePrinting'] = pInfo.GetContinuePrinting()self['curPage'] = pInfo.GetCurPage()self['numPreviewPages'] = pInfo.GetNumPreviewPages()self['userData'] = pInfo.GetUserData()self['draw'] = pInfo.GetDraw()self['pageDesc'] = pInfo.GetPageDesc()self['minPage'] = pInfo.GetMinPage()self['maxPage'] = pInfo.GetMaxPage()self['offsetPage'] = pInfo.GetOffsetPage()self['fromPage'] = pInfo.GetFromPage()self['toPage'] = pInfo.GetToPage()self['copies'] = 0self['deviceName'] = ''self['driverName'] = ''self['printAll'] = 0self['printCollate'] = 0self['printRange'] = 0self['printSelection'] = 0):
        
        def __init__(self, pInfo, dlgID, printSetupOnly, flags, parent, dllid):
            self.dll = dllFromDll(dllid)
            if isinstance(dlgID, list):
                pass
            if isinstance(dlgID, list):
                pass
            raise TypeError('dlgID parameter must be an integer resource ID')
            dlg = None(dlgID, printSetupOnly, flags, parent, self.dll)
            window.Wnd.__init__(self, dlg)
            self.HookCommands()
            self.bHaveInit = None
            self.pInfo = pInfo
            flags = pInfo.GetFlags()
            self['toFile'] = flags & win32ui.PD_PRINTTOFILE != 0
            self['direct'] = pInfo.GetDirect()
            self['preview'] = pInfo.GetPreview()
            self['continuePrinting'] = pInfo.GetContinuePrinting()
            self['curPage'] = pInfo.GetCurPage()
            self['numPreviewPages'] = pInfo.GetNumPreviewPages()
            self['userData'] = pInfo.GetUserData()
            self['draw'] = pInfo.GetDraw()
            self['pageDesc'] = pInfo.GetPageDesc()
            self['minPage'] = pInfo.GetMinPage()
            self['maxPage'] = pInfo.GetMaxPage()
            self['offsetPage'] = pInfo.GetOffsetPage()
            self['fromPage'] = pInfo.GetFromPage()
            self['toPage'] = pInfo.GetToPage()
            self['copies'] = 0
            self['deviceName'] = ''
            self['driverName'] = ''
            self['printAll'] = 0
            self['printCollate'] = 0
            self['printRange'] = 0
            self['printSelection'] = 0

    
    def OnInitDialog(self):
        self.pInfo.CreatePrinterDC()
        return self._obj_.OnInitDialog()

    
    def OnCancel(self):
        del self.pInfo

    
    def OnOK(self):
        '''DoModal has finished. Can now access the users choices'''
        self._obj_.OnOK()
        pInfo = self.pInfo
        flags = pInfo.GetFlags()
        self['toFile'] = flags & win32ui.PD_PRINTTOFILE != 0
        self['direct'] = pInfo.GetDirect()
        self['preview'] = pInfo.GetPreview()
        self['continuePrinting'] = pInfo.GetContinuePrinting()
        self['curPage'] = pInfo.GetCurPage()
        self['numPreviewPages'] = pInfo.GetNumPreviewPages()
        self['userData'] = pInfo.GetUserData()
        self['draw'] = pInfo.GetDraw()
        self['pageDesc'] = pInfo.GetPageDesc()
        self['minPage'] = pInfo.GetMinPage()
        self['maxPage'] = pInfo.GetMaxPage()
        self['offsetPage'] = pInfo.GetOffsetPage()
        self['fromPage'] = pInfo.GetFromPage()
        self['toPage'] = pInfo.GetToPage()
        self['copies'] = pInfo.GetCopies()
        self['deviceName'] = pInfo.GetDeviceName()
        self['driverName'] = pInfo.GetDriverName()
        self['printAll'] = pInfo.PrintAll()
        self['printCollate'] = pInfo.PrintCollate()
        self['printRange'] = pInfo.PrintRange()
        self['printSelection'] = pInfo.PrintSelection()
        del self.pInfo

    __static_attributes__ = ('bHaveInit', 'dll', 'pInfo')

PrintDialog = None(PrintDialog, 'PrintDialog', Dialog)

def PropertyPage():
    '''PropertyPage'''
    __firstlineno__ = 187
    __doc__ = 'Base class for a Property Page'
    if (lambda self, id, dllid, caption: self.dll = dllFromDll(dllid)if self.dll:
passif self.dll:
passoldRes = None(self.dll)if isinstance(id, list):
passif self.dll:
passif self.dll:
passNone(oldRes)window.Wnd.__init__(self, dlg)self.HookCommands()):
        
        def __init__(self, id, dllid, caption):
            '''id is the resource ID
dllid may be None, a dll object, or a string with a dll name'''
            self.dll = dllFromDll(dllid)
            if self.dll:
                pass
            if self.dll:
                pass
            oldRes = None(self.dll)
            if isinstance(id, list):
                pass
            if self.dll:
                pass
            if self.dll:
                pass
            None(oldRes)
            window.Wnd.__init__(self, dlg)
            self.HookCommands()

    __static_attributes__ = ('dll',)

PropertyPage = None(PropertyPage, 'PropertyPage', Dialog)

def PropertySheet():
    '''PropertySheet'''
    __firstlineno__ = 208
    if (lambda self, caption, dll, pageList: self.dll = dllFromDll(dll)self.sheet = None(caption)window.Wnd.__init__(self, self.sheet)if pageList:
passNone):
        
        def __init__(self, caption, dll, pageList):
            """Initialize a property sheet.  pageList is a list of ID's"""
            self.dll = dllFromDll(dll)
            self.sheet = None(caption)
            window.Wnd.__init__(self, self.sheet)
            if pageList:
                pass
            return None

    
    def OnInitDialog(self):
        return self._obj_.OnInitDialog()

    
    def DoModal(self):
        if self.dll:
            pass
        if self.dll:
            pass
        oldRes = None(self.dll)
        rc = self.sheet.DoModal()
        if self.dll:
            pass
        if self.dll:
            pass
        None(oldRes)
        return rc

    
    def AddPage(self, pages):
        if self.dll:
            pass
        if self.dll:
            pass
        oldRes = None(self.dll)
        
        try:
            pages[0]
            isSeq = 1
        except (TypeError, KeyError):
            win32ui.SetResource
            isSeq = 0

        if isSeq:
            pass
        if self.dll:
            pass
        if self.dll:
            None(oldRes)
        return None

    
    def DoAddSinglePage(self, page):
        '''Page may be page, or int ID. Assumes DLL setup'''
        if isinstance(page, int):
            pass
        if isinstance(page, int):
            win32ui.CreatePropertyPage(None(page))
        return None
        self.sheet.AddPage(page)

    __static_attributes__ = ('dll', 'sheet')

PropertySheet = None(PropertySheet, 'PropertySheet', window.Wnd)
if (lambda prompt, defValue, title: if title:
passtitle = None().GetWindowText()
def DlgSimpleInput():
'''GetSimpleInput.<locals>.DlgSimpleInput'''
__firstlineno__ = 261
def __init__(self, prompt, defValue, title):
self.title = titleDialog.__init__(self, win32ui.IDD_SIMPLE_INPUT)self.AddDDX(win32ui.IDC_EDIT1, 'result')self.AddDDX(win32ui.IDC_PROMPT1, 'prompt')self._obj_.data['result'] = defValueself._obj_.data['prompt'] = prompt
def OnInitDialog(self):
self.SetWindowText(self.title)Dialog.OnInitDialog(self)__static_attributes__ = ('title',)DlgSimpleInput = None(DlgSimpleInput, 'DlgSimpleInput', Dialog)
class dlg(title, defValue, prompt):
