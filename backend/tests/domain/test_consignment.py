from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.consignment import (
    parse_optional_load_kind,
    require_consignment_ref,
    require_consignment_shipment_id,
    require_consignment_source_ref,
    require_ftl_room,
)
from app.domain.errors import ConsignmentFtlLimit, InvalidConsignment


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


def test_parse_optional_load_kind_none() -> None:
    assert parse_optional_load_kind(None) is None


def test_parse_optional_load_kind_ftl() -> None:
    assert parse_optional_load_kind(" FTL ") == "ftl"


def test_parse_optional_load_kind_rejects_other() -> None:
    with pytest.raises(InvalidConsignment, match="ftl albo ltl"):
        parse_optional_load_kind("groupage")


def test_require_ftl_room_raises() -> None:
    with pytest.raises(ConsignmentFtlLimit, match="FTL"):
        require_ftl_room(1)


def test_require_ftl_room_allows_empty() -> None:
    require_ftl_room(0)
