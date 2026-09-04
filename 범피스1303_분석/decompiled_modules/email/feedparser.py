# Source Generated with Decompyle++
# File: feedparser.marshal (Python 3.13)

"""FeedParser - An email feed parser.

The feed parser implements an interface for incrementally parsing an email
message, line by line.  This has advantages for certain applications, such as
those reading email messages off a socket.

FeedParser.feed() is the primary interface for pushing new data into the
parser.  It returns when there's nothing more it can do with the available
data.  When you have no more data to push into the parser, call .close().
This completes the parsing and returns the root message object.

The other advantage of this parser is that it will never raise a parsing
exception.  Instead, when it finds something unexpected, it adds a 'defect' to
the current message.  Defects are just instances that live on the message
object's .defects attribute.
"""
__all__ = [
    'FeedParser',
    'BytesFeedParser']
import re
from email import errors
from email._policybase import compat32
from collections import deque
from io import StringIO
NLCRE = None('\\r\\n|\\r|\\n')
NLCRE_bol = None('(\\r\\n|\\r|\\n)')
NLCRE_eol = None('(\\r\\n|\\r|\\n)\\Z')
NLCRE_crack = None('(\\r\\n|\\r|\\n)')
headerRE = None('^(From |[\\041-\\071\\073-\\176]*:|[\\t ])')
EMPTYSTRING = ''
NL = '\n'
boundaryendRE = None('(?P<end>--)?(?P<ws>[ \\t]*)(?P<linesep>\\r\\n|\\r|\\n)?$')
NeedMoreData = None()

def BufferedSubFile():
    '''BufferedSubFile'''
    __firstlineno__ = 46
    __doc__ = 'A file-ish object that can have new data loaded into it.\n\nYou can also push and pop line-matching predicates onto a stack.  When the\ncurrent predicate matches the current line, a false EOF response\n(i.e. empty string) is returned instead.  This lets the parser adhere to a\nsimple abstraction -- it parses until EOF closes the current message.\n'
    
    def __init__(self):
        self._partial = StringIO(newline = '')
        self._lines = deque()
        self._eofstack = []
        self._closed = False

    
    def push_eof_matcher(self, pred):
        self._eofstack.append(pred)

    
    def pop_eof_matcher(self):
        return self._eofstack.pop()

    
    def close(self):
        self._partial.seek(0)
        self.pushlines(self._partial.readlines())
        self._partial.seek(0)
        self._partial.truncate()
        self._closed = True

    
    def readline(self):
        if self._lines:
            pass
        if not self._lines:
            if self._closed:
                pass
            if self._closed:
                pass
            return ''
        return NeedMoreData
        line = self._lines.popleft()
        for ateof in reversed(self._eofstack):
            if None(line):
                pass
            if not None(line):
                continue
            self._lines.appendleft(line)
            ateof
            return ''
        return line

    
    def unreadline(self, line):
        if not line is not NeedMoreData:
            pass
        raise None
        self._lines.appendleft(line)

    
    def push(self, data):
        '''Push some new data into this object.'''
        self._partial.write(data)
        if '\n' not in data and '\r' not in data:
            pass
        return None
        self._partial.seek(0)
        parts = self._partial.readlines()
        self._partial.seek(0)
        self._partial.truncate()
        if parts[-1].endswith('\n'):
            pass
        if not parts[-1].endswith('\n'):
            pass
        self._partial.write(parts.pop())
        self.pushlines(parts)

    
    def pushlines(self, lines):
        self._lines.extend(lines)

    
    def __iter__(self):
        return self

    
    def __next__(self):
        line = self.readline()
        if line == '':
            pass
        raise StopIteration
        return line

    __static_attributes__ = ('_closed', '_eofstack', '_lines', '_partial')

BufferedSubFile = None(BufferedSubFile, 'BufferedSubFile', object)

