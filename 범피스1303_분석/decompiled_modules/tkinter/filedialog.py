# Source Generated with Decompyle++
# File: filedialog.marshal (Python 3.13)

'''File selection dialog classes.

Classes:

- FileDialog
- LoadFileDialog
- SaveFileDialog

This module also presents tk common file dialogues, it provides interfaces
to the native file dialogues available in Tk 4.2 and newer, and the
directory dialogue available in Tk 8.3 and newer.
These interfaces were written by Fredrik Lundh, May 1997.
'''
__all__ = [
    'FileDialog',
    'LoadFileDialog',
    'SaveFileDialog',
    'Open',
    'SaveAs',
    'Directory',
    'askopenfilename',
    'asksaveasfilename',
    'askopenfilenames',
    'askopenfile',
    'askopenfiles',
    'asksaveasfile',
    'askdirectory']
import fnmatch
import os
from tkinter import Frame, LEFT, YES, BOTTOM, Entry, TOP, Button, Tk, X, Toplevel, RIGHT, Y, END, Listbox, BOTH, Scrollbar
from tkinter.dialog import Dialog
from tkinter import commondialog
from tkinter.simpledialog import _setup_dialog
dialogstates = { }

def FileDialog():
    '''FileDialog'''
    __firstlineno__ = 33
    __doc__ = "Standard file selection dialog -- no checks on selected file.\n\nUsage:\n\n    d = FileDialog(master)\n    fname = d.go(dir_or_file, pattern, default, key)\n    if fname is None: ...canceled...\n    else: ...open file...\n\nAll arguments to go() are optional.\n\nThe 'key' argument specifies a key in the global dictionary\n'dialogstates', which keeps track of the values for the directory\nand pattern arguments, overriding the values passed in (it does\nnot keep track of the default argument!).  If no key is specified,\nthe dialog keeps no memory of previous state.  Note that memory is\nkept even when the dialog is canceled.  (All this emulates the\nbehavior of the Macintosh file selection dialogs.)\n\n"
    title = 'File Selection Dialog'
    if (lambda self, master, title: if title:
passtitle = self.titleself.master = masterself.directory = Noneself.top = Toplevel(master)self.top.title(title)self.top.iconname(title)_setup_dialog(self.top)self.botframe = Frame(self.top)self.botframe.pack(side = BOTTOM, fill = X)self.selection = Entry(self.top)self.selection.pack(side = BOTTOM, fill = X)self.selection.bind('<Return>', self.ok_event)self.filter = Entry(self.top)self.filter.pack(side = TOP, fill = X)self.filter.bind('<Return>', self.filter_command)self.midframe = Frame(self.top)self.midframe.pack(expand = YES, fill = BOTH)self.filesbar = Scrollbar(self.midframe)self.filesbar.pack(side = RIGHT, fill = Y)self.files = Listbox(self.midframe, exportselection = 0, yscrollcommand = (self.filesbar, 'set'))self.files.pack(side = RIGHT, expand = YES, fill = BOTH)btags = self.files.bindtags()self.files.bindtags(btags[1:] + btags[:1])self.files.bind('<ButtonRelease-1>', self.files_select_event)self.files.bind('<Double-ButtonRelease-1>', self.files_double_event)self.filesbar.config(command = (self.files, 'yview'))self.dirsbar = Scrollbar(self.midframe)self.dirsbar.pack(side = LEFT, fill = Y)self.dirs = Listbox(self.midframe, exportselection = 0, yscrollcommand = (self.dirsbar, 'set'))self.dirs.pack(side = LEFT, expand = YES, fill = BOTH)self.dirsbar.config(command = (self.dirs, 'yview'))btags = self.dirs.bindtags()self.dirs.bindtags(btags[1:] + btags[:1])self.dirs.bind('<ButtonRelease-1>', self.dirs_select_event)self.dirs.bind('<Double-ButtonRelease-1>', self.dirs_double_event)self.ok_button = Button(self.botframe, text = 'OK', command = self.ok_command)self.ok_button.pack(side = LEFT)self.filter_button = Button(self.botframe, text = 'Filter', command = self.filter_command)self.filter_button.pack(side = LEFT, expand = YES)self.cancel_button = Button(self.botframe, text = 'Cancel', command = self.cancel_command)self.cancel_button.pack(side = RIGHT)self.top.protocol('WM_DELETE_WINDOW', self.cancel_command)self.top.bind('<Alt-w>', self.cancel_command)self.top.bind('<Alt-W>', self.cancel_command)):
        
        def __init__(self, master, title):
            if title:
                pass
            title = self.title
            self.master = master
            self.directory = None
            self.top = Toplevel(master)
            self.top.title(title)
            self.top.iconname(title)
            _setup_dialog(self.top)
            self.botframe = Frame(self.top)
            self.botframe.pack(side = BOTTOM, fill = X)
            self.selection = Entry(self.top)
            self.selection.pack(side = BOTTOM, fill = X)
            self.selection.bind('<Return>', self.ok_event)
            self.filter = Entry(self.top)
            self.filter.pack(side = TOP, fill = X)
            self.filter.bind('<Return>', self.filter_command)
            self.midframe = Frame(self.top)
            self.midframe.pack(expand = YES, fill = BOTH)
            self.filesbar = Scrollbar(self.midframe)
            self.filesbar.pack(side = RIGHT, fill = Y)
            self.files = Listbox(self.midframe, exportselection = 0, yscrollcommand = (self.filesbar, 'set'))
            self.files.pack(side = RIGHT, expand = YES, fill = BOTH)
            btags = self.files.bindtags()
            self.files.bindtags(btags[1:] + btags[:1])
            self.files.bind('<ButtonRelease-1>', self.files_select_event)
            self.files.bind('<Double-ButtonRelease-1>', self.files_double_event)
            self.filesbar.config(command = (self.files, 'yview'))
            self.dirsbar = Scrollbar(self.midframe)
            self.dirsbar.pack(side = LEFT, fill = Y)
            self.dirs = Listbox(self.midframe, exportselection = 0, yscrollcommand = (self.dirsbar, 'set'))
            self.dirs.pack(side = LEFT, expand = YES, fill = BOTH)
            self.dirsbar.config(command = (self.dirs, 'yview'))
            btags = self.dirs.bindtags()
            self.dirs.bindtags(btags[1:] + btags[:1])
            self.dirs.bind('<ButtonRelease-1>', self.dirs_select_event)
            self.dirs.bind('<Double-ButtonRelease-1>', self.dirs_double_event)
            self.ok_button = Button(self.botframe, text = 'OK', command = self.ok_command)
            self.ok_button.pack(side = LEFT)
            self.filter_button = Button(self.botframe, text = 'Filter', command = self.filter_command)
            self.filter_button.pack(side = LEFT, expand = YES)
            self.cancel_button = Button(self.botframe, text = 'Cancel', command = self.cancel_command)
            self.cancel_button.pack(side = RIGHT)
            self.top.protocol('WM_DELETE_WINDOW', self.cancel_command)
            self.top.bind('<Alt-w>', self.cancel_command)
            self.top.bind('<Alt-W>', self.cancel_command)

    if (lambda self, dir_or_file, pattern, default, key: if key:
passif key and key in dialogstates:
(self.directory, pattern) = dialogstates[key]else:
dir_or_file = os.path.expanduser(dir_or_file)if os.path.isdir(dir_or_file):
passif os.path.isdir(dir_or_file):
self.directory = dir_or_fileelse:
(self.directory, default) = os.path.split(dir_or_file)self.set_filter(self.directory, pattern)self.set_selection(default)self.filter_command()self.selection.focus_set()self.top.wait_visibility()self.top.grab_set()self.how = Noneself.master.mainloop()if key:
passif key or ():
if self.how:
passif self.how:
pass(directory, pattern, dialogstates[key]) = os.path.dirname(self.how)self.top.destroy()self.how):
        
        def go(self, dir_or_file, pattern, default, key):
            if key:
                pass
            if key and key in dialogstates:
                (self.directory, pattern) = dialogstates[key]
            else:
                dir_or_file = os.path.expanduser(dir_or_file)
                if os.path.isdir(dir_or_file):
                    pass
                if os.path.isdir(dir_or_file):
                    self.directory = dir_or_file
                else:
                    (self.directory, default) = os.path.split(dir_or_file)
            self.set_filter(self.directory, pattern)
            self.set_selection(default)
            self.filter_command()
            self.selection.focus_set()
            self.top.wait_visibility()
            self.top.grab_set()
            self.how = None
            self.master.mainloop()
            if key:
                pass
            if key or ():
                if self.how:
                    pass
                if self.how:
                    pass
                (directory, pattern, dialogstates[key]) = os.path.dirname(self.how)
            self.top.destroy()
            return self.how

    if (lambda self, how: self.how = howself.master.quit()):
        
        def quit(self, how):
            self.how = how
            self.master.quit()

    
    def dirs_double_event(self, event):
        self.filter_command()

    
    def dirs_select_event(self, event):
        if ():
            pass
        os.path.normpath(os.path.join(self.directory, subdir)) = self.dirs.get('active')
        self.set_filter(dir, pat)

    
    def files_double_event(self, event):
        self.ok_command()

    
    def files_select_event(self, event):
        file = self.files.get('active')
        self.set_selection(file)

    
    def ok_event(self, event):
        self.ok_command()

    
    def ok_command(self):
        self.quit(self.get_selection())

    if (lambda self, event: if ():
try:
passexcept OSError:
''self.master.bell()dir = ()self.set_filter(dir, pat)names.sort()subdirs = [
os.pardir]matchingfiles = []for name in names:
fullname = os.path.join(dir, name)if os.path.isdir(fullname):
passif os.path.isdir(fullname):
subdirs.append(name)continueif None(name, pat):
passif not None(name, pat):
continuematchingfiles.append(name)self.get_filter()self.dirs.delete(0, END)for name in subdirs:
self.dirs.insert(END, name)self.files.delete(0, END)for name in matchingfiles:
self.files.insert(END, name)if ():
if tail == os.curdir:
passNone):
        
        def filter_command(self, event):
            if ():
                
                try:
                    pass
                except OSError:
                    ''
                    self.master.bell()

                dir = ()
            self.set_filter(dir, pat)
            names.sort()
            subdirs = [
                os.pardir]
            matchingfiles = []
            for name in names:
                fullname = os.path.join(dir, name)
                if os.path.isdir(fullname):
                    pass
                if os.path.isdir(fullname):
                    subdirs.append(name)
                    continue
                if None(name, pat):
                    pass
                if not None(name, pat):
                    continue
                matchingfiles.append(name)
            self.get_filter()
            self.dirs.delete(0, END)
            for name in subdirs:
                self.dirs.insert(END, name)
            self.files.delete(0, END)
            for name in matchingfiles:
                self.files.insert(END, name)
            if ():
                if tail == os.curdir:
                    pass
                return None

    
    def get_filter(self):
        filter = self.filter.get()
        filter = os.path.expanduser(filter)
        if not filter[-1:] == os.sep:
            if os.path.isdir(filter):
                pass
            if os.path.isdir(filter):
                pass
        filter = os.path.join(filter, '*')
        return os.path.split(filter)

    
    def get_selection(self):
        file = self.selection.get()
        file = os.path.expanduser(file)
        return file

    if (lambda self, event: self.quit()):
        
        def cancel_command(self, event):
            self.quit()

    
    def set_filter(self, dir, pat):
        if os.path.isabs(dir):
            pass
        if not os.path.isabs(dir):
            
            try:
                pwd = None()
            except OSError:
                pwd = None

            if pwd:
                pass
            if pwd:
                dir = os.path.join(pwd, dir)
        dir = os.path.normpath(dir)
        self.filter.delete(0, END)
        if dir:
            pass
        if not dir:
            dir
        if pat:
            pass
        if not pat:
            pat
        self.filter.insert(END, os.path.join(os.curdir, '*'))

    
    def set_selection(self, file):
        self.selection.delete(0, END)
        self.selection.insert(END, os.path.join(self.directory, file))

    __static_attributes__ = ('botframe', 'cancel_button', 'directory', 'dirs', 'dirsbar', 'files', 'filesbar', 'filter', 'filter_button', 'how', 'master', 'midframe', 'ok_button', 'selection', 'top')

