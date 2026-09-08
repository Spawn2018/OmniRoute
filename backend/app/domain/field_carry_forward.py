from uuid import UUID

from app.domain.errors import InvalidFieldCarryForward

_KEYS = frozenset({"incoterm", "trade_side", "named_place"})
_MAX_VALUE = 128


def require_carry_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidFieldCarryForward("quotation_id musi być UUID")
    return raw


def require_carry_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidFieldCarryForward("shipment_id musi być UUID")
    return raw


def require_field_key(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFieldCarryForward("pole musi być tekstem")
    token = raw.strip()
    if token not in _KEYS:
        raise InvalidFieldCarryForward("nieznane pole przeniesienia")
    return token


def require_field_value(key: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFieldCarryForward("wartość pola musi być tekstem")
    token = raw.strip()
    if len(token) > _MAX_VALUE:
        raise InvalidFieldCarryForward("wartość pola za długa")
    if key in {"incoterm", "trade_side"} and token == "":
        raise InvalidFieldCarryForward("pusta wartość pola")
    return token


def require_field_map(raw: object) -> dict[str, str]:
    if type(raw) is not dict:
        raise InvalidFieldCarryForward("mapa pól musi być obiektem")
    if len(raw) == 0:
        raise InvalidFieldCarryForward("brak pól do przeniesienia")
    mapped: dict[str, str] = {}
    for key, value in raw.items():
        token = require_field_key(key)
        mapped[token] = require_field_value(token, value)
    return mapped
