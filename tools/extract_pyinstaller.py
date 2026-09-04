from __future__ import annotations

import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path, PureWindowsPath


MAGIC = b"MEI\x0c\x0b\x0a\x0b\x0e"
COOKIE = ">8sIIII64s"


def safe_relative(name: str) -> Path:
    parts = [part for part in PureWindowsPath(name).parts if part not in ("", ".", "..", "\\")]
    if not parts:
        return Path("unnamed")
    return Path(*parts)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: extract_pyinstaller.py INPUT.exe OUTPUT_DIR")

    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    extracted = output / "extracted"
    extracted.mkdir(exist_ok=True)

    data = source.read_bytes()
    cookie_offset = data.rfind(MAGIC)
    if cookie_offset < 0:
        raise SystemExit("PyInstaller cookie not found")

    magic, package_size, toc_offset, toc_size, python_version, python_library = struct.unpack_from(
        COOKIE, data, cookie_offset
    )
    archive_base = len(data) - package_size
    pos = archive_base + toc_offset
    toc_end = pos + toc_size
    entries: list[dict[str, object]] = []

    while pos < toc_end:
        entry_size = struct.unpack_from(">I", data, pos)[0]
        entry_pos, compressed_size, uncompressed_size, compressed, type_code = struct.unpack_from(
            ">IIIBc", data, pos + 4
        )
        name = data[pos + 18 : pos + entry_size].split(b"\0", 1)[0].decode("utf-8", "replace")
        blob = data[archive_base + entry_pos : archive_base + entry_pos + compressed_size]
        if compressed:
            blob = zlib.decompress(blob)

        relative = safe_relative(name)
        if type_code in (b"m", b"s"):
            relative = Path("code") / relative.with_suffix(".marshal")
        else:
            relative = Path("resources") / relative
        target = extracted / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)

        entries.append(
            {
                "name": name,
                "type": type_code.decode("latin1"),
                "compressed": bool(compressed),
                "compressed_size": compressed_size,
                "uncompressed_size": uncompressed_size,
                "output": str(relative),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
        pos += entry_size

    metadata = {
        "source": str(source),
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "source_size": len(data),
        "cookie_offset": cookie_offset,
        "package_size": package_size,
        "archive_base": archive_base,
        "python_version": python_version,
        "python_library": python_library.split(b"\0", 1)[0].decode("ascii", "replace"),
        "entry_count": len(entries),
        "entries": entries,
    }
    (output / "archive_manifest.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({key: metadata[key] for key in ("source_sha256", "python_version", "python_library", "entry_count")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
