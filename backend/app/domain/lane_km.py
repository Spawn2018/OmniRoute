import re
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidLaneKm

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://lane-km/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_km_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidLaneKm("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidLaneKm("oznaczenie: snake 2–32")
    return token


def require_lane_km(raw: object, token: str) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidLaneKm(f"{token} nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidLaneKm(f"{token} musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidLaneKm(f"{token} musi być liczbą dziesiętną") from exc
    if parsed < 0:
        raise InvalidLaneKm(f"{token} nie może być ujemne")
    return parsed.quantize(_FOUR)


def require_lane_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidLaneKm("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidLaneKm("obce wskazanie zapisu km korytarza")
    if len(token) > _MAX_REF:
        raise InvalidLaneKm("obce wskazanie zapisu km korytarza za długie")
    return token
