import re

from app.domain.errors import InvalidInventoryPositionMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"position", "plant", "sku", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://inventory-position-mark/"
_REF_CAP = 256


def parse_inventory_position_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInventoryPositionMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInventoryPositionMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInventoryPositionMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInventoryPositionMark(
            "rodzaj: position, plant, sku albo other",
        )
    if type(origin) is not str:
        raise InvalidInventoryPositionMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInventoryPositionMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidInventoryPositionMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
