from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidMoney

_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
_FOUR_PLACES = Decimal("0.0001")
_MAX_ABS = Decimal("10000000000")


@dataclass(frozen=True, slots=True)
class Currency:
    code: str

    def __post_init__(self) -> None:
        if _CURRENCY_RE.fullmatch(self.code) is None:
            raise InvalidMoney("waluta ISO 4217 — CHAR(3)")


def _decimal_amount(amount: object) -> Decimal:
    if isinstance(amount, float) or isinstance(amount, bool):
        raise InvalidMoney("kwota nie może być float")
    if not isinstance(amount, Decimal | str | int):
        raise InvalidMoney("kwota musi być Decimal, str albo int")
    try:
        parsed = amount if isinstance(amount, Decimal) else Decimal(str(amount))
    except InvalidOperation as exc:
        raise InvalidMoney("kwota nie jest liczbą dziesiętną") from exc
    if not parsed.is_finite():
        raise InvalidMoney("kwota musi być skończona")
    exponent = parsed.as_tuple().exponent
    if not isinstance(exponent, int) or exponent < -4:
        raise InvalidMoney("skala kwoty to Numeric(14,4)")
    quantized = parsed.quantize(_FOUR_PLACES)
    if quantized.copy_abs() >= _MAX_ABS:
        raise InvalidMoney("precyzja kwoty to Numeric(14,4)")
    return quantized


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency

    @classmethod
    def of(cls, amount: object, currency: object) -> Money:
        parsed = _decimal_amount(amount)
        if isinstance(currency, Currency):
            bound = currency
        elif isinstance(currency, str):
            bound = Currency(currency)
        else:
            raise InvalidMoney("waluta ISO 4217 — CHAR(3)")
        return cls(amount=parsed, currency=bound)

    def as_pair(self) -> tuple[str, str]:
        return (format(self.amount, "f"), self.currency.code)
