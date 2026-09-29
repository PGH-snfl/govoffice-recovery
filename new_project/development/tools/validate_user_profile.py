"""현재 Windows 사용자의 DPAPI 개인정보 저장 왕복을 검증한다."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from govoffice.adapters.windows_user_profile import Windows사용자프로필저장소  # noqa: E402
from govoffice.services.user_profile import 사용자프로필서비스  # noqa: E402


REPORT = PROJECT / "development" / "reports" / "dynamic_validation" / "user_profile_storage.json"


def main() -> None:
    with tempfile.TemporaryDirectory() as 임시:
        경로 = Path(임시) / "user_profile.dat"
        저장소 = Windows사용자프로필저장소(경로)
        서비스 = 사용자프로필서비스(저장소)
        입력값 = {
            "이름": "검증사용자",
            "전화번호": "010-1111-2222",
            "이메일": "verify@example.com",
        }
        서비스.저장(입력값)
        암호문 = 경로.read_bytes()
        불러온값 = 서비스.불러오기().사전()
        평문미포함 = all(값.encode("utf-8") not in 암호문 for 값 in 입력값.values())
        왕복일치 = all(불러온값[키] == 값 for 키, 값 in 입력값.items())
        보고서 = {
            "feature": "windows_user_profile_dpapi",
            "ok": 평문미포함 and 왕복일치,
            "plaintext_absent": 평문미포함,
            "roundtrip_matches": 왕복일치,
            "encrypted_size": len(암호문),
        }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(보고서, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(보고서, ensure_ascii=False))
    raise SystemExit(0 if 보고서["ok"] else 1)


if __name__ == "__main__":
    main()
