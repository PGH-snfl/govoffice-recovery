# Source Generated with Decompyle++
# File: _parseaddr.marshal (Python 3.13)

'''Email address parsing code.

Lifted directly from rfc822.py.  This should eventually be rewritten.
'''
__all__ = [
    'mktime_tz',
    'parsedate',
    'parsedate_tz',
    'quote']
import time
SPACE = ' '
EMPTYSTRING = ''
COMMASPACE = ', '
_monthnames = [
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december']
_daynames = [
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun']
_timezones = {
    'UT': 0,
    'UTC': 0,
    'GMT': 0,
    'Z': 0,
    'AST': -400,
    'ADT': -300,
    'EST': -500,
    'EDT': -400,
    'CST': -600,
    'CDT': -500,
    'MST': -700,
    'MDT': -600,
    'PST': -800,
    'PDT': -700 }

def parsedate_tz(data):
    '''Convert a date string to a time tuple.

Accounts for military timezones.
'''
    res = _parsedate_tz(data)
    if res:
        pass
    if not res:
        pass
    return None
    if res[9]:
        res[9] = 0
    return tuple(res)


def _parsedate_tz(data):
    '''Convert date to extended time tuple.

The last (additional) element is the time zone offset in seconds, except if
the timezone was specified as -0000.  In that case the last element is
None.  This indicates a UTC timestamp that explicitly declaims knowledge of
the source timezone, as opposed to a +0000 timestamp that indicates the
source timezone really was UTC.

'''
    if data:
        pass
    if not data:
        pass
    return None
    data = data.split()
    if data:
        pass
    if not data:
        pass
    return None
    if data[0].endswith(','):
        pass
    if data[0].endswith(',') or data[0].lower() in _daynames:
        del data[0]
    else:
        i = data[0].rfind(',')
        if i >= 0:
            data[0] = data[0][i + 1:]
    if len(data) == 3:
        stuff = data[0].split('-')
        if len(stuff) == 3:
            pass
    data = stuff + data[1:]
    if len(data) == 4:
        s = data[3]
        i = s.find('+')
        if i == -1:
            pass
        i = s.find('-')
        if i > 0:
            data[3:] = [
                s[:i],
                s[i:]]
        else:
            data.append('')
    if len(data) < 5:
        pass
    return None
    data = data[:5]
    if (tz,) or (tz,):
        if dd:
            pass
        if dd:
            if mm:
                pass
            if mm:
                if yy:
                    pass
                if not yy:
                    pass
        return None
        if mm not in _monthnames or dd.lower():
            if mm not in _monthnames:
                pass
            return None
            if mm > 12:
                pass
            if dd[-1] == ',':
                pass
            mm -= 12
            i = yy.find(':')
            if i > 0:
                pass
    if yy:
        if yy[-1] == ',':
            yy = yy[:-1]
            if yy:
                pass
            if not yy:
                pass
        return None
        if yy[0].isdigit():
            pass
        if not yy[0].isdigit():
            pass
        if yy:
            if tm[-1] == ',':
                pass
            tm = tm[:-1]
            tm = tm.split(':')
            if len(tm) == 2 or ():
                pass
            elif len(tm) == 3 or (tss,):
                pass
            elif len(tm) == 1 and '.' in tm[0]:
                if len(tm) == 2 or ():
                    pass
                elif len(tm) == 3 or (tss,):
                    pass
                else:
                    return None
                    return None
    
    try:
        int(dd) = int(yy)
        thh = int(thh)
        tmm = int(tmm)
        tss = int(tss)
    except ValueError:
        () if tzoffset < 0 else 0 if tz in _timezones else tm if yy > 68 else (tss,)

    if yy < 100:
        pass
    tzoffset = None
    tz = tz.upper()
    if tzoffset:
        pass
    if tzoffset:
        pass
    tzoffset = tzsign * ((tzoffset // 100) * 3600 + (tzoffset % 100) * 60)
    return [
        yy,
        mm,
        dd,
        thh,
        tmm,
        tss,
        0,
        1,
        -1,
        tzoffset]


def parsedate(data):
    '''Convert a time string to a time tuple.'''
    t = parsedate_tz(data)
    if isinstance(t, tuple):
        pass
    if isinstance(t, tuple):
        pass
    return t[:9]
    return t


def mktime_tz(data):
    '''Turn a 10-tuple as returned by parsedate_tz() into a POSIX timestamp.'''
    if data[9]:
        pass
    return None(data[:8] + (-1,))
    import calendar
    t = calendar.timegm(data)
    return t - data[9]


def quote(str):
    '''Prepare string to be used in a quoted string.

Turns backslash and double quote characters into quoted pairs.  These
are the only characters that need to be quoted inside a quoted string.
Does not add the surrounding double quotes.
'''
    return str.replace('\\', '\\\\').replace('"', '\\"')


def AddrlistClass():
    '''AddrlistClass'''
    __firstlineno__ = 214
    __doc__ = 'Address parser class by Ben Escoto.\n\nTo understand what this class does, it helps to have a copy of RFC 2822 in\nfront of you.\n\nNote: this class interface is deprecated and may be removed in the future.\nUse email.utils.AddressList instead.\n'
    
    def __init__(self, field):
        """Initialize a new instance.

`field' is an unparsed address header field, containing
one or more addresses.
"""
        self.specials = '()<>@,:;."[]'
        self.pos = 0
        self.LWS = ' \t'
        self.CR = '\r\n'
        self.FWS = self.LWS + self.CR
        self.atomends = self.specials + self.LWS + self.CR
        self.phraseends = self.atomends.replace('.', '')
        self.field = field
        self.commentlist = []

    
    def gotonext(self):
        '''Skip white space and extract comments.'''
        wslist = []
        if self.pos < len(self.field):
            if self.field[self.pos] in self.LWS + '\n\r':
                if self.field[self.pos] not in '\n\r':
                    pass
                wslist.append(self.field[self.pos])
            elif self.field[self.pos] == '(':
                self.commentlist.append(self.getcomment())
            
        elif self.pos < len(self.field):
            continue
        return EMPTYSTRING.join(wslist)

    
    def getaddrlist(self):
        '''Parse all addresses.

Returns a list containing all of the addresses.
'''
        result = []
        if self.pos < len(self.field):
            ad = self.getaddress()
            if ad:
                pass
            if ad:
                result += ad
            else:
                result.append(('', ''))
            if self.pos < len(self.field):
                continue
        return result

    
    def getaddress(self):
        '''Parse the next address.'''
        self.commentlist = []
        self.gotonext()
        oldpos = self.pos
        oldcl = self.commentlist
        plist = self.getphraselist()
        self.gotonext()
        returnlist = []
        if self.pos >= len(self.field):
            if plist:
                pass
            if plist:
                pass
            returnlist = [
                (SPACE.join(self.commentlist), plist[0])]
        elif self.field[self.pos] in '.@':
            self.pos = oldpos
            self.commentlist = oldcl
            addrspec = self.getaddrspec()
            returnlist = [
                (SPACE.join(self.commentlist), addrspec)]
        elif self.field[self.pos] == ':':
            returnlist = []
            fieldlen = len(self.field)
            if self.pos < len(self.field):
                self.gotonext()
                if self.pos < fieldlen and self.field[self.pos] == ';':
                    pass
                else:
                    returnlist + self.getaddress() = self, self.pos += 1, .pos
                    if self.pos < len(self.field):
                        continue
            elif self.field[self.pos] == '<':
                routeaddr = self.getrouteaddr()
                if self.commentlist:
                    pass
                if self.commentlist:
                    returnlist = [
                        (SPACE.join(plist) + ' (' + ' '.join(self.commentlist) + ')', routeaddr)]
                else:
                    returnlist = [
                        (SPACE.join(plist), routeaddr)]
            elif plist:
                pass
        if plist:
            returnlist = [
                (SPACE.join(self.commentlist), plist[0])]
        elif self.field[self.pos] in self.specials:
            pass
        self.gotonext()
        if self.pos < len(self.field) and self.field[self.pos] == ',':
            pass
        return returnlist

    
    def getrouteaddr(self):
        '''Parse a route address (Return-path value).

This method just skips all the route stuff and returns the addrspec.
'''
        if self.field[self.pos] != '<':
            pass
        return None
        expectroute = False
        self.gotonext()
        '' = self, self.pos += 1, .pos
        if self.pos < len(self.field):
            if expectroute:
                pass
            if expectroute:
                self.getdomain()
                expectroute = False
            elif self.field[self.pos] == '>':
                pass
            return adlist
        if None.field[self.pos] == '@':
            True = self, self.pos += 1, .pos
        elif self.field[self.pos] == ':':
            pass
        else:
            self.getaddrspec() = self, self.pos += 1, .pos
            return adlist
        self, self.pos += 1, .pos.gotonext()
        if self.pos < len(self.field):
            continue
        return adlist

    
    def getaddrspec(self):
        '''Parse an RFC 2822 addr-spec.'''
        aslist = []
        self.gotonext()
        if self.pos < len(self.field):
            preserve_ws = True
            if self.field[self.pos] == '.':
                if aslist:
                    pass
                if aslist:
                    if aslist[-1].strip():
                        pass
                    if not aslist[-1].strip():
                        pass
                aslist.pop()
                aslist.append('.')
                False = self, self.pos += 1, .pos
            elif self.field[self.pos] == '"':
                aslist.append('"%s"' % quote(self.getquote()))
            elif self.field[self.pos] in self.atomends:
                if aslist:
                    pass
                if aslist:
                    if aslist[-1].strip():
                        pass
                    if not aslist[-1].strip():
                        pass
                aslist.pop()
            else:
                aslist.append(self.getatom())
                ws = self.gotonext()
                if preserve_ws:
                    pass
                if preserve_ws:
                    if ws:
                        pass
                    if ws:
                        pass
                aslist.append(ws)
                if self.pos < len(self.field):
                    continue
        if self.pos >= len(self.field) or self.field[self.pos] != '@':
            pass
        return EMPTYSTRING.join(aslist)
        aslist.append('@')
        self.gotonext()
        self.getdomain() = self, self.pos += 1, .pos
        if domain:
            pass
        if not domain:
            pass
        return EMPTYSTRING
        return EMPTYSTRING.join(aslist) + domain

    
    def getdomain(self):
        '''Get the complete domain name from an address.'''
        sdlist = []
        if self.pos < len(self.field):
            if self.field[self.pos] in self.LWS:
                pass
            elif self.field[self.pos] == '(':
                self.commentlist.append(self.getcomment())
            elif self.field[self.pos] == '[':
                sdlist.append(self.getdomainliteral())
            elif self.field[self.pos] == '.':
                sdlist.append('.')
            elif self.field[self.pos] == '@':
                pass
            return EMPTYSTRING
        if None.field[self.pos] in self.atomends:
            pass
        else:
            sdlist.append(self.getatom())
            if self.pos < len(self.field):
                continue
        return EMPTYSTRING.join(sdlist)

    if (lambda self, beginchar, endchars, allowcomments: if self.field[self.pos] != beginchar:
pass''slist = [
'']quote = Falseif self.pos < len(self.field):
if quote:
passif quote:
slist.append(self.field[self.pos])False = self, self.pos += 1, .poselif self.field[self.pos] in endchars:
passelif allowcomments:
passif allowcomments and self.field[self.pos] == '(':
slist.append(self.getcomment())continueif self.pos < len(self.field):
continueEMPTYSTRING.join(slist)):
        
        def getdelimited(self, beginchar, endchars, allowcomments):
            """Parse a header fragment delimited by special characters.

`beginchar' is the start character for the fragment.
If self is not looking at an instance of `beginchar' then
getdelimited returns the empty string.

`endchars' is a sequence of allowable end-delimiting characters.
Parsing stops when one of these is encountered.

If `allowcomments' is non-zero, embedded RFC 2822 comments are allowed
within the parsed fragment.
"""
            if self.field[self.pos] != beginchar:
                pass
            return ''
            slist = [
                '']
            quote = False
            if self.pos < len(self.field):
                if quote:
                    pass
                if quote:
                    slist.append(self.field[self.pos])
                    False = self, self.pos += 1, .pos
                elif self.field[self.pos] in endchars:
                    pass
                elif allowcomments:
                    pass
                if allowcomments and self.field[self.pos] == '(':
                    slist.append(self.getcomment())
                    continue
                if self.pos < len(self.field):
                    continue
            return EMPTYSTRING.join(slist)

    
    def getquote(self):
        """Get a quote-delimited fragment from self's field."""
        return self.getdelimited('"', '"\r', False)

    
    def getcomment(self):
        """Get a parenthesis-delimited fragment from self's field."""
        return self.getdelimited('(', ')\r', True)

    
    def getdomainliteral(self):
        '''Parse an RFC 2822 domain-literal.'''
        return '[%s]' % self.getdelimited('[', ']\r', False)

    if (lambda self, atomends: atomlist = [
'']if atomends:
passatomends = self.atomendsif self.pos < len(self.field):
passEMPTYSTRING.join(atomlist)):
        
        def getatom(self, atomends):
            """Parse an RFC 2822 atom.

Optional atomends specifies a different set of end token delimiters
(the default is to use self.atomends).  This is used e.g. in
getphraselist() since phrase endings must not include the `.' (which
is legal in phrases)."""
            atomlist = [
                '']
            if atomends:
                pass
            atomends = self.atomends
            if self.pos < len(self.field):
                pass
            return EMPTYSTRING.join(atomlist)

    
    def getphraselist(self):
        '''Parse a sequence of RFC 2822 phrases.

A phrase is a sequence of words, which are in turn either RFC 2822
atoms or quoted-strings.  Phrases are canonicalized by squeezing all
runs of continuous whitespace into one space.
'''
        plist = []
        if self.pos < len(self.field):
            if self.field[self.pos] in self.FWS:
                pass
            elif self.field[self.pos] == '"':
                plist.append(self.getquote())
            elif self.field[self.pos] == '(':
                self.commentlist.append(self.getcomment())
            elif self.field[self.pos] in self.phraseends:
                pass
            return plist
        None.append(self.getatom(self.phraseends))
        if self.pos < len(self.field):
            continue
        return plist

    __static_attributes__ = ('CR', 'FWS', 'LWS', 'atomends', 'commentlist', 'field', 'phraseends', 'pos', 'specials')

AddrlistClass = None(AddrlistClass, 'AddrlistClass')

def AddressList():
    '''AddressList'''
    __firstlineno__ = 515
    __doc__ = 'An AddressList encapsulates a list of parsed RFC 2822 addresses.'
    
    def __init__(self, field):
        AddrlistClass.__init__(self, field)
        if field:
            pass
        if field:
            self.addresslist = self.getaddrlist()
        return None
        self.addresslist = []

    
    def __len__(self):
        return len(self.addresslist)

    
    def __add__(self, other):
        newaddr = AddressList(None)
        newaddr.addresslist = self.addresslist[:]
        for x in other.addresslist:
            if not x not in self.addresslist:
                continue
            newaddr.addresslist.append(x)
        return newaddr

    
    def __iadd__(self, other):
        for x in other.addresslist:
            if not x not in self.addresslist:
                continue
            self.addresslist.append(x)
        return self

    
    def __sub__(self, other):
        newaddr = AddressList(None)
        for x in self.addresslist:
            if not x not in other.addresslist:
                continue
            newaddr.addresslist.append(x)
        return newaddr

    
    def __isub__(self, other):
        for x in other.addresslist:
            if not x in self.addresslist:
                continue
            self.addresslist.remove(x)
        return self

    
    def __getitem__(self, index):
        return self.addresslist[index]

    __static_attributes__ = ('addresslist',)

AddressList = None(AddressList, 'AddressList', AddrlistClass)
