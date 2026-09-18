import re

from app.domain.errors import InvalidBlankSailingMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"blank", "congestion", "gate", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://blank-sailing-mark/"
_REF_CAP = 256


def parse_blank_sailing_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidBlankSailingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidBlankSailingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidBlankSailingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidBlankSailingMark(
            "rodzaj: blank, congestion, gate albo other",
        )
    if type(origin) is not str:
        raise InvalidBlankSailingMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidBlankSailingMark(
            "obce wskazanie zapisu znacznika blank sailing",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidBlankSailingMark(
            "obce wskazanie zapisu znacznika blank sailing za długie",
        )
    return slug, token, pointer
