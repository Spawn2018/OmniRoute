from uuid import UUID

from app.domain.errors import InvalidShipmentDocument

_KINDS = frozenset({"noted", "attached", "other", "rod"})
_MAX_REF = 256
_FIXTURE = "fixture://shipment-document/"
_MANUAL = "tenant:manual"


def require_document_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipmentDocument("shipment_id musi być UUID")
    return raw


def require_document_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentDocument("document_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidShipmentDocument("nieznany rodzaj dokumentu")
    return token


def require_document_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentDocument("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidShipmentDocument("wskazanie zapisu dokumentu")
    if len(token) > _MAX_REF:
        raise InvalidShipmentDocument("wskazanie zapisu dokumentu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidShipmentDocument("obce wskazanie zapisu dokumentu")
    return token
