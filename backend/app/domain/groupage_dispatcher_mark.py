import re

from app.domain.errors import InvalidGroupageDispatcherMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"line", "hub", "cutoff", "consol", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://groupage-dispatcher-mark/"
_REF_CAP = 256


def parse_groupage_dispatcher_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidGroupageDispatcherMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidGroupageDispatcherMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidGroupageDispatcherMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidGroupageDispatcherMark("rodzaj: line, hub, cutoff, consol albo other")
    if type(origin) is not str:
        raise InvalidGroupageDispatcherMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidGroupageDispatcherMark("obce wskazanie zapisu dyspozytora")
    if len(pointer) > _REF_CAP:
        raise InvalidGroupageDispatcherMark("obce wskazanie zapisu dyspozytora za dlugie")
    return slug, token, pointer
