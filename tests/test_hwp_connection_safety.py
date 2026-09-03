import unittest
from unittest.mock import patch

from govoffice.runtime.recovered_hwp.한컴오피스.recovered_source.common import (
    connection as connection_module,
)
from govoffice.runtime.recovered_hwp.한컴오피스.recovered_source.common.connection import (
    HwpConnectionMixin,
)


class 가짜문서:
    def __init__(self, 소유자, 문서id="doc-1"):
        self.소유자 = 소유자
        self.DocumentID = 문서id
        self.Modified = True
        self.닫기인자 = []

    def SetActive_XHwpDocument(self):
        if self.DocumentID in self.소유자.활성화거부ids:
            return None
        self.소유자.활성문서id = self.DocumentID
        self.소유자.활성화목록.append(self.DocumentID)
        return None

    def Close(self, 저장):
        self.닫기인자.append(저장)
        if self.Modified:
            raise AssertionError("Modified를 False로 만든 뒤 닫아야 합니다.")
        if self.소유자.활성문서id != self.DocumentID:
            raise AssertionError("Close 전에 정확한 문서를 활성화해야 합니다.")
        if self.소유자.닫기반환값 is not True:
            return self.소유자.닫기반환값
        if len(self.소유자.문서들) == 1 and self.소유자.마지막문서유지:
            return True
        self.소유자.문서들.remove(self)
        self.소유자.활성문서id = (
            self.소유자.문서들[-1].DocumentID if self.소유자.문서들 else None
        )
        return True


class 가짜문서목록:
    def __init__(self, 소유자, *, 보고개수=None):
        self.소유자 = 소유자
        self.보고개수 = 보고개수

    @property
    def Count(self):
        return len(self.소유자.문서들) if self.보고개수 is None else self.보고개수

    @property
    def Active_XHwpDocument(self):
        return next(
            (
                문서
                for 문서 in self.소유자.문서들
                if 문서.DocumentID == self.소유자.활성문서id
            ),
            None,
        )

    def Item(self, 번호):
        return self.소유자.문서들[번호]


class 가짜전용대상:
    def __init__(
        self,
        문서id="doc-1",
        *,
        추가문서ids=(),
        보고개수=None,
        마지막문서유지=False,
        닫기반환값=True,
    ):
        self.문서들 = []
        self.문서 = 가짜문서(self, 문서id)
        self.문서들.append(self.문서)
        self.문서들.extend(가짜문서(self, 추가id) for 추가id in 추가문서ids)
        self.활성문서id = 문서id
        self.활성화목록 = []
        self.활성화거부ids = set()
        self.마지막문서유지 = 마지막문서유지
        self.닫기반환값 = 닫기반환값
        self.XHwpDocuments = 가짜문서목록(self, 보고개수=보고개수)
        self.Clear호출 = []
        self.Quit호출 = 0

    def Clear(self, 옵션):
        self.Clear호출.append(옵션)

    def Quit(self):
        self.Quit호출 += 1


class 시험연결(HwpConnectionMixin):
    pass