def FeedParser():
    '''FeedParser'''
    __firstlineno__ = 136
    __doc__ = 'A feed-style parser of email.'
    if (lambda self, _factory, *, policy, Message = lines: self.policy = policyself._old_style_factory = Falseif _factory:
if policy.message_factory:
Message = Messageself._factory = Messageelse:
self._factory = policy.message_factoryelse:
self._factory = _factorytry:
None(policy = self.policy)except TypeError:
policy.message_factoryself._old_style_factory = Trueself._input = BufferedSubFile()self._msgstack = []self._parse = self._parsegen().__next__self._cur = Noneself._last = Noneself._headersonly = FalseNone) and (lambda self, _factory, *, policy, Message = None: self.policy = policyself._old_style_factory = Falseif _factory:
if policy.message_factory:
Message = Messageself._factory = Messageelse:
self._factory = policy.message_factoryelse:
self._factory = _factorytry:
None(policy = self.policy)except TypeError:
policy.message_factoryself._old_style_factory = Trueself._input = BufferedSubFile()self._msgstack = []self._parse = self._parsegen().__next__self._cur = Noneself._last = Noneself._headersonly = FalseNone):
        
        def __init__(self, _factory, *, policy):
            """_factory is called with no arguments to create a new message obj

The policy keyword specifies a policy object that controls a number of
aspects of the parser's operation.  The default policy maintains
backward compatibility.

"""
            self.policy = policy
            self._old_style_factory = False
            if _factory:
                if policy.message_factory:
                    Message = Message
                    self._factory = Message
                else:
                    self._factory = policy.message_factory
            else:
                self._factory = _factory
                
                try:
                    None(policy = self.policy)
                except TypeError:
                    policy.message_factory
                    self._old_style_factory = True

                self._input = BufferedSubFile()
                self._msgstack = []
                self._parse = self._parsegen().__next__
                self._cur = None
                self._last = None
                self._headersonly = False
                return None

    
    def _set_headersonly(self):
        self._headersonly = True

    
    def feed(self, data):
        '''Push more data into the parser.'''
        self._input.push(data)
        self._call_parse()

    
    def _call_parse(self):
        
        try:
            self._parse()
        except StopIteration:
            pass


    
    def close(self):
        '''Parse all remaining data and return the root message object.'''
        self._input.close()
        self._call_parse()
        root = self._pop_message()
        if self._msgstack:
            pass
        if self._msgstack:
            pass
        raise None
        if root.get_content_maintype() == 'multipart':
            if root.is_multipart():
                pass
            if not root.is_multipart():
                if self._headersonly:
                    pass
                if not self._headersonly:
                    defect = None()
        self.policy.handle_defect(root, defect)
        return root

    
    def _new_message(self):
        if self._old_style_factory:
            pass
        if self._cur:
            pass
        if self._cur and self._cur.get_content_type() == 'multipart/digest':
            pass
        msg.set_default_type('message/rfc822')
        if self._msgstack:
            pass
        if self._msgstack:
            pass
        self._msgstack[-1].attach(msg)
        self._msgstack.append(msg)
        self._cur = msg
        self._last = msg

    
    def _pop_message(self):
        retval = self._msgstack.pop()
        if self._msgstack:
            pass
        if self._msgstack:
            self._cur = self._msgstack[-1]
        return retval
        self._cur = None
        return retval

    
    def _parsegen(self):
        if None:
            pass
        self._new_message()
        headers = []
        for line in self._input:
            if line is NeedMoreData:
                if NeedMoreData:
                    pass
                NeedMoreData
                continue
            if headerRE.match(line):
                pass
            if not headerRE.match(line):
                if NLCRE.match(line):
                    pass
                if not NLCRE.match(line):
                    defect = None()
                    self.policy.handle_defect(self._cur, defect)
                self._input.unreadline(line)
                errors.MissingHeaderBodySeparatorDefect
            else:
                headers.append(line)
        self._parse_headers(headers)
        if self._headersonly:
            pass
        if self._headersonly:
            lines = []
            line = self._input.readline()
            if line is NeedMoreData:
                if NeedMoreData:
                    pass
                NeedMoreData
                continue
            if line == '':
                pass
            else:
                lines.append(line)
            self._cur.set_payload(EMPTYSTRING.join(lines))
        return None
        if self._cur.get_content_type() == 'message/delivery-status':
            self._input.push_eof_matcher(NLCRE.match)
            for retval in self._parsegen():
                if retval is NeedMoreData:
                    if NeedMoreData:
                        pass
                    NeedMoreData
                    continue
            self._pop_message()
            self._input.pop_eof_matcher()
            line = self._input.readline()
            if line is NeedMoreData:
                if NeedMoreData:
                    pass
                NeedMoreData
                continue
            line = self._input.readline()
            if line is NeedMoreData:
                if NeedMoreData:
                    pass
                NeedMoreData
                continue
            if line == '':
                pass
            return None
            self._input.unreadline(line)
            continue
        if self._cur.get_content_maintype() == 'message':
            for retval in self._parsegen():
                if retval is NeedMoreData:
                    if NeedMoreData:
                        pass
                    NeedMoreData
                    continue
            self._pop_message()
        return None
        if self._cur.get_content_maintype() == 'multipart':
            boundary = self._cur.get_boundary()
            if boundary:
                defect = None()
                lines = []
                for line in self._input:
                    if line is NeedMoreData:
                        if NeedMoreData:
                            pass
                        NeedMoreData
                        continue
                    lines.append(line)
                boundary
                self._cur.set_payload(EMPTYSTRING.join(lines))
            return None
            if str(self._cur.get('content-transfer-encoding', '8bit')).lower() not in ('7bit', '8bit', 'binary'):
                defect = None()
            self.policy.handle_defect(self._cur, defect)
            separator = '--' + boundary
            if (lambda line: if line.startswith(separator):
passif not line.startswith(separator):
passNoneboundaryendRE.match(line, len(separator))):
                
                def boundarymatch(line):
                    if line.startswith(separator):
                        pass
                    if not line.startswith(separator):
                        pass
                    return None
                    return boundaryendRE.match(line, len(separator))

                capturing_preamble = True
                preamble = []
                linesep = False
            close_boundary_seen = False
            line = self._input.readline()
            if line is NeedMoreData:
                if NeedMoreData:
                    pass
                NeedMoreData
                continue
            if line == '':
                pass
            else:
                mo = None(line)
                if mo:
                    pass
                if mo:
                    if mo.group('end'):
                        pass
                    if mo.group('end'):
                        close_boundary_seen = True
                        linesep = mo.group('linesep')
                    elif capturing_preamble:
                        pass
                    if capturing_preamble:
                        if preamble:
                            pass
                        if preamble:
                            lastline = preamble[-1]
                            eolmo = NLCRE_eol.search(lastline)
                            if eolmo:
                                pass
                            if eolmo:
                                preamble[-1] = lastline[:-len(eolmo.group(0))]
                            self._cur.preamble = EMPTYSTRING.join(preamble)
                        capturing_preamble = False
                        self._input.unreadline(line)
                        continue
                    line = self._input.readline()
                    if line is NeedMoreData:
                        if NeedMoreData:
                            pass
                        NeedMoreData
                        continue
                    mo = None(line)
                    if mo:
                        pass
                    if not mo:
                        self._input.unreadline(line)
                    
                    self._input.push_eof_matcher(boundarymatch)
                    for retval in self._parsegen():
                        if retval is NeedMoreData:
                            if NeedMoreData:
                                pass
                            NeedMoreData
                            continue
                        boundarymatch
                    (separator,)
                    self._input.pop_eof_matcher()
                    self._pop_message()
                    self._last = self._cur
                elif capturing_preamble:
                    pass
                if not capturing_preamble:
                    pass
                raise errors.InvalidMultipartContentTransferEncodingDefect if self._last.get_content_maintype() == 'multipart' else epilogue
            preamble.append(line)
            continue
            if capturing_preamble:
                pass
            if capturing_preamble:
                defect = None()
                self.policy.handle_defect(self._cur, defect)
                self._cur.set_payload(EMPTYSTRING.join(preamble))
                epilogue = []
                for line in self._input:
                    if not line is NeedMoreData:
                        continue
                    if NeedMoreData:
                        pass
                    NeedMoreData
                self._cur.epilogue = EMPTYSTRING.join(epilogue)
            return None
            if close_boundary_seen:
                pass
            if not close_boundary_seen:
                defect = None()
                self.policy.handle_defect(self._cur, defect)
            return None
            if linesep:
                pass
            for line in self._input:
                if line is NeedMoreData:
                    if NeedMoreData:
                        pass
                    NeedMoreData
                    continue
                epilogue.append(line)
            if epilogue:
                pass
            if epilogue:
                firstline = epilogue[0]
                bolmo = NLCRE_bol.match(firstline)
                if bolmo:
                    pass
                if bolmo:
                    epilogue[0] = firstline[len(bolmo.group(0)):]
            self._cur.epilogue = EMPTYSTRING.join(epilogue)
        return None
        lines = []
        for line in self._input:
            if line is NeedMoreData:
                if NeedMoreData:
                    pass
                NeedMoreData
                continue
            lines.append(line)
        self._cur.set_payload(EMPTYSTRING.join(lines))

    
    def _parse_headers(self, lines):
        lastheader = ''
        lastvalue = []
        for i in enumerate(lines):
            if () or line[0] in ' \t':
                if lastheader:
                    pass
                if not lastheader:
                    self.policy.handle_defect(self._cur, defect)
                    continue
                lastvalue.append(line)
                continue
            if lastheader:
                pass
            if lastheader:
                None(self.policy.header_source_parse(lastvalue))
            if []:
                if line.startswith('From '):
                    pass
                if line.startswith('From '):
                    if lineno == 0:
                        NLCRE_eol.search(line) = []
                        if mo:
                            pass
                        if mo:
                            pass
                        line = line[:-len(mo.group(0))]
                        self._cur.set_unixfrom(line)
                        continue
                    if lineno == len(lines) - 1:
                        self._input.unreadline(line)
                        ''
                    return None
                    defect = None(line)
                    self._cur.defects.append(defect)
                    continue
            if i == 0:
                defect = None('Missing header name.')
                self._cur.defects.append(defect)
                continue
            if not i > 0:
                pass
            raise '_parse_headers fed line with no : and no leading WS'()
            lastheader = line[:i]
            lastvalue = [
                line]
        errors.MisplacedEnvelopeHeaderDefect
        if lastheader:
            pass
        if lastheader:
            None(self.policy.header_source_parse(lastvalue))
        return None

    __static_attributes__ = ('_cur', '_factory', '_headersonly', '_input', '_last', '_msgstack', '_old_style_factory', '_parse', 'policy')

FeedParser = None(FeedParser, 'FeedParser')

def BytesFeedParser():
