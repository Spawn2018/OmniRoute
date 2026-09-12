import re

from app.domain.errors import InvalidMqcMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"mqc", "actual", "gap", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://mqc-mark/"
_REF_CAP = 256


def parse_mqc_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidMqcMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidMqcMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidMqcMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidMqcMark(
            "rodzaj: mqc, actual, gap albo other",
        )
    if type(origin) is not str:
        raise InvalidMqcMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidMqcMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidMqcMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
