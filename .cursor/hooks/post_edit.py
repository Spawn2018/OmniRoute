#!/usr/bin/env python3
"""Uruchamiany po każdej edycji agenta. Zwraca błędy przez followup_message."""
import json
import subprocess
import sys
from pathlib import Path

payload = json.load(sys.stdin)
path = Path(payload["file_path"])
problems: list[str] = []

RUFF = "E,F,B,BLE,C901,ARG,PLW0621,SLF001,F841"

if path.suffix == ".py":
    subprocess.run(["ruff", "format", str(path)], check=False)
    r = subprocess.run(
        ["ruff", "check", "--select", RUFF, str(path)],
        capture_output=True,
        text=True,
    )
    if r.returncode:
        problems.append("ruff:\n" + r.stdout)
    m = subprocess.run(
        ["mypy", "--follow-imports=skip", str(path)],
        capture_output=True,
        text=True,
    )
    if m.returncode:
        problems.append("mypy:\n" + m.stdout)

elif path.suffix in {".ts", ".tsx"}:
    frontend = Path("frontend")
    if frontend.is_dir():
        subprocess.run(
            ["pnpm", "prettier", "--write", str(path)],
            cwd="frontend",
            check=False,
        )
        t = subprocess.run(
            ["pnpm", "tsc", "--noEmit"],
            cwd="frontend",
            capture_output=True,
            text=True,
        )
        if t.returncode:
            problems.append("tsc:\n" + t.stdout[-3000:])

if problems:
    print(
        json.dumps(
            {
                "followup_message": (
                    "Popraw poniższe zanim przejdziesz dalej. "
                    "Nie wyłączaj reguł, nie dodawaj noqa.\n\n" + "\n\n".join(problems)
                )
            }
        )
    )
