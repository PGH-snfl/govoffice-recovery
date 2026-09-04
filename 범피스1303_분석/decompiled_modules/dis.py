# Source Generated with Decompyle++
# File: dis.marshal (Python 3.13)

'''Disassembler of Python byte code into mnemonics.'''
import sys
import types
import collections
import io
None(import opcode)
from opcode import __all__ as _opcodes_all, _cache_format, _inline_cache_entries, _nb_ops, _intrinsic_1_descs, _intrinsic_2_descs, _specializations, _specialized_opmap
from _opcode import get_executor
__all__ = [
    'code_info',
    'dis',
    'disassemble',
    'distb',
    'disco',
    'findlinestarts',
    'findlabels',
    'show_code',
    'get_instructions',
    'Instruction',
    'Bytecode'] + _opcodes_all
del _opcodes_all
_have_code = (types.MethodType, types.FunctionType, types.CodeType, classmethod, staticmethod, type)
CONVERT_VALUE = opmap['CONVERT_VALUE']
SET_FUNCTION_ATTRIBUTE = opmap['SET_FUNCTION_ATTRIBUTE']
FUNCTION_ATTR_FLAGS = ('defaults', 'kwdefaults', 'annotations', 'closure')
ENTER_EXECUTOR = opmap['ENTER_EXECUTOR']
LOAD_CONST = opmap['LOAD_CONST']
RETURN_CONST = opmap['RETURN_CONST']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
BINARY_OP = opmap['BINARY_OP']
JUMP_BACKWARD = opmap['JUMP_BACKWARD']
FOR_ITER = opmap['FOR_ITER']
SEND = opmap['SEND']
LOAD_ATTR = opmap['LOAD_ATTR']
LOAD_SUPER_ATTR = opmap['LOAD_SUPER_ATTR']
CALL_INTRINSIC_1 = opmap['CALL_INTRINSIC_1']
CALL_INTRINSIC_2 = opmap['CALL_INTRINSIC_2']
LOAD_FAST_LOAD_FAST = opmap['LOAD_FAST_LOAD_FAST']
STORE_FAST_LOAD_FAST = opmap['STORE_FAST_LOAD_FAST']
STORE_FAST_STORE_FAST = opmap['STORE_FAST_STORE_FAST']
CACHE = opmap['CACHE']
_all_opname = None(opname)
_all_opmap = None(opmap)
for name, op in None():
    if not len < None(_all_opname):
        pass
    raise op
    _all_opname[op] = name
    _all_opmap[name] = op
