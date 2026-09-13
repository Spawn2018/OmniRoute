import re

from app.domain.errors import InvalidShipperTenderMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"round", "bench", "spot", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://shipper-tender-mark/"
_REF_CAP = 256


def parse_shipper_tender_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipperTenderMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidShipperTenderMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidShipperTenderMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidShipperTenderMark("rodzaj: round, bench, spot albo other")
    if type(origin) is not str:
        raise InvalidShipperTenderMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidShipperTenderMark("obce wskazanie zapisu trybu")
    if len(pointer) > _REF_CAP:
        raise InvalidShipperTenderMark("obce wskazanie zapisu trybu za dlugie")
    return slug, token, pointer
