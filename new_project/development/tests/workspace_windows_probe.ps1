param([string]$Project=(Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
# Reuse synthetic profile/backend fixtures only, not the nested-window test body.
$fixture=Get-Content (Join-Path $PSScriptRoot 'document_field_manager_probe.ps1') -Raw -Encoding UTF8
$fixture=$fixture.Substring(0,$fixture.IndexOf('$global:ManagerProbe='))
. ([scriptblock]::Create($fixture)) -Project $Project
. (Join-Path $Project 'workspace_windows.ps1')
. (Join-Path $Project 'document_authoring_ui.ps1')
. (Join-Path $Project 'document_authoring_flow_ui.ps1')
Add-Type -Path (Join-Path $Project 'gui_poll_guard.cs') -ReferencedAssemblies @([Windows.Window].Assembly.Location,[Windows.Media.Visual].Assembly.Location,[Windows.Threading.Dispatcher].Assembly.Location,'System.dll','System.Core.dll','System.Xaml.dll')
[GovOfficePollGuard]::Initialize()
Add-Type -TypeDefinition @'
using System;using System.Runtime.InteropServices;
public static class ModelessProbeNative {[DllImport("user32.dll")] public static extern bool IsWindowEnabled(IntPtr hwnd);}
'@
$tokens=$null;$errors=$null;$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $Project 'launch_gui.ps1'),[ref]$tokens,[ref]$errors)
foreach($name in @('Open-DocumentFieldManager','Show-DocumentFieldManager')){
 $definition=$ast.Find({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 . ([scriptblock]::Create($definition.Extent.Text))
}
$realBackend=${function:Send-Backend}
function Send-Backend($Command){
 switch($Command.action){
  'authoring_overview' {return @{ok=$true;result=@{templates=@(@{id='template';name='모의 양식'});jobs=@();account=@{connected=$true;email='test@example.invalid'}}}}
  'authoring_connection_check' {return @{ok=$true;result=@{operation_id='check'}}}
  'authoring_operation' {return @{ok=$true;result=@{status='completed';result=@{connected=$true;email='test@example.invalid'}}}}
  default {return & $realBackend $Command}
 }
}
$realShow=${function:Show-WorkspaceWindow}
function Show-WorkspaceWindow($Dialog,$Key){$Dialog.Opacity=0;$Dialog.ShowInTaskbar=$false;& $realShow $Dialog $Key}
function Find-Control($Node,$Type,$Content){
 if($Node -is $Type -and ($null -eq $Content -or [string]$Node.Content -eq $Content)){return $Node}
 foreach($child in [Windows.LogicalTreeHelper]::GetChildren($Node)){
  if($child -is [Windows.DependencyObject]){$found=Find-Control $child $Type $Content;if($found){return $found}}
 }
}
function Enabled-Native($Dialog){[ModelessProbeNative]::IsWindowEnabled([Windows.Interop.WindowInteropHelper]::new($Dialog).Handle)}
function Pump([int]$Milliseconds){
 $frame=[Windows.Threading.DispatcherFrame]::new();$timer=[Windows.Threading.DispatcherTimer]::new();$timer.Interval=[TimeSpan]::FromMilliseconds($Milliseconds)
 $timer.Add_Tick({$frame.Continue=$false}.GetNewClosure());$timer.Start();try{[Windows.Threading.Dispatcher]::PushFrame($frame)}finally{$timer.Stop()}
}
$app=[Windows.Application]::Current;if($null -eq $app){$app=[Windows.Application]::new()};$app.ShutdownMode='OnExplicitShutdown'
$Window=[Windows.Window]::new();$Window.Opacity=0;$Window.ShowInTaskbar=$false;$app.MainWindow=$Window
$mainButton=[Windows.Controls.Button]::new();$mainButton.Content='main';$Window.Content=$mainButton
$script:MainClicks=0;$mainButton.Add_Click({$script:MainClicks++})
try{
 $Window.Show()
 # These calls MUST return while their windows are still open.
 Open-DocumentFieldManager $Window
 $manager=$script:WorkspaceWindows['profile-manager']
 Assert ($manager.IsVisible -and -not $script:ProfileReviewActive) 'Manager did not return or left modal guard active'
 Open-ProfileDataTable $Window
 $data=$script:WorkspaceWindows['profile-data']
 Open-DocumentAuthoring $Window
 $author=$script:WorkspaceWindows['authoring']
 Assert ($script:WorkspaceWindows.Count -eq 3) 'Independent workspaces not opened'
 foreach($windowItem in @($Window,$manager,$data,$author)){Assert (Enabled-Native $windowItem) 'Another window was disabled'}
 Click $mainButton
 Assert ($script:MainClicks -eq 1) 'Main event blocked by child window'
 # Fire handlers after their creating functions have returned and other windows opened.
 $grid=Find-Control $manager ([Windows.Controls.Grid]) $null
 $tree=@($grid.Children|Where-Object{$_ -is [Windows.Controls.ScrollViewer]})[0].Content
 CellClick (Find-Cell $tree '김예시')
 Click (Find-Control $manager ([Windows.Controls.Button]) '기본값 지정')
 Assert ((Last-Change).field_id -eq 'name' -and (Last-Change).value -eq '김예시') 'Handler lost its own window state'
 Click (Find-Control $data ([Windows.Controls.Button]) '새로고침')
 $author.FindName('ProjectTitle').Text='창별 입력 상태'
 Pump 1150
 Assert ($author.FindName('Account').Text.Contains('test@example.invalid')) 'Authoring timer stopped when opening function returned'
 Assert ($author.FindName('ProjectTitle').Text -eq '창별 입력 상태') 'Another window overwrote writing inputs'
 Open-DocumentFieldManager $Window
 Assert ($script:WorkspaceWindows.Count -eq 3 -and $script:WorkspaceWindows['profile-manager'] -eq $manager) 'Duplicate manager created'
 $script:ClosedCallbacks=0;Add-WorkspaceClosedAction 'profile-manager' {$script:ClosedCallbacks++}
 Click (Find-Control $manager ([Windows.Controls.Button]) '닫기')
 Assert ($script:WorkspaceWindows.Count -eq 2 -and $script:ClosedCallbacks -eq 1) 'Close cleanup/callback failed'
 Assert ((Enabled-Native $Window) -and (Enabled-Native $data) -and (Enabled-Native $author)) 'Closing one disabled the others'
 Open-DocumentFieldManager $Window
 Assert ($script:WorkspaceWindows['profile-manager'] -ne $manager) 'Closed manager could not reopen'
 $Window.Close();Pump 50
 Assert ($script:WorkspaceWindows.Count -eq 0) 'Owned windows/registry survived main close'
 'WORKSPACE_WINDOWS_OK: real modeless HWNDs; 3 simultaneous production windows; native input enabled; callbacks after return; authoring timer; duplicate focus; reopen; owner cleanup'
}finally{foreach($dialog in @($script:WorkspaceWindows.Values)){$dialog.Close()};$Window.Close();$app.Shutdown()}
