import re

from app.domain.errors import InvalidEccnMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"eccn", "ear", "license", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://eccn-mark/"
_REF_CAP = 256


def parse_eccn_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidEccnMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidEccnMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidEccnMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidEccnMark(
            "rodzaj: eccn, ear, license albo other",
        )
    if type(origin) is not str:
        raise InvalidEccnMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidEccnMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidEccnMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
