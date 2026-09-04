param(
    [string]$DllPath = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot

if ([string]::IsNullOrWhiteSpace($DllPath)) {
    $DllPath = Join-Path $projectRoot "runtime\HwpAutomation\FilePathCheckerModuleExample.dll"
}

if (-not (Test-Path -LiteralPath $DllPath -PathType Leaf)) {
    throw "Security module DLL not found: $DllPath`nCopy FilePathCheckerModuleExample.dll from Hancom's official Automation security-module ZIP to this location."
}

$resolvedDll = (Resolve-Path -LiteralPath $DllPath).Path
$moduleKey = "HKCU:\Software\HNC\HwpAutomation\Modules"
$usesKey = Join-Path $moduleKey "Uses"
$moduleName = "FilePathCheckerModuleExample"

New-Item -Path $moduleKey -Force | Out-Null
New-ItemProperty `
    -Path $moduleKey `
    -Name $moduleName `
    -PropertyType String `
    -Value $resolvedDll `
    -Force | Out-Null

New-Item -Path $usesKey -Force | Out-Null
New-ItemProperty `
    -Path $usesKey `
    -Name $moduleName `
    -PropertyType DWord `
    -Value 1 `
    -Force | Out-Null

$registeredPath = (Get-ItemProperty -Path $moduleKey -Name $moduleName).$moduleName
$enabled = (Get-ItemProperty -Path $usesKey -Name $moduleName).$moduleName

Write-Host "HWP Automation security module registration completed."
Write-Host "Name: $moduleName"
Write-Host "DLL : $registeredPath"
Write-Host "Uses: $enabled"
