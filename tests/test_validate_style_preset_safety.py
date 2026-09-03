from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "govoffice_style_preset_validator_for_test",
    PROJECT / "tools" / "validate_style_preset.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - 테스트 로더 자체의 고장
    raise RuntimeError("서식 프리셋 검증기 모듈을 읽지 못했습니다.")
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class _가짜문서:
    def __init__(self, 소유자: "_가짜문서목록", 문서id: int) -> None:
        self.소유자 = 소유자
        self.DocumentID = 문서id
        self.Modified = True
        self.close_args: list[bool] = []
        self.activate_calls = 0

    def SetActive_XHwpDocument(self) -> bool:
        self.activate_calls += 1
        if self.DocumentID not in self.소유자.activation_mismatch_ids:
            self.소유자.active_id = self.DocumentID
        return True

    def Close(self, is_dirty: bool) -> bool:
        self.close_args.append(is_dirty)
        if self.Modified:
            raise AssertionError("Close 전에 Modified=False가 적용돼야 합니다.")
        # 실제 HWP의 위험한 의미론을 모사한다. Close를 호출한 proxy가 아니라
        # 현재 활성 문서가 닫히므로 검증기가 먼저 정확히 활성화해야 한다.
        활성문서 = self.소유자.Active_XHwpDocument
        if 활성문서 is None:
            return False
        if self.소유자.close_return is not True:
            return self.소유자.close_return
        self.소유자.close_order.append(활성문서.DocumentID)
        self.소유자._닫기예약(활성문서)
        return True


class _가짜문서목록:
    def __init__(
        self,
        ids: list[int],
        *,
        active_id: int | None = None,
        activation_mismatch_ids: set[int] | None = None,
        close_delay_polls: int = 0,
        close_return: object = True,
    ) -> None:
        self.documents = [_가짜문서(self, 문서id) for 문서id in ids]
        self.active_id = ids[-1] if active_id is None and ids else active_id
        self.activation_mismatch_ids = set(activation_mismatch_ids or ())
        self.close_delay_polls = close_delay_polls
        self.close_return = close_return
        self.close_order: list[int] = []
        self._pending_close: tuple[_가짜문서, int] | None = None

    def _닫기예약(self, 문서: _가짜문서) -> None:
        if self.close_delay_polls:
            self._pending_close = (문서, self.close_delay_polls)
            return
        self._문서제거(문서)

    def _문서제거(self, 문서: _가짜문서) -> None:
        self.documents.remove(문서)
        if self.active_id == 문서.DocumentID:
            self.active_id = self.documents[-1].DocumentID if self.documents else None

    def _지연닫기진행(self) -> None:
        if self._pending_close is None:
            return
        문서, 남은횟수 = self._pending_close
        if 남은횟수 > 0:
            self._pending_close = (문서, 남은횟수 - 1)
            return
        self._pending_close = None
        self._문서제거(문서)

    @property
    def Count(self) -> int:
        self._지연닫기진행()
        return len(self.documents)

    @property
    def Active_XHwpDocument(self):
        return next(
            (문서 for 문서 in self.documents if 문서.DocumentID == self.active_id),
            None,
        )

    def Item(self, index: int):
        return self.documents[index]


class _가짜한글:
    def __init__(self, ids: list[int], **kwargs) -> None:
        self.XHwpDocuments = _가짜문서목록(ids, **kwargs)
        self.quit_calls = 0

    def Quit(self) -> None:
        self.quit_calls += 1


class _가짜잠금:
    def __init__(self) -> None:
        self.abandoned = False
        self.acquired = False
        self.released = False

    def acquire(self) -> None:
        self.acquired = True

    def release(self) -> None:
        self.released = True


class _소유권불명한글:
    def __init__(self) -> None:
        self.quit_calls = 0

    def Quit(self) -> None:
        self.quit_calls += 1


