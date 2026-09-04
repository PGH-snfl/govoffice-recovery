import json
import tempfile
import unittest
from pathlib import Path

from govoffice.adapters.json_style_presets import JSON서식프리셋저장소
from govoffice.adapters.json_user_profile import JSON사용자프로필저장소
from govoffice.adapters.windows_user_profile import Windows사용자프로필저장소
from govoffice.domain.presets import 서식필드, 서식프리셋
from govoffice.domain.user_profile import 사용자프로필
from govoffice.services.profile_fill import HWPML개인정보채우기
from govoffice.services.style_presets import 서식프리셋서비스
from govoffice.services.user_profile import 사용자프로필서비스


개인정보_HWPML = """<HWPML><BODY><SECTION>
<P><TEXT><CHAR>성명</CHAR></TEXT></P><P><TEXT><CHAR></CHAR></TEXT></P>
<P><TEXT><CHAR>전화번호</CHAR></TEXT></P><P><TEXT><CHAR>010-9999-8888</CHAR></TEXT></P>
<P><TEXT><CHAR>이메일: old@example.com</CHAR></TEXT></P>
<P><TEXT><CHAR>부서</CHAR></TEXT></P><P><TEXT><CHAR>기존부서</CHAR></TEXT></P>
</SECTION></BODY></HWPML>"""


class 가짜한글:
    def __init__(self) -> None:
        self.삽입텍스트 = []
        self.출력hwpml = None

    def 문장(self, 내용: str) -> None:
        self.삽입텍스트.append(내용)

    def 선택영역서식내보내기(self) -> str:
        return 개인정보_HWPML

    def 선택영역새문서생성(self, hwpml: str):
        self.출력hwpml = hwpml
        return True

    def 서식조각삽입(self, hwpml: str):
        self.출력hwpml = hwpml
        return True


