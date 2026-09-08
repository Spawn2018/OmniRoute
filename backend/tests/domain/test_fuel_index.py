from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidFuelIndex
from app.domain.fuel_index import (
    require_index_kind,
    require_index_source_ref,
    require_index_value,
    require_published_on,
)


@given(st.sampled_from(["fsc", "baf", "caf", "FSC"]))
def test_index_kind_normalizes_allowlist(raw: str) -> None:
    assert require_index_kind(raw) == raw.strip().lower()


@given(st.sampled_from(["", "oil", "FSC1"]))
def test_index_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidFuelIndex, match="rodzaj"):
        require_index_kind(raw)


def test_published_on_parses_iso() -> None:
    assert require_published_on("2026-03-01").isoformat() == "2026-03-01"


@given(st.sampled_from(["", "   ", "nope"]))
def test_published_on_rejects_empty_and_garbage(raw: str) -> None:
    with pytest.raises(InvalidFuelIndex, match="data"):
        require_published_on(raw)


def test_index_value_rejects_float() -> None:
    with pytest.raises(InvalidFuelIndex, match="indeks"):
        require_index_value(12.5)  # type: ignore[arg-type]


def test_index_value_rejects_zero() -> None:
    with pytest.raises(InvalidFuelIndex, match="indeks"):
        require_index_value("0")


_POSITIVE = st.decimals(
    min_value="0.0001",
    max_value="9999",
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


@given(_POSITIVE)
def test_index_value_quantizes(units: Decimal) -> None:
    assert require_index_value(str(units)) == units


def test_index_source_ref_accepts_fixture() -> None:
    assert require_index_source_ref(" fixture://fuel-index/1 ") == "fixture://fuel-index/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_index_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidFuelIndex):
        require_index_source_ref(raw)
