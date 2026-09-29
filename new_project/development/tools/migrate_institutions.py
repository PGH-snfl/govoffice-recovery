from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    프로젝트 = Path(__file__).resolve().parents[2]
    작업공간 = 프로젝트.parent
    원본경로 = 작업공간 / "recovered" / "institutions"
    대상경로 = 프로젝트 / "src" / "govoffice" / "institutions" / "packages"
    대상경로.mkdir(parents=True, exist_ok=True)

    기관수 = 0
    기능수 = 0
    for 원본manifest in sorted(원본경로.glob("*/manifest.json")):
        원본 = json.loads(원본manifest.read_text(encoding="utf-8"))
        대상기관 = 대상경로 / 원본["id"]
        (대상기관 / "icons").mkdir(parents=True, exist_ok=True)
        (대상기관 / "templates").mkdir(exist_ok=True)

        기능목록 = []
        for 항목 in 원본.get("functions", []):
            메서드 = 항목.get("legacy_method") or 항목.get("method")
            if not 메서드:
                continue
            기능목록.append(
                {
                    "id": 항목["id"],
                    "name": 항목["name"],
                    "method": 메서드,
                    "parameters": 항목.get("parameters", []),
                    "ui_ready": 항목.get("ui_ready", True),
                    "recovery_status": 항목.get("status", "source"),
                }
            )

        대상 = {
            "id": 원본["id"],
            "name": 원본["name"],
            "type": 원본["type"],
            "version": 원본["version"],
            "api_version": 원본["api_version"],
            "enabled": 원본.get("enabled", True),
            "legacy_window": 원본.get("legacy_window"),
            "functions": 기능목록,
        }
        (대상기관 / "manifest.json").write_text(
            json.dumps(대상, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (대상기관 / "icons" / ".gitkeep").touch()
        (대상기관 / "templates" / ".gitkeep").touch()
        기관수 += 1
        기능수 += len(기능목록)

    print(json.dumps({"institutions": 기관수, "functions": 기능수}, ensure_ascii=False))


if __name__ == "__main__":
    main()
