param([string]$Source,[string]$Launcher)
$ErrorActionPreference='Stop'
# Parse production functions only: no window, mouse, document or HWP process.
function Assert($Condition,$Message){if(-not $Condition){throw $Message}}
function Test-WorkspaceWindow($Key){return $false}
function Read-Ast($Path){
    $tokens=$null;$errors=$null
    $result=[System.Management.Automation.Language.Parser]::ParseFile($Path,[ref]$tokens,[ref]$errors)
    Assert ($errors.Count -eq 0) 'PowerShell parse failed'
    return $result
}
$profileAst=Read-Ast $Source
$launcherAst=Read-Ast $Launcher
$authoringAst=Read-Ast (Join-Path (Split-Path -Parent $Launcher) 'document_authoring_ui.ps1')
$wanted=@('Invoke-ProfileReviewSession','Open-ProfileSelectionImport','Open-ProfileDataTable','Open-DocumentFieldManager','Open-DocumentAuthoring','Refresh-HwpDocumentStatus')
foreach($ast in @($profileAst,$launcherAst,$authoringAst)){
    foreach($definition in $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -in $wanted},$true)){
        . ([scriptblock]::Create($definition.Extent.Text))
    }
}
$selectionHook=$launcherAst.Find({param($n)
    $n -is [System.Management.Automation.Language.InvokeMemberExpressionAst] -and
    $n.Expression.Extent.Text -eq '$SelectionProbeTimer' -and $n.Member.Value -eq 'Add_Tick'
},$true)
Assert ($null -ne $selectionHook) 'Selection timer callback not found'
$selectionBody=$selectionHook.Find({param($n) $n -is [System.Management.Automation.Language.ScriptBlockExpressionAst]},$true)
$selectionTick=[scriptblock]::Create($selectionBody.ScriptBlock.Extent.Text.TrimStart('{').TrimEnd('}'))
function New-FakeTimer([bool]$Enabled){
    $timer=[pscustomobject]@{IsEnabled=$Enabled;Starts=0;Stops=0}
    $timer|Add-Member ScriptMethod Stop {$this.IsEnabled=$false;$this.Stops++}
    $timer|Add-Member ScriptMethod Start {$this.IsEnabled=$true;$this.Starts++}
    return $timer
}
function Write-ProfileReviewTrace($Stage){}
function Send-Backend($Command){throw 'Unexpected background backend request'}
function Set-HwpDocumentPanelState($Response){throw 'Unexpected background panel update'}
function Set-HwpDocumentControlsBusy {throw 'Unexpected background UI work'}
function Show-ProfileSelectionImport($OwnerWindow){& $script:ReviewProbe}
function Show-ProfileDataTable($OwnerWindow){& $script:ReviewProbe}
function Show-DocumentAuthoring($OwnerWindow){& $script:ReviewProbe}
function Show-DocumentFieldManager($OwnerWindow){& $script:ReviewProbe}
$script:DocumentStatusTimer=New-FakeTimer $true
$script:SelectionProbeTimer=New-FakeTimer $false
$script:GuiClosing=$false;$script:ProfileReviewActive=$false
$script:BackendRequestInFlight=$false;$LayoutPreview=$true
$script:ReviewProbe={
    Assert $script:ProfileReviewActive 'Review guard missing'
    Assert (-not $script:DocumentStatusTimer.IsEnabled -and -not $script:SelectionProbeTimer.IsEnabled) 'Timers still enabled'
    # Simulate already queued callbacks while the dialog's nested loop runs.
    Refresh-HwpDocumentStatus
    & $selectionTick
    Invoke-ProfileReviewSession $null {throw 'Duplicate review entered'}
    $script:SelectionMouseDown=$true
}
Open-ProfileSelectionImport $null
Assert (-not $script:ProfileReviewActive -and -not $script:SelectionMouseDown) 'Review/gesture state leaked'
Assert ($script:DocumentStatusTimer.IsEnabled -and $script:DocumentStatusTimer.Starts -eq 1) 'Previously running timer not restored'
Assert (-not $script:SelectionProbeTimer.IsEnabled -and $script:SelectionProbeTimer.Starts -eq 0) 'Previously stopped timer started'
Open-ProfileDataTable $null
Assert ($script:DocumentStatusTimer.Starts -eq 2) 'Data manager polling not isolated'
Open-DocumentAuthoring $null
Assert ($script:DocumentStatusTimer.Starts -eq 3) 'Document authoring polling not isolated'
Open-DocumentFieldManager $null
Assert ($script:DocumentStatusTimer.Starts -eq 4) 'New value manager polling not isolated'
$script:ReviewProbe={throw 'synthetic review failure'}
$failed=$false
try{Open-ProfileSelectionImport $null}catch{$failed=$_.Exception.Message -eq 'synthetic review failure'}
Assert $failed 'Review error swallowed'
Assert (-not $script:ProfileReviewActive -and $script:DocumentStatusTimer.IsEnabled) 'Error cleanup failed'
$script:ReviewProbe={$script:GuiClosing=$true}
Open-ProfileDataTable $null
Assert (-not $script:DocumentStatusTimer.IsEnabled) 'Timer restarted during application shutdown'
Assert (-not $script:ProfileReviewActive) 'Shutdown left review locked'
'PROFILE_REVIEW_ISOLATION_OK'
