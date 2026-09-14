import pytest

from app.domain.errors import InvalidRfidMark
from app.domain.rfid_mark import parse_rfid_mark_row


def test_parse_rfid_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_rfid_mark_row(
        "rfid_gate_01",
        "Gate",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("rfid_gate_01", "gate", "tenant:manual")


def test_parse_rfid_mark_row_rejects_live_rfid_kind() -> None:
    with pytest.raises(InvalidRfidMark, match="rodzaj"):
        parse_rfid_mark_row("rfid_gate_01", "live_rfid", "tenant:manual")
