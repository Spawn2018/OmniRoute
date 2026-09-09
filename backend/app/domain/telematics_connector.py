from app.domain.errors import InvalidTelematicsConnector

_KINDS = frozenset({"omni_telematic", "external_api"})
_PROVIDERS = frozenset({"gbox", "ikol", "flotis", "wialon", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://telematics-connector/"
_MANUAL = "tenant:manual"


def require_observation_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTelematicsConnector("reżim musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidTelematicsConnector("reżim: allowlista HITL")
    return token


def require_provider_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTelematicsConnector("dostawca musi być tekstem")
    token = raw.strip().lower()
    if token not in _PROVIDERS:
        raise InvalidTelematicsConnector("dostawca: allowlista HITL")
    return token


def require_connector_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTelematicsConnector("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTelematicsConnector("wskazanie zapisu konektora GPS")
    if len(token) > _MAX_REF:
        raise InvalidTelematicsConnector("wskazanie zapisu konektora GPS za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTelematicsConnector("obce wskazanie zapisu konektora GPS")
    return token
