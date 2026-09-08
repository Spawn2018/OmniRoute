import re
from uuid import UUID

from app.domain.errors import InvalidStop

_KINDS = frozenset(
    {"loading", "unloading", "customs", "ferry", "terminal", "depot", "other"},
)
_STATUSES = frozenset({"pending", "at_stop", "completed", "failed"})
_ZONE = re.compile(r"^[A-Za-z_]+/[A-Za-z0-9_+-]+(?:/[A-Za-z0-9_+-]+)?$")
_MAX_REF = 256
_FIXTURE = "fixture://stop/"
_MANUAL = "tenant:manual"


def require_stop_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidStop("shipment_id musi być UUID")
    return raw


def require_stop_location_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidStop("location_id musi być UUID")
    return raw


def require_stop_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("stop_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidStop("nieznany rodzaj punktu")
    return token


def require_sequence_no(raw: object) -> int:
    if type(raw) is not int or isinstance(raw, bool):
        raise InvalidStop("sequence_no musi być liczbą całkowitą")
    if raw < 1:
        raise InvalidStop("numer punktu musi być dodatni")
    return raw


def require_time_zone(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("time_zone musi być tekstem")
    token = raw.strip()
    if _ZONE.fullmatch(token) is None:
        raise InvalidStop("nieznana strefa czasowa")
    return token


def require_stop_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidStop("nieznany status punktu")
    return token


def require_stop_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidStop("wskazanie zapisu punktu")
    if len(token) > _MAX_REF:
        raise InvalidStop("wskazanie zapisu punktu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidStop("obce wskazanie zapisu punktu")
    return token
