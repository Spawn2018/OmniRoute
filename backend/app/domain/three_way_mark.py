import re

from app.domain.errors import InvalidThreeWayMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_WAY_KINDS = frozenset({"buyer", "seller", "carrier", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://three-way-mark/"


def parse_three_way_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidThreeWayMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidThreeWayMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidThreeWayMark("rodzaj 3-way musi być tekstem")
    token = kind.strip().lower()
    if token not in _WAY_KINDS:
        raise InvalidThreeWayMark(
            "rodzaj 3-way: buyer, seller, carrier albo other",
        )
    if type(origin) is not str:
        raise InvalidThreeWayMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidThreeWayMark(
            "obce wskazanie zapisu znacznika 3-way",
        )
    if len(pointer) > 256:
        raise InvalidThreeWayMark(
            "obce wskazanie zapisu znacznika 3-way za długie",
        )
    return slug, token, pointer
