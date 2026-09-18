import re

from app.domain.errors import InvalidPostalEpoMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"register", "label", "track", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://postal-epo-mark/"
_REF_CAP = 256


def parse_postal_epo_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPostalEpoMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPostalEpoMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPostalEpoMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPostalEpoMark("EPO: register, label, track albo other")
    if type(origin) is not str:
        raise InvalidPostalEpoMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPostalEpoMark("obce wskazanie zapisu znacznika EPO")
    if len(pointer) > _REF_CAP:
        raise InvalidPostalEpoMark("obce wskazanie zapisu znacznika EPO za długie")
    return slug, token, pointer
