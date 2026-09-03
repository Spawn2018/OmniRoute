from datetime import datetime
from uuid import UUID

from app.domain.errors import InvalidTrackingEvent

_KINDS = frozenset({"departed", "arrived", "noted"})
_MAX_REF = 256
_FIXTURE = "fixture://tracking/"
_MANUAL = "tenant:manual"


def require_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTrackingEvent("shipment_id musi być UUID")
    return raw


def require_event_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrackingEvent("event_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidTrackingEvent("nieznany rodzaj zdarzenia")
    return token


def require_occurred_at(raw: object) -> datetime:
    if type(raw) is not datetime:
        raise InvalidTrackingEvent("occurred_at musi być datą")
    if raw.tzinfo is None:
        raise InvalidTrackingEvent("occurred_at wymaga strefy")
    return raw


def require_tracking_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrackingEvent("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTrackingEvent("wskazanie zapisu zdarzenia")
    if len(token) > _MAX_REF:
        raise InvalidTrackingEvent("wskazanie zapisu zdarzenia za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTrackingEvent("obce wskazanie zapisu zdarzenia")
    return token
