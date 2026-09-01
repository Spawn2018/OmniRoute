import re
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidPortSurcharge

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
_TITLE_MAX = 128
_WHEN_MAX = 512
_FOUR = Decimal("0.0001")


def normalize_surcharge_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPortSurcharge("kod extra musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidPortSurcharge("kod extra: snake 2–32")
    return token


def normalize_surcharge_title(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPortSurcharge("tytuł extra musi być tekstem")
    title = " ".join(raw.split())
    if title == "":
        raise InvalidPortSurcharge("tytuł extra jest wymagany")
    if len(title) > _TITLE_MAX:
        raise InvalidPortSurcharge("tytuł extra za długi")
    return title


def normalize_applies_when(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPortSurcharge("warunek extra musi być tekstem")
    note = raw.strip()
    if note == "":
        raise InvalidPortSurcharge("warunek extra jest wymagany")
    if len(note) > _WHEN_MAX:
        raise InvalidPortSurcharge("warunek extra za długi")
    return note


def normalize_surcharge_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPortSurcharge("waluta extra musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidPortSurcharge("waluta extra: ISO 4217, trzy litery")
    return token


def normalize_surcharge_amount(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidPortSurcharge("kwota extra nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidPortSurcharge("kwota extra musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidPortSurcharge("kwota extra musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidPortSurcharge("kwota extra musi być dodatnia")
    return parsed.quantize(_FOUR)
