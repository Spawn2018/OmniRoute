#!/usr/bin/env python3
"""Ścieżki w OS + zakaz imion person z archiwum w żywych plikach."""
from __future__ import annotations

import re
import subprocess
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
PERSONA_SCAN = [
    ROOT / ".cursor" / "commands",
    ROOT / ".cursor" / "skills",
    ROOT / ".cursor" / "rules",
    ROOT / ".cursor" / "plans" / "omniroute-realizacja.plan.md",
    ROOT / "docs" / "adr",
    ROOT / "docs" / "ops",
]

BACKTICK = re.compile(r"`([^`\n]+)`")
MD_LINK = re.compile(r"\]\(([^)]+)\)")
CANON_TABLE = re.compile(
    r"<!-- os-canon-table:start -->.*?<!-- os-canon-table:end -->",
    re.DOTALL,
)
PERSONA_WORD = re.compile(r"\b(?:audytor-wydajnosci|kronikarz|testolog|weryfikator)\b")


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


def _unverifiable_token(rel: str) -> bool:
    """Adres, fragment prozy albo wzorzec z placeholderem — nie ścieżka w repo."""
    if rel.startswith(("http://", "https://", "mailto:")):
        return True
    if any(ch in rel for ch in (" ", "(", ")", "except", "→")):
        return True
    if "*" in rel or "<" in rel or ">" in rel:
        return True
    if "/" in rel and not rel.startswith(
        ("docs/", "backend/", "frontend/", ".cursor/", "scripts/", "tests/")
    ):
        return rel.count("/") == 1 and not rel.endswith(
            (".md", ".mdc", ".py", ".ts", ".tsx", ".json")
        )
    return False


def exists(rel: str, base: Path) -> bool:
    if _unverifiable_token(rel):
        return True

    # Link w Markdownie jest względny wobec własnego pliku, nie wobec ROOT —
    # bez tego poprawne `../deltas/...` z docs/state/CURRENT.md wygląda na martwy ref.
    linked = (base / rel).resolve()
    if linked.is_relative_to(ROOT) and linked.exists():
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


def strip_canon_table(text: str) -> str:
    return CANON_TABLE.sub("", text)


def archive_persona_names(text: str) -> frozenset[str]:
    return frozenset(PERSONA_WORD.findall(strip_canon_table(text)))


def iter_md(src: Path) -> list[Path]:
    if not src.exists():
        return []
    if src.is_file():
        return [src] if src.suffix in {".md", ".mdc"} else []
    return [path for path in src.rglob("*") if path.suffix in {".md", ".mdc"}]


def stale_ref_errors() -> list[str]:
    errors: list[str] = []
    for src in SCAN:
        for path in iter_md(src):
            for rel in collect_paths(path.read_text(encoding="utf-8")):
                rel = rel.replace("\\", "/")
                if rel.startswith("/") or rel.startswith("Informacje"):
                    continue
                if "://" in rel:
                    continue
                if not exists(rel, path.parent):
                    errors.append(f"{path.relative_to(ROOT)}: brak `{rel}`")
    return errors


def tracked_relative_paths() -> frozenset[str]:
    # Żywy OS = pliki w git. Lokalna notatka w docs/ops nie blokuje bramki.
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return frozenset(
        Path(part).as_posix()
        for part in completed.stdout.decode("utf-8").split("\0")
        if part
    )


def persona_errors() -> list[str]:
    tracked = tracked_relative_paths()
    errors: list[str] = []
    for src in PERSONA_SCAN:
        for path in iter_md(src):
            rel = path.relative_to(ROOT).as_posix()
            if rel not in tracked:
                continue
            names = archive_persona_names(path.read_text(encoding="utf-8"))
            if names:
                listed = ", ".join(sorted(names))
                errors.append(f"{rel}: nazwa archiwalna ({listed})")
    return errors


def _print_capped(errors: list[str]) -> None:
    unique = sorted(set(errors))
    for err in unique[:50]:
        print(" ", err)
    extra = len(unique) - 50
    if extra > 0:
        print(f"  ... i {extra} więcej")


def main() -> int:
    stale = stale_ref_errors()
    personae = persona_errors()
    if stale:
        print("Context rot / stale refs:\n")
        _print_capped(stale)
    if personae:
        print("Archive SH role names in live OS files:\n")
        _print_capped(personae)
    if stale or personae:
        return 1
    print("check_agent_refs: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
