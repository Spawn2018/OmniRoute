import re

from app.domain.errors import InvalidPenaltyMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"otif", "delay", "damage", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://penalty-mark/"
_REF_CAP = 256


def parse_penalty_mark_row(code: object, kind: object, origin: object) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPenaltyMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPenaltyMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPenaltyMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPenaltyMark("rodzaj: otif, delay, damage albo other")
    if type(origin) is not str:
        raise InvalidPenaltyMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPenaltyMark("obce wskazanie zapisu znacznika kary")
    if len(pointer) > _REF_CAP:
        raise InvalidPenaltyMark("obce wskazanie zapisu znacznika kary za długie")
    return slug, token, pointer
