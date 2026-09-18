import re

from app.domain.errors import InvalidWasteMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"bdo", "kpo", "wsr", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://waste-mark/"
_REF_CAP = 256


def parse_waste_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidWasteMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidWasteMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidWasteMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidWasteMark("rodzaj: bdo, kpo, wsr albo other")
    if type(origin) is not str:
        raise InvalidWasteMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidWasteMark("obce wskazanie zapisu znacznika odpadów")
    if len(pointer) > _REF_CAP:
        raise InvalidWasteMark("obce wskazanie zapisu znacznika odpadów za długie")
    return slug, token, pointer
