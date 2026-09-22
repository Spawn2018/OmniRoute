import re
from uuid import UUID

from app.domain.errors import InvalidShipmentLeg
from app.domain.location import LocationKind

_MAX_REF = 256
_FIXTURE = "fixture://shipment-leg/"
_MANUAL = "tenant:manual"
_ROAD = "road"
_RAIL = "rail"
_CHINA = "china_rail"
_OCEAN = "ocean_lcl"
_AIR = "air"
_KINDS = frozenset({_ROAD, _RAIL, _CHINA, _OCEAN, _AIR})
_CN = "CN"
_LAND = frozenset({LocationKind.POSTAL_ZONE.value, LocationKind.ADDRESS.value})
_RAIL_FLAG = "rail"
_AIR_FLAG = "airport"
_WAYBILL = re.compile(r"^[A-Za-z0-9-]{2,32}$")


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
        raise InvalidShipmentLeg(
            "leg_kind spoza zbioru: road, rail, china_rail, ocean_lcl, air",
        )
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


def require_china_rail_country(code: object) -> None:
    if type(code) is not str:
        raise InvalidShipmentLeg("kod kraju portu musi być tekstem")
    if code != _CN:
        raise InvalidShipmentLeg("port poza Chinami nie jest odcinkiem kolej z Chin")


def require_ocean_seaport(flag: object) -> None:
    if type(flag) is not bool:
        raise InvalidShipmentLeg("is_seaport musi być logiczne")
    if not flag:
        raise InvalidShipmentLeg("port śródlądowy nie jest odcinkiem drobnicy")


def require_air_port_flag(flags: object) -> None:
    if type(flags) is not list:
        raise InvalidShipmentLeg("flagi portu muszą być listą")
    if _AIR_FLAG not in flags:
        raise InvalidShipmentLeg("port bez flagi airport nie jest odcinkiem lotniczym")


def require_air_waybill_no(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidShipmentLeg("numer musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if _WAYBILL.fullmatch(token) is None:
        raise InvalidShipmentLeg("numer listu lotniczego: 2–32 litery cyfry myślnik")
    return token


def require_air_waybill_kind(
    leg_kind: str,
    hawb_no: str | None,
    mawb_no: str | None,
) -> None:
    if hawb_no is None and mawb_no is None:
        return
    if leg_kind != _AIR:
        raise InvalidShipmentLeg("list lotniczy tylko na odcinku air")


def require_waybill_number_prefix(raw: str | None) -> str:
    if raw is None:
        raise InvalidShipmentLeg("prefiks: nadanie numeru wymaga prefiksu w ustawieniach")
    if type(raw) is not str:
        raise InvalidShipmentLeg("prefiks: nadanie numeru wymaga prefiksu w ustawieniach")
    token = raw.strip()
    if token == "":
        raise InvalidShipmentLeg("prefiks: nadanie numeru wymaga prefiksu w ustawieniach")
    return token


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
