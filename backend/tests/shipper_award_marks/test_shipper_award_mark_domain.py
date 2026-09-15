import pytest

from app.domain.errors import InvalidShipperAwardMark
from app.domain.shipper_award_mark import parse_shipper_award_mark_row


def test_parse_shipper_award_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_shipper_award_mark_row(
        "shipper_award_go_01",
        "Go",
        "tenant:manual",
    )
    assert code == "shipper_award_go_01"
    assert kind == "go"
    assert origin == "tenant:manual"


def test_parse_shipper_award_mark_row_rejects_alpega_kind() -> None:
    with pytest.raises(InvalidShipperAwardMark, match="award_kind"):
        parse_shipper_award_mark_row("shipper_award_go_01", "alpega", "tenant:manual")