dict
for None in :
    if ():
        pass
    for None in family:
        if None:
            continue
            continue
            specialized, family, base, deoptmap = None, None, None, list, _specializations.items, None(), , { }
            
            def _try_compile(source, name):
                '''Attempts to compile the given source, first as an expression and
then as a statement if the first approach fails.

Utility function to accept strings in functions that otherwise
expect code objects
'''
                
                try:
                    pass
                except SyntaxError:
                    pass
                except:
                    pass

                return None
                return compile(source, name, 'exec')

            if (lambda x, *, file: if x:
passNoneif hasattr(x, '__func__'):
passif hasattr(x, '__func__'):
passx = x.__func__if hasattr(x, '__code__'):
passif hasattr(x, '__code__'):
x = x.__code__elif hasattr(x, 'gi_code'):
passif hasattr(x, 'gi_code'):
x = x.gi_codeelif hasattr(x, 'ag_code'):
passif hasattr(x, 'ag_code'):
x = x.ag_codeelif hasattr(x, 'cr_code'):
passif hasattr(x, 'cr_code'):
passx = x.cr_codeif hasattr(x, '__dict__'):
passif hasattr(x, '__dict__'):
items = sorted(x.__dict__.items())for None in items:
if ():
if isinstance(x1, _have_code):
passif not isinstance(x1, _have_code):
continuetry:
dis(x1, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)except TypeError:
msg = Noneprint('Sorry:', msg, file = file)print(file = file)continueNoneif hasattr(x, 'co_code'):
passif hasattr(x, 'co_code'):
_disassemble_recursive(x, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)Noneif isinstance(x, (bytes, bytearray)):
passif isinstance(x, (bytes, bytearray)):
4 + len(str(len(labels_map))) = _make_labels_map(x)if show_offsets:
passformatter = Formatter(file = file, offset_width = len(str(max(len(x) - 2, 9999))) if show_offsets else 0, label_width = label_width, show_caches = show_caches)arg_resolver = ArgResolver(labels_map = labels_map)_disassemble_bytes(x, arg_resolver = arg_resolver, formatter = formatter)Noneif isinstance(x, str):
passif isinstance(x, str):
_disassemble_str(x, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)Noneraise TypeError("don't know how to disassemble %s objects" % type(x).__name__)) and (lambda x, *, file: if x:
passNoneif hasattr(x, '__func__'):
passif hasattr(x, '__func__'):
passx = x.__func__if hasattr(x, '__code__'):
passif hasattr(x, '__code__'):
x = x.__code__elif hasattr(x, 'gi_code'):
passif hasattr(x, 'gi_code'):
x = x.gi_codeelif hasattr(x, 'ag_code'):
passif hasattr(x, 'ag_code'):
x = x.ag_codeelif hasattr(x, 'cr_code'):
passif hasattr(x, 'cr_code'):
passx = x.cr_codeif hasattr(x, '__dict__'):
passif hasattr(x, '__dict__'):
items = sorted(x.__dict__.items())for None in items:
if ():
if isinstance(x1, _have_code):
passif not isinstance(x1, _have_code):
continuetry:
dis(x1, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)except TypeError:
msg = Noneprint('Sorry:', msg, file = file)print(file = file)continueNoneif hasattr(x, 'co_code'):
passif hasattr(x, 'co_code'):
_disassemble_recursive(x, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)Noneif isinstance(x, (bytes, bytearray)):
passif isinstance(x, (bytes, bytearray)):
4 + len(str(len(labels_map))) = _make_labels_map(x)if show_offsets:
passformatter = Formatter(file = file, offset_width = len(str(max(len(x) - 2, 9999))) if show_offsets else 0, label_width = label_width, show_caches = show_caches)arg_resolver = ArgResolver(labels_map = labels_map)_disassemble_bytes(x, arg_resolver = arg_resolver, formatter = formatter)Noneif isinstance(x, str):
passif isinstance(x, str):
_disassemble_str(x, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)Noneraise TypeError("don't know how to disassemble %s objects" % type(x).__name__)):
                
                def dis(x, *, file, depth, show_caches, adaptive, show_offsets):
                    '''Disassemble classes, methods, functions, and other compiled objects.

With no argument, disassemble the last traceback.

Compiled objects currently include generator objects, async generator
objects, and coroutine objects, all of which store their code object
in a special attribute.
'''
                    if x:
                        pass
                    return None
                    if hasattr(x, '__func__'):
                        pass
                    if hasattr(x, '__func__'):
                        pass
                    x = x.__func__
                    if hasattr(x, '__code__'):
                        pass
                    if hasattr(x, '__code__'):
                        x = x.__code__
                    elif hasattr(x, 'gi_code'):
                        pass
                    if hasattr(x, 'gi_code'):
                        x = x.gi_code
                    elif hasattr(x, 'ag_code'):
                        pass
                    if hasattr(x, 'ag_code'):
                        x = x.ag_code
                    elif hasattr(x, 'cr_code'):
                        pass
                    if hasattr(x, 'cr_code'):
                        pass
                    x = x.cr_code
                    if hasattr(x, '__dict__'):
                        pass
                    if hasattr(x, '__dict__'):
                        items = sorted(x.__dict__.items())
                        for None in items:
                            if ():
                                if isinstance(x1, _have_code):
                                    pass
                                if not isinstance(x1, _have_code):
                                    continue
                                
                                try:
                                    dis(x1, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)
                                except TypeError:
                                    msg = None
                                    print('Sorry:', msg, file = file)

                                print(file = file)
                                continue
                                return None
                                if hasattr(x, 'co_code'):
                                    pass
                                if hasattr(x, 'co_code'):
                                    _disassemble_recursive(x, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)
                                return None
                                if isinstance(x, (bytes, bytearray)):
                                    pass
                                if isinstance(x, (bytes, bytearray)):
                                    4 + len(str(len(labels_map))) = _make_labels_map(x)
                                    if show_offsets:
                                        pass
                                    formatter = Formatter(file = file, offset_width = len(str(max(len(x) - 2, 9999))) if show_offsets else 0, label_width = label_width, show_caches = show_caches)
                                    arg_resolver = ArgResolver(labels_map = labels_map)
                                    _disassemble_bytes(x, arg_resolver = arg_resolver, formatter = formatter)
                    return None
                    if isinstance(x, str):
                        pass
                    if isinstance(x, str):
                        _disassemble_str(x, file = file, depth = depth, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)
                    return None
                    raise TypeError("don't know how to disassemble %s objects" % type(x).__name__)

