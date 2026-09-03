from datetime import UTC, datetime
from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTrackingEvent
from app.domain.tracking_event import (
    require_event_kind,
    require_occurred_at,
    require_shipment_id,
    require_tracking_source_ref,
)


def test_require_event_kind_accepts_allowlist() -> None:
    assert require_event_kind(" departed ") == "departed"
    assert require_event_kind("arrived") == "arrived"
    assert require_event_kind("noted") == "noted"


def test_require_event_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidTrackingEvent, match="rodzaj"):
        require_event_kind("eta")


def test_require_occurred_at_rejects_naive() -> None:
    with pytest.raises(InvalidTrackingEvent, match="strefy"):
        require_occurred_at(datetime(2026, 9, 3, 10, 0))


def test_require_occurred_at_keeps_aware() -> None:
    stamp = datetime(2026, 9, 3, 10, 0, tzinfo=UTC)
    assert require_occurred_at(stamp) is stamp


def test_require_tracking_source_ref_accepts_fixture() -> None:
    assert (
        require_tracking_source_ref(" fixture://tracking/1 ") == "fixture://tracking/1"
    )


@given(st.sampled_from(["", "   ", "http://ais.example/x"]))
def test_require_tracking_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTrackingEvent):
        require_tracking_source_ref(raw)


def test_require_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidTrackingEvent, match="UUID"):
        require_shipment_id("ship")  # type: ignore[arg-type]


def test_require_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_shipment_id(token) == token
