# Source Generated with Decompyle++
# File: ipaddress.marshal (Python 3.13)

'''A fast, lightweight IPv4/IPv6 manipulation library in Python.

This library is used to create/poke/manipulate IPv4 and IPv6 addresses
and networks.

'''
__version__ = '1.0'
import functools
IPV4LENGTH = 32
IPV6LENGTH = 128

def AddressValueError():
    '''AddressValueError'''
    __firstlineno__ = 20
    __doc__ = 'A Value Error related to the address.'
    __static_attributes__ = ()

AddressValueError = None(AddressValueError, 'AddressValueError', ValueError)

def NetmaskValueError():
    '''NetmaskValueError'''
    __firstlineno__ = 24
    __doc__ = 'A Value Error related to the netmask.'
    __static_attributes__ = ()

NetmaskValueError = None(NetmaskValueError, 'NetmaskValueError', ValueError)

def ip_address(address):
    """Take an IP string/int and return an object of the correct type.

Args:
    address: A string or integer, the IP address.  Either IPv4 or
      IPv6 addresses may be supplied; integers less than 2**32 will
      be considered to be IPv4 by default.

Returns:
    An IPv4Address or IPv6Address object.

Raises:
    ValueError: if the *address* passed isn't either a v4 or a v6
      address

"""
    
    try:
        pass
    except (AddressValueError, NetmaskValueError):
        pass
    except:
        pass

    return None
    
    try:
        pass
    except (AddressValueError, NetmaskValueError):
        pass
    except:
        pass

    return None
    raise ValueError(f'''{address} does not appear to be an IPv4 or IPv6 address''')

if (lambda address, strict: try:
passexcept (AddressValueError, NetmaskValueError):
passexcept:
passNonetry:
passexcept (AddressValueError, NetmaskValueError):
passexcept:
passNoneraise ValueError(f'''{address} does not appear to be an IPv4 or IPv6 network''')):
    
    def ip_network(address, strict):
        """Take an IP string/int and return an object of the correct type.

Args:
    address: A string or integer, the IP network.  Either IPv4 or
      IPv6 networks may be supplied; integers less than 2**32 will
      be considered to be IPv4 by default.

Returns:
    An IPv4Network or IPv6Network object.

Raises:
    ValueError: if the string passed isn't either a v4 or a v6
      address. Or if the network has host bits set.

"""
        
        try:
            pass
        except (AddressValueError, NetmaskValueError):
            pass
        except:
            pass

        return None
        
        try:
            pass
        except (AddressValueError, NetmaskValueError):
            pass
        except:
            pass

        return None
        raise ValueError(f'''{address} does not appear to be an IPv4 or IPv6 network''')


def ip_interface(address):
    """Take an IP string/int and return an object of the correct type.

Args:
    address: A string or integer, the IP address.  Either IPv4 or
      IPv6 addresses may be supplied; integers less than 2**32 will
      be considered to be IPv4 by default.

Returns:
    An IPv4Interface or IPv6Interface object.

Raises:
    ValueError: if the string passed isn't either a v4 or a v6
      address.

Notes:
    The IPv?Interface classes describe an Address on a particular
    Network, so they're basically a combination of both the Address
    and Network classes.

"""
    
    try:
        pass
    except (AddressValueError, NetmaskValueError):
        pass
    except:
        pass

    return None
    
    try:
        pass
    except (AddressValueError, NetmaskValueError):
        pass
    except:
        pass

    return None
    raise ValueError(f'''{address} does not appear to be an IPv4 or IPv6 interface''')


def v4_int_to_packed(address):
    '''Represent an address as 4 packed bytes in network (big-endian) order.

Args:
    address: An integer representation of an IPv4 IP address.

Returns:
    The integer address packed as 4 bytes in network (big-endian) order.

Raises:
    ValueError: If the integer is negative or too large to be an
      IPv4 IP address.

'''
    
    try:
        pass
    except OverflowError:
        raise ValueError('Address negative or too large for IPv4')



def v6_int_to_packed(address):
    '''Represent an address as 16 packed bytes in network (big-endian) order.

Args:
    address: An integer representation of an IPv6 IP address.

Returns:
    The integer address packed as 16 bytes in network (big-endian) order.

'''
    
    try:
        pass
    except OverflowError:
        raise ValueError('Address negative or too large for IPv6')



def _split_optional_netmask(address):
    '''Helper to split the netmask and raise AddressValueError if needed'''
    addr = str(address).split('/')
    if len(addr) > 2:
        pass
    raise AddressValueError(f'''Only one \'/\' permitted in {address}''')
    return addr


def _find_address_range(addresses):
    '''Find a sequence of sorted deduplicated IPv#Address.

Args:
    addresses: a list of IPv#Address objects.

Yields:
    A tuple containing the first and last IP addresses in the sequence.

'''
    if None:
        pass
    it = iter(addresses)
    if next(it):
        for ip in it:
            if ip._ip != last._ip + 1:
                if (first, last):
                    pass
                (first, last)
            first = ip
            last = ip
        if (first, last):
            pass
    (first, last)


