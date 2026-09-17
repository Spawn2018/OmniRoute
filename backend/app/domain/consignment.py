import re
from typing import Literal
from uuid import UUID

from app.domain.errors import ConsignmentFtlLimit, InvalidConsignment

_REF = re.compile(r"^[A-Za-z0-9._:-]{2,64}$")
_MAX_SOURCE = 256
_FIXTURE = "fixture://consignment/"
_MANUAL = "tenant:manual"

ConsignmentLoadKind = Literal["ftl", "ltl"]


def require_consignment_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidConsignment("przesyłka musi być tekstem")
    token = raw.strip()
    if _REF.fullmatch(token) is None:
        raise InvalidConsignment("przesyłka: 2–64 litery cyfry . _ : -")
    return token


def require_consignment_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidConsignment("zlecenie musi być UUID")
    return raw


def require_consignment_stop_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidConsignment("punkt musi być UUID")
    return raw


def require_stop_on_consignment_shipment(
    shipment_id: UUID,
    stop_shipment_id: UUID,
) -> None:
    if shipment_id != stop_shipment_id:
        raise InvalidConsignment("punkt spoza trasy zlecenia")


def require_consignment_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidConsignment("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidConsignment("wskazanie zapisu przesyłki")
    if len(token) > _MAX_SOURCE:
        raise InvalidConsignment("wskazanie zapisu przesyłki za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidConsignment("obce wskazanie zapisu przesyłki")
    return token


def parse_optional_load_kind(raw: object | None) -> ConsignmentLoadKind | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidConsignment("tryb załadunku musi być tekstem")
    token = raw.strip().lower()
    if token == "ftl":
        return "ftl"
    if token == "ltl":
        return "ltl"
    raise InvalidConsignment("tryb załadunku: ftl albo ltl")


def require_ftl_room(existing_count: int) -> None:
    if existing_count >= 1:
        raise ConsignmentFtlLimit("FTL dopuszcza tylko jedną przesyłkę na zlecenie")
