# Source Generated with Decompyle++
# File: tracemalloc.marshal (Python 3.13)

from collections.abc import Sequence, Iterable
from functools import total_ordering
import fnmatch
import linecache
import os.path as os
import pickle
None(import _tracemalloc)
from _tracemalloc import _get_object_traceback, _get_traces

def _format_size(size, sign):
    for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB'):
        if abs(size) < 100 and unit != 'B':
            if sign:
                pass
            if sign:
                
            return None, '%+.1f %s' % (size, unit)
        
        return None, None % (size, unit)
        if abs(size) < 10240 or unit == 'TiB':
            if sign:
                pass
            if sign:
                
            return None, '%+.0f %s' % (size, unit)
        
        return None, None % (size, unit)


def Statistic():
    '''Statistic'''
    __firstlineno__ = 30
    __doc__ = '\nStatistic difference on memory allocations between two Snapshot instance.\n'
    __slots__ = ('traceback', 'size', 'count')
    
    def __init__(self, traceback, size, count):
        self.traceback = traceback
        self.size = size
        self.count = count

    
    def __hash__(self):
        return hash((self.traceback, self.size, self.count))

    
    def __eq__(self, other):
        if isinstance(other, Statistic):
            pass
        if not isinstance(other, Statistic):
            pass
        return NotImplemented
        if self.traceback == other.traceback:
            pass
        if self.traceback == other.traceback:
            self.traceback == other.traceback
            if self.size == other.size:
                pass
            if self.size == other.size:
                self.size == other.size
        return self.count == other.count

    
    def __str__(self):
        text = '%s: size=%s, count=%i' % (self.traceback, _format_size(self.size, False), self.count)
        if self.count:
            pass
        if self.count:
            average = self.size / self.count
        text += ', average=%s' % _format_size(average, False)
        return text

    
    def __repr__(self):
        return '<Statistic traceback=%r size=%i count=%i>' % (self.traceback, self.size, self.count)

    
    def _sort_key(self):
        return (self.size, self.count, self.traceback)

    __static_attributes__ = ('count', 'size', 'traceback')

Statistic = None(Statistic, 'Statistic')

def StatisticDiff():
    '''StatisticDiff'''
    __firstlineno__ = 70
    __doc__ = '\nStatistic difference on memory allocations between an old and a new\nSnapshot instance.\n'
    __slots__ = ('traceback', 'size', 'size_diff', 'count', 'count_diff')
    
    def __init__(self, traceback, size, size_diff, count, count_diff):
        self.traceback = traceback
        self.size = size
        self.size_diff = size_diff
        self.count = count
        self.count_diff = count_diff

    
    def __hash__(self):
        return hash((self.traceback, self.size, self.size_diff, self.count, self.count_diff))

    
    def __eq__(self, other):
        if isinstance(other, StatisticDiff):
            pass
        if not isinstance(other, StatisticDiff):
            pass
        return NotImplemented
        if self.traceback == other.traceback:
            pass
        if self.traceback == other.traceback:
            self.traceback == other.traceback
            if self.size == other.size:
                pass
            if self.size == other.size:
                self.size == other.size
                if self.size_diff == other.size_diff:
                    pass
                if self.size_diff == other.size_diff:
                    self.size_diff == other.size_diff
                    if self.count == other.count:
                        pass
                    if self.count == other.count:
                        self.count == other.count
        return self.count_diff == other.count_diff

    
    def __str__(self):
        text = '%s: size=%s (%s), count=%i (%+i)' % (self.traceback, _format_size(self.size, False), _format_size(self.size_diff, True), self.count, self.count_diff)
        if self.count:
            pass
        if self.count:
            average = self.size / self.count
        text += ', average=%s' % _format_size(average, False)
        return text

    
    def __repr__(self):
        return '<StatisticDiff traceback=%r size=%i (%+i) count=%i (%+i)>' % (self.traceback, self.size, self.size_diff, self.count, self.count_diff)

    
    def _sort_key(self):
        return (abs(self.size_diff), self.size, abs(self.count_diff), self.count, self.traceback)

    __static_attributes__ = ('count', 'count_diff', 'size', 'size_diff', 'traceback')

