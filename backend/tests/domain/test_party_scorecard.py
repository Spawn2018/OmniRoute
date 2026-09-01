from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPartyScorecard
from app.domain.party_scorecard import (
    optional_non_negative_hours,
    optional_unit_interval,
    required_sample_size,
    required_window_days,
)

_UNIT = st.decimals(
    min_value=Decimal("0"),
    max_value=Decimal("1"),
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


def test_optional_unit_interval_blank_is_unknown() -> None:
    assert optional_unit_interval(None, "response_rate") is None
    assert optional_unit_interval("  ", "response_rate") is None


def test_optional_unit_interval_rejects_outside_zero_one() -> None:
    with pytest.raises(InvalidPartyScorecard, match="0–1"):
        optional_unit_interval("1.0001", "response_rate")


def test_optional_unit_interval_rejects_float() -> None:
    with pytest.raises(InvalidPartyScorecard, match="dziesiętną"):
        optional_unit_interval(0.5, "response_rate")


def test_optional_non_negative_hours_rejects_negative() -> None:
    with pytest.raises(InvalidPartyScorecard, match="ujemna"):
        optional_non_negative_hours("-0.1")


def test_required_window_days_defaults_to_ninety() -> None:
    assert required_window_days(None) == 90


def test_required_window_days_rejects_zero() -> None:
    with pytest.raises(InvalidPartyScorecard, match="dodatnie"):
        required_window_days(0)


def test_required_sample_size_defaults_to_zero() -> None:
    assert required_sample_size(None) == 0


@given(value=_UNIT)
def test_optional_unit_interval_is_idempotent_on_canonical_decimal(value: Decimal) -> None:
    assert optional_unit_interval(value, "price_position") == value.quantize(Decimal("0.0001"))
    assert optional_unit_interval(str(value), "price_position") == value.quantize(Decimal("0.0001"))
