param([switch]$Apply)

# Preview by default. Only allowlisted generated files are removed, after a
# byte-for-byte verified ZIP backup. Never clean arbitrary *.pyc or user data.
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$repoPrefix = $repoRoot.TrimEnd('\') + '\'
$candidates = [Collections.Generic.List[object]]::new()

function Assert-ProjectPath([string]$Path) {
    $absolute = [IO.Path]::GetFullPath($Path)
    if (-not $absolute.StartsWith($repoPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Outside project: $absolute"
    }
    # Refuse junctions/symlinks anywhere along the path.
    $cursor = $absolute
    while ($cursor -ne $repoRoot) {
        if (Test-Path -LiteralPath $cursor) {
            $item = Get-Item -LiteralPath $cursor -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Reparse point is not a cleanup target: $cursor"
            }
        }
        $cursor = [IO.Path]::GetDirectoryName($cursor)
    }
    return $absolute
}

function Add-Candidate([IO.FileInfo]$File, [string]$Reason) {
    $absolute = Assert-ProjectPath $File.FullName
    $candidates.Add([pscustomobject]@{
        Path = $absolute
        RelativePath = $absolute.Substring($repoPrefix.Length).Replace('\','/')
        Reason = $Reason
        Bytes = $File.Length
    })
}

$cacheRoots = @('new_project/src', 'new_project/development/tests',
    'new_project/development/tools', 'new_project/__pycache__', 'recovered', 'tools')
foreach ($relative in $cacheRoots) {
    $folder = Assert-ProjectPath (Join-Path $repoRoot $relative)
    if (-not (Test-Path -LiteralPath $folder)) { continue }
    foreach ($file in Get-ChildItem -LiteralPath $folder -File -Recurse -Force) {
        if ($file.Directory.Name -ne '__pycache__') { continue }
        if ($file.Name -notmatch '^(.+)\.cpython-\d+(?:\.opt-\d+)?\.pyc$') { continue }
        $sourceName = $Matches[1] + '.py'
        $sourcePath = Join-Path $file.Directory.Parent.FullName $sourceName
        if (Test-Path -LiteralPath $sourcePath -PathType Leaf) {
            Add-Candidate $file 'regenerable_python_cache_with_existing_source'
        }
    }
}

$previewRoot = Assert-ProjectPath (Join-Path $repoRoot 'tmp/pdfs')
if (Test-Path -LiteralPath $previewRoot) {
    foreach ($file in Get-ChildItem -LiteralPath $previewRoot -File -Recurse) {
        $relative = $file.FullName.Substring($previewRoot.Length+1).Replace('\','/')
        if ($relative -match '^(font-flow-v[12]|polish-v[12]|uniform-fonts-v[12]|word-wrap-(v1|final))(-\d{2})?\.(png|pdf)$' -or
            $relative -match '^bd075e52-review/page-\d{2}\.png$') {
            Add-Candidate $file 'temporary_document_render_preview'
        }
    }
}
$demo = Assert-ProjectPath (Join-Path $repoRoot '.codex_score_demo.py')
if (Test-Path -LiteralPath $demo -PathType Leaf) {
    Add-Candidate (Get-Item -LiteralPath $demo) 'obsolete_one_off_demo_with_old_absolute_workspace_path'
}

$summary = [ordered]@{
    Mode = $(if ($Apply) { 'apply' } else { 'preview_only' })
    Files = $candidates.Count
    Bytes = ($candidates | Measure-Object Bytes -Sum).Sum
    Groups = @($candidates | Group-Object Reason | ForEach-Object {
        [pscustomobject]@{Reason=$_.Name; Files=$_.Count; Bytes=($_.Group | Measure-Object Bytes -Sum).Sum}
    })
}
if (-not $Apply -or -not $candidates.Count) {
    $summary | ConvertTo-Json -Depth 5
    exit 0
}

$backupRoot = Assert-ProjectPath (Join-Path $repoRoot ('system_backups/cleanup-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')))
New-Item -ItemType Directory -Path $backupRoot | Out-Null
$archivePath = Join-Path $backupRoot 'removed-files.zip'
$manifestPath = Join-Path $backupRoot 'manifest.json'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$manifest = @($candidates | ForEach-Object {
    [pscustomobject]@{RelativePath=$_.RelativePath; Reason=$_.Reason; Bytes=$_.Bytes;
        SHA256=(Get-FileHash -LiteralPath $_.Path -Algorithm SHA256).Hash; Status='pending'}
})
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8
$archive = [IO.Compression.ZipFile]::Open($archivePath, [IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($entry in $candidates) {
        [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $entry.Path, $entry.RelativePath, [IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
} finally { $archive.Dispose() }

# Verify every archived file BEFORE deleting any file.
$archive = [IO.Compression.ZipFile]::OpenRead($archivePath)
try {
    foreach ($entry in $manifest) {
        $saved = $archive.GetEntry($entry.RelativePath)
        if ($null -eq $saved -or $saved.Length -ne $entry.Bytes) { throw "Backup mismatch: $($entry.RelativePath)" }
        $stream = $saved.Open()
        $sha = [Security.Cryptography.SHA256]::Create()
        try { $hash = [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','') }
        finally { $sha.Dispose(); $stream.Dispose() }
        if ($hash -ne $entry.SHA256) { throw "Backup hash mismatch: $($entry.RelativePath)" }
    }
} finally { $archive.Dispose() }

foreach ($entry in $manifest) {
    $path = Assert-ProjectPath (Join-Path $repoRoot $entry.RelativePath)
    try {
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $entry.SHA256) {
            $entry.Status = 'preserved_changed_since_backup'
            continue
        }
        # Exact file only; no wildcard, recursive deletion, or shell handoff.
        Remove-Item -LiteralPath $path -Force
        $entry.Status = 'removed_with_verified_backup'
    } catch {
        $entry.Status = 'preserved_delete_failed: ' + $_.Exception.Message
    }
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8
$summary.Backup = $backupRoot
$summary.Removed = @($manifest | Where-Object Status -eq 'removed_with_verified_backup').Count
$summary.Preserved = @($manifest | Where-Object Status -ne 'removed_with_verified_backup').Count
$summary | ConvertTo-Json -Depth 5
