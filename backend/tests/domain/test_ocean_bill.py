from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidOceanBill
from app.domain.ocean_bill import (
    require_bill_kind,
    require_bill_no,
    require_bill_shipment_id,
    require_bill_source_ref,
)


@given(st.sampled_from(["HLCUSHA1234567", "MSCU-AB12", "hlb1"]))
def test_bill_no_keeps_carrier_token(raw: str) -> None:
    assert require_bill_no(raw) == raw


@given(st.sampled_from(["", "X", "HBL 1", "a" * 33, "hbl_west"]))
def test_bill_no_rejects_non_carrier_token(raw: str) -> None:
    with pytest.raises(InvalidOceanBill, match="numer"):
        require_bill_no(raw)


@given(st.sampled_from(["hbl", "mbl"]))
def test_bill_kind_allowlist(raw: str) -> None:
    assert require_bill_kind(raw) == raw


@given(st.sampled_from(["hawb", "swb", "bill_of_lading", "HBL"]))
def test_bill_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidOceanBill, match="rodzaj"):
        require_bill_kind(raw)


def test_bill_source_ref_accepts_fixture() -> None:
    assert (
        require_bill_source_ref(" fixture://ocean-bill/1 ") == "fixture://ocean-bill/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_bill_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidOceanBill):
        require_bill_source_ref(raw)


def test_bill_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidOceanBill, match="UUID"):
        require_bill_shipment_id("hbl")  # type: ignore[arg-type]


def test_bill_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_bill_shipment_id(token) == token
