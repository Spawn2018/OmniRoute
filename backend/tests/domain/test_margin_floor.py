from decimal import Decimal

import pytest

from app.domain.errors import InvalidMarginFloor, MarginFloorBreach
from app.domain.margin_floor import (
    parse_margin_floor_row,
    parse_optional_floor_lane,
    require_margin_above_floor,
)


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "floor_code": "floor_gdn_ham",
        "origin_unlocode": "PLGDN",
        "destination_unlocode": "DEHAM",
        "floor_amount": "120",
        "floor_currency": "EUR",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_margin_floor_row(
        body["floor_code"],
        body["origin_unlocode"],
        body["destination_unlocode"],
        body["floor_amount"],
        body["floor_currency"],
        body["source_ref"],
    )


def test_parse_accepts_manual_row() -> None:
    draft = _ok()
    assert draft.floor_code == "floor_gdn_ham"
    assert draft.origin_unlocode == "PLGDN"
    assert draft.destination_unlocode == "DEHAM"
    assert draft.floor_amount == Decimal("120.0000")
    assert draft.floor_currency == "EUR"


def test_parse_rejects_float_amount() -> None:
    with pytest.raises(InvalidMarginFloor, match="float"):
        _ok(floor_amount=1.5)


def test_parse_rejects_bad_currency() -> None:
    with pytest.raises(InvalidMarginFloor, match="waluta"):
        _ok(floor_currency="eur")


def test_parse_rejects_same_ends() -> None:
    with pytest.raises(InvalidMarginFloor, match="końców"):
        _ok(destination_unlocode="PLGDN")


def test_parse_rejects_bad_unlocode() -> None:
    with pytest.raises(InvalidMarginFloor, match="para miejsc"):
        _ok(origin_unlocode="xx")


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidMarginFloor, match="oznaczenie"):
        _ok(floor_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidMarginFloor, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")


def test_optional_lane_none_when_both_missing() -> None:
    assert parse_optional_floor_lane(None, None) is None


def test_optional_lane_requires_both_ends() -> None:
    with pytest.raises(InvalidMarginFloor, match="obu końców"):
        parse_optional_floor_lane("PLGDN", None)


def test_require_margin_above_floor_raises_breach() -> None:
    with pytest.raises(MarginFloorBreach, match="podłogi"):
        require_margin_above_floor(
            margin_amount=Decimal("3.0000"),
            margin_currency="EUR",
            floor_amount=Decimal("5.0000"),
            floor_currency="EUR",
        )


def test_require_margin_above_floor_allows_equal() -> None:
    require_margin_above_floor(
        margin_amount=Decimal("5.0000"),
        margin_currency="EUR",
        floor_amount=Decimal("5.0000"),
        floor_currency="EUR",
    )
