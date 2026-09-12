import re

from app.domain.errors import InvalidVdaOdetteMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"vda", "odette", "label", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://vda-odette-mark/"
_REF_CAP = 256


def parse_vda_odette_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidVdaOdetteMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidVdaOdetteMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidVdaOdetteMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidVdaOdetteMark(
            "rodzaj: vda, odette, label albo other",
        )
    if type(origin) is not str:
        raise InvalidVdaOdetteMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidVdaOdetteMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidVdaOdetteMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