StatisticDiff = None(StatisticDiff, 'StatisticDiff')

def _compare_grouped_stats(old_group, new_group):
    statistics = []
    for None in new_group.items():
        pass
    for None in old_group.items():
        if ():
            pass
    ()
    return statistics


def Frame():
    '''Frame'''
    __firstlineno__ = 140
    __doc__ = '\nFrame of a traceback.\n'
    __slots__ = ('_frame',)
    
    def __init__(self, frame):
        self._frame = frame

    filename = (lambda self: self._frame[0])()
    lineno = (lambda self: self._frame[1])()
    
    def __eq__(self, other):
        if isinstance(other, Frame):
            pass
        if not isinstance(other, Frame):
            pass
        return NotImplemented
        return self._frame == other._frame

    
    def __lt__(self, other):
        if isinstance(other, Frame):
            pass
        if not isinstance(other, Frame):
            pass
        return NotImplemented
        return self._frame < other._frame

    
    def __hash__(self):
        return hash(self._frame)

    
    def __str__(self):
        return f'''{self.filename}:{self.lineno}'''

    
    def __repr__(self):
        return f'''<Frame filename={self.filename} lineno={self.lineno}>'''

    __static_attributes__ = ('_frame',)

Frame = None(Frame, 'Frame')()

def Traceback():
    '''Traceback'''
    __firstlineno__ = 179
    __doc__ = '\nSequence of Frame instances sorted from the oldest frame\nto the most recent frame.\n'
    __slots__ = ('_frames', '_total_nframe')
    if (lambda self, frames, total_nframe: None(self)self._frames = tuple(reversed(frames))self._total_nframe = total_nframe):
        
        def __init__(self, frames, total_nframe):
            None(self)
            self._frames = tuple(reversed(frames))
            self._total_nframe = total_nframe

    total_nframe = (lambda self: self._total_nframe)()
    
    def __len__(self):
        return len(self._frames)

    
    def __getitem__(self, index):
        if isinstance(index, slice):
            pass
        if isinstance(index, slice):
            pass
        return (lambda .0: if None:
passfor trace in .0:
if Frame(trace):
passFrame(trace))(self._frames[index]())
        return Frame(self._frames[index])

    
    def __contains__(self, frame):
        return frame._frame in self._frames

    
    def __hash__(self):
        return hash(self._frames)

    
    def __eq__(self, other):
        if isinstance(other, Traceback):
            pass
        if not isinstance(other, Traceback):
            pass
        return NotImplemented
        return self._frames == other._frames

    
    def __lt__(self, other):
        if isinstance(other, Traceback):
            pass
        if not isinstance(other, Traceback):
            pass
        return NotImplemented
        return self._frames < other._frames

    
    def __str__(self):
        return str(self[0])

    
    def __repr__(self):
        s = f'''<Traceback {tuple(self)}'''
        if self._total_nframe:
            s += '>'
        return s
        s += f''' total_nframe={self.total_nframe}>'''
        return s

    if (lambda self, limit, most_recent_first: lines = []if most_recent_first:
passif most_recent_first:
passframe_slice = reversed(frame_slice)for frame in frame_slice:
lines.append(f'''  File "{frame.filename}", line {frame.lineno}''')line = None(frame.filename, frame.lineno).strip()if line:
passif not line:
continuelines.append('    %s' % line)None if limit else limitlines):
        
        def format(self, limit, most_recent_first):
            lines = []
            if most_recent_first:
                pass
            if most_recent_first:
                pass
            frame_slice = reversed(frame_slice)
            for frame in frame_slice:
                lines.append(f'''  File "{frame.filename}", line {frame.lineno}''')
                line = None(frame.filename, frame.lineno).strip()
                if line:
                    pass
                if not line:
                    continue
                lines.append('    %s' % line)
            None if limit else limit
            return lines

    __static_attributes__ = ('_frames', '_total_nframe')

Traceback = None(Traceback, 'Traceback', Sequence)()

