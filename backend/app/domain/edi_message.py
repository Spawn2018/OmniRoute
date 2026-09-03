from uuid import UUID

from app.domain.errors import InvalidEdiMessage

_KINDS = frozenset({"noted", "outbound", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://edi-message/"
_MANUAL = "tenant:manual"


def require_edi_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidEdiMessage("shipment_id musi być UUID")
    return raw


def require_edi_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidEdiMessage("message_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidEdiMessage("nieznany rodzaj komunikatu")
    return token


def require_edi_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidEdiMessage("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidEdiMessage("wskazanie zapisu komunikatu")
    if len(token) > _MAX_REF:
        raise InvalidEdiMessage("wskazanie zapisu komunikatu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidEdiMessage("obce wskazanie zapisu komunikatu")
    return token
