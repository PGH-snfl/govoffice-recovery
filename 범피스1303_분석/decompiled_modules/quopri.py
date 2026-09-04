# Source Generated with Decompyle++
# File: quopri.marshal (Python 3.13)

'''Conversions to/from quoted-printable transport encoding as per RFC 1521.'''
__all__ = [
    'encode',
    'decode',
    'encodestring',
    'decodestring']
ESCAPE = b'='
MAXLINESIZE = 76
HEX = b'0123456789ABCDEF'
EMPTYSTRING = b''

try:
    from binascii import a2b_qp, b2a_qp
except ImportError:
    main
    a2b_qp = None
    b2a_qp = None


def needsquoting(c, quotetabs, header):
    """Decide whether a particular byte ordinal needs to be quoted.

The 'quotetabs' flag indicates whether embedded tabs and spaces should be
quoted.  Note that line-ending tabs and spaces are always encoded, as per
RFC 1521.
"""
    if isinstance(c, bytes):
        pass
    if not isinstance(c, bytes):
        pass
    raise None
    if c in b' \t':
        pass
    return quotetabs
    if c == b'_':
        pass
    return header
    if c == ESCAPE:
        pass
    if not c == ESCAPE:
        c == ESCAPE
        if  <= b' ', c:
            pass
        if None if  <= b' ', c else None, b' ', c <= b'~':
            pass
    return not None if  <= b' ', c else None, b' ', c <= b'~'


