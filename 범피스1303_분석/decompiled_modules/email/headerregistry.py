# Source Generated with Decompyle++
# File: headerregistry.marshal (Python 3.13)

'''Representing and manipulating email headers via custom objects.

This module provides an implementation of the HeaderRegistry API.
The implementation is designed to flexibly follow RFC5322 rules.
'''
from types import MappingProxyType
from email import utils
from email import errors
from email import _header_value_parser as parser

def Address():
    '''Address'''
    __firstlineno__ = 12
    if (lambda self, display_name, username, domain, addr_spec: inputs = ''.join(filter(None, (display_name, username, domain, addr_spec)))if '\r' in inputs or '\n' in inputs:
passraise ValueError('invalid arguments; address parts cannot contain CR or LF')if addr_spec:
if username:
passif not username:
if domain:
passif domain:
passraise TypeError('addrspec specified when username and/or domain also specified')if ():
if rest:
passif rest:
passraise ValueError("Invalid addr_spec; only '{}' could be parsed from '{}'".format(a_s, addr_spec))if a_s.all_defects:
passif a_s.all_defects:
passraise a_s.all_defects[0]a_s.domain = a_s.local_partself._display_name = display_nameself._username = usernameself._domain = domain):
        
        def __init__(self, display_name, username, domain, addr_spec):
            """Create an object representing a full email address.

An address can have a 'display_name', a 'username', and a 'domain'.  In
addition to specifying the username and domain separately, they may be
specified together by using the addr_spec keyword *instead of* the
username and domain keywords.  If an addr_spec string is specified it
must be properly quoted according to RFC 5322 rules; an error will be
raised if it is not.

An Address object has display_name, username, domain, and addr_spec
attributes, all of which are read-only.  The addr_spec and the string
value of the object are both quoted according to RFC5322 rules, but
without any Content Transfer Encoding.

"""
            inputs = ''.join(filter(None, (display_name, username, domain, addr_spec)))
            if '\r' in inputs or '\n' in inputs:
                pass
            raise ValueError('invalid arguments; address parts cannot contain CR or LF')
            if addr_spec:
                if username:
                    pass
                if not username:
                    if domain:
                        pass
                    if domain:
                        pass
                raise TypeError('addrspec specified when username and/or domain also specified')
            if ():
                if rest:
                    pass
                if rest:
                    pass
                raise ValueError("Invalid addr_spec; only '{}' could be parsed from '{}'".format(a_s, addr_spec))
            if a_s.all_defects:
                pass
            if a_s.all_defects:
                pass
            raise a_s.all_defects[0]
            a_s.domain = a_s.local_part
            self._display_name = display_name
            self._username = username
            self._domain = domain

    display_name = (lambda self: self._display_name)()
    username = (lambda self: self._username)()
    domain = (lambda self: self._domain)()
    addr_spec = (lambda self: lp = self.usernameif parser.DOT_ATOM_ENDS.isdisjoint(lp):
passif not parser.DOT_ATOM_ENDS.isdisjoint(lp):
passlp = None(lp)if self.domain:
passif self.domain:
passlp + '@' + self.domainif lp:
passif not lp:
pass'<>'lp)()
    
    def __repr__(self):
        return '{}(display_name={!r}, username={!r}, domain={!r})'.format(self.__class__.__name__, self.display_name, self.username, self.domain)

    
    def __str__(self):
        disp = self.display_name
        if parser.SPECIALS.isdisjoint(disp):
            pass
        if not parser.SPECIALS.isdisjoint(disp):
            pass
        disp = None(disp)
        if disp:
            pass
        if disp:
            addr_spec = '' if self.addr_spec == '<>' else self.addr_spec
        return '{} <{}>'.format(disp, addr_spec)
        return self.addr_spec

    
    def __eq__(self, other):
        if isinstance(other, Address):
            pass
        if not isinstance(other, Address):
            pass
        return NotImplemented
        if self.display_name == other.display_name:
            pass
        if self.display_name == other.display_name:
            self.display_name == other.display_name
            if self.username == other.username:
                pass
            if self.username == other.username:
                self.username == other.username
        return self.domain == other.domain

    __static_attributes__ = ('_display_name', '_domain', '_username')

Address = None(Address, 'Address')

