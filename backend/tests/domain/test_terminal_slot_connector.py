from datetime import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTerminalSlotConnector
from app.domain.terminal_slot_connector import (
    require_connector_code,
    require_cutoff_clock,
    require_gate_clock,
    require_slot_mode,
    require_slot_source_ref,
    require_terminal_code,
)


def test_connector_code_accepts_snake() -> None:
    assert require_connector_code("gdynia_bct") == "gdynia_bct"


def test_connector_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidTerminalSlotConnector, match="oznaczenie"):
        require_connector_code("X")
    with pytest.raises(InvalidTerminalSlotConnector, match="oznaczenie"):
        require_connector_code(1)


def test_terminal_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidTerminalSlotConnector, match="terminal"):
        require_terminal_code("BCT")
    with pytest.raises(InvalidTerminalSlotConnector, match="terminal"):
        require_terminal_code(None)


@given(st.sampled_from(["api", "email_hitl", "portal_task", "unsupported", " API "]))
def test_slot_mode_allowlist(raw: str) -> None:
    assert require_slot_mode(raw) == raw.strip().lower()


@given(st.sampled_from(["", "navis", "selenium", "live", "confirmed"]))
def test_slot_mode_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTerminalSlotConnector, match="tryb"):
        require_slot_mode(raw)


def test_gate_clock_parses_hhmm() -> None:
    assert require_gate_clock("06:00") == time(6, 0)
    assert require_gate_clock(time(22, 30, 15)) == time(22, 30, 15)


def test_gate_clock_rejects_unreadable() -> None:
    with pytest.raises(InvalidTerminalSlotConnector, match="godziny"):
        require_gate_clock("25:00")
    with pytest.raises(InvalidTerminalSlotConnector, match="godziny"):
        require_gate_clock(6.5)


def test_cutoff_clock_rejects_unreadable() -> None:
    with pytest.raises(InvalidTerminalSlotConnector, match="odcięcie"):
        require_cutoff_clock("night")
    with pytest.raises(InvalidTerminalSlotConnector, match="odcięcie"):
        require_cutoff_clock(True)


def test_slot_source_ref_accepts_manual_and_fixture() -> None:
    assert require_slot_source_ref("tenant:manual") == "tenant:manual"
    assert require_slot_source_ref(" fixture://terminal-slot-connector/1 ") == (
        "fixture://terminal-slot-connector/1"
    )


@given(st.sampled_from(["", "   ", "http://n4.example/x", "fixture://dock/1"]))
def test_slot_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTerminalSlotConnector, match="obce"):
        require_slot_source_ref(raw)
