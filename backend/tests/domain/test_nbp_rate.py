from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidCurrency, InvalidNbpRate
from app.domain.nbp_rate import normalize_currency, normalize_nbp_mid

_CURRENCY = st.from_regex(r"[A-Z]{3}", fullmatch=True).filter(lambda token: token != "PLN")


def test_normalize_currency_strips_and_uppercases() -> None:
    assert normalize_currency(" eur ") == "EUR"


def test_normalize_currency_rejects_pln() -> None:
    with pytest.raises(InvalidCurrency, match="PLN"):
        normalize_currency("PLN")


def test_normalize_currency_rejects_non_iso() -> None:
    with pytest.raises(InvalidCurrency, match="ISO 4217"):
        normalize_currency("EURO")


def test_normalize_nbp_mid_quantizes_four_decimals() -> None:
    assert normalize_nbp_mid("4.1234") == Decimal("4.1234")
    assert normalize_nbp_mid("4.12346") == Decimal("4.1235")


def test_normalize_nbp_mid_rejects_float() -> None:
    with pytest.raises(InvalidNbpRate, match="dziesiętn"):
        normalize_nbp_mid(4.12)  # type: ignore[arg-type]


@given(token=_CURRENCY)
def test_normalize_currency_is_idempotent(token: str) -> None:
    assert normalize_currency(token) == token
    assert normalize_currency(f" {token.lower()} ") == token


@given(
    units=st.decimals(
        min_value="0.0001",
        max_value="10000",
        places=4,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_normalize_nbp_mid_preserves_decimal(units: Decimal) -> None:
    assert normalize_nbp_mid(units) == units
    assert normalize_nbp_mid(str(units)) == units
