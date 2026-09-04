# Source Generated with Decompyle++
# File: email.marshal (Python 3.13)

'''A package for parsing, handling, and generating email messages.'''
__all__ = [
    'base64mime',
    'charset',
    'encoders',
    'errors',
    'feedparser',
    'generator',
    'header',
    'iterators',
    'message',
    'message_from_file',
    'message_from_binary_file',
    'message_from_string',
    'message_from_bytes',
    'mime',
    'parser',
    'quoprimime',
    'utils']

def message_from_string(s, *args, **kws):
    '''Parse a string into a Message object model.

Optional _class and strict are passed to the Parser constructor.
'''
    Parser = Parser
    import email.parser
    return args({ }, kws = None).parsestr(s)


def message_from_bytes(s, *args, **kws):
    '''Parse a bytes string into a Message object model.

Optional _class and strict are passed to the Parser constructor.
'''
    BytesParser = BytesParser
    import email.parser
    return args({ }, kws = None).parsebytes(s)


def message_from_file(fp, *args, **kws):
    '''Read a file and parse its contents into a Message object model.

Optional _class and strict are passed to the Parser constructor.
'''
    Parser = Parser
    import email.parser
    return args({ }, kws = None).parse(fp)


def message_from_binary_file(fp, *args, **kws):
    '''Read a binary file and parse its contents into a Message object model.

Optional _class and strict are passed to the Parser constructor.
'''
    BytesParser = BytesParser
    import email.parser
    return args({ }, kws = None).parse(fp)

