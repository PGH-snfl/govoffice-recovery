# Source Generated with Decompyle++
# File: _header_value_parser.marshal (Python 3.13)

'''Header value parser implementing various email-related RFC parsing rules.

The parsing methods defined in this module implement various email related
parsing rules.  Principal among them is RFC 5322, which is the followon
to RFC 2822 and primarily a clarification of the former.  It also implements
RFC 2047 encoded word decoding.

RFC 5322 goes to considerable trouble to maintain backward compatibility with
RFC 822 in the parse phase, while cleaning up the structure on the generation
phase.  This parser supports correct RFC 5322 generation by tagging white space
as folding white space only when folding is allowed in the non-obsolete rule
sets.  Actually, the parser is even more generous when accepting input than RFC
5322 mandates, following the spirit of Postel\'s Law, which RFC 5322 encourages.
Where possible deviations from the standard are annotated on the \'defects\'
attribute of tokens that deviate.

The general structure of the parser follows RFC 5322, and uses its terminology
where there is a direct correspondence.  Where the implementation requires a
somewhat different structure than that used by the formal grammar, new terms
that mimic the closest existing terms are used.  Thus, it really helps to have
a copy of RFC 5322 handy when studying this code.

Input to the parser is a string that has already been unfolded according to
RFC 5322 rules.  According to the RFC this unfolding is the very first step, and
this parser leaves the unfolding step to a higher level message parser, which
will have already detected the line breaks that need unfolding while
determining the beginning and end of each header.

The output of the parser is a TokenList object, which is a list subclass.  A
TokenList is a recursive data structure.  The terminal nodes of the structure
are Terminal objects, which are subclasses of str.  These do not correspond
directly to terminal objects in the formal grammar, but are instead more
practical higher level combinations of true terminals.

All TokenList and Terminal objects have a \'value\' attribute, which produces the
semantically meaningful value of that part of the parse subtree.  The value of
all whitespace tokens (no matter how many sub-tokens they may contain) is a
single space, as per the RFC rules.  This includes \'CFWS\', which is herein
included in the general class of whitespace tokens.  There is one exception to
the rule that whitespace tokens are collapsed into single spaces in values: in
the value of a \'bare-quoted-string\' (a quoted-string with no leading or
trailing whitespace), any whitespace that appeared between the quotation marks
is preserved in the returned value.  Note that in all Terminal strings quoted
pairs are turned into their unquoted values.

All TokenList and Terminal objects also have a string value, which attempts to
be a "canonical" representation of the RFC-compliant form of the substring that
produced the parsed subtree, including minimal use of quoted pair quoting.
Whitespace runs are not collapsed.

Comment tokens also have a \'content\' attribute providing the string found
between the parens (including any nested comments) with whitespace preserved.

All TokenList and Terminal objects have a \'defects\' attribute which is a
possibly empty list all of the defects found while creating the token.  Defects
may appear on any token in the tree, and a composite list of all defects in the
subtree is available through the \'all_defects\' attribute of any node.  (For
Terminal notes x.defects == x.all_defects.)

Each object in a parse tree is called a \'token\', and each has a \'token_type\'
attribute that gives the name from the RFC 5322 grammar that it represents.
Not all RFC 5322 nodes are produced, and there is one non-RFC 5322 node that
may be produced: \'ptext\'.  A \'ptext\' is a string of printable ascii characters.
It is returned in place of lists of (ctext/quoted-pair) and
(qtext/quoted-pair).

XXX: provide complete list of token types.
'''
import re
import sys
import urllib
from string import hexdigits
from operator import itemgetter
from email import _encoded_words as _ew
from email import errors
from email import utils
WSP = None(' \t')
CFWS_LEADER = set | None('(')
SPECIALS = None('()<>@,:;.\\"[]')
ATOM_ENDS = SPECIALS | WSP
DOT_ATOM_ENDS = set - None('.')
PHRASE_ENDS = set - None('."(')
TSPECIALS = set - None('.')
TOKEN_ENDS = TSPECIALS | WSP
ASPECIALS = set | None("*'%")
ATTRIBUTE_ENDS = ASPECIALS | WSP
EXTENDED_ATTRIBUTE_ENDS = set - None('%')
NLSET = {
    '\n',
    '\r'}
SPECIALSNL = SPECIALS | NLSET

