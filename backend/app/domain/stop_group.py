import re
from uuid import UUID

from app.domain.errors import InvalidStopGroup

_GROUP = re.compile(r"^[A-Za-z0-9_-]{2,32}$")
_MAX_SOURCE = 256
_FIXTURE = "fixture://stop-group/"
_MANUAL = "tenant:manual"


def require_stop_group_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStopGroup("grupa musi być tekstem")
    token = raw.strip()
    if _GROUP.fullmatch(token) is None:
        raise InvalidStopGroup("grupa: 2–32 litery cyfry _ -")
    return token


def require_stop_group_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidStopGroup("zlecenie musi być UUID")
    return raw


def require_stop_group_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidStopGroup("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidStopGroup("wskazanie zapisu grupy")
    if len(token) > _MAX_SOURCE:
        raise InvalidStopGroup("wskazanie zapisu grupy za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidStopGroup("obce wskazanie zapisu grupy")
    return token
