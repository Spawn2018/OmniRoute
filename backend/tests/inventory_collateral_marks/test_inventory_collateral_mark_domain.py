import pytest

from app.domain.errors import InvalidInventoryCollateralMark
from app.domain.inventory_collateral_mark import parse_inventory_collateral_mark_row


def test_parse_inventory_collateral_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_inventory_collateral_mark_row(
        "col_pledge_01",
        "Pledge",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("col_pledge_01", "pledge", "tenant:manual")


def test_parse_inventory_collateral_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidInventoryCollateralMark, match="rodzaj"):
        parse_inventory_collateral_mark_row(
            "col_pledge_01",
            "live_pledge",
            "tenant:manual",
        )
