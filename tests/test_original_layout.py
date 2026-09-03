import inspect
import json
import struct
import unittest
from pathlib import Path

from govoffice.adapters.recovered_hwp import _복구클래스


LAYOUT = Path(__file__).resolve().parents[1] / "config" / "original_layout.json"
ICON_ROOT = LAYOUT.parents[1] / "assets" / "icons"
LAUNCHER = LAYOUT.parents[1] / "launch_gui.ps1"
AFFECTED_INSTITUTIONS = {
    "buyeo",
    "chungnam",
    "gangwon",
    "gyeonggi",
    "gyeongnam",
    "hongseong",
    "sejong",
}


def png_dimensions(icon: str) -> tuple[int, int]:
    relative = icon.replace("\\", "/").removeprefix("아이콘/")
    header = ICON_ROOT.joinpath(*relative.split("/")).read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise AssertionError(f"PNG 아이콘이 아닙니다: {icon}")
    return struct.unpack(">II", header[16:24])


def active(buttons: list[dict]) -> list[dict]:
    return [button for button in buttons if button.get("enabled")]


def rectangle(button: dict, offset: tuple[int, int] = (0, 0)) -> tuple[int, int, int, int]:
    left = offset[0] + button["x"]
    top = offset[1] + button["y"]
    return left, top, left + button["width"], top + button["height"]


def rectangles_overlap(
    first: dict,
    second: dict,
    first_offset: tuple[int, int] = (0, 0),
    second_offset: tuple[int, int] = (0, 0),
) -> bool:
    left1, top1, right1, bottom1 = rectangle(first, first_offset)
    left2, top2, right2, bottom2 = rectangle(second, second_offset)
    return max(left1, left2) < min(right1, right2) and max(top1, top2) < min(bottom1, bottom2)


