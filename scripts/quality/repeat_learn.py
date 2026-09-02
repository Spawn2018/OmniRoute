#!/usr/bin/env python3
"""Powtórzone czerwone CI → karta machine. Nie rusza AGENTS/GROUNDING."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "docs" / "_knowledge" / "memory-patterns"
THRESHOLD = 3
RUN_LIMIT = 40


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "run"


def load_failed_runs(payload: list[dict[str, object]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in payload:
        if row.get("conclusion") != "failure":
            continue
        name = str(row.get("name") or "gate")
        counter[name] += 1
    return counter


def repeats(counter: Counter[str], threshold: int = THRESHOLD) -> list[tuple[str, int]]:
    return sorted(
        ((name, count) for name, count in counter.items() if count >= threshold),
        key=lambda pair: (-pair[1], pair[0]),
    )


def fetch_runs() -> list[dict[str, object]]:
    done = subprocess.run(
        [
            "gh",
            "run",
            "list",
            "--branch",
            "main",
            "--limit",
            str(RUN_LIMIT),
            "--json",
            "conclusion,name,displayTitle,url",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if done.returncode != 0 or not done.stdout.strip():
        return []
    parsed = json.loads(done.stdout)
    if not isinstance(parsed, list):
        return []
    return parsed


def card_path(job: str) -> Path:
    return KNOWLEDGE / f"machine-repeat-{_slug(job)}.md"


def write_repeat_card(job: str, count: int) -> Path:
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    path = card_path(job)
    if path.is_file():
        return path
    path.write_text(
        f"""# Machine — powtórzony fail CI `{job}`

**Status:** machine. Orakulum: `gh run list` co najmniej {THRESHOLD} czerwonych na `main`.
Nie edytuje AGENTS.md ani GROUNDING.md.

## Sygnał

Job/workflow `{job}` padł {count} razy w ostatnich {RUN_LIMIT} runach.

## Zamiast

1. Czytaj komentarz `report-failure` na commicie (code-gate vs meta).
2. Napraw kod albo cytat kontraktu. C2 = higiena, nie nowe zasady.
3. `just meta-gate` przed pushem. `python scripts/quality/agentlint.py --write`
   tylko gdy ruszasz AGENTS/GROUNDING/rules, w **tym samym** commicie.

## Zakaz

- `--no-verify`
- Auto-AGENTS (dopisywanie zasad, żeby gate przeszedł)
- Żywy OpenAI w gate
""",
        encoding="utf-8",
    )
    return path


def learn(write: bool) -> list[str]:
    lines: list[str] = []
    counter = load_failed_runs(fetch_runs())
    found = repeats(counter)
    if not found:
        lines.append("repeat_learn: brak wzorca 3+ czerwonych na main")
        return lines
    for job, count in found:
        if write:
            path = write_repeat_card(job, count)
            rel = path.relative_to(ROOT).as_posix()
            lines.append(f"repeat_learn: {count}x {job} -> {rel}")
        else:
            lines.append(f"repeat_learn: {count}x {job} (karta przy /zamknij)")
    return lines


def main() -> int:
    import argparse
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    for line in learn(write=args.write):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
