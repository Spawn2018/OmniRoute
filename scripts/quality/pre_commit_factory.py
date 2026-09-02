#!/usr/bin/env python3
"""Git pre-commit: jeden pisarz na drzewo + podpis agentlinta w tym samym commicie."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = {
    "AGENTS.md",
    "GROUNDING.md",
    ".cursor/rules/security-tenancy.mdc",
    ".cursor/rules/no-slop.mdc",
    ".cursor/rules/context.mdc",
}
BASELINE = "scripts/quality/agentlint.baseline.json"


def _run(args: list[str]) -> str:
    done = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout


def leftover_worktree() -> list[str]:
    """Cokolwiek niejest w indeksie: inny pisarz albo niedokończony plaster."""
    leftover: list[str] = []
    for line in _run(["git", "status", "--porcelain", "-uall"]).splitlines():
        if len(line) < 2:
            continue
        staged, unstaged = line[0], line[1]
        if line.startswith("??") or unstaged in "MD":
            leftover.append(line)
        elif staged in "MADRC" and unstaged in "MADRC" and unstaged != " ":
            leftover.append(line)
    return leftover


def staged_names() -> set[str]:
    names = _run(["git", "diff", "--cached", "--name-only", "-z"]).split("\0")
    return {n.replace("\\", "/") for n in names if n}


def main() -> int:
    leftover = leftover_worktree()
    if leftover:
        print(
            "pre-commit: drzewo ma pliki poza tym commitem. "
            "To zwykle drugi pisarz albo niedokończony plaster.",
            file=sys.stderr,
        )
        print("pre-commit: dociągnij je do tego commita albo poczekaj, aż pas 1 skończy.", file=sys.stderr)
        for row in leftover[:20]:
            print(f"  {row}", file=sys.stderr)
        return 1

    staged = staged_names()
    if staged & CONTRACT and BASELINE not in staged:
        print(
            "pre-commit: zmiana AGENTS.md / GROUNDING.md / alwaysApply rules "
            "wymaga scripts/quality/agentlint.baseline.json w TYM SAMYM commicie.",
            file=sys.stderr,
        )
        print(
            "pre-commit: python scripts/quality/agentlint.py --write && git add "
            + BASELINE,
            file=sys.stderr,
        )
        return 1

    if staged & CONTRACT or BASELINE in staged:
        check = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "quality" / "agentlint.py")],
            cwd=ROOT,
        )
        if check.returncode != 0:
            print("pre-commit: agentlint nie zgadza się z baseline.", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