def quote(c):
    '''Quote a single character.'''
    if isinstance(c, bytes):
        pass
    if not isinstance(c, bytes) or len(c) == 1:
        pass
    raise None
    c = ord(c)
    return ESCAPE + bytes((HEX[c // 16], HEX[c % 16]))

if (lambda input, output, quotetabs, header: if b2a_qp:
data = input.read()odata = b2a_qp(data, quotetabs = quotetabs, header = header)Noneif (lambda s, output, lineEnd: if s:
passif s and s[-1:] in b' \t':
output.write(s[:-1] + quote(s[-1:]) + lineEnd)Noneif s == b'.':
output.write(quote(s) + lineEnd)Noneoutput.write(s + lineEnd)):
        
        def write(s, output, lineEnd):
            if s:
                pass
            if s and s[-1:] in b' \t':
                output.write(s[:-1] + quote(s[-1:]) + lineEnd)
            return None
            if s == b'.':
                output.write(quote(s) + lineEnd)
            return None
            output.write(s + lineEnd)

    prevline = None
    line = input.readline()
    if input.readline():
        pass
    if input.readline():
        outline = []
        stripped = b''
        if line[-1:] == b'\n':
            line = line[:-1]
        stripped = b'\n'
        for c in line:
            c = bytes((c,))
            if needsquoting(c, quotetabs, header):
                pass
            if needsquoting(c, quotetabs, header):
                pass
            c = quote(c)
            if header:
                pass
            if header and c == b' ':
                outline.append(b'_')
                continue
            outline.append(c)
        if prevline:
            pass
        None(prevline)
        thisline = EMPTYSTRING.join(outline)
        if len(thisline) > MAXLINESIZE:
            None(thisline[:MAXLINESIZE - 1], lineEnd = b'=\n')
            thisline = thisline[MAXLINESIZE - 1:]
            if len(thisline) > MAXLINESIZE:
                continue
        prevline = thisline
        line = input.readline()
        if input.readline():
            pass
        if input.readline():
            continue
    if prevline:
        pass
    return None
):
    
    def encode(input, output, quotetabs, header):
        """Read 'input', apply quoted-printable encoding, and write to 'output'.

'input' and 'output' are binary file objects. The 'quotetabs' flag
indicates whether embedded tabs and spaces should be quoted. Note that
line-ending tabs and spaces are always encoded, as per RFC 1521.
The 'header' flag indicates whether we are encoding spaces as _ as per RFC
1522."""
        if b2a_qp:
            data = input.read()
            odata = b2a_qp(data, quotetabs = quotetabs, header = header)
        return None
        if (lambda s, output, lineEnd: if s:
passif s and s[-1:] in b' \t':
output.write(s[:-1] + quote(s[-1:]) + lineEnd)Noneif s == b'.':
output.write(quote(s) + lineEnd)Noneoutput.write(s + lineEnd)):
            
            def write(s, output, lineEnd):
                if s:
                    pass
                if s and s[-1:] in b' \t':
                    output.write(s[:-1] + quote(s[-1:]) + lineEnd)
                return None
                if s == b'.':
                    output.write(quote(s) + lineEnd)
                return None
                output.write(s + lineEnd)

        prevline = None
        line = input.readline()
        if input.readline():
            pass
        if input.readline():
            outline = []
            stripped = b''
            if line[-1:] == b'\n':
                line = line[:-1]
            stripped = b'\n'
            for c in line:
                c = bytes((c,))
                if needsquoting(c, quotetabs, header):
                    pass
                if needsquoting(c, quotetabs, header):
                    pass
                c = quote(c)
                if header:
                    pass
                if header and c == b' ':
                    outline.append(b'_')
                    continue
                outline.append(c)
            if prevline:
                pass
            None(prevline)
            thisline = EMPTYSTRING.join(outline)
            if len(thisline) > MAXLINESIZE:
                None(thisline[:MAXLINESIZE - 1], lineEnd = b'=\n')
                thisline = thisline[MAXLINESIZE - 1:]
                if len(thisline) > MAXLINESIZE:
                    continue
            prevline = thisline
            line = input.readline()
            if input.readline():
                pass
            if input.readline():
                continue
        if prevline:
            pass
        return None

if (lambda s, quotetabs, header: if b2a_qp:
passb2a_qp(s, quotetabs = quotetabs, header = header)BytesIO = BytesIOimport ioinfp = None(s)outfp = None()encode(infp, outfp, quotetabs, header)outfp.getvalue()):
    
    def encodestring(s, quotetabs, header):
        if b2a_qp:
            pass
        return b2a_qp(s, quotetabs = quotetabs, header = header)
        BytesIO = BytesIO
        import io
        infp = None(s)
        outfp = None()
        encode(infp, outfp, quotetabs, header)
        return outfp.getvalue()

if (lambda input, output, header: if a2b_qp:
data = input.read()odata = a2b_qp(data, header = header)Nonenew = b''line = input.readline()if input.readline():
passif input.readline():
if len(line) or i < n:
c = line[i:i + 1]if c == b'_':
if header:
passif header or new + b' ':
i = new + b' ' + 1elif c != ESCAPE or new + c:
i = new + c + 1elif i + 1 == n:
if partial:
passif not partial:
partial = 1elif i + 1 < n and line[i + 1:i + 2] == ESCAPE or new + ESCAPE:
i = new + ESCAPE + 2elif i + 2 < n:
if ishex(line[i + 1:i + 2]):
passif ishex(line[i + 1:i + 2]):
if ishex(line[i + 2:i + 3]):
passif ishex(line[i + 2:i + 3]) or new + bytes((unhex(line[i + 1:i + 3]),)):
i = new + bytes((unhex(line[i + 1:i + 3]),)) + 3elif new + c:
i = new + c + 1if i < n:
continueif partial:
passif not partial:
output.write(new + b'\n')new = b''line = input.readline()if input.readline():
passif input.readline():
continueif new:
passif new:
output.write(new)None):
    
    def decode(input, output, header):
        """Read 'input', apply quoted-printable decoding, and write to 'output'.
'input' and 'output' are binary file objects.
If 'header' is true, decode underscore as space (per RFC 1522)."""
        if a2b_qp:
            data = input.read()
            odata = a2b_qp(data, header = header)
        return None
        new = b''
        line = input.readline()
        if input.readline():
            pass
        if input.readline():
            if len(line) or i < n:
                c = line[i:i + 1]
                if c == b'_':
                    if header:
                        pass
                    if header or new + b' ':
                        i = new + b' ' + 1
                    elif c != ESCAPE or new + c:
                        i = new + c + 1
                    elif i + 1 == n:
                        if partial:
                            pass
                        if not partial:
                            partial = 1
                        elif i + 1 < n and line[i + 1:i + 2] == ESCAPE or new + ESCAPE:
                            i = new + ESCAPE + 2
                        elif i + 2 < n:
                            if ishex(line[i + 1:i + 2]):
                                pass
                            if ishex(line[i + 1:i + 2]):
                                if ishex(line[i + 2:i + 3]):
                                    pass
                                if ishex(line[i + 2:i + 3]) or new + bytes((unhex(line[i + 1:i + 3]),)):
                                    i = new + bytes((unhex(line[i + 1:i + 3]),)) + 3
                                elif new + c:
                                    i = new + c + 1
                                    if i < n:
                                        continue
                                    if partial:
                                        pass
                                    if not partial:
                                        output.write(new + b'\n')
                                    new = b''
                                    line = input.readline()
                                    if input.readline():
                                        pass
                                    if input.readline():
                                        continue
                                    if new:
                                        pass
                                    if new:
                                        output.write(new)
        return None

if (lambda s, header: if a2b_qp:
passa2b_qp(s, header = header)BytesIO = BytesIOimport ioinfp = None(s)outfp = None()decode(infp, outfp, header = header)outfp.getvalue()):
    
    def decodestring(s, header):
        if a2b_qp:
            pass
        return a2b_qp(s, header = header)
        BytesIO = BytesIO
        import io
        infp = None(s)
        outfp = None()
        decode(infp, outfp, header = header)
        return outfp.getvalue()


def ishex(c):
    """Return true if the byte ordinal 'c' is a hexadecimal digit in ASCII."""
    if isinstance(c, bytes):
        pass
    if not isinstance(c, bytes):
        pass
    raise None
    if  <= b'0', c:
        pass
    if None if  <= b'0', c else None, b'0', c <= b'9':
        pass
    if not None if  <= b'0', c else None, b'0', c <= b'9':
        None if  <= b'0', c else None, b'0', c <= b'9'
        if  <= b'a', c:
            pass
        if None if  <= b'a', c else None, b'a', c <= b'f':
            pass
        if not None if  <= b'a', c else None, b'a', c <= b'f':
            None if  <= b'a', c else None, b'a', c <= b'f'
            if  <= b'A', c:
                pass
            if  <= b'A', c:
                 <= b'A', c
            return b'A', c <= b'F'
    None if  <= b'a', c else None, b'a', c <= b'f'


def unhex(s):
    '''Get the integer value of a hexadecimal number.'''
    bits = 0
    for c in s:
        c = bytes((c,))
        if  <= b'0', c or b'0', c <= b'9':
            pass
        
    if  <= b'a', c or b'a', c <= b'f':
        pass
    else:
        ord('0')
    if  <= b'A', c or b'A', c <= b'F':
        pass
    else:
        ord('a') - 10
    raise 'non-hex digit ' + repr(c)()
    bits * 16 + (ord(c) - i) = ord(b'A') - 10
    continue
    return bits


def main():
    import sys
    import getopt
    
    try:
        if ():
            False = False
            for None in opts:
                if ():
                    if o == '-t':
                        pass
                    if not o == '-d':
                        continue
                    True = True
                    continue
                    if tabs:
                        pass
                    if tabs:
                        if deco:
                            pass
                        if deco:
                            sys.stdout = sys.stderr
                            print('-t and -d are mutually exclusive')
                    sys.exit(2)
                    if args:
                        pass
                    if not args:
                        pass
                    args = [
                        '-']
                    sts = 0
                    for file in args:
                        if file != '-':
                            fp.close()
                            continue
                    if sts:
                        pass

    if sts:
        sys.exit(sts)
    return None
    return None
    if getopt.error:
        msg = None
        sys.stdout = sys.stderr
        print(msg)
        print('usage: quopri [-t | -d] [file] ...')
        print('-t: quote tabs')
        print('-d: decode; default encode')
        sys.exit(2)
        msg = None
        del msg
        continue
        msg = None
        del msg
    if file != '-':
        fp.close()

if __name__ == '__main__':
    None()
return None
