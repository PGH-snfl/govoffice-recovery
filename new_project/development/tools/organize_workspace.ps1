param([switch]$Apply)

# One-time workspace layout migration. Default: read-only preview.
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$repoPrefix = $repoRoot.TrimEnd('\') + '\'
$plan = @(
    @('범피스1303.exe', 'originals/범피스1303.exe'),
    @('범피스가이드북.pdf', 'originals/범피스가이드북.pdf'),
    @('예시 문서', 'materials/examples'),
    @('3. 제출서류 및 참고', 'materials/submission-reference'),
    @('첨부자료', 'materials/attachments'),
    @('AI 문서 작성 실검증 결과', 'materials/validation'),
    @('범피스 예시1.hwp', 'materials/examples/범피스 예시1.hwp'),
    @('범피스 예시2.hwp', 'materials/examples/범피스 예시2.hwp'),
    @('new_project/development/DESIGN_TABLE_PROTECTION.md', 'new_project/development/docs/DESIGN_TABLE_PROTECTION.md'),
    @('new_project/development/OUTPUT_POLISH.md', 'new_project/development/docs/OUTPUT_POLISH.md'),
    @('new_project/development/REVIEW_MEMOS.md', 'new_project/development/docs/REVIEW_MEMOS.md'),
    @('new_project/development/TEMPLATE_LAYOUT_DATABASE.md', 'new_project/development/docs/TEMPLATE_LAYOUT_DATABASE.md')
)

function Safe-Path([string]$Relative) {
    $absolute = [IO.Path]::GetFullPath((Join-Path $repoRoot $Relative))
    if (-not $absolute.StartsWith($repoPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target is outside workspace: $absolute"
    }
    $cursor = $absolute
    while ($cursor -ne $repoRoot) {
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Refusing reparse point: $cursor"
            }
        }
        $cursor = [IO.Path]::GetDirectoryName($cursor)
    }
    return $absolute
}

$pending = [Collections.Generic.List[object]]::new()
$inventory = [Collections.Generic.List[object]]::new()
foreach ($pair in $plan) {
    $source = Safe-Path $pair[0]
    $target = Safe-Path $pair[1]
    if (-not (Test-Path -LiteralPath $source)) {
        if (Test-Path -LiteralPath $target) { continue }
        throw "Neither source nor target exists: $source"
    }
    if (Test-Path -LiteralPath $target) { throw "Destination exists; never merge or overwrite: $target" }
    $item = Get-Item -LiteralPath $source -Force
    $files = if ($item.PSIsContainer) {
        $children = @(Get-ChildItem -LiteralPath $source -Recurse -Force)
        if (@($children | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
            throw "Source contains a reparse point: $source"
        }
        @($children | Where-Object { -not $_.PSIsContainer })
    } else { @($item) }
    foreach ($file in $files) {
        $suffix = if ($item.PSIsContainer) { '/' + $file.FullName.Substring($source.Length+1).Replace('\','/') } else { '' }
        $inventory.Add([pscustomobject]@{OldPath=$pair[0]+$suffix; NewPath=$pair[1]+$suffix;
            Bytes=$file.Length; SHA256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash})
    }
    $pending.Add([pscustomobject]@{Source=$source; Target=$target; OldPath=$pair[0]; NewPath=$pair[1]})
}
if (-not $Apply -or -not $pending.Count) {
    [pscustomobject]@{Mode='preview'; Moves=$pending.Count; Files=$inventory.Count; Plan=@($pending | Select-Object OldPath,NewPath)} | ConvertTo-Json -Depth 5
    exit 0
}
$journalDir = Safe-Path ('system_backups/directory-layout-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -Path $journalDir -ItemType Directory | Out-Null
$journalPath = Join-Path $journalDir 'manifest.json'
$journal = [ordered]@{Status='planned'; Files=@($inventory); Moves=@($pending | Select-Object OldPath,NewPath)}
$journal | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $journalPath -Encoding utf8
$completed = [Collections.Generic.List[object]]::new()
try {
    foreach ($move in $pending) {
        $source = Safe-Path $move.OldPath
        $target = Safe-Path $move.NewPath
        if (Test-Path -LiteralPath $target) { throw "Destination appeared: $target" }
        $parent = [IO.Path]::GetDirectoryName($target)
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -Path $parent -ItemType Directory | Out-Null }
        Move-Item -LiteralPath $source -Destination $target
        $completed.Add($move)
    }
    foreach ($entry in $inventory) {
        $target = Safe-Path $entry.NewPath
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -ne $entry.SHA256) {
            throw "Content mismatch after move: $target"
        }
    }
    $journal.Status = 'moved_and_hash_verified'
} catch {
    $failure = $_
    $rollbackFailures = [Collections.Generic.List[string]]::new()
    for ($i=$completed.Count-1; $i -ge 0; $i--) {
        $move = $completed[$i]
        try {
            $old = Safe-Path $move.OldPath
            $new = Safe-Path $move.NewPath
            if (Test-Path -LiteralPath $old) { throw "Old path appeared; refusing overwrite: $old" }
            Move-Item -LiteralPath $new -Destination $old
        } catch { $rollbackFailures.Add($_.Exception.Message) }
    }
    $journal.Status = 'failed_with_rollback_attempt'
    $journal.Error = $failure.Exception.Message
    $journal.RollbackErrors = @($rollbackFailures)
    throw $failure
} finally {
    $journal | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $journalPath -Encoding utf8
}
[pscustomobject]@{Status=$journal.Status; Moves=$pending.Count; Files=$inventory.Count; Manifest=$journalPath} | ConvertTo-Json
