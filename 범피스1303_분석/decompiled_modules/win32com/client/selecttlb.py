# Source Generated with Decompyle++
# File: selecttlb.marshal (Python 3.13)

'''Utilities for selecting and enumerating the Type Libraries installed on the system'''
import pythoncom
import win32api
import win32con

def TypelibSpec():
    '''TypelibSpec'''
    __firstlineno__ = 8
    if (lambda self, clsid, lcid, major, minor, flags: self.clsid = str(clsid)self.lcid = int(lcid)self.major = majorself.minor = minorself.dll = Noneself.desc = Noneself.ver_desc = Noneself.flags = flags):
        
        def __init__(self, clsid, lcid, major, minor, flags):
            self.clsid = str(clsid)
            self.lcid = int(lcid)
            self.major = major
            self.minor = minor
            self.dll = None
            self.desc = None
            self.ver_desc = None
            self.flags = flags

    
    def __getitem__(self, item):
        if item == 0:
            pass
        return self.ver_desc
        raise IndexError("Can't index me!")

    
    def __lt__(self, other):
        if self.ver_desc:
            pass
        if not self.ver_desc:
            self.ver_desc
        if self.desc:
            pass
        if not self.desc:
            self.desc
        me = (''.lower(), ''.lower(), self.major, self.minor)
        if other.ver_desc:
            pass
        if not other.ver_desc:
            other.ver_desc
        if other.desc:
            pass
        if not other.desc:
            other.desc
        them = (''.lower(), ''.lower(), other.major, other.minor)
        return me < them

    
    def __eq__(self, other):
        if self.ver_desc:
            pass
        if not self.ver_desc:
            self.ver_desc
        if other.ver_desc:
            pass
        if not other.ver_desc:
            other.ver_desc
        if ''.lower() == ''.lower():
            pass
        if ''.lower() == ''.lower():
            ''.lower() == ''.lower()
            if self.desc:
                pass
            if not self.desc:
                self.desc
            if other.desc:
                pass
            if not other.desc:
                other.desc
            if ''.lower() == ''.lower():
                pass
            if ''.lower() == ''.lower():
                ''.lower() == ''.lower()
                if self.major == other.major:
                    pass
                if self.major == other.major:
                    self.major == other.major
        return self.minor == other.minor

    
    def Resolve(self):
        if self.dll:
            pass
        return 0
        tlb = None(self.dll)
        self.FromTypelib(tlb, None)
        return 1

    if (lambda self, typelib, dllName: la = typelib.GetLibAttr()self.clsid = str(la[0])self.lcid = la[1]self.major = la[3]self.minor = la[4]if dllName:
passif dllName:
self.dll = dllNameNone):
        
        def FromTypelib(self, typelib, dllName):
            la = typelib.GetLibAttr()
            self.clsid = str(la[0])
            self.lcid = la[1]
            self.major = la[3]
            self.minor = la[4]
            if dllName:
                pass
            if dllName:
                self.dll = dllName
            return None

    __static_attributes__ = ('clsid', 'desc', 'dll', 'flags', 'lcid', 'major', 'minor', 'ver_desc')

TypelibSpec = None(TypelibSpec, 'TypelibSpec')

def EnumKeys(root):
    index = 0
    ret = []
    
    try:
        item = None(root, index)
    except win32api.error:
        pass

    
    try:
        val = None(root, item)
    except win32api.error:
        val = ''

    ret.append((item, val))
    index += 1
    continue

FLAG_RESTRICTED = 1
FLAG_CONTROL = 2
FLAG_HIDDEN = 4
if (lambda excludeFlags: key = None(win32con.HKEY_CLASSES_ROOT, 'Typelib')iids = EnumKeys(key)results = []for None in iids:
if ():
try:
passfor None in EnumKeys(key2):
if ():
if len(major_minor) < 2:
passmajor_minor[0] = version.split('.', 1)minor = major_minor[1]key3 = None(key2, str(version))try:
flags = win32api.RegQueryValue(None(key3, 'FLAGS'))except (win32api.error, ValueError):
()flags = 0if not flags & excludeFlags == 0:
continuefor None in EnumKeys(key3):
if ():
try:
passexcept ValueError:
win32api.RegOpenKeytry:
None(key3, f'''{lcid}\\win32''') = win32api.RegOpenKeyexcept win32api.error:
try:
key4 = None(key3, f'''{lcid}\\win64''')except win32api.error:
passtry:
(dll, typ) = None(key4, None)if typ == win32con.REG_EXPAND_SZ:
passdll = None(dll)except win32api.error:
()dll = Nonespec = TypelibSpec(iid, lcid, major, minor, flags)spec.dll = dllspec.desc = tlbdescspec.ver_desc = tlbdesc + ' (' + version + ')'continuecontinue()continue()resultsif win32api.error:
()continue):
    
    def EnumTlbs(excludeFlags):
        '''Return a list of TypelibSpec objects, one for each registered library.'''
        key = None(win32con.HKEY_CLASSES_ROOT, 'Typelib')
        iids = EnumKeys(key)
        results = []
        for None in iids:
            if ():
                
                try:
                    pass

                for None in EnumKeys(key2):
                    if ():
                        if len(major_minor) < 2:
                            pass
                        major_minor[0] = version.split('.', 1)
                        minor = major_minor[1]
                        key3 = None(key2, str(version))
                        
                        try:
                            flags = win32api.RegQueryValue(None(key3, 'FLAGS'))
                        except (win32api.error, ValueError):
                            ()
                            flags = 0

                        if not flags & excludeFlags == 0:
                            continue
                    for None in EnumKeys(key3):
                        if ():
                            
                            try:
                                pass
                            except ValueError:
                                win32api.RegOpenKey

                            
                            try:
                                None(key3, f'''{lcid}\\win32''') = win32api.RegOpenKey
                            except win32api.error:
                                
                                try:
                                    key4 = None(key3, f'''{lcid}\\win64''')
                                except win32api.error:
                                    pass


                            
                            try:
                                (dll, typ) = None(key4, None)
                                if typ == win32con.REG_EXPAND_SZ:
                                    pass
                                dll = None(dll)
                            except win32api.error:
                                ()
                                dll = None

                            spec = TypelibSpec(iid, lcid, major, minor, flags)
                            spec.dll = dll
                            spec.desc = tlbdesc
                            spec.ver_desc = tlbdesc + ' (' + version + ')'
                            continue
                            continue
                            ()
                            continue
                            ()
                            return results
                        if win32api.error:
                            ()
                            continue


def FindTlbsWithDescription(desc):
    '''Find all installed type libraries with the specified description'''
    ret = []
    items = EnumTlbs()
    for item in items:
        if not item.desc == desc:
            continue
        ret.append(item)
    return ret

if (lambda title, excludeFlags: import pywin.dialogs.list as pywinitems = EnumTlbs(excludeFlags)for i in items:
i.major = int(i.major, 16)i.minor = int(i.minor, 16)items.sort()rc = pywin.dialogs.list.SelectFromLists(title, items, [
'Type Library'])if rc:
passNoneitems[rc]):
    
    def SelectTlb(title, excludeFlags):
        '''Display a list of all the type libraries, and select one.   Returns None if cancelled'''
        import pywin.dialogs.list as pywin
        items = EnumTlbs(excludeFlags)
        for i in items:
            i.major = int(i.major, 16)
            i.minor = int(i.minor, 16)
        items.sort()
        rc = pywin.dialogs.list.SelectFromLists(title, items, [
            'Type Library'])
        if rc:
            pass
        return None
        return items[rc]

if __name__ == '__main__':
    SelectTlb(None().__dict__)
return None
