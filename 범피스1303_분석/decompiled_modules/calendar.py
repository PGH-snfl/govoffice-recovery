# Source Generated with Decompyle++
# File: calendar.marshal (Python 3.13)

'''Calendar printing functions

Note when comparing these calendars to the ones printed by cal(1): By
default, these calendars have Monday as the first day of the week, and
Sunday as the last (the European convention). Use setfirstweekday() to
set the first day of the week (0=Monday, 6=Sunday).'''
import sys
import datetime
from enum import IntEnum, global_enum
import locale as _locale
from itertools import repeat
__all__ = [
    'IllegalMonthError',
    'IllegalWeekdayError',
    'setfirstweekday',
    'firstweekday',
    'isleap',
    'leapdays',
    'weekday',
    'monthrange',
    'monthcalendar',
    'prmonth',
    'month',
    'prcal',
    'calendar',
    'timegm',
    'month_name',
    'month_abbr',
    'day_name',
    'day_abbr',
    'Calendar',
    'TextCalendar',
    'HTMLCalendar',
    'LocaleTextCalendar',
    'LocaleHTMLCalendar',
    'weekheader',
    'Day',
    'Month',
    'JANUARY',
    'FEBRUARY',
    'MARCH',
    'APRIL',
    'MAY',
    'JUNE',
    'JULY',
    'AUGUST',
    'SEPTEMBER',
    'OCTOBER',
    'NOVEMBER',
    'DECEMBER',
    'MONDAY',
    'TUESDAY',
    'WEDNESDAY',
    'THURSDAY',
    'FRIDAY',
    'SATURDAY',
    'SUNDAY']
error = ValueError

def IllegalMonthError():
    '''IllegalMonthError'''
    __firstlineno__ = 32
    
    def __init__(self, month):
        self.month = month

    
    def __str__(self):
        return 'bad month number %r; must be 1-12' % self.month

    __static_attributes__ = ('month',)

IllegalMonthError = None(IllegalMonthError, 'IllegalMonthError', ValueError, IndexError)

def IllegalWeekdayError():
    '''IllegalWeekdayError'''
    __firstlineno__ = 39
    
    def __init__(self, weekday):
        self.weekday = weekday

    
    def __str__(self):
        return 'bad weekday number %r; must be 0 (Monday) to 6 (Sunday)' % self.weekday

    __static_attributes__ = ('weekday',)

IllegalWeekdayError = None(IllegalWeekdayError, 'IllegalWeekdayError', ValueError)

def __getattr__(name):
    if name in ('January', 'February'):
        import warnings
        warnings.warn(f'''The \'{name}\' attribute is deprecated, use \'{name.upper()}\' instead''', DeprecationWarning, stacklevel = 2)
        if name == 'January':
            pass
        return 1
    return 2
    raise AttributeError(f'''module \'{__name__}\' has no attribute \'{name}\'''')


def Month():
    '''Month'''
    __firstlineno__ = 60
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12
    __static_attributes__ = ()

Month = None(Month, 'Month', IntEnum)()

def Day():
    '''Day'''
    __firstlineno__ = 77
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    __static_attributes__ = ()

Day = None(Day, 'Day', IntEnum)()
mdays = [
    0,
    31,
    28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31]

def _localized_month():
    '''_localized_month'''
    __firstlineno__ = 96
    for None in :
        pass
    datetime.date
    datetime, i, .0, _months = None, None, None, range, None(12), , [], None
    _months.insert(0, (lambda x: ''))
    
    def __init__(self, format):
        self.format = format

    
    def __getitem__(self, i):
        funcs = self._months[i]
        if isinstance(i, slice):
            pass
        if isinstance(i, slice):
            for None in :
                if None:
                    continue
                    return f,
                return None(self.format)

    
    def __len__(self):
        return 13

    __static_attributes__ = ('format',)
    return None
    

_localized_month = None(_localized_month, '_localized_month')

def _localized_day():
    '''_localized_day'''
    __firstlineno__ = 115
    for None in :
        pass
    datetime.date
    datetime, i, .0, _days = None, None, None, range, None(7), , [], None
    
    def __init__(self, format):
        self.format = format

    
    def __getitem__(self, i):
        funcs = self._days[i]
        if isinstance(i, slice):
            pass
        if isinstance(i, slice):
            for None in :
                if None:
                    continue
                    return f,
                return None(self.format)

    
    def __len__(self):
        return 7

    __static_attributes__ = ('format',)
    return None
    

