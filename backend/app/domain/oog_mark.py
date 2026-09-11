import re

from app.domain.errors import InvalidOogMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"oog", "lashing", "escort", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://oog-mark/"
_REF_CAP = 256


def parse_oog_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOogMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidOogMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidOogMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidOogMark(
            "rodzaj: oog, lashing, escort albo other",
        )
    if type(origin) is not str:
        raise InvalidOogMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidOogMark("obce wskazanie zapisu znacznika OOG")
    if len(pointer) > _REF_CAP:
        raise InvalidOogMark("obce wskazanie zapisu znacznika OOG za długie")
    return slug, token, pointer
