from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from dataclasses import asdict, replace
from pathlib import Path

from govoffice.services.hwpml_table_analysis import (
    HWPMLTableFieldAnalyzer,
    apply_candidate_field_overrides,
    group_related_candidates,
    select_review_candidates,
)
from govoffice.services.style_presets import HWPML등록필드분류기


def cell(text: str, **attributes: int) -> str:
    attrs = " ".join(f'{name}="{value}"' for name, value in attributes.items())
    return f"<CELL {attrs}><P><TEXT><CHAR>{text}</CHAR></TEXT></P></CELL>"


def table(*rows: str, title: str | None = None) -> str:
    heading = f"<P><TEXT><CHAR>{title}</CHAR></TEXT></P>" if title else ""
    return f"<HWPML><BODY><SECTION>{heading}<TABLE>{''.join(rows)}</TABLE></SECTION></BODY></HWPML>"


def row(*cells: str) -> str:
    return f"<ROW>{''.join(cells)}</ROW>"


class HWPMLTableFieldAnalyzerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = HWPMLTableFieldAnalyzer()

    def test_검토후보는_확정을_전부남기고_미확정만_최대10개로_제한한다(self):
        source = [
            {
                "candidate_id": f"candidate-{index}",
                "recommended": index % 3 != 0,
                "registered": index % 2 == 0,
                "confidence": 0.7 + index / 100,
                "table": 0,
                "row": index,
                "col": 0,
            }
            for index in range(45)
        ]

        result = select_review_candidates(source)

        confirmed = [candidate for candidate in result if candidate["recommended"]]
        unconfirmed = [candidate for candidate in result if not candidate["recommended"]]
        self.assertEqual(30, len(confirmed))
        self.assertEqual(10, len(unconfirmed))
        self.assertEqual(40, len(result))
        self.assertTrue(any(candidate["candidate_id"] == "candidate-0" for candidate in result))

    def test_검토후보는_등록여부와_신뢰도와_무관하게_문서발견순서를_유지한다(self):
        source = [
            {
                "candidate_id": "top-new",
                "recommended": True,
                "registered": False,
                "confidence": 0.81,
            },
            {
                "candidate_id": "middle-unconfirmed",
                "recommended": False,
                "registered": False,
                "confidence": 0.2,
            },
            {
                "candidate_id": "bottom-registered",
                "recommended": True,
                "registered": True,
                "confidence": 0.99,
            },
        ]

        result = select_review_candidates(source, unconfirmed_limit=1)

        self.assertEqual(
            ["top-new", "middle-unconfirmed", "bottom-registered"],
            [candidate["candidate_id"] for candidate in result],
        )

    def test_분석결과는_위쪽신규필드를_아래쪽등록필드보다_먼저_반환한다(self):
        source = table(
            row(cell("기관구분"), cell("대학교")),
            row(cell("이름"), cell("홍길동")),
        )

        result = self.analyzer.analyze(source, registered_fields=("이름",))

        self.assertEqual(
            ["기관구분", "이름"],
            [candidate.field for candidate in result.candidates],
        )
        self.assertEqual(
            ["기관구분", "이름"],
            [candidate["field"] for candidate in result.as_dict()["candidates"]],
        )

    def test_사용자가_옮긴_하위필드는_이름과_위치를_유지하고_부모만_바꾼다(self):
        source = (
            {
                "candidate_id": "source",
                "field": "연구자명",
                "field_path": "연구자 정보 > 연구자명",
                "canonical_field": "연구자 정보 > 연구자명",
                "profile_field_id": "source-id",
                "parent_profile_field_id": "source-parent-id",
                "value": "홍길동",
                "locator": {"segments": ({"start": 0, "end": 3},)},
            },
            {
                "candidate_id": "target",
                "field": "책임자 정보 > 성명",
                "value": "김하늘",
            },
        )

        result = apply_candidate_field_overrides(
            source,
            {
                "source": {
                    "field": "책임자 정보 > 연구자명",
                    "kind": "child",
                    "target_parent": "책임자 정보",
                }
            },
        )

        self.assertEqual("책임자 정보 > 연구자명", result[0]["field"])
        self.assertEqual("책임자 정보 > 연구자명", result[0]["field_path"])
        self.assertEqual("책임자 정보 > 연구자명", result[0]["canonical_field"])
        self.assertEqual("연구자 정보 > 연구자명", result[0]["source_field_path"])
        self.assertEqual("source-id", result[0]["source_profile_field_id"])
        self.assertEqual("source-parent-id", result[0]["source_parent_profile_field_id"])
        self.assertEqual("child", result[0]["structure_move_kind"])
        self.assertEqual("책임자 정보", result[0]["structure_target_parent"])
        self.assertIsNone(result[0]["profile_field_id"])
        self.assertIsNone(result[0]["parent_profile_field_id"])
        self.assertEqual(source[0]["locator"], result[0]["locator"])
        self.assertEqual("연구자명", source[0]["field"])
        self.assertEqual("책임자 정보 > 성명", result[1]["field"])

    def test_대표묶음의_하위필드들을_대상에_직접_옮기는_저장정보를_처리한다(self):
        source = tuple(
            {
                "candidate_id": f"child-{index}",
                "field": f"사업 정보 > {name}",
                "field_path": f"사업 정보 > {name}",
                "semantic_representative_field": "사업 정보",
                "semantic_child_field": name,
                "profile_field_id": f"stable-{index}",
                "parent_profile_field_id": "old-parent",
                "value": value,
                "locator": {"segments": ({"start": index, "end": index + 1},)},
            }
            for index, (name, value) in enumerate((("사업명", "문서 자동화"), ("연락처", "010-1234-1234")))
        )
        result = apply_candidate_field_overrides(
            source,
            {
                item["candidate_id"]: {
                    "field": f"연구자 정보 > {item['semantic_child_field']}",
                    "kind": "child",
                    "target_parent": "연구자 정보",
                }
                for item in source
            },
        )
        self.assertEqual(
            ["연구자 정보 > 사업명", "연구자 정보 > 연락처"],
            [item["field_path"] for item in result],
        )
        for original, moved in zip(source, result):
            self.assertEqual(original["value"], moved["value"])
            self.assertEqual(original["locator"], moved["locator"])
            self.assertEqual(original["profile_field_id"], moved["source_profile_field_id"])
            self.assertEqual("child", moved["structure_move_kind"])
            self.assertEqual("연구자 정보", moved["structure_target_parent"])
            self.assertTrue(original["field_path"].startswith("사업 정보 > "))

    def test_구조이동은_없는후보와_빈필드명을_거부한다(self):
        source = ({"candidate_id": "known", "field": "과제명", "value": "A"},)

        with self.assertRaisesRegex(ValueError, "없는 후보"):
            apply_candidate_field_overrides(
                source,
                {"missing": {"field": "사업 정보 > 과제명", "kind": "child", "target_parent": "사업 정보"}},
            )
        with self.assertRaisesRegex(ValueError, "필드명이 올바르지"):
            apply_candidate_field_overrides(
                source,
                {"known": {"field": "  ", "kind": "child", "target_parent": "사업 정보"}},
            )
        with self.assertRaisesRegex(ValueError, "기존 필드명을 유지"):
            apply_candidate_field_overrides(
                source,
                {"known": {"field": "사업 정보 > 사업명", "kind": "child", "target_parent": "사업 정보"}},
            )

    def test_병합구조_후보는_미확정이어도_개수제한없이_전부_검토한다(self):
        structural = [
            {
                "candidate_id": f"structural-{index}",
                "recommended": False,
                "classification_basis": "merged_structure",
                "confidence": 0.95,
                "table": 0,
                "row": index,
                "col": 0,
            }
            for index in range(15)
        ]
        generic = [
            {
                "candidate_id": f"generic-{index}",
                "recommended": False,
                "classification_basis": "semantic",
                "confidence": 0.7,
                "table": 1,
                "row": index,
                "col": 0,
            }
            for index in range(15)
        ]

        result = select_review_candidates((*structural, *generic))

        self.assertEqual(15, sum(item["candidate_id"].startswith("structural-") for item in result))
        self.assertEqual(10, sum(item["candidate_id"].startswith("generic-") for item in result))

    def test_같은_프로필필드와_같은값은_관계묶음으로만_연결한다(self):
        source = [
            {
                "candidate_id": "name-1",
                "field": "성함",
                "value": "홍길동",
                "profile_field_id": "person-name",
                "recommended": True,
            },
            {
                "candidate_id": "name-2",
                "field": "연구자명",
                "value": "홍길동",
                "profile_field_id": "person-name",
                "recommended": False,
            },
            {
                "candidate_id": "phone-1",
                "field": "전화번호",
                "value": "홍길동",
                "profile_field_id": "phone",
                "recommended": True,
            },
            {
                "candidate_id": "name-3",
                "field": "성함",
                "value": "김길동",
                "profile_field_id": "legacy-name",
                "recommended": False,
            },
        ]

        result = group_related_candidates(source)

        self.assertEqual(4, len(result))
        self.assertEqual(4, len({item["candidate_id"] for item in result}))
        self.assertEqual(1, len({item["relationship_cluster_id"] for item in result}))
        self.assertEqual(1, len({item["relationship_sort_rank"] for item in result}))
        self.assertEqual(("동일 값", "동일 필드"), result[0]["relationship_reasons"])
        self.assertEqual(
            [True, False, True, False],
            [item["recommended"] for item in result],
        )
        self.assertEqual(
            ["성함", "연구자명", "전화번호", "성함"],
            [item["field"] for item in result],
        )
        self.assertEqual([0, 1, 2, 3], [item["document_order"] for item in result])
        self.assertEqual([0, 0, 0, 0], [item["relationship_anchor_order"] for item in result])

    def test_유사한_필드나_값도_검토관계로_묶고_무관한후보는_분리한다(self):
        source = [
            {
                "candidate_id": "lead-1",
                "field": "연구책임자명",
                "value": "김하늘",
            },
            {
                "candidate_id": "lead-2",
                "field": "연구책임자",
                "value": "박바다",
            },
            {
                "candidate_id": "org-1",
                "field": "소속기관",
                "value": "서울과학기술대학교",
            },
            {
                "candidate_id": "org-2",
                "field": "주관기관",
                "value": "서울과학기술대학",
            },
            {
                "candidate_id": "unrelated",
                "field": "사업기간",
                "value": "2026년",
            },
        ]

        result = {item["candidate_id"]: item for item in group_related_candidates(source)}

        self.assertEqual(
            result["lead-1"]["relationship_cluster_id"],
            result["lead-2"]["relationship_cluster_id"],
        )
        self.assertIn("유사 필드", result["lead-1"]["relationship_reasons"])
        self.assertEqual(
            result["org-1"]["relationship_cluster_id"],
            result["org-2"]["relationship_cluster_id"],
        )
        self.assertIn("유사 값", result["org-1"]["relationship_reasons"])
        self.assertEqual(0, result["lead-1"]["relationship_sort_rank"])
        self.assertEqual(1, result["org-1"]["relationship_sort_rank"])
        self.assertEqual(2, result["unrelated"]["relationship_sort_rank"])
        self.assertNotEqual(
            result["unrelated"]["relationship_cluster_id"],
            result["lead-1"]["relationship_cluster_id"],
        )
        self.assertNotEqual(
            result["unrelated"]["relationship_cluster_id"],
            result["org-1"]["relationship_cluster_id"],
        )

    def test_빈필드와_빈값은_서로_관계후보로_합치지_않는다(self):
        result = group_related_candidates(
            (
                {"candidate_id": "empty-1", "field": "", "value": ""},
                {"candidate_id": "empty-2", "field": "", "value": ""},
            )
        )

        self.assertNotEqual(
            result[0]["relationship_cluster_id"],
            result[1]["relationship_cluster_id"],
        )

    def test_셀서식은_불명확한_라벨과_값을_문서내_표본으로_보조판별한다(self):
        source = (
            '<HWPML><BODY><TABLE>'
            '<ROW><CELL ShadeColor="#D9EAF7"><P><CHAR>이름</CHAR></P></CELL>'
            '<CELL ShadeColor="#FFFFFF"><P><CHAR>홍길동</CHAR></P></CELL></ROW>'
            '<ROW><CELL ShadeColor="#D9EAF7"><P><CHAR>ABC123</CHAR></P></CELL>'
            '<CELL ShadeColor="#FFFFFF"><P><CHAR>새 값</CHAR></P></CELL></ROW>'
            '</TABLE></BODY></HWPML>'
        )

        result = self.analyzer.analyze(source, registered_fields=("이름",))
        style_candidate = next(item for item in result.candidates if item.label == "ABC123")

        self.assertEqual("cell_style", style_candidate.classification_basis)
        self.assertEqual("새 값", style_candidate.value)
        self.assertNotEqual(
            style_candidate.label_style.signature,
            style_candidate.value_style.signature,
        )
        self.assertIn(style_candidate.label_style.signature, result.style_rules["field"])
        self.assertIn(style_candidate.value_style.signature, result.style_rules["value"])

    def test_가로_병합셀은_대표필드이고_바로아래_라벨은_하위필드다(self):
        source = table(
            row(cell("연구책임자", RowAddr=0, ColAddr=0, ColSpan=4)),
            row(
                cell("성명", RowAddr=1, ColAddr=0),
                cell("홍길동", RowAddr=1, ColAddr=1),
                cell("직위", RowAddr=1, ColAddr=2),
                cell("교수", RowAddr=1, ColAddr=3),
            ),
            title="표 밖 제목은 부모가 아님",
        )

        result = self.analyzer.analyze(source)
        recommended = {item.label: item.field for item in result.candidates if item.recommended}

        self.assertEqual("연구책임자 > 성명", recommended["성명"])
        self.assertEqual("연구책임자 > 직위", recommended["직위"])
        self.assertNotIn("표 밖 제목", " ".join(recommended.values()))
        grouped = [
            item
            for item in result.candidates
            if item.label in {"성명", "직위"}
        ]
        self.assertEqual(1, len({item.structural_group_id for item in grouped}))
        self.assertTrue(
            all(item.structural_parent_field == "연구책임자" for item in grouped)
        )

    def test_떨어진_셀은_필드값이나_대표하위관계로_묶지_않는다(self):
        source = table(
            row(
                cell("하위필드", RowAddr=0, ColAddr=0),
                cell("관련없는값", RowAddr=0, ColAddr=2),
            ),
        )

        result = self.analyzer.analyze(source, registered_fields=("하위필드",))

        self.assertFalse(
            any(
                item.label == "하위필드" and item.value == "관련없는값"
                for item in result.candidates
            )
        )

    def test_병합대표필드_옆의_문구제한없는_모든쌍을_수집하고_자리표시자는_제외한다(self):
        긴필드 = ("2026년도 숫자와 문장부호?!가 포함된 매우 긴 하위필드 이름 " * 2).strip()
        source = table(
            row(
                cell("상위구분", RowAddr=0, ColAddr=0, RowSpan=2),
                cell(긴필드, RowAddr=0, ColAddr=1),
                cell("짧은 한글 값", RowAddr=0, ColAddr=2),
                cell("코드123", RowAddr=0, ColAddr=3),
                cell("A-2026", RowAddr=0, ColAddr=4),
            ),
            row(
                cell("설명문입니다.", RowAddr=1, ColAddr=1),
                cell("사용자가 판단할 값", RowAddr=1, ColAddr=2),
                cell("빈자리", RowAddr=1, ColAddr=3),
                cell("-", RowAddr=1, ColAddr=4),
            ),
        )

        result = self.analyzer.analyze(source)
        structural = [
            item
            for item in result.candidates
            if item.classification_basis == "merged_structure"
        ]

        self.assertEqual(
            {
                (긴필드, "짧은 한글 값"),
                ("코드123", "A-2026"),
                ("설명문입니다.", "사용자가 판단할 값"),
            },
            {(candidate.label, candidate.value) for candidate in structural},
        )
        self.assertTrue(all(item.recommended for item in structural))
        self.assertEqual(
            {
                긴필드,
                "코드123",
                "설명문입니다.",
            },
            {item.label for item in structural},
        )
        self.assertEqual(
            {
                "짧은 한글 값",
                "A-2026",
                "사용자가 판단할 값",
            },
            {item.value for item in structural},
        )
        self.assertTrue(all(item.parent_field == "상위구분" for item in structural))
        self.assertTrue(all(item.field_path == item.field for item in structural))
        # 값으로 소비된 셀은 뒤에서 다시 필드가 될 수 없다.
        self.assertFalse(
            {item.value for item in structural} & {item.label for item in structural}
        )
        self.assertFalse(any(item.value == "-" for item in result.candidates))

    @staticmethod
    def assert_candidates_do_not_overlap(candidates) -> None:
        occupied = []
        for candidate in candidates:
            for segment in candidate.locator.segments:
                for path, slot, start, end, candidate_id in occupied:
                    same_slot = path == segment.element_path and slot == segment.text_slot
                    overlaps = max(start, segment.start) < min(end, segment.end)
                    if same_slot and overlaps:
                        raise AssertionError(
                            f"{candidate_id} and {candidate.candidate_id} overlap"
                        )
                occupied.append(
                    (
                        segment.element_path,
                        segment.text_slot,
                        segment.start,
                        segment.end,
                        candidate.candidate_id,
                    )
                )

    def test_registered_aliases_map_horizontal_cells_to_canonical_fields(self):
        source = table(
            row(cell("성명"), cell("홍길동")),
            row(cell("전자우편"), cell("hong@example.com")),
        )

        result = self.analyzer.analyze(
            source,
            registered_fields={"이름": ("기존값",), "이메일": ()},
            aliases={"이름": ("이름", "성명", "성함"), "이메일": ("전자우편",)},
        )

        self.assertEqual([], list(result.unregistered_candidates))
        self.assertEqual(["이름", "이메일"], [item.field for item in result.registered_candidates])
        self.assertEqual(["right", "right"], [item.direction for item in result.registered_candidates])
        self.assertTrue(all(item.registered and item.recommended for item in result.candidates))
        self.assertEqual([(0, 0), (1, 0)], [(item.row, item.col) for item in result.candidates])
        self.assertEqual([(0, 1), (1, 1)], [(item.value_row, item.value_col) for item in result.candidates])

    def test_each_label_cell_chooses_below_or_right_in_a_mixed_table(self):
        source = table(
            row(cell("과제명"), cell("책임자")),
            row(cell("범정부오피스"), cell("김철수")),
            row(cell("연락처"), cell("010-1234-5678")),
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("과제명", "책임자", "전화번호"),
            aliases={"전화번호": ("연락처",)},
        )
        by_field = {item.field: item for item in result.registered_candidates}

        self.assertEqual("below", by_field["과제명"].direction)
        self.assertEqual("범정부오피스", by_field["과제명"].value)
        self.assertEqual("below", by_field["책임자"].direction)
        self.assertEqual("김철수", by_field["책임자"].value)
        self.assertEqual("right", by_field["전화번호"].direction)
        self.assertEqual("010-1234-5678", by_field["전화번호"].value)

    def test_inline_value_uses_nearby_title_to_suggest_a_role_field(self):
        source = table(
            row(cell("성명: 김철수")),
            title="연구책임자 정보",
        )

        result = self.analyzer.analyze(source)
        self.assertEqual(0, len(result.registered_candidates))
        self.assertEqual(1, len(result.unregistered_candidates))
        candidate = result.unregistered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("성명", candidate.label)
        self.assertEqual("김철수", candidate.value)
        self.assertEqual("inline", candidate.direction)
        self.assertEqual("연구책임자 정보", candidate.context_title)
        self.assertTrue(candidate.recommended)

    def test_title_role_overrides_the_registered_generic_name_alias(self):
        source = table(
            row(cell("성명: 김철수")),
            title="연구책임자 정보",
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명", "성함")},
        )

        self.assertEqual(0, len(result.registered_candidates))
        candidate = result.unregistered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("성명", candidate.label)
        self.assertFalse(candidate.registered)
        self.assertTrue(candidate.recommended)

    def test_registered_title_role_becomes_the_canonical_registered_field(self):
        source = table(
            row(cell("성명: 김철수")),
            title="연구책임자 정보",
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름", "연구책임자"),
            aliases={"이름": ("성명", "성함")},
        )

        self.assertEqual(0, len(result.unregistered_candidates))
        candidate = result.registered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("성명", candidate.label)
        self.assertTrue(candidate.registered)
        self.assertTrue(candidate.recommended)

    def test_multiple_nearby_headings_form_role_then_subtitle_context(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P>"
            "<P><TEXT><CHAR>연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명", "성함")},
        )

        self.assertEqual(0, len(result.registered_candidates))
        candidate = result.unregistered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("연구책임자 > 연락 정보", candidate.context_title)
        self.assertTrue(candidate.recommended)

    def test_long_body_paragraph_stops_older_role_context(self):
        body_text = (
            "이 문단은 표의 제목이 아니며 연구책임자의 연락 정보를 "
            "작성하는 방법을 사용자에게 자세히 설명하기 위한 일반 본문입니다."
        )
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P>"
            f"<P><TEXT><CHAR>{body_text}</CHAR></TEXT></P>"
            "<P><TEXT><CHAR>연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.registered_candidates[0]
        self.assertEqual("이름", candidate.field)
        self.assertEqual("연락 정보", candidate.context_title)

    def test_previous_table_is_a_hard_title_context_boundary(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('과제명'), cell('범정부오피스'))}</TABLE>"
            "<P><TEXT><CHAR>연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름", "과제명"),
            aliases={"이름": ("성명",)},
        )

        candidate = next(item for item in result.candidates if item.table == 1)
        self.assertEqual("이름", candidate.field)
        self.assertEqual("연락 정보", candidate.context_title)

    def test_different_section_does_not_supply_title_context(self):
        source = (
            "<HWPML><BODY>"
            "<SECTION><P><TEXT><CHAR>연구책임자</CHAR></TEXT></P></SECTION>"
            "<SECTION>"
            "<P><TEXT><CHAR>연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.registered_candidates[0]
        self.assertEqual("이름", candidate.field)
        self.assertEqual("연락 정보", candidate.context_title)

    def test_multiple_blank_paragraphs_make_a_heading_too_distant(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P>"
            "<P/><P/>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.registered_candidates[0]
        self.assertEqual("이름", candidate.field)
        self.assertIsNone(candidate.context_title)

    def test_xml_detail_nodes_do_not_make_an_adjacent_heading_distant(self):
        detail_nodes = "".join("<MARK/>" for _ in range(130))
        source = (
            "<HWPML><BODY><SECTION>"
            f"<P><TEXT><CHAR>연구책임자{detail_nodes}</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.unregistered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("연구책임자", candidate.context_title)

    def test_table_wrapper_text_after_the_table_is_not_a_nearby_title(self):
        source = (
            "<HWPML><BODY><SECTION><P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "<TEXT><CHAR>연구책임자</CHAR></TEXT>"
            "</P></SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.registered_candidates[0]
        self.assertEqual("이름", candidate.field)
        self.assertIsNone(candidate.context_title)

    def test_table_wrapper_does_not_consume_the_one_allowed_blank_paragraph(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P><P/>"
            f"<P><TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE></P>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.unregistered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("연구책임자", candidate.context_title)

    def test_peer_role_titles_do_not_form_a_false_hierarchy(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P>"
            "<P><TEXT><CHAR>참여연구자</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.unregistered_candidates[0]
        self.assertEqual("참여연구자", candidate.field)
        self.assertEqual("참여연구자", candidate.context_title)

    def test_page_break_stops_the_older_role_title(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>연구책임자</CHAR></TEXT></P>"
            "<P PageBreak=\"true\"><TEXT><CHAR>연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.registered_candidates[0]
        self.assertEqual("이름", candidate.field)
        self.assertEqual("연락 정보", candidate.context_title)

    def test_outline_levels_prove_a_parent_child_title_hierarchy(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P HeadingType=\"Outline\" Level=\"0\"><TEXT><CHAR>"
            "연구책임자</CHAR></TEXT></P>"
            "<P HeadingType=\"Outline\" Level=\"1\"><TEXT><CHAR>"
            "연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.unregistered_candidates[0]
        self.assertEqual("연구책임자", candidate.field)
        self.assertEqual("연구책임자 > 연락 정보", candidate.context_title)

    def test_same_outline_level_keeps_only_the_nearest_title(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P HeadingType=\"Outline\" Level=\"1\"><TEXT><CHAR>"
            "연구책임자</CHAR></TEXT></P>"
            "<P HeadingType=\"Outline\" Level=\"1\"><TEXT><CHAR>"
            "연락 정보</CHAR></TEXT></P>"
            f"<TABLE>{row(cell('성명'), cell('홍길동'))}</TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )

        candidate = result.registered_candidates[0]
        self.assertEqual("이름", candidate.field)
        self.assertEqual("연락 정보", candidate.context_title)

    def test_title_role_falls_back_when_local_context_has_no_role(self):
        source = table(
            row(
                cell("연락처", RowAddr=0, ColAddr=0, RowSpan=2),
                cell("성명", RowAddr=0, ColAddr=1),
                cell("홍길동", RowAddr=0, ColAddr=2),
            ),
            row(
                cell("전자우편", RowAddr=1, ColAddr=1),
                cell("owner@example.com", RowAddr=1, ColAddr=2),
            ),
            title="연구책임자 정보",
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름", "이메일"),
            aliases={"이름": ("성명",), "이메일": ("전자우편",)},
        )

        by_label = {item.label: item for item in result.candidates if item.recommended}
        self.assertEqual("연락처 > 성명", by_label["성명"].field)

    def test_rowspan_and_colspan_are_used_as_cell_ranges_not_fixed_columns(self):
        source = table(
            row(
                cell("부서명", RowAddr=0, ColAddr=0, RowSpan=2, ColSpan=2),
                cell("정보화전략팀", RowAddr=0, ColAddr=2, RowSpan=2, ColSpan=3),
            )
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("부서",),
            aliases={"부서": ("부서명",)},
        )
        candidate = result.registered_candidates[0]
        self.assertEqual("right", candidate.direction)
        self.assertEqual((0, 0), (candidate.row, candidate.col))
        self.assertEqual((0, 2), (candidate.value_row, candidate.value_col))
        self.assertEqual("정보화전략팀", candidate.value)

    def test_same_value_for_different_fields_has_unique_ids_and_exact_locators(self):
        source = table(
            row(cell("책임자"), cell("홍길동")),
            row(cell("연구자"), cell("홍길동")),
        )

        result = self.analyzer.analyze(source, registered_fields=("책임자", "연구자"))
        self.assertEqual(2, len(result.registered_candidates))
        first, second = result.registered_candidates
        self.assertNotEqual(first.candidate_id, second.candidate_id)
        self.assertNotEqual(first.locator.segments[0].element_path, second.locator.segments[0].element_path)
        self.assertEqual((0, 1), (first.locator.row, first.locator.col))
        self.assertEqual((1, 1), (second.locator.row, second.locator.col))
        for candidate in result.candidates:
            self.assertEqual(
                candidate.value,
                "".join(segment.text for segment in candidate.locator.segments),
            )

    def test_same_slot_candidates_keep_distinct_offsets_and_occurrences(self):
        source = table(
            row(cell("책임자: 홍길동\n연구자: 홍길동")),
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("책임자", "연구자"),
        )
        self.assertEqual(2, len(result.registered_candidates))
        first, second = result.registered_candidates
        self.assertNotEqual(first.candidate_id, second.candidate_id)
        self.assertEqual(1, first.locator.occurrence)
        self.assertEqual(2, second.locator.occurrence)
        first_segment = first.locator.segments[0]
        second_segment = second.locator.segments[0]
        self.assertEqual(first_segment.element_path, second_segment.element_path)
        self.assertEqual(first_segment.text_slot, second_segment.text_slot)
        self.assertLess(first_segment.end, second_segment.start)

    def test_locator_spans_multiple_text_slots_and_selects_only_the_value_range(self):
        source = (
            "<HWPML><BODY><SECTION><TABLE><ROW><CELL>"
            "<P><TEXT><CHAR>성명: 홍<MARK/>길</CHAR><CHAR>동</CHAR></TEXT></P>"
            "</CELL></ROW></TABLE></SECTION></BODY></HWPML>"
        )

        candidate = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        ).registered_candidates[0]

        self.assertEqual("홍길동", candidate.value)
        self.assertGreaterEqual(len(candidate.locator.segments), 3)
        self.assertEqual(
            candidate.value,
            "".join(segment.text for segment in candidate.locator.segments),
        )
        root = ET.fromstring(source)
        for segment in candidate.locator.segments:
            element = root
            for child_index in segment.element_path:
                element = element[child_index]
            slot = getattr(element, segment.text_slot)
            self.assertEqual(segment.text, slot[segment.start : segment.end])

    def test_alias_collision_is_unregistered_and_not_auto_recommended(self):
        source = table(row(cell("성명"), cell("홍길동")))

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름", "책임자"),
            aliases={"이름": ("성명",), "책임자": ("성명",)},
        )

        self.assertEqual(0, len(result.registered_candidates))
        candidate = result.unregistered_candidates[0]
        self.assertEqual("성명", candidate.field)
        self.assertFalse(candidate.recommended)

    def test_overlapping_candidates_keep_only_the_clear_stronger_recommendation(self):
        source = table(
            row(
                cell("책임자", RowAddr=0, ColAddr=0, ColSpan=2),
                cell("홍길동", RowAddr=0, ColAddr=2, RowSpan=2),
            ),
            row(cell("연구자", RowAddr=1, ColAddr=0)),
            row(
                cell("과제명", RowAddr=2, ColAddr=0),
                cell("범정부오피스", RowAddr=2, ColAddr=1),
            ),
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("책임자", "연구자", "과제명"),
        )
        by_field = {candidate.field: candidate for candidate in result.candidates}

        self.assertGreater(by_field["책임자"].confidence, by_field["연구자"].confidence)
        self.assertTrue(by_field["책임자"].recommended)
        self.assertFalse(by_field["연구자"].recommended)
        self.assertTrue(by_field["과제명"].recommended)
        recommended = [candidate for candidate in result.candidates if candidate.recommended]
        self.assert_candidates_do_not_overlap(recommended)

    def test_tied_overlapping_candidates_are_all_left_for_user_review(self):
        source = table(
            row(
                cell("책임자", RowAddr=0, ColAddr=0),
                cell("홍길동", RowAddr=0, ColAddr=1, RowSpan=2),
            ),
            row(cell("연구자", RowAddr=1, ColAddr=0)),
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("책임자", "연구자"),
        )

        self.assertEqual(2, len(result.candidates))
        self.assertEqual(
            result.candidates[0].confidence,
            result.candidates[1].confidence,
        )
        self.assertFalse(any(candidate.recommended for candidate in result.candidates))
        self.assert_candidates_do_not_overlap(
            [candidate for candidate in result.candidates if candidate.recommended]
        )

    def test_result_and_nested_locator_dataclasses_are_json_serializable(self):
        source = table(row(cell("과제명"), cell("범정부오피스")))
        result = self.analyzer.analyze(source, registered_fields=("과제명",))

        json.dumps(result.as_dict(), ensure_ascii=False)
        json.dumps(asdict(result.candidates[0]), ensure_ascii=False)
        payload = result.as_dict()["candidates"][0]
        self.assertIn("candidate_id", payload)
        self.assertIn("locator", payload)
        self.assertIn("segments", payload["locator"])

    def test_empty_or_broken_hwpml_is_rejected_without_calling_hwp(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            self.analyzer.analyze("  ")
        with self.assertRaisesRegex(ValueError, "cannot be parsed"):
            self.analyzer.analyze("<HWPML>")

    def test_clear_inline_fields_outside_tables_use_exact_locators_without_duplicates(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>성명: 홍<MARK/>길동</CHAR></TEXT></P>"
            "<P><TEXT><CHAR>임시표현: ABC-01</CHAR></TEXT></P>"
            "<TABLE><ROW><CELL><P><TEXT><CHAR>성명: 표안값</CHAR>"
            "</TEXT></P></CELL></ROW></TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름",),
            aliases={"이름": ("성명",)},
        )
        outside = [candidate for candidate in result.candidates if candidate.table == -1]
        inside = [candidate for candidate in result.candidates if candidate.table >= 0]

        self.assertEqual(2, len(outside))
        self.assertEqual(1, len(inside))
        name = next(candidate for candidate in outside if candidate.label == "성명")
        uncertain = next(candidate for candidate in outside if candidate.label == "임시표현")
        self.assertEqual("이름", name.field)
        self.assertTrue(name.registered)
        self.assertTrue(name.recommended)
        self.assertGreaterEqual(len(name.locator.segments), 2)
        self.assertEqual(
            name.value,
            "".join(segment.text for segment in name.locator.segments),
        )
        self.assertFalse(uncertain.registered)
        self.assertFalse(uncertain.recommended)
        self.assertTrue(all(candidate.candidate_id.startswith("p") for candidate in outside))

    def test_saved_values_are_reverse_indexed_with_ids_and_ambiguous_owners(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>고유 저장값</CHAR></TEXT></P>"
            "<TABLE><ROW><CELL><P><TEXT><CHAR>공유 저장값</CHAR>"
            "</TEXT></P></CELL></ROW></TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_values=(
                {
                    "id": "field_project",
                    "대표필드명": "과제명",
                    "값목록": ("고유 저장값",),
                },
                {
                    "id": "field_owner",
                    "대표필드명": "책임자",
                    "값목록": ("공유 저장값",),
                },
                {
                    "id": "field_researcher",
                    "대표필드명": "연구자",
                    "값목록": ("공유 저장값",),
                },
            ),
        )

        self.assertEqual(3, len(result.registered_candidates))
        unique = next(item for item in result.candidates if item.field == "과제명")
        shared = [item for item in result.candidates if item.value == "공유 저장값"]
        self.assertEqual(-1, unique.table)
        self.assertEqual("field_project", unique.profile_field_id)
        self.assertTrue(unique.recommended)
        self.assertEqual({"책임자", "연구자"}, {item.field for item in shared})
        self.assertEqual(
            {"field_owner", "field_researcher"},
            {item.profile_field_id for item in shared},
        )
        self.assertFalse(any(item.recommended for item in shared))
        for candidate in result.candidates:
            self.assertEqual(
                candidate.value,
                "".join(segment.text for segment in candidate.locator.segments),
            )

    def test_saved_value_map_uses_word_boundaries_and_label_candidate_wins_dedup(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>서울특별시 / 서울</CHAR></TEXT></P>"
            "<TABLE><ROW>"
            f"{cell('과제명')}{cell('범정부오피스')}"
            "</ROW></TABLE></SECTION></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("과제명",),
            registered_values=(
                {"대표필드명": "지역", "값목록": ("서울",)},
                {
                    "id": "stable-project-id",
                    "대표필드명": "과제명",
                    "값목록": ("범정부오피스",),
                },
            ),
        )

        region_candidates = [item for item in result.candidates if item.field == "지역"]
        project_candidates = [item for item in result.candidates if item.field == "과제명"]
        self.assertEqual(1, len(region_candidates))
        self.assertEqual("서울", region_candidates[0].locator.segments[0].text)
        self.assertEqual(1, len(project_candidates))
        self.assertEqual("과제명", project_candidates[0].label)
        self.assertEqual("right", project_candidates[0].direction)
        self.assertEqual("stable-project-id", project_candidates[0].profile_field_id)
        self.assertTrue(project_candidates[0].recommended)

    def test_manual_exact_search_finds_a_partial_word_across_text_slots(self):
        source = (
            "<HWPML><BODY><TABLE><ROW><CELL><P><TEXT>"
            "<CHAR>연구<MARK/>과</CHAR><CHAR>제명</CHAR>"
            "</TEXT></P></CELL></ROW></TABLE></BODY></HWPML>"
        )

        candidates = self.analyzer.find_exact_value(
            source,
            "연구과제",
            "과제명",
            profile_field_id="field_project",
        )

        self.assertEqual(1, len(candidates))
        candidate = candidates[0]
        self.assertEqual("연구과제", candidate.value)
        self.assertEqual("과제명", candidate.field)
        self.assertEqual("field_project", candidate.profile_field_id)
        self.assertFalse(candidate.recommended)
        self.assertGreaterEqual(len(candidate.locator.segments), 3)
        self.assertEqual(
            candidate.value,
            "".join(segment.text for segment in candidate.locator.segments),
        )

    def test_manual_exact_search_does_not_reject_hyphen_placeholders(self):
        source = (
            "<HWPML><BODY><SECTION>"
            "<P><TEXT><CHAR>-</CHAR></TEXT></P>"
            "<TABLE><ROW><CELL><P><TEXT><CHAR>-</CHAR></TEXT></P>"
            "</CELL></ROW></TABLE>"
            "</SECTION></BODY></HWPML>"
        )

        candidates = self.analyzer.정확값찾기(source, "-", "기타 지원금")

        self.assertEqual(2, len(candidates))
        self.assertEqual({-1, 0}, {candidate.table for candidate in candidates})
        self.assertTrue(all(candidate.registered for candidate in candidates))
        self.assertFalse(any(candidate.recommended for candidate in candidates))
        self.assertTrue(
            all(candidate.locator.segments[0].text == "-" for candidate in candidates)
        )

    def test_manual_exact_search_returns_overlaps_in_paragraphs_without_char(self):
        source = "<HWPML><BODY><P><TEXT>ababa</TEXT></P></BODY></HWPML>"

        candidates = self.analyzer.find_exact_value(source, "aba", "pattern")

        self.assertEqual(2, len(candidates))
        self.assertEqual(
            [0, 2],
            [candidate.locator.segments[0].start for candidate in candidates],
        )
        self.assertEqual(2, len({candidate.candidate_id for candidate in candidates}))
        self.assertEqual([1, 2], [candidate.locator.occurrence for candidate in candidates])

    def test_nonrecommended_bridge_does_not_suppress_disjoint_recommendations(self):
        source = "<HWPML><BODY><P><CHAR>abcdefg</CHAR></P></BODY></HWPML>"
        left = replace(
            self.analyzer.find_exact_value(source, "abc", "left")[0],
            recommended=True,
            confidence=0.9,
        )
        bridge = replace(
            self.analyzer.find_exact_value(source, "cde", "bridge")[0],
            recommended=False,
            confidence=0.6,
        )
        right = replace(
            self.analyzer.find_exact_value(source, "efg", "right")[0],
            recommended=True,
            confidence=0.85,
        )

        resolved = self.analyzer._resolve_recommendation_overlaps(
            (left, bridge, right)
        )
        by_field = {candidate.field: candidate for candidate in resolved}

        self.assertTrue(by_field["left"].recommended)
        self.assertFalse(by_field["bridge"].recommended)
        self.assertTrue(by_field["right"].recommended)

    def test_weaker_recommended_bridge_only_suppresses_its_direct_conflict(self):
        source = "<HWPML><BODY><P><CHAR>abcdefg</CHAR></P></BODY></HWPML>"
        left = replace(
            self.analyzer.find_exact_value(source, "abc", "left")[0],
            recommended=True,
            confidence=0.9,
        )
        bridge = replace(
            self.analyzer.find_exact_value(source, "cde", "bridge")[0],
            recommended=True,
            confidence=0.8,
        )
        right = replace(
            self.analyzer.find_exact_value(source, "efg", "right")[0],
            recommended=True,
            confidence=0.7,
        )

        resolved = self.analyzer._resolve_recommendation_overlaps(
            (left, bridge, right)
        )
        by_field = {candidate.field: candidate for candidate in resolved}

        self.assertTrue(by_field["left"].recommended)
        self.assertFalse(by_field["bridge"].recommended)
        self.assertTrue(by_field["right"].recommended)
        self.assert_candidates_do_not_overlap(
            [candidate for candidate in resolved if candidate.recommended]
        )

    def test_registered_value_map_allows_reserved_canonical_names(self):
        source = (
            "<HWPML><BODY><P><CHAR>Alice</CHAR></P>"
            "<P><CHAR>X</CHAR></P></BODY></HWPML>"
        )

        result = self.analyzer.analyze(
            source,
            registered_values={"name": ("Alice",), "values": ("X",)},
        )

        self.assertEqual({"name", "values"}, {item.field for item in result.candidates})

    def test_short_numeric_saved_value_is_not_taken_from_a_structured_number(self):
        source = "<HWPML><BODY><P><CHAR>코드 02-56-1234 / 56</CHAR></P></BODY></HWPML>"

        result = self.analyzer.analyze(
            source,
            registered_values={"짧은코드": ("56",)},
        )

        candidates = [item for item in result.candidates if item.field == "짧은코드"]
        self.assertEqual(1, len(candidates))
        self.assertFalse(candidates[0].recommended)

    def test_nested_role_group_namespaces_every_person_attribute(self):
        source = table(
            row(
                cell("연구책임자", RowAddr=0, ColAddr=0, RowSpan=2, ColSpan=2),
                cell("성명", RowAddr=0, ColAddr=2),
                cell("김철수", RowAddr=0, ColAddr=3),
                cell("연락처", RowAddr=0, ColAddr=4, RowSpan=2),
                cell("직장전화", RowAddr=0, ColAddr=5),
                cell("02-000-0000", RowAddr=0, ColAddr=6),
            ),
            row(
                cell("전자우편", RowAddr=1, ColAddr=5),
                cell("owner@example.com", RowAddr=1, ColAddr=6),
            ),
        )

        result = self.analyzer.analyze(
            source,
            registered_fields=("이름", "전화번호", "이메일"),
            aliases={
                "이름": ("성명",),
                "전화번호": ("직장전화",),
                "이메일": ("전자우편",),
            },
        )
        recommended = {item.label: item for item in result.candidates if item.recommended}

        self.assertEqual("연구책임자 > 성명", recommended["성명"].field)
        self.assertEqual("연락처 > 직장전화", recommended["직장전화"].field)
        self.assertEqual("연락처 > 전자우편", recommended["전자우편"].field)
        self.assertIn("연락처", recommended["직장전화"].field)

    def test_actual_research_plan_semantics_do_not_recommend_neighboring_headers(self):
        preset_dir = Path(__file__).resolve().parents[2] / "config" / "style_presets"
        matches = sorted(preset_dir.glob("style_05df258377*.hml"))
        if not matches:
            self.skipTest("semantic regression HWPML fixture is not installed")
        source = matches[0].read_text(encoding="utf-8")
        result = self.analyzer.analyze(
            source,
            registered_fields=("이름", "전화번호", "이메일", "연구개발과제명"),
            aliases={
                "이름": ("성명", "성함"),
                "전화번호": ("연락처", "직장전화", "휴대전화"),
                "이메일": ("전자우편",),
            },
        )

        def at(
            row_index: int,
            col_index: int,
            value_row: int,
            value_col: int,
        ):
            found = [
                candidate
                for candidate in result.candidates
                if candidate.table == 4
                and candidate.row == row_index
                and candidate.col == col_index
                and candidate.value_row == value_row
                and candidate.value_col == value_col
            ]
            self.assertEqual(
                1,
                len(found),
                f"candidate t4 r{row_index}c{col_index} -> r{value_row}c{value_col}",
            )
            return found[0]

        def missing(
            row_index: int,
            col_index: int,
            value_row: int,
            value_col: int,
        ):
            self.assertFalse(
                any(
                    candidate.table == 4
                    and candidate.row == row_index
                    and candidate.col == col_index
                    and candidate.value_row == value_row
                    and candidate.value_col == value_col
                    for candidate in result.candidates
                )
            )

        # 병합 대표셀 자체와 '-' 자리표시자는 후보로 만들지 않는다.
        for coordinates in (
            (9, 0, 9, 6),
            (14, 6, 14, 8),
            (21, 4, 21, 7),
            (22, 13, 22, 20),
            (23, 13, 24, 13),
            (32, 0, 32, 6),
        ):
            missing(*coordinates)

        # 중간 대표셀이 아닌 실제 하위필드/값 쌍은 문구의 형태와 무관하게
        # 후보로 남겨 사용자가 선택 해제할 수 있게 한다.
        for coordinates in (
            (30, 27, 30, 29),
        ):
            candidate = at(*coordinates)
            self.assertTrue(candidate.recommended)
            self.assertEqual("merged_structure", candidate.classification_basis)

        # 빈 행이나 떨어진 행을 건너뛰어 임의의 값을 연결하지는 않는다.
        for coordinates in (
            (29, 27, 30, 27),
            (30, 29, 32, 27),
        ):
            missing(*coordinates)

        project_ko = at(9, 6, 9, 10)
        project_en = at(10, 6, 10, 10)
        owner_name = at(13, 6, 13, 12)
        owner_phone = at(14, 8, 14, 12)
        owner_mobile = at(14, 21, 14, 28)
        staff_name = at(32, 6, 32, 12)
        staff_phone = at(33, 8, 33, 12)
        staff_mobile = at(33, 19, 33, 27)
        institution_name = at(11, 6, 11, 10)
        institution_address = at(12, 6, 12, 10)
        government_cash = at(23, 4, 24, 4)
        institution_cash = at(23, 7, 24, 7)
        partner_cash = at(23, 20, 24, 20)
        stage_one_year_one = at(17, 9, 17, 11)
        stage_one_year_two = at(18, 9, 18, 11)
        stage_two_year_one = at(19, 9, 19, 11)
        stage_two_year_two = at(20, 9, 20, 11)

        self.assertEqual("연구개발과제명 > 국문", project_ko.field)
        self.assertEqual("연구개발과제명 > 영문", project_en.field)
        self.assertNotEqual(project_ko.field, project_en.field)
        self.assertEqual("연구책임자 > 성명", owner_name.field)
        self.assertEqual("연락처 > 직장전화", owner_phone.field)
        self.assertEqual("연락처 > 휴대전화", owner_mobile.field)
        self.assertNotEqual(owner_phone.field, owner_mobile.field)
        self.assertEqual("연구개발과제실무담당자 > 성명", staff_name.field)
        self.assertEqual("연락처 > 직장전화", staff_phone.field)
        self.assertEqual("연락처 > 휴대전화", staff_mobile.field)
        self.assertNotEqual(staff_phone.field, staff_mobile.field)
        self.assertEqual(owner_phone.field, staff_phone.field)
        self.assertEqual("주관연구개발기관 > 기관명", institution_name.field)
        self.assertEqual("주관연구개발기관 > 주소", institution_address.field)
        self.assertEqual("정부지원연구개발비 > 현금", government_cash.field)
        self.assertEqual("기관부담연구개발비 > 현금", institution_cash.field)
        self.assertEqual("기타(협력기업) > 현금", partner_cash.field)
        self.assertEqual("단계 > 1년차", stage_one_year_one.field)
        self.assertEqual("단계 > 2년차", stage_one_year_two.field)
        self.assertEqual("2단계 > 1년차", stage_two_year_one.field)
        self.assertEqual("단계 > 2년차", stage_two_year_two.field)
        self.assertNotEqual(stage_one_year_one.field, stage_two_year_one.field)
        self.assertEqual(stage_one_year_two.field, stage_two_year_two.field)
        self.assertFalse(government_cash.recommended)
        self.assertTrue(
            all(
                candidate.recommended
                for candidate in (
                    project_ko,
                    project_en,
                    owner_name,
                    owner_phone,
                    owner_mobile,
                    staff_name,
                    staff_phone,
                    staff_mobile,
                    institution_name,
                    institution_address,
                    institution_cash,
                    partner_cash,
                    stage_one_year_one,
                    stage_one_year_two,
                    stage_two_year_one,
                    stage_two_year_two,
                )
            )
        )
        self.assertFalse(
            any(
                candidate.recommended
                and (
                    self.analyzer._is_placeholder(candidate.value)
                    or candidate.label == candidate.value
                )
                for candidate in result.candidates
            )
        )
        recommended = [candidate for candidate in result.candidates if candidate.recommended]
        self.assert_candidates_do_not_overlap(recommended)
        for candidate in recommended:
            self.assertEqual(
                candidate.value,
                "".join(segment.text for segment in candidate.locator.segments),
            )

    def test_all_actual_hwpml_recommendations_can_be_exactly_tokenized(self):
        preset_dir = Path(__file__).resolve().parents[2] / "config" / "style_presets"
        hwpml_files = sorted(preset_dir.glob("*.hml"))
        if not hwpml_files:
            self.skipTest("actual HWPML preset fixtures are not installed")
        classifier = HWPML등록필드분류기()

        for hwpml_file in hwpml_files:
            with self.subTest(hwpml_file=hwpml_file.name):
                source = hwpml_file.read_text(encoding="utf-8")
                result = self.analyzer.analyze(source)
                recommended = [
                    candidate for candidate in result.candidates if candidate.recommended
                ]
                self.assert_candidates_do_not_overlap(recommended)
                classified = classifier.선택후보분류(source, recommended)
                self.assertEqual(
                    len({candidate.field for candidate in recommended}),
                    len(classified.필드목록),
                )


if __name__ == "__main__":
    unittest.main()
