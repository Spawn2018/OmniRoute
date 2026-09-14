import pytest

from app.domain.errors import InvalidL3GateMark
from app.domain.l3_gate_mark import parse_l3_gate_mark_row


def test_parse_l3_gate_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_l3_gate_mark_row(
        "l3_sot_01",
        "Sot",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("l3_sot_01", "sot", "tenant:manual")


def test_parse_l3_gate_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidL3GateMark, match="rodzaj"):
        parse_l3_gate_mark_row(
            "l3_sot_01",
            "l3_write",
            "tenant:manual",
        )
