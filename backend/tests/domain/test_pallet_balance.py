from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPalletBalance
from app.domain.pallet_balance import (
    require_balance_party_id,
    require_balance_source_ref,
    require_pallet_kind,
    require_unit_count,
)


@given(st.sampled_from(["chep", "lpr"]))
def test_pallet_kind_allowlist(raw: str) -> None:
    assert require_pallet_kind(raw) == raw


@given(st.sampled_from(["euro", "epal", "CHEP"]))
def test_pallet_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidPalletBalance, match="rodzaj"):
        require_pallet_kind(raw)


@given(st.integers(min_value=0, max_value=10_000))
def test_unit_count_accepts_non_negative_int(raw: int) -> None:
    assert require_unit_count(raw) == raw


@given(st.sampled_from([-1, True, 1.5, "12"]))
def test_unit_count_rejects_negative_float_bool_text(raw: object) -> None:
    with pytest.raises(InvalidPalletBalance, match="sztuk"):
        require_unit_count(raw)


def test_balance_source_ref_accepts_fixture() -> None:
    assert (
        require_balance_source_ref(" fixture://pallet-balance/1 ")
        == "fixture://pallet-balance/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_balance_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidPalletBalance):
        require_balance_source_ref(raw)


def test_balance_party_id_rejects_text() -> None:
    with pytest.raises(InvalidPalletBalance, match="UUID"):
        require_balance_party_id("chep")  # type: ignore[arg-type]


def test_balance_party_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_balance_party_id(token) == token
