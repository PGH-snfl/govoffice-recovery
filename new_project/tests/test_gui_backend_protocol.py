import json
import base64
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
BACKEND = PROJECT / "gui_backend.py"
LAUNCHER = PROJECT / "launch_gui.ps1"


class GUI백엔드문자열프로토콜시험(unittest.TestCase):
    def test_UTF8_파이프에서_한글_성공과_오류메시지가_깨지지_않는다(self):
        process = subprocess.Popen(
            [sys.executable, str(BACKEND)],
            cwd=PROJECT.parent,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        입력 = "\n".join(
            json.dumps(명령, ensure_ascii=False)
            for 명령 in (
                {"action": "style_preset_list"},
                {"action": "hwp_document_status"},
                {"action": "hwp_document_open", "path": str(PROJECT / "__missing__.hwp")},
                {"action": "존재하지않는기능"},
                {"action": "shutdown"},
            )
        ) + "\n"
        출력, 오류 = process.communicate(입력, timeout=15)
        self.assertEqual(0, process.returncode, 오류)
        응답 = [json.loads(줄) for 줄 in 출력.splitlines()]
        self.assertEqual("READY", 응답[0]["message"])
        self.assertIn("저장된 서식 프리셋", 응답[1]["message"])
        self.assertEqual("현재 한글 문서 상태", 응답[2]["message"])
        self.assertFalse(응답[2]["document"]["connected"])
        self.assertIsNone(응답[2]["document"]["active_document_id"])
        self.assertEqual(0, 응답[2]["document"]["output_document_count"])
        self.assertFalse(응답[3]["ok"])
        self.assertEqual("hwp_document_open", 응답[3]["action"])
        self.assertFalse(응답[3]["document"]["connected"])
        self.assertEqual("알 수 없는 요청입니다: 존재하지않는기능", 응답[4]["message"])
        self.assertEqual("백엔드 종료", 응답[5]["message"])

    def test_문서수명주기_JSON_action과_원본보호옵션이_명시돼있다(self):
        소스 = BACKEND.read_text(encoding="utf-8")
        for action in (
            "hwp_document_open",
            "hwp_document_status",
            "hwp_document_show",
            "hwp_document_minimize",
            "hwp_document_close",
        ):
            self.assertIn(f'"{action}"', 소스)
        self.assertIn('"save_changes" in command', 소스)
        self.assertIn('error_type="ConfirmationRequired"', 소스)
        self.assertIn('"document": 안전문서상태()', 소스)

    def test_GUI런처가_백엔드_입출력을_UTF8로_고정한다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")
        self.assertNotIn("$Info.StandardInputEncoding", 소스)
        self.assertIn("function ConvertTo-AsciiJson", 소스)
        self.assertIn("ConvertTo-AsciiJson $Command", 소스)
        self.assertIn("$Info.EnvironmentVariables['PYTHONIOENCODING'] = 'utf-8'", 소스)

    def test_메인창이_연결된_한글문서_제목표시줄과_제어를_갖는다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn('Name="HwpDocumentPanel"', 소스)
        self.assertIn('Text="연결된 한글 문서"', 소스)
        self.assertIn('Name="HwpDocumentTitle"', 소스)
        self.assertIn('Name="HwpDocumentPath"', 소스)
        for 이름, 제목 in (
            ("HwpDocumentOpen", "문서 열기"),
            ("HwpDocumentShow", "화면에 표시/복원"),
            ("HwpDocumentMinimize", "최소화"),
            ("HwpDocumentClose", "닫기"),
        ):
            self.assertIn(f'Name="{이름}" Content="{제목}"', 소스)

        for action in (
            "hwp_document_open",
            "hwp_document_status",
            "hwp_document_show",
            "hwp_document_minimize",
            "hwp_document_close",
        ):
            self.assertIn(f"$Command.action -eq '{action}'", 소스)

        self.assertIn("function Refresh-HwpDocumentStatus", 소스)
        self.assertIn("$Command=@{action=$Action}", 소스)
        self.assertIn("$Response=Send-Backend $Command", 소스)
        self.assertIn("$DocumentStatusTimer.Interval=[TimeSpan]::FromMilliseconds(1500)", 소스)
        self.assertIn("$DocumentStatusTimer.Add_Tick({Refresh-HwpDocumentStatus $true})", 소스)
        self.assertNotIn(
            "$DocumentStatusTimer.Add_Tick({Refresh-HwpDocumentStatus $true}.GetNewClosure())",
            소스,
        )
        self.assertIn("$DocumentStatusTimer.Stop()", 소스)
        self.assertIn("$HwpDocumentShow.IsEnabled=", 소스)
        self.assertIn("$HwpDocumentMinimize.IsEnabled=", 소스)
        self.assertIn("$HwpDocumentClose.IsEnabled=", 소스)

    def test_문서패널을_추가해도_기존_콘텐츠와_네비가_잘리지_않는다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn('<Canvas Name="Root" Width="300" Height="824"', 소스)
        self.assertIn('Name="HwpDocumentPanel" Width="300" Height="104" Canvas.Left="0" Canvas.Top="50"', 소스)
        self.assertIn('<Canvas Name="Content" Width="300" Height="400" Canvas.Left="0" Canvas.Top="184"', 소스)
        self.assertIn('<Canvas Name="Navigation" Width="300" Height="240" Canvas.Left="0" Canvas.Top="584"', 소스)
        self.assertIn("$MainScale = Get-FitScale 300 824", 소스)
        self.assertIn("$Window.Height = 824 * $MainScale", 소스)

    def test_새로만든_화면은_차분한_보라색_단색테마를_공유한다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("function New-PurpleAccentBrush", 소스)
        self.assertIn("ConvertFromString('#66558F')", 소스)
        self.assertIn("function Get-PurpleButtonTemplate", 소스)
        self.assertNotIn("New-InstagramGradientBrush", 소스)
        self.assertNotIn("LinearGradientBrush", 소스)
        self.assertNotIn("GradientStop", 소스)
        self.assertNotIn("#E1306C", 소스)
        self.assertIn('CornerRadius="8"', 소스)
        self.assertIn("$Avatar.CornerRadius=25", 소스)
        self.assertIn("$BasicCard.CornerRadius=12", 소스)
        self.assertIn("Set-OriginalFlatButton $HwpDocumentOpen $true", 소스)
        self.assertIn("if ($Path -and (Test-Path -LiteralPath $Path))", 소스)

    def test_모든_문서열기는_파일선택후_절대경로를_관리문서로_보낸다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("[Microsoft.Win32.OpenFileDialog]::new()", 소스)
        self.assertIn("*.hwp;*.hwpx", 소스)
        self.assertIn("[System.IO.Path]::GetFullPath($Dialog.FileName)", 소스)
        self.assertIn("Invoke-HwpDocumentAction 'hwp_document_open' @{path=$FullPath;visible=$true}", 소스)
        self.assertIn("tip='불러오기'; click={Open-HwpDocument}", 소스)
        상단_불러오기 = 소스.split("$TopItems = @(", 1)[1].split("@{x=100", 1)[0]
        self.assertNotIn("method='불러오기'", 상단_불러오기)

    def test_수정된_관리문서를_닫을때_저장여부를_묻는다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("function Close-HwpDocument", 소스)
        self.assertIn("@('modified','dirty','is_modified')", 소스)
        self.assertIn("[System.Windows.MessageBoxButton]::YesNoCancel", 소스)
        self.assertIn("[System.Windows.MessageBoxResult]::Cancel", 소스)
        self.assertIn("@{save_changes=[bool]$SaveChanges}", 소스)

    def test_외부문서와_프로그램관리문서를_구분하고_관리문서만_창제어한다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("외부 한글 연결됨", 소스)
        self.assertIn("프로그램에서 불러온 문서 아님", 소스)
        self.assertIn("$DocumentOpen -and $Managed", 소스)
        self.assertIn("$HwpDocumentShow.IsEnabled=[bool]($BackendAvailable -and $DocumentOpen -and $Managed", 소스)
        self.assertIn("$HwpDocumentMinimize.IsEnabled=[bool]($BackendAvailable -and $DocumentOpen -and $Managed", 소스)

    def test_상태폴링은_문서를_활성화하지않고_실제작업과_표시만_관리원문서를_활성화한다(self):
        백엔드 = BACKEND.read_text(encoding="utf-8")
        연결구간 = 백엔드.split("def 연결(*, 관리작업: bool = True) -> None:", 1)[1].split(
            "def 안전문서상태", 1
        )[0]
        상태구간 = 백엔드.split('if action == "hwp_document_status":', 1)[1].split(
            'if action in {"hwp_document_show"', 1
        )[0]
        선택상태구간 = 백엔드.split(
            'if action == "style_preset_selection_status":', 1
        )[1].split('if action == "table_edit":', 1)[0]
        분석구간 = 백엔드.split('if action == "style_preset_analyze":', 1)[1].split(
            'if action == "style_preset_manual_candidate":', 1
        )[0]

        self.assertIn("한글.관리작업문서활성화()", 연결구간)
        self.assertIn("if 관리작업:", 연결구간)
        self.assertIn("연결(관리작업=False)", 백엔드)
        self.assertNotIn("관리작업문서활성화", 상태구간)
        self.assertNotIn("관리작업문서활성화", 선택상태구간)
        self.assertIn("한글.관리작업문서활성화()", 분석구간)

    def test_프리셋선택은_외부HWP를_ready로_오인하거나_첫창을_임의활성화하지않는다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")
        선택상태구간 = 백엔드.split(
            'if action == "style_preset_selection_status":', 1
        )[1].split('if action == "table_edit":', 1)[0]
        활성화구간 = 런처.split("function Activate-SelectionHwp", 1)[1].split(
            "function Invoke-LayoutButton", 1
        )[0]
        선택버튼구간 = 런처.split("$ChooseSelection.Add_Click", 1)[1].split(
            "function Refresh-StylePresetList", 1
        )[0]

        self.assertIn("managed_document_ready=관리문서준비", 선택상태구간)
        self.assertIn("managed_document_active=관리선택가능", 선택상태구간)
        self.assertNotIn("ActivateFirstHwpWindow", 활성화구간)
        self.assertIn("Open-HwpDocument", 선택버튼구간)
        self.assertNotIn("method='불러오기'", 선택버튼구간)

    def test_출력문서개수를_패널에_표시하고_열려있으면_관리닫기를_안내한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn('"output_document_count": 0', 백엔드)
        self.assertIn("@('output_document_count')", 런처)
        self.assertIn("출력 문서 $($OutputDocumentCount)개 별도 열림", 런처)
        self.assertIn("출력 문서를 저장하거나 닫은 후 다시 시도하세요.", 런처)

    def test_문서변경가능_일반액션은_실패해도_선택초안과_캐시를_먼저_폐기한다(self):
        백엔드 = BACKEND.read_text(encoding="utf-8")
        self.assertIn("def 선택상태무효화() -> None:", 백엔드)
        for 현재액션, 다음액션 in (
            ("user_profile_insert", "format_copy"),
            ("format_copy", "style_preset_selection_clear"),
            ("table_edit", "style_preset_capture"),
            ("style_preset_apply", "style_preset_delete"),
            ("run", "h_action"),
            ("h_action", "run_sequence"),
        ):
            구간 = 백엔드.split(f'if action == "{현재액션}":', 1)[1].split(
                f'if action == "{다음액션}":', 1
            )[0]
            self.assertIn("선택상태무효화()", 구간, 현재액션)
        실행연속구간 = 백엔드.split('if action == "run_sequence":', 1)[1].split(
            'raise ValueError(f"알 수 없는 요청입니다:', 1
        )[0]
        self.assertIn("선택상태무효화()", 실행연속구간)

    def test_모든_일반실행경로는_전후_DocumentID를_대조해_신규출력을_추적한다(self):
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertGreaterEqual(백엔드.count("한글.관리작업추적실행("), 8)
        for 액션 in (
            "user_profile_insert",
            "format_copy",
            "table_edit",
            "style_preset_apply",
            "run",
            "h_action",
            "run_sequence",
        ):
            self.assertIn(f'if action == "{액션}":', 백엔드)

    def test_다른문서를_열때_현재관리문서의_저장여부를_먼저처리한다(self):
        소스 = LAUNCHER.read_text(encoding="utf-8-sig")
        열기구간 = 소스.split("function Open-HwpDocument", 1)[1].split(
            "function Request-CloseManagedHwpDocument", 1
        )[0]

        self.assertIn("$SamePath", 열기구간)
        self.assertIn("Request-CloseManagedHwpDocument", 열기구간)
        self.assertIn("if(-not (Request-CloseManagedHwpDocument)){return}", 열기구간)

    def test_프리셋저장은_기존선택문서만_사용하고_새한글을_실행하지_않는다(self):
        소스 = BACKEND.read_text(encoding="utf-8")
        분석구간 = 소스.split('if action == "style_preset_analyze":', 1)[1].split(
            'if action == "style_preset_list":', 1
        )[0]
        저장구간 = 소스.split('if action == "style_preset_capture":', 1)[1].split(
            'if action == "style_preset_analyze":', 1
        )[0]

        self.assertIn("서식프리셋준비()", 분석구간)
        self.assertIn("서식프리셋준비()", 저장구간)
        self.assertNotIn("\n        연결()\n", 분석구간)
        self.assertNotIn("\n        연결()\n", 저장구간)

    def test_한글_마우스드래그가_끝나면_선택영역을_즉시_캐시한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn("GovOfficeSelectionMouse", 런처)
        self.assertIn("function Activate-SelectionHwp", 런처)
        self.assertIn("action='hwp_document_show'", 런처)
        self.assertIn("GetAsyncKeyState", 런처)
        self.assertIn("action='style_preset_selection_probe'", 런처)
        self.assertIn("action='style_preset_selection_clear'", 런처)
        self.assertIn('action == "style_preset_selection_probe"', 백엔드)
        self.assertIn('action == "style_preset_selection_status"', 백엔드)
        self.assertIn("_최근선택유효초 = 300.0", 백엔드)
        self.assertIn("한글 문서와 선택 영역을 확인하는 중입니다.", 런처)
        self.assertIn("한글에서 영역 선택", 런처)
        self.assertIn("한글 문서 열기", 런처)
        self.assertIn(
            "$Capture.IsEnabled=[bool]($state.hwp_running -and $state.selection_ready)",
            런처,
        )
        self.assertIn("& $RefreshSelectionState $true", 런처)
        self.assertIn("$analysis=Send-Backend @{action='style_preset_analyze'}", 런처)
        self.assertIn("if($analysis.no_registered_fields)", 런처)
        self.assertIn("selected_candidate_ids=@()", 런처)

    def test_프리셋검토는_필드명이_아닌_정확한_후보ID로_저장한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn("$candidate.candidate_id", 런처)
        self.assertIn("candidate_ids=@($selected)", 런처)
        self.assertIn("selected_candidate_ids=@($review.candidate_ids)", 런처)
        self.assertNotIn("selected_fields", 런처)
        self.assertNotIn('command.get("selected_fields"', 백엔드)
        self.assertIn('command.get("selected_candidate_ids", [])', 백엔드)
        self.assertIn("분석 결과에 없는 필드 후보가 선택되었습니다", 백엔드)
        self.assertIn("HWPMLTableFieldAnalyzer().analyze", 백엔드)
        self.assertIn("registered_values=[대표필드.사전()", 백엔드)
        self.assertIn("HWPML등록필드분류기().선택후보분류", 백엔드)

    def test_후보검토는_확정전체와_미확정을_한페이지에서_계층별로_표시한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn("$CandidateById=@{}", 런처)
        self.assertNotIn("PageSize=10", 런처)
        self.assertNotIn("$ReviewState.Page", 런처)
        self.assertNotIn("$Checks|Where-Object", 런처)
        self.assertIn("$DisplayByKey=@{}", 런처)
        self.assertIn("& $RenderSummary -Title '확정 후보'", 런처)
        self.assertIn("& $RenderSummary -Title '미확정 후보 (최대 10개)'", 런처)
        self.assertIn('& $RenderGroups -Rows @($AllCandidates)', 런처)
        self.assertIn('대표필드: {0} · 하위 항목 {1}개', 런처)
        self.assertIn('"{0}하위필드: {1}`n값: {2}', 런처)
        self.assertIn('$GroupHeader.Add_Click', 런처)
        self.assertIn('$child.IsChecked=$target', 런처)
        self.assertIn('$candidate.structural_group_id', 런처)
        self.assertIn('$candidate.structural_parent_field', 런처)
        self.assertIn('$candidate.semantic_group_id', 런처)
        self.assertIn('$candidate.semantic_representative_field', 런처)
        self.assertIn('$candidate.semantic_child_id', 런처)
        self.assertIn('$candidate.relationship_sort_rank', 런처)
        self.assertIn('$row.group_key', 런처)
        self.assertIn('("{0}{3}{1}{3}{2}" -f $semanticGroup,$semanticChild,$value,[char]31)', 런처)
        self.assertIn('$OrderedAnalysisCandidates=@($Analysis.candidates)', 런처)
        self.assertIn('Sort-Object relationship_anchor_order,document_order', 런처)
        self.assertIn('연결 위치 $($row.ids.Count)곳', 런처)
        self.assertIn('def 의미필드키(', 백엔드)
        self.assertIn('group_related_candidates(', 백엔드)
        self.assertIn('항목["semantic_group_id"] = 의미그룹ID', 백엔드)
        self.assertIn('f"profile-parent:{의미대표필드.id}"', 백엔드)
        self.assertIn('f"profile-field:{대표필드.id}"', 백엔드)
        self.assertIn("analysis_ms=분석소요ms", 백엔드)
        self.assertIn('"style_rules": 분석결과.get("style_rules", {})', 백엔드)
        self.assertIn("select_review_candidates(후보, _최대미확정추천후보)", 백엔드)
        self.assertIn("_최대미확정추천후보 = 10", 백엔드)
        self.assertNotIn("-not [bool]$candidate.recommended", 런처)
        self.assertIn("이동 손잡이를 원하는 대표필드 제목 위에 놓으세요", 런처)
        self.assertIn('후보["field"] = 저장경로', 백엔드)

    def test_후보행과_대표필드를_드래그해_부모구조만_바꾸고_저장한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn("≡ 하위필드 옮기기", 런처)
        self.assertIn("≡ 대표필드 끌기", 런처)
        self.assertIn("$AttachDragSource=", 런처)
        self.assertIn("Add_PreviewMouseLeftButtonDown", 런처)
        self.assertIn("Add_PreviewMouseMove", 런처)
        self.assertIn("MinimumHorizontalDragDistance", 런처)
        self.assertIn("[System.Windows.DataObject]::new", 런처)
        self.assertIn("[System.Windows.DragDrop]::DoDragDrop", 런처)
        self.assertIn("Write-GuiRuntimeError 'style review drag move'", 런처)
        self.assertNotIn("Write-GuiRuntimeError 'style review child drop'", 런처)
        self.assertIn("$eventArgs.Handled=$true", 런처)
        self.assertIn("[System.Windows.Input.MouseButtonState]::Pressed", 런처)
        self.assertNotIn("$DragHandle.Add_MouseLeftButtonDown", 런처)
        self.assertIn("$RowContainer.AllowDrop=$false", 런처)
        self.assertIn("$HeaderBorder.AllowDrop=$true", 런처)
        self.assertIn("govoffice-candidate:", 런처)
        self.assertIn("govoffice-group:", 런처)
        self.assertIn("$HeaderContext=[pscustomobject]@{row=$GroupRows[0];actions=$ReviewActions;guide=$Guide", 런처)
        self.assertIn("$RowContext=[pscustomobject]@{row=$row;actions=$ReviewActions;guide=$Guide", 런처)
        self.assertIn("& ($context.actions.MoveChild) $sourceId $context.row", 런처)
        self.assertIn("& ($context.actions.MoveGroup) $sourceGroup $context.row", 런처)
        self.assertNotIn("actions.Merge", 런처)
        self.assertNotIn("actions.MergeGroup", 런처)
        self.assertIn("$this.Tag.guide.Text", 런처)
        self.assertIn("구조 이동 되돌리기", 런처)
        self.assertIn("GOVOFFICE_LAYOUT_PREVIEW_DRAG_SELFTEST", 런처)
        self.assertIn("DRAG_REVIEW_SELFTEST_OK", 런처)
        self.assertIn("하위필드 연속 구조 이동 자체검증에 실패했습니다", 런처)
        self.assertIn("자동 병합하지 않았습니다", 런처)
        self.assertIn("preview_third", 런처)
        self.assertIn("candidate_field_overrides=$review.candidate_field_overrides", 런처)
        self.assertIn("candidate_field_overrides=$fieldOverrides", 런처)
        self.assertIn("target_parent=[string]$move.target_parent", 런처)
        self.assertIn("apply_candidate_field_overrides(", 백엔드)
        self.assertIn('command.get("candidate_field_overrides", {})', 백엔드)
        self.assertIn('구조 이동 방식', (PROJECT / "src" / "govoffice" / "services" / "hwpml_table_analysis.py").read_text(encoding="utf-8"))

    def test_wpf_이벤트_오류는_기록하고_프로그램을_강제종료하지_않는다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("gui_runtime_errors.log", 런처)
        self.assertIn("function Write-GuiRuntimeError", 런처)
        self.assertIn("Add_DispatcherUnhandledException", 런처)
        self.assertIn("$eventArgs.Handled=$true", 런처)
        self.assertIn("Write-GuiRuntimeError 'WPF dispatcher event'", 런처)
        self.assertIn("Write-GuiRuntimeError 'main window ShowDialog'", 런처)
        self.assertIn("finally{try{$AppMutex.ReleaseMutex()}", 런처)
        self.assertIn("GOVOFFICE_LAYOUT_PREVIEW_EXCEPTION_SELFTEST", 런처)
        self.assertIn("DISPATCHER_EXCEPTION_SELFTEST_OK", 런처)

    def test_구조이동_결과를_행과_대표필드와_저장버튼에_계속_표시한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("original_fields=$originalFields", 런처)
        self.assertIn("move_kinds=$moveKinds", 런처)
        self.assertIn("✓ 구조 이동 적용 중", 런처)
        self.assertIn("값과 필드명은 합쳐지지 않습니다", 런처)
        self.assertIn("✓ 구조 이동", 런처)
        self.assertIn("✓ 이동됨", 런처)
        self.assertIn("하위필드 이동", 런처)
        self.assertIn("대표필드 구조 이동", 런처)
        self.assertIn("구조 이동 되돌리기 ($($CandidateOverrides.Count))", 런처)
        self.assertIn("구조 이동 $($CandidateOverrides.Count)개 반영 후 저장", 런처)

    def test_후보에_없는_값은_한글에서_직접선택해_exact후보로_추가한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")
        수동창 = 런처.split("function Open-ManualStyleCandidate", 1)[1].split(
            "function Open-StyleCaptureReview", 1
        )[0]

        self.assertIn("직접 항목 추가", 런처)
        self.assertIn("한글에서 값 선택", 런처)
        self.assertIn("action='style_preset_manual_selection_begin'", 런처)
        self.assertIn("selection_token=$script:ManualSelectionToken", 런처)
        self.assertIn("$Import.IsEnabled=$false", 런처)
        self.assertIn(
            "if(-not $script:ManualSelectionToken){[void](Send-Backend "
            "@{action='style_preset_selection_clear'})}",
            런처,
        )
        self.assertIn("action='style_preset_manual_candidate'", 런처)
        self.assertIn("action='style_preset_selection_probe'", 수동창)
        self.assertIn("ForegroundProcessId", 수동창)
        self.assertIn('action == "style_preset_manual_candidate"', 백엔드)
        self.assertIn('한글.원본.대상.HAction.Run("Cancel")', 백엔드)
        self.assertIn("find_exact_value", 백엔드)
        self.assertIn("manual_token", 백엔드)
        self.assertIn("선택HWPML본문텍스트", 백엔드)
        self.assertIn("후보locator겹침", 백엔드)
        self.assertIn("conflicting_candidate_ids", 백엔드)
        self.assertIn("본문 $([int]$candidate.row+1)번째 문단", 런처)
        self.assertIn('"document_key": 문서키', 백엔드)
        self.assertIn('"document_key": 분석문서키', 백엔드)
        self.assertIn("선택캐시가현재문서인가", 백엔드)
        self.assertIn('활성문서id = 상태.get("active_document_id")', 백엔드)
        self.assertIn("if not isinstance(활성문서id, str) or not 활성문서id.strip()", 백엔드)
        self.assertIn("문서키가현재문서인가", 백엔드)
        self.assertIn("if not 문서키가현재문서인가(분석문서키)", 백엔드)
        self.assertGreaterEqual(
            백엔드.count('not 문서키가현재문서인가(_서식초안.get("document_key"))'),
            3,
        )
        self.assertIn("한글 문서가 변경되었습니다. 저장할 영역을 다시 분석하세요.", 백엔드)

    def test_프리셋검토가_기존값과_새추천을_구분하고_새값을_프로필에_합친다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn("이동 손잡이를 원하는 대표필드 제목 위에 놓으세요", 런처)
        self.assertIn("대표필드추가", 백엔드)
        self.assertIn("대표필드값추가", 백엔드)
        self.assertIn("별칭추가", 백엔드)
        self.assertIn("사용자프로필저장소.저장(이전프로필)", 백엔드)
        self.assertIn("and 라벨소유자 is None", 백엔드)
        self.assertIn("occurrence_count", 백엔드)
        self.assertIn("$OptionsById", 런처)
        self.assertIn("$Options[[string]$alias]=$groupValues", 런처)

    def test_기존대표필드를_하위로_재배치하고_구조용대표필드를_빈값으로_저장한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        self.assertIn('action == "user_profile_field_parent_set"', 백엔드)
        self.assertIn("대표필드상위변경", 백엔드)
        self.assertIn("프로필 = 이전.대표필드추가(필드명)", 백엔드)
        self.assertIn("if 입력값:", 백엔드)
        self.assertIn("$SetParent.Content='상위 변경'", 런처)
        self.assertIn("구조용 대표필드는 비워도 됩니다", 런처)
        self.assertIn("parent_field_id=$parentId", 런처)

    def test_사용자탭에서_대표필드_여러값_별칭_기본값을_관리한다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        백엔드 = BACKEND.read_text(encoding="utf-8")

        for action in (
            "user_profile_aliases_set",
            "user_profile_default_set",
            "user_profile_field_delete",
        ):
            self.assertIn(f'action == "{action}"', 백엔드)
            self.assertIn(f"action='{action}'", 런처)
        self.assertIn("대표필드 · 입력값 · 별칭 관리", 런처)
        self.assertIn("별칭 전체 저장", 런처)
        self.assertIn("기본값 지정", 런처)
        self.assertNotIn("필드 병합", 런처)
        self.assertIn("그 필드의 하위 구조로 저장됩니다", 런처)
        self.assertIn("필드 삭제", 런처)
        self.assertIn("$group.aliases", 런처)
        self.assertIn("$DefaultsById", 런처)
        self.assertIn('"aliases": list(대표필드.별칭)', 백엔드)
        self.assertIn('"default": 대표필드.기본값', 백엔드)

    def test_GUI는_단일인스턴스로_프로필_동시덮어쓰기를_막는다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertIn("Local\\GovOfficeRecoveredApplication", 런처)
        self.assertIn("이미 실행 중입니다", 런처)
        self.assertIn("$AppMutex.ReleaseMutex()", 런처)

    def test_GUI백엔드_모든_응답은_작업별_유한_타임아웃으로_읽는다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")

        self.assertNotIn("StandardOutput.ReadLine()", 런처)
        self.assertIn("StandardOutput.ReadLineAsync()", 런처)
        self.assertIn("function Wait-BackendLineTask", 런처)
        self.assertIn("$ReadTask.Wait($TimeoutMilliseconds)", 런처)
        self.assertIn("function Get-BackendRequestTimeout", 런처)
        self.assertIn("'hwp_document_status','style_preset_selection_status'", 런처)
        self.assertIn("'style_preset_analyze','style_preset_capture','style_preset_apply'", 런처)
        self.assertIn("$TimeoutMilliseconds=Get-BackendRequestTimeout $Command", 런처)

    def test_타임아웃은_백엔드를_정리하고_오염세션의_재시작을_막는다(self):
        런처 = LAUNCHER.read_text(encoding="utf-8-sig")
        전송구간 = 런처.split("function Send-Backend", 1)[1].split("[xml]$Xaml", 1)[0]

        self.assertIn("$Cleaned=Stop-BackendProcess -Process $script:Backend", 전송구간)
        self.assertIn("$WasTimeout=$Failure.Exception -is [System.TimeoutException]", 전송구간)
        self.assertIn("if($script:BackendUnhealthy)", 전송구간)
        self.assertIn("if($Action -ne 'connect')", 전송구간)
        self.assertIn("[void](Start-BackendProcess)", 전송구간)
        self.assertIn("상단의 다시 연결", 전송구간)
        self.assertIn("if($WasTimeout){", 전송구간)
        self.assertIn("$script:BackendUnhealthy=$true", 전송구간)
        self.assertIn("한글 작업 상태를 확인할 수 없습니다", 전송구간)
        self.assertIn("범정부오피스를 완전히 종료하고 다시 실행하세요", 전송구간)
        self.assertIn("$Process.StandardInput.Close()", 런처)
        self.assertIn("$Process.WaitForExit(750)", 런처)
        self.assertIn("$Process.Kill()", 런처)
        self.assertIn("Stop-BackendProcess -Process $script:Backend -RequestShutdown $true", 런처)

    def test_가짜_응답task와_프로세스에서_타임아웃과_정리가_실제로_유한하다(self):
        launcher_path = str(LAUNCHER).replace("'", "''")
        harness = rf"""
$ErrorActionPreference='Stop'
$tokens=$null
$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile('{launcher_path}',[ref]$tokens,[ref]$errors)
if($errors.Count -gt 0){{throw ($errors | ForEach-Object Message | Out-String)}}
$wanted=@('ConvertTo-AsciiJson','Get-BackendRequestTimeout','Wait-BackendLineTask','Stop-BackendProcess')
$definitions=$ast.FindAll({{param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -in $wanted}},$true)
foreach($definition in $definitions){{. ([scriptblock]::Create($definition.Extent.Text))}}
foreach($name in $wanted){{if(-not (Get-Command $name -ErrorAction SilentlyContinue)){{throw "missing:$name"}}}}

$pending=[System.Threading.Tasks.TaskCompletionSource[string]]::new()
$clock=[System.Diagnostics.Stopwatch]::StartNew()
$timedOut=$false
try{{[void](Wait-BackendLineTask -ReadTask $pending.Task -TimeoutMilliseconds 80 -Context 'fake')}}catch [System.TimeoutException]{{$timedOut=$true}}
$clock.Stop()
if(-not $timedOut){{throw 'pending task did not time out'}}
if($clock.ElapsedMilliseconds -gt 1500){{throw "timeout was not bounded: $($clock.ElapsedMilliseconds)"}}
$completed=[System.Threading.Tasks.TaskCompletionSource[string]]::new()
$completed.SetResult('ready')
if((Wait-BackendLineTask -ReadTask $completed.Task -TimeoutMilliseconds 500 -Context 'fake') -ne 'ready'){{throw 'completed task result mismatch'}}

$info=[System.Diagnostics.ProcessStartInfo]::new()
$info.FileName=(Get-Command powershell.exe).Source
$info.Arguments='-NoProfile -Command "Start-Sleep -Seconds 30"'
$info.UseShellExecute=$false
$info.CreateNoWindow=$true
$info.RedirectStandardInput=$true
$info.RedirectStandardOutput=$true
$info.RedirectStandardError=$true
$fake=[System.Diagnostics.Process]::Start($info)
$fakePid=$fake.Id
$script:Backend=$fake
$script:BackendUnhealthy=$false
$cleanupClock=[System.Diagnostics.Stopwatch]::StartNew()
$cleaned=Stop-BackendProcess -Process $fake
$cleanupClock.Stop()
if(-not $cleaned){{throw 'fake backend cleanup failed'}}
if($null -ne $script:Backend){{throw 'backend reference was not cleared'}}
if(Get-Process -Id $fakePid -ErrorAction SilentlyContinue){{throw 'fake backend process is still alive'}}
if($cleanupClock.ElapsedMilliseconds -gt 5000){{throw "cleanup was not bounded: $($cleanupClock.ElapsedMilliseconds)"}}

$result=[ordered]@{{
    timed_out=$timedOut
    wait_ms=$clock.ElapsedMilliseconds
    cleaned=$cleaned
    cleanup_ms=$cleanupClock.ElapsedMilliseconds
    quick_timeout=(Get-BackendRequestTimeout @{{action='hwp_document_status'}})
    long_timeout=(Get-BackendRequestTimeout @{{action='style_preset_apply'}})
}}
Write-Output ('HARNESS:' + ($result | ConvertTo-Json -Compress))
"""
        encoded = base64.b64encode(harness.encode("utf-16le")).decode("ascii")
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded],
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        result_line = next(
            (line for line in result.stdout.splitlines() if line.startswith("HARNESS:")),
            None,
        )
        self.assertIsNotNone(result_line, result.stdout)
        payload = json.loads(result_line.removeprefix("HARNESS:"))
        self.assertTrue(payload["timed_out"])
        self.assertTrue(payload["cleaned"])
        self.assertLess(payload["wait_ms"], 1500)
        self.assertLess(payload["cleanup_ms"], 5000)
        self.assertEqual(5000, payload["quick_timeout"])
        self.assertEqual(30000, payload["long_timeout"])


if __name__ == "__main__":
    unittest.main()
