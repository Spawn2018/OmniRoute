from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.channel_quote import (
    manual_channel_source_ref,
    normalize_quote_amount,
    normalize_quote_currency,
    normalize_quote_date,
    normalize_transit_days,
)
from app.domain.errors import InvalidChannelQuote

_CURRENCY = st.from_regex(r"[A-Z]{3}", fullmatch=True)


def test_normalize_quote_currency_strips_and_uppercases() -> None:
    assert normalize_quote_currency(" pln ") == "PLN"


def test_normalize_quote_currency_rejects_non_iso() -> None:
    with pytest.raises(InvalidChannelQuote, match="ISO 4217"):
        normalize_quote_currency("EURO")


def test_normalize_quote_amount_rejects_float() -> None:
    with pytest.raises(InvalidChannelQuote, match="float"):
        normalize_quote_amount(12.5)  # type: ignore[arg-type]


def test_normalize_quote_amount_rejects_zero() -> None:
    with pytest.raises(InvalidChannelQuote, match="dodatnia"):
        normalize_quote_amount("0")


def test_normalize_quote_date_rejects_string() -> None:
    with pytest.raises(InvalidChannelQuote, match="dniem"):
        normalize_quote_date("2026-09-01")


def test_manual_channel_source_ref_includes_user() -> None:
    user_id = uuid4()
    assert manual_channel_source_ref(user_id) == f"tenant:manual:{user_id}"


def test_normalize_transit_days_rejects_zero() -> None:
    with pytest.raises(InvalidChannelQuote, match="1 dzień"):
        normalize_transit_days(0)
    assert normalize_transit_days(None) is None
    assert normalize_transit_days(12) == 12


def test_normalize_quote_date_accepts_date() -> None:
    day = date(2026, 9, 1)
    assert normalize_quote_date(day) == day


@given(token=_CURRENCY)
def test_normalize_quote_currency_is_idempotent(token: str) -> None:
    assert normalize_quote_currency(token) == token
    assert normalize_quote_currency(f" {token.lower()} ") == token


@given(
    units=st.decimals(
        min_value="0.0001",
        max_value="10000",
        places=4,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_normalize_quote_amount_preserves_decimal(units: Decimal) -> None:
    assert normalize_quote_amount(units) == units
    assert normalize_quote_amount(str(units)) == units
