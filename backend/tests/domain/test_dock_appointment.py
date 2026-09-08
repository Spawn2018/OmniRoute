from datetime import date, time

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from app.domain.dock_appointment import (
    require_appointment_code,
    require_appointment_status,
    require_dock_source_ref,
    require_dock_window,
    require_stop_on_shipment,
    require_warehouse_location_kind,
    require_window_date,
)
from app.domain.errors import InvalidDockAppointment
from app.domain.location import LocationKind

_CLOCK = st.builds(time, st.integers(0, 23), st.integers(0, 59), st.integers(0, 59))


@given(st.sampled_from(["dock_1", "gate_a", "hub_west"]))
def test_appointment_code_normalizes_snake(raw: str) -> None:
    assert require_appointment_code(raw) == raw


@given(st.sampled_from(["", "X", "1dock", "DOCK 1", "a" * 33]))
def test_appointment_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidDockAppointment, match="snake"):
        require_appointment_code(raw)


@given(st.sampled_from(["noted", "advised", "at_dock", "released"]))
def test_appointment_status_allowlist(raw: str) -> None:
    assert require_appointment_status(raw) == raw


@given(st.sampled_from(["pending", "queued", "wms", "confirmed"]))
def test_appointment_status_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidDockAppointment, match="status"):
        require_appointment_status(raw)


@given(_CLOCK, _CLOCK)
def test_dock_window_rejects_when_end_not_after_start(start: time, end: time) -> None:
    assume(end <= start)
    with pytest.raises(InvalidDockAppointment, match="okno"):
        require_dock_window(start, end)


@given(_CLOCK, _CLOCK)
def test_dock_window_keeps_times_when_end_after_start(start: time, end: time) -> None:
    assume(end > start)
    assert require_dock_window(start, end) == (
        time(start.hour, start.minute, start.second),
        time(end.hour, end.minute, end.second),
    )


@given(st.just(LocationKind.UNLOCODE.value))
def test_warehouse_kind_rejects_unlocode(kind: str) -> None:
    with pytest.raises(InvalidDockAppointment, match="magazyn"):
        require_warehouse_location_kind(kind)


@given(st.sampled_from([LocationKind.POSTAL_ZONE.value, LocationKind.ADDRESS.value]))
def test_warehouse_kind_allows_land_place(kind: str) -> None:
    assert require_warehouse_location_kind(kind) == kind


def test_stop_off_shipment_is_trasy() -> None:
    from uuid import uuid4

    with pytest.raises(InvalidDockAppointment, match="trasy"):
        require_stop_on_shipment(uuid4(), uuid4())


def test_window_date_is_calendar_day() -> None:
    assert require_window_date(date(2026, 9, 9)) == date(2026, 9, 9)


def test_source_ref_fixture_or_manual() -> None:
    assert require_dock_source_ref("tenant:manual") == "tenant:manual"
    assert (
        require_dock_source_ref("fixture://dock-appointment/1") == "fixture://dock-appointment/1"
    )
    with pytest.raises(InvalidDockAppointment, match="obce"):
        require_dock_source_ref("https://evil.example/dock")
