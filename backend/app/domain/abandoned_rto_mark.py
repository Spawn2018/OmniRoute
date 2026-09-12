import re

from app.domain.errors import InvalidAbandonedRtoMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"abandoned", "rto", "return", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://abandoned-rto-mark/"
_REF_CAP = 256


def parse_abandoned_rto_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidAbandonedRtoMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidAbandonedRtoMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidAbandonedRtoMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidAbandonedRtoMark(
            "rodzaj: abandoned, rto, return albo other",
        )
    if type(origin) is not str:
        raise InvalidAbandonedRtoMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidAbandonedRtoMark("obce wskazanie zapisu znacznika abandoned/RTO")
    if len(pointer) > _REF_CAP:
        raise InvalidAbandonedRtoMark(
            "obce wskazanie zapisu znacznika abandoned/RTO za długie",
        )
    return slug, token, pointer
