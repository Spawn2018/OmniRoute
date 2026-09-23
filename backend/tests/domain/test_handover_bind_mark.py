import pytest

from app.domain.errors import InvalidHandoverBindMark
from app.domain.handover_bind_mark import parse_handover_bind_mark_row


def test_parse_handover_bind_mark_row_accepts_note() -> None:
    code, kind, origin = parse_handover_bind_mark_row(
        "bind_note_01",
        "note",
        "fixture://handover-bind/a",
    )
    assert code == "bind_note_01"
    assert kind == "note"
    assert origin == "fixture://handover-bind/a"


def test_parse_handover_bind_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidHandoverBindMark, match="wiązanie"):
        parse_handover_bind_mark_row(
            "bind_note_01",
            "live",
            "tenant:manual",
        )


def test_parse_handover_bind_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidHandoverBindMark, match="obce"):
        parse_handover_bind_mark_row(
            "bind_note_01",
            "note",
            "http://evil",
        )
