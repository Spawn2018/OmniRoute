import re

from app.domain.errors import InvalidFactoringConnector

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"smeo", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://smeo/"
_MANUAL = "tenant:manual"


def require_connector_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFactoringConnector("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidFactoringConnector("oznaczenie: snake 2–32")
    return token


def require_system_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFactoringConnector("system musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidFactoringConnector("system: allowlista HITL")
    return token


def require_factoring_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFactoringConnector("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidFactoringConnector("obce wskazanie zapisu konektora faktoringu")
    if len(token) > _MAX_REF:
        raise InvalidFactoringConnector("obce wskazanie zapisu konektora faktoringu za długie")
    return token
