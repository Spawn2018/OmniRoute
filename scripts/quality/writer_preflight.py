#!/usr/bin/env python3
"""Start sesji piszącej: /noc na main = wyłączność. Pomocnik tylko poza ROOT."""
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


def _side_lane(status: str) -> int:
    if status == "stop":
        print(
            "writer-preflight: brak żywego koordynatora /noc.",
            file=sys.stderr,
        )
        return 1
    if Path.cwd().resolve() == ROOT.resolve():
        print(
            "writer-preflight: pas pomocniczy na drzewie main = stop. Worktree.",
            file=sys.stderr,
        )
        return 1
    print("writer-preflight: OK (pas pomocniczy)")
    return 0


def main() -> int:
    allow_noc = "--allow-noc" in sys.argv
    allow_side = "--allow-noc-helper" in sys.argv
    if allow_noc and allow_side:
        print(
            "writer-preflight: --allow-noc i --allow-noc-helper naraz = stop.",
            file=sys.stderr,
        )
        return 1
    if allow_noc:
        print("writer-preflight: OK (sesja /noc)")
        return 0
    status = noc_status()
    if allow_side:
        return _side_lane(status)
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