class 실제서식검증안전성시험(unittest.TestCase):
    def test_새_PID는_시작시각까지_같은_정확히_한개만_소유한다(self):
        with (
            patch.object(
                validator,
                "_hwp_process_snapshot",
                side_effect=({100: 10, 200: 20}, {100: 10, 200: 20}),
            ),
            patch.object(validator.time, "sleep", return_value=None),
        ):
            result = validator._새프로세스확인({100: 10}, 제한초=1.0, 안정초=0.0)
        self.assertEqual({200: 20}, result)

    def test_새_PID가_둘이면_소유권을_추측하지_않는다(self):
        with patch.object(
            validator,
            "_hwp_process_snapshot",
            return_value={100: 10, 200: 20, 300: 30},
        ):
            with self.assertRaisesRegex(RuntimeError, "둘 이상"):
                validator._새프로세스확인({100: 10}, 제한초=0.1, 안정초=0.0)

    def test_main은_PID_소유권이_불명확하면_COM에_Quit을_보내지_않는다(self):
        lock = _가짜잠금()
        hwp = _소유권불명한글()
        snapshot_calls = 0

        def snapshot():
            nonlocal snapshot_calls
            snapshot_calls += 1
            if snapshot_calls == 1:
                return {100: 10}
            return {100: 10, 200: 20, 300: 30}

        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            with (
                patch.object(validator, "REPORT", report),
                patch.object(validator, "_검증단독잠금", return_value=lock),
                patch.object(validator, "_이전보고서읽기", return_value={}),
                patch.object(validator, "_hwp_process_snapshot", side_effect=snapshot),
                patch.object(validator, "DispatchEx", return_value=object()),
                patch.object(validator, "EnsureDispatch", return_value=hwp),
                patch.object(validator.pythoncom, "CoInitialize", return_value=None),
                patch.object(validator.pythoncom, "CoUninitialize", return_value=None),
            ):
                with (
                    contextlib.redirect_stdout(io.StringIO()),
                    self.assertRaises(SystemExit) as exit_error,
                ):
                    validator.main()

            self.assertEqual(1, exit_error.exception.code)
            self.assertTrue(report.is_file())
        self.assertEqual(0, hwp.quit_calls)
        self.assertTrue(lock.acquired)
        self.assertTrue(lock.released)

    def test_이전_검증_PID는_시작시각까지_같을때만_잔류로_차단한다(self):
        previous = {
            "process_exit_confirmed": False,
            "validation_hwp_processes": [
                {"pid": 200, "start_time_utc_ticks": 20},
                {"pid": 300, "start_time_utc_ticks": 30},
            ],
        }
        current = {200: 999, 300: 30}
        self.assertEqual(
            {300: 30},
            validator._이전검증잔류확인(previous, current),
        )

    def test_출력문서만_활성화해_닫고_원본은_Quit용으로_남긴다(self):
        hwp = _가짜한글([10, 20])
        original, output = hwp.XHwpDocuments.documents

        closed = validator._소유문서닫기(hwp, [10, 20])

        self.assertEqual([20], closed)
        self.assertEqual([original], hwp.XHwpDocuments.documents)
        self.assertEqual([False], output.close_args)
        self.assertEqual([], original.close_args)
        self.assertFalse(original.Modified)
        self.assertEqual(10, hwp.XHwpDocuments.active_id)

    def test_알수없는_문서가_섞이면_어떤_문서도_닫지_않는다(self):
        hwp = _가짜한글([10, 20, 99])

        with self.assertRaisesRegex(RuntimeError, "정확히 일치하지 않아"):
            validator._소유문서닫기(hwp, [10, 20])

        self.assertEqual([10, 20, 99], [doc.DocumentID for doc in hwp.XHwpDocuments.documents])
        self.assertTrue(all(not doc.close_args for doc in hwp.XHwpDocuments.documents))

    def test_활성_DocumentID가_다르면_어떤_문서도_닫지_않는다(self):
        hwp = _가짜한글([10, 20], active_id=10, activation_mismatch_ids={20})

        with self.assertRaisesRegex(RuntimeError, "실제 활성 DocumentID"):
            validator._소유문서닫기(hwp, [10, 20])

        self.assertEqual([10, 20], [doc.DocumentID for doc in hwp.XHwpDocuments.documents])
        self.assertTrue(all(not doc.close_args for doc in hwp.XHwpDocuments.documents))

    def test_Close가_COM정수0을_반환하면_원본과_Quit준비를_진행하지_않는다(self):
        hwp = _가짜한글([10, 20], close_return=0)

        with self.assertRaisesRegex(RuntimeError, "닫지 못했습니다"):
            validator._소유문서닫기(hwp, [10, 20])

        self.assertEqual([10, 20], [doc.DocumentID for doc in hwp.XHwpDocuments.documents])
        self.assertTrue(hwp.XHwpDocuments.documents[0].Modified)

    def test_Close의_비동기반영을_제한대기한_뒤_원본만_남긴다(self):
        hwp = _가짜한글([10, 20], close_delay_polls=2)

        with patch.object(validator.time, "sleep", return_value=None):
            closed = validator._소유문서닫기(hwp, [10, 20])

        self.assertEqual([20], closed)
        self.assertEqual([10], [doc.DocumentID for doc in hwp.XHwpDocuments.documents])
        self.assertFalse(hwp.XHwpDocuments.documents[0].Modified)

    def test_GUI와_같은_mutex를_쓰고_Clear_정리를_사용하지_않는다(self):
        source = (PROJECT / "tools" / "validate_style_preset.py").read_text(encoding="utf-8")
        launcher = (PROJECT / "launch_gui.ps1").read_text(encoding="utf-8")
        self.assertIn('GUI_MUTEX_NAME = r"Local\\GovOfficeRecoveredApplication"', source)
        self.assertIn("Local\\GovOfficeRecoveredApplication", launcher)
        self.assertNotIn(".Clear(", source)
        self.assertIn("문서.Close(False)", source)
        self.assertIn('보고서["document_cleanup_ok"] = True', source)
        self.assertIn('보고서.get("process_exit_confirmed")', source)


if __name__ == "__main__":
    unittest.main()
