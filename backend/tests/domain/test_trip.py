import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTrip
from app.domain.trip import (
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


@given(st.sampled_from(["queued", "running", "open"]))
def test_trip_status_is_not_loose_workflow_word(raw: str) -> None:
    with pytest.raises(InvalidTrip, match="status"):
        require_trip_status(raw)
