# Personal data tools. Existing preset capture/review remains independent.
$script:ProfileReviewActive=$false
function Write-ProfileReviewTrace([string]$Stage) {
    # Diagnostics contain stages/counts only, never extracted personal values.
    if(Get-Command Write-GuiRuntimeError -ErrorAction SilentlyContinue){
        Write-GuiRuntimeError 'profile review lifecycle' $Stage
    }
}
function Invoke-ProfileReviewSession($OwnerWindow,[scriptblock]$Review) {
    if($script:ProfileReviewActive){return}
    $script:ProfileReviewActive=$true
    $pollPause=if('GovOfficePollGuard' -as [type]){[GovOfficePollGuard]::Pause()}else{$null}
    $timers=@();$clock=[System.Diagnostics.Stopwatch]::StartNew()
    try{
        # ShowDialog runs a nested event loop, including during native title-bar
        # moves. Do not let background HWP requests enter that loop. Preserve
        # stopped timers and keep explicit analyze/save requests available.
        foreach($name in @('DocumentStatusTimer','SelectionProbeTimer')){
            $timer=Get-Variable -Name $name -Scope Script -ValueOnly -ErrorAction SilentlyContinue
            if($null -ne $timer){
                $timers+=@{Timer=$timer;WasEnabled=[bool]$timer.IsEnabled}
                $timer.Stop()
            }
        }
        $script:SelectionMouseDown=$false
        Write-ProfileReviewTrace 'begin; background_polling=paused'
        & $Review $OwnerWindow
    }finally{
        # Discard an unfinished mouse gesture; never export it after closing.
        $script:SelectionMouseDown=$false
        $script:ProfileReviewActive=$false
        foreach($entry in $timers){
            if($entry.WasEnabled -and -not $script:GuiClosing){$entry.Timer.Start()}
        }
        $clock.Stop()
        if($null -ne $pollPause){$pollPause.Dispose()}
        Write-ProfileReviewTrace ("end; elapsed_ms={0}" -f $clock.ElapsedMilliseconds)
    }
}
function Open-ProfileSelectionImport($OwnerWindow=$Window) {
    if(Test-WorkspaceWindow 'profile-import'){return}
    Invoke-ProfileReviewSession $OwnerWindow {param($owner) Show-ProfileSelectionImport $owner}
}
function Open-ProfileDataTable($OwnerWindow=$Window) {
    if(Test-WorkspaceWindow 'profile-data'){return}
    Invoke-ProfileReviewSession $OwnerWindow {param($owner) Show-ProfileDataTable $owner}
}
function New-ProfileToolWindow($Title,$OwnerWindow) {
    $dialog=[System.Windows.Window]::new();$dialog.Title=$Title;$dialog.Width=980;$dialog.Height=680
    $dialog.MinWidth=720;$dialog.MinHeight=460;$dialog.Background='#F7F5FA';$dialog.FontFamily='맑은 고딕'
    $dialog.WindowStartupLocation='CenterOwner';if($OwnerWindow){$dialog.Owner=$OwnerWindow}
    return $dialog
}
function New-ProfileToolButton($Text) {
    $button=[System.Windows.Controls.Button]::new();$button.Content=$Text;$button.Padding='12,7';$button.Margin='4'
    $button.Background='#68518F';$button.Foreground='White';return $button
}
function Read-ProfileTableText($OwnerWindow,$Title,$Value) {
    if($script:ProfileReviewActive){return Show-ProfileTableText $OwnerWindow $Title $Value}
    Invoke-ProfileReviewSession $OwnerWindow {param($owner) Show-ProfileTableText $owner $Title $Value}
}
function Show-ProfileTableText($OwnerWindow,$Title,$Value) {
    $edit=New-ProfileToolWindow $Title $OwnerWindow;$edit.Width=540;$edit.Height=260;$edit.MinWidth=440;$edit.MinHeight=240
    $panel=[System.Windows.Controls.StackPanel]::new();$panel.Margin='20';$edit.Content=$panel
    $label=[System.Windows.Controls.TextBlock]::new();$label.Text=$Title;$label.Margin='0,0,0,10';[void]$panel.Children.Add($label)
    $box=[System.Windows.Controls.TextBox]::new();$box.Text=[string]$Value;$box.MinHeight=60;$box.AcceptsReturn=$true;$box.TextWrapping='Wrap';[void]$panel.Children.Add($box)
    $ok=New-ProfileToolButton '확인';[void]$panel.Children.Add($ok)
    $result=@{Value=$null};$ok.Add_Click({$result.Value=$box.Text;$edit.DialogResult=$true}.GetNewClosure())
    $edit.Add_ContentRendered({[void]$box.Focus();$box.SelectAll()}.GetNewClosure())
    [void]$edit.ShowDialog();return $result.Value
}
function Show-ProfileSelectionImport($OwnerWindow) {
    $analysis=Send-Backend @{action='user_profile_selection_analyze'}
    if(-not $analysis.ok){
        $diagnostic=if($analysis.selection_diagnostic){$analysis.selection_diagnostic|ConvertTo-Json -Compress}else{'{}'}
        Write-GuiRuntimeError 'profile selection read' ([string]$analysis.message+' / '+$diagnostic)
        throw ([string]$analysis.message+"`n진단: "+$diagnostic)
    }
    if(@($analysis.candidates).Count -eq 0){[void][System.Windows.MessageBox]::Show($OwnerWindow,'읽을 수 있는 항목이 없습니다. 표에서 항목 이름과 값을 함께 선택해 주세요.','선택 영역에서 개인정보 저장');return}
    Write-ProfileReviewTrace ("analysis_ready; candidates={0}" -f @($analysis.candidates).Count)
    $dialog=New-ProfileToolWindow '선택 영역에서 개인정보 저장' $OwnerWindow
    $layout=[System.Windows.Controls.DockPanel]::new();$layout.Margin='16';$dialog.Content=$layout
    $help=[System.Windows.Controls.TextBlock]::new();$help.Text="선택 영역에서 읽은 항목만 표시합니다. 체크한 항목만 저장됩니다. 프리셋은 변경하지 않습니다.`n필드와 값을 더블클릭해 수정하세요. 하위 필드는 ‘연구자 > 이름’처럼 >로 구분합니다.";$help.TextWrapping='Wrap';$help.Margin='4,0,4,14';[System.Windows.Controls.DockPanel]::SetDock($help,'Top');[void]$layout.Children.Add($help)
    $save=New-ProfileToolButton '체크한 항목을 사용자 정보에 저장';[System.Windows.Controls.DockPanel]::SetDock($save,'Bottom');[void]$layout.Children.Add($save)
    $table=[System.Windows.Controls.DataGrid]::new();$table.AutoGenerateColumns=$false;$table.CanUserAddRows=$false;$table.CanUserDeleteRows=$false;$table.RowHeaderWidth=0;$table.MinRowHeight=34
    # One real toggle fills the cell. The centered inner checkbox is only a
    # visual, so clicking either the mark or the padding toggles exactly once.
    # Native CheckBox behavior also preserves keyboard Space/accessibility.
    $check=[System.Windows.Controls.DataGridTemplateColumn]::new();$check.Header='저장';$check.Width=55;$check.IsReadOnly=$true
    $check.CellStyle=[System.Windows.Markup.XamlReader]::Parse(@'
<Style xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" TargetType="DataGridCell">
  <Setter Property="Padding" Value="0"/>
  <Setter Property="HorizontalContentAlignment" Value="Stretch"/>
  <Setter Property="VerticalContentAlignment" Value="Stretch"/>
</Style>
'@)
    $check.CellTemplate=[System.Windows.Markup.XamlReader]::Parse(@'
<DataTemplate xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <CheckBox x:Name="SelectionToggle" IsChecked="{Binding selected, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"
            IsThreeState="False" HorizontalAlignment="Stretch" VerticalAlignment="Stretch"
            AutomationProperties.Name="저장 항목 선택" ToolTip="이 칸 어디든 누르면 저장 선택이 켜지거나 꺼집니다.">
    <CheckBox.Template>
      <ControlTemplate TargetType="CheckBox">
        <Border Background="Transparent">
          <CheckBox x:Name="SelectionMark" IsHitTestVisible="False" Focusable="False" IsTabStop="False"
                    HorizontalAlignment="Center" VerticalAlignment="Center" IsThreeState="False"
                    IsChecked="{Binding IsChecked, RelativeSource={RelativeSource TemplatedParent}, Mode=OneWay}"/>
        </Border>
      </ControlTemplate>
    </CheckBox.Template>
  </CheckBox>
</DataTemplate>
'@)
    [void]$table.Columns.Add($check)
    foreach($definition in @(@('field','필드 경로 (상위 > 하위)',300),@('value','저장할 값',330),@('confidence','분석 결과',140))){
        $column=[System.Windows.Controls.DataGridTextColumn]::new();$column.Header=$definition[1];$column.Binding=[System.Windows.Data.Binding]::new($definition[0]);$column.Width=$definition[2];$column.IsReadOnly=$definition[0] -eq 'confidence';[void]$table.Columns.Add($column)
    }
    $rows=[System.Collections.ObjectModel.ObservableCollection[object]]::new()
    foreach($candidate in @($analysis.candidates)){
        $path=if($candidate.field_path){$candidate.field_path}else{$candidate.field}
        $state=if($candidate.recommended){'추천'}else{'직접 확인 필요'}
        $rows.Add([pscustomobject]@{selected=[bool]$candidate.recommended;candidate_id=[string]$candidate.candidate_id;field=[string]$path;value=[string]$candidate.value;confidence=$state})
    }
    $table.ItemsSource=$rows;[void]$layout.Children.Add($table)
    $save.Add_Click({try{
        [void]$table.CommitEdit([System.Windows.Controls.DataGridEditingUnit]::Cell,$true);[void]$table.CommitEdit([System.Windows.Controls.DataGridEditingUnit]::Row,$true)
        $selected=@($rows|Where-Object selected|ForEach-Object{@{candidate_id=$_.candidate_id;field=$_.field;value=$_.value}})
        $response=Send-Backend @{action='user_profile_selection_save';draft_id=$analysis.draft_id;rows=$selected}
        if(-not $response.ok){throw $response.message};$Status.Text=$response.message;$dialog.Close()
    }catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    Write-ProfileReviewTrace 'selection_dialog_ready'
    $dialog.Add_ContentRendered({Write-ProfileReviewTrace 'selection_dialog_rendered'})
    Show-WorkspaceWindow $dialog 'profile-import'
}
function Invoke-ProfileTableEdit($State,$Command) {
    $Command.action='user_profile_table_mutate';$Command.snapshot=$State.Profile.values
    $response=Send-Backend $Command;if(-not $response.ok){throw $response.message}
    $State.Note.Text=$response.message
    Update-ProfileTable $State
}
function Add-ProfileTableMenu($Cell,$State,$Field,$Value,$Kind) {
    $menu=[System.Windows.Controls.ContextMenu]::new();$Cell.ContextMenu=$menu
    $operations=if($Kind -eq 'field'){@('필드 이름 수정','별칭 수정','값 추가','최상위로 이동','필드 삭제')}else{@('값 수정','기본 출력값으로 지정','값 삭제')}
    foreach($operation in $operations){
        $item=[System.Windows.Controls.MenuItem]::new();$item.Header=$operation
        $item.Add_Click({try{
            $command=@{field_id=$Field.id;value=$Value}
            switch($operation){
                '필드 이름 수정' {$name=Read-ProfileTableText $State.Dialog '필드 이름 수정' $Field.name;if($null -eq $name){return};$command.operation='edit_field';$command.name=$name}
                '별칭 수정' {$aliases=Read-ProfileTableText $State.Dialog '별칭 수정 (쉼표로 구분)' (@($Field.aliases)-join ', ');if($null -eq $aliases){return};$command.operation='edit_field';$command.name=$Field.name;$command.aliases=@($aliases -split ','|ForEach-Object{$_.Trim()}|Where-Object{$_})}
                '값 추가' {$new=Read-ProfileTableText $State.Dialog '새 값 추가' '';if($null -eq $new){return};$command.operation='add_value';$command.value=$new}
                '최상위로 이동' {$command.operation='move_field';$command.target_id=''}
                '필드 삭제' {if([System.Windows.MessageBox]::Show($State.Dialog,"‘$($Field.path)’ 필드와 모든 하위 필드·값을 삭제할까요? 연결된 프리셋의 자동 입력에도 영향을 줍니다.",'필드 삭제','YesNo','Warning') -ne 'Yes'){return};$command.operation='delete_field'}
                '값 수정' {$new=Read-ProfileTableText $State.Dialog '값 수정' $Value;if($null -eq $new){return};$command.operation='edit_value';$command.new_value=$new}
                '기본 출력값으로 지정' {$command.operation='default'}
                '값 삭제' {if([System.Windows.MessageBox]::Show($State.Dialog,'선택한 값을 삭제할까요?','값 삭제','YesNo','Warning') -ne 'Yes'){return};$command.operation='delete_value'}
            }
            Invoke-ProfileTableEdit $State $command
        }catch{Show-Error $_.Exception.Message}}.GetNewClosure());[void]$menu.Items.Add($item)
    }
}
function Set-ProfileCellDrag($Cell,$State,$Field,$Value,$Kind) {
    $Cell.AllowDrop=$true
    $Cell.Cursor=[System.Windows.Input.Cursors]::Hand
    $Cell.Add_PreviewMouseLeftButtonDown({param($sender,$event)
        if($State.Select){& $State.Select $Field $Value $Kind}
        if($event.ClickCount -eq 2){
            $event.Handled=$true;$State.DragStart=$null;$State.DragSource=$null
            try{
                $command=@{field_id=$Field.id}
                if($Kind -eq 'field'){
                    $new=Read-ProfileTableText $State.Dialog '필드 이름 수정' $Field.name
                    if($null -eq $new){return};$command.operation='edit_field';$command.name=$new
                }else{
                    $new=Read-ProfileTableText $State.Dialog '값 수정' $Value
                    if($null -eq $new){return};$command.operation='edit_value';$command.value=$Value;$command.new_value=$new
                }
                Invoke-ProfileTableEdit $State $command
            }catch{Show-Error $_.Exception.Message}
            return
        }
        $State.DragStart=$event.GetPosition($State.Grid);$State.DragSource=$sender
    }.GetNewClosure())
    $Cell.Add_PreviewMouseMove({param($sender,$event)
        if($event.LeftButton -ne [System.Windows.Input.MouseButtonState]::Pressed -or $State.DragSource -ne $sender -or $null -eq $State.DragStart){return}
        $point=$event.GetPosition($State.Grid)
        if([Math]::Abs($point.X-$State.DragStart.X) -lt [System.Windows.SystemParameters]::MinimumHorizontalDragDistance -and [Math]::Abs($point.Y-$State.DragStart.Y) -lt [System.Windows.SystemParameters]::MinimumVerticalDragDistance){return}
        $State.DragStart=$null
        $payload=[pscustomobject]@{field_id=$Field.id;value=$Value;kind=$Kind;page_id=$State.PageId}
        $data=[System.Windows.DataObject]::new();$data.SetData('GovOffice.ProfileTable',$payload)
        $pollPause=if('GovOfficePollGuard' -as [type]){[GovOfficePollGuard]::Pause()}else{$null}
        try{[void][System.Windows.DragDrop]::DoDragDrop($sender,$data,[System.Windows.DragDropEffects]::Move)}finally{$State.DragSource=$null;if($null -ne $pollPause){$pollPause.Dispose()}}
        $event.Handled=$true
    }.GetNewClosure())
    $Cell.Add_DragOver({param($sender,$event)
        $event.Effects=[System.Windows.DragDropEffects]::None
        if($event.Data.GetDataPresent('GovOffice.ProfileTable')){
            $payload=$event.Data.GetData('GovOffice.ProfileTable')
            if($payload.page_id -eq $State.PageId -and $payload.field_id -ne $Field.id){$event.Effects=[System.Windows.DragDropEffects]::Move}
        };$event.Handled=$true
    }.GetNewClosure())
    $Cell.Add_Drop({param($sender,$event)
        $event.Handled=$true
        if(-not $event.Data.GetDataPresent('GovOffice.ProfileTable')){return}
        $payload=$event.Data.GetData('GovOffice.ProfileTable');if($payload.page_id -ne $State.PageId -or $payload.field_id -eq $Field.id){return}
        try{$op=if($payload.kind -eq 'field'){'move_field'}else{'move_value'};Invoke-ProfileTableEdit $State @{operation=$op;field_id=$payload.field_id;value=$payload.value;target_id=$Field.id}}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
}
function Add-ProfileTableCell($State,$Text,[int]$Row,[int]$Column,[int]$Span,$Field,$Value,$Kind) {
    $cell=[System.Windows.Controls.Border]::new();$cell.BorderBrush='#D9D2E4';$cell.BorderThickness='0,0,1,1';$cell.Padding='10,8';$cell.Background=if($Kind -eq 'field'){'#EEE8F5'}else{'White'}
    $label=[System.Windows.Controls.TextBlock]::new();$label.Text=[string]$Text;$label.TextWrapping='Wrap';$label.VerticalAlignment='Center';$cell.Child=$label
    if($Kind -eq 'field'){$label.FontWeight='SemiBold';$cell.ToolTip="경로: $($Field.path)`n고정 식별자: $($Field.id)`n더블클릭: 이름 수정 / 드래그: 값과 하위 필드 함께 이동"}
    elseif($Kind -eq 'value'){$cell.ToolTip='더블클릭: 값 수정 / 드래그: 값 이동'}
    [System.Windows.Controls.Grid]::SetRow($cell,$Row);[System.Windows.Controls.Grid]::SetColumn($cell,$Column);[System.Windows.Controls.Grid]::SetRowSpan($cell,$Span);[void]$State.Grid.Children.Add($cell)
    if($Kind -in @('field','value')){Add-ProfileTableMenu $cell $State $Field $Value $Kind;Set-ProfileCellDrag $cell $State $Field $Value $Kind}
    return $cell
}
function Add-ProfileTableBranch($State,$Field,[int]$Depth) {
    $start=$State.Row
    foreach($value in @($Field.values)){
        $row=[System.Windows.Controls.RowDefinition]::new();$row.Height='Auto';$row.MinHeight=38;[void]$State.Grid.RowDefinitions.Add($row)
        [void](Add-ProfileTableCell $State $value $State.Row $State.Depth 1 $Field $value 'value')
        $default=if($value -ceq $Field.default){'기본 출력값'}else{''}
        [void](Add-ProfileTableCell $State $default $State.Row ($State.Depth+1) 1 $null '' 'text');$State.Row++
    }
    foreach($child in @($State.Profile.field_groups|Where-Object{$_.parent_id -eq $Field.id})){Add-ProfileTableBranch $State $child ($Depth+1)}
    if($State.Row -eq $start){
        $row=[System.Windows.Controls.RowDefinition]::new();$row.Height='Auto';$row.MinHeight=38;[void]$State.Grid.RowDefinitions.Add($row)
        [void](Add-ProfileTableCell $State '(저장된 값 없음)' $State.Row $State.Depth 1 $null '' 'text');$State.Row++
    }
    $label=$Field.name;if(@($Field.aliases).Count){$label+="`n별칭: "+(@($Field.aliases)-join ', ')}
    [void](Add-ProfileTableCell $State $label $start $Depth ($State.Row-$start) $Field '' 'field')
}
function Add-FieldTableColumnResize($State,[string[]]$Keys) {
    # Header-only thumbs: native mouse capture, no document drag/drop or polling.
    if(-not $State.ContainsKey('ColumnWidths')){$State.ColumnWidths=@{}}
    for($index=0;$index -lt $State.Grid.ColumnDefinitions.Count;$index++){
        $definition=$State.Grid.ColumnDefinitions[$index];$key=$Keys[$index]
        if($State.ColumnWidths.ContainsKey($key)){$definition.Width=[System.Windows.GridLength]::new([Math]::Max($definition.MinWidth,$State.ColumnWidths[$key]))}
        $handle=[System.Windows.Controls.Primitives.Thumb]::new()
        $handle.Width=8;$handle.HorizontalAlignment='Right';$handle.VerticalAlignment='Stretch';$handle.Cursor='SizeWE';$handle.Focusable=$true
        $handle.ToolTip='좌우로 끌어 열 너비 조절 · 방향키로 미세 조절';$handle.Tag=$key
        $handle.Template=[System.Windows.Markup.XamlReader]::Parse(@'
<ControlTemplate xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" TargetType="Thumb">
  <Border x:Name="Grip" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" Background="Transparent" BorderBrush="#B9A8CD" BorderThickness="0,0,2,0"/>
  <ControlTemplate.Triggers><Trigger Property="IsMouseOver" Value="True"><Setter TargetName="Grip" Property="Background" Value="#DDD1EC"/></Trigger><Trigger Property="IsKeyboardFocused" Value="True"><Setter TargetName="Grip" Property="Background" Value="#DDD1EC"/></Trigger></ControlTemplate.Triggers>
</ControlTemplate>
'@)
        $resize={param([double]$Delta)
            # Freeze star widths before changing one column; adjacent columns stay put.
            for($j=0;$j -lt $State.Grid.ColumnDefinitions.Count;$j++){
                $column=$State.Grid.ColumnDefinitions[$j]
                if(-not $column.Width.IsAbsolute){$column.Width=[System.Windows.GridLength]::new([Math]::Max($column.MinWidth,$column.ActualWidth))}
                $State.ColumnWidths[$Keys[$j]]=$column.Width.Value
            }
            $definition.Width=[System.Windows.GridLength]::new([Math]::Max($definition.MinWidth,[Math]::Min(2000,$definition.Width.Value+$Delta)))
            $State.ColumnWidths[$key]=$definition.Width.Value
        }.GetNewClosure()
        $handle.Add_DragStarted({param($sender,$event)
            if($State.ContainsKey('DragStart')){$State.DragStart=$null;$State.DragSource=$null}
            $event.Handled=$true
        }.GetNewClosure())
        $handle.Add_DragDelta({param($sender,$event) & $resize $event.HorizontalChange;$event.Handled=$true}.GetNewClosure())
        $handle.Add_KeyDown({param($sender,$event)
            if($event.Key -eq 'Left'){& $resize -10;$event.Handled=$true}
            elseif($event.Key -eq 'Right'){& $resize 10;$event.Handled=$true}
        }.GetNewClosure())
        [System.Windows.Controls.Grid]::SetRow($handle,0);[System.Windows.Controls.Grid]::SetColumn($handle,$index)
        [System.Windows.Controls.Panel]::SetZIndex($handle,10);[void]$State.Grid.Children.Add($handle)
    }
}
function Show-PersonalFieldTree($Tree,$Profile,$OwnerWindow,[scriptblock]$OnChanged) {
    $expanded=@{}
    if($Tree.Tag -is [hashtable]){foreach($id in $Tree.Tag.Keys){$expanded[$id]=$Tree.Tag[$id].IsExpanded}}
    $Tree.Items.Clear();$nodes=@{};$fields=@{};$hasChildren=@{}
    foreach($field in @($Profile.field_groups)){$fields[[string]$field.id]=$field;if($field.parent_id){$hasChildren[[string]$field.parent_id]=$true}}
    foreach($field in @($Profile.field_groups)){
        # Basic leaf information is already in the summary card; keep any children.
        if(-not $field.parent_id -and $field.name -in @('이름','전화번호','이메일') -and -not $hasChildren.ContainsKey([string]$field.id)){continue}
        $node=[System.Windows.Controls.TreeViewItem]::new();$node.Tag=[string]$field.id
        $node.IsExpanded=if($expanded.ContainsKey([string]$field.id)){$expanded[[string]$field.id]}else{$true}
        $node.Header=New-PersonalTreeHeader $field.name $field '' 'field' $Profile $OwnerWindow $OnChanged
        $node.ToolTip=[string]$field.path
        foreach($value in @($field.values)){
            $valueNode=[System.Windows.Controls.TreeViewItem]::new();$valueNode.Tag=[string]$field.id
            $display=if($value -ceq $field.default){[string]$value+'  · 기본값'}else{[string]$value}
            $valueNode.Header=New-PersonalTreeHeader $display $field ([string]$value) 'value' $Profile $OwnerWindow $OnChanged
            [void]$node.Items.Add($valueNode)
        }
        $nodes[[string]$field.id]=$node
    }
    foreach($field in @($Profile.field_groups)){
        $id=[string]$field.id;if(-not $nodes.ContainsKey($id)){continue}
        $parent=[string]$field.parent_id;$seen=@{$id=$true};$ancestor=$parent
        while($ancestor -and $fields.ContainsKey($ancestor)){
            if($seen.ContainsKey($ancestor)){throw '필드 계층에 순환 관계가 있습니다.'}
            $seen[$ancestor]=$true;$ancestor=[string]$fields[$ancestor].parent_id
        }
        if($parent -and $nodes.ContainsKey($parent)){[void]$nodes[$parent].Items.Add($nodes[$id])}else{[void]$Tree.Items.Add($nodes[$id])}
    }
    if($Tree.Items.Count -eq 0){[void]$Tree.Items.Add([System.Windows.Controls.TextBlock]@{Text='저장된 문서 필드가 없습니다.';Foreground='#777777';Margin='6'})}
    $Tree.Tag=$nodes
}
function New-PersonalTreeHeader($Text,$Field,[string]$Value,[string]$Kind,$Profile,$OwnerWindow,[scriptblock]$OnChanged) {
    $header=[System.Windows.Controls.Label]::new();$header.Padding='2,3';$header.Cursor='Hand'
    $label=[System.Windows.Controls.TextBlock]::new();$label.Text=[string]$Text;$label.TextWrapping='Wrap';$label.MaxWidth=200
    $label.Foreground=if($Kind -eq 'field'){'#55447A'}else{'#333333'}
    if($Kind -eq 'field'){$label.FontWeight='SemiBold'}
    $header.Content=$label;$header.ToolTip="더블클릭하여 수정`n$Text"
    $header.Add_PreviewMouseDoubleClick({param($sender,$event)
        if($event.ChangedButton -ne [System.Windows.Input.MouseButton]::Left){return}
        $event.Handled=$true
        $review={
            param($owner)
            try{
                $initial=if($Kind -eq 'field'){[string]$Field.name}else{$Value}
                $title=if($Kind -eq 'field'){'필드 이름 수정'}else{'값 수정'}
                $edited=Read-ProfileTableText $owner $title $initial;if($null -eq $edited){return}
                $command=@{action='user_profile_table_mutate';field_id=[string]$Field.id;snapshot=$Profile.values}
                if($Kind -eq 'field'){$command.operation='edit_field';$command.name=$edited}else{$command.operation='edit_value';$command.value=$Value;$command.new_value=$edited}
                $response=Send-Backend $command;if(-not $response.ok){throw $response.message}
                & $OnChanged
            }catch{Show-Error $_.Exception.Message}
        }
        Invoke-ProfileReviewSession $OwnerWindow $review
    }.GetNewClosure())
    return $header
}
function Update-ProfileTable($State) {
    $response=Send-Backend @{action='user_profile_get'};if(-not $response.ok){throw $response.message};$State.Profile=$response
    $State.Grid.Children.Clear();$State.Grid.RowDefinitions.Clear();$State.Grid.ColumnDefinitions.Clear();$State.Depth=1;$State.DragStart=$null
    foreach($field in @($response.field_groups)){
        $depth=1;$parent=$field.parent_id;$seen=@{}
        while($parent){if($seen.ContainsKey($parent)){throw '필드 계층에 순환 관계가 있습니다.'};$seen[$parent]=$true;$depth++;$ancestor=@($response.field_groups|Where-Object{$_.id -eq $parent})|Select-Object -First 1;$parent=$ancestor.parent_id}
        $State.Depth=[Math]::Max($State.Depth,$depth)
    }
    for($i=0;$i -lt ($State.Depth+2);$i++){$column=[System.Windows.Controls.ColumnDefinition]::new();$column.Width=if($i -eq $State.Depth){'2*'}else{'*'};$column.MinWidth=if($i -eq $State.Depth){220}else{145};[void]$State.Grid.ColumnDefinitions.Add($column)}
    $header=[System.Windows.Controls.RowDefinition]::new();$header.Height='Auto';[void]$State.Grid.RowDefinitions.Add($header)
    for($i=0;$i -lt $State.Depth;$i++){$title=if($i -eq 0){'대표 필드'}else{"하위 필드 $i"};[void](Add-ProfileTableCell $State $title 0 $i 1 $null '' 'header')}
    [void](Add-ProfileTableCell $State '저장된 값' 0 $State.Depth 1 $null '' 'header');[void](Add-ProfileTableCell $State '출력 설정' 0 ($State.Depth+1) 1 $null '' 'header')
    $State.Row=1
    foreach($field in @($response.field_groups|Where-Object{-not $_.parent_id})){
        if($State.DocumentFieldsOnly -and $field.name -in @('이름','전화번호','이메일') -and -not @($response.field_groups|Where-Object{$_.parent_id -eq $field.id}).Count){continue}
        Add-ProfileTableBranch $State $field 0
    }
    if($State.Row -eq 1){
        $empty=[System.Windows.Controls.RowDefinition]::new();$empty.Height='Auto';[void]$State.Grid.RowDefinitions.Add($empty)
        $cell=Add-ProfileTableCell $State '저장된 문서 필드가 없습니다. 위에서 새 필드와 값을 추가하세요.' 1 0 1 $null '' 'text'
        [System.Windows.Controls.Grid]::SetColumnSpan($cell,($State.Depth+2))
    }
    $widthKeys=@(for($i=0;$i -lt $State.Depth;$i++){"field-$i"})+@('value','default')
    Add-FieldTableColumnResize $State $widthKeys
    if($State.OnRefreshed){& $State.OnRefreshed}
}
function Show-ProfileDataTable($OwnerWindow) {
    $dialog=New-ProfileToolWindow '사용자 데이터 관리 — 필드와 값' $OwnerWindow
    $layout=[System.Windows.Controls.DockPanel]::new();$layout.Margin='16';$layout.Background='#F7F5FA';$dialog.Content=$layout
    $help=[System.Windows.Controls.TextBlock]::new();$help.Text="필드 → 하위 필드 → 여러 값 순서입니다. 같은 필드의 셀은 세로로 병합됩니다.`n더블클릭: 항목 이름·값 바로 수정 / 우클릭: 추가·삭제·별칭 / 드래그: 필드 또는 값 이동`n기본 이름·전화번호·이메일 필드는 유지됩니다. 수정창에서 확인하면 저장됩니다.";$help.TextWrapping='Wrap';$help.Margin='4,0,4,10';[System.Windows.Controls.DockPanel]::SetDock($help,'Top');[void]$layout.Children.Add($help)
    $bar=[System.Windows.Controls.StackPanel]::new();$bar.Orientation='Horizontal';[System.Windows.Controls.DockPanel]::SetDock($bar,'Top');[void]$layout.Children.Add($bar)
    $refresh=New-ProfileToolButton '새로고침';[void]$bar.Children.Add($refresh)
    $root=New-ProfileToolButton '여기로 필드 끌기 → 최상위로 이동';$root.AllowDrop=$true;[void]$bar.Children.Add($root)
    $note=[System.Windows.Controls.TextBlock]::new();$note.Text='필드 삭제는 확인 후 진행합니다. 이름 변경·이동은 기존 필드 식별자를 유지합니다.';$note.TextWrapping='Wrap';$note.Margin='4,10';[System.Windows.Controls.DockPanel]::SetDock($note,'Bottom');[void]$layout.Children.Add($note)
    $scroll=[System.Windows.Controls.ScrollViewer]::new();$scroll.HorizontalScrollBarVisibility='Auto';$scroll.VerticalScrollBarVisibility='Auto';[void]$layout.Children.Add($scroll)
    $grid=[System.Windows.Controls.Grid]::new();$grid.VerticalAlignment='Top';$grid.Background='White';$scroll.Content=$grid
    $state=@{Dialog=$dialog;Grid=$grid;Profile=$null;Note=$note;Row=1;Depth=1;DragStart=$null;DragSource=$null;PageId=[Guid]::NewGuid().ToString()}
    $refresh.Add_Click({try{Update-ProfileTable $state}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $root.Add_DragOver({param($sender,$event)
        $event.Effects=[System.Windows.DragDropEffects]::None
        if($event.Data.GetDataPresent('GovOffice.ProfileTable')){$payload=$event.Data.GetData('GovOffice.ProfileTable');if($payload.kind -eq 'field' -and $payload.page_id -eq $state.PageId){$event.Effects=[System.Windows.DragDropEffects]::Move}};$event.Handled=$true
    }.GetNewClosure())
    $root.Add_Drop({param($sender,$event)
        $event.Handled=$true;if(-not $event.Data.GetDataPresent('GovOffice.ProfileTable')){return};$payload=$event.Data.GetData('GovOffice.ProfileTable');if($payload.kind -ne 'field' -or $payload.page_id -ne $state.PageId){return}
        try{Invoke-ProfileTableEdit $state @{operation='move_field';field_id=$payload.field_id;target_id=''}}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    Update-ProfileTable $state
    Show-WorkspaceWindow $dialog 'profile-data'
}
