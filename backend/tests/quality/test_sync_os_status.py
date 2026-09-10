"""CURRENT.md steruje README — regresja rozjazdu „następny = Charge 0.25”."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "sync_os_status.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("sync_os_status", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_current_and_plan_command() -> None:
    sync = _load()
    status = sync.parse_current(
        "**Ostatni plaster:** **3.0** M-03 `organization_setting`\n"
        "**Etap:** **Plan** (zero kodu). Nie `/plaster`.\n"
        "**Następny:** **Q1** archiwum M-05 Geografia\n"
    )
    assert status.command == "/plan-modul"
    assert "Q1" in status.next_step


def test_plaster_command_when_etap_is_agent() -> None:
    sync = _load()
    status = sync.parse_current(
        "**Ostatni plaster:** **1.2** M-08 `charge`\n"
        "**Etap:** plaster\n"
        "**Następny:** 1.3 accept HITL\n"
    )
    assert status.command == "/plaster"


def test_refaktor_command_when_etap_is_refaktor() -> None:
    sync = _load()
    status = sync.parse_current(
        "**Ostatni plaster:** **59.0** kanon jakości\n"
        "**Etap:** Refaktor\n"
        "**Następny:** Q-E1 katalogi do 4,4\n"
    )
    assert status.command == "/refaktor"


def test_missing_field_raises() -> None:
    sync = _load()
    try:
        sync.parse_current("**Ostatni plaster:** 3.0\n")
    except ValueError as exc:
        assert "Etap" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_replace_marked_swaps_inner() -> None:
    sync = _load()
    text = "a\n<!-- os-status:start -->\nold\n<!-- os-status:end -->\nb\n"
    out = sync.replace_marked(text, sync.STATUS_START, sync.STATUS_END, "new", "t")
    assert "old" not in out
    assert "new" in out


def test_agents_kanon_rejects_program_as_sot() -> None:
    sync = _load()
    assert not sync.agents_kanon_ok("| Program 12m (SoT) | `docs/state/PROGRAM-12M.md` |")
    assert sync.agents_kanon_ok("| Plan realizacji (jedyny) | `docs/PLAN-REALIZACJA.md` |")


def test_plan_status_is_next_not_blocked() -> None:
    sync = _load()
    status = sync.OsStatus("235.0", "Plan", "236.0 leftover T3")
    rendered = sync.render_plan_status(status)
    assert rendered.startswith("**Następny:**")
    assert "zablokowany" not in rendered


def test_current_does_not_tell_noc_to_skip_leftovers() -> None:
    text = (_ROOT / "docs" / "state" / "CURRENT.md").read_text(encoding="utf-8")
    assert "`/noc` pomija" not in text
    assert "Named parks parked" not in text


def test_plan_os_status_label_is_next() -> None:
    plan = (_ROOT / "docs" / "PLAN-REALIZACJA.md").read_text(encoding="utf-8")
    start = plan.index("<!-- os-status:start -->")
    end = plan.index("<!-- os-status:end -->")
    block = plan[start:end]
    assert "**Następny (zablokowany):**" not in block
    assert "**Następny:**" in block
