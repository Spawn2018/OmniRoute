#!/usr/bin/env python3
"""Podłoga jakości: liczby tylko rosną. Nie edytuje AGENTS ani GROUNDING."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = Path(__file__).resolve().parent / "quality_floor.json"
GROUNDING = ROOT / "GROUNDING.md"
CASES = ROOT / "docs" / "_bench" / "cases"
PROMPTFOO = ROOT / "backend" / "tests" / "extraction" / "test_promptfoo_fixtures.py"
HC = re.compile(r"^## HC-0([1-8])\b", re.MULTILINE)


def isolation_tests() -> int:
    tests = ROOT / "backend" / "tests"
    return len(list(tests.rglob("test_*isolation*.py")))


def bench_cases() -> int:
    if not CASES.is_dir():
        return 0
    return len([path for path in CASES.glob("*.md") if path.name != "TEMPLATE.md"])


def promptfoo_fixtures() -> int:
    if not PROMPTFOO.is_file():
        return 0
    return len(re.findall(r'"doc://promptfoo/', PROMPTFOO.read_text(encoding="utf-8")))


def grounding_hc() -> int:
    if not GROUNDING.is_file():
        return 0
    return len(HC.findall(GROUNDING.read_text(encoding="utf-8")))


def snapshot() -> dict[str, int]:
    return {
        "isolation_tests": isolation_tests(),
        "bench_cases": bench_cases(),
        "promptfoo_fixtures": promptfoo_fixtures(),
        "grounding_hc": grounding_hc(),
    }


def load_baseline() -> dict[str, int]:
    if not BASELINE.is_file():
        raise FileNotFoundError(f"brak {BASELINE.name} — python scripts/quality/quality_floor.py --write")
    payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    return {key: int(payload[key]) for key in snapshot()}


def regressions(current: dict[str, int], floor: dict[str, int]) -> list[str]:
    errors: list[str] = []
    for key, need in floor.items():
        got = current[key]
        if got < need:
            errors.append(f"{key}: {got} < podłoga {need}")
    return errors


def check() -> list[str]:
    return regressions(snapshot(), load_baseline())


def write_baseline() -> None:
    current = snapshot()
    if BASELINE.is_file():
        errors = regressions(current, load_baseline())
        if errors:
            raise ValueError("; ".join(errors))
    BASELINE.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        try:
            write_baseline()
        except ValueError as err:
            print(f"quality_floor: {err}")
            return 1
        print(f"wrote {BASELINE.relative_to(ROOT).as_posix()} {snapshot()}")
        return 0
    errors = check()
    if errors:
        print("quality_floor: jakość spadła")
        for err in errors:
            print(f"  {err}")
        return 1
    print("quality_floor: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
