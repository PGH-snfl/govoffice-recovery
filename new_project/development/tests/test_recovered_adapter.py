import contextlib
import io
import unittest
import inspect
import tempfile
from pathlib import Path
from unittest.mock import patch

from govoffice.adapters.recovered_hwp import 복구한글어댑터
from govoffice.runtime.recovered_hwp.한컴오피스.compat.legacy_runtime import _bytecode_root
from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리_기본 import 한컴기본
from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리_1 import 한컴1
from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리_2 import 한컴2
from govoffice.runtime.recovered_hwp.한컴오피스.한컴라이브러리 import 기본한컴
from govoffice.runtime.recovered_hwp.한컴오피스.compat.legacy_runtime import (
    Legacy한컴기본,
    Legacy한컴1,
    Legacy한컴2,
    Legacy기본한컴,
)


class 명령기록:
    def __init__(self):
        self.명령 = []

    def Run(self, 이름):
        self.명령.append(이름)


class 가짜원본:
    def __init__(self):
        self.문장목록 = []
        self.대상 = type("대상", (), {"HAction": 명령기록()})()

    def 문장(self, 내용):
        self.문장목록.append(내용)


class 가짜COM:
    def __init__(self, 내보내기결과="<HWPML/>"):
        self.호출 = []
        self.HAction = 명령기록()
        self.내보내기결과 = 내보내기결과

    def GetTextFile(self, 형식, 옵션):
        self.호출.append(("get", 형식, 옵션))
        return self.내보내기결과

    def SetTextFile(self, 내용, 형식, 옵션):
        self.호출.append(("set", 내용, 형식, 옵션))
        return True


class 불러오기실패가짜COM(가짜COM):
    def SetTextFile(self, 내용, 형식, 옵션):
        self.호출.append(("set", 내용, 형식, 옵션))
        return False


class 가짜항목목록:
    def __init__(self, 항목):
        self.항목 = 항목

    @property
    def Count(self):
        return 1

    def Item(self, 번호):
        if 번호 != 0:
            raise IndexError(번호)
        return self.항목


class 활성가짜문서목록(가짜항목목록):
    @property
    def Active_XHwpDocument(self):
        return self.항목


class 가짜문서:
    def __init__(self):
        self.DocumentID = f"document_{id(self)}"
        self.FullName = ""
        self.Title = ""
        self.ReadOnly = False
        self.Modified = False
        self.활성화횟수 = 0

    def SetActive_XHwpDocument(self):
        self.활성화횟수 += 1
        return True


class 가짜창:
    def __init__(self):
        self.Visible = False
        self.WindowState = 0


class 관리가짜COM(가짜COM):
    def __init__(self, 내보내기결과="<HWPML/>"):
        super().__init__(내보내기결과)
        self.문서 = 가짜문서()
        self.창 = 가짜창()
        self.XHwpDocuments = 활성가짜문서목록(self.문서)
        self.XHwpWindows = 가짜항목목록(self.창)
        self.열기목록 = []
        self.정리목록 = []
        self.종료횟수 = 0
        self.저장횟수 = 0

    def Open(self, 경로):
        self.열기목록.append(경로)
        self.문서.FullName = 경로
        self.문서.Title = Path(경로).name
        return True

    def Clear(self, 옵션):
        self.정리목록.append(옵션)
        return True

    def Save(self):
        self.저장횟수 += 1
        self.문서.Modified = False
        return True

    def Quit(self):
        self.종료횟수 += 1


class 직접닫기가짜문서(가짜문서):
    def __init__(self, 소유자, 이름="관리 문서"):
        super().__init__()
        self.소유자 = 소유자
        self.Title = 이름
        self.닫기인자 = []

    def Close(self, 저장):
        self.닫기인자.append(저장)
        if self.Modified:
            raise AssertionError("Modified를 먼저 False로 만들어야 한다.")
        self.소유자.문서목록.remove(self)
        return True


class 직접닫기문서목록:
    def __init__(self, 소유자):
        self.소유자 = 소유자

    @property
    def Count(self):
        return len(self.소유자.문서목록)

    @property
    def Active_XHwpDocument(self):
        return self.소유자.문서목록[0] if self.소유자.문서목록 else None

    def Item(self, 번호):
        return self.소유자.문서목록[번호]


class Clear실패관리가짜COM(관리가짜COM):
    def __init__(self):
        super().__init__()
        self.문서목록 = []
        self.문서 = 직접닫기가짜문서(self)
        self.문서목록.append(self.문서)
        self.XHwpDocuments = 직접닫기문서목록(self)

    def Clear(self, 옵션):
        self.정리목록.append(옵션)
        raise RuntimeError("RPC server fault")


class 롤백가짜문서(가짜문서):
    def __init__(self, 소유자, 이름):
        super().__init__()
        self.소유자 = 소유자
        self.Title = 이름
        self.닫기인자 = []
        self.활성화횟수 = 0

    def Close(self, 저장):
        self.닫기인자.append(저장)
        if self.Modified:
            raise AssertionError("Modified를 먼저 False로 만들어야 한다.")
        self.소유자.문서목록.remove(self)
        self.소유자.활성문서 = self.소유자.원래문서
        return True

    def SetActive_XHwpDocument(self):
        self.활성화횟수 += 1
        self.소유자.활성문서 = self


