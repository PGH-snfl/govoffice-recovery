# Source Generated with Decompyle++
# File: simpledialog.marshal (Python 3.13)

'''This modules handles dialog boxes.

It contains the following public symbols:

SimpleDialog -- A simple but flexible modal dialog box

Dialog -- a base class for dialogs

askinteger -- get an integer from the user

askfloat -- get a float from the user

askstring -- get a string from the user
'''
None(import tkinter)
from tkinter import _get_temp_root, _destroy_temp_root
from tkinter import messagebox

def SimpleDialog():
    '''SimpleDialog'''
    __firstlineno__ = 31
    if (lambda self, master, text, buttons, default, cancel, title, class_: if class_:
passif title:
passif title:
self.root.title(title)self.root.iconname(title)_setup_dialog(self.root)self.message = Message(self.root, text = text, aspect = 400)self.message.pack(expand = 1, fill = BOTH)self.frame = Frame(self.root)self.frame.pack()self.num = defaultself.cancel = cancelself.default = defaultself.root.bind('<Return>', self.return_event)for num in range(len(buttons)):
s = buttons[num]if (lambda self, num: self.done(num)):
                pass
            b = self.frame(s, text = (self, num), command = (lambda self, num: self.done(num)))
            if num == default:
                pass
            b.config(relief = RIDGE, borderwidth = 8)
            b.pack(side = LEFT, fill = BOTH, expand = 1)
        self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self.root.transient(master)
        _place_window(self.root, master)
):
        
        def __init__(self, master, text, buttons, default, cancel, title, class_):
            if class_:
                pass
            if title:
                pass
            if title:
                self.root.title(title)
            self.root.iconname(title)
            _setup_dialog(self.root)
            self.message = Message(self.root, text = text, aspect = 400)
            self.message.pack(expand = 1, fill = BOTH)
            self.frame = Frame(self.root)
            self.frame.pack()
            self.num = default
            self.cancel = cancel
            self.default = default
            self.root.bind('<Return>', self.return_event)
            for num in range(len(buttons)):
                s = buttons[num]
                if (lambda self, num: self.done(num)):
                    pass
                b = self.frame(s, text = (self, num), command = (lambda self, num: self.done(num)))
                if num == default:
                    pass
                b.config(relief = RIDGE, borderwidth = 8)
                b.pack(side = LEFT, fill = BOTH, expand = 1)
            self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
            self.root.transient(master)
            _place_window(self.root, master)

    
    def go(self):
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.mainloop()
        self.root.destroy()
        return self.num

    
    def return_event(self, event):
        if self.default:
            pass
        return None
        self.done(self.default)

    
    def wm_delete_window(self):
        if self.cancel:
            pass
        return None
        self.done(self.cancel)

    
    def done(self, num):
        self.num = num
        self.root.quit()

    __static_attributes__ = ('cancel', 'default', 'frame', 'message', 'num', 'root')

SimpleDialog = None(SimpleDialog, 'SimpleDialog')

