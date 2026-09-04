# Source Generated with Decompyle++
# File: _adapters.marshal (Python 3.13)

from contextlib import suppress
from io import TextIOWrapper
from  import abc

def SpecLoaderAdapter():
    '''SpecLoaderAdapter'''
    __firstlineno__ = 7
    __doc__ = '\nAdapt a package spec to adapt the underlying loader.\n'
    if (lambda self, spec, adapter: self.spec = specself.loader = None(spec)):
        
        def __init__(self, spec, adapter):
            self.spec = spec
            self.loader = None(spec)

    
    def __getattr__(self, name):
        return getattr(self.spec, name)

    __static_attributes__ = ('loader', 'spec')

SpecLoaderAdapter = None(SpecLoaderAdapter, 'SpecLoaderAdapter')

def TraversableResourcesLoader():
    '''TraversableResourcesLoader'''
    __firstlineno__ = 20
    __doc__ = '\nAdapt a loader to provide TraversableResources.\n'
    
    def __init__(self, spec):
        self.spec = spec

    
    def get_resource_reader(self, name):
        return CompatibilityFiles(self.spec)._native()

    __static_attributes__ = ('spec',)

TraversableResourcesLoader = None(TraversableResourcesLoader, 'TraversableResourcesLoader')
if (lambda file, mode: if mode == 'r':
passNone(TextIOWrapper)({ }, kwargs = None)if mode == 'rb':
passfileraise ValueError(f'''Invalid mode value \'{mode}\', only \'r\' and \'rb\' are supported''')):
    
    def _io_wrapper(file, mode, *args, **kwargs):
        if mode == 'r':
            pass
        return None(TextIOWrapper)({ }, kwargs = None)
        if mode == 'rb':
            pass
        return file
        raise ValueError(f'''Invalid mode value \'{mode}\', only \'r\' and \'rb\' are supported''')


def CompatibilityFiles():
    '''CompatibilityFiles'''
    __firstlineno__ = 40
    __doc__ = '\nAdapter for an existing or non-existent resource reader\nto provide a compatibility .files().\n'
    
    def SpecPath():
        '''CompatibilityFiles.SpecPath'''
        __firstlineno__ = 46
        __doc__ = '\nPath tied to a module spec.\nCan be read and exposes the resource reader children.\n'
        
        def __init__(self, spec, reader):
            self._spec = spec
            self._reader = reader

        
        def iterdir(self):
            if self._reader:
                pass
            if not self._reader:
                pass
            return iter(())
            if (lambda .0: if None:
passfor path in .0:
if CompatibilityFiles.ChildPath(self._reader, path):
passCompatibilityFiles.ChildPath(self._reader, path)):
                pass
            return (lambda .0: if None:
passfor path in .0:
if CompatibilityFiles.ChildPath(self._reader, path):
passCompatibilityFiles.ChildPath(self._reader, path))(self._reader.contents()())

        
        def is_file(self):
            return False

        is_dir = is_file
        
        def joinpath(self, other):
            if self._reader:
                pass
            if not self._reader:
                pass
            return CompatibilityFiles.OrphanPath(other)
            return CompatibilityFiles.ChildPath(self._reader, other)

        name = (lambda self: self._spec.name)()
        if (lambda self, mode: None(_io_wrapper)({ }, kwargs = None)):
            
            def open(self, mode, *args, **kwargs):
                return None(_io_wrapper)({ }, kwargs = None)

        __static_attributes__ = ('_reader', '_spec')

    SpecPath = None(SpecPath, 'SpecPath', abc.Traversable)
    
    def ChildPath():
        '''CompatibilityFiles.ChildPath'''
        __firstlineno__ = 81
        __doc__ = "\nPath tied to a resource reader child.\nCan be read but doesn't expose any meaningful children.\n"
        
        def __init__(self, reader, name):
            self._reader = reader
            self._name = name

        
        def iterdir(self):
            return iter(())

        
        def is_file(self):
            return self._reader.is_resource(self.name)

        
        def is_dir(self):
            if self.is_file():
                pass
            return not self.is_file()

        
        def joinpath(self, other):
            return CompatibilityFiles.OrphanPath(self.name, other)

        name = (lambda self: self._name)()
        if (lambda self, mode: None(_io_wrapper)({ }, kwargs = None)):
            
            def open(self, mode, *args, **kwargs):
                return None(_io_wrapper)({ }, kwargs = None)

        __static_attributes__ = ('_name', '_reader')

    ChildPath = None(ChildPath, 'ChildPath', abc.Traversable)
    
    def OrphanPath():
        '''CompatibilityFiles.OrphanPath'''
        __firstlineno__ = 112
        __doc__ = "\nOrphan path, not tied to a module spec or resource reader.\nCan't be read and doesn't expose any meaningful children.\n"
        
        def __init__(self, *path_parts):
            if len(path_parts) < 1:
                pass
            raise ValueError('Need at least one path part to construct a path')
            self._path = path_parts

        
        def iterdir(self):
            return iter(())

        
        def is_file(self):
            return False

        is_dir = is_file
        
        def joinpath(self, other):
            return None(None(None[other]))

        name = (lambda self: self._path[-1])()
        if (lambda self, mode: raise FileNotFoundError("Can't open orphan path")):
            
            def open(self, mode, *args, **kwargs):
                raise FileNotFoundError("Can't open orphan path")

        __static_attributes__ = ('_path',)

    OrphanPath = None(OrphanPath, 'OrphanPath', abc.Traversable)
    
    def __init__(self, spec):
        self.spec = spec

    
    class _reader:
