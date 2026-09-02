#!/usr/bin/env python3
"""OS-3: test z kodem, how-to albo leftover, delta zanim produkt. Nie rusza HC."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPEN = ROOT / "docs" / "deltas" / "open"
PRODUCT_PREFIXES = (
    "backend/app/",
    "backend/alembic/",
    "frontend/src/features/",
    "frontend/src/routes/",
)


def is_new_service_or_api(rel: str) -> bool:
    if not rel.endswith(".py") or rel.endswith("__init__.py"):
        return False
    return rel.startswith("backend/app/services/") or rel.startswith("backend/app/api/")


def is_product_path(rel: str) -> bool:
    return any(rel.startswith(prefix) for prefix in PRODUCT_PREFIXES)


def is_test_path(rel: str) -> bool:
    return rel.startswith("backend/tests/") and rel.endswith(".py")


def is_write_surface(rel: str, source: str) -> bool:
    if rel.endswith("catalog-page.tsx") and rel.startswith("frontend/src/features/"):
        return True
    if rel.startswith("backend/app/api/") and rel.endswith(".py"):
        return "@router.post" in source or "router.post(" in source
    return False


def product_open_deltas(open_dir: Path) -> list[Path]:
    if not open_dir.is_dir():
        return []
    return [
        path
        for path in sorted(open_dir.glob("*.md"))
        if not path.name.upper().startswith("OS-")
    ]


def missing_tests(added: frozenset[str], changed: frozenset[str]) -> list[str]:
    new_code = sorted(rel for rel in added if is_new_service_or_api(rel))
    if not new_code:
        return []
    if any(is_test_path(rel) for rel in changed):
        return []
    return [f"{rel}: nowy serwis/API bez zmiany w backend/tests/" for rel in new_code]


def missing_operator_docs(
    added: frozenset[str],
    changed: frozenset[str],
    sources: dict[str, str],
) -> list[str]:
    writes = [
        rel
        for rel in sorted(added)
        if is_write_surface(rel, sources.get(rel, ""))
    ]
    if not writes:
        return []
    has_howto = any(rel.startswith("docs/operator/") for rel in changed)
    has_debt = "docs/ops/docs-debt.md" in changed
    if has_howto or has_debt:
        return []
    listed = ", ".join(writes)
    return [
        f"{listed}: job zapisu bez docs/operator/ i bez linii leftover w docs-debt.md"
    ]


def missing_product_delta(
    changed: frozenset[str],
    open_product: list[Path],
    archived_added: frozenset[str],
) -> list[str]:
    if not any(is_product_path(rel) for rel in changed):
        return []
    if open_product:
        return []
    archived = any(
        rel.startswith("docs/deltas/archived/") and rel.endswith(".md")
        for rel in archived_added
    )
    if archived:
        return []
    return [
        "kod produktu bez delty w docs/deltas/open/ (nie OS-*) "
        "ani archiwum w tym commicie — najpierw /plan-modul"
    ]


def read_if_exists(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")
