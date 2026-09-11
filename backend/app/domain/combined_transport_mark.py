import re

from app.domain.errors import InvalidCombinedTransportMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"combined", "mobility", "piggyback", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://combined-transport-mark/"
_REF_CAP = 256


def parse_combined_transport_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCombinedTransportMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCombinedTransportMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCombinedTransportMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCombinedTransportMark(
            "rodzaj: combined, mobility, piggyback albo other",
        )
    if type(origin) is not str:
        raise InvalidCombinedTransportMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCombinedTransportMark("obce wskazanie zapisu znacznika combined transport")
    if len(pointer) > _REF_CAP:
        raise InvalidCombinedTransportMark(
            "obce wskazanie zapisu znacznika combined transport za długie",
        )
    return slug, token, pointer
