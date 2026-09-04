# Source Generated with Decompyle++
# File: makepy.marshal (Python 3.13)

'''Generate a .py file from an OLE TypeLibrary file.


This module is concerned only with the actual writing of
a .py file.  It draws on the @build@ module, which builds
the knowledge of a COM interface.

'''
usageHelp = ' \nUsage:\n\n  makepy.py [-i] [-v|q] [-h] [-u] [-o output_file] [-d] [typelib, ...]\n\n  -i    -- Show information for the specified typelib.\n\n  -v    -- Verbose output.\n\n  -q    -- Quiet output.\n\n  -h    -- Do not generate hidden methods.\n\n  -u    -- Convert all Unicode objects to strings.\n\n  -o    -- Create output in a specified output file.  If the path leading\n           to the file does not exist, any missing directories will be\n           created.\n           NOTE: -o cannot be used with -d.  This will generate an error.\n\n  -d    -- Generate the base code now and the class code on demand.\n           Recommended for large type libraries.\n\n  typelib -- A TLB, DLL, OCX or anything containing COM type information.\n             If a typelib is not specified, a window containing a textbox\n             will open from which you can select a registered type\n             library.\n\nExamples:\n\n  makepy.py -d\n\n    Presents a list of registered type libraries from which you can make\n    a selection.\n\n  makepy.py -d "Microsoft Excel 8.0 Object Library"\n\n    Generate support for the type library with the specified description\n    (in this case, the MS Excel object model).\n\n'
import importlib
import os
import sys
import pythoncom
from win32com.client import Dispatch, gencache, genpy, selecttlb
bForDemandDefault = 0

def usage():
    sys.stderr.write(usageHelp)
    None(2)


def ShowInfo(spec):
    if spec:
        pass
    for None in infos:
        if () or desc:
            pass
        print(' {}, lcid={}, major={}, minor={}'.format(tlbSpec.clsid, tlbSpec.lcid, tlbSpec.major, tlbSpec.minor))
        print(' >>> # Use these commands in Python code to auto generate .py support')
        print(' >>> from win32com.client import gencache')
        print(" >>> gencache.EnsureModule('{}', {}, {}, {})".format(tlbSpec.clsid, tlbSpec.lcid, tlbSpec.major, tlbSpec.minor))
    ()


def SimpleProgress():
    '''SimpleProgress'''
    __firstlineno__ = 122
    __doc__ = 'A simple progress class prints its output to stderr'
    
    def __init__(self, verboseLevel):
        self.verboseLevel = verboseLevel

    
    def Close(self):
        pass

    
    def Finished(self):
        if self.verboseLevel > 1:
            sys.stderr.write('Generation complete..\n')
        return None

    if (lambda self, desc, maxticks: if self.verboseLevel:
passif self.verboseLevel:
sys.stderr.write(desc + '\n')None):
        
        def SetDescription(self, desc, maxticks):
            if self.verboseLevel:
                pass
            if self.verboseLevel:
                sys.stderr.write(desc + '\n')
            return None

    if (lambda self, desc: pass):
        
        def Tick(self, desc):
            pass

    if (lambda self, desc, verboseLevel: if self.verboseLevel >= verboseLevel:
sys.stderr.write(desc + '\n')None):
        
        def VerboseProgress(self, desc, verboseLevel):
            if self.verboseLevel >= verboseLevel:
                sys.stderr.write(desc + '\n')
            return None

    
    def LogBeginGenerate(self, filename):
        self.VerboseProgress('Generating to %s' % filename, 1)

    
    def LogWarning(self, desc):
        self.VerboseProgress('WARNING: ' + desc, 1)

    __static_attributes__ = ('verboseLevel',)

SimpleProgress = None(SimpleProgress, 'SimpleProgress', genpy.GeneratorProgress)

def GUIProgress():
    '''GUIProgress'''
    __firstlineno__ = 153
    
    def __init__(self, verboseLevel):
        import pywin
        import win32ui
        SimpleProgress.__init__(self, verboseLevel)
        self.dialog = None

    
    def Close(self):
        if self.dialog:
            self.dialog = None
        return None

    
    def Starting(self, tlb_desc):
        SimpleProgress.Starting(self, tlb_desc)
        if self.dialog:
            status = status
            self.dialog = status.ThreadedStatusProgressDialog(tlb_desc)
        return None
        self.dialog.SetTitle(tlb_desc)

    if (lambda self, desc, maxticks: self.dialog.SetText(desc)if maxticks:
passif maxticks:
self.dialog.SetMaxTicks(maxticks)None):
        
        def SetDescription(self, desc, maxticks):
            self.dialog.SetText(desc)
            if maxticks:
                pass
            if maxticks:
                self.dialog.SetMaxTicks(maxticks)
            return None

    if (lambda self, desc: self.dialog.Tick()if desc:
passNone):
        
        def Tick(self, desc):
            self.dialog.Tick()
            if desc:
                pass
            return None

    __static_attributes__ = ('dialog',)

