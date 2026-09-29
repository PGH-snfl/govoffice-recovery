param([string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
function global:Set-OriginalFlatButton {}
function global:Show-Error($Message){throw $Message}
function global:Refresh-HwpDocumentStatus {}
$global:Status=[System.Windows.Controls.TextBlock]::new()
$global:FavoriteTest=[pscustomobject]@{items=@();calls=@();edits=0}
$global:FavoriteEntry=[pscustomobject]@{id='entry';name='Example';category='Table';operations=@([pscustomobject]@{type='method';method='Size';args=@(11)})}
function global:Send-Backend($command){
    $FavoriteTest.calls+=,$command
    switch($command.action){
        'favorite_catalog' {return [pscustomobject]@{ok=$true;entries=@($FavoriteEntry)}}
        'favorite_list' {return [pscustomobject]@{ok=$true;favorites=@($FavoriteTest.items)}}
        'favorite_save' {$FavoriteTest.items=@([pscustomobject]@{id='saved';name=$command.name;catalog_id='entry';operations=$command.operations;available=$true});return [pscustomobject]@{ok=$true}}
        'favorite_delete' {$FavoriteTest.items=@();return [pscustomobject]@{ok=$true}}
        'favorite_run' {return [pscustomobject]@{ok=$true;message='Executed'}}
        default {throw ('Unexpected action '+$command.action)}
    }
}
function Click($button){$button.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))}
$sourceText=Get-Content -LiteralPath $Source -Raw -Encoding UTF8
$sourceText=$sourceText.Replace('function ', 'function global:').Replace('[void]$Dialog.ShowDialog()', '& $global:FavoriteProbe')
$sourceText=$sourceText.Replace('Show-WorkspaceWindow $Dialog "favorites:$InstitutionId"', '& $global:FavoriteProbe')
function global:Test-WorkspaceWindow($Key){return $false}
function global:Add-WorkspaceClosedAction($Key,$Action){}
$sourceText=$sourceText.Replace('$Dialog.Owner=$OwnerWindow', '$Dialog.Owner=$null')
Invoke-Expression $sourceText
$global:FavoriteProbe={
    if($null -ne $Inputs){
        $FavoriteTest.edits++
        $Name.Text='Saved size'
        $Inputs[0].control.Text='14'
        Click $Save
        return
    }
    if($Catalog.Items.Count -ne 1){throw 'Catalog missing'}
    $Search.Text='missing'
    if($Catalog.Items.Count -ne 0){throw 'Filter failed'}
    $Search.Text='Example';$Catalog.SelectedIndex=0
    Click $Actions.Children[5]
    if($Favorites.Items.Count -ne 1){throw 'Saved item not refreshed'}
    $Favorites.SelectedIndex=0
    Click $Actions.Children[0]
    if(-not @($FavoriteTest.calls|Where-Object{$_.action -eq 'favorite_run'}).Count){throw 'Run disconnected'}
    Click $Actions.Children[1]
    if($FavoriteTest.edits -ne 2){throw 'Edit not connected'}
    $Favorites.SelectedIndex=0
    Click $Actions.Children[2]
    if($Favorites.Items.Count -ne 0){throw 'Delete not refreshed'}
    $Dialog.Close()
}
Open-Favorites $null
if($FavoriteTest.calls.Where({$_.action -eq 'favorite_save'})[0].operations[0].args[0] -ne 14){throw 'Input not saved'}
# Two successive manager closes must refresh the same visible strip.
$global:FavoriteProbe={ $FavoriteTest.items=@([pscustomobject]@{id='saved';name='Saved size';available=$true});$Dialog.Close() }
$strip=New-FavoriteStrip $null
Click $strip.Children[0]
if($strip.Children.Count -ne 2){throw 'First strip refresh failed'}
Click $strip.Children[0]
if($strip.Children.Count -ne 2){throw 'Second strip refresh failed'}
Write-Output 'FAVORITES_UI_OK'
