import re

from app.domain.errors import InvalidExchangeConnector

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"trans_eu", "timocom", "teleroute", "transporeon", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://portal/"
_MANUAL = "tenant:manual"


def require_connector_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidExchangeConnector("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidExchangeConnector("oznaczenie: snake 2–32")
    return token


def require_system_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidExchangeConnector("system musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidExchangeConnector("system: allowlista HITL")
    return token


def require_exchange_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidExchangeConnector("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidExchangeConnector("obce wskazanie zapisu konektora giełdy")
    if len(token) > _MAX_REF:
        raise InvalidExchangeConnector("obce wskazanie zapisu konektora giełdy za długie")
    return token