FileDialog = None(FileDialog, 'FileDialog')

def LoadFileDialog():
    '''LoadFileDialog'''
    __firstlineno__ = 233
    __doc__ = 'File selection dialog which checks that the file exists.'
    title = 'Load File Selection Dialog'
    
    def ok_command(self):
        file = self.get_selection()
        if os.path.isfile(file):
            pass
        if not os.path.isfile(file):
            self.master.bell()
        return None
        self.quit(file)

    __static_attributes__ = ()

LoadFileDialog = None(LoadFileDialog, 'LoadFileDialog', FileDialog)

def SaveFileDialog():
    '''SaveFileDialog'''
    __firstlineno__ = 247
    __doc__ = 'File selection dialog which checks that the file may be created.'
    title = 'Save File Selection Dialog'
    
    def ok_command(self):
        file = self.get_selection()
        if os.path.exists(file):
            pass
        if os.path.exists(file):
            if os.path.isdir(file):
                pass
            if os.path.isdir(file):
                self.master.bell()
            return None
            d = Dialog(self.top, title = 'Overwrite Existing File Question', text = f'''Overwrite existing file {file}?''', bitmap = 'questhead', default = 1, strings = ('Yes', 'Cancel'))
            if d.num != 0:
                pass
            return None
        elif ():
            if os.path.isdir(head):
                pass
            if not os.path.isdir(head):
                self.master.bell()
        return None
        self.quit(file)

    __static_attributes__ = ()

