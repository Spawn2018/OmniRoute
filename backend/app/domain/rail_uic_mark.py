import re

from app.domain.errors import InvalidRailUicMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_RAIL_KINDS = frozenset({"uic", "cim", "smgs", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://rail-uic-mark/"


def parse_rail_uic_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRailUicMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidRailUicMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRailUicMark("rodzaj kolejowy musi być tekstem")
    token = kind.strip().lower()
    if token not in _RAIL_KINDS:
        raise InvalidRailUicMark(
            "rodzaj kolejowy: uic, cim, smgs albo other",
        )
    if type(origin) is not str:
        raise InvalidRailUicMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidRailUicMark(
            "obce wskazanie zapisu znacznika UIC/CIM/SMGS",
        )
    if len(pointer) > 256:
        raise InvalidRailUicMark(
            "obce wskazanie zapisu znacznika UIC/CIM/SMGS za długie",
        )
    return slug, token, pointer
