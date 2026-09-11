import pytest

from app.domain.collaboration_mark import parse_collaboration_mark_row
from app.domain.errors import InvalidCollaborationMark


def test_parse_collaboration_accepts() -> None:
    code, kind, origin = parse_collaboration_mark_row(
        " seat_shipper_01 ",
        " Shipper ",
        "fixture://collaboration-mark/a",
    )
    assert code == "seat_shipper_01"
    assert kind == "shipper"
    assert origin == "fixture://collaboration-mark/a"


def test_parse_collaboration_rejects() -> None:
    with pytest.raises(InvalidCollaborationMark, match="oznaczenie"):
        parse_collaboration_mark_row("X", "shipper", "tenant:manual")
    with pytest.raises(InvalidCollaborationMark, match="rodzaj"):
        parse_collaboration_mark_row("seat_01", "broker", "tenant:manual")
    with pytest.raises(InvalidCollaborationMark, match="obce"):
        parse_collaboration_mark_row("seat_01", "carrier", "http://evil")
