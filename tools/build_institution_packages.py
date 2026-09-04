from __future__ import annotations

import json
from pathlib import Path


기관목록 = {
    "namhae": "남해",
    "seoul": "서울",
    "gyeongnam": "경남도",
    "incheon": "인천",
    "gyeonggi": "경기",
    "yongin": "용인",
    "buan": "부안",
    "jeju": "제주",
    "yeongdeok": "영덕",
    "gurye": "구례",
    "chungju": "충주",
    "geumcheon": "금천",
    "gwangju": "광주광역",
    "gwangsan": "광주광산",
    "gwangju_bukgu": "광주북구",
    "namyangju": "남양주",
    "chungnam": "충남",
    "buyeo": "부여",
    "hapcheon": "합천",
    "uijeongbu": "의정부",
    "hongseong": "홍성",
    "gangwon": "강원",
    "sejong": "세종",
}


def 전체_hwp_메서드(manifest: dict) -> dict[str, dict]:
    결과 = {}
    for 모듈 in manifest["modules"].values():
        for 메서드 in 모듈["methods"]:
            결과.setdefault(메서드["name"], 메서드)
    return 결과


def main() -> None:
    루트 = Path(__file__).resolve().parents[1]
    복구 = 루트 / "recovered"
    hwp_manifest = json.loads(
        (복구 / "metadata" / "hwp_api_manifest.json").read_text(encoding="utf-8")
    )
    전체메서드 = 전체_hwp_메서드(hwp_manifest)
    기관루트 = 복구 / "institutions"

    카탈로그 = []
    for 기관id, 접두어 in 기관목록.items():
        패키지 = 기관루트 / 기관id
        함수폴더 = 패키지 / "functions"
        아이콘폴더 = 패키지 / "icons"
        서식폴더 = 패키지 / "templates"
        함수폴더.mkdir(parents=True, exist_ok=True)
        아이콘폴더.mkdir(exist_ok=True)
        서식폴더.mkdir(exist_ok=True)

        메서드목록 = sorted(이름 for 이름 in 전체메서드 if 이름.startswith(접두어))
        기능목록 = [
            {
                "id": f"{기관id}.{이름}",
                "name": 이름,
                "handler": "functions.legacy:실행",
                "legacy_method": 이름,
                "parameters": 전체메서드[이름]["args"][1:],
                "ui_ready": len(전체메서드[이름]["args"]) == 1,
                "status": "legacy-compatible",
            }
            for 이름 in 메서드목록
        ]
        manifest = {
            "id": 기관id,
            "name": 접두어,
            "type": "local-government",
            "version": "0.1.0",
            "api_version": "1",
            "enabled": True,
            "legacy_window": f"{접두어}창",
            "functions": 기능목록,
        }
        (패키지 / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (패키지 / "__init__.py").write_text(
            f'"""{접두어} 기관 기능 패키지."""\n', encoding="utf-8"
        )
        (함수폴더 / "__init__.py").write_text(
            "from .legacy import 실행\n\n__all__ = [\"실행\"]\n", encoding="utf-8"
        )
        (함수폴더 / "legacy.py").write_text(
            '"""소스화 전 기관 함수를 원본 호환 facade에 연결한다."""\n\n'
            "def 실행(한컴, 기능, *args, **kwargs):\n"
            "    메서드 = getattr(한컴, 기능)\n"
            "    return 메서드(*args, **kwargs)\n",
            encoding="utf-8",
        )
        (아이콘폴더 / ".gitkeep").touch()
        (서식폴더 / ".gitkeep").touch()
        카탈로그.append(
            {
                "id": 기관id,
                "name": 접두어,
                "version": "0.1.0",
                "function_count": len(기능목록),
            }
        )

    카탈로그경로 = 복구 / "config" / "institution_catalog.json"
    카탈로그경로.parent.mkdir(parents=True, exist_ok=True)
    카탈로그경로.write_text(
        json.dumps({"institutions": 카탈로그}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"institutions": len(카탈로그), "functions": sum(x["function_count"] for x in 카탈로그)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
