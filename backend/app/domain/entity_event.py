from uuid import UUID

from app.domain.errors import InvalidEntityEvent
from app.domain.rate_line import require_source_ref

_EVENT_KINDS = frozenset({"inquiry_queued", "inquiry_sent", "quote_recorded"})
_SUBJECT_KINDS = frozenset({"carrier_inquiry", "quotation", "channel_quote"})


def require_entity_event_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidEntityEvent("event_kind musi być tekstem")
    token = raw.strip()
    if token not in _EVENT_KINDS:
        raise InvalidEntityEvent("event_kind spoza allowlisty B0a")
    return token


def require_entity_subject_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidEntityEvent("subject_kind musi być tekstem")
    token = raw.strip()
    if token not in _SUBJECT_KINDS:
        raise InvalidEntityEvent("subject_kind spoza allowlisty B0a")
    return token


def require_entity_subject_id(raw: object) -> UUID:
    if isinstance(raw, UUID):
        return raw
    if type(raw) is not str:
        raise InvalidEntityEvent("subject_id musi być UUID")
    try:
        return UUID(raw.strip())
    except ValueError as exc:
        raise InvalidEntityEvent("subject_id musi być UUID") from exc


def require_entity_source_ref(raw: object) -> str:
    return require_source_ref(raw)
