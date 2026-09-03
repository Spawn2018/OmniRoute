from uuid import UUID

from app.domain.errors import InvalidQuoteInvoiceSettlement

_MAX_REF = 256
_FIXTURE = "fixture://quote-invoice-settlement/"
_MANUAL = "tenant:manual"


def require_settlement_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidQuoteInvoiceSettlement("quotation_id musi być UUID")
    return raw


def require_settlement_invoice_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidQuoteInvoiceSettlement("sales_invoice_id musi być UUID")
    return raw


def require_settlement_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidQuoteInvoiceSettlement("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidQuoteInvoiceSettlement("wskazanie zapisu rozliczenia")
    if len(token) > _MAX_REF:
        raise InvalidQuoteInvoiceSettlement("wskazanie zapisu rozliczenia za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidQuoteInvoiceSettlement("obce wskazanie zapisu rozliczenia")
    return token