class 사용자프로필시험(unittest.TestCase):
    def test_기존대표필드를_값과_ID를_유지한채_새대표필드의_하위로_옮긴다(self):
        프로필 = 사용자프로필.생성({})
        프로필 = 프로필.대표필드추가(
            "직장전화",
            ("010-1111-2222", "010-3333-4444"),
            ("휴대폰",),
        )
        기존ID = 프로필.대표필드찾기("직장전화").id
        프로필 = 프로필.대표필드추가("연락수단")

        결과 = 프로필.대표필드상위변경(기존ID, "연락수단")
        하위 = 결과.대표필드찾기("연락수단 > 직장전화")
        self.assertEqual(기존ID, 하위.id)
        self.assertEqual(("010-1111-2222", "010-3333-4444"), 하위.값목록)
        self.assertEqual(("휴대폰",), 하위.별칭)
        self.assertEqual("연락수단 > 직장전화", 결과.필드경로(하위))

        결과 = 결과.대표필드값추가(하위.id, "010-5555-6666")
        self.assertEqual(
            ("010-1111-2222", "010-3333-4444", "010-5555-6666"),
            결과.필드값찾기("연락수단 > 직장전화"),
        )

    def test_하위필드가_있는_대표필드도_다른_대표필드_아래로_통째로_옮긴다(self):
        프로필 = 사용자프로필.생성({})
        프로필 = 프로필.대표필드추가("과제 정보")
        프로필 = 프로필.하위필드추가("과제 정보", "과제명", ("문서 자동화",))
        프로필 = 프로필.대표필드추가("신청서")
        과제정보ID = 프로필.필드ID찾기("과제 정보")
        과제명ID = 프로필.필드ID찾기("과제 정보 > 과제명")

        결과 = 프로필.대표필드상위변경(과제정보ID, "신청서")

        중간 = 결과.대표필드찾기("신청서 > 과제 정보")
        하위 = 결과.대표필드찾기("신청서 > 과제 정보 > 과제명")
        self.assertEqual(과제정보ID, 중간.id)
        self.assertEqual(과제명ID, 하위.id)
        self.assertEqual(("문서 자동화",), 하위.값목록)
        self.assertEqual("신청서 > 과제 정보 > 과제명", 결과.필드경로(하위))
        with self.assertRaisesRegex(ValueError, "후손"):
            결과.대표필드상위변경(중간.id, 하위.id)

    def test_같은이름의_하위필드가_있으면_자동병합하지_않고_이동을_거부한다(self):
        프로필 = 사용자프로필.생성({})
        프로필 = 프로필.대표필드추가("연구자 정보")
        프로필 = 프로필.하위필드추가("연구자 정보", "성명", ("홍길동",))
        프로필 = 프로필.대표필드추가("책임자 정보")
        프로필 = 프로필.하위필드추가("책임자 정보", "성명", ("김철수",))
        연구자성명 = 프로필.대표필드찾기("연구자 정보 > 성명")
        책임자정보 = 프로필.대표필드찾기("책임자 정보")

        with self.assertRaisesRegex(ValueError, "자동 병합하지 않습니다"):
            프로필.대표필드상위변경(연구자성명.id, 책임자정보.id)

        self.assertEqual(("홍길동",), 프로필.필드값찾기("연구자 정보 > 성명"))
        self.assertEqual(("김철수",), 프로필.필드값찾기("책임자 정보 > 성명"))

    def test_대표필드_아래_하위필드는_같은_별칭을_각_그룹에서_쓸수있다(self):
        프로필 = 사용자프로필.생성({})
        프로필 = 프로필.대표필드추가("연구책임자")
        프로필 = 프로필.하위필드추가(
            "연구책임자", "이름", ("홍길동",), ("성명", "성함")
        )
        프로필 = 프로필.대표필드추가("참여연구자")
        프로필 = 프로필.하위필드추가(
            "참여연구자", "이름", ("김철수",), ("성명", "성함")
        )

        책임자이름 = 프로필.대표필드찾기("연구책임자 > 성명")
        연구자이름 = 프로필.대표필드찾기("참여연구자 > 성명")
        self.assertIsNotNone(책임자이름)
        self.assertIsNotNone(연구자이름)
        self.assertNotEqual(책임자이름.id, 연구자이름.id)
        self.assertEqual(("홍길동",), 프로필.필드값찾기("연구책임자 > 이름"))
        self.assertEqual(("김철수",), 프로필.필드값찾기("참여연구자 > 이름"))
        self.assertEqual(
            ("이름",),
            tuple(필드.대표필드명 for 필드 in 프로필.하위필드목록("연구책임자")),
        )

    def test_하위필드_부모ID를_JSON_v4로_왕복한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            경로 = Path(임시) / "user_profile.json"
            저장소 = JSON사용자프로필저장소(경로)
            프로필 = 사용자프로필.생성({}).대표필드추가("연구책임자")
            프로필 = 프로필.하위필드추가("연구책임자", "전화번호", ("02-123-4567",))
            저장소.저장(프로필)

            다시읽기 = 저장소.불러오기()
            하위 = 다시읽기.대표필드찾기("연구책임자 > 전화번호")
            상위 = 다시읽기.대표필드찾기("연구책임자")
            self.assertEqual(상위.id, 하위.상위필드id)
            self.assertEqual(4, json.loads(경로.read_text(encoding="utf-8"))["schema_version"])

    def test_내부용_JSON은_확장된_필드값관계를_왕복한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            저장소 = JSON사용자프로필저장소(Path(임시) / "user_profile.json")
            서비스 = 사용자프로필서비스(저장소)
            서비스.저장(
                {
                    "이름": "홍길동",
                    "전화번호": "010-1234-5678",
                    "이메일": "hong@example.com",
                    "문서항목": [
                        {"필드명": "과제명", "입력값": "범정부오피스"},
                        {"필드명": "과제명", "입력값": "문서 자동화"},
                    ],
                }
            )
            결과 = 저장소.불러오기()
            self.assertEqual(("범정부오피스", "문서 자동화"), 결과.필드값목록()["과제명"])
            데이터 = (Path(임시) / "user_profile.json").read_text(encoding="utf-8")
            self.assertIn('"schema_version": 4', 데이터)
            self.assertIn('"대표필드목록"', 데이터)

    def test_schema_v2를_대표필드_v3로_이전하고_ID를_고정한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            경로 = Path(임시) / "user_profile.json"
            경로.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "values": {
                            "이름": "홍길동",
                            "전화번호": "010-1234-5678",
                            "이메일": "hong@example.com",
                            "문서항목": [
                                {"필드명": "과제명", "입력값": "범정부오피스"},
                                {"필드명": "과제명", "입력값": "문서 자동화"},
                            ],
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            저장소 = JSON사용자프로필저장소(경로)

            이전결과 = 저장소.불러오기()
            과제필드 = 이전결과.대표필드찾기("과제명")
            self.assertIsNotNone(과제필드)
            assert 과제필드 is not None
            self.assertTrue(과제필드.id.startswith("profile_field_"))
            self.assertEqual(("범정부오피스", "문서 자동화"), 과제필드.값목록)

            저장소.저장(이전결과)
            저장ID = 과제필드.id
            재로드 = 저장소.불러오기()
            self.assertEqual(저장ID, 재로드.대표필드찾기("과제명").id)
            self.assertEqual(4, json.loads(경로.read_text(encoding="utf-8"))["schema_version"])

    def test_대표필드의_별칭과_여러값을_해석하고_기본값을_선택한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            저장소 = JSON사용자프로필저장소(Path(임시) / "user_profile.json")
            서비스 = 사용자프로필서비스(저장소)
            서비스.대표필드추가(
                "과제명",
                ("범정부오피스", "문서 자동화", "범정부오피스"),
                ("사업명", "프로젝트명"),
            )
            서비스.대표필드값추가("사업명", "대학혁신사업")
            결과 = 서비스.기본값지정("프로젝트명", "대학혁신사업")

            self.assertEqual("과제명", 결과.대표필드명찾기("사업명"))
            self.assertEqual(결과.대표필드찾기("과제명").id, 결과.필드ID찾기("사업명"))
            self.assertEqual(
                결과.필드ID찾기("과제명"), 결과.대표필드ID매핑()["과제명"]
            )
            self.assertEqual(
                ("범정부오피스", "문서 자동화", "대학혁신사업"),
                결과.필드값찾기("프로젝트명"),
            )
            self.assertEqual("대학혁신사업", 결과.필드기본값찾기("사업명"))
            self.assertEqual(
                결과.필드값목록()["과제명"],
                결과.별칭포함필드값목록()["사업명"],
            )
            self.assertEqual(("사업명", "프로젝트명"), 결과.별칭매핑()["과제명"])
            self.assertEqual("과제명", 결과.별칭대표필드매핑()["사업명"])
            self.assertEqual("대학혁신사업", 서비스.자동입력값()["프로젝트명"])
            self.assertEqual(
                "대학혁신사업", 서비스.자동입력값()[결과.필드ID찾기("과제명")]
            )

    def test_사용자필드를_대표필드에_병합해_값과_별칭을_이어간다(self):
        프로필 = 사용자프로필.생성({})
        프로필 = 프로필.대표필드추가("과제명", ("주과제",), ("프로젝트명",))
        프로필 = 프로필.대표필드추가("사업명", ("부과제",), ("사업 제목",))
        대상ID = 프로필.필드ID찾기("과제명")

        결과 = 프로필.대표필드병합("사업명", "과제명")

        self.assertEqual(대상ID, 결과.필드ID찾기("과제명"))
        self.assertEqual("과제명", 결과.대표필드명찾기("사업명"))
        self.assertEqual("과제명", 결과.대표필드명찾기("사업 제목"))
        self.assertEqual(("주과제", "부과제"), 결과.필드값찾기("프로젝트명"))
        with self.assertRaisesRegex(ValueError, "기본 대표 필드"):
            결과.대표필드병합("이름", "과제명")

    def test_프리셋_자동출력은_표시이름보다_안정ID를_우선한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            한글 = 가짜한글()
            저장소 = JSON서식프리셋저장소(Path(임시) / "presets")
            저장소.저장(
                서식프리셋(
                    id="style_stableidpreset",
                    이름="안정 ID",
                    hwpml="<HWPML><BODY><P><CHAR>{{GOVOFFICE_FIELD_1}}</CHAR></P></BODY></HWPML>",
                    필드목록=(
                        서식필드(
                            id="field-1",
                            토큰="{{GOVOFFICE_FIELD_1}}",
                            안내문구="과거 표시명",
                            값유형="과거 표시명",
                            프로필필드id="profile-stable-1",
                        ),
                    ),
                    내용정책="registered_fields",
                )
            )
            서비스 = 서식프리셋서비스(
                한글,
                저장소,
                개인정보제공=lambda: {
                    "profile-stable-1": "안정 ID 값",
                    "과거 표시명": "이름 조회 값",
                },
            )

            self.assertTrue(서비스.출력("style_stableidpreset"))
            self.assertIn("안정 ID 값", 한글.출력hwpml)
            self.assertNotIn("이름 조회 값", 한글.출력hwpml)

    def test_기본필드도_대표필드로_별칭과_여러값을_보존한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            저장소 = JSON사용자프로필저장소(Path(임시) / "user_profile.json")
            서비스 = 사용자프로필서비스(저장소)
            서비스.저장({"이름": "홍길동"})
            서비스.별칭추가("이름", "성명")
            서비스.대표필드값추가("성명", "김철수")
            결과 = 서비스.기본값지정("이름", "김철수")

            self.assertEqual("김철수", 결과.이름)
            self.assertEqual(("홍길동", "김철수"), 결과.필드값찾기("성명"))
            self.assertEqual("이름", 결과.대표필드명찾기("성명"))

    def test_기본대표필드는_v2와_별칭없는_v3에서도_표준별칭을_보강한다(self):
        v2결과 = 사용자프로필.생성(
            {
                "이름": "홍길동",
                "문서항목": [{"필드명": "성명", "입력값": "김철수"}],
            }
        )
        self.assertEqual("이름", v2결과.대표필드명찾기("성명"))
        self.assertEqual(("홍길동", "김철수"), v2결과.필드값찾기("성함"))
        self.assertEqual("전화번호", v2결과.대표필드명찾기("연락처"))
        self.assertEqual("이메일", v2결과.대표필드명찾기("E-mail"))

        v3결과 = 사용자프로필.생성(
            {
                "대표필드목록": [
                    {"id": "fixed_name", "대표필드명": "이름", "값목록": ["홍길동"]},
                    {"id": "fixed_phone", "대표필드명": "전화번호"},
                    {"id": "fixed_email", "대표필드명": "이메일"},
                    {"id": "fixed_person", "대표필드명": "성명", "값목록": ["별도 인물"]},
                ]
            }
        )
        self.assertEqual("성명", v3결과.대표필드명찾기("성명"))
        self.assertEqual("이름", v3결과.대표필드명찾기("성함"))

    def test_같은_별칭을_서로_다른_대표필드에_지정하지_않는다(self):
        프로필 = 사용자프로필.생성({}).대표필드추가("책임자", ("홍길동",), ("담당자명",))
        프로필 = 프로필.대표필드추가("연구자", ("홍길동",))
        with self.assertRaisesRegex(ValueError, "사용 중"):
            프로필.별칭추가("연구자", "담당자명")

    def test_같은필드의_여러값과_같은값의_여러필드를_관계로_보존한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            저장소 = Windows사용자프로필저장소(
                Path(임시) / "profile.dat",
                암호화=lambda 값: 값,
                복호화=lambda 값: 값,
            )
            서비스 = 사용자프로필서비스(저장소)
            서비스.저장({"이름": "홍길동", "전화번호": "010-1234-5678", "이메일": "hong@example.com"})
            서비스.문서항목추가("과제명", "범정부오피스")
            서비스.문서항목추가("과제명", "문서 자동화")
            서비스.문서항목추가("책임자", "홍길동")
            서비스.문서항목추가("연구자", "홍길동")
            서비스.문서항목추가("연구자", "홍길동")

            프로필 = 서비스.불러오기()
            self.assertEqual(("범정부오피스", "문서 자동화"), 프로필.필드값목록()["과제명"])
            self.assertEqual(("이름", "책임자", "연구자"), 프로필.값별필드목록()["홍길동"])
            self.assertEqual(4, len(프로필.문서항목))
            with self.assertRaisesRegex(ValueError, "상단의 기본 정보"):
                서비스.문서항목추가("이름", "다른 이름")

    def test_JSON_기타항목은_추가_중복제외_삭제까지_왕복한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            경로 = Path(임시) / "user_profile.json"
            저장소 = JSON사용자프로필저장소(경로)
            서비스 = 사용자프로필서비스(저장소)

            서비스.문서항목추가("과제명", "범정부오피스")
            서비스.문서항목추가("과제명", "범정부오피스")
            self.assertEqual(1, len(서비스.불러오기().문서항목))

            서비스.문서항목삭제("과제명", "범정부오피스")
            self.assertEqual((), 서비스.불러오기().문서항목)
            self.assertEqual([], list(Path(임시).glob(".*.tmp")))

    def test_이전_고정필드는_기타문서항목으로_자동이전한다(self):
        결과 = 사용자프로필.생성({"이름": "홍길동", "소속": "서울과기대", "부서": "정보전산원"})
        self.assertEqual(("서울과기대",), 결과.필드값목록()["소속"])
        self.assertEqual(("정보전산원",), 결과.필드값목록()["부서"])

    def test_프로필은_평문이_아닌_암호문으로_저장하고_왕복한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            경로 = Path(임시) / "profile.dat"
            저장소 = Windows사용자프로필저장소(
                경로,
                암호화=lambda 평문: b"ENCRYPTED:" + 평문[::-1],
                복호화=lambda 암호문: 암호문.removeprefix(b"ENCRYPTED:")[::-1],
            )
            서비스 = 사용자프로필서비스(저장소)
            서비스.저장({"이름": "홍길동", "전화번호": "010-1234-5678", "이메일": "hong@example.com"})

            암호문 = 경로.read_bytes()
            self.assertNotIn("홍길동".encode(), 암호문)
            self.assertEqual("홍길동", 서비스.불러오기().이름)
            self.assertEqual("010-1234-5678", 서비스.불러오기().전화번호)

    def test_개인탭_값은_현재커서에_텍스트만_삽입한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            저장소 = Windows사용자프로필저장소(
                Path(임시) / "profile.dat",
                암호화=lambda 값: 값,
                복호화=lambda 값: 값,
            )
            한글 = 가짜한글()
            서비스 = 사용자프로필서비스(저장소, 한글)
            서비스.저장({"이름": "홍길동", "이메일": "hong@example.com"})

            self.assertEqual("홍길동", 서비스.텍스트삽입("이름"))
            self.assertEqual(["홍길동"], 한글.삽입텍스트)
            with self.assertRaisesRegex(ValueError, "전화번호 값을 먼저 저장"):
                서비스.텍스트삽입("전화번호")

    def test_라벨의_옆칸과_인라인값을_개인정보로_채운다(self):
        결과 = HWPML개인정보채우기().채우기(
            개인정보_HWPML,
            {
                "이름": "홍길동",
                "전화번호": "010-1234-5678",
                "이메일": "hong@example.com",
                "부서": "정보화전략팀",
            },
        )
        self.assertIn("홍길동", 결과)
        self.assertIn("010-1234-5678", 결과)
        self.assertIn("이메일: hong@example.com", 결과)
        self.assertIn("정보화전략팀", 결과)
        self.assertNotIn("010-9999-8888", 결과)
        self.assertNotIn("old@example.com", 결과)
        self.assertNotIn("기존부서", 결과)

    def test_등록필드가_없으면_프리셋원본과_출력본을_그대로_유지한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            한글 = 가짜한글()
            저장소 = JSON서식프리셋저장소(Path(임시) / "presets")
            서비스 = 서식프리셋서비스(한글, 저장소, 개인정보제공=lambda: {})

            프리셋 = 서비스.선택영역저장("자동 입력")
            self.assertEqual(개인정보_HWPML, 저장소.불러오기(프리셋.id).hwpml)
            self.assertTrue(서비스.출력(프리셋.id))
            self.assertEqual(개인정보_HWPML, 한글.출력hwpml)
            self.assertEqual(개인정보_HWPML, 저장소.불러오기(프리셋.id).hwpml)

    def test_사용자탭에_저장된_값만_필드로_분류하고_다른_사용자값으로_출력한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            한글 = 가짜한글()
            저장소 = JSON서식프리셋저장소(Path(임시) / "presets")
            현재값 = {"이름": "", "전화번호": "010-9999-8888", "이메일": "old@example.com"}
            서비스 = 서식프리셋서비스(한글, 저장소, 개인정보제공=lambda: 현재값)

            프리셋 = 서비스.선택영역저장("등록 필드 분류")
            저장본 = 저장소.불러오기(프리셋.id)
            self.assertEqual("registered_fields", 저장본.내용정책)
            self.assertEqual(2, 저장본.필드수)
            self.assertNotIn("010-9999-8888", 저장본.hwpml)
            self.assertNotIn("old@example.com", 저장본.hwpml)
            self.assertIn("기존부서", 저장본.hwpml)

            현재값.update({"전화번호": "010-1234-5678", "이메일": "new@example.com"})
            self.assertTrue(서비스.출력(프리셋.id))
            self.assertIn("010-1234-5678", 한글.출력hwpml)
            self.assertIn("new@example.com", 한글.출력hwpml)
            self.assertIn("기존부서", 한글.출력hwpml)

    def test_등록필드는_있지만_선택영역에_일치값이_없으면_원본을_그대로_저장한다(self):
        with tempfile.TemporaryDirectory() as 임시:
            한글 = 가짜한글()
            저장소 = JSON서식프리셋저장소(Path(임시) / "presets")
            서비스 = 서식프리셋서비스(
                한글,
                저장소,
                개인정보제공=lambda: {"이름": "홍길동", "부서": "정보전산원"},
            )

            프리셋 = 서비스.선택영역저장("일치 없음")
            저장본 = 저장소.불러오기(프리셋.id)
            self.assertEqual("original", 저장본.내용정책)
            self.assertEqual((), 저장본.필드목록)
            self.assertEqual(개인정보_HWPML, 저장본.hwpml)


if __name__ == "__main__":
    unittest.main()
