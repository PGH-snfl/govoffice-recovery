# Parse and instantiate the production two-stage screen without showing it.
$ErrorActionPreference='Stop'
Add-Type -AssemblyName PresentationFramework
$Project=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Tokens=$null;$Errors=$null
$Ast=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $Project 'document_authoring_flow_ui.ps1'),[ref]$Tokens,[ref]$Errors)
if($Errors.Count){throw ($Errors | Out-String)}
$Literal=$Ast.Find({param($Node) $Node -is [System.Management.Automation.Language.StringConstantExpressionAst] -and $Node.Value.StartsWith('<Window ')},$true)
[xml]$Markup=$Literal.Value
$Dialog=[Windows.Markup.XamlReader]::Load([System.Xml.XmlNodeReader]::new($Markup))
try{
 foreach($Name in @('Steps','Step1Card','Step2Card','Step3Card','Step4Card','ChoosePage','WritingPage','ProgressPage','CompletePage','Inputs','ReadOnlyNotice','Disclosure','Start','Open','Back','Next')){
  if(-not $Dialog.FindName($Name)){throw "Missing control: $Name"}
 }
 foreach($Name in @('Facts','References','Consent','Reviewed','ProfileName','ProfilePhone','InputValue','ShowAll','Folder')){
  if($Dialog.FindName($Name)){throw "Unexpected control: $Name"}
 }
 $ns=[Xml.XmlNamespaceManager]::new($Markup.NameTable);$ns.AddNamespace('w','http://schemas.microsoft.com/winfx/2006/xaml/presentation')
 if($Markup.SelectNodes('//w:TextBox',$ns).Count -ne 2){throw 'Exactly two text inputs required'}
 if($Dialog.FindName('Steps').Children.Count -ne 4){throw 'Four navigation steps required'}
 $Buttons=@($Dialog.FindName('CompletePage').Children | Where-Object {$_ -is [Windows.Controls.Button]})
 if($Buttons.Count -ne 1 -or $Buttons[0].Name -ne 'Open'){throw 'Completion must have only output-open action'}
 if($Dialog.FindName('Start').Content -ne '문서 작성 시작'){throw 'Korean encoding mismatch'}
 if($Dialog.FindName('ChoosePage').Visibility -ne 'Visible' -or $Dialog.FindName('WritingPage').Visibility -ne 'Collapsed'){throw 'Initial visibility mismatch'}
 [pscustomobject]@{ok=$true;steps=4;required_inputs=2;visible_test=$false}|ConvertTo-Json -Compress
}finally{$Dialog.Close()}
