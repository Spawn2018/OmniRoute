import pytest

from app.domain.errors import InvalidHandoverNote
from app.domain.handover_note import parse_handover_note_row


def test_parse_handover_note_row_accepts_manual() -> None:
    code, sit, back, assess, rec, origin = parse_handover_note_row(
        "shift_a_01",
        "sytuacja",
        "tlo",
        "ocena",
        "rekom",
        "tenant:manual",
    )
    assert code == "shift_a_01"
    assert sit == "sytuacja"
    assert back == "tlo"
    assert assess == "ocena"
    assert rec == "rekom"
    assert origin == "tenant:manual"


def test_parse_handover_note_row_rejects_empty_field() -> None:
    with pytest.raises(InvalidHandoverNote, match="sytuacja"):
        parse_handover_note_row(
            "shift_a_01",
            "  ",
            "tlo",
            "ocena",
            "rekom",
            "tenant:manual",
        )


def test_parse_handover_note_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidHandoverNote, match="wskazanie"):
        parse_handover_note_row(
            "shift_a_01",
            "sytuacja",
            "tlo",
            "ocena",
            "rekom",
            "http://evil.example/x",
        )
