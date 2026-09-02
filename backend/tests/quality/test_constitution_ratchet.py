"""Ratchet konstytucji: HC nie znikają, AGENTS nie puchnie, jakość tylko w górę."""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_GROUNDING = _ROOT / "GROUNDING.md"
_AGENTS = _ROOT / "AGENTS.md"


def test_grounding_keeps_hc_01_through_hc_08() -> None:
    text = _GROUNDING.read_text(encoding="utf-8")
    for index in range(1, 9):
        assert f"HC-0{index}" in text


def test_grounding_keeps_money_hitl_and_no_llm_math() -> None:
    text = _GROUNDING.read_text(encoding="utf-8")
    assert "Decimal" in text
    assert "nie liczy" in text
    assert "akceptacji człowieka" in text
    assert "organization_id" in text
    assert "FORCE ROW LEVEL SECURITY" in text


def test_agents_stays_within_line_budget() -> None:
    lines = _AGENTS.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 130


def test_agents_keeps_tenancy_charge_and_hitl() -> None:
    text = _AGENTS.read_text(encoding="utf-8")
    assert "organization_id" in text
    assert "`charge`" in text
    assert "akceptacji człowieka" in text
    assert "Decimal" in text