def make_quoted_pairs(value):
    '''Escape dquote and backslash for use within a quoted-string.'''
    return str(value).replace('\\', '\\\\').replace('"', '\\"')


def quote_string(value):
    escaped = make_quoted_pairs(value)
    return f'''"{escaped}"'''

rfc2047_matcher = None("\n   =\\?            # literal =?\n   [^?]*          # charset\n   \\?             # literal ?\n   [qQbB]         # literal 'q' or 'b', case insensitive\n   \\?             # literal ?\n  .*?             # encoded word\n  \\?=             # literal ?=\n", re.VERBOSE | re.MULTILINE)

def TokenList():
    '''TokenList'''
    __firstlineno__ = 125
    token_type = None
    syntactic_break = True
    ew_combine_allowed = True
    if (lambda self: args({ }, kw = None)self.defects = []):
        
        def __init__(self, *args, **kw):
            args({ }, kw = None)
            self.defects = []

        
        def __str__(self):
            return (lambda .0: if None:
passfor x in .0:
if str(x):
passstr(x))(self())

    if (lambda self: super(__class__, self())):
        
        def __repr__(self):
            return super(__class__, self())

    value = (lambda self: (lambda .0: if None:
passfor None in .0:
if None:
if None.value:
passif not None.value:
continueif x.value:
pass)(self())
)()
    all_defects = (lambda self: (lambda .0: if None:
passfor None in .0:
if None:
if None.all_defects:
passcontinue)(self(), self.defects)
)()
    
    def startswith_fws(self):
        return self[0].startswith_fws()

    as_ew_allowed = (lambda self: (lambda .0: if None:
passfor None in .0:
if None:
if None.as_ew_allowed:
passcontinue)(self())
)()
    comments = (lambda self: comments = []for token in self:
comments.extend(token.comments)comments)()
    
    def fold(self, *, policy):
        return _refold_parse_tree(self, policy = policy)

    if (lambda self, indent: None(self.ppstr(indent = indent))):
        
        def pprint(self, indent):
            None(self.ppstr(indent = indent))

    if (lambda self, indent: None(self._pp(indent = indent))):
        
        def ppstr(self, indent):
            return None(self._pp(indent = indent))

    if (lambda self, indent: if None:
passif '{}{}/{}('.format(indent, self.__class__.__name__, self.token_type):
pass'{}{}/{}('.format(indent, self.__class__.__name__, self.token_type)for token in self:
if hasattr(token, '_pp'):
passif not hasattr(token, '_pp'):
if indent + '    !! invalid element in token list: {!r}'.format(token):
passindent + '    !! invalid element in token list: {!r}'.format(token)continueif None and None:
passif self.defects:
passif self.defects:
extra = ' Defects: {}'.format(self.defects)else:
extra = ''if '{}){}'.format(indent, extra):
pass'{}){}'.format(indent, extra)Nonecontinue):
        
        def _pp(self, indent):
            if None:
                pass
            if '{}{}/{}('.format(indent, self.__class__.__name__, self.token_type):
                pass
            '{}{}/{}('.format(indent, self.__class__.__name__, self.token_type)
            for token in self:
                if hasattr(token, '_pp'):
                    pass
                if not hasattr(token, '_pp'):
                    if indent + '    !! invalid element in token list: {!r}'.format(token):
                        pass
                    indent + '    !! invalid element in token list: {!r}'.format(token)
                    continue
                if None and None:
                    pass
            if self.defects:
                pass
            if self.defects:
                extra = ' Defects: {}'.format(self.defects)
            else:
                extra = ''
            if '{}){}'.format(indent, extra):
                pass
            '{}){}'.format(indent, extra)
            return None
            continue

    __static_attributes__ = ('defects',)
    __classcell__ = __class__
    return __class__

TokenList = None(TokenList, 'TokenList', list)

def WhiteSpaceTokenList():
    '''WhiteSpaceTokenList'''
    __firstlineno__ = 192
    value = (lambda self: ' ')()
    comments = (lambda self: for None in :
if None:
if not None.token_type == 'comment':
continue, []x,)()
    __static_attributes__ = ()

WhiteSpaceTokenList = None(WhiteSpaceTokenList, 'WhiteSpaceTokenList', TokenList)

def UnstructuredTokenList():
    '''UnstructuredTokenList'''
    __firstlineno__ = 203
    token_type = 'unstructured'
    __static_attributes__ = ()

