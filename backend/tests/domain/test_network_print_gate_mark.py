import pytest

from app.domain.errors import InvalidNetworkPrintGateMark
from app.domain.network_print_gate_mark import parse_network_print_gate_mark_row


def test_parse_network_print_gate_mark_row_accepts_block() -> None:
    code, kind, origin = parse_network_print_gate_mark_row(
        "gate_block_01",
        "block_409",
        "fixture://network-print-gate/a",
    )
    assert code == "gate_block_01"
    assert kind == "block_409"
    assert origin == "fixture://network-print-gate/a"


def test_parse_network_print_gate_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidNetworkPrintGateMark, match="gate"):
        parse_network_print_gate_mark_row(
            "gate_block_01",
            "live",
            "tenant:manual",
        )


def test_parse_network_print_gate_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidNetworkPrintGateMark, match="obce"):
        parse_network_print_gate_mark_row(
            "gate_block_01",
            "warn_only",
            "http://evil",
        )
