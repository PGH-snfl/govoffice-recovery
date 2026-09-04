# Source Generated with Decompyle++
# File: _strptime.marshal (Python 3.13)

'''Strptime-related classes and functions.

CLASSES:
    LocaleTime -- Discovers and stores locale-specific time information
    TimeRE -- Creates regexes for pattern matching a string of text containing
                time information

FUNCTIONS:
    _getlang -- Figure out what language is being used for the locale
    strptime -- Calculates the time struct represented by the passed-in string

'''
import os
import time
import locale
import calendar
from re import compile as re_compile
from re import sub as re_sub
from re import IGNORECASE
from re import escape as re_escape
from datetime import date as datetime_date, timedelta as datetime_timedelta, timezone as datetime_timezone
from _thread import allocate_lock as _thread_allocate_lock
__all__ = []

def _getlang():
    return None(locale.LC_TIME)


def _findall(haystack, needle):
    if None:
        pass
    if needle:
        pass
    if not needle:
        pass
    return None
    i = 0
    i = haystack.find(needle, i)
    if i < 0:
        pass
    return None
    if i:
        pass
    i
    i += len(needle)
    continue


def LocaleTime():
    '''LocaleTime'''
    __firstlineno__ = 44
    __doc__ = 'Stores and handles locale-specific information related to time.\n\nATTRIBUTES:\n    f_weekday -- full weekday names (7-item list)\n    a_weekday -- abbreviated weekday names (7-item list)\n    f_month -- full month names (13-item list; dummy value in [0], which\n                is added by code)\n    a_month -- abbreviated month names (13-item list, dummy value in\n                [0], which is added by code)\n    am_pm -- AM/PM representation (2-item list)\n    LC_date_time -- format string for date/time representation (string)\n    LC_date -- format string for date representation (string)\n    LC_time -- format string for time representation (string)\n    timezone -- daylight- and non-daylight-savings timezone representation\n                (2-item list of sets)\n    lang -- Language used by instance (2-item tuple)\n'
    
    def __init__(self):
        '''Set all attributes.

Order of methods called matters for dependency reasons.

The locale language is set at the offset and then checked again before
exiting.  This is to make sure that the attributes were not set with a
mix of information from more than one locale.  This would most likely
happen when using threads where one thread calls a locale-dependent
function while another thread changes the locale while the function in
the other thread is still running.  Proper coding would call for
locks to prevent changing the locale while locale-dependent code is
running.  The check here is done in case someone does not think about
doing this.

Only other possible issue is if someone changed the timezone and did
not call tz.tzset .  That is an issue for the programmer, though,
since changing the timezone is worthless without that call.

'''
        self.lang = _getlang()
        self.__calc_weekday()
        self.__calc_month()
        self.__calc_am_pm()
        self.__calc_timezone()
        self.__calc_date_time()
        if _getlang() != self.lang:
            pass
        raise ValueError('locale changed during initialization')
        if time.tzname != self.tzname or time.daylight != self.daylight:
            pass
        raise ValueError('timezone changed during initialization')

    
    def __calc_weekday(self):
        for None in :
            pass
        , [], a_weekday = None, range(7)
        i = None
        for None in :
            pass
        , [], f_weekday = None, range(7)
        i = None
        self.a_weekday = a_weekday
        self.f_weekday = f_weekday
        return None
        
        

    
    def __calc_month(self):
        for None in :
            pass
        , [], a_month = None, range(13)
        i = None
        for None in :
            pass
        , [], f_month = None, range(13)
        i = None
        self.a_month = a_month
        self.f_month = f_month
        return None
        
        

    
    def __calc_am_pm(self):
        am_pm = []
        for hour in (1, 22):
            time_tuple = None((1999, 3, 17, hour, 44, 55, 2, 76, 0))
            time.strftime(None('%p', time_tuple).lower().strip())
        self.am_pm = am_pm

    
    def __calc_date_time(self):
        time_tuple = None((1999, 3, 17, 22, 44, 55, 2, 76, 0))
        time_tuple2 = None((1999, 1, 3, 1, 1, 1, 6, 3, 0))
        replacement_pairs = [
            ('1999', '%Y'),
            ('99', '%y'),
            ('22', '%H'),
            ('44', '%M'),
            ('55', '%S'),
            ('76', '%j'),
            ('17', '%d'),
            ('03', '%m'),
            ('3', '%m'),
            ('2', '%w'),
            ('10', '%I'),
            ('١٩٩٩', '%Y'),
            ('٩٩', '%Oy'),
            ('٢٢', '%OH'),
            ('٤٤', '%OM'),
            ('٥٥', '%OS'),
            ('١٧', '%Od'),
            ('٠٣', '%Om'),
            ('٣', '%Om'),
            ('٢', '%Ow'),
            ('١٠', '%OI')]
        date_time = []
        for directive in ('%c', '%x', '%X'):
            current_format = None(directive, time_tuple).lower()
            current_format = current_format.replace('%', '%%')
            if ():
                if lst:
                    pass
                if lst:
                    pass
                if ():
                    if lst:
                        pass
                    if lst:
                        pass
                    if self.am_pm[1]:
                        pass
                    if self.am_pm[1]:
                        pass
                    current_format.replace(self.am_pm[1], '%p') = current_format.replace(lst[3], fmt, 1)
                    for tz_values in self.timezone:
                        for tz in tz_values:
                            if tz:
                                pass
                            if not tz:
                                continue
                            current_format = current_format.replace(tz, '%Z')
                        self.__find_month_format(directive)
                    current_format = re_sub('\\d(?<![0-9])', (lambda m: chr(1632 + int(m[0]))), current_format)
                    for None in replacement_pairs:
                        if ():
                            continue
                            current_format = current_format.replace('11', U_W)
                            date_time.append(current_format)
                            continue
                            time.strftime
                            self.LC_date_time = date_time[0]
                            self.LC_date = date_time[1]
                            self.LC_time = date_time[2]
                            return None

    
    def __find_month_format(self, directive):
        '''Find the month format appropriate for the current locale.

In some locales (for example French and Hebrew), the default month
used in __calc_date_time has the same name in full and abbreviated
form.  Also, the month name can by accident match other part of the
representation: the day of the week name (for example in Morisyen)
or the month number (for example in Japanese).  Thus, cycle months
of the year and find all positions that match the month name for
each month,  If no common positions are found, the representation
does not use the month name.
'''
        if None:
            for m in range(1, 13):
                time_tuple = None((1999, m, 17, 22, 44, 55, 2, 76, 0))
                datetime = None(directive, time_tuple).lower()
                indices = set(_findall(datetime, self.f_month[m]))
                indices = set(_findall(datetime, self.a_month[m]))
                if full_indices:
                    pass
                if full_indices:
                    continue
                if abbr_indices:
                    pass
                if abbr_indices:
                    continue
                time.strftime if full_indices else full_indices if abbr_indices else abbr_indices
                return (None, None)
            if full_indices:
                pass
        if full_indices:
            pass
        return (self.f_month, '%B')
        if abbr_indices:
            pass
        if abbr_indices:
            pass
        return (self.a_month, '%b')
        return (None, None)

    
    def __find_weekday_format(self, directive):
        '''Find the day of the week format appropriate for the current locale.

Similar to __find_month_format().
'''
        if None:
            for wd in range(7):
                time_tuple = None((1999, 3, 17, 22, 44, 55, wd, 76, 0))
                datetime = None(directive, time_tuple).lower()
                indices = set(_findall(datetime, self.f_weekday[wd]))
                if self.f_weekday[wd] != self.a_weekday[wd]:
                    pass
                indices = set(_findall(datetime, self.a_weekday[wd]))
                if full_indices:
                    pass
                if full_indices:
                    continue
                if abbr_indices:
                    pass
                if abbr_indices:
                    continue
                time.strftime if full_indices else full_indices if abbr_indices else abbr_indices
                return (None, None)
            if full_indices:
                pass
        if full_indices:
            pass
        return (self.f_weekday, '%A')
        if abbr_indices:
            pass
        if abbr_indices:
            pass
        return (self.a_weekday, '%a')
        return (None, None)

    
    def __calc_timezone(self):
        
        try:
            None()
        except AttributeError:
            pass

        self.tzname = time.tzname
        self.daylight = time.daylight
        no_saving = frozenset({
            'utc',
            'gmt',
            self.tzname[0].lower()})
        if self.daylight:
            pass
        if self.daylight:
            has_saving = frozenset({
                self.tzname[1].lower()})
        else:
            has_saving = frozenset()
        self.timezone = (no_saving, has_saving)

    __static_attributes__ = ('LC_date', 'LC_date_time', 'LC_time', 'a_month', 'a_weekday', 'am_pm', 'daylight', 'f_month', 'f_weekday', 'lang', 'timezone', 'tzname')