_localized_day = None(_localized_day, '_localized_day')
day_name = None('%A')
day_abbr = None('%a')
month_name = None('%B')
month_abbr = None('%b')

def isleap(year):
    '''Return True for leap years, False for non-leap years.'''
    if year % 4 == 0:
        pass
    if year % 4 == 0:
        year % 4 == 0
        if year % 100 != 0:
            pass
        if not year % 100 != 0:
            year % 100 != 0
    return year % 400 == 0


def leapdays(y1, y2):
    '''Return number of leap years in range [y1, y2).
Assume y1 <= y2.'''
    y1 -= 1
    y2 -= 1
    return (y2 // 4 - y1 // 4 - y2 // 100 - y1 // 100) + (y2 // 400 - y1 // 400)


def weekday(year, month, day):
    '''Return weekday (0-6 ~ Mon-Sun) for year, month (1-12), day (1-31).'''
    if not  <= datetime.MINYEAR, year or datetime.MINYEAR, year <= datetime.MAXYEAR:
        pass
    
    return datetime.date(None(year, month, day).weekday())


def _validate_month(month):
    if not  <= 1, month or 1, month <= 12:
        pass
    
    raise IllegalMonthError(month)


def monthrange(year, month):
    '''Return weekday of first day of month (0-6 ~ Mon-Sun)
and number of days (28-31) for year, month.'''
    _validate_month(month)
    day1 = weekday(year, month, 1)
    if month == FEBRUARY:
        pass
    if month == FEBRUARY:
        month == FEBRUARY
    ndays = mdays[month] + isleap(year)
    return (day1, ndays)


def _monthlen(year, month):
    if month == FEBRUARY:
        pass
    if month == FEBRUARY:
        month == FEBRUARY
    return mdays[month] + isleap(year)


def _prevmonth(year, month):
    if month == 1:
        pass
    return (year - 1, 12)
    return (year, month - 1)


def _nextmonth(year, month):
    if month == 12:
        pass
    return (year + 1, 1)
    return (year, month + 1)


def Calendar():
    '''Calendar'''
    __firstlineno__ = 194
    __doc__ = "\nBase calendar class. This class doesn't do any formatting. It simply\nprovides data to subclasses.\n"
    if (lambda self, firstweekday: self.firstweekday = firstweekday):
        
        def __init__(self, firstweekday):
            self.firstweekday = firstweekday

    
    def getfirstweekday(self):
        return self._firstweekday % 7

    
    def setfirstweekday(self, firstweekday):
        self._firstweekday = firstweekday

    firstweekday = None(getfirstweekday, setfirstweekday)
    
    def iterweekdays(self):
        '''
Return an iterator for one week of weekday numbers starting with the
configured first one.
'''
        if None:
            pass
        for i in range(self.firstweekday, self.firstweekday + 7):
            if i % 7:
                pass
            i % 7

    
    def itermonthdates(self, year, month):
        '''
Return an iterator for one month. The iterator will yield datetime.date
values and will always iterate through complete weeks, so it will yield
dates outside the specified month.
'''
        if None:
            pass
        for None in self.itermonthdays3(year, month):
            if (d,):
                if None(y, m, d):
                    pass
                continue
                (d,)
                return None

    
    def itermonthdays(self, year, month):
        '''
Like itermonthdates(), but will yield day numbers. For days outside
the specified month the day number is 0.
'''
        if None:
            pass
        if ():
            if None and None:
                pass
            continue
        if None and None:
            pass
        continue
        (self.firstweekday - day1 - ndays) % 7 = range(1, ndays + 1)
        if None and None:
            pass
        continue
        return None
        continue
        continue
        continue

    
    def itermonthdays2(self, year, month):
        '''
Like itermonthdates(), but will yield (day number, weekday number)
tuples. For days outside the specified month the day number is 0.
'''
        if None:
            pass
        for None in enumerate(self.itermonthdays(year, month), self.firstweekday):
            if ():
                if (d, i % 7):
                    pass
                continue
                return None

    
    def itermonthdays3(self, year, month):
        '''
Like itermonthdates(), but will yield (year, month, day) tuples.  Can be
used for dates outside of datetime.date range.
'''
        if None:
            pass
        if ():
            (self.firstweekday - day1 - ndays) % 7 = (day1 - self.firstweekday) % 7
            if ():
                for None in range(end - days_before, end):
                    if (y, m, d):
                        pass
                    (y, m, d)
                for d in range(1, ndays + 1):
                    if (year, month, d):
                        pass
                    (year, month, d)
                monthrange(year, month)
                if ():
                    for None in range(1, days_after + 1):
                        if (y, m, d):
                            pass
                    return None

    
    def itermonthdays4(self, year, month):
        '''
Like itermonthdates(), but will yield (year, month, day, day_of_week) tuples.
Can be used for dates outside of datetime.date range.
'''
        if None:
            pass
        for None in enumerate(self.itermonthdays3(year, month)):
            if (d,):
                if (y, m, d, (self.firstweekday + i) % 7):
                    pass
                continue
                (i,)
                return None

    
    def monthdatescalendar(self, year, month):
        """
Return a matrix (list of lists) representing a month's calendar.
Each row represents a week; week entries are datetime.date values.
"""
        dates = list(self.itermonthdates(year, month))
        for None in :
            if None:
                continue
                return i,

    
    def monthdays2calendar(self, year, month):
        """
Return a matrix representing a month's calendar.
Each row represents a week; week entries are
(day number, weekday number) tuples. Day numbers outside this month
are zero.
"""
        days = list(self.itermonthdays2(year, month))
        for None in :
            if None:
                continue
                return i,

    
    def monthdayscalendar(self, year, month):
        """
Return a matrix representing a month's calendar.
Each row represents a week; days outside this month are zero.
"""
        days = list(self.itermonthdays(year, month))
        for None in :
            if None:
                continue
                return i,

    if (lambda self, year, width: for None in :
if None:
continueNone, Month, months, m = Nonefor None in :
if None:
continuei,):
        
        def yeardatescalendar(self, year, width):
            '''
Return the data for the specified year ready for formatting. The return
value is a list of month rows. Each month row contains up to width months.
Each month contains between 4 and 6 weeks and each week contains 1-7
days. Days are datetime.date objects.
'''
            for None in :
                if None:
                    continue
                    None, Month, months, m = None
            for None in :
                if None:
                    continue
                    return i,
                

    if (lambda self, year, width: for None in :
if None:
continueNone, Month, months, m = Nonefor None in :
if None:
continuei,):
        
        def yeardays2calendar(self, year, width):
            '''
Return the data for the specified year ready for formatting (similar to
yeardatescalendar()). Entries in the week lists are
(day number, weekday number) tuples. Day numbers outside this month are
zero.
'''
            for None in :
                if None:
                    continue
                    None, Month, months, m = None
            for None in :
                if None:
                    continue
                    return i,
                

    if (lambda self, year, width: for None in :
if None:
continueNone, Month, months, m = Nonefor None in :
if None:
continuei,):
        
        def yeardayscalendar(self, year, width):
            '''
Return the data for the specified year ready for formatting (similar to
yeardatescalendar()). Entries in the week lists are day numbers.
Day numbers outside this month are zero.
'''
            for None in :
                if None:
                    continue
                    None, Month, months, m = None
            for None in :
                if None:
                    continue
                    return i,
                

    __static_attributes__ = ('_firstweekday', 'firstweekday')

Calendar = None(Calendar, 'Calendar', object)

def TextCalendar():
    '''TextCalendar'''
    __firstlineno__ = 330
    __doc__ = '\nSubclass of Calendar that outputs a calendar as a simple plain text\nsimilar to the UNIX program cal.\n'
    
    def prweek(self, theweek, width):
        '''
Print a single week (no newline).
'''
        print(self.formatweek(theweek, width), end = '')

    
    def formatday(self, day, weekday, width):
        '''
Returns a formatted day.
'''
        if day == 0:
            s = ''
        else:
            s = '%2i' % day
        return s.center(width)

    
    def formatweek(self, theweek, width):
        '''
Returns a single week in a string (no newline).
'''
        if (lambda .0: if None:
passfor None in .0:
if () and self.formatday(d, wd, width):
pass):
            pass
        return (lambda .0: if None:
passfor None in .0:
if () and self.formatday(d, wd, width):
pass)(theweek())

    
    def formatweekday(self, day, width):
        '''
Returns a formatted week day name.
'''
        if width >= 9:
            names = day_name
        else:
            names = day_abbr
        return names[day][:width].center(width)

    
    def formatweekheader(self, width):
        '''
Return a header for a week.
'''
        if (lambda .0: if None:
passfor i in .0:
if self.formatweekday(i, width):
passself.formatweekday(i, width)):
            pass
        return (lambda .0: if None:
passfor i in .0:
if self.formatweekday(i, width):
passself.formatweekday(i, width))(self.iterweekdays()())

    if (lambda self, theyear, themonth, width, withyear: _validate_month(themonth)s = month_name[themonth]if withyear:
passif withyear:
passs = f'''{s} {theyear}'''s.center(width)):
        
        def formatmonthname(self, theyear, themonth, width, withyear):
            '''
Return a formatted month name.
'''
            _validate_month(themonth)
            s = month_name[themonth]
            if withyear:
                pass
            if withyear:
                pass
            s = f'''{s} {theyear}'''
            return s.center(width)

    if (lambda self, theyear, themonth, w, l: print(self.formatmonth(theyear, themonth, w, l), end = '')):
        
        def prmonth(self, theyear, themonth, w, l):
            """
Print a month's calendar.
"""
            print(self.formatmonth(theyear, themonth, w, l), end = '')

    if (lambda self, theyear, themonth, w, l: w = max(2, w)l = max(1, l)s = self.formatmonthname(theyear, themonth, 7 * (w + 1) - 1)s = s.rstrip()s += '\n' * ls += self.formatweekheader(w).rstrip()s += '\n' * lfor week in self.monthdays2calendar(theyear, themonth):
s += self.formatweek(week, w).rstrip()s += '\n' * ls):
        
        def formatmonth(self, theyear, themonth, w, l):
            """
Return a month's calendar string (multi-line).
"""
            w = max(2, w)
            l = max(1, l)
            s = self.formatmonthname(theyear, themonth, 7 * (w + 1) - 1)
            s = s.rstrip()
            s += '\n' * l
            s += self.formatweekheader(w).rstrip()
            s += '\n' * l
            for week in self.monthdays2calendar(theyear, themonth):
                s += self.formatweek(week, w).rstrip()
                s += '\n' * l
            return s

    if (lambda self, theyear, w, l, c, m: w = max(2, w)l = max(1, l)c = max(2, c)colwidth = (w + 1) * 7 - 1v = []a = v.appendNone(repr(theyear).center(colwidth * m + c * (m - 1)).rstrip())None('\n' * l)header = self.formatweekheader(w)for None in enumerate(self.yeardays2calendar(theyear, m)):
if ():
if (lambda .0: if None:
passfor k in .0:
if self.formatmonthname(theyear, k, colwidth, False):
passself.formatmonthname(theyear, k, colwidth, False)):
                    
                    def months()(.0):
                        if None:
                            pass
                        for k in .0:
                            if self.formatmonthname(theyear, k, colwidth, False):
                                pass
                            self.formatmonthname(theyear, k, colwidth, False)

                None(formatstring(names, colwidth, c).rstrip())
                None('\n' * l)
                if (lambda .0: if None:
passfor k in .0:
if header:
passheader):
                    headers = months()
            None('\n' * l)
            height = (lambda .0: if None:
passfor cal in .0:
if len(cal):
passlen(cal))(row())
            for j in range(height):
                weeks = []
                for cal in row:
                    if j >= len(cal):
                        weeks.append('')
                        continue
                    weeks.append(self.formatweek(cal[j], w))
                None(formatstring(weeks, colwidth, c).rstrip())
                None('\n' * l)
            a
        a
        return ''.join(v)
):
        
        def formatyear(self, theyear, w, l, c, m):
            """
Returns a year's calendar as a multi-line string.
"""
            w = max(2, w)
            l = max(1, l)
            c = max(2, c)
            colwidth = (w + 1) * 7 - 1
            v = []
            a = v.append
            None(repr(theyear).center(colwidth * m + c * (m - 1)).rstrip())
            None('\n' * l)
            header = self.formatweekheader(w)
            for None in enumerate(self.yeardays2calendar(theyear, m)):
                if ():
                    if (lambda .0: if None:
passfor k in .0:
if self.formatmonthname(theyear, k, colwidth, False):
passself.formatmonthname(theyear, k, colwidth, False)):
                        
                        def months()(.0):
                            if None:
                                pass
                            for k in .0:
                                if self.formatmonthname(theyear, k, colwidth, False):
                                    pass
                                self.formatmonthname(theyear, k, colwidth, False)

                    None(formatstring(names, colwidth, c).rstrip())
                    None('\n' * l)
                    if (lambda .0: if None:
passfor k in .0:
if header:
passheader):
                        headers = months()
                None('\n' * l)
                height = (lambda .0: if None:
passfor cal in .0:
if len(cal):
passlen(cal))(row())
                for j in range(height):
                    weeks = []
                    for cal in row:
                        if j >= len(cal):
                            weeks.append('')
                            continue
                        weeks.append(self.formatweek(cal[j], w))
                    None(formatstring(weeks, colwidth, c).rstrip())
                    None('\n' * l)
                a
            a
            return ''.join(v)

    if (lambda self, theyear, w, l, c, m: print(self.formatyear(theyear, w, l, c, m), end = '')):
        
        def pryear(self, theyear, w, l, c, m):
            """Print a year's calendar."""
            print(self.formatyear(theyear, w, l, c, m), end = '')

    __static_attributes__ = ()

TextCalendar = None(TextCalendar, 'TextCalendar', Calendar)

def HTMLCalendar():
    '''HTMLCalendar'''
    __firstlineno__ = 449
    __doc__ = '\nThis calendar returns complete HTML pages.\n'
    cssclasses = [
        'mon',
        'tue',
        'wed',
        'thu',
        'fri',
        'sat',
        'sun']
    cssclasses_weekday_head = cssclasses
    cssclass_noday = 'noday'
    cssclass_month_head = 'month'
    cssclass_month = 'month'
    cssclass_year_head = 'year'
    cssclass_year = 'year'
    
    def formatday(self, day, weekday):
        '''
Return a day as a table cell.
'''
        if day == 0:
            pass
        return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        return '<td class="%s">%d</td>' % (self.cssclasses[weekday], day)

    
    def formatweek(self, theweek):
        '''
Return a complete week as a table row.
'''
        if (lambda .0: if None:
passfor None in .0:
if ():
if self.formatday(d, wd):
pass):
            pass
        s = (lambda .0: if None:
passfor None in .0:
if ():
if self.formatday(d, wd):
pass)(theweek())
        return '<tr>%s</tr>' % s

    
    def formatweekday(self, day):
        '''
Return a weekday name as a table header.
'''
        return f'''<th class="{self.cssclasses_weekday_head[day]}">{day_abbr[day]}</th>'''

    
    def formatweekheader(self):
        '''
Return a header for a week as a table row.
'''
        if (lambda .0: if None:
passfor i in .0:
if self.formatweekday(i):
passself.formatweekday(i)):
            pass
        s = (lambda .0: if None:
passfor i in .0:
if self.formatweekday(i):
passself.formatweekday(i))(self.iterweekdays()())
        return '<tr>%s</tr>' % s

    if (lambda self, theyear, themonth, withyear: _validate_month(themonth)if withyear:
passif withyear:
s = f'''{month_name[themonth]} {theyear}'''else:
s = '%s' % month_name[themonth]f'''<tr><th colspan="7" class="{self.cssclass_month_head}">{s}</th></tr>'''):
        
        def formatmonthname(self, theyear, themonth, withyear):
            '''
Return a month name as a table row.
'''
            _validate_month(themonth)
            if withyear:
                pass
            if withyear:
                s = f'''{month_name[themonth]} {theyear}'''
            else:
                s = '%s' % month_name[themonth]
            return f'''<tr><th colspan="7" class="{self.cssclass_month_head}">{s}</th></tr>'''

    if (lambda self, theyear, themonth, withyear: v = []a = v.appendNone('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % self.cssclass_month)None('\n')None(self.formatmonthname(theyear, themonth, withyear = withyear))None('\n')None(self.formatweekheader())None('\n')for week in self.monthdays2calendar(theyear, themonth):
None(self.formatweek(week))None('\n')aNone('</table>')None('\n')''.join(v)):
        
        def formatmonth(self, theyear, themonth, withyear):
            '''
Return a formatted month as a table.
'''
            v = []
            a = v.append
            None('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % self.cssclass_month)
            None('\n')
            None(self.formatmonthname(theyear, themonth, withyear = withyear))
            None('\n')
            None(self.formatweekheader())
            None('\n')
            for week in self.monthdays2calendar(theyear, themonth):
                None(self.formatweek(week))
                None('\n')
            a
            None('</table>')
            None('\n')
            return ''.join(v)

    if (lambda self, theyear, width: v = []a = v.appendwidth = max(width, 1)None('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % self.cssclass_year)None('\n')None('<tr><th colspan="%d" class="%s">%s</th></tr>' % (width, self.cssclass_year_head, theyear))for i in range(JANUARY, JANUARY + 12, width):
months = range(i, min(i + width, 13))None('<tr>')for m in months:
None('<td>')None(self.formatmonth(theyear, m, withyear = False))None('</td>')aNone('</tr>')aNone('</table>')''.join(v)):
        
        def formatyear(self, theyear, width):
            '''
Return a formatted year as a table of tables.
'''
            v = []
            a = v.append
            width = max(width, 1)
            None('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % self.cssclass_year)
            None('\n')
            None('<tr><th colspan="%d" class="%s">%s</th></tr>' % (width, self.cssclass_year_head, theyear))
            for i in range(JANUARY, JANUARY + 12, width):
                months = range(i, min(i + width, 13))
                None('<tr>')
                for m in months:
                    None('<td>')
                    None(self.formatmonth(theyear, m, withyear = False))
                    None('</td>')
                a
                None('</tr>')
            a
            None('</table>')
            return ''.join(v)

    if (lambda self, theyear, width, css, encoding: if encoding:
passencoding = None()v = []a = v.appendNone('<?xml version="1.0" encoding="%s"?>\n' % encoding)None('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')None('<html>\n')None('<head>\n')None('<meta http-equiv="Content-Type" content="text/html; charset=%s" />\n' % encoding)if css:
passNone('<link rel="stylesheet" type="text/css" href="%s" />\n' % css)None('<title>Calendar for %d</title>\n' % theyear)None('</head>\n')None('<body>\n')None(self.formatyear(theyear, width))None('</body>\n')None('</html>\n')''.join(v).encode(encoding, 'xmlcharrefreplace')):
        
        def formatyearpage(self, theyear, width, css, encoding):
            '''
Return a formatted year as a complete HTML page.
'''
            if encoding:
                pass
            encoding = None()
            v = []
            a = v.append
            None('<?xml version="1.0" encoding="%s"?>\n' % encoding)
            None('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
            None('<html>\n')
            None('<head>\n')
            None('<meta http-equiv="Content-Type" content="text/html; charset=%s" />\n' % encoding)
            if css:
                pass
            None('<link rel="stylesheet" type="text/css" href="%s" />\n' % css)
            None('<title>Calendar for %d</title>\n' % theyear)
            None('</head>\n')
            None('<body>\n')
            None(self.formatyear(theyear, width))
            None('</body>\n')
            None('</html>\n')
            return ''.join(v).encode(encoding, 'xmlcharrefreplace')

    __static_attributes__ = ()

HTMLCalendar = None(HTMLCalendar, 'HTMLCalendar', Calendar)

def different_locale():
    '''different_locale'''
    __firstlineno__ = 586
    
    def __init__(self, locale):
        self.locale = locale
        self.oldlocale = None

    
    def __enter__(self):
        self.oldlocale = None(_locale.LC_TIME, None)
        None(_locale.LC_TIME, self.locale)

    
    def __exit__(self, *args):
        None(_locale.LC_TIME, self.oldlocale)

    __static_attributes__ = ('locale', 'oldlocale')

different_locale = None(different_locale, 'different_locale')

def _get_default_locale():
    locale = None(_locale.LC_TIME, None)
    if locale == 'C':
        
        try:
            different_locale('')
            locale = None(_locale.LC_TIME, None)
        with None:
            if :
                pass

        None(None, None)
    return locale
    return locale
    
    try:
        different_locale('')
        locale = None(_locale.LC_TIME, None)
    with None:
        if :
            pass

    if not :
        pass
    except:
        pass
    _locale.setlocale
    return locale


def LocaleTextCalendar():
