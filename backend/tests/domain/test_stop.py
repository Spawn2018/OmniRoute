from datetime import UTC, datetime
from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidStop
from app.domain.stop import (
    require_eta_legal,
    require_eta_physical,
    require_notes_for_driver,
    require_sequence_no,
    require_stop_group_code,
    require_stop_kind,
    require_stop_quantity,
    require_stop_status,
    require_stop_weight_kg,
    require_time_zone,
)


def test_stop_allowlists() -> None:
    assert require_stop_kind("loading") == "loading"
    assert require_stop_status("pending") == "pending"
    assert require_sequence_no(1) == 1
    assert require_time_zone("Europe/Warsaw") == "Europe/Warsaw"


def test_stop_rejects_pickup_queued_and_bare_utc() -> None:
    with pytest.raises(InvalidStop, match="rodzaj"):
        require_stop_kind("pickup")
    with pytest.raises(InvalidStop, match="status"):
        require_stop_status("queued")
    with pytest.raises(InvalidStop, match="strefa"):
        require_time_zone("UTC")
    with pytest.raises(InvalidStop, match="dodatni"):
        require_sequence_no(0)


@given(st.sampled_from(["pickup", "delivery", "waypoint"]))
def test_stop_kind_is_not_qargo_alias(raw: str) -> None:
    with pytest.raises(InvalidStop, match="rodzaj"):
        require_stop_kind(raw)


def test_eta_clocks_require_timezone() -> None:
    clock = datetime(2026, 9, 9, 12, 0, tzinfo=UTC)
    assert require_eta_physical("2026-09-09T12:00:00+00:00") == clock
    assert require_eta_legal("2026-09-09T12:00:00Z") == clock
    with pytest.raises(InvalidStop, match="fizyczny"):
        require_eta_physical("")
    with pytest.raises(InvalidStop, match="fizyczny"):
        require_eta_physical("2026-09-09T12:00:00")
    with pytest.raises(InvalidStop, match="prawny"):
        require_eta_legal("nie-czas")


def test_stop_group_code_omits_blank_and_keeps_token() -> None:
    assert require_stop_group_code(None) is None
    assert require_stop_group_code("  ") is None
    assert require_stop_group_code(" ZA-WY-1 ") == "ZA-WY-1"


def test_stop_group_code_rejects_loose_token() -> None:
    with pytest.raises(InvalidStop, match="grupa"):
        require_stop_group_code("x")
    with pytest.raises(InvalidStop, match="grupa"):
        require_stop_group_code("has space")


def test_notes_for_driver_omits_blank_and_keeps_token() -> None:
    assert require_notes_for_driver(None) is None
    assert require_notes_for_driver("  ") is None
    assert require_notes_for_driver(" brama B ") == "brama B"


def test_notes_for_driver_rejects_too_long() -> None:
    with pytest.raises(InvalidStop, match="notatka"):
        require_notes_for_driver("x" * 257)


def test_stop_weight_kg_omits_blank_and_keeps_decimal() -> None:
    assert require_stop_weight_kg(None) is None
    assert require_stop_weight_kg("  ") is None
    assert require_stop_weight_kg("12.5") == Decimal("12.5000")
    assert require_stop_weight_kg("0") == Decimal("0.0000")


def test_stop_weight_kg_rejects_float_and_negative() -> None:
    with pytest.raises(InvalidStop, match="waga"):
        require_stop_weight_kg(12.5)
    with pytest.raises(InvalidStop, match="waga"):
        require_stop_weight_kg("-1")


def test_stop_quantity_omits_blank_and_keeps_int() -> None:
    assert require_stop_quantity(None) is None
    assert require_stop_quantity("  ") is None
    assert require_stop_quantity(0) == 0
    assert require_stop_quantity(12) == 12
    assert require_stop_quantity("3") == 3


def test_stop_quantity_rejects_float_bool_and_negative() -> None:
    with pytest.raises(InvalidStop, match="ilość"):
        require_stop_quantity(1.5)
    with pytest.raises(InvalidStop, match="ilość"):
        require_stop_quantity(True)
    with pytest.raises(InvalidStop, match="ilość"):
        require_stop_quantity(-1)
