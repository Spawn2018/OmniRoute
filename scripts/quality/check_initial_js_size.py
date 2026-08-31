"""Initial JS gzip must stay under AGENTS.md budget (250 kB)."""

from __future__ import annotations

import gzip
import re
import sys
from pathlib import Path

LIMIT_BYTES = 250 * 1024
SCRIPT_SRC = re.compile(r"""(?:src|href)=["']([^"']+\.js)["']""")


def script_paths(index_html: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for match in SCRIPT_SRC.finditer(index_html):
        src = match.group(1)
        if src in seen:
            continue
        seen.add(src)
        found.append(src)
    return found


def gzip_bytes(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), compresslevel=9))


def initial_js_gzip_bytes(dist_dir: Path) -> int:
    index = dist_dir / "index.html"
    if not index.is_file():
        raise FileNotFoundError(f"brak {index} — najpierw pnpm build")
    total = 0
    for src in script_paths(index.read_text(encoding="utf-8")):
        relative = src.lstrip("/")
        asset = dist_dir / relative
        if not asset.is_file():
            raise FileNotFoundError(f"brak assetu initial JS: {asset}")
        total += gzip_bytes(asset)
    return total


def main(argv: list[str]) -> int:
    dist_dir = Path(argv[1] if len(argv) > 1 else "frontend/dist")
    size = initial_js_gzip_bytes(dist_dir)
    if size >= LIMIT_BYTES:
        print(f"FAIL: initial JS gzip {size} B >= {LIMIT_BYTES} B", file=sys.stderr)
        return 1
    print(f"OK: initial JS gzip {size} B < {LIMIT_BYTES} B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