class 롤백가짜문서목록:
    def __init__(self, 소유자):
        self.소유자 = 소유자

    @property
    def Count(self):
        return len(self.소유자.문서목록)

    @property
    def Active_XHwpDocument(self):
        return self.소유자.활성문서

    def Item(self, 번호):
        return self.소유자.문서목록[번호]


class 롤백가짜창:
    def __init__(self, 소유자):
        self.소유자 = 소유자
        self.Visible = False
        self.WindowState = 0

    @property
    def Active_XHwpDocument(self):
        return self.소유자.활성문서


class 롤백가짜창목록:
    def __init__(self, 소유자):
        self.활성창 = 롤백가짜창(소유자)

    @property
    def Active_XHwpWindow(self):
        return self.활성창


class 롤백가짜명령(명령기록):
    def __init__(self, 소유자):
        super().__init__()
        self.소유자 = 소유자

    def Run(self, 이름):
        self.명령.append(이름)
        if 이름 == "FileNew":
            self.소유자.문서목록.append(self.소유자.새문서)
            self.소유자.활성문서 = self.소유자.새문서
        return True


class 문서객체불러오기실패가짜COM(가짜COM):
    def __init__(self):
        super().__init__()
        self.문서목록 = []
        self.원래문서 = 롤백가짜문서(self, "원래")
        self.새문서 = 롤백가짜문서(self, "출력 실패")
        self.문서목록.append(self.원래문서)
        self.활성문서 = self.원래문서
        self.XHwpDocuments = 롤백가짜문서목록(self)
        self.XHwpWindows = 롤백가짜창목록(self)
        self.HAction = 롤백가짜명령(self)

    def SetTextFile(self, 내용, 형식, 옵션):
        self.호출.append(("set", 내용, 형식, 옵션))
        self.활성문서.Modified = True
        return False


class 문서객체출력성공가짜COM(문서객체불러오기실패가짜COM):
    def SetTextFile(self, 내용, 형식, 옵션):
        self.호출.append(("set", 내용, 형식, 옵션))
        self.활성문서.Modified = True
        return True


class 전용가짜원본(가짜원본):
    def __init__(self, 전용=None):
        super().__init__()
        self.수동대상 = self.대상
        self.전용대상 = 전용 if 전용 is not None else 관리가짜COM()
        self._전용Automation대상 = None
        self.전용열기횟수 = 0

    def 전용한컴열기(self):
        self.전용열기횟수 += 1
        self._전용Automation대상 = self.전용대상
        self.대상 = self.전용대상
        return self.전용대상


class 열기실패전용COM(Clear실패관리가짜COM):
    def __init__(self, *, 경로불일치=False):
        super().__init__()
        self._oleobj_ = object()
        self.경로불일치 = 경로불일치

    def Open(self, 경로):
        self.열기목록.append(경로)
        self.문서.FullName = f"{경로}.wrong" if self.경로불일치 else 경로
        self.문서.Title = Path(self.문서.FullName).name
        return True if self.경로불일치 else False


class 안전정리전용가짜원본(전용가짜원본):
    def __init__(self, 전용, *, 식별자=(200, 2000), 프로세스목록=None):
        super().__init__(전용)
        self._전용Automation프로세스식별자 = None
        self.생성식별자 = 식별자
        self.프로세스목록 = list(
            프로세스목록
            or [((100, 1000),), ((100, 1000), (200, 2000))]
        )
        self.안전종료호출 = []

    def 전용한컴열기(self):
        결과 = super().전용한컴열기()
        self._전용Automation프로세스식별자 = self.생성식별자
        return 결과

    def _한글프로세스식별자목록(self):
        return self.프로세스목록.pop(0)

    def _프로세스식별자실행중(self, 식별자):
        return 식별자 == self.생성식별자

    def _전용Automation대상안전종료(self, 대상, 식별자):
        self.안전종료호출.append((대상, 식별자))
        for 문서 in reversed(tuple(대상.문서목록)):
            문서.Modified = False
            문서.Close(False)
        대상.Quit()
        return {"process_exited": True}


class 가짜위치:
    def __init__(self, 위치):
        self.위치 = dict(zip(("List", "Para", "Pos"), 위치))

    def Item(self, 이름):
        return self.위치[이름]


class 위치확인가짜COM(가짜COM):
    def __init__(self, 시작, 끝, 내보내기결과="<HWPML/>"):
        super().__init__(내보내기결과)
        self.위치목록 = [가짜위치(시작), 가짜위치(끝)]

    def CreateSet(self, _):
        return self.위치목록.pop(0)

    def GetSelectedPosBySet(self, *_):
        return True


