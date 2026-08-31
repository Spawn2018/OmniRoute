from app.domain.errors import MixedCurrencyCharge
from app.domain.money import Money


def margin(buy: Money, sell: Money) -> Money:
    if buy.currency != sell.currency:
        raise MixedCurrencyCharge("buy i sell muszą mieć tę samą walutę")
    return Money.of(sell.amount - buy.amount, buy.currency)
