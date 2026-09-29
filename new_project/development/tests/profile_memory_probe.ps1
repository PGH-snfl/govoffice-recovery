param([string]$Project, [ValidateSet('profile','wait','tabs')][string]$Mode='profile')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
$script:ProbeWindows=[System.Collections.Generic.List[System.WeakReference]]::new()
$script:ProbeClock=[System.Diagnostics.Stopwatch]::StartNew()
function Check-Budget {
    if($script:ProbeClock.Elapsed.TotalSeconds -gt 20){throw 'Probe time budget exceeded'}
    if([Diagnostics.Process]::GetCurrentProcess().PrivateMemorySize64 -gt 400MB){throw 'Probe memory budget exceeded'}
}
function Measure-Probe([int]$Count){
    # WPF queues cleanup/binding work. Drain it before testing reachability,
    # otherwise a pending dispatcher operation can look like a memory leak.
    $frame=[System.Windows.Threading.DispatcherFrame]::new()
    $drain=[System.Windows.Threading.DispatcherTimer]::new([System.Windows.Threading.DispatcherPriority]::ApplicationIdle)
    $drain.Interval=[TimeSpan]::FromMilliseconds(5);$drain.Tag=$frame
    $drain.Add_Tick({param($sender,$eventArgs) $sender.Stop();$sender.Tag.Continue=$false})
    try{$drain.Start();[System.Windows.Threading.Dispatcher]::PushFrame($frame)}finally{$drain.Stop()}
    [GC]::Collect();[GC]::WaitForPendingFinalizers();[GC]::Collect()
    $p=[Diagnostics.Process]::GetCurrentProcess()
    [pscustomobject]@{Iterations=$Count;PrivateMB=[math]::Round($p.PrivateMemorySize64/1MB,2);WorkingMB=[math]::Round($p.WorkingSet64/1MB,2);ManagedMB=[math]::Round([GC]::GetTotalMemory($false)/1MB,2);RetainedObjects=@($script:ProbeWindows|Where-Object IsAlive).Count;Handles=$p.HandleCount}
}
if($Mode -eq 'profile'){
    function Write-GuiRuntimeError($Context,$Failure){}
    function Send-Backend($Command){
        if($Command.action -ne 'user_profile_selection_analyze'){throw 'Unexpected request'}
        return [pscustomobject]@{ok=$true;draft_id='synthetic';candidates=@(1..12|ForEach-Object{
            [pscustomobject]@{candidate_id="test_$_";field="field_$_";value="example_$_";recommended=$true}
        })}
    }
    # Use production construction, binding and handlers, but NEVER ShowDialog.
    $sourceText=Get-Content -LiteralPath (Join-Path $Project 'profile_table_ui.ps1') -Raw -Encoding UTF8
    $sourceText=$sourceText.Replace('[void]$dialog.ShowDialog()', '& $global:ProfileMemoryDialogProbe')
    Invoke-Expression $sourceText
    $global:ProfileMemoryDialogProbe={
        $table.Measure([System.Windows.Size]::new(900,500))
        $table.Arrange([System.Windows.Rect]::new(0,0,900,500));$table.UpdateLayout()
        $script:ProbeWindows.Add([System.WeakReference]::new($dialog))
        $dialog.Close()
    }
    function Invoke-ProbeIteration {Open-ProfileSelectionImport $null}
}elseif($Mode -eq 'tabs'){
    $tokens=$null;$errors=$null
    $ast=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $Project 'launch_gui.ps1'),[ref]$tokens,[ref]$errors)
    if($errors.Count){throw 'Launcher parse failed'}
    $wanted=@('Render-Tab','Resolve-Icon','New-ImageButton','Set-OriginalFlatButton','Get-PurpleButtonTemplate')
    foreach($definition in $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -in $wanted},$true)){
        . ([scriptblock]::Create($definition.Extent.Text))
    }
    $Assets=Join-Path ([IO.Path]::GetFullPath($Project)) 'assets/icons'
    $Content=[System.Windows.Controls.Canvas]::new()
    $Status=[System.Windows.Controls.TextBlock]::new();$NavButtons=@{}
    $layout=Get-Content -LiteralPath (Join-Path $Project 'config/original_layout.json') -Raw -Encoding UTF8|ConvertFrom-Json
    $TabMap=@{};foreach($tab in $layout.tabs){$TabMap[$tab.id]=$tab}
    $script:ProbeTabNames=@($layout.tabs|ForEach-Object id|Where-Object{$_ -ne '개인'})
    $script:ProbeTabIndex=0
    function Invoke-ProbeIteration {
        Render-Tab $script:ProbeTabNames[$script:ProbeTabIndex % $script:ProbeTabNames.Count]
        $script:ProbeTabIndex++
        $Content.Measure([System.Windows.Size]::new(300,400))
        $Content.Arrange([System.Windows.Rect]::new(0,0,300,400));$Content.UpdateLayout()
        foreach($control in $Content.Children){$script:ProbeWindows.Add([System.WeakReference]::new($control))}
        $Content.Children.Clear()
    }
}else{
    $tokens=$null;$errors=$null
    $ast=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $Project 'launch_gui.ps1'),[ref]$tokens,[ref]$errors)
    if($errors.Count){throw 'Launcher parse failed'}
    $definition=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Wait-BackendLineTask'},$true)
    . ([scriptblock]::Create($definition.Extent.Text))
    Add-Type -TypeDefinition @'
using System.Threading.Tasks;
public static class MemoryProbeReply {
    public static async Task<string> Pending() {
        await Task.Delay(5).ConfigureAwait(false);
        return "synthetic";
    }
}
'@
    [void][System.Windows.Threading.Dispatcher]::CurrentDispatcher
    function Invoke-ProbeIteration {
        $result=Wait-BackendLineTask -ReadTask ([MemoryProbeReply]::Pending()) -TimeoutMilliseconds 2000 -Context 'memory probe'
        if($result -ne 'synthetic'){throw 'Bad reply'}
    }
}
$snapshots=@(Measure-Probe 0)
for($i=1;$i -le 30;$i++){
    Check-Budget
    Invoke-ProbeIteration
    if($i -in @(5,10,20,30)){$snapshots+=Measure-Probe $i}
}
[pscustomobject]@{Mode=$Mode;ActualWindowShown=$false;HwpConnected=$false;Samples=$snapshots} | ConvertTo-Json -Depth 4
