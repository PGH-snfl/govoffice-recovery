# Source Generated with Decompyle++
# File: errors.marshal (Python 3.13)

'''email package exception classes.'''

def MessageError():
    '''MessageError'''
    __firstlineno__ = 8
    __doc__ = 'Base class for errors in the email package.'
    __static_attributes__ = ()

MessageError = None(MessageError, 'MessageError', Exception)

def MessageParseError():
    '''MessageParseError'''
    __firstlineno__ = 12
    __doc__ = 'Base class for message parsing errors.'
    __static_attributes__ = ()

MessageParseError = None(MessageParseError, 'MessageParseError', MessageError)

def HeaderParseError():
    '''HeaderParseError'''
    __firstlineno__ = 16
    __doc__ = 'Error while parsing headers.'
    __static_attributes__ = ()

HeaderParseError = None(HeaderParseError, 'HeaderParseError', MessageParseError)

def BoundaryError():
    '''BoundaryError'''
    __firstlineno__ = 20
    __doc__ = "Couldn't find terminating boundary."
    __static_attributes__ = ()

BoundaryError = None(BoundaryError, 'BoundaryError', MessageParseError)

def MultipartConversionError():
    '''MultipartConversionError'''
    __firstlineno__ = 24
    __doc__ = 'Conversion to a multipart is prohibited.'
    __static_attributes__ = ()

MultipartConversionError = None(MultipartConversionError, 'MultipartConversionError', MessageError, TypeError)

def CharsetError():
    '''CharsetError'''
    __firstlineno__ = 28
    __doc__ = 'An illegal charset was given.'
    __static_attributes__ = ()

CharsetError = None(CharsetError, 'CharsetError', MessageError)

def HeaderWriteError():
    '''HeaderWriteError'''
    __firstlineno__ = 32
    __doc__ = 'Error while writing headers.'
    __static_attributes__ = ()

HeaderWriteError = None(HeaderWriteError, 'HeaderWriteError', MessageError)

def MessageDefect():
