import pytest

from app.domain.errors import InvalidShipmentCloneMark
from app.domain.shipment_clone_mark import parse_shipment_clone_mark_row


def test_parse_shipment_clone_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_shipment_clone_mark_row(
        "clone_last_01",
        "Last_Similar",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("clone_last_01", "last_similar", "tenant:manual")


def test_parse_shipment_clone_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidShipmentCloneMark, match="rodzaj"):
        parse_shipment_clone_mark_row(
            "clone_last_01",
            "auto_copy",
            "tenant:manual",
        )


def test_parse_shipment_clone_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidShipmentCloneMark, match="wskazanie"):
        parse_shipment_clone_mark_row(
            "clone_last_01",
            "other",
            "http://evil.example/x",
        )
