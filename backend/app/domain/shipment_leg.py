from uuid import UUID

from app.domain.errors import InvalidShipmentLeg
from app.domain.location import LocationKind

_MAX_REF = 256
_FIXTURE = "fixture://shipment-leg/"
_MANUAL = "tenant:manual"
_ROAD = "road"
_RAIL = "rail"
_KINDS = frozenset({_ROAD, _RAIL})
_LAND = frozenset({LocationKind.POSTAL_ZONE.value, LocationKind.ADDRESS.value})
_RAIL_FLAG = "rail"


def require_leg_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipmentLeg("shipment_id musi być UUID")
    return raw


def require_leg_location_id(raw: object, *, field: str) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipmentLeg(f"{field} musi być UUID")
    return raw


def require_distinct_ends(origin_id: UUID, destination_id: UUID) -> None:
    if origin_id == destination_id:
        raise InvalidShipmentLeg("początek i koniec odcinka muszą być różne")


def require_road_location_kind(kind: object) -> str:
    if type(kind) is not str:
        raise InvalidShipmentLeg("rodzaj lokalizacji musi być tekstem")
    if kind == LocationKind.UNLOCODE.value:
        raise InvalidShipmentLeg("port UN/LOCODE nie jest odcinkiem drogowym")
    if kind not in _LAND:
        raise InvalidShipmentLeg("lokalizacja odcinka musi być strefą albo adresem")
    return kind


def require_leg_kind(raw: object) -> str:
    if raw is None:
        return _ROAD
    if type(raw) is not str:
        raise InvalidShipmentLeg("leg_kind musi być tekstem")
    token = raw.strip()
    if token == "":
        return _ROAD
    if token not in _KINDS:
        raise InvalidShipmentLeg("leg_kind spoza zbioru: road, rail")
    return token


def require_road_leg_kind() -> str:
    return _ROAD


def require_rail_location_kind(kind: object) -> str:
    if type(kind) is not str:
        raise InvalidShipmentLeg("rodzaj lokalizacji musi być tekstem")
    if kind != LocationKind.UNLOCODE.value:
        raise InvalidShipmentLeg("odcinek kolejowy wymaga lokalizacji UN/LOCODE")
    return kind


def require_rail_port_flag(flags: object) -> None:
    if type(flags) is not list:
        raise InvalidShipmentLeg("flagi portu muszą być listą")
    if _RAIL_FLAG not in flags:
        raise InvalidShipmentLeg("port bez flagi rail nie jest odcinkiem kolejowym")


def require_leg_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentLeg("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidShipmentLeg("wskazanie zapisu odcinka")
    if len(token) > _MAX_REF:
        raise InvalidShipmentLeg("wskazanie zapisu odcinka za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidShipmentLeg("obce wskazanie zapisu odcinka")
    return token