UnstructuredTokenList = None(UnstructuredTokenList, 'UnstructuredTokenList', TokenList)

def Phrase():
    '''Phrase'''
    __firstlineno__ = 207
    token_type = 'phrase'
    __static_attributes__ = ()

Phrase = None(Phrase, 'Phrase', TokenList)

def Word():
    '''Word'''
    __firstlineno__ = 210
    token_type = 'word'
    __static_attributes__ = ()

Word = None(Word, 'Word', TokenList)

def CFWSList():
    '''CFWSList'''
    __firstlineno__ = 214
    token_type = 'cfws'
    __static_attributes__ = ()

CFWSList = None(CFWSList, 'CFWSList', WhiteSpaceTokenList)

def Atom():
    '''Atom'''
    __firstlineno__ = 218
    token_type = 'atom'
    __static_attributes__ = ()

Atom = None(Atom, 'Atom', TokenList)

def Token():
    '''Token'''
    __firstlineno__ = 222
    token_type = 'token'
    encode_as_ew = False
    __static_attributes__ = ()

Token = None(Token, 'Token', TokenList)

def EncodedWord():
    '''EncodedWord'''
    __firstlineno__ = 227
    token_type = 'encoded-word'
    cte = None
    charset = None
    lang = None
    __static_attributes__ = ()

EncodedWord = None(EncodedWord, 'EncodedWord', TokenList)

def QuotedString():
    '''QuotedString'''
    __firstlineno__ = 234
    token_type = 'quoted-string'
    content = (lambda self: for x in self:
if not x.token_type == 'bare-quoted-string':
continueNone, x.value)()
    quoted_value = (lambda self: res = []for x in self:
if x.token_type == 'bare-quoted-string':
res.append(str(x))continueres.append(x.value)''.join(res))()
    stripped_value = (lambda self: for token in self:
if not token.token_type == 'bare-quoted-string':
continueNone, token.value)()
    __static_attributes__ = ()

QuotedString = None(QuotedString, 'QuotedString', TokenList)

def BareQuotedString():
    '''BareQuotedString'''
    __firstlineno__ = 261
    token_type = 'bare-quoted-string'
    
    def __str__(self):
        return ''.join((lambda .0: if None:
passfor x in .0:
if str(x):
passstr(x))(self()))

    value = (lambda self: (lambda .0: if None:
passfor x in .0:
if str(x):
passstr(x))(self())
)()
    __static_attributes__ = ()

BareQuotedString = None(BareQuotedString, 'BareQuotedString', QuotedString)

def Comment():
    '''Comment'''
    __firstlineno__ = 273
    token_type = 'comment'
    
    def __str__(self):
        for None in :
            if None:
                pass
        , []
        return ''.join(None([
            sum, [
                '('], self,
            x,,
            [
                ')']], []))
        

    
    def quote(self, value):
        if value.token_type == 'comment':
            pass
        return str(value)
        return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    content = (lambda self: (lambda .0: if None:
passfor x in .0:
if str(x):
passstr(x))(self())
)()
    comments = (lambda self: [
self.content])()
    __static_attributes__ = ()

Comment = None(Comment, 'Comment', WhiteSpaceTokenList)

def AddressList():
    '''AddressList'''
    __firstlineno__ = 299
    token_type = 'address-list'
    addresses = (lambda self: for None in :
if None:
if not None.token_type == 'address':
continue, []x,)()
    mailboxes = (lambda self: (lambda .0: if None:
passfor None in .0:
if None:
if not None.token_type == 'address':
continueif x.mailboxes:
pass)(self(), [])
)()
    all_mailboxes = (lambda self: (lambda .0: if None:
passfor None in .0:
if None:
if not None.token_type == 'address':
continueif x.all_mailboxes:
pass)(self(), [])
)()
    __static_attributes__ = ()

AddressList = None(AddressList, 'AddressList', TokenList)

def Address():
    '''Address'''
    __firstlineno__ = 318
    token_type = 'address'
    display_name = (lambda self: if self[0].token_type == 'group':
passself[0].display_name)()
    mailboxes = (lambda self: if self[0].token_type == 'mailbox':
pass[
self[0]]if self[0].token_type == 'invalid-mailbox':
pass[]self[0].mailboxes)()
    all_mailboxes = (lambda self: if self[0].token_type == 'mailbox':
pass[
self[0]]if self[0].token_type == 'invalid-mailbox':
pass[
self[0]]self[0].all_mailboxes)()
    __static_attributes__ = ()

