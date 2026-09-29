$ErrorActionPreference = 'Stop'
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
try{[Console]::InputEncoding = $Utf8NoBom;[Console]::OutputEncoding = $Utf8NoBom}catch{}
$LayoutPreview = $env:GOVOFFICE_LAYOUT_PREVIEW -eq '1'
$InstalledPackage = Test-Path -LiteralPath (Join-Path $PSScriptRoot 'deployment.json')
$SkipElevation = $InstalledPackage -or $env:GOVOFFICE_SKIP_ELEVATION -eq '1'

# HWPFrame.HwpObject가 설치된 한글의 권한 수준과 호출자 권한이 다르면
# COM 생성이 반환되지 않고 대기할 수 있다. 원본을 실제로 검증한 조건과
# 동일하게 런처 자체를 관리자 권한으로 한 번만 재실행한다.
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
$administrator = [Security.Principal.WindowsBuiltInRole]::Administrator
if (-not $LayoutPreview -and -not $SkipElevation -and -not $principal.IsInRole($administrator)) {
    try {
        $argumentList = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
        Start-Process -FilePath 'powershell.exe' -Verb RunAs -ArgumentList $argumentList | Out-Null
    } catch {
        Add-Type -AssemblyName PresentationFramework
        [System.Windows.MessageBox]::Show('한글 자동화에는 관리자 권한이 필요합니다. UAC 승인을 취소하지 말고 다시 실행하세요.', '범정부오피스') | Out-Null
        exit 1
    }
    exit 0
}
Add-Type -AssemblyName PresentationFramework
if(-not ('GovOfficePollGuard' -as [type])){
    Add-Type -Path (Join-Path $PSScriptRoot 'gui_poll_guard.cs') -ReferencedAssemblies @(
        [System.Windows.Window].Assembly.Location,
        [System.Windows.Media.Visual].Assembly.Location,
        [System.Windows.Threading.Dispatcher].Assembly.Location,'System.dll','System.Core.dll','System.Xaml.dll')
}
[GovOfficePollGuard]::Initialize()
$MutexCreated=$false
$MutexName=if($LayoutPreview){"Local\GovOfficeRecoveredApplicationPreview_$PID"}else{'Local\GovOfficeRecoveredApplication'}
$AppMutex=[System.Threading.Mutex]::new($true,$MutexName,[ref]$MutexCreated)
if(-not $MutexCreated){
    [System.Windows.MessageBox]::Show('범정부오피스가 이미 실행 중입니다. 기존 창을 사용하세요.','범정부오피스')|Out-Null
    $AppMutex.Dispose()
    exit 0
}
Add-Type -TypeDefinition @'
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

public static class GovOfficeWindowIdentity
{
    // Give the native GUI its own taskbar group instead of the PowerShell host.
    [DllImport("shell32.dll", CharSet = CharSet.Unicode)]
    private static extern int SetCurrentProcessExplicitAppUserModelID(string appId);

    public static void Initialize()
    {
        Marshal.ThrowExceptionForHR(SetCurrentProcessExplicitAppUserModelID("GovOffice.Desktop"));
    }
}

public static class GovOfficeSelectionMouse
{
    [StructLayout(LayoutKind.Sequential)]
    private struct POINT { public int X; public int Y; }

    [DllImport("user32.dll")]
    private static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    private static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    [DllImport("user32.dll")]
    private static extern short GetAsyncKeyState(int virtualKey);

    [DllImport("user32.dll")]
    private static extern bool GetCursorPos(out POINT point);

    [DllImport("user32.dll")]
    private static extern bool EnumWindows(EnumWindowsProc callback, IntPtr value);

    [DllImport("user32.dll")]
    private static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    private static extern bool ShowWindowAsync(IntPtr hWnd, int command);

    [DllImport("user32.dll")]
    private static extern bool SetForegroundWindow(IntPtr hWnd);

    private delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr value);

    public static int ForegroundProcessId()
    {
        uint processId;
        GetWindowThreadProcessId(GetForegroundWindow(), out processId);
        return unchecked((int)processId);
    }

    public static bool LeftButtonDown()
    {
        return (GetAsyncKeyState(1) & 0x8000) != 0;
    }

    public static int[] CursorPosition()
    {
        POINT point;
        return GetCursorPos(out point) ? new[] { point.X, point.Y } : new[] { 0, 0 };
    }

    public static bool ActivateFirstHwpWindow()
    {
        IntPtr found = IntPtr.Zero;
        EnumWindows(delegate(IntPtr hWnd, IntPtr value)
        {
            if (!IsWindowVisible(hWnd)) return true;
            uint processId;
            GetWindowThreadProcessId(hWnd, out processId);
            try
            {
                if (Process.GetProcessById(unchecked((int)processId)).ProcessName.Equals("Hwp", StringComparison.OrdinalIgnoreCase))
                {
                    found = hWnd;
                    return false;
                }
            }
            catch { }
            return true;
        }, IntPtr.Zero);
        if (found == IntPtr.Zero) return false;
        ShowWindowAsync(found, 9);
        return SetForegroundWindow(found);
    }
}
'@

