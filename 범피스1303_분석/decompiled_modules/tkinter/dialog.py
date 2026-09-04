# Source Generated with Decompyle++
# File: dialog.marshal (Python 3.13)

from tkinter import _cnfmerge, Widget, TclError, Button, Pack
__all__ = [
    'Dialog']
DIALOG_ICON = 'questhead'

def Dialog():
    '''Dialog'''
    __firstlineno__ = 10
    if (lambda self, master, cnf: cnf = _cnfmerge((cnf, kw))self.widgetName = '__dialog__'self._setup(master, cnf)self.num = self.tk.getint(self.tk.call(None(None)))try:
None(self)except TclError:
pass):
        
        def __init__(self, master, cnf, **kw):
            cnf = _cnfmerge((cnf, kw))
            self.widgetName = '__dialog__'
            self._setup(master, cnf)
            self.num = self.tk.getint(self.tk.call(None(None)))
            
            try:
                None(self)
            except TclError:
                pass


    
    def destroy(self):
        pass

    __static_attributes__ = ('num', 'widgetName')

Dialog = None(Dialog, 'Dialog', Widget)

def _test():
    d = Dialog(None, {
        'title': 'File Modified',
        'text': 'File "Python.h" has been modified since the last time it was saved. Do you want to save it before exiting the application.',
        'bitmap': DIALOG_ICON,
        'default': 0,
        'strings': ('Save File', 'Discard Changes', 'Return to Editor') })
    print(d.num)

if __name__ == '__main__':
    t = None(None, {
        Pack: { },
        'command': _test,
        'text': 'Test' })
    q = None(None, {
        Pack: { },
        'command': t.quit,
        'text': 'Quit' })
    t.mainloop()
return None
