param([string]$Project=(Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
Add-Type -Path (Join-Path $Project 'gui_poll_guard.cs') -ReferencedAssemblies @(
    [System.Windows.Window].Assembly.Location,[System.Windows.Media.Visual].Assembly.Location,
    [System.Windows.Threading.Dispatcher].Assembly.Location,'System.dll','System.Core.dll','System.Xaml.dll')
[GovOfficePollGuard]::Initialize()
[GovOfficePollGuard]::Initialize()
function Assert($condition,$message){if(-not $condition){throw $message}}
# Exercise the production message handler in memory only. No OS messages,
# windows, physical mouse actions, backend, HWP or user files are used.
$method=[GovOfficePollGuard].GetMethod('OnMessage',[Reflection.BindingFlags]'NonPublic,Static')
function Message([int]$Handle,[int]$Id){
    $argsForHook=[object[]]@([IntPtr]$Handle,$Id,[IntPtr]::Zero,[IntPtr]::Zero,$false)
    [void]$method.Invoke($null,$argsForHook)
    Assert (-not $argsForHook[4]) 'Window movement message was consumed'
}
$script:Calls=0
$handler=[GovOfficePollGuard]::Wrap([EventHandler]{$script:Calls++})
$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq 1) 'Normal polling disabled'
Message 100 0x0231
Message 100 0x0231
1..100 | ForEach-Object {$handler.Invoke($null,[EventArgs]::Empty)}
Assert ($script:Calls -eq 1 -and [GovOfficePollGuard]::IsMoving) 'Polling entered native drag loop'
Message 200 0x0231
Message 100 0x0232
$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq 1) 'Another moving window was ignored'
Message 200 0x0082
$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq 2 -and -not [GovOfficePollGuard]::IsMoving) 'Destroyed window left polling locked'
Message 300 0x0231
Message 300 0x0232
$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq 3) 'Polling did not resume after movement'
Message 999 0x0232
Assert (-not [GovOfficePollGuard]::IsMoving) 'Unmatched exit changed state'

$expected=@('$DocumentStatusTimer','$SelectionProbeTimer','$SelectionStateTimer','$ManualStateTimer','$Timer')
$found=@()
foreach($name in @('launch_gui.ps1','document_authoring_ui.ps1','document_authoring_flow_ui.ps1')){
    $tokens=$null;$errors=$null
    $ast=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $Project $name),[ref]$tokens,[ref]$errors)
    Assert ($errors.Count -eq 0) "Parse failed: $name"
    foreach($hook in $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.InvokeMemberExpressionAst] -and $n.Member.Value -eq 'Add_Tick'},$true)){
        if($hook.Expression.Extent.Text -in $expected){
            Assert ($hook.Arguments[0].Extent.Text.StartsWith('[GovOfficePollGuard]::Wrap(')) "Unguarded polling: $($hook.Expression)"
            $found+=$hook.Expression.Extent.Text
        }
    }
}
Assert (@($expected | Where-Object {$_ -notin $found}).Count -eq 0) 'Missing polling integration'
$before=$script:Calls;$first=[GovOfficePollGuard]::Pause();$second=[GovOfficePollGuard]::Pause()
$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq $before -and [GovOfficePollGuard]::IsPaused) 'Pause allowed a callback'
$first.Dispose();$first.Dispose();$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq $before -and [GovOfficePollGuard]::IsPaused) 'Nested/double disposal released another pause'
$second.Dispose();$handler.Invoke($null,[EventArgs]::Empty)
Assert ($script:Calls -eq $before+1 -and -not [GovOfficePollGuard]::IsPaused) 'Pause did not recover'
'WINDOW_POLL_GUARD_OK: 5 polling routes; 100 blocked ticks; move/resize/close recovery'
