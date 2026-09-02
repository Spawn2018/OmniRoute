"""C2: cytat `just` / MCP / scripts w kontrakcie musi istnieć w repo."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "contract_drift.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("contract_drift", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_missing_just_recipe_is_reported() -> None:
    drift = _load()
    recipes = drift.just_recipes("gate:\n    @echo ok\n")
    errors = drift.drift_in_text(
        "AGENTS.md",
        "Odpal `just signals` po puszcie.",
        recipes,
        frozenset({"github"}),
    )
    assert any("just signals" in err for err in errors)


def test_parameterized_recipe_does_not_swallow_later_names() -> None:
    drift = _load()
    recipes = drift.just_recipes(
        "migration name:\n    echo x\n\ndocs:\n    echo y\n"
    )
    assert recipes == frozenset({"migration", "docs"})


def test_existing_just_recipe_is_silent() -> None:
    drift = _load()
    recipes = drift.just_recipes("gate:\n    @echo ok\n")
    errors = drift.drift_in_text(
        "AGENTS.md",
        "Odpal `just gate` po puszcie.",
        recipes,
        frozenset({"github"}),
    )
    assert errors == []


def test_mcp_postgres_without_server_is_reported() -> None:
    drift = _load()
    errors = drift.drift_in_text(
        "AGENTS.md",
        "Schemat sprawdzasz przez MCP Postgres.",
        frozenset({"gate"}),
        frozenset({"github"}),
    )
    assert any("Postgres" in err for err in errors)


def test_github_mcp_server_is_silent() -> None:
    drift = _load()
    errors = drift.drift_in_text(
        "AGENTS.md",
        "Jedyny serwer: MCP GitHub.",
        frozenset({"gate"}),
        frozenset({"github"}),
    )
    assert errors == []


def test_missing_script_backtick_is_reported() -> None:
    drift = _load()
    errors = drift.drift_in_text(
        ".cursor/commands/zamknij.md",
        "Odpal `scripts/quality/nie-ma-tego.py`.",
        frozenset({"gate"}),
        frozenset({"github"}),
    )
    assert any("nie-ma-tego.py" in err for err in errors)


def test_live_contract_has_no_drift() -> None:
    drift = _load()
    assert drift.contract_drift_errors() == []
