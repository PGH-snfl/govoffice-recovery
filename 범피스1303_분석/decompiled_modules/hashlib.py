# Source Generated with Decompyle++
# File: hashlib.marshal (Python 3.13)

'''hashlib module - A common interface to many hash functions.

new(name, data=b\'\', **kwargs) - returns a new hash object implementing the
                                given hash function; initializing the hash
                                using the given binary data.

Named constructor functions are also available, these are faster
than using new(name):

md5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(),
sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.

More algorithms may be available on your platform but the above are guaranteed
to exist.  See the algorithms_guaranteed and algorithms_available attributes
to find out what algorithm names can be passed to new().

NOTE: If you want the adler32 or crc32 hash functions they are available in
the zlib module.

Choose your hash function wisely.  Some have known collision weaknesses.
sha384 and sha512 will be slow on 32 bit platforms.

Hash objects have these methods:
 - update(data): Update the hash object with the bytes in data. Repeated calls
                 are equivalent to a single call with the concatenation of all
                 the arguments.
 - digest():     Return the digest of the bytes passed to the update() method
                 so far as a bytes object.
 - hexdigest():  Like digest() except the digest is returned as a string
                 of double length, containing only hexadecimal digits.
 - copy():       Return a copy (clone) of the hash object. This can be used to
                 efficiently compute the digests of datas that share a common
                 initial substring.

For example, to obtain the digest of the byte string \'Nobody inspects the
spammish repetition\':

    >>> import hashlib
    >>> m = hashlib.md5()
    >>> m.update(b"Nobody inspects")
    >>> m.update(b" the spammish repetition")
    >>> m.digest()
    b\'\\xbbd\\x9c\\x83\\xdd\\x1e\\xa5\\xc9\\xd9\\xde\\xc9\\xa1\\x8d\\xf0\\xff\\xe9\'

More condensed:

    >>> hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
    \'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2\'

'''
__always_supported = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128', 'shake_256')
algorithms_guaranteed = None(__always_supported)
algorithms_available = None(__always_supported)
__all__ = __always_supported + ('new', 'algorithms_guaranteed', 'algorithms_available', 'file_digest')
__builtin_constructor_cache = { }
__block_openssl_constructor = {
    'blake2b',
    'blake2s'}

def __get_builtin_constructor(name):
    cache = __builtin_constructor_cache
    constructor = cache.get(name)
    if constructor:
        pass
    return constructor
    
    try:
        if name in frozenset({'SHA1', 'sha1'}):
            import _sha1
            cache['SHA1'] = _sha1.sha1
            cache['sha1'] = _sha1.sha1
        elif name in frozenset({'MD5', 'md5'}):
            import _md5
            cache['MD5'] = _md5.md5
            cache['md5'] = _md5.md5
        elif name in frozenset({'SHA224', 'SHA256', 'sha224', 'sha256'}):
            import _sha2
            cache['SHA224'] = _sha2.sha224
            cache['sha224'] = _sha2.sha224
            cache['SHA256'] = _sha2.sha256
            cache['sha256'] = _sha2.sha256
        elif name in frozenset({'SHA384', 'SHA512', 'sha384', 'sha512'}):
            import _sha2
            cache['SHA384'] = _sha2.sha384
            cache['sha384'] = _sha2.sha384
            cache['SHA512'] = _sha2.sha512
            cache['sha512'] = _sha2.sha512
        elif name in frozenset({'blake2b', 'blake2s'}):
            import _blake2
            cache['blake2b'] = _blake2.blake2b
            cache['blake2s'] = _blake2.blake2s
        elif name in frozenset({'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'}):
            import _sha3
            cache['sha3_224'] = _sha3.sha3_224
            cache['sha3_256'] = _sha3.sha3_256
            cache['sha3_384'] = _sha3.sha3_384
            cache['sha3_512'] = _sha3.sha3_512
        elif name in frozenset({'shake_128', 'shake_256'}):
            import _sha3
            cache['shake_128'] = _sha3.shake_128
            cache['shake_256'] = _sha3.shake_256

    constructor = cache.get(name)
    if constructor:
        pass
    return constructor
    raise ValueError('unsupported hash type ' + name)
    if ImportError:
        constructor
    continue


