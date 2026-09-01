"""Integrity scan instrukcji agenta (CSA / control plane) — Faza D."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = Path(__file__).resolve().parent / "agentlint.baseline.json"

TRACKED = [
    "AGENTS.md",
    "GROUNDING.md",
    ".cursor/rules/security-tenancy.mdc",
    ".cursor/rules/no-slop.mdc",
    ".cursor/rules/context.mdc",
]

# Typowe wzorce injection w README/rules (CSA)
SUSPICIOUS = re.compile(
    r"(ignore previous instructions|disregard all rules|exfiltrate|api[_-]?key\s*=\s*['\"]sk-)",
    re.IGNORECASE,
)

MAX_ALWAYS_APPLY_HINT = 25_000  # bajty — miękki budżet pliku always-on


def _sha256(path: Path) -> str:
    # Hash po treści, nie po bajtach: przy core.autocrlf=true edytor zapisuje kontrakt
    # z CRLF, git widzi plik jako niezmieniony (indeks trzyma LF), a surowy hash
    # rozjeżdża się z baseline zbudowanym na LF w CI. Baseline LF zostaje ważny.
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _collect() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in TRACKED:
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(f"brak wymaganego pliku: {rel}")
        if path.stat().st_size > MAX_ALWAYS_APPLY_HINT:
            raise ValueError(f"{rel} przekracza budżet {MAX_ALWAYS_APPLY_HINT} B")
        text = path.read_text(encoding="utf-8")
        if SUSPICIOUS.search(text):
            raise ValueError(f"podejrzany wzorzec w {rel}")
        hashes[rel] = _sha256(path)
    return hashes


def write_baseline() -> None:
    payload = {"files": _collect()}
    BASELINE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {BASELINE_PATH}")


def check() -> int:
    if not BASELINE_PATH.is_file():
        print("agentlint: brak baseline — uruchom: python scripts/quality/agentlint.py --write")
        return 1
    expected = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))["files"]
    actual = _collect()
    if expected != actual:
        print("agentlint: hash mismatch (zmiana AGENTS/GROUNDING/rules wymaga aktualizacji baseline)")
        for key in sorted(set(expected) | set(actual)):
            if expected.get(key) != actual.get(key):
                print(f"  {key}: expected={expected.get(key)} actual={actual.get(key)}")
        print("Aktualizacja świadoma: python scripts/quality/agentlint.py --write")
        return 1
    print("agentlint: OK")
    return 0


def main() -> int:
    if "--write" in sys.argv:
        write_baseline()
        return 0
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
