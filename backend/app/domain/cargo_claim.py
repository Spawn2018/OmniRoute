from datetime import date
from uuid import UUID

from app.domain.errors import InvalidCargoClaim

_KINDS = frozenset({"damage", "shortage", "other"})
_OSD = frozenset({"overage", "shortage", "damage", "loss"})
_WINDOWS = frozenset({"notice_7", "notice_21"})
_MAX_REF = 256
_FIXTURE = "fixture://cargo-claim/"
_MANUAL = "tenant:manual"


def require_claim_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCargoClaim("shipment_id musi być UUID")
    return raw


def require_claim_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCargoClaim("claim_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidCargoClaim("nieznany rodzaj reklamacji")
    return token


def require_claim_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCargoClaim("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCargoClaim("wskazanie zapisu reklamacji")
    if len(token) > _MAX_REF:
        raise InvalidCargoClaim("wskazanie zapisu reklamacji za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCargoClaim("obce wskazanie zapisu reklamacji")
    return token


def require_damage_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCargoClaim("osd musi być tekstem")
    token = raw.strip()
    if token not in _OSD:
        raise InvalidCargoClaim("nieznany kod osd")
    return token


def require_cmr_notice_window(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCargoClaim("okno musi być tekstem")
    token = raw.strip()
    if token not in _WINDOWS:
        raise InvalidCargoClaim("nieznane okno CMR")
    return token


def require_notice_due_at(raw: object) -> date:
    if type(raw) is not str:
        raise InvalidCargoClaim("zawiadomienie musi być dniem")
    token = raw.strip()
    if token == "":
        raise InvalidCargoClaim("zawiadomienie musi być dniem")
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidCargoClaim("zawiadomienie musi być dniem ISO") from exc


def require_suit_due_at(raw: object) -> date:
    if type(raw) is not str:
        raise InvalidCargoClaim("pozew musi być dniem")
    token = raw.strip()
    if token == "":
        raise InvalidCargoClaim("pozew musi być dniem")
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidCargoClaim("pozew musi być dniem ISO") from exc


def require_cmr_order(notice: date, suit: date) -> None:
    if suit < notice:
        raise InvalidCargoClaim("kolejność terminów CMR")
