from __future__ import annotations

import json
import marshal
import struct
import sys
import zlib
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: extract_pyz_313.py INPUT.pyz OUTPUT_DIR")
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    output.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    if data[:4] != b"PYZ\0":
        raise SystemExit("not a PYZ archive")
    toc_offset = struct.unpack_from(">I", data, 8)[0]
    toc = marshal.loads(data[toc_offset:])
    manifest = {}
    toc_entries = toc.items() if isinstance(toc, dict) else toc
    for name, (type_code, offset, size) in toc_entries:
        relative = Path(*name.split("."))
        target = output / relative.with_suffix(".marshal")
        if size:
            blob = zlib.decompress(data[offset : offset + size])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
        manifest[name] = {
            "type": type_code,
            "offset": offset,
            "compressed_size": size,
            "output": str(target.relative_to(output)) if size else None,
        }
    (output / "pyz_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({"module_count": len(manifest), "toc_offset": toc_offset}))


if __name__ == "__main__":
    main()
