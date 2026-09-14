import pytest

from app.domain.errors import InvalidOpsRoomMark
from app.domain.ops_room_mark import parse_ops_room_mark_row


def test_parse_ops_room_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_ops_room_mark_row(
        "ops_shift_01",
        "Shift",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("ops_shift_01", "shift", "tenant:manual")


def test_parse_ops_room_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidOpsRoomMark, match="rodzaj"):
        parse_ops_room_mark_row(
            "ops_shift_01",
            "live_board",
            "tenant:manual",
        )
