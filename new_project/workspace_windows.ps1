# Modeless workspace windows. Short confirmation/value dialogs remain modal.
$script:WorkspaceWindows=@{}
function Test-WorkspaceWindow([string]$Key) {
    $dialog=$script:WorkspaceWindows[$Key]
    if($null -eq $dialog -or -not $dialog.IsVisible){return $false}
    if($dialog.WindowState -eq 'Minimized'){$dialog.WindowState='Normal'}
    [void]$dialog.Activate();return $true
}
function Show-WorkspaceWindow($Dialog,[string]$Key) {
    if(Test-WorkspaceWindow $Key){$Dialog.Close();return}
    $windows=$script:WorkspaceWindows;$windows[$Key]=$Dialog
    $Dialog.Add_Closed({if($windows[$Key] -eq $Dialog){$windows.Remove($Key)}}.GetNewClosure())
    try{$Dialog.Show()}catch{if($windows[$Key] -eq $Dialog){$windows.Remove($Key)};throw}
}
function Add-WorkspaceClosedAction([string]$Key,[scriptblock]$Action) {
    $dialog=$script:WorkspaceWindows[$Key]
    if($null -ne $dialog){$dialog.Add_Closed({Invoke-WorkspaceClosedAction $Action}.GetNewClosure())}
}
function Invoke-WorkspaceClosedAction([scriptblock]$Action) {
    if($script:GuiClosing){return}
    try{& $Action}catch{Show-Error $_.Exception.Message}
}
