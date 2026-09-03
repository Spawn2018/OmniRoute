from uuid import UUID

from app.domain.errors import InvalidBookkeeping

_MAX_REF = 256
_FIXTURE = "fixture://bookkeeping/"
_MANUAL = "tenant:manual"


def require_bookkeeping_charge_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidBookkeeping("charge_id musi być UUID")
    return raw


def require_bookkeeping_invoice_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidBookkeeping("sales_invoice_id musi być UUID")
    return raw


def require_bookkeeping_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBookkeeping("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidBookkeeping("wskazanie zapisu dekretu")
    if len(token) > _MAX_REF:
        raise InvalidBookkeeping("wskazanie zapisu dekretu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidBookkeeping("obce wskazanie zapisu dekretu")
    return token
