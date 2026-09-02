#!/usr/bin/env python3
"""Taśma /zamknij: bench + orakulum RLS/izolacja. Nie rusza GROUNDING ani AGENTS."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "docs" / "state" / "CURRENT.md"
CASES = ROOT / "docs" / "_bench" / "cases"
KNOWLEDGE = ROOT / "docs" / "_knowledge" / "memory-patterns"
LAST_PLASTER = re.compile(
    r"^\*\*Ostatni plaster:\*\*\s+\*\*([0-9]+(?:\.[0-9]+)*)\*\*",
    re.MULTILINE,
)
CREATE_TABLE = re.compile(r"op\.create_table\s*\(", re.IGNORECASE)


def last_plaster_id(current_text: str) -> str:
    match = LAST_PLASTER.search(current_text)
    if match is None:
        raise ValueError("CURRENT.md bez pola Ostatni plaster z numerem")
    return match.group(1)


def _git_names(args: list[str]) -> set[str]:
    done = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        return set()
    return {line.replace("\\", "/") for line in done.stdout.splitlines() if line}


def review_paths() -> frozenset[str]:
    names: set[str] = set()
    names |= _git_names(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"])
    names |= _git_names(["git", "diff", "--name-only"])
    names |= _git_names(["git", "diff", "--cached", "--name-only"])
    return frozenset(names)


def bench_case_paths(plaster_id: str) -> list[Path]:
    if not CASES.is_dir():
        return []
    return sorted(CASES.glob(f"{plaster_id}-*.md"))


def alembic_rls_errors(paths: frozenset[str]) -> list[str]:
    errors: list[str] = []
    isolation_in_review = any(
        name.endswith(".py") and "isolation" in Path(name).name for name in paths
    )
    for rel in sorted(paths):
        if not rel.startswith("backend/alembic/versions/") or not rel.endswith(".py"):
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        if CREATE_TABLE.search(source) is None:
            continue
        if "FORCE ROW LEVEL SECURITY" not in source:
            errors.append(f"{rel}: CREATE TABLE bez FORCE ROW LEVEL SECURITY")
        if not isolation_in_review:
            errors.append(
                f"{rel}: nowa tabela w przeglądzie bez pliku testu izolacji w tym samym commicie"
            )
    return errors


def bench_missing_error(plaster_id: str) -> list[str]:
    if bench_case_paths(plaster_id):
        return []
    return [
        f"brak docs/_bench/cases/{plaster_id}-*.md — "
        "python scripts/quality/craft_close.py --write"
    ]


def check_errors() -> list[str]:
    plaster_id = last_plaster_id(CURRENT.read_text(encoding="utf-8"))
    return bench_missing_error(plaster_id) + alembic_rls_errors(review_paths())


def _slug(plaster_id: str) -> str:
    return f"{plaster_id}-closed"


def write_bench_case(plaster_id: str) -> Path:
    CASES.mkdir(parents=True, exist_ok=True)
    existing = bench_case_paths(plaster_id)
    if existing:
        return existing[0]
    path = CASES / f"{_slug(plaster_id)}.md"
    files = "\n".join(f"- `{name}`" for name in sorted(review_paths())[:40]) or "- (brak diffu)"
    path.write_text(
        f"""# BENCH-{plaster_id}

**Źródło:** plaster `{plaster_id}`
**Typ:** zamknięcie taśmy

## Zadanie

Zadanie z `docs/state/CURRENT.md` w chwili zamknięcia `{plaster_id}`.

## Kontekst wejściowy

- `docs/state/CURRENT.md`
- jedna spec z CURRENT

## Wynik referencyjny

**Pliki w przeglądzie:**

{files}

## Metryki referencyjne

| Metryka | Wartość |
|---|---|
| test izolacji przy nowej tabeli | patrz `craft_close.py --check` |
| FORCE ROW LEVEL SECURITY | patrz `craft_close.py --check` |

## Pułapka tego przypadku

Uzupełnij przy następnym podobnym plasterze — jedna linia, co agent tu psuje.
""",
        encoding="utf-8",
    )
    return path


def write_rls_machine_card() -> Path:
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    path = KNOWLEDGE / "machine-nowa-tabela-rls-izolacja.md"
    if path.is_file():
        return path
    path.write_text(
        """# Machine — nowa tabela: RLS i izolacja

**Status:** machine. Orakulum: `python scripts/quality/craft_close.py --check`.
Nie jest zasadą w AGENTS.md. Nie edytuje GROUNDING.md.

## Sygnał

Migracja w `backend/alembic/versions/` z `op.create_table` w tym samym
commicie co plaster, bez `FORCE ROW LEVEL SECURITY` albo bez pliku
`test_*isolation*`.

## Zamiast

1. `organization_id` na tabeli.
2. `ALTER TABLE … FORCE ROW LEVEL SECURITY`.
3. Test izolacji w `backend/tests/<bc>/` — wzorzec
   `backend/tests/inbound_messages/test_inbound_message_isolation.py`.
4. Kontrakt serwisu: `assert "FORCE ROW LEVEL SECURITY" in source`.

## Zakaz

- Tabela biznesowa bez RLS „na później”.
- Izolacja tylko w komentarzu.
- Dopisywanie HC do AGENTS zamiast testu.
""",
        encoding="utf-8",
    )
    return path


def write_all() -> list[Path]:
    plaster_id = last_plaster_id(CURRENT.read_text(encoding="utf-8"))
    return [write_bench_case(plaster_id), write_rls_machine_card()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        for path in write_all():
            print(f"craft_close: {path.relative_to(ROOT).as_posix()}")
        return 0
    errors = check_errors()
    if errors:
        print("craft_close:")
        for err in errors:
            print(f"  {err}")
        return 1
    print("craft_close: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
