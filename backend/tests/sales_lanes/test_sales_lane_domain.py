import pytest

from app.domain.errors import InvalidSalesLane
from app.domain.sales_lane import parse_sales_lane_row


def test_parse_sales_lane_row_accepts_manual() -> None:
    code, kind, origin, frm, to = parse_sales_lane_row(
        "sln_repeat_01",
        "Repeat",
        "tenant:manual",
        "plgdn",
        "deham",
    )
    assert (code, kind, origin, frm, to) == (
        "sln_repeat_01",
        "repeat",
        "tenant:manual",
        "PLGDN",
        "DEHAM",
    )


def test_parse_sales_lane_row_rejects_pipeline_kind() -> None:
    with pytest.raises(InvalidSalesLane, match="rodzaj"):
        parse_sales_lane_row(
            "sln_repeat_01",
            "pipeline",
            "tenant:manual",
            "PLGDN",
            "DEHAM",
        )


def test_parse_sales_lane_row_rejects_same_ends() -> None:
    with pytest.raises(InvalidSalesLane, match="tych samych"):
        parse_sales_lane_row(
            "sln_repeat_01",
            "repeat",
            "tenant:manual",
            "PLGDN",
            "PLGDN",
        )


def test_parse_sales_lane_row_rejects_bad_unlocode() -> None:
    with pytest.raises(InvalidSalesLane, match="para miejsc"):
        parse_sales_lane_row(
            "sln_repeat_01",
            "repeat",
            "tenant:manual",
            "XXX",
            "DEHAM",
        )
