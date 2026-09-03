from uuid import UUID

from app.domain.errors import InvalidOutboxEvent
from app.domain.rate_line import require_source_ref

_PENDING = "pending"
_SAVED = "inbound_message_saved"
_SOURCE_PREFIX = "outbox://"


def outbox_pending_status() -> str:
    return _PENDING


def inbound_message_saved_kind() -> str:
    return _SAVED


def require_outbox_source_ref(raw: object) -> str:
    origin = require_source_ref(raw)
    if not origin.startswith(_SOURCE_PREFIX):
        raise InvalidOutboxEvent("source_ref: tylko outbox://")
    return origin


def require_outbox_event_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOutboxEvent("event_kind musi być tekstem")
    token = raw.strip()
    if token != _SAVED:
        raise InvalidOutboxEvent("event_kind: tylko inbound_message_saved")
    return token


def require_outbox_subject_id(raw: object) -> UUID:
    if isinstance(raw, UUID):
        return raw
    if type(raw) is not str:
        raise InvalidOutboxEvent("subject_id musi być UUID")
    token = raw.strip()
    try:
        return UUID(token)
    except ValueError as exc:
        raise InvalidOutboxEvent("subject_id musi być UUID") from exc
