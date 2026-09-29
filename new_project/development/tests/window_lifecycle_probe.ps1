param([string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
# Run the production initialization order in an isolated WPF process.
$text=Get-Content -LiteralPath $Source -Raw -Encoding UTF8
$start=$text.IndexOf('[xml]$Xaml = ')
if($start -lt 0){throw 'Window initialization not found'}
$end=$text.IndexOf('$script:WpfApplication.Add_DispatcherUnhandledException', $start)
Invoke-Expression $text.Substring($start,$end-$start)
$dispatcher=$Window.Dispatcher
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
# Instrument only the test window factory. Keep production ShowDialog and save
# handlers intact, including their nested dispatcher loops.
$factory=${function:New-ProfileToolWindow}
function New-ProfileToolWindow($Title,$OwnerWindow){
    $result=& $factory $Title $OwnerWindow
    $result.Add_ContentRendered({param($sender,$event)
        if($sender.Content.Children[1] -is [System.Windows.Controls.Button]){
            $saveButton=$sender.Content.Children[1]
            $saveButton.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))
        }else{$sender.Close()}
    })
    return $result
}
$script:cycles=0
$Window.Add_ContentRendered({
    for($i=0;$i -lt 3;$i++){
        Open-ProfileSelectionImport $Window
        Open-ProfileDataTable $Window
        if($dispatcher.HasShutdownStarted){throw 'Dispatcher shut down after review close'}
        $script:cycles++
    }
    $Window.Close()
})
try {
    [void]$Window.ShowDialog()
    if($script:cycles -ne 3){throw "Only $script:cycles cycles completed"}
    'WINDOW_LIFECYCLE_OK'
} finally {
    $Window.Close()
    if(-not $dispatcher.HasShutdownStarted){$script:WpfApplication.Shutdown()}
}
