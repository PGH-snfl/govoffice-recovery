param([switch]$NoLaunch, [switch]$OfflineCheck, [string]$InstallRoot = '')
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
try {
    $Source = Join-Path $PSScriptRoot 'app'
    if (-not (Test-Path -LiteralPath (Join-Path $Source 'deployment.json'))) { throw '설치 파일이 누락되었습니다. ZIP 전체를 먼저 압축 해제하세요.' }
    $Manifest = Get-Content -LiteralPath (Join-Path $Source 'deployment.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $SourceFull = [IO.Path]::GetFullPath($Source).TrimEnd('\') + '\'
    foreach ($Entry in $Manifest.files.PSObject.Properties) {
        $File = [IO.Path]::GetFullPath((Join-Path $Source $Entry.Name))
        if (-not $File.StartsWith($SourceFull, [StringComparison]::OrdinalIgnoreCase)) { throw '설치 파일 경로가 올바르지 않습니다.' }
        if (-not (Test-Path -LiteralPath $File -PathType Leaf)) { throw "설치 파일 누락: $($Entry.Name)" }
        $Hasher = [Security.Cryptography.SHA256]::Create()
        $Stream = [IO.File]::OpenRead($File)
        try { $Hash = [BitConverter]::ToString($Hasher.ComputeHash($Stream)).Replace('-', '') }
        finally { $Stream.Dispose(); $Hasher.Dispose() }
        if ($Hash -ne $Entry.Value) { throw "설치 파일 손상: $($Entry.Name)" }
    }
    if (-not $InstallRoot) { $InstallRoot = Join-Path $env:LOCALAPPDATA 'Programs\GovOffice' }
    $Release = Join-Path ([IO.Path]::GetFullPath($InstallRoot)) ('releases\' + $Manifest.build + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
    [void][IO.Directory]::CreateDirectory($Release)
    foreach ($Entry in $Manifest.files.PSObject.Properties) {
        $Target = Join-Path $Release $Entry.Name
        [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Target))
        Copy-Item -LiteralPath (Join-Path $Source $Entry.Name) -Destination $Target
    }
    Copy-Item -LiteralPath (Join-Path $Source 'deployment.json') -Destination $Release
    $Python = Join-Path $Release 'runtime\python\python.exe'
    $CheckArgs = @((Join-Path $Release 'product\support\deployment_check.py'))
    if ($OfflineCheck) { $CheckArgs += '--offline' } else { $CheckArgs += '--register' }
    $Raw = & $Python @CheckArgs
    $CheckExit = $LASTEXITCODE
    $Report = ($Raw -join "`n") | ConvertFrom-Json
    foreach ($Item in $Report.checks) { Write-Host "$($Item.name): $($Item.detail)" }
    $ReportDir = if ($OfflineCheck) { $Release } else { Join-Path $env:LOCALAPPDATA 'GovOffice\logs' }
    [void][IO.Directory]::CreateDirectory($ReportDir)
    [IO.File]::WriteAllText((Join-Path $ReportDir 'installation-check.json'), ($Report | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
    if ($CheckExit -ne 0) { throw "프로그램 파일은 설치됐지만 실행 조건이 충족되지 않았습니다. 위 원인을 해결한 뒤 다시 설치하세요.`n위치: $Release" }
    if (-not $OfflineCheck) {
        $Shell = New-Object -ComObject WScript.Shell
        foreach ($Folder in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))) {
            $Shortcut = $Shell.CreateShortcut((Join-Path $Folder '범정부오피스.lnk'))
            $Shortcut.TargetPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
            $Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$(Join-Path $Release 'launch_gui.ps1')`""
            $Shortcut.WorkingDirectory = $Release
            $Shortcut.Description = '범정부오피스'
            $Shortcut.Save()
        }
    }
    Write-Host "설치 완료: $Release"
    if (-not $NoLaunch -and -not $OfflineCheck) {
        Start-Process -FilePath 'powershell.exe' -WindowStyle Hidden -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $Release 'launch_gui.ps1')`""
    }
} catch { Write-Host "설치 확인 필요: $($_.Exception.Message)" -ForegroundColor Red; exit 1 }