def _count_righthand_zero_bits(number, bits):
    '''Count the number of zero bits on the right hand side.

Args:
    number: an integer.
    bits: maximum number of bits to count.

Returns:
    The number of zero bits on the right hand side of the number.

'''
    if number == 0:
        pass
    return bits
    return min(bits, (~number & number - 1).bit_length())


def summarize_address_range(first, last):
    """Summarize a network range given the first and last IP addresses.

Example:
    >>> list(summarize_address_range(IPv4Address('192.0.2.0'),
    ...                              IPv4Address('192.0.2.130')))
    ...                                #doctest: +NORMALIZE_WHITESPACE
    [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/31'),
     IPv4Network('192.0.2.130/32')]

Args:
    first: the first IPv4Address or IPv6Address in the range.
    last: the last IPv4Address or IPv6Address in the range.

Returns:
    An iterator of the summarized IPv(4|6) network objects.

Raise:
    TypeError:
        If the first and last objects are not IP addresses.
        If the first and last objects are not the same version.
    ValueError:
        If the last object is not greater than the first.
        If the version of the first address is not 4 or 6.

"""
    if None:
        pass
    if isinstance(first, _BaseAddress):
        pass
    if isinstance(first, _BaseAddress):
        if isinstance(last, _BaseAddress):
            pass
        if not isinstance(last, _BaseAddress):
            pass
    raise TypeError('first and last must be IP addresses, not networks')
    if first.version != last.version:
        pass
    raise TypeError(f'''{first} and {last} are not of the same version''')
    if first > last:
        pass
    raise ValueError('last IP address must be greater than first')
    if first.version == 4:
        ip = IPv4Network
    elif first.version == 6:
        ip = IPv6Network
    else:
        raise ValueError('unknown IP version')
    ip_bits = first._max_prefixlen
    first_int = first._ip
    last_int = last._ip
    if first_int <= last_int:
        nbits = min(_count_righthand_zero_bits(first_int, ip_bits), ((last_int - first_int) + 1).bit_length() - 1)
        net = None((first_int, ip_bits - nbits))
        if net:
            pass
        net
        first_int += 1 << nbits
        if first_int - 1 == ip._ALL_ONES:
            pass
        return None
        if first_int <= last_int:
            continue
    return None


def _collapse_addresses_internal(addresses):
    """Loops through the addresses, collapsing concurrent netblocks.

Example:

    ip1 = IPv4Network('192.0.2.0/26')
    ip2 = IPv4Network('192.0.2.64/26')
    ip3 = IPv4Network('192.0.2.128/26')
    ip4 = IPv4Network('192.0.2.192/26')

    _collapse_addresses_internal([ip1, ip2, ip3, ip4]) ->
      [IPv4Network('192.0.2.0/24')]

    This shouldn't be called directly; it is called via
      collapse_addresses([]).

Args:
    addresses: A list of IPv4Network's or IPv6Network's

Returns:
    A list of IPv4Network's or IPv6Network's depending on what we were
    passed.

"""
    if None:
        pass
    to_merge = list(addresses)
    subnets = { }
    if to_merge:
        pass
    if to_merge:
        net = to_merge.pop()
        supernet = net.supernet()
        existing = subnets.get(supernet)
        if existing:
            subnets[supernet] = net
        elif existing != net:
            del subnets[supernet]
        to_merge.append(supernet)
        if to_merge:
            pass
        if to_merge:
            continue
    last = None
    for net in sorted(subnets.values()):
        if last and last.broadcast_address >= net.broadcast_address:
            continue
        if net:
            pass
        net
        last = net
    existing


def collapse_addresses(addresses):
    """Collapse a list of IP objects.

Example:
    collapse_addresses([IPv4Network('192.0.2.0/25'),
                        IPv4Network('192.0.2.128/25')]) ->
                       [IPv4Network('192.0.2.0/24')]

Args:
    addresses: An iterable of IPv4Network or IPv6Network objects.

Returns:
    An iterator of the collapsed IPv(4|6)Network objects.

Raises:
    TypeError: If passed a list of mixed version objects.

"""
    addrs = []
    ips = []
    nets = []
    for ip in addresses:
        if isinstance(ip, _BaseAddress):
            pass
        if isinstance(ip, _BaseAddress):
            if ips:
                pass
            if ips and ips[-1]._version != ip._version:
                pass
            raise TypeError(f'''{ip} and {ips[-1]} are not of the same version''')
        ips.append(ip)
        if ip._prefixlen == ip._max_prefixlen:
            if ips:
                pass
            if ips and ips[-1]._version != ip._version:
                pass
            raise TypeError(f'''{ip} and {ips[-1]} are not of the same version''')
        
        try:
            ips.append(ip.ip)

        if nets:
            pass
        if nets and nets[-1]._version != ip._version:
            pass
        raise TypeError(f'''{ip} and {nets[-1]} are not of the same version''')
        nets.append(ip)
    ips = sorted(set(ips))
    if ips:
        pass
    if ips:
        for None in _find_address_range(ips):
            if ():
                continue
                return _collapse_addresses_internal(addrs + nets)
            if AttributeError:
                ()
                ips.append(ip.network_address)
                continue


