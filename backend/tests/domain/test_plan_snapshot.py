from datetime import datetime
from uuid import UUID, uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPlanSnapshot
from app.domain.plan_snapshot import (
    require_author_label,
    require_recorded_at,
    require_resource_id,
    require_shipment_id,
    require_snapshot_code,
    require_snapshot_source_ref,
    require_trip_id,
)

_HITL = "2026-09-10T12:00:00+02:00"


@given(st.sampled_from(["plan_v1", "winter_cut", "ab"]))
def test_snapshot_code_accepts_snake(raw: str) -> None:
    assert require_snapshot_code(f" {raw} ") == raw


@given(st.sampled_from(["", "X", "1bad", "MIGAWKA", "plan-v1"]))
def test_snapshot_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidPlanSnapshot, match="migawka"):
        require_snapshot_code(raw)


def test_triplet_uuid_accepts_uuid_and_text() -> None:
    stamp = uuid4()
    assert require_shipment_id(stamp) == stamp
    assert require_trip_id(str(stamp)) == stamp
    assert require_resource_id(f" {stamp} ") == stamp


@given(st.sampled_from(["", "nie-uuid", "123"]))
def test_triplet_uuid_rejects_with_polish_tokens(raw: str) -> None:
    with pytest.raises(InvalidPlanSnapshot, match="zlecenie"):
        require_shipment_id(raw)
    with pytest.raises(InvalidPlanSnapshot, match="przejazd"):
        require_trip_id(raw)
    with pytest.raises(InvalidPlanSnapshot, match="zasob"):
        require_resource_id(raw)


def test_author_label_strips_and_bounds() -> None:
    assert require_author_label("  Anna  ") == "Anna"
    with pytest.raises(InvalidPlanSnapshot, match="autor"):
        require_author_label("")
    with pytest.raises(InvalidPlanSnapshot, match="autor"):
        require_author_label("x" * 65)


def test_recorded_at_requires_timezone() -> None:
    when = require_recorded_at(_HITL)
    assert isinstance(when, datetime)
    assert when.tzinfo is not None
    with pytest.raises(InvalidPlanSnapshot, match="czas"):
        require_recorded_at("")
    with pytest.raises(InvalidPlanSnapshot, match="czas"):
        require_recorded_at("2026-09-10T12:00:00")
    with pytest.raises(InvalidPlanSnapshot, match="czas"):
        require_recorded_at("nie-iso")


def test_snapshot_source_ref_accepts_fixture() -> None:
    assert require_snapshot_source_ref(" fixture://plan-snapshot/1 ") == (
        "fixture://plan-snapshot/1"
    )
    assert require_snapshot_source_ref("tenant:manual") == "tenant:manual"


@given(st.sampled_from(["", "   ", "http://hold.example/x", "fixture://other/1"]))
def test_snapshot_source_ref_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidPlanSnapshot, match="obce"):
        require_snapshot_source_ref(raw)


def test_shipment_id_type_guard() -> None:
    with pytest.raises(InvalidPlanSnapshot, match="zlecenie"):
        require_shipment_id(1)
    assert require_shipment_id(UUID("00000000-0000-4000-8000-000000000001"))
