import pytest

from app.domain.errors import InvalidPoFinancingMark
from app.domain.po_financing_mark import parse_po_financing_mark_row


def test_parse_po_financing_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_po_financing_mark_row(
        "po_trade_01",
        "Release",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("po_trade_01", "release", "tenant:manual")


def test_parse_po_financing_mark_row_rejects_live_http_kind() -> None:
    with pytest.raises(InvalidPoFinancingMark, match="rodzaj"):
        parse_po_financing_mark_row("po_trade_01", "live_http", "tenant:manual")