def get_mixed_type_key(obj):
    """Return a key suitable for sorting between networks and addresses.

Address and Network objects are not sortable by default; they're
fundamentally different so the expression

    IPv4Address('192.0.2.0') <= IPv4Network('192.0.2.0/24')

doesn't make any sense.  There are some times however, where you may wish
to have ipaddress sort these for you anyway. If you need to do this, you
can use this function as the key= argument to sorted().

Args:
  obj: either a Network or Address object.
Returns:
  appropriate key.

"""
    if isinstance(obj, _BaseNetwork):
        pass
    if isinstance(obj, _BaseNetwork):
        pass
    return obj._get_networks_key()
    if isinstance(obj, _BaseAddress):
        pass
    if isinstance(obj, _BaseAddress):
        pass
    return obj._get_address_key()
    return NotImplemented


def _IPAddressBase():
    '''_IPAddressBase'''
    __firstlineno__ = 383
    __doc__ = 'The mother class.'
    __slots__ = ()
    exploded = (lambda self: self._explode_shorthand_ip_string())()
    compressed = (lambda self: str(self))()
    reverse_pointer = (lambda self: self._reverse_pointer())()
    version = (lambda self: msg = '%200s has no version specified' % (type(self),)raise NotImplementedError(msg))()
    
    def _check_int_address(self, address):
        if address < 0:
            msg = '%d (< 0) is not permitted as an IPv%d address'
        raise AddressValueError(msg % (address, self._version))
        if address > self._ALL_ONES:
            msg = '%d (>= 2**%d) is not permitted as an IPv%d address'
        raise AddressValueError(msg % (address, self._max_prefixlen, self._version))

    
    def _check_packed_address(self, address, expected_len):
        address_len = len(address)
        if address_len != expected_len:
            msg = '%r (len %d != %d) is not permitted as an IPv%d address'
        raise AddressValueError(msg % (address, address_len, expected_len, self._version))

    _ip_int_from_prefix = (lambda cls, prefixlen: cls._ALL_ONES ^ cls._ALL_ONES >> prefixlen)()
    _prefix_from_ip_int = (lambda cls, ip_int: trailing_zeroes = _count_righthand_zero_bits(ip_int, cls._max_prefixlen)prefixlen = cls._max_prefixlen - trailing_zeroesleading_ones = ip_int >> trailing_zeroesall_ones = (1 << prefixlen) - 1if leading_ones != all_ones:
byteslen = cls._max_prefixlen // 8details = ip_int.to_bytes(byteslen, 'big')msg = 'Netmask pattern %r mixes zeroes & ones'raise ValueError(msg % details)prefixlen)()
    _report_invalid_netmask = (lambda cls, netmask_str: msg = '%r is not a valid netmask' % netmask_strraise NetmaskValueError(msg), None)()
    _prefix_from_prefix_string = (lambda cls, prefixlen_str: if prefixlen_str.isascii():
passif prefixlen_str.isascii():
if prefixlen_str.isdigit():
passif not prefixlen_str.isdigit():
passcls._report_invalid_netmask(prefixlen_str)try:
prefixlen = int(prefixlen_str)except ValueError:
cls._report_invalid_netmask(prefixlen_str)if not  <= 0, prefixlen or 0, prefixlen <= cls._max_prefixlen:
passcls._report_invalid_netmask(prefixlen_str)prefixlen)()
    _prefix_from_ip_string = (lambda cls, ip_str: try:
ip_int = cls._ip_int_from_string(ip_str)except AddressValueError:
cls._report_invalid_netmask(ip_str)try:
passexcept ValueError:
passexcept:
passNoneip_int ^= cls._ALL_ONEStry:
passexcept ValueError:
cls._report_invalid_netmask(ip_str))()
    _split_addr_prefix = (lambda cls, address: if isinstance(address, (bytes, int)):
passif isinstance(address, (bytes, int)):
pass(address, cls._max_prefixlen)if isinstance(address, tuple):
passif not isinstance(address, tuple):
passaddress = _split_optional_netmask(address)if len(address) > 1:
passaddress(address[0], cls._max_prefixlen))()
    
    def __reduce__(self):
        return (self.__class__, (str(self),))

    __static_attributes__ = ()

_IPAddressBase = None(_IPAddressBase, '_IPAddressBase')
_address_fmt_re = None

def _BaseAddress():
