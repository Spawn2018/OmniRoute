from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidMoney
from app.domain.money import Money

_FOUR_PLACES = Decimal("0.0001")
_CURRENCY = st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=3, max_size=3)
_AMOUNT = st.decimals(
    min_value=Decimal("-9999999999.9999"),
    max_value=Decimal("9999999999.9999"),
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


def test_money_binds_decimal_amount_to_currency() -> None:
    money = Money.of("125.5", "EUR")
    assert money.amount == Decimal("125.5000")
    assert money.currency.code == "EUR"


def test_money_rejects_float() -> None:
    with pytest.raises(InvalidMoney, match="float"):
        Money.of(1.25, "EUR")  # type: ignore[arg-type]


def test_money_rejects_bool() -> None:
    with pytest.raises(InvalidMoney):
        Money.of(True, "EUR")  # type: ignore[arg-type]


def test_money_rejects_currency_that_is_not_iso4217() -> None:
    with pytest.raises(InvalidMoney, match="ISO 4217"):
        Money.of("10", "eu")


def test_money_rejects_more_than_four_fractional_digits() -> None:
    with pytest.raises(InvalidMoney, match="14,4"):
        Money.of("1.12345", "EUR")


def test_same_amount_different_currency_is_not_equal() -> None:
    assert Money.of("10", "EUR") != Money.of("10", "USD")


def test_money_serializes_amount_as_decimal_string() -> None:
    pair = Money.of("10", "PLN").as_pair()
    assert pair == ("10.0000", "PLN")
    assert not isinstance(pair[0], float)


def test_money_rejects_non_decimal_input() -> None:
    with pytest.raises(InvalidMoney):
        Money.of(["10"], "EUR")


def test_money_rejects_unparseable_string() -> None:
    with pytest.raises(InvalidMoney):
        Money.of("10 EUR", "EUR")


def test_money_rejects_non_finite_decimal() -> None:
    with pytest.raises(InvalidMoney):
        Money.of(Decimal("NaN"), "EUR")


def test_money_rejects_amount_outside_numeric_14_4() -> None:
    with pytest.raises(InvalidMoney, match="14,4"):
        Money.of("10000000000", "EUR")


def test_money_accepts_existing_currency() -> None:
    first = Money.of("1", "EUR")
    again = Money.of("2", first.currency)
    assert again.currency is first.currency


def test_money_rejects_non_string_currency() -> None:
    with pytest.raises(InvalidMoney, match="ISO 4217"):
        Money.of("1", 978)


@given(amount=_AMOUNT, code=_CURRENCY)
def test_money_roundtrip_keeps_amount_bound_to_currency(amount: Decimal, code: str) -> None:
    money = Money.of(amount, code)
    assert money.amount == amount.quantize(_FOUR_PLACES)
    assert money.currency.code == code
    assert Money.of(str(money.amount), money.currency.code) == money