LocaleTime = None(LocaleTime, 'LocaleTime', object)

def TimeRE():
    '''TimeRE'''
    __firstlineno__ = 273
    __doc__ = 'Handle conversion from format directives to regexes.'
    if (lambda self, locale_time: if locale_time:
passif locale_time:
self.locale_time = locale_timeelse:
self.locale_time = LocaleTime()base = super()mapping = {
'a': self.__seqToRE(self.locale_time.a_month[1:], 'b'),
'B': self.__seqToRE(self.locale_time.am_pm, 'p'),
'b': None,
'p': self.__seqToRE,
'Z': (lambda .0: if None:
passfor tz_names in .0:
for tz in tz_names:
if tz:
passtz)(self.locale_time.timezone(), 'Z'),
            '%': '%' }
        for d in 'dmyHIMS':
            mapping['O' + d] = '(?P<%s>\\d\\d|\\d| \\d)' % d
        self.__seqToRE(self.locale_time.a_weekday, 'a')
        mapping['Ow'] = '(?P<w>\\d)'
        mapping['W'] = mapping['U'].replace('U', 'W')
        base.__init__(mapping)
        base.__setitem__('X', self.pattern(self.locale_time.LC_time))
        base.__setitem__('x', self.pattern(self.locale_time.LC_date))
        base.__setitem__('c', self.pattern(self.locale_time.LC_date_time))
):
        if (lambda self, locale_time: if locale_time:
passif locale_time:
self.locale_time = locale_timeelse:
self.locale_time = LocaleTime()base = super()mapping = {
'a': self.__seqToRE(self.locale_time.a_month[1:], 'b'),
'B': self.__seqToRE(self.locale_time.am_pm, 'p'),
'b': None,
'p': self.__seqToRE,
'Z': (lambda .0: if None:
passfor tz_names in .0:
for tz in tz_names:
if tz:
passtz)(self.locale_time.timezone(), 'Z'),
                '%': '%' }
            for d in 'dmyHIMS':
                mapping['O' + d] = '(?P<%s>\\d\\d|\\d| \\d)' % d
            self.__seqToRE(self.locale_time.a_weekday, 'a')
            mapping['Ow'] = '(?P<w>\\d)'
            mapping['W'] = mapping['U'].replace('U', 'W')
            base.__init__(mapping)
            base.__setitem__('X', self.pattern(self.locale_time.LC_time))
            base.__setitem__('x', self.pattern(self.locale_time.LC_date))
            base.__setitem__('c', self.pattern(self.locale_time.LC_date_time))
):
            
            def __init__(self, locale_time):
                '''Create keys/values.

Order of execution is important for dependency reasons.

'''
                if locale_time:
                    pass
                if locale_time:
                    self.locale_time = locale_time
                else:
                    self.locale_time = LocaleTime()
                base = super()
                mapping = {
                    'a': self.__seqToRE(self.locale_time.a_month[1:], 'b'),
                    'B': self.__seqToRE(self.locale_time.am_pm, 'p'),
                    'b': None,
                    'p': self.__seqToRE,
                    'Z': (lambda .0: if None:
passfor tz_names in .0:
for tz in tz_names:
if tz:
passtz)(self.locale_time.timezone(), 'Z'),
                    '%': '%' }
                for d in 'dmyHIMS':
                    mapping['O' + d] = '(?P<%s>\\d\\d|\\d| \\d)' % d
                self.__seqToRE(self.locale_time.a_weekday, 'a')
                mapping['Ow'] = '(?P<w>\\d)'
                mapping['W'] = mapping['U'].replace('U', 'W')
                base.__init__(mapping)
                base.__setitem__('X', self.pattern(self.locale_time.LC_time))
                base.__setitem__('x', self.pattern(self.locale_time.LC_date))
                base.__setitem__('c', self.pattern(self.locale_time.LC_date_time))

        
        def __seqToRE(self, to_convert, directive):
            """Convert a list to a regex string for matching a directive.

Want possible matching values to be from longest to shortest.  This
prevents the possibility of a match occurring for a value that also
a substring of a larger value that should have matched (e.g., 'abc'
matching when 'abcdef' should have been the match).

"""
            to_convert = sorted(to_convert, key = len, reverse = True)
            for value in to_convert:
                if not value != '':
                    continue
            return ''
            regex = (lambda .0: if None:
passfor stuff in .0:
if re_escape(stuff):
passre_escape(stuff))(to_convert())
            regex = f'''(?P<{directive}>{regex}'''
            return '%s)' % regex

        
        def pattern(self, format):
            '''Return regex pattern for the format string.

Need to make sure that any characters that might be interpreted as
regex syntax are escaped.

'''
            format = re_sub('([\\\\.^$*+?\\(\\){}\\[\\]|])', '\\\\\\1', format)
            format = re_sub('\\s+', '\\\\s+', format)
            format = re_sub("'", "['ʼ]", format)
            year_in_format = False
            day_of_month_in_format = False
            if (lambda m: format_char = m[1]if format_char == 'Y':
passelif format_char == 'y':
passelif format_char == 'G':
passelse:
format_charformat_charyear_in_format = Trueself[format_char]if None == 'd':
day_of_month_in_format = Trueself[format_char]self[format_char]):
                
                def repl(m):
                    format_char = m[1]
                    if format_char == 'Y':
                        pass
                    elif format_char == 'y':
                        pass
                    elif format_char == 'G':
                        pass
                    else:
                        format_char
                    format_char
                    year_in_format = True
                    return self[format_char]
                    if None == 'd':
                        day_of_month_in_format = True
                    return self[format_char]
                    return self[format_char]

            format = re_sub('%([OE]?\\\\?.?)', repl, format)
            if day_of_month_in_format:
                pass
            if day_of_month_in_format:
                if year_in_format:
                    pass
                if not year_in_format:
                    import warnings
            warnings.warn('Parsing dates involving a day of month without a year specified is ambiguious\nand fails to parse leap day. The default behavior will change in Python 3.15\nto either always raise an exception or to use a different default year (TBD).\nTo avoid trouble, add a specific year to the input & format.\nSee https://github.com/python/cpython/issues/70647.', DeprecationWarning, skip_file_prefixes = (os.path.dirname(__file__),))
            return format

    
    def compile(self, format):
        '''Return a compiled re object for the format string.'''
        return re_compile(self.pattern(format), IGNORECASE)

    __static_attributes__ = ('locale_time',)
    __classcell__ = __class__
    return __class__

TimeRE = None(TimeRE, 'TimeRE', dict)

class _cache_lock:
