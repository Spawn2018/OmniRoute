"""Bench obowiązkowy dla Ostatni plaster; RLS przy CREATE TABLE w przeglądzie."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "craft_close.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("craft_close", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parses_last_plaster_id_from_current_shape() -> None:
    close = _load()
    text = (
        "**Ostatni plaster:** **66.0** S3 treść `inbound_message`\n"
        "**Etap:** Plan\n"
    )
    assert close.last_plaster_id(text) == "66.0"


def test_create_table_without_force_rls_is_reported() -> None:
    close = _load()
    migration = _ROOT / "backend" / "alembic" / "versions" / "_craft_close_tmp.py"
    migration.write_text("def upgrade() -> None:\n    op.create_table('demo')\n", encoding="utf-8")
    rel = migration.relative_to(_ROOT).as_posix()
    try:
        errors = close.alembic_rls_errors(frozenset({rel}))
        assert any("FORCE ROW LEVEL SECURITY" in err for err in errors)
        assert any("izolacji" in err for err in errors)
    finally:
        migration.unlink(missing_ok=True)


def test_create_table_with_rls_and_isolation_file_is_silent() -> None:
    close = _load()
    errors = close.alembic_rls_errors(
        frozenset(
            {
                "backend/alembic/versions/026_inbound_message_rls.py",
                "backend/tests/inbound_messages/test_inbound_message_isolation.py",
            }
        )
    )
    assert errors == []


def test_live_current_has_a_bench_case() -> None:
    close = _load()
    plaster_id = close.last_plaster_id(
        (_ROOT / "docs" / "state" / "CURRENT.md").read_text(encoding="utf-8")
    )
    assert close.bench_case_paths(plaster_id)
