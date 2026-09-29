param([string]$Project=(Split-Path -Parent (Split-Path -Parent $PSScriptRoot)),[string]$ImagePath='')
# Run the real manager and shared table events against synthetic personal data.
$ErrorActionPreference='Stop'
function Test-WorkspaceWindow($Key){return $false}
Add-Type -AssemblyName PresentationFramework
. (Join-Path $Project 'profile_table_ui.ps1')
function Assert($Value,$Message){if(-not $Value){throw $Message}}
function Show-Error($Message){throw $Message}
function Set-OriginalSectionHeader($Header,$Text){}
function Set-OriginalFlatButton($Button,$Primary){}
function Write-GuiRuntimeError($Context,$Failure){}
$Status=[Windows.Controls.TextBlock]::new()
$script:Calls=[Collections.Generic.List[object]]::new();$script:Edit='변경한 값'
$script:Profile=[pscustomobject]@{ok=$true;values=@{snapshot='test'};field_groups=@(
 [pscustomobject]@{id='basic';name='이름';path='이름';parent_id='';values=@('기본 이름');default='기본 이름';aliases=@()},
 [pscustomobject]@{id='root';name='연구책임자';path='연구책임자';parent_id='';values=@();default='';aliases=@()},
 [pscustomobject]@{id='name';name='성명';path='연구책임자 > 성명';parent_id='root';values=@('홍길동','김예시');default='홍길동';aliases=@('담당자명')},
 [pscustomobject]@{id='phone';name='전화번호';path='연구책임자 > 전화번호';parent_id='root';values=@('010-1234-1234');default='010-1234-1234';aliases=@()},
 [pscustomobject]@{id='other';name='참여기관';path='참여기관';parent_id='';values=@('서울과학기술대학교');default='서울과학기술대학교';aliases=@()}
)}
function Send-Backend($Command){
 $script:Calls.Add($Command)
 if($Command.action -eq 'user_profile_get'){return $script:Profile}
 if($Command.action -eq 'user_profile_table_mutate'){
  $field=@($script:Profile.field_groups|Where-Object{$_.id -eq $Command.field_id})[0]
  if($Command.operation -eq 'edit_value'){$field.values=@($field.values|ForEach-Object{if($_ -ceq $Command.value){$Command.new_value}else{$_}});if($field.default -ceq $Command.value){$field.default=$Command.new_value}}
  if($Command.operation -eq 'edit_field'){$field.name=$Command.name;$field.path='연구책임자 > '+$Command.name}
 }
 return [pscustomobject]@{ok=$true;message='시험 저장 완료'}
}
function Read-ProfileTableText($Owner,$Title,$Value){return $script:Edit}
function Click($Button){$Button.RaiseEvent([Windows.RoutedEventArgs]::new([Windows.Controls.Button]::ClickEvent))}
function CellClick($Cell,[int]$Count=1){
 $event=[Windows.Input.MouseButtonEventArgs]::new([Windows.Input.Mouse]::PrimaryDevice,0,[Windows.Input.MouseButton]::Left)
 [Windows.Input.MouseButtonEventArgs].GetProperty('ClickCount').SetValue($event,$Count,$null)
 $event.RoutedEvent=[Windows.UIElement]::PreviewMouseLeftButtonDownEvent;$Cell.RaiseEvent($event)
}
function Find-Cell($Grid,$Text){@($Grid.Children|Where-Object{$_ -is [Windows.Controls.Border] -and $_.Child.Text -like $Text})[0]}
function Last-Change {@($script:Calls|Where-Object{$_.action -ne 'user_profile_get'})[-1]}
$global:ManagerProbe={
 try{
  Assert $script:ProfileReviewActive 'Manager did not pause background polling'
  Assert ($TableGrid -is [Windows.Controls.Grid] -and $Table.Depth -eq 2) 'Manager still has flat table'
  $root=Find-Cell $TableGrid '연구책임자';$child=Find-Cell $TableGrid '성명*'
  Assert ([Windows.Controls.Grid]::GetRowSpan($root) -eq 3 -and [Windows.Controls.Grid]::GetRowSpan($child) -eq 2) 'Hierarchy/merged cells missing'
  Assert ($null -eq (Find-Cell $TableGrid '기본 이름')) 'Basic leaf duplicated in document fields'
  Assert ($null -ne (Find-Cell $TableGrid '010-1234-1234')) 'Nested basic-name field hidden'
  CellClick (Find-Cell $TableGrid '김예시')
  Assert ($Table.SelectedItem.profile_field_id -eq 'name' -and $Value.Text -eq '김예시' -and $FieldName.Text -eq '성명' -and $Parent.SelectedItem.id -eq 'root') 'Selection did not populate existing controls'
  Click $SetDefault
  Assert ((Last-Change).action -eq 'user_profile_default_set' -and (Last-Change).value -eq '김예시') 'Default button lost selection'
  CellClick (Find-Cell $TableGrid '김예시') 2
  Assert ((Last-Change).operation -eq 'edit_value' -and (Last-Change).field_id -eq 'name') 'Double-click did not edit correct value'
  Assert ($null -ne (Find-Cell $TableGrid '변경한 값')) 'Edited value not refreshed in tree'
  $script:Edit=$null;$before=$script:Calls.Count
  CellClick (Find-Cell $TableGrid '변경한 값') 2
  Assert ($script:Calls.Count -eq $before) 'Cancelled edit saved'
  $script:Edit='신청자 성명';CellClick (Find-Cell $TableGrid '성명*') 2
  Assert ($FieldName.Text -eq '신청자 성명' -and (Last-Change).field_id -eq 'name') 'Rename did not refresh form/identity'
  $Aliases.Text='성명, 담당자';Click $SaveAliases
  Assert ((Last-Change).action -eq 'user_profile_aliases_set' -and (Last-Change).aliases.Count -eq 2) 'Alias save broken'
  $Parent.SelectedIndex=0;Click $SetParent
  Assert ((Last-Change).action -eq 'user_profile_field_parent_set' -and (Last-Change).parent_field_id -eq '') 'Parent button broken'
  $FieldName.Text='새 항목';$Value.Text='새 입력';Click $Add
  Assert ((Last-Change).action -eq 'user_profile_entry_add' -and (Last-Change).value -eq '새 입력') 'Add button broken'
  CellClick (Find-Cell $TableGrid '변경한 값');Click $Delete
  Assert ((Last-Change).action -eq 'user_profile_entry_delete' -and (Last-Change).value -eq '변경한 값') 'Delete button broken'
  $Grid.Measure([Windows.Size]::new(1020,740));$Grid.Arrange([Windows.Rect]::new(0,0,1020,740));$Grid.UpdateLayout()
  $grip=@($TableGrid.Children|Where-Object{$_ -is [Windows.Controls.Primitives.Thumb]})[0]
  $before=$TableGrid.ColumnDefinitions[0].ActualWidth
  $drag=[Windows.Controls.Primitives.DragDeltaEventArgs]::new(50,0);$drag.RoutedEvent=[Windows.Controls.Primitives.Thumb]::DragDeltaEvent;$grip.RaiseEvent($drag)
  Assert ([Math]::Abs($TableGrid.ColumnDefinitions[0].Width.Value-$before-50) -lt 1) 'Column resize failed'
  $width=$TableGrid.ColumnDefinitions[0].Width.Value;& $RefreshDocumentFieldRows
  Assert ($TableGrid.ColumnDefinitions[0].Width.Value -eq $width) 'Refresh lost column width'
  if($ImagePath){
   $Grid.Background=$Dialog.Background;$Grid.UpdateLayout();$bitmap=[Windows.Media.Imaging.RenderTargetBitmap]::new(1020,740,96,96,[Windows.Media.PixelFormats]::Pbgra32);$bitmap.Render($Grid)
   $encoder=[Windows.Media.Imaging.PngBitmapEncoder]::new();$encoder.Frames.Add([Windows.Media.Imaging.BitmapFrame]::Create($bitmap));$stream=[IO.File]::Create($ImagePath);try{$encoder.Save($stream)}finally{$stream.Dispose()}
  }
  $script:Profile.field_groups=@();& $RefreshDocumentFieldRows
  Assert ($null -eq $Table.SelectedItem -and $null -ne (Find-Cell $TableGrid '저장된 문서 필드가 없습니다*')) 'Empty state or stale selection incorrect'
  'DOCUMENT_FIELD_MANAGER_OK: shared hierarchy, selection, edit, add, aliases, parent, default, delete, resize, empty state'
 }finally{$Dialog.Close()}
}
$tokens=$null;$errors=$null;$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $Project 'launch_gui.ps1'),[ref]$tokens,[ref]$errors)
Assert ($errors.Count -eq 0) 'Launcher parse failed'
foreach($name in @('Open-DocumentFieldManager','Show-DocumentFieldManager')){
 $definition=$ast.Find({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name},$true)
 . ([scriptblock]::Create($definition.Extent.Text.Replace("Show-WorkspaceWindow `$Dialog 'profile-manager'",'& $global:ManagerProbe')))
}
Open-DocumentFieldManager $null
Assert (-not $script:ProfileReviewActive) 'Review state leaked after close'
