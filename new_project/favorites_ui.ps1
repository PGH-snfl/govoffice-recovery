# WPF favorites UI. Backend owns persistence and execution validation.
function Invoke-Favorite([string]$Id) {
    try{$r=Send-Backend @{action='favorite_run';id=$Id};if(-not $r.ok){throw $r.message};$Status.Text=$r.message;Refresh-HwpDocumentStatus $true}catch{Show-Error $_.Exception.Message}
}

function Invoke-FavoritePreview($Command) {
    if($null -eq $script:PreviewFavoriteItems){$script:PreviewFavoriteItems=New-Object System.Collections.ArrayList}
    $Entries=@();$index=0;foreach($item in @($Layout.tabs[0].buttons|Where-Object{$_.enabled -and @($_.operations).Count}|Select-Object -First 2)){$Entries+=,[pscustomobject]@{id="preview-$index";name=$item.name;category='표';operations=$item.operations};$index++}
    switch($Command.action){
        'favorite_catalog' {return [pscustomobject]@{ok=$true;entries=$Entries}}
        'favorite_list' {return [pscustomobject]@{ok=$true;favorites=@($script:PreviewFavoriteItems)}}
        'favorite_save' {$id=if($Command.id){$Command.id}else{[guid]::NewGuid().ToString()};$old=@($script:PreviewFavoriteItems|Where-Object{$_.id -eq $id});foreach($item in $old){$script:PreviewFavoriteItems.Remove($item)};[void]$script:PreviewFavoriteItems.Add([pscustomobject]@{id=$id;name=$Command.name;catalog_id=$Command.catalog_id;operations=$Command.operations;available=$true});return [pscustomobject]@{ok=$true}}
        'favorite_delete' {$old=@($script:PreviewFavoriteItems|Where-Object{$_.id -eq $Command.id});foreach($item in $old){$script:PreviewFavoriteItems.Remove($item)};return [pscustomobject]@{ok=$true}}
        'favorite_run' {return [pscustomobject]@{ok=$true;message='미리보기: 실제 한글에는 실행하지 않았습니다.'}}
        'favorite_move' {return [pscustomobject]@{ok=$true;message='순서 저장은 자동 테스트로 확인합니다.'}}
    }
}

