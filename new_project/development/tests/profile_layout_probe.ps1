param([string]$Project,[string]$ImagePath='')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
. (Join-Path $Project 'profile_table_ui.ps1')
. (Join-Path $Project 'document_authoring_ui.ps1')
function Assert($Condition,$Message){if(-not $Condition){throw $Message}}
function Write-GuiRuntimeError($Context,$Failure){}
function Show-Error($Message){throw ($Message+' '+(Get-PSCallStack | Out-String))}
$script:Commands=[System.Collections.Generic.List[object]]::new();$script:RefreshCount=0;$script:Edit='edited'
$script:Profile=[pscustomobject]@{ok=$true;values=@{snapshot='test'};field_groups=@(
    [pscustomobject]@{id='basic';name='이름';parent_id='';path='이름';values=@('홍길동');aliases=@();default='홍길동'},
    [pscustomobject]@{id='root';name='연구자';parent_id='';path='연구자';values=@();aliases=@();default=''},
    [pscustomobject]@{id='child';name='성명';parent_id='root';path='연구자 > 성명';values=@('홍길동','김예시');aliases=@();default='홍길동'},
    [pscustomobject]@{id='phone';name='연락처';parent_id='root';path='연구자 > 연락처';values=@('010-1234-5678');aliases=@();default=''},
    [pscustomobject]@{id='second';name='참여기관';parent_id='';path='참여기관';values=@();aliases=@();default=''},
    [pscustomobject]@{id='duplicate';name='성명';parent_id='second';path='참여기관 > 성명';values=@('박예시');aliases=@();default=''}
)}
function Send-Backend($Command){$script:Commands.Add($Command);if($Command.action -eq 'user_profile_get'){return $script:Profile};return [pscustomobject]@{ok=$true;message='ok'}}
function Read-ProfileTableText($Owner,$Title,$Value){return $script:Edit}
function Resize($Thumb,[double]$Delta){$event=[System.Windows.Controls.Primitives.DragDeltaEventArgs]::new($Delta,0);$event.RoutedEvent=[System.Windows.Controls.Primitives.Thumb]::DragDeltaEvent;$Thumb.RaiseEvent($event);Assert $event.Handled 'Resize event leaked to field dragging'}
function Measure-Grid($Grid){$Grid.Measure([System.Windows.Size]::new(940,700));$Grid.Arrange([System.Windows.Rect]::new(0,0,940,700));$Grid.UpdateLayout()}
$state=@{Grid=[System.Windows.Controls.Grid]::new();Profile=$null;Row=1;Depth=1;PageId='test';DragStart=$null;Note=[System.Windows.Controls.TextBlock]::new()}
Update-ProfileTable $state;Measure-Grid $state.Grid
$handles=@($state.Grid.Children | Where-Object {$_ -is [System.Windows.Controls.Primitives.Thumb]})
Assert ($handles.Count -eq $state.Grid.ColumnDefinitions.Count) 'Missing header resize handles'
Assert (@($handles | Where-Object {[System.Windows.Controls.Grid]::GetRow($_) -ne 0}).Count -eq 0) 'Resize grip outside header'
$original=$state.Grid.ColumnDefinitions[0].ActualWidth;$neighbor=$state.Grid.ColumnDefinitions[1].ActualWidth
Resize $handles[0] 60
Assert ([Math]::Abs($state.Grid.ColumnDefinitions[0].Width.Value-$original-60) -lt 1) 'Dragged column did not resize'
Assert ([Math]::Abs($state.Grid.ColumnDefinitions[1].Width.Value-$neighbor) -lt 1) 'Unrelated column changed'
$saved=$state.Grid.ColumnDefinitions[0].Width.Value
Update-ProfileTable $state
Assert ($state.Grid.ColumnDefinitions[0].Width.Value -eq $saved) 'Width lost on table refresh'
$handle=@($state.Grid.Children | Where-Object {$_ -is [System.Windows.Controls.Primitives.Thumb]})[0]
Resize $handle -9999
Assert ($state.Grid.ColumnDefinitions[0].Width.Value -eq $state.Grid.ColumnDefinitions[0].MinWidth) 'Minimum width not enforced'
$table=@{Grid=[System.Windows.Controls.Grid]::new();Collapsed=@{};Select={};Changed={};EditName={};EditValue={}}
$rows=@([pscustomobject]@{id='p1';path=@('정보','성명');label='성명';topic='정보';value='예시';ai=$false;context=''})
Show-AuthoringInputTable $table $rows;Measure-Grid $table.Grid
$grip=@($table.Grid.Children | Where-Object {$_ -is [System.Windows.Controls.Primitives.Thumb]})[0]
Resize $grip 40;$width=$table.Grid.ColumnDefinitions[0].Width.Value
Show-AuthoringInputTable $table $rows
Assert ($table.Grid.ColumnDefinitions[0].Width.Value -eq $width) 'Authoring refresh lost widths'
$tree=[System.Windows.Controls.TreeView]::new();$changed={$script:RefreshCount++}
Show-PersonalFieldTree $tree $script:Profile $null $changed
Assert ($tree.Items.Count -eq 2) 'Basic leaf duplicated or hierarchy flattened'
Assert ($tree.Tag['root'].Items.Count -eq 2 -and $tree.Tag['child'].Items.Count -eq 2) 'Parent/child/value structure wrong'
Assert ($tree.Tag['duplicate'].Parent -eq $tree.Tag['second']) 'Equal field labels were merged across parents'
$tree.Tag['root'].IsExpanded=$false
Show-PersonalFieldTree $tree $script:Profile $null $changed
Assert (-not $tree.Tag['root'].IsExpanded) 'Collapsed branch not preserved'
function DoubleClick-Header($Header){
    $event=[System.Windows.Input.MouseButtonEventArgs]::new([System.Windows.Input.Mouse]::PrimaryDevice,0,[System.Windows.Input.MouseButton]::Left)
    $event.RoutedEvent=[System.Windows.Controls.Control]::PreviewMouseDoubleClickEvent
    $Header.RaiseEvent($event)
}
DoubleClick-Header $tree.Tag['child'].Items[1].Header
Assert ($script:Commands[-1].field_id -eq 'child' -and $script:Commands[-1].value -eq '김예시' -and $script:RefreshCount -eq 1) 'Tree double-click edited the wrong value'
$script:Edit=$null;$before=$script:Commands.Count
DoubleClick-Header $tree.Tag['child'].Header
Assert ($script:Commands.Count -eq $before) 'Cancelled tree edit saved'
$script:Edit='renamed';DoubleClick-Header $tree.Tag['child'].Header
Assert ($script:Commands[-1].field_id -eq 'child' -and $script:Commands[-1].operation -eq 'edit_field') 'Tree name edit lost stable identity'
# Render the actual personal tab with synthetic values; never touch user data.
$tokens=$null;$errors=$null;$ast=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $Project 'launch_gui.ps1'),[ref]$tokens,[ref]$errors)
foreach($fn in $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -in @('Render-PersonalTab','New-PurpleAccentBrush','Set-OriginalFlatButton','Get-PurpleButtonTemplate')},$true)){. ([scriptblock]::Create($fn.Extent.Text))}
function New-FavoriteStrip($Owner){return [System.Windows.Controls.StackPanel]::new()}
$Content=[System.Windows.Controls.Canvas]::new();$Content.Width=300;$Content.Height=400;$Content.Background='White';$Status=[System.Windows.Controls.TextBlock]::new();$Window=$null
Render-PersonalTab
Assert (@($Content.Children | Where-Object {$_ -is [System.Windows.Controls.TreeView]}).Count -eq 1) 'Personal tab did not install tree'
$personalTree=@($Content.Children | Where-Object {$_ -is [System.Windows.Controls.TreeView]})[0]
DoubleClick-Header $personalTree.Tag['child'].Items[0].Header
Assert ($script:Commands[-2].action -eq 'user_profile_table_mutate' -and $script:Commands[-1].action -eq 'user_profile_get') 'Personal tab edit did not refresh live data'
$Content.Measure([System.Windows.Size]::new(300,400));$Content.Arrange([System.Windows.Rect]::new(0,0,300,400));$Content.UpdateLayout()
if($ImagePath){
    $bitmap=[System.Windows.Media.Imaging.RenderTargetBitmap]::new(600,800,192,192,[System.Windows.Media.PixelFormats]::Pbgra32);$bitmap.Render($Content)
    $encoder=[System.Windows.Media.Imaging.PngBitmapEncoder]::new();$encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap));$stream=[IO.File]::Create($ImagePath);try{$encoder.Save($stream)}finally{$stream.Dispose()}
}
'PROFILE_LAYOUT_OK: both tables resize, refresh preserves width, personal hierarchy and double-click edits'
