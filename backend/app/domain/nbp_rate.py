import re
from datetime import date
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidCurrency, InvalidNbpRate

_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


def normalize_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCurrency("waluta musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidCurrency("waluta: ISO 4217, trzy litery")
    if token == "PLN":
        raise InvalidCurrency("NBP nie kwotuje PLN/PLN")
    return token


def normalize_nbp_mid(raw: object) -> Decimal:
    if isinstance(raw, bool) or not isinstance(raw, int | str | Decimal):
        raise InvalidNbpRate("kurs średni musi być liczbą dziesiętną")
    try:
        mid = Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidNbpRate("kurs średni musi być liczbą dziesiętną") from exc
    if mid <= 0:
        raise InvalidNbpRate("kurs średni musi być dodatni")
    return mid.quantize(Decimal("0.0001"))


def normalize_rate_date(raw: object) -> date:
    if type(raw) is date:
        return raw
    raise InvalidNbpRate("data kursu NBP musi być dniem")