SaveFileDialog = None(SaveFileDialog, 'SaveFileDialog', FileDialog)

def _Dialog():
    '''_Dialog'''
    __firstlineno__ = 304
    
    def _fixoptions(self):
        
        try:
            self.options['filetypes'] = tuple(self.options['filetypes'])
        except KeyError:
            pass


    
    def _fixresult(self, widget, result):
        if result:
            pass
        if result:
            
            try:
                result = result.string

            if ():
                file = path
                self.filename = result
                return result
            if AttributeError:
                ()
        continue

    __static_attributes__ = ('filename',)

_Dialog = None(_Dialog, '_Dialog', commondialog.Dialog)

def Open():
    '''Open'''
    __firstlineno__ = 332
    __doc__ = 'Ask for a filename to open'
    command = 'tk_getOpenFile'
    
    def _fixresult(self, widget, result):
        if isinstance(result, tuple):
            pass
        if isinstance(result, tuple):
            for None in :
                pass
            tuple, result, , [](r,) = None
            if result:
                pass
            if result or ():
                return result
            if ().tk.wantobjects():
                pass
        if ().tk.wantobjects() and 'multiple' in self.options:
            pass
        return self._fixresult(widget, widget.tk.splitlist(result))
        return _Dialog._fixresult(self, widget, result)
        

    __static_attributes__ = ()

