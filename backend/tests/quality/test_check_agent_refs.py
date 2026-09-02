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


def test_persona_scan_skips_untracked_scratch() -> None:
    refs = _load_refs()
    scratch = _ROOT / "docs" / "ops" / "_scratch_testolog.md"
    scratch.write_text("kronikarz testolog weryfikator", encoding="utf-8")
    try:
        errors = refs.persona_errors()
        assert errors == []
        assert "_scratch_testolog.md" not in "\n".join(errors)
    finally:
        scratch.unlink(missing_ok=True)


def test_uri_scheme_is_not_reported_as_missing_file() -> None:
    refs = _load_refs()
    assert not any("://" in err for err in refs.stale_ref_errors())


def test_relative_link_resolves_against_its_own_file() -> None:
    refs = _load_refs()
    state = _ROOT / "docs" / "state"
    assert refs.exists("../deltas/archived/4.0-port.md", state)
    assert refs.exists("../adr/0003-frontend-ui-system-2026.md", state)


def test_relative_link_to_absent_file_is_still_reported() -> None:
    refs = _load_refs()
    state = _ROOT / "docs" / "state"
    assert not refs.exists("../deltas/archived/9.9-nie-ma.md", state)
