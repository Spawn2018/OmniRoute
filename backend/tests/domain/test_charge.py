from decimal import Decimal

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from app.domain.charge import margin
from app.domain.errors import MixedCurrencyCharge
from app.domain.money import Money

_FOUR_PLACES = Decimal("0.0001")
_AMOUNT = st.decimals(
    min_value=Decimal("-9999999999.9999"),
    max_value=Decimal("9999999999.9999"),
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


def test_margin_is_sell_minus_buy_same_currency() -> None:
    buy = Money.of("10.5", "EUR")
    sell = Money.of("14", "EUR")
    computed = margin(buy, sell)
    assert computed.amount == Decimal("3.5000")
    assert computed.currency.code == "EUR"
    assert not isinstance(computed.amount, float)


def test_margin_rejects_mixed_currency() -> None:
    with pytest.raises(MixedCurrencyCharge, match="tę samą walutę"):
        margin(Money.of("10", "EUR"), Money.of("14", "USD"))


def test_margin_allows_negative_when_sell_below_buy() -> None:
    computed = margin(Money.of("20", "PLN"), Money.of("12.25", "PLN"))
    assert computed.amount == Decimal("-7.7500")
    assert computed.currency.code == "PLN"


@given(buy_amount=_AMOUNT, sell_amount=_AMOUNT)
def test_margin_matches_decimal_subtraction(buy_amount: Decimal, sell_amount: Decimal) -> None:
    assume((sell_amount - buy_amount).copy_abs() < Decimal("10000000000"))
    buy = Money.of(buy_amount, "EUR")
    sell = Money.of(sell_amount, "EUR")
    computed = margin(buy, sell)
    assert computed.amount == (sell_amount - buy_amount).quantize(_FOUR_PLACES)
    assert computed.currency.code == "EUR"
