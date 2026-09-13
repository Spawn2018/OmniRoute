import re

from app.domain.errors import InvalidLoadOrderMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"sequence", "stack", "door", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://load-order-mark/"
_REF_CAP = 256


def parse_load_order_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLoadOrderMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidLoadOrderMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLoadOrderMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLoadOrderMark("rodzaj: sequence, stack, door albo other")
    if type(origin) is not str:
        raise InvalidLoadOrderMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidLoadOrderMark("obce wskazanie zapisu kolejności")
    if len(pointer) > _REF_CAP:
        raise InvalidLoadOrderMark("obce wskazanie zapisu kolejności za dlugie")
    return slug, token, pointer