GUIProgress = None(GUIProgress, 'GUIProgress', SimpleProgress)

def GetTypeLibsForSpec(arg):
    '''Given an argument on the command line (either a file name, library
description, or ProgID of an object) return a list of actual typelibs
to use.'''
    typelibs = []
    
    try:
        tlb = None(arg)
        spec = None(None, 0, 0, 0)
        spec.FromTypelib(tlb, arg)
        typelibs.append((tlb, spec))
    except pythoncom.com_error:
        tlbs = None(arg)
        if len(tlbs) == 0:
            pass
        print("Could not locate a type library matching '%s'" % arg)
        for None in tlbs:
            attr = tlb.GetLibAttr()
            spec.major = attr[3]
            spec.minor = attr[4]
            spec.lcid = attr[1]
            typelibs.append((tlb, spec))
        spec.dll

    
    try:
        pass
    except pythoncom.com_error:
        if (tb,):
            None(1)
            return None

    return None
    
    try:
        pass
    except pythoncom.com_error:
        if (tb,):
            None(1)
            return None


if (lambda typelibInfo, file, verboseLevel, progressInstance, bForDemand, bBuildHidden: if verboseLevel:
passverboseLevel = 0if bForDemand:
passif bForDemand and file:
passraise RuntimeError('You can only perform a demand-build when the output goes to the gen_py directory')if isinstance(typelibInfo, tuple):
passif isinstance(typelibInfo, tuple) or () or ():
passelif isinstance(typelibInfo, selecttlb.TypelibSpec):
passif isinstance(typelibInfo, selecttlb.TypelibSpec):
typelibs = [
(tlb, typelibInfo)]elif hasattr(typelibInfo, 'GetLibAttr'):
passif progressInstance:
passprogressInstance = SimpleProgress(verboseLevel)progress = progressInstancebToGenDir = file is Nonefor typelib, info in typelibs:
gen = None(typelib, info.dll, progress, bBuildHidden = bBuildHidden)this_name = None(info.clsid, info.lcid, info.major, info.minor)worked = Falsetry:
gen.generate(fileUse, bForDemand)worked = Trueif file:
try:
except:
gen.finish_writer(outputName, fileUse, worked)None(None, None)with None:
if :
passif not :
passexcept:
passNone()if bToGenDir:
passif not bToGenDir:
continueprogress.SetDescription('Importing module')None(info.clsid, info.lcid, info.major, info.minor)importlib.invalidate_cachesprogress.Close()Nonetry:
None(this_name)gen.finish_writer(outputName, fileUse, worked)with None:
if :
passif not :
passexcept:
passfileNone if file else os.path.join if bForDemand else os.mkdirtry:
gen.generate(fileUse, bForDemand)worked = Trueif file:
try:
except:
gen.finish_writer(outputName, fileUse, worked)None(None, None)with None:
if :
passif not :
passexcept:
pass):
    
    def GenerateFromTypeLibSpec(typelibInfo, file, verboseLevel, progressInstance, bForDemand, bBuildHidden):
        if verboseLevel:
            pass
        verboseLevel = 0
        if bForDemand:
            pass
        if bForDemand and file:
            pass
        raise RuntimeError('You can only perform a demand-build when the output goes to the gen_py directory')
        if isinstance(typelibInfo, tuple):
            pass
        if isinstance(typelibInfo, tuple) or () or ():
            pass
        elif isinstance(typelibInfo, selecttlb.TypelibSpec):
            pass
        if isinstance(typelibInfo, selecttlb.TypelibSpec):
            typelibs = [
                (tlb, typelibInfo)]
        elif hasattr(typelibInfo, 'GetLibAttr'):
            pass
        if progressInstance:
            pass
        progressInstance = SimpleProgress(verboseLevel)
        progress = progressInstance
        bToGenDir = file is None
        for typelib, info in typelibs:
            gen = None(typelib, info.dll, progress, bBuildHidden = bBuildHidden)
            this_name = None(info.clsid, info.lcid, info.major, info.minor)
            worked = False
            
            try:
                gen.generate(fileUse, bForDemand)
                worked = True
            if file:
                
                try:
                    except:
                        gen.finish_writer(outputName, fileUse, worked)
                        None(None, None)
                        with None:
                            if :
                                pass

                if not :
                    pass
                except:
                    pass
                

            None()
            if bToGenDir:
                pass
            if not bToGenDir:
                continue
            progress.SetDescription('Importing module')
            None(info.clsid, info.lcid, info.major, info.minor)
        importlib.invalidate_caches
        progress.Close()
        return None
        
        try:
            None(this_name)
            gen.finish_writer(outputName, fileUse, worked)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        file
        None if file else os.path.join if bForDemand else os.mkdir
        
        try:
            gen.generate(fileUse, bForDemand)
            worked = True
        if file:
            
            try:
                except:
                    gen.finish_writer(outputName, fileUse, worked)
                    None(None, None)
                    with None:
                        if :
                            pass

            if not :
                pass
            except:
                pass
            


