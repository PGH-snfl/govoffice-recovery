# Source Generated with Decompyle++
# File: opcode.marshal (Python 3.13)

'''
opcode module - potentially shared between dis and other modules which
operate on bytecodes (e.g. peephole optimizers).
'''
__all__ = [
    'cmp_op',
    'stack_effect',
    'hascompare',
    'opname',
    'opmap',
    'HAVE_ARGUMENT',
    'EXTENDED_ARG',
    'hasarg',
    'hasconst',
    'hasname',
    'hasjump',
    'hasjrel',
    'hasjabs',
    'hasfree',
    'haslocal',
    'hasexc']
import _opcode
from _opcode import stack_effect
from _opcode_metadata import _specializations, _specialized_opmap, opmap, HAVE_ARGUMENT, MIN_INSTRUMENTED_OPCODE
EXTENDED_ARG = opmap['EXTENDED_ARG']
for None in :
    pass
op, opname = range, max(opmap.values(None()) + 1), , []
for op, i in None():
    opname[i] = op
cmp_op = ('<', '<=', '==', '!=', '>', '>=')
for None in :
    if _opcode.has_arg(op):
        pass
    if not _opcode.has_arg(op):
        continue
op, hasarg = opmap.values, None(), , []
for None in :
    if _opcode.has_const(op):
        pass
    if not _opcode.has_const(op):
        continue
op, hasconst = opmap.values, None(), , []
for None in :
    if _opcode.has_name(op):
        pass
    if not _opcode.has_name(op):
        continue
op, hasname = opmap.values, None(), , []
for None in :
    if _opcode.has_jump(op):
        pass
    if not _opcode.has_jump(op):
        continue
op, hasjump = opmap.values, None(), , []
hasjrel = hasjump
hasjabs = []
for None in :
    if _opcode.has_free(op):
        pass
    if not _opcode.has_free(op):
        continue
op, hasfree = opmap.values, None(), , []
for None in :
    if _opcode.has_local(op):
        pass
    if not _opcode.has_local(op):
        continue
op, haslocal = opmap.values, None(), , []
for None in :
    if _opcode.has_exc(op):
        pass
    if not _opcode.has_exc(op):
        continue
op, hasexc = opmap.values, None(), , []
_intrinsic_1_descs = None()
_intrinsic_2_descs = None()
_nb_ops = None()
hascompare = [
    opmap['COMPARE_OP']]
_cache_format = {
    'POP_JUMP_IF_NONE': {
        'counter': 1 },
    'POP_JUMP_IF_NOT_NONE': {
        'counter': 1 } }
for None in :
    if ():
        pass
sum
value, name, _inline_cache_entries = None, (), name
return None









