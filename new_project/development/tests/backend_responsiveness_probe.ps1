param([string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
$tokens=$null;$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($Source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'launcher parse failed'}
$wanted=@('Wait-BackendLineTask','Send-Backend','Refresh-HwpDocumentStatus')
foreach($definition in $ast.FindAll({param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -in $wanted},$true)){
    . ([scriptblock]::Create($definition.Extent.Text))
}
# No real windows, HWP processes, or profile data are opened by this probe.
$dispatcher=[System.Windows.Threading.Dispatcher]::CurrentDispatcher
$pending=[System.Threading.Tasks.TaskCompletionSource[string]]::new()
$script:TickCount=0;$script:DuplicateRejected=$false
$script:BackendRequestInFlight=$true
$LayoutPreview=$true
$inputTimer=[System.Windows.Threading.DispatcherTimer]::new()
$inputTimer.Interval=[TimeSpan]::FromMilliseconds(25)
$inputTimer.Add_Tick({
    $script:TickCount++
    try{[void](Send-Backend @{action='connect'})}catch{$script:DuplicateRejected=$true}
    # Polling must not send another backend request during the pending read.
    Refresh-HwpDocumentStatus
    if($script:TickCount -ge 3){$pending.TrySetResult('selected-block-ready')|Out-Null}
})
try{
    $inputTimer.Start()
    $value=Wait-BackendLineTask -ReadTask $pending.Task -TimeoutMilliseconds 2000 -Context 'responsive probe'
}finally{$inputTimer.Stop()}
if($value -ne 'selected-block-ready' -or $script:TickCount -lt 3){throw 'dispatcher did not handle events while waiting'}
if(-not $script:DuplicateRejected){throw 'duplicate request was not rejected'}
$empty=[System.Threading.Tasks.TaskCompletionSource[string]]::new()
$timedOut=$false
try{[void](Wait-BackendLineTask -ReadTask $empty.Task -TimeoutMilliseconds 100 -Context 'timeout probe')}
catch [System.TimeoutException]{$timedOut=$true}
if(-not $timedOut){throw 'pending read did not time out'}
'BACKEND_RESPONSIVE_OK'
