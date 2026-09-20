from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidStopGroup
from app.domain.stop_group import (
    require_stop_group_code,
    require_stop_group_shipment_id,
    require_stop_group_source_ref,
)


@given(st.sampled_from(["G1", "grp_west", "ab-cd"]))
def test_stop_group_code_keeps_token(raw: str) -> None:
    assert require_stop_group_code(raw) == raw


@given(st.sampled_from(["", "X", "g p", "a" * 33, "grp/west"]))
def test_stop_group_code_rejects_bad_token(raw: str) -> None:
    with pytest.raises(InvalidStopGroup, match="grupa"):
        require_stop_group_code(raw)


def test_stop_group_source_ref_accepts_fixture() -> None:
    assert (
        require_stop_group_source_ref(" fixture://stop-group/1 ")
        == "fixture://stop-group/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_stop_group_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidStopGroup, match="obce|grupy"):
        require_stop_group_source_ref(raw)


def test_stop_group_shipment_id_rejects_bool() -> None:
    with pytest.raises(InvalidStopGroup, match="zlecenie"):
        require_stop_group_shipment_id(True)  # type: ignore[arg-type]


def test_stop_group_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_stop_group_shipment_id(token) == token