Address = None(Address, 'Address', TokenList)

def MailboxList():
    '''MailboxList'''
    __firstlineno__ = 343
    token_type = 'mailbox-list'
    mailboxes = (lambda self: for None in :
if None:
if not None.token_type == 'mailbox':
continue, []x,)()
    all_mailboxes = (lambda self: for None in :
if not x.token_type in ('mailbox', 'invalid-mailbox'):
continuex,)()
    __static_attributes__ = ()

MailboxList = None(MailboxList, 'MailboxList', TokenList)

def GroupList():
    '''GroupList'''
    __firstlineno__ = 357
    token_type = 'group-list'
    mailboxes = (lambda self: if self:
passif self or self[0].token_type != 'mailbox-list':
pass[]self[0].mailboxes)()
    all_mailboxes = (lambda self: if self:
passif self or self[0].token_type != 'mailbox-list':
pass[]self[0].all_mailboxes)()
    __static_attributes__ = ()

GroupList = None(GroupList, 'GroupList', TokenList)

def Group():
    '''Group'''
    __firstlineno__ = 374
    token_type = 'group'
    mailboxes = (lambda self: if self[2].token_type != 'group-list':
pass[]self[2].mailboxes)()
    all_mailboxes = (lambda self: if self[2].token_type != 'group-list':
pass[]self[2].all_mailboxes)()
    display_name = (lambda self: self[0].display_name)()
    __static_attributes__ = ()

Group = None(Group, 'Group', TokenList)

def NameAddr():
    '''NameAddr'''
    __firstlineno__ = 395
    token_type = 'name-addr'
    display_name = (lambda self: if len(self) == 1:
passNoneself[0].display_name)()
    local_part = (lambda self: self[-1].local_part)()
    domain = (lambda self: self[-1].domain)()
    route = (lambda self: self[-1].route)()
    addr_spec = (lambda self: self[-1].addr_spec)()
    __static_attributes__ = ()

NameAddr = None(NameAddr, 'NameAddr', TokenList)

def AngleAddr():
    '''AngleAddr'''
    __firstlineno__ = 422
    token_type = 'angle-addr'
    local_part = (lambda self: for x in self:
if not x.token_type == 'addr-spec':
continueNone, x.local_part)()
    domain = (lambda self: for x in self:
if not x.token_type == 'addr-spec':
continueNone, x.domain)()
    route = (lambda self: for x in self:
if not x.token_type == 'obs-route':
continueNone, x.domains)()
    addr_spec = (lambda self: for x in self:
if not x.token_type == 'addr-spec':
continueif x.local_part:
passif x.local_part:
None, x.addr_specNone, quote_string(x.local_part) + x.addr_spec'<>')()
    __static_attributes__ = ()

AngleAddr = None(AngleAddr, 'AngleAddr', TokenList)

def ObsRoute():
    '''ObsRoute'''
    __firstlineno__ = 456
    token_type = 'obs-route'
    domains = (lambda self: for None in :
if None:
if not None.token_type == 'domain':
continue, []x,)()
    __static_attributes__ = ()

ObsRoute = None(ObsRoute, 'ObsRoute', TokenList)

def Mailbox():
    '''Mailbox'''
    __firstlineno__ = 465
    token_type = 'mailbox'
    display_name = (lambda self: if self[0].token_type == 'name-addr':
passself[0].display_name)()
    local_part = (lambda self: self[0].local_part)()
    domain = (lambda self: self[0].domain)()
    route = (lambda self: if self[0].token_type == 'name-addr':
passself[0].route)()
    addr_spec = (lambda self: self[0].addr_spec)()
    __static_attributes__ = ()

Mailbox = None(Mailbox, 'Mailbox', TokenList)

def InvalidMailbox():
    '''InvalidMailbox'''
    __firstlineno__ = 492
    token_type = 'invalid-mailbox'
    display_name = (lambda self: pass)()
    local_part = display_name
    domain = display_name
    route = display_name
    addr_spec = display_name
    __static_attributes__ = ()

InvalidMailbox = None(InvalidMailbox, 'InvalidMailbox', TokenList)

