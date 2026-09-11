import re

from app.domain.errors import InvalidYardMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"yard_slot", "weigh", "eir", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://yard-mark/"
_REF_CAP = 256


def parse_yard_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidYardMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidYardMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidYardMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidYardMark(
            "rodzaj: yard_slot, weigh, eir albo other",
        )
    if type(origin) is not str:
        raise InvalidYardMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidYardMark("obce wskazanie zapisu znacznika yard")
    if len(pointer) > _REF_CAP:
        raise InvalidYardMark(
            "obce wskazanie zapisu znacznika yard za długie",
        )
    return slug, token, pointer
