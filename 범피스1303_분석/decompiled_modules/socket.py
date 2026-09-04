# Source Generated with Decompyle++
# File: socket.marshal (Python 3.13)

"""This module provides socket operations and some related functions.
On Unix, it supports IP (Internet Protocol) and Unix domain sockets.
On other systems, it only supports IP. Functions specific for a
socket are available as methods of the socket object.

Functions:

socket() -- create a new socket object
socketpair() -- create a pair of new socket objects [*]
fromfd() -- create a socket object from an open file descriptor [*]
send_fds() -- Send file descriptor to the socket.
recv_fds() -- Receive file descriptors from the socket.
fromshare() -- create a socket object from data received from socket.share() [*]
gethostname() -- return the current hostname
gethostbyname() -- map a hostname to its IP number
gethostbyaddr() -- map an IP number or hostname to DNS info
getservbyname() -- map a service name and a protocol name to a port number
getprotobyname() -- map a protocol name (e.g. 'tcp') to a number
ntohs(), ntohl() -- convert 16, 32 bit int from network to host byte order
htons(), htonl() -- convert 16, 32 bit int from host to network byte order
inet_aton() -- convert IP addr string (123.45.67.89) to 32-bit packed format
inet_ntoa() -- convert 32-bit packed format IP to string (123.45.67.89)
socket.getdefaulttimeout() -- get the default timeout value
socket.setdefaulttimeout() -- set the default timeout value
create_connection() -- connects to an address, with an optional timeout and
                       optional source address.
create_server() -- create a TCP socket and bind it to a specified address.

 [*] not available on all platforms!

Special objects:

SocketType -- type object for socket objects
error -- exception raised for I/O errors
has_ipv6 -- boolean value indicating if IPv6 is supported

IntEnum constants:

AF_INET, AF_UNIX -- socket domains (first argument to socket() call)
SOCK_STREAM, SOCK_DGRAM, SOCK_RAW -- socket types (second argument)

Integer constants:

Many other constants may be defined; these may be used in calls to
the setsockopt() and getsockopt() methods.
"""
import _socket
None(import _socket)
import os
import sys
import io
import selectors
from enum import IntEnum, IntFlag

try:
    import errno
except ImportError:
    (0, 0, 0, 0)
    errno = None

EBADF = None(errno, 'EBADF', 9)
EAGAIN = None(errno, 'EAGAIN', 11)
EWOULDBLOCK = None(errno, 'EWOULDBLOCK', 11)
__all__ = [
    'fromfd',
    'getfqdn',
    'create_connection',
    'create_server',
    'has_dualstack_ipv6',
    'AddressFamily',
    'SocketKind']
os._get_exports_list(None(_socket))
None('AddressFamily', __name__, (lambda C: if C.isupper():
passif C.isupper():
C.isupper()C.startswith('AF_')))
None('SocketKind', __name__, (lambda C: if C.isupper():
passif C.isupper():
C.isupper()C.startswith('SOCK_')))
None('MsgFlag', __name__, (lambda C: if C.isupper():
passif C.isupper():
C.isupper()C.startswith('MSG_')))
None('AddressInfo', __name__, (lambda C: if C.isupper():
passif C.isupper():
C.isupper()C.startswith('AI_')))
_LOCALHOST = '127.0.0.1'
_LOCALHOST_V6 = '::1'

def _intenum_converter(value, enum_klass):
    """Convert a numeric family value to an IntEnum member.

If it's not a known member, return the numeric value itself.
"""
    
    try:
        pass
    except ValueError:
        pass


if sys.platform.lower().startswith('win'):
    pass