def Dialog():
    '''Dialog'''
    __firstlineno__ = 89
    __doc__ = 'Class to open dialogs.\n\nThis class is intended as a base class for custom dialogs\n'
    if (lambda self, parent, title: master = parentif master:
passmaster = _get_temp_root()Toplevel.__init__(self, master)self.withdraw()if parent:
if parent.winfo_viewable():
passif parent.winfo_viewable():
passself.transient(parent)if title:
passif title:
passself.title(title)_setup_dialog(self)self.parent = parentself.result = Nonebody = Frame(self)self.initial_focus = self.body(body)body.pack(padx = 5, pady = 5)self.buttonbox()if self.initial_focus:
self.initial_focus = selfself.protocol('WM_DELETE_WINDOW', self.cancel)_place_window(self, parent)self.initial_focus.focus_set()self.wait_visibility()self.grab_set()self.wait_window(self)):
        
        def __init__(self, parent, title):
            '''Initialize a dialog.

Arguments:

    parent -- a parent window (the application window)

    title -- the dialog title
'''
            master = parent
            if master:
                pass
            master = _get_temp_root()
            Toplevel.__init__(self, master)
            self.withdraw()
            if parent:
                if parent.winfo_viewable():
                    pass
                if parent.winfo_viewable():
                    pass
            self.transient(parent)
            if title:
                pass
            if title:
                pass
            self.title(title)
            _setup_dialog(self)
            self.parent = parent
            self.result = None
            body = Frame(self)
            self.initial_focus = self.body(body)
            body.pack(padx = 5, pady = 5)
            self.buttonbox()
            if self.initial_focus:
                self.initial_focus = self
            self.protocol('WM_DELETE_WINDOW', self.cancel)
            _place_window(self, parent)
            self.initial_focus.focus_set()
            self.wait_visibility()
            self.grab_set()
            self.wait_window(self)

    
    def destroy(self):
        '''Destroy the window'''
        self.initial_focus = None
        Toplevel.destroy(self)
        _destroy_temp_root(self.master)

    
    def body(self, master):
        '''create dialog body.

return widget that should have initial focus.
This method should be overridden, and is called
by the __init__ method.
'''
        pass

    
    def buttonbox(self):
        '''add standard button box.

override if you do not want the standard buttons
'''
        box = Frame(self)
        w = Button(box, text = 'OK', width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = 'Cancel', width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)
        box.pack()

    if (lambda self, event: if self.validate():
passif not self.validate():
self.initial_focus.focus_set()Noneself.withdraw()self.update_idletasks()try:
self.apply()except:
passself.cancel()):
        
        def ok(self, event):
            if self.validate():
                pass
            if not self.validate():
                self.initial_focus.focus_set()
            return None
            self.withdraw()
            self.update_idletasks()
            
            try:
                self.apply()
            except:
                pass

            self.cancel()

    if (lambda self, event: if self.parent:
passself.parent.focus_set()self.destroy()):
        
        def cancel(self, event):
            if self.parent:
                pass
            self.parent.focus_set()
            self.destroy()

    
    def validate(self):
        '''validate the data

This method is called automatically to validate the data before the
dialog is destroyed. By default, it always validates OK.
'''
        return 1

    
    def apply(self):
        '''process the data

This method is called automatically to process the data, *after*
the dialog is destroyed. By default, it does nothing.
'''
        pass

    __static_attributes__ = ('initial_focus', 'parent', 'result')

Dialog = None(Dialog, 'Dialog', Toplevel)
if (lambda w, parent: w.wm_withdraw()w.update_idletasks()minwidth = w.winfo_reqwidth()minheight = w.winfo_reqheight()maxwidth = w.winfo_vrootwidth()maxheight = w.winfo_vrootheight()if parent:
if parent.winfo_ismapped():
passw.wm_maxsize(maxwidth, maxheight)w.wm_geometry('+%d+%d' % (x, y))w.wm_deiconify()):
    
    def _place_window(w, parent):
        w.wm_withdraw()
        w.update_idletasks()
        minwidth = w.winfo_reqwidth()
        minheight = w.winfo_reqheight()
        maxwidth = w.winfo_vrootwidth()
        maxheight = w.winfo_vrootheight()
        if parent:
            if parent.winfo_ismapped():
                pass
        w.wm_maxsize(maxwidth, maxheight)
        w.wm_geometry('+%d+%d' % (x, y))
        w.wm_deiconify()


def _setup_dialog(w):
    if w._windowingsystem == 'aqua':
        w.tk.call('::tk::unsupported::MacWindowStyle', 'style', w, 'moveableModal', '')
    return None
    if w._windowingsystem == 'x11':
        w.wm_attributes(type = 'dialog')
    return None


def _QueryDialog():
    '''_QueryDialog'''
    __firstlineno__ = 270
    if (lambda self, title, prompt, initialvalue, minvalue, maxvalue, parent: self.prompt = promptself.minvalue = minvalueself.maxvalue = maxvalueself.initialvalue = initialvalueDialog.__init__(self, parent, title)):
        
        def __init__(self, title, prompt, initialvalue, minvalue, maxvalue, parent):
            self.prompt = prompt
            self.minvalue = minvalue
            self.maxvalue = maxvalue
            self.initialvalue = initialvalue
            Dialog.__init__(self, parent, title)

    
    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    
    def body(self, master):
        w = Label(master, text = self.prompt, justify = LEFT)
        w.grid(row = 0, padx = 5, sticky = W)
        self.entry = Entry(master, name = 'entry')
        self.entry.grid(row = 1, padx = 5, sticky = W + E)
        if self.initialvalue:
            pass
        self.entry.select_range(0, END)
        return self.entry

    
    def validate(self):
        
        try:
            result = self.getresult()
        except ValueError:
            messagebox.showwarning
            None('Illegal value', self.errormessage + '\nPlease try again', parent = self)

        if self.minvalue and result < self.minvalue:
            None('Too small', 'The allowed minimum value is %s. Please try again.' % self.minvalue, parent = self)
        return 0
        if self.maxvalue and result > self.maxvalue:
            None('Too large', 'The allowed maximum value is %s. Please try again.' % self.maxvalue, parent = self)
        return 0
        self.result = result
        return 1

    __static_attributes__ = ('entry', 'initialvalue', 'maxvalue', 'minvalue', 'prompt', 'result')

