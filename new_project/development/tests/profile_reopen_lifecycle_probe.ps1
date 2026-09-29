param([string]$Source)
$ErrorActionPreference='Stop'
# This legacy probe isolates nested modal editor lifetime. Modeless windows have a separate probe.
function Test-WorkspaceWindow($Key){return $false}
function Show-WorkspaceWindow($Dialog,$Key){[void]$Dialog.ShowDialog()}
Add-Type -AssemblyName PresentationFramework
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class ProfileLifecycleNative {
    [DllImport("user32.dll")] public static extern bool IsWindowEnabled(IntPtr hwnd);
}
'@
# Real launcher initialization; no backend, login or HWP is started.
$text=Get-Content -LiteralPath $Source -Raw -Encoding UTF8
$start=$text.IndexOf('[xml]$Xaml = ')
if($start -lt 0){throw 'Window initialization not found'}
$end=$text.IndexOf('$script:WpfApplication.Add_DispatcherUnhandledException', $start)
Invoke-Expression $text.Substring($start,$end-$start)
$Window.Opacity=0;$Window.ShowInTaskbar=$false
$dispatcher=$Window.Dispatcher
$script:Probe=@{Cycles=0;Loaded=0;Editors=0;Failure=$null}
function Send-Backend($Command){
    switch($Command.action){
        user_profile_selection_analyze {return [pscustomobject]@{ok=$true;draft_id='test';candidates=@([pscustomobject]@{candidate_id='one';field='name';value='test';recommended=$true})}}
        user_profile_selection_save {return [pscustomobject]@{ok=$true;message='test saved'}}
        user_profile_get {return [pscustomobject]@{ok=$true;values=@{};field_groups=@([pscustomobject]@{id='one';name='name';path='name';parent_id='';aliases=@();values=@('test');default='test'})}}
        default {throw "Unexpected request: $($Command.action)"}
    }
}
function Show-Error($Message){throw $Message}
function Write-GuiRuntimeError($Context,$Failure){}
. (Join-Path (Split-Path -Parent $Source) 'profile_table_ui.ps1')
$factory=${function:New-ProfileToolWindow}
function New-ProfileToolWindow($Title,$OwnerWindow){
    $result=& $factory $Title $OwnerWindow
    $result.Opacity=0;$result.ShowInTaskbar=$false
    $result.Add_Loaded({param($sender,$event)
        if($event.OriginalSource -ne $sender){return}
        $script:Probe.Loaded++
        $closeTimer=[System.Windows.Threading.DispatcherTimer]::new()
        $closeTimer.Interval=[TimeSpan]::FromMilliseconds(100);$closeTimer.Tag=$sender
        $closeTimer.Add_Tick({param($tickSender,$tickEvent)
            $tickSender.Stop();$testWindow=$tickSender.Tag
            try{
                if($testWindow.Content -is [System.Windows.Controls.StackPanel]){
                    # Real nested text editor, cancelled without saving.
                    $testWindow.Close();return
                }
                if($testWindow.Content.Children[1] -is [System.Windows.Controls.Button]){
                    $testWindow.Content.Children[1].RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))
                }else{
                    $null=Read-ProfileTableText $testWindow 'test editor' 'example'
                    $script:Probe.Editors++
                    $testWindow.Close()
                }
            }catch{$script:Probe.Failure=$_;$testWindow.Close()}
        })
        $closeTimer.Start()
    })
    return $result
}
# Separate actions across dispatcher turns to expose queued shutdown after close.
$cycleTimer=[System.Windows.Threading.DispatcherTimer]::new()
$cycleTimer.Interval=[TimeSpan]::FromMilliseconds(150)
$cycleTimer.Add_Tick({
    $cycleTimer.Stop()
    try{
        if($script:Probe.Cycles -ge 12){$Window.Close();return}
        $before=$script:Probe.Loaded
        if($script:Probe.Cycles % 2 -eq 0){Open-ProfileDataTable $Window}else{Open-ProfileSelectionImport $Window}
        if($null -ne $script:Probe.Failure){throw $script:Probe.Failure}
        if($script:Probe.Loaded -le $before){throw 'A reopened dialog never became visible'}
        $handle=[System.Windows.Interop.WindowInteropHelper]::new($Window).Handle
        if(-not [ProfileLifecycleNative]::IsWindowEnabled($handle)){throw 'Main window input remained disabled'}
        if($dispatcher.HasShutdownStarted){throw 'Dispatcher shut down after review close'}
        if(@($script:WpfApplication.Windows) -notcontains $Window){throw 'Main window missing from application ownership'}
        if($script:WpfApplication.MainWindow -ne $Window){throw 'Application main window changed to an editor'}
        $script:Probe.Cycles++
        $cycleTimer.Start()
    }catch{$script:Probe.Failure=$_;$Window.Close()}
})
$Window.Add_Loaded({$cycleTimer.Start()})
try {
    [void]$Window.ShowDialog()
    if($null -ne $script:Probe.Failure){throw $script:Probe.Failure}
    if($script:Probe.Cycles -ne 12 -or $script:Probe.Editors -ne 6 -or $script:Probe.Loaded -ne 18){throw 'Incomplete lifecycle coverage'}
    'WINDOW_LIFECYCLE_OK: 12 dialogs, 6 nested editors, main input enabled after every close'
} finally {
    $cycleTimer.Stop();$Window.Close()
    if(-not $dispatcher.HasShutdownStarted){$script:WpfApplication.Shutdown()}
}
