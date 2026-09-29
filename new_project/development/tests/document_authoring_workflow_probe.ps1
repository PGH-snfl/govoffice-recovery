param([string]$ScreenshotDirectory='')
# Exercise production callbacks in memory. No window is shown, no backend,
# personal file, HWP, network or login is used.
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
$Project=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
. (Join-Path $Project 'profile_table_ui.ps1')
. (Join-Path $Project 'document_authoring_ui.ps1')
Add-Type -Path (Join-Path $Project 'gui_poll_guard.cs') -ReferencedAssemblies @(
 [System.Windows.Window].Assembly.Location,[System.Windows.Media.Visual].Assembly.Location,
 [System.Windows.Threading.Dispatcher].Assembly.Location,'System.dll','System.Core.dll','System.Xaml.dll')
[GovOfficePollGuard]::Initialize()
$script:BackendRequestInFlight=$false
$script:Calls=[System.Collections.Generic.List[object]]::new()
$script:Templates=@([pscustomobject]@{id='existing';name='저장된 예시 양식';folder='unused'})
$script:Operation=$null
$script:Created=$null
$script:MockAccount=@{connected=$true;email='example@test.invalid';plan='test'}
$script:MockJob=@{status='ready';completed=@();total=2;written_count=0;manual_topics=@();output_dir='unused'}
function Send-Backend($Command){
 $script:Calls.Add($Command)
 $Result=switch($Command.action){
  'authoring_overview' { @{templates=$script:Templates;jobs=@();account=$script:MockAccount} }
  'authoring_connection_check' {$script:Operation=@{status='completed';result=$script:MockAccount};@{operation_id='check'}}
  'authoring_logout' {$script:MockAccount=@{connected=$false};$script:Operation=@{status='completed';result=$script:MockAccount};@{operation_id='logout'}}
  'authoring_login' {$script:MockAccount=@{connected=$true;email='second@test.invalid';plan='test'};$script:Operation=@{status='completed';result=$script:MockAccount};@{operation_id='login'}}
  'authoring_profile' { @{values=@{'이름'='홍길동';'전화번호'='010-1234-1234';'이메일'='example@test.invalid'}} }
  'authoring_profile_save' { @{values=$Command.values} }
  'authoring_register_builtin' {
   $script:Templates=@([pscustomobject]@{id='new';name='새 양식';folder='unused'})+$script:Templates
   $script:Operation=@{status='completed';result=@{id='new';topics=@(@{id='s1'},@{id='s2'})}}
   @{operation_id='register'}
  }
  'authoring_register_file' {
   $reviews=@([pscustomobject]@{index=4;label='설명 칸';text='____';reason='본문인지 확인 필요';writable=$true},[pscustomobject]@{index=9;label='복합 표';text='표·그림';reason='복합 요소';writable=$false})
   $script:Templates=@([pscustomobject]@{id='ai';name='AI 분석 양식';analysis_reviews=$reviews;has_guide_outline=$true;analysis_version='v1'})+$script:Templates
   $script:Operation=@{status='completed';phase='AI 소주제·작성요령 추출 완료';result=@{id='ai';topics=@(@{id='s1'});analysis_reviews=$reviews;registration_mode='guides_then_research_and_write';guide_file='C:\synthetic\registered-guides.md';manual_topics=@()}}
   @{operation_id='analysis'}
  }
  'authoring_analysis_resolve' {
   $item=@($script:Templates|Where-Object {$_.id -eq $Command.template_id})[0]
   $item.analysis_reviews=@($item.analysis_reviews|Where-Object {-not $Command.choices.ContainsKey([string]$_.index)})
   @{id=$item.id}
  }
  'authoring_guide_outline' {
   @{outline=@{common_instructions=@(@{index=10;text='전체 공통 요령'});chapters=@(@{index=0;title='1. 연구 필요성';instructions=@();subtopics=@(@{index=1;title='1-1. 기술 현황';instructions=@(@{index=11;text='공개 통계를 근거로 작성'});subtopics=@()})});unassigned_indices=@()}}
  }
  'authoring_delete_template' {
   if($Command.confirmed -ne $true){throw 'Deletion was not confirmed'}
   if($script:DeleteError){throw '등록 폴더 이동 단계에서 실패했습니다.'}
   $script:Templates=@($script:Templates|Where-Object {$_.id -ne $Command.template_id})
   @{deleted=$true;template_id=$Command.template_id;recoverable=$true;archive_path='test archive only';storage='archived'}
  }
  'authoring_prepare_inputs' {
   $script:Operation=@{status='completed';result=@{template_id=$Command.template_id;rows=@($script:MockRows)}}
   @{operation_id='inputs'}
  }
  'authoring_operation' { if($Command.operation_id -eq 'open-output'){@{status='completed';result=@{document_open=$true;visible=$true;path='unused.hwp'}}}else{$script:Operation} }
  'authoring_validate_inputs' { @{values=$Command.local_values} }
  'authoring_create' {$script:Created=$Command;@{id='job';output_dir='unused'}}
  'authoring_prepare_replay' {
   $script:Operation=@{status='completed';result=@{template_id=$Command.template_id;replay=$true;path=$Command.path;sha256='verified';topics=2;rows=@();brief=@{title='저장된 응답 주제';description='저장된 응답 설명'};message='AI 호출 없이 저장된 응답을 사용합니다.'}}
   @{operation_id='replay-load'}
  }
  'authoring_create_replay' {$script:Created=$Command;@{id='job';output_dir='unused'}}
  'authoring_status' { $script:MockJob }
  'authoring_resume' {$script:MockJob.status='running';$script:MockJob.error='';$script:MockJob}
  'authoring_stop' {$script:MockJob.status='paused';$script:MockJob}
  default {throw ('Unexpected backend call: '+$Command.action)}
 }
 # Match the real backend's JSON/PSCustomObject boundary, not just hashtables.
 return (@{ok=$true;result=$Result}|ConvertTo-Json -Depth 40|ConvertFrom-Json)
}
function Assert($Value,$Message){if(-not $Value){throw $Message}}
function Click($Button){$Button.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Button]::ClickEvent))}
function DoubleClick($Control){
 $Event=[System.Windows.Input.MouseButtonEventArgs]::new([System.Windows.Input.Mouse]::PrimaryDevice,0,[System.Windows.Input.MouseButton]::Left)
 $Event.RoutedEvent=[System.Windows.Controls.Control]::PreviewMouseDoubleClickEvent;$Control.RaiseEvent($Event)
}
$script:EditResult=$null
function Read-ProfileTableText($OwnerWindow,$Title,$Value){$script:EditTitle=$Title;return $script:EditResult}
function Save-Design($Dialog,$Name,[double]$Width=1040,[double]$Height=820){
 if(-not $ScreenshotDirectory){return}
 [void][IO.Directory]::CreateDirectory($ScreenshotDirectory)
 $Root=$Dialog.Content
 $Root.Measure([System.Windows.Size]::new($Width,$Height));$Root.Arrange([System.Windows.Rect]::new(0,0,$Width,$Height));$Root.UpdateLayout()
 $Bitmap=[System.Windows.Media.Imaging.RenderTargetBitmap]::new([int]$Width,[int]$Height,96,96,[System.Windows.Media.PixelFormats]::Pbgra32)
 $Backdrop=[System.Windows.Media.DrawingVisual]::new();$Drawing=$Backdrop.RenderOpen();$Drawing.DrawRectangle($Dialog.Background,$null,[System.Windows.Rect]::new(0,0,$Width,$Height));$Drawing.Close();$Bitmap.Render($Backdrop)
 $Bitmap.Render($Root)
 $Encoder=[System.Windows.Media.Imaging.PngBitmapEncoder]::new();$Encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($Bitmap))
 $File=[IO.File]::Create((Join-Path $ScreenshotDirectory ($Name+'.png')))
 try{$Encoder.Save($File)}finally{$File.Dispose()}
}

