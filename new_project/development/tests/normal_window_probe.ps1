param([string]$Project=(Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
function Assert($Condition,$Message){if(-not $Condition){throw $Message}}
$source=Get-Content -LiteralPath (Join-Path $Project 'launch_gui.ps1') -Raw -Encoding UTF8
$tokens=$null;$errors=$null
[void][System.Management.Automation.Language.Parser]::ParseInput($source,[ref]$tokens,[ref]$errors)
Assert ($errors.Count -eq 0) 'Launcher parse failed'
$markup=[regex]::Match($source,"(?s)\[xml\]\`$Xaml = @'\r?\n(.*?)\r?\n'@").Groups[1].Value
Assert ($markup.Length -gt 0) 'Main window markup not found'
# Construct only; no Show/ShowDialog, HWP connection or mouse input.
$window=[System.Windows.Markup.XamlReader]::Parse($markup)
try{
    Assert (-not $window.Topmost) 'Main window is still always-on-top'
    Assert $window.ShowInTaskbar 'Main window missing from taskbar'
    Assert ($window.WindowStyle -eq 'SingleBorderWindow') 'Native title bar missing'
    Assert ($window.ResizeMode -eq 'CanMinimize') 'Native minimize button missing'
    Assert ($null -ne $window.FindName('MainViewbox')) 'Content scaling lost'
}finally{$window.Close()}
$native=[regex]::Match($source,"(?s)Add-Type -TypeDefinition @'\r?\n(.*?)\r?\n'@").Groups[1].Value
Assert ($native.Length -gt 0) 'Native helpers not found'
Add-Type -TypeDefinition $native
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class GovOfficeIdentityProbe {
    [DllImport("shell32.dll")]
    private static extern int GetCurrentProcessExplicitAppUserModelID(out IntPtr value);
    public static string Read() {
        IntPtr value;
        Marshal.ThrowExceptionForHR(GetCurrentProcessExplicitAppUserModelID(out value));
        try { return Marshal.PtrToStringUni(value); }
        finally { Marshal.FreeCoTaskMem(value); }
    }
}
'@
# Identity applies to this disposable test process only, with no registry writes.
[GovOfficeWindowIdentity]::Initialize()
Assert ([GovOfficeIdentityProbe]::Read() -eq 'GovOffice.Desktop') 'Taskbar identity not applied'
Assert ($source.IndexOf('[GovOfficeWindowIdentity]::Initialize()') -lt $source.IndexOf('[xml]$Xaml')) 'Identity applied too late'
'NORMAL_WINDOW_OK: native titlebar, taskbar, minimize, non-topmost, app identity'