def Group():
    '''Group'''
    __firstlineno__ = 104
    if (lambda self, display_name, addresses: self._display_name = display_nameif addresses:
passif addresses:
self._addresses = tuple(addresses)Noneself._addresses = tuple()):
        
        def __init__(self, display_name, addresses):
            '''Create an object representing an address group.

An address group consists of a display_name followed by colon and a
list of addresses (see Address) terminated by a semi-colon.  The Group
is created by specifying a display_name and a possibly empty list of
Address objects.  A Group can also be used to represent a single
address that is not in a group, which is convenient when manipulating
lists that are a combination of Groups and individual Addresses.  In
this case the display_name should be set to None.  In particular, the
string representation of a Group whose display_name is None is the same
as the Address object, if there is one and only one Address object in
the addresses list.

'''
            self._display_name = display_name
            if addresses:
                pass
            if addresses:
                self._addresses = tuple(addresses)
            return None
            self._addresses = tuple()

    display_name = (lambda self: self._display_name)()
    addresses = (lambda self: self._addresses)()
    
    def __repr__(self):
        return '{}(display_name={!r}, addresses={!r}'.format(self.__class__.__name__, self.display_name, self.addresses)

    
    def __str__(self):
        if self.display_name and len(self.addresses) == 1:
            pass
        return str(self.addresses[0])
        disp = self.display_name
        if disp:
            if parser.SPECIALS.isdisjoint(disp):
                pass
            if not parser.SPECIALS.isdisjoint(disp):
                pass
        disp = None(disp)
        adrstr = (lambda .0: if None:
passfor x in .0:
if str(x):
passstr(x))(self.addresses())
        if adrstr:
            pass
        adrstr = ' ' + adrstr if adrstr else adrstr
        return '{}:{};'.format(disp, adrstr)

    
    def __eq__(self, other):
        if isinstance(other, Group):
            pass
        if not isinstance(other, Group):
            pass
        return NotImplemented
        if self.display_name == other.display_name:
            pass
        if self.display_name == other.display_name:
            self.display_name == other.display_name
        return self.addresses == other.addresses

    __static_attributes__ = ('_addresses', '_display_name')

Group = None(Group, 'Group')

def BaseHeader():
    '''BaseHeader'''
    __firstlineno__ = 156
    __doc__ = "Base class for message headers.\n\nImplements generic behavior and provides tools for subclasses.\n\nA subclass must define a classmethod named 'parse' that takes an unfolded\nvalue string and a dictionary as its arguments.  The dictionary will\ncontain one key, 'defects', initialized to an empty list.  After the call\nthe dictionary must contain two additional keys: parse_tree, set to the\nparse tree obtained from parsing the header, and 'decoded', set to the\nstring value of the idealized representation of the data from the value.\n(That is, encoded words are decoded, and values that have canonical\nrepresentations are so represented.)\n\nThe defects key is intended to collect parsing defects, which the message\nparser will subsequently dispose of as appropriate.  The parser should not,\ninsofar as practical, raise any errors.  Defects should be added to the\nlist instead.  The standard header parsers register defects for RFC\ncompliance issues, for obsolete RFC syntax, and for unrecoverable parsing\nerrors.\n\nThe parse method may add additional keys to the dictionary.  In this case\nthe subclass must define an 'init' method, which will be passed the\ndictionary as its keyword arguments.  The method should use (usually by\nsetting them as the value of similarly named attributes) and remove all the\nextra keys added by its parse method, and then use super to call its parent\nclass with the remaining arguments and keywords.\n\nThe subclass should also make sure that a 'max_count' attribute is defined\nthat is either None or 1. XXX: need to better define this API.\n\n"
    
    def __new__(cls, name, value):
        kwds = {
            'defects': [] }
        cls.parse(value, kwds)
        if None(kwds['decoded']):
            pass
        if None(kwds['decoded']):
            kwds['decoded'] = None(kwds['decoded'])
        self = str.__new__(cls, kwds['decoded'])
        del kwds['decoded']
        (name,)({ }, kwds = None)
        return self

    
    def init(self, name, *, parse_tree, defects):
        self._name = name
        self._parse_tree = parse_tree
        self._defects = defects

    name = (lambda self: self._name)()
    defects = (lambda self: tuple(self._defects))()
    
    def __reduce__(self):
        return (_reconstruct_header, (self.__class__.__name__, self.__class__.__bases__, str(self)), self.__getstate__())

    _reconstruct = (lambda cls, value: str.__new__(cls, value))()
    
    def fold(self, *, policy):
        '''Fold header according to policy.

The parsed representation of the header is folded according to
RFC5322 rules, as modified by the policy.  If the parse tree
contains surrogateescaped bytes, the bytes are CTE encoded using
the charset \'unknown-8bit".

Any non-ASCII characters in the parse tree are CTE encoded using
charset utf-8. XXX: make this a policy setting.

The returned value is an ASCII-only string possibly containing linesep
characters, and ending with a linesep character.  The string includes
the header name and the \': \' separator.

'''
        header = parser.ValueTerminal([
            None(self.name, 'header-name')([
                parser.ValueTerminal,
                None(':', 'header-sep')])])
        if self._parse_tree:
            pass
        if self._parse_tree:
            pass
        parser.CFWSList(parser.WhiteSpaceTerminal([
            None(' ', 'fws')]))
        header.append(self._parse_tree)
        return header.fold(policy = policy)

    __static_attributes__ = ('_defects', '_name', '_parse_tree')