$script:MockRows=@(
 [pscustomobject]@{id='P0003';field_ids=@('P0003','P0004');profile_field_id='name';topic='저장된 개인정보';path=@('연구책임자','이름');label='이름';context='연구책임자 > 이름';ai=$false;value='홍길동'},
 [pscustomobject]@{id='P0005';field_ids=@('P0005');profile_field_id='phone';topic='저장된 개인정보';path=@('연구책임자','전화번호');label='전화번호';context='연구책임자 > 전화번호';ai=$false;value='010-1234-1234'}
)
function Invoke-AuthoringWorkflowProbe($Dialog,$UI,$State,$Actions,$Timer){
 try{
  $script:OpenedOutputs=[System.Collections.Generic.List[string]]::new()
  $script:OpenFailure=$false
  $Actions.LaunchOutput={param($path) $script:OpenedOutputs.Add($path);if($script:OpenFailure){throw 'synthetic open failure'};@{operation_id='open-output'}}
  $Timer.Stop();& $Actions.Poll
  Assert ($State.connected -and $UI.Account.Text.Contains('example@test.invalid')) 'Account identity missing'
  Assert ($State.page -eq 1 -and -not $UI.Step2Card.IsEnabled) 'Unprepared next step enabled'
  & $Actions.Page 2
  Assert ($State.page -eq 1) 'Page guard bypassed'
  Save-Design $Dialog '01-template'
  Assert ($UI.Import.IsEnabled) 'AI-connected registration unavailable'
  Assert ($UI.ReconnectBody.IsEnabled) 'Saved template body reconnection unavailable'
  $originalBegin=$Actions.Begin
  $Actions.Begin={param($command) $script:ReconnectCommand=$command}
  Click $UI.ReconnectBody
  Assert ($script:ReconnectCommand.action -eq 'authoring_reanalyze_template' -and $script:ReconnectCommand.template_id -eq 'existing') 'Reconnect button targets wrong template/action'
  $Actions.Begin=$originalBegin
  $State.connected=$false;& $Actions.Update
  Assert (-not $UI.Import.IsEnabled) 'AI finder enabled without login'
  $State.operation='raw-export';$State.operationAction='authoring_extract_guides'
  $script:Operation=@{status='completed';result=@{guide_file='C:\synthetic\guides.md';heading_count=2;instruction_count=4;ai_requests=1}}
  & $Actions.Poll
  Assert ($UI.OpenGuideFile.Visibility -eq 'Visible' -and $State.guideFile -eq 'C:\synthetic\guides.md') 'Export file button not connected'
  Assert ($UI.GuideOutline.Visibility -eq 'Collapsed') 'Old classified outline remained after raw export'
  Assert ($UI.Notice.Text.Contains('AI 요청 1회')) 'AI finder result missing'
  Assert ($UI.Import.Content -eq '문서 작성용 양식 등록' -and $UI.ExtractGuides.Content -eq '소주제·작성요령 파일 추출') 'Registration and guide export are not separate'
  $State.connected=$true;& $Actions.Update
  & $Actions.Begin @{action='authoring_register_file';path='synthetic.hwp'};& $Actions.Poll
  Assert ($UI.AnalysisReview.Visibility -eq 'Visible' -and $State.analysisChoices.Count -eq 2) 'Ambiguous fields not displayed'
  Assert ($State.analysisChoices['9'].Items.Count -eq 2) 'Unsafe complex element allowed writable roles'
  Assert ($UI.GuideOutline.Visibility -eq 'Visible') 'Outline viewer missing'
  Assert ($State.guideFile -eq 'C:\synthetic\registered-guides.md' -and $UI.Notice.Text.Contains('자료조사와 본문 작성을 시작')) 'Guide registration did not lead to writing'
  $UI.GuideOutline.IsExpanded=$true
  Assert ($UI.GuideTree.Items.Count -eq 2) 'Common and chapter roots not displayed'
  Assert ($UI.GuideTree.Items[1].Items[0].Header.Text -eq '1-1. 기술 현황') 'Subtopic hierarchy not displayed'
  Assert ($UI.GuideTree.Items[1].Items[0].Items[0].Header.Text -eq '공개 통계를 근거로 작성') 'Original guidance missing'
  $UI.GuideOutline.IsExpanded=$false;$UI.GuideOutline.IsExpanded=$true
  Assert (@($script:Calls|Where-Object {$_.action -eq 'authoring_guide_outline'}).Count -eq 1) 'Outline unnecessarily reloaded'
  Save-Design $Dialog '01-analysis-review'
  $State.analysisChoices['4'].SelectedIndex=2
  Click $UI.ApplyAnalysis
  Assert ($State.analysisChoices.Count -eq 1 -and $State.analysisChoices.ContainsKey('9')) 'Unselected ambiguity was lost'
  Assert (@($script:Calls|Where-Object {$_.action -eq 'authoring_analysis_resolve'})[-1].choices['4'] -eq 'body') 'Review selection sent wrong role'
  $Actions.ConfirmDeleteTemplate={param($name) $false}
  Click $UI.DeleteTemplate
  Assert ($UI.Templates.SelectedItem.id -eq 'ai') 'Cancelled deletion changed selection'
  Assert (@($script:Calls|Where-Object {$_.action -eq 'authoring_delete_template'}).Count -eq 0) 'Cancel sent a delete request'
  $State.prepared='ai';$State.rows=@($script:MockRows)
  $Actions.ConfirmDeleteTemplate={param($name) $true}
  $script:DeleteError=$true;Click $UI.DeleteTemplate
  Assert ($UI.Templates.SelectedItem.id -eq 'ai' -and -not $State.editing) 'Failed deletion changed the template or locked UI'
  Assert ($UI.Notice.Text.Contains('등록 폴더 이동')) 'Deletion error stage not shown'
  $script:DeleteError=$false
  Click $UI.DeleteTemplate
  Assert ($UI.Notice.Text.Contains('삭제 보관 폴더')) 'Successful deletion did not report an archive move'
  Assert (@($UI.Templates.ItemsSource|Where-Object {$_.id -eq 'ai'}).Count -eq 0) 'Deleted template remains visible'
  Assert ($null -eq $State.prepared -and $State.rows.Count -eq 0) 'Deleted template inputs were retained'
  Assert (-not $State.editing -and -not $UI.Step2Card.IsEnabled) 'Deletion did not reset navigation/edit state'
  Click $UI.Builtin;& $Actions.Poll
  Assert ($UI.Templates.SelectedItem.id -eq 'new') 'Registered form not selected'
  Assert (@($script:Calls | Where-Object {$_.action -eq 'authoring_profile_save'}).Count -eq 0) 'Registration rewrote personal profile'
  Click $UI.Next;& $Actions.Poll
  Assert ($State.page -eq 2 -and $State.table.Cells.Count -eq 2) ('Saved-only preparation failed: '+$UI.Notice.Text)
  Assert ($State.table.Grid.ColumnDefinitions.Count -eq 3) 'Personal-only table still has AI column'
  Assert ($null -eq $State.table.Cells.P0003.Toggle) 'AI switch still visible'
  Assert ($State.rows[0].field_ids.Count -eq 2) 'Duplicate document targets lost'
  $script:EditResult='이번 문서 이름'
  DoubleClick $State.table.Cells.P0003.Button
  Assert ($State.rows[0].value -eq '이번 문서 이름') 'Optional double-click edit failed'
  $script:EditResult=$null
  DoubleClick $State.table.Cells.P0003.Button
  Assert ($State.rows[0].value -eq '이번 문서 이름') 'Cancel changed value'
  $State.editing=$true;$count=$script:Calls.Count;& $Actions.Poll
  Assert ($script:Calls.Count -eq $count) 'Poll entered modal editor'
  $State.editing=$false
  Click $UI.Step1Card;Click $UI.Step2Card
  Assert ($State.page -eq 2 -and $State.rows[0].value -eq '이번 문서 이름') 'Back navigation lost edited value'
  $UI.ProjectTitle.Text='검증 과제'
  Assert (-not $UI.Start.IsEnabled) 'Details must be required'
  $UI.Description.Text='지역 공공시설의 에너지 절감 방안을 작성해 주세요.'
  Assert ($UI.Start.IsEnabled) 'Two inputs did not enable start'
  Save-Design $Dialog '02-writing-input'
  Save-Design $Dialog '02-writing-input-compact' 800 650
  $UI.WritingPage.ScrollToBottom();Save-Design $Dialog '02-saved-info';$UI.WritingPage.ScrollToTop()
  Click $UI.Start
  Assert ($null -ne $script:Created -and $State.page -eq 3) ('Create failed: '+$UI.Notice.Text)
  Assert ($script:Created.brief.Count -eq 2) 'Extra brief inputs sent'
  Assert ($script:Created.research_enabled -eq $true) 'Public research not enabled for a new job'
  Assert ($script:Created.review_mode -eq 'final_output' -and -not $script:Created.reviewed) 'Review was incorrectly marked complete'
  Assert ($script:Created.local_values.P0003 -eq '이번 문서 이름' -and $script:Created.local_values.P0004 -eq '이번 문서 이름') 'Deduplicated edit did not fill every target'
  Assert (@($script:Created.local_values.PSObject.Properties).Count -eq 3) 'Unexpected local fields sent'
  foreach($name in @('Steps','Navigation')){Assert ($UI[$name].Visibility -eq 'Visible') "Missing navigation $name"}
  Assert (-not $UI.Step4Card.IsEnabled -and -not $UI.Next.IsEnabled) 'Unfinished completion enabled'
  Click $UI.Step4Card;Assert ($State.page -eq 3) 'Completion guard bypassed'
  Click $UI.Back
  Assert ($State.page -eq 2 -and $UI.ProjectTitle.IsReadOnly -and $UI.Description.IsReadOnly) 'Running review is not locked'
  Assert ($UI.ProjectTitle.Background.ToString() -eq '#FFECEDEF' -and $State.table.ReadOnly) 'Read-only grey style missing'
  Assert (-not $UI.Templates.IsEnabled -and -not $UI.Import.IsEnabled -and -not $UI.Start.IsEnabled -and -not $UI.DeleteTemplate.IsEnabled) 'Job inputs can be changed'
  $script:EditTitle=$null;$script:EditResult='수정하면 안 됨'
  DoubleClick $State.table.Cells.P0003.Button
  & $State.table.EditValue $State.rows[0]
  Assert ($null -eq $script:EditTitle -and $State.rows[0].value -eq '이번 문서 이름') 'Read-only value opened editor'
  $group=@($State.table.Groups.Values)[0];Click $group
  Assert ($State.table.Cells.Count -eq 0) 'Read-only tree could not collapse'
  Click @($State.table.Groups.Values)[0]
  Assert ($State.table.Cells.Count -eq 2) 'Read-only tree could not expand'
  Save-Design $Dialog '02-running-readonly'
  $UI.WritingPage.ScrollToBottom();Save-Design $Dialog '02-running-readonly-values';$UI.WritingPage.ScrollToTop()
  Click $UI.Back;Assert ($State.page -eq 1 -and -not $UI.Back.IsEnabled) 'Back boundary incorrect'
  Click $UI.Next;Assert ($State.page -eq 2) 'Next did not return to locked inputs'
  $script:MockJob=@{status='running';title='검증 과제';phase='공개 자료 검색·원문 확인 중 · 이번 소주제 웹 작업 3회 완료';completed=@('s1');total=2;current_topic='2. 추진 내용';error=''}
  & $Actions.Poll
  Assert ($UI.JobProgress.Value -eq 47 -and $State.page -eq 2 -and -not $UI.Logout.IsEnabled) 'Poll stole review page or unlocked account'
  Click $UI.Next;Assert ($State.page -eq 3) 'Next did not return to progress'
  Save-Design $Dialog '03-progress'
  $script:MockJob.status='failed';$script:MockJob.error='연결이 끊겼습니다.'
  & $Actions.Poll
  Assert ($UI.Resume.Visibility -eq 'Visible' -and $UI.JobError.Text) 'Failure recovery hidden'
  Click $UI.EditAgain
  Assert ($State.job -eq 'job' -and $State.page -eq 2 -and $UI.ProjectTitle.IsReadOnly) 'Failure bypass unlocked job'
  Click $UI.Next
  Click $UI.Resume
  Assert ($State.busy -and $UI.Resume.Visibility -eq 'Collapsed') 'Resume failed'
  Assert ($State.autoOpenJob -eq 'job' -and $script:OpenedOutputs.Count -eq 0) 'Resume did not arm completion-only opening'
  Click $UI.Step2Card
  $script:MockJob=@{status='completed';title='검증 과제';phase='저장 완료';completed=@('s1','s2');total=2;hwp_path='unused.hwp';input_summary=@(@{value='이번 문서 이름'},@{value='이번 문서 이름'},@{value='010-1234-1234'});review=@('사실 확인 필요')}
  & $Actions.Poll
  Assert ($State.page -eq 2 -and $UI.Step4Card.IsEnabled) 'Completion stole the active review page'
  Assert ($script:OpenedOutputs.Count -eq 1 -and $script:OpenedOutputs[0] -eq 'unused.hwp' -and -not $State.autoOpenJob) 'Completed job did not open exactly its output'
  Assert (-not $UI.Open.IsEnabled -and $State.outputOperation) 'Duplicate open not blocked while pending'
  Click $UI.Open
  Assert ($script:OpenedOutputs.Count -eq 1) 'Pending open started twice'
  & $Actions.Poll;& $Actions.Poll
  Assert ($script:OpenedOutputs.Count -eq 1) 'Repeated status polling reopened output'
  $State.jobStatus=$null;& $Actions.Poll
  Assert ($script:OpenedOutputs.Count -eq 1) 'Previously completed job auto-opened on reload'
  Click $UI.Step4Card
  Assert ($State.page -eq 4 -and $UI.CompletePage.Visibility -eq 'Visible') 'Completion page not shown'
  Assert ($UI.ProgressPage.Visibility -eq 'Collapsed' -and $UI.Navigation.Visibility -eq 'Visible' -and $UI.Steps.Visibility -eq 'Visible') 'Completion navigation missing'
  Assert (-not $UI.Next.IsEnabled -and $UI.Back.IsEnabled) 'Completion boundary incorrect'
  Assert ($UI.CompletionSummary.Text.Contains('3 개 칸') -and $UI.CompletionSummary.Text.Contains('2 개 항목')) 'Completion work summary inaccurate'
  $script:MockJob.research_enabled=$true
  $script:MockJob.research_summary=@{completed_topics=2;source_count=4;web_actions=6}
  & $Actions.Poll
  Assert ($UI.CompletionSummary.Text.Contains('참고 출처 4개')) 'Research summary missing'
  $script:OpenFailure=$true;$State.autoOpenJob='job';& $Actions.Poll
  Assert ($script:OpenedOutputs.Count -eq 2 -and $UI.OutputOpenError.Text.Contains('synthetic open failure')) 'Auto-open error not displayed'
  & $Actions.Poll
  Assert ($script:OpenedOutputs.Count -eq 2 -and $UI.OutputOpenError.Text.Contains('synthetic open failure')) 'Polling erased error or retried failed open'
  $script:OpenFailure=$false;Click $UI.Open;& $Actions.Poll
  Assert ($script:OpenedOutputs.Count -eq 3 -and -not $UI.OutputOpenError.Text) 'Manual retry did not open or clear error'
  Save-Design $Dialog '04-complete'
  Save-Design $Dialog '04-complete-compact' 800 650
  $UI.CompletePage.Parent.ScrollToBottom();Save-Design $Dialog '04-complete-compact-bottom' 800 650
  $UI.CompletePage.Parent.ScrollToTop()
  Click $UI.Step2Card;& $Actions.Poll;& $Actions.Poll
  Assert ($State.page -eq 2 -and $UI.Description.IsReadOnly -and $State.table.ReadOnly) 'Completed poll stole input view or unlocked values'
  Click $UI.Next;& $Actions.Poll
  Assert ($State.page -eq 3 -and $UI.Next.IsEnabled) 'Completed progress page not reviewable'
  Click $UI.Next;Assert ($State.page -eq 4) 'Next failed to reach completed output'
  # A completed job reopened in another window must show its saved data, not the current profile/form.
  $State.snapshotJob=$null
  $script:MockJob.template_id='archived';$script:MockJob.template_name='삭제된 양식의 작업 사본'
  $script:MockJob.brief=@{title='저장된 작업 주제';description='시작 당시의 세부 내용'}
  $script:MockJob.input_snapshot=@([pscustomobject]@{id='old';field_ids=@('old');label='이름';path=@('담당자','이름');context='담당자 > 이름';value='과거 저장값';ai=$false})
  & $Actions.Poll;Click $UI.Step2Card
  Assert ($UI.ProjectTitle.Text -eq '저장된 작업 주제' -and $UI.Description.Text -eq '시작 당시의 세부 내용' -and $State.rows[0].value -eq '과거 저장값') 'Saved snapshot did not replace unrelated screen data'
  Assert ($UI.Templates.SelectedItem.id -eq 'archived' -and $State.table.ReadOnly) 'Archived template not displayed read-only'
  # A new form with no saved values must still allow writing with only two inputs.
  $State.job=$null;$State.snapshotJob=$null;$State.jobStatus=$null;$State.output=$null;$State.prepared=$null;$script:MockRows=@();$UI.Templates.SelectedItem=@($UI.Templates.ItemsSource | Where-Object {$_.id -eq 'new'})[0];& $Actions.Page 1
  Click $UI.Next;& $Actions.Poll
  Assert ($State.page -eq 2 -and $State.rows.Count -eq 0 -and $State.table.Cells.Count -eq 0) ('Empty saved profile blocked: '+$UI.Notice.Text)
  Assert ($UI.Start.IsEnabled) 'Missing personal values became required'
  Click $UI.Start
  Assert (@($script:Created.local_values.PSObject.Properties).Count -eq 0) 'Empty profile added hidden fields'
  Assert ($State.autoOpenJob -eq 'job') 'New job did not arm auto-open'
  Assert (@($script:Calls | Where-Object {$_.action -eq 'authoring_profile_save'}).Count -eq 0) 'Optional edits mutated saved profile'
  $State.job=$null;$State.busy=$false;$State.prepared=$null;& $Actions.Refresh
  $State.connected=$false;$script:MockAccount=@{connected=$false};$State.snapshotJob=$null;$State.jobStatus=$null;& $Actions.Page 1;& $Actions.Update
  Assert ($UI.LoadResponses.IsEnabled) 'Saved response button requires AI login'
  & $Actions.LoadResponses 'C:\synthetic\responses.json';& $Actions.Poll
  Assert ($State.page -eq 2 -and $State.replay.sha256 -eq 'verified') ('Replay preparation failed: '+$UI.Notice.Text)
  Assert ($UI.ProjectTitle.IsReadOnly -and $UI.Description.IsReadOnly -and $UI.ProjectTitle.Text -eq '저장된 응답 주제') 'Replay subject not preserved'
  Assert ($UI.Start.IsEnabled -and -not $State.connected) 'Offline start disabled'
  Save-Design $Dialog '02-saved-response'
  Click $UI.Start
  Assert ($script:Created.action -eq 'authoring_create_replay' -and $script:Created.sha256 -eq 'verified') ('Replay invoked wrong action: '+$UI.Notice.Text)
  Assert (-not $UI.LoadResponses.IsEnabled -and $State.page -eq 3) 'Replay inputs not locked while running'
  $script:MockJob=@{status='completed';execution_mode='saved_response';title='저장된 응답 주제';phase='저장 완료';completed=@('s1','s2');total=2;hwp_path='unused.hwp';input_summary=@();review=@()}
  & $Actions.Poll
  Assert ($UI.CompletionSummary.Text.Contains('외부 AI 호출은 하지 않았습니다')) 'Offline completion message missing'
  & $Actions.Poll
  $State.job=$null;$State.busy=$false;$State.prepared=$null;$State.jobStatus=$null;& $Actions.ClearResponses;& $Actions.Refresh
  for($remove=0;$remove -lt 3 -and $UI.Templates.Items.Count -gt 0;$remove++){Click $UI.DeleteTemplate}
  Assert ($UI.Templates.Items.Count -eq 0 -and -not $UI.DeleteTemplate.IsEnabled) 'Last template deletion did not leave an empty safe list'
  Assert (-not $UI.Step2Card.IsEnabled -and -not $State.editing) 'Empty template list retained writable navigation'
  'AUTHORING_WORKFLOW_OK: two inputs; saved-only rows; duplicate fan-out; optional edits; progress; recovery; completion; empty profile'
 }catch{Write-Output $_.ScriptStackTrace;throw}finally{$State.closing=$true;$Timer.Stop();$Dialog.Close()}
}
$Source=[IO.File]::ReadAllText((Join-Path $Project 'document_authoring_flow_ui.ps1'),[Text.Encoding]::UTF8)
$Source=$Source.Replace("Show-WorkspaceWindow `$Dialog 'authoring'",'Invoke-AuthoringWorkflowProbe $Dialog $UI $State $Actions $Timer')
. ([scriptblock]::Create($Source))
Show-DocumentAuthoring $null
