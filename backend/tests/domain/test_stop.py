from datetime import UTC, datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidStop
from app.domain.stop import (
    require_eta_legal,
    require_eta_physical,
    require_sequence_no,
    require_stop_kind,
    require_stop_status,
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
