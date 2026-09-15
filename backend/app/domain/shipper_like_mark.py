import re

from app.domain.errors import InvalidShipperLikeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"match", "gap", "bench", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://shipper-like-mark/"
_REF_CAP = 256


def parse_shipper_like_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipperLikeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidShipperLikeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidShipperLikeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidShipperLikeMark("rodzaj: match, gap, bench albo other")
    if type(origin) is not str:
        raise InvalidShipperLikeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidShipperLikeMark("obce wskazanie zapisu stance")
    if len(pointer) > _REF_CAP:
        raise InvalidShipperLikeMark("obce wskazanie zapisu stance za dlugie")
    return slug, token, pointer
