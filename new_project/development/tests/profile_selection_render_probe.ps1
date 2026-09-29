param([string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
. $Source
$global:Status=[System.Windows.Controls.TextBlock]::new()
function global:Show-Error($Message){throw $Message}
function global:Send-Backend($Command){
    if($Command.action -ne 'user_profile_selection_analyze'){throw 'Unexpected request'}
    return [pscustomobject]@{ok=$true;draft_id='test';candidates=@(1..12|ForEach-Object{
        [pscustomobject]@{candidate_id="row$_";field_path="연구자 > 항목 $_";value="시험 값 $_";recommended=$true}
    })}
}
$global:RenderProbeWindow=$null
$global:Rendered=$false
function New-ProfileToolWindow($Title,$OwnerWindow){
    $dialog=[System.Windows.Window]::new();$dialog.Title='Profile render self-test';$dialog.Width=980;$dialog.Height=680
    $dialog.ShowInTaskbar=$false;$dialog.Opacity=0
    $global:RenderProbeWindow=$dialog
    $dialog.Add_ContentRendered({$global:Rendered=$true})
    return $dialog
}
$timer=[System.Windows.Threading.DispatcherTimer]::new()
$timer.Interval=[TimeSpan]::FromMilliseconds(100)
$clock=[Diagnostics.Stopwatch]::StartNew()
$timer.Add_Tick({
    if($global:RenderProbeWindow -and ($global:Rendered -or $clock.ElapsedMilliseconds -gt 3000)){
        $global:RenderProbeWindow.Close()
    }
})
try{
    $timer.Start()
    Open-ProfileSelectionImport $null
    if(-not $global:Rendered){throw 'Result dialog never rendered'}
    $grid=@($global:RenderProbeWindow.Content.Children|Where-Object{$_ -is [System.Windows.Controls.DataGrid]})[0]
    if($grid.Items.Count -ne 12){throw 'Wrong row count'}
    if($null -eq $grid.ItemContainerGenerator.ContainerFromIndex(0)){throw 'No rendered row'}
    Write-Output "PROFILE_RENDER_OK rows=12 elapsed_ms=$($clock.ElapsedMilliseconds)"
}finally{$timer.Stop();$clock.Stop()}
