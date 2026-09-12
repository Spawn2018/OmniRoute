import re

from app.domain.errors import InvalidRailCimMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"uic", "cim", "smgs", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://rail-cim-mark/"


def parse_rail_cim_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRailCimMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidRailCimMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRailCimMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidRailCimMark("rodzaj: uic, cim, smgs albo other")
    if type(origin) is not str:
        raise InvalidRailCimMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidRailCimMark("obce wskazanie zapisu znacznika rail CIM")
    if len(pointer) > 256:
        raise InvalidRailCimMark("obce wskazanie zapisu znacznika rail CIM za długie")
    return slug, token, pointer