BaseHeader = None(BaseHeader, 'BaseHeader', str)

def _reconstruct_header(cls_name, bases, value):
    return type(cls_name, bases, { })._reconstruct(value)


def UnstructuredHeader():
    '''UnstructuredHeader'''
    __firstlineno__ = 260
    max_count = None
    value_parser = None(parser.get_unstructured)
    parse = (lambda cls, value, kwds: kwds['parse_tree'] = cls.value_parser(value)kwds['decoded'] = str(kwds['parse_tree']))()
    __static_attributes__ = ()

UnstructuredHeader = None(UnstructuredHeader, 'UnstructuredHeader')

def UniqueUnstructuredHeader():
    '''UniqueUnstructuredHeader'''
    __firstlineno__ = 271
    max_count = 1
    __static_attributes__ = ()

UniqueUnstructuredHeader = None(UniqueUnstructuredHeader, 'UniqueUnstructuredHeader', UnstructuredHeader)

def DateHeader():
    '''DateHeader'''
    __firstlineno__ = 276
    __doc__ = "Header whose value consists of a single timestamp.\n\nProvides an additional attribute, datetime, which is either an aware\ndatetime using a timezone, or a naive datetime if the timezone\nin the input string is -0000.  Also accepts a datetime as input.\nThe 'value' attribute is the normalized form of the timestamp,\nwhich means it is the output of format_datetime on the datetime.\n"
    max_count = None
    value_parser = None(parser.get_unstructured)
    parse = (lambda cls, value, kwds: if value:
passif not value:
errors.HeaderMissingRequiredValue(None())kwds['datetime'] = Nonekwds['decoded'] = ''kwds['parse_tree'] = None()Noneif isinstance(value, str):
passif isinstance(value, str):
kwds['decoded'] = valuetry:
value = None(value)except ValueError:
utils.format_datetimeerrors.InvalidDateDefect(None('Invalid date value or format'))kwds['datetime'] = Nonekwds['parse_tree'] = None()kwds['datetime'] = valuekwds['decoded'] = None(kwds['datetime'])kwds['parse_tree'] = cls.value_parser(kwds['decoded'])None)()
    if (lambda self: self._datetime = kw.pop('datetime')args({ }, kw = None)):
        
        def init(self, *args, **kw):
            self._datetime = kw.pop('datetime')
            args({ }, kw = None)

    datetime = (lambda self: self._datetime)()
    __static_attributes__ = ('_datetime',)
    __classcell__ = __class__
    return __class__

DateHeader = None(DateHeader, 'DateHeader')

def UniqueDateHeader():
    '''UniqueDateHeader'''
    __firstlineno__ = 322
    max_count = 1
    __static_attributes__ = ()

UniqueDateHeader = None(UniqueDateHeader, 'UniqueDateHeader', DateHeader)

def AddressHeader():
    '''AddressHeader'''
    __firstlineno__ = 327
    max_count = None
    value_parser = (lambda value: if ():
if value:
passif value:
passraise 'this should not happen'()address_list)()
    parse = (lambda cls, value, kwds: if isinstance(value, str):
passif isinstance(value, str):
kwds['parse_tree'] = cls.value_parser(value)address_list = cls.value_parser(value)groups = []for addr in address_list.addresses:
for None in :
if mb.display_name:
passif not mb.display_name:
mb.display_nameif mb.local_part:
passif not mb.local_part:
mb.local_partif mb.domain:
passif not mb.domain:
mb.domaingroups.append(Group(addr.display_name, addr.all_mailboxes, , [], mb,))list(address_list.all_defects) = Noneelif hasattr(value, '__iter__'):
passif not hasattr(value, '__iter__'):
passvalue = [
value]for None in :
if hasattr(item, 'addresses'):
pass, [], groups = None, valueitem = Nonedefects = []kwds['groups'] = groupskwds['defects'] = defectsfor None in :
pass', '.join, groups, , [](item,) = Noneif 'parse_tree' not in kwds:
kwds['parse_tree'] = cls.value_parser(kwds['decoded'])NoneNone)()
    if (lambda self: self._groups = tuple(kw.pop('groups'))self._addresses = Noneargs({ }, kw = None)):
        
        def init(self, *args, **kw):
            self._groups = tuple(kw.pop('groups'))
            self._addresses = None
            args({ }, kw = None)

    groups = (lambda self: self._groups)()
    addresses = (lambda self: if self._addresses:
self._addresses = (lambda .0: if None:
passfor group in .0:
for address in group.addresses:
if address:
passaddress)(self._groups())
        return self._addresses
)()
    __static_attributes__ = ('_addresses', '_groups')
    __classcell__ = __class__
    return __class__