def get_object_traceback(obj):
    '''
Get the traceback where the Python object *obj* was allocated.
Return a Traceback instance.

Return None if the tracemalloc module is not tracing memory allocations or
did not trace the allocation of the object.
'''
    frames = _get_object_traceback(obj)
    if frames:
        pass
    return Traceback(frames)


def Trace():
    '''Trace'''
    __firstlineno__ = 272
    __doc__ = '\nTrace of a memory block.\n'
    __slots__ = ('_trace',)
    
    def __init__(self, trace):
        self._trace = trace

    domain = (lambda self: self._trace[0])()
    size = (lambda self: self._trace[1])()
    traceback = (lambda self: Traceback(self._trace[2:]))()
    
    def __eq__(self, other):
        if isinstance(other, Trace):
            pass
        if not isinstance(other, Trace):
            pass
        return NotImplemented
        return self._trace == other._trace

    
    def __hash__(self):
        return hash(self._trace)

    
    def __str__(self):
        return f'''{self.traceback}: {_format_size(self.size, False)}'''

    
    def __repr__(self):
        return f'''<Trace domain={self.domain} size={_format_size(self.size, False)}, traceback={self.traceback}>'''

    __static_attributes__ = ('_trace',)

Trace = None(Trace, 'Trace')

def _Traces():
    '''_Traces'''
    __firstlineno__ = 311
    
    def __init__(self, traces):
        None(self)
        self._traces = traces

    
    def __len__(self):
        return len(self._traces)

    
    def __getitem__(self, index):
        if isinstance(index, slice):
            pass
        if isinstance(index, slice):
            pass
        return (lambda .0: if None:
passfor trace in .0:
if Trace(trace):
passTrace(trace))(self._traces[index]())
        return Trace(self._traces[index])

    
    def __contains__(self, trace):
        return trace._trace in self._traces

    
    def __eq__(self, other):
        if isinstance(other, _Traces):
            pass
        if not isinstance(other, _Traces):
            pass
        return NotImplemented
        return self._traces == other._traces

    
    def __repr__(self):
        return '<Traces len=%s>' % len(self)

    __static_attributes__ = ('_traces',)

_Traces = None(_Traces, '_Traces', Sequence)

def _normalize_filename(filename):
    filename = os.path.normcase(filename)
    if filename.endswith('.pyc'):
        pass
    if filename.endswith('.pyc'):
        pass
    filename = filename[:-1]
    return filename


def BaseFilter():
    '''BaseFilter'''
    __firstlineno__ = 345
    
    def __init__(self, inclusive):
        self.inclusive = inclusive

    
    def _match(self, trace):
        raise NotImplementedError

    __static_attributes__ = ('inclusive',)

BaseFilter = None(BaseFilter, 'BaseFilter')

def Filter():
    '''Filter'''
    __firstlineno__ = 353
    if (lambda self, inclusive, filename_pattern, lineno, all_frames, domain: self(inclusive)self.inclusive = inclusiveself._filename_pattern = _normalize_filename(filename_pattern)self.lineno = linenoself.all_frames = all_framesself.domain = domain):
        if (lambda self, inclusive, filename_pattern, lineno, all_frames, domain: self(inclusive)self.inclusive = inclusiveself._filename_pattern = _normalize_filename(filename_pattern)self.lineno = linenoself.all_frames = all_framesself.domain = domain):
            
            def __init__(self, inclusive, filename_pattern, lineno, all_frames, domain):
                self(inclusive)
                self.inclusive = inclusive
                self._filename_pattern = _normalize_filename(filename_pattern)
                self.lineno = lineno
                self.all_frames = all_frames
                self.domain = domain

    filename_pattern = (lambda self: self._filename_pattern)()
    
    def _match_frame_impl(self, filename, lineno):
        filename = _normalize_filename(filename)
        if None(filename, self._filename_pattern):
            pass
        if not None(filename, self._filename_pattern):
            pass
        return False
        if self.lineno:
            pass
        return True
        return lineno == self.lineno

    
    def _match_frame(self, filename, lineno):
        if self.inclusive:
            pass
        return self._match_frame_impl(filename, lineno) ^ (not (self.inclusive))

    
    def _match_traceback(self, traceback):
