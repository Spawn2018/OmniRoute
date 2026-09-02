#!/usr/bin/env python3
"""Start sesji piszącej: /noc aktywna = stop. Nie zastępuje pre-commit."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOC = ROOT / "docs" / "state" / "NOC-LIVE.md"


def noc_status() -> str:
    if not NOC.is_file():
        return "stop"
    for raw in NOC.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip().lower()
    return "stop"


def main() -> int:
    status = noc_status()
    if status != "stop":
        print(
            f"writer-preflight: NOC-LIVE status={status}. "
            "Druga sesja pisząca = stop. /noc jest wyłączna.",
            file=sys.stderr,
        )
        return 1
    print("writer-preflight: OK (noc nie jedzie)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
