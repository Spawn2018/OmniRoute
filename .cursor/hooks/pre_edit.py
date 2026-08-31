#!/usr/bin/env python3
"""Weto na plikach, których agent nie ma zmieniać."""
import json
import re
import subprocess
import sys
from pathlib import Path

payload = json.load(sys.stdin)
path = str(payload["file_path"])

PROTECTED = [
    (r"frontend/src/api/", "katalog generowany — użyj `just api-types`"),
    (r"docs/deltas/archived/", "delta zarchiwizowana — utwórz nową"),
    (r"\.cursor/hooks/", "zmiana hooków wymaga decyzji człowieka"),
    (r"docs/adr/.*\.md", "ADR ze statusem przyjęta jest niezmienny"),
    (r"Informacje z claude/", "archiwum tylko do odczytu"),
]

for pattern, reason in PROTECTED:
    if re.search(pattern, path):
        print(json.dumps({"block": True, "followup_message": f"Odmowa: {reason}"}))
        sys.exit(0)

if "alembic/versions" in path:
    applied = subprocess.run(["alembic", "current"], capture_output=True, text=True)
    rev = Path(path).stem.split("_")[0]
    if rev and rev in applied.stdout:
        print(
            json.dumps(
                {
                    "block": True,
                    "followup_message": (
                        "Ta migracja jest już zastosowana. "
                        "Utwórz nową: `just migration <nazwa>`."
                    ),
                }
            )
        )