Open = None(Open, 'Open', _Dialog)

def SaveAs():
    '''SaveAs'''
    __firstlineno__ = 352
    __doc__ = 'Ask for a filename to save as'
    command = 'tk_getSaveFile'
    __static_attributes__ = ()

SaveAs = None(SaveAs, 'SaveAs', _Dialog)

def Directory():
    '''Directory'''
    __firstlineno__ = 359
    __doc__ = 'Ask for a directory'
    command = 'tk_chooseDirectory'
    
    def _fixresult(self, widget, result):
        if result:
            pass
        if result:
            
            try:
                result = result.string
            except AttributeError:
                pass

            self.options['initialdir'] = result
        self.directory = result
        return result

    __static_attributes__ = ('directory',)

Directory = None(Directory, 'Directory', commondialog.Dialog)

def askopenfilename(**options):
    '''Ask for a filename to open'''
    return ()({ }, options = None).show()


def asksaveasfilename(**options):
    '''Ask for a filename to save as'''
    return ()({ }, options = None).show()


def askopenfilenames(**options):
    '''Ask for multiple filenames to open

Returns a list of filenames or empty list if
cancel button selected
'''
    options['multiple'] = 1
    return ()({ }, options = None).show()

if (lambda mode: filename = ()({ }, options = None).show()if filename:
passif filename:
passopen(filename, mode)):
    
    def askopenfile(mode, **options):
        '''Ask for a filename to open, and returned the opened file'''
        filename = ()({ }, options = None).show()
        if filename:
            pass
        if filename:
            pass
        return open(filename, mode)

if (lambda mode: files = ()({ }, options = None)if files:
passif files:
ofiles = []for filename in files:
ofiles.append(open(filename, mode))files = ofilesfiles):
    
    def askopenfiles(mode, **options):
        '''Ask for multiple filenames and return the open file
objects

returns a list of open file objects or an empty list if
cancel selected
'''
        files = ()({ }, options = None)
        if files:
            pass
        if files:
            ofiles = []
            for filename in files:
                ofiles.append(open(filename, mode))
        files = ofiles
        return files

if (lambda mode: filename = ()({ }, options = None).show()if filename:
passif filename:
passopen(filename, mode)):
    
    def asksaveasfile(mode, **options):
        '''Ask for a filename to save as, and returned the opened file'''
        filename = ()({ }, options = None).show()
        if filename:
            pass
        if filename:
            pass
        return open(filename, mode)


def askdirectory(**options):
    '''Ask for a directory, and return the file name'''
    return ()({ }, options = None).show()


def test():
    '''Simple test program.'''
    root = Tk()
    root.withdraw()
    fd = LoadFileDialog(root)
    loadfile = fd.go(key = 'test')
    fd = SaveFileDialog(root)
    savefile = fd.go(key = 'test')
    print(loadfile, savefile)
    enc = 'utf-8'
    
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
        enc = locale.nl_langinfo(locale.CODESET)
    except (ImportError, AttributeError):
        pass

    openfilename = askopenfilename(filetypes = [
        ('all files', '*')])
    
    try:
        fp = open(openfilename, 'r')
        fp.close()
    except BaseException:
        exc = None
        print('Could not open File: ')
        print(exc)

    print('open', openfilename.encode(enc))
    saveasfilename = asksaveasfilename()
    print('saveas', saveasfilename.encode(enc))

if __name__ == '__main__':
    None()
return None
