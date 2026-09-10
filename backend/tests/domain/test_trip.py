from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTrip
from app.domain.trip import (
    require_distinct_drivers,
    require_expected_buy,
    require_route_label,
    require_trip_actual_distance_km,
    require_trip_no,
    require_trip_planned_distance_km,
    require_trip_slot,
    require_trip_source_ref,
    require_trip_status,
    require_trip_subcontractor_party_id,
)


def test_trip_allowlists() -> None:
    assert require_trip_no(" TR-1 ") == "TR-1"
    assert require_trip_status("in_transit") == "in_transit"
    assert require_trip_source_ref("fixture://trip/a") == "fixture://trip/a"
    require_trip_slot("vehicle", "vehicle")
    require_trip_slot("driver", "driver")


def test_trip_rejects_queued_and_driver_on_vehicle_slot() -> None:
    with pytest.raises(InvalidTrip, match="status"):
        require_trip_status("queued")
    with pytest.raises(InvalidTrip, match="numer"):
        require_trip_no("  ")
    with pytest.raises(InvalidTrip, match="rodzaj"):
        require_trip_slot("vehicle", "driver")
    with pytest.raises(InvalidTrip, match="obce"):
        require_trip_source_ref("https://evil.example/trip")


def test_trip_freezes_expected_buy_only_in_transit() -> None:
    amount, currency = require_expected_buy("in_transit", "1250.5000", "eur")
    assert str(amount) == "1250.5000"
    assert currency == "EUR"
    idle_amount, idle_currency = require_expected_buy("planned", None, None)
    assert idle_amount is None
    assert idle_currency is None
    with pytest.raises(InvalidTrip, match="kwota"):
        require_expected_buy("in_transit", None, None)
    with pytest.raises(InvalidTrip, match="snapshot"):
        require_expected_buy("planned", "10.0000", "EUR")
    with pytest.raises(InvalidTrip, match="kwota"):
        require_expected_buy("in_transit", 0.5, "EUR")


@given(st.sampled_from(["queued", "running", "open"]))
def test_trip_status_is_not_loose_workflow_word(raw: str) -> None:
    with pytest.raises(InvalidTrip, match="status"):
        require_trip_status(raw)


def test_distinct_drivers_allows_second_seat_or_blank() -> None:
    first = uuid4()
    second = uuid4()
    require_distinct_drivers(first, second)
    require_distinct_drivers(first, None)
    require_distinct_drivers(None, second)


def test_distinct_drivers_rejects_same_uuid() -> None:
    token = uuid4()
    with pytest.raises(InvalidTrip, match="kierowca"):
        require_distinct_drivers(token, token)


def test_route_label_omits_blank_and_keeps_token() -> None:
    assert require_route_label(None) is None
    assert require_route_label("  ") is None
    assert require_route_label(" GDYNIA (PL) - BLONIE (PL) ") == "GDYNIA (PL) - BLONIE (PL)"


def test_route_label_rejects_too_long() -> None:
    with pytest.raises(InvalidTrip, match="trasa"):
        require_route_label("x" * 129)


def test_planned_distance_omits_blank_and_keeps_zero() -> None:
    assert require_trip_planned_distance_km(None) is None
    assert require_trip_planned_distance_km("  ") is None
    assert str(require_trip_planned_distance_km(0)) == "0.0000"
    assert str(require_trip_planned_distance_km("12.5")) == "12.5000"


def test_planned_distance_rejects_float_bool_and_negative() -> None:
    with pytest.raises(InvalidTrip, match="km"):
        require_trip_planned_distance_km(1.5)
    with pytest.raises(InvalidTrip, match="km"):
        require_trip_planned_distance_km(True)
    with pytest.raises(InvalidTrip, match="km"):
        require_trip_planned_distance_km(-1)


def test_actual_distance_omits_blank_and_keeps_zero() -> None:
    assert require_trip_actual_distance_km(None) is None
    assert require_trip_actual_distance_km("  ") is None
    assert str(require_trip_actual_distance_km(0)) == "0.0000"
    assert str(require_trip_actual_distance_km("8.25")) == "8.2500"


def test_actual_distance_rejects_float_bool_and_negative() -> None:
    with pytest.raises(InvalidTrip, match="km"):
        require_trip_actual_distance_km(1.5)
    with pytest.raises(InvalidTrip, match="km"):
        require_trip_actual_distance_km(True)
    with pytest.raises(InvalidTrip, match="km"):
        require_trip_actual_distance_km(-1)


def test_subcontractor_party_id_accepts_uuid_and_rejects_text() -> None:
    mark = uuid4()
    assert require_trip_subcontractor_party_id(None) is None
    assert require_trip_subcontractor_party_id(mark) == mark
    with pytest.raises(InvalidTrip, match="podwykonawca"):
        require_trip_subcontractor_party_id(str(mark))
    with pytest.raises(InvalidTrip, match="podwykonawca"):
        require_trip_subcontractor_party_id(True)
