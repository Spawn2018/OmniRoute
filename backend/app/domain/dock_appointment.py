import re
from datetime import date, datetime, time
from uuid import UUID

from app.domain.errors import InvalidDockAppointment
from app.domain.location import LocationKind

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_STATUSES = frozenset({"noted", "advised", "at_dock", "released"})
_MAX_REF = 256
_FIXTURE = "fixture://dock-appointment/"
_MANUAL = "tenant:manual"
_WAREHOUSE = frozenset({LocationKind.POSTAL_ZONE.value, LocationKind.ADDRESS.value})
_TIME_FORMATS = ("%H:%M:%S", "%H:%M")
_DATE_FORMATS = ("%Y-%m-%d",)


def require_appointment_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDockAppointment("appointment_code musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidDockAppointment("kod awizacji: snake 2–32")
    return token


def require_appointment_uuid(raw: object, *, field: str) -> UUID:
    if type(raw) is not UUID:
        raise InvalidDockAppointment(f"{field} musi być UUID")
    return raw


def require_appointment_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDockAppointment("appointment_status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidDockAppointment("nieznany status awizacji")
    return token


def require_warehouse_location_kind(kind: object) -> str:
    if type(kind) is not str:
        raise InvalidDockAppointment("rodzaj lokalizacji musi być tekstem")
    if kind == LocationKind.UNLOCODE.value:
        raise InvalidDockAppointment("port UN/LOCODE nie jest magazynem spedycyjnym")
    if kind not in _WAREHOUSE:
        raise InvalidDockAppointment("magazyn musi być strefą albo adresem")
    return kind


def require_stop_on_shipment(shipment_id: UUID, stop_shipment_id: UUID) -> None:
    if shipment_id != stop_shipment_id:
        raise InvalidDockAppointment("stop spoza trasy zlecenia")


def _clock(raw: object, *, field: str) -> time:
    if type(raw) is bool or isinstance(raw, float):
        raise InvalidDockAppointment(f"{field} nie może być float")
    if type(raw) is time:
        return time(raw.hour, raw.minute, raw.second)
    if type(raw) is str:
        token = raw.strip()
        for fmt in _TIME_FORMATS:
            try:
                return datetime.strptime(token, fmt).time()
            except ValueError:
                continue
    raise InvalidDockAppointment(f"{field} musi być godziną lokalną")


def require_dock_window(start: object, end: object) -> tuple[time, time]:
    open_at = _clock(start, field="window_start_local")
    close_at = _clock(end, field="window_end_local")
    if close_at <= open_at:
        raise InvalidDockAppointment("okno doku: koniec po starcie")
    return open_at, close_at


def require_window_date(raw: object) -> date:
    if type(raw) is date and type(raw) is not datetime:
        return raw
    if type(raw) is str:
        token = raw.strip()
        for fmt in _DATE_FORMATS:
            try:
                return datetime.strptime(token, fmt).date()
            except ValueError:
                continue
    raise InvalidDockAppointment("window_date musi być dniem kalendarzowym")


def require_dock_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDockAppointment("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidDockAppointment("wskazanie zapisu awizacji")
    if len(token) > _MAX_REF:
        raise InvalidDockAppointment("wskazanie zapisu awizacji za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidDockAppointment("obce wskazanie zapisu awizacji")
    return token
