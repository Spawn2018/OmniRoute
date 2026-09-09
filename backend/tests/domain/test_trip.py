from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTrip
from app.domain.trip import (
    require_distinct_drivers,
    require_expected_buy,
    require_trip_no,
    require_trip_slot,
    require_trip_source_ref,
    require_trip_status,
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