if (lambda tb, *, file: if tb:
try:
if hasattr(sys, 'last_exc'):
passif tb.tb_next:
passif tb.tb_next:
if tb.tb_next:
passif tb.tb_next.tb_next:
passif tb.tb_next.tb_next:
continuedisassemble(tb.tb_frame.f_code, tb.tb_lasti, file = file, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)Noneif AttributeError:
passraise RuntimeError('no last traceback to disassemble'), None) and (lambda tb, *, file: if tb:
try:
if hasattr(sys, 'last_exc'):
passif tb.tb_next:
passif tb.tb_next:
if tb.tb_next:
passif tb.tb_next.tb_next:
passif tb.tb_next.tb_next:
continuedisassemble(tb.tb_frame.f_code, tb.tb_lasti, file = file, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)Noneif AttributeError:
passraise RuntimeError('no last traceback to disassemble'), None):
    
    def distb(tb, *, file, show_caches, adaptive, show_offsets):
        '''Disassemble a traceback (default: last traceback).'''
        if tb:
            
            try:
                if hasattr(sys, 'last_exc'):
                    pass

            if tb.tb_next:
                pass
            if tb.tb_next:
                if tb.tb_next:
                    pass
                if tb.tb_next.tb_next:
                    pass
                if tb.tb_next.tb_next:
                    continue
        disassemble(tb.tb_frame.f_code, tb.tb_lasti, file = file, show_caches = show_caches, adaptive = adaptive, show_offsets = show_offsets)
        return None
        if AttributeError:
            pass
        raise RuntimeError('no last traceback to disassemble'), None

COMPILER_FLAG_NAMES = {
    1: 'OPTIMIZED',
    2: 'NEWLOCALS',
    4: 'VARARGS',
    8: 'VARKEYWORDS',
    16: 'NESTED',
    32: 'GENERATOR',
    64: 'NOFREE',
    128: 'COROUTINE',
    256: 'ITERABLE_COROUTINE',
    512: 'ASYNC_GENERATOR' }

def pretty_flags(flags):
    '''Return pretty representation of code flags.'''
    names = []
    for i in range(32):
        flag = 1 << i
        if flags & flag:
            pass
        if not flags & flag:
            continue
        names.append(COMPILER_FLAG_NAMES.get(flag, hex(flag)))
        flags ^= flag
        if flags:
            pass
        if flags:
            continue
    names.append(hex(flags))
    return ', '.join(names)


def _Unknown():
    '''_Unknown'''
    __firstlineno__ = 175
    
    def __repr__(self):
        return '<unknown>'

    __static_attributes__ = ()

_Unknown = None(_Unknown, '_Unknown')

class UNKNOWN:
