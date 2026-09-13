import pytest

from app.domain.errors import InvalidFerryBookingMark
from app.domain.ferry_booking_mark import parse_ferry_booking_mark_row


def test_parse_ferry_booking_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_ferry_booking_mark_row(
        "fbk_book_01",
        "Booking",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("fbk_book_01", "booking", "tenant:manual")


def test_parse_ferry_booking_mark_row_rejects_ticket_kind() -> None:
    with pytest.raises(InvalidFerryBookingMark, match="rodzaj"):
        parse_ferry_booking_mark_row("fbk_book_01", "ticket", "tenant:manual")