def Domain():
    '''Domain'''
    __firstlineno__ = 503
    token_type = 'domain'
    as_ew_allowed = False
    if (lambda self: __class__(self.split())):
        domain = (lambda self: __class__(self.split()))()
        __static_attributes__ = ()
    __classcell__ = __class__
    return __class__

Domain = None(Domain, 'Domain', TokenList)

def DotAtom():
    '''DotAtom'''
    __firstlineno__ = 513
    token_type = 'dot-atom'
    __static_attributes__ = ()

DotAtom = None(DotAtom, 'DotAtom', TokenList)

def DotAtomText():
    '''DotAtomText'''
    __firstlineno__ = 517
    token_type = 'dot-atom-text'
    as_ew_allowed = True
    __static_attributes__ = ()

DotAtomText = None(DotAtomText, 'DotAtomText', TokenList)

def NoFoldLiteral():
    '''NoFoldLiteral'''
    __firstlineno__ = 522
    token_type = 'no-fold-literal'
    as_ew_allowed = False
    __static_attributes__ = ()

NoFoldLiteral = None(NoFoldLiteral, 'NoFoldLiteral', TokenList)

def AddrSpec():
    '''AddrSpec'''
    __firstlineno__ = 527
    token_type = 'addr-spec'
    as_ew_allowed = False
    local_part = (lambda self: self[0].local_part)()
    domain = (lambda self: if len(self) < 3:
passNoneself[-1].domain)()
    value = (lambda self: if len(self) < 3:
passself[0].valueself[0].value.rstrip() + self[1].value + self[2].value.lstrip())()
    addr_spec = (lambda self: nameset = set(self.local_part)if len(nameset) > len(nameset - DOT_ATOM_ENDS):
lp = quote_string(self.local_part)else:
lp = self.local_partif self.domain:
passlp + '@' + self.domainlp)()
    __static_attributes__ = ()

AddrSpec = None(AddrSpec, 'AddrSpec', TokenList)

def ObsLocalPart():
    '''ObsLocalPart'''
    __firstlineno__ = 560
    token_type = 'obs-local-part'
    as_ew_allowed = False
    __static_attributes__ = ()

ObsLocalPart = None(ObsLocalPart, 'ObsLocalPart', TokenList)

def DisplayName():
    '''DisplayName'''
    __firstlineno__ = 566
    token_type = 'display-name'
    ew_combine_allowed = False
    display_name = (lambda self: res = TokenList(self)if len(res) == 0:
passres.valueif res[0].token_type == 'cfws':
res.pop(0)elif isinstance(res[0], TokenList):
passif isinstance(res[0], TokenList) and res[0][0].token_type == 'cfws':
res[0] = TokenList(res[0][1:])if res[-1].token_type == 'cfws':
res.pop()res.valueif isinstance(res[-1], TokenList):
passif isinstance(res[-1], TokenList) and res[-1][-1].token_type == 'cfws':
res[-1] = TokenList(res[-1][:-1])res.value)()
    if (lambda self: quote = Falseif self.defects:
passif self.defects:
quote = Trueelse:
for x in self:
if not x.token_type == 'quoted-string':
continuequote = Trueif len(self) != 0:
if quote:
passif quote:
if not '' or self[0].token_type == 'cfws':
if isinstance(self[0], TokenList):
passif isinstance(self[0], TokenList) and self[0][0].token_type == 'cfws':
passpre = ' 'if not self[-1].token_type == 'cfws':
if isinstance(self[-1], TokenList):
passif isinstance(self[-1], TokenList) and self[-1][-1].token_type == 'cfws':
passpost = ' 'pre + quote_string(self.display_name) + postself):
        value = (lambda self: quote = Falseif self.defects:
passif self.defects:
quote = Trueelse:
for x in self:
if not x.token_type == 'quoted-string':
continuequote = Trueif len(self) != 0:
if quote:
passif quote:
if not '' or self[0].token_type == 'cfws':
if isinstance(self[0], TokenList):
passif isinstance(self[0], TokenList) and self[0][0].token_type == 'cfws':
passpre = ' 'if not self[-1].token_type == 'cfws':
if isinstance(self[-1], TokenList):
passif isinstance(self[-1], TokenList) and self[-1][-1].token_type == 'cfws':
passpost = ' 'pre + quote_string(self.display_name) + postself)()
        __static_attributes__ = ()
    __classcell__ = __class__
    return __class__

