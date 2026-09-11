import re

from app.domain.errors import InvalidScheduleExceptionMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"delay", "cancel", "reroute", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://schedule-exception-mark/"
_REF_CAP = 256


def parse_schedule_exception_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidScheduleExceptionMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidScheduleExceptionMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidScheduleExceptionMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidScheduleExceptionMark(
            "rodzaj: delay, cancel, reroute albo other",
        )
    if type(origin) is not str:
        raise InvalidScheduleExceptionMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidScheduleExceptionMark("obce wskazanie zapisu znacznika schedule_exception")
    if len(pointer) > _REF_CAP:
        raise InvalidScheduleExceptionMark(
            "obce wskazanie zapisu znacznika schedule_exception za długie",
        )
    return slug, token, pointer
