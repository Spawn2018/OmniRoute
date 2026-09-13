import re

from app.domain.errors import InvalidLclConsoleMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"console", "cfs", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://lcl-console-mark/"
_REF_CAP = 256


def parse_lcl_console_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLclConsoleMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidLclConsoleMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLclConsoleMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLclConsoleMark("rodzaj: console, cfs albo other")
    if type(origin) is not str:
        raise InvalidLclConsoleMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidLclConsoleMark("obce wskazanie zapisu konsoli LCL")
    if len(pointer) > _REF_CAP:
        raise InvalidLclConsoleMark("obce wskazanie zapisu konsoli LCL za dlugie")
    return slug, token, pointer
