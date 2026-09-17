import re

from app.domain.errors import InvalidPostalDispatchMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"en", "uss", "epo", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://postal-dispatch-mark/"
_REF_CAP = 256


def parse_postal_dispatch_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPostalDispatchMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPostalDispatchMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPostalDispatchMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPostalDispatchMark(
            "rodzaj: en, uss, epo albo other",
        )
    if type(origin) is not str:
        raise InvalidPostalDispatchMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPostalDispatchMark("obce wskazanie zapisu znacznika ksiazki PP")
    if len(pointer) > _REF_CAP:
        raise InvalidPostalDispatchMark(
            "obce wskazanie zapisu znacznika ksiazki PP za długie",
        )
    return slug, token, pointer
