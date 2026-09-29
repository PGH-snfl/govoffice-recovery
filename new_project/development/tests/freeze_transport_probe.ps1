param([string]$Source,[string]$Python)
$ErrorActionPreference='Stop'
$tokens=$null;$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($Source,[ref]$tokens,[ref]$errors)
$wanted=@('ConvertTo-AsciiJson','Get-BackendRequestTimeout','Wait-BackendLineTask','Read-BackendLine','Send-Backend')
foreach($definition in $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -in $wanted},$true)){
    . ([scriptblock]::Create($definition.Extent.Text))
}
# Own disposable child only: reproduce redirected-stderr backpressure, with no
# COM, application windows, profile writes or user documents.
$info=[System.Diagnostics.ProcessStartInfo]::new()
$info.FileName=$Python
$info.Arguments='-c "import sys; sys.stderr.write(''x''*262144); sys.stderr.flush(); print(''READY'', flush=True)"'
$info.UseShellExecute=$false;$info.CreateNoWindow=$true
$info.RedirectStandardOutput=$true;$info.RedirectStandardError=$true
$child=[System.Diagnostics.Process]::Start($info)
try{
    $read=$child.StandardOutput.ReadLineAsync()
    $blocked=$false
    try{[void](Wait-BackendLineTask $read 500 'stderr probe')}catch [System.TimeoutException]{$blocked=$true}
    if(-not $blocked){throw 'Expected stderr backpressure was not reproduced'}
    $drain=$child.StandardError.ReadToEndAsync()
    $ready=Wait-BackendLineTask $read 3000 'drained stderr probe'
    if($ready -ne 'READY'){throw 'Draining stderr did not restore response'}
    if(-not $child.WaitForExit(3000)){throw 'Test child did not exit'}
    'STDERR_BACKPRESSURE_CONFIRMED: blocked until stderr was drained'
}finally{
    if(-not $child.HasExited){$child.Kill();[void]$child.WaitForExit(2000)}
    $child.Dispose()
}
# Simulate a timed-out call through the production request state machine.
$sink=[System.IO.StringWriter]::new()
$script:Backend=[pscustomobject]@{HasExited=$false;StandardInput=$sink}
$script:BackendUnhealthy=$false;$script:BackendRequestInFlight=$false;$LayoutPreview=$false
function Read-BackendLine {throw [System.TimeoutException]::new('Synthetic timeout')}
function Stop-BackendProcess {$script:Backend=$null;return $true}
try{[void](Send-Backend @{action='hwp_document_status'})}catch{}
if(-not $script:BackendUnhealthy){throw 'Expected unhealthy state missing'}
$blockedActions=@()
foreach($action in @('user_profile_get','user_profile_table_mutate','connect')){
    try{[void](Send-Backend @{action=$action});throw 'Request unexpectedly allowed'}
    catch{if($_.Exception.Message -eq 'Request unexpectedly allowed'){throw};$blockedActions+=$action}
}
if($script:BackendRequestInFlight){throw 'Request flag leaked'}
'GLOBAL_TIMEOUT_LOCK_CONFIRMED: '+($blockedActions -join ', ')
