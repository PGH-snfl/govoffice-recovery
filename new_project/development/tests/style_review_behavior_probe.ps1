param([string]$Launcher)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
$source=Get-Content -LiteralPath $Launcher -Raw -Encoding UTF8
$tokens=$null;$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseInput($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw $errors[0]}
$function=$ast.Find({param($node)
    $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and
    $node.Name -eq 'Open-StyleCaptureReview'
},$true)
if($null -eq $function){throw 'Review function missing'}
# Execute the production dialog and its handlers without displaying a test window.
# Only the modal wait is replaced with a synchronous probe in the same scope.
$definition=$function.Extent.Text.Replace('[void]$Dialog.ShowDialog()', '& $script:ReviewProbe')
Invoke-Expression $definition
function global:New-PurpleAccentBrush { return [System.Windows.Media.Brushes]::Purple }
function global:Set-OriginalSectionHeader {}
function global:Set-OriginalFlatButton {}
function global:Write-GuiRuntimeError($context,$failure){throw $failure}
function global:Show-Error($message){throw $message}
$LayoutPreview=$false

function Assert-Equal($actual,$expected,$message){
    if(($actual -join '|') -cne ($expected -join '|')){
        throw ($message+': expected '+($expected -join '|')+', got '+($actual -join '|'))
    }
}
function New-Candidate($id,$group,$child,[bool]$recommended,[int]$order){
    [pscustomobject]@{
        candidate_id=$id;field="$group > $child";field_path="$group > $child"
        semantic_group_id=$group;semantic_representative_field=$group
        semantic_child_field=$child;semantic_child_id=$child
        recommended=$recommended;registered=$false;value="value-$id"
        direction='right';table=0;row=$order;col=0;document_order=$order
        relationship_anchor_order=$order;relationship_sort_rank=0
    }
}
function Click-Check($check){
    # OnClick applies ToggleButton's real two/three-state transition before Click.
    $method=[System.Windows.Controls.Primitives.ToggleButton].GetMethod('OnClick',[System.Reflection.BindingFlags]'Instance,NonPublic')
    [void]$method.Invoke($check,@())
}

# Interleaved input tests stable group ordering and stable ordering within groups.
$analysis=[pscustomobject]@{candidates=@(
    (New-Candidate 'a-low1' 'A' 'a1' $false 0),
    (New-Candidate 'b-low1' 'B' 'b1' $false 1),
    (New-Candidate 'c-high1' 'C' 'c1' $true 2),
    (New-Candidate 'b-high1' 'B' 'b2' $true 3),
    (New-Candidate 'b-low2' 'B' 'b3' $false 4),
    (New-Candidate 'd-low1' 'D' 'd1' $false 5),
    (New-Candidate 'b-high2' 'B' 'b4' $true 6)
)}
$script:ReviewProbe={
    $expected=@('b-high1','b-high2','b-low1','b-low2','c-high1','a-low1','d-low1')
    Assert-Equal @($Checks|ForEach-Object{$_.Tag.row.ids[0]}) $expected 'Initial priority/order'
    $bChecks=@($Checks|Where-Object{$_.Tag.row.group_key -eq 'B'})
    $parent=$bChecks[0].Tag.group.Parent
    Assert-Equal $parent.IsThreeState $false 'Representative must be two-state'
    Assert-Equal $parent.IsChecked $true 'Partly selected group must be on'
    Click-Check $parent
    Assert-Equal @($bChecks|ForEach-Object{$_.IsChecked}) @($false,$false,$false,$false) 'Group off'
    Click-Check $parent
    Assert-Equal @($bChecks|ForEach-Object{$_.IsChecked}) @($true,$true,$true,$true) 'Group on'
    Click-Check $bChecks[0]
    Assert-Equal $parent.IsChecked $true 'Remaining selected children keep group on'
    & $ReviewActions.Rebuild
    Assert-Equal @($Checks|ForEach-Object{$_.Tag.row.ids[0]}) $expected 'Manual toggles must not reorder'
    $bChecks=@($Checks|Where-Object{$_.Tag.row.group_key -eq 'B'})
    foreach($check in $bChecks){if($check.IsChecked){Click-Check $check}}
    Assert-Equal $bChecks[0].Tag.group.Parent.IsChecked $false 'All children off'
    $Dialog.Close()
}
[void](Open-StyleCaptureReview $analysis $null)

