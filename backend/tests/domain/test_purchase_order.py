import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPurchaseOrder
from app.domain.purchase_order import parse_purchase_order_row


def test_parse_purchase_order_row_accepts_manual_with_plant() -> None:
    code, plant, origin = parse_purchase_order_row(
        " po_gdansk_01 ",
        " Gdańsk ",
        " tenant:manual ",
    )
    assert (code, plant, origin) == ("po_gdansk_01", "Gdańsk", "tenant:manual")


def test_parse_purchase_order_row_accepts_missing_and_blank_plant() -> None:
    without = parse_purchase_order_row("po_no_plant", None, "fixture://purchase-order/a")
    assert without[1] is None
    blank = parse_purchase_order_row("po_blank_plant", "  ", "tenant:manual")
    assert blank[1] is None


def test_parse_purchase_order_row_rejects_bad_code() -> None:
    with pytest.raises(InvalidPurchaseOrder, match="oznaczenie"):
        parse_purchase_order_row("X", None, "tenant:manual")
    with pytest.raises(InvalidPurchaseOrder, match="oznaczenie"):
        parse_purchase_order_row(1, None, "tenant:manual")


def test_parse_purchase_order_row_rejects_long_plant() -> None:
    with pytest.raises(InvalidPurchaseOrder, match="zakład"):
        parse_purchase_order_row("po_gdansk_01", "x" * 129, "tenant:manual")
    with pytest.raises(InvalidPurchaseOrder, match="zakład"):
        parse_purchase_order_row("po_gdansk_01", 12, "tenant:manual")


@given(st.sampled_from(["", "   ", "https://vendor.example/po", "fixture://asn/1"]))
def test_parse_purchase_order_row_rejects_foreign_origin(raw: str) -> None:
    with pytest.raises(InvalidPurchaseOrder, match="obce"):
        parse_purchase_order_row("po_gdansk_01", None, raw)
