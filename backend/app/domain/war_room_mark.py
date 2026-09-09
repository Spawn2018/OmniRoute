from app.domain.errors import InvalidWarRoomMark

_KINDS = (
    "weather",
    "congestion",
    "labor",
    "carrier",
    "credit",
    "other",
)
_FIXTURE = "fixture://war-room-mark/"
_MANUAL = "tenant:manual"


def require_incident_kind(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip().lower()
            if token in _KINDS:
                return token
            raise InvalidWarRoomMark("incydent: allowlista HITL")
        case _:
            raise InvalidWarRoomMark("incydent musi być tekstem")


def require_room_source_ref(raw: object) -> str:
    if not isinstance(raw, str):
        raise InvalidWarRoomMark("source_ref musi być tekstem")
    stamp = raw.strip()
    from_catalog = stamp == _MANUAL or stamp.startswith(_FIXTURE)
    if not from_catalog:
        if stamp == "":
            raise InvalidWarRoomMark("wskazanie zapisu sali kryzysowej")
        raise InvalidWarRoomMark("obce wskazanie zapisu sali kryzysowej")
    if len(stamp) > 256:
        raise InvalidWarRoomMark("wskazanie zapisu sali kryzysowej za długie")
    return stamp
