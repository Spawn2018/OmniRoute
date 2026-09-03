from uuid import UUID

from app.domain.errors import InvalidFraudFlag

_KINDS = frozenset({"billing", "document", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://fraud-flag/"
_MANUAL = "tenant:manual"


def require_flag_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidFraudFlag("party_id musi być UUID")
    return raw


def require_flag_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFraudFlag("flag_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidFraudFlag("nieznany rodzaj flagi oszustwa")
    return token


def require_flag_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFraudFlag("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidFraudFlag("wskazanie zapisu flagi oszustwa")
    if len(token) > _MAX_REF:
        raise InvalidFraudFlag("wskazanie zapisu flagi oszustwa za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidFraudFlag("obce wskazanie zapisu flagi oszustwa")
    return token
