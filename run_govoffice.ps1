# Windows PowerShell 5.1. Keep UTF-8 BOM when editing Korean file names.
[CmdletBinding()]
param(
    [string]$ProjectDir = '',
    [switch]$CheckOnly,
    [switch]$Help
)
$ErrorActionPreference = 'Stop'
if ($Help) {
    Write-Host 'run_govoffice.ps1 [-ProjectDir C:\work\govoffice] [-CheckOnly]'
    Write-Host 'Windows 64-bit + desktop Hancom HWP required. Existing checkout is not pulled.'
    exit 0
}
try {
    if ($env:OS -ne 'Windows_NT' -or -not [Environment]::Is64BitOperatingSystem) {
        throw 'Windows 64-bit is required (WPF + HWP COM).'
    }
    if ([string]::IsNullOrWhiteSpace($ProjectDir)) {
        if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'new_project\product\support\check_checkout.py')) {
            $ProjectDir = $PSScriptRoot
        } else {
            $ProjectDir = Join-Path $PSScriptRoot 'govoffice-recovery'
        }
    }
    $ProjectDir = [IO.Path]::GetFullPath($ProjectDir)
    if (-not (Test-Path -LiteralPath $ProjectDir)) {
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git for Windows, or extract the entire repository and use -ProjectDir.' }
        Write-Host "Downloading private repository to $ProjectDir"
        $HasGh = $false
        if (Get-Command gh -ErrorAction SilentlyContinue) {
            & gh auth status *> $null
            $HasGh = ($LASTEXITCODE -eq 0)
        }
        if ($HasGh) {
            & gh repo clone PGH-snfl/govoffice-recovery $ProjectDir -- --depth 1
        } else {
            & git clone --depth 1 https://github.com/PGH-snfl/govoffice-recovery.git $ProjectDir
        }
        if ($LASTEXITCODE -ne 0) { throw 'Clone failed. Check private repository access and Git authentication, or use a complete ZIP checkout.' }
    }
    $Python = Join-Path $ProjectDir '범피스1303_분석\python313\python.exe'
    $Check = Join-Path $ProjectDir 'new_project\product\support\check_checkout.py'
    $Gui = Join-Path $ProjectDir 'new_project\launch_gui.ps1'
    foreach ($Required in @($Python, $Check, $Gui)) {
        if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) { throw "Required file missing: $Required. Download the entire repository." }
    }
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location -LiteralPath $ProjectDir
    try {
        # Same checker as 시작전_점검.cmd, without that wrapper's pause prompt.
        & $Python -B $Check
        if ($LASTEXITCODE -ne 0) { throw 'Preflight failed. Read the checks above; the GUI was not started.' }
        if ($CheckOnly) { Write-Host 'Preflight passed. HWP document editing has not been tested.'; exit 0 }
        # Existing launcher handles its own elevation and WPF/backend lifecycle.
        $PowerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
        & $PowerShell -NoProfile -ExecutionPolicy Bypass -File $Gui
        if ($LASTEXITCODE -ne 0) { throw "GovOffice launcher exited with code $LASTEXITCODE" }
    } finally { Pop-Location }
} catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
}
