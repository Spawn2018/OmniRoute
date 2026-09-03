from uuid import UUID

from app.domain.errors import InvalidSalesInvoice

_KINDS = frozenset({"issued", "noted", "other"})
_MAX_REF = 256
_MAX_INVOICE_REF = 64
_FIXTURE = "fixture://sales-invoice/"
_MANUAL = "tenant:manual"


def require_invoice_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidSalesInvoice("shipment_id musi być UUID")
    return raw


def require_invoice_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSalesInvoice("invoice_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidSalesInvoice("nieznany rodzaj faktury")
    return token


def require_invoice_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSalesInvoice("numer faktury musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidSalesInvoice("numer faktury")
    if len(token) > _MAX_INVOICE_REF:
        raise InvalidSalesInvoice("numer faktury za długi")
    return token


def require_invoice_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSalesInvoice("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidSalesInvoice("wskazanie zapisu faktury")
    if len(token) > _MAX_REF:
        raise InvalidSalesInvoice("wskazanie zapisu faktury za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidSalesInvoice("obce wskazanie zapisu faktury")
    return token
