# Source Generated with Decompyle++
# File: signal.marshal (Python 3.13)

import _signal
None(import _signal)
from enum import IntEnum as _IntEnum
_globals = None()
None('Signals', __name__, (lambda name: if name.isupper():
passif name.isupper():
name.isupper()if name.startswith('SIG'):
passif name.startswith('SIG'):
name.startswith('SIG')if name.startswith('SIG_'):
passif not name.startswith('SIG_'):
passif not not name.startswith('SIG_'):
not name.startswith('SIG_')name.startswith('CTRL_')))
None('Handlers', __name__, (lambda name: name in ('SIG_DFL', 'SIG_IGN')))
if 'pthread_sigmask' in _globals:
    pass
None('Sigmasks', __name__, (lambda name: name in ('SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK')))

def _int_to_enum(value, enum_klass):
    """Convert a possible numeric value to an IntEnum member.
If it's not a known member, return the value itself.
"""
    if isinstance(value, int):
        pass
    if not isinstance(value, int):
        pass
    return value
    
    try:
        pass
    except ValueError:
        pass



def _enum_to_int(value):
    """Convert an IntEnum member to a numeric value.
If it's not an IntEnum member return the value itself.
"""
    
    try:
        pass
    except (ValueError, TypeError):
        pass



def _wraps(wrapped):
