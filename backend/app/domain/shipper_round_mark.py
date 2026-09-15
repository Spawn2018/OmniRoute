import re

from app.domain.errors import InvalidShipperRoundMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"first", "second", "final", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://shipper-round-mark/"
_REF_CAP = 256


def parse_shipper_round_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipperRoundMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidShipperRoundMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidShipperRoundMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidShipperRoundMark("rodzaj: first, second, final albo other")
    if type(origin) is not str:
        raise InvalidShipperRoundMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidShipperRoundMark("obce wskazanie zapisu rundy")
    if len(pointer) > _REF_CAP:
        raise InvalidShipperRoundMark("obce wskazanie zapisu rundy za dlugie")
    return slug, token, pointer