if sys.platform.lower().startswith('win'):
    errorTab = { }
    errorTab[6] = 'Specified event object handle is invalid.'
    errorTab[8] = 'Insufficient memory available.'
    errorTab[87] = 'One or more parameters are invalid.'
    errorTab[995] = 'Overlapped operation aborted.'
    errorTab[996] = 'Overlapped I/O event object not in signaled state.'
    errorTab[997] = 'Overlapped operation will complete later.'
    errorTab[10004] = 'The operation was interrupted.'
    errorTab[10009] = 'A bad file handle was passed.'
    errorTab[10013] = 'Permission denied.'
    errorTab[10014] = 'A fault occurred on the network??'
    errorTab[10022] = 'An invalid operation was attempted.'
    errorTab[10024] = 'Too many open files.'
    errorTab[10035] = 'The socket operation would block.'
    errorTab[10036] = 'A blocking operation is already in progress.'
    errorTab[10037] = 'Operation already in progress.'
    errorTab[10038] = 'Socket operation on nonsocket.'
    errorTab[10039] = 'Destination address required.'
    errorTab[10040] = 'Message too long.'
    errorTab[10041] = 'Protocol wrong type for socket.'
    errorTab[10042] = 'Bad protocol option.'
    errorTab[10043] = 'Protocol not supported.'
    errorTab[10044] = 'Socket type not supported.'
    errorTab[10045] = 'Operation not supported.'
    errorTab[10046] = 'Protocol family not supported.'
    errorTab[10047] = 'Address family not supported by protocol family.'
    errorTab[10048] = 'The network address is in use.'
    errorTab[10049] = 'Cannot assign requested address.'
    errorTab[10050] = 'Network is down.'
    errorTab[10051] = 'Network is unreachable.'
    errorTab[10052] = 'Network dropped connection on reset.'
    errorTab[10053] = 'Software caused connection abort.'
    errorTab[10054] = 'The connection has been reset.'
    errorTab[10055] = 'No buffer space available.'
    errorTab[10056] = 'Socket is already connected.'
    errorTab[10057] = 'Socket is not connected.'
    errorTab[10058] = 'The network has been shut down.'
    errorTab[10059] = 'Too many references.'
    errorTab[10060] = 'The operation timed out.'
    errorTab[10061] = 'Connection refused.'
    errorTab[10062] = 'Cannot translate name.'
    errorTab[10063] = 'The name is too long.'
    errorTab[10064] = 'The host is down.'
    errorTab[10065] = 'The host is unreachable.'
    errorTab[10066] = 'Directory not empty.'
    errorTab[10067] = 'Too many processes.'
    errorTab[10068] = 'User quota exceeded.'
    errorTab[10069] = 'Disk quota exceeded.'
    errorTab[10070] = 'Stale file handle reference.'
    errorTab[10071] = 'Item is remote.'
    errorTab[10091] = 'Network subsystem is unavailable.'
    errorTab[10092] = 'Winsock.dll version out of range.'
    errorTab[10093] = 'Successful WSAStartup not yet performed.'
    errorTab[10101] = 'Graceful shutdown in progress.'
    errorTab[10102] = 'No more results from WSALookupServiceNext.'
    errorTab[10103] = 'Call has been canceled.'
    errorTab[10104] = 'Procedure call table is invalid.'
    errorTab[10105] = 'Service provider is invalid.'
    errorTab[10106] = 'Service provider failed to initialize.'
    errorTab[10107] = 'System call failure.'
    errorTab[10108] = 'Service not found.'
    errorTab[10109] = 'Class type not found.'
    errorTab[10110] = 'No more results from WSALookupServiceNext.'
    errorTab[10111] = 'Call was canceled.'
    errorTab[10112] = 'Database query was refused.'
    errorTab[11001] = 'Host not found.'
    errorTab[11002] = 'Nonauthoritative host not found.'
    errorTab[11003] = 'This is a nonrecoverable error.'
    errorTab[11004] = 'Valid name, no data record requested type.'
    errorTab[11005] = 'QoS receivers.'
    errorTab[11006] = 'QoS senders.'
    errorTab[11007] = 'No QoS senders.'
    errorTab[11008] = 'QoS no receivers.'
    errorTab[11009] = 'QoS request confirmed.'
    errorTab[11010] = 'QoS admission error.'
    errorTab[11011] = 'QoS policy failure.'
    errorTab[11012] = 'QoS bad style.'
    errorTab[11013] = 'QoS bad object.'
    errorTab[11014] = 'QoS traffic control error.'
    errorTab[11015] = 'QoS generic error.'
    errorTab[11016] = 'QoS service type error.'
    errorTab[11017] = 'QoS flowspec error.'
    errorTab[11018] = 'Invalid QoS provider buffer.'
    errorTab[11019] = 'Invalid QoS filter style.'
    errorTab[11020] = 'Invalid QoS filter style.'
    errorTab[11021] = 'Incorrect QoS filter count.'
    errorTab[11022] = 'Invalid QoS object length.'
    errorTab[11023] = 'Incorrect QoS flow count.'
    errorTab[11024] = 'Unrecognized QoS object.'
    errorTab[11025] = 'Invalid QoS policy object.'
    errorTab[11026] = 'Invalid QoS flow descriptor.'
    errorTab[11027] = 'Invalid QoS provider-specific flowspec.'
    errorTab[11028] = 'Invalid QoS provider-specific filterspec.'
    errorTab[11029] = 'Invalid QoS shape discard mode object.'
    errorTab[11030] = 'Invalid QoS shaping rate object.'
    errorTab[11031] = 'Reserved policy QoS element type.'
