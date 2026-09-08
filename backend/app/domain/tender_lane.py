from uuid import UUID

from app.domain.errors import InvalidTenderLane, InvalidUnlocode
from app.domain.port import normalize_unlocode

_MAX_REF = 256
_FIXTURE = "fixture://tender-lane/"
_MANUAL = "tenant:manual"


def require_lot_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderLane("tender_lot_id musi być UUID")
    return raw


def require_lane_pair(origin_raw: object, dest_raw: object) -> tuple[str, str]:
    if type(origin_raw) is not str or type(dest_raw) is not str:
        raise InvalidTenderLane("korytarz musi być parą kodów UN/LOCODE")
    try:
        origin = normalize_unlocode(origin_raw)
        dest = normalize_unlocode(dest_raw)
    except InvalidUnlocode as exc:
        raise InvalidTenderLane(f"korytarz: {exc}") from exc
    if origin == dest:
        raise InvalidTenderLane("korytarz nie może mieć tych samych końców")
    return origin, dest


def require_lane_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderLane("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderLane("wskazanie zapisu korytarza przetargu")
    if len(token) > _MAX_REF:
        raise InvalidTenderLane("wskazanie zapisu korytarza przetargu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderLane("obce wskazanie zapisu korytarza przetargu")
    return token
