# Two input stages plus progress/result navigation; started jobs are read-only.
function Show-DocumentAuthoring($OwnerWindow) {
    [xml]$Markup=@'
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" Title="문서 작성 · 범정부오피스" Width="1040" Height="820" MinWidth="780" MinHeight="600" WindowStartupLocation="CenterOwner" Background="#F4F2F7" FontFamily="맑은 고딕" FontSize="13" Foreground="#302938">
 <Window.Resources>
  <Style TargetType="Button"><Setter Property="Padding" Value="16,10"/><Setter Property="Margin" Value="0,0,8,0"/><Setter Property="Background" Value="White"/><Setter Property="Foreground" Value="#604878"/><Setter Property="BorderBrush" Value="#DCD3E5"/><Setter Property="Cursor" Value="Hand"/><Style.Triggers><Trigger Property="IsEnabled" Value="False"><Setter Property="Opacity" Value="0.45"/></Trigger></Style.Triggers></Style>
  <Style x:Key="Primary" TargetType="Button" BasedOn="{StaticResource {x:Type Button}}"><Setter Property="Background" Value="#705291"/><Setter Property="Foreground" Value="White"/><Setter Property="FontWeight" Value="SemiBold"/></Style>
  <Style TargetType="TextBox"><Setter Property="Padding" Value="12"/><Setter Property="Margin" Value="0,8,0,18"/><Setter Property="BorderBrush" Value="#DDD5E6"/><Setter Property="Background" Value="White"/><Style.Triggers><Trigger Property="IsReadOnly" Value="True"><Setter Property="Background" Value="#ECEDEF"/><Setter Property="Foreground" Value="#60646C"/><Setter Property="BorderBrush" Value="#D1D4D9"/></Trigger></Style.Triggers></Style>
  <Style TargetType="TextBlock"><Setter Property="TextWrapping" Value="Wrap"/></Style>
 </Window.Resources>
 <Grid Margin="28"><Grid.RowDefinitions><RowDefinition Height="Auto"/><RowDefinition Height="Auto"/><RowDefinition Height="*"/><RowDefinition Height="Auto"/></Grid.RowDefinitions>
  <Grid Margin="0,0,0,20"><Grid.ColumnDefinitions><ColumnDefinition Width="*"/><ColumnDefinition Width="Auto"/></Grid.ColumnDefinitions>
   <StackPanel><TextBlock Text="서울과학기술대학교" FontSize="12" Foreground="#82718F"/><TextBlock Text="문서 작성" FontSize="28" FontWeight="SemiBold" Margin="0,4"/></StackPanel>
   <StackPanel x:Name="AccountPanel" Grid.Column="1" MaxWidth="380"><TextBlock x:Name="Account" Text="AI 연결 확인 중" Margin="0,0,0,8"/><WrapPanel><Button x:Name="Login" Content="AI 로그인"/><Button x:Name="Check" Content="연결 확인"/><Button x:Name="Logout" Content="연결 해제"/></WrapPanel></StackPanel>
  </Grid>
  <UniformGrid x:Name="Steps" Grid.Row="1" Columns="4" Margin="0,0,0,16"><Button x:Name="Step1Card" Content="01  양식 선택"/><Button x:Name="Step2Card" Content="02  작성 내용"/><Button x:Name="Step3Card" Content="03  작업 진행"/><Button x:Name="Step4Card" Content="04  완료"/></UniformGrid>
  <Border Grid.Row="2" Background="White" CornerRadius="12" BorderBrush="#E2DBE9" BorderThickness="1" Padding="24"><Grid>
   <ScrollViewer x:Name="ChoosePage" VerticalScrollBarVisibility="Auto"><StackPanel>
    <TextBlock Text="어떤 양식으로 작성할까요?" FontSize="22" FontWeight="SemiBold"/>
    <TextBlock Text="양식을 선택하세요. 작성요령과 입력 위치는 프로그램이 준비합니다." Margin="0,10,0,20" Foreground="#776D81"/>
    <ComboBox x:Name="Templates" DisplayMemberPath="name" MinHeight="40" Margin="0,0,0,18"/>
    <WrapPanel><Button x:Name="Import" Content="문서 작성용 양식 등록"/><Button x:Name="Builtin" Content="기후부 기본 양식 추가"/><Button x:Name="DeleteTemplate" Content="선택한 양식 삭제" Foreground="#A33643"/></WrapPanel>
    <WrapPanel Margin="0,12,0,0"><Button x:Name="ExtractGuides" Content="소주제·작성요령 파일 추출"/><Button x:Name="ReconnectBody" Content="본문 작성 위치 다시 연결"/></WrapPanel>
    <WrapPanel Margin="0,12,0,0"><Button x:Name="LoadResponses" Content="저장된 AI 응답으로 작성"/><Button x:Name="ClearResponses" Content="응답 선택 해제" Visibility="Collapsed"/></WrapPanel>
    <TextBlock x:Name="ReplayInfo" Text="저장된 응답 파일을 불러오면 AI 호출 없이 동일한 문단·표 서식과 검사 기능으로 한글 파일을 만듭니다." Margin="0,10,0,0" Foreground="#604878"/>
    <TextBlock Text="양식 등록: AI가 소주제·작성요령과 빈 입력칸의 용도를 판정합니다. 불확실한 칸만 문맥을 더해 재검토하고, 남은 항목은 원본 그대로 둡니다. 작성 내용을 입력한 뒤 시작하면 자료조사와 본문 작성을 진행합니다. 등록 시 양식 원문이 연결된 AI로 전달되며 계정 사용량이 발생합니다." Margin="0,12,0,0" Foreground="#776D81"/>
    <TextBlock Text="AI가 원문에서 소주제와 작성요령만 찾고, 프로그램이 해당 원문을 Markdown(.md) 파일에 그대로 옮깁니다. 요약·본문 작성·공통 요령 재분류는 하지 않습니다. 문서 원문이 연결된 AI에 전달되며 계정 사용량이 발생합니다. 기존 등록 양식과 작업은 변경하지 않습니다." Margin="0,12,0,0" Foreground="#776D81"/>
    <Button x:Name="OpenGuideFile" Content="추출한 작성요령 파일 열기" Visibility="Collapsed" HorizontalAlignment="Left" Margin="0,12,0,0"/>
    <TextBlock x:Name="TemplateInfo" Margin="0,18" Foreground="#776D81"/>
    <Button x:Name="CancelAnalysis" Content="작성요령 추출 중단" Visibility="Collapsed" HorizontalAlignment="Left" Margin="0,0,0,12"/>
    <Expander x:Name="GuideOutline" Header="주제별 작성요령 보기" Visibility="Collapsed" Margin="0,0,0,14">
     <TreeView x:Name="GuideTree" MaxHeight="320" BorderThickness="0" ScrollViewer.HorizontalScrollBarVisibility="Disabled"/>
    </Expander>
    <Expander x:Name="AnalysisReview" Header="자동 판단이 어려운 항목 확인" Visibility="Collapsed" IsExpanded="True"><StackPanel>
     <TextBlock Text="자동 재검토 뒤에도 애매한 위치만 표시합니다. 선택하지 않은 항목은 원본 그대로 둡니다. 필요한 항목만 지정하세요. 확인 결과는 기존 양식을 바꾸지 않고 새 등록본으로 저장합니다." Margin="0,8"/>
     <StackPanel x:Name="AnalysisRows"/>
     <Button x:Name="ApplyAnalysis" Content="선택한 항목 적용" HorizontalAlignment="Left" Margin="0,10"/>
    </StackPanel></Expander>
    <Expander Header="이전 작업 이어보기" Margin="0,20,0,0"><ComboBox x:Name="Jobs" DisplayMemberPath="title" MinHeight="36" Margin="0,12"/></Expander>
   </StackPanel></ScrollViewer>
   <ScrollViewer x:Name="WritingPage" Visibility="Collapsed" VerticalScrollBarVisibility="Auto"><StackPanel>
    <TextBlock x:Name="WritingTitle" Text="무엇을 작성할까요?" FontSize="22" FontWeight="SemiBold"/>
    <TextBlock x:Name="WritingIntro" Text="아래 두 가지만 입력하세요. 나머지는 작성된 한글 파일에서 확인하고 수정하면 됩니다." Margin="0,10,0,20" Foreground="#776D81"/>
    <TextBlock Text="작성 주제" FontWeight="SemiBold"/><TextBox x:Name="ProjectTitle"/>
    <TextBlock Text="주제 세부 내용" FontWeight="SemiBold"/>
    <TextBox x:Name="Description" Height="100" AcceptsReturn="True" TextWrapping="Wrap" VerticalScrollBarVisibility="Auto"/>
    <TextBlock Text="목적과 원하는 내용을 자유롭게 적어 주세요. 확정된 기간·예산·근거가 있으면 함께 적어 주세요. 없는 사실은 임의로 만들지 않습니다." Foreground="#776D81" Margin="0,0,0,16"/>
    <Expander x:Name="PersonalInfo" Header="개인 탭에서 가져온 정보 · 필요한 경우에만 수정" IsExpanded="True">
     <StackPanel><TextBlock x:Name="InputHelp" Text="저장된 값만 중복 없이 표시합니다. 값을 더블클릭하면 이번 문서에 넣을 값만 수정됩니다. 같은 정보가 필요한 모든 칸에 반영됩니다." Margin="0,10" Foreground="#776D81"/>
      <ScrollViewer Height="180" HorizontalScrollBarVisibility="Auto" VerticalScrollBarVisibility="Auto"><Grid x:Name="Inputs" Background="White" VerticalAlignment="Top"/></ScrollViewer>
     </StackPanel>
    </Expander>
   </StackPanel></ScrollViewer>
   <ScrollViewer Visibility="{Binding Visibility, ElementName=ProgressPage}" VerticalScrollBarVisibility="Auto"><StackPanel x:Name="ProgressPage" Visibility="Collapsed" VerticalAlignment="Center">
    <TextBlock Text="문서를 작성하고 있습니다" FontSize="24" FontWeight="SemiBold"/>
    <TextBlock x:Name="JobTitle" FontSize="17" Margin="0,12,0,26"/>
    <Border x:Name="PhaseCard" Background="#F1EBF7" Padding="20" CornerRadius="10"><StackPanel>
     <TextBlock x:Name="PhaseText" FontSize="18" FontWeight="SemiBold"/><TextBlock x:Name="TopicText" Margin="0,12"/>
     <ProgressBar x:Name="JobProgress" Height="12" Maximum="100" Foreground="#80629E"/>
     <TextBlock x:Name="PercentText" Margin="0,10"/>
     <ProgressBar x:Name="PhaseSpinner" Height="3" IsIndeterminate="True" Foreground="#80629E"/>
    </StackPanel></Border>
    <TextBlock x:Name="JobError" Foreground="#A33643" Margin="0,18"/>
    <WrapPanel><Button x:Name="Stop" Content="작성 중단"/><Button x:Name="Resume" Content="이어서 작성" Visibility="Collapsed"/><Button x:Name="EditAgain" Content="입력 내용 확인" Visibility="Collapsed"/></WrapPanel>
   </StackPanel></ScrollViewer>
   <ScrollViewer Visibility="{Binding Visibility, ElementName=CompletePage}" VerticalScrollBarVisibility="Auto"><StackPanel x:Name="CompletePage" Visibility="Collapsed" VerticalAlignment="Center">
    <TextBlock Text="한글 파일을 만들었습니다" FontSize="25" FontWeight="SemiBold" Foreground="#53745E"/>
    <TextBlock x:Name="CompletionSummary" FontSize="15" Margin="0,24" LineHeight="27"/>
    <Button x:Name="Open" Content="최종 출력본 한글 파일 열기" Style="{StaticResource Primary}" HorizontalAlignment="Left"/>
    <TextBlock x:Name="OutputOpenError" Foreground="#A33643" Margin="0,12,0,0"/>
   </StackPanel></ScrollViewer>
  </Grid></Border>
  <StackPanel Grid.Row="3" Margin="0,14,0,0">
   <Border x:Name="ReadOnlyNotice" Visibility="Collapsed" Background="#E7E9EC" CornerRadius="6" Padding="12,8" Margin="0,0,0,10"><TextBlock Text="작업 시작 당시의 입력 내용입니다. 회색 영역은 확인만 가능하며 수정할 수 없습니다." Foreground="#555C66"/></Border>
   <TextBlock x:Name="Notice" Foreground="#926023" Margin="0,0,0,8"/>
   <TextBlock x:Name="Disclosure" Visibility="Collapsed" Text="주제·세부 내용과 작성요령을 외부 AI에 전달해 공개 자료를 조사·분석한 뒤 작성합니다. 조사에는 추가 시간과 계정 사용량이 들 수 있습니다. 저장 정보는 별도 전송하지 않지만 양식 원문의 개인정보는 포함될 수 있습니다." Foreground="#776D81" Margin="0,0,0,12"/>
   <Grid x:Name="Navigation"><Grid.ColumnDefinitions><ColumnDefinition Width="*"/><ColumnDefinition Width="Auto"/></Grid.ColumnDefinitions>
    <Button x:Name="Back" Content="이전" HorizontalAlignment="Left"/>
    <StackPanel Grid.Column="1" Orientation="Horizontal"><Button x:Name="Next" Content="다음" Style="{StaticResource Primary}"/><Button x:Name="Start" Content="문서 작성 시작" Style="{StaticResource Primary}" Visibility="Collapsed"/></StackPanel>
   </Grid>
  </StackPanel>
 </Grid>
</Window>
'@
    $Dialog=[Windows.Markup.XamlReader]::Load([System.Xml.XmlNodeReader]::new($Markup));$Dialog.Owner=$OwnerWindow
    $area=[System.Windows.SystemParameters]::WorkArea;$Dialog.MinWidth=[Math]::Min(780,$area.Width-24);$Dialog.MinHeight=[Math]::Min(600,$area.Height-24);$Dialog.Width=[Math]::Min(1040,$area.Width-24);$Dialog.Height=[Math]::Min(820,$area.Height-24)
    $UI=@{};foreach($name in @('AccountPanel','Account','Login','Check','Logout','Steps','Step1Card','Step2Card','Step3Card','Step4Card','ChoosePage','Templates','Import','Builtin','TemplateInfo','Jobs','WritingPage','ProjectTitle','Description','PersonalInfo','InputHelp','Inputs','ReadOnlyNotice','Disclosure','ProgressPage','JobTitle','PhaseCard','PhaseText','TopicText','JobProgress','PercentText','PhaseSpinner','JobError','Stop','Resume','EditAgain','CompletePage','CompletionSummary','Open','Notice','Navigation','Back','Next','Start')){$UI[$name]=$Dialog.FindName($name)}
    $State=@{page=1;operation=$null;operationAction='';job=$null;snapshotJob=$null;jobStatus=$null;busy=$false;polling=$false;closing=$false;connected=$false;prepared=$null;rows=@();output=$null;loginUrl=$null;refreshing=$false;editing=$false}
    foreach($name in @('WritingTitle','WritingIntro')){$UI[$name]=$Dialog.FindName($name)}
    foreach($name in @('AnalysisReview','AnalysisRows','ApplyAnalysis','CancelAnalysis','GuideOutline','GuideTree','DeleteTemplate','OpenGuideFile')){$UI[$name]=$Dialog.FindName($name)}
    foreach($name in @('ExtractGuides','ReconnectBody')){$UI[$name]=$Dialog.FindName($name)}
    foreach($name in @('LoadResponses','ClearResponses','ReplayInfo')){$UI[$name]=$Dialog.FindName($name)}
    $State.replay=$null
    $aiDisclosure=$UI.Disclosure.Text
    $Actions=@{}
    $UI.OutputOpenError=$Dialog.FindName('OutputOpenError')
    $State.autoOpenJob=$null
    $State.outputOperation=$null
    $Actions.OpenOutput={
        if($State.outputOperation){return}
        try{
            $request=& $Actions.LaunchOutput $State.output
            if(-not $request.operation_id){throw '한글 파일 열기 작업을 시작하지 못했습니다.'}
            $State.outputOperation=$request.operation_id;$UI.Open.IsEnabled=$false
            $UI.OutputOpenError.Text='한글에서 출력본을 열고 확인하고 있습니다.'
        }
        catch{$UI.OutputOpenError.Text='한글 파일을 열지 못했습니다. 아래 경로의 파일을 확인하거나 열기 버튼으로 다시 시도하세요.'+"`n"+$State.output+"`n"+$_.Exception.Message}
    }.GetNewClosure()
    $Call={param($command) $r=Send-Backend $command;if(-not $r.ok){throw $r.message};return $r.result}.GetNewClosure()
    $Actions.LaunchOutput={param($path) & $Call @{action='authoring_open_output';job_id=$State.job}}.GetNewClosure()
    $Actions.Update={
        $free=(-not $State.operation -and -not $State.outputOperation -and -not $State.busy -and -not $State.editing)
        $UI.Open.IsEnabled=(-not $State.operation -and -not $State.outputOperation -and $State.jobStatus -eq 'completed' -and [bool]$State.output)
        $ready=$State.prepared -and $UI.Templates.SelectedItem.id -eq $State.prepared
        $locked=[bool]$State.job;$nav=(-not $State.operation -and -not $State.editing)
        foreach($n in @('Templates','Import','Builtin')){$UI[$n].IsEnabled=($free -and -not $locked)}
        $UI.Import.IsEnabled=($free -and -not $locked -and $State.connected)
        $UI.ExtractGuides.IsEnabled=$UI.Import.IsEnabled
        $UI.ReconnectBody.IsEnabled=($UI.Import.IsEnabled -and $null -ne $UI.Templates.SelectedItem -and
            (-not $UI.Templates.SelectedItem.has_slot_audit -or $UI.Templates.SelectedItem.can_recheck_slots))
        $UI.ReconnectBody.Content=if($UI.Templates.SelectedItem.has_slot_audit){'불확실한 입력칸만 AI 재검토'}else{'본문 작성 위치 다시 연결'}
        $UI.ReconnectBody.ToolTip=if($UI.Templates.SelectedItem.has_slot_audit){'저장된 확정 판정은 재사용하고 남은 입력칸만 AI에 다시 보냅니다. 기존 양식과 작업은 보존합니다.'}else{'양식을 다시 읽고 작성 위치를 새 등록본으로 연결합니다.'}
        $UI.DeleteTemplate.IsEnabled=($free -and -not $locked -and $null -ne $UI.Templates.SelectedItem)
        $UI.LoadResponses.IsEnabled=($free -and -not $locked -and $null -ne $UI.Templates.SelectedItem)
        $UI.ClearResponses.IsEnabled=($free -and -not $locked)
        $UI.ClearResponses.Visibility=if($State.replay -and -not $locked){'Visible'}else{'Collapsed'}
        $UI.Import.ToolTip=if($State.connected){'AI가 소주제·작성요령과 빈 입력칸을 분석하고, 불확실한 칸만 한 번 더 확인합니다. 자료조사와 본문 작성은 작성 내용 입력 후 진행합니다.'}else{'양식을 등록할 AI 계정을 먼저 연결해 주세요.'}
        $UI.AnalysisReview.IsEnabled=($free -and -not $locked)
        $UI.GuideOutline.IsEnabled=(-not $State.operation)
        $UI.CancelAnalysis.Visibility=if($State.operation -and $State.operationAction -in @('authoring_register_file','authoring_extract_guides','authoring_reanalyze_template')){'Visible'}else{'Collapsed'}
        $UI.CancelAnalysis.Content='양식 분석·작성요령 추출 중단'
        $UI.Jobs.IsEnabled=$free
        foreach($n in @('ProjectTitle','Description')){$UI[$n].IsEnabled=(-not $State.operation);$UI[$n].IsReadOnly=($locked -or [bool]$State.replay)}
        $UI.Inputs.IsEnabled=(-not $State.operation)
        if($State.table){$State.table.ReadOnly=$locked}
        $UI.Templates.Background=if($locked){'#ECEDEF'}else{'White'}
        $UI.Step1Card.IsEnabled=$nav;$UI.Back.IsEnabled=($nav -and $State.page -gt 1)
        $UI.Step2Card.IsEnabled=($nav -and $(if($locked){$State.snapshotJob -eq $State.job}else{$ready}))
        $UI.Step3Card.IsEnabled=($nav -and $locked)
        $UI.Step4Card.IsEnabled=($nav -and $locked -and $State.jobStatus -eq 'completed' -and [bool]$State.output)
        $UI.Next.IsEnabled=($nav -and $(switch($State.page){1 {$UI.Step2Card.IsEnabled -or (-not $locked -and $null -ne $UI.Templates.SelectedItem)};2 {$UI.Step3Card.IsEnabled};3 {$UI.Step4Card.IsEnabled};default {$false}}))
        $UI.Start.IsEnabled=($free -and -not $locked -and $ready -and ($State.connected -or [bool]$State.replay) -and -not [string]::IsNullOrWhiteSpace($UI.ProjectTitle.Text) -and -not [string]::IsNullOrWhiteSpace($UI.Description.Text))
        $UI.Start.Content=if($State.replay){'저장된 응답으로 한글 만들기'}else{'문서 작성 시작'}
        if(-not $State.connected){$UI.Account.Text=if($State.replay){'○ 저장 응답 사용 · AI 연결 불필요'}else{'○ AI 연결 필요'}}
        $UI.Disclosure.Text=if($State.replay){'AI 호출·새 자료조사·재요약 없이 저장된 응답을 사용합니다. 문단·표 정렬, 확인 메모, 출력 검사는 동일합니다. 메모에는 확인할 내용과 확인 방법이 연결됩니다. 원래 응답이 셀 분량을 넘으면 잘라내지 않고 검토 사항으로 표시합니다.'}else{$aiDisclosure}
        $UI.Login.IsEnabled=($free -and -not $State.connected);$UI.Logout.IsEnabled=($free -and $State.connected);$UI.Check.IsEnabled=$free
        $UI.ReadOnlyNotice.Visibility=if($locked -and $State.page -le 2){'Visible'}else{'Collapsed'}
        $UI.Start.Visibility=if($State.page -eq 2 -and -not $locked){'Visible'}else{'Collapsed'}
        $UI.Disclosure.Visibility=if($State.page -eq 2 -and -not $locked){'Visible'}else{'Collapsed'}
        $UI.PersonalInfo.Header=if($locked){'작업에 사용한 저장 정보 · 확인 전용'}else{'개인 탭에서 가져온 정보 · 필요한 경우에만 수정'}
        $UI.WritingTitle.Text=if($locked){'작업에 사용한 입력 내용'}else{'무엇을 작성할까요?'}
        $UI.WritingIntro.Text=if($locked){'시작 당시의 내용을 확인할 수 있습니다. 다른 단계를 보는 동안에도 작업은 계속 진행됩니다.'}else{'아래 두 가지만 입력하세요. 나머지는 작성된 한글 파일에서 확인하고 수정하면 됩니다.'}
        $UI.InputHelp.Text=if($locked){'작업 시작 때 확정된 값입니다. 항목을 펼치거나 열 너비를 조절해서 확인할 수 있으며 값은 수정할 수 없습니다.'}else{'저장된 값만 중복 없이 표시합니다. 값을 더블클릭하면 이번 문서에 넣을 값만 수정됩니다. 같은 정보가 필요한 모든 칸에 반영됩니다.'}
        if($State.replay -and -not $locked){$UI.WritingIntro.Text='저장된 응답의 주제·내용입니다. AI를 다시 호출하지 않으므로 주제는 읽기 전용입니다. 아래 입력 정보는 이번 출력에 한해 수정할 수 있습니다.';$UI.PersonalInfo.Header='응답 파일에 함께 저장된 입력 정보 · 필요한 경우 수정'}
    }.GetNewClosure()
    $Actions.Page={param([int]$page)
        & $Actions.Update
        if($page -lt 1 -or $page -gt 4 -or -not $UI["Step${page}Card"].IsEnabled){return}
        $State.page=$page
        foreach($pair in @(@('ChoosePage',1),@('WritingPage',2),@('ProgressPage',3),@('CompletePage',4))){$UI[$pair[0]].Visibility=if($page -eq $pair[1]){'Visible'}else{'Collapsed'}}
        foreach($n in @('Steps','Navigation','Notice')){$UI[$n].Visibility='Visible'}
        $UI.AccountPanel.Visibility=if($page -le 2){'Visible'}else{'Collapsed'}
        foreach($index in 1..4){$UI["Step${index}Card"].Background=if($page -eq $index){'#E8DFF1'}else{'White'}}
        & $Actions.Update
    }.GetNewClosure()
    $Actions.Account={param($account)
        $State.connected=[bool]$account.connected
        $UI.Account.Text=if($State.connected){'● '+$(if($account.email){$account.email}else{'AI 연결됨'})}else{'○ AI 연결 필요'}
        $UI.Account.Foreground=if($State.connected){'#417352'}else{'#776D81'}
    }.GetNewClosure()
    $Actions.Refresh={
        $data=& $Call @{action='authoring_overview'};& $Actions.Account $data.account
        $selected=$UI.Templates.SelectedItem;$State.refreshing=$true
        try{$UI.Templates.ItemsSource=@($data.templates);if($selected){$UI.Templates.SelectedItem=@($data.templates|Where-Object {$_.id -eq $selected.id})[0]};if($UI.Templates.SelectedIndex -lt 0 -and $data.templates.Count){$UI.Templates.SelectedIndex=0};$UI.Jobs.ItemsSource=@($data.jobs)}finally{$State.refreshing=$false}
        if($State.job){$State.snapshotJob=$null}
        & $Actions.ShowAnalysis
        & $Actions.Update
        if($data.template_warnings){$UI.Notice.Text="읽을 수 없는 양식 $(@($data.template_warnings).Count)개를 목록에서 제외했습니다. 원본은 유지됩니다. 접근 가능한 양식을 선택해 주세요."}
    }.GetNewClosure()
    $Actions.ShowAnalysis={
        if($UI.Templates.SelectedItem.guide_file){$State.guideFile=[string]$UI.Templates.SelectedItem.guide_file;$UI.OpenGuideFile.Visibility='Visible'}
        $UI.GuideOutline.Visibility=if($UI.Templates.SelectedItem.has_guide_outline){'Visible'}else{'Collapsed'}
        $guideKey="$($UI.Templates.SelectedItem.id):$($UI.Templates.SelectedItem.analysis_version)"
        if($State.guideKey -ne $guideKey){$UI.GuideOutline.IsExpanded=$false;$UI.GuideTree.Items.Clear();$State.guideKey=$null}
        $UI.AnalysisRows.Children.Clear();$State.analysisChoices=@{}
        $items=@($UI.Templates.SelectedItem.analysis_reviews | Where-Object {$null -ne $_})
        $UI.AnalysisReview.Visibility=if($items.Count -and -not $State.job){'Visible'}else{'Collapsed'}
        $UI.AnalysisReview.Header="자동 판단이 어려운 항목 $($items.Count)곳 확인 · 선택 사항"
        foreach($group in @($items | Group-Object {if($_.section){[string]$_.section}else{'기타 확인 항목'}})){
            $section=[Windows.Controls.Expander]::new();$section.Header="$($group.Name) · $(@($group.Group).Count)곳";$section.Margin='0,6,0,8';$section.IsExpanded=(@($group.Group).Count -le 3)
            $content=[Windows.Controls.StackPanel]::new()
            foreach($item in $group.Group){
                $panel=[Windows.Controls.StackPanel]::new();$panel.Margin='0,6,0,12'
                $text=[Windows.Controls.TextBlock]::new();$text.Text="문단 $($item.index) · $($item.label)`n$($item.context)`n확인 사유: $($item.reason)";$text.TextWrapping='Wrap';$panel.Children.Add($text)|Out-Null
                $select=[Windows.Controls.ComboBox]::new();$select.Margin='0,8,0,0';$select.MinHeight=34
                if($UI.Templates.SelectedItem.review_mode -eq 'guided_slots'){
                    if($item.topic_index -ge 0){$select.ItemsSource=@('선택 안 함 · 원본 유지','원본 유지로 확정','AI 본문 작성','사실값 입력','저장 정보 입력');$select.Tag=@('','preserve','body','factual','personal')}
                    else{$select.ItemsSource=@('선택 안 함 · 원본 유지','원본 유지로 확정','사실값 입력 위치 · 값 없으면 빈칸','저장 정보 입력');$select.Tag=@('','preserve','factual','personal')}
                }else{
                    $select.ItemsSource=if($item.writable){@('선택 안 함 · 원본 유지','원본 유지로 확정','AI 본문 작성','저장 정보 입력','빈칸으로 유지')}else{@('선택 안 함 · 원본 유지','원본 유지로 확정')}
                    $select.Tag=if($item.writable){@('','preserve','body','personal','blank')}else{@('','preserve')}
                }
                $select.SelectedIndex=0;$State.analysisChoices[[string]$item.index]=$select
                $panel.Children.Add($select)|Out-Null;$content.Children.Add($panel)|Out-Null
            }
            $section.Content=$content;$UI.AnalysisRows.Children.Add($section)|Out-Null
        }
    }.GetNewClosure()
    $Actions.ConfirmDeleteTemplate={param($name)
        [System.Windows.MessageBox]::Show($Dialog,"‘$name’ 양식을 등록 목록에서 삭제할까요?`n`n원래 선택한 한글 파일과 기존 작업·출력 문서는 유지됩니다.`n등록 사본은 복구할 수 있도록 삭제 보관 폴더로 옮깁니다. 이동에 실패하면 삭제하지 않습니다.",'등록 양식 삭제','YesNo','Warning','No') -eq 'Yes'
    }.GetNewClosure()
    $Actions.DeleteTemplate={
        if(-not $UI.DeleteTemplate.IsEnabled -or -not $UI.Templates.SelectedItem){return}
        $selected=$UI.Templates.SelectedItem;$State.editing=$true;& $Actions.Update
        try{
            if(-not (& $Actions.ConfirmDeleteTemplate $selected.name)){return}
            $result=& $Call @{action='authoring_delete_template';template_id=$selected.id;confirmed=$true}
            if(-not $result.deleted){throw '양식 삭제 결과를 확인할 수 없습니다.'}
            $State.prepared=$null;$State.rows=@();$State.guideKey=$null
            if($State.table){$State.table.Collapsed.Clear()}
            & $Actions.RenderInputs;& $Actions.Refresh
            $UI.TemplateInfo.Text='';$UI.Notice.Text='선택한 양식을 삭제했습니다. 기존 작업과 출력 문서는 유지되며, 등록 사본은 삭제 보관 폴더에 보관됩니다.'
        }catch{$UI.Notice.Text=$_.Exception.Message}finally{$State.editing=$false;& $Actions.Update}
    }.GetNewClosure()
    $UI.DeleteTemplate.Add_Click({& $Actions.DeleteTemplate}.GetNewClosure())
    $Actions.ShowGuideOutline={
        if($State.operation -or -not $UI.Templates.SelectedItem.has_guide_outline){return}
        $guideKey="$($UI.Templates.SelectedItem.id):$($UI.Templates.SelectedItem.analysis_version)"
        if($State.guideKey -eq $guideKey){return}
        $result=& $Call @{action='authoring_guide_outline';template_id=$UI.Templates.SelectedItem.id}
        $UI.GuideTree.Items.Clear()
        $node={param($title) $item=[Windows.Controls.TreeViewItem]::new();$label=[Windows.Controls.TextBlock]::new();$label.Text=[string]$title;$label.TextWrapping='Wrap';$label.MaxWidth=660;$item.Header=$label;return $item}
        if(@($result.outline.common_instructions | Where-Object {$null -ne $_}).Count){
            $common=& $node '공통 작성요령'
            foreach($rule in $result.outline.common_instructions){$common.Items.Add((& $node $rule.text))|Out-Null}
            $UI.GuideTree.Items.Add($common)|Out-Null
        }
        foreach($chapter in $result.outline.chapters){
            $major=& $node $chapter.title;$major.IsExpanded=$true
            if(@($chapter.instructions).Count){$rules=& $node '이 대주제의 공통 요령';foreach($rule in $chapter.instructions){$rules.Items.Add((& $node $rule.text))|Out-Null};$major.Items.Add($rules)|Out-Null}
            foreach($topic in $chapter.subtopics){$minor=& $node $topic.title;foreach($rule in $topic.instructions){$minor.Items.Add((& $node $rule.text))|Out-Null};$major.Items.Add($minor)|Out-Null}
            $UI.GuideTree.Items.Add($major)|Out-Null
        }
        $State.guideKey=$guideKey
    }.GetNewClosure()
    $UI.GuideOutline.Add_Expanded({try{& $Actions.ShowGuideOutline}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $Actions.Begin={param($command)
        if($State.operation -or $State.busy){return}
        if($State.job -and ($command.action -like 'authoring_register*' -or $command.action -eq 'authoring_prepare_inputs')){return}
        $r=& $Call $command;$State.operation=$r.operation_id;$State.operationAction=$command.action;$State.loginUrl=$null
        $UI.Notice.Text=switch($command.action){'authoring_prepare_inputs' {'저장된 개인정보를 연결하고 있습니다.'};{$_ -like 'authoring_register*'} {'양식과 작성요령을 저장하고 있습니다.'};default {'AI 연결을 확인하고 있습니다.'}}
        & $Actions.Update
    }.GetNewClosure()
    $Actions.LoadResponses={param($path)
        if(-not $UI.LoadResponses.IsEnabled){return}
        & $Actions.Begin @{action='authoring_prepare_replay';template_id=$UI.Templates.SelectedItem.id;path=$path}
        $UI.Notice.Text='저장된 응답과 선택한 양식의 입력 위치를 확인하고 있습니다. AI를 호출하지 않습니다.'
    }.GetNewClosure()
    $Actions.ClearResponses={
        if($State.job -or $State.busy -or $State.operation){return}
        $State.replay=$null;$State.prepared=$null;$State.rows=@();& $Actions.RenderInputs
        $UI.ReplayInfo.Text='저장된 응답 파일을 불러오면 AI 호출 없이 동일한 문단·표 서식과 검사 기능으로 한글 파일을 만듭니다.'
        & $Actions.Page 1
    }.GetNewClosure()
    $Actions.RenderInputs={$State.table.ReadOnly=[bool]$State.job;Show-AuthoringInputTable $State.table $State.rows}.GetNewClosure()
    $Actions.LoadSnapshot={param($job)
        $State.refreshing=$true
        try{
            $State.prepared=$job.template_id
            $selected=@($UI.Templates.ItemsSource|Where-Object {$_.id -eq $job.template_id})[0]
            if(-not $selected){$selected=[pscustomobject]@{id=$job.template_id;name=$job.template_name};$UI.Templates.ItemsSource=@($selected)+@($UI.Templates.ItemsSource)}
            $UI.Templates.SelectedItem=$selected
            $UI.ProjectTitle.Text=[string]$job.brief.title;$UI.Description.Text=[string]$job.brief.description
            $State.rows=@($job.input_snapshot);$State.table.Collapsed.Clear();$State.snapshotJob=$State.job
            & $Actions.RenderInputs
            $UI.TemplateInfo.Text='이 작업을 시작할 때 선택한 양식입니다. 작업에 저장된 입력 내용을 확인할 수 있습니다.'
        }finally{$State.refreshing=$false}
    }.GetNewClosure()
    $editValue={param($row)
        if($State.job -or $State.busy -or $State.operation -or $State.editing){return}
        $State.editing=$true
        try{$value=Read-ProfileTableText $Dialog ('이번 문서의 '+$row.label+' 수정') $row.value;if($null -ne $value){$row.value=[string]$value;& $Actions.RenderInputs}}catch{$UI.Notice.Text=$_.Exception.Message}finally{$State.editing=$false;& $Actions.Update}
    }.GetNewClosure()
    $State.table=@{Grid=$UI.Inputs;PersonalOnly=$true;Cells=@{};Groups=@{};Collapsed=[System.Collections.Generic.Dictionary[string,bool]]::new([StringComparer]::Ordinal);Select={};Changed={};EditName={};EditValue=$editValue;Render=$Actions.RenderInputs}
    $Actions.Start={
        & $Actions.Update;if(-not $UI.Start.IsEnabled){return}
        $values=@{};foreach($row in $State.rows){foreach($id in @($row.field_ids)){$values[[string]$id]=[string]$row.value}}
        $checked=& $Call @{action='authoring_validate_inputs';template_id=$State.prepared;local_values=$values}
        # Starting explicitly accepts the visible disclosure; no extra checkbox.
        if($State.replay){
            $r=& $Call @{action='authoring_create_replay';template_id=$State.prepared;path=$State.replay.path;sha256=$State.replay.sha256;local_values=$checked.values;input_snapshot=@($State.rows)}
        }else{
            $r=& $Call @{action='authoring_create';template_id=$State.prepared;brief=@{title=$UI.ProjectTitle.Text;description=$UI.Description.Text};local_values=$checked.values;input_snapshot=@($State.rows);review_mode='final_output';research_enabled=$true;external_consent=$true}
        }
        $State.job=$r.id;$State.snapshotJob=$r.id;$State.jobStatus='running';$State.output=$null;$State.busy=$true;$UI.JobTitle.Text=$UI.ProjectTitle.Text;$UI.PhaseText.Text='입력값을 채우고 작성을 준비합니다.';$UI.JobError.Text='';$UI.JobProgress.Value=0;$UI.PhaseSpinner.Visibility='Visible';$UI.Resume.Visibility='Collapsed';$UI.EditAgain.Visibility='Collapsed';$UI.Stop.Visibility='Visible'
        $State.autoOpenJob=$r.id;$UI.OutputOpenError.Text=''
        foreach($row in $State.rows){$row.value=[string]$checked.values.([string]$row.id)};& $Actions.RenderInputs
        & $Actions.Page 3
    }.GetNewClosure()
    $UI.ProjectTitle.Add_TextChanged({& $Actions.Update}.GetNewClosure());$UI.Description.Add_TextChanged({& $Actions.Update}.GetNewClosure())
    $UI.Step1Card.Add_Click({& $Actions.Page 1}.GetNewClosure());$UI.Back.Add_Click({& $Actions.Page ($State.page-1)}.GetNewClosure());$UI.Step2Card.Add_Click({& $Actions.Page 2}.GetNewClosure())
    $UI.Step3Card.Add_Click({& $Actions.Page 3}.GetNewClosure());$UI.Step4Card.Add_Click({& $Actions.Page 4}.GetNewClosure())
    $UI.Templates.Add_SelectionChanged({if($State.refreshing){return};if($UI.Templates.SelectedItem.id -ne $State.prepared){$State.prepared=$null;$State.rows=@();$State.replay=$null;$UI.ReplayInfo.Text='다른 양식에서는 응답 파일을 다시 불러와 입력 위치를 확인하세요.'};$UI.TemplateInfo.Text='작성요령에 맞춰 자료를 조사·분석하고, 실행 방안을 구성한 뒤 순서대로 본문을 작성합니다.';& $Actions.ShowAnalysis;& $Actions.Update}.GetNewClosure())
    $UI.ApplyAnalysis.Add_Click({try{
        if($State.job -or $State.operation -or $State.busy){return}
        $choices=@{}
        foreach($key in $State.analysisChoices.Keys){$select=$State.analysisChoices[$key];$index=$select.SelectedIndex;if($index -gt 0){$choices[$key]=@($select.Tag)[$index]}}
        if(-not $choices.Count){return}
        $result=& $Call @{action='authoring_analysis_resolve';template_id=$UI.Templates.SelectedItem.id;choices=$choices}
        $State.prepared=$null;$State.rows=@();& $Actions.Refresh
        if($result.id){$UI.Templates.SelectedItem=@($UI.Templates.ItemsSource|Where-Object {$_.id -eq $result.id})[0];& $Actions.ShowAnalysis}
        $UI.Notice.Text='선택한 처리 방식을 저장했습니다. 선택하지 않은 항목은 원본을 유지합니다.'
        if($result.derived_from_template_id){$UI.Notice.Text+=' 기존 양식은 보존하고 확인 결과를 새 양식으로 등록했습니다.'}
    }catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.CancelAnalysis.Add_Click({try{if($State.operation){$null=& $Call @{action='authoring_cancel_operation';operation_id=$State.operation};$UI.Notice.Text='추출 중단을 요청했습니다. 진행 중인 문서 읽기 또는 AI 요청을 정리하고 있습니다.'}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Next.Add_Click({try{if(-not $UI.Next.IsEnabled){return};if($State.page -eq 1 -and -not $State.job -and $State.prepared -ne $UI.Templates.SelectedItem.id){& $Actions.Begin @{action='authoring_prepare_inputs';template_id=$UI.Templates.SelectedItem.id}}else{& $Actions.Page ($State.page+1)}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Builtin.Add_Click({try{& $Actions.Begin @{action='authoring_register_builtin'}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Import.Add_Click({try{$picker=[Microsoft.Win32.OpenFileDialog]::new();$picker.Filter='한글 양식 (*.hwp)|*.hwp';if($picker.ShowDialog($Dialog)){& $Actions.Begin @{action='authoring_register_file';path=$picker.FileName}}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.LoadResponses.Add_Click({try{$picker=[Microsoft.Win32.OpenFileDialog]::new();$picker.Filter='저장된 AI 응답 (*.json)|*.json';if($picker.ShowDialog($Dialog)){& $Actions.LoadResponses $picker.FileName}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.ClearResponses.Add_Click({& $Actions.ClearResponses}.GetNewClosure())
    $UI.ExtractGuides.Add_Click({try{$picker=[Microsoft.Win32.OpenFileDialog]::new();$picker.Filter='한글 양식 (*.hwp)|*.hwp';if($picker.ShowDialog($Dialog)){& $Actions.Begin @{action='authoring_extract_guides';path=$picker.FileName}}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.ReconnectBody.Add_Click({try{if($UI.ReconnectBody.IsEnabled){& $Actions.Begin @{action='authoring_reanalyze_template';template_id=$UI.Templates.SelectedItem.id}}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.OpenGuideFile.Add_Click({try{
        if(-not $State.guideFile -or -not (Test-Path -LiteralPath $State.guideFile -PathType Leaf)){throw '추출한 파일을 찾지 못했습니다.'}
        Start-Process -FilePath $State.guideFile | Out-Null
    }catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Login.Add_Click({try{& $Actions.Begin @{action='authoring_login'}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure());$UI.Check.Add_Click({try{& $Actions.Begin @{action='authoring_connection_check'}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Logout.Add_Click({try{if([System.Windows.MessageBox]::Show($Dialog,'이 PC에서 공유하는 Codex 로그인도 해제됩니다. 연결을 해제할까요?','AI 연결 해제','YesNo','Question') -eq 'Yes'){& $Actions.Begin @{action='authoring_logout'}}}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Start.Add_Click({try{& $Actions.Start}catch{$UI.Notice.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Stop.Add_Click({try{$null=& $Call @{action='authoring_stop';job_id=$State.job}}catch{$UI.JobError.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.Resume.Add_Click({try{$null=& $Call @{action='authoring_resume';job_id=$State.job};$State.autoOpenJob=$State.job;$UI.OutputOpenError.Text='';$State.busy=$true;$UI.JobError.Text='';$UI.Resume.Visibility='Collapsed';$UI.EditAgain.Visibility='Collapsed';$UI.Stop.Visibility='Visible'}catch{$UI.JobError.Text=$_.Exception.Message}}.GetNewClosure())
    $UI.EditAgain.Add_Click({& $Actions.Page 2}.GetNewClosure())
    $UI.Open.Add_Click({& $Actions.OpenOutput}.GetNewClosure())
    $UI.Jobs.Add_SelectionChanged({if(-not $State.refreshing -and $UI.Jobs.SelectedItem -and -not $State.busy -and -not $State.operation){$State.job=$UI.Jobs.SelectedItem.id;$State.autoOpenJob=$null;$UI.OutputOpenError.Text='';$State.snapshotJob=$null;$State.jobStatus=$null;$State.output=$null;& $Actions.Page 3;& $Actions.Poll}}.GetNewClosure())
    $Actions.Poll={
        if($State.polling -or $State.closing -or $State.editing -or $script:BackendRequestInFlight){return};$State.polling=$true
        try{
            if($State.outputOperation){
                try{
                    $opened=& $Call @{action='authoring_operation';operation_id=$State.outputOperation}
                    if($opened.status -eq 'failed'){
                        $State.outputOperation=$null;$UI.OutputOpenError.Text='한글 파일을 열지 못했습니다: '+$opened.error
                    }elseif($opened.status -eq 'completed'){
                        $State.outputOperation=$null
                        if(-not $opened.result.document_open -or -not $opened.result.visible){throw '한글 창 표시를 확인하지 못했습니다.'}
                        $UI.OutputOpenError.Text=''
                    }
                }catch{$State.outputOperation=$null;$UI.OutputOpenError.Text='열기 결과를 확인하지 못했습니다: '+$_.Exception.Message}
            }
            if($State.operation){
                $op=& $Call @{action='authoring_operation';operation_id=$State.operation}
                if($op.phase){$UI.Notice.Text=[string]$op.phase}
                if($op.login_url -and $op.login_url -ne $State.loginUrl){$url=[uri]$op.login_url;if($url.Scheme -ne 'https' -or $url.Host -notin @('auth.openai.com','auth0.openai.com','chatgpt.com')){throw '로그인 주소를 확인할 수 없습니다.'};$State.loginUrl=$op.login_url;Start-Process -FilePath $op.login_url | Out-Null}
                if($op.status -eq 'failed'){$State.operation=$null;$UI.Notice.Text=$op.error;if($State.operationAction -in @('authoring_login','authoring_connection_check','authoring_logout')){& $Actions.Account @{connected=$false}}}
                elseif($op.status -eq 'completed'){
                    $State.operation=$null;$UI.Notice.Text='';$result=$op.result
                    & $Actions.Refresh
                    if($null -ne $result.connected){& $Actions.Account $result}
                    if($result.guide_file -and -not $result.id){
                        $State.guideFile=[string]$result.guide_file;$UI.OpenGuideFile.Visibility='Visible'
                        $UI.GuideOutline.Visibility='Collapsed'
                        $UI.Notice.Text="AI 추출 완료 · 소주제 $($result.heading_count)개 · 작성요령 $($result.instruction_count)문단 · AI 요청 $($result.ai_requests)회`n$($result.guide_file)"
                    }
                    if($result.id){$UI.Templates.SelectedItem=@($UI.Templates.ItemsSource|Where-Object {$_.id -eq $result.id})[0];$registrationLabel=if($result.analysis_status -eq 'partial'){'양식 저장 · 일부 분석/확인 필요'}else{'양식 등록 완료'};$UI.Notice.Text="$registrationLabel · 확인 필요 $(@($result.analysis_reviews | Where-Object {$null -ne $_}).Count)개. 미확인 항목은 원본을 유지합니다.";if($result.unmapped_input_count){$UI.Notice.Text+=" 자동 연결하지 않은 빈칸 $($result.unmapped_input_count)개는 최종 문서에서 확인하세요."}}
                    if($result.registration_mode -eq 'guides_then_research_and_write'){
                        $State.guideFile=[string]$result.guide_file;$UI.OpenGuideFile.Visibility='Visible'
                        $resolved=[int]$result.input_slot_analysis.second_pass_resolved_count;$remaining=@($result.analysis_reviews | Where-Object {$null -ne $_}).Count;$covered=@($result.covered_review_indices | Where-Object {$null -ne $_}).Count
                        $UI.Notice.Text="소주제·작성요령과 입력칸 저장 완료. 불확실한 칸 $resolved 곳을 추가로 자동 판정했습니다. $covered 곳은 제목 뒤 새 문단으로 작성하고 원래 빈칸은 보존합니다. 입력칸 위치에 대한 사용자 확인 대상은 $remaining 곳입니다. 다음 화면에서 작성 내용을 입력하면 자료조사와 본문 작성을 시작합니다."
                        if(@($result.manual_topics).Count){$UI.Notice.Text+=' 자동 입력 위치가 없는 소주제 '+@($result.manual_topics).Count+'개는 원본을 유지하므로 최종 확인이 필요합니다.'}
                        if($result.recheck_no_change){$UI.Notice.Text='AI가 불확실한 입력칸을 다시 확인했지만 추가로 확정할 위치는 없었습니다. 기존 양식은 그대로 유지했습니다.'}
                    }
                    if($null -ne $result.rows -and $result.template_id -eq $UI.Templates.SelectedItem.id){$State.rows=@($result.rows);$State.prepared=$result.template_id;$State.table.Collapsed.Clear();& $Actions.RenderInputs;& $Actions.Page 2}
                    if($result.replay -and $result.template_id -eq $UI.Templates.SelectedItem.id){
                        $State.replay=$result;$UI.ProjectTitle.Text=[string]$result.brief.title;$UI.Description.Text=[string]$result.brief.description
                        $UI.ReplayInfo.Text="불러온 응답: $($result.title) · $($result.topics)개 주제`n$($result.path)";$UI.Notice.Text=[string]$result.message
                    }
                }
            }
            if($State.job){
                $job=& $Call @{action='authoring_status';job_id=$State.job};$previousStatus=$State.jobStatus;$State.jobStatus=$job.status;$State.busy=$job.status -in @('running','exporting');$State.output=$job.hwp_path
                if($State.snapshotJob -ne $State.job){& $Actions.LoadSnapshot $job}
                $done=@($job.completed).Count;$total=[Math]::Max(1,[int]$job.total)
                $UI.JobTitle.Text=$job.title;$UI.PhaseText.Text=$job.phase;$UI.TopicText.Text=$job.current_topic
                $percent=if($job.status -eq 'completed'){100}else{[Math]::Min(95,[Math]::Floor(95*$done/$total))}
                $UI.JobProgress.Value=$percent;$UI.PercentText.Text="$percent% · 작성 항목 $done / $($job.total)개 처리";$UI.PhaseSpinner.Visibility=if($State.busy){'Visible'}else{'Collapsed'}
                $UI.Stop.Visibility=if($State.busy){'Visible'}else{'Collapsed'};$UI.Resume.Visibility=if($job.status -in @('failed','paused','interrupted','ready')){'Visible'}else{'Collapsed'};$UI.EditAgain.Visibility=$UI.Resume.Visibility;$UI.JobError.Text=[string]$job.error
                if($job.status -eq 'completed' -and $State.output){
                    $personalCount=@($job.input_summary | Where-Object {$null -ne $_}).Count
                    $personalSummary=if($personalCount){"저장 정보로 문서의 $personalCount 개 칸을 채웠습니다."}else{'연결된 저장 정보 없이 본문을 작성했습니다.'}
                    $UI.CompletionSummary.Text="작성 주제: $($job.title)`n`n$personalSummary`n작성요령을 참고하여 $done 개 항목을 처리했습니다.`n본문과 서식 검사를 거쳐 한글 파일을 저장했습니다.`n`n출력본을 읽어보고 사실·수치·확인 필요 표시를 수정해 주세요."
                    if($job.execution_mode -eq 'saved_response'){$UI.CompletionSummary.Text="작성 주제: $($job.title)`n`n저장된 AI 응답 $done 개 항목을 불러왔습니다. 외부 AI 호출은 하지 않았습니다.`n$personalSummary`n문단·표 서식, 확인 메모와 검사를 거쳐 한글 파일을 저장했습니다.`n`n출력본의 사실·수치·표 분량과 해당 위치에 연결된 확인 메모를 검토해 주세요."}
                    if($job.native.memo_count){$UI.CompletionSummary.Text+="`n확인 메모 $($job.native.memo_count)개: AI가 작성한 본문에서 확인할 내용과 확인 방법을 읽을 수 있습니다. 단순 빈칸 입력 안내는 제외합니다."}
                    if($job.research_enabled){$researchLabel=if($job.execution_mode -eq 'saved_response'){'보관된 자료 조사·분석'}else{'자료 조사·분석'};$UI.CompletionSummary.Text+="`n$researchLabel $($job.research_summary.completed_topics)개 주제 · 참고 출처 $($job.research_summary.source_count)개. 조사 기록은 결과 폴더에 저장했습니다."}
                    if(@($job.review).Count){$UI.CompletionSummary.Text+="`n검토 안내 $(@($job.review).Count)건이 있습니다. 자동 검사는 사실과 증빙의 검증을 대신하지 않습니다."}
                    # Never pull the user away from an input review page on a timer tick.
                    if($State.page -eq 3 -and $previousStatus -ne 'completed'){& $Actions.Page 4}
                    # Only a job started/resumed in this dialog opens automatically.
                    # Consume before launching so failed opens are not retried every tick.
                    if($State.autoOpenJob -and $State.autoOpenJob -eq $State.job){
                        $State.autoOpenJob=$null
                        & $Actions.OpenOutput
                    }
                }
            }
            & $Actions.Update
        }catch{if($State.page -eq 3){$UI.JobError.Text=$_.Exception.Message}else{$UI.Notice.Text=$_.Exception.Message}}
        finally{$State.polling=$false}
    }.GetNewClosure()
    $Timer=[System.Windows.Threading.DispatcherTimer]::new();$Timer.Interval=[TimeSpan]::FromSeconds(1)
    $Timer.Add_Tick([GovOfficePollGuard]::Wrap({& $Actions.Poll}.GetNewClosure()))
    $Dialog.Add_Closed({$State.closing=$true;$Timer.Stop()}.GetNewClosure())
    try{& $Actions.Refresh;& $Actions.Page 1;& $Actions.Begin @{action='authoring_connection_check'};$Timer.Start();Show-WorkspaceWindow $Dialog 'authoring'}catch{$Timer.Stop();throw}
}