def duplicate_signature(button: dict) -> str:
    return json.dumps(
        {
            key: button.get(key)
            for key in ("name", "x", "y", "width", "height", "icon", "operations", "page_id")
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def iter_render_buttons(data: dict):
    for tab in data["tabs"]:
        yield from tab["buttons"]
    for institution in data["institutions"].values():
        layout = institution.get("layout")
        if not layout:
            yield from institution["layout_buttons"]
            continue
        yield from layout["base_buttons"]
        yield from layout["page_controls"]
        for page in layout["pages"]:
            yield from page["buttons"]


class 원본레이아웃시험(unittest.TestCase):
    def test_버튼크기는_원본_PNG_픽셀크기와_같다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        for button in iter_render_buttons(data):
            if not button.get("icon"):
                self.assertTrue(button.get("source_extension"), button["name"])
                continue
            self.assertEqual(png_dimensions(button["icon"]), (button["width"], button["height"]), button["name"])

    def test_메인탭_활성버튼은_콘텐츠영역에서_잘리지_않는다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        width = data["window"]["width"]
        height = data["window"]["content_height"]
        for tab in data["tabs"]:
            for button in (item for item in tab["buttons"] if item["enabled"]):
                self.assertGreaterEqual(button["x"], 0, button["name"])
                self.assertGreaterEqual(button["y"], 0, button["name"])
                self.assertLessEqual(button["x"] + button["width"], width, button["name"])
                self.assertLessEqual(button["y"] + button["height"], height, button["name"])

    def test_기관창은_콘텐츠범위와_작업영역에_맞춰진다(self):
        launcher = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("$LayoutSpec=$Institution.layout", launcher)
        self.assertIn("$NominalWidth", launcher)
        self.assertIn("$DialogScale=Get-FitScale", launcher)
        self.assertIn("$Viewbox.StretchDirection='DownOnly'", launcher)
        self.assertIn("SetZIndex($Close,100000)", launcher)

    def test_과거_겹침기관은_페이지구조로_분리됐다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        for institution_id in AFFECTED_INSTITUTIONS:
            with self.subTest(institution=institution_id):
                institution = data["institutions"][institution_id]
                layout = institution.get("layout")
                self.assertIsInstance(layout, dict)
                self.assertTrue(layout["pages"])
                self.assertTrue(layout["page_controls"])
                self.assertEqual(institution["layout_buttons"], layout["base_buttons"])

    def test_기관페이지_내부_활성버튼은_겹치지_않는다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        for institution_id, institution in data["institutions"].items():
            layout = institution.get("layout")
            if not layout:
                continue
            for page in layout["pages"]:
                buttons = active(page["buttons"])
                for index, first in enumerate(buttons):
                    for second in buttons[index + 1 :]:
                        with self.subTest(
                            institution=institution_id,
                            page=page["id"],
                            first=first["name"],
                            second=second["name"],
                        ):
                            self.assertFalse(rectangles_overlap(first, second))

    def test_기관_고정버튼과_페이지컨트롤은_서로_겹치지_않는다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        for institution_id, institution in data["institutions"].items():
            layout = institution.get("layout")
            if not layout:
                continue
            fixed = active(layout["base_buttons"]) + active(layout["page_controls"])
            for index, first in enumerate(fixed):
                for second in fixed[index + 1 :]:
                    with self.subTest(
                        institution=institution_id,
                        first=first["name"],
                        second=second["name"],
                    ):
                        self.assertFalse(rectangles_overlap(first, second))

    def test_선택페이지를_포함한_실제렌더범위도_겹치지_않는다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        for institution_id, institution in data["institutions"].items():
            layout = institution.get("layout")
            if not layout:
                continue
            fixed = active(layout["base_buttons"]) + active(layout["page_controls"])
            for page in layout["pages"]:
                frame = page["frame"]
                page_offset = (frame["x"], frame["y"])
                for fixed_button in fixed:
                    for page_button in active(page["buttons"]):
                        with self.subTest(
                            institution=institution_id,
                            page=page["id"],
                            fixed=fixed_button["name"],
                            page_button=page_button["name"],
                        ):
                            self.assertFalse(
                                rectangles_overlap(fixed_button, page_button, second_offset=page_offset)
                            )

    def test_활성버튼은_렌더범위별로_완전중복되지_않는다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        scopes = [(f"tab:{tab['id']}", active(tab["buttons"])) for tab in data["tabs"]]
        for institution_id, institution in data["institutions"].items():
            layout = institution.get("layout")
            if not layout:
                scopes.append((f"institution:{institution_id}:legacy", active(institution["layout_buttons"])))
                continue
            scopes.append(
                (
                    f"institution:{institution_id}:fixed",
                    active(layout["base_buttons"]) + active(layout["page_controls"]),
                )
            )
            scopes.extend(
                (f"institution:{institution_id}:page:{page['id']}", active(page["buttons"]))
                for page in layout["pages"]
            )
        for scope, buttons in scopes:
            signatures = [duplicate_signature(button) for button in buttons]
            with self.subTest(scope=scope):
                self.assertEqual(len(signatures), len(set(signatures)))

    def test_런처는_선택된_페이지하나만_렌더한다(self):
        launcher = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("$LayoutSpec=$Institution.layout", launcher)
        self.assertIn("$HasPagedLayout", launcher)
        self.assertIn("$PageState", launcher)
        self.assertIn("$ShowPage", launcher)
        self.assertIn("$Page=$PageMap[$PageId]", launcher)
        self.assertIn("$PageButtons=@($Page.buttons|Where-Object", launcher)
        self.assertIn("$Canvas.Children.Remove($PageState.Canvas)", launcher)
        self.assertIn("New-ImageButton $PageCanvas", launcher)

    def test_활성버튼은_모든_동작과_필수인자가_복원됐다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        recovered = _복구클래스()
        active = [button for tab in data["tabs"] for button in tab["buttons"] if button["enabled"]]
        self.assertEqual(328, len(active))
        for button in active:
            if button.get("institution_id"):
                continue
            self.assertTrue(button["operations"])
            for operation in button["operations"]:
                self.assertTrue(operation["allowed"])
                if operation["type"] != "method":
                    continue
                required = [
                    parameter
                    for parameter in inspect.signature(getattr(recovered, operation["method"])).parameters.values()
                    if parameter.name != "self"
                    and parameter.default is inspect.Parameter.empty
                    and parameter.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                ]
                self.assertGreaterEqual(len(operation["args"]), len(required), button["name"])

    def test_지자체버튼은_정상복구_기관기능만_연결한다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        institution_tab = next(tab for tab in data["tabs"] if tab["id"] == "지자체")
        active = [button for button in institution_tab["buttons"] if button["enabled"]]
        self.assertEqual(23, len(active))
        self.assertEqual(475, sum(len(item["functions"]) for item in data["institutions"].values()))
        for institution_id, institution in data["institutions"].items():
            layout = institution.get("layout")
            if not layout:
                continue
            with self.subTest(institution=institution_id):
                self.assertEqual(institution["layout_buttons"], layout["base_buttons"])

    def test_서울과기대는_교직탭에서_기관화면으로_진입한다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        education_tab = next(tab for tab in data["tabs"] if tab["id"] == "교직")
        button = next(item for item in education_tab["buttons"] if item.get("institution_id") == "seoultech")
        self.assertTrue(button["enabled"])
        self.assertTrue(button["source_extension"])
        self.assertEqual("서울과학기술대학교", data["institutions"]["seoultech"]["name"])
        features = data["institutions"]["seoultech"]["custom_features"]
        self.assertEqual("style_preset_manager", features[0]["action"])
        launcher = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("Open-StylePresetManager $Dialog", launcher)

    def test_서식프리셋은_상단공통버튼이_아니라_서울과기대_기관기능이다(self):
        launcher = LAUNCHER.read_text(encoding="utf-8")
        top_items = launcher.split("$TopItems = @(", 1)[1].split(")\nforeach($Item in $TopItems)", 1)[0]
        self.assertNotIn("tip='서식 프리셋'", top_items)
        self.assertIn("$Institution.custom_features", launcher)

    def test_개인탭은_기관과_분리되고_기본정보와_기타문서항목을_제공한다(self):
        launcher = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("'가이드','개인'", launcher)
        self.assertIn("function Render-PersonalTab", launcher)
        self.assertIn("action='user_profile_basic_save'", launcher)
        self.assertIn("action='user_profile_entry_add'", launcher)
        self.assertNotIn("$Dialog.DialogResult=$true;$Dialog.Close()", launcher)
        self.assertNotIn("function Refresh-PersonalView", launcher)
        self.assertIn("$RefreshPersonalView = {", launcher)
        self.assertIn("& $RefreshPersonalView", launcher)
        self.assertIn("function Open-DocumentFieldManager", launcher)
        self.assertIn("function Open-BasicProfileEditor", launcher)
        self.assertIn("출력 사용자 정보", launcher)
        self.assertIn("새 값 입력 · 관리", launcher)
        self.assertIn("if($Name -eq '개인')", launcher)

    def test_글자문단모양복사는_안내형_서식복사로_연결된다(self):
        data = json.loads(LAYOUT.read_text(encoding="utf-8"))
        text_tab = next(tab for tab in data["tabs"] if tab["id"] == "글자")
        button = next(item for item in text_tab["buttons"] if item["name"] == "글자문단모양복사")
        self.assertEqual("guided_format_copy", button["feature_id"])
        self.assertEqual("글자문단모양복사", button["operations"][0]["method"])
        launcher = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("function Invoke-FormatCopy", launcher)
        self.assertIn("$Item.feature_id -eq 'guided_format_copy'", launcher)

    def test_원본_콜백과_현재_연결표에_차이가_없다(self):
        report = json.loads((LAYOUT.parents[1] / "reports" / "button_binding_verification.json").read_text(encoding="utf-8"))
        self.assertEqual(0, report["differences"])
        self.assertEqual(0, report["operation_mismatches"])
        self.assertEqual(0, report["layout_button_missing"])
        self.assertEqual(1, report["source_extensions"])


if __name__ == "__main__":
    unittest.main()