function Edit-Favorite($Entry,$Existing,$OwnerWindow) {
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='즐겨찾기 이름 · 입력값';$Dialog.Width=460;$Dialog.Height=520;$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.Background='White'
    $Root=[System.Windows.Controls.DockPanel]::new();$Root.Margin=12;$Dialog.Content=$Root
    $Save=[System.Windows.Controls.Button]::new();$Save.Content='즐겨찾기 저장';$Save.Height=34;Set-OriginalFlatButton $Save $true;[System.Windows.Controls.DockPanel]::SetDock($Save,'Bottom');[void]$Root.Children.Add($Save)
    $Scroll=[System.Windows.Controls.ScrollViewer]::new();$Panel=[System.Windows.Controls.StackPanel]::new();$Scroll.Content=$Panel;[void]$Root.Children.Add($Scroll)
    $Label=[System.Windows.Controls.TextBlock]::new();$Label.Text='표시할 이름';[void]$Panel.Children.Add($Label)
    $Name=[System.Windows.Controls.TextBox]::new();$Name.Text=if($Existing){$Existing.name}else{$Entry.name};$Name.Margin='0,4,0,12';[void]$Panel.Children.Add($Name)
    $Original=if($Existing){$Existing.operations}else{$Entry.operations}
    $Decoded=ConvertFrom-Json -InputObject (ConvertTo-Json -InputObject @($Original) -Depth 40)
    $Operations=@($Decoded)
    $Inputs=New-Object System.Collections.ArrayList
    foreach($Operation in $Operations){
        if($Operation.type -eq 'method'){$Operation.args=@($Operation.args)}
        $Title=[System.Windows.Controls.TextBlock]::new();$Title.Text=if($Operation.method){$Operation.method}else{$Operation.command};$Title.FontWeight='Bold';$Title.Margin='0,8';[void]$Panel.Children.Add($Title)
        for($index=0;$index -lt @($Operation.args).Count;$index++){
            $value=$Operation.args[$index];$Label=[System.Windows.Controls.TextBlock]::new();$Label.Text="입력값 $($index+1)";[void]$Panel.Children.Add($Label)
            $Input=[System.Windows.Controls.TextBox]::new();$Input.Margin='0,3,0,8';$Input.Text=[string]$value
            if($value -is [pscustomobject] -or $value -is [array]){$Input.Text='내장 자료 (변경하지 않음)';$Input.IsReadOnly=$true}
            [void]$Panel.Children.Add($Input);[void]$Inputs.Add([pscustomobject]@{control=$Input;operation=$Operation;index=$index;original=$value})
        }
    }
    $Notice=[System.Windows.Controls.TextBlock]::new();$Notice.Text='저장한 입력값으로 바로 실행합니다. 기능 자체의 대화상자는 표시될 수 있습니다.';$Notice.TextWrapping='Wrap';$Notice.Margin='0,12';[void]$Panel.Children.Add($Notice)
    $Save.Add_Click({try{
        foreach($item in $Inputs){
            $text=$item.control.Text;$old=$item.original
            if($old -is [pscustomobject] -or $old -is [array]){continue}
            if($old -is [bool]){$value=[bool]::Parse($text)}
            elseif($old -is [int] -or $old -is [long]){$value=[long]::Parse($text,[Globalization.CultureInfo]::InvariantCulture)}
            elseif($old -is [double] -or $old -is [decimal]){$value=[double]::Parse($text,[Globalization.CultureInfo]::InvariantCulture)}
            elseif($null -eq $old){$value=$null}else{$value=$text}
            $item.operation.args[$item.index]=$value
        }
        $command=@{action='favorite_save';catalog_id=$Entry.id;name=$Name.Text;operations=@($Operations)};if($Existing){$command.id=$Existing.id}
        $r=Send-Backend $command;if(-not $r.ok){throw $r.message};$Dialog.Close()
    }catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    [void]$Dialog.ShowDialog()
}

function Open-Favorites($OwnerWindow=$Window,[string]$InstitutionId='') {
    if(Test-WorkspaceWindow "favorites:$InstitutionId"){return}
    try{$r=Send-Backend @{action='favorite_catalog';institution_id=$InstitutionId};if(-not $r.ok){throw $r.message};$Entries=@($r.entries)}catch{Show-Error $_.Exception.Message;return}
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='즐겨찾기 추가 · 관리';$Dialog.Width=760;$Dialog.Height=550;$Dialog.MinWidth=620;$Dialog.MinHeight=420;$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.Background='White'
    $Grid=[System.Windows.Controls.Grid]::new();$Grid.Margin=12;$Dialog.Content=$Grid
    foreach($h in @(34,'*',42)){$row=[System.Windows.Controls.RowDefinition]::new();$row.Height=[System.Windows.GridLengthConverter]::new().ConvertFromString([string]$h);[void]$Grid.RowDefinitions.Add($row)}
    foreach($i in 0..1){[void]$Grid.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new())}
    $Heading=[System.Windows.Controls.TextBlock]::new();$Heading.Text='내 즐겨찾기 · 더블클릭으로 실행';$Heading.FontWeight='Bold';$Heading.Margin=5;[void]$Grid.Children.Add($Heading)
    $SearchRow=[System.Windows.Controls.DockPanel]::new();$SearchRow.Margin='5,0,0,5';[System.Windows.Controls.Grid]::SetColumn($SearchRow,1);[void]$Grid.Children.Add($SearchRow)
    $SearchLabel=[System.Windows.Controls.TextBlock]::new();$SearchLabel.Text='기능 검색';$SearchLabel.Margin='0,5,8,0';[void]$SearchRow.Children.Add($SearchLabel)
    $Search=[System.Windows.Controls.TextBox]::new();$Search.ToolTip='추가할 기능 검색';[void]$SearchRow.Children.Add($Search)
    $Favorites=[System.Windows.Controls.ListBox]::new();$Favorites.DisplayMemberPath='name';$Favorites.Margin='0,0,5,0';[System.Windows.Controls.Grid]::SetRow($Favorites,1);[void]$Grid.Children.Add($Favorites)
    $Catalog=[System.Windows.Controls.ListBox]::new();$Catalog.DisplayMemberPath='display';[System.Windows.Controls.Grid]::SetColumn($Catalog,1);[System.Windows.Controls.Grid]::SetRow($Catalog,1);[void]$Grid.Children.Add($Catalog)
    $Filter={ $Catalog.Items.Clear();foreach($entry in $Entries){$display="$($entry.category) · $($entry.name)";if(-not $Search.Text -or $display.IndexOf($Search.Text,[StringComparison]::OrdinalIgnoreCase) -ge 0){[void]$Catalog.Items.Add([pscustomobject]@{display=$display;entry=$entry})}}}.GetNewClosure()
    $Refresh={param([string]$SelectedId='') $r=Send-Backend @{action='favorite_list';institution_id=$InstitutionId};if(-not $r.ok){throw $r.message};$Favorites.Items.Clear();foreach($item in @($r.favorites)){[void]$Favorites.Items.Add($item);if($item.id -eq $SelectedId){$Favorites.SelectedItem=$item}}}.GetNewClosure()
    $Actions=[System.Windows.Controls.WrapPanel]::new();[System.Windows.Controls.Grid]::SetRow($Actions,2);[System.Windows.Controls.Grid]::SetColumnSpan($Actions,2);[void]$Grid.Children.Add($Actions)
    foreach($label in @('실행','수정','해제','위로','아래로','선택 기능 추가')){
        $Button=[System.Windows.Controls.Button]::new();$Button.Content=$label;$Button.Margin='0,6,6,0';$Button.Padding='10,4';Set-OriginalFlatButton $Button ($label -eq '선택 기능 추가');[void]$Actions.Children.Add($Button)
        $Button.Add_Click({try{
            $action=[string]$this.Content;$item=$Favorites.SelectedItem
            if($action -eq '선택 기능 추가'){if($Catalog.SelectedItem){Edit-Favorite $Catalog.SelectedItem.entry $null $Dialog;& $Refresh};return}
            if(-not $item){return}
            if($action -eq '실행'){Invoke-Favorite $item.id;return}
            if($action -eq '수정'){$entry=@($Entries|Where-Object{$_.id -eq $item.catalog_id}|Select-Object -First 1);if(-not $entry.Count){throw '이전 버전 즐겨찾기는 오른쪽 기능 목록에서 다시 추가해 주세요.'};Edit-Favorite $entry[0] $item $Dialog}
            else{$command=@{id=$item.id;institution_id=$InstitutionId};if($action -eq '해제'){$command.action='favorite_delete'}else{$command.action='favorite_move';$command.direction=if($action -eq '위로'){-1}else{1}};$r=Send-Backend $command;if(-not $r.ok){throw $r.message}}
            & $Refresh $item.id
        }catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    }
    $Search.Add_TextChanged({& $Filter}.GetNewClosure());$Favorites.Add_MouseDoubleClick({if($Favorites.SelectedItem){Invoke-Favorite $Favorites.SelectedItem.id}}.GetNewClosure())
    try{& $Filter;& $Refresh}catch{Show-Error $_.Exception.Message}
    Show-WorkspaceWindow $Dialog "favorites:$InstitutionId"
}

function New-FavoriteStrip($OwnerWindow,[string]$InstitutionId='') {
    $Panel=[System.Windows.Controls.WrapPanel]::new();$Panel.Margin=4
    $State=[pscustomobject]@{Refresh=$null}
    $Refresh={
        $Panel.Children.Clear();$Manage=[System.Windows.Controls.Button]::new();$Manage.Content='★ 즐겨찾기 · 관리';$Manage.Margin=2;$Manage.Padding='6,3';Set-OriginalFlatButton $Manage $false;[void]$Panel.Children.Add($Manage)
        $Manage.Tag=[pscustomobject]@{owner=$OwnerWindow;institution=$InstitutionId;state=$State}
        $Manage.Add_Click({$ctx=$this.Tag;Open-Favorites $ctx.owner $ctx.institution;Add-WorkspaceClosedAction ('favorites:'+$ctx.institution) $ctx.state.Refresh;& $ctx.state.Refresh})
        try{$r=Send-Backend @{action='favorite_list';institution_id=$InstitutionId};if(-not $r.ok){throw $r.message};foreach($item in @($r.favorites)){
            $Button=[System.Windows.Controls.Button]::new();$Button.Content=$item.name;$Button.ToolTip=$item.name;$Button.MaxWidth=160;$Button.Margin=2;$Button.Padding='6,3';$Button.Tag=$item.id;$Button.IsEnabled=($item.available -ne $false);Set-OriginalFlatButton $Button $true;$Button.Add_Click({Invoke-Favorite ([string]$this.Tag)});[void]$Panel.Children.Add($Button)
        }}catch{$Text=[System.Windows.Controls.TextBlock]::new();$Text.Text=$_.Exception.Message;[void]$Panel.Children.Add($Text)}
    }.GetNewClosure()
    $State.Refresh=$Refresh;& $Refresh
    return ,$Panel
}

function Add-InstitutionFavorites($Dialog,[string]$InstitutionId) {
    $Previous=$Dialog.Content;$Dialog.Content=$null;$Dock=[System.Windows.Controls.DockPanel]::new();$Dialog.Content=$Dock
    $Scroll=[System.Windows.Controls.ScrollViewer]::new();$Scroll.MaxHeight=80;$Scroll.VerticalScrollBarVisibility='Auto';$Scroll.Content=New-FavoriteStrip $Dialog $InstitutionId
    [System.Windows.Controls.DockPanel]::SetDock($Scroll,'Top');[void]$Dock.Children.Add($Scroll);[void]$Dock.Children.Add($Previous)
}