class 복구어댑터시험(unittest.TestCase):
    def test_경로문서는_수동문서가_아닌_전용객체로_열고_상태를_유지한다(self):
        원본 = 전용가짜원본()
        수동대상 = 원본.수동대상
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "시험 문서.hwp"
            경로.write_bytes(b"mock")
            상태 = 어댑터.관리문서열기(str(경로))

        self.assertIs(원본.전용대상, 원본.대상)
        self.assertIsNot(수동대상, 원본.대상)
        self.assertEqual([str(경로.resolve())], 원본.전용대상.열기목록)
        self.assertEqual(1, 원본.전용열기횟수)
        self.assertTrue(상태["connected"])
        self.assertTrue(상태["managed"])
        self.assertTrue(상태["opened"])
        self.assertEqual("시험 문서.hwp", 상태["title"])
        self.assertEqual(str(경로.resolve()), 상태["path"])
        self.assertTrue(상태["editable"])
        self.assertFalse(상태["modified"])
        self.assertTrue(상태["visible"])
        self.assertFalse(상태["minimized"])

        # 외부 코드가 연결 대상을 바꿔도 관리 문서 상태 조회가 전용 객체를 복원한다.
        원본.대상 = 수동대상
        self.assertTrue(어댑터.문서상태()["managed"])
        self.assertIs(원본.전용대상, 원본.대상)

    def test_열기실패시_신규프로세스소유권이_모호하면_종료명령을_0회_호출한다(self):
        전용대상 = 열기실패전용COM()
        원본 = 안전정리전용가짜원본(
            전용대상,
            식별자=None,
            프로세스목록=[((100, 1000),)],
        )
        이전대상 = 원본.수동대상
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "소유권모호.hwp"
            경로.write_bytes(b"mock")
            with self.assertRaisesRegex(RuntimeError, "0회 호출"):
                어댑터.관리문서열기(경로)

        self.assertEqual([], 전용대상.정리목록)
        self.assertEqual([], 전용대상.문서.닫기인자)
        self.assertEqual(0, 전용대상.종료횟수)
        self.assertEqual([], 원본.안전종료호출)
        self.assertIs(이전대상, 원본.대상)
        self.assertIs(전용대상, 어댑터._안전정리보류대상)

    def test_열기실패시_입증된_전용프로세스만_DocumentID별로_닫는다(self):
        전용대상 = 열기실패전용COM()
        원본 = 안전정리전용가짜원본(전용대상)
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "열기실패.hwp"
            경로.write_bytes(b"mock")
            with self.assertRaisesRegex(RuntimeError, "열지 못했습니다"):
                어댑터.관리문서열기(경로)

        self.assertEqual([], 전용대상.정리목록)
        self.assertEqual([False], 전용대상.문서.닫기인자)
        self.assertEqual([], 전용대상.문서목록)
        self.assertEqual(1, 전용대상.종료횟수)
        self.assertEqual([(전용대상, (200, 2000))], 원본.안전종료호출)
        self.assertIs(원본.수동대상, 원본.대상)

    def test_열기후_경로검증실패도_입증된_전용프로세스만_안전정리한다(self):
        전용대상 = 열기실패전용COM(경로불일치=True)
        원본 = 안전정리전용가짜원본(전용대상)
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "경로검증.hwp"
            경로.write_bytes(b"mock")
            with (
                patch.object(어댑터, "_관리창찾기", return_value=4242),
                patch.object(
                    어댑터,
                    "_네이티브창정보",
                    return_value={"visible": True, "minimized": False},
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "경로가 선택한 파일과 일치"):
                    어댑터.관리문서열기(경로, 표시=False)

        self.assertEqual([], 전용대상.정리목록)
        self.assertEqual([False], 전용대상.문서.닫기인자)
        self.assertEqual(1, 전용대상.종료횟수)
        self.assertEqual([(전용대상, (200, 2000))], 원본.안전종료호출)
        self.assertIsNone(어댑터._관리대상)

    def test_관리문서를_최소화_복원하고_Clear1_Quit으로_대화상자없이_닫는다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "닫기시험.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)

            최소상태 = 어댑터.문서최소화()
            self.assertTrue(최소상태["minimized"])
            self.assertEqual(1, 원본.전용대상.창.WindowState)

            표시상태 = 어댑터.문서표시()
            self.assertTrue(표시상태["visible"])
            self.assertFalse(표시상태["minimized"])
            self.assertEqual(0, 원본.전용대상.창.WindowState)

            종료상태 = 어댑터.관리문서닫기()

        self.assertEqual([1], 원본.전용대상.정리목록)
        self.assertEqual(1, 원본.전용대상.종료횟수)
        self.assertIs(원본.수동대상, 원본.대상)
        self.assertTrue(종료상태["connected"])
        self.assertFalse(종료상태["managed"])
        self.assertFalse(종료상태["document_open"])
        self.assertTrue(종료상태["closed"])
        self.assertFalse(종료상태["discarded_changes"])
        self.assertEqual(str(경로.resolve()), 종료상태["previous_document"]["path"])

    def test_Clear가_serverfault여도_DocumentID가_확인된_소유문서만_직접닫고_Quit한다(self):
        전용대상 = Clear실패관리가짜COM()
        원본 = 전용가짜원본(전용대상)
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "Clear실패.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            전용대상.문서.Modified = True

            종료상태 = 어댑터.관리문서닫기(False)

        self.assertEqual([1], 전용대상.정리목록)
        self.assertEqual([False], 전용대상.문서.닫기인자)
        self.assertEqual([], 전용대상.문서목록)
        self.assertEqual(1, 전용대상.종료횟수)
        self.assertTrue(종료상태["closed"])

    def test_같은인스턴스에_소유권불명문서가_있으면_Clear와_Quit을_실행하지_않는다(self):
        전용대상 = Clear실패관리가짜COM()
        원본 = 전용가짜원본(전용대상)
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "소유권검사.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            외부문서 = 직접닫기가짜문서(전용대상, "사용자 문서")
            전용대상.문서목록.append(외부문서)

            with self.assertRaisesRegex(PermissionError, "프로그램 소유가 아닌"):
                어댑터.관리문서닫기(False)

        self.assertEqual([], 전용대상.정리목록)
        self.assertEqual([], 외부문서.닫기인자)
        self.assertEqual(0, 전용대상.종료횟수)
        self.assertIs(전용대상, 어댑터._관리대상)

    def test_Quit후_PID가_남아있으면_closed로_표시하거나_관리상태를_버리지_않는다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "PID확인.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            원본.전용대상._oleobj_ = object()
            어댑터._관리창프로세스id = 42424
            with (
                patch.object(어댑터, "_관리대상정상", return_value=True),
                patch.object(어댑터, "_관리창찾기", return_value=4242),
                patch.object(
                    어댑터,
                    "_네이티브창정보",
                    return_value={"visible": True, "minimized": False},
                ),
                patch.object(어댑터, "_프로세스종료대기", return_value=False),
            ):
                with self.assertRaisesRegex(RuntimeError, "종료되지 않아"):
                    어댑터.관리문서닫기(False)

        self.assertEqual(1, 원본.전용대상.종료횟수)
        self.assertIs(원본.전용대상, 어댑터._관리대상)

    def test_실제COM_문서목록이_불완전하면_Clear와_Quit을_실행하지_않는다(self):
        class 불완전목록:
            Count = 2

            def __init__(self, 문서):
                self.Active_XHwpDocument = 문서

            def Item(self, 번호):
                if 번호 == 0:
                    return self.Active_XHwpDocument
                raise RuntimeError("두 번째 문서 열거 실패")

        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "불완전목록.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            원본.전용대상._oleobj_ = object()
            원본.전용대상.XHwpDocuments = 불완전목록(원본.전용대상.문서)
            with patch.object(어댑터, "_관리대상정상", return_value=True):
                with self.assertRaisesRegex(RuntimeError, "완전히 열거"):
                    어댑터.관리문서닫기(False)

        self.assertEqual([], 원본.전용대상.정리목록)
        self.assertEqual(0, 원본.전용대상.종료횟수)
        self.assertIs(원본.전용대상, 어댑터._관리대상)

    def test_수동으로_연_문서는_닫지_않는다(self):
        원본 = 가짜원본()
        수동대상 = 원본.대상
        어댑터 = 복구한글어댑터(원본)

        with self.assertRaisesRegex(PermissionError, "수동으로 연 한글 문서"):
            어댑터.관리문서닫기()
        self.assertIs(수동대상, 원본.대상)

    def test_관리문서에_선택이_없어도_ROT의_수동문서로_바꾸지_않는다(self):
        전용대상 = 관리가짜COM("")
        원본 = 전용가짜원본(전용대상)
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "선택시험.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            원본._실행중인_한글목록 = lambda: self.fail("관리 문서가 있으면 ROT를 열거하면 안 됩니다.")
            with self.assertRaisesRegex(ValueError, "프로그램이 연 문서에서 선택 영역"):
                어댑터.선택영역서식내보내기()
        self.assertIs(전용대상, 원본.대상)

    def test_다른_관리문서를_덮어열지_않고_먼저_정상종료하도록_안내한다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            첫경로 = Path(임시폴더) / "첫문서.hwp"
            둘째경로 = Path(임시폴더) / "둘째문서.hwp"
            첫경로.write_bytes(b"first")
            둘째경로.write_bytes(b"second")
            어댑터.관리문서열기(첫경로)
            with self.assertRaisesRegex(RuntimeError, "hwp_document_close"):
                어댑터.관리문서열기(둘째경로)
        self.assertEqual([str(첫경로.resolve())], 원본.전용대상.열기목록)
        self.assertEqual([], 원본.전용대상.정리목록)

    def test_수정문서는_저장여부_확인전에는_닫지_않고_명시적_저장을_지원한다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "수정문서.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            원본.전용대상.문서.Modified = True

            확인상태 = 어댑터.관리문서닫기()
            self.assertTrue(확인상태["confirmation_required"])
            self.assertFalse(확인상태["closed"])
            self.assertEqual([], 원본.전용대상.정리목록)
            self.assertEqual(0, 원본.전용대상.종료횟수)

            종료상태 = 어댑터.관리문서닫기(True)

        self.assertEqual(1, 원본.전용대상.저장횟수)
        self.assertEqual([1], 원본.전용대상.정리목록)
        self.assertEqual(1, 원본.전용대상.종료횟수)
        self.assertTrue(종료상태["saved_changes"])
        self.assertFalse(종료상태["discarded_changes"])

    def test_수정문서는_명시적_폐기선택으로만_저장없이_닫는다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "폐기문서.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            원본.전용대상.문서.Modified = True
            종료상태 = 어댑터.관리문서닫기(False)

        self.assertEqual(0, 원본.전용대상.저장횟수)
        self.assertEqual([1], 원본.전용대상.정리목록)
        self.assertTrue(종료상태["discarded_changes"])
        self.assertFalse(종료상태["saved_changes"])

    def test_ReadOnly가_없으면_EditMode로_편집가능여부를_판정한다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "편집모드.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            del 원본.전용대상.문서.ReadOnly
            원본.전용대상.문서.EditMode = 1
            self.assertTrue(어댑터.문서상태()["editable"])
            원본.전용대상.문서.EditMode = 0
            self.assertFalse(어댑터.문서상태()["editable"])

    def test_EditMode의_기본모드와_배포용비트를_분리한다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "편집모드비트.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            for 모드, 편집가능, 설명, 배포용 in (
                (0, False, "읽기 전용", False),
                (1, True, "편집 가능", False),
                (2, True, "일부만 편집 가능", False),
                (16, False, "읽기 전용", True),
                (17, True, "편집 가능", True),
                (18, True, "일부만 편집 가능", True),
            ):
                원본.전용대상.문서.EditMode = 모드
                상태 = 어댑터.문서상태()
                self.assertEqual(편집가능, 상태["editable"], 모드)
                self.assertEqual(설명, 상태["edit_mode_label"], 모드)
                self.assertEqual(배포용, 상태["distribution"], 모드)

    def test_다른이름으로저장한_실시간경로가_캐시보다_우선한다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            첫경로 = Path(임시폴더) / "원래이름.hwp"
            새경로 = Path(임시폴더) / "바뀐이름.hwp"
            첫경로.write_bytes(b"mock")
            새경로.write_bytes(b"mock")
            어댑터.관리문서열기(첫경로)
            원본.전용대상.문서.FullName = str(새경로.resolve())
            원본.전용대상.문서.Title = 새경로.name

            상태 = 어댑터.문서상태()

        self.assertEqual(str(새경로.resolve()), 상태["path"])
        self.assertEqual(새경로.resolve(), 어댑터._관리문서경로)

    def test_끊긴_관리COM은_캐시를_비우고_수동대상을_복원한다(self):
        class 끊긴목록:
            @property
            def Count(self):
                raise RuntimeError("RPC server unavailable")

        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "종료된문서.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            원본.전용대상._oleobj_ = object()
            원본.전용대상.XHwpWindows = 끊긴목록()
            상태 = 어댑터.문서상태()

        self.assertFalse(상태["managed"])
        self.assertFalse(상태["document_open"])
        self.assertIs(원본.수동대상, 원본.대상)
        self.assertIsNone(어댑터._관리대상)

    def test_실제IXHwpWindow에_WindowState가_없어도_저장한_HWND로_제어한다(self):
        원본 = 전용가짜원본()
        어댑터 = 복구한글어댑터(원본)
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "네이티브창.hwp"
            경로.write_bytes(b"mock")
            어댑터.관리문서열기(경로)
            del 원본.전용대상.창.WindowState
            with (
                patch.object(어댑터, "_실제COM객체", return_value=True),
                patch.object(어댑터, "_관리대상정상", return_value=True),
                patch.object(어댑터, "_관리창찾기", return_value=4242),
                patch.object(어댑터, "_네이티브창정보", return_value=None),
                patch.object(어댑터, "_네이티브창명령", return_value=True) as 명령,
            ):
                self.assertTrue(어댑터.문서최소화()["minimized"])
                self.assertFalse(어댑터.문서표시()["minimized"])

        명령.assert_any_call(4242, 6)
        명령.assert_any_call(4242, 9, 활성화=True)

    def test_새_Hwp_PID나_HWND가_둘이상이면_네이티브관리창을_임의선택하지_않는다(self):
        어댑터 = 복구한글어댑터(전용가짜원본())
        어댑터._관리전창핸들 = {10}
        어댑터._관리전프로세스ids = {100}
        모호한창 = [
            {"hwnd": 20, "pid": 200, "title": "같은문서.hwp - 한글", "visible": True},
            {"hwnd": 21, "pid": 201, "title": "같은문서.hwp - 한글", "visible": True},
        ]
        with patch.object(어댑터, "_한글창목록", return_value=모호한창):
            self.assertIsNone(어댑터._관리창찾기("같은문서.hwp"))
        self.assertIsNone(어댑터._관리창핸들)
        self.assertIsNone(어댑터._관리창프로세스id)

        재사용PID창 = [
            {"hwnd": 30, "pid": 100, "title": "같은문서.hwp - 한글", "visible": True}
        ]
        with patch.object(어댑터, "_한글창목록", return_value=재사용PID창):
            self.assertIsNone(어댑터._관리창찾기("같은문서.hwp"))

        안전한창 = [
            {"hwnd": 40, "pid": 400, "title": "같은문서.hwp - 한글", "visible": True}
        ]
        with patch.object(어댑터, "_한글창목록", return_value=안전한창):
            self.assertEqual(40, 어댑터._관리창찾기("같은문서.hwp"))
        self.assertEqual(400, 어댑터._관리창프로세스id)

    def test_수동문서의_표시와_최소화는_거부한다(self):
        어댑터 = 복구한글어댑터(가짜원본())
        with self.assertRaisesRegex(PermissionError, "프로그램에서 불러온"):
            어댑터.문서표시()
        with self.assertRaisesRegex(PermissionError, "프로그램에서 불러온"):
            어댑터.문서최소화()

    def test_HWP_HWPX외_파일은_불러오지_않는다(self):
        어댑터 = 복구한글어댑터(전용가짜원본())
        with tempfile.TemporaryDirectory() as 임시폴더:
            경로 = Path(임시폴더) / "문서.txt"
            경로.write_text("not hwp", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, ".hwp와 .hwpx"):
                어댑터.관리문서열기(경로)

    def test_새포트를_원본호출로_변환한다(self):
        원본 = 가짜원본()
        어댑터 = 복구한글어댑터(원본)
        어댑터.문장("내용")
        어댑터.줄바꿈()
        self.assertEqual(["내용"], 원본.문장목록)
        self.assertEqual(["BreakPara"], 원본.대상.HAction.명령)

    def test_선택영역_HWPML을_내보내고_쪽서식과_함께_새문서로_적용한다(self):
        원본 = 가짜원본()
        원본.대상 = 가짜COM()
        원본._실행중인_한글목록 = lambda: self.fail("현재 선택이 있으면 ROT를 열거하면 안 됩니다.")
        어댑터 = 복구한글어댑터(원본)

        self.assertEqual("<HWPML/>", 어댑터.선택영역서식내보내기())
        self.assertTrue(어댑터.서식조각삽입("<HWPML/>"))
        self.assertTrue(어댑터.선택영역새문서생성("<HWPML/>"))
        self.assertEqual(
            [
                ("get", "HWPML2X", "saveblock"),
                ("set", "<HWPML/>", "HWPML2X", "insertfile"),
                ("set", "<HWPML/>", "HWPML2X", ""),
            ],
            원본.대상.호출,
        )
        self.assertEqual(["FileNew"], 원본.대상.HAction.명령)

    def test_새문서_DocumentID가_불명확하면_FileClose로_활성문서를_추측하지_않는다(self):
        원본 = 가짜원본()
        원본.대상 = 불러오기실패가짜COM()
        어댑터 = 복구한글어댑터(원본)

        with self.assertRaisesRegex(RuntimeError, "DocumentID"):
            어댑터.선택영역새문서생성("<HWPML/>")

        self.assertEqual(["FileNew"], 원본.대상.HAction.명령)

    def test_실패한_새문서를_저장질문없이_닫고_원래문서로_복귀한다(self):
        원본 = 가짜원본()
        원본.대상 = 문서객체불러오기실패가짜COM()
        어댑터 = 복구한글어댑터(원본)

        with self.assertRaisesRegex(RuntimeError, "새 문서로 불러오지"):
            어댑터.선택영역새문서생성("<HWPML/>")

        대상 = 원본.대상
        self.assertFalse(대상.새문서.Modified)
        self.assertEqual([False], 대상.새문서.닫기인자)
        self.assertEqual(["원래"], [문서.Title for 문서 in 대상.문서목록])
        self.assertIs(대상.원래문서, 대상.활성문서)
        self.assertEqual(0, 대상.원래문서.활성화횟수)
        self.assertEqual(["FileNew"], 대상.HAction.명령)

    def test_성공한_출력문서의_DocumentID를_추적하고_관리상태는_원본문서를_유지한다(self):
        대상 = 문서객체출력성공가짜COM()
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID

        self.assertTrue(어댑터.선택영역새문서생성("<HWPML/>"))

        self.assertIn(대상.새문서.DocumentID, 어댑터._출력문서ids)
        상태 = 어댑터.문서상태()
        self.assertEqual(대상.원래문서.DocumentID, 상태["document_id"])
        self.assertEqual(대상.새문서.DocumentID, 상태["active_document_id"])
        self.assertEqual(1, 상태["output_document_count"])
        self.assertTrue(상태["output_document_count_exact"])

    def test_상태폴링은_출력탭의_포커스를_바꾸지않고_작업직전에만_원문서를_활성화한다(self):
        대상 = 문서객체출력성공가짜COM()
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID
        어댑터.선택영역새문서생성("<HWPML/>")

        상태 = 어댑터.문서상태()

        self.assertIs(대상.새문서, 대상.활성문서)
        self.assertEqual(0, 대상.원래문서.활성화횟수)
        self.assertEqual(대상.새문서.DocumentID, 상태["active_document_id"])

        작업상태 = 어댑터.관리작업문서활성화()

        self.assertIs(대상.원래문서, 대상.활성문서)
        self.assertEqual(1, 대상.원래문서.활성화횟수)
        self.assertEqual(대상.원래문서.DocumentID, 작업상태["active_document_id"])

    def test_관리원문서_활성화후_ID가_바뀌지않으면_작업을_거부한다(self):
        대상 = 문서객체출력성공가짜COM()
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID
        어댑터.선택영역새문서생성("<HWPML/>")
        대상.원래문서.SetActive_XHwpDocument = lambda: True

        with self.assertRaisesRegex(RuntimeError, "활성 DocumentID"):
            어댑터.관리작업문서활성화()

        self.assertIs(대상.새문서, 대상.활성문서)

    def test_관리문서를_불러오지않으면_일반변경작업의_활성화를_거부한다(self):
        어댑터 = 복구한글어댑터(가짜원본())

        with self.assertRaisesRegex(PermissionError, "문서 열기"):
            어댑터.관리작업문서활성화()

    def test_살아있는_출력문서가_있으면_관리닫기의_Clear_Close_Quit을_모두_거부한다(self):
        대상 = 문서객체출력성공가짜COM()
        대상.정리목록 = []
        대상.종료횟수 = 0
        대상.Clear = lambda 옵션: 대상.정리목록.append(옵션)
        대상.Quit = lambda: setattr(대상, "종료횟수", 대상.종료횟수 + 1)
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID
        어댑터.선택영역새문서생성("<HWPML/>")

        with self.assertRaisesRegex(PermissionError, "출력 문서를 저장하거나 닫은 후"):
            어댑터.관리문서닫기(False)

        self.assertEqual([], 대상.정리목록)
        self.assertEqual([], 대상.원래문서.닫기인자)
        self.assertEqual([], 대상.새문서.닫기인자)
        self.assertEqual(0, 대상.종료횟수)
        self.assertIs(대상, 어댑터._관리대상)

    def test_사용자가_출력문서를_닫으면_상태에서_추적ID와_개수를_정리한다(self):
        대상 = 문서객체출력성공가짜COM()
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID
        어댑터.선택영역새문서생성("<HWPML/>")
        대상.새문서.Modified = False
        대상.새문서.Close(False)

        상태 = 어댑터.문서상태()

        self.assertEqual(0, 상태["output_document_count"])
        self.assertEqual(set(), 어댑터._출력문서ids)

    def test_일반복구메서드가_만든_새문서도_실행전후_ID대조로_출력추적한다(self):
        대상 = 문서객체출력성공가짜COM()
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID

        결과 = 어댑터.관리작업추적실행(lambda: 대상.HAction.Run("FileNew"))

        self.assertTrue(결과)
        self.assertEqual({대상.새문서.DocumentID}, 어댑터._출력문서ids)
        self.assertEqual(1, 어댑터.문서상태()["output_document_count"])

    def test_일반복구메서드가_새문서후_실패해도_출력ID를_잃지않는다(self):
        대상 = 문서객체출력성공가짜COM()
        원본 = 가짜원본()
        원본.대상 = 대상
        어댑터 = 복구한글어댑터(원본)
        어댑터._관리대상 = 대상
        어댑터._관리문서id = 대상.원래문서.DocumentID

        def 실패작업():
            대상.HAction.Run("FileNew")
            raise ValueError("기능 실패")

        with self.assertRaisesRegex(ValueError, "기능 실패"):
            어댑터.관리작업추적실행(실패작업)

        self.assertEqual({대상.새문서.DocumentID}, 어댑터._출력문서ids)

    def test_활성문서속성을_읽지못하면_Item0을_활성문서ID로_추측하지_않는다(self):
        원본 = 가짜원본()
        원본.대상 = 관리가짜COM()
        원본.대상.XHwpDocuments = 가짜항목목록(원본.대상.문서)
        어댑터 = 복구한글어댑터(원본)

        상태 = 어댑터.문서상태()

        self.assertIsNone(상태["active_document_id"])
        self.assertEqual(원본.대상.문서.DocumentID, 상태["document_id"])

    def test_다른_한글창에_선택영역이_있으면_자동으로_그문서에_연결한다(self):
        현재문서 = 가짜COM("")
        선택문서 = 가짜COM("<HWPML><BODY/></HWPML>")
        원본 = 가짜원본()
        원본.대상 = 현재문서
        원본._실행중인_한글목록 = lambda: (현재문서, 선택문서)
        어댑터 = 복구한글어댑터(원본)

        self.assertEqual("<HWPML><BODY/></HWPML>", 어댑터.선택영역서식내보내기())
        self.assertIs(선택문서, 원본.대상)

    def test_미연결상태에서도_새문서를_만들지_않고_기존선택문서를_찾는다(self):
        선택문서 = 가짜COM("<HWPML><BODY/></HWPML>")
        원본 = 가짜원본()
        원본.대상 = None
        원본._실행중인_한글목록 = lambda: (선택문서,)
        어댑터 = 복구한글어댑터(원본)

        self.assertEqual("<HWPML><BODY/></HWPML>", 어댑터.선택영역서식내보내기())
        self.assertIs(선택문서, 원본.대상)

    def test_다른문서_검색중_진단출력이_GUI프로토콜에_섞이지_않는다(self):
        선택문서 = 가짜COM("<HWPML><BODY/></HWPML>")
        원본 = 가짜원본()
        원본.대상 = 가짜COM("")

        def 실행중목록():
            print("백엔드 JSON에 섞이면 안 되는 진단")
            return (선택문서,)

        원본._실행중인_한글목록 = 실행중목록
        어댑터 = 복구한글어댑터(원본)
        출력 = io.StringIO()
        with contextlib.redirect_stdout(출력):
            self.assertEqual("<HWPML><BODY/></HWPML>", 어댑터.선택영역서식내보내기())
        self.assertEqual("", 출력.getvalue())

    def test_모든_한글창에_선택영역이_없을때만_안내한다(self):
        현재문서 = 가짜COM("")
        다른문서 = 가짜COM("")
        원본 = 가짜원본()
        원본.대상 = 현재문서
        원본._실행중인_한글목록 = lambda: (현재문서, 다른문서)
        어댑터 = 복구한글어댑터(원본)

        with self.assertRaisesRegex(ValueError, "선택 영역을 찾지 못했습니다"):
            어댑터.선택영역서식내보내기()

    def test_블록시작과_끝이_같으면_saveblock을_호출하지_않는다(self):
        원본 = 가짜원본()
        원본.대상 = 위치확인가짜COM((0, 0, 3), (0, 0, 3))
        원본._실행중인_한글목록 = lambda: ()
        어댑터 = 복구한글어댑터(원본)

        with self.assertRaisesRegex(ValueError, "선택 영역을 찾지 못했습니다"):
            어댑터.선택영역서식내보내기()
        self.assertEqual([], 원본.대상.호출)

    def test_블록시작과_끝이_다르면_saveblock을_내보낸다(self):
        원본 = 가짜원본()
        원본.대상 = 위치확인가짜COM((0, 0, 3), (0, 0, 12))
        원본._실행중인_한글목록 = lambda: self.fail("현재 선택이 있으면 ROT를 열거하면 안 됩니다.")
        어댑터 = 복구한글어댑터(원본)

        self.assertEqual("<HWPML/>", 어댑터.선택영역서식내보내기())
        self.assertEqual([("get", "HWPML2X", "saveblock")], 원본.대상.호출)

    def test_셀블록은_글자범위가_같거나_조회불가여도_선택으로_인식한다(self):
        for mode in (3, 19):
            for unavailable in (False, True):
                with self.subTest(mode=mode, unavailable=unavailable):
                    원본 = 가짜원본()
                    원본.대상 = 위치확인가짜COM((1, 0, 0), (1, 0, 0))
                    원본.대상.SelectionMode = mode
                    if unavailable:
                        원본.대상.GetSelectedPosBySet = lambda *_: False
                    원본._실행중인_한글목록 = lambda: self.fail("셀 선택 중 다른 문서로 전환 금지")
                    어댑터 = 복구한글어댑터(원본)
                    self.assertEqual("<HWPML/>", 어댑터.선택영역서식내보내기())
                    self.assertEqual([("get", "HWPML2X", "saveblock")], 원본.대상.호출)
                    self.assertEqual(3, 어댑터.최근선택진단["selection_kind"])

    def test_선택모드가_없으면_커서나_오래된위치를_블록으로_오인하지_않는다(self):
        원본 = 가짜원본()
        원본.대상 = 위치확인가짜COM((1, 0, 0), (2, 0, 0))
        원본.대상.SelectionMode = 0
        원본._실행중인_한글목록 = lambda: ()
        어댑터 = 복구한글어댑터(원본)
        with self.assertRaises(ValueError):
            어댑터.선택영역서식내보내기()
        self.assertEqual([], 원본.대상.호출)

    def test_새프로젝트는_로컬_호환바이트코드를_사용한다(self):
        root = _bytecode_root()
        self.assertEqual("bytecode", root.parents[0].name)
        for name in ("한컴라이브러리_기본.marshal", "한컴라이브러리_1.marshal", "한컴라이브러리_2.marshal", "한컴라이브러리.marshal"):
            self.assertTrue((root / name).is_file(), name)

    def test_미설치글꼴은_위험한_AllReplace를_호출하지_않는다(self):
        원본 = 한컴기본()
        호출 = []
        원본.대상 = type("대상", (), {"CreateAction": lambda *_: 호출.append(True)})()
        with patch.object(원본, "_폰트설치됨", return_value=False):
            self.assertFalse(원본.글자폰트바꾸기간격("없는 글꼴", "없는 대체 글꼴", -8))
        self.assertEqual([], 호출)

    def test_없는_Style_액션은_오류없이_건너뛴다(self):
        원본 = 한컴기본()
        원본.대상 = type("대상", (), {"CreateAction": lambda *_: None})()
        self.assertFalse(원본.글자스타일(1))

    def test_증감계산은_잘못된_입력에서_프로세스를_중단하지_않는다(self):
        원본 = 한컴기본()
        self.assertEqual("테스트", 원본.증감계산("테스트", "퍼센트정수"))
        self.assertEqual("0→5", 원본.증감계산("0→5", "단위정수"))

    def test_JSON변환은_빈_문서에서_오류없이_반환한다(self):
        원본 = 한컴기본()
        원본.블록텍스트 = lambda: ""
        원본.문장 = lambda *_: self.fail("빈 JSON은 문장을 삽입하지 않아야 합니다")
        self.assertFalse(원본.JSON에서변환())

    def test_공개메서드_시그니처는_원본_기본인자를_유지한다(self):
        pairs = (
            (Legacy한컴기본, 한컴기본),
            (Legacy한컴1, 한컴1),
            (Legacy한컴2, 한컴2),
            (Legacy기본한컴, 기본한컴),
        )
        for legacy, recovered in pairs:
            for name in dir(legacy):
                if name.startswith("_") or not hasattr(recovered, name):
                    continue
                original = getattr(legacy, name)
                current = getattr(recovered, name)
                if callable(original) and callable(current):
                    self.assertEqual(
                        str(inspect.signature(original)),
                        str(inspect.signature(current)),
                        f"시그니처 불일치: {name}",
                    )


if __name__ == "__main__":
    unittest.main()