__all__.append('errorTab')

def _GiveupOnSendfile():
    '''_GiveupOnSendfile'''
    __firstlineno__ = 212
    __static_attributes__ = ()

_GiveupOnSendfile = None(_GiveupOnSendfile, '_GiveupOnSendfile', Exception)

def socket():
    '''socket'''
    __firstlineno__ = 215
    __doc__ = 'A subclass of _socket.socket adding the makefile() method.'
    __slots__ = [
        '__weakref__',
        '_io_refs',
        '_closed']
    if (lambda self, family, type, proto, fileno: if fileno:
if family == -1:
passfamily = AF_INETif type == -1:
passtype = SOCK_STREAMif proto == -1:
passproto = 0_socket.socket.__init__(self, family, type, proto, fileno)self._io_refs = 0self._closed = False):
        
        def __init__(self, family, type, proto, fileno):
            if fileno:
                if family == -1:
                    pass
                family = AF_INET
                if type == -1:
                    pass
                type = SOCK_STREAM
                if proto == -1:
                    pass
            proto = 0
            _socket.socket.__init__(self, family, type, proto, fileno)
            self._io_refs = 0
            self._closed = False

    
    def __enter__(self):
        return self

    
    def __exit__(self, *args):
        if self._closed:
            pass
        if not self._closed:
            self.close()
        return None

    
    def __repr__(self):
        '''Wrap __repr__() to reveal the real class name and socket
address(es).
'''
        closed = getattr(self, '_closed', False)
        if closed:
            pass
        s = '<%s.%s%s fd=%i, family=%s, type=%s, proto=%i' % (self.__class__.__module__, self.__class__.__qualname__, ' [closed]' if closed else '', self.fileno(), self.family, self.type, self.proto)
        if closed:
            pass
        if not closed:
            
            try:
                laddr = self.getsockname()
                if laddr:
                    pass
                if laddr:
                    pass
                s += ', laddr=%s' % str(laddr)

            
            try:
                raddr = self.getpeername()
                if raddr:
                    pass
                if raddr:
                    pass
                s += ', raddr=%s' % str(raddr)
            except (error, AttributeError):
                pass

            s += '>'
            return s
        if (error, AttributeError):
            pass
        continue

    
    def __getstate__(self):
        raise TypeError(f'''cannot pickle {self.__class__.__name__} object''')

    
    def dup(self):
        '''dup() -> socket object

Duplicate the socket. Return a new socket object connected to the same
system resource. The new socket is non-inheritable.
'''
        fd = dup(self.fileno())
        sock = self.__class__(self.family, self.type, self.proto, fileno = fd)
        sock.settimeout(self.gettimeout())
        return sock

    
    def accept(self):
        '''accept() -> (socket object, address info)

Wait for an incoming connection.  Return a new socket
representing the connection, and the address of the client.
For IP sockets, the address info is a pair (hostaddr, port).
'''
        if ():
            pass
        if getdefaulttimeout():
            if self.gettimeout():
                pass
            if self.gettimeout():
                pass
        sock.setblocking(True)
        return (sock, addr)

    if (lambda self, mode, buffering, *, encoding, errors, newline: if not set(mode) <= {
'b',
'r',
'w'}:
passraise ValueError(f'''invalid mode {mode} (only r, w, b allowed)''')writing = 'w' in modeif 'r' in mode:
passif not 'r' in mode:
'r' in modeif writing:
passreading = not writingif reading:
passif not reading:
if writing:
passif not writing:
passraise Nonebinary = 'b' in moderawmode = ''if reading:
passif reading:
passrawmode += 'r'if writing:
passif writing:
passrawmode += 'w'raw = SocketIO(self, rawmode)if buffering:
pass-1 = bufferingif buffering < 0:
passbuffering = io.DEFAULT_BUFFER_SIZEif buffering == 0:
if binary:
passif not binary:
passraise ValueError('unbuffered streams must be binary')rawif reading:
passif reading:
if writing:
passif writing:
buffer = None(raw, raw, buffering)elif reading:
passif reading:
buffer = None(raw, buffering)elif writing:
passif not writing:
passraise io.BufferedReaderbuffer = None(raw, buffering)if binary:
passif binary:
passbufferencoding = None(encoding)text = None(buffer, encoding, errors, newline)text.mode = modetext) and (lambda self, mode, buffering, *, encoding, errors, newline: if not set(mode) <= {
'b',
'r',
'w'}:
passraise ValueError(f'''invalid mode {mode} (only r, w, b allowed)''')writing = 'w' in modeif 'r' in mode:
passif not 'r' in mode:
'r' in modeif writing:
passreading = not writingif reading:
passif not reading:
if writing:
passif not writing:
passraise Nonebinary = 'b' in moderawmode = ''if reading:
passif reading:
passrawmode += 'r'if writing:
passif writing:
passrawmode += 'w'raw = SocketIO(self, rawmode)if buffering:
pass-1 = bufferingif buffering < 0:
passbuffering = io.DEFAULT_BUFFER_SIZEif buffering == 0:
if binary:
passif not binary:
passraise ValueError('unbuffered streams must be binary')rawif reading:
passif reading:
if writing:
passif writing:
buffer = None(raw, raw, buffering)elif reading:
passif reading:
buffer = None(raw, buffering)elif writing:
passif not writing:
passraise io.BufferedReaderbuffer = None(raw, buffering)if binary:
passif binary:
passbufferencoding = None(encoding)text = None(buffer, encoding, errors, newline)text.mode = modetext):
        
        def makefile(self, mode, buffering, *, encoding, errors, newline):
            """makefile(...) -> an I/O stream connected to the socket

The arguments are as for io.open() after the filename, except the only
supported mode values are 'r' (default), 'w', 'b', or a combination of
those.
"""
            if not set(mode) <= {
                'b',
                'r',
                'w'}:
                pass
            raise ValueError(f'''invalid mode {mode} (only r, w, b allowed)''')
            writing = 'w' in mode
            if 'r' in mode:
                pass
            if not 'r' in mode:
                'r' in mode
                if writing:
                    pass
            reading = not writing
            if reading:
                pass
            if not reading:
                if writing:
                    pass
                if not writing:
                    pass
            raise None
            binary = 'b' in mode
            rawmode = ''
            if reading:
                pass
            if reading:
                pass
            rawmode += 'r'
            if writing:
                pass
            if writing:
                pass
            rawmode += 'w'
            raw = SocketIO(self, rawmode)
            if buffering:
                pass
            -1 = buffering
            if buffering < 0:
                pass
            buffering = io.DEFAULT_BUFFER_SIZE
            if buffering == 0:
                if binary:
                    pass
                if not binary:
                    pass
                raise ValueError('unbuffered streams must be binary')
            return raw
            if reading:
                pass
            if reading:
                if writing:
                    pass
                if writing:
                    buffer = None(raw, raw, buffering)
                elif reading:
                    pass
            if reading:
                buffer = None(raw, buffering)
            elif writing:
                pass
            if not writing:
                pass
            raise io.BufferedReader
            buffer = None(raw, buffering)
            if binary:
                pass
            if binary:
                pass
            return buffer
            encoding = None(encoding)
            text = None(buffer, encoding, errors, newline)
            text.mode = mode
            return text

    if None(os, 'sendfile'):
        pass
    if None(os, 'sendfile') and (lambda self, file, offset, count: self._check_sendfile_params(file, offset, count)sockno = self.fileno()try:
fileno = file.fileno()except (AttributeError, io.UnsupportedOperation):
err = selectors.PollSelector if hasattr(selectors, 'PollSelector') else selectors.SelectSelector if blocksize <= 0 else selector_selectraise _GiveupOnSendfile(err)err = Nonedel errtry:
fsize = None(fileno).st_sizeexcept OSError:
err = selectors.PollSelector if hasattr(selectors, 'PollSelector') else selectors.SelectSelector if blocksize <= 0 else selector_selectraise _GiveupOnSendfile(err)err = Nonedel errif fsize:
passif not fsize:
pass0if count:
passif not count:
countblocksize = min(fsize, 1073741824)timeout = self.gettimeout()if timeout == 0:
passraise ValueError('non-blocking sockets are not supported')if hasattr(selectors, 'PollSelector'):
passselector.register(sockno, selectors.EVENT_WRITE)total_sent = 0selector_select = selector.selectos_sendfile = os.sendfiletry:
if timeout:
passif timeout:
if None(timeout):
passif not None(timeout):
passraise TimeoutError('timed out')if count:
passif count:
blocksize = min(count - total_sent, blocksize)if total_sent > 0:
if hasattr(file, 'seek'):
passif hasattr(file, 'seek'):
file.seek(offset)total_senttotal_sentif total_sent > 0:
if hasattr(file, 'seek'):
passif hasattr(file, 'seek'):
file.seek(offset)):
        
        def _sendfile_use_sendfile(self, file, offset, count):
            self._check_sendfile_params(file, offset, count)
            sockno = self.fileno()
            
            try:
                fileno = file.fileno()
            except (AttributeError, io.UnsupportedOperation):
                err = selectors.PollSelector if hasattr(selectors, 'PollSelector') else selectors.SelectSelector if blocksize <= 0 else selector_select
                raise _GiveupOnSendfile(err)
                err = None
                del err

            
            try:
                fsize = None(fileno).st_size
            except OSError:
                err = selectors.PollSelector if hasattr(selectors, 'PollSelector') else selectors.SelectSelector if blocksize <= 0 else selector_select
                raise _GiveupOnSendfile(err)
                err = None
                del err

            if fsize:
                pass
            if not fsize:
                pass
            return 0
            if count:
                pass
            if not count:
                count
            blocksize = min(fsize, 1073741824)
            timeout = self.gettimeout()
            if timeout == 0:
                pass
            raise ValueError('non-blocking sockets are not supported')
            if hasattr(selectors, 'PollSelector'):
                pass
            selector.register(sockno, selectors.EVENT_WRITE)
            total_sent = 0
            selector_select = selector.select
            os_sendfile = os.sendfile
            
            try:
                if timeout:
                    pass
                if timeout:
                    if None(timeout):
                        pass
                    if not None(timeout):
                        pass
                raise TimeoutError('timed out')
                if count:
                    pass
                if count:
                    blocksize = min(count - total_sent, blocksize)

            if total_sent > 0:
                if hasattr(file, 'seek'):
                    pass
                if hasattr(file, 'seek'):
                    file.seek(offset)
                return total_sent
            return total_sent
            if total_sent > 0:
                if hasattr(file, 'seek'):
                    pass
                if hasattr(file, 'seek'):
                    file.seek(offset)

    elif (lambda self, file, offset, count: raise _GiveupOnSendfile('os.sendfile() not available on this platform')):
        
        def _sendfile_use_sendfile(self, file, offset, count):
            raise _GiveupOnSendfile('os.sendfile() not available on this platform')

    if (lambda self, file, offset, count: self._check_sendfile_params(file, offset, count)if self.gettimeout() == 0:
passraise ValueError('non-blocking sockets are not supported')if offset:
passif offset:
passfile.seek(offset)if count:
passblocksize = min(count, 8192) if count else 8192total_sent = 0file_read = file.readsock_send = self.sendtry:
if count:
passif count:
blocksize = min(count - total_sent, blocksize)if blocksize <= 0:
passelse:
data = file_read(None(blocksize))if data:
passif not data:
passelse:
try:
sent = None(data)except BlockingIOError:
passtotal_sent += sentif sent < len(data):
data = data[sent:]if total_sent > 0:
if hasattr(file, 'seek'):
passif hasattr(file, 'seek'):
except:
passcontinueif total_sent > 0:
if hasattr(file, 'seek'):
passif hasattr(file, 'seek'):
file.seek(offset + total_sent)total_senttotal_senttry:
if count:
passif count:
blocksize = min(count - total_sent, blocksize)if blocksize <= 0:
passelse:
data = file_read(None(blocksize))if data:
passif not data:
passelse:
try:
sent = None(data)except BlockingIOError:
passtotal_sent += sentif sent < len(data):
data = data[sent:]if total_sent > 0:
if hasattr(file, 'seek'):
passif hasattr(file, 'seek'):
except:
pass):
        
        def _sendfile_use_send(self, file, offset, count):
            self._check_sendfile_params(file, offset, count)
            if self.gettimeout() == 0:
                pass
            raise ValueError('non-blocking sockets are not supported')
            if offset:
                pass
            if offset:
                pass
            file.seek(offset)
            if count:
                pass
            blocksize = min(count, 8192) if count else 8192
            total_sent = 0
            file_read = file.read
            sock_send = self.send
            
            try:
                if count:
                    pass
                if count:
                    blocksize = min(count - total_sent, blocksize)
                    if blocksize <= 0:
                        pass
                    else:
                        data = file_read(None(blocksize))
                        if data:
                            pass
                        if not data:
                            pass
                        else:
                            
                            try:
                                sent = None(data)
                            except BlockingIOError:
                                pass

                            total_sent += sent
                            if sent < len(data):
                                data = data[sent:]
                            
                
            if total_sent > 0:
                if hasattr(file, 'seek'):
                    pass
                if hasattr(file, 'seek'):
                    except:
                        pass

            continue
            if total_sent > 0:
                if hasattr(file, 'seek'):
                    pass
                if hasattr(file, 'seek'):
                    file.seek(offset + total_sent)
                return total_sent
            return total_sent
            
            try:
                if count:
                    pass
                if count:
                    blocksize = min(count - total_sent, blocksize)
                    if blocksize <= 0:
                        pass
                    else:
                        data = file_read(None(blocksize))
                        if data:
                            pass
                        if not data:
                            pass
                        else:
                            
                            try:
                                sent = None(data)
                            except BlockingIOError:
                                pass

                            total_sent += sent
                            if sent < len(data):
                                data = data[sent:]
                            
                
            if total_sent > 0:
                if hasattr(file, 'seek'):
                    pass
                if hasattr(file, 'seek'):
                    except:
                        pass


    
    def _check_sendfile_params(self, file, offset, count):
        if 'b' not in getattr(file, 'mode', 'b'):
            pass
        raise ValueError('file should be opened in binary mode')
        if self.type & SOCK_STREAM:
            pass
        if not self.type & SOCK_STREAM:
            pass
        raise ValueError('only SOCK_STREAM type sockets are supported')
        if count:
            if isinstance(count, int):
                pass
            if not isinstance(count, int):
                pass
            raise TypeError('count must be a positive integer (got {!r})'.format(count))
        if count <= 0:
            pass
        raise ValueError('count must be a positive integer (got {!r})'.format(count))
        return None

    if (lambda self, file, offset, count: try:
passexcept _GiveupOnSendfile:
pass):
        
        def sendfile(self, file, offset, count):
            '''sendfile(file[, offset[, count]]) -> sent

Send a file until EOF is reached by using high-performance
os.sendfile() and return the total number of bytes which
were sent.
*file* must be a regular file object opened in binary mode.
If os.sendfile() is not available (e.g. Windows) or file is
not a regular file socket.send() will be used instead.
*offset* tells from where to start reading the file.
If specified, *count* is the total number of bytes to transmit
as opposed to sending the file until EOF is reached.
File position is updated on return or also in case of error in
which case file.tell() can be used to figure out the number of
bytes which were sent.
The socket must be of SOCK_STREAM type.
Non-blocking sockets are not supported.
'''
            
            try:
                pass
            except _GiveupOnSendfile:
                pass


    
    def _decref_socketios(self):
        if self._io_refs > 0:
            pass
        if self._closed:
            pass
        if self._closed:
            self.close()
        return None

    if (lambda self, _ss: _ss.close(self)):
        
        def _real_close(self, _ss):
            _ss.close(self)

    
    def close(self):
        self._closed = True
        if self._io_refs <= 0:
            self._real_close()
        return None

    if (lambda self: self._closed = Trueself()):
        
        def detach(self):
            '''detach() -> file descriptor

Close the socket object without closing the underlying file descriptor.
The object cannot be used after this call, but the file descriptor
can be reused for other purposes.  The file descriptor is returned.
'''
            self._closed = True
            return self()

        if (lambda self: __class__(self, AddressFamily)):
            family = (lambda self: __class__(self, AddressFamily))()
    if (lambda self: __class__(self, SocketKind)):
        type = (lambda self: __class__(self, SocketKind))()
    get_inheritable.__doc__ = 'Get the inheritable flag of the socket'
    set_inheritable.__doc__ = 'Set the inheritable flag of the socket'
    __static_attributes__ = ('_closed', '_io_refs')
    __classcell__ = __class__
    return __class__

