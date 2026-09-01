#!/usr/bin/env python3
"""Blokuje commit przy naruszeniu architektury, duplikacji, martwym kodzie."""
import json
import subprocess
import sys

checks = [
    (
        "OS status vs CURRENT.md",
        ["python", "scripts/quality/sync_os_status.py", "--check"],
    ),
    ("architektura", ["lint-imports"]),
    (
        "duplikacja",
        [
            "jscpd",
            "--threshold",
            "3",
            "--min-lines",
            "5",
            "--reporters",
            "console",
            "--silent",
            "backend/app",
            "frontend/src",
        ],
    ),
    ("martwy kod", ["vulture", "backend/app", "--min-confidence", "80"]),
]

failures = []
for name, cmd in checks:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        continue
    if r.returncode:
        failures.append(f"[{name}]\n{r.stdout or r.stderr}")

if failures:
    print(
        json.dumps(
            {
                "block": True,
                "followup_message": (
                    "Commit zablokowany:\n\n"
                    + "\n\n".join(failures)
                    + "\n\nDuplikacja: sprawdź, czy nie powielasz istniejącej funkcji. "
                    "Uruchom subagenta lowca-duplikatow."
                ),
            }
        )
    )