DisplayName = None(DisplayName, 'DisplayName', Phrase)

def LocalPart():
    '''LocalPart'''
    __firstlineno__ = 614
    token_type = 'local-part'
    as_ew_allowed = False
    value = (lambda self: if self[0].token_type == 'quoted-string':
passself[0].quoted_valueself[0].value)()
    local_part = (lambda self: res = [
DOT]last = DOTlast_is_tl = Falsefor tok in self[0] + [
DOT]:
if tok.token_type == 'cfws':
continueif last_is_tl:
passif last_is_tl and tok.token_type == 'dot' and last[-1].token_type == 'cfws':
res[-1] = TokenList(last[:-1])is_tl = isinstance(tok, TokenList)if is_tl:
passif is_tl and last.token_type == 'dot' and tok[0].token_type == 'cfws':
res.append(TokenList(tok[1:]))else:
res.append(tok)last = res[-1]last_is_tl = is_tlres = TokenList(res[1:-1])res.value)()
    __static_attributes__ = ()

LocalPart = None(LocalPart, 'LocalPart', TokenList)

def DomainLiteral():
    '''DomainLiteral'''
    __firstlineno__ = 650
    token_type = 'domain-literal'
    as_ew_allowed = False
    if (lambda self: __class__(self.split())):
        domain = (lambda self: __class__(self.split()))()
    ip = (lambda self: for x in self:
if not x.token_type == 'ptext':
continueNone, x.value)()
    __static_attributes__ = ()
    __classcell__ = __class__
    return __class__

DomainLiteral = None(DomainLiteral, 'DomainLiteral', TokenList)

def MIMEVersion():
    '''MIMEVersion'''
    __firstlineno__ = 666
    token_type = 'mime-version'
    major = None
    minor = None
    __static_attributes__ = ()

MIMEVersion = None(MIMEVersion, 'MIMEVersion', TokenList)

def Parameter():
    '''Parameter'''
    __firstlineno__ = 673
    token_type = 'parameter'
    sectioned = False
    extended = False
    charset = 'us-ascii'
    section_number = (lambda self: if self.sectioned:
passif self.sectioned:
passself[1].number0)()
    param_value = (lambda self: for token in self:
if token.token_type == 'value':
None, token.stripped_valueif not token.token_type == 'quoted-string':
continuefor None in token:
if not token.token_type == 'bare-quoted-string':
continuefor None in token:
if not token.token_type == 'value':
continueNone, None, None, token.stripped_value'')()
    __static_attributes__ = ()

Parameter = None(Parameter, 'Parameter', TokenList)

def InvalidParameter():
    '''InvalidParameter'''
    __firstlineno__ = 701
    token_type = 'invalid-parameter'
    __static_attributes__ = ()

InvalidParameter = None(InvalidParameter, 'InvalidParameter', Parameter)

def Attribute():
    '''Attribute'''
    __firstlineno__ = 706
    token_type = 'attribute'
    stripped_value = (lambda self: for token in self:
if token.token_type.endswith('attrtext'):
passif not token.token_type.endswith('attrtext'):
continueNone, token.value)()
    __static_attributes__ = ()

Attribute = None(Attribute, 'Attribute', TokenList)

def Section():
    '''Section'''
    __firstlineno__ = 716
    token_type = 'section'
    number = None
    __static_attributes__ = ()

Section = None(Section, 'Section', TokenList)

def Value():
    '''Value'''
    __firstlineno__ = 722
    token_type = 'value'
    stripped_value = (lambda self: token = self[0]if token.token_type == 'cfws':
passtoken = self[1]if token.token_type.endswith(('quoted-string', 'attribute', 'extended-attribute')):
passif token.token_type.endswith(('quoted-string', 'attribute', 'extended-attribute')):
passtoken.stripped_valueself.value)()
    __static_attributes__ = ()

Value = None(Value, 'Value', TokenList)

