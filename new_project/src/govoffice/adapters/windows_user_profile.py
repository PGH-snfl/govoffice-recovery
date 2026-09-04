from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from ..domain.user_profile import 사용자프로필


class Windows사용자프로필저장소:
    """현재 Windows 사용자 계정의 DPAPI로 개인정보를 암호화해 보관한다."""

    def __init__(
        self,
        경로: str | Path,
        암호화: Callable[[bytes], bytes] | None = None,
        복호화: Callable[[bytes], bytes] | None = None,
    ) -> None:
        self._경로 = Path(경로)
        self._암호화 = 암호화 or self._DPAPI암호화
        self._복호화 = 복호화 or self._DPAPI복호화

    def 불러오기(self) -> 사용자프로필:
        if not self._경로.is_file():
            return 사용자프로필()
        try:
            평문 = self._복호화(self._경로.read_bytes())
            데이터 = json.loads(평문.decode("utf-8"))
            if 데이터.get("schema_version") not in {1, 2}:
                raise ValueError("지원하지 않는 사용자 프로필 형식입니다.")
            return 사용자프로필.생성(데이터.get("values", {}))
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as 오류:
            raise ValueError("저장된 사용자 프로필을 읽을 수 없습니다.") from 오류

    def 저장(self, 프로필: 사용자프로필) -> None:
        데이터 = {
            "schema_version": 2,
            "values": 프로필.사전(),
        }
        평문 = json.dumps(데이터, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        암호문 = self._암호화(평문)
        self._경로.parent.mkdir(parents=True, exist_ok=True)
        임시경로 = self._경로.with_suffix(self._경로.suffix + ".tmp")
        임시경로.write_bytes(암호문)
        임시경로.replace(self._경로)

    @staticmethod
    def _DPAPI암호화(평문: bytes) -> bytes:
        return Windows사용자프로필저장소._DPAPI처리(평문, 복호화=False)

    @staticmethod
    def _DPAPI복호화(암호문: bytes) -> bytes:
        return Windows사용자프로필저장소._DPAPI처리(암호문, 복호화=True)

    @staticmethod
    def _DPAPI처리(입력값: bytes, *, 복호화: bool) -> bytes:
        """번들 pywin32 DLL에 의존하지 않고 Windows DPAPI를 직접 호출한다."""
        import ctypes
        from ctypes import wintypes

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [
                ("cbData", wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_ubyte)),
            ]

        입력버퍼 = ctypes.create_string_buffer(입력값)
        입력블롭 = DATA_BLOB(
            len(입력값),
            ctypes.cast(입력버퍼, ctypes.POINTER(ctypes.c_ubyte)),
        )
        출력블롭 = DATA_BLOB()
        crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        crypt32.CryptProtectData.argtypes = [
            ctypes.POINTER(DATA_BLOB),
            wintypes.LPCWSTR,
            ctypes.POINTER(DATA_BLOB),
            ctypes.c_void_p,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(DATA_BLOB),
        ]
        crypt32.CryptProtectData.restype = wintypes.BOOL
        crypt32.CryptUnprotectData.argtypes = [
            ctypes.POINTER(DATA_BLOB),
            ctypes.POINTER(wintypes.LPWSTR),
            ctypes.POINTER(DATA_BLOB),
            ctypes.c_void_p,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(DATA_BLOB),
        ]
        crypt32.CryptUnprotectData.restype = wintypes.BOOL
        kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        kernel32.LocalFree.restype = ctypes.c_void_p
        금지플래그 = 0x1  # CRYPTPROTECT_UI_FORBIDDEN
        if 복호화:
            성공 = crypt32.CryptUnprotectData(
                ctypes.byref(입력블롭),
                None,
                None,
                None,
                None,
                금지플래그,
                ctypes.byref(출력블롭),
            )
        else:
            성공 = crypt32.CryptProtectData(
                ctypes.byref(입력블롭),
                "범정부오피스 사용자 프로필",
                None,
                None,
                None,
                금지플래그,
                ctypes.byref(출력블롭),
            )
        if not 성공:
            raise OSError(ctypes.get_last_error(), "Windows DPAPI 처리에 실패했습니다.")
        try:
            return ctypes.string_at(출력블롭.pbData, 출력블롭.cbData)
        finally:
            kernel32.LocalFree(출력블롭.pbData)
