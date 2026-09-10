from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.consignment import (
    require_consignment_ref,
    require_consignment_shipment_id,
    require_consignment_source_ref,
)
from app.domain.errors import InvalidConsignment


@given(st.sampled_from(["CN-1", "house.west:1", "ab"]))
def test_consignment_ref_keeps_token(raw: str) -> None:
    assert require_consignment_ref(raw) == raw


@given(st.sampled_from(["", "X", "CN 1", "a" * 65, "cn/west"]))
def test_consignment_ref_rejects_bad_token(raw: str) -> None:
    with pytest.raises(InvalidConsignment, match="przesyłka"):
        require_consignment_ref(raw)


def test_consignment_source_ref_accepts_fixture() -> None:
    assert (
        require_consignment_source_ref(" fixture://consignment/1 ")
        == "fixture://consignment/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_consignment_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidConsignment, match="obce|przesyłki"):
        require_consignment_source_ref(raw)


def test_consignment_shipment_id_rejects_bool() -> None:
    with pytest.raises(InvalidConsignment, match="zlecenie"):
        require_consignment_shipment_id(True)  # type: ignore[arg-type]


def test_consignment_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_consignment_shipment_id(token) == token
