import re

from app.domain.errors import InvalidIdpConnector

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_PROVIDERS = frozenset({"auth0"})
_MAX_REF = 256
_FIXTURE = "fixture://auth0/"
_MANUAL = "tenant:manual"
_HOST = re.compile(
    r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$"
)
_MAX_HOST = 253


def require_connector_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIdpConnector("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidIdpConnector("oznaczenie: snake 2–32")
    return token


def require_provider_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIdpConnector("dostawca musi być tekstem")
    token = raw.strip().lower()
    if token not in _PROVIDERS:
        raise InvalidIdpConnector("dostawca: allowlista HITL")
    return token


def require_public_domain(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidIdpConnector("domena musi być tekstem")
    token = raw.strip().lower()
    if token == "":
        return None
    if "://" in token or "/" in token or " " in token:
        raise InvalidIdpConnector("domena: host bez schematu")
    if len(token) > _MAX_HOST or _HOST.fullmatch(token) is None:
        raise InvalidIdpConnector("domena: host publiczny")
    return token


def require_idp_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIdpConnector("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidIdpConnector("obce wskazanie zapisu konektora IdP")
    if len(token) > _MAX_REF:
        raise InvalidIdpConnector("obce wskazanie zapisu konektora IdP za długie")
    return token
