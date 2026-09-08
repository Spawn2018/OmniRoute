from datetime import date
from uuid import UUID

from app.domain.errors import InvalidTenderQuote

_MAX_REF = 256
_FIXTURE = "fixture://tender-quote/"
_MANUAL = "tenant:manual"


def require_quote_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderQuote("quotation_id musi być UUID")
    return raw


def require_valid_until(raw: object) -> date:
    if type(raw) is not str:
        raise InvalidTenderQuote("data ważności musi być dniem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderQuote("data ważności musi być dniem")
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidTenderQuote("data ważności musi być dniem ISO") from exc


def require_order_limit(raw: object) -> int:
    if type(raw) is bool or type(raw) is float:
        raise InvalidTenderQuote("limit orderów nie może być float")
    if type(raw) is not int:
        raise InvalidTenderQuote("limit orderów musi być liczbą całkowitą")
    if raw <= 0:
        raise InvalidTenderQuote("limit orderów musi być dodatni")
    return raw


def require_bid_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderQuote("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderQuote("wskazanie zapisu oferty przetargowej")
    if len(token) > _MAX_REF:
        raise InvalidTenderQuote("wskazanie zapisu oferty przetargowej za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderQuote("obce wskazanie zapisu oferty przetargowej")
    return token
