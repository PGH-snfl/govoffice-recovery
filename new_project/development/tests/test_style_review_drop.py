"""Exercise real WPF drop routes on a representative title and its body."""

import base64
import os
from pathlib import Path
import shutil
import subprocess
import unittest


@unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"), "Windows WPF required")
class StyleReviewDropTest(unittest.TestCase):
    def test_title_and_body_drop_dispatch_once_with_complete_ids(self):
        launcher = Path(__file__).resolve().parents[2] / "launch_gui.ps1"
        script = r"""
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
$source=Get-Content -LiteralPath '__LAUNCHER__' -Raw -Encoding UTF8
$tokens=$null;$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseInput($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw $errors[0]}
$drop=$ast.Find({param($node)
    $node -is [System.Management.Automation.Language.InvokeMemberExpressionAst] -and
    $node.Expression.Extent.Text -eq '$HeaderBorder' -and $node.Member.Value -eq 'Add_Drop'
},$true)
if($null -eq $drop){throw 'Representative drop handler missing'}
function Write-GuiRuntimeError($context,$failure){throw $failure}
$calls=[System.Collections.Generic.List[object]]::new()
$actions=[pscustomobject]@{
    MoveChild={param($id,$row) $calls.Add(@('child',$id,$row.group_key))}.GetNewClosure()
    MoveGroup={param($id,$row) $calls.Add(@('group',$id,$row.group_key))}.GetNewClosure()
}
$HeaderBorder=[System.Windows.Controls.Border]::new()
$HeaderBorder.AllowDrop=$true
$HeaderBorder.Tag=[pscustomobject]@{
    row=[pscustomobject]@{group_key='target'};actions=$actions
    rest_background='White';guide=[System.Windows.Controls.TextBlock]::new()
}
# Register the exact production handler, then raise a real routed WPF event.
Invoke-Expression $drop.Extent.Text
$GroupCard=[System.Windows.Controls.Border]::new()
$GroupCard.AllowDrop=$true
$GroupCard.Tag=$HeaderBorder.Tag
$GroupCard.Tag | Add-Member -NotePropertyName drop_header -NotePropertyValue $HeaderBorder
$panel=[System.Windows.Controls.StackPanel]::new()
$GroupCard.Child=$panel
[void]$panel.Children.Add($HeaderBorder)
$body=[System.Windows.Controls.DockPanel]::new()
$body.AllowDrop=$true
$check=[System.Windows.Controls.CheckBox]::new()
[void]$body.Children.Add($check)
[void]$panel.Children.Add($body)
foreach($method in @('Add_PreviewDrop','Add_PreviewDragOver')){
    $handler=$ast.Find({param($node)
        $node -is [System.Management.Automation.Language.InvokeMemberExpressionAst] -and
        $node.Expression.Extent.Text -eq '$GroupCard' -and $node.Member.Value -eq $method
    },$true)
    if($null -eq $handler){throw ('Group card handler missing: '+$method)}
    Invoke-Expression $handler.Extent.Text
}
$cases=@(
    @('govoffice-candidate:preview_registered','child','preview_registered'),
    @('govoffice-group:preview-group-business','group','preview-group-business'),
    @('govoffice-candidate:x','child','x'),
    @('govoffice-group:x','group','x')
)
foreach($target in @($HeaderBorder,$body,$check)){
foreach($case in $cases){
    $calls.Clear()
    $data=[System.Windows.DataObject]::new([string],[string]$case[0])
    $constructor=[System.Windows.DragEventArgs].GetConstructors([System.Reflection.BindingFlags]'Instance,NonPublic') | Where-Object {$_.GetParameters().Count -eq 5} | Select-Object -First 1
    $event=$constructor.Invoke(@($data,[System.Windows.DragDropKeyStates]::None,[System.Windows.DragDropEffects]::Move,$target,[System.Windows.Point]::new(1,1)))
    $event.RoutedEvent=[System.Windows.DragDrop]::PreviewDragOverEvent
    $target.RaiseEvent($event)
    if(-not $event.Handled -or $event.Effects -ne [System.Windows.DragDropEffects]::Move){throw 'Body is not accepting move'}
    $event.Handled=$false
    $event.RoutedEvent=[System.Windows.DragDrop]::PreviewDropEvent
    $target.RaiseEvent($event)
    # WPF preserves Handled from the preview route into the bubbling route.
    $event.RoutedEvent=[System.Windows.DragDrop]::DropEvent
    $target.RaiseEvent($event)
    if($calls.Count -ne 1){throw 'Drop did not dispatch exactly once'}
    if($calls[0][0] -cne $case[1] -or $calls[0][1] -cne $case[2] -or $calls[0][2] -cne 'target'){
        throw ('Drop corrupted source ID: expected '+$case[2]+', received '+$calls[0][1])
    }
    if(-not $event.Handled){throw 'Drop was not consumed'}
}
}
Write-Output 'DROP_EVENT_OK'
""".replace("__LAUNCHER__", str(launcher).replace("'", "''"))
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-STA", "-EncodedCommand",
             base64.b64encode(script.encode("utf-16-le")).decode("ascii")],
            capture_output=True, timeout=30,
        )
        self.assertEqual(0, result.returncode, result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
        self.assertIn(b"DROP_EVENT_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
