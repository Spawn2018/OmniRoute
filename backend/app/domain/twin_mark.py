import re

from app.domain.errors import InvalidTwinMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_FIXTURE = "fixture://twin-mark/"
_MANUAL = "tenant:manual"


def require_twin_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTwinMark("postać musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTwinMark("rodzaj: snake 2–32")
    return token


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
