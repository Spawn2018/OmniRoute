from datetime import date
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidFuelIndex

_KINDS = frozenset({"fsc", "baf", "caf"})
_MAX_REF = 256
_FIXTURE = "fixture://fuel-index/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_index_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFuelIndex("rodzaj indeksu musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidFuelIndex("nieznany rodzaj indeksu")
    return token


def require_published_on(raw: object) -> date:
    if type(raw) is not str:
        raise InvalidFuelIndex("data indeksu musi być dniem")
    token = raw.strip()
    if token == "":
        raise InvalidFuelIndex("data indeksu musi być dniem")
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidFuelIndex("data indeksu musi być dniem ISO") from exc


def require_index_value(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidFuelIndex("indeks nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidFuelIndex("indeks musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidFuelIndex("indeks musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidFuelIndex("indeks musi być dodatni")
    return parsed.quantize(_FOUR)


def require_index_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFuelIndex("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidFuelIndex("wskazanie zapisu indeksu paliwowego")
    if len(token) > _MAX_REF:
        raise InvalidFuelIndex("wskazanie zapisu indeksu paliwowego za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidFuelIndex("obce wskazanie zapisu indeksu paliwowego")
    return token
