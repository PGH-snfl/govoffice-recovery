# Source Generated with Decompyle++
# File: argparse.marshal (Python 3.13)

"""Command-line parsing library

This module is an optparse-inspired command-line parsing library that:

    - handles both optional and positional arguments
    - produces highly informative usage messages
    - supports parsers that dispatch to sub-parsers

The following is a simple usage example that sums integers from the
command-line and writes the result to a file::

    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'integers', metavar='int', nargs='+', type=int,
        help='an integer to be summed')
    parser.add_argument(
        '--log', default=sys.stdout, type=argparse.FileType('w'),
        help='the file where the sum should be written')
    args = parser.parse_args()
    args.log.write('%s' % sum(args.integers))
    args.log.close()

The module contains the following public classes:

    - ArgumentParser -- The main entry point for command-line parsing. As the
        example above shows, the add_argument() method is used to populate
        the parser with actions for optional and positional arguments. Then
        the parse_args() method is invoked to convert the args at the
        command-line into an object with attributes.

    - ArgumentError -- The exception raised by ArgumentParser objects when
        there are errors with the parser's actions. Errors raised while
        parsing the command-line are caught by ArgumentParser and emitted
        as command-line messages.

    - FileType -- A factory for defining types of files to be created. As the
        example above shows, instances of FileType are typically passed as
        the type= argument of add_argument() calls.

    - Action -- The base class for parser actions. Typically actions are
        selected by passing strings like 'store_true' or 'append_const' to
        the action= argument of add_argument(). However, for greater
        customization of ArgumentParser actions, subclasses of Action may
        be defined and passed as the action= argument.

    - HelpFormatter, RawDescriptionHelpFormatter, RawTextHelpFormatter,
        ArgumentDefaultsHelpFormatter -- Formatter classes which
        may be passed as the formatter_class= argument to the
        ArgumentParser constructor. HelpFormatter is the default,
        RawDescriptionHelpFormatter and RawTextHelpFormatter tell the parser
        not to change the formatting for help text, and
        ArgumentDefaultsHelpFormatter adds information about argument defaults
        to the help.

All other classes in this module are considered implementation details.
(Also note that HelpFormatter and RawDescriptionHelpFormatter are only
considered public as object names -- the API of the formatter objects is
still considered an implementation detail.)
"""
__version__ = '1.1'
__all__ = [
    'ArgumentParser',
    'ArgumentError',
    'ArgumentTypeError',
    'BooleanOptionalAction',
    'FileType',
    'HelpFormatter',
    'ArgumentDefaultsHelpFormatter',
    'RawDescriptionHelpFormatter',
    'RawTextHelpFormatter',
    'MetavarTypeHelpFormatter',
    'Namespace',
    'Action',
    'ONE_OR_MORE',
    'OPTIONAL',
    'PARSER',
    'REMAINDER',
    'SUPPRESS',
    'ZERO_OR_MORE']
import os as _os
import re as _re
import sys as _sys
from gettext import gettext as _, ngettext
SUPPRESS = '==SUPPRESS=='
OPTIONAL = '?'
ZERO_OR_MORE = '*'
ONE_OR_MORE = '+'
PARSER = 'A...'
REMAINDER = '...'
_UNRECOGNIZED_ARGS_ATTR = '_unrecognized_args'

def _AttributeHolder():
    '''_AttributeHolder'''
    __firstlineno__ = 107
    __doc__ = "Abstract base class that provides __repr__.\n\nThe __repr__ method returns a string in the format::\n    ClassName(attr=name, attr=name, ...)\nThe attributes are determined either by a class-level attribute,\n'_kwarg_names', or by inspecting the instance __dict__.\n"
    
    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = []
        star_args = { }
        for arg in self._get_args():
            arg_strings.append(repr(arg))
        for None in self._get_kwargs():
            if ():
                if name.isidentifier():
                    pass
                if name.isidentifier():
                    arg_strings.append(f'''{name}={value}''')
                    continue
                continue
                if star_args:
                    pass
                if star_args:
                    pass
        arg_strings.append('**%s' % repr(star_args))
        return f'''{type_name}({', '.join(arg_strings)})'''

    
    def _get_kwargs(self):
        return list(self.__dict__.items())

    
    def _get_args(self):
        return []

    __static_attributes__ = ()

_AttributeHolder = None(_AttributeHolder, '_AttributeHolder', object)

def _copy_items(items):
    if items:
        pass
    return []
    if type(items) is list:
        pass
    return items[:]
    import copy
    return copy.copy(items)


