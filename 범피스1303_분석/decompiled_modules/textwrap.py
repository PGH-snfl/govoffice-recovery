# Source Generated with Decompyle++
# File: textwrap.marshal (Python 3.13)

'''Text wrapping and filling.
'''
import re
__all__ = [
    'TextWrapper',
    'wrap',
    'fill',
    'dedent',
    'indent',
    'shorten']
_whitespace = '\t\n\x0b\x0c\r '

def TextWrapper():
    '''TextWrapper'''
    __firstlineno__ = 17
    __doc__ = '\nObject for wrapping/filling text.  The public interface consists of\nthe wrap() and fill() methods; the other methods are just there for\nsubclasses to override in order to tweak the default behaviour.\nIf you want to completely replace the main wrapping algorithm,\nyou\'ll probably have to override _wrap_chunks().\n\nSeveral instance attributes control various aspects of wrapping:\n  width (default: 70)\n    the maximum width of wrapped lines (unless break_long_words\n    is false)\n  initial_indent (default: "")\n    string that will be prepended to the first line of wrapped\n    output.  Counts towards the line\'s width.\n  subsequent_indent (default: "")\n    string that will be prepended to all lines save the first\n    of wrapped output; also counts towards each line\'s width.\n  expand_tabs (default: true)\n    Expand tabs in input text to spaces before further processing.\n    Each tab will become 0 .. \'tabsize\' spaces, depending on its position\n    in its line.  If false, each tab is treated as a single character.\n  tabsize (default: 8)\n    Expand tabs in input text to 0 .. \'tabsize\' spaces, unless\n    \'expand_tabs\' is false.\n  replace_whitespace (default: true)\n    Replace all whitespace characters in the input text by spaces\n    after tab expansion.  Note that if expand_tabs is false and\n    replace_whitespace is true, every tab will be converted to a\n    single space!\n  fix_sentence_endings (default: false)\n    Ensure that sentence-ending punctuation is always followed\n    by two spaces.  Off by default because the algorithm is\n    (unavoidably) imperfect.\n  break_long_words (default: true)\n    Break words longer than \'width\'.  If false, those words will not\n    be broken, and some lines might be longer than \'width\'.\n  break_on_hyphens (default: true)\n    Allow breaking hyphenated words. If true, wrapping will occur\n    preferably on whitespaces and right after hyphens part of\n    compound words.\n  drop_whitespace (default: true)\n    Drop leading and trailing whitespace from lines.\n  max_lines (default: None)\n    Truncate wrapped lines.\n  placeholder (default: \' [...]\')\n    Append to the last line of truncated text.\n'
    unicode_whitespace_trans = None(ord, _whitespace)(ord, None(' '))
    word_punct = '[\\w!"\\\'&.,?]'
    letter = '[^\\d\\W]'
    whitespace = re.escape % None(_whitespace)
    nowhitespace = '[^' + whitespace[1:]
    wordsep_re = None('\n        ( # any whitespace\n          %(ws)s+\n        | # em-dash between words\n          (?<=%(wp)s) -{2,} (?=\\w)\n        | # word, possibly hyphenated\n          %(nws)s+? (?:\n            # hyphenated word\n              -(?: (?<=%(lt)s{2}-) | (?<=%(lt)s-%(lt)s-))\n              (?= %(lt)s -? %(lt)s)\n            | # end of word\n              (?=%(ws)s|\\Z)\n            | # em-dash\n              (?<=%(wp)s) (?=-{2,}\\w)\n            )\n        )' % {
        'wp': word_punct,
        'lt': letter,
        'ws': whitespace,
        'nws': nowhitespace }, re.VERBOSE)
    del word_punct
    del letter
    del nowhitespace
    wordsep_simple_re = None('(%s+)' % whitespace)
    del whitespace
    sentence_end_re = None('[a-z][\\.\\!\\?][\\"\\\']?\\Z')
    if (lambda self, width, initial_indent, subsequent_indent, expand_tabs, replace_whitespace, fix_sentence_endings, break_long_words, drop_whitespace, break_on_hyphens, tabsize, *, max_lines, placeholder, 