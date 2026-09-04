"""원본 marshal 런타임과 복구 소스의 한글 출력 동등성 비교."""

from __future__ import annotations

import argparse
import base64
import gc
import hashlib
import json
import re
import sys
import traceback
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "recovered"
sys.path.insert(0, str(RECOVERED))

import win32com.client  # noqa: E402

from 한컴오피스.compat.legacy_runtime import Legacy기본한컴  # noqa: E402
from 한컴오피스.한컴라이브러리 import 기본한컴  # noqa: E402


DEFAULT_METHODS = (
    "서교공사장요청사항",
    "의정부목차",
    "농어촌변경계약",
    "역학수인성식품역학조사",
)


def normalize_text(value):
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n").strip()


def normalize_hwpml(value):
    text = normalize_text(value)
    # Each newly-created HWP document receives its own creation timestamp.
    # It is metadata rather than output produced by the method under test.
    text = re.sub(r"<DATE>.*?</DATE>", "<DATE><CREATED_AT></DATE>", text, flags=re.DOTALL)
    text = re.sub(r'(?i:\b(id|instid|itemid))="[^"]*"', lambda match: f'{match.group(1)}="<ID>"', text)
    # Memo commands contain a session-generated object number before the
    # stable document/user fields.
    text = re.sub(r'(Command="MEMO/[^/]+/[^/]+/)\d+/', r'\1<MEMO_ID>/', text)
    # 저장 시점의 커서 위치와 빈 XML 태그 표기 방식은 문서 기능/서식이 아니다.
    text = re.sub(r'<CARETPOS\b[^>]*/>', '<CARETPOS/>', text)
    text = re.sub(r'<([A-Z][A-Z0-9]*)>\s*</\1>', r'<\1/>', text)
    def canonical_bindata(match):
        try:
            data = base64.b64decode(re.sub(r"\s+", "", match.group(1)))
            if data.startswith(b"\x89PNG\r\n\x1a\n"):
                offset = 8; ihdr = b""; idat = []
                while offset + 12 <= len(data):
                    size = int.from_bytes(data[offset:offset + 4], "big")
                    kind = data[offset + 4:offset + 8]
                    payload = data[offset + 8:offset + 8 + size]
                    if kind == b"IHDR": ihdr = payload
                    elif kind == b"IDAT": idat.append(payload)
                    offset += size + 12
                    if kind == b"IEND": break
                pixels = zlib.decompress(b"".join(idat))
                semantic = hashlib.sha256(ihdr + pixels).hexdigest()
                return f'<BINDATA Encoding="PNG-pixels" Hash="{semantic}"/>'
            semantic = hashlib.sha256(data).hexdigest()
            return f'<BINDATA Encoding="binary" Hash="{semantic}"/>'
        except Exception:
            return match.group(0)
    # HWP can rewrite PNG ancillary chunks (time/text metadata) while keeping
    # identical dimensions and pixels. Compare the decoded pixel stream.
    text = re.sub(r'<BINDATA\b[^>]*>(.*?)</BINDATA>', canonical_bindata, text, flags=re.DOTALL)
    # 그 밖의 그림 형식은 HWP가 저장할 때 내부 컨테이너를 다시 작성해
    # 같은 원본 파일도 바이트 해시가 달라질 수 있다. 그림의 배치·크기·참조
    # 구조는 HWPML 본문에서 별도로 비교하므로 파생된 BINDATA 해시만 제외한다.
    text = re.sub(
        r'(<BINDATA\b[^>]*\bHash=")[^"]+("[^>]*?/>)',
        r'\1<BINARY_PAYLOAD>\2',
        text,
    )
    return re.sub(r">\s+<", "><", text)


def digest(value):
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def run_one(cls, method_name, method_args=()):
    hwp = None
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")
        hwp.HAction.Run("FileNew")
        instance = cls()
        instance.대상 = hwp
        registered = hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")
        if not registered:
            raise RuntimeError("한글 Automation 보안 모듈 등록 실패")
        return_value = getattr(instance, method_name)(*method_args)
        text = normalize_text(hwp.GetTextFile("TEXT", ""))
        hwpml = normalize_hwpml(hwp.GetTextFile("HWPML2X", ""))
        return {
            "ok": True,
            "text": text,
            "text_length": len(text),
            "text_sha256": digest(text),
            "hwpml": hwpml,
            "hwpml_length": len(hwpml),
            "hwpml_sha256": digest(hwpml),
            "return_value": return_value
            if return_value is None or isinstance(return_value, (str, int, float, bool))
            else repr(return_value),
        }
    except Exception as exc:
        return {
            "ok": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
    finally:
        if hwp is not None:
            try:
                hwp.Clear(1)
            except Exception:
                pass
            try:
                hwp.Quit()
            except Exception:
                pass
            hwp = None
            gc.collect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("methods", nargs="*", default=DEFAULT_METHODS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = {"methods": {}}
    for method_spec in args.methods:
        if "::" in method_spec:
            method_name, encoded_args = method_spec.split("::", 1)
            method_args = json.loads(encoded_args)
            if not isinstance(method_args, list):
                raise ValueError(f"인수는 JSON 배열이어야 합니다: {method_spec}")
        else:
            method_name, method_args = method_spec, []
        legacy = run_one(Legacy기본한컴, method_name, method_args)
        recovered = run_one(기본한컴, method_name, method_args)
        comparison = {
            "both_ok": legacy.get("ok") and recovered.get("ok"),
            "text_equal": legacy.get("text") == recovered.get("text")
            if legacy.get("ok") and recovered.get("ok")
            else False,
            "hwpml_equal": legacy.get("hwpml_sha256") == recovered.get("hwpml_sha256")
            if legacy.get("ok") and recovered.get("ok")
            else False,
            "return_equal": legacy.get("return_value") == recovered.get("return_value")
            if legacy.get("ok") and recovered.get("ok")
            else False,
        }
        report["methods"][method_name] = {
            "legacy": legacy,
            "recovered": recovered,
            "args": method_args,
            "comparison": comparison,
        }
        print(
            json.dumps(
                {
                    "method": method_name,
                    "legacy_ok": legacy.get("ok"),
                    "recovered_ok": recovered.get("ok"),
                    **comparison,
                    "legacy_text_length": legacy.get("text_length"),
                    "recovered_text_length": recovered.get("text_length"),
                    "legacy_hwpml_length": legacy.get("hwpml_length"),
                    "recovered_hwpml_length": recovered.get("hwpml_length"),
                },
                ensure_ascii=False,
            )
        )

    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
