import re
from datetime import date
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidChannelQuote

_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
_FOUR = Decimal("0.0001")


def normalize_quote_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidChannelQuote("waluta oferty musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidChannelQuote("waluta oferty: ISO 4217, trzy litery")
    return token


def normalize_quote_amount(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidChannelQuote("kwota oferty nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidChannelQuote("kwota oferty musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidChannelQuote("kwota oferty musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidChannelQuote("kwota oferty musi być dodatnia")
    return parsed.quantize(_FOUR)


def normalize_quote_date(raw: object) -> date:
    if type(raw) is date:
        return raw
    raise InvalidChannelQuote("data oferty musi być dniem")


def manual_channel_source_ref(user_id: UUID) -> str:
    return f"tenant:manual:{user_id}"


def normalize_transit_days(raw: object) -> int | None:
    if raw is None:
        return None
    if type(raw) is bool or isinstance(raw, float):
        raise InvalidChannelQuote("czas tranzytu musi być liczbą całkowitą dni")
    if type(raw) is int:
        days = raw
    elif type(raw) is str and raw.strip() == "":
        return None
    elif type(raw) is str and raw.strip().isdigit():
        days = int(raw.strip())
    else:
        raise InvalidChannelQuote("czas tranzytu musi być liczbą całkowitą dni")
    if days < 1:
        raise InvalidChannelQuote("czas tranzytu: co najmniej 1 dzień")
    return days
