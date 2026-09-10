import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidStop

_KINDS = frozenset(
    {"loading", "unloading", "customs", "ferry", "terminal", "depot", "other"},
)
_STATUSES = frozenset({"pending", "at_stop", "completed", "failed"})
_ZONE = re.compile(r"^[A-Za-z_]+/[A-Za-z0-9_+-]+(?:/[A-Za-z0-9_+-]+)?$")
_GROUP = re.compile(r"^[A-Za-z0-9_-]{2,32}$")
_MAX_REF = 256
_MAX_NOTES = 256
_MAX_PACK = 32
_MAX_SEAL = 32
_FIXTURE = "fixture://stop/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_stop_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidStop("shipment_id musi być UUID")
    return raw


def require_stop_location_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidStop("location_id musi być UUID")
    return raw


def require_stop_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("stop_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidStop("nieznany rodzaj punktu")
    return token


def require_sequence_no(raw: object) -> int:
    if type(raw) is not int or isinstance(raw, bool):
        raise InvalidStop("sequence_no musi być liczbą całkowitą")
    if raw < 1:
        raise InvalidStop("numer punktu musi być dodatni")
    return raw


def require_time_zone(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("time_zone musi być tekstem")
    token = raw.strip()
    if _ZONE.fullmatch(token) is None:
        raise InvalidStop("nieznana strefa czasowa")
    return token


def require_stop_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidStop("nieznany status punktu")
    return token


def require_stop_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStop("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidStop("wskazanie zapisu punktu")
    if len(token) > _MAX_REF:
        raise InvalidStop("wskazanie zapisu punktu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidStop("obce wskazanie zapisu punktu")
    return token


def require_stop_group_code(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidStop("grupa punktów musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if _GROUP.fullmatch(token) is None:
        raise InvalidStop("nieznana grupa punktów")
    return token


def require_notes_for_driver(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidStop("notatka dla kierowcy musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_NOTES:
        raise InvalidStop("notatka dla kierowcy za długa")
    return token


def require_stop_weight_kg(raw: object) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidStop("waga nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidStop("waga musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidStop("waga musi być liczbą dziesiętną") from exc
    if parsed < 0:
        raise InvalidStop("waga nie może być ujemna")
    return parsed.quantize(_FOUR)


def require_stop_quantity(raw: object) -> int | None:
    if raw is None:
        return None
    if type(raw) is str:
        token = raw.strip()
        if token == "":
            return None
        try:
            raw = int(token)
        except ValueError as exc:
            raise InvalidStop("ilość musi być liczbą całkowitą") from exc
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidStop("ilość nie może być float")
    if type(raw) is not int:
        raise InvalidStop("ilość musi być liczbą całkowitą")
    if raw < 0:
        raise InvalidStop("ilość nie może być ujemna")
    return raw


def require_stop_packaging_code(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidStop("opakowanie musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_PACK:
        raise InvalidStop("opakowanie za długie")
    return token


def require_stop_seal_in(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidStop("plomba musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_SEAL:
        raise InvalidStop("plomba za długa")
    return token


def _require_eta_clock(raw: object, label: str) -> datetime:
    if type(raw) is not str:
        raise InvalidStop(f"{label} musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidStop(f"{label}: brak ETA")
    try:
        parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidStop(f"{label}: ISO-8601") from exc
    if parsed.tzinfo is None:
        raise InvalidStop(f"{label}: brak strefy")
    return parsed


def require_eta_physical(raw: object) -> datetime:
    return _require_eta_clock(raw, "fizyczny")


def require_eta_legal(raw: object) -> datetime:
    return _require_eta_clock(raw, "prawny")
