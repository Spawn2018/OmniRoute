from uuid import UUID

from app.domain.errors import InvalidShipmentStakeholder

_ROLES = frozenset(
    {
        "shipper",
        "consignee",
        "origin_agent",
        "dest_agent",
        "ocean_carrier",
        "omni_customs",
        "client_customs",
    },
)
_MAX_REF = 256
_FIXTURE = "fixture://shipment-stakeholder/"
_MANUAL = "tenant:manual"


def require_stakeholder_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipmentStakeholder("shipment_id musi być UUID")
    return raw


def require_stakeholder_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipmentStakeholder("party_id musi być UUID")
    return raw


def require_stakeholder_role(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentStakeholder("rola musi być tekstem")
    token = raw.strip()
    if token not in _ROLES:
        raise InvalidShipmentStakeholder("nieznana rola strony zlecenia")
    return token


def require_stakeholder_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentStakeholder("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidShipmentStakeholder("wskazanie zapisu strony zlecenia")
    if len(token) > _MAX_REF:
        raise InvalidShipmentStakeholder("wskazanie zapisu strony zlecenia za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidShipmentStakeholder("obce wskazanie zapisu strony zlecenia")
    return token
