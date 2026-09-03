from uuid import UUID

from app.domain.errors import InvalidOperationalException

_KINDS = frozenset({"noted", "blocked", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://operational-exception/"
_MANUAL = "tenant:manual"


def require_exception_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidOperationalException("shipment_id musi być UUID")
    return raw


def require_exception_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOperationalException("exception_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidOperationalException("nieznany rodzaj wyjątku")
    return token


def require_exception_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOperationalException("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidOperationalException("wskazanie zapisu wyjątku")
    if len(token) > _MAX_REF:
        raise InvalidOperationalException("wskazanie zapisu wyjątku za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidOperationalException("obce wskazanie zapisu wyjątku")
    return token
