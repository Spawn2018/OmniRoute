import pytest

from app.domain.errors import InvalidPositionEvent
from app.domain.position_event import parse_position_event_row


def test_parse_position_event_row_accepts_manual() -> None:
    code, kind, origin = parse_position_event_row(
        "pos_yard_01",
        "Gps",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("pos_yard_01", "gps", "tenant:manual")


def test_parse_position_event_row_rejects_poll_kind() -> None:
    with pytest.raises(InvalidPositionEvent, match="rodzaj"):
        parse_position_event_row("pos_yard_01", "poll", "tenant:manual")
