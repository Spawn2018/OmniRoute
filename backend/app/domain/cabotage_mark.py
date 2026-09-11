import re

from app.domain.errors import InvalidCabotageMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"counter", "driver_return", "vehicle_return", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://cabotage-mark/"
_REF_CAP = 256


def parse_cabotage_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCabotageMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCabotageMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCabotageMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCabotageMark(
            "rodzaj: counter, driver_return, vehicle_return albo other",
        )
    if type(origin) is not str:
        raise InvalidCabotageMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCabotageMark("obce wskazanie zapisu znacznika cabotage")
    if len(pointer) > _REF_CAP:
        raise InvalidCabotageMark(
            "obce wskazanie zapisu znacznika cabotage za długie",
        )
    return slug, token, pointer
