from datetime import date

import pytest

from app.domain.errors import InvalidShipment
from app.domain.shipment import require_shipment_anchor_date


def test_anchor_date_none_and_blank_are_null() -> None:
    assert require_shipment_anchor_date(None) is None
    assert require_shipment_anchor_date("") is None
    assert require_shipment_anchor_date("  ") is None


def test_anchor_date_iso_and_date_object() -> None:
    assert require_shipment_anchor_date("2026-09-22") == date(2026, 9, 22)
    assert require_shipment_anchor_date(date(2026, 1, 2)) == date(2026, 1, 2)


def test_anchor_date_bad_shape_is_data() -> None:
    with pytest.raises(InvalidShipment, match="data"):
        require_shipment_anchor_date("22-09-2026")
    with pytest.raises(InvalidShipment, match="data"):
        require_shipment_anchor_date(123)