$analysis=[pscustomobject]@{candidates=@(
    (New-Candidate 'source1' 'Source' 'name' $true 0),
    (New-Candidate 'source2' 'Source' 'phone' $false 1),
    (New-Candidate 'target' 'Target' 'email' $true 2),
    (New-Candidate 'third' 'Third' 'department' $true 3)
)}
$script:ReviewProbe={
    & $ReviewActions.MoveGroup 'Source' $CandidateById['target']
    Assert-Equal @($AllCandidates|Where-Object{$_.group_key -eq 'Source'}).Count 0 'Source card removed'
    Assert-Equal @($AllCandidates|Where-Object{$_.group_key -eq 'Target'}).Count 3 'Children join target directly'
    Assert-Equal $CandidateOverrides['source1'].field 'Target > name' 'No intermediate Source level'
    Assert-Equal $CandidateOverrides['source2'].field 'Target > phone' 'All children moved including unchecked'
    Assert-Equal $CandidateOverrides['source1'].kind 'child' 'Save as direct child move'
    Assert-Equal $Selected['source2'] $false 'Unchecked child must stay unchecked'
    Assert-Equal $CandidateById['source1'].value 'value-source1' 'Value unchanged'
    & $ReviewActions.MoveChild 'source2' $CandidateById['third']
    Assert-Equal $CandidateOverrides['source2'].field 'Third > phone' 'Child can be moved again'
    & $ReviewActions.MoveGroup 'Target' $CandidateById['third']
    Assert-Equal $CandidateOverrides['source1'].field 'Third > name' 'Group can be moved again'
    Assert-Equal $CandidateOverrides['target'].field 'Third > email' 'Original target child also moves'
    Assert-Equal @($AllCandidates|Where-Object{$_.group_key -eq 'Third'}).Count 4 'One final group'
    # Confirm uses the actual serialization handler; excluded candidates stay excluded.
    $Confirm.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))
}
$saved=Open-StyleCaptureReview $analysis $null
Assert-Equal @($saved.candidate_ids|Sort-Object) @('source1','target','third') 'Saved selection'
Assert-Equal $saved.candidate_field_overrides['source1'].target_parent 'Third' 'Saved parent'
Assert-Equal $saved.candidate_field_overrides['source2'].field 'Third > phone' 'Saved unchecked override remains optional'

$analysis=[pscustomobject]@{candidates=@(
    (New-Candidate 'source1' 'Source' 'phone' $true 0),
    (New-Candidate 'source2' 'Source' 'name' $true 1),
    (New-Candidate 'target' 'Target' 'name' $true 2)
)}
$script:ReviewProbe={
    & $ReviewActions.MoveGroup 'Source' $CandidateById['source1']
    Assert-Equal $CandidateOverrides.Count 0 'Self drop is no-op'
    & $ReviewActions.MoveGroup 'Source' $CandidateById['target']
    Assert-Equal $CandidateOverrides.Count 0 'Collision must not partially move children'
    Assert-Equal $CandidateById['source1'].full_field 'Source > phone' 'First child untouched on later collision'
    & $ReviewActions.MoveChild 'source1' $CandidateById['target']
    Assert-Equal $CandidateOverrides.Count 1 'Non-conflicting individual move still works'
    $ResetMove.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))
    Assert-Equal $CandidateOverrides.Count 0 'Reset clears overrides'
    Assert-Equal $CandidateById['source1'].full_field 'Source > phone' 'Reset restores source'
    $Dialog.Close()
}
[void](Open-StyleCaptureReview $analysis $null)
# Normalized candidates from multiple locations share one card without losing
# different values of the same child field, or folded duplicate locations.
$same1=New-Candidate 'same1' 'Research' 'name' $true 0
$same2=New-Candidate 'same2' 'Research' 'name' $true 1
$same3=New-Candidate 'same3' 'Research' 'name' $true 2
$same3.value=$same1.value
$analysis=[pscustomobject]@{candidates=@($same1,$same2,$same3)}
$script:ReviewProbe={
    Assert-Equal @($Checks).Count 2 'Different values visible, identical values folded'
    Assert-Equal @($AllCandidates|Select-Object -ExpandProperty group_key -Unique).Count 1 'One representative'
    Assert-Equal @($Checks[0].Tag.row.ids).Count 2 'Both identical-value locations retained'
    Assert-Equal @($AllCandidates|ForEach-Object{$_.value}) @('value-same1','value-same2') 'Values not overwritten'
    $Confirm.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Primitives.ButtonBase]::ClickEvent))
}
$saved=Open-StyleCaptureReview $analysis $null
Assert-Equal @($saved.candidate_ids|Sort-Object) @('same1','same2','same3') 'Every document location saved'

# Old snapshots can still have different group IDs for the same display path.
# A name equality alone must not be mistaken for a cycle.
$left=New-Candidate 'left' 'Research' 'name' $true 0
$right=New-Candidate 'right' 'Research' 'phone' $true 1
$left.semantic_group_id='old-structural-group'
$right.semantic_group_id='old-body-group'
$analysis=[pscustomobject]@{candidates=@($left,$right)}
$script:ReviewProbe={
    & $ReviewActions.MoveGroup 'old-structural-group' $CandidateById['right']
    Assert-Equal $CandidateOverrides.Count 1 'Same representative name is not a cycle'
    Assert-Equal $CandidateById['left'].group_key $CandidateById['right'].group_key 'Same-name cards joined'
    Assert-Equal $CandidateOverrides['left'].field 'Research > name' 'No extra nesting'
    $Dialog.Close()
}
[void](Open-StyleCaptureReview $analysis $null)
Write-Output 'REVIEW_BEHAVIOR_OK'
