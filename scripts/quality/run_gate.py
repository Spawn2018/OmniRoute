#!/usr/bin/env python3
"""Lokalny just gate: zbiera code-gate i meta-gate, nie przerywa po pierwszym."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _just(recipe: str) -> int:
    print(f"\n=== {recipe} ===\n", flush=True)
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    return subprocess.call(["just", recipe], cwd=ROOT, env=env)


def main() -> int:
    code = _just("code-gate")
    meta = _just("meta-gate")
    print("\n=== podsumowanie ===")
    print(f"KOD:  {'OK' if code == 0 else 'FAIL'} (code-gate)")
    print(f"META: {'OK' if meta == 0 else 'FAIL'} (meta-gate)")
    if code != 0 or meta != 0:
        return 1
    print("gate: code-gate + meta-gate OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
