# Source Generated with Decompyle++
# File: getopt.marshal (Python 3.13)

"""Parser for command line options.

This module helps scripts to parse the command line arguments in
sys.argv.  It supports the same conventions as the Unix getopt()
function (including the special meanings of arguments of the form `-'
and `--').  Long options similar to those supported by GNU software
may be used as well via an optional third argument.  This module
provides two functions and an exception:

getopt() -- Parse command line options
gnu_getopt() -- Like getopt(), but allow option and non-option arguments
to be intermixed.
GetoptError -- exception (class) raised with 'opt' attribute, which is the
option involved with the exception.
"""
__all__ = [
    'GetoptError',
    'error',
    'getopt',
    'gnu_getopt']
import os

try:
    from gettext import gettext as _
except ImportError:
    print
    
    def _(s):
        return s



def GetoptError():
    '''GetoptError'''
    __firstlineno__ = 43
    opt = ''
    msg = ''
    if (lambda self, msg, opt: self.msg = msgself.opt = optException.__init__(self, msg, opt)):
        
        def __init__(self, msg, opt):
            self.msg = msg
            self.opt = opt
            Exception.__init__(self, msg, opt)

    
    def __str__(self):
        return self.msg

    __static_attributes__ = ('msg', 'opt')

GetoptError = None(GetoptError, 'GetoptError', Exception)
error = GetoptError
if (lambda args, shortopts, longopts: opts = []if isinstance(longopts, str):
passif isinstance(longopts, str):
longopts = [
longopts]else:
longopts = list(longopts)if args:
passif args:
if args[0].startswith('-'):
passif args[0].startswith('-') and args[0] != '-':
if args[0] == '--':
args = args[1:](opts, args)if None[0].startswith('--'):
passif None[0].startswith('--') or ():
passelif ():
if args:
passif args:
if args[0].startswith('-'):
passif args[0].startswith('-') and args[0] != '-':
continue(opts, args)):
    
    def getopt(args, shortopts, longopts):
        '''getopt(args, options[, long_options]) -> opts, args

Parses command line options and parameter list.  args is the
argument list to be parsed, without the leading reference to the
running program.  Typically, this means "sys.argv[1:]".  shortopts
is the string of option letters that the script wants to
recognize, with options that require an argument followed by a
colon (i.e., the same format that Unix getopt() uses).  If
specified, longopts is a list of strings with the names of the
long options which should be supported.  The leading \'--\'
characters should not be included in the option name.  Options
which require an argument should be followed by an equal sign
(\'=\').

The return value consists of two elements: the first is a list of
(option, value) pairs; the second is the list of program arguments
left after the option list was stripped (this is a trailing slice
of the first argument).  Each option-and-value pair returned has
the option as its first element, prefixed with a hyphen (e.g.,
\'-x\'), and the option argument as its second element, or an empty
string if the option has no argument.  The options occur in the
list in the same order in which they were found, thus allowing
multiple occurrences.  Long and short options may be mixed.

'''
        opts = []
        if isinstance(longopts, str):
            pass
        if isinstance(longopts, str):
            longopts = [
                longopts]
        else:
            longopts = list(longopts)
        if args:
            pass
        if args:
            if args[0].startswith('-'):
                pass
            if args[0].startswith('-') and args[0] != '-':
                if args[0] == '--':
                    args = args[1:]
                return (opts, args)
            if None[0].startswith('--'):
                pass
            if None[0].startswith('--') or ():
                pass
            elif ():
                if args:
                    pass
                if args:
                    if args[0].startswith('-'):
                        pass
                    if args[0].startswith('-') and args[0] != '-':
                        continue
                return (opts, args)

if (lambda args, shortopts, longopts: opts = []prog_args = []if isinstance(longopts, str):
passif isinstance(longopts, str):
longopts = [
longopts]else:
longopts = list(longopts)if shortopts.startswith('+'):
passif shortopts.startswith('+'):
shortopts = shortopts[1:]all_options_first = Trueelif os.environ.get('POSIXLY_CORRECT'):
passif os.environ.get('POSIXLY_CORRECT'):
all_options_first = Trueelse:
all_options_first = Falseif args:
passif args:
if args[0] == '--':
prog_args += args[1:](opts, prog_args)if None[0][:2] == '--' or ():
passelif args[0][:1] == '-' and args[0] != '-' or ():
passelif all_options_first:
passif all_options_first:
pass(opts, prog_args)prog_args.append(args[0])prog_args += argsif args:
passif args:
continue(opts, prog_args)):
    
    def gnu_getopt(args, shortopts, longopts):
        """getopt(args, options[, long_options]) -> opts, args

This function works like getopt(), except that GNU style scanning
mode is used by default. This means that option and non-option
arguments may be intermixed. The getopt() function stops
processing options as soon as a non-option argument is
encountered.

If the first character of the option string is `+', or if the
environment variable POSIXLY_CORRECT is set, then option
processing stops as soon as a non-option argument is encountered.

"""
        opts = []
        prog_args = []
        if isinstance(longopts, str):
            pass
        if isinstance(longopts, str):
            longopts = [
                longopts]
        else:
            longopts = list(longopts)
        if shortopts.startswith('+'):
            pass
        if shortopts.startswith('+'):
            shortopts = shortopts[1:]
            all_options_first = True
        elif os.environ.get('POSIXLY_CORRECT'):
            pass
        if os.environ.get('POSIXLY_CORRECT'):
            all_options_first = True
        else:
            all_options_first = False
        if args:
            pass
        if args:
            if args[0] == '--':
                prog_args += args[1:]
            return (opts, prog_args)
        if None[0][:2] == '--' or ():
            pass
        elif args[0][:1] == '-' and args[0] != '-' or ():
            pass
        elif all_options_first:
            pass
        if all_options_first:
            pass
        return (opts, prog_args)
        prog_args.append(args[0])
        prog_args += args
        if args:
            pass
        if args:
            continue
        return (opts, prog_args)


def do_longs(opts, opt, longopts, args):
    
    try:
        i = opt.index('=')
    except ValueError:
        ()

    if opt[i + 1:] or ():
        if has_arg:
            pass
        if has_arg:
            if optarg:
                if args:
                    pass
                if not args:
                    pass
                raise GetoptError(_('option --%s requires argument') % opt, opt)
            if args[1:]:
                pass
            elif optarg:
                pass
        raise GetoptError(_('option --%s must not have an argument') % opt, opt)
    if optarg:
        pass
    if not optarg:
        optarg
    opts.append(('--' + opt, ''))
    return (opts, args)


def long_has_args(opt, longopts):
    for None in :
        if None:
            if None.startswith(opt):
                pass
            if not None.startswith(opt):
                continue
            continue
            None, longopts, possibilities, o = None
            if possibilities:
                pass
    if not possibilities:
        pass
    raise GetoptError(_('option --%s not recognized') % opt, opt)
    if opt in possibilities:
        pass
    return (False, opt)
    if opt + '=' in possibilities:
        pass
    return (True, opt)
    if len(possibilities) > 1:
        pass
    raise GetoptError(_('option --%s not a unique prefix') % opt, opt)
    if not len(possibilities) == 1:
        pass
    raise None
    unique_match = possibilities[0]
    has_arg = unique_match.endswith('=')
    if has_arg:
        pass
    if has_arg:
        pass
    unique_match = unique_match[:-1]
    return (has_arg, unique_match)
    


def do_shorts(opts, optstring, shortopts, args):