_QueryDialog = None(_QueryDialog, '_QueryDialog', Dialog)

def _QueryInteger():
    '''_QueryInteger'''
    __firstlineno__ = 337
    errormessage = 'Not an integer.'
    
    def getresult(self):
        return self.getint(self.entry.get())

    __static_attributes__ = ()

_QueryInteger = None(_QueryInteger, '_QueryInteger', _QueryDialog)

def askinteger(title, prompt, **kw):
    '''get an integer from the user

Arguments:

    title -- the dialog title
    prompt -- the label text
    **kw -- see SimpleDialog class

Return value is an integer
'''
    d = (title, prompt)({ }, kw = None)
    return d.result


def _QueryFloat():
    '''_QueryFloat'''
    __firstlineno__ = 359
    errormessage = 'Not a floating-point value.'
    
    def getresult(self):
        return self.getdouble(self.entry.get())

    __static_attributes__ = ()

_QueryFloat = None(_QueryFloat, '_QueryFloat', _QueryDialog)

def askfloat(title, prompt, **kw):
    '''get a float from the user

Arguments:

    title -- the dialog title
    prompt -- the label text
    **kw -- see SimpleDialog class

Return value is a float
'''
    d = (title, prompt)({ }, kw = None)
    return d.result


def _QueryString():
    '''_QueryString'''
    __firstlineno__ = 381
    
    def __init__(self, *args, **kw):
        if 'show' in kw:
            self._QueryString__show = kw['show']
            del kw['show']
        else:
            self._QueryString__show = None
        None(None)({ }, kw = None)

    
    def body(self, master):
        entry = _QueryDialog.body(self, master)
        if self._QueryString__show:
            pass
        entry.configure(show = self._QueryString__show)
        return entry

    
    def getresult(self):
        return self.entry.get()

    __static_attributes__ = ('__show',)

_QueryString = None(_QueryString, '_QueryString', _QueryDialog)

def askstring(title, prompt, **kw):
    '''get a string from the user

Arguments:

    title -- the dialog title
    prompt -- the label text
    **kw -- see SimpleDialog class

Return value is a string
'''
    d = (title, prompt)({ }, kw = None)
    return d.result

if __name__ == '__main__':
    
    def test():
        root = Tk()
        if (lambda root: d = SimpleDialog(root, text = 'This is a test dialog.  Would this have been an actual dialog, the buttons below would have been glowing in soft pink light.\nDo you believe this?', buttons = [
'Yes',
'No',
'Cancel'], default = 0, cancel = 2, title = 'Test Dialog')print(d.go())None(askinteger('Spam', 'Egg count', initialvalue = 144))None(askfloat('Spam', 'Egg weight\n(in tons)', minvalue = 1, maxvalue = 100))print(askstring('Spam', 'Egg label'))):
            
            def doit(root):
                d = SimpleDialog(root, text = 'This is a test dialog.  Would this have been an actual dialog, the buttons below would have been glowing in soft pink light.\nDo you believe this?', buttons = [
                    'Yes',
                    'No',
                    'Cancel'], default = 0, cancel = 2, title = 'Test Dialog')
                print(d.go())
                None(askinteger('Spam', 'Egg count', initialvalue = 144))
                None(askfloat('Spam', 'Egg weight\n(in tons)', minvalue = 1, maxvalue = 100))
                print(askstring('Spam', 'Egg label'))

        t = Button(root, text = 'Test', command = doit)
        t.pack()
        q = Button(root, text = 'Quit', command = t.quit)
        q.pack()
        t.mainloop()

    <NODE:12>
return None