def MimeParameters():
    '''MimeParameters'''
    __firstlineno__ = 737
    token_type = 'mime-parameters'
    syntactic_break = False
    params = (lambda self: if None:
passparams = { }for token in self:
if token.token_type.endswith('parameter'):
passif not token.token_type.endswith('parameter'):
continueif token[0].token_type != 'attribute':
continuename = token[0].value.strip()if name not in params:
params[name] = []params[name].append((token.section_number, token))for parts in params.items():
if ():
parts[0][1] = sorted(parts, key = itemgetter(0))charset = first_param.charsetif first_param.extended:
passif first_param.extended and len(parts) > 1 and parts[1][0] == 0:
errors.InvalidHeaderDefect(None('duplicate parameter name; duplicate(s) ignored'))value_parts = []i = 0for None in parts:
if ():
if section_number != i:
if param.extended:
passif not param.extended:
errors.InvalidHeaderDefect(None('duplicate parameter name; duplicate ignored'))continuei += 1if param.extended:
passif param.extended:
try:
value = urllib.parse.unquote_to_bytes(value)except UnicodeEncodeError:
value = urllib.parse.unquote(value, encoding = 'latin-1')try:
value = value.decode(charset, 'surrogateescape')except (LookupError, UnicodeEncodeError):
value = value.decode('us-ascii', 'surrogateescape')if None(value):
passif None(value):
passvalue_parts.append(value)value = ''.join(value_parts)if (name, value):
pass(name, value)param.defects.append)()
    
    def __str__(self):
        params = []
        for None in self.params:
            if ():
                if value:
                    pass
                if value:
                    params.append('{}={}'.format(name, quote_string(value)))
                    continue
        if params:
            pass
        if params:
            pass
        return ' ' + params
        return ''

    __static_attributes__ = ()

MimeParameters = None(MimeParameters, 'MimeParameters', TokenList)

def ParameterizedHeaderValue():
    '''ParameterizedHeaderValue'''
    __firstlineno__ = 823
    syntactic_break = False
    params = (lambda self: for token in reversed(self):
if not token.token_type == 'mime-parameters':
continueNone, token.params{ })()
    __static_attributes__ = ()

ParameterizedHeaderValue = None(ParameterizedHeaderValue, 'ParameterizedHeaderValue', TokenList)

def ContentType():
    '''ContentType'''
    __firstlineno__ = 837
    token_type = 'content-type'
    as_ew_allowed = False
    maintype = 'text'
    subtype = 'plain'
    __static_attributes__ = ()

ContentType = None(ContentType, 'ContentType', ParameterizedHeaderValue)

def ContentDisposition():
    '''ContentDisposition'''
    __firstlineno__ = 844
    token_type = 'content-disposition'
    as_ew_allowed = False
    content_disposition = None
    __static_attributes__ = ()

ContentDisposition = None(ContentDisposition, 'ContentDisposition', ParameterizedHeaderValue)

def ContentTransferEncoding():
    '''ContentTransferEncoding'''
    __firstlineno__ = 850
    token_type = 'content-transfer-encoding'
    as_ew_allowed = False
    cte = '7bit'
    __static_attributes__ = ()

ContentTransferEncoding = None(ContentTransferEncoding, 'ContentTransferEncoding', TokenList)

def HeaderLabel():
    '''HeaderLabel'''
    __firstlineno__ = 856
    token_type = 'header-label'
    as_ew_allowed = False
    __static_attributes__ = ()

HeaderLabel = None(HeaderLabel, 'HeaderLabel', TokenList)

def MsgID():
    '''MsgID'''
    __firstlineno__ = 861
    token_type = 'msg-id'
    as_ew_allowed = False
    
    def fold(self, policy):
        return str(self) + policy.linesep

    __static_attributes__ = ()

MsgID = None(MsgID, 'MsgID', TokenList)

def MessageID():
    '''MessageID'''
    __firstlineno__ = 870
    token_type = 'message-id'
    __static_attributes__ = ()

MessageID = None(MessageID, 'MessageID', MsgID)

def InvalidMessageID():
    '''InvalidMessageID'''
    __firstlineno__ = 874
    token_type = 'invalid-message-id'
    __static_attributes__ = ()

InvalidMessageID = None(InvalidMessageID, 'InvalidMessageID', MessageID)

def Header():
    '''Header'''
    __firstlineno__ = 878
    token_type = 'header'
    __static_attributes__ = ()

Header = None(Header, 'Header', TokenList)

