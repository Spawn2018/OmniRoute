"""Regresja: żywy OS nie woła person z archiwum poza tabelą ADR."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "check_agent_refs.py"


def _load_refs() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_agent_refs", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_archive_persona_word_outside_canon_table_is_reported() -> None:
    refs = _load_refs()
    hits = refs.archive_persona_names("Fail-first: testolog pisze testy.")
    assert "testolog" in hits


def test_archive_persona_inside_canon_table_is_ignored() -> None:
    refs = _load_refs()
    text = (
        "<!-- os-canon-table:start -->\n"
        "| testolog | `/testy` |\n"
        "<!-- os-canon-table:end -->\n"
        "Kanon: `/testy`.\n"
    )
    assert refs.archive_persona_names(text) == frozenset()


def test_command_slash_testy_is_not_an_archive_persona() -> None:
    refs = _load_refs()
    assert refs.archive_persona_names("Następna tura: `/testy`.") == frozenset()


def test_live_os_tree_has_no_archive_persona_names() -> None:
    refs = _load_refs()
    assert refs.persona_errors() == []
