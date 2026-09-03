from uuid import UUID

from app.domain.errors import InvalidCollectiveInvoice

_MAX_REF = 256
_FIXTURE = "fixture://collective-invoice/"
_MANUAL = "tenant:manual"


def require_collective_invoice_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCollectiveInvoice("sales_invoice_id musi być UUID")
    return raw


def require_collective_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCollectiveInvoice("shipment_id musi być UUID")
    return raw


def require_collective_extra_shipment(anchor_id: UUID, extra_id: UUID) -> UUID:
    if extra_id == anchor_id:
        raise InvalidCollectiveInvoice("to zlecenie już jest kotwicą faktury")
    return extra_id


def require_collective_same_party(anchor_party_id: UUID, extra_party_id: UUID) -> None:
    if extra_party_id != anchor_party_id:
        raise InvalidCollectiveInvoice("dodatkowe zlecenie innego kontrahenta")


def require_collective_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCollectiveInvoice("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCollectiveInvoice("wskazanie zapisu zbiorczej")
    if len(token) > _MAX_REF:
        raise InvalidCollectiveInvoice("wskazanie zapisu zbiorczej za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCollectiveInvoice("obce wskazanie zapisu zbiorczej")
    return token
