import pytest

from app.domain.errors import InvalidTripBillMark
from app.domain.trip_bill_mark import parse_trip_bill_mark_row


def test_parse_trip_bill_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_trip_bill_mark_row(
        "bill_ready_01",
        "Ready",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("bill_ready_01", "ready", "tenant:manual")


def test_parse_trip_bill_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidTripBillMark, match="rodzaj"):
        parse_trip_bill_mark_row(
            "bill_ready_01",
            "trips_to_bill",
            "tenant:manual",
        )


def test_parse_trip_bill_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidTripBillMark, match="wskazanie"):
        parse_trip_bill_mark_row(
            "bill_ready_01",
            "other",
            "http://evil.example/x",
        )
