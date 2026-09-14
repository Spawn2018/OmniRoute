import pytest

from app.domain.errors import InvalidInventoryFinanceMark
from app.domain.inventory_finance_mark import parse_inventory_finance_mark_row


def test_parse_inventory_finance_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_inventory_finance_mark_row(
        "inv_release_01",
        "Release",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("inv_release_01", "release", "tenant:manual")


def test_parse_inventory_finance_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidInventoryFinanceMark, match="rodzaj"):
        parse_inventory_finance_mark_row(
            "inv_release_01",
            "live_valuation",
            "tenant:manual",
        )
