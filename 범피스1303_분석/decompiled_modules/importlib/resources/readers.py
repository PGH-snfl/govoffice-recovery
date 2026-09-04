# Source Generated with Decompyle++
# File: readers.marshal (Python 3.13)

from __future__ import annotations
import collections
import contextlib
import itertools
import pathlib
import operator
import re
import warnings
import zipfile
from collections.abc import Iterator
from  import abc
from _itertools import only

def remove_duplicates(items):
    return iter(collections.OrderedDict.fromkeys(items))


def FileReader():
    '''FileReader'''
    __firstlineno__ = 22
    
    def __init__(self, loader):
        self.path = None(loader.path).parent

    
    def resource_path(self, resource):
        '''
Return the file system path to prevent
`resources.path()` from creating a temporary
copy.
'''
        return str(self.path.joinpath(resource))

    
    def files(self):
        return self.path

    __static_attributes__ = ('path',)

FileReader = None(FileReader, 'FileReader', abc.TraversableResources)

def ZipReader():
    '''ZipReader'''
    __firstlineno__ = 38
    
    def __init__(self, loader, module):
        self.prefix = loader.prefix.replace('\\', '/')
        if loader.is_package(module):
            pass
        if loader.is_package(module):
            ()
            if module.rpartition('.'):
                loader.archive = self, self.prefix += name + '/', .prefix
                return None

    if (lambda self, resource: try:
passexcept KeyError:
exc = Noneraise FileNotFoundError(exc.args[0])exc = Nonedel exc):
        
        def open_resource(self, resource):
            
            try:
                pass
            except KeyError:
                exc = None
                raise FileNotFoundError(exc.args[0])
                exc = None
                del exc


        
        def is_resource(self, path):
            '''
Workaround for `zipfile.Path.is_file` returning true
for non-existent paths.
'''
            target = self.files().joinpath(path)
            if target.is_file():
                pass
            if target.is_file():
                target.is_file()
            return target.exists()

        
        def files(self):
            return None(self.archive, self.prefix)

    __static_attributes__ = ('archive', 'prefix')
    __classcell__ = __class__
    return __class__

ZipReader = None(ZipReader, 'ZipReader', abc.TraversableResources)

def MultiplexedPath():
    '''MultiplexedPath'''
    __firstlineno__ = 64
    __doc__ = '\nGiven a series of Traversable objects, implement a merged\nversion of the interface across all objects. Useful for\nnamespace packages which may be multihomed at a single\nname.\n'
    
    def __init__(self, *paths):
        self._paths = list(map(_ensure_traversable, remove_duplicates(paths)))
        if self._paths:
            pass
        if not self._paths:
            message = 'MultiplexedPath must contain at least one path'
        raise FileNotFoundError(message)
        if (lambda .0: if None:
passfor None in .0:
if None:
if None.is_dir():
pass)(self._paths()):
            pass
        if not (lambda .0: if None:
passfor None in .0:
if None:
if None.is_dir():
pass)(self._paths()):
            pass
        raise NotADirectoryError('MultiplexedPath only supports directories')

    
    def iterdir(self):
        children = self._paths()
        by_name = None('name')
        groups = None(sorted(children, key = by_name), key = by_name)
        
        def <genexpr>(.0):
            if None:
                pass
            for None in .0:
                if ():
                    if locs:
                        pass
                    continue
                    return None

        return self._follow(<genexpr>, groups())

    
    def read_bytes(self):
        raise FileNotFoundError(f'''{self} is not a file''')

    
    def read_text(self, *args, **kwargs):
        raise FileNotFoundError(f'''{self} is not a file''')

    
    def is_dir(self):
        return True

    
    def is_file(self):
        return False

    if (lambda self: try:
passexcept abc.TraversalError:
pass):
        
        def joinpath(self, *descendants):
            
            try:
                pass
            except abc.TraversalError:
                pass


    _follow = (lambda cls, children: if (one_file,):
try:
pass(one_file,)if ValueError:
(one_file,)try:
passif NotADirectoryError:
(one_file,))()
    
    def open(self, *args, **kwargs):
        raise FileNotFoundError(f'''{self} is not a file''')

    name = (lambda self: self._paths[0].name)()
    
    def __repr__(self):
        paths = (lambda .0: if None:
passfor path in .0:
if f'''\'{path}\'''':
passf'''\'{path}\'''')(self._paths())
        return f'''MultiplexedPath({paths})'''

    __static_attributes__ = ('_paths',)
    __classcell__ = __class__
    return __class__

