import copy
import ast
from pathlib import Path
import time
from types import SimpleNamespace
import unittest

from govoffice.domain.user_profile import 사용자프로필
from govoffice.services.style_review_fields import normalize_review_fields
from govoffice.services.hwpml_table_analysis import HWPMLTableFieldAnalyzer
from govoffice.services.hwpml_table_analysis import apply_candidate_field_overrides
from govoffice.services.style_presets import HWPML등록필드분류기
from govoffice.services.user_profile import 사용자프로필서비스


def candidate(id, path, value, **extra):
    return dict(candidate_id=id, field=path, field_path=path, value=value,
                recommended=True, locator={"segments": [{"element_path": [id]}]}, **extra)


class ReviewFieldsTest(unittest.TestCase):
    def test_same_parent_across_tables_body_and_direct_values_has_one_identity(self):
        source = [
            candidate("t1", "연구자 정보 > 성명", "홍길동", structural_parent_field="연구자 정보", label="성명", table=0),
            candidate("p1", "연구자 정보 > 전화", "010-1111-1111", table=-1),
            candidate("t2", "연구자 정보 > 성명", "김하늘", table=1),
            candidate("direct", "연구자 정보", "담당 연구자", table=-1),
        ]
        original = copy.deepcopy(source)
        result = normalize_review_fields(source, 사용자프로필())
        self.assertEqual(1, len({c["semantic_group_id"] for c in result}))
        self.assertEqual(result[0]["semantic_child_id"], result[2]["semantic_child_id"])
        self.assertEqual("", result[3]["semantic_child_field"])
        self.assertEqual(source, original)
        for before, after in zip(source, result):
            for key in ("candidate_id", "value", "locator", "recommended", "table"):
                self.assertEqual(before[key], after[key])
        self.assertEqual(result, normalize_review_fields(result, 사용자프로필()))

    def test_existing_parent_and_scoped_aliases_are_reused_without_profile_mutation(self):
        profile = 사용자프로필().대표필드추가("연구자 정보", 별칭=("연구인력",))
        parent = profile.대표필드찾기("연구자 정보")
        profile = profile.대표필드추가("성명", ("기존 사용자",), 별칭=("이름",), 상위필드=parent.id)
        leaf = profile.대표필드찾기("연구자 정보 > 성명")
        before = profile.사전()
        result = normalize_review_fields([
            candidate("a", "연구인력 > 이름", "홍길동"),
            candidate("b", "전화", "010-2222-2222", structural_parent_field="연구인력", label="전화"),
            candidate("c", "연구자 정보 > 성명", "김하늘"),
        ], profile)
        self.assertEqual(before, profile.사전())
        self.assertEqual(["연구자 정보 > 성명", "연구자 정보 > 전화", "연구자 정보 > 성명"], [c["field"] for c in result])
        self.assertEqual({f"profile-group:{parent.id}"}, {c["semantic_group_id"] for c in result})
        self.assertEqual(leaf.id, result[0]["profile_field_id"])
        self.assertIsNone(result[1]["profile_field_id"])
        self.assertEqual(parent.id, result[1]["parent_profile_field_id"])
        self.assertEqual(("기존 사용자",), profile.필드값찾기("연구자 정보 > 성명"))

    def test_same_leaf_under_different_ancestors_stays_separate(self):
        source = [
            candidate("a", "책임자 > 연락처 > 전화", "111", structural_parent_field="연락처"),
            candidate("b", "참여자 > 연락처 > 전화", "222", structural_parent_field="연락처"),
        ]
        result = normalize_review_fields(source, 사용자프로필())
        self.assertNotEqual(result[0]["semantic_group_id"], result[1]["semantic_group_id"])
        self.assertEqual([s["field"] for s in source], [s["field"] for s in result])

    def test_scoped_parent_is_not_replaced_by_its_own_parent(self):
        profile = 사용자프로필().대표필드추가("책임자")
        profile = profile.대표필드추가("연락처", 상위필드=profile.대표필드찾기("책임자").id)
        contact = profile.대표필드찾기("책임자 > 연락처")
        result = normalize_review_fields([
            candidate("a", "책임자 > 연락처 > 전화", "111", structural_parent_field="연락처"),
        ], profile)
        self.assertEqual("책임자 > 연락처", result[0]["semantic_representative_field"])
        self.assertEqual(f"profile-group:{contact.id}", result[0]["semantic_group_id"])

    def test_whitespace_variants_share_path_without_losing_values_or_selection(self):
        a = candidate("a", " 연구자  정보>성명 ", "홍길동")
        b = candidate("b", "연구자 정보 > 성명", "김하늘")
        b["recommended"] = False
        result = normalize_review_fields([a, b], 사용자프로필())
        self.assertEqual(result[0]["semantic_group_id"], result[1]["semantic_group_id"])
        self.assertEqual(result[0]["semantic_child_id"], result[1]["semantic_child_id"])
        self.assertEqual([True, False], [c["recommended"] for c in result])
        self.assertEqual(["홍길동", "김하늘"], [c["value"] for c in result])

    def test_real_mixed_table_and_body_analysis_reuses_registered_parent(self):
        profile = 사용자프로필().대표필드추가("연구자 정보")
        parent = profile.대표필드찾기("연구자 정보")
        profile = profile.대표필드추가("성명", 상위필드=parent.id)
        profile = profile.대표필드추가("전화번호", 상위필드=parent.id)
        def p(text):
            return f"<P><TEXT><CHAR>{text}</CHAR></TEXT></P>"
        def table(value):
            return f"<TABLE><ROW><CELL>{p('연구자 정보 > 성명')}</CELL><CELL>{p(value)}</CELL></ROW></TABLE>"
        xml = f"<HWPML><BODY><SECTION>{table('홍길동')}{p('연구자 정보 > 전화번호: 010-1234-1234')}{table('김하늘')}</SECTION></BODY></HWPML>"
        raw = HWPMLTableFieldAnalyzer().analyze(xml, registered_fields=[profile.필드경로(f) for f in profile.대표필드목록]).as_dict()["candidates"]
        result = normalize_review_fields(raw, profile)
        self.assertEqual(3, len(result))
        self.assertEqual(["홍길동", "010-1234-1234", "김하늘"], [c["value"] for c in result])
        self.assertEqual({f"profile-group:{parent.id}"}, {c["semantic_group_id"] for c in result})
        self.assertEqual(3, len({str(c["locator"]) for c in result}))

    def test_capture_handler_adds_selected_values_to_existing_field_without_overwrite(self):
        profile = 사용자프로필().대표필드추가("연구자 정보")
        parent = profile.대표필드찾기("연구자 정보")
        profile = profile.대표필드추가("성명", ("기존 사용자",), 상위필드=parent.id)
        leaf = profile.대표필드찾기("연구자 정보 > 성명")
        xml = "<HWPML><BODY><SECTION>" + "".join(
            f"<TABLE><ROW><CELL><P><TEXT><CHAR>연구자 정보 &gt; 성명</CHAR></TEXT></P></CELL>"
            f"<CELL><P><TEXT><CHAR>{value}</CHAR></TEXT></P></CELL></ROW></TABLE>"
            for value in ("홍길동", "김하늘")
        ) + "</SECTION></BODY></HWPML>"
        raw = HWPMLTableFieldAnalyzer().analyze(xml, registered_fields=("연구자 정보 > 성명",)).as_dict()["candidates"]
        candidates = normalize_review_fields(raw, profile)
        self.assertEqual(2, len(candidates))
        backend = Path(__file__).resolve().parents[2] / "gui_backend.py"
        tree = ast.parse(backend.read_text(encoding="utf-8"))
        handler = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "처리")
        code = compile(ast.Module(body=[handler], type_ignores=[]), str(backend), "exec")

        class MemoryStore:
            def __init__(self):
                self.profile = profile
                self.writes = 0

            def 불러오기(self):
                return self.profile

            def 저장(self, value):
                self.profile = value
                self.writes += 1

        for selected_count in (1, 2):
            with self.subTest(selected_count=selected_count):
                store = MemoryStore()
                captured = []
                def capture(name, source, chosen, **kwargs):
                    captured.extend(chosen)
                    return SimpleNamespace(id="test", 이름=name, 필드수=1, 생성시각="test", 범위="user", 내용정책="original")
                namespace = dict(
                    time=time, apply_candidate_field_overrides=apply_candidate_field_overrides,
                    사용자프로필서비스=사용자프로필서비스, 사용자프로필저장소=store,
                    HWPML등록필드분류기=HWPML등록필드분류기,
                    서식프리셋=SimpleNamespace(선택후보저장=capture),
                    서식프리셋준비=lambda: None, 서식복사취소=lambda: None,
                    문서키가현재문서인가=lambda key: True, 응답=lambda *args, **kwargs: None,
                    _서식초안유효초=900,
                    _서식초안=dict(id="draft", created_at=time.monotonic(), document_key="doc",
                                 profile_snapshot=profile.사전(), hwpml=xml, candidates=candidates),
                )
                exec(code, namespace)
                self.assertEqual(0, store.writes)
                namespace["처리"](dict(action="style_preset_capture", name="test", draft_id="draft",
                                      selected_candidate_ids=[c["candidate_id"] for c in candidates[:selected_count]]))
                self.assertEqual(1, store.writes)
                self.assertEqual(leaf.id, store.profile.대표필드찾기("연구자 정보 > 성명").id)
                self.assertEqual(("기존 사용자", *["홍길동", "김하늘"][:selected_count]), store.profile.필드값찾기("연구자 정보 > 성명"))
                self.assertEqual(len(profile.대표필드목록), len(store.profile.대표필드목록))
                self.assertEqual([c["locator"] for c in candidates[:selected_count]], [c["locator"] for c in captured])


if __name__ == "__main__":
    unittest.main()
