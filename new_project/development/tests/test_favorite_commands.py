import ast
from copy import deepcopy
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import io
import contextlib

from govoffice.adapters.json_favorites import JSON즐겨찾기저장소
from govoffice.services.favorite_commands import FavoriteCommands
from govoffice.services.favorites import 즐겨찾기서비스


LAYOUT = dict(tabs=[dict(id="표", buttons=[
    dict(name="서식", enabled=True, operations=[dict(type="method", method="크기", args=[11]), dict(type="h_action", command="ParagraphShapeAlignCenter")]),
    dict(name="제외", enabled=False, operations=[dict(type="method", method="크기", args=[1])]),
])], institutions={"school": dict(name="학교", functions=[dict(name="제목", method="제목", ui_ready=True, parameters=[])])})


class FavoriteCommandsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "favorites.json"
        self.store = JSON즐겨찾기저장소(self.path)
        self.service = FavoriteCommands(self.store, LAYOUT, {"크기", "제목"})
        self.basic, self.school = list(self.service.catalog.values())

    def save(self, entry=None, name="즐겨찾기"):
        entry = entry or self.basic
        return self.service.save(entry["id"], name, entry["operations"])

    def test_roundtrip_edit_order_delete_and_institution_filter(self):
        first = self.save()
        second = self.save(self.school, "학교 제목")
        self.assertEqual(2, len(self.service.catalog))
        self.assertEqual(first["id"], self.save()["id"])
        self.assertEqual(2, len(self.service.listing()))
        self.assertEqual(1, len(self.service.listing("other")))
        self.assertEqual(2, len(self.service.listing("school")))
        edited = deepcopy(first["operations"])
        edited[0]["args"] = [14]
        self.service.save(self.basic["id"], "14포인트", edited, first["id"])
        reopened = FavoriteCommands(JSON즐겨찾기저장소(self.path), LAYOUT, {"크기", "제목"})
        self.assertEqual([14], reopened.listing()[0]["operations"][0]["args"])
        self.assertEqual("14포인트", reopened.listing()[0]["name"])
        mutations = 즐겨찾기서비스(self.store, None)
        mutations.이동(second["id"], 0)
        self.assertEqual(second["id"], reopened.listing()[0]["id"])
        mutations.삭제(first["id"])
        self.assertEqual([second["id"]], [item["id"] for item in reopened.listing()])

    def test_invalid_edits_and_missing_ids_do_not_overwrite(self):
        saved = self.save()
        before = self.path.read_bytes()
        bad = deepcopy(saved["operations"])
        bad[0]["method"] = "임의실행"
        with self.assertRaises(ValueError):
            self.service.save(self.basic["id"], "bad", bad, saved["id"])
        bad = deepcopy(saved["operations"])
        bad[0]["args"] = ["not a number"]
        with self.assertRaises(ValueError):
            self.service.save(self.basic["id"], "bad", bad, saved["id"])
        with self.assertRaises(ValueError):
            self.service.save(self.basic["id"], "bad", saved["operations"], "missing")
        self.assertEqual(before, self.path.read_bytes())

    def test_retired_methods_are_visible_but_cannot_execute(self):
        saved = self.save()
        current = FavoriteCommands(self.store, LAYOUT, set())
        self.assertFalse(current.listing()[0]["available"])
        with self.assertRaises(ValueError):
            current.operations(current.find(saved["id"]))

    def test_integral_float_survives_powershell_json_roundtrip(self):
        layout = deepcopy(LAYOUT)
        layout["tabs"][0]["buttons"][0]["operations"][0]["args"] = [1.0]
        service = FavoriteCommands(self.store, layout, {"크기", "제목"})
        entry = next(iter(service.catalog.values()))
        operations = deepcopy(entry["operations"])
        operations[0]["args"] = [2]
        saved = service.save(entry["id"], "숫자", operations)
        self.assertIs(type(saved["operations"][0]["args"][0]), float)
        operations[0]["args"] = [True]
        with self.assertRaises(ValueError):
            service.save(entry["id"], "잘못된 숫자", operations)

    def test_backend_executes_saved_sequence_through_managed_document_path(self):
        saved = self.save()
        calls = []
        outputs = []
        hwp = SimpleNamespace(
            원본=SimpleNamespace(대상=SimpleNamespace(HAction=SimpleNamespace(Run=lambda command: calls.append(command)))),
            기능실행=lambda name, *args: calls.append((name, args)),
            관리작업추적실행=lambda fn: fn(),
        )
        ns = dict(즐겨찾기명령=self.service, 즐겨찾기저장소=self.store, 즐겨찾기서비스=즐겨찾기서비스,
                  응답=lambda *args, **kwargs: outputs.append((args, kwargs)),
                  한글=hwp, 연결=lambda: None, 선택상태무효화=lambda: None, 서식복사취소=lambda: None,
                  인자해석=lambda value: value, 허용기능={"크기", "제목"}, 필수인자목록=lambda *args: [],
                  io=io, contextlib=contextlib)
        tree = ast.parse((Path(__file__).resolve().parents[2] / "gui_backend.py").read_text(encoding="utf-8"))
        handler = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "처리")
        exec(compile(ast.Module(body=[handler], type_ignores=[]), "backend", "exec"), ns)
        ns["처리"](dict(action="favorite_run", id=saved["id"]))
        self.assertEqual([("크기", (11,)), "ParagraphShapeAlignCenter"], calls)
        self.assertTrue(outputs[-1][0][0])
        ns["처리"](dict(action="favorite_delete", id=saved["id"]))
        with self.assertRaises(ValueError):
            ns["처리"](dict(action="favorite_run", id=saved["id"]))
        self.assertEqual(2, len(calls))
