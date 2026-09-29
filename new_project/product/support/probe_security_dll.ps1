param([Parameter(Mandatory=$true)][string]$DllPath)
$ErrorActionPreference = 'Stop'
try {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class GovOfficeDllProbe {
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    public static extern IntPtr LoadLibraryEx(string path, IntPtr file, uint flags);
    [DllImport("kernel32.dll", CharSet=CharSet.Ansi, ExactSpelling=true, SetLastError=true)]
    public static extern IntPtr GetProcAddress(IntPtr module, string name);
    [DllImport("kernel32.dll")]
    public static extern bool FreeLibrary(IntPtr module);
}
'@
    $module = [GovOfficeDllProbe]::LoadLibraryEx([IO.Path]::GetFullPath($DllPath), [IntPtr]::Zero, 8)
    if ($module -eq [IntPtr]::Zero) { throw "LoadLibrary error $([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
    try {
        if ([GovOfficeDllProbe]::GetProcAddress($module, 'IsAccessiblePath') -eq [IntPtr]::Zero) { throw 'IsAccessiblePath export missing' }
        Write-Output 'DLL_OK'
    } finally { [void][GovOfficeDllProbe]::FreeLibrary($module) }
} catch { Write-Output $_.Exception.Message; exit 1 }
