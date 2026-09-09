import re
from uuid import UUID

from app.domain.errors import InvalidCashDiscount

_KIND = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://cash-discount/"
_MANUAL = "tenant:manual"


def require_invoice_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCashDiscount("sales_invoice_id musi być UUID")
    return raw


def require_discount_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCashDiscount("skonto musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _KIND.fullmatch(token) is None:
        raise InvalidCashDiscount("skonto: snake 2–32")
    return token


def require_cash_discount_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCashDiscount("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCashDiscount("wskazanie zapisu skonta")
    if len(token) > _MAX_REF:
        raise InvalidCashDiscount("wskazanie zapisu skonta za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCashDiscount("obce wskazanie zapisu skonta")
    return token
