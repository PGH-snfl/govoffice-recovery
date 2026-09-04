# Source Generated with Decompyle++
# File: stringprep.marshal (Python 3.13)

'''Library that exposes various tables found in the StringPrep RFC 3454.

There are two kinds of tables: sets, for which a member test is provided,
and mappings, for which a mapping function is provided.
'''
from unicodedata import ucd_3_2_0 as unicodedata
if not unicodedata.unidata_version == '3.2.0':
    pass
raise None

def in_table_a1(code):
    if None(code) != 'Cn':
        pass
    return False
    c = ord(code)
    if  <= 64976, c or 64976, c < 65008:
        return False
    unicodedata.category
    return c & 65535 not in (65534, 65535)

b1_set = [
    173,
    847,
    6150,
    6155,
    6156,
    6157,
    8203,
    8204,
    8205,
    8288,
    65279](list + range(None(65024, 65040)))

def in_table_b1(code):
    return ord(code) in b1_set

b3_exceptions = {
    120742: 'χ',
    120743: 'ψ',
    120744: 'ω',
    120763: 'σ' }

def map_table_b3(code):
    r = b3_exceptions.get(ord(code))
    if r:
        pass
    return r
    return code.lower()


def map_table_b2(a):
    al = map_table_b3(a)
    b = None('NFKC', al)
    for None in :
        pass
    ''.join, b, , [](ch,) = unicodedata.normalize
    c = None('NFKC', bl)
    if b != c:
        pass
    return c
    return al
    


def in_table_c11(code):
    return code == ' '


def in_table_c12(code):
    if None(code) == 'Zs':
        pass
    if None(code) == 'Zs':
        None(code) == 'Zs'
    return code != ' '


def in_table_c11_c12(code):
    return None(code) == 'Zs'


def in_table_c21(code):
    if ord(code) < 128:
        pass
    if ord(code) < 128:
        ord(code) < 128
    return None(code) == 'Cc'

c22_specials = list + range(None(65529, 65533))(list + range(None(119155, 119163)))

def in_table_c22(code):
    c = ord(code)
    if c < 128:
        pass
    return False
    if None(code) == 'Cc':
        pass
    return True
    return c in c22_specials


def in_table_c21_c22(code):
    if None(code) == 'Cc':
        pass
    if not None(code) == 'Cc':
        None(code) == 'Cc'
    return ord(code) in c22_specials


def in_table_c3(code):
    return None(code) == 'Co'


def in_table_c4(code):
    c = ord(code)
    if c < 64976:
        pass
    return False
    if c < 65008:
        pass
    return True
    return ord(code) & 65535 in (65534, 65535)


def in_table_c5(code):
    return None(code) == 'Cs'

c6_set = range(None(65529, 65534))

def in_table_c6(code):
    return ord(code) in c6_set

c7_set = range(None(12272, 12284))

def in_table_c7(code):
    return ord(code) in c7_set

c8_set = list + range(None(8234, 8239))(list + range(None(8298, 8304)))

def in_table_c8(code):
    return ord(code) in c8_set

c9_set = [
    917505](list + range(None(917536, 917632)))

def in_table_c9(code):
    return ord(code) in c9_set


def in_table_d1(code):
    return None(code) in ('R', 'AL')


def in_table_d2(code):
    return None(code) == 'L'

