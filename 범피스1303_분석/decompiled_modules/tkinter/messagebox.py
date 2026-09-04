# Source Generated with Decompyle++
# File: messagebox.marshal (Python 3.13)

from tkinter.commondialog import Dialog
__all__ = [
    'showinfo',
    'showwarning',
    'showerror',
    'askquestion',
    'askokcancel',
    'askyesno',
    'askyesnocancel',
    'askretrycancel']
ERROR = 'error'
INFO = 'info'
QUESTION = 'question'
WARNING = 'warning'
ABORTRETRYIGNORE = 'abortretryignore'
OK = 'ok'
OKCANCEL = 'okcancel'
RETRYCANCEL = 'retrycancel'
YESNO = 'yesno'
YESNOCANCEL = 'yesnocancel'
ABORT = 'abort'
RETRY = 'retry'
IGNORE = 'ignore'
OK = 'ok'
CANCEL = 'cancel'
YES = 'yes'
NO = 'no'

def Message():
    '''Message'''
    __firstlineno__ = 61
    __doc__ = 'A message box'
    command = 'tk_messageBox'
    __static_attributes__ = ()

Message = None(Message, 'Message', Dialog)
if (lambda title, message, _icon, _type: if _icon:
passif _icon and 'icon' not in options:
options['icon'] = _iconif _type:
passif _type and 'type' not in options:
options['type'] = _typeif title:
passif title:
options['title'] = titleif message:
passif message:
options['message'] = messageres = ()({ }, options = None).show()if isinstance(res, bool):
passif isinstance(res, bool):
if res:
passif res:
passYESMessagestr(res)):
    
    def _show(title, message, _icon, _type, **options):
        if _icon:
            pass
        if _icon and 'icon' not in options:
            options['icon'] = _icon
        if _type:
            pass
        if _type and 'type' not in options:
            options['type'] = _type
        if title:
            pass
        if title:
            options['title'] = title
        if message:
            pass
        if message:
            options['message'] = message
        res = ()({ }, options = None).show()
        if isinstance(res, bool):
            pass
        if isinstance(res, bool):
            if res:
                pass
            if res:
                pass
            return YES
        return Message
        return str(res)

if (lambda title, message: (title, message, INFO, OK)({ }, options = None)):
    
    def showinfo(title, message, **options):
        '''Show an info message'''
        return (title, message, INFO, OK)({ }, options = None)

if (lambda title, message: (title, message, WARNING, OK)({ }, options = None)):
    
    def showwarning(title, message, **options):
        '''Show a warning message'''
        return (title, message, WARNING, OK)({ }, options = None)

if (lambda title, message: (title, message, ERROR, OK)({ }, options = None)):
    
    def showerror(title, message, **options):
        '''Show an error message'''
        return (title, message, ERROR, OK)({ }, options = None)

if (lambda title, message: (title, message, QUESTION, YESNO)({ }, options = None)):
    
    def askquestion(title, message, **options):
        '''Ask a question'''
        return (title, message, QUESTION, YESNO)({ }, options = None)

if (lambda title, message: s = (title, message, QUESTION, OKCANCEL)({ }, options = None)s == OK):
    
    def askokcancel(title, message, **options):
        '''Ask if operation should proceed; return true if the answer is ok'''
        s = (title, message, QUESTION, OKCANCEL)({ }, options = None)
        return s == OK

if (lambda title, message: s = (title, message, QUESTION, YESNO)({ }, options = None)s == YES):
    
    def askyesno(title, message, **options):
        '''Ask a question; return true if the answer is yes'''
        s = (title, message, QUESTION, YESNO)({ }, options = None)
        return s == YES

if (lambda title, message: s = (title, message, QUESTION, YESNOCANCEL)({ }, options = None)s = str(s)if s == CANCEL:
passNones == YES):
    
    def askyesnocancel(title, message, **options):
        '''Ask a question; return true if the answer is yes, None if cancelled.'''
        s = (title, message, QUESTION, YESNOCANCEL)({ }, options = None)
        s = str(s)
        if s == CANCEL:
            pass
        return None
        return s == YES

if (lambda title, message: s = (title, message, WARNING, RETRYCANCEL)({ }, options = None)s == RETRY):
    
    def askretrycancel(title, message, **options):
        '''Ask if operation should be retried; return true if the answer is yes'''
        s = (title, message, WARNING, RETRYCANCEL)({ }, options = None)
        return s == RETRY

if __name__ == '__main__':
    'info'(showinfo, None('Spam', 'Egg Information'))
    'warning'(showwarning, None('Spam', 'Egg Warning'))
    'error'(showerror, None('Spam', 'Egg Alert'))
    'question'(askquestion, None('Spam', 'Question?'))
    'proceed'(askokcancel, None('Spam', 'Proceed?'))
    'yes/no'(askyesno, None('Spam', 'Got it?'))
    'yes/no/cancel'(askyesnocancel, None('Spam', 'Want it?'))
    'try again'(askretrycancel, None('Spam', 'Try again?'))
return None
