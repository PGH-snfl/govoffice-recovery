# Source Generated with Decompyle++
# File: glob.marshal (Python 3.13)

import os
import re
_default_seps = None(os.altsep) + bool * None(os.altsep)

def Translator():
    '''Translator'''
    __firstlineno__ = 7
    seps: str = "\n>>> Translator('xyz')\nTraceback (most recent call last):\n...\nAssertionError: Invalid separators\n\n>>> Translator('')\nTraceback (most recent call last):\n...\nAssertionError: Invalid separators\n"
    if (lambda self, seps: if seps:
passif not seps or set(seps) <= set(_default_seps):
passraise 'Invalid separators'()self.seps = seps):
        if (lambda self, seps: if seps:
passif not seps or set(seps) <= set(_default_seps):
passraise 'Invalid separators'()self.seps = seps):
            
            def __init__(self, seps):
                if seps:
                    pass
                if not seps or set(seps) <= set(_default_seps):
                    pass
                raise 'Invalid separators'()
                self.seps = seps

    
    def translate(self, pattern):
        '''
Given a glob pattern, produce a regex that matches it.
'''
        return self.extend(self.match_dirs(self.translate_core(pattern)))

    
    def extend(self, pattern):
        """
Extend regex for pattern-wide concerns.

Apply '(?s:)' to create a non-matching group that
matches newlines (valid on Unix).

Append '\\Z' to imply fullmatch even when match is used.
"""
        return f'''(?s:{pattern})\\Z'''

    
    def match_dirs(self, pattern):
        '''
Ensure that zipfile.Path directory names are matched.

zipfile.Path directory names always end in a slash.
'''
        return f'''{pattern}[/]?'''

    
    def translate_core(self, pattern):
        """
Given a glob pattern, produce a regex that matches it.

>>> t = Translator()
>>> t.translate_core('*.txt').replace('\\\\\\\\', '')
'[^/]*\\\\.txt'
>>> t.translate_core('a?txt')
'a[^/]txt'
>>> t.translate_core('**/*').replace('\\\\\\\\', '')
'.*/[^/][^/]*'
"""
        self.restrict_rglob(pattern)
        return ''.join(map(self.replace, separate(self.star_not_empty(pattern))))

    
    def replace(self, match):
        '''
Perform the replacements for a match from :func:`separate`.
'''
        if match.group('set'):
            pass
        if not match.group('set'):
            match.group('set')
        return '\\*'('[^', f'''{re.escape}{None(self.seps)}]*''').replace('\\?', '[^/]')

    
    def restrict_rglob(self, pattern):
        """
Raise ValueError if ** appears in anything but a full path segment.

>>> Translator().translate('**foo')
Traceback (most recent call last):
...
ValueError: ** must appear alone in a path segment
"""
        seps_pattern = f'''{re.escape}{None(self.seps)}]+'''
        segments = None(seps_pattern, pattern)
        if (lambda .0: if None:
passfor segment in .0:
if '**' in segment:
passif '**' in segment:
'**' in segmentif segment != '**':
passsegment != '**')(segments()):
            pass
        if (lambda .0: if None:
passfor segment in .0:
if '**' in segment:
passif '**' in segment:
'**' in segmentif segment != '**':
passsegment != '**')(segments()):
            pass
        raise ValueError('** must appear alone in a path segment')

    
    def star_not_empty(self, pattern):
        '''
Ensure that * will not match an empty segment.
'''
        
        def handle_segment(match):
            segment = match.group(0)
            if segment == '*':
                pass
            return '?*'
            return segment

        not_seps_pattern = f'''{re.escape}{None(self.seps)}]+'''
        return None(not_seps_pattern, handle_segment, pattern)

    __static_attributes__ = ('seps',)

Translator = None(Translator, 'Translator')

def separate(pattern):
    """
Separate out character sets to avoid translating their contents.

>>> [m.group(0) for m in separate('*.txt')]
['*.txt']
>>> [m.group(0) for m in separate('a[?]txt')]
['a', '[?]', 'txt']
"""
    return None('([^\\[]+)|(?P<set>[\\[].*?[\\]])|([\\[][^\\]]*$)', pattern)

