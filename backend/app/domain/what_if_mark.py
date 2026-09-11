import re

from app.domain.errors import InvalidWhatIfMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"fuel", "port", "bankruptcy", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://what-if-mark/"
_REF_CAP = 256


def parse_what_if_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidWhatIfMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidWhatIfMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidWhatIfMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidWhatIfMark(
            "rodzaj: fuel, port, bankruptcy albo other",
        )
    if type(origin) is not str:
        raise InvalidWhatIfMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidWhatIfMark("obce wskazanie zapisu znacznika what-if")
    if len(pointer) > _REF_CAP:
        raise InvalidWhatIfMark(
            "obce wskazanie zapisu znacznika what-if za długie",
        )
    return slug, token, pointer
