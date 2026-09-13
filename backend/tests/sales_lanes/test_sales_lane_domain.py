import pytest

from app.domain.errors import InvalidSalesLane
from app.domain.sales_lane import parse_sales_lane_row


def test_parse_sales_lane_row_accepts_manual() -> None:
    code, kind, origin = parse_sales_lane_row(
        "sln_repeat_01",
        "Repeat",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("sln_repeat_01", "repeat", "tenant:manual")


def test_parse_sales_lane_row_rejects_pipeline_kind() -> None:
    with pytest.raises(InvalidSalesLane, match="rodzaj"):
        parse_sales_lane_row("sln_repeat_01", "pipeline", "tenant:manual")