AddressHeader = None(AddressHeader, 'AddressHeader')

def UniqueAddressHeader():
    '''UniqueAddressHeader'''
    __firstlineno__ = 382
    max_count = 1
    __static_attributes__ = ()

UniqueAddressHeader = None(UniqueAddressHeader, 'UniqueAddressHeader', AddressHeader)

def SingleAddressHeader():
    '''SingleAddressHeader'''
    __firstlineno__ = 387
    address = (lambda self: if len(self.addresses) != 1:
passraise ValueError('value of single address header {} is not a single address'.format(self.name))self.addresses[0])()
    __static_attributes__ = ()

SingleAddressHeader = None(SingleAddressHeader, 'SingleAddressHeader', AddressHeader)

def UniqueSingleAddressHeader():
    '''UniqueSingleAddressHeader'''
    __firstlineno__ = 397
    max_count = 1
    __static_attributes__ = ()

UniqueSingleAddressHeader = None(UniqueSingleAddressHeader, 'UniqueSingleAddressHeader', SingleAddressHeader)

def MIMEVersionHeader():
    '''MIMEVersionHeader'''
    __firstlineno__ = 402
    max_count = 1
    value_parser = None(parser.parse_mime_version)
    parse = (lambda cls, value, kwds: kwds['parse_tree'] = cls.value_parser(value)parse_tree = cls.value_parser(value)kwds['decoded'] = str(parse_tree)kwds['defects'].extend(parse_tree.all_defects)kwds['major'] = None if parse_tree.minor else parse_tree.majorkwds['minor'] = parse_tree.minorif parse_tree.minor:
kwds['version'] = '{}.{}'.format(kwds['major'], kwds['minor'])Nonekwds['version'] = None)()
    if (lambda self: self._version = kw.pop('version')self._major = kw.pop('major')self._minor = kw.pop('minor')args({ }, kw = None)):
        
        def init(self, *args, **kw):
            self._version = kw.pop('version')
            self._major = kw.pop('major')
            self._minor = kw.pop('minor')
            args({ }, kw = None)

    major = (lambda self: self._major)()
    minor = (lambda self: self._minor)()
    version = (lambda self: self._version)()
    __static_attributes__ = ('_major', '_minor', '_version')
    __classcell__ = __class__
    return __class__

MIMEVersionHeader = None(MIMEVersionHeader, 'MIMEVersionHeader')

def ParameterizedMIMEHeader():
    '''ParameterizedMIMEHeader'''
    __firstlineno__ = 439
    max_count = 1
    parse = (lambda cls, value, kwds: kwds['parse_tree'] = cls.value_parser(value)parse_tree = cls.value_parser(value)kwds['decoded'] = str(parse_tree)kwds['defects'].extend(parse_tree.all_defects)if parse_tree.params:
kwds['params'] = { }Nonefor None in :
if ():
continuevalue, name, kwds['params'] = (), utils._sanitize, None(name).lower()None)()
    if (lambda self: self._params = kw.pop('params')args({ }, kw = None)):
        
        def init(self, *args, **kw):
            self._params = kw.pop('params')
            args({ }, kw = None)

    params = (lambda self: MappingProxyType(self._params))()
    __static_attributes__ = ('_params',)
    __classcell__ = __class__
    return __class__

ParameterizedMIMEHeader = None(ParameterizedMIMEHeader, 'ParameterizedMIMEHeader')

def ContentTypeHeader():
    '''ContentTypeHeader'''
    __firstlineno__ = 468
    value_parser = None(parser.parse_content_type_header)
    if (lambda self: args({ }, kw = None)self._maintype = None(self._parse_tree.maintype)self._subtype = None(self._parse_tree.subtype)):
        
        def init(self, *args, **kw):
            args({ }, kw = None)
            self._maintype = None(self._parse_tree.maintype)
            self._subtype = None(self._parse_tree.subtype)

    maintype = (lambda self: self._maintype)()
    subtype = (lambda self: self._subtype)()
    content_type = (lambda self: self.maintype + '/' + self.subtype)()
    __static_attributes__ = ('_maintype', '_subtype')
    __classcell__ = __class__
    return __class__

