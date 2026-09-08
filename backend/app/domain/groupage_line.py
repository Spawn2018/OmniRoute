import re
from datetime import datetime, time
from uuid import UUID

from app.domain.errors import InvalidGroupageLine
from app.domain.location import LocationKind

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://groupage-line/"
_MANUAL = "tenant:manual"
_LAND = frozenset({LocationKind.POSTAL_ZONE.value, LocationKind.ADDRESS.value})
_ISODOW = frozenset(range(1, 8))
_TIME_FORMATS = ("%H:%M:%S", "%H:%M")


def require_line_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGroupageLine("line_code musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidGroupageLine("kod linii: snake 2–32")
    return token


def require_line_location_id(raw: object, *, field: str) -> UUID:
    if type(raw) is not UUID:
        raise InvalidGroupageLine(f"{field} musi być UUID")
    return raw


def require_distinct_line_ends(origin_id: UUID, destination_id: UUID) -> None:
    if origin_id == destination_id:
        raise InvalidGroupageLine("początek i koniec linii muszą być różne")


def require_line_location_kind(kind: object) -> str:
    if type(kind) is not str:
        raise InvalidGroupageLine("rodzaj lokalizacji musi być tekstem")
    if kind == LocationKind.UNLOCODE.value:
        raise InvalidGroupageLine("port UN/LOCODE nie jest końcem linii drobnicy")
    if kind not in _LAND:
        raise InvalidGroupageLine("koniec linii musi być strefą albo adresem")
    return kind


def require_cutoff_local(raw: object) -> time:
    if type(raw) is bool or isinstance(raw, float):
        raise InvalidGroupageLine("cutoff_local nie może być float")
    if type(raw) is time:
        return time(raw.hour, raw.minute, raw.second)
    if type(raw) is str:
        token = raw.strip()
        for fmt in _TIME_FORMATS:
            try:
                parsed = datetime.strptime(token, fmt).time()
            except ValueError:
                continue
            return parsed
    raise InvalidGroupageLine("cutoff_local musi być godziną lokalną")


def require_line_transit_days(raw: object) -> int:
    if type(raw) is bool or isinstance(raw, float):
        raise InvalidGroupageLine("transit_days musi być liczbą całkowitą dni")
    if type(raw) is int:
        days = raw
    elif type(raw) is str and raw.strip().isdigit():
        days = int(raw.strip())
    else:
        raise InvalidGroupageLine("transit_days musi być liczbą całkowitą dni")
    if days < 1:
        raise InvalidGroupageLine("transit_days: co najmniej 1 dzień")
    return days


def require_operating_dows(raw: object) -> list[int]:
    if type(raw) is not list:
        raise InvalidGroupageLine("operating_dows musi być listą ISODOW")
    if raw == []:
        raise InvalidGroupageLine("operating_dows nie może być puste")
    unique: list[int] = []
    for item in raw:
        if type(item) is not int:
            raise InvalidGroupageLine("operating_dows: ISODOW 1–7")
        if item not in _ISODOW:
            raise InvalidGroupageLine("operating_dows: ISODOW 1–7")
        if item not in unique:
            unique.append(item)
    return sorted(unique)


def require_line_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGroupageLine("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidGroupageLine("wskazanie zapisu linii")
    if len(token) > _MAX_REF:
        raise InvalidGroupageLine("wskazanie zapisu linii za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidGroupageLine("obce wskazanie zapisu linii")
    return token
