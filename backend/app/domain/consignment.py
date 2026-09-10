import re
from uuid import UUID

from app.domain.errors import InvalidConsignment

_REF = re.compile(r"^[A-Za-z0-9._:-]{2,64}$")
_MAX_SOURCE = 256
_FIXTURE = "fixture://consignment/"
_MANUAL = "tenant:manual"


def require_consignment_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidConsignment("przesyłka musi być tekstem")
    token = raw.strip()
    if _REF.fullmatch(token) is None:
        raise InvalidConsignment("przesyłka: 2–64 litery cyfry . _ : -")
    return token


def require_consignment_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidConsignment("zlecenie musi być UUID")
    return raw


def require_consignment_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidConsignment("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidConsignment("wskazanie zapisu przesyłki")
    if len(token) > _MAX_SOURCE:
        raise InvalidConsignment("wskazanie zapisu przesyłki za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidConsignment("obce wskazanie zapisu przesyłki")
    return token
