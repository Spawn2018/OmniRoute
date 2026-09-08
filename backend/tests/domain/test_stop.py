
import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidStop
from app.domain.stop import (
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
