import re
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidRateCard

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
_MAX_WHEN = 512
_MAX_REF = 256
_FIXTURE = "fixture://rate-card/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_card_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidRateCard("kod karty musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidRateCard("kod karty: snake 2–32")
    return token


def require_applies_when(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidRateCard("warunek karty musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) > _MAX_WHEN:
        raise InvalidRateCard("warunek karty: 1–512 znaków")
    return token


def require_card_amount(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidRateCard("kwota nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidRateCard("kwota musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidRateCard("kwota musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidRateCard("kwota musi być dodatnia")
    return parsed.quantize(_FOUR)


def require_card_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidRateCard("waluta karty musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidRateCard("waluta karty: ISO 4217, trzy litery")
    return token


def require_card_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidRateCard("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidRateCard("wskazanie zapisu karty stawek")
    if len(token) > _MAX_REF:
        raise InvalidRateCard("wskazanie zapisu karty stawek za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidRateCard("obce wskazanie zapisu karty stawek")
    return token
