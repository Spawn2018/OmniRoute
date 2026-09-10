import re
from datetime import datetime
from uuid import UUID

from app.domain.errors import InvalidPlanSnapshot

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://plan-snapshot/"
_MANUAL = "tenant:manual"
_AUTHOR_MAX = 64


def require_snapshot_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPlanSnapshot("migawka musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidPlanSnapshot("migawka: snake 2–32")
    return token


def _as_uuid(raw: object, token: str) -> UUID:
    if isinstance(raw, UUID):
        return raw
    if type(raw) is not str:
        raise InvalidPlanSnapshot(token)
    try:
        return UUID(raw.strip())
    except ValueError as exc:
        raise InvalidPlanSnapshot(token) from exc


def require_shipment_id(raw: object) -> UUID:
    return _as_uuid(raw, "zlecenie")


def require_trip_id(raw: object) -> UUID:
    return _as_uuid(raw, "przejazd")


def require_resource_id(raw: object) -> UUID:
    return _as_uuid(raw, "zasob")


def require_author_label(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPlanSnapshot("autor musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) > _AUTHOR_MAX:
        raise InvalidPlanSnapshot("autor: 1–64 znaki")
    return token


def require_recorded_at(raw: object) -> datetime:
    if type(raw) is not str:
        raise InvalidPlanSnapshot("czas musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidPlanSnapshot("czas: brak wartości")
    try:
        parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidPlanSnapshot("czas: ISO-8601") from exc
    if parsed.tzinfo is None:
        raise InvalidPlanSnapshot("czas: brak strefy")
    return parsed


def require_snapshot_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPlanSnapshot("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidPlanSnapshot("obce wskazanie zapisu migawki")
    if len(token) > _MAX_REF:
        raise InvalidPlanSnapshot("obce wskazanie zapisu migawki za długie")
    return token
