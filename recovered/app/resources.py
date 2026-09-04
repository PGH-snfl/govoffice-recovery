import sys
from pathlib import Path


def 리소스경로(*parts: str) -> Path:
    """개발 실행과 PyInstaller 실행에서 동일한 리소스 경로를 반환한다."""
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return root.joinpath(*parts)

