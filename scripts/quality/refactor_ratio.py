#!/usr/bin/env python3
"""Stosunek kodu przeniesionego do dodanego. Próg alarmowy: 10%."""
import argparse
import subprocess
import sys


def analyze(weeks: int) -> dict:
    log = subprocess.run(
        ["git", "log", f"--since={weeks}.weeks", "--numstat", "--format=%H|%an"],
        capture_output=True,
        text=True,
        cwd=".",
    ).stdout

    added = deleted = 0
    for line in log.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit():
            added += int(parts[0])
            deleted += int(parts[1])

    moves = subprocess.run(
        [
            "git",
            "log",
            f"--since={weeks}.weeks",
            "-M",
            "--diff-filter=R",
            "--numstat",
            "--format=",
        ],
        capture_output=True,
        text=True,
        cwd=".",
    ).stdout
    moved = sum(
        int(p.split("\t")[0])
        for p in moves.splitlines()
        if p.split("\t")[0].isdigit()
    )

    total = added + moved
    ratio = (moved / total * 100) if total else 0.0
    return {"added": added, "deleted": deleted, "moved": moved, "ratio": ratio}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--weeks", type=int, default=4)
    p.add_argument("--fail-under", type=float, default=10.0)
    args = p.parse_args()

    try:
        r = analyze(args.weeks)
    except FileNotFoundError:
        print("refactor_ratio: git niedostępny — pominięto")
        sys.exit(0)

    print(f"Ostatnie {args.weeks} tyg.")
    print(f"  dodane:       {r['added']:>8}")
    print(f"  przeniesione: {r['moved']:>8}")
    print(f"  stosunek:     {r['ratio']:>7.1f}%   (próg {args.fail_under}%)")
    if r["ratio"] < args.fail_under and r["added"] > 100:
        print("\nKod przestał być refaktoryzowany. Uruchom /refaktor")
        sys.exit(1)
