import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from govoffice.adapters.json_style_presets import JSON서식프리셋저장소
from govoffice.domain.presets import 서식필드, 서식프리셋


def 프리셋(이름: str, 본문: str, *, 필드: tuple[서식필드, ...] = ()) -> 서식프리셋:
    return 서식프리셋(
        id="style_atomic",
        이름=이름,
        hwpml=f"<HWPML><BODY><CHAR>{본문}</CHAR></BODY></HWPML>",
        필드목록=필드,
        생성시각="2026-09-01T00:00:00+00:00",
        범위="selection_page",
        내용정책="registered_fields" if 필드 else "original",
    )


class JSON서식프리셋쌍저장시험(unittest.TestCase):
    def test_두_임시파일을_fsync한_뒤_hml과_json_순으로_커밋한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            디렉터리 = Path(임시)
            저장소 = JSON서식프리셋저장소(디렉터리)
            사건 = []
            실제fsync = os.fsync
            실제replace = os.replace

            def fsync(파일번호):
                사건.append(("fsync", 파일번호))
                return 실제fsync(파일번호)

            def replace(원본, 대상):
                # 첫 승격 시점에 두 임시 파일의 쓰기가 이미 끝나 있다.
                if not any(항목[0] == "replace" for 항목 in 사건):
                    self.assertEqual(2, len(list(디렉터리.glob("*.new.*"))))
                사건.append(("replace", Path(원본).name, Path(대상).name))
                return 실제replace(원본, 대상)

            with patch(
                "govoffice.adapters.json_style_presets.os.fsync", side_effect=fsync
            ), patch(
                "govoffice.adapters.json_style_presets.os.replace", side_effect=replace
            ):
                저장소.저장(프리셋("새 프리셋", "새 본문"))

            첫교체 = next(순번 for 순번, 항목 in enumerate(사건) if 항목[0] == "replace")
            self.assertEqual(2, sum(항목[0] == "fsync" for 항목 in 사건[:첫교체]))
            교체대상 = [항목[2] for 항목 in 사건 if 항목[0] == "replace"]
            self.assertEqual(["style_atomic.hml", "style_atomic.json"], 교체대상)
            self.assertEqual("새 프리셋", 저장소.불러오기("style_atomic").이름)
            self.assertEqual([], list(디렉터리.glob(".*.new.*")))
            self.assertEqual([], list(디렉터리.glob(".*.backup.*")))

    def test_신규_json_커밋이_실패하면_노출된_반쪽_프리셋을_남기지_않는다(self):
        with tempfile.TemporaryDirectory() as 임시:
            디렉터리 = Path(임시)
            저장소 = JSON서식프리셋저장소(디렉터리)
            실제replace = os.replace

            def replace(원본, 대상):
                if Path(원본).name.endswith(".new.json"):
                    raise OSError("JSON 커밋 실패")
                return 실제replace(원본, 대상)

            with patch(
                "govoffice.adapters.json_style_presets.os.replace", side_effect=replace
            ):
                with self.assertRaisesRegex(ValueError, "style_atomic"):
                    저장소.저장(프리셋("실패", "저장되면 안 됨"))

            self.assertFalse((디렉터리 / "style_atomic.json").exists())
            self.assertFalse((디렉터리 / "style_atomic.hml").exists())
            self.assertEqual((), 저장소.목록())
            self.assertEqual([], list(디렉터리.iterdir()))

    def test_덮어쓰기_json_커밋이_실패하면_기존_쌍을_완전히_복구한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            디렉터리 = Path(임시)
            저장소 = JSON서식프리셋저장소(디렉터리)
            저장소.저장(프리셋("기존 프리셋", "기존 본문"))
            기존hml = (디렉터리 / "style_atomic.hml").read_bytes()
            기존json = (디렉터리 / "style_atomic.json").read_bytes()
            실제replace = os.replace

            def replace(원본, 대상):
                if Path(원본).name.endswith(".new.json"):
                    raise OSError("덮어쓰기 JSON 커밋 실패")
                return 실제replace(원본, 대상)

            with patch(
                "govoffice.adapters.json_style_presets.os.replace", side_effect=replace
            ):
                with self.assertRaises(ValueError):
                    저장소.저장(프리셋("새 프리셋", "새 본문"))

            self.assertEqual(기존hml, (디렉터리 / "style_atomic.hml").read_bytes())
            self.assertEqual(기존json, (디렉터리 / "style_atomic.json").read_bytes())
            복구됨 = 저장소.불러오기("style_atomic")
            self.assertEqual("기존 프리셋", 복구됨.이름)
            self.assertIn("기존 본문", 복구됨.hwpml)
            self.assertEqual(1, len(저장소.목록()))
            self.assertFalse(any(경로.name.startswith(".") for 경로 in 디렉터리.iterdir()))

    def test_롤백_교체마저_실패하면_목록에_반쪽을_노출하지_않고_백업을_보존한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            디렉터리 = Path(임시)
            저장소 = JSON서식프리셋저장소(디렉터리)
            저장소.저장(프리셋("기존", "복구해야 할 본문"))
            실제replace = os.replace

            def replace(원본, 대상):
                원본이름 = Path(원본).name
                if 원본이름.endswith(".new.json"):
                    raise OSError("JSON 커밋 실패")
                if ".backup.hml" in 원본이름:
                    raise OSError("HML 롤백 실패")
                return 실제replace(원본, 대상)

            with patch(
                "govoffice.adapters.json_style_presets.os.replace", side_effect=replace
            ):
                with self.assertRaises(ValueError):
                    저장소.저장(프리셋("신규", "실패할 본문"))

            self.assertFalse((디렉터리 / "style_atomic.json").exists())
            self.assertEqual((), 저장소.목록())
            백업 = list(디렉터리.glob(".*.backup.*"))
            self.assertEqual({".hml", ".json"}, {p.suffix for p in 백업})
            hml백업 = next(p for p in 백업 if p.suffix == ".hml")
            self.assertIn("복구해야 할 본문", hml백업.read_text(encoding="utf-8"))

    def test_두_임시파일이_완성되기_전에_실패하면_기존_파일을_건드리지_않는다(self):
        with tempfile.TemporaryDirectory() as 임시:
            디렉터리 = Path(임시)
            저장소 = JSON서식프리셋저장소(디렉터리)
            저장소.저장(프리셋("기존", "원본"))
            원본 = {p.name: p.read_bytes() for p in 디렉터리.iterdir()}
            실제쓰기 = 저장소._동기화쓰기
            호출수 = 0

            def 쓰기(경로, 내용):
                nonlocal 호출수
                호출수 += 1
                if 호출수 == 2:
                    raise OSError("메타데이터 임시 쓰기 실패")
                return 실제쓰기(경로, 내용)

            with patch.object(저장소, "_동기화쓰기", side_effect=쓰기):
                with self.assertRaises(ValueError):
                    저장소.저장(프리셋("신규", "변경"))

            self.assertEqual(원본, {p.name: p.read_bytes() for p in 디렉터리.iterdir()})

    def test_프로필필드id를_저장하고_기존_선택적_필드도_읽는다(self):
        with tempfile.TemporaryDirectory() as 임시:
            디렉터리 = Path(임시)
            저장소 = JSON서식프리셋저장소(디렉터리)
            필드 = 서식필드(
                id="field_1",
                토큰="{{GOVOFFICE_FIELD_1}}",
                안내문구="책임자",
                값유형="책임자",
                프로필필드id="profile_field_owner",
                조각그룹=((
                    ("{{GOVOFFICE_FIELD_1}}{{GOVOFFICE_RUN_0001_0001_0001}}", 1),
                    ("{{GOVOFFICE_RUN_0001_0001_0002}}", 2),
                ),),
            )
            저장소.저장(프리셋("프로필 연결", "{{GOVOFFICE_FIELD_1}}", 필드=(필드,)))
            self.assertEqual(
                "profile_field_owner",
                저장소.불러오기("style_atomic").필드목록[0].프로필필드id,
            )
            self.assertEqual(필드.조각그룹, 저장소.불러오기("style_atomic").필드목록[0].조각그룹)

            # 이전 스키마에는 이 키가 없었다. 없으면 None으로 읽어야 한다.
            메타경로 = 디렉터리 / "style_atomic.json"
            메타 = json.loads(메타경로.read_text(encoding="utf-8"))
            메타["fields"][0].pop("프로필필드id")
            메타["fields"][0].pop("조각그룹")
            메타경로.write_text(json.dumps(메타, ensure_ascii=False), encoding="utf-8")
            self.assertIsNone(
                저장소.불러오기("style_atomic").필드목록[0].프로필필드id
            )
            self.assertEqual((), 저장소.불러오기("style_atomic").필드목록[0].조각그룹)


if __name__ == "__main__":
    unittest.main()
