import re

from app.domain.errors import InvalidErpConnector

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"optima"})
_MAX_REF = 256
_FIXTURE = "fixture://optima/"
_MANUAL = "tenant:manual"


def require_connector_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidErpConnector("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidErpConnector("oznaczenie: snake 2–32")
    return token


def require_system_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidErpConnector("system musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidErpConnector("system: allowlista HITL")
    return token


def require_erp_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidErpConnector("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidErpConnector("obce wskazanie zapisu konektora Optima")
    if len(token) > _MAX_REF:
        raise InvalidErpConnector("obce wskazanie zapisu konektora Optima za długie")
    return token