if (lambda child, typelibInfo, verboseLevel, progressInstance: if verboseLevel:
passverboseLevel = 0if isinstance(typelibInfo, tuple):
passspec = None(typelibCLSID, lcid, major, minor)spec.FromTypelib(tlb, str(typelibCLSID))typelibs = [
(tlb, spec)]if progressInstance:
passprogressInstance = SimpleProgress(verboseLevel)progress = progressInstancefor None in typelibs:
if ():
gencache.GetGeneratePath(None(), dir_name) = os.path.joingen = None(typelib, info.dll, progress)gen.generate_child(child, dir_path_name)progress.SetDescription('Importing module')None()try:
None(dir_name)__import__('win32com.gen_py.' + dir_name + '.' + child)with None:
if :
passgencache.ModuleMutexprogress.Close()Nonetry:
None(dir_name)__import__('win32com.gen_py.' + dir_name + '.' + child)with None:
if :
passif not :
passexcept:
passgenpy.Generatorcontinue):
    
    def GenerateChildFromTypeLibSpec(child, typelibInfo, verboseLevel, progressInstance):
        if verboseLevel:
            pass
        verboseLevel = 0
        if isinstance(typelibInfo, tuple):
            pass
        spec = None(typelibCLSID, lcid, major, minor)
        spec.FromTypelib(tlb, str(typelibCLSID))
        typelibs = [
            (tlb, spec)]
        if progressInstance:
            pass
        progressInstance = SimpleProgress(verboseLevel)
        progress = progressInstance
        for None in typelibs:
            if ():
                gencache.GetGeneratePath(None(), dir_name) = os.path.join
                gen = None(typelib, info.dll, progress)
                gen.generate_child(child, dir_path_name)
                progress.SetDescription('Importing module')
                None()
            
            try:
                None(dir_name)
                __import__('win32com.gen_py.' + dir_name + '.' + child)
            with None:
                if :
                    pass

        gencache.ModuleMutex
        progress.Close()
        return None
        
        try:
            None(dir_name)
            __import__('win32com.gen_py.' + dir_name + '.' + child)
        with None:
            if :
                pass

        if not :
            pass
        except:
            pass
        genpy.Generator
        continue


def main():
    import getopt
    hiddenSpec = 1
    outputName = None
    verboseLevel = 1
    doit = 1
    bForDemand = bForDemandDefault
    
    try:
        if ():
            for None in opts:
                if ():
                    if o == '-h':
                        continue
                    if o == '-o':
                        v = 0
                        continue
                    if o == '-v':
                        verboseLevel += 1
                        continue
                    if o == '-q':
                        verboseLevel -= 1
                        continue
                    if o == '-i':
                        doit = 0
                        continue
                    if not o == '-d':
                        continue
                    if bForDemand:
                        pass
                    bForDemand = not bForDemand
                    continue
                    if bForDemand:
                        pass
                    if bForDemand and outputName:
                        pass

    usage()
    if doit:
        pass
    if not doit:
        pass
    return 0
    if len(args) == 0:
        rc = None()
        if rc:
            pass
        None(1)
    args = [
        rc]
    for arg in args:
        GenerateFromTypeLibSpec(arg, f, verboseLevel = verboseLevel, bForDemand = bForDemand, bBuildHidden = hiddenSpec)
    os.makedirs if outputName else None
    if f:
        pass
    if f:
        f.close()
    return None
    return None
    if getopt.error:
        msg = outputName
        sys.stderr.write(str(msg) + '\n')
        usage()
        msg = None
        del msg
        continue
        msg = None
        del msg

if __name__ == '__main__':
    rc = None()
    if rc:
        pass
    if rc:
        pass
    None(rc)
    None(0)
return None
