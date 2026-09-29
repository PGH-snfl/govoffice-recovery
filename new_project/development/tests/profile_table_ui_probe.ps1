param([string]$Source,[string]$ImagePath)
$ErrorActionPreference='Stop'
function Test-WorkspaceWindow($Key){return $false}
Add-Type -AssemblyName PresentationFramework
function global:Show-Error($Message){throw $Message}
$global:Status=[System.Windows.Controls.TextBlock]::new()
$global:TableProbeCalls=[System.Collections.Generic.List[object]]::new()
$global:TableProbeProfile=[pscustomobject]@{ok=$true;values=@{test='snapshot'};field_groups=@(
    [pscustomobject]@{id='a';name='연구자';path='연구자';parent_id='';values=@();aliases=@();default=''},
    [pscustomobject]@{id='b';name='성명';path='연구자 > 성명';parent_id='a';values=@('홍길동','김하늘');aliases=@('이름');default='홍길동'},
    [pscustomobject]@{id='c';name='전화번호';path='연구자 > 전화번호';parent_id='a';values=@('010-1234-5678');aliases=@();default='010-1234-5678'},
    [pscustomobject]@{id='d';name='책임자';path='책임자';parent_id='';values=@('담당자');aliases=@();default='담당자'}
)}
function global:Send-Backend($Command){
    $global:TableProbeCalls.Add($Command)
    switch($Command.action){
        'user_profile_get' {return $global:TableProbeProfile}
        'user_profile_table_mutate' {return [pscustomobject]@{ok=$true;message='Saved'}}
        'user_profile_selection_analyze' {return [pscustomobject]@{ok=$true;draft_id='draft';candidates=@(
            [pscustomobject]@{candidate_id='selected';field='성명';value='홍길동';recommended=$true},
            [pscustomobject]@{candidate_id='unchecked';field='기타';value='읽지않음';recommended=$false})}}
        'user_profile_selection_save' {return [pscustomobject]@{ok=$true;message='Saved'}}
        default {throw "Unexpected $($Command.action)"}
    }
}
function Assert($Condition,$Message){if(-not $Condition){throw $Message}}
function Click($Button){$Button.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))}
function DoubleClick($Cell){
    $event=[System.Windows.Input.MouseButtonEventArgs]::new([System.Windows.Input.Mouse]::PrimaryDevice,0,[System.Windows.Input.MouseButton]::Left)
    [System.Windows.Input.MouseButtonEventArgs].GetProperty('ClickCount').SetValue($event,2,$null)
    $event.RoutedEvent=[System.Windows.UIElement]::PreviewMouseLeftButtonDownEvent;$Cell.RaiseEvent($event)
}
function Drop-On($Cell,$Payload){
    $data=[System.Windows.DataObject]::new();$data.SetData('GovOffice.ProfileTable',$Payload)
    $constructor=[System.Windows.DragEventArgs].GetConstructors([System.Reflection.BindingFlags]'Instance,NonPublic,Public')|Select-Object -First 1
    $args=$constructor.Invoke(@($data,[System.Windows.DragDropKeyStates]::LeftMouseButton,[System.Windows.DragDropEffects]::Move,$Cell.PSObject.BaseObject,[System.Windows.Point]::new(1,1)))
    $args.RoutedEvent=[System.Windows.DragDrop]::DropEvent;$Cell.RaiseEvent($args)
}
$sourceText=Get-Content -LiteralPath $Source -Raw -Encoding UTF8
$tokens=$null;$errors=$null;[void][System.Management.Automation.Language.Parser]::ParseInput($sourceText,[ref]$tokens,[ref]$errors)
Assert ($errors.Count -eq 0) 'PowerShell parse failed'
# Exercise production WPF controls/events in memory, without opening a user window.
$sourceText=$sourceText.Replace('[void]$dialog.ShowDialog()', '& $global:ProfileTableProbe')
$sourceText=$sourceText.Replace("Show-WorkspaceWindow `$dialog 'profile-data'", '& $global:ProfileTableProbe').Replace("Show-WorkspaceWindow `$dialog 'profile-import'", '& $global:ProfileTableProbe')
$sourceText=$sourceText.Replace('$dialog.DialogResult=$true', '$dialog.Close()')
Invoke-Expression $sourceText
$global:ProfileTableProbe={
    $fieldCells=@($grid.Children|Where-Object{$null -ne $_.ToolTip})
    $parent=@($fieldCells|Where-Object{$_.Child.Text -eq '연구자'})[0]
    $child=@($fieldCells|Where-Object{$_.Child.Text -like '성명*'})[0]
    $target=@($fieldCells|Where-Object{$_.Child.Text -eq '책임자'})[0]
    Assert ([System.Windows.Controls.Grid]::GetRowSpan($parent) -eq 3) 'Parent merge span'
    Assert ([System.Windows.Controls.Grid]::GetRowSpan($child) -eq 2) 'Multi-value field merge span'
    Assert ($child.ContextMenu.Items.Count -eq 5) 'Field context menu missing'
    $valueCell=@($grid.Children|Where-Object{$_.Child.Text -eq '김하늘'})[0]
    Assert ($valueCell.ContextMenu.Items.Count -eq 3) 'Value context menu missing'
    # Dialog prompts are stubbed; invoke the actual editing menu handlers.
    $global:ProfileEditResult='변경 시험값'
    function global:Read-ProfileTableText($OwnerWindow,$Title,$Value){return $global:ProfileEditResult}
    DoubleClick $child
    Assert ($global:TableProbeCalls[-2].operation -eq 'edit_field' -and $global:TableProbeCalls[-2].field_id -eq 'b') 'Field double-click did not use stable field ID'
    Assert ($null -eq $state.DragStart -and $null -eq $state.DragSource) 'Double-click left dragging armed'
    DoubleClick $valueCell
    Assert ($global:TableProbeCalls[-2].operation -eq 'edit_value' -and $global:TableProbeCalls[-2].value -eq '김하늘') 'Value double-click edited the wrong value'
    $count=$global:TableProbeCalls.Count;$global:ProfileEditResult=$null
    DoubleClick $valueCell
    Assert ($global:TableProbeCalls.Count -eq $count) 'Cancelled edit was saved'
    $global:ProfileEditResult='변경 시험값'
    $child.ContextMenu.Items[0].RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.MenuItem]::ClickEvent))
    Assert ($global:TableProbeCalls[-2].operation -eq 'edit_field' -and $global:TableProbeCalls[-2].name -eq '변경 시험값') 'Field rename menu not connected'
    $valueCell.ContextMenu.Items[0].RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.MenuItem]::ClickEvent))
    Assert ($global:TableProbeCalls[-2].operation -eq 'edit_value' -and $global:TableProbeCalls[-2].new_value -eq '변경 시험값') 'Value edit menu not connected'
    # Same production Drop handler: representative, child and value all emit stable IDs.
    Drop-On $target ([pscustomobject]@{page_id=$state.PageId;kind='field';field_id='a';value=''})
    Assert ($global:TableProbeCalls[-2].operation -eq 'move_field') 'Representative drag not connected'
    Assert ($global:TableProbeCalls[-2].field_id -eq 'a' -and $global:TableProbeCalls[-2].target_id -eq 'd') 'Representative IDs incorrect'
    Drop-On $target ([pscustomobject]@{page_id=$state.PageId;kind='field';field_id='b';value=''})
    Assert ($global:TableProbeCalls[-2].field_id -eq 'b') 'Child drag not connected'
    Drop-On $target ([pscustomobject]@{page_id=$state.PageId;kind='value';field_id='b';value='김하늘'})
    Assert ($global:TableProbeCalls[-2].operation -eq 'move_value' -and $global:TableProbeCalls[-2].value -eq '김하늘') 'Value drag not connected'
    $valueCell.ContextMenu.Items[1].RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.MenuItem]::ClickEvent))
    Assert ($global:TableProbeCalls[-2].operation -eq 'default') 'Default context menu not connected'
    Drop-On $root ([pscustomobject]@{page_id=$state.PageId;kind='field';field_id='b';value=''})
    Assert ($global:TableProbeCalls[-2].target_id -eq '') 'Root drop not connected'
    $count=$global:TableProbeCalls.Count
    Drop-On $target ([pscustomobject]@{page_id='other';kind='field';field_id='b';value=''})
    Assert ($global:TableProbeCalls.Count -eq $count) 'Foreign drag accepted'
    if($ImagePath){
        $layout.Measure([System.Windows.Size]::new(940,580));$layout.Arrange([System.Windows.Rect]::new(0,0,940,580));$layout.UpdateLayout()
        $bitmap=[System.Windows.Media.Imaging.RenderTargetBitmap]::new(940,580,96,96,[System.Windows.Media.PixelFormats]::Pbgra32);$bitmap.Render($layout)
        $encoder=[System.Windows.Media.Imaging.PngBitmapEncoder]::new();$encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap));$stream=[System.IO.File]::Create($ImagePath);try{$encoder.Save($stream)}finally{$stream.Dispose()}
    }
    $dialog.Close()
}
Open-ProfileDataTable $null
$global:ProfileTableProbe={
    Assert ($table.Items.Count -eq 2) 'Import candidates missing'
    # Realize the production template in memory, without showing a window.
    $table.Measure([System.Windows.Size]::new(900,300))
    $table.Arrange([System.Windows.Rect]::new(0,0,900,300));$table.UpdateLayout()
    function Find-Toggle($Node){
        if($Node -is [System.Windows.Controls.CheckBox] -and $Node.Name -eq 'SelectionToggle'){return $Node}
        for($i=0;$i -lt [System.Windows.Media.VisualTreeHelper]::GetChildrenCount($Node);$i++){
            $found=Find-Toggle ([System.Windows.Media.VisualTreeHelper]::GetChild($Node,$i))
            if($null -ne $found){return $found}
        }
    }
    $cellContent=$check.GetCellContent($rows[0])
    Assert ($null -ne $cellContent) 'Selection cell not realized'
    $toggle=Find-Toggle $cellContent
    Assert ($null -ne $toggle) 'Full-cell checkbox missing'
    Assert ($toggle.ActualWidth -ge 50 -and $toggle.ActualHeight -ge 30) 'Checkbox does not cover the cell'
    foreach($point in @([System.Windows.Point]::new(2,2),[System.Windows.Point]::new(($toggle.ActualWidth-2),($toggle.ActualHeight-2)))){
        # The owner is deliberately never shown, so InputHitTest excludes the
        # entire invisible window. Inspect the measured visual geometry instead.
        $hitResult=[System.Windows.Media.VisualTreeHelper]::HitTest($toggle,$point)
        $hit=if($null -ne $hitResult){$hitResult.VisualHit}else{$null}
        while($null -ne $hit -and $hit -ne $toggle){$hit=[System.Windows.Media.VisualTreeHelper]::GetParent($hit)}
        Assert ($hit -eq $toggle) 'Blank cell padding does not route to checkbox'
    }
    $mark=$toggle.Template.FindName('SelectionMark',$toggle)
    Assert (-not $mark.IsHitTestVisible -and -not $mark.Focusable) 'Inner visual could toggle twice'
    $peer=[System.Windows.Automation.Peers.CheckBoxAutomationPeer]::new($toggle)
    $provider=[System.Windows.Automation.Provider.IToggleProvider]$peer.GetPattern([System.Windows.Automation.Peers.PatternInterface]::Toggle)
    Assert ([bool]$rows[0].selected) 'Initial checked state missing'
    $provider.Toggle()
    Assert (-not $rows[0].selected -and -not $rows[1].selected) 'Toggle off did not update only its row'
    $provider.Toggle()
    Assert ($rows[0].selected -and -not $rows[1].selected) 'Toggle on did not update only its row'
    Assert (-not $table.Columns[1].IsReadOnly -and -not $table.Columns[2].IsReadOnly) 'Text editing disabled'
    $rows[0].field='연구자 > 성명';$rows[0].value='수정한 이름'
    Click $save
    $command=$global:TableProbeCalls[-1]
    Assert ($command.action -eq 'user_profile_selection_save') 'Import save not connected'
    Assert ($command.rows.Count -eq 1 -and $command.rows[0].candidate_id -eq 'selected') 'Unchecked candidate saved'
    Assert ($command.rows[0].field -eq '연구자 > 성명' -and $command.rows[0].value -eq '수정한 이름') 'Edited import not saved'
}
Open-ProfileSelectionImport $null
Write-Output 'PROFILE_TABLE_UI_OK: merged cells, field/child/value/root drops, context menu, selection import'
