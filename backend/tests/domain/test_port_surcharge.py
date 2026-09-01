from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPortSurcharge
from app.domain.port_surcharge import (
    normalize_applies_when,
    normalize_surcharge_amount,
    normalize_surcharge_code,
    normalize_surcharge_currency,
    normalize_surcharge_title,
)

_TOKEN = st.from_regex(r"[a-z][a-z0-9_]{1,31}", fullmatch=True)
_CURRENCY = st.from_regex(r"[A-Z]{3}", fullmatch=True)


def test_normalize_surcharge_code_lowers_and_strips() -> None:
    assert normalize_surcharge_code(" THC ") == "thc"


def test_normalize_surcharge_code_replaces_hyphen() -> None:
    assert normalize_surcharge_code("isps-fee") == "isps_fee"


def test_normalize_surcharge_code_rejects_spaces() -> None:
    with pytest.raises(InvalidPortSurcharge, match="snake"):
        normalize_surcharge_code("thc extra")


def test_normalize_surcharge_title_collapses_space() -> None:
    assert normalize_surcharge_title("  THC  weekend  ") == "THC weekend"


def test_normalize_applies_when_trims() -> None:
    assert normalize_applies_when("  weekend i święta  ") == "weekend i święta"


def test_normalize_applies_when_rejects_blank() -> None:
    with pytest.raises(InvalidPortSurcharge, match="warunek"):
        normalize_applies_when("  ")


def test_normalize_surcharge_currency_allows_pln() -> None:
    assert normalize_surcharge_currency(" pln ") == "PLN"


def test_normalize_surcharge_amount_rejects_float() -> None:
    with pytest.raises(InvalidPortSurcharge, match="float"):
        normalize_surcharge_amount(12.5)  # type: ignore[arg-type]


def test_normalize_surcharge_amount_rejects_zero() -> None:
    with pytest.raises(InvalidPortSurcharge, match="dodatnia"):
        normalize_surcharge_amount("0")


@given(token=_TOKEN)
def test_normalize_surcharge_code_is_idempotent(token: str) -> None:
    assert normalize_surcharge_code(token) == token
    assert normalize_surcharge_code(f" {token} ") == token


@given(token=_CURRENCY)
def test_normalize_surcharge_currency_is_idempotent(token: str) -> None:
    assert normalize_surcharge_currency(token) == token
    assert normalize_surcharge_currency(f" {token.lower()} ") == token


@given(
    units=st.decimals(
        min_value="0.0001",
        max_value="10000",
        places=4,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_normalize_surcharge_amount_preserves_decimal(units: Decimal) -> None:
    assert normalize_surcharge_amount(units) == units
    assert normalize_surcharge_amount(str(units)) == units
