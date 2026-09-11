import re

from app.domain.errors import InvalidTimeToFixMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"open", "wip", "done", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://time-to-fix-mark/"
_REF_CAP = 256


def parse_time_to_fix_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTimeToFixMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTimeToFixMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTimeToFixMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidTimeToFixMark(
            "rodzaj: open, wip, done albo other",
        )
    if type(origin) is not str:
        raise InvalidTimeToFixMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidTimeToFixMark("obce wskazanie zapisu znacznika TIME-TO-FIX")
    if len(pointer) > _REF_CAP:
        raise InvalidTimeToFixMark(
            "obce wskazanie zapisu znacznika TIME-TO-FIX za długie",
        )
    return slug, token, pointer