socket = None(socket, 'socket', _socket.socket)
if (lambda fd, family, type, proto: nfd = dup(fd)socket(family, type, proto, nfd)):
    
    def fromfd(fd, family, type, proto):
        '''fromfd(fd, family, type[, proto]) -> socket object

Create a socket object from a duplicate of the given file
descriptor.  The remaining arguments are the same as for socket().
'''
        nfd = dup(fd)
        return socket(family, type, proto, nfd)

if None(_socket.socket, 'sendmsg'):
    pass
if None(_socket.socket, 'sendmsg'):
    import array
    if (lambda sock, buffers, fds, flags, address: buffers(_socket.SOL_SOCKET, [
(_socket.SCM_RIGHTS, array.array, None('i', fds))])):
        
        def send_fds(sock, buffers, fds, flags, address):
            '''send_fds(sock, buffers, fds[, flags[, address]]) -> integer

Send the list of file descriptors fds over an AF_UNIX socket.
'''
            return buffers(_socket.SOL_SOCKET, [
                (_socket.SCM_RIGHTS, array.array, None('i', fds))])

__all__.append('send_fds')
if None(_socket.socket, 'recvmsg'):
    pass
if None(_socket.socket, 'recvmsg'):
    import array
    if (lambda sock, bufsize, maxfds, flags: 