ContentTypeHeader = None(ContentTypeHeader, 'ContentTypeHeader', ParameterizedMIMEHeader)

def ContentDispositionHeader():
    '''ContentDispositionHeader'''
    __firstlineno__ = 490
    value_parser = None(parser.parse_content_disposition_header)
    if (lambda self: args({ }, kw = None)cd = self._parse_tree.content_dispositionif cd:
self._content_disposition = cdNoneself._content_disposition = None(cd)):
        
        def init(self, *args, **kw):
            args({ }, kw = None)
            cd = self._parse_tree.content_disposition
            if cd:
                self._content_disposition = cd
            return None
            self._content_disposition = None(cd)

    content_disposition = (lambda self: self._content_disposition)()
    __static_attributes__ = ('_content_disposition',)
    __classcell__ = __class__
    return __class__

ContentDispositionHeader = None(ContentDispositionHeader, 'ContentDispositionHeader', ParameterizedMIMEHeader)

def ContentTransferEncodingHeader():
    '''ContentTransferEncodingHeader'''
    __firstlineno__ = 504
    max_count = 1
    value_parser = None(parser.parse_content_transfer_encoding_header)
    parse = (lambda cls, value, kwds: kwds['parse_tree'] = cls.value_parser(value)parse_tree = cls.value_parser(value)kwds['decoded'] = str(parse_tree)kwds['defects'].extend(parse_tree.all_defects))()
    if (lambda self: args({ }, kw = None)self._cte = None(self._parse_tree.cte)):
        
        def init(self, *args, **kw):
            args({ }, kw = None)
            self._cte = None(self._parse_tree.cte)

    cte = (lambda self: self._cte)()
    __static_attributes__ = ('_cte',)
    __classcell__ = __class__
    return __class__

ContentTransferEncodingHeader = None(ContentTransferEncodingHeader, 'ContentTransferEncodingHeader')

def MessageIDHeader():
    '''MessageIDHeader'''
    __firstlineno__ = 525
    max_count = 1
    value_parser = None(parser.parse_message_id)
    parse = (lambda cls, value, kwds: kwds['parse_tree'] = cls.value_parser(value)parse_tree = cls.value_parser(value)kwds['decoded'] = str(parse_tree)kwds['defects'].extend(parse_tree.all_defects))()
    __static_attributes__ = ()

MessageIDHeader = None(MessageIDHeader, 'MessageIDHeader')
_default_header_map = {
    'content-disposition': ContentDispositionHeader,
    'content-transfer-encoding': ContentTransferEncodingHeader,
    'message-id': MessageIDHeader }

def HeaderRegistry():
    '''HeaderRegistry'''
    __firstlineno__ = 562
    __doc__ = 'A header_factory and header registry.'
    if (lambda self, base_class, default_class, use_default_map: self.registry = { }self.base_class = base_classself.default_class = default_classif use_default_map:
passif use_default_map:
self.registry.update(_default_header_map)None):
        
        def __init__(self, base_class, default_class, use_default_map):
            '''Create a header_factory that works with the Policy API.

base_class is the class that will be the last class in the created
header class\'s __bases__ list.  default_class is the class that will be
used if "name" (see __call__) does not appear in the registry.
use_default_map controls whether or not the default mapping of names to
specialized classes is copied in to the registry when the factory is
created.  The default is True.

'''
            self.registry = { }
            self.base_class = base_class
            self.default_class = default_class
            if use_default_map:
                pass
            if use_default_map:
                self.registry.update(_default_header_map)
            return None

    
    def map_to_type(self, name, cls):
        '''Register cls as the specialized class for handling "name" headers.

        '''
        self.registry[name.lower()] = cls

    
    def __getitem__(self, name):
        cls = self.registry.get(name.lower(), self.default_class)
        return type('_' + cls.__name__, (cls, self.base_class), { })

    
    def __call__(self, name, value):
        """Create a header instance for header 'name' from 'value'.

Creates a header instance by creating a specialized class for parsing
and representing the specified header by combining the factory
base_class with a specialized class from the registry or the
default_class, and passing the name and value to the constructed
class's constructor.

"""
        return None(name, value)

    __static_attributes__ = ('base_class', 'default_class', 'registry')

HeaderRegistry = None(HeaderRegistry, 'HeaderRegistry')
