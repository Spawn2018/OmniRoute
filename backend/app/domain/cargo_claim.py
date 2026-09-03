from uuid import UUID

from app.domain.errors import InvalidCargoClaim

_KINDS = frozenset({"damage", "shortage", "other"})
_MAX_REF = 256
_FIXTURE = "fixture://cargo-claim/"
_MANUAL = "tenant:manual"


def require_claim_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCargoClaim("shipment_id musi być UUID")
    return raw


def require_claim_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCargoClaim("claim_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidCargoClaim("nieznany rodzaj reklamacji")
    return token


def require_claim_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCargoClaim("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCargoClaim("wskazanie zapisu reklamacji")
    if len(token) > _MAX_REF:
        raise InvalidCargoClaim("wskazanie zapisu reklamacji za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCargoClaim("obce wskazanie zapisu reklamacji")
    return token
