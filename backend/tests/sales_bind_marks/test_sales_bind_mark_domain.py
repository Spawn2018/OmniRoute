import pytest

from app.domain.errors import InvalidSalesBindMark
from app.domain.sales_bind_mark import parse_sales_bind_mark_row


def test_parse_sales_bind_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_sales_bind_mark_row(
        "sales_bind_opp_01",
        "Opportunity",
        "tenant:manual",
    )
    assert code == "sales_bind_opp_01"
    assert kind == "opportunity"
    assert origin == "tenant:manual"


def test_parse_sales_bind_mark_row_rejects_hubspot_kind() -> None:
    with pytest.raises(InvalidSalesBindMark, match="bind_kind"):
        parse_sales_bind_mark_row("sales_bind_opp_01", "hubspot", "tenant:manual")