class Hwp연결안전시험(unittest.TestCase):
    def test_생성전_프로세스목록을_못읽으면_DispatchEx도_실행하지_않는다(self):
        연결 = 시험연결()
        with (
            patch.object(시험연결, "_한글프로세스식별자목록", return_value=None),
            patch.object(connection_module, "DispatchEx") as dispatch,
        ):
            with self.assertRaisesRegex(RuntimeError, "DispatchEx를 실행하지"):
                연결._새한글()
        dispatch.assert_not_called()

    def test_신규프로세스가_둘이면_Clear_Close_Quit을_0회_호출한다(self):
        연결 = 시험연결()
        대상 = 가짜전용대상()
        with (
            patch.object(
                시험연결,
                "_한글프로세스식별자목록",
                side_effect=[((100, 1000),), ((100, 1000), (200, 2000), (300, 3000))],
            ),
            patch.object(connection_module, "DispatchEx", return_value=대상),
            patch.object(connection_module, "EnsureDispatch", side_effect=lambda 값: 값),
        ):
            with self.assertRaisesRegex(RuntimeError, "0회 호출"):
                연결._새한글()

        self.assertEqual([], 대상.Clear호출)
        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual(0, 대상.Quit호출)

    def test_DocumentID가_없으면_Close_Quit을_0회_호출한다(self):
        대상 = 가짜전용대상(문서id="")
        with patch.object(
            시험연결,
            "_한글프로세스식별자목록",
            return_value=((200, 2000),),
        ):
            with self.assertRaisesRegex(RuntimeError, "DocumentID"):
                시험연결._전용Automation대상안전종료(대상, (200, 2000))

        self.assertEqual([], 대상.Clear호출)
        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual(0, 대상.Quit호출)

    def test_문서목록이_불완전하면_Close_Quit을_0회_호출한다(self):
        대상 = 가짜전용대상(보고개수=2)
        with patch.object(
            시험연결,
            "_한글프로세스식별자목록",
            return_value=((200, 2000),),
        ):
            with self.assertRaisesRegex(RuntimeError, "모든 문서"):
                시험연결._전용Automation대상안전종료(대상, (200, 2000))

        self.assertEqual([], 대상.Clear호출)
        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual(0, 대상.Quit호출)

    def test_입증된_신규프로세스는_마지막문서를_Quit으로_종료한다(self):
        연결 = 시험연결()
        대상 = 가짜전용대상()
        with (
            patch.object(
                시험연결,
                "_한글프로세스식별자목록",
                side_effect=[
                    ((100, 1000),),
                    ((100, 1000), (200, 2000)),
                    ((100, 1000), (200, 2000)),
                    ((100, 1000), (200, 2000)),
                    ((100, 1000),),
                ],
            ),
            patch.object(connection_module, "DispatchEx", return_value=대상),
            patch.object(connection_module, "EnsureDispatch", side_effect=lambda 값: 값),
            patch.object(연결, "_보안모듈등록", side_effect=RuntimeError("등록 실패")),
        ):
            with self.assertRaisesRegex(RuntimeError, "등록 실패"):
                연결._새한글()

        self.assertEqual([], 대상.Clear호출)
        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual(["doc-1"], 대상.활성화목록)
        self.assertEqual([대상.문서], 대상.문서들)
        self.assertFalse(대상.문서.Modified)
        self.assertEqual(1, 대상.Quit호출)
        self.assertIsNone(연결.대상)
        self.assertIsNone(연결._전용Automation프로세스식별자)

    def test_마지막_소유문서가_기본빈문서로_남아도_Quit으로_프로세스를_끝낸다(self):
        대상 = 가짜전용대상(마지막문서유지=True)
        with (
            patch.object(
                시험연결,
                "_한글프로세스식별자목록",
                return_value=((200, 2000),),
            ),
            patch.object(시험연결, "_프로세스식별자종료대기", return_value=True),
        ):
            결과 = 시험연결._전용Automation대상안전종료(대상, (200, 2000))

        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual(["doc-1"], 대상.활성화목록)
        self.assertEqual([대상.문서], 대상.문서들)
        self.assertFalse(대상.문서.Modified)
        self.assertEqual(1, 대상.Quit호출)
        self.assertTrue(결과["process_exited"])

    def test_활성_DocumentID가_일치하지_않으면_Close_Quit을_0회_호출한다(self):
        대상 = 가짜전용대상()
        대상.활성문서id = "다른-doc"
        대상.활성화거부ids.add("doc-1")
        with patch.object(
            시험연결,
            "_한글프로세스식별자목록",
            return_value=((200, 2000),),
        ):
            with self.assertRaisesRegex(RuntimeError, "Active DocumentID"):
                시험연결._전용Automation대상안전종료(대상, (200, 2000))

        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual(0, 대상.Quit호출)

    def test_Close가_COM정수0을_반환하면_Quit하지_않는다(self):
        대상 = 가짜전용대상(추가문서ids=("doc-2",), 닫기반환값=0)
        with patch.object(
            시험연결,
            "_한글프로세스식별자목록",
            return_value=((200, 2000),),
        ):
            with self.assertRaisesRegex(RuntimeError, r"Close\(False\)"):
                시험연결._전용Automation대상안전종료(대상, (200, 2000))

        self.assertEqual([], 대상.문서.닫기인자)
        self.assertEqual([False], 대상.문서들[1].닫기인자)
        self.assertEqual(0, 대상.Quit호출)

    def test_추가문서는_정확히_활성화해_닫고_마지막문서는_Quit에_맡긴다(self):
        대상 = 가짜전용대상(추가문서ids=("doc-2", "doc-3"))
        with (
            patch.object(
                시험연결,
                "_한글프로세스식별자목록",
                return_value=((200, 2000),),
            ),
            patch.object(시험연결, "_프로세스식별자종료대기", return_value=True),
        ):
            결과 = 시험연결._전용Automation대상안전종료(대상, (200, 2000))

        self.assertEqual(["doc-3", "doc-2", "doc-1"], 대상.활성화목록)
        self.assertEqual([대상.문서], 대상.문서들)
        self.assertEqual(["doc-3", "doc-2"], 결과["closed_document_ids"])
        self.assertEqual("doc-1", 결과["retained_document_id"])
        self.assertEqual(1, 대상.Quit호출)


if __name__ == "__main__":
    unittest.main()
