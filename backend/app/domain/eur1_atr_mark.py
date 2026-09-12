import re

from app.domain.errors import InvalidEur1AtrMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"eur1", "atr", "origin", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://eur1-atr-mark/"
_REF_CAP = 256


def parse_eur1_atr_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidEur1AtrMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidEur1AtrMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidEur1AtrMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidEur1AtrMark(
            "rodzaj: eur1, atr, origin albo other",
        )
    if type(origin) is not str:
        raise InvalidEur1AtrMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidEur1AtrMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidEur1AtrMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
