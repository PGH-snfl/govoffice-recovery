# Source Generated with Decompyle++
# File: list.marshal (Python 3.13)

import commctrl
import win32api
import win32con
import win32ui
from pywin.mfc import dialog

def ListDialog():
    '''ListDialog'''
    __firstlineno__ = 8
    
    def __init__(self, title, list):
        dialog.Dialog.__init__(self, self._maketemplate(title))
        self.HookMessage(self.on_size, win32con.WM_SIZE)
        self.HookNotify(self.OnListItemChange, commctrl.LVN_ITEMCHANGED)
        self.HookCommand(self.OnListClick, win32ui.IDC_LIST1)
        self.items = list

    
    def _maketemplate(self, title):
        style = win32con.WS_DLGFRAME | win32con.WS_SYSMENU | win32con.WS_VISIBLE
        ls = win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.LVS_ALIGNLEFT | commctrl.LVS_REPORT
        bs = win32con.WS_CHILD | win32con.WS_VISIBLE
        return [
            [
                title,
                (0, 0, 200, 200),
                style,
                None,
                (8, 'MS Sans Serif')],
            [
                'SysListView32',
                None,
                win32ui.IDC_LIST1,
                (0, 0, 200, 200),
                ls],
            [
                128,
                'OK',
                win32con.IDOK,
                (10, 0, 50, 14),
                bs | win32con.BS_DEFPUSHBUTTON],
            [
                128,
                'Cancel',
                win32con.IDCANCEL,
                (0, 0, 50, 14),
                bs]]

    
    def FillList(self):
        size = self.GetWindowRect()
        width = size[2] - size[0] - 10
        itemDetails = (commctrl.LVCFMT_LEFT, width, 'Item', 0)
        self.itemsControl.InsertColumn(0, itemDetails)
        index = 0
        for item in self.items:
            index = self.itemsControl.InsertItem(index + 1, str(item), 0)

    
    def OnListClick(self, id, code):
        if code == commctrl.NM_DBLCLK:
            pass
        self.EndDialog(win32con.IDOK)
        return 1

    
    def OnListItemChange(self, std, extra):
        if (code,):
            (itemNotify, sub, newState, oldState, change, point, lparam) = (code,)
            oldSel = oldState & commctrl.LVIS_SELECTED != 0
        newSel = newState & commctrl.LVIS_SELECTED != 0
        if oldSel != newSel:
            
            try:
                self.selecteditem = itemNotify
                self.butOK.EnableWindow(1)
            except win32ui.error:
                
                self.selecteditem = None

            return None
            return None

    
    def OnInitDialog(self):
        rc = dialog.Dialog.OnInitDialog(self)
        self.itemsControl = self.GetDlgItem(win32ui.IDC_LIST1)
        self.butOK = self.GetDlgItem(win32con.IDOK)
        self.butCancel = self.GetDlgItem(win32con.IDCANCEL)
        self.FillList()
        size = self.GetWindowRect()
        self.LayoutControls(size[2] - size[0], size[3] - size[1])
        self.butOK.EnableWindow(0)
        return rc

    
    def LayoutControls(self, w, h):
        self.itemsControl.MoveWindow((0, 0, w, h - 30))
        self.butCancel.MoveWindow((10, h - 24, 60, h - 4))
        self.butOK.MoveWindow((w - 60, h - 24, w - 10, h - 4))

    
    def on_size(self, params):
        lparam = params[3]
        w = None(lparam)
        h = None(lparam)
        self.LayoutControls(w, h)

    __static_attributes__ = ('butCancel', 'butOK', 'items', 'itemsControl', 'selecteditem')

ListDialog = None(ListDialog, 'ListDialog', dialog.Dialog)

def ListsDialog():
    '''ListsDialog'''
    __firstlineno__ = 93
    if (lambda self, title, list, colHeadings: ListDialog.__init__(self, title, list)self.colHeadings = colHeadings):
        
        def __init__(self, title, list, colHeadings):
            ListDialog.__init__(self, title, list)
            self.colHeadings = colHeadings

    
    def FillList(self):
        index = 0
        size = self.GetWindowRect()
        width = win32api.GetSystemMetrics - None(win32con.SM_CXVSCROLL)
        numCols = len(self.colHeadings)
        for col in self.colHeadings:
            itemDetails = (commctrl.LVCFMT_LEFT, int(width / numCols), col, 0)
            self.itemsControl.InsertColumn(index, itemDetails)
            index += 1
        index = 0
        for items in self.items:
            index = self.itemsControl.InsertItem(index + 1, str(items[0]), 0)
            for itemno in range(1, numCols):
                item = items[itemno]
                self.itemsControl.SetItemText(index, itemno, str(item))

    __static_attributes__ = ('colHeadings',)

ListsDialog = None(ListsDialog, 'ListsDialog', ListDialog)

def SelectFromList(title, lst):
    dlg = ListDialog(title, lst)
    if dlg.DoModal() == win32con.IDOK:
        pass
    return dlg.selecteditem


def SelectFromLists(title, lists, headings):
    dlg = ListsDialog(title, lists, headings)
    if dlg.DoModal() == win32con.IDOK:
        pass
    return dlg.selecteditem


def test():
    print(SelectFromLists('Multi-List', [
        ('1', 1, 'a'),
        ('2', 2, 'b'),
        ('3', 3, 'c')], [
        'Col 1',
        'Col 2']))

if __name__ == '__main__':
    <NODE:12>
return None
