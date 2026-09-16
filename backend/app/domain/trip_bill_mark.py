import re

from app.domain.errors import InvalidTripBillMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ready", "held", "billed", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://trip-bill-mark/"
_REF_CAP = 256


def parse_trip_bill_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTripBillMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTripBillMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTripBillMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidTripBillMark(
            "rodzaj: ready, held, billed albo other",
        )
    if type(origin) is not str:
        raise InvalidTripBillMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidTripBillMark(
            "obce wskazanie zapisu gotowości przejazdu do FV",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidTripBillMark(
            "obce wskazanie zapisu gotowości przejazdu do FV za długie",
        )
    return slug, token, pointer
