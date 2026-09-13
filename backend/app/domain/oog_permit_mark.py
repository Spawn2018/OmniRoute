import re

from app.domain.errors import InvalidOogPermitMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"permit", "pilot", "route", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://oog-permit-mark/"
_REF_CAP = 256


def parse_oog_permit_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOogPermitMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidOogPermitMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidOogPermitMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidOogPermitMark("rodzaj: permit, pilot, route albo other")
    if type(origin) is not str:
        raise InvalidOogPermitMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidOogPermitMark("obce wskazanie zapisu zezwolenia OOG")
    if len(pointer) > _REF_CAP:
        raise InvalidOogPermitMark("obce wskazanie zapisu zezwolenia OOG za dlugie")
    return slug, token, pointer
