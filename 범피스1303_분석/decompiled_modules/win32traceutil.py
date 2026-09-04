# Source Generated with Decompyle++
# File: win32traceutil.marshal (Python 3.13)

import win32trace

def RunAsCollector():
    import sys
    
    try:
        import win32api
        win32api.SetConsoleTitle('Python Trace Collector')
    except:
        pass

    None()
    print('Collecting Python Trace Output...')
    
    try:
        win32trace.blockingread(None(500))
        continue
    except KeyboardInterrupt:
        print('Ctrl+C')



def SetupForPrint():
    None()
    
    try:
        print('Redirecting output to win32trace remote collector')
    except:
        pass

    None()

if __name__ == '__main__':
    None()
return None
None()
