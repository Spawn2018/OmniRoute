import re

from app.domain.errors import InvalidSapConnector

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"sap", "oracle"})
_MAX_REF = 256
_FIXTURE = "fixture://sap-connector/"
_MANUAL = "tenant:manual"


def require_connector_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSapConnector("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidSapConnector("oznaczenie: snake 2–32")
    return token


def require_system_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSapConnector("system musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidSapConnector("system: allowlista HITL")
    return token


def require_sap_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSapConnector("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidSapConnector("obce wskazanie zapisu konektora SAP/Oracle")
    if len(token) > _MAX_REF:
        raise InvalidSapConnector("obce wskazanie zapisu konektora SAP/Oracle za długie")
    return token
