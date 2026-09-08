from uuid import UUID

from app.domain.errors import InvalidTrip

_STATUSES = frozenset({"draft", "planned", "in_transit", "completed", "cancelled"})
_SLOTS = frozenset({"vehicle", "trailer", "driver"})
_MAX_NO = 64
_MAX_REF = 256
_FIXTURE = "fixture://trip/"
_MANUAL = "tenant:manual"


def require_trip_no(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("trip_no musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTrip("numer przejazdu")
    if len(token) > _MAX_NO:
        raise InvalidTrip("numer przejazdu za długi")
    return token


def require_trip_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidTrip("nieznany status przejazdu")
    return token


def require_trip_resource_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidTrip("wskazanie zasobu musi być UUID")
    return raw


def require_trip_slot(slot: object, resource_kind: object) -> None:
    if type(slot) is not str or slot not in _SLOTS:
        raise InvalidTrip("nieznany slot floty")
    if type(resource_kind) is not str or resource_kind != slot:
        raise InvalidTrip("rodzaj zasobu nie pasuje")


def require_trip_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTrip("wskazanie zapisu przejazdu")
    if len(token) > _MAX_REF:
        raise InvalidTrip("wskazanie zapisu przejazdu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTrip("obce wskazanie zapisu przejazdu")
    return token