MultiplexedPath = None(MultiplexedPath, 'MultiplexedPath', abc.Traversable)

def NamespaceReader():
    '''NamespaceReader'''
    __firstlineno__ = 137
    
    def __init__(self, namespace_path):
        if 'NamespacePath' not in str(namespace_path):
            pass
        raise ValueError('Invalid path')
        self.path = MultiplexedPath(filter(bool, map(self._resolve, namespace_path)))

    if (lambda cls, path_str: dirs = cls._candidate_paths(path_str)()next(dirs, None)):
        pass
    _resolve = (lambda cls, path_str: dirs = cls._candidate_paths(path_str)()next(dirs, None))()
    if (lambda cls, path_str: if None:
passif None(path_str):
passNone(path_str)if None and None:
passcontinueNonecontinue):
        pass
    _candidate_paths = (lambda cls, path_str: if None:
passif None(path_str):
passNone(path_str)if None and None:
passcontinueNonecontinue)()
    if (lambda path_str: if None:
passfor match in list(re.finditer(None('[\\\\/]', path_str))):
try:
None(FileNotFoundError, IsADirectoryError, NotADirectoryError, PermissionError)inner = path_str[match.end():].replace('\\', '/') + '/'if None(path_str[:match.start()], inner.lstrip('/')):
passNone(path_str[:match.start()], inner.lstrip('/'))with None:
if :
passNone(None, None)contextlib.suppressNonetry:
None(FileNotFoundError, IsADirectoryError, NotADirectoryError, PermissionError)inner = path_str[match.end():].replace('\\', '/') + '/'if None(path_str[:match.start()], inner.lstrip('/')):
passNone(path_str[:match.start()], inner.lstrip('/'))with None:
if :
passif not :
passexcept:
passcontinue):
        pass
    _resolve_zip_path = (lambda path_str: if None:
passfor match in list(re.finditer(None('[\\\\/]', path_str))):
try:
None(FileNotFoundError, IsADirectoryError, NotADirectoryError, PermissionError)inner = path_str[match.end():].replace('\\', '/') + '/'if None(path_str[:match.start()], inner.lstrip('/')):
passNone(path_str[:match.start()], inner.lstrip('/'))with None:
if :
passNone(None, None)contextlib.suppressNonetry:
None(FileNotFoundError, IsADirectoryError, NotADirectoryError, PermissionError)inner = path_str[match.end():].replace('\\', '/') + '/'if None(path_str[:match.start()], inner.lstrip('/')):
passNone(path_str[:match.start()], inner.lstrip('/'))with None:
if :
passif not :
passexcept:
passcontinue)()
    
    def resource_path(self, resource):
        '''
Return the file system path to prevent
`resources.path()` from creating a temporary
copy.
'''
        return str(self.path.joinpath(resource))

    
    def files(self):
        return self.path

    __static_attributes__ = ('path',)

NamespaceReader = None(NamespaceReader, 'NamespaceReader', abc.TraversableResources)

def _ensure_traversable(path):
    '''
Convert deprecated string arguments to traversables (pathlib.Path).

Remove with Python 3.15.
'''
    if isinstance(path, str):
        pass
    if not isinstance(path, str):
        pass
    return path
    None('String arguments are deprecated. Pass a Traversable instead.', DeprecationWarning, stacklevel = 3)
    return None(path)