def HelpFormatter():
    '''HelpFormatter'''
    __firstlineno__ = 155
    __doc__ = 'Formatter for generating usage messages and argument help strings.\n\nOnly the name of this class is considered a public API. All the methods\nprovided by the class are considered an implementation detail.\n'
    if (lambda self, prog, indent_increment, max_help_position, width: if width:
import shutilwidth = shutil.get_terminal_size().columnswidth -= 2self._prog = progself._indent_increment = indent_incrementself._max_help_position = min(max_help_position, max(width - 20, indent_increment * 2))self._width = widthself._current_indent = 0self._level = 0self._action_max_length = 0self._root_section = self._Section(self, None)self._current_section = self._root_sectionself._whitespace_matcher = None('\\s+', _re.ASCII)self._long_break_matcher = None('\\n\\n\\n+')):
        
        def __init__(self, prog, indent_increment, max_help_position, width):
            if width:
                import shutil
                width = shutil.get_terminal_size().columns
            width -= 2
            self._prog = prog
            self._indent_increment = indent_increment
            self._max_help_position = min(max_help_position, max(width - 20, indent_increment * 2))
            self._width = width
            self._current_indent = 0
            self._level = 0
            self._action_max_length = 0
            self._root_section = self._Section(self, None)
            self._current_section = self._root_section
            self._whitespace_matcher = None('\\s+', _re.ASCII)
            self._long_break_matcher = None('\\n\\n\\n+')

    
    def _indent(self):
        pass

    
    def _dedent(self):
        if not self._current_indent >= 0:
            pass
        raise 'Indent decreased below 0.'()

    
    def _Section():
        '''HelpFormatter._Section'''
        __firstlineno__ = 203
        if (lambda self, formatter, parent, heading: self.formatter = formatterself.parent = parentself.heading = headingself.items = []):
            
            def __init__(self, formatter, parent, heading):
                self.formatter = formatter
                self.parent = parent
                self.heading = heading
                self.items = []

        
        def format_help(self):
            if self.parent:
                pass
            self.formatter._indent()
            join = self.formatter._join_parts
            for None in :
                if ():
                    continue
                    , [], None, ()(args, func) = join, None, self.items
                    if self.parent:
                        pass
            self.formatter._dedent()
            if item_help:
                pass
            if not item_help:
                pass
            return ''
            return None([
                '\n',
                heading,
                item_help,
                '\n'])
            

        __static_attributes__ = ('formatter', 'heading', 'items', 'parent')

    _Section = None(_Section, '_Section', object)
    
    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    
    def start_section(self, heading):
        self._indent()
        section = self._Section(self, self._current_section, heading)
        self._add_item(section.format_help, [])
        self._current_section = section

    
    def end_section(self):
        self._current_section = self._current_section.parent
        self._dedent()

    
    def add_text(self, text):
        if text is not SUPPRESS:
            if text:
                pass
            return None
        return None

    if (lambda self, usage, actions, groups, prefix: if usage is not SUPPRESS:
args = (usage, actions, groups, prefix)self._add_item(self._format_usage, args)None):
        
        def add_usage(self, usage, actions, groups, prefix):
            if usage is not SUPPRESS:
                args = (usage, actions, groups, prefix)
                self._add_item(self._format_usage, args)
            return None

    
    def add_argument(self, action):
        if action.help is not SUPPRESS:
            get_invocation = self._format_action_invocation
            invocation_lengths = [
                get_invocation(None(action)) + self._current_indent]
            for subaction in self._iter_indented_subactions(action):
                len(get_invocation(None(subaction)) + self._current_indent)
            action_length = max(invocation_lengths)
            self._action_max_length = max(self._action_max_length, action_length)
            self._add_item(self._format_action, [
                action])
        return None

    
    def add_arguments(self, actions):
        for action in actions:
            self.add_argument(action)

    
    def format_help(self):
        help = self._root_section.format_help()
        if help:
            pass
        if help:
            help = self._long_break_matcher.sub('\n\n', help)
        help = help.strip('\n') + '\n'
        return help

    
    def _join_parts(self, part_strings):
        for None in :
            if part:
                pass
            if not part:
                continue
            if not part is not SUPPRESS:
                continue
        return ''.join, part_strings, , [](part,)
        

    
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix:
            pass
        prefix = _('usage: ')
        if usage:
            usage = None % dict(prog = self._prog)
        elif usage:
            if actions:
                pass
            if not actions:
                usage = None % dict(prog = self._prog)
            elif usage:
                prog = None % dict(prog = self._prog)
                optionals = []
                positionals = []
                for action in actions:
                    if action.option_strings:
                        pass
                    if action.option_strings:
                        optionals.append(action)
                        continue
                    positionals.append(action)
                format = self._format_actions_usage
                action_usage = None(optionals + positionals, groups)
                for None in :
                    if None:
                        if None:
                            pass
                        if not None:
                            continue
                        continue
                        None, ' '.join, (prog, action_usage)(s,) = format
                        text_width = self._width - self._current_indent
                        if len(prefix) + len(usage) > text_width:
                            opt_parts = self._get_actions_usage_parts(optionals, groups)
                            pos_parts = self._get_actions_usage_parts(positionals, groups)
                            if (lambda parts, indent, prefix: lines = []line = []indent_length = len(indent)for part in parts:
if line_len + 1 + len(part) > text_width:
if line:
passif line:
lines.append(indent + ' '.join(line))line = []line_len = indent_length - 1line.append(part)line_len += len(part) + 1if line:
passif line:
passlines.append(indent + ' '.join(line))if prefix:
lines[0] = lines[0][indent_length:]lines):
                                if (lambda parts, indent, prefix: lines = []line = []indent_length = len(indent)for part in parts:
if line_len + 1 + len(part) > text_width:
if line:
passif line:
lines.append(indent + ' '.join(line))line = []line_len = indent_length - 1line.append(part)line_len += len(part) + 1if line:
passif line:
passlines.append(indent + ' '.join(line))if prefix:
lines[0] = lines[0][indent_length:]lines):
                                    
                                    def get_lines(parts, indent, prefix):
                                        lines = []
                                        line = []
                                        indent_length = len(indent)
                                        for part in parts:
                                            if line_len + 1 + len(part) > text_width:
                                                if line:
                                                    pass
                                                if line:
                                                    lines.append(indent + ' '.join(line))
                                                    line = []
                                            line_len = indent_length - 1
                                            line.append(part)
                                            line_len += len(part) + 1
                                        if line:
                                            pass
                                        if line:
                                            pass
                                        lines.append(indent + ' '.join(line))
                                        if prefix:
                                            lines[0] = lines[0][indent_length:]
                                        return lines

        usage = '\n'.join(lines)
        return f'''{prefix}{usage}\n\n'''
        

    
    def _format_actions_usage(self, actions, groups):
        return ' '.join(self._get_actions_usage_parts(actions, groups))

    
    def _get_actions_usage_parts(self, actions, groups):
        group_actions = set()
        inserts = { }
        for group in groups:
            if group._group_actions:
                pass
            if not group._group_actions:
                pass
            raise ValueError(f'''empty group {group}''')
            if (lambda .0: if None:
passfor None in .0:
if None and None.help is SUPPRESS:
pass)(group._group_actions()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None and None.help is SUPPRESS:
pass)(group._group_actions()):
                continue
            
            try:
                start = actions.index(group._group_actions[0])

            end = start + len(group._group_actions)
            if actions[start:end] == group._group_actions:
                group_actions.update(group._group_actions)
                inserts[(start, end)] = group
                continue
        parts = []
        for action in actions:
            if action.help is SUPPRESS:
                part = None
            elif action.option_strings:
                pass
            if not action.option_strings:
                default = self._get_default_metavar_for_positional(action)
                part = self._format_args(action, default)
                if action in group_actions and part[0] == '[' and part[-1] == ']':
                    pass
                part = part[1:-1]
            else:
                option_string = action.option_strings[0]
                if action.nargs == 0:
                    part = action.format_usage()
                else:
                    default = self._get_default_metavar_for_optional(action)
                    args_string = self._format_args(action, default)
                    part = f'''{option_string} {args_string}'''
                if action.required:
                    pass
                if action.required and action not in group_actions:
                    pass
                part = '[%s]' % part
            parts.append(part)
        inserted_separators_indices = set()
        for None in sorted(inserts, reverse = True):
            if ():
                for None in :
                    if None:
                        if None:
                            continue
                        continue
                        , [], group_parts, item = inserts[(start, end)], parts[start:end]
                        group_size = len(group_parts)
                        if group.required:
                            pass
                        group_parts[0] = open + group_parts[0]
                        group_parts[-1] = group_parts[-1] + close
                        for i, part in enumerate(group_parts[:-1], start = start):
                            if not i not in inserted_separators_indices:
                                continue
                            parts[i] = part + ' |'
                            inserted_separators_indices.add(i)
                        None if group.required else ()
                        parts[start + group_size - 1] = group_parts[-1]
                        for i in range(start + group_size, end):
                            parts[i] = None
                        continue
                        for None in :
                            if None:
                                if None:
                                    continue
                                continue
                                return item,
                            if ValueError:
                                continue
                        
                        

    
    def _format_text(self, text):
        if '%(prog)' in text:
            pass
        text = None % dict(prog = self._prog)
        text_width = max(self._width - self._current_indent, 11)
        indent = ' ' * self._current_indent
        return self._fill_text(text, text_width, indent) + '\n\n'

    
    def _format_action(self, action):
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)
        if action.help:
            pass
        if not action.help:
            tup = (self._current_indent, '', action_header)
            action_header = '%*s%s\n' % tup
        elif len(action_header) <= action_width:
            tup = (self._current_indent, '', action_width, action_header)
            action_header = '%*s%-*s  ' % tup
            indent_first = 0
        else:
            tup = (self._current_indent, '', action_header)
            action_header = '%*s%s\n' % tup
            indent_first = help_position
        parts = [
            action_header]
        if action.help:
            pass
        if action.help:
            if action.help.strip():
                pass
            if action.help.strip():
                help_text = self._expand_help(action)
                if help_text:
                    pass
                if help_text:
                    help_lines = self._split_lines(help_text, help_width)
                    parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
                    for line in help_lines[1:]:
                        parts.append('%*s%s\n' % (help_position, '', line))
            elif action_header.endswith('\n'):
                pass
        if not action_header.endswith('\n'):
            pass
        parts.append('\n')
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))
        return self._join_parts(parts)

    
    def _format_action_invocation(self, action):
        if action.option_strings:
            pass
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
        return self._metavar_formatter(action, default)(None(1))
        if action.nargs == 0:
            pass
        return ', '.join(action.option_strings)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

    
    def _metavar_formatter(self, action, default_metavar):
