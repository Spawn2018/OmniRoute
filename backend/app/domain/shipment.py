import re
from uuid import UUID

from app.domain.errors import InvalidShipment

_DRAFT = "draft"
_MAX_REF = 256
_FIXTURE = "fixture://shipment/"
_MANUAL = "tenant:manual"
_FIXTURE_NUM = "fixture://shipment-ref/"
_OMNI_NUM = "omni://shipment/"
_OMNI_TAIL = re.compile(r"^[a-z0-9][a-z0-9._-]{1,62}$")


def shipment_draft_status() -> str:
    return _DRAFT


def require_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipment("quotation_id musi być UUID")
    return raw


def require_party_on_quotation(raw: UUID | None) -> UUID:
    if raw is None:
        raise InvalidShipment("wycena bez kontrahenta")
    return raw


def require_shipment_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipment("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidShipment("wskazanie zapisu zlecenia")
    if len(token) > _MAX_REF:
        raise InvalidShipment("wskazanie zapisu zlecenia za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidShipment("obce wskazanie zapisu zlecenia")
    return token


def require_shipment_ref(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidShipment("numer musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_REF:
        raise InvalidShipment("numer zlecenia za długi")
    if token.startswith(_FIXTURE_NUM):
        rest = token.removeprefix(_FIXTURE_NUM)
        if rest == "":
            raise InvalidShipment("numer: allowlista HITL")
        return token
    if token.startswith(_OMNI_NUM):
        rest = token.removeprefix(_OMNI_NUM)
        if _OMNI_TAIL.fullmatch(rest) is None:
            raise InvalidShipment("numer: allowlista HITL")
        return token
    raise InvalidShipment("obce wskazanie numeru zlecenia")