def Terminal():
    '''Terminal'''
    __firstlineno__ = 886
    as_ew_allowed = True
    ew_combine_allowed = True
    syntactic_break = True
    if (lambda cls, value, token_type: self = cls(cls, value)self.token_type = token_typeself.defects = []self):
        
        def __new__(cls, value, token_type):
            self = cls(cls, value)
            self.token_type = token_type
            self.defects = []
            return self

        if (lambda self: super(__class__, self())):
            
            def __repr__(self):
                return super(__class__, self())

            
            def pprint(self):
                print(self.__class__.__name__ + '/' + self.token_type)

    all_defects = (lambda self: list(self.defects))()
    if (lambda self, indent: if self.defects:
passif not self.defects:
pass[
self.__class__.__name__(self.token_type, super, __class__, self(), '')][
None(None, None, '{}{}/{}({}){}'.format, indent, ' {}'.format(self.defects))]):
        if (lambda self, indent: if self.defects:
passif not self.defects:
pass[
self.__class__.__name__(self.token_type, super, __class__, self(), '')][
None(None, None, '{}{}/{}({}){}'.format, indent, ' {}'.format(self.defects))]):
            
            def _pp(self, indent):
                if self.defects:
                    pass
                if not self.defects:
                    pass
                return [
                    self.__class__.__name__(self.token_type, super, __class__, self(), '')]
                return [
                    None(None, None, '{}{}/{}({}){}'.format, indent, ' {}'.format(self.defects))]

        
        def pop_trailing_ws(self):
            pass

    comments = (lambda self: [])()
    
    def __getnewargs__(self):
        return (str(self), self.token_type)

    __static_attributes__ = ('defects', 'token_type')
    __classcell__ = __class__
    return __class__

Terminal = None(Terminal, 'Terminal', str)

def WhiteSpaceTerminal():
    '''WhiteSpaceTerminal'''
    __firstlineno__ = 929
    value = (lambda self: ' ')()
    
    def startswith_fws(self):
        return True

    __static_attributes__ = ()

WhiteSpaceTerminal = None(WhiteSpaceTerminal, 'WhiteSpaceTerminal', Terminal)

def ValueTerminal():
    '''ValueTerminal'''
    __firstlineno__ = 939
    value = (lambda self: self)()
    
    def startswith_fws(self):
        return False

    __static_attributes__ = ()

ValueTerminal = None(ValueTerminal, 'ValueTerminal', Terminal)

def EWWhiteSpaceTerminal():
    '''EWWhiteSpaceTerminal'''
    __firstlineno__ = 949
    value = (lambda self: '')()
    
    def __str__(self):
        return ''

    __static_attributes__ = ()

EWWhiteSpaceTerminal = None(EWWhiteSpaceTerminal, 'EWWhiteSpaceTerminal', WhiteSpaceTerminal)

def _InvalidEwError():
    '''_InvalidEwError'''
    __firstlineno__ = 959
    __doc__ = 'Invalid encoded word found while parsing headers.'
    __static_attributes__ = ()

_InvalidEwError = None(_InvalidEwError, '_InvalidEwError', errors.HeaderParseError)
DOT = None('.', 'dot')
ListSeparator = None(',', 'list-separator')
ListSeparator.as_ew_allowed = False
ListSeparator.syntactic_break = False
RouteComponentMarker = None('@', 'route-component-marker')
_wsp_splitter = None('([{}]+)'.format(''.join(WSP))).split
_non_atom_end_matcher = '[^{}]+'.format(re.escape(None(''.join(ATOM_ENDS)))).match
_non_printable_finder = None('[\\x00-\\x20\\x7F]').findall
_non_token_end_matcher = '[^{}]+'.format(re.escape(None(''.join(TOKEN_ENDS)))).match
_non_attribute_end_matcher = '[^{}]+'.format(re.escape(None(''.join(ATTRIBUTE_ENDS)))).match
_non_extended_attribute_end_matcher = '[^{}]+'.format(re.escape(None(''.join(EXTENDED_ATTRIBUTE_ENDS)))).match

def _validate_xtext(xtext):
    '''If input token contains ASCII non-printables, register a defect.'''
    non_printables = _non_printable_finder(xtext)
    if non_printables:
        pass
    if non_printables:
        pass
    errors.NonPrintableDefect(None(non_printables))
    if None(xtext):
        pass
    if None(xtext):
        errors.UndecodableBytesDefect(None('Non-ASCII characters found in header token'))
    return None


def _get_ptext_to_endchars(value, endchars):
