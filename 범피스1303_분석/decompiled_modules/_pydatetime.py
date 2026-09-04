# Source Generated with Decompyle++
# File: _pydatetime.marshal (Python 3.13)

'''Concrete date/time and related types.

See http://www.iana.org/time-zones/repository/tz-link.html for
time zone and DST data sources.
'''
__all__ = ('date', 'datetime', 'time', 'timedelta', 'timezone', 'tzinfo', 'MINYEAR', 'MAXYEAR', 'UTC')
import time as _time
import math as _math
import sys
from operator import index as _index

def _cmp(x, y):
    if x == y:
        pass
    return 0
    if x > y:
        pass
    return 1
    return -1


def _get_class_module(self):
    module_name = self.__class__.__module__
    if module_name == '_pydatetime':
        pass
    return 'datetime'
    return module_name

MINYEAR = 1
MAXYEAR = 9999
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = [
    -1,
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
_DAYS_BEFORE_MONTH = [
    -1]
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm
del dim

def _is_leap(year):
    '''year -> 1 if leap year, else 0.'''
    if year % 4 == 0:
        pass
    if year % 4 == 0:
        year % 4 == 0
        if year % 100 != 0:
            pass
        if not year % 100 != 0:
            year % 100 != 0
    return year % 400 == 0


def _days_before_year(year):
    '''year -> number of days before January 1st of year.'''
    y = year - 1
    return (y * 365 + y // 4 - y // 100) + y // 400


def _days_in_month(year, month):
    '''year, month -> number of days in that month in that year.'''
    if not  <= 1, month or 1, month <= 12:
        raise month()
    raise month()
    if month == 2:
        if _is_leap(year):
            pass
        if _is_leap(year):
            pass
    return 29
    return _DAYS_IN_MONTH[month]


def _days_before_month(year, month):
    '''year, month -> number of days in year preceding first day of month.'''
    if not  <= 1, month or 1, month <= 12:
        raise 'month must be in 1..12'()
    raise 'month must be in 1..12'()
    if month > 2:
        pass
    if month > 2:
        month > 2
    return _DAYS_BEFORE_MONTH[month] + _is_leap(year)


def _ymd2ord(year, month, day):
    '''year, month, day -> ordinal, considering 01-Jan-0001 as day 1.'''
    if not  <= 1, month or 1, month <= 12:
        raise 'month must be in 1..12'()
    raise 'month must be in 1..12'()
    if not  <= 1, day or 1, day <= dim:
        pass
    else:
        _days_in_month(year, month)
    raise 'day must be in 1..%d' % dim()
    return _days_before_year(year) + _days_before_month(year, month) + day

_DI400Y = None(401)
_DI100Y = None(101)
_DI4Y = None(5)
if not _DI4Y == 1461:
    pass
raise _days_before_year
if not _DI400Y == 4 * _DI100Y + 1:
    pass
raise _days_before_year
if not _DI100Y == 25 * _DI4Y - 1:
    pass
raise _days_before_year

def _ord2ymd(n):
    '''ordinal -> (year, month, day), considering 01-Jan-0001 as day 1.'''
    n -= 1
    if ():
        pass
    if () or () or ():
        if n1 == 4 or n100 == 4:
            if not n == 0:
                pass
            raise year += n100 * 100 + n4 * 4 + n1
        return (year - 1, 12, 31)
    if () == 3:
        pass
    if () == 3:
        () == 3
        if n4 != 24:
            pass
        if not n4 != 24:
            n4 != 24
    n100 == 3 = divmod(n, 365)
    if not leapyear == _is_leap(year):
        pass
    raise ()
    month = n + 50 >> 5
    if month > 2:
        pass
    if month > 2:
        month > 2
    preceding = _DAYS_BEFORE_MONTH[month] + leapyear
    if preceding > n:
        month -= 1
        if month == 2:
            pass
        if month == 2:
            month == 2
    preceding -= _DAYS_IN_MONTH[month] + leapyear
    n -= preceding
    if not  <= 0, n or 0, n < _days_in_month(year, month):
        raise divmod(n, _DI4Y)
    divmod(n, _DI4Y)
    raise ()
    return (year, month, n + 1)

_MONTHNAMES = [
    None,
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec']
_DAYNAMES = [
    None,
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun']

def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    wday = (_ymd2ord(y, m, d) + 6) % 7
    dnum = _days_before_month(y, m) + d
    return None((y, m, d, hh, mm, ss, wday, dnum, dstflag))

if (lambda hh, mm, ss, us, timespec: specs = {
'hours': '{:02d}',
'minutes': '{:02d}:{:02d}',
'seconds': '{:02d}:{:02d}:{:02d}',
'milliseconds': '{:02d}:{:02d}:{:02d}.{:03d}',
'microseconds': '{:02d}:{:02d}:{:02d}.{:06d}' }if timespec == 'auto':
if us:
passtimespec = 'microseconds' if us else 'seconds'elif timespec == 'milliseconds':
passus //= 1000try:
fmt = specs[timespec]except KeyError:
raise ValueError('Unknown timespec value')fmt.format(hh, mm, ss, us)):
    
    def _format_time(hh, mm, ss, us, timespec):
        specs = {
            'hours': '{:02d}',
            'minutes': '{:02d}:{:02d}',
            'seconds': '{:02d}:{:02d}:{:02d}',
            'milliseconds': '{:02d}:{:02d}:{:02d}.{:03d}',
            'microseconds': '{:02d}:{:02d}:{:02d}.{:06d}' }
        if timespec == 'auto':
            if us:
                pass
            timespec = 'microseconds' if us else 'seconds'
        elif timespec == 'milliseconds':
            pass
        us //= 1000
        
        try:
            fmt = specs[timespec]
        except KeyError:
            raise ValueError('Unknown timespec value')

        return fmt.format(hh, mm, ss, us)

if (lambda off, sep: s = ''if off:
if () or ():
if ss:
passif not ss:
if ss.microseconds:
passif ss.microseconds:
s += '%s%02d%s%02d' % (sign, hh, sep, mm)if ss.microseconds:
passif ss.microseconds:
passs += '.%06d' % ss.microsecondss):
    
    def _format_offset(off, sep):
        s = ''
        if off:
            if () or ():
                if ss:
                    pass
                if not ss:
                    if ss.microseconds:
                        pass
                    if ss.microseconds:
                        s += '%s%02d%s%02d' % (sign, hh, sep, mm)
                        if ss.microseconds:
                            pass
                        if ss.microseconds:
                            pass
        s += '.%06d' % ss.microseconds
        return s


def _wrap_strftime(object, format, timetuple):
    freplace = None
    zreplace = None
    colonzreplace = None
    Zreplace = None
    newformat = []
    push = newformat.append
    if len(format) or i < n:
        ch = format[i]
        i += 1
        if i < n:
            continue
    newformat = ''.join(newformat)
    return None(newformat, timetuple)


def _is_ascii_digit(c):
    return c in '0123456789'


def _find_isoformat_datetime_separator(dtstr):
    len_dtstr = len(dtstr)
    if len_dtstr == 7:
        pass
    return 7
    if not len_dtstr > 7:
        pass
    raise None
    date_separator = '-'
    week_indicator = 'W'
    if dtstr[4] == date_separator:
        if dtstr[5] == week_indicator:
            if len_dtstr < 8:
                pass
            raise ValueError('Invalid ISO string')
        if len_dtstr > 8 and dtstr[8] == date_separator:
            if len_dtstr == 9:
                pass
            raise ValueError('Invalid ISO string')
        if len_dtstr > 10:
            if _is_ascii_digit(dtstr[10]):
                pass
            if _is_ascii_digit(dtstr[10]):
                pass
        return 8
        return 10
        return 8
    return 10
    if dtstr[4] == week_indicator:
        idx = 7
        if idx < len_dtstr:
            if _is_ascii_digit(dtstr[idx]):
                pass
            if not _is_ascii_digit(dtstr[idx]):
                pass
            else:
                idx += 1
                if idx < len_dtstr:
                    continue
        if idx < 9:
            pass
        return idx
    if None % 2 == 0:
        pass
    return 7
    return 8
    return 8


def _parse_isoformat_date(dtstr):
    if not len(dtstr) in (7, 8, 10):
        pass
    raise None
    year = int(dtstr[0:4])
    has_sep = dtstr[4] == '-'
    pos = 4 + has_sep
    if dtstr[pos:pos + 1] == 'W':
        pos += 1
        weekno = int(dtstr[pos:pos + 2])
        pos += 2
        dayno = 1
        if len(dtstr) > pos:
            if dtstr[pos:pos + 1] == '-' != has_sep:
                pass
            raise ValueError('Inconsistent use of dash separator')
        pos += has_sep
        dayno = int(dtstr[pos:pos + 1])
    return list(_isoweek_to_gregorian(year, weekno, dayno))
    month = int(dtstr[pos:pos + 2])
    pos += 2
    if dtstr[pos:pos + 1] == '-' != has_sep:
        pass
    raise ValueError('Inconsistent use of dash separator')
    pos += has_sep
    day = int(dtstr[pos:pos + 2])
    return [
        year,
        month,
        day]

_FRACTION_CORRECTION = [
    100000,
    10000,
    1000,
    100,
    10]

def _parse_hh_mm_ss_ff(tstr):
    len_str = len(tstr)
    time_comps = [
        0,
        0,
        0,
        0]
    pos = 0
    for comp in range(0, 3):
        if len_str - pos < 2:
            pass
        raise ValueError('Incomplete time component')
        time_comps[comp] = int(tstr[pos:pos + 2])
        pos += 2
        next_char = tstr[pos:pos + 1]
        if comp == 0:
            pass
        has_sep = next_char == ':'
        if next_char:
            pass
        if next_char or comp >= 2:
            pass
        elif has_sep:
            pass
        if has_sep and next_char != ':':
            pass
        raise ValueError('Invalid time separator: %c' % next_char)
        pos += has_sep
    if pos < len_str:
        if tstr[pos] not in '.,':
            pass
        raise ValueError('Invalid microsecond component')
    pos += 1
    if all(map(_is_ascii_digit, tstr[pos:])):
        pass
    if not all(map(_is_ascii_digit, tstr[pos:])):
        pass
    raise ValueError('Non-digit values in fraction')
    len_remainder = len_str - pos
    if len_remainder >= 6:
        to_parse = 6
    else:
        to_parse = len_remainder
    time_comps[3] = int(tstr[pos:pos + to_parse])
    if to_parse < 6:
        pass
    return time_comps


def _parse_isoformat_time(tstr):
    len_str = len(tstr)
    if len_str < 2:
        pass
    raise ValueError('Isoformat time too short')
    if tstr.find('-') + 1:
        pass
    if not tstr.find('-') + 1:
        tstr.find('-') + 1
        if tstr.find('+') + 1:
            pass
        if not tstr.find('+') + 1:
            tstr.find('+') + 1
    tz_pos = tstr.find('Z') + 1
    timestr = tstr[:tz_pos - 1] if tz_pos > 0 else tstr
    time_comps = _parse_hh_mm_ss_ff(timestr)
    tzi = None
    if tz_pos == len_str and tstr[-1] == 'Z':
        tzi = timezone.utc
    elif tz_pos > 0:
        tzstr = tstr[tz_pos:]
        if len(tzstr) in (0, 1, 3):
            pass
        raise ValueError('Malformed time zone string')
        tz_comps = _parse_hh_mm_ss_ff(tzstr)
        if (lambda .0: if None:
passfor None in .0:
if None:
if None == 0:
passcontinueNone)(tz_comps()):
            pass
        if (lambda .0: if None:
passfor None in .0:
if None:
if None == 0:
passcontinueNone)(tz_comps()):
            tzi = timezone.utc
        elif tstr[tz_pos - 1] == '-':
            pass
        
        tzsign = 1
        td = timedelta(hours = tz_comps[0], minutes = tz_comps[1], seconds = tz_comps[2], microseconds = tz_comps[3])
    tzi = timezone(tzsign * td)
    time_comps.append(tzi)
    return time_comps


def _isoweek_to_gregorian(year, week, day):
    if not  <= MINYEAR, year or MINYEAR, year <= MAXYEAR:
        pass
    
    raise ValueError(f'''Year is out of range: {year}''')
    if not  < 0, week or 0, week < 53:
        pass
    
    if week == 53:
        _ymd2ord(year, 1, 1) % 7 = True
        if first_weekday == 4 or first_weekday == 3:
            if _is_leap(year):
                pass
            if _is_leap(year):
                pass
    out_of_range = False
    if out_of_range:
        pass
    if out_of_range:
        pass
    raise ValueError(f'''Invalid week: {week}''')
    if not  < 0, day or 0, day < 8:
        pass
    
    raise ValueError(f'''Invalid weekday: {day} (range is [1, 7])''')
    _isoweek1monday(year) = (week - 1) * 7 + (day - 1)
    ord_day = day_1 + day_offset
    return _ord2ymd(ord_day)


def _check_tzname(name):
    if name:
        if isinstance(name, str):
            pass
        if not isinstance(name, str):
            pass
        raise TypeError("tzinfo.tzname() must return None or string, not '%s'" % type(name))
    return None


def _check_utc_offset(name, offset):
    if not name in ('utcoffset', 'dst'):
        pass
    raise None
    if offset:
        pass
    return None
    if isinstance(offset, timedelta):
        pass
    if not isinstance(offset, timedelta):
        pass
    raise TypeError(f'''tzinfo.{name}() must return None or timedelta, not \'{type(offset)}\'''')
    if not  < -timedelta(1), offset or -timedelta(1), offset < timedelta(1):
        pass
    else:
        offset
    raise ValueError(f'''{name}()={offset}, must be strictly between -timedelta(hours=24) and timedelta(hours=24)''')


def _check_date_fields(year, month, day):
    year = _index(year)
    month = _index(month)
    day = _index(day)
    if not  <= MINYEAR, year or MINYEAR, year <= MAXYEAR:
        pass
    
    raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if not  <= 1, month or 1, month <= 12:
        pass
    
    raise ValueError('month must be in 1..12', month)
    if not  <= 1, day or 1, day <= dim:
        pass
    else:
        _days_in_month(year, month)
    raise ValueError('day must be in 1..%d' % dim, day)
    return (year, month, day)


def _check_time_fields(hour, minute, second, microsecond, fold):
    hour = _index(hour)
    minute = _index(minute)
    second = _index(second)
    microsecond = _index(microsecond)
    if not  <= 0, hour or 0, hour <= 23:
        pass
    
    raise ValueError('hour must be in 0..23', hour)
    if not  <= 0, minute or 0, minute <= 59:
        pass
    
    raise ValueError('minute must be in 0..59', minute)
    if not  <= 0, second or 0, second <= 59:
        pass
    
    raise ValueError('second must be in 0..59', second)
    if not  <= 0, microsecond or 0, microsecond <= 999999:
        pass
    
    raise ValueError('microsecond must be in 0..999999', microsecond)
    if fold not in (0, 1):
        pass
    raise ValueError('fold must be either 0 or 1', fold)
    return (hour, minute, second, microsecond, fold)


def _check_tzinfo_arg(tz):
    if tz:
        if isinstance(tz, tzinfo):
            pass
        if not isinstance(tz, tzinfo):
            pass
        raise TypeError('tzinfo argument must be None or of a tzinfo subclass')
    return None


def _divide_and_round(a, b):
    '''divide a by b and round result to the nearest integer

When the ratio is exactly half-way between two integers,
the even integer is returned.
'''
    if ():
        r *= 2
        if greater_than_half:
            pass
        if (greater_than_half or r == b) and q % 2 == 1:
            pass
    q += 1
    return q


def timedelta():
    '''timedelta'''
    __firstlineno__ = 578
    __doc__ = 'Represent the difference between two datetime objects.\n\nSupported operators:\n\n- add, subtract timedelta\n- unary plus, minus, abs\n- compare to timedelta\n- multiply, divide by int\n\nIn addition, datetime supports subtraction of two datetime objects\nreturning a timedelta, and addition or subtraction of a datetime\nand a timedelta giving a datetime.\n\nRepresentation: (days, seconds, microseconds).\n'
    __slots__ = ('_days', '_seconds', '_microseconds', '_hashcode')
    if (lambda cls, days, seconds, microseconds, milliseconds, minutes, hours, weeks: d = 0if 0:
days += weeks * 7seconds += minutes * 60 + hours * 3600microseconds += milliseconds * 1000if isinstance(days, float):
passif isinstance(days, float) or () or ():
if not daysecondswhole == int(daysecondswhole):
passraise ()if not days == int(days):
passraise int(daysecondswhole)int(days) = 0daysecondsfrac = 0d = daysif isinstance(daysecondsfrac, float):
passif not isinstance(daysecondsfrac, float):
passraise 0if not abs(daysecondsfrac) <= 1:
passraise Noneif isinstance(d, int):
passif not isinstance(d, int):
passraise Noneif not abs(s) <= 86400:
passraise Noneif isinstance(seconds, float):
passif isinstance(seconds, float) or ():
if not seconds == int(seconds):
passraise ()secondsfrac += daysecondsfrac = int(seconds)if not abs(secondsfrac) <= 2:
passraise ()secondsfrac = daysecondsfracif isinstance(secondsfrac, float):
passif not isinstance(secondsfrac, float):
passraise None(seconds)if not abs(secondsfrac) <= 2:
passraise _math.modfif isinstance(seconds, int):
passif not isinstance(seconds, int):
passraise Noneif ():
d += daysif isinstance(s, int):
passif not isinstance(s, int):
passraise ()if not abs(s) <= 172800:
passraise divmod(seconds, 86400)usdouble = secondsfrac * 1e+06if not abs(usdouble) < 2.1e+06:
passraise Noneif isinstance(microseconds, float):
passif isinstance(microseconds, float):
microseconds = round(microseconds + usdouble)if ():
passif isinstance(s, int):
passif not isinstance(s, int):
passraise divmod(seconds, 86400) if () else ()if isinstance(microseconds, int):
passif not isinstance(microseconds, int):
passraise ()if not abs(s) <= 259200:
passraise divmod(microseconds, 1000000)if not abs(microseconds) < 3.1e+06:
passraise ()if () or ():
if isinstance(d, int):
passif not isinstance(d, int):
passraise d += daysif isinstance(s, int):
passif isinstance(s, int):
if not  <= 0, s or 0, s < 86400:
raise ()()raise divmod(s, 86400)if isinstance(us, int):
passif isinstance(us, int):
if not  <= 0, us or 0, us < 1000000:
raise s += secondss += secondsraise ()if abs(d) > 999999999:
passraise OverflowError('timedelta # of days is too large: %d' % d)d = object.__new__(cls)self._seconds = sself._microseconds = usself._hashcode = -1self):
        
        def __new__(cls, days, seconds, microseconds, milliseconds, minutes, hours, weeks):
            d = 0
            if 0:
                days += weeks * 7
                seconds += minutes * 60 + hours * 3600
                microseconds += milliseconds * 1000
                if isinstance(days, float):
                    pass
                if isinstance(days, float) or () or ():
                    if not daysecondswhole == int(daysecondswhole):
                        pass
                    raise ()
                if not days == int(days):
                    pass
                raise int(daysecondswhole)
            int(days) = 0
            daysecondsfrac = 0
            d = days
            if isinstance(daysecondsfrac, float):
                pass
            if not isinstance(daysecondsfrac, float):
                pass
            raise 0
            if not abs(daysecondsfrac) <= 1:
                pass
            raise None
            if isinstance(d, int):
                pass
            if not isinstance(d, int):
                pass
            raise None
            if not abs(s) <= 86400:
                pass
            raise None
            if isinstance(seconds, float):
                pass
            if isinstance(seconds, float) or ():
                if not seconds == int(seconds):
                    pass
                raise ()
            secondsfrac += daysecondsfrac = int(seconds)
            if not abs(secondsfrac) <= 2:
                pass
            raise ()
            secondsfrac = daysecondsfrac
            if isinstance(secondsfrac, float):
                pass
            if not isinstance(secondsfrac, float):
                pass
            raise None(seconds)
            if not abs(secondsfrac) <= 2:
                pass
            raise _math.modf
            if isinstance(seconds, int):
                pass
            if not isinstance(seconds, int):
                pass
            raise None
            if ():
                d += days
            if isinstance(s, int):
                pass
            if not isinstance(s, int):
                pass
            raise ()
            if not abs(s) <= 172800:
                pass
            raise divmod(seconds, 86400)
            usdouble = secondsfrac * 1e+06
            if not abs(usdouble) < 2.1e+06:
                pass
            raise None
            if isinstance(microseconds, float):
                pass
            if isinstance(microseconds, float):
                microseconds = round(microseconds + usdouble)
                if ():
                    pass
            if isinstance(s, int):
                pass
            if not isinstance(s, int):
                pass
            raise divmod(seconds, 86400) if () else ()
            if isinstance(microseconds, int):
                pass
            if not isinstance(microseconds, int):
                pass
            raise ()
            if not abs(s) <= 259200:
                pass
            raise divmod(microseconds, 1000000)
            if not abs(microseconds) < 3.1e+06:
                pass
            raise ()
            if () or ():
                if isinstance(d, int):
                    pass
                if not isinstance(d, int):
                    pass
            raise d += days
            if isinstance(s, int):
                pass
            if isinstance(s, int):
                if not  <= 0, s or 0, s < 86400:
                    raise ()
            ()
            raise divmod(s, 86400)
            if isinstance(us, int):
                pass
            if isinstance(us, int):
                if not  <= 0, us or 0, us < 1000000:
                    raise s += seconds
            s += seconds
            raise ()
            if abs(d) > 999999999:
                pass
            raise OverflowError('timedelta # of days is too large: %d' % d)
            d = object.__new__(cls)
            self._seconds = s
            self._microseconds = us
            self._hashcode = -1
            return self

    
    def __repr__(self):
        args = []
        if self._days:
            pass
        if self._days:
            pass
        args.append('days=%d' % self._days)
        if self._seconds:
            pass
        if self._seconds:
            pass
        args.append('seconds=%d' % self._seconds)
        if self._microseconds:
            pass
        if self._microseconds:
            pass
        args.append('microseconds=%d' % self._microseconds)
        if args:
            pass
        if not args:
            pass
        args.append('0')
        return f'''{_get_class_module(self)}.{self.__class__.__qualname__}({', '.join(args)})'''

    
    def __str__(self):
        if () or ():
            if self._days:
                pass
            if self._days:
                (lambda n: if abs(n) != 1:
passif abs(n) != 1:
abs(n) != 1if 's':
passif not 's':
's'(n, '')) = '%d:%02d:%02d' % (hh, mm, ss)
        s = plural % None(self._days) + s
        if self._microseconds:
            pass
        if self._microseconds:
            pass
        s = s + '.%06d' % self._microseconds
        return s

    
    def total_seconds(self):
        '''Total seconds in the duration.'''
        return ((self.days * 86400 + self.seconds) * 1000000 + self.microseconds) / 1000000

    days = (lambda self: self._days)()
    seconds = (lambda self: self._seconds)()
    microseconds = (lambda self: self._microseconds)()
    
    def __add__(self, other):
        if isinstance(other, timedelta):
            pass
        if isinstance(other, timedelta):
            pass
        return timedelta(self._days + other._days, self._seconds + other._seconds, self._microseconds + other._microseconds)
        return NotImplemented

    __radd__ = __add__
    
    def __sub__(self, other):
        if isinstance(other, timedelta):
            pass
        if isinstance(other, timedelta):
            pass
        return timedelta(self._days - other._days, self._seconds - other._seconds, self._microseconds - other._microseconds)
        return NotImplemented

    
    def __rsub__(self, other):
        if isinstance(other, timedelta):
            pass
        if isinstance(other, timedelta):
            pass
        return -self + other
        return NotImplemented

    
    def __neg__(self):
        return timedelta(-(self._days), -(self._seconds), -(self._microseconds))

    
    def __pos__(self):
        return self

    
    def __abs__(self):
        if self._days < 0:
            pass
        return -self
        return self

    
    def __mul__(self, other):
