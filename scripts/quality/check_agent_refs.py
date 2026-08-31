#!/usr/bin/env python3
"""Sprawdza, czy ścieżki w AGENTS/GROUNDING/skills/rules istnieją w repo."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCAN = [
    ROOT / "AGENTS.md",
    ROOT / "GROUNDING.md",
    ROOT / ".cursor" / "rules",
    ROOT / ".cursor" / "skills",
    ROOT / ".cursor" / "commands",
    ROOT / "docs" / "state" / "CURRENT.md",
]

BACKTICK = re.compile(r"`([^`\n]+)`")
MD_LINK = re.compile(r"\]\(([^)]+)\)")


def collect_paths(text: str) -> set[str]:
    found: set[str] = set()
    for m in BACKTICK.finditer(text):
        token = m.group(1).strip()
        if "/" in token or token.endswith((".md", ".mdc", ".py", ".ts", ".tsx")):
            found.add(token.split("#")[0])
    for m in MD_LINK.finditer(text):
        target = m.group(1).strip()
        if not target.startswith(("http", "mailto")):
            found.add(target.split("#")[0])
    return found


def exists(rel: str) -> bool:
    if rel.startswith(("http://", "https://", "mailto:")):
        return True
    if any(ch in rel for ch in (" ", "(", ")", "except", "→")):
        return True
    if "*" in rel or "<" in rel or ">" in rel:
        return True
    # repo/org paths (GitHub references, not local paths)
    if "/" in rel and not rel.startswith(("docs/", "backend/", "frontend/", ".cursor/", "scripts/", "tests/")):
        if rel.count("/") == 1 and not rel.endswith((".md", ".mdc", ".py", ".ts", ".tsx", ".json")):
            return True

    candidates = [rel]
    bare = Path(rel).name
    candidates.extend(
        [
            f"docs/state/{bare}",
            f"docs/{bare}",
            f"docs/spec/{bare}",
            f"backend/app/{rel}",
        ]
    )
    for c in candidates:
        if (ROOT / c).exists():
            return True

    optional_prefixes = (
        "backend/",
        "frontend/",
        "tests/patterns/",
        "docs/spec/",
        "domains/_template/",
    )
    if any(rel.startswith(p) for p in optional_prefixes):
        return True
    if rel.endswith(".py") and ("/" not in rel or "app/" in rel):
        return True
    return False


def main() -> int:
    errors: list[str] = []
    for src in SCAN:
        if src.is_dir():
            files = list(src.rglob("*"))
        else:
            files = [src] if src.exists() else []
        for f in files:
            if f.suffix not in {".md", ".mdc"}:
                continue
            text = f.read_text(encoding="utf-8")
            for rel in collect_paths(text):
                rel = rel.replace("\\", "/")
                if rel.startswith("/") or rel.startswith("Informacje"):
                    continue
                if not exists(rel):
                    errors.append(f"{f.relative_to(ROOT)}: brak `{rel}`")

    if errors:
        print("Context rot / stale refs:\n")
        for e in sorted(set(errors))[:50]:
            print(" ", e)
        if len(errors) > 50:
            print(f"  ... i {len(errors) - 50} więcej")
        return 1

    print("check_agent_refs: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
