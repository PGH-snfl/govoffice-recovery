# Document writing stays in a background worker; this window only polls short commands.
function Open-DocumentAuthoring($OwnerWindow) {
    if(Test-WorkspaceWindow 'authoring'){return}
    # Reuse the existing modal-session isolation, including queued-tick guards
    # and restoring only timers which were running before this dialog opened.
    Invoke-ProfileReviewSession $OwnerWindow {param($owner) Show-DocumentAuthoring $owner}
}
function New-AuthoringInputTree($Rows) {
    $Root=@{children=[System.Collections.Generic.List[object]]::new();rows=@();depth=0}
    foreach($Row in $Rows){
        $Parts=@($Row.path | Where-Object {-not [string]::IsNullOrWhiteSpace([string]$_)})
        if($Parts.Count -eq 0){$Parts=@([string]$Row.topic)+@(([string]$Row.label -split '>') | ForEach-Object {$_.Trim()} | Where-Object {$_})}
        if($Parts.Count -eq 0){$Parts=@('문서 입력정보',[string]$Row.id)}
        $Node=$Root;$Path=[System.Collections.Generic.List[string]]::new()
        foreach($Part in $Parts){
            $Path.Add([string]$Part)
            $Child=$null
            foreach($Candidate in $Node.children){if($Candidate.name -ceq $Part){$Child=$Candidate;break}}
            if($null -eq $Child){
                $Child=@{name=[string]$Part;key=($Path.ToArray() | ConvertTo-Json -Compress);children=[System.Collections.Generic.List[object]]::new();rows=[System.Collections.Generic.List[object]]::new()}
                $Node.children.Add($Child)
            }
            $Node=$Child
        }
        $Node.rows.Add($Row)
        $Root.depth=[Math]::Max($Root.depth,$Parts.Count)
    }
    return $Root
}
function Add-AuthoringInputCell($Table,$Child,[int]$Row,[int]$Column,[int]$Span=1,[string]$Color='White') {
    if($Table.ReadOnly){$Color=if($Row -eq 0){'#DDE0E4'}else{'#ECEDEF'}}
    $Cell=[System.Windows.Controls.Border]::new();$Cell.Background=$Color;$Cell.BorderBrush='#DDD5E7';$Cell.BorderThickness='0,0,1,1';$Cell.Padding='8,7';$Cell.Child=$Child
    [System.Windows.Controls.Grid]::SetRow($Cell,$Row);[System.Windows.Controls.Grid]::SetColumn($Cell,$Column);[System.Windows.Controls.Grid]::SetRowSpan($Cell,$Span)
    [void]$Table.Grid.Children.Add($Cell)
    return $Cell
}
function New-AuthoringInputText([string]$Text) {
    $Label=[System.Windows.Controls.TextBlock]::new();$Label.Text=$Text;$Label.TextWrapping='Wrap';$Label.VerticalAlignment='Center'
    return $Label
}
function Add-AuthoringInputBranch($Table,$Node,[int]$Depth) {
    $Start=$Table.Row
    $Collapsed=$Table.Collapsed.ContainsKey($Node.key) -and $Table.Collapsed[$Node.key]
    if($Collapsed){
        $Definition=[System.Windows.Controls.RowDefinition]::new();$Definition.Height='Auto';$Definition.MinHeight=42;$Table.Grid.RowDefinitions.Add($Definition)
        $Cell=Add-AuthoringInputCell $Table (New-AuthoringInputText '접힌 항목 · 펼치면 입력값을 확인할 수 있습니다.') $Table.Row ($Depth+1)
        $Extra=if($Table.PersonalOnly){0}else{1}
        [System.Windows.Controls.Grid]::SetColumnSpan($Cell,($Table.Depth+$Extra-$Depth));$Table.Row++
    }else{
        foreach($Row in $Node.rows){
            $Definition=[System.Windows.Controls.RowDefinition]::new();$Definition.Height='Auto';$Definition.MinHeight=48;$Table.Grid.RowDefinitions.Add($Definition)
            $Button=[System.Windows.Controls.Button]::new();$Button.Padding='7';$Button.Margin='0';$Button.HorizontalContentAlignment='Stretch';$Button.Tag=$Row.id
            $Button.ToolTip=if($Table.PersonalOnly){"$($Row.context)`n연결된 문서 칸: $(@($Row.field_ids).Count)개"}else{"문서 위치: $($Row.id)`n$($Row.context)"}
            $Value=New-AuthoringInputText $(if($Row.ai -and -not $Row.value){'AI 작성 예정'}elseif(-not $Row.value){'(빈칸)'}else{[string]$Row.value})
            $Button.Content=$Value
            if($Table.ReadOnly){$Button.Background='#ECEDEF';$Button.Foreground='#60646C';$Button.Cursor='Arrow'}
            $Button.Add_Click({& $Table.Select $Row}.GetNewClosure())
            $Button.Add_PreviewMouseDoubleClick({param($Sender,$Event)
                if($Table.ReadOnly -or $Event.ChangedButton -ne [System.Windows.Input.MouseButton]::Left -or -not $Sender.IsEnabled){return}
                $Event.Handled=$true;& $Table.EditValue $Row
            }.GetNewClosure())
            $Button.ToolTip+=if($Table.ReadOnly){"`n작업 시작 당시 값 · 수정 불가"}else{"`n더블클릭: 값 수정창 바로 열기"}
            [void](Add-AuthoringInputCell $Table $Button $Table.Row $Table.Depth)
            $Toggle=$null
            if(-not $Table.PersonalOnly){
            $Toggle=[System.Windows.Controls.CheckBox]::new();$Toggle.IsThreeState=$false;$Toggle.IsChecked=[bool]$Row.ai;$Toggle.HorizontalAlignment='Center';$Toggle.VerticalAlignment='Center';$Toggle.Tag=$Row.id
            $Toggle.ToolTip='켜기: AI 본문 작성 / 끄기: 직접 입력값 사용'
            $Toggle.IsEnabled=-not $Table.ReadOnly
            $Toggle.Add_Click({param($Sender,$Event) if($Table.ReadOnly){return};$Row.ai=[bool]$Sender.IsChecked;& $Table.Changed $Row}.GetNewClosure())
            [void](Add-AuthoringInputCell $Table $Toggle $Table.Row ($Table.Depth+1))
            }
            $Table.Cells[$Row.id]=@{Button=$Button;Text=$Value;Toggle=$Toggle;Row=$Row}
            $Table.Row++
        }
        foreach($Child in $Node.children){Add-AuthoringInputBranch $Table $Child ($Depth+1)}
    }
    $Label=New-AuthoringInputText $Node.name;$Label.FontWeight='SemiBold'
    $NameControl=[System.Windows.Controls.Label]::new();$NameControl.Content=$Label;$NameControl.Padding='3,6';$NameControl.VerticalContentAlignment='Center'
    $NameControl.ToolTip=if($Table.PersonalOnly){'개인 탭에 저장된 항목'}else{'더블클릭: 항목 이름 수정 (이 작성 화면에만 적용)'}
    $NameControl.Add_PreviewMouseDoubleClick({param($Sender,$Event)
        if($Table.ReadOnly -or $Table.PersonalOnly -or $Event.ChangedButton -ne [System.Windows.Input.MouseButton]::Left -or -not $Sender.IsEnabled){return}
        $Event.Handled=$true;& $Table.EditName $Node $Depth
    }.GetNewClosure())
    $Table.Labels[$Node.key]=$NameControl
    $Content=$NameControl
    if($Node.children.Count -gt 0 -or $Node.rows.Count -gt 1){
        $Button=[System.Windows.Controls.Button]::new();$Button.Padding='4,6';$Button.Margin='0';$Button.Tag=$Node.key
        $Button.Content=if($Collapsed){'▶'}else{'▼'}
        $Button.ToolTip='하위 항목 접기 / 펼치기 · 입력값은 그대로 유지됩니다.'
        $Button.Add_Click({$Table.Collapsed[$Node.key]=-not ($Table.Collapsed.ContainsKey($Node.key) -and $Table.Collapsed[$Node.key]);& $Table.Render}.GetNewClosure())
        $Table.Groups[$Node.key]=$Button
        $Panel=[System.Windows.Controls.DockPanel]::new();$Panel.LastChildFill=$true
        [System.Windows.Controls.DockPanel]::SetDock($Button,'Left');[void]$Panel.Children.Add($Button);[void]$Panel.Children.Add($NameControl);$Content=$Panel
    }
    [void](Add-AuthoringInputCell $Table $Content $Start $Depth ($Table.Row-$Start) '#F0EAF7')
}
function Show-AuthoringInputTable($Table,$Rows) {
    $Tree=New-AuthoringInputTree $Rows;$Table.Depth=[Math]::Max(2,$Tree.depth);$Table.Row=1;$Table.Tree=$Tree
    $Extra=if($Table.PersonalOnly){1}else{2}
    $Table.Grid.MinWidth=$Table.Depth*125+200
    $Table.Cells=@{};$Table.Groups=@{};$Table.Labels=@{}
    $Table.Grid.Children.Clear();$Table.Grid.RowDefinitions.Clear();$Table.Grid.ColumnDefinitions.Clear()
    for($Index=0;$Index -lt $Table.Depth+$Extra;$Index++){
        $Column=[System.Windows.Controls.ColumnDefinition]::new()
        $Column.Width=if($Index -eq $Table.Depth){'2*'}elseif($Index -eq $Table.Depth+1){'70'}else{'*'}
        $Column.MinWidth=if($Index -eq $Table.Depth){200}elseif($Index -eq $Table.Depth+1){70}else{125}
        $Table.Grid.ColumnDefinitions.Add($Column)
    }
    $Header=[System.Windows.Controls.RowDefinition]::new();$Header.Height='Auto';$Table.Grid.RowDefinitions.Add($Header)
    for($Index=0;$Index -lt $Table.Depth+$Extra;$Index++){
        $Title=if($Index -eq 0){'대표항목'}elseif($Index -eq $Table.Depth){'문서에 넣을 값'}elseif($Index -eq $Table.Depth+1){'AI 본문'}else{"하위항목 $Index"}
        $Text=New-AuthoringInputText $Title;$Text.FontWeight='SemiBold'
        [void](Add-AuthoringInputCell $Table $Text 0 $Index 1 '#E8E0F0')
    }
    foreach($Node in $Tree.children){Add-AuthoringInputBranch $Table $Node 0}
    if($Rows.Count -eq 0){
        $Definition=[System.Windows.Controls.RowDefinition]::new();$Definition.Height='Auto';$Table.Grid.RowDefinitions.Add($Definition)
        $Empty=if($Table.PersonalOnly){'이 양식에 연결된 저장 정보가 없습니다. 추가 입력 없이 작성할 수 있습니다.'}else{'직접 입력할 항목이 없습니다. AI 본문 칸도 보려면 위의 모두 보기를 켜세요.'}
        $Cell=Add-AuthoringInputCell $Table (New-AuthoringInputText $Empty) 1 0
        [System.Windows.Controls.Grid]::SetColumnSpan($Cell,($Table.Depth+$Extra))
    }
    $widthKeys=@(for($i=0;$i -lt $Table.Depth;$i++){"field-$i"})+@('value')
    if(-not $Table.PersonalOnly){$widthKeys+=@('ai')}
    Add-FieldTableColumnResize $Table $widthKeys
}
