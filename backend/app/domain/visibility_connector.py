import re

from app.domain.errors import InvalidVisibilityConnector

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_VENDORS = frozenset({"p44", "fourkites", "shippeo"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://visibility/"
_REF_CAP = 256


def parse_visibility_row(code: object, kind: object, origin: object) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidVisibilityConnector("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidVisibilityConnector("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidVisibilityConnector("system musi być tekstem")
    vendor = kind.strip().casefold()
    if vendor not in _VENDORS:
        raise InvalidVisibilityConnector("system: allowlista HITL")
    if type(origin) is not str:
        raise InvalidVisibilityConnector("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidVisibilityConnector("obce wskazanie zapisu konektora widoczności")
    if len(pointer) > _REF_CAP:
        raise InvalidVisibilityConnector("obce wskazanie zapisu konektora widoczności za długie")
    return slug, vendor, pointer
