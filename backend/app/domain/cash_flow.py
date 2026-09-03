from uuid import UUID

from app.domain.errors import InvalidCashFlow

_MAX_REF = 256
_FIXTURE = "fixture://cash-flow/"
_MANUAL = "tenant:manual"


def require_cash_flow_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCashFlow("quotation_id musi być UUID")
    return raw


def require_cash_flow_payment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCashFlow("bank_payment_id musi być UUID")
    return raw


def require_cash_flow_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCashFlow("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCashFlow("wskazanie zapisu przepływu")
    if len(token) > _MAX_REF:
        raise InvalidCashFlow("wskazanie zapisu przepływu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCashFlow("obce wskazanie zapisu przepływu")
    return token
