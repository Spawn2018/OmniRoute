from app.domain.errors import InvalidTwinMark

_KINDS = (
    "vehicle",
    "driver",
    "container",
    "shipment",
    "network",
    "plan",
    "office",
    "cargo",
)
_FIXTURE = "fixture://twin-mark/"
_MANUAL = "tenant:manual"


def require_twin_kind(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip().lower()
            if token in _KINDS:
                return token
            raise InvalidTwinMark("postać: allowlista HITL")
        case _:
            raise InvalidTwinMark("postać musi być tekstem")


def require_twin_source_ref(raw: object) -> str:
    if not isinstance(raw, str):
        raise InvalidTwinMark("source_ref musi być tekstem")
    stamp = raw.strip()
    from_catalog = stamp == _MANUAL or stamp.startswith(_FIXTURE)
    if not from_catalog:
        if stamp == "":
            raise InvalidTwinMark("wskazanie zapisu bliźniaka")
        raise InvalidTwinMark("obce wskazanie zapisu bliźniaka")
    if len(stamp) > 256:
        raise InvalidTwinMark("wskazanie zapisu bliźniaka za długie")
    return stamp