def __get_openssl_constructor(name):
    if name in __block_openssl_constructor:
        pass
    return __get_builtin_constructor(name)
    
    try:
        f = getattr(_hashlib, 'openssl_' + name)
        None(usedforsecurity = False)
    except (AttributeError, ValueError):
        pass



def __py_new(name, *args, **kwargs):
    """new(name, data=b'', **kwargs) - Return a new hashing object using the
named algorithm; optionally initialized with data (which must be
a bytes-like object).
"""
    return args({ }, kwargs = None)


def __hash_new(name, *args, **kwargs):
    """new(name, data=b'') - Return a new hashing object using the named algorithm;
optionally initialized with data (which must be a bytes-like object).
"""
    if name in __block_openssl_constructor:
        pass
    return args({ }, kwargs = None)
    
    try:
        pass
    except ValueError:
        __get_builtin_constructor(name)



try:
    import _hashlib
    new = __hash_new
    __get_hash = __get_openssl_constructor
    algorithms_available = algorithms_available.union(_hashlib.openssl_md_meth_names)
except ImportError:
    set
    _hashlib = None
    new = __py_new
    __get_hash = __get_builtin_constructor


try:
    from _hashlib import pbkdf2_hmac
    __all__ += ('pbkdf2_hmac',)
except ImportError:
    pass


try:
    from _hashlib import scrypt
except ImportError:
    pass

if (lambda fileobj, digest, *, _bufsize, digestobj = None: if isinstance(digest, str):
passif hasattr(fileobj, 'getbuffer'):
passif hasattr(fileobj, 'getbuffer'):
digestobj.update(fileobj.getbuffer())digestobjif hasattr(fileobj, 'readinto'):
passif hasattr(fileobj, 'readinto'):
if hasattr(fileobj, 'readable'):
passif hasattr(fileobj, 'readable'):
if fileobj.readable():
passif not fileobj.readable():
passraise ValueError(f'''\'{fileobj}\' is not a file-like object in binary reading mode.''')buf = bytearray(_bufsize)view = memoryview(buf)size = fileobj.readinto(buf)if size:
passraise BlockingIOError('I/O operation would block.')if size == 0:
passdigestobjdigestobj.update(view[:size])continue):
    
    def file_digest(fileobj, digest, *, _bufsize):
        """Hash the contents of a file-like object. Returns a digest object.

*fileobj* must be a file-like object opened for reading in binary mode.
It accepts file objects from open(), io.BytesIO(), and SocketIO objects.
The function may bypass Python's I/O and use the file descriptor *fileno*
directly.

*digest* must either be a hash algorithm name as a *str*, a hash
constructor, or a callable that returns a hash object.
"""
        if isinstance(digest, str):
            pass
        if hasattr(fileobj, 'getbuffer'):
            pass
        if hasattr(fileobj, 'getbuffer'):
            digestobj.update(fileobj.getbuffer())
        return digestobj
        if hasattr(fileobj, 'readinto'):
            pass
        if hasattr(fileobj, 'readinto'):
            if hasattr(fileobj, 'readable'):
                pass
            if hasattr(fileobj, 'readable'):
                if fileobj.readable():
                    pass
                if not fileobj.readable():
                    pass
        raise ValueError(f'''\'{fileobj}\' is not a file-like object in binary reading mode.''')
        buf = bytearray(_bufsize)
        view = memoryview(buf)
        size = fileobj.readinto(buf)
        if size:
            pass
        raise BlockingIOError('I/O operation would block.')
        if size == 0:
            pass
        return digestobj
        digestobj.update(view[:size])
        continue

for __func_name in __always_supported:
    
    try:
        None()[__func_name] = globals
    except ValueError:
        set
        import logging
        None('code for hash %s was not found.', __func_name)

set
del __always_supported
del __func_name
del __get_hash
del __py_new
del __hash_new
del __get_openssl_constructor
