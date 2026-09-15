import pytest

from app.domain.errors import InvalidShipperBindMark
from app.domain.shipper_bind_mark import parse_shipper_bind_mark_row


def test_parse_shipper_bind_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_shipper_bind_mark_row(
        "shipper_bind_tender_01",
        "Tender",
        "tenant:manual",
    )
    assert code == "shipper_bind_tender_01"
    assert kind == "tender"
    assert origin == "tenant:manual"


def test_parse_shipper_bind_mark_row_rejects_alpega_kind() -> None:
    with pytest.raises(InvalidShipperBindMark, match="bind_kind"):
        parse_shipper_bind_mark_row("shipper_bind_tender_01", "alpega", "tenant:manual")