$ProjectDir = if($env:GOVOFFICE_PROJECT_DIR){[System.IO.Path]::GetFullPath($env:GOVOFFICE_PROJECT_DIR)}else{Split-Path -Parent $MyInvocation.MyCommand.Path}
$WorkspaceDir = Split-Path -Parent $ProjectDir
$RuntimeReportDir = Join-Path $ProjectDir 'development\reports\runtime'
if ($InstalledPackage) { $RuntimeReportDir = Join-Path $env:LOCALAPPDATA 'GovOffice\logs' }
$RuntimeErrorLog = Join-Path $RuntimeReportDir 'gui_runtime_errors.log'
[void][System.IO.Directory]::CreateDirectory($RuntimeReportDir)
function Write-GuiRuntimeError([string]$Context,[object]$Failure) {
    try {
        $Exception=if($Failure -is [System.Management.Automation.ErrorRecord]){$Failure.Exception}elseif($Failure -is [Exception]){$Failure}else{$null}
        $Message=if($null -ne $Exception){$Exception.ToString()}else{[string]$Failure}
        $ScriptStack=if($Failure -is [System.Management.Automation.ErrorRecord]){[string]$Failure.ScriptStackTrace}else{''}
        $Entry="[{0}] {1}`r`n{2}`r`n{3}`r`n" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff'),$Context,$Message,$ScriptStack
        [System.IO.File]::AppendAllText($RuntimeErrorLog,$Entry,$Utf8NoBom)
    } catch {}
}
$Python = Join-Path $ProjectDir 'runtime\python\python.exe'
if (-not (Test-Path -LiteralPath $Python)) {
    $Python = Get-ChildItem -LiteralPath $WorkspaceDir -Directory | Where-Object { $_.Name -like '*1303_*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'python313\python.exe')) } | Select-Object -First 1 | ForEach-Object { Join-Path $_.FullName 'python313\python.exe' }
}
if (-not $Python) { [System.Windows.MessageBox]::Show('번들 Python을 찾지 못했습니다.'); exit 1 }
if ($InstalledPackage -and -not $LayoutPreview) {
    try {
        $CheckOutput = & $Python (Join-Path $ProjectDir 'product\support\deployment_check.py') --register
        if ($LASTEXITCODE -ne 0) {
            $CheckReport = ($CheckOutput -join "`n") | ConvertFrom-Json
            $Problems = @($CheckReport.checks | Where-Object { -not $_.ok } | ForEach-Object { "$($_.name): $($_.detail)" }) -join "`n"
            throw $Problems
        }
    } catch {
        [System.Windows.MessageBox]::Show("실행 준비를 완료하지 못했습니다.`n$($_.Exception.Message)", '범정부오피스 설치 확인') | Out-Null
        exit 1
    }
}

$script:Backend = $null
$script:BackendUnhealthy = $false
$script:BackendRequestInFlight = $false
$script:GuiClosing = $false
$script:BackendStartupTimeoutMilliseconds = 15000

function ConvertTo-AsciiJson([object]$Value) {
    $Json = $Value | ConvertTo-Json -Compress -Depth 10
    return [regex]::Replace($Json, '[^\x00-\x7F]', {
        param($Match)
        $Builder = [System.Text.StringBuilder]::new()
        foreach($Character in $Match.Value.ToCharArray()) {
            [void]$Builder.Append(('\u{0:x4}' -f [int][char]$Character))
        }
        return $Builder.ToString()
    })
}

function Get-BackendRequestTimeout([hashtable]$Command) {
    # DispatcherTimer와 버튼 이벤트는 모두 UI 스레드에서 호출된다. COM이
    # 응답하지 않을 때 창 전체가 무기한 멈추지 않도록 작업 성격별 상한을 둔다.
    $Action=[string]$Command.action
    if($Action -eq 'climate_plan_generate'){return 60000}
    if($Action -in @(
        'hwp_document_status','style_preset_selection_status',
        'style_preset_selection_probe','style_preset_selection_clear',
        'style_preset_list','user_profile_get'
    )){return 5000}
    if($Action -in @(
        'connect','hwp_document_open','hwp_document_close',
        'style_preset_analyze','style_preset_capture','style_preset_apply'
    )){return 30000}
    return 15000
}

function Wait-BackendLineTask {
    param(
        [Parameter(Mandatory=$true)][System.Threading.Tasks.Task[string]]$ReadTask,
        [Parameter(Mandatory=$true)][int]$TimeoutMilliseconds,
        [Parameter(Mandatory=$true)][string]$Context
    )
    if($TimeoutMilliseconds -le 0){throw [System.ArgumentOutOfRangeException]::new('TimeoutMilliseconds')}
    $DispatcherType='System.Windows.Threading.Dispatcher' -as [type]
    $Dispatcher=if($null -ne $DispatcherType){$DispatcherType::FromThread([System.Threading.Thread]::CurrentThread)}else{$null}
    if($null -ne $Dispatcher -and -not $ReadTask.IsCompleted){
        # Keep WPF painting/input alive while waiting. Send-Backend serializes
        # requests and both polling timers skip ticks during this nested loop.
        $WaitFrame=[System.Windows.Threading.DispatcherFrame]::new()
        $WaitClock=[System.Diagnostics.Stopwatch]::StartNew()
        $WaitTimer=[System.Windows.Threading.DispatcherTimer]::new()
        $WaitTimer.Interval=[TimeSpan]::FromMilliseconds(20)
        $WaitTimer.Add_Tick({
            if($ReadTask.IsCompleted -or $WaitClock.ElapsedMilliseconds -ge $TimeoutMilliseconds){$WaitFrame.Continue=$false}
        }.GetNewClosure())
        try{$WaitTimer.Start();[System.Windows.Threading.Dispatcher]::PushFrame($WaitFrame)}
        finally{$WaitTimer.Stop();$WaitClock.Stop()}
        $Completed=$ReadTask.IsCompleted
    }else{$Completed=$ReadTask.Wait($TimeoutMilliseconds)}
    if(-not $Completed){
        throw [System.TimeoutException]::new("$Context 응답 대기 시간이 종료되었습니다.")
    }
    return $ReadTask.GetAwaiter().GetResult()
}

function Read-BackendLine {
    param(
        [Parameter(Mandatory=$true)][System.Diagnostics.Process]$Process,
        [Parameter(Mandatory=$true)][int]$TimeoutMilliseconds,
        [Parameter(Mandatory=$true)][string]$Context
    )
    if($Process.HasExited){throw [System.IO.EndOfStreamException]::new('기능 백엔드가 종료되었습니다.')}
    $ReadTask=$Process.StandardOutput.ReadLineAsync()
    return Wait-BackendLineTask -ReadTask $ReadTask -TimeoutMilliseconds $TimeoutMilliseconds -Context $Context
}

function Stop-BackendProcess {
    param(
        [System.Diagnostics.Process]$Process=$script:Backend,
        [bool]$RequestShutdown=$false
    )
    if($null -eq $Process){$script:Backend=$null;$script:BackendUnhealthy=$false;return $true}
    try{$Exited=$Process.HasExited}catch{$Exited=$true}
    if(-not $Exited -and $RequestShutdown){
        try{
            $Process.StandardInput.WriteLine((ConvertTo-AsciiJson @{action='shutdown'}))
            $Process.StandardInput.Flush()
        }catch{}
        try{$Exited=$Process.WaitForExit(5000)}catch{$Exited=$false}
    }
    if(-not $Exited){
        # 요청이 COM 내부에서 멈췄다면 stdin EOF로 정상 finally 정리를 먼저
        # 유도하고, 짧은 유예 후에도 남은 Python 백엔드만 종료한다.
        try{$Process.StandardInput.Close()}catch{}
        try{$Exited=$Process.WaitForExit(750)}catch{$Exited=$false}
    }
    if(-not $Exited){
        try{$Process.Kill();$Exited=$Process.WaitForExit(2000)}catch{$Exited=$false}
    }
    if(-not $Exited){
        $script:BackendUnhealthy=$true
        return $false
    }
    try{$Process.StandardInput.Dispose()}catch{}
    try{$Process.StandardOutput.Dispose()}catch{}
    try{$Process.StandardError.Dispose()}catch{}
    try{$Process.Dispose()}catch{}
    if([object]::ReferenceEquals($script:Backend,$Process)){$script:Backend=$null}
    $script:BackendUnhealthy=$false
    return $true
}

function Start-BackendProcess {
    if($LayoutPreview){return $null}
    if($script:BackendUnhealthy){
        throw '이전 기능 백엔드를 종료하지 못해 안전하게 다시 시작할 수 없습니다. 프로그램을 종료한 뒤 다시 실행하세요.'
    }
    if($null -ne $script:Backend){
        try{if(-not $script:Backend.HasExited){return $script:Backend}}catch{}
        [void](Stop-BackendProcess -Process $script:Backend)
    }
    $Info=[System.Diagnostics.ProcessStartInfo]::new()
    $Info.FileName=$Python
    $Info.Arguments='"' + (Join-Path $ProjectDir 'gui_backend.py') + '"'
    $Info.WorkingDirectory=$WorkspaceDir
    $Info.UseShellExecute=$false
    $Info.CreateNoWindow=$true
    $Info.RedirectStandardInput=$true
    $Info.RedirectStandardOutput=$true
    $Info.RedirectStandardError=$true
    $Info.EnvironmentVariables['PYTHONUTF8'] = '1'
    $Info.EnvironmentVariables['PYTHONIOENCODING'] = 'utf-8'
    $script:Backend=[System.Diagnostics.Process]::Start($Info)
    try{
        $ReadyLine=Read-BackendLine -Process $script:Backend -TimeoutMilliseconds $script:BackendStartupTimeoutMilliseconds -Context '기능 백엔드 시작'
        if(-not $ReadyLine){throw '기능 백엔드가 준비 응답 없이 종료되었습니다.'}
        $Ready=$ReadyLine | ConvertFrom-Json
        if(-not $Ready.ok){throw [string]$Ready.message}
        return $script:Backend
    }catch{
        [void](Stop-BackendProcess -Process $script:Backend)
        throw
    }
}

if(-not $LayoutPreview){
    try{[void](Start-BackendProcess)}catch{
        [System.Windows.MessageBox]::Show($_.Exception.Message,'범정부오피스 시작 오류')|Out-Null
        try{$AppMutex.ReleaseMutex()}catch{}
        $AppMutex.Dispose()
        exit 1
    }
}

$script:PreviewHwpDocument = [ordered]@{
    ok=$true
    message='미리보기 문서가 연결되었습니다.'
    hwp_running=$true
    document_open=$true
    managed=$true
    title='범정부오피스_미리보기.hwp'
    path='C:\문서\범정부오피스_미리보기.hwp'
    editable=$true
    modified=$false
    visible=$true
    minimized=$false
}

function Send-Backend([hashtable]$Command) {
    if($script:BackendRequestInFlight){throw '한글에서 이전 작업을 처리하고 있습니다. 완료 후 다시 누르세요.'}
    if ($LayoutPreview) {
        if($Command.action -like 'favorite_*'){return Invoke-FavoritePreview $Command}
        if($Command.action -eq 'hwp_document_status'){
            return [pscustomobject]$script:PreviewHwpDocument
        }
        if($Command.action -eq 'hwp_document_open'){
            $PreviewPath=if($Command.path){[System.IO.Path]::GetFullPath([string]$Command.path)}else{'C:\문서\범정부오피스_미리보기.hwp'}
            $script:PreviewHwpDocument.ok=$true;$script:PreviewHwpDocument.message='미리보기 문서를 열었습니다.';$script:PreviewHwpDocument.hwp_running=$true;$script:PreviewHwpDocument.document_open=$true;$script:PreviewHwpDocument.managed=$true;$script:PreviewHwpDocument.title=[System.IO.Path]::GetFileName($PreviewPath);$script:PreviewHwpDocument.path=$PreviewPath;$script:PreviewHwpDocument.editable=$true;$script:PreviewHwpDocument.modified=$false;$script:PreviewHwpDocument.visible=$true;$script:PreviewHwpDocument.minimized=$false
            return [pscustomobject]$script:PreviewHwpDocument
        }
        if($Command.action -eq 'hwp_document_show'){
            $script:PreviewHwpDocument.ok=$true;$script:PreviewHwpDocument.message='문서 창을 화면에 표시했습니다.';$script:PreviewHwpDocument.visible=$true;$script:PreviewHwpDocument.minimized=$false
            return [pscustomobject]$script:PreviewHwpDocument
        }
        if($Command.action -eq 'hwp_document_minimize'){
            $script:PreviewHwpDocument.ok=$true;$script:PreviewHwpDocument.message='문서 창을 최소화했습니다.';$script:PreviewHwpDocument.visible=$false;$script:PreviewHwpDocument.minimized=$true
            return [pscustomobject]$script:PreviewHwpDocument
        }
        if($Command.action -eq 'hwp_document_close'){
            $script:PreviewHwpDocument.ok=$true;$script:PreviewHwpDocument.message='문서를 닫았습니다.';$script:PreviewHwpDocument.document_open=$false;$script:PreviewHwpDocument.managed=$false;$script:PreviewHwpDocument.title='';$script:PreviewHwpDocument.path='';$script:PreviewHwpDocument.editable=$false;$script:PreviewHwpDocument.modified=$false;$script:PreviewHwpDocument.visible=$false;$script:PreviewHwpDocument.minimized=$false
            return [pscustomobject]$script:PreviewHwpDocument
        }
        if($Command.action -eq 'user_profile_get'){
            return [pscustomobject]@{
                ok=$true;message='사용자 정보 미리보기';
                values=[pscustomobject]@{이름='홍길동';전화번호='010-1234-5678';이메일='hong@example.com';문서항목=@([pscustomobject]@{필드명='과제명';입력값='범정부오피스'},[pscustomobject]@{필드명='과제명';입력값='문서 자동화'},[pscustomobject]@{필드명='책임자';입력값='홍길동'})};
                field_groups=@([pscustomobject]@{id='profile_field_name';name='이름';aliases=@('성명','성함');values=@('홍길동');default='홍길동'},[pscustomobject]@{id='profile_field_phone';name='전화번호';aliases=@('전화','연락처');values=@('010-1234-5678');default='010-1234-5678'},[pscustomobject]@{id='profile_field_email';name='이메일';aliases=@('전자우편','E-mail');values=@('hong@example.com');default='hong@example.com'},[pscustomobject]@{id='profile_field_project';name='과제명';aliases=@('사업명','프로젝트명');values=@('범정부오피스','문서 자동화');default='범정부오피스'},[pscustomobject]@{id='profile_field_owner';name='책임자';aliases=@('연구책임자','총괄책임자');values=@('홍길동');default='홍길동'});
                value_links=@([pscustomobject]@{value='홍길동';fields=@('이름','책임자')})
            }
        }
        if($Command.action -in @('user_profile_save','user_profile_basic_save','user_profile_entry_add','user_profile_entry_delete','user_profile_aliases_set','user_profile_default_set','user_profile_field_merge','user_profile_field_delete')){return [pscustomobject]@{ok=$true;message='사용자 정보 미리보기 저장 완료'}}
        if($Command.action -eq 'style_preset_selection_status'){return [pscustomobject]@{ok=$true;message='선택 영역이 확인되었습니다. 바로 프리셋으로 저장할 수 있습니다.';hwp_running=$true;managed_document_ready=$true;managed_document_active=$true;selection_ready=$true;selection_source='preview'}}
        if($Command.action -eq 'style_preset_list'){return [pscustomobject]@{ok=$true;message='저장된 서식 프리셋 0개';presets=@()}}
        if($Command.action -eq 'style_preset_analyze'){
            $registered=[pscustomobject]@{candidate_id='preview_registered';field='사업 정보 > 사업명';field_path='사업 정보 > 사업명';label='사업명';value='범정부오피스';table=0;row=0;col=0;value_row=0;value_col=1;direction='right';confidence=.95;registered=$true;recommended=$true;context_title='사업 정보';semantic_group_id='preview-group-business';semantic_representative_field='사업 정보';semantic_child_id='preview-child-business-name';semantic_child_field='사업명'}
            $unregistered=[pscustomobject]@{candidate_id='preview_new';field='연구자 정보 > 성명';field_path='연구자 정보 > 성명';label='성명';value='김철수';table=0;row=1;col=0;value_row=1;value_col=1;direction='right';confidence=.89;registered=$false;recommended=$true;context_title='연구자 정보';semantic_group_id='preview-group-researcher';semantic_representative_field='연구자 정보';semantic_child_id='preview-child-researcher-name';semantic_child_field='성명'}
            $third=[pscustomobject]@{candidate_id='preview_third';field='과제 정보 > 과제명';field_path='과제 정보 > 과제명';label='과제명';value='차세대 문서 자동화';table=0;row=2;col=0;value_row=2;value_col=1;direction='right';confidence=.86;registered=$false;recommended=$true;context_title='과제 정보';semantic_group_id='preview-group-project';semantic_representative_field='과제 정보';semantic_child_id='preview-child-project-name';semantic_child_field='과제명'}
            return [pscustomobject]@{ok=$true;message='선택 영역 분석 미리보기';draft_id='preview_draft';candidates=@($registered,$unregistered,$third);registered_candidates=@($registered);unregistered_candidates=@($unregistered,$third)}
        }
        if($Command.action -eq 'style_preset_capture'){return [pscustomobject]@{ok=$true;message='서식 프리셋 미리보기 저장 완료'}}
        if($Command.action -eq 'style_preset_manual_selection_begin'){return [pscustomobject]@{ok=$true;message='한글에서 필드로 지정할 실제 값만 드래그하세요.';selection_token='preview_manual_selection';captured=$false}}
        if($Command.action -eq 'style_preset_manual_selection_cancel'){return [pscustomobject]@{ok=$true;message='직접 값 선택을 취소했습니다.';captured=$false}}
        if($Command.action -eq 'style_preset_manual_candidate'){$manual=[pscustomobject]@{candidate_id='preview_manual';field=[string]$Command.field_name;label=[string]$Command.field_name;value='직접 선택한 값';table=-1;row=2;col=0;value_row=2;value_col=0;direction='inline';confidence=1;registered=$true;recommended=$true;context_title=$null;manual=$true};return [pscustomobject]@{ok=$true;message='직접 선택한 값의 위치를 추가했습니다.';candidates=@($manual);conflicting_candidate_ids=@();multiple_locations=$false}}
        if($Command.action -eq 'style_preset_selection_probe'){return [pscustomobject]@{ok=$true;message='선택 영역 감지 완료';captured=$true;managed_document_ready=$true}}
        if($Command.action -eq 'style_preset_selection_clear'){return [pscustomobject]@{ok=$true;message='이전 선택 영역을 지웠습니다.';captured=$false}}
        return [pscustomobject]@{ok=$false;message='레이아웃 미리보기에서는 문서 기능을 실행하지 않습니다.'}
    }
    $Action=[string]$Command.action
    if($script:BackendUnhealthy){
        throw '이전 기능 백엔드를 종료하지 못해 통신을 재개할 수 없습니다. 프로그램을 종료한 뒤 다시 실행하세요.'
    }
    if($null -eq $script:Backend -or $script:Backend.HasExited){
        # 정상 종료 등 비오염 연결 해제 뒤에는 타이머가 자동으로 새 백엔드를
        # 만들지 않고 사용자의 '다시 연결' 요청에서만 명시적으로 재시작한다.
        if($Action -ne 'connect'){
            throw '기능 백엔드 연결이 끊어졌습니다. 상단의 다시 연결을 눌러 백엔드를 안전하게 다시 시작하세요.'
        }
        $script:BackendRequestInFlight=$true
        try{[void](Start-BackendProcess)}catch{$script:BackendRequestInFlight=$false;throw}
    }
    $TimeoutMilliseconds=Get-BackendRequestTimeout $Command
    $script:BackendRequestInFlight=$true
    try{
        $script:Backend.StandardInput.WriteLine((ConvertTo-AsciiJson $Command))
        $script:Backend.StandardInput.Flush()
        $Line=Read-BackendLine -Process $script:Backend -TimeoutMilliseconds $TimeoutMilliseconds -Context "기능 '$Action'"
        if(-not $Line){throw [System.IO.EndOfStreamException]::new('기능 백엔드가 응답하지 않습니다.')}
        return $Line | ConvertFrom-Json
    }catch{
        $Failure=$_
        $WasTimeout=$Failure.Exception -is [System.TimeoutException]
        $Cleaned=Stop-BackendProcess -Process $script:Backend
        if($WasTimeout){
            # COM 호출이 어디까지 실행됐는지 알 수 없는 상태에서는 새 백엔드가
            # 같은 Hwp.exe를 다시 잡거나 별도 인스턴스를 만드는 것을 허용하지 않는다.
            # 프로그램 전체를 다시 시작하기 전까지 이 세션은 오염 상태로 둔다.
            $script:BackendUnhealthy=$true
            $Seconds=[math]::Round($TimeoutMilliseconds/1000,1)
            $Recovery=if($Cleaned){'백엔드는 정리했지만 한글 작업 상태를 확인할 수 없습니다. 열린 한글 문서를 확인한 뒤 범정부오피스를 완전히 종료하고 다시 실행하세요.'}else{'백엔드를 종료하지 못했습니다. 범정부오피스를 완전히 종료한 뒤 다시 실행하세요.'}
            throw [System.TimeoutException]::new("기능 '$Action'이(가) ${Seconds}초 안에 응답하지 않았습니다. $Recovery",$Failure.Exception)
        }
        $Recovery=if($Cleaned){' 상단의 다시 연결을 눌러 재시작하세요.'}else{' 프로그램을 종료한 뒤 다시 실행하세요.'}
        throw [System.InvalidOperationException]::new("기능 백엔드 통신이 끊어졌습니다.$Recovery",$Failure.Exception)
    }finally{$script:BackendRequestInFlight=$false}
}

if(-not $LayoutPreview){
    try{[GovOfficeWindowIdentity]::Initialize()}catch{Write-GuiRuntimeError 'window app identity' $_}
}
[xml]$Xaml = @'
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" Title="범정부오피스" Width="300" Height="824" Left="0" Top="0" Topmost="False" ResizeMode="CanMinimize" WindowStyle="SingleBorderWindow" Background="White" ShowInTaskbar="True" UseLayoutRounding="True" SnapsToDevicePixels="True">
  <Viewbox Name="MainViewbox" Stretch="Uniform" StretchDirection="DownOnly">
    <Canvas Name="Root" Width="300" Height="824" Background="White">
      <Canvas Name="TopBar" Width="300" Height="50" Canvas.Left="0" Canvas.Top="0" Background="White"/>
      <Border Name="HwpDocumentPanel" Width="300" Height="104" Canvas.Left="0" Canvas.Top="50" Background="#FAFAFA" BorderBrush="#DBDBDB" BorderThickness="0,1,0,1">
        <Grid Margin="8,4,8,4">
          <Grid.RowDefinitions>
            <RowDefinition Height="18"/><RowDefinition Height="21"/><RowDefinition Height="21"/><RowDefinition Height="32"/>
          </Grid.RowDefinitions>
          <Grid>
            <Grid.ColumnDefinitions><ColumnDefinition Width="*"/><ColumnDefinition Width="Auto"/></Grid.ColumnDefinitions>
            <TextBlock Text="연결된 한글 문서" FontFamily="맑은 고딕" FontSize="9" FontWeight="SemiBold" Foreground="#737373" VerticalAlignment="Center"/>
            <Border Grid.Column="1" Background="#F3F0F8" BorderBrush="#D9D2E7" BorderThickness="1" CornerRadius="8" Padding="6,1"><TextBlock Name="HwpDocumentState" Text="연결 확인 중" FontFamily="맑은 고딕" FontSize="8" Foreground="#55447A"/></Border>
          </Grid>
          <TextBlock Name="HwpDocumentTitle" Grid.Row="1" Text="열린 문서 없음" FontFamily="맑은 고딕" FontSize="11" FontWeight="SemiBold" Foreground="#262626" TextTrimming="CharacterEllipsis" VerticalAlignment="Center"/>
          <TextBlock Name="HwpDocumentPath" Grid.Row="2" Text="한글 문서 상태를 확인하는 중입니다." FontFamily="맑은 고딕" FontSize="8" Foreground="#737373" TextTrimming="CharacterEllipsis" VerticalAlignment="Center"/>
          <StackPanel Grid.Row="3" Orientation="Horizontal" HorizontalAlignment="Center" VerticalAlignment="Bottom">
            <Button Name="HwpDocumentOpen" Content="문서 열기" Width="65" Height="26" Margin="0,2,3,0" FontFamily="맑은 고딕" FontSize="8" Background="#E7E7E7" Foreground="#202020" BorderBrush="#BEBEBE"/>
            <Button Name="HwpDocumentShow" Content="화면에 표시/복원" Width="91" Height="26" Margin="0,2,3,0" FontFamily="맑은 고딕" FontSize="8" Background="White" Foreground="#202020" BorderBrush="#BEBEBE"/>
            <Button Name="HwpDocumentMinimize" Content="최소화" Width="55" Height="26" Margin="0,2,3,0" FontFamily="맑은 고딕" FontSize="8" Background="White" Foreground="#202020" BorderBrush="#BEBEBE"/>
            <Button Name="HwpDocumentClose" Content="닫기" Width="45" Height="26" Margin="0,2,0,0" FontFamily="맑은 고딕" FontSize="8" Background="White" Foreground="#202020" BorderBrush="#BEBEBE"/>
          </StackPanel>
        </Grid>
      </Border>
      <Border Width="300" Height="30" Canvas.Left="0" Canvas.Top="154" Background="White"><TextBlock Name="Status" Text="범정부오피스" HorizontalAlignment="Center" VerticalAlignment="Center" FontFamily="맑은 고딕" FontSize="9" Foreground="#555555" TextTrimming="CharacterEllipsis"/></Border>
      <Canvas Name="Content" Width="300" Height="400" Canvas.Left="0" Canvas.Top="184" Background="White" ClipToBounds="True"/>
      <Canvas Name="Navigation" Width="300" Height="240" Canvas.Left="0" Canvas.Top="584" Background="White"/>
    </Canvas>
  </Viewbox>
</Window>
'@
# Application must exist before XAML creates the main Window, otherwise that
# window is absent from Application.Windows. Closing a child then initiates
# shutdown and the next ShowDialog can leave the main window disabled.
$script:WpfApplication=[System.Windows.Application]::Current
if($null -eq $script:WpfApplication){$script:WpfApplication=[System.Windows.Application]::new()}
$Window = [Windows.Markup.XamlReader]::Load([System.Xml.XmlNodeReader]::new($Xaml))
$script:WpfApplication.MainWindow=$Window
$script:WpfApplication.ShutdownMode=[System.Windows.ShutdownMode]::OnMainWindowClose
if($LayoutPreview){$Window.WindowStyle='SingleBorderWindow';$Window.Topmost=$false;$Window.Title='범정부오피스 레이아웃 미리보기'}
$TopBar = $Window.FindName('TopBar'); $Content = $Window.FindName('Content'); $Navigation = $Window.FindName('Navigation'); $Status = $Window.FindName('Status')
$script:MainStatus=$Status
$script:WpfApplication.Add_DispatcherUnhandledException({
    $eventArgs=$_
    try{
        $record=[System.Management.Automation.ErrorRecord]::new($eventArgs.Exception,'WpfDispatcherUnhandledException',[System.Management.Automation.ErrorCategory]::NotSpecified,$null)
        Write-GuiRuntimeError 'WPF dispatcher event' $record
        if($eventArgs.Exception.Message -like '*GOVOFFICE_DISPATCHER_EXCEPTION_SELFTEST*'){$script:PreviewDispatcherExceptionCaught=$true}
        if($null -ne $script:MainStatus){$script:MainStatus.Text="오류를 복구했습니다: $($eventArgs.Exception.Message)"}
    }finally{$eventArgs.Handled=$true}
})
$HwpDocumentPanel=$Window.FindName('HwpDocumentPanel');$HwpDocumentState=$Window.FindName('HwpDocumentState');$HwpDocumentTitle=$Window.FindName('HwpDocumentTitle');$HwpDocumentPath=$Window.FindName('HwpDocumentPath')
$HwpDocumentOpen=$Window.FindName('HwpDocumentOpen');$HwpDocumentShow=$Window.FindName('HwpDocumentShow');$HwpDocumentMinimize=$Window.FindName('HwpDocumentMinimize');$HwpDocumentClose=$Window.FindName('HwpDocumentClose')
$Assets = Join-Path $ProjectDir 'assets\icons'
$Layout = Get-Content -LiteralPath (Join-Path $ProjectDir 'config\original_layout.json') -Raw -Encoding UTF8 | ConvertFrom-Json
# Native institution features come from their library manifest, not a stale
# snapshot of the recovered executable's layout.
$SeoultechManifestPath=Join-Path $ProjectDir 'src\govoffice\institutions\packages\seoultech\manifest.json'
if(Test-Path -LiteralPath $SeoultechManifestPath){
    $SeoultechManifest=Get-Content -LiteralPath $SeoultechManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $Layout.institutions.seoultech | Add-Member -MemberType NoteProperty -Name custom_features -Value @($SeoultechManifest.custom_features) -Force
}
$TabMap = @{}; foreach ($Tab in $Layout.tabs) { $TabMap[$Tab.id] = $Tab }
$CurrentTab = '사용'; $NavButtons = @{}
. (Join-Path $ProjectDir 'favorites_ui.ps1')
. (Join-Path $ProjectDir 'workspace_windows.ps1')
. (Join-Path $ProjectDir 'profile_table_ui.ps1')
. (Join-Path $ProjectDir 'document_authoring_ui.ps1')
. (Join-Path $ProjectDir 'document_authoring_flow_ui.ps1')

function Get-FitScale([double]$Width, [double]$Height, [double]$Margin=0) {
    $Area = [System.Windows.SystemParameters]::WorkArea
    $AvailableWidth = [math]::Max(1, $Area.Width - (2 * $Margin))
    $AvailableHeight = [math]::Max(1, $Area.Height - (2 * $Margin))
    return [math]::Min(1, [math]::Min($AvailableWidth / $Width, $AvailableHeight / $Height))
}

$MainArea = [System.Windows.SystemParameters]::WorkArea
$MainScale = Get-FitScale 300 824
$Window.Width = 300 * $MainScale
$Window.Height = 824 * $MainScale
$Window.Left = $MainArea.Left
$Window.Top = $MainArea.Top

function Resolve-Icon([string]$Relative) {
    if ([string]::IsNullOrWhiteSpace($Relative)) { return $null }
    $Clean = $Relative -replace '^아이콘[/\\]+','' -replace '[/\\]+','\'
    return Join-Path $Assets $Clean
}
function New-ImageButton($Parent, [double]$X, [double]$Y, [double]$Width, [double]$Height, [string]$Icon, [scriptblock]$Click, [string]$Tip='', [bool]$Enabled=$true) {
    $Button = [System.Windows.Controls.Button]::new(); $Button.Width=$Width; $Button.Height=$Height; $Button.Padding=0; $Button.BorderThickness=0; $Button.Background=[System.Windows.Media.Brushes]::White; $Button.ToolTip=$Tip
    $Path = Resolve-Icon $Icon
    if ($Path -and (Test-Path -LiteralPath $Path)) { $Image=[System.Windows.Controls.Image]::new(); $Image.Source=[System.Windows.Media.Imaging.BitmapImage]::new([Uri]$Path); $Image.Stretch='Fill'; $Button.Content=$Image } else { $Button.Content=$Tip; $Button.FontSize=8;Set-OriginalFlatButton $Button $false }
    if (-not $Enabled) { $Button.Opacity=.35 }
    $Button.Add_Click($Click); [System.Windows.Controls.Canvas]::SetLeft($Button,$X); [System.Windows.Controls.Canvas]::SetTop($Button,$Y); [void]$Parent.Children.Add($Button); return $Button
}

# 복구 과정에서 새로 만든 화면은 낮은 채도의 보라색 단색 포인트를
# 공유한다. 원본 이미지 버튼과 성공·경고 상태색은 그대로 둔다.
function New-PurpleAccentBrush {
    return [System.Windows.Media.BrushConverter]::new().ConvertFromString('#66558F')
}
function Get-PurpleButtonTemplate {
    if($null -eq $script:PurpleButtonTemplate){
        $script:PurpleButtonTemplate=[Windows.Markup.XamlReader]::Parse(@'
<ControlTemplate xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" TargetType="{x:Type Button}">
  <Border x:Name="Chrome" CornerRadius="8" Background="{TemplateBinding Background}" BorderBrush="{TemplateBinding BorderBrush}" BorderThickness="{TemplateBinding BorderThickness}" Padding="{TemplateBinding Padding}">
    <ContentPresenter HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}" VerticalAlignment="{TemplateBinding VerticalContentAlignment}" RecognizesAccessKey="True"/>
  </Border>
  <ControlTemplate.Triggers>
    <Trigger Property="IsMouseOver" Value="True"><Setter TargetName="Chrome" Property="Opacity" Value="0.88"/></Trigger>
    <Trigger Property="IsEnabled" Value="False"><Setter TargetName="Chrome" Property="Opacity" Value="0.42"/></Trigger>
  </ControlTemplate.Triggers>
</ControlTemplate>
'@)
    }
    return $script:PurpleButtonTemplate
}
function Set-OriginalFlatButton($Button,[bool]$Emphasis=$false) {
    if($null -eq $Button){return}
    $Button.FontFamily='맑은 고딕';$Button.FontWeight='SemiBold'
    $Button.Foreground=if($Emphasis){'White'}else{'#262626'};$Button.BorderBrush=if($Emphasis){'#66558F'}else{'#DBDBDB'};$Button.BorderThickness=1
    $Button.Background=if($Emphasis){New-PurpleAccentBrush}else{'White'}
    $Button.Padding='8,2';$Button.HorizontalContentAlignment='Center';$Button.VerticalContentAlignment='Center'
    $Button.Template=Get-PurpleButtonTemplate
}
function Set-OriginalSectionHeader($Header,$HeaderText) {
    if($null -ne $Header){$Header.Background='White';$Header.BorderBrush='#66558F';$Header.BorderThickness='0,0,0,2'}
    if($null -ne $HeaderText){$HeaderText.Foreground='#262626';$HeaderText.FontFamily='맑은 고딕'}
}
Set-OriginalFlatButton $HwpDocumentOpen $true;Set-OriginalFlatButton $HwpDocumentShow $false;Set-OriginalFlatButton $HwpDocumentMinimize $false;Set-OriginalFlatButton $HwpDocumentClose $false

$script:HwpDocumentBusy=$false
$script:LastHwpDocumentStatus=$null

function Get-HwpDocumentValue($Response,[string[]]$Names,$Fallback=$null) {
    if($null -eq $Response){return $Fallback}
    $Containers=@($Response)
    $DocumentProperty=$Response.PSObject.Properties['document']
    if($null -ne $DocumentProperty -and $null -ne $DocumentProperty.Value){$Containers+=@($DocumentProperty.Value)}
    foreach($Container in $Containers){
        foreach($Name in $Names){
            $Property=$Container.PSObject.Properties[$Name]
            if($null -ne $Property -and $null -ne $Property.Value){return $Property.Value}
        }
    }
    return $Fallback
}

function Set-HwpDocumentPanelState($Response) {
    $script:LastHwpDocumentStatus=$Response
    $Ok=[bool](Get-HwpDocumentValue $Response @('ok') $false)
    $Message=[string](Get-HwpDocumentValue $Response @('message','status') '')
    $Running=[bool](Get-HwpDocumentValue $Response @('hwp_running','running','connected') $false)
    $Title=[string](Get-HwpDocumentValue $Response @('title','document_title','file_title','filename','name') '')
    $Path=[string](Get-HwpDocumentValue $Response @('path','document_path','full_path','file_path') '')
    $OpenValue=Get-HwpDocumentValue $Response @('document_open','has_document','open') $null
    $DocumentOpen=if($null -ne $OpenValue){[bool]$OpenValue}else{[bool]($Title -or $Path)}
    $ManagedValue=Get-HwpDocumentValue $Response @('managed','program_managed') $null
    $Managed=if($null -ne $ManagedValue){[bool]$ManagedValue}else{$DocumentOpen}
    $EditableValue=Get-HwpDocumentValue $Response @('editable','can_edit','writable') $null
    $Editable=if($null -ne $EditableValue){[bool]$EditableValue}else{$false}
    $EditModeLabel=[string](Get-HwpDocumentValue $Response @('edit_mode_label') '')
    $ModifiedValue=Get-HwpDocumentValue $Response @('modified','dirty','is_modified') $null
    $Modified=$null -ne $ModifiedValue -and [bool]$ModifiedValue
    $OutputDocumentCount=[int](Get-HwpDocumentValue $Response @('output_document_count') 0)
    $Visible=[bool](Get-HwpDocumentValue $Response @('visible','is_visible') $false)
    $Minimized=[bool](Get-HwpDocumentValue $Response @('minimized','is_minimized') $false)
    $BackendAvailable=$LayoutPreview -or ($null -ne $Backend -and -not $Backend.HasExited)

    if(-not $Ok){
        $HwpDocumentState.Text='연결 확인 필요'
        $HwpDocumentTitle.Text='한글 문서 상태를 확인할 수 없습니다.'
        $HwpDocumentPath.Text=if($Message){$Message}else{'문서 열기로 다시 시도하세요.'}
    }elseif($DocumentOpen -and $Managed){
        if(-not $Title -and $Path){$Title=[System.IO.Path]::GetFileName($Path)}
        if(-not $Title){$Title='제목 없는 한글 문서'}
        $EditLabel=if($EditModeLabel){$EditModeLabel}elseif($null -eq $EditableValue){'편집 상태 확인 불가'}elseif($Editable){'편집 가능'}else{'읽기 전용'}
        $ModifiedLabel=if($Modified){' · 수정됨'}elseif($null -eq $ModifiedValue){' · 수정 상태 확인 불가'}else{''}
        $OutputLabel=if($OutputDocumentCount -gt 0){" · 출력 문서 $($OutputDocumentCount)개 별도 열림"}else{''}
        $HwpDocumentTitle.Text="$Title  ·  $EditLabel$ModifiedLabel$OutputLabel"
        $HwpDocumentPath.Text=if($Path){$Path}elseif($Message){$Message}else{'문서 경로가 없는 상태입니다.'}
        if($Minimized){$HwpDocumentState.Text='최소화됨'}elseif($Visible){$HwpDocumentState.Text='화면에 표시 중'}else{$HwpDocumentState.Text='문서 연결됨'}
    }elseif($DocumentOpen){
        if(-not $Title -and $Path){$Title=[System.IO.Path]::GetFileName($Path)}
        if(-not $Title){$Title='외부 한글 문서'}
        $HwpDocumentState.Text='외부 한글 연결됨'
        $HwpDocumentTitle.Text="$Title  ·  프로그램에서 불러온 문서 아님"
        $HwpDocumentPath.Text=if($Path){$Path}else{'문서 열기로 파일을 불러오면 이 화면에서 제어할 수 있습니다.'}
    }elseif($Running){
        $HwpDocumentState.Text='한글 실행 중'
        $HwpDocumentTitle.Text='열린 한글 문서 없음'
        $HwpDocumentPath.Text=if($Message){$Message}else{'문서 열기를 눌러 파일을 선택하세요.'}
    }else{
        $HwpDocumentState.Text='연결 대기'
        $HwpDocumentTitle.Text='한글 문서가 연결되지 않았습니다.'
        $HwpDocumentPath.Text=if($Message){$Message}else{'문서 열기로 한글을 시작하세요.'}
    }
    $HwpDocumentPath.ToolTip=$HwpDocumentPath.Text
    $HwpDocumentOpen.IsEnabled=[bool]($BackendAvailable -and -not $script:HwpDocumentBusy)
    $HwpDocumentShow.IsEnabled=[bool]($BackendAvailable -and $DocumentOpen -and $Managed -and -not $script:HwpDocumentBusy)
    $HwpDocumentMinimize.IsEnabled=[bool]($BackendAvailable -and $DocumentOpen -and $Managed -and -not $Minimized -and -not $script:HwpDocumentBusy)
    $HwpDocumentClose.IsEnabled=[bool]($BackendAvailable -and $DocumentOpen -and $Managed -and -not $script:HwpDocumentBusy)
    $HwpDocumentShow.ToolTip=if($DocumentOpen -and -not $Managed){'문서 열기로 불러온 문서만 표시하거나 복원할 수 있습니다.'}else{'한글 문서 창 표시 또는 복원'}
    $HwpDocumentMinimize.ToolTip=if($DocumentOpen -and -not $Managed){'문서 열기로 불러온 문서만 최소화할 수 있습니다.'}else{'한글 문서 창 최소화'}
    $HwpDocumentClose.ToolTip=if($OutputDocumentCount -gt 0){'출력 문서를 저장하거나 닫은 후 관리 원문서를 닫으세요.'}elseif($DocumentOpen -and -not $Managed){'프로그램에서 연 문서만 닫을 수 있습니다.'}else{'연결된 문서 닫기'}
}

function Set-HwpDocumentControlsBusy {
    $HwpDocumentOpen.IsEnabled=$false
    $HwpDocumentShow.IsEnabled=$false
    $HwpDocumentMinimize.IsEnabled=$false
    $HwpDocumentClose.IsEnabled=$false
}

function Refresh-HwpDocumentStatus([bool]$Silent=$true) {
    if($script:ProfileReviewActive -or $script:HwpDocumentBusy -or $script:BackendRequestInFlight){return}
    if(-not $LayoutPreview -and ($null -eq $Backend -or $Backend.HasExited)){
        Set-HwpDocumentPanelState ([pscustomobject]@{ok=$false;message='기능 백엔드가 종료되었습니다.'})
        return
    }
    $script:HwpDocumentBusy=$true
    Set-HwpDocumentControlsBusy
    try{
        $Response=Send-Backend @{action='hwp_document_status'}
        $script:HwpDocumentBusy=$false
        Set-HwpDocumentPanelState $Response
        if(-not $Response.ok -and -not $Silent){Show-Error $Response.message}
    }catch{
        $script:HwpDocumentBusy=$false
        Set-HwpDocumentPanelState ([pscustomobject]@{ok=$false;message=$_.Exception.Message})
        if(-not $Silent){Show-Error $_.Exception.Message}
    }
}

function Invoke-HwpDocumentAction([string]$Action,[hashtable]$Arguments=$null) {
    if($script:HwpDocumentBusy){return}
    $script:HwpDocumentBusy=$true
    Set-HwpDocumentControlsBusy
    try{
        $Command=@{action=$Action}
        if($null -ne $Arguments){foreach($Key in $Arguments.Keys){$Command[$Key]=$Arguments[$Key]}}
        $Response=Send-Backend $Command
        $script:HwpDocumentBusy=$false
        if(-not $Response.ok){throw $Response.message}
        Set-HwpDocumentPanelState $Response
        $Status.Text=$Response.message
        Refresh-HwpDocumentStatus $true
        return $Response
    }catch{
        $script:HwpDocumentBusy=$false
        Show-Error $_.Exception.Message
        Refresh-HwpDocumentStatus $true
        return $null
    }
}

function Open-HwpDocument {
    $Dialog=[Microsoft.Win32.OpenFileDialog]::new()
    $Dialog.Title='한글 문서 열기'
    $Dialog.Filter='한글 문서 (*.hwp;*.hwpx)|*.hwp;*.hwpx|HWP 문서 (*.hwp)|*.hwp|HWPX 문서 (*.hwpx)|*.hwpx'
    $Dialog.DefaultExt='.hwp'
    $Dialog.CheckFileExists=$true
    $Dialog.Multiselect=$false
    $CurrentPath=[string](Get-HwpDocumentValue $script:LastHwpDocumentStatus @('path','document_path','full_path','file_path') '')
    if($CurrentPath -and (Test-Path -LiteralPath $CurrentPath)){$Dialog.InitialDirectory=Split-Path -Parent $CurrentPath}
    if($Dialog.ShowDialog($Window) -ne $true){return}
    $FullPath=[System.IO.Path]::GetFullPath($Dialog.FileName)
    Refresh-HwpDocumentStatus $true
    $Managed=[bool](Get-HwpDocumentValue $script:LastHwpDocumentStatus @('managed','program_managed') $false)
    $LoadedPath=[string](Get-HwpDocumentValue $script:LastHwpDocumentStatus @('path','document_path','full_path','file_path') '')
    $SamePath=$false
    if($Managed -and $LoadedPath){
        try{$SamePath=[System.StringComparer]::OrdinalIgnoreCase.Equals([System.IO.Path]::GetFullPath($LoadedPath),$FullPath)}catch{$SamePath=$false}
    }
    if($Managed -and -not $SamePath){
        if(-not (Request-CloseManagedHwpDocument)){return}
    }
    [void](Invoke-HwpDocumentAction 'hwp_document_open' @{path=$FullPath;visible=$true})
}

function Request-CloseManagedHwpDocument {
    Refresh-HwpDocumentStatus $true
    $Managed=[bool](Get-HwpDocumentValue $script:LastHwpDocumentStatus @('managed','program_managed') $false)
    if(-not $Managed){return $true}
    $OutputDocumentCount=[int](Get-HwpDocumentValue $script:LastHwpDocumentStatus @('output_document_count') 0)
    if($OutputDocumentCount -gt 0){
        Show-Error '출력 문서를 저장하거나 닫은 후 다시 시도하세요.'
        return $false
    }
    $ModifiedValue=Get-HwpDocumentValue $script:LastHwpDocumentStatus @('modified','dirty','is_modified') $null
    $NeedsConfirmation=$null -eq $ModifiedValue -or [bool]$ModifiedValue
    $SaveChanges=$false
    if($NeedsConfirmation){
        $Prompt=if($null -eq $ModifiedValue){'문서의 수정 상태를 확인할 수 없습니다. 저장하고 닫을까요?'}else{'수정된 내용을 저장하고 문서를 닫을까요?'}
        $Choice=[System.Windows.MessageBox]::Show("$Prompt`n`n예: 저장 후 닫기  ·  아니오: 저장하지 않고 닫기",'한글 문서 닫기',[System.Windows.MessageBoxButton]::YesNoCancel,[System.Windows.MessageBoxImage]::Question)
        if($Choice -eq [System.Windows.MessageBoxResult]::Cancel){return $false}
        $SaveChanges=$Choice -eq [System.Windows.MessageBoxResult]::Yes
    }
    $Response=Invoke-HwpDocumentAction 'hwp_document_close' @{save_changes=[bool]$SaveChanges}
    return $null -ne $Response -and [bool]$Response.ok
}

function Close-HwpDocument {
    [void](Request-CloseManagedHwpDocument)
}

$HwpDocumentOpen.Add_Click({Open-HwpDocument})
$HwpDocumentShow.Add_Click({Invoke-HwpDocumentAction 'hwp_document_show'})
$HwpDocumentMinimize.Add_Click({Invoke-HwpDocumentAction 'hwp_document_minimize'})
$HwpDocumentClose.Add_Click({Close-HwpDocument})

function Show-Error([string]$Message) { $Status.Text="오류: $Message"; [System.Windows.MessageBox]::Show($Message,'범정부오피스 오류') | Out-Null }
function Connect-Hwp { try { $r=Send-Backend @{action='connect'}; $Status.Text=$r.message; if(-not $r.ok){Show-Error $r.message}else{Refresh-HwpDocumentStatus $true} } catch { Show-Error $_.Exception.Message } }
function Activate-SelectionHwp {
    try{
        $state=Send-Backend @{action='hwp_document_status'}
        if($state.ok -and $state.document.managed){
            $shown=Send-Backend @{action='hwp_document_show'}
            return [bool]$shown.ok
        }
    }catch{return $false}
    return $false
}
function Invoke-LayoutButton($Item) {
    try {
        $r=Send-Backend @{action='run_sequence';operations=@($Item.operations)}
        $Status.Text=$r.message; if(-not $r.ok){Show-Error $r.message}else{Refresh-HwpDocumentStatus $true}
    } catch { Show-Error $_.Exception.Message }
}
function Invoke-FormatCopy {
    try {
        $r=Send-Backend @{action='format_copy'}
        $Status.Text=$r.message
        if(-not $r.ok){Show-Error $r.message}
    } catch { Show-Error $_.Exception.Message }
}
function Open-ManualStyleCandidate($Analysis,$OwnerWindow=$Window) {
    $Profile=Send-Backend @{action='user_profile_get'};if(-not $Profile.ok){throw $Profile.message}
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='직접 필드 지정';$Dialog.Width=540;$Dialog.Height=330;$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.ResizeMode='NoResize';$Dialog.Background='White';$Dialog.FontFamily='맑은 고딕'
    $Grid=[System.Windows.Controls.Grid]::new();$Dialog.Content=$Grid;foreach($height in @(58,62,54,'*',46)){$row=[System.Windows.Controls.RowDefinition]::new();if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)};[void]$Grid.RowDefinitions.Add($row)}
    $Header=[System.Windows.Controls.Border]::new();$Header.Background='#66558F';$HeaderText=[System.Windows.Controls.TextBlock]::new();$HeaderText.Text='후보에 없는 값을 직접 지정합니다';$HeaderText.Foreground='White';$HeaderText.FontSize=17;$HeaderText.FontWeight='Bold';$HeaderText.Margin='16,15';$Header.Child=$HeaderText;[void]$Grid.Children.Add($Header)
    $Guide=[System.Windows.Controls.TextBlock]::new();$Guide.Text="1. 대표필드를 고르거나 새 이름을 입력합니다.`n2. '한글에서 값 선택'을 누른 뒤 전체 영역 안의 실제 값만 정확히 드래그합니다.";$Guide.Margin='16,10';$Guide.TextWrapping='Wrap';$Guide.Foreground='#555555';[System.Windows.Controls.Grid]::SetRow($Guide,1);[void]$Grid.Children.Add($Guide)
    $FieldGrid=[System.Windows.Controls.Grid]::new();$FieldGrid.Margin='16,7';$labelColumn=[System.Windows.Controls.ColumnDefinition]::new();$labelColumn.Width=92;[void]$FieldGrid.ColumnDefinitions.Add($labelColumn);[void]$FieldGrid.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new());$FieldLabel=[System.Windows.Controls.TextBlock]::new();$FieldLabel.Text='대표필드';$FieldLabel.FontWeight='SemiBold';$FieldLabel.VerticalAlignment='Center';[void]$FieldGrid.Children.Add($FieldLabel);$Field=[System.Windows.Controls.ComboBox]::new();$Field.IsEditable=$true;$Field.Height=32;$Field.DisplayMemberPath='path';foreach($group in @($Profile.field_groups)){if(-not $group.path){$group|Add-Member -NotePropertyName path -NotePropertyValue ([string]$group.name) -Force};[void]$Field.Items.Add($group)};[System.Windows.Controls.Grid]::SetColumn($Field,1);[void]$FieldGrid.Children.Add($Field);[System.Windows.Controls.Grid]::SetRow($FieldGrid,2);[void]$Grid.Children.Add($FieldGrid)
    $SelectionPanel=[System.Windows.Controls.Border]::new();$SelectionPanel.Margin='16,4';$SelectionPanel.Padding='12';$SelectionPanel.Background='#F8F6FB';$SelectionPanel.BorderBrush='#D9D2E7';$SelectionPanel.BorderThickness=1;$SelectionPanel.CornerRadius=10;$SelectionGrid=[System.Windows.Controls.Grid]::new();[void]$SelectionGrid.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new());$buttonColumn=[System.Windows.Controls.ColumnDefinition]::new();$buttonColumn.Width=145;[void]$SelectionGrid.ColumnDefinitions.Add($buttonColumn);$SelectionPanel.Child=$SelectionGrid;$SelectionStatus=[System.Windows.Controls.TextBlock]::new();$SelectionStatus.Text='아직 직접 지정할 값을 선택하지 않았습니다.';$SelectionStatus.TextWrapping='Wrap';$SelectionStatus.VerticalAlignment='Center';[void]$SelectionGrid.Children.Add($SelectionStatus);$Choose=[System.Windows.Controls.Button]::new();$Choose.Content='한글에서 값 선택';$Choose.Width=135;$Choose.Height=34;[System.Windows.Controls.Grid]::SetColumn($Choose,1);[void]$SelectionGrid.Children.Add($Choose);[System.Windows.Controls.Grid]::SetRow($SelectionPanel,3);[void]$Grid.Children.Add($SelectionPanel)
    $Buttons=[System.Windows.Controls.StackPanel]::new();$Buttons.Orientation='Horizontal';$Buttons.HorizontalAlignment='Right';$Buttons.Margin='16,6,16,8';$Import=[System.Windows.Controls.Button]::new();$Import.Content='선택값 가져오기';$Import.Width=120;$Import.Margin='0,0,8,0';$Import.Background='#66558F';$Import.Foreground='White';$Import.IsEnabled=$false;$Cancel=[System.Windows.Controls.Button]::new();$Cancel.Content='취소';$Cancel.Width=75;[void]$Buttons.Children.Add($Import);[void]$Buttons.Children.Add($Cancel);[System.Windows.Controls.Grid]::SetRow($Buttons,4);[void]$Grid.Children.Add($Buttons)
    Set-OriginalSectionHeader $Header $HeaderText;Set-OriginalFlatButton $Choose $false;Set-OriginalFlatButton $Import $true;Set-OriginalFlatButton $Cancel $false
    $script:ManualCandidateResult=$null;$script:ManualSelectionToken=$null
    $BeginManualSelection={
        $begin=Send-Backend @{action='style_preset_manual_selection_begin';draft_id=$Analysis.draft_id};if(-not $begin.ok){throw $begin.message};$script:ManualSelectionToken=[string]$begin.selection_token;$Import.IsEnabled=$false;$SelectionStatus.Text=$begin.message;$SelectionPanel.Background='#F8F6FB';$SelectionPanel.BorderBrush='#D9D2E7'
    }.GetNewClosure()
    $Choose.Add_Click({try{& $BeginManualSelection;$script:SelectionReturnWindow=$Dialog;if(-not (Activate-SelectionHwp)){$SelectionStatus.Text='화면에 표시된 관리 한글 창을 찾지 못했습니다.'}}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $ManualStateTimer=[System.Windows.Threading.DispatcherTimer]::new();$ManualStateTimer.Interval=[TimeSpan]::FromMilliseconds(300);$ManualStateTimer.Add_Tick([GovOfficePollGuard]::Wrap({
        try{
            if(-not $script:ManualSelectionToken){return}
            # 100ms 마우스 폴링이 짧은 드래그를 놓치더라도 한글이 전면이고
            # 버튼을 놓은 상태라면 현재 선택을 직접 확인한다. 더블클릭·키보드
            # 선택도 이 경로로 잡힌다.
            $foregroundPid=[GovOfficeSelectionMouse]::ForegroundProcessId()
            if($foregroundPid -gt 0 -and -not [GovOfficeSelectionMouse]::LeftButtonDown()){
                try{$foregroundProcess=Get-Process -Id $foregroundPid -ErrorAction Stop}catch{$foregroundProcess=$null}
                if($null -ne $foregroundProcess -and $foregroundProcess.ProcessName -eq 'Hwp'){
                    $probe=Send-Backend @{action='style_preset_selection_probe'}
                    if($probe.captured -and $null -ne $script:SelectionReturnWindow){$returnWindow=$script:SelectionReturnWindow;$script:SelectionReturnWindow=$null;[void]$returnWindow.Activate()}
                }
            }
            $state=Send-Backend @{action='style_preset_selection_status';probe=$false}
            if($state.selection_ready){$Import.IsEnabled=$true;$SelectionStatus.Text='직접 선택한 값이 확인되었습니다. 선택값 가져오기를 누르세요.';$SelectionPanel.Background='#ECF8F0';$SelectionPanel.BorderBrush='#54A56B'}
        }catch{}
    }.GetNewClosure()));$ManualStateTimer.Start()
    $Import.Add_Click({try{$fieldName=[string]$Field.Text;if([string]::IsNullOrWhiteSpace($fieldName)){$SelectionStatus.Text='대표필드를 선택하거나 새 이름을 입력하세요.';return};$response=Send-Backend @{action='style_preset_manual_candidate';draft_id=$Analysis.draft_id;selection_token=$script:ManualSelectionToken;field_name=$fieldName.Trim()};if(-not $response.ok){throw $response.message};$script:ManualCandidateResult=$response;$Dialog.Close()}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $Cancel.Add_Click({$Dialog.Close()});$Dialog.Add_Closed({$ManualStateTimer.Stop();if($script:SelectionReturnWindow -eq $Dialog){$script:SelectionReturnWindow=$null};if($script:ManualSelectionToken){try{[void](Send-Backend @{action='style_preset_manual_selection_cancel';selection_token=$script:ManualSelectionToken})}catch{}}}.GetNewClosure());try{& $BeginManualSelection}catch{Show-Error $_.Exception.Message};[void]$Dialog.ShowDialog();$result=$script:ManualCandidateResult;$script:ManualCandidateResult=$null;$script:ManualSelectionToken=$null;return $result
}
function Open-StyleCaptureReview($Analysis,$OwnerWindow=$Window) {
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='서식 저장 필드 확인';$Dialog.Width=760;$Dialog.Height=690;$Dialog.MinWidth=680;$Dialog.MinHeight=540;$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.ResizeMode='CanResizeWithGrip';$Dialog.Background='White';$Dialog.FontFamily='맑은 고딕'
    $Grid=[System.Windows.Controls.Grid]::new();$Dialog.Content=$Grid;foreach($height in @(58,88,'*',48)){$row=[System.Windows.Controls.RowDefinition]::new();if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)};[void]$Grid.RowDefinitions.Add($row)}
    $Header=[System.Windows.Controls.Border]::new();$Header.Background='#66558F';[System.Windows.Controls.Grid]::SetRow($Header,0);[void]$Grid.Children.Add($Header);$HeaderText=[System.Windows.Controls.TextBlock]::new();$HeaderText.Text='어떤 값을 입력 필드로 저장할지 확인하세요';$HeaderText.Foreground='White';$HeaderText.FontSize=17;$HeaderText.FontWeight='Bold';$HeaderText.Margin='16,15';$Header.Child=$HeaderText
    Set-OriginalSectionHeader $Header $HeaderText
    $Guide=[System.Windows.Controls.TextBlock]::new();$Guide.Margin='16,8';$Guide.TextWrapping='Wrap';$Guide.Foreground='#555555';$Guide.Text=if(@($Analysis.candidates).Count){'이동 손잡이를 원하는 대표필드 묶음 안에 놓으세요. 제목뿐 아니라 값·하위필드 영역에도 놓을 수 있습니다. 대표필드를 끌면 그 안의 하위필드들이 대상 대표필드로 옮겨집니다. 하위필드도 개별 이동할 수 있습니다. 처음 체크된 후보를 먼저 표시하며 각 항목군 안의 기존 순서는 유지합니다.'}else{'선택 영역에서 필드 후보를 찾지 못했습니다. 확인하면 원본 내용과 서식을 그대로 저장합니다.'};[System.Windows.Controls.Grid]::SetRow($Guide,1);[void]$Grid.Children.Add($Guide)
    $Scroll=[System.Windows.Controls.ScrollViewer]::new();$Scroll.Margin='16,4';$Panel=[System.Windows.Controls.StackPanel]::new();$Scroll.Content=$Panel;[System.Windows.Controls.Grid]::SetRow($Scroll,2);[void]$Grid.Children.Add($Scroll)
    # 대표필드/하위필드 계층은 유지한다. 완전히 같은 필드와 값은 한 줄로
    # 접어 중복 노출을 없애고, 유사 관계는 병합하지 않은 채 정렬에만 쓴다.
    $CandidateById=@{};$DisplayByKey=@{};$AllCandidates=New-Object System.Collections.ArrayList;$Selected=@{};$Checks=New-Object System.Collections.ArrayList;$CandidateOverrides=@{};$SourceCandidates=New-Object System.Collections.ArrayList;$ReviewActions=[pscustomobject]@{MoveChild=$null;MoveGroup=$null;Rebuild=$null;Reset=$null;Confirm=$null};$DefaultGuideText=$Guide.Text
    # ButtonBase(CheckBox)가 마우스를 캡처하기 전에 독립 손잡이가 포인터를 잡는다.
    # 일정 거리 이상 움직였을 때만 DataObject 기반 WPF 드래그를 시작해 클릭 오작동도 막는다.
    $AttachDragSource={param([System.Windows.FrameworkElement]$Element,[string]$Payload)
        $DragState=[pscustomobject]@{payload=$Payload;armed=$false;start=$null;guide=$Guide};$Element.Tag=$DragState
        $Element.Add_PreviewMouseLeftButtonDown({$eventArgs=$_;try{$state=$this.Tag;$state.start=$eventArgs.GetPosition($this);$state.armed=$true;if(-not $this.CaptureMouse()){throw '드래그 손잡이가 마우스를 확보하지 못했습니다.'};$eventArgs.Handled=$true}catch{$failure=$_;try{$this.Tag.armed=$false;if($this.IsMouseCaptured){$this.ReleaseMouseCapture()}}catch{};Write-GuiRuntimeError 'style review drag mouse down' $failure;$this.Tag.guide.Text="드래그를 시작하지 못했습니다: $($failure.Exception.Message)";$eventArgs.Handled=$true}}.GetNewClosure())
        $Element.Add_PreviewMouseMove({$eventArgs=$_;try{$state=$this.Tag;if(-not [bool]$state.armed-or $eventArgs.LeftButton -ne [System.Windows.Input.MouseButtonState]::Pressed){return};$current=$eventArgs.GetPosition($this);$dx=[Math]::Abs([double]$current.X-[double]$state.start.X);$dy=[Math]::Abs([double]$current.Y-[double]$state.start.Y);if($dx -lt [System.Windows.SystemParameters]::MinimumHorizontalDragDistance -and $dy -lt [System.Windows.SystemParameters]::MinimumVerticalDragDistance){return};$state.armed=$false;if($this.IsMouseCaptured){$this.ReleaseMouseCapture()};$data=[System.Windows.DataObject]::new([string],[string]$state.payload);[void][System.Windows.DragDrop]::DoDragDrop($this,$data,[System.Windows.DragDropEffects]::Move);$eventArgs.Handled=$true}catch{$failure=$_;try{$this.Tag.armed=$false;if($this.IsMouseCaptured){$this.ReleaseMouseCapture()}}catch{};Write-GuiRuntimeError 'style review drag move' $failure;$this.Tag.guide.Text="드래그 처리 중 오류를 복구했습니다: $($failure.Exception.Message)";$eventArgs.Handled=$true}}.GetNewClosure())
        $Element.Add_PreviewMouseLeftButtonUp({$eventArgs=$_;try{$state=$this.Tag;$state.armed=$false;if($this.IsMouseCaptured){$this.ReleaseMouseCapture()};$eventArgs.Handled=$true}catch{$failure=$_;Write-GuiRuntimeError 'style review drag mouse up' $failure;$eventArgs.Handled=$true}}.GetNewClosure())
        $Element.Add_LostMouseCapture({try{if($null -ne $this.Tag){$this.Tag.armed=$false}}catch{Write-GuiRuntimeError 'style review drag capture lost' $_}}.GetNewClosure())
    }.GetNewClosure()
    # 백엔드가 전달한 HWPML 위→아래 순서를 그대로 사용한다. 구버전 응답만
    # 등록/신규 배열을 합치는 호환 경로로 처리한다.
    $OrderedAnalysisCandidates=@($Analysis.candidates)
    if($OrderedAnalysisCandidates.Count -eq 0){$OrderedAnalysisCandidates=@($Analysis.registered_candidates)+@($Analysis.unregistered_candidates)}
    foreach($candidate in $OrderedAnalysisCandidates){[void]$SourceCandidates.Add($candidate)}
    $AddCandidates={param([object[]]$Candidates)
        $sourceSequence=0
        foreach($candidate in @($Candidates)){
            $id=[string]$candidate.candidate_id;if([string]::IsNullOrWhiteSpace($id)-or $CandidateById.ContainsKey($id)){continue}
            $direction=if($candidate.direction -eq 'right'){'오른쪽 값'}elseif($candidate.direction -eq 'below'){'아래쪽 값'}else{'같은 칸 값'}
            $position=if([int]$candidate.table -lt 0){"본문 $([int]$candidate.row+1)번째 문단 · $direction"}else{("표 {0} · 라벨 {1}행 {2}열 · {3}" -f ([int]$candidate.table+1),([int]$candidate.row+1),([int]$candidate.col+1),$direction)}
            $certainty=[bool]$candidate.recommended;$registration=if($candidate.registered){'저장된 필드'}else{'새 필드'}
            $structuralParent=[string]$candidate.structural_parent_field;$structuralGroup=[string]$candidate.structural_group_id;$semanticGroup=[string]$candidate.semantic_group_id
            $representative=[string]$candidate.semantic_representative_field;if([string]::IsNullOrWhiteSpace($representative)){if(-not [string]::IsNullOrWhiteSpace($structuralParent)){$representative=$structuralParent}else{$representative=[string]$candidate.representative_field;if([string]::IsNullOrWhiteSpace($representative)){$representative=[string]$candidate.field}}}
            $child=[string]$candidate.semantic_child_field;if([string]::IsNullOrWhiteSpace($child)){if(-not [string]::IsNullOrWhiteSpace($structuralParent)){$child=[string]$candidate.label}else{$child=[string]$candidate.child_field}}
            $semanticChild=[string]$candidate.semantic_child_id;if([string]::IsNullOrWhiteSpace($semanticChild)){$semanticChild=$child.Trim().ToLowerInvariant()};if([string]::IsNullOrWhiteSpace($semanticGroup)){$semanticGroup=$structuralGroup};if([string]::IsNullOrWhiteSpace($semanticGroup)){$semanticGroup="candidate:$id"};$value=[string]$candidate.value;$fullField=[string]$candidate.field_path;if([string]::IsNullOrWhiteSpace($fullField)){$fullField=[string]$candidate.field};$originalFullField=$fullField
            $moveKind='';$wasMoved=$false;if($CandidateOverrides.ContainsKey($id)){$override=$CandidateOverrides[$id];$semanticGroup=[string]$override.group_key;$semanticChild=[string]$override.child_key;$representative=[string]$override.representative;$child=[string]$override.child;$fullField=[string]$override.field;$moveKind=[string]$override.kind;$wasMoved=$true}
            $key=("{0}{3}{1}{3}{2}" -f $semanticGroup,$semanticChild,$value,[char]31);$similarityRank=[int]$candidate.relationship_sort_rank;$documentOrder=if($null -ne $candidate.PSObject.Properties['document_order']){[int]$candidate.document_order}else{$sourceSequence};$relationshipAnchorOrder=if($null -ne $candidate.PSObject.Properties['relationship_anchor_order']){[int]$candidate.relationship_anchor_order}else{$documentOrder};$sourceSequence++
            if($DisplayByKey.ContainsKey($key)){
                $row=$DisplayByKey[$key];[void]$row.ids.Add($id);if(-not $row.positions.Contains($position)){[void]$row.positions.Add($position)};if(-not $row.values.Contains($value)){[void]$row.values.Add($value)};if(-not $row.original_fields.Contains($originalFullField)){[void]$row.original_fields.Add($originalFullField)};if($moveKind -and -not $row.move_kinds.Contains($moveKind)){[void]$row.move_kinds.Add($moveKind)};if($wasMoved){$row.moved=$true}
                if($certainty -and -not [bool]$row.confirmed){$row.confirmed=$true}
                if([bool]$candidate.registered){$row.registration='저장된 필드'}
            }else{
                $ids=New-Object System.Collections.ArrayList;[void]$ids.Add($id);$positions=New-Object System.Collections.ArrayList;[void]$positions.Add($position);$values=New-Object System.Collections.ArrayList;[void]$values.Add($value);$originalFields=New-Object System.Collections.ArrayList;[void]$originalFields.Add($originalFullField);$moveKinds=New-Object System.Collections.ArrayList;if($moveKind){[void]$moveKinds.Add($moveKind)}
                $row=[pscustomobject]@{key=$key;group_key=$semanticGroup;child_key=$semanticChild;structural_group_key=$structuralGroup;ids=$ids;representative=$representative;full_field=$fullField;child=$child;value=$value;values=$values;confirmed=$certainty;registration=$registration;positions=$positions;similarity_rank=$similarityRank;document_order=$documentOrder;relationship_anchor_order=$relationshipAnchorOrder;style=([string]$candidate.classification_basis -eq 'cell_style');moved=$wasMoved;original_fields=$originalFields;move_kinds=$moveKinds}
                $DisplayByKey[$key]=$row;[void]$AllCandidates.Add($row)
            }
            $CandidateById[$id]=$row;if(-not $Selected.ContainsKey($id)){$Selected[$id]=$certainty}
        }
    }.GetNewClosure()
    & $AddCandidates @($SourceCandidates)
    $SyncChecks={foreach($check in @($Checks)){$row=$check.Tag.row;foreach($candidateId in @($row.ids)){$Selected[[string]$candidateId]=[bool]$check.IsChecked}}}.GetNewClosure()
    $RenderSummary={param([string]$Title,[int]$Count,[string]$Color,[string]$Foreground)
        if($Count -eq 0){return};$Summary=[System.Windows.Controls.Border]::new();$Summary.Background=$Color;$Summary.BorderBrush='#DED8EA';$Summary.BorderThickness=1;$Summary.CornerRadius=9;$Summary.Margin='0,6,8,4';$Summary.Padding='10,5';$Summary.HorizontalAlignment='Left';$SummaryText=[System.Windows.Controls.TextBlock]::new();$SummaryText.Text=("{0} · {1}개" -f $Title,$Count);$SummaryText.FontWeight='SemiBold';$SummaryText.Foreground=$Foreground;$Summary.Child=$SummaryText;[void]$Panel.Children.Add($Summary)
    }.GetNewClosure()
    $RenderGroups={param([object[]]$Rows)
        # 최초 문서/관계 순서를 만든 뒤, 최초 추천 여부로 안정 분할한다.
        # 사용자가 체크를 바꿀 때마다 위치가 튀지 않도록 Selected는 정렬에 쓰지 않는다.
        $groups=[ordered]@{};foreach($row in @($Rows|Sort-Object relationship_anchor_order,document_order)){if(-not $groups.Contains([string]$row.group_key)){$groups[[string]$row.group_key]=New-Object System.Collections.ArrayList};[void]$groups[[string]$row.group_key].Add($row)}
        $priorityGroups=New-Object System.Collections.ArrayList;$otherGroups=New-Object System.Collections.ArrayList
        foreach($key in @($groups.Keys)){
            $priorityRows=@($groups[$key]|Where-Object{[bool]$_.confirmed})
            $otherRows=@($groups[$key]|Where-Object{-not [bool]$_.confirmed})
            $groups[$key]=@($priorityRows)+@($otherRows)
            if($priorityRows.Count){[void]$priorityGroups.Add($key)}else{[void]$otherGroups.Add($key)}
        }
        foreach($groupKey in (@($priorityGroups)+@($otherGroups))){
            $GroupRows=@($groups[$groupKey]);$groupTitle=[string]$GroupRows[0].representative;$groupMovedCount=0;foreach($groupRow in $GroupRows){foreach($candidateId in @($groupRow.ids)){if($CandidateOverrides.ContainsKey([string]$candidateId)){$groupMovedCount++}}};$GroupCard=[System.Windows.Controls.Border]::new();$GroupCard.BorderBrush=if($groupMovedCount){'#66558F'}else{'#D9D2E5'};$GroupCard.BorderThickness=if($groupMovedCount){2}else{1};$GroupCard.CornerRadius=12;$groupDepth=[Math]::Max(0,@($groupTitle -split '>').Count-1);$GroupCard.Margin=("{0},8,0,4" -f ([Math]::Min(72,$groupDepth*18)));$GroupPanel=[System.Windows.Controls.StackPanel]::new();$GroupCard.Child=$GroupPanel
            $HeaderRestBackground=if($groupMovedCount){'#F3F0F8'}else{'#F8F6FB'};$HeaderContext=[pscustomobject]@{row=$GroupRows[0];actions=$ReviewActions;guide=$Guide;rest_background=$HeaderRestBackground};$HeaderBorder=[System.Windows.Controls.Border]::new();$HeaderBorder.Background=$HeaderRestBackground;$HeaderBorder.BorderBrush='#DED8EA';$HeaderBorder.BorderThickness='0,0,0,1';$HeaderBorder.Padding='10,8';$HeaderBorder.AllowDrop=$true;$HeaderBorder.Tag=$HeaderContext;$HeaderBorder.ToolTip='하위필드를 놓으면 이 묶음으로 이동하고, 대표필드를 놓으면 그 안의 하위필드들이 이 묶음으로 이동합니다.';$HeaderContent=[System.Windows.Controls.DockPanel]::new();$GroupDragHandle=[System.Windows.Controls.Border]::new();$GroupDragHandle.Background=New-PurpleAccentBrush;$GroupDragHandle.CornerRadius=8;$GroupDragHandle.Padding='8,4';$GroupDragHandle.Margin='10,0,0,0';$GroupDragHandle.Cursor='Hand';$GroupDragLabel=[System.Windows.Controls.TextBlock]::new();$GroupDragLabel.Text='≡ 대표필드 끌기';$GroupDragLabel.Foreground='White';$GroupDragLabel.FontSize=10;$GroupDragHandle.Child=$GroupDragLabel;[System.Windows.Controls.DockPanel]::SetDock($GroupDragHandle,[System.Windows.Controls.Dock]::Right);[void]$HeaderContent.Children.Add($GroupDragHandle);$GroupHeader=[System.Windows.Controls.CheckBox]::new();$GroupHeader.FontWeight='Bold';$GroupHeader.FontSize=13;$GroupHeader.Foreground=if($groupMovedCount){'#55447A'}else{'#262626'};$GroupHeader.IsThreeState=$false;$movedHeaderText=if($groupMovedCount){" · ✓ 구조 이동 $groupMovedCount개"}else{''};$GroupHeader.Content=("대표필드: {0} · 하위 항목 {1}개{2}" -f $groupTitle,$GroupRows.Count,$movedHeaderText);[void]$HeaderContent.Children.Add($GroupHeader);$HeaderBorder.Child=$HeaderContent;[void]$GroupPanel.Children.Add($HeaderBorder)
            # 제목뿐 아니라 값/체크박스 위의 드롭도 대표필드로 전달한다.
            # 터널 이벤트로 내부 컨트롤보다 먼저 받아 중복 실행을 막는다.
            $GroupCard.AllowDrop=$true
            $GroupCard.Background=[System.Windows.Media.Brushes]::Transparent
            $GroupCard.Tag=$HeaderContext
            $HeaderContext | Add-Member -NotePropertyName drop_header -NotePropertyValue $HeaderBorder
            $GroupCard.ToolTip='이 묶음 안에 놓으면 대표필드 아래로 이동합니다.'
            $GroupCard.Add_PreviewDragOver({
                $eventArgs=$_
                try{
                    $payload=[string]$eventArgs.Data.GetData([string])
                    if($payload.StartsWith('govoffice-candidate:') -or $payload.StartsWith('govoffice-group:')){
                        $this.Background='#ECF9F0'
                        $eventArgs.Effects=[System.Windows.DragDropEffects]::Move
                        $eventArgs.Handled=$true
                    }
                }catch{Write-GuiRuntimeError 'style review group drag over' $_}
            }.GetNewClosure())
            $GroupCard.Add_DragLeave({$this.Background=[System.Windows.Media.Brushes]::Transparent}.GetNewClosure())
            $GroupCard.Add_PreviewDrop({
                $eventArgs=$_
                try{
                    $payload=[string]$eventArgs.Data.GetData([string])
                    if(-not ($payload.StartsWith('govoffice-candidate:') -or $payload.StartsWith('govoffice-group:'))){return}
                    $header=$this.Tag.drop_header
                    $this.Background=[System.Windows.Media.Brushes]::Transparent
                    $context=$this.Tag
                    if($payload.StartsWith('govoffice-candidate:')){
                        $sourceId=$payload.Substring(20)
                        & ($context.actions.MoveChild) $sourceId $context.row
                    }else{
                        $sourceGroup=$payload.Substring(16)
                        & ($context.actions.MoveGroup) $sourceGroup $context.row
                    }
                    $header.Background=$this.Tag.rest_background
                    $eventArgs.Handled=$true
                }catch{
                    Write-GuiRuntimeError 'style review group drop' $_
                    $this.Tag.guide.Text="구조 이동 오류: $($_.Exception.Message)"
                    $eventArgs.Handled=$true
                }
            }.GetNewClosure())
            & $AttachDragSource $GroupDragHandle "govoffice-group:$groupKey"
            $HeaderBorder.Add_DragEnter({$eventArgs=$_;try{if($eventArgs.Data.GetDataPresent([string])){$this.Background='#B7F0CA';$this.BorderBrush='#16803C';$this.BorderThickness=2;$eventArgs.Effects=[System.Windows.DragDropEffects]::Move;$eventArgs.Handled=$true}}catch{$failure=$_;Write-GuiRuntimeError 'style review representative drag enter' $failure;$eventArgs.Handled=$true}}.GetNewClosure());$HeaderBorder.Add_DragLeave({try{$this.Background=$this.Tag.rest_background;$this.BorderThickness=0}catch{Write-GuiRuntimeError 'style review representative drag leave' $_}}.GetNewClosure());$HeaderBorder.Add_Drop({$eventArgs=$_;try{$context=$this.Tag;$this.Background=$context.rest_background;$this.BorderThickness=0;$payload=[string]$eventArgs.Data.GetData([string]);if($payload.StartsWith('govoffice-candidate:')){$sourceId=$payload.Substring(20);& ($context.actions.MoveChild) $sourceId $context.row}elseif($payload.StartsWith('govoffice-group:')){$sourceGroup=$payload.Substring(16);& ($context.actions.MoveGroup) $sourceGroup $context.row};$eventArgs.Handled=$true}catch{$failure=$_;Write-GuiRuntimeError 'style review representative drop' $failure;$this.Tag.guide.Text="구조 이동 오류를 복구했습니다: $($failure.Exception.Message)";$eventArgs.Handled=$true}}.GetNewClosure())
            $ChildChecks=New-Object System.Collections.ArrayList;$GroupState=[pscustomobject]@{Parent=$GroupHeader;Children=$ChildChecks;Updating=$false};$GroupHeader.Tag=$GroupState
            foreach($row in $GroupRows){
                $allSelected=$true;foreach($candidateId in @($row.ids)){if(-not [bool]$Selected[[string]$candidateId]){$allSelected=$false;break}}
                $rowMoved=[bool]$row.moved;$RowRestBackground=if($rowMoved){'#ECF9F0'}else{'Transparent'};$RowContext=[pscustomobject]@{row=$row;actions=$ReviewActions;guide=$Guide;rest_background=$RowRestBackground};$RowContainer=[System.Windows.Controls.DockPanel]::new();$RowContainer.Margin='24,3,8,3';$RowContainer.Background=$RowRestBackground;$RowContainer.AllowDrop=$true;$RowContainer.Tag=$RowContext;$RowContainer.ToolTip='손잡이를 원하는 대표필드 묶음 안에 놓으세요.';$Check=[System.Windows.Controls.CheckBox]::new();$Check.Padding='7';$Check.FontSize=11;$Check.Tag=[pscustomobject]@{row=$row;group=$GroupState};$Check.IsChecked=$allSelected
                $statusText=if([bool]$row.confirmed){'확정'}else{'미확정'};$styleText=if([bool]$row.style){' · 셀 서식 판별'}else{''};$childText=if([string]::IsNullOrWhiteSpace([string]$row.child)){'(대표필드 직접 값)'}else{[string]$row.child};$valueText=@($row.values)-join ' / ';$positionText=[string]$row.positions[0];$duplicateText=if($row.ids.Count -gt 1){" · 연결 위치 $($row.ids.Count)곳"}else{''}
                $DragHandle=[System.Windows.Controls.Border]::new();$DragHandle.Background='White';$DragHandle.BorderBrush='#D9D2E5';$DragHandle.BorderThickness=1;$DragHandle.CornerRadius=8;$DragHandle.Padding='8,5';$DragHandle.Margin='10,0,0,0';$DragHandle.Cursor='Hand';$DragLabel=[System.Windows.Controls.TextBlock]::new();$DragLabel.Text='≡ 하위필드 옮기기';$DragLabel.Foreground='#55447A';$DragLabel.FontWeight='SemiBold';$DragHandle.Child=$DragLabel;[System.Windows.Controls.DockPanel]::SetDock($DragHandle,[System.Windows.Controls.Dock]::Right);[void]$RowContainer.Children.Add($DragHandle)
                if($rowMoved){$MoveBadge=[System.Windows.Controls.Border]::new();$MoveBadge.Background='#2F855A';$MoveBadge.CornerRadius=10;$MoveBadge.Padding='8,3';$MoveBadge.Margin='8,2,0,2';$MoveBadge.VerticalAlignment='Top';$MoveBadgeText=[System.Windows.Controls.TextBlock]::new();$MoveBadgeText.Text='✓ 이동됨';$MoveBadgeText.Foreground='White';$MoveBadgeText.FontSize=10;$MoveBadgeText.FontWeight='Bold';$MoveBadge.Child=$MoveBadgeText;[System.Windows.Controls.DockPanel]::SetDock($MoveBadge,[System.Windows.Controls.Dock]::Right);[void]$RowContainer.Children.Add($MoveBadge)}
                $moveLine='';if($rowMoved){$changedOrigins=@($row.original_fields|Where-Object{[string]$_ -ne [string]$row.full_field}|Sort-Object -Unique);$kindLabels=@($row.move_kinds|ForEach-Object{if($_ -eq 'child'){'하위필드 이동'}elseif($_ -eq 'representative'){'대표필드 구조 이동'}else{'구조 이동'}}|Sort-Object -Unique);$kindText=$kindLabels -join ', ';$moveLine=("✓ {0}: {1}  →  {2}`n" -f $kindText,($changedOrigins -join ', '),$row.full_field)}
                $Text=[System.Windows.Controls.TextBlock]::new();$Text.TextWrapping='Wrap';$Text.Foreground=if($rowMoved){'#195C37'}else{'#222222'};$Text.Text=("{0}하위필드: {1}`n값: {2}`n{3}{4} · {5} · {6}{7}" -f $moveLine,$childText,$valueText,$positionText,$duplicateText,$statusText,$row.registration,$styleText);$Check.Content=$Text;$Check.Background='Transparent';[void]$RowContainer.Children.Add($Check);[void]$ChildChecks.Add($Check);[void]$Checks.Add($Check);[void]$GroupPanel.Children.Add($RowContainer)
                & $AttachDragSource $DragHandle "govoffice-candidate:$([string]$row.ids[0])"
                $Check.Add_Click({$state=$this.Tag.group;if([bool]$state.Updating){return};$checkedCount=0;foreach($child in @($state.Children)){if($child.IsChecked -eq $true){$checkedCount++}};$state.Updating=$true;$state.Parent.IsChecked=($checkedCount -gt 0);$state.Updating=$false}.GetNewClosure())
            }
            $initialChecked=0;foreach($child in @($ChildChecks)){if($child.IsChecked -eq $true){$initialChecked++}};$GroupHeader.IsChecked=($initialChecked -gt 0)
            $GroupHeader.Add_Click({$state=$this.Tag;if([bool]$state.Updating){return};$state.Updating=$true;$target=($this.IsChecked -eq $true);foreach($child in @($state.Children)){$child.IsChecked=$target};$state.Updating=$false}.GetNewClosure());[void]$Panel.Children.Add($GroupCard)
        }
    }.GetNewClosure()
    $RenderAll={
        & $SyncChecks;$Panel.Children.Clear();$Checks.Clear();$confirmed=New-Object System.Collections.ArrayList;$unconfirmed=New-Object System.Collections.ArrayList
        foreach($row in @($AllCandidates)){if([bool]$row.confirmed){[void]$confirmed.Add($row)}else{[void]$unconfirmed.Add($row)}}
        if($CandidateOverrides.Count){$moveTargetCount=@($CandidateOverrides.Values|ForEach-Object{[string]$_.field}|Sort-Object -Unique).Count;$MoveState=[System.Windows.Controls.Border]::new();$MoveState.Background='#DDF6E7';$MoveState.BorderBrush='#38A169';$MoveState.BorderThickness=2;$MoveState.CornerRadius=6;$MoveState.Margin='0,5,8,8';$MoveState.Padding='12,8';$MoveStateText=[System.Windows.Controls.TextBlock]::new();$MoveStateText.Text=("✓ 구조 이동 적용 중 · 문서 위치 {0}개 · 이동 후 필드 {1}개`n연두색 항목은 부모 경로만 변경되며 값과 필드명은 합쳐지지 않습니다." -f $CandidateOverrides.Count,$moveTargetCount);$MoveStateText.Foreground='#195C37';$MoveStateText.FontWeight='Bold';$MoveStateText.TextWrapping='Wrap';$MoveState.Child=$MoveStateText;[void]$Panel.Children.Add($MoveState)}
        if($AllCandidates.Count -eq 0){$Empty=[System.Windows.Controls.TextBlock]::new();$Empty.Text='저장할 필드 후보가 없습니다. 원본 내용과 서식을 그대로 저장합니다.';$Empty.Margin='10,18';$Empty.Foreground='#737373';[void]$Panel.Children.Add($Empty)}else{& $RenderSummary -Title '확정 후보' -Count $confirmed.Count -Color '#F1EEF8' -Foreground '#55447A';& $RenderSummary -Title '미확정 후보 (최대 10개)' -Count $unconfirmed.Count -Color '#FFF7E8' -Foreground '#C45B20';& $RenderGroups -Rows @($AllCandidates)}
        if($null -ne $ReviewActions.Reset){$ReviewActions.Reset.IsEnabled=($CandidateOverrides.Count -gt 0);$ReviewActions.Reset.Content=if($CandidateOverrides.Count){"구조 이동 되돌리기 ($($CandidateOverrides.Count))"}else{'구조 이동 되돌리기'};$ReviewActions.Reset.Background=if($CandidateOverrides.Count){'#F3F0F8'}else{'White'}};if($null -ne $ReviewActions.Confirm){$ReviewActions.Confirm.Content=if($CandidateOverrides.Count){"구조 이동 $($CandidateOverrides.Count)개 반영 후 저장"}else{'이대로 저장'};$ReviewActions.Confirm.Background=New-PurpleAccentBrush;$ReviewActions.Confirm.Foreground='White'}
        $Scroll.ScrollToTop()
    }.GetNewClosure()
    $ReviewActions.Rebuild={& $SyncChecks;$CandidateById.Clear();$DisplayByKey.Clear();$AllCandidates.Clear();$Checks.Clear();& $AddCandidates @($SourceCandidates);& $RenderAll}.GetNewClosure()
    $ReviewActions.MoveChild={param([string]$SourceId,[object]$TargetRow)
        & $SyncChecks;if(-not $CandidateById.ContainsKey($SourceId)-or $null -eq $TargetRow){return};$SourceRow=$CandidateById[$SourceId];$targetGroup=[string]$TargetRow.group_key;$targetRepresentative=[string]$TargetRow.representative;if([string]$SourceRow.group_key -eq $targetGroup){$Guide.Text='이미 이 대표필드 아래에 있는 하위필드입니다.';return}
        $sourceChild=[string]$SourceRow.child;if([string]::IsNullOrWhiteSpace($sourceChild)){$sourceChild=@([string]$SourceRow.representative -split '>')[-1].Trim()};if([string]::IsNullOrWhiteSpace($sourceChild)){throw '이동할 하위필드 이름을 확인할 수 없습니다.'}
        $collision=@($AllCandidates|Where-Object{[string]$_.group_key -eq $targetGroup -and [string]$_.child -eq $sourceChild -and [string]$_.key -ne [string]$SourceRow.key}|Select-Object -First 1);if($collision.Count){$Guide.Text="'$targetRepresentative' 아래에 '$sourceChild' 필드가 이미 있습니다. 자동 병합하지 않았습니다.";return}
        $targetField="$targetRepresentative > $sourceChild";$targetChildKey=if([string]::IsNullOrWhiteSpace([string]$SourceRow.child_key)){"moved-child:$($sourceChild.ToLowerInvariant())"}else{[string]$SourceRow.child_key};foreach($candidateId in @($SourceRow.ids)){$CandidateOverrides[[string]$candidateId]=[pscustomobject]@{field=$targetField;group_key=$targetGroup;child_key=$targetChildKey;representative=$targetRepresentative;child=$sourceChild;kind='child';target_parent=$targetRepresentative}}
        & $ReviewActions.Rebuild;$Guide.Text=("구조 이동 완료: '{0}'을(를) '{1}' 아래로 옮겼습니다. 값과 다른 필드는 합치지 않았습니다." -f $SourceRow.full_field,$targetRepresentative)
    }.GetNewClosure()
    $ReviewActions.MoveGroup={param([string]$SourceGroup,[object]$TargetRow)
        & $SyncChecks
        $sourceRows=@($AllCandidates|Where-Object{[string]$_.group_key -eq $SourceGroup})
        if($sourceRows.Count -eq 0-or $null -eq $TargetRow){return}
        $sourceRepresentative=[string]$sourceRows[0].representative
        $targetRepresentative=[string]$TargetRow.representative;$targetGroup=[string]$TargetRow.group_key
        if($SourceGroup -eq $targetGroup){$Guide.Text='이미 같은 대표필드 묶음입니다.';return}
        if($targetRepresentative.StartsWith("$sourceRepresentative > ",[System.StringComparison]::OrdinalIgnoreCase)){$Guide.Text='대표필드를 자기 하위 구조 안으로 옮길 수 없습니다.';return}
        # 전체를 먼저 검증한다. 충돌 시 일부 하위필드만 이동되는 일이 없어야 한다.
        $pending=@{}
        foreach($sourceRow in $sourceRows){
            $targetChild=[string]$sourceRow.child
            if([string]::IsNullOrWhiteSpace($targetChild)){$targetChild=@($sourceRepresentative -split '>')[-1].Trim()}
            if([string]::IsNullOrWhiteSpace($targetChild)){throw '이동할 하위필드 이름을 확인할 수 없습니다.'}
            $collision=@($AllCandidates|Where-Object{[string]$_.group_key -eq $targetGroup -and [string]$_.child -eq $targetChild}|Select-Object -First 1)
            if($collision.Count){$Guide.Text="'$targetRepresentative' 아래에 '$targetChild' 필드가 이미 있습니다. 묶음 전체를 이동하지 않았습니다. 값은 자동 병합하지 않았습니다.";return}
            $targetField="$targetRepresentative > $targetChild"
            $targetChildKey=if([string]::IsNullOrWhiteSpace([string]$sourceRow.child_key)){"moved-child:$($targetChild.ToLowerInvariant())"}else{[string]$sourceRow.child_key}
            foreach($candidateId in @($sourceRow.ids)){
                $pending[[string]$candidateId]=[pscustomobject]@{field=$targetField;group_key=$targetGroup;child_key=$targetChildKey;representative=$targetRepresentative;child=$targetChild;kind='child';target_parent=$targetRepresentative}
            }
        }
        foreach($candidateId in @($pending.Keys)){$CandidateOverrides[$candidateId]=$pending[$candidateId]}
        & $ReviewActions.Rebuild
        $Guide.Text=("이동 완료: '{0}'의 하위필드 {1}개를 '{2}' 묶음으로 옮겼습니다. 원래 묶음 이름은 경로에 넣지 않으며 필드명과 값은 유지됩니다." -f $sourceRepresentative,$sourceRows.Count,$targetRepresentative)
    }.GetNewClosure()
    if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_DRAG_SELFTEST -eq '1'){
        if($AllCandidates.Count -lt 3){throw '드래그 자체검증에 필요한 후보가 부족합니다.'};$firstRow=$AllCandidates[0];$secondRow=$AllCandidates[1];$firstId=[string]$firstRow.ids[0];$secondId=[string]$secondRow.ids[0];$eventContext=[pscustomobject]@{actions=$ReviewActions;row=$secondRow};& ($eventContext.actions.MoveChild) $firstId $eventContext.row;if($CandidateOverrides.Count -lt 1-or $CandidateOverrides.ContainsKey($secondId)-or $CandidateById[$firstId].group_key -ne $CandidateById[$secondId].group_key){throw '하위필드 구조 이동 자체검증에 실패했습니다.'};$visualTexts=New-Object System.Collections.ArrayList;$visualQueue=[System.Collections.Generic.Queue[System.Windows.DependencyObject]]::new();$visualQueue.Enqueue($Panel);while($visualQueue.Count){$visualNode=$visualQueue.Dequeue();if($visualNode -is [System.Windows.Controls.TextBlock]){[void]$visualTexts.Add([string]$visualNode.Text)};for($visualIndex=0;$visualIndex -lt [System.Windows.Media.VisualTreeHelper]::GetChildrenCount($visualNode);$visualIndex++){$visualQueue.Enqueue([System.Windows.Media.VisualTreeHelper]::GetChild($visualNode,$visualIndex))}};$visualText=$visualTexts -join "`n";if($visualText -notlike '*✓ 구조 이동 적용 중*'-or $visualText -notlike '*✓ 이동됨*'){throw '구조 이동 결과 시각 표시 자체검증에 실패했습니다.'};$CandidateOverrides.Clear();& $ReviewActions.Rebuild
        $firstRow=$AllCandidates[0];$secondRow=$AllCandidates[1];$firstId=[string]$firstRow.ids[0];$sourceChild=[string]$firstRow.child;if([string]::IsNullOrWhiteSpace($sourceChild)){$sourceChild=@([string]$firstRow.representative -split '>')[-1].Trim()};$targetRepresentative=[string]$secondRow.representative;& $ReviewActions.MoveGroup ([string]$firstRow.group_key) $secondRow;if($CandidateOverrides.Count -lt 1-or [string]$CandidateOverrides[$firstId].field -ne "$targetRepresentative > $sourceChild"-or $CandidateById[$firstId].group_key -ne $CandidateById[$secondId].group_key){throw '대표필드 하위필드 일괄 이동 자체검증에 실패했습니다.'};$CandidateOverrides.Clear();& $ReviewActions.Rebuild
        $firstId=[string]$AllCandidates[0].ids[0];$secondId=[string]$AllCandidates[1].ids[0];$thirdId=[string]$AllCandidates[2].ids[0];& $ReviewActions.MoveChild $firstId $CandidateById[$secondId];& $ReviewActions.MoveChild $firstId $CandidateById[$thirdId];if($CandidateOverrides.Count -ne 1-or $CandidateById[$firstId].group_key -ne $CandidateById[$thirdId].group_key-or $CandidateById[$firstId].key -eq $CandidateById[$thirdId].key){throw '하위필드 연속 구조 이동 자체검증에 실패했습니다.'};$script:PreviewReviewSelfTest='DRAG_REVIEW_SELFTEST_OK';return [pscustomobject]@{confirmed=$false}
    }
    & $RenderAll
    $Buttons=[System.Windows.Controls.StackPanel]::new();$Buttons.Orientation='Horizontal';$Buttons.HorizontalAlignment='Right';$Buttons.Margin='16,6,16,8';$Manual=[System.Windows.Controls.Button]::new();$Manual.Content='직접 항목 추가';$Manual.Width=110;$Manual.Margin='0,0,8,0';$ResetMove=[System.Windows.Controls.Button]::new();$ResetMove.Content='구조 이동 되돌리기';$ResetMove.Width=145;$ResetMove.Margin='0,0,8,0';$ResetMove.IsEnabled=$false;$ReviewActions.Reset=$ResetMove;$Confirm=[System.Windows.Controls.Button]::new();$Confirm.Content='이대로 저장';$Confirm.Width=175;$Confirm.Margin='0,0,8,0';$Confirm.Background='#66558F';$Confirm.Foreground='White';$ReviewActions.Confirm=$Confirm;$Cancel=[System.Windows.Controls.Button]::new();$Cancel.Content='취소';$Cancel.Width=75;[void]$Buttons.Children.Add($Manual);[void]$Buttons.Children.Add($ResetMove);[void]$Buttons.Children.Add($Confirm);[void]$Buttons.Children.Add($Cancel);[System.Windows.Controls.Grid]::SetRow($Buttons,3);[void]$Grid.Children.Add($Buttons)
    Set-OriginalFlatButton $Manual $false;Set-OriginalFlatButton $ResetMove $false;Set-OriginalFlatButton $Confirm $true;Set-OriginalFlatButton $Cancel $false
    $ReviewResult=[pscustomobject]@{Value=$null}
    $Manual.Add_Click({try{$manualResult=Open-ManualStyleCandidate $Analysis $Dialog;if($null -eq $manualResult){return};& $SyncChecks;foreach($id in @($manualResult.conflicting_candidate_ids)){$Selected[[string]$id]=$false};foreach($candidate in @($manualResult.candidates)){$candidateId=[string]$candidate.candidate_id;$found=-1;for($sourceIndex=0;$sourceIndex -lt $SourceCandidates.Count;$sourceIndex++){if([string]$SourceCandidates[$sourceIndex].candidate_id -eq $candidateId){$found=$sourceIndex;break}};if($found -ge 0){$SourceCandidates[$found]=$candidate}else{[void]$SourceCandidates.Add($candidate)};$Selected[$candidateId]=-not [bool]$manualResult.multiple_locations};& $ReviewActions.Rebuild}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $ResetMove.Add_Click({try{& $SyncChecks;$CandidateOverrides.Clear();& $ReviewActions.Rebuild;$this.IsEnabled=$false;$Guide.Text=$DefaultGuideText}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $Confirm.Add_Click({& $SyncChecks;$selectedIds=New-Object System.Collections.Generic.HashSet[string];foreach($id in @($Selected.Keys)){if([bool]$Selected[$id]){[void]$selectedIds.Add([string]$id)}};$fieldOverrides=@{};foreach($id in @($CandidateOverrides.Keys)){$move=$CandidateOverrides[$id];$fieldOverrides[[string]$id]=@{field=[string]$move.field;kind=[string]$move.kind;target_parent=[string]$move.target_parent}};$ReviewResult.Value=[pscustomobject]@{confirmed=$true;candidate_ids=@($selectedIds);candidate_field_overrides=$fieldOverrides};$Dialog.Close()}.GetNewClosure())
    $Cancel.Add_Click({$Dialog.Close()})
    [void]$Dialog.ShowDialog();return $ReviewResult.Value
}
function Open-StyleOutputValues($Preset,$OwnerWindow=$Window) {
    if(@($Preset.fields).Count -eq 0){return @{}}
    $Profile=Send-Backend @{action='user_profile_get'};if(-not $Profile.ok){throw $Profile.message}
    $Options=@{};$OptionsById=@{};$Defaults=@{};$DefaultsById=@{}
    foreach($group in @($Profile.field_groups)){
        $groupValues=@($group.values);$groupDefault=[string]$group.default
        $Options[[string]$group.name]=$groupValues;$Defaults[[string]$group.name]=$groupDefault
        foreach($alias in @($group.aliases)){
            if(-not [string]::IsNullOrWhiteSpace([string]$alias)){
                $Options[[string]$alias]=$groupValues;$Defaults[[string]$alias]=$groupDefault
            }
        }
        if($group.id){$OptionsById[[string]$group.id]=$groupValues;$DefaultsById[[string]$group.id]=$groupDefault}
    }
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='출력 값 확인';$Dialog.Width=540;$Dialog.Height=[math]::Min(620,180+(@($Preset.fields).Count*72));$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.Background='White';$Dialog.FontFamily='맑은 고딕'
    $Grid=[System.Windows.Controls.Grid]::new();$Dialog.Content=$Grid;foreach($height in @(58,46,'*',42)){$row=[System.Windows.Controls.RowDefinition]::new();if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)};[void]$Grid.RowDefinitions.Add($row)}
    $Header=[System.Windows.Controls.Border]::new();$Header.Background='#66558F';[System.Windows.Controls.Grid]::SetRow($Header,0);[void]$Grid.Children.Add($Header);$HeaderText=[System.Windows.Controls.TextBlock]::new();$HeaderText.Text='문서에 출력할 값을 확인하세요';$HeaderText.Foreground='White';$HeaderText.FontSize=17;$HeaderText.FontWeight='Bold';$HeaderText.Margin='16,15';$Header.Child=$HeaderText
    Set-OriginalSectionHeader $Header $HeaderText
    $Guide=[System.Windows.Controls.TextBlock]::new();$Guide.Text='저장된 여러 값 중 하나를 선택하거나 직접 입력할 수 있습니다.';$Guide.Margin='16,12';$Guide.Foreground='#555555';[System.Windows.Controls.Grid]::SetRow($Guide,1);[void]$Grid.Children.Add($Guide)
    $Scroll=[System.Windows.Controls.ScrollViewer]::new();$Scroll.Margin='16,4';$Panel=[System.Windows.Controls.StackPanel]::new();$Scroll.Content=$Panel;[System.Windows.Controls.Grid]::SetRow($Scroll,2);[void]$Grid.Children.Add($Scroll)
    $Editors=New-Object System.Collections.ArrayList
    foreach($field in @($Preset.fields)){
        $Row=[System.Windows.Controls.Grid]::new();$Row.Margin='0,4,0,6';$labelColumn=[System.Windows.Controls.ColumnDefinition]::new();$labelColumn.Width=130;[void]$Row.ColumnDefinitions.Add($labelColumn);[void]$Row.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new())
        $count=if([int]$field.occurrence_count -gt 1){" ($([int]$field.occurrence_count)곳)"}else{''};$Label=[System.Windows.Controls.TextBlock]::new();$Label.Text=([string]$field.name)+$count;$Label.FontWeight='SemiBold';$Label.VerticalAlignment='Center';$Label.TextWrapping='Wrap';[void]$Row.Children.Add($Label)
        $useId=[bool]($field.profile_field_id -and $OptionsById.ContainsKey([string]$field.profile_field_id));$fieldOptions=if($useId){@($OptionsById[[string]$field.profile_field_id])}else{@($Options[[string]$field.name])};$defaultValue=if($useId){[string]$DefaultsById[[string]$field.profile_field_id]}else{[string]$Defaults[[string]$field.name]}
        $Combo=[System.Windows.Controls.ComboBox]::new();$Combo.Height=32;$Combo.IsEditable=$true;$Combo.VerticalContentAlignment='Center';[System.Windows.Controls.Grid]::SetColumn($Combo,1);foreach($value in $fieldOptions){[void]$Combo.Items.Add([string]$value)};if($Combo.Items.Count){$defaultIndex=-1;for($i=0;$i -lt $Combo.Items.Count;$i++){if([string]$Combo.Items[$i] -eq $defaultValue){$defaultIndex=$i;break}};$Combo.SelectedIndex=if($defaultIndex -ge 0){$defaultIndex}else{0}};[void]$Row.Children.Add($Combo);[void]$Panel.Children.Add($Row)
        [void]$Editors.Add([pscustomobject]@{id=[string]$field.id;name=[string]$field.name;control=$Combo})
    }
    $Buttons=[System.Windows.Controls.StackPanel]::new();$Buttons.Orientation='Horizontal';$Buttons.HorizontalAlignment='Right';$Buttons.Margin='16,6,16,8';$Output=[System.Windows.Controls.Button]::new();$Output.Content='새 문서로 출력';$Output.Width=120;$Output.Margin='0,0,8,0';$Output.Background='#66558F';$Output.Foreground='White';$Cancel=[System.Windows.Controls.Button]::new();$Cancel.Content='취소';$Cancel.Width=75;[void]$Buttons.Children.Add($Output);[void]$Buttons.Children.Add($Cancel);[System.Windows.Controls.Grid]::SetRow($Buttons,3);[void]$Grid.Children.Add($Buttons)
    Set-OriginalFlatButton $Output $true;Set-OriginalFlatButton $Cancel $false
    $script:StyleOutputResult=$null
    $Output.Add_Click({$values=@{};foreach($editor in $Editors){$text=[string]$editor.control.Text;if([string]::IsNullOrWhiteSpace($text)){[System.Windows.MessageBox]::Show("$($editor.name) 값을 선택하거나 입력하세요.",'출력 값 확인')|Out-Null;return};$values[$editor.id]=$text.Trim()};$script:StyleOutputResult=$values;$Dialog.Close()})
    $Cancel.Add_Click({$Dialog.Close()});[void]$Dialog.ShowDialog();$result=$script:StyleOutputResult;$script:StyleOutputResult=$null;return $result
}
function Open-StylePresetManager($OwnerWindow=$Window) {
    if(Test-WorkspaceWindow 'presets'){return}
    $Dialog = [System.Windows.Window]::new()
    $Dialog.Title = '서식 프리셋'
    $Dialog.Width = 430
    $Dialog.Height = 560
    $Dialog.WindowStartupLocation = 'CenterOwner'
    $Dialog.Owner = $OwnerWindow
    $Dialog.ResizeMode = 'NoResize'
    $Dialog.FontFamily = '맑은 고딕'

    $Grid = [System.Windows.Controls.Grid]::new()
    foreach($height in @(68,62,36,40,'*',42,34)){
        $row=[System.Windows.Controls.RowDefinition]::new()
        if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)}
        [void]$Grid.RowDefinitions.Add($row)
    }
    $Dialog.Content = $Grid

    $GuidePanel=[System.Windows.Controls.StackPanel]::new();$GuidePanel.Margin='12,7,12,4'
    $GuideTitle=[System.Windows.Controls.TextBlock]::new();$GuideTitle.Text='서식 프리셋';$GuideTitle.FontSize=16;$GuideTitle.FontWeight='Bold';$GuideTitle.Foreground='#262626';[void]$GuidePanel.Children.Add($GuideTitle)
    $Guide=[System.Windows.Controls.TextBlock]::new();$Guide.Text='저장값이 없으면 선택 영역 전체를 보존하고, 저장값이 있으면 일치한 값만 입력 필드로 분류합니다.';$Guide.Margin='0,4,0,0';$Guide.TextWrapping='Wrap';$Guide.Foreground='#737373';$Guide.FontSize=10;[void]$GuidePanel.Children.Add($Guide)
    [System.Windows.Controls.Grid]::SetRow($GuidePanel,0);[void]$Grid.Children.Add($GuidePanel)

    $SelectionPanel=[System.Windows.Controls.Border]::new();$SelectionPanel.Margin='12,4,12,5';$SelectionPanel.Padding='10,6';$SelectionPanel.BorderThickness=1;$SelectionPanel.CornerRadius=10
    $SelectionGrid=[System.Windows.Controls.Grid]::new();$selectionButtonColumn=[System.Windows.Controls.ColumnDefinition]::new();$selectionButtonColumn.Width=145;[void]$SelectionGrid.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new());[void]$SelectionGrid.ColumnDefinitions.Add($selectionButtonColumn);$SelectionPanel.Child=$SelectionGrid
    $SelectionStatus=[System.Windows.Controls.TextBlock]::new();$SelectionStatus.Text='한글 문서와 선택 영역을 확인하는 중입니다.';$SelectionStatus.TextWrapping='Wrap';$SelectionStatus.VerticalAlignment='Center';$SelectionStatus.Foreground='#55447A';[void]$SelectionGrid.Children.Add($SelectionStatus)
    $ChooseSelection=[System.Windows.Controls.Button]::new();$ChooseSelection.Content='한글에서 영역 선택';$ChooseSelection.Width=135;$ChooseSelection.Height=32;$ChooseSelection.Margin='8,0,0,0';[System.Windows.Controls.Grid]::SetColumn($ChooseSelection,1);[void]$SelectionGrid.Children.Add($ChooseSelection)
    [System.Windows.Controls.Grid]::SetRow($SelectionPanel,1);[void]$Grid.Children.Add($SelectionPanel)

    $NamePanel = [System.Windows.Controls.DockPanel]::new(); $NamePanel.Margin='12,2,12,4'
    $Capture = [System.Windows.Controls.Button]::new(); $Capture.Content='프리셋 저장'; $Capture.Width=110; $Capture.Margin='8,0,0,0';$Capture.IsEnabled=$false
    [System.Windows.Controls.DockPanel]::SetDock($Capture,'Right'); [void]$NamePanel.Children.Add($Capture)
    $Name = [System.Windows.Controls.TextBox]::new(); $Name.VerticalContentAlignment='Center'; $Name.ToolTip='프리셋 이름';$Name.BorderBrush='#DBDBDB';$Name.BorderThickness=1;$Name.Padding='7,0'
    [void]$NamePanel.Children.Add($Name); [System.Windows.Controls.Grid]::SetRow($NamePanel,2); [void]$Grid.Children.Add($NamePanel)

    $TableActions = [System.Windows.Controls.StackPanel]::new(); $TableActions.Orientation='Horizontal'; $TableActions.Margin='12,3,12,3'
    $AddRow = [System.Windows.Controls.Button]::new(); $AddRow.Content='아래 행 추가'; $AddRow.Width=110; $AddRow.Margin='0,0,8,0'
    $AddLeftColumn = [System.Windows.Controls.Button]::new(); $AddLeftColumn.Content='왼쪽 열 추가'; $AddLeftColumn.Width=110; $AddLeftColumn.Margin='0,0,8,0'
    $AddRightColumn = [System.Windows.Controls.Button]::new(); $AddRightColumn.Content='오른쪽 열 추가'; $AddRightColumn.Width=110
    [void]$TableActions.Children.Add($AddRow); [void]$TableActions.Children.Add($AddLeftColumn); [void]$TableActions.Children.Add($AddRightColumn)
    [System.Windows.Controls.Grid]::SetRow($TableActions,3); [void]$Grid.Children.Add($TableActions)

    $List = [System.Windows.Controls.ListBox]::new(); $List.Margin='12,4,12,6'; $List.DisplayMemberPath='display';$List.Background='#FAFAFA';$List.BorderBrush='#DBDBDB'
    [System.Windows.Controls.Grid]::SetRow($List,4); [void]$Grid.Children.Add($List)
    $EmptyPresetState=[System.Windows.Controls.TextBlock]::new();$EmptyPresetState.Text="저장된 프리셋이 없습니다.`n선택 영역을 저장하면 여기에 표시됩니다.";$EmptyPresetState.HorizontalAlignment='Center';$EmptyPresetState.VerticalAlignment='Center';$EmptyPresetState.TextAlignment='Center';$EmptyPresetState.Foreground='#8E8E8E';$EmptyPresetState.FontSize=11;$EmptyPresetState.IsHitTestVisible=$false;[System.Windows.Controls.Grid]::SetRow($EmptyPresetState,4);[void]$Grid.Children.Add($EmptyPresetState)

    $Actions = [System.Windows.Controls.StackPanel]::new(); $Actions.Orientation='Horizontal'; $Actions.HorizontalAlignment='Right'; $Actions.Margin='12,3,12,3'
    $Apply = [System.Windows.Controls.Button]::new(); $Apply.Content='새 문서로 복제'; $Apply.Width=120; $Apply.Margin='0,0,8,0'
    $Delete = [System.Windows.Controls.Button]::new(); $Delete.Content='삭제'; $Delete.Width=70; $Delete.Margin='0,0,8,0'
    $Close = [System.Windows.Controls.Button]::new(); $Close.Content='닫기'; $Close.Width=70
    [void]$Actions.Children.Add($Apply); [void]$Actions.Children.Add($Delete); [void]$Actions.Children.Add($Close)
    [System.Windows.Controls.Grid]::SetRow($Actions,5); [void]$Grid.Children.Add($Actions)

    $LocalStatus = [System.Windows.Controls.TextBlock]::new(); $LocalStatus.Margin='12,4,12,6'; $LocalStatus.Foreground='#555555'; $LocalStatus.TextTrimming='CharacterEllipsis'
    [System.Windows.Controls.Grid]::SetRow($LocalStatus,6); [void]$Grid.Children.Add($LocalStatus)
    foreach($OriginalButton in @($ChooseSelection,$Capture,$AddRow,$AddLeftColumn,$AddRightColumn,$Apply,$Delete,$Close)){Set-OriginalFlatButton $OriginalButton ($OriginalButton -in @($Capture,$Apply))}
    $SelectionPanel.Background='#F8F6FB';$SelectionPanel.BorderBrush='#D9D2E7';$SelectionPanel.CornerRadius=10

    $RefreshSelectionState={
        param([bool]$Probe=$false)
        $state=Send-Backend @{action='style_preset_selection_status';probe=$Probe}
        if(-not $state.ok){throw $state.message}
        $SelectionStatus.Text=$state.message
        # 선택이 확인된 경우에만 저장 버튼을 열고, 클릭 순간에도 아래 저장
        # 핸들러가 한 번 더 live probe하여 오래된 캐시 사용을 막는다.
        $Capture.IsEnabled=[bool]($state.hwp_running -and $state.selection_ready)
        if(-not $state.managed_document_ready){
            $SelectionPanel.Background='#FAFAFA';$SelectionPanel.BorderBrush='#DBDBDB';$ChooseSelection.Content='한글 문서 열기';$ChooseSelection.IsEnabled=$true
        }elseif($state.selection_ready){
            $SelectionPanel.Background='#F3F0F8';$SelectionPanel.BorderBrush='#CFC6E1';$ChooseSelection.Content='영역 다시 선택';$ChooseSelection.IsEnabled=$true
        }else{
            $SelectionPanel.Background='#F8F6FB';$SelectionPanel.BorderBrush='#D9D2E7';$ChooseSelection.Content='한글에서 영역 선택';$ChooseSelection.IsEnabled=$true
        }
    }.GetNewClosure()

    $ChooseSelection.Add_Click({
        try{
            $state=Send-Backend @{action='style_preset_selection_status';probe=$false}
            if(-not $state.managed_document_ready){
                Open-HwpDocument
                $state=Send-Backend @{action='style_preset_selection_status';probe=$false}
                if(-not $state.managed_document_ready){$SelectionStatus.Text=$state.message;return}
            }
            [void](Send-Backend @{action='style_preset_selection_clear'})
            $SelectionStatus.Text='한글에서 저장할 영역을 마우스로 드래그하세요.'
            $script:SelectionReturnWindow=$Dialog
            if(-not (Activate-SelectionHwp)){$SelectionStatus.Text='관리 중인 한글 창을 찾지 못했습니다. 한글 문서를 다시 불러오세요.'}
        }catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())

    $RefreshStylePresetList = {
        $response=Send-Backend @{action='style_preset_list'}
        if(-not $response.ok){throw $response.message}
        $List.Items.Clear()
        foreach($preset in @($response.presets)){
            $scopeLabel = if($preset.scope -eq 'selection_page'){'선택 영역+쪽 서식'}elseif($preset.scope -eq 'document'){'이전 전체 문서'}else{'기존 선택 영역'}
            $contentLabel = if($preset.content_policy -eq 'original'){'원본 전체 유지'}elseif($preset.content_policy -eq 'registered_fields'){"등록 필드 $($preset.field_count)개 분류"}else{"기존 민감정보 $($preset.field_count)개 치환"}
            $preset | Add-Member -NotePropertyName display -NotePropertyValue ("{0} · {1} · {2}" -f $preset.name,$scopeLabel,$contentLabel) -Force
            [void]$List.Items.Add($preset)
        }
        $EmptyPresetState.Visibility=if($List.Items.Count -eq 0){'Visible'}else{'Collapsed'}
        $LocalStatus.Text=$response.message
    }.GetNewClosure()
    $Capture.Add_Click({
        try{
            $state=Send-Backend @{action='style_preset_selection_status';probe=$true}
            if(-not $state.hwp_running){& $RefreshSelectionState $false;$LocalStatus.Text='먼저 한글 문서를 여세요.';return}
            $presetName=$Name.Text.Trim()
            if(-not $presetName){$presetName='서식 '+(Get-Date -Format 'yyyy-MM-dd HHmm')}
            # 상태 조회 결과만 믿고 중단하지 않고, 예전에 잘 되던 방식대로 실제
            # 저장 분석 호출에서 현재 선택 블록을 직접 다시 읽는다.
            $analysis=Send-Backend @{action='style_preset_analyze'}
            if(-not $analysis.ok){throw $analysis.message}
            if($analysis.no_registered_fields){
                # 사용자 값이 하나도 없으면 추측 후보를 자동 필드로 만들지 않고
                # 선택 영역의 내용과 서식을 그대로 프리셋으로 보존한다.
                $response=Send-Backend @{action='style_preset_capture';name=$presetName;draft_id=$analysis.draft_id;selected_candidate_ids=@()}
            }else{
                $review=Open-StyleCaptureReview $analysis $Dialog
                if($null -eq $review -or -not $review.confirmed){$LocalStatus.Text='서식 저장을 취소했습니다.';return}
                $response=Send-Backend @{action='style_preset_capture';name=$presetName;draft_id=$analysis.draft_id;selected_candidate_ids=@($review.candidate_ids);candidate_field_overrides=$review.candidate_field_overrides}
            }
            if(-not $response.ok){throw $response.message}
            $Name.Clear(); & $RefreshStylePresetList; $LocalStatus.Text=$response.message; $Status.Text=$response.message
        }catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $AddRow.Add_Click({try{$response=Send-Backend @{action='table_edit';operation='insert_lower_row'};if(-not $response.ok){throw $response.message};$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $AddLeftColumn.Add_Click({try{$response=Send-Backend @{action='table_edit';operation='insert_left_column'};if(-not $response.ok){throw $response.message};$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $AddRightColumn.Add_Click({try{$response=Send-Backend @{action='table_edit';operation='insert_right_column'};if(-not $response.ok){throw $response.message};$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $Apply.Add_Click({
        if(-not $List.SelectedItem){$LocalStatus.Text='출력할 프리셋을 선택하세요.';return}
        try{
            $values=Open-StyleOutputValues $List.SelectedItem $Dialog
            if($null -eq $values){$LocalStatus.Text='출력을 취소했습니다.';return}
            $response=Send-Backend @{action='style_preset_apply';preset_id=$List.SelectedItem.id;values=$values}
            if(-not $response.ok){throw $response.message}
            $LocalStatus.Text=$response.message; $Status.Text=$response.message
        }catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $List.Add_MouseDoubleClick({if($List.SelectedItem){$Apply.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Button]::ClickEvent))}}.GetNewClosure())
    $Delete.Add_Click({
        if(-not $List.SelectedItem){$LocalStatus.Text='삭제할 프리셋을 선택하세요.';return}
        try{
            $response=Send-Backend @{action='style_preset_delete';preset_id=$List.SelectedItem.id}
            if(-not $response.ok){throw $response.message}
            & $RefreshStylePresetList; $LocalStatus.Text=$response.message
        }catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $Close.Add_Click({$Dialog.Close()}.GetNewClosure())
    # 마우스 후킹 결과만 기다리지 않고 한글 COM의 saveblock을 주기적으로 직접
    # 확인한다. 드래그가 끝난 뒤에는 별도 버튼 없이 선택 상태가 바로 갱신된다.
    $SelectionStateTimer=[System.Windows.Threading.DispatcherTimer]::new();$SelectionStateTimer.Interval=[TimeSpan]::FromMilliseconds(700);$SelectionStateTimer.Add_Tick([GovOfficePollGuard]::Wrap({try{if(-not [GovOfficeSelectionMouse]::LeftButtonDown()){& $RefreshSelectionState $true}}catch{}}.GetNewClosure()));$SelectionStateTimer.Start()
    $Dialog.Add_Closed({$SelectionStateTimer.Stop();if($script:SelectionReturnWindow -eq $Dialog){$script:SelectionReturnWindow=$null}}.GetNewClosure())
    try{& $RefreshSelectionState $true;& $RefreshStylePresetList}catch{Show-Error $_.Exception.Message}
    Show-WorkspaceWindow $Dialog 'presets'
}
function Get-GeometrySize($Geometry, [double]$DefaultWidth, [double]$DefaultHeight) {
    $Width=$DefaultWidth;$Height=$DefaultHeight
    if($Geometry -is [string]){
        if($Geometry -match '^\s*(?<width>\d+(?:\.\d+)?)x(?<height>\d+(?:\.\d+)?)'){
            $Width=[double]$Matches.width;$Height=[double]$Matches.height
        }
    }elseif($null -ne $Geometry){
        if($Geometry.PSObject.Properties['width']){$Width=[double]$Geometry.width}
        if($Geometry.PSObject.Properties['height']){$Height=[double]$Geometry.height}
    }
    return [pscustomobject]@{Width=$Width;Height=$Height}
}
function Open-Institution([string]$InstitutionId) {
    if(Test-WorkspaceWindow "institution:$InstitutionId"){return}
    $Property=$Layout.institutions.PSObject.Properties[$InstitutionId]
    if($null -eq $Property){Show-Error "기관 정보를 찾을 수 없습니다: $InstitutionId";return}
    $Institution=$Property.Value
    $LayoutSpec=$Institution.layout
    $Pages=@();if($null -ne $LayoutSpec){$Pages=@($LayoutSpec.pages)}
    $HasPagedLayout=$Pages.Count -gt 0
    if($HasPagedLayout){
        $BaseButtons=@($LayoutSpec.base_buttons|Where-Object{$_.enabled -ne $false})
        $PageControls=@($LayoutSpec.page_controls|Where-Object{$_.enabled -ne $false})
        $DefaultWidth=300.0;$DefaultHeight=360.0
        if($Institution.window){$DefaultWidth=[double]$Institution.window.width;$DefaultHeight=[double]$Institution.window.height}
        $BaseGeometry=Get-GeometrySize $LayoutSpec.geometry $DefaultWidth $DefaultHeight
        $FixedWidth=50.0;$FixedHeight=50.0
        foreach($ButtonItem in @($BaseButtons)+@($PageControls)){
            $FixedWidth=[math]::Max($FixedWidth,[double]$ButtonItem.x+[double]$ButtonItem.width)
            $FixedHeight=[math]::Max($FixedHeight,[double]$ButtonItem.y+[double]$ButtonItem.height)
        }
        $BaseWidth=[math]::Max($FixedWidth,[double]$BaseGeometry.Width);$BaseHeight=[math]::Max($FixedHeight,[double]$BaseGeometry.Height)

        $Dialog=[System.Windows.Window]::new();$Dialog.Title="범정부오피스 · $($Institution.name)";$Dialog.Topmost=$false;$Dialog.Owner=$Window;$Dialog.WindowStyle='None';$Dialog.ResizeMode='NoResize';$Dialog.Background=[System.Windows.Media.Brushes]::White;$Dialog.UseLayoutRounding=$true;$Dialog.SnapsToDevicePixels=$true
        $Canvas=[System.Windows.Controls.Canvas]::new();$Canvas.Background=[System.Windows.Media.Brushes]::White;$Canvas.ClipToBounds=$true
        $Viewbox=[System.Windows.Controls.Viewbox]::new();$Viewbox.Stretch='Uniform';$Viewbox.StretchDirection='DownOnly';$Viewbox.Child=$Canvas;$Dialog.Content=$Viewbox
        $Close=New-ImageButton $Canvas ($BaseWidth-50) 0 50 50 '상단바\닫기.PNG' {$Dialog.Close()}.GetNewClosure() '닫기' $true
        [System.Windows.Controls.Panel]::SetZIndex($Close,100000)
        $Drag=[System.Windows.Controls.Border]::new();$Drag.Height=50;$Drag.Background=[System.Windows.Media.Brushes]::Transparent;[System.Windows.Controls.Canvas]::SetLeft($Drag,0);[System.Windows.Controls.Canvas]::SetTop($Drag,0);$Drag.Add_MouseLeftButtonDown({$Dialog.DragMove()}.GetNewClosure());$Canvas.Children.Add($Drag)|Out-Null
        [System.Windows.Controls.Panel]::SetZIndex($Drag,-100)

        $ApplyDialogSize={
            param([double]$LogicalWidth,[double]$LogicalHeight)
            $Scale=Get-FitScale $LogicalWidth $LogicalHeight 12
            $Canvas.Width=$LogicalWidth;$Canvas.Height=$LogicalHeight
            $Dialog.Width=$LogicalWidth*$Scale;$Dialog.Height=$LogicalHeight*$Scale
            [System.Windows.Controls.Canvas]::SetLeft($Close,$LogicalWidth-50)
            $Drag.Width=[math]::Max(0,$LogicalWidth-50)
            $Area=[System.Windows.SystemParameters]::WorkArea
            $Dialog.Left=[math]::Max($Area.Left,$Area.Right-$Dialog.Width-12)
            $Dialog.Top=[math]::Max($Area.Top,[math]::Min($Area.Top+100,$Area.Bottom-$Dialog.Height))
        }.GetNewClosure()
        & $ApplyDialogSize $BaseWidth $BaseHeight

        foreach($ButtonItem in $BaseButtons){
            $Captured=$ButtonItem;$BaseButton=New-ImageButton $Canvas $ButtonItem.x $ButtonItem.y $ButtonItem.width $ButtonItem.height $ButtonItem.icon {Invoke-LayoutButton $Captured}.GetNewClosure() $ButtonItem.name $true
            [System.Windows.Controls.Panel]::SetZIndex($BaseButton,10)
        }

        $PageMap=@{};foreach($Page in $Pages){$PageMap[[string]$Page.id]=$Page}
        $PageControlGeometry=@{}
        $PageControlCollapsedGeometry=@{}
        foreach($ControlItem in $PageControls){
            $ControlPageId=[string]$ControlItem.page_id
            if($ControlPageId -and $ControlItem.PSObject.Properties['geometry']){$PageControlGeometry[$ControlPageId]=$ControlItem.geometry}
            elseif($ControlPageId -and $ControlItem.PSObject.Properties['expanded_window']){$PageControlGeometry[$ControlPageId]=$ControlItem.expanded_window}
            if($ControlPageId -and $ControlItem.PSObject.Properties['collapsed_window']){$PageControlCollapsedGeometry[$ControlPageId]=$ControlItem.collapsed_window}
        }
        $PageState=@{CurrentId=$null;Canvas=$null}
        $PageControlViews=[System.Collections.ArrayList]::new()
        $ShowPage={
            param([string]$PageId)
            if($PageState.Canvas){[void]$Canvas.Children.Remove($PageState.Canvas);$PageState.Canvas=$null}
            if($PageState.CurrentId -eq $PageId){
                $PageState.CurrentId=$null
                foreach($View in $PageControlViews){$View.Button.Opacity=1}
                $CollapsedWidth=$BaseWidth;$CollapsedHeight=$BaseHeight
                if($PageControlCollapsedGeometry.ContainsKey($PageId)){
                    $CollapsedGeometry=Get-GeometrySize $PageControlCollapsedGeometry[$PageId] $BaseWidth $BaseHeight
                    $CollapsedWidth=[math]::Max($FixedWidth,[double]$CollapsedGeometry.Width)
                    $CollapsedHeight=[math]::Max($FixedHeight,[double]$CollapsedGeometry.Height)
                }
                & $ApplyDialogSize $CollapsedWidth $CollapsedHeight
                $Status.Text="$($Institution.name) · 페이지 접힘"
                return
            }
            if(-not $PageMap.ContainsKey($PageId)){Show-Error "기관 페이지 정보를 찾을 수 없습니다: $PageId";return}
            $Page=$PageMap[$PageId];$Frame=$Page.frame
            $FrameX=0.0;$FrameY=0.0;$FrameWidth=1.0;$FrameHeight=1.0
            if($null -ne $Frame){
                if($Frame.PSObject.Properties['x']){$FrameX=[double]$Frame.x}
                if($Frame.PSObject.Properties['y']){$FrameY=[double]$Frame.y}
                if($Frame.PSObject.Properties['width']){$FrameWidth=[math]::Max(1,[double]$Frame.width)}
                if($Frame.PSObject.Properties['height']){$FrameHeight=[math]::Max(1,[double]$Frame.height)}
            }
            $PageButtons=@($Page.buttons|Where-Object{$_.enabled -ne $false})
            foreach($ButtonItem in $PageButtons){
                $FrameWidth=[math]::Max($FrameWidth,[double]$ButtonItem.x+[double]$ButtonItem.width)
                $FrameHeight=[math]::Max($FrameHeight,[double]$ButtonItem.y+[double]$ButtonItem.height)
            }
            $PageCanvas=[System.Windows.Controls.Canvas]::new();$PageCanvas.Width=$FrameWidth;$PageCanvas.Height=$FrameHeight;$PageCanvas.Background=[System.Windows.Media.Brushes]::White;$PageCanvas.ClipToBounds=$true
            [System.Windows.Controls.Canvas]::SetLeft($PageCanvas,$FrameX);[System.Windows.Controls.Canvas]::SetTop($PageCanvas,$FrameY);[System.Windows.Controls.Panel]::SetZIndex($PageCanvas,100);[void]$Canvas.Children.Add($PageCanvas)
            foreach($ButtonItem in $PageButtons){
                $Captured=$ButtonItem;[void](New-ImageButton $PageCanvas $ButtonItem.x $ButtonItem.y $ButtonItem.width $ButtonItem.height $ButtonItem.icon {Invoke-LayoutButton $Captured}.GetNewClosure() $ButtonItem.name $true)
            }
            $GeometryValue=$Page.geometry
            if($null -eq $GeometryValue -and $Page.PSObject.Properties['expanded_window']){$GeometryValue=$Page.expanded_window}
            if($null -eq $GeometryValue -and $PageControlGeometry.ContainsKey($PageId)){$GeometryValue=$PageControlGeometry[$PageId]}
            $PageGeometry=Get-GeometrySize $GeometryValue $BaseWidth $BaseHeight
            $TargetWidth=[math]::Max($BaseWidth,[math]::Max([double]$PageGeometry.Width,$FrameX+$FrameWidth))
            $TargetHeight=[math]::Max($BaseHeight,[math]::Max([double]$PageGeometry.Height,$FrameY+$FrameHeight))
            $PageState.CurrentId=$PageId;$PageState.Canvas=$PageCanvas
            foreach($View in $PageControlViews){$View.Button.Opacity=if($View.PageId -eq $PageId){0.65}else{1}}
            & $ApplyDialogSize $TargetWidth $TargetHeight
            $PageName=if($Page.name){$Page.name}else{$PageId};$Status.Text="$($Institution.name) · $PageName"
        }.GetNewClosure()

        foreach($ControlItem in $PageControls){
            $CapturedPageId=[string]$ControlItem.page_id
            if(-not $CapturedPageId){continue}
            $ControlButton=New-ImageButton $Canvas $ControlItem.x $ControlItem.y $ControlItem.width $ControlItem.height $ControlItem.icon {& $ShowPage $CapturedPageId}.GetNewClosure() $ControlItem.name $true
            [System.Windows.Controls.Panel]::SetZIndex($ControlButton,1000)
            [void]$PageControlViews.Add([pscustomobject]@{PageId=$CapturedPageId;Button=$ControlButton})
        }
        [System.Windows.Controls.Panel]::SetZIndex($Close,100000)
        $Status.Text="$($Institution.name) · 기본 버튼 $($BaseButtons.Count)개 · 페이지 $($Pages.Count)개"
        Add-InstitutionFavorites $Dialog $InstitutionId;Show-WorkspaceWindow $Dialog "institution:$InstitutionId";return
    }

    $LayoutButtons=@($Institution.layout_buttons|Where-Object enabled)
    if($Institution.window -and $LayoutButtons.Count){
        $NominalWidth=[double]$Institution.window.width;$NominalHeight=[double]$Institution.window.height
        foreach($ButtonItem in $LayoutButtons){$NominalWidth=[math]::Max($NominalWidth,[double]$ButtonItem.x+[double]$ButtonItem.width);$NominalHeight=[math]::Max($NominalHeight,[double]$ButtonItem.y+[double]$ButtonItem.height)}
        $DialogScale=Get-FitScale $NominalWidth $NominalHeight 12
        $Dialog=[System.Windows.Window]::new();$Dialog.Title="범정부오피스 · $($Institution.name)";$Dialog.Width=$NominalWidth*$DialogScale;$Dialog.Height=$NominalHeight*$DialogScale;$Dialog.Topmost=$false;$Dialog.Owner=$Window;$Dialog.WindowStyle='None';$Dialog.ResizeMode='NoResize';$Dialog.Background=[System.Windows.Media.Brushes]::White;$Dialog.UseLayoutRounding=$true;$Dialog.SnapsToDevicePixels=$true
        $Area=[System.Windows.SystemParameters]::WorkArea;$Dialog.Left=[math]::Max($Area.Left,$Area.Right-$Dialog.Width-12);$Dialog.Top=[math]::Max($Area.Top,[math]::Min($Area.Top+100,$Area.Bottom-$Dialog.Height))
        $Canvas=[System.Windows.Controls.Canvas]::new();$Canvas.Width=$NominalWidth;$Canvas.Height=$NominalHeight;$Canvas.Background=[System.Windows.Media.Brushes]::White;$Canvas.ClipToBounds=$true
        $Viewbox=[System.Windows.Controls.Viewbox]::new();$Viewbox.Stretch='Uniform';$Viewbox.StretchDirection='DownOnly';$Viewbox.Child=$Canvas;$Dialog.Content=$Viewbox
        $Close=New-ImageButton $Canvas ($NominalWidth-50) 0 50 50 '상단바\닫기.PNG' {$Dialog.Close()}.GetNewClosure() '닫기' $true
        [System.Windows.Controls.Panel]::SetZIndex($Close,100000)
        $Drag=[System.Windows.Controls.Border]::new();$Drag.Width=$NominalWidth-50;$Drag.Height=50;$Drag.Background=[System.Windows.Media.Brushes]::Transparent;[System.Windows.Controls.Canvas]::SetLeft($Drag,0);[System.Windows.Controls.Canvas]::SetTop($Drag,0);$Drag.Add_MouseLeftButtonDown({$Dialog.DragMove()}.GetNewClosure());$Canvas.Children.Add($Drag)|Out-Null
        [System.Windows.Controls.Panel]::SetZIndex($Drag,-100)
        foreach($ButtonItem in $LayoutButtons){$Captured=$ButtonItem;[void](New-ImageButton $Canvas $ButtonItem.x $ButtonItem.y $ButtonItem.width $ButtonItem.height $ButtonItem.icon {Invoke-LayoutButton $Captured}.GetNewClosure() $ButtonItem.name $true)}
        $Status.Text="$($Institution.name) · 원본 기관 버튼 $($LayoutButtons.Count)개"
        Add-InstitutionFavorites $Dialog $InstitutionId;Show-WorkspaceWindow $Dialog "institution:$InstitutionId";return
    }
    if(@($Institution.functions).Count -eq 0){
        $CustomFeatures=@($Institution.custom_features)
        $NominalHeight=if($CustomFeatures.Count){220+($CustomFeatures.Count*58)}else{220}
        $DialogScale=Get-FitScale 300 $NominalHeight 12
        $Dialog=[System.Windows.Window]::new();$Dialog.Title="범정부오피스 · $($Institution.name)";$Dialog.Width=300*$DialogScale;$Dialog.Height=$NominalHeight*$DialogScale;$Dialog.Topmost=$false;$Dialog.Owner=$Window;$Dialog.WindowStyle='None';$Dialog.ResizeMode='NoResize';$Dialog.Background=[System.Windows.Media.Brushes]::White;$Dialog.UseLayoutRounding=$true;$Dialog.SnapsToDevicePixels=$true
        $Area=[System.Windows.SystemParameters]::WorkArea;$Dialog.Left=[math]::Max($Area.Left,$Area.Right-$Dialog.Width-12);$Dialog.Top=[math]::Max($Area.Top,[math]::Min($Area.Top+100,$Area.Bottom-$Dialog.Height))
        $Canvas=[System.Windows.Controls.Canvas]::new();$Canvas.Width=300;$Canvas.Height=$NominalHeight;$Canvas.Background=[System.Windows.Media.Brushes]::White;$Viewbox=[System.Windows.Controls.Viewbox]::new();$Viewbox.Stretch='Uniform';$Viewbox.StretchDirection='DownOnly';$Viewbox.Child=$Canvas;$Dialog.Content=$Viewbox
        $CloseButton=New-ImageButton $Canvas 250 0 50 50 '상단바\닫기.PNG' {$Dialog.Close()}.GetNewClosure() '닫기' $true
        $Drag=[System.Windows.Controls.Border]::new();$Drag.Width=250;$Drag.Height=50;$Drag.Background=[System.Windows.Media.Brushes]::Transparent;[System.Windows.Controls.Canvas]::SetLeft($Drag,0);[System.Windows.Controls.Canvas]::SetTop($Drag,0);$Drag.Add_MouseLeftButtonDown({$Dialog.DragMove()}.GetNewClosure());[void]$Canvas.Children.Add($Drag)
        $InstitutionAvatar=[System.Windows.Controls.Border]::new();$InstitutionAvatar.Width=44;$InstitutionAvatar.Height=44;$InstitutionAvatar.CornerRadius=22;$InstitutionAvatar.Background=New-PurpleAccentBrush;[System.Windows.Controls.Canvas]::SetLeft($InstitutionAvatar,12);[System.Windows.Controls.Canvas]::SetTop($InstitutionAvatar,55);[void]$Canvas.Children.Add($InstitutionAvatar)
        $InstitutionAvatarText=[System.Windows.Controls.TextBlock]::new();$InstitutionAvatarText.Text='S';$InstitutionAvatarText.Foreground='White';$InstitutionAvatarText.FontSize=18;$InstitutionAvatarText.FontWeight='Bold';$InstitutionAvatarText.HorizontalAlignment='Center';$InstitutionAvatarText.VerticalAlignment='Center';$InstitutionAvatar.Child=$InstitutionAvatarText
        $Title=[System.Windows.Controls.TextBlock]::new();$Title.Text=$Institution.name;$Title.Width=226;$Title.FontFamily='맑은 고딕';$Title.FontSize=16;$Title.FontWeight='Bold';$Title.Foreground='#262626';$Title.TextTrimming='CharacterEllipsis';[System.Windows.Controls.Canvas]::SetLeft($Title,64);[System.Windows.Controls.Canvas]::SetTop($Title,59);[void]$Canvas.Children.Add($Title)
        $Message=[System.Windows.Controls.TextBlock]::new();$Message.Text=if($CustomFeatures.Count){'기관 전용 기능'}else{"기관 화면이 연결되었습니다.`n전용 기능은 복구·검증 후 이 화면에 추가됩니다."};$Message.Width=226;$Message.FontFamily='맑은 고딕';$Message.FontSize=10;$Message.Foreground='#737373';$Message.TextWrapping='Wrap';[System.Windows.Controls.Canvas]::SetLeft($Message,64);[System.Windows.Controls.Canvas]::SetTop($Message,84);[void]$Canvas.Children.Add($Message)
        $Divider=[System.Windows.Controls.Border]::new();$Divider.Width=276;$Divider.Height=2;$Divider.CornerRadius=1;$Divider.Background=New-PurpleAccentBrush;[System.Windows.Controls.Canvas]::SetLeft($Divider,12);[System.Windows.Controls.Canvas]::SetTop($Divider,116);[void]$Canvas.Children.Add($Divider)
        $FeatureY=132
        foreach($Feature in $CustomFeatures){
            $CapturedFeature=$Feature
            $FeatureButton=New-ImageButton $Canvas 10 $FeatureY 280 48 '' {
                if($CapturedFeature.action -eq 'style_preset_manager'){Open-StylePresetManager $Dialog;return}
                if($CapturedFeature.action -eq 'document_authoring'){Open-DocumentAuthoring $Dialog;return}
                if($CapturedFeature.action -eq 'climate_plan_generate'){
                    try {
                        $Status.Text='기후부 연구계획서 예시 생성 중… 원본은 변경하지 않습니다.'
                        $Dialog.IsEnabled=$false
                        $Reply=Send-Backend @{action='climate_plan_generate'}
                        if(-not $Reply.ok){throw $Reply.message}
                        $Status.Text="예시 생성 완료 · $($Reply.result.pages)쪽 · 실제 제출 전 검토 필요"
                        Start-Process -FilePath $Reply.result.hwp_path | Out-Null
                        Start-Process -FilePath 'explorer.exe' -ArgumentList ('"'+$Reply.result.output_dir+'"') | Out-Null
                    } catch {Show-Error $_.Exception.Message}
                    finally {$Dialog.IsEnabled=$true}
                    return
                }
                Show-Error "지원하지 않는 기관 기능입니다: $($CapturedFeature.action)"
            }.GetNewClosure() $Feature.name $true
            $FeatureButton.FontSize=12;$FeatureButton.Height=48;$FeatureY+=58
        }
        $Footer=[System.Windows.Controls.TextBlock]::new();$Footer.Text='범정부오피스';$Footer.Width=276;$Footer.HorizontalAlignment='Center';$Footer.TextAlignment='Center';$Footer.FontFamily='맑은 고딕';$Footer.FontSize=9;$Footer.Foreground='#8A8A8A';[System.Windows.Controls.Canvas]::SetLeft($Footer,12);[System.Windows.Controls.Canvas]::SetTop($Footer,$NominalHeight-30);[void]$Canvas.Children.Add($Footer)
        $Status.Text="$($Institution.name) · 기관 기능 $($CustomFeatures.Count)개"
        Add-InstitutionFavorites $Dialog $InstitutionId;Show-WorkspaceWindow $Dialog "institution:$InstitutionId";return
    }
    $GenericArea=[System.Windows.SystemParameters]::WorkArea
    $Dialog=[System.Windows.Window]::new();$Dialog.Title="범정부오피스 · $($Institution.name)";$Dialog.Width=[math]::Min(460,[math]::Max(1,$GenericArea.Width-24));$Dialog.Height=[math]::Min(620,[math]::Max(1,$GenericArea.Height-24));$Dialog.Topmost=$false;$Dialog.Owner=$Window;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.Background=[System.Windows.Media.Brushes]::White
    $Grid=[System.Windows.Controls.Grid]::new();$Dialog.Content=$Grid
    foreach($height in @(42,34,'*',34,38,26)){ $row=[System.Windows.Controls.RowDefinition]::new(); if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)};[void]$Grid.RowDefinitions.Add($row)}
    $Title=[System.Windows.Controls.TextBlock]::new();$Title.Text="$($Institution.name) 기능";$Title.FontFamily='맑은 고딕';$Title.FontSize=18;$Title.FontWeight='Bold';$Title.Margin=10;$Grid.Children.Add($Title)|Out-Null
    $Search=[System.Windows.Controls.TextBox]::new();$Search.Margin='8,2';$Search.ToolTip='기관 기능 검색';[System.Windows.Controls.Grid]::SetRow($Search,1);$Grid.Children.Add($Search)|Out-Null
    $List=[System.Windows.Controls.ListBox]::new();$List.Margin='8,2';$List.FontFamily='맑은 고딕';$List.FontSize=13;$List.DisplayMemberPath='name';[System.Windows.Controls.Grid]::SetRow($List,2);$Grid.Children.Add($List)|Out-Null
    $ParameterLabel=[System.Windows.Controls.TextBlock]::new();$ParameterLabel.Margin='8,6';$ParameterLabel.Text='매개변수 없음';[System.Windows.Controls.Grid]::SetRow($ParameterLabel,3);$Grid.Children.Add($ParameterLabel)|Out-Null
    $ArgumentGrid=[System.Windows.Controls.Grid]::new();$ArgumentGrid.Margin='8,2';$ArgumentGrid.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new())|Out-Null;$column=[System.Windows.Controls.ColumnDefinition]::new();$column.Width=80;$ArgumentGrid.ColumnDefinitions.Add($column)|Out-Null;[System.Windows.Controls.Grid]::SetRow($ArgumentGrid,4);$Grid.Children.Add($ArgumentGrid)|Out-Null
    $Args=[System.Windows.Controls.TextBox]::new();$Args.Text='[]';$Args.VerticalContentAlignment='Center';$ArgumentGrid.Children.Add($Args)|Out-Null
    $Run=[System.Windows.Controls.Button]::new();$Run.Content='실행';$Run.Margin='5,0,0,0';[System.Windows.Controls.Grid]::SetColumn($Run,1);$ArgumentGrid.Children.Add($Run)|Out-Null
    $LocalStatus=[System.Windows.Controls.TextBlock]::new();$LocalStatus.Margin='8,4';$LocalStatus.Text="정상 연결 기능 $($Institution.functions.Count)개";[System.Windows.Controls.Grid]::SetRow($LocalStatus,5);$Grid.Children.Add($LocalStatus)|Out-Null
    $RefreshInstitutionList = { $List.Items.Clear();foreach($Function in $Institution.functions){if(-not $Search.Text -or $Function.name -like "*$($Search.Text)*"){$List.Items.Add($Function)|Out-Null}} }.GetNewClosure()
    $Search.Add_TextChanged({& $RefreshInstitutionList}.GetNewClosure())
    $List.Add_SelectionChanged({if($List.SelectedItem){$parameters=@($List.SelectedItem.parameters);$ParameterLabel.Text=if($parameters.Count){'매개변수: '+($parameters -join ', ')}else{'매개변수 없음'};$Args.Text='[]'}}.GetNewClosure())
    $Run.Add_Click({
        if(-not $List.SelectedItem){return}
        try{$values=@(ConvertFrom-Json -InputObject $Args.Text);$function=$List.SelectedItem;if($values.Count -lt @($function.parameters).Count){throw '필수 매개변수 값을 JSON 배열로 입력하세요.'};$operation=[pscustomobject]@{type='method';method=$function.method;args=$values};$response=Send-Backend @{action='run_sequence';operations=@($operation)};$LocalStatus.Text=$response.message;$Status.Text="$($Institution.name) · $($response.message)";if(-not $response.ok){Show-Error $response.message}}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $List.Add_MouseDoubleClick({if($List.SelectedItem -and @($List.SelectedItem.parameters).Count -eq 0){$Run.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Button]::ClickEvent))}}.GetNewClosure())
    & $RefreshInstitutionList
    Add-InstitutionFavorites $Dialog $InstitutionId;Show-WorkspaceWindow $Dialog "institution:$InstitutionId"
}
function Open-BasicProfileEditor($OwnerWindow=$Window) {
    $Profile=Send-Backend @{action='user_profile_get'};if(-not $Profile.ok){throw $Profile.message}
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='기본 정보 수정';$Dialog.Width=430;$Dialog.Height=330;$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.ResizeMode='NoResize';$Dialog.Background='White';$Dialog.FontFamily='맑은 고딕'
    $Grid=[System.Windows.Controls.Grid]::new();$Dialog.Content=$Grid;foreach($height in @(58,'*',48)){$row=[System.Windows.Controls.RowDefinition]::new();if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)};[void]$Grid.RowDefinitions.Add($row)}
    $Header=[System.Windows.Controls.Border]::new();$Header.Background='#66558F';[System.Windows.Controls.Grid]::SetRow($Header,0);[void]$Grid.Children.Add($Header);$HeaderText=[System.Windows.Controls.TextBlock]::new();$HeaderText.Text='기본 사용자 정보 수정';$HeaderText.Foreground='White';$HeaderText.FontSize=18;$HeaderText.FontWeight='Bold';$HeaderText.Margin='18,14';$Header.Child=$HeaderText
    Set-OriginalSectionHeader $Header $HeaderText
    $Form=[System.Windows.Controls.Grid]::new();$Form.Margin='22,16';$labelColumn=[System.Windows.Controls.ColumnDefinition]::new();$labelColumn.Width=90;[void]$Form.ColumnDefinitions.Add($labelColumn);[void]$Form.ColumnDefinitions.Add([System.Windows.Controls.ColumnDefinition]::new());foreach($i in 0..2){$row=[System.Windows.Controls.RowDefinition]::new();$row.Height=54;[void]$Form.RowDefinitions.Add($row)};[System.Windows.Controls.Grid]::SetRow($Form,1);[void]$Grid.Children.Add($Form)
    $BasicFields=@('이름','전화번호','이메일');$Editors=@{}
    for($i=0;$i -lt $BasicFields.Count;$i++){
        $field=$BasicFields[$i];$Label=[System.Windows.Controls.TextBlock]::new();$Label.Text=$field;$Label.FontWeight='SemiBold';$Label.VerticalAlignment='Center';[System.Windows.Controls.Grid]::SetRow($Label,$i);[void]$Form.Children.Add($Label)
        $Input=[System.Windows.Controls.TextBox]::new();$Input.Height=32;$Input.VerticalContentAlignment='Center';$Input.Margin='0,6';$property=$Profile.values.PSObject.Properties[$field];if($null -ne $property){$Input.Text=[string]$property.Value};[System.Windows.Controls.Grid]::SetRow($Input,$i);[System.Windows.Controls.Grid]::SetColumn($Input,1);[void]$Form.Children.Add($Input);$Editors[$field]=$Input
    }
    $Buttons=[System.Windows.Controls.StackPanel]::new();$Buttons.Orientation='Horizontal';$Buttons.HorizontalAlignment='Right';$Buttons.Margin='16,6,16,8';$Save=[System.Windows.Controls.Button]::new();$Save.Content='저장';$Save.Width=85;$Save.Margin='0,0,8,0';$Save.Background='#66558F';$Save.Foreground='White';$Cancel=[System.Windows.Controls.Button]::new();$Cancel.Content='취소';$Cancel.Width=75;[void]$Buttons.Children.Add($Save);[void]$Buttons.Children.Add($Cancel);[System.Windows.Controls.Grid]::SetRow($Buttons,2);[void]$Grid.Children.Add($Buttons)
    Set-OriginalFlatButton $Save $true;Set-OriginalFlatButton $Cancel $false
    # DialogResult를 설정하면 ShowDialog 창은 즉시 닫힌다. 그 뒤 Close()를 다시
    # 호출하면 저장 자체는 성공했어도 "창이 닫힌 뒤 작업할 수 없음" 오류가 난다.
    $Save.Add_Click({try{$values=@{};foreach($field in $BasicFields){$values[$field]=$Editors[$field].Text};$response=Send-Backend @{action='user_profile_basic_save';values=$values};if(-not $response.ok){throw $response.message};$Status.Text=$response.message;$Dialog.DialogResult=$true}catch{Show-Error $_.Exception.Message}})
    $Cancel.Add_Click({$Dialog.Close()});return $Dialog.ShowDialog()
}
function Open-DocumentFieldManager($OwnerWindow=$Window) {
    if(Test-WorkspaceWindow 'profile-manager'){return}
    Invoke-ProfileReviewSession $OwnerWindow {param($owner) Show-DocumentFieldManager $owner}
}
function Show-DocumentFieldManager($OwnerWindow) {
    $Dialog=[System.Windows.Window]::new();$Dialog.Title='대표필드 · 입력값 · 별칭 관리';$Dialog.Width=1020;$Dialog.Height=740;$Dialog.MinWidth=850;$Dialog.MinHeight=610;$Dialog.Owner=$OwnerWindow;$Dialog.WindowStartupLocation='CenterOwner';$Dialog.ResizeMode='CanResize';$Dialog.Background='White';$Dialog.FontFamily='맑은 고딕'
    $Grid=[System.Windows.Controls.Grid]::new();$Dialog.Content=$Grid
    foreach($height in @(58,170,42,'*',36,42)){$row=[System.Windows.Controls.RowDefinition]::new();if($height -eq '*'){$row.Height=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$row.Height=[System.Windows.GridLength]::new([double]$height)};[void]$Grid.RowDefinitions.Add($row)}
    $Header=[System.Windows.Controls.Border]::new();$Header.Background='#66558F';[System.Windows.Controls.Grid]::SetRow($Header,0);[void]$Grid.Children.Add($Header)
    $HeaderText=[System.Windows.Controls.TextBlock]::new();$HeaderText.Text='문서 대표필드 · 여러 입력값 · 별칭 관리';$HeaderText.Foreground='White';$HeaderText.FontSize=18;$HeaderText.FontWeight='Bold';$HeaderText.Margin='18,14';$Header.Child=$HeaderText
    Set-OriginalSectionHeader $Header $HeaderText

    $InputGrid=[System.Windows.Controls.Grid]::new();$InputGrid.Margin='16,8,16,4';foreach($width in @(95,'*',95,'*')){$column=[System.Windows.Controls.ColumnDefinition]::new();if($width -eq '*'){$column.Width=[System.Windows.GridLength]::new(1,[System.Windows.GridUnitType]::Star)}else{$column.Width=[System.Windows.GridLength]::new([double]$width)};[void]$InputGrid.ColumnDefinitions.Add($column)};foreach($height in @(52,52,44)){$row=[System.Windows.Controls.RowDefinition]::new();$row.Height=$height;[void]$InputGrid.RowDefinitions.Add($row)}
    $FieldLabel=[System.Windows.Controls.TextBlock]::new();$FieldLabel.Text='필드 이름';$FieldLabel.VerticalAlignment='Center';$FieldLabel.FontWeight='SemiBold';[void]$InputGrid.Children.Add($FieldLabel)
    $FieldName=[System.Windows.Controls.TextBox]::new();$FieldName.Margin='0,8,12,8';$FieldName.VerticalContentAlignment='Center';$FieldName.ToolTip='예: 과제명, 책임자, 연구자';[System.Windows.Controls.Grid]::SetColumn($FieldName,1);[void]$InputGrid.Children.Add($FieldName)
    $ValueLabel=[System.Windows.Controls.TextBlock]::new();$ValueLabel.Text='입력값';$ValueLabel.VerticalAlignment='Center';$ValueLabel.FontWeight='SemiBold';[System.Windows.Controls.Grid]::SetColumn($ValueLabel,2);[void]$InputGrid.Children.Add($ValueLabel)
    $Value=[System.Windows.Controls.TextBox]::new();$Value.Margin='0,8,0,8';$Value.VerticalContentAlignment='Center';$Value.ToolTip='문서에 실제로 들어갈 값. 구조용 대표필드는 비워도 됩니다.';[System.Windows.Controls.Grid]::SetColumn($Value,3);[void]$InputGrid.Children.Add($Value)
    $AliasLabel=[System.Windows.Controls.TextBlock]::new();$AliasLabel.Text='별칭';$AliasLabel.VerticalAlignment='Center';$AliasLabel.FontWeight='SemiBold';[System.Windows.Controls.Grid]::SetRow($AliasLabel,1);[void]$InputGrid.Children.Add($AliasLabel)
    $Aliases=[System.Windows.Controls.TextBox]::new();$Aliases.Margin='0,8,0,8';$Aliases.VerticalContentAlignment='Center';$Aliases.ToolTip='쉼표로 구분: 사업명, 프로젝트명';[System.Windows.Controls.Grid]::SetRow($Aliases,1);[System.Windows.Controls.Grid]::SetColumn($Aliases,1);[System.Windows.Controls.Grid]::SetColumnSpan($Aliases,3);[void]$InputGrid.Children.Add($Aliases)
    $ParentLabel=[System.Windows.Controls.TextBlock]::new();$ParentLabel.Text='상위 필드';$ParentLabel.VerticalAlignment='Center';$ParentLabel.FontWeight='SemiBold';[System.Windows.Controls.Grid]::SetRow($ParentLabel,2);[void]$InputGrid.Children.Add($ParentLabel)
    $Parent=[System.Windows.Controls.ComboBox]::new();$Parent.Margin='0,5,0,5';$Parent.Height=32;$Parent.DisplayMemberPath='path';$Parent.ToolTip='없음이면 최상위 대표필드, 선택하면 그 필드의 하위 구조로 저장됩니다.';[void]$Parent.Items.Add([pscustomobject]@{id='';path='(상위 없음 — 대표필드로 저장)'});$Parent.SelectedIndex=0;[System.Windows.Controls.Grid]::SetRow($Parent,2);[System.Windows.Controls.Grid]::SetColumn($Parent,1);[System.Windows.Controls.Grid]::SetColumnSpan($Parent,3);[void]$InputGrid.Children.Add($Parent)
    [System.Windows.Controls.Grid]::SetRow($InputGrid,1);[void]$Grid.Children.Add($InputGrid)

    $CommandPanel=[System.Windows.Controls.StackPanel]::new();$CommandPanel.Orientation='Horizontal';$CommandPanel.HorizontalAlignment='Right';$CommandPanel.Margin='16,0,16,4'
    $Add=[System.Windows.Controls.Button]::new();$Add.Content='필드·값 저장';$Add.Width=100;$Add.Margin='0,0,8,0';$Add.Background='#F1EEF8';$Add.Foreground='#55447A';$Add.FontWeight='SemiBold'
    $SetParent=[System.Windows.Controls.Button]::new();$SetParent.Content='상위 변경';$SetParent.Width=82;$SetParent.Margin='0,0,8,0'
    $SaveAliases=[System.Windows.Controls.Button]::new();$SaveAliases.Content='별칭 전체 저장';$SaveAliases.Width=115;$SaveAliases.Margin='0,0,8,0'
    $SetDefault=[System.Windows.Controls.Button]::new();$SetDefault.Content='기본값 지정';$SetDefault.Width=95;$SetDefault.Margin='0,0,8,0'
    $Delete=[System.Windows.Controls.Button]::new();$Delete.Content='값 삭제';$Delete.Width=82;$Delete.Margin='0,0,8,0'
    $DeleteField=[System.Windows.Controls.Button]::new();$DeleteField.Content='필드 삭제';$DeleteField.Width=88
    [void]$CommandPanel.Children.Add($Add);[void]$CommandPanel.Children.Add($SetParent);[void]$CommandPanel.Children.Add($SaveAliases);[void]$CommandPanel.Children.Add($SetDefault);[void]$CommandPanel.Children.Add($Delete);[void]$CommandPanel.Children.Add($DeleteField);[System.Windows.Controls.Grid]::SetRow($CommandPanel,2);[void]$Grid.Children.Add($CommandPanel)

    $TableScroll=[System.Windows.Controls.ScrollViewer]::new();$TableScroll.Margin='16,4,16,6';$TableScroll.HorizontalScrollBarVisibility='Auto';$TableScroll.VerticalScrollBarVisibility='Auto'
    $TableGrid=[System.Windows.Controls.Grid]::new();$TableGrid.Name='DocumentFieldTreeTable';$TableGrid.Background='White';$TableGrid.VerticalAlignment='Top';$TableScroll.Content=$TableGrid
    [System.Windows.Controls.Grid]::SetRow($TableScroll,3);[void]$Grid.Children.Add($TableScroll)
    $LocalStatus=[System.Windows.Controls.TextBlock]::new();$LocalStatus.Margin='16,8';$LocalStatus.Foreground='#555555';$LocalStatus.TextTrimming='CharacterEllipsis';[System.Windows.Controls.Grid]::SetRow($LocalStatus,4);[void]$Grid.Children.Add($LocalStatus)
    $Bottom=[System.Windows.Controls.StackPanel]::new();$Bottom.Orientation='Horizontal';$Bottom.HorizontalAlignment='Right';$Bottom.Margin='16,4,16,8';$Close=[System.Windows.Controls.Button]::new();$Close.Content='닫기';$Close.Width=80;$Close.Height=28;[void]$Bottom.Children.Add($Close);[System.Windows.Controls.Grid]::SetRow($Bottom,5);[void]$Grid.Children.Add($Bottom)
    foreach($OriginalButton in @($Add,$SetParent,$SaveAliases,$SetDefault,$Delete,$DeleteField,$Close)){Set-OriginalFlatButton $OriginalButton ($OriginalButton -eq $Add)}

    $Table=@{Dialog=$Dialog;Grid=$TableGrid;Profile=$null;Note=$LocalStatus;Row=1;Depth=1;DragStart=$null;DragSource=$null;PageId=[Guid]::NewGuid().ToString();SelectedItem=$null;DocumentFieldsOnly=$true}
    $Table.Select={param($field,$storedValue,$kind)
        if($kind -eq 'field'){$storedValue=[string]$field.default}
        $Table.SelectedItem=[pscustomobject]@{profile_field_id=[string]$field.id;parent_field_id=[string]$field.parent_id;field_name=[string]$field.path;leaf_name=[string]$field.name;aliases=(@($field.aliases)-join ', ');value=[string]$storedValue}
        $FieldName.Text=[string]$field.name;$Value.Text=[string]$storedValue;$Aliases.Text=(@($field.aliases)-join ', ')
        $Parent.SelectedIndex=0
        for($i=0;$i -lt $Parent.Items.Count;$i++){if([string]$Parent.Items[$i].id -eq [string]$field.parent_id){$Parent.SelectedIndex=$i;break}}
        $related=@($Table.Profile.field_groups|Where-Object{$_.id -ne $field.id -and $storedValue -and $_.values -ccontains $storedValue}|ForEach-Object{$_.path})
        $LocalStatus.Text='선택: '+$field.path+$(if($related.Count){' · 같은 값이 있는 필드: '+($related -join ', ')}else{' · 더블클릭으로 이름·값 수정 / 우클릭으로 관리'})
    }.GetNewClosure()
    $Table.OnRefreshed={
        $response=$Table.Profile;$previous=$Table.SelectedItem
        $selectedParentId=if($Parent.SelectedItem){[string]$Parent.SelectedItem.id}else{''}
        $Parent.Items.Clear();[void]$Parent.Items.Add([pscustomobject]@{id='';path='(상위 없음 — 대표필드로 저장)'})
        foreach($group in @($response.field_groups)){if($group.name -notin @('이름','전화번호','이메일')){[void]$Parent.Items.Add($group)}}
        $Parent.SelectedIndex=0
        for($i=0;$i -lt $Parent.Items.Count;$i++){if([string]$Parent.Items[$i].id -eq $selectedParentId){$Parent.SelectedIndex=$i;break}}
        $LocalStatus.Text='대표 필드 → 하위 필드 → 저장값 · 상단 열 경계 끌기: 너비 조절 · 더블클릭: 수정'
        $Table.SelectedItem=$null
        if($previous){
            $field=@($response.field_groups|Where-Object{$_.id -eq $previous.profile_field_id})|Select-Object -First 1
            if($field){$selectedValue=if($field.values -ccontains $previous.value){$previous.value}else{$field.default};& $Table.Select $field $selectedValue 'value'}
            else{$FieldName.Clear();$Value.Clear();$Aliases.Clear()}
        }
    }.GetNewClosure()
    $RefreshDocumentFieldRows = {Update-ProfileTable $Table}.GetNewClosure()
    $Add.Add_Click({
        try{
            $aliasValues=@($Aliases.Text -split '[,;，；]'|ForEach-Object{$_.Trim()}|Where-Object{$_})
            $parentId=if($Parent.SelectedItem){[string]$Parent.SelectedItem.id}else{''};$response=Send-Backend @{snapshot=$Table.Profile.values;action='user_profile_entry_add';parent_field_id=$parentId;field_name=$FieldName.Text;value=$Value.Text;aliases=$aliasValues};if(-not $response.ok){throw $response.message}
            $LocalStatus.Text=$response.message;$Table.SelectedItem=$null;$Value.Clear();& $RefreshDocumentFieldRows;$Status.Text=$response.message
        }catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $SetParent.Add_Click({
        if(-not $Table.SelectedItem){$LocalStatus.Text='상위를 변경할 필드를 먼저 선택하세요.';return}
        try{$parentId=if($Parent.SelectedItem){[string]$Parent.SelectedItem.id}else{''};$response=Send-Backend @{snapshot=$Table.Profile.values;action='user_profile_field_parent_set';field_id=$Table.SelectedItem.profile_field_id;parent_field_id=$parentId};if(-not $response.ok){throw $response.message};& $RefreshDocumentFieldRows;$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $SaveAliases.Add_Click({
        if(-not $Table.SelectedItem){$LocalStatus.Text='별칭을 수정할 대표필드의 값을 하나 선택하세요.';return}
        try{$aliasValues=@($Aliases.Text -split '[,;，；]'|ForEach-Object{$_.Trim()}|Where-Object{$_});$response=Send-Backend @{snapshot=$Table.Profile.values;action='user_profile_aliases_set';field_id=$Table.SelectedItem.profile_field_id;aliases=$aliasValues};if(-not $response.ok){throw $response.message};& $RefreshDocumentFieldRows;$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $SetDefault.Add_Click({
        if(-not $Table.SelectedItem){$LocalStatus.Text='기본으로 사용할 입력값을 선택하세요.';return}
        try{$response=Send-Backend @{snapshot=$Table.Profile.values;action='user_profile_default_set';field_id=$Table.SelectedItem.profile_field_id;value=$Table.SelectedItem.value};if(-not $response.ok){throw $response.message};& $RefreshDocumentFieldRows;$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $Delete.Add_Click({
        if(-not $Table.SelectedItem){$LocalStatus.Text='삭제할 입력값을 선택하세요.';return}
        if([string]::IsNullOrWhiteSpace([string]$Table.SelectedItem.value)){$LocalStatus.Text='이 필드에는 삭제할 값이 없습니다. 필드 삭제를 사용하세요.';return}
        try{$response=Send-Backend @{snapshot=$Table.Profile.values;action='user_profile_entry_delete';field_name=$Table.SelectedItem.field_name;value=$Table.SelectedItem.value};if(-not $response.ok){throw $response.message};& $RefreshDocumentFieldRows;$LocalStatus.Text=$response.message}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $DeleteField.Add_Click({
        if(-not $Table.SelectedItem){$LocalStatus.Text='삭제할 대표필드를 선택하세요.';return}
        $answer=[System.Windows.MessageBox]::Show("$($Table.SelectedItem.field_name) 대표필드와 모든 값·별칭을 삭제할까요?",'대표필드 삭제',[System.Windows.MessageBoxButton]::YesNo,[System.Windows.MessageBoxImage]::Warning);if($answer -ne [System.Windows.MessageBoxResult]::Yes){return}
        try{$response=Send-Backend @{snapshot=$Table.Profile.values;action='user_profile_field_delete';field_id=$Table.SelectedItem.profile_field_id};if(-not $response.ok){throw $response.message};& $RefreshDocumentFieldRows;$LocalStatus.Text=$response.message;$Status.Text=$response.message}catch{Show-Error $_.Exception.Message}
    }.GetNewClosure())
    $Value.Add_KeyDown({if($_.Key -eq 'Enter'){$Add.RaiseEvent([System.Windows.RoutedEventArgs]::new([System.Windows.Controls.Button]::ClickEvent))}}.GetNewClosure())
    $RefreshButton=New-ProfileToolButton '새로고침';$RefreshButton.Height=28;$RefreshButton.Padding='10,2';[void]$Bottom.Children.Insert(0,$RefreshButton)
    $RefreshButton.Add_Click({try{& $RefreshDocumentFieldRows}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $Close.Add_Click({$Dialog.Close()}.GetNewClosure())
    try{& $RefreshDocumentFieldRows}catch{Show-Error $_.Exception.Message}
    Show-WorkspaceWindow $Dialog 'profile-manager'
}
function Render-PersonalTab {
    $Content.Children.Clear()
    $Title=[System.Windows.Controls.TextBlock]::new();$Title.Text='출력 사용자 정보';$Title.FontFamily='맑은 고딕';$Title.FontSize=16;$Title.FontWeight='Bold';$Title.Foreground='#262626';[System.Windows.Controls.Canvas]::SetLeft($Title,10);[System.Windows.Controls.Canvas]::SetTop($Title,8);[void]$Content.Children.Add($Title)
    $EditBasic=[System.Windows.Controls.Button]::new();$EditBasic.Content='기본정보 수정';$EditBasic.Width=92;$EditBasic.Height=27;$EditBasic.FontSize=9;[System.Windows.Controls.Canvas]::SetLeft($EditBasic,198);[System.Windows.Controls.Canvas]::SetTop($EditBasic,5);[void]$Content.Children.Add($EditBasic);Set-OriginalFlatButton $EditBasic $false
    $AccentLine=[System.Windows.Controls.Border]::new();$AccentLine.Width=280;$AccentLine.Height=2;$AccentLine.Background=New-PurpleAccentBrush;$AccentLine.CornerRadius=1;[System.Windows.Controls.Canvas]::SetLeft($AccentLine,10);[System.Windows.Controls.Canvas]::SetTop($AccentLine,35);[void]$Content.Children.Add($AccentLine)
    $BasicCard=[System.Windows.Controls.Border]::new();$BasicCard.Width=280;$BasicCard.Height=128;$BasicCard.Background='White';$BasicCard.BorderBrush='#DBDBDB';$BasicCard.BorderThickness=1;$BasicCard.CornerRadius=12;[System.Windows.Controls.Canvas]::SetLeft($BasicCard,10);[System.Windows.Controls.Canvas]::SetTop($BasicCard,43);[void]$Content.Children.Add($BasicCard)
    $BasicCanvas=[System.Windows.Controls.Canvas]::new();$BasicCard.Child=$BasicCanvas
    $Avatar=[System.Windows.Controls.Border]::new();$Avatar.Width=50;$Avatar.Height=50;$Avatar.CornerRadius=25;$Avatar.Background=New-PurpleAccentBrush;[System.Windows.Controls.Canvas]::SetLeft($Avatar,12);[System.Windows.Controls.Canvas]::SetTop($Avatar,15);[void]$BasicCanvas.Children.Add($Avatar)
    $AvatarText=[System.Windows.Controls.TextBlock]::new();$AvatarText.Text='+';$AvatarText.Foreground='White';$AvatarText.FontSize=19;$AvatarText.FontWeight='Bold';$AvatarText.HorizontalAlignment='Center';$AvatarText.VerticalAlignment='Center';$Avatar.Child=$AvatarText
    $NameValue=[System.Windows.Controls.TextBlock]::new();$NameValue.Text='저장된 이름 없음';$NameValue.Width=190;$NameValue.FontSize=15;$NameValue.FontWeight='Bold';$NameValue.Foreground='#262626';$NameValue.TextTrimming='CharacterEllipsis';[System.Windows.Controls.Canvas]::SetLeft($NameValue,74);[System.Windows.Controls.Canvas]::SetTop($NameValue,13);[void]$BasicCanvas.Children.Add($NameValue)
    $PhoneLabel=[System.Windows.Controls.TextBlock]::new();$PhoneLabel.Text='전화';$PhoneLabel.Width=38;$PhoneLabel.FontSize=9;$PhoneLabel.Foreground='#737373';[System.Windows.Controls.Canvas]::SetLeft($PhoneLabel,74);[System.Windows.Controls.Canvas]::SetTop($PhoneLabel,47);[void]$BasicCanvas.Children.Add($PhoneLabel)
    $PhoneValue=[System.Windows.Controls.TextBlock]::new();$PhoneValue.Text='저장된 값 없음';$PhoneValue.Width=150;$PhoneValue.FontSize=10;$PhoneValue.Foreground='#262626';$PhoneValue.TextTrimming='CharacterEllipsis';[System.Windows.Controls.Canvas]::SetLeft($PhoneValue,112);[System.Windows.Controls.Canvas]::SetTop($PhoneValue,44);[void]$BasicCanvas.Children.Add($PhoneValue)
    $EmailLabel=[System.Windows.Controls.TextBlock]::new();$EmailLabel.Text='이메일';$EmailLabel.Width=38;$EmailLabel.FontSize=9;$EmailLabel.Foreground='#737373';[System.Windows.Controls.Canvas]::SetLeft($EmailLabel,74);[System.Windows.Controls.Canvas]::SetTop($EmailLabel,76);[void]$BasicCanvas.Children.Add($EmailLabel)
    $EmailValue=[System.Windows.Controls.TextBlock]::new();$EmailValue.Text='저장된 값 없음';$EmailValue.Width=150;$EmailValue.FontSize=10;$EmailValue.Foreground='#262626';$EmailValue.TextTrimming='CharacterEllipsis';[System.Windows.Controls.Canvas]::SetLeft($EmailValue,112);[System.Windows.Controls.Canvas]::SetTop($EmailValue,73);[void]$BasicCanvas.Children.Add($EmailValue)

    $OtherTitle=[System.Windows.Controls.TextBlock]::new();$OtherTitle.Text='문서 출력 필드';$OtherTitle.FontSize=12;$OtherTitle.FontWeight='Bold';$OtherTitle.Foreground='#262626';[System.Windows.Controls.Canvas]::SetLeft($OtherTitle,10);[System.Windows.Controls.Canvas]::SetTop($OtherTitle,185);[void]$Content.Children.Add($OtherTitle)
    $Manage=[System.Windows.Controls.Button]::new();$Manage.Content='새 값 입력 · 관리';$Manage.Width=112;$Manage.Height=28;$Manage.FontSize=9;[System.Windows.Controls.Canvas]::SetLeft($Manage,178);[System.Windows.Controls.Canvas]::SetTop($Manage,178);[void]$Content.Children.Add($Manage);Set-OriginalFlatButton $Manage $true
    $FieldList=[System.Windows.Controls.TreeView]::new();$FieldList.Name='PersonalFieldTree';$FieldList.Width=280;$FieldList.Height=130;$FieldList.FontSize=10;$FieldList.BorderBrush='#DBDBDB';$FieldList.Background='#FAFAFA';$FieldList.Padding='4';[System.Windows.Controls.ScrollViewer]::SetHorizontalScrollBarVisibility($FieldList,[System.Windows.Controls.ScrollBarVisibility]::Auto);[System.Windows.Controls.Canvas]::SetLeft($FieldList,10);[System.Windows.Controls.Canvas]::SetTop($FieldList,170);[void]$Content.Children.Add($FieldList)
    $BasicCard.Height=92;[System.Windows.Controls.Canvas]::SetTop($OtherTitle,144);[System.Windows.Controls.Canvas]::SetTop($Manage,138)
    $PersonalActions=@{}
    $LocalStatus=[System.Windows.Controls.TextBlock]::new();$LocalStatus.Width=280;$LocalStatus.FontSize=9;$LocalStatus.Foreground='#555555';$LocalStatus.TextTrimming='CharacterEllipsis';[System.Windows.Controls.Canvas]::SetLeft($LocalStatus,10);[System.Windows.Controls.Canvas]::SetTop($LocalStatus,302);[void]$Content.Children.Add($LocalStatus)
    $BasicFields=@('이름','전화번호','이메일')
    $ImportPersonal=New-ProfileToolButton '선택 영역 → 개인정보 저장';$ImportPersonal.Width=168;$ImportPersonal.Height=28;$ImportPersonal.FontSize=9;$ImportPersonal.Padding='2';$ImportPersonal.Margin='0';[System.Windows.Controls.Canvas]::SetLeft($ImportPersonal,10);[System.Windows.Controls.Canvas]::SetTop($ImportPersonal,320);[void]$Content.Children.Add($ImportPersonal)
    $DataTable=New-ProfileToolButton '데이터 표 관리';$DataTable.Width=106;$DataTable.Height=28;$DataTable.FontSize=9;$DataTable.Padding='2';$DataTable.Margin='0';[System.Windows.Controls.Canvas]::SetLeft($DataTable,184);[System.Windows.Controls.Canvas]::SetTop($DataTable,320);[void]$Content.Children.Add($DataTable)
    $FavoriteScroll=[System.Windows.Controls.ScrollViewer]::new();$FavoriteScroll.Width=288;$FavoriteScroll.Height=48;$FavoriteScroll.VerticalScrollBarVisibility='Auto';$FavoriteScroll.Content=New-FavoriteStrip $Window;[System.Windows.Controls.Canvas]::SetLeft($FavoriteScroll,6);[System.Windows.Controls.Canvas]::SetTop($FavoriteScroll,352);[void]$Content.Children.Add($FavoriteScroll)
    # 개인 탭은 이 함수가 끝난 뒤에도 화면에 남는다. 이벤트에서 다시 쓸
    # 갱신 코드를 지역 함수로 만들면 함수 스코프 종료와 함께 사라지므로,
    # UI 컨트롤을 캡처한 클로저로 보관한다.
    $RefreshPersonalView = {
        $response=Send-Backend @{action='user_profile_get'};if(-not $response.ok){throw $response.message}
        $name=[string]$response.values.이름;$phone=[string]$response.values.전화번호;$email=[string]$response.values.이메일
        $NameValue.Text=if($name){$name}else{'저장된 이름 없음'};$AvatarText.Text=if($name){$name.Substring(0,1)}else{'+'};$PhoneValue.Text=if($phone){$phone}else{'저장된 값 없음'};$EmailValue.Text=if($email){$email}else{'저장된 값 없음'}
        Show-PersonalFieldTree $FieldList $response $Window $PersonalActions.Refresh
        $LocalStatus.Text="현재 출력값 미리보기 · 기타 필드 $(@($response.field_groups|Where-Object{$_.name -notin $BasicFields}).Count)개"
    }.GetNewClosure()
    $PersonalActions.Refresh=$RefreshPersonalView
    $EditBasic.Add_Click({try{[void](Open-BasicProfileEditor $Window);& $RefreshPersonalView}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    $ImportPersonal.Add_Click({
        $ImportPersonal.IsEnabled=$false;$DataTable.IsEnabled=$false
        try{Open-ProfileSelectionImport $Window;Add-WorkspaceClosedAction 'profile-import' $RefreshPersonalView;& $RefreshPersonalView}catch{Show-Error $_.Exception.Message}
        finally{$ImportPersonal.IsEnabled=$true;$DataTable.IsEnabled=$true}
    }.GetNewClosure())
    $DataTable.Add_Click({
        $ImportPersonal.IsEnabled=$false;$DataTable.IsEnabled=$false
        try{Open-ProfileDataTable $Window;Add-WorkspaceClosedAction 'profile-data' $RefreshPersonalView;& $RefreshPersonalView}catch{Show-Error $_.Exception.Message}
        finally{$ImportPersonal.IsEnabled=$true;$DataTable.IsEnabled=$true}
    }.GetNewClosure())
    $Manage.Add_Click({Open-DocumentFieldManager $Window;Add-WorkspaceClosedAction 'profile-manager' $RefreshPersonalView;try{& $RefreshPersonalView}catch{Show-Error $_.Exception.Message}}.GetNewClosure())
    try{& $RefreshPersonalView;$Status.Text='개인 · 사용자 정보'}catch{Show-Error $_.Exception.Message}
}
function Render-Tab([string]$Name) {
    $script:CurrentTab=$Name; $Content.Children.Clear(); foreach($key in $NavButtons.Keys){$NavButtons[$key].Opacity=1}
    if($Name -eq '개인'){Render-PersonalTab;return}
    $Tab=$TabMap[$Name]; $Visible=@($Tab.buttons|Where-Object enabled); foreach($Item in $Visible){ $Captured=$Item; if($Item.institution_id){$CapturedId=$Item.institution_id;$handler={Open-Institution $CapturedId}.GetNewClosure()}elseif($Item.feature_id -eq 'guided_format_copy'){$handler={Invoke-FormatCopy}.GetNewClosure()}else{$handler={Invoke-LayoutButton $Captured}.GetNewClosure()}; [void](New-ImageButton $Content $Item.x $Item.y $Item.width $Item.height $Item.icon $handler $Item.name $true) }
    $Status.Text="$Name · 연결된 원본 버튼 $($Visible.Count)개"
}

$TopItems = @(
    @{x=50; icon='상단바\불러오기.PNG'; tip='불러오기'; click={Open-HwpDocument}},
    @{x=100;icon='상단바\다시연결.PNG';tip='다시 연결';click={Connect-Hwp}},
    @{x=150;icon='상단바\새창.PNG';tip='새 문서';click={Invoke-LayoutButton ([pscustomobject]@{operations=@([pscustomobject]@{type='method';method='새창';args=@()});name='새 문서'})}},
    @{x=200;icon='상단바\최소화.PNG';tip='최소화';click={$Window.WindowState='Minimized'}},
    @{x=250;icon='상단바\닫기.PNG';tip='종료';click={$Window.Close()}}
)
foreach($Item in $TopItems){[void](New-ImageButton $TopBar $Item.x 0 50 50 $Item.icon $Item.click $Item.tip $true)}
$TopBar.Add_MouseLeftButtonDown({ if($_.ChangedButton -eq 'Left'){$Window.DragMove()} })

$Tabs=@('표','표세부','블록','이동','편리','글자','문자','중앙','지자체','사용','교직','공기업','기본서식','국방','가이드','개인')
for($i=0;$i -lt $Tabs.Count;$i++){
    $Name=$Tabs[$i]; $row=[math]::Floor($i/5); $x=($i%5)*60; $y=$row*60; $folder=if($i -lt 5){'중간네비게이션'}else{'네비게이션'}; $icon="$folder\네비게이션$Name.PNG"; $CapturedName=$Name
    $button=New-ImageButton $Navigation $x $y 60 60 $icon {Render-Tab $CapturedName}.GetNewClosure() $Name $true; $NavButtons[$Name]=$button
}
$Window.Add_KeyDown({if($_.Key -eq 'Z' -and [System.Windows.Input.Keyboard]::Modifiers -band [System.Windows.Input.ModifierKeys]::Control){Invoke-LayoutButton ([pscustomobject]@{operations=@([pscustomobject]@{type='method';method='취소';args=@(1)});name='취소'})}})
$DocumentStatusTimer=[System.Windows.Threading.DispatcherTimer]::new()
$DocumentStatusTimer.Interval=[TimeSpan]::FromMilliseconds(1500)
$DocumentStatusTimer.Add_Tick([GovOfficePollGuard]::Wrap({Refresh-HwpDocumentStatus $true}))
$DocumentStatusTimer.Start()
$script:SelectionMouseDown=$false
$script:SelectionStart=@(0,0)
$script:SelectionReturnWindow=$null
$SelectionProbeTimer=[System.Windows.Threading.DispatcherTimer]::new()
$SelectionProbeTimer.Interval=[TimeSpan]::FromMilliseconds(100)
$SelectionProbeTimer.Add_Tick([GovOfficePollGuard]::Wrap({
    if($script:ProfileReviewActive -or $script:BackendRequestInFlight){return}
    if($LayoutPreview -or $null -eq $Backend -or $Backend.HasExited){return}
    $foregroundPid=[GovOfficeSelectionMouse]::ForegroundProcessId()
    if($foregroundPid -le 0){$script:SelectionMouseDown=$false;return}
    try{$foregroundProcess=Get-Process -Id $foregroundPid -ErrorAction Stop}catch{$script:SelectionMouseDown=$false;return}
    if($foregroundProcess.ProcessName -ne 'Hwp'){$script:SelectionMouseDown=$false;return}
    $isDown=[GovOfficeSelectionMouse]::LeftButtonDown()
    if($isDown -and -not $script:SelectionMouseDown){
        $script:SelectionMouseDown=$true
        $script:SelectionStart=@([GovOfficeSelectionMouse]::CursorPosition())
        return
    }
    if(-not $isDown -and $script:SelectionMouseDown){
        $script:SelectionMouseDown=$false
        $end=@([GovOfficeSelectionMouse]::CursorPosition())
        $distance=[math]::Abs($end[0]-$script:SelectionStart[0])+[math]::Abs($end[1]-$script:SelectionStart[1])
        try{
            if($distance -ge 6){$probeResult=Send-Backend @{action='style_preset_selection_probe'};if($probeResult.captured -and $null -ne $script:SelectionReturnWindow){$returnWindow=$script:SelectionReturnWindow;$script:SelectionReturnWindow=$null;[void]$returnWindow.Activate()}}
            # 직접 항목 추가 대화상자가 새 드래그를 기다리는 동안의 단순
            # 클릭은 수동 선택 세션 자체를 지우면 안 된다. 세션이 없는 일반
            # 프리셋 선택 흐름에서만 이전 선택 캐시를 비운다.
            else{if(-not $script:ManualSelectionToken){[void](Send-Backend @{action='style_preset_selection_clear'})}}
        }catch{}
    }
}))
$SelectionProbeTimer.Start()
$Window.Add_Closed({
    $script:GuiClosing=$true
    $DocumentStatusTimer.Stop()
    $SelectionProbeTimer.Stop()
    if($null -ne $script:Backend){
        # 응답은 읽지 않고 정상 shutdown에 최대 5초만 준 뒤,
        # 남아 있는 Python 백엔드만 정리한다.
        [void](Stop-BackendProcess -Process $script:Backend -RequestShutdown $true)
    }
})
$InitialTab=if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_TAB){[string]$env:GOVOFFICE_LAYOUT_PREVIEW_TAB}else{'사용'}
Render-Tab $InitialTab
Refresh-HwpDocumentStatus $true
if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_SURFACE){
    $script:PreviewSurfaceOpened=$false
    $Window.Add_ContentRendered({
        if($script:PreviewSurfaceOpened){return};$script:PreviewSurfaceOpened=$true
        switch([string]$env:GOVOFFICE_LAYOUT_PREVIEW_SURFACE){
            'seoultech' {Open-Institution 'seoultech'}
            'preset' {Open-StylePresetManager $Window}
            'profile' {[void](Open-BasicProfileEditor $Window)}
            'fields' {Open-DocumentFieldManager $Window}
        }
    })
}
if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_REVIEW -eq '1'){
    $script:PreviewReviewOpened=$false
    $Window.Add_ContentRendered({
        if($script:PreviewReviewOpened){return};$script:PreviewReviewOpened=$true
        try{$previewAnalysis=Send-Backend @{action='style_preset_analyze'};[void](Open-StyleCaptureReview $previewAnalysis $Window);if($env:GOVOFFICE_LAYOUT_PREVIEW_DRAG_SELFTEST -eq '1'){$Window.Close()}}catch{$script:PreviewReviewSelfTest="DRAG_REVIEW_SELFTEST_FAILED: $($_.Exception.Message)";$Window.Close()}
    })
}
if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_EXCEPTION_SELFTEST -eq '1'){
    $script:PreviewDispatcherExceptionCaught=$false
    $Window.Add_ContentRendered({
        $script:ExceptionSelfTestTimer=[System.Windows.Threading.DispatcherTimer]::new();$script:ExceptionSelfTestTimer.Interval=[TimeSpan]::FromMilliseconds(200);$script:ExceptionSelfTestTimer.Add_Tick({$script:ExceptionSelfTestTimer.Stop();$Window.Close()});$script:ExceptionSelfTestTimer.Start()
        throw [System.InvalidOperationException]::new('GOVOFFICE_DISPATCHER_EXCEPTION_SELFTEST')
    })
}
$script:MainWindowFailure=$null
try{[void]$Window.ShowDialog()}catch{$script:MainWindowFailure=$_;Write-GuiRuntimeError 'main window ShowDialog' $_;if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_DRAG_SELFTEST -eq '1'){$script:PreviewReviewSelfTest="DRAG_REVIEW_SELFTEST_FAILED: $($_.Exception.Message)"}else{try{[System.Windows.MessageBox]::Show("화면 오류를 기록했습니다. 프로그램을 다시 실행해 주세요.`n`n$($_.Exception.Message)",'범정부오피스 오류')|Out-Null}catch{}}}finally{try{$AppMutex.ReleaseMutex()}catch{};$AppMutex.Dispose()}
if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_DRAG_SELFTEST -eq '1'){Write-Output $script:PreviewReviewSelfTest}
if($LayoutPreview -and $env:GOVOFFICE_LAYOUT_PREVIEW_EXCEPTION_SELFTEST -eq '1'){if($script:PreviewDispatcherExceptionCaught -and $null -eq $script:MainWindowFailure){Write-Output 'DISPATCHER_EXCEPTION_SELFTEST_OK'}else{Write-Output 'DISPATCHER_EXCEPTION_SELFTEST_FAILED';exit 1}}
if($null -ne $script:MainWindowFailure){exit 1}
