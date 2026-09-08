from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidRateCard
from app.domain.rate_card import (
    require_applies_when,
    require_card_amount,
    require_card_code,
    require_card_currency,
    require_card_source_ref,
)


@given(st.sampled_from(["weekend", "ltl_100", "band_west"]))
def test_card_code_normalizes_snake(raw: str) -> None:
    assert require_card_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_card_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidRateCard, match="kod"):
        require_card_code(raw)


@given(st.sampled_from(["weekend", "kontener 40HC"]))
def test_applies_when_keeps_text(raw: str) -> None:
    assert require_applies_when(raw) == raw


@given(st.sampled_from(["", "   ", "x" * 513]))
def test_applies_when_rejects_empty_and_long(raw: str) -> None:
    with pytest.raises(InvalidRateCard, match="warunek"):
        require_applies_when(raw)


def test_card_amount_rejects_float() -> None:
    with pytest.raises(InvalidRateCard, match="kwota"):
        require_card_amount(12.5)  # type: ignore[arg-type]


def test_card_amount_rejects_zero() -> None:
    with pytest.raises(InvalidRateCard, match="kwota"):
        require_card_amount("0")


_POSITIVE = st.decimals(
    min_value="0.0001",
    max_value="9999",
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


@given(_POSITIVE)
def test_card_amount_quantizes(units: Decimal) -> None:
    assert require_card_amount(str(units)) == units


def test_card_currency_iso() -> None:
    assert require_card_currency("eur") == "EUR"


def test_card_source_ref_accepts_fixture() -> None:
    assert require_card_source_ref(" fixture://rate-card/1 ") == "fixture://rate-card/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_card_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidRateCard):
        require_card_source_ref(raw)